import os
from importlib import util

from rich.console import Console
console = Console()


def main():
    if util.find_spec("poetry"):
        os.system("poetry update tony-tests")
    else:
        console.print("[red]Sorry, I don't know how to update if you aren't using "
                      "poetry as a dependency manager.")
        exit(1)


if __name__ == "__main__":
    main()
