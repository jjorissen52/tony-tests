import collections
import datetime
import json
import os
import time
import runpy
from typing import List

import fire
import pytest

from pathlib import Path
from rich.markdown import Markdown
from rich.table import Table

from tony_tests.settings import TEST_DIR, PROBLEM_DIR, RESULTS_FILE
from tony_tests.tests.utils import SOLUTION_DIR
from tony_tests.utils import match_pattern, console, error

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


SOLUTION_TEMPLATE = """\
def {name}():
    return "Hello World!"


if __name__ == '__main__':
    print({name}())
"""


class CLI:
    def problem(self, pattern=None):
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

        with open(problem) as p:
            console.print(Markdown(p.read()))

    def start(self, pattern):
        matched = match_pattern("", "md", pattern, PROBLEM_DIR)
        new_solution = Path(SOLUTION_DIR / f"{matched.stem}.py")
        if new_solution.exists():
            error("A solution file for this problem already exists!")
            exit(1)
        with open(new_solution, "w") as w:
            w.write(SOLUTION_TEMPLATE.format(name=new_solution.stem[3:]))

    def run(self, pattern):
        matched = match_pattern("", "py", pattern, SOLUTION_DIR)
        runpy.run_path(matched, run_name='__main__')

    def submit(self, pattern):
        matched = match_pattern("test_", "py", pattern, TEST_DIR)
        result = not int(pytest.main([str(matched)]))
        store_results([(matched.stem.replace("test_", ""), result)])
        result and self.results()

    def results(self):
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


def main():
    fire.Fire(CLI)
