import os
import json

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fin:
    README = fin.read()

with open(os.path.join(os.path.dirname(__file__), 'manifest.json')) as fin:
    manifest = json.load(fin)


setup(
    name = "aiovast",
    version =  "4.0.0",
    packages = find_packages(
        include=["vast", "vast.*"]
    ),
    package_data = None,
    include_package_data = True,
    description = "Python3 library to scale functions using asyncio",
    long_description = README,
    url = "https://github.com/TannerBurns/vast",
    author = "Tanner Burns",
    author_email = "tjburns102@gmail.com",
    install_requires = [
        "requests",
        "tqdm",
        "colored"
    ],
    classifiers =  [
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    entry_points = {}
)
