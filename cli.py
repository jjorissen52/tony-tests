import collections
import json
import os
from typing import List

import fire
import pytest

from pathlib import Path
from rich.markdown import Markdown
from rich.table import Table

from tony_tests.utils import match_pattern, console, error

BASE_DIR = Path(__file__).parent / "tony_tests"
TEST_DIR = BASE_DIR / "tests"
PROBLEM_DIR = BASE_DIR / "problems"
RESULTS_FILE = Path(os.environ["HOME"]) / ".config" / "tony_tests" / "results.json"

result_tup = collections.namedtuple("result", "problem,result")


def store_results(results: List[result_tup]):
    current = {}
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, "r") as r:
            current = json.load(r)
    else:
        os.makedirs(RESULTS_FILE.parent, exist_ok=True)
    for problem, result in results:
        current[problem] = not result
    with open(RESULTS_FILE, "w") as w:
        json.dump(current, w)

class CLI:
    def problem(self, pattern):
        matched = match_pattern("", "md", pattern, PROBLEM_DIR)
        with open(matched) as p:
            console.print(Markdown(p.read()))

    def submit(self, pattern):
        matched = match_pattern("test_", "py", pattern, TEST_DIR)
        result = pytest.main([str(matched)])
        return store_results([(matched.stem.replace("test_", ""), result)])

    def results(self):
        if not RESULTS_FILE.exists():
            error(f"Results file {RESULTS_FILE} does not exist yet. Have you submitted results?")
            exit(1)
        with open(RESULTS_FILE, "r") as r:
            results = json.load(r)
        table = Table(title="Submission Results")
        table.add_column("Status", justify="center")
        table.add_column("Problem", justify="right", style="cyan")
        print(results)
        for file in os.listdir(PROBLEM_DIR):
            if os.path.isfile(PROBLEM_DIR / file):
                problem = Path(file).stem
                indicator = "[ ]"
                result = results.get(problem)
                if result is not None:
                    indicator = "[green]:heavy_check_mark:" if results.get(problem) else "[red]✗"
                table.add_row(indicator, problem)
        console.print(table)

    def test(self):
        pytest.main([str(TEST_DIR)])


def main():
    fire.Fire(CLI)
