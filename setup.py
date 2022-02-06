import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="haloinfinite",
    version="0.2.0",
    description="API wrapper for Halo Infinite written in Python",
    long_description=read("README.md"),
    url="https://github.com/ingmferrer/haloinfinite",
    long_description_content_type="text/markdown",
    author="Miguel Ferrer",
    author_email="ingferrermiguel@gmail.com",
    license="MIT",
    packages=["haloinfinite"],
    install_requires=[
        "requests",
        "python-dateutil",
    ],
    zip_safe=False,
)
