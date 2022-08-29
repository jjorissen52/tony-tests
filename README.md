### Getting Started
1. Change into the directory that contains your python projects and clone this project with `git clone git@github.com:jjorissen52/tony-tests.git`
2. Create a virtual environment with `python3 -m venv venv`
3. Activate the environment with `source ./venv/bin/activate`
4. Install the project and its dependencies by running `poetry install`
5. Verify that the installation works as expected by running `tony --help`

### Using the CLI
This project provides a CLI interface to make it easy for you to interact with the problems and tests. To discover
CLI commands, simply run
```bash
# to discover CLI commands
tony
# to show help for a command use
# tony <command> --help
# e.g.
tony problem --help
```
