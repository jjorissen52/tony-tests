import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "tests"
PROBLEM_DIR = BASE_DIR / "problems"
FIXTURES_DIR = BASE_DIR / "fixtures"
RESULTS_FILE = Path(os.environ["HOME"]) / ".config" / "tony_tests" / "results.json"
CACHE_FILE = RESULTS_FILE.parent / "cache"
REMOTE_PYPROJECT = "https://raw.githubusercontent.com/jjorissen52/tony-tests/master/pyproject.toml"
