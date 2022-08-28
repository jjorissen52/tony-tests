from pathlib import Path

from tony_tests.utils import error, import_string, match_pattern

SOLUTION_DIR = Path(__file__).parent.parent / "solutions"


def import_solution(obj):
    module_match = match_pattern("", "py", obj, SOLUTION_DIR)
    full_obj_name = f"tony_tests.solutions.{module_match.stem}.{obj}"
    try:
        return import_string(full_obj_name)
    except: # noqa
        error(f"Unable to import {full_obj_name}. Are you sure the name is right?")
        exit(1)
