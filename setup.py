from setuptools import setup, find_packages

setup(
    name="sorda",
    version="0.1.2.dev-10",
    author="qinka",
    author_email="me@qinka.pro",
    description="Run excute",
    long_description="Run and excute, see https://github.com/Qinka/sorda",
    url="https://github.com/Qinka/sorda",
    packages=find_packages(),
    install_requires=[
        "pyyaml"
    ],
)