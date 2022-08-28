import collections
import json
import os
import re
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
    for problem, result in results:
        current[problem] = not result
    with open(RESULTS_FILE, "w") as w:
        json.dump(current, w)


class CLI:
    def problem(self, pattern):
        matched = match_pattern("", "md", pattern, PROBLEM_DIR)
        with open(matched) as p:
            console.print(Markdown(p.read()))

    def solve(self, pattern):
        matched = match_pattern("", "md", pattern, PROBLEM_DIR)
        new_solution = Path(SOLUTION_DIR / f"{matched.stem}.py")
        if new_solution.exists():
            error("A solution file for this problem already exists!")
            exit(1)
        with open(new_solution, "w") as w:
            w.write(f"def {pattern}():\n    pass")

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

    def create(self, name):
        TEST_TEMPLATE = """\n
        from tony_tests.tests.utils import import_solution

        {problem} = import_solution("{problem}")


        def test_{problem}():
            assert False, "no test yet!"

        """
        is_problem = re.compile(r"\d{2}_.+\.md")
        next_number = f'{len([f for f in os.listdir(PROBLEM_DIR) if re.match(is_problem, f)]) + 1:02d}'
        problem_file = Path(PROBLEM_DIR / f"{next_number}_{name}.md")
        test_file = Path(TEST_DIR / f"test_{next_number}_{name}.py")
        if problem_file.exists():
            error(f"{problem_file} exists; skipping")
        else:
            with open(problem_file, 'w'):
                pass
        if test_file.exists():
            error(f"{test_file} exists; skipping")
        else:
            with open(test_file, 'w') as w:
                w.write(TEST_TEMPLATE.format(problem=name))


def main():
    fire.Fire(CLI)
