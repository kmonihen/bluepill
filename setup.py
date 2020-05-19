from setuptools import setup, find_packages

_PACKAGES = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_INSTALL_REQUIRES = [
    "placebo"
]

setup(
    name='bluepill',
    version='1.0',
    description='An expanded decorator class for modifying Placebo playback or recording with boto3 calls.',
    author='Keith Monihen',
    author_email='kmonihen@gmail.com',
    packages=_PACKAGES,
    package_dir={'bluepill': 'bluepill'},
    python_requires=">=3.6",
    install_requires=_INSTALL_REQUIRES,
    setup_requires=["pytest-runner"],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)