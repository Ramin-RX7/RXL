from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_descriptions = fh.read()

s = setup(
    name = "RXL",
    version = "0.0.1",
    license = "LGPL",
    description = "RXL Features",
    url = "https://github.com/Ramin-RX7/RX7-Lib/",
    packages = find_packages(),
    install_requires = [],
    python_requires = ">= 3.8",
    author = "Ramin RX7",
    author_email = "rawmin.rx@gmail.com",
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
    long_description = long_descriptions,
    long_description_content_type = "text/markdown",
    )
