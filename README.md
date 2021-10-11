# DECAF API Client (Python)

[![Github](https://github.com/telostat/decaf-api-client-python/workflows/Install%20and%20Test/badge.svg)](https://github.com/telostat/decaf-api-client-python/actions)

> **TODO:** Provide a complete README file.

## Development

Create a virtual environment, if you did not create one before:

```sh
python3.9 -m venv /opt/venvs/decaf-client-python
```

### Start Development

Activate the virtual environment:

```sh
. /opt/venvs/decaf-client-python/bin/activate
```

Upgrade `pip` and `setuptools`:

```sh
pip install --upgrade pip setuptools
```

Install `pipenv`:

```sh
pip install pipenv
```

Install production and development dependencies:

```sh
pipenv install --dev
```

Run tests:

```sh
pipenv run tox
```

Open the codebase in VSCode:

```sh
code .
```

## Build and Publish

Install/upgrade `twine`:

```sh
pip install --upgrade twine
```

Build the source distribution:

```sh
python setup.py sdist bdist_wheel
```

Check the distribution(s):

```sh
twine check dist/*
```

Upload the distribution:

```sh
twine upload -s dist/*
```

## License and Copyrights

This software is licensed under [The 3-Clause BSD
License](https://opensource.org/licenses/BSD-3-Clause).
