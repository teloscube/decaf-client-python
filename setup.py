import os
import re

from setuptools import setup

setup(
    name="decaf-api-client",
    version=re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", open("decaf/api/client/__init__.py").read()).group(1),
    description="DECAF API Client",
    long_description=open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author="Vehbi Sinan Tunalioglu",
    author_email="vst@vsthost.com",
    url="https://github.com/telostat/decaf-api-client-python",
    package_data={"decaf.api.client": ["py.typed"]},
    packages=["decaf.api.client"],
    include_package_data=True,
    zip_safe=False,
    install_requires=['dataclasses==0.7;python_version=="3.6"', "requests<3"],
    dependency_links=[],
    scripts=[],
)
