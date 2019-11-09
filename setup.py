import json

from setuptools import setup, find_packages

with open('README.md', 'r') as fin:
    README = fin.read()

with open('manifest.json', 'r') as fin:
    manifest = json.load(fin)

setup (
    name = manifest.get('name', 'manifest.name'),
    version = manifest.get('version', '0.0.0'),
    author = manifest.get('author', 'manifest.author'),
    author_email = manifest.get('author_email', 'manifest.author.email'),
    description = manifest.get('description', 'manifest.description'),
    long_description = README,
    long_description_content_type = 'text/markdown',
    url = 'https://www.github.com/tannerburns/vast',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'requests',
        'tqdm',
        'colored'
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)