# Changelog

## [0.0.12](https://github.com/teloscube/decaf-client-python/compare/0.0.11...0.0.12) (2024-09-26)


### ⚠ BREAKING CHANGES

* **dev:** switch to pyproject.toml, pyproject.nix

### Documentation

* update README and LICENSE ([3a7415c](https://github.com/teloscube/decaf-client-python/commit/3a7415cf1f7c178a7678d4ea5e5bd9d7b1c2b522))


### Miscellaneous Chores

* release 0.0.12 ([aaef4f7](https://github.com/teloscube/decaf-client-python/commit/aaef4f7d74978437d6b53f47724bac3e9f59ba89))
* release 0.0.12 ([770c3b1](https://github.com/teloscube/decaf-client-python/commit/770c3b1af935cac2f2985a0b9dbf037c275ac56c))


### Code Refactoring

* **dev:** switch to pyproject.toml, pyproject.nix ([3a97934](https://github.com/teloscube/decaf-client-python/commit/3a979345fceb969e06598352026e45f79f7c3f1b))

### [0.0.11](https://github.com/teloscube/decaf-client-python/compare/0.0.10...0.0.11) (2021-10-11)


### Features

* add py38 and py39 to supported versions ([8a769cc](https://github.com/teloscube/decaf-client-python/commit/8a769ccd890ab6061cf4c597b5b3911f7e78dce3))


### Bug Fixes

* **deps:** update production dependencies ([acd373d](https://github.com/teloscube/decaf-client-python/commit/acd373d854d8e9180bbe0b35ddb2edc618c9dbbe))

### [0.0.10](https://github.com/telostat/decaf-api-client-python/compare/0.0.9...0.0.10) (2020-06-11)


### Features

* add artifact resource retriever ([9561fc8](https://github.com/telostat/decaf-api-client-python/commit/9561fc8f4944182c693b97b2170fb8cdfa0343bb))


### Bug Fixes

* use correct type for portrolio resource id ([4b83b01](https://github.com/telostat/decaf-api-client-python/commit/4b83b013da3ee4554334af5135708e5614254b14))

### [0.0.9](https://github.com/telostat/decaf-api-client-python/compare/0.0.8...0.0.9) (2020-05-26)


### Features

* **endpoints:** add artifact and action type endpoints, resources ([9faa489](https://github.com/telostat/decaf-api-client-python/commit/9faa489f225f232aab467f6fe90105f632475382))
* **endpoints:** add analytical types endpoint (read-only) ([834e7ff](https://github.com/telostat/decaf-api-client-python/commit/834e7ffae620427446e5448d8ea7b89d9b88c013))

### Bug Fixes

* **resources:** make ActionResource.pxmain optional ([ee0e485](https://github.com/telostat/decaf-api-client-python/commit/ee0e485958850171da5ba7152d2b89e4bb785846))
* **resources:** use correct Id types for resources ([f20d011](https://github.com/telostat/decaf-api-client-python/commit/f20d0112d7054b6d67295ea8ec308508e1f3dac0))
* **endpoints:** use correct ID types for action resource relations ([3c38c47](https://github.com/telostat/decaf-api-client-python/commit/3c38c4792107e6437540c5745fc269b35ceb9c42))

### [0.0.8](https://github.com/telostat/decaf-api-client-python/compare/0.0.7...0.0.8) (2020-04-08)


### Features

* **endpoints:** add actions endpoint (read-only) ([99f7b75](https://github.com/telostat/decaf-api-client-python/commit/99f7b75b8fc4b32e6cf8f55a18b0726afcab63ee))
* **endpoints:** add artifacts endpoint (read-only) ([e78e68b](https://github.com/telostat/decaf-api-client-python/commit/e78e68b6493984c6b0466252877f300d1bbff817))
* **endpoints:** add quants endpoint ([b2ac7fb](https://github.com/telostat/decaf-api-client-python/commit/b2ac7fb79a0b5763c00dafd2972bd1738bd64204))
* **endpoints:** add stocks endpoint ([bd938e0](https://github.com/telostat/decaf-api-client-python/commit/bd938e0f529e27497d2df53b985ce275501c5b45))


### Bug Fixes

* use correct type for _LaterS placeholder newtype ([7f1cd91](https://github.com/telostat/decaf-api-client-python/commit/7f1cd916c2870c54c9e714ffa898f7d08b5eeb73))

### [0.0.7](https://github.com/telostat/decaf-api-client-python/compare/0.0.6...0.0.7) (2020-04-08)


### Features

* **endpoint:** add teams endpoint ([c5e3a35](https://github.com/telostat/decaf-api-client-python/commit/c5e3a35f355e7c45b596868ed16c91ecb264d012))
* **endpoints:** add accounts endpoint ([6d82a7d](https://github.com/telostat/decaf-api-client-python/commit/6d82a7dadd07e75691786275ffc574366a5d323b))
* **endpoints:** add consolidation endpoint ([c06e3ab](https://github.com/telostat/decaf-api-client-python/commit/c06e3abdf6ad6c7c89a409916597818e92892504))
* **endpoints:** add countries endpoint ([0ae1885](https://github.com/telostat/decaf-api-client-python/commit/0ae18859826fa2c9e3897b5b1a7fa533962dceb3))
* **endpoints:** add currencies endpoint ([a0ba2fd](https://github.com/telostat/decaf-api-client-python/commit/a0ba2fd22eadd1ebb8f462e23e0a7efe5cffc03e))
* **endpoints:** add institutions endpoint ([a834be1](https://github.com/telostat/decaf-api-client-python/commit/a834be1c331fa8233d3fdc81d2624ab2978db726))
* **endpoints:** add portfolios endpoint ([819ef18](https://github.com/telostat/decaf-api-client-python/commit/819ef188150c56864c5d3a58b133ed99f13914c3))
* **endpoints:** add users endpoint ([1131641](https://github.com/telostat/decaf-api-client-python/commit/1131641346ec8c37f83dc9d209198d1eb62e49d0))
* **machinery:** add alternative client authentication methods ([4c7eda1](https://github.com/telostat/decaf-api-client-python/commit/4c7eda15660b759144f7e93e6156021270e6efa3))
* **machinery:** improve client machinery, add endpoint machinery ([d64cc41](https://github.com/telostat/decaf-api-client-python/commit/d64cc41e74f0c129131ab24d489d61fa8f6a5d8c))
* **utils:** add some functions and definitions for convenience ([d184487](https://github.com/telostat/decaf-api-client-python/commit/d18448732c635f099ef46432fd6f97095a12c1ac))

### 0.0.6 (2020-01-28)

### Bug Fixes

* **build:** add dataclasses dependency (Python36), simplify setup.py ([4d65633](https://github.com/telostat/decaf-api-client-python/commit/4d6563394ea66f1f0c5ea4123411fee6b88dba48))

### 0.0.5 (2020-01-22)

### Features

* add PATCH method to the client ([cfefe3d](https://github.com/telostat/decaf-api-client-python/commit/cfefe3df4a94d1b16b6dea89e763f1513753edb0))

### 0.0.4 (2019-07-31)

* 2019-07-31 a143018 Add put method to the client (vst@vsthost.com)
* 2019-05-30 764faa8 Create client from profile (vst@vsthost.com)
* 2019-05-18 5f52572 (chore) Bump version to 0.0.4.dev0 (vst@vsthost.com)

### 0.0.3 (2019-05-18)

* 2019-05-18 90e269d Merge branch '0.0.3' (vst@vsthost.com)
* 2019-05-18 9eaf384 (fix) Fix README.md and setup.py (vst@vsthost.com)
* 2019-05-18 bd7b714 (fix) Fix packaging (vst@vsthost.com)
* 2019-05-18 79e7758 (release) Update change log (vst@vsthost.com)
* 2019-05-18 2d88cb1 (release) Bump version to 0.0.3 (vst@vsthost.com)
* 2019-05-18 6176470 (chore) Adapt setup to README.md (vst@vsthost.com)
* 2019-05-18 0e4ad31 (chore) Convert README from .rst to .md (vst@vsthost.com)
* 2019-05-18 b3e58f9 (chore) Upgrade requests dependency (vst@vsthost.com)
* 2019-05-18 643cb5f (chore) Rename package to decaf.api.client (vst@vsthost.com)
* 2019-04-16 bb66fda (chore) Version bumped to 0.0.3.dev0 (vst@vsthost.com)

### 0.0.2 (2019-04-16)

* 2019-04-16 1984637 Merge branch '0.0.2' (vst@vsthost.com)
* 2019-04-16 747dd8c (release) Change log updated (vst@vsthost.com)
* 2019-04-16 d3cdc74 (release) Version bumped to 0.0.2 (vst@vsthost.com)
* 2019-03-07 23be6ea (improve) Support for remote value collections (vst@vsthost.com)
* 2019-03-07 77c19bc (fix) Entity endpoint attribute fix (vst@vsthost.com)
* 2019-03-06 d13ba17 (improve) Request timeouts and exception handling (vst@vsthost.com)
* 2019-03-05 779002b (chore) Revisit dev dependencies (vst@vsthost.com)
* 2019-03-05 e590bd8 (chore) Version bumped to 0.0.2.dev0 (vst@vsthost.com)

### 0.0.1 (2019-03-05)

* 2019-03-05 3b3ebcb Merge branch '0.0.1' (vst@vsthost.com)
* 2019-03-05 d663296 (release) Change log updated (vst@vsthost.com)
* 2019-03-05 b4a0bdc (release) Version bumped to 0.0.1 (vst@vsthost.com)
* 2019-03-05 afd8b3b Initial code commit (vst@vsthost.com)
* 2019-03-05 a90b4dc Initial commit (vst@vsthost.com)
