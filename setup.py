import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="haloinfinite",
    version="0.2.0",
    description="API wrapper for Halo Infinite written in Python",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Miguel Ferrer",
    author_email="ingferrermiguel@gmail.com",
    url="https://github.com/ingmferrer/haloinfinite",
    license="MIT",
    packages=["haloinfinite"],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "python-dateutil",
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="python api wrapper library halo infinite",
    project_urls={
        "Documentation": "https://github.com/ingmferrer/haloinfinite",
        "Source": "https://github.com/ingmferrer/haloinfinite",
        "Tracker": "https://github.com/ingmferrer/haloinfinite/issues",
    },
)
