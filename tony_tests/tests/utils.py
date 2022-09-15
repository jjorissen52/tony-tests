import os.path
import sys

from tony_tests.settings import SOLUTIONS_DIR
from tony_tests.utils import error, import_string, match_pattern


def import_solution(problem_name, sub_path=""):
    sys.path.insert(0, os.path.abspath(SOLUTIONS_DIR))
    module_match = match_pattern("", "py", problem_name, SOLUTIONS_DIR)
    full_obj_name = f"{module_match.stem}.{problem_name if not sub_path else sub_path}"
    try:
        return import_string(full_obj_name)
    except: # noqa
        error(f"Unable to import {full_obj_name}. Are you sure the name is right?")
        exit(1)
