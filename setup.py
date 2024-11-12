from setuptools import setup, find_packages

setup(
    name="employee_directory",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "sqlmodel",
        "pytest",
        "httpx"
    ],
)