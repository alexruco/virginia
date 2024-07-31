# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="virginia",
    version="0.1.0",
    author="Alex Ruco",
    author_email="alex@ruco.pt",
    description="A Python library for webpage status checking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexruco/virginia",
    packages=find_packages(include=['virginia', 'virginia.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "httpx[http2]",
    ],
    entry_points={
        "console_scripts": [
            "check_page=virginia.main:check_page_availability",
        ],
    },
)
