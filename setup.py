#!/usr/bin/env python3
"""
Setup script for Advanced Data Processor
=======================================

This script installs the Advanced Data Processor application and its dependencies.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="advanced-data-processor",
    version="1.0.0",
    author="Data Processing Team",
    author_email="support@dataprocessor.com",
    description="A powerful desktop application for data processing with one-click operations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/advanced-data-processor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Database",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "data-processor=code:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.html", "*.csv"],
    },
    keywords="data processing, data analysis, data cleaning, visualization, GUI, desktop application",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/advanced-data-processor/issues",
        "Source": "https://github.com/yourusername/advanced-data-processor",
        "Documentation": "https://github.com/yourusername/advanced-data-processor/blob/main/README.md",
    },
) 