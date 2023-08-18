### Status badges:
[![Actions Status](https://github.com/SHArtyom/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/SHArtyom/python-project-52/actions)
[![lint_check](https://github.com/SHArtyom/python-project-52/actions/workflows/lint_check.yml/badge.svg)](https://github.com/SHArtyom/python-project-52/actions/workflows/lint_check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/fede384f0b607f81c238/maintainability)](https://codeclimate.com/github/SHArtyom/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fede384f0b607f81c238/test_coverage)](https://codeclimate.com/github/SHArtyom/python-project-52/test_coverage)
# Task manager
___
This web-application is a simple task manager built on Django 4.2.3 framework.
You can arrange tasks, select executors and change statuses for the tasks.
## Check out local
___
 ```
 git clone https://github.com/SHArtyom/python-project-52.git
 cd python-project-52
 pip install poetry
 make build
 make start 
 ```
Ensure you add an .env file to your root directory, which includes SECRET_KEY variable with its value:

```SECRET_KEY = 'this_is_an_example_of_secret_key_variable_value'```
## Requirements
Python 3.9