# Copyright 2024-present Kensho Technologies, LLC.
# Package metadata is located in pyproject.toml

from distutils.core import setup  # pylint: disable=deprecated-module

setup(
    name="kensho_kenverters",
    packages=["kensho_kenverters"],
    version="1.2.1",
    license="Apache-2.0",
    description="Python Toolkit for Kensho Extract",
    author="Valerie Faucon-Morin",
    author_email="valerie.fauconmorin@spglobal.com",
    url="https://github.com/kensho-technologies/kenverters",
    download_url="https://github.com/kensho-technologies/kenverters/archive/refs/tags/v_1_2_1.tar.gz",  # noqa:E501
    keywords=["Kensho Extract", "Python Toolkit"],
    install_requires=[
        "pandas",
        "pydantic",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
