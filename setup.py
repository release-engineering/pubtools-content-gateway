from setuptools import setup, find_packages


def get_description():
    return "Automate pushing to Content Gateway"


def get_long_description():
    with open("README.md") as f:
        text = f.read()

    # Long description is everything after README's initial heading
    idx = text.find("\n\n")
    return text[idx:]


def get_requirements():
    # Note: at time of writing, requirements.txt is empty.
    # It exists anyway for a consistent setup.
    with open("requirements.txt") as f:
        return f.read().splitlines()

INSTALL_REQUIRES = ['urllib3', 'six', 'requests', 'mock', 'pytest', 'requests_mock']
# INSTALL_REQUIRES = get_requirements()

classifiers = [
    "Development Status :: 1 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

setup(
    name="pubtools-content-gateway",
    version="0.1",
    description=get_description(),
    long_description_content_type="text/markdown",
    author="Javed Alam",
    author_email="jalam@redhat.com",
    # url="https://github.com/release-engineering/pubtools-content-gateway",
    url="https://github.com/jalam453/pubtools-content-gateway",
    classifiers=classifiers,
    packages=find_packages(exclude=["tests"]),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "push-cgw-metadata = pubtools._content_gateway.push_cgw:main"
        ],
        "target": [
            "push-staged = pubtools._content_gateway.push_staged:entry_point",
        ]
    },
    include_package_data=True,
    python_requires=">=2.6",
    project_urls={
        "Changelog": "https://github.com/jalam453/pubtools-content-gateway",
        # "Documentation": "https://github.com/jalam453/pubtools-content-gateway",
    },
)
