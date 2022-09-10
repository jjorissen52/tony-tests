import os
import re
from pathlib import Path

import fire
import pytest

from tony_tests.settings import TEST_DIR, PROBLEM_DIR, RESULTS_FILE, CACHE_FILE, CONFIG_FILE
from tony_tests.utils import error, match_pattern, import_string


class CLI:
    def test(self):
        pytest.main([str(TEST_DIR)])

    def create(self, name):
        TEST_TEMPLATE = """\
from tony_tests.tests.utils import import_solution

{problem} = import_solution("{problem}")


def test_{problem}():
    assert False, "no test yet!"

"""
        is_problem = re.compile(r"\d{2}_.+\.md")
        number = f'{len([f for f in os.listdir(PROBLEM_DIR) if re.match(is_problem, f)]) + 1:02d}'
        existing_match = match_pattern("", "md", name, PROBLEM_DIR, False) or \
            match_pattern("test_", "py", name, TEST_DIR, False)
        if existing_match:
            number = re.search(r"([0-9]+)", existing_match.stem).groups()[0]
        problem_file = Path(PROBLEM_DIR / f"{number}_{name}.md")
        test_file = Path(TEST_DIR / f"test_{number}_{name}.py")
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

    def rm(self, results=False, cache=False, config=False):
        if not (results or cache or config):
            error("Must include at least one to remove.")
        results and os.remove(RESULTS_FILE)
        cache and os.remove(CACHE_FILE)
        config and os.remove(CONFIG_FILE)

    def run(self, obj, arg):
        return import_string(obj)(arg)


def main():
    fire.Fire(CLI)
