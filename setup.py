from setuptools import setup, find_packages

setup(
    name="dlt-source-morphais",
    version="0.0.2",
    author="Planet A GmbH",
    author_email="dev@planet-a.com",
    packages=find_packages(exclude=["tests"]),
    description="A DLT source for Morphais",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "dlt>=1.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
