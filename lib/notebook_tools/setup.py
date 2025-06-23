"""
Setup script for notebook_tools library.
"""

from setuptools import setup, find_packages

setup(
    name="notebook_tools",
    version="0.1.0",
    description="Tools and widgets for enhancing Jupyter notebooks",
    packages=find_packages(),
    install_requires=[
        "ipywidgets>=7.0",
        "jupyter",
    ],
    python_requires=">=3.7",
)