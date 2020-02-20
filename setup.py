import os
import json

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fin:
    README = fin.read()

with open(os.path.join(os.path.dirname(__file__), 'manifest.json')) as fin:
    manifest = json.load(fin)

setup(
    name = manifest.get('name', 'default.manifest.name'),
    version =  manifest.get('version', '0.0.0'),
    packages = find_packages(
        include=manifest.get('package_include', []), 
        exclude=manifest.get('package_exclude', [])
    ),
    package_data = manifest.get('package_data', None),
    include_package_data = manifest.get('include_package_data', True),
    description =  manifest.get('description', 'default.manifest.description'),
    url = manifest.get('url', 'default.manifest.url'),
    author = manifest.get('author', 'default.manifest.author'),
    author_email = manifest.get('author_email', 'default.manifest.author_email'),
    install_requires = manifest.get('requirements', []),
    classifiers =  manifest.get('classifiers', []),
    entry_points = manifest.get('entry_points', {}),
    scripts = manifest.get('scripts', None),
    keywords = manifest.get('keywords', [])
)
