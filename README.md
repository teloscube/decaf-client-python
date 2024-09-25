# DECAF API Client (Python)

[![Test](https://github.com/teloscube/decaf-client-python/actions/workflows/test.yml/badge.svg)](https://github.com/teloscube/decaf-client-python/actions/workflows/test.yml)

> **TODO:** Provide a complete README file.

## Development

A Nix shell is provided for development:

```sh
nix develop
```

Build to run tests:

```sh
nix build
```

## Build and Publish

Build the source distribution:

```sh
python -m build --sdist --wheel
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

This software is licensed under [The 3-Clause BSD License].

<!-- REFERENCES -->

[The 3-Clause BSD License]: https://opensource.org/licenses/BSD-3-Clause
