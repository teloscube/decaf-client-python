# DECAF API Client (Python)

[![Github](https://github.com/telostat/decaf-api-client-python/workflows/Install%20and%20Test/badge.svg)](https://github.com/telostat/decaf-api-client-python/actions)

> **TODO:** Provide a complete README file.

## Development

A Nix shell is provided for development:

```sh
nix-shell
```

Run tests:

```sh
tox
```

Open the codebase in Visual Studio Code:

```sh
code .
```

Alternatively, you can issue following commands directly without entering the
Nix shell:

```sh
nix-shell --arg python "\"python39\"" --run tox
nix-shell --arg python "\"python310\"" --run tox
```

## Build and Publish

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
