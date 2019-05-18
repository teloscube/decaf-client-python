"""
This module provides the setup procedure.
"""

import os
import re

from setuptools import setup

#: Defines the name of this package.
Name = "decaf-api-client"

#: Defines the description of this package.
Description = "DECAF API Client"

#: Defines the package root directory.
BaseDir = os.path.abspath(os.path.dirname(__file__))

#: Defines the regular expression of the version.
VersionRE = r"__version__\s*=\s*['\"]([^'\"]*)['\"]"

#: Defines the version of this package.
Version = re.search(VersionRE, open(f"{BaseDir}/decaf/api/client/__init__.py", encoding="utf_8_sig").read()).group(1)

#: Defines the README file contents.
with open(os.path.join(BaseDir, "README.md")) as cfile:
    Readme = cfile.read()

#: Defines a list of required libraries.
Requirements = [
    "requests==2.22.0"
]

#: Defines extra requirements for various other purposes.
RequirementsExtras = {
    "dev": [
        "flake8",
        "ipython",
        "mypy",
        "tox",
        "twine",
        "wheel",
    ],
}

## Proceed with setup:
setup(
    name=Name,
    version=Version,
    description=Description,
    long_description=Readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    author="Vehbi Sinan Tunalioglu",
    author_email="vst@vsthost.com",
    url="https://github.com/telostat/decaf-api-client-python",
    packages=[
        "decaf.api.client"
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=Requirements,
    extras_require=RequirementsExtras,
    dependency_links=[],
    scripts=[],
)
