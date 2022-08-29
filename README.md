# Getting Started
1. Change into the directory that contains your python projects and clone this project with `git clone git@github.com:jjorissen52/tony-tests.git`
2. Change into the project directory with `cd tony-tests`
3. Create a virtual environment with `python3 -m venv venv`
4. Activate the environment with `source ./venv/bin/activate`
5. Install the project and its dependencies by running `poetry install`
6. Verify that the installation works as expected by running `tony --help`

# Using the CLI
This project provides a CLI interface to make it easy for you to interact with the problems and tests.
```bash
# to discover CLI commands
tony
# to show help for a command use
# tony <command> --help
# e.g.
tony problem --help


### Examples
```bash
# show the next problem
tony problem

# start a new solution file
tony start 01
tony start fizzbuzz

# run your solution file
tony run 01
tony run fizzbuzz

# submit your solution
tony submit 01

# show the results of your submissions so far
tony results
```
