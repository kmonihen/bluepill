#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="bluepill",
    version="1.0.1",
    author="Keith Monihen",
    author_email="keith.monihen@stelligent.com",
    description="An expanded decorator class for modifying Placebo playback or recording with boto3 calls.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kmonihen/BluePill",
    packages=find_packages(exclude=['tests*']),
    package_dir={'bluepill': 'bluepill'},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)