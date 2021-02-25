#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup_requirements = [
    "pytest-runner>=5.2",
]

test_requirements = [
    "black>=19.10b0",
    "codecov>=2.1.4",
    "flake8>=3.8.3",
    "flake8-debugger>=3.2.1",
    "pytest>=5.4.3",
    "pytest-cov>=2.9.0",
    "pytest-raises>=0.11",
]

dev_requirements = [
    *setup_requirements,
    *test_requirements,
    "bump2version>=1.0.1",
    "coverage>=5.1",
    "ipython>=7.15.0",
    "m2r2>=0.2.7",
    "pytest-runner>=5.2",
    "Sphinx>=3.4.3",
    "sphinx_rtd_theme>=0.5.1",
    "tox>=3.15.2",
    "twine>=3.1.1",
    "wheel>=0.34.2",
]

requirements = [
    "numpy",
    "scipy",
    "matplotlib"
]

extra_requirements = {
    "setup": setup_requirements,
    "test": test_requirements,
    "dev": dev_requirements,
    "all": [
        *requirements,
        *dev_requirements,
    ]
}

setup(
    author="Paul Grimes",
    author_email="pgrimes@cfa.harvard.edu",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Python package to operate, and analyze the results from, the SAO Receiver Lab Nearfield beamscanner.",
    entry_points={
        "console_scripts": [
            "my_example=python_beamscanner.bin.my_example:main"
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="python_beamscanner",
    name="python_beamscanner",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*"]),
    python_requires=">=3.7",
    setup_requires=setup_requirements,
    test_suite="python_beamscanner/tests",
    tests_require=test_requirements,
    extras_require=extra_requirements,
    url="https://github.com/PaulKGrimes/python_beamscanner",
    # Do not edit this string manually, always use bumpversion
    # Details in CONTRIBUTING.rst
    version="0.0.0",
    zip_safe=False,
)

py~=1.10.0
colorama~=0.4.4
numpy~=1.20.1
pip~=21.0.1
wheel~=0.36.2
openssl~=1.1.1j
keyring~=22.0.1
attrs~=20.3.0
toml~=0.10.2
regex~=2020.11.13
click~=7.1.2
appdirs~=1.4.4
pathspec~=0.8.1
black~=20.8b1
pytest~=6.2.2
setuptools~=49.6.0
pytz~=2021.1
scipy~=1.6.1
pkginfo~=1.7.0
flake8~=3.8.4
pyflakes~=2.2.0
wcwidth~=0.2.5
pluggy~=0.13.1
iniconfig~=1.1.1
atomicwrites~=1.4.0
certifi~=2020.12.5
chardet~=4.0.0
requests~=2.25.1
codecov~=2.1.11
urllib3~=1.26.3
six~=1.15.0
coverage~=5.4
idna~=2.10
pyparsing~=2.4.7
ipython~=7.20.0
sphinx~=3.5.1
docutils~=0.16
jinja2~=2.11.3
pycodestyle~=2.6.0
