# Copyright 2024-present Kensho Technologies, LLC.
# Package metadata is located in pyproject.toml
# this file is just a fallback for older setuptools versions.

from distutils.core import setup
setup(
  name = 'kensho_kenverters',         # How you named your package folder (MyLib)
  packages = ['kensho_kenverters'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='Apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python Toolkit for Kensho Extract',   # Give a short description about your library
  author = 'Valerie Faucon-Morin',                   # Type in your name
  author_email = 'valerie.fauconmorin@spglobal.com',      # Type in your E-Mail
  url = 'https://github.com/kensho-technologies/kenverters',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kensho-technologies/kenverters/archive/refs/tags/v_1_0_0.tar.gz',    # I explain this later on
  keywords = ['Kensho Extract', 'Python Toolkit'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'pydantic',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: Apache Software License',

    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)