#!/usr/bin/env python

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

from setuptools import setup, find_packages
setup(
    name="joule",
    version="0.1",
    packages=find_packages(),
    scripts=['joule'],

    # metadata for upload to PyPI
    author="Justin Cole",
    author_email="justincole01@gmail.com",
    description="CNC Laser controller",
    long_description=long_description,
    license="MIT",
    keywords="CNC laser raspberry pi",
    url="https://github.com/whisperoftheshot/joule",
)
