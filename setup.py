#!/usr/bin/env python3
"""
Setup script for Study CLI Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="study-cli",
    version="1.0.0",
    description="A command-line interface for managing and searching study materials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Study CLI",
    python_requires=">=3.6",
    py_modules=["study_cli"],
    entry_points={
        "console_scripts": [
            "study-cli=study_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)