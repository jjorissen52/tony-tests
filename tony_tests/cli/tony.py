import collections
import datetime
import json
import os
import queue
import time
import runpy
from threading import Thread
from typing import List
from importlib import metadata

import fire
import pytest
import toml

from pathlib import Path

import requests
from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.table import Table

from tony_tests.settings import TEST_DIR, PROBLEM_DIR, FIXTURE_DIR, RESULTS_FILE, BASE_DIR, REMOTE_PYPROJECT, \
    CACHE_FILE, SOLUTIONS_DIR
from tony_tests.utils import match_pattern, console, error, load_solution_template

result_tup = collections.namedtuple("result", "problem,result")


def store_results(results: List[result_tup]):
    current = {}
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, "r") as r:
            current = json.load(r)
    else:
        os.makedirs(RESULTS_FILE.parent, exist_ok=True)
    for problem, correct in results:
        if not correct:
            current[problem] = dict(correct=False)
        elif not current.get(problem, {}).get('correct'):
            current[problem] = dict(correct=True, solved=time.time())
    with open(RESULTS_FILE, "w") as w:
        json.dump(current, w)


class CLI:
    """
    CLI for interacting with the problem set. Most of these commands accept a single "pattern" to describe
    which problem you are interacting with. E.g., patterns corresponding to fizzbuzz would be 01 or fizzbuzz.
    """
    def problem(self, pattern=None):
        """
        Display the instructions of the indicated problem. If no pattern is provided,
        the instructions of the next pattern in the list will be displayed.
        """
        problem = None
        if pattern:
            problem = match_pattern("", "md", pattern, PROBLEM_DIR)
        else:
            results = {}
            if RESULTS_FILE.exists():
                with open(RESULTS_FILE, "r") as r:
                    results = json.load(r)
            for file in sorted(os.listdir(PROBLEM_DIR)):
                if os.path.isfile(PROBLEM_DIR / file):
                    path = Path(PROBLEM_DIR / file)
                    if not results.get(path.stem, {}).get('correct', False):
                        problem = path
                        break
        if not problem:
            return console.print("[cyan]What??? You've done everything already!! 🎉 🎉 🎉")

        with open(problem) as p:
            console.print(Markdown(f"# {problem.stem}"))
            console.print(Markdown(p.read()))
            console.print(Markdown(f"# {problem.stem}"))

    def start(self, pattern):
        """
        Creates a new empty solution file for the indicated problem.
        """
        matched = match_pattern("", "md", pattern, PROBLEM_DIR)
        new_solution = Path(SOLUTIONS_DIR / f"{matched.stem}.py")
        if new_solution.exists():
            error("A solution file for this problem already exists!")
            exit(1)
        os.makedirs(SOLUTIONS_DIR, exist_ok=True)
        with open(new_solution, "w") as w:
            w.write(load_solution_template(matched.stem, name=new_solution.stem[3:]))

    def run(self, pattern):
        """
        Run your solution as a script.
        """
        matched = match_pattern("", "py", pattern, SOLUTIONS_DIR)
        runpy.run_path(matched, run_name='__main__')

    def submit(self, pattern):
        """
        Submits your solution and checks it against the tests.
        """
        matched = match_pattern("test_", "py", pattern, TEST_DIR)
        result = not int(pytest.main(["-s", str(matched)]))
        store_results([(matched.stem.replace("test_", ""), result)])
        result and self.results()

    def fixtures(self, pattern):
        """
        Lists any fixtures (files) related to the indicated problem.
        """
        matched = match_pattern("", "", pattern, FIXTURE_DIR, predicate=os.path.isdir)
        files = sorted([matched / f for f in os.listdir(matched) if os.path.isfile(matched / f)])
        table = Table()
        table.add_column("Name", style="cyan")
        table.add_column("Path", justify="right", style="purple")
        for file in files:
            table.add_row(file.name, str(file))
        console.print(table)

    def results(self):
        """
        Shows the results of all the solutions you've submitted so far.
        """
        results = {}
        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, "r") as r:
                results = json.load(r)
        table = Table()
        table.add_column("Status", justify="center")
        table.add_column("Problem", justify="left", style="cyan")
        table.add_column("Solved", justify="right", style="purple")
        for file in sorted(os.listdir(PROBLEM_DIR)):
            if os.path.isfile(PROBLEM_DIR / file):
                problem = Path(file).stem
                indicator = "[ ]"
                result = results.get(problem, {}).get('correct')
                solved = results.get(problem, {}).get('solved', 0)
                if result is not None:
                    indicator = "[green]:heavy_check_mark:" if result else "[red]✗"
                table.add_row(
                    indicator, problem, datetime.datetime.fromtimestamp(solved).strftime("%c") if solved else "-"
                )
        console.print(table)

    def update(self):
        """
        Install the latest update
        """
        runpy.run_path(BASE_DIR / "cli" / "update.py", run_name='__main__')


def main():
    q = queue.Queue(maxsize=1)

    def check_remote_version():
        start = time.time()

        def get_cached():
            payload = None
            if os.path.exists(CACHE_FILE):
                try:
                    with open(CACHE_FILE) as r:
                        cached = json.load(r)
                    exp = cached.get("exp", 0)
                    if exp > start:
                        payload = cached["payload"]
                except:  # noqa
                    os.remove(CACHE_FILE)
            if payload:
                return payload
            payload = requests.get(REMOTE_PYPROJECT).text
            with open(CACHE_FILE, "w") as w:
                json.dump(dict(
                    exp=start + 3600,  # expire in an hour
                    payload=payload
                ), w)
            return payload

        try:
            q.put(toml.loads(get_cached())["tool"]["poetry"]["version"])
        except:  # noqa
            q.put(None)

    Thread(target=check_remote_version, daemon=True).start()
    fire.Fire(CLI)
    if remote_version := q.get(timeout=1):
        local_version = metadata.metadata('tony-tests')['Version']
        if remote_version != local_version:
            if Confirm.ask(
                f"[purple]({local_version}) [cyan]Looks like tony-tests {remote_version} is available! Would you like to install it?",
                default="y"
            ):
                runpy.run_path(BASE_DIR / "cli" / "update.py", run_name='__main__')
                if os.path.exists(CACHE_FILE):
                    os.remove(CACHE_FILE)
