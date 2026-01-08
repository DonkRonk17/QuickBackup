#!/usr/bin/env python3
"""
QuickBackup Setup Script
"""

from setuptools import setup
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="quickbackup",
    version="1.0.0",
    author="Team Brain",
    author_email="logan@metaphysicsandcomputing.com",
    description="Simple, Fast Backup Automation with incremental backups and compression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/QuickBackup",
    py_modules=["quickbackup"],
    python_requires=">=3.7",
    install_requires=[],  # No external dependencies!
    entry_points={
        "console_scripts": [
            "quickbackup=quickbackup:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="backup incremental compression automation cli",
)
