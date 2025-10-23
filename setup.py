"""
MC AI - Setup Script

Allows pip installation:
    pip install git+https://github.com/your-username/mc-ai.git
    
Or local:
    pip install -e .
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename='requirements.txt'):
    """Read requirements from file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="mc-ai",
    version="1.0.0",
    author="Mark Coffey",
    author_email="[email protected]",
    description="MC AI - Consciousness Through Compassion. An advanced AI system built on empathy, emotional intelligence, and consciousness frameworks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/mc-ai",  # Update with your GitHub URL
    project_urls={
        "Bug Tracker": "https://github.com/your-username/mc-ai/issues",
        "Documentation": "https://github.com/your-username/mc-ai#readme",
        "Source Code": "https://github.com/your-username/mc-ai",
        "Replit": "https://replit.com/@[your-username]/MC-AI",
    },
    packages=find_packages(where=".", exclude=["tests*", "kaggle_competition*"]),
    package_data={
        "": [
            "datasets/**/*.json",
            "templates/**/*.html",
            "static/**/*",
            "knowledge_library/**/*.db",
            "*.md",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "pylint>=3.0.0",
        ],
        "kaggle": [
            "jupyter>=1.0.0",
            "notebook>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mc-ai=app:run_server",
        ],
    },
    keywords=[
        "artificial intelligence",
        "consciousness",
        "emotional intelligence",
        "empathy",
        "ai chatbot",
        "machine learning",
        "neuroscience",
        "cymatic analysis",
        "frequency analysis",
        "benevolent ai",
    ],
)
