from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_descriptions = fh.read()

s = setup(
    name = "RXL",
    description = "RXL Features",
    version = "0.0.2",
    license = "LGPL",
    url = "https://github.com/Ramin-RX7/RX-Language/",
    author = "Ramin RX7",
    author_email = "rawmin.rx@gmail.com",

    packages = find_packages(),
    install_requires = [],
    python_requires = ">= 3.8",

    classifiers = [
        'Programming Language :: Python :: 3',
    ],

    long_description = long_descriptions,
    long_description_content_type = "text/markdown",

    entry_points={
        'console_scripts': [
            'RXL = RXL.RXL:main',
        ],
    },
)
