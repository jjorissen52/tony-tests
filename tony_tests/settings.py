import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "tests"
PROBLEM_DIR = BASE_DIR / "problems"
RESULTS_FILE = Path(os.environ["HOME"]) / ".config" / "tony_tests" / "results.json"
