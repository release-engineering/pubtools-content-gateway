# -*- coding: utf-8 -*-
"""setup.py"""

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [("tox-args=", "a", "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex

        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


long_description = read_content("docs/README.rst") + read_content(
    os.path.join("docs/", "CHANGELOG.rst")
)

extras_require = {"reST": ["Sphinx"]}
if os.environ.get("READTHEDOCS", None):
    extras_require["reST"].append("recommonmark")


def get_description():
    return "Automate pushing to Content Gateway"


def get_long_description():
    with open("docs/README.rst") as f:
        text = f.read()

    # Long description is everything after README's initial heading
    idx = text.find("\n\n")
    return text[idx:]


def get_requirements():
    # Note: at time of writing, requirements.txt is empty.
    # It exists anyway for a consistent setup.
    with open("requirements.txt") as f:
        return f.read().splitlines()


# INSTALL_REQUIRES = ['urllib3', 'six', 'requests-mock', 'requests', 'mock', 'pytest', 'setuptools']
INSTALL_REQUIRES = get_requirements()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

setup(
    name="pubtools-content-gateway",
    version="0.4.0",
    description=get_description(),
    long_description_content_type="text/markdown",
    author="Javed Alam",
    author_email="jalam@redhat.com",
    url="https://github.com/release-engineering/pubtools-content-gateway",
    classifiers=classifiers,
    packages=find_packages(exclude=["tests"]),
    install_requires=INSTALL_REQUIRES,
    tests_require=["tox", "mock", "requests_mock", "pushcollector", "requests", "tox", "pytest", "covdefaults",
                   "pytest-cov"],
    data_files=[],
    entry_points={
        "console_scripts": [
            "push-cgw-metadata = pubtools._content_gateway.push_cgw:main"
        ],
        "target": [
            "push-staged-cgw = pubtools._content_gateway.push_staged_cgw:entry_point",
        ]
    },
    include_package_data=True,
    python_requires=">=3.6",
    project_urls={
        "Changelog": "https://release-engineering.github.io/pubtools-content-gateway/CHANGELOG.html",
        "Documentation": "https://release-engineering.github.io/pubtools-content-gateway/",
    },
    cmdclass={"test": Tox},
)
