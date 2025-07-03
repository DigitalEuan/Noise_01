#!/usr/bin/env python3
"""
Setup script for UBP Noise Theory Validation Package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ubp-noise-theory",
    version="1.0.0",
    author="UBP Research Team",
    description="Validation framework for the Universal Binary Principle (UBP) Noise Theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="noise theory, UBP, universal binary principle, signal processing, physics",
    project_urls={
        "Documentation": "https://github.com/ubp-research/noise-theory",
        "Source": "https://github.com/ubp-research/noise-theory",
        "Tracker": "https://github.com/ubp-research/noise-theory/issues",
    },
)

