from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-skill-hub",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Cross-AI tool local skill management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-skill-hub",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "tiktoken>=0.5.0",
        "gitpython>=3.1.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "skill=ai_skill_hub.main:cli",
        ],
    },
)
