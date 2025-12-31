#!/usr/bin/env python3
"""
Vibecode Studio Setup Script
Install Vibecode Studio globally to use across all projects
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [line.strip() for line in requirements_file.read_text().splitlines() 
                   if line.strip() and not line.startswith('#')]

setup(
    name="vibecode-studio",
    version="1.0.0",
    description="Multi-Agent AI Development System with Premium Skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vibecode Team",
    author_email="k.nguyen@griffith.edu.au",
    url="https://github.com/khoi1009/Vibecode-with-Multi-Agent",
    license="MIT",
    
    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "docs", "dist"]),
    py_modules=["vibecode_studio"],
    
    # Include non-Python files
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yaml", "*.yml"],
        "skills": ["**/*"],
        "core": ["*.py"],
        "agents": ["*.py"],
    },
    
    # Python version requirement
    python_requires=">=3.7",
    
    # Dependencies
    install_requires=requirements,
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "vibecode=vibecode_studio:main",
            "vibe=vibecode_studio:main",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    
    # Keywords
    keywords="ai development multi-agent code-generation skills automation",
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/khoi1009/Vibecode-with-Multi-Agent/issues",
        "Source": "https://github.com/khoi1009/Vibecode-with-Multi-Agent",
        "Documentation": "https://github.com/khoi1009/Vibecode-with-Multi-Agent#readme",
    },
)
