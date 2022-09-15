import json
import os
import logging
import sys
from pathlib import Path

from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console(file=sys.stderr)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "tests"
PROBLEM_DIR = BASE_DIR / "problems"
FIXTURE_DIR = BASE_DIR / "fixtures"
TEMPLATE_DIR = BASE_DIR / "templates"
CONFIG_DIR = Path(os.environ["HOME"]) / ".config" / "tony_tests"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    REMOTE_PYPROJECT: str = "https:\/\/raw.githubusercontent.com/jjorissen52/tony-tests/master/pyproject.toml"
    RESULTS_FILE: Path = CONFIG_DIR / "results.json"
    CACHE_FILE: Path = CONFIG_DIR / "cache"
    SOLUTIONS_DIR: Path = None


def check_file(file):
    if os.path.exists(file):
        if not file.is_file():
            console.print(f"[red]Config file {file} is not a file. Please remove it and try again.")
            exit(1)
        return True


def init_config() -> Config:
    try:
        if check_file(CONFIG_FILE):
            with open(CONFIG_FILE) as r:
                return Config(**json.load(r))
    except Exception:  # noqa
        logger.exception("Failed to load config file.")
        if Confirm.ask(f"[red]Unable to load contents of config file {CONFIG_FILE}. Would you like to delete it?"):
            os.remove(CONFIG_FILE)
    return Config()


def set_config(config: Config):
    try:
        check_file(CONFIG_FILE)
        with open(CONFIG_FILE, "w") as w:
            logger.debug("Saving config file.")
            json.dump(config, w, indent=4, default=pydantic_encoder)
    except Exception:  # noqa
        logger.exception("Failed to save config file.")


def get_solutions_dir(config: Config):
    solutions_dir = config.SOLUTIONS_DIR
    while not solutions_dir:
        proposed_dir = os.path.abspath(Prompt.ask(
            "[cyan]There is currently no solutions directory configured for your project. "
            "Where would you like to store your solutions?", default="."
        ))
        if Confirm.ask(f"[cyan]SOLUTIONS_DIR={proposed_dir}", default="y"):
            solutions_dir = proposed_dir
            break
    return Path(solutions_dir)


CONFIG = init_config()

SOLUTIONS_DIR = get_solutions_dir(CONFIG)
if SOLUTIONS_DIR != CONFIG.SOLUTIONS_DIR:
    CONFIG.SOLUTIONS_DIR = SOLUTIONS_DIR
    set_config(CONFIG)
RESULTS_FILE = Path(CONFIG.RESULTS_FILE)
CACHE_FILE = Path(CONFIG.CACHE_FILE)
REMOTE_PYPROJECT = CONFIG.REMOTE_PYPROJECT
