import importlib
import os
import re
import sys
from pathlib import Path

from rich.console import Console

console = Console()


def error(*args, **kwargs):
    console.print(*args, style="red", **kwargs)


def match_pattern(prefix, suffix, pattern, dir):
    all_files = [f for f in os.listdir(dir)
                 if os.path.isfile(dir / f)]
    full_match = re.compile(f"{pattern}")
    stem_match = re.compile(rf"{prefix}.*{pattern}.*\.{suffix}")
    removed_stem_match = re.compile(rf"{prefix}.*{Path(pattern).stem}.*\.{suffix}")
    name_match = re.compile(rf"{prefix}\d+_.*{pattern}.*\.{suffix}")
    number_match = re.compile(rf"{prefix}{pattern}_.+\.{suffix}")

    for matcher in [number_match, name_match, stem_match, full_match, removed_stem_match]:
        matches = [f for f in all_files if matcher.match(f)]
        if len(matches) > 1:
            error(f"More than one match for pattern {pattern}:")
            error(f"{[dir / m for m in matches]}")
            exit(1)
        if matches:
            return dir / matches[0]
    console.print(f"No matches for pattern {pattern}")
    exit(1)


# Everything below was ripped shamelessly from
# https://github.com/django/django/blob/0dd29209091280ccf34e07c9468746c396b7778e/django/utils/module_loading.py

def cached_import(module_path, class_name):
    # Check whether module is loaded and fully initialized.
    if not (
        (module := sys.modules.get(module_path))
        and (spec := getattr(module, "__spec__", None))
        and getattr(spec, "_initializing", False) is False
    ):
        module = importlib.import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err
