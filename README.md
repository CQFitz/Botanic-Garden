# Botanic-Garden

## ToDo
- Better guide
- Better comment

## Set Up Development
This project uses python 3.8.
This guide assumes you are using linux, and good with command line.

### Set Up Pyenv
- Install dependencies from this link https://github.com/pyenv/pyenv/wiki/Common-build-problems
- Install `pyenv`
- Install `pyenv-virtualenv`
- Install python 3.8.7 with `pyenv` and create virtual project for this project:
    - `pyenv install 3.8.7`
    - `pyenv virtualenv 3.8.7 botanic-garden`
    - `pyenv activate botanic-garden`
- Install dependencies with `pip install -r requirements.txt`
- Set `$ export FLASK_CONFIG='development'` for working in development


### Set Up Database
After activate the virtual project
Run`$ python db_create.py` for creating the database and insert some example data
