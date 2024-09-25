{
  description = "Flake to develop, test, build and publish DECAF API Client for Python.";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/release-24.05";
  inputs.pyproject-nix.url = "github:nix-community/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs = { nixpkgs, pyproject-nix, ... }:
    let
      inherit (nixpkgs) lib;

      ## Use x86_64-linux for simplicity:
      pkgs = nixpkgs.legacyPackages.x86_64-linux;

      ## Load pyproject.toml:
      project = pyproject-nix.lib.project.loadPyproject {
        ## Read and unmarshal pyproject.toml relative to this flake (project root):
        projectRoot = ./.;
      };

      ## Use default nixpkgs Python3 interpreter and package set but override pydantic:
      python = pkgs.python3.override {
        packageOverrides = self: super: {
          pydantic = super.pydantic_1;
        };
      };

      ## Get the library version:
      version = builtins.head (builtins.match ''.*__version__[ ]*=[ ]*"(.*)".*'' (builtins.readFile ./decaf/api/client/__init__.py));
    in
    {
      ## Create default development shell containing dependencies from pyproject.toml:
      devShells.x86_64-linux.default =
        let
          arg = project.renderers.withPackages {
            inherit python;
            extras = [ "test" "dev" ];
          };
          pythonEnv = python.withPackages arg;
        in
        pkgs.mkShell {
          packages = [
            pythonEnv
          ];
        };

      ## Build our package using `buildPythonPackage`:
      packages.x86_64-linux.default =
        let
          attrs = project.renderers.buildPythonPackage {
            inherit python;
            extras = [ "test" ];
          };
        in
        python.pkgs.buildPythonPackage (attrs // {
          version = version;

          nativeCheckInputs = [
            python.pkgs.isort
            python.pkgs.black
            python.pkgs.mypy
            python.pkgs.pytest
            python.pkgs.flake8
          ];

          checkPhase = ''
            runHook preCheck

            isort --diff --check decaf/
            black --check decaf/
            mypy --namespace-packages decaf/api/client
            flake8
            pytest --verbose --ignore=setup.py --ignore-glob=tmp/* --doctest-modules

            runHook postCheck
          '';
        });
    };
}
