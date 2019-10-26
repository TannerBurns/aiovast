from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    README = fh.read()

setup(
     name='vast',
     version='2.1.1',
     author="Tanner Burns",
     author_email="tjburns102@gmail.com",
     description="Python3 library to easily scale up and out!",
     long_description=README,
     long_description_content_type="text/markdown",
     url="https://www.github.com/tannerburns/vast",
     packages=find_packages(),
     include_package_data=True,
     install_requires=[
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )