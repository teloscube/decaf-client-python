{ ... }:

let
  ## Import Nix packages:
  pkgs = import (import ./nix/sources.nix).nixpkgs { };

  ## Define Python packages:
  python-packages = p: with p; [
    ## Production dependencies:
    pydantic
    requests
    typing-extensions

    ## Development and testing dependencies:
    black
    flake8
    ipython
    isort
    mypy
    pytest
    tox
    twine
    types-requests
    wheel
  ];

  ## Get a Python with our dependencies:
  this-python = pkgs.python3.withPackages python-packages;
in
pkgs.mkShell {
  packages = [
    this-python
  ];
}
