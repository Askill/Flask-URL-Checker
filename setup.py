# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use Python Boilerplate to start
# simple, usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os

from setuptools import setup, find_packages

# Meta information
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)

# Save version and author to __meta__.py
path = os.path.join(dirname, 'src', 'Star-Mapper', '__meta__.py')
data = '''# Automatically created. Please do not edit.
__version__ = u'%s'
__author__ = u'Patrice Matz'
''' % version
with open(path, 'wb') as F:
    F.write(data.encode())

setup(
    # Basic info
    name='Star-Mapper',
    version=version,
    author='Patrice Matz',
    author_email='mail@patricematz.de',
    url='https://github.com/Askill/Star-Mapper',
    description='Calls every link on a given website and produces an explorable graph visualization.',
    long_description=open('./docs/README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=['graph', "web crawler",  'network', 'visualization'],
    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        "requests",
        "lxml",
        "urllib3"
    ],
    # Data files
    package_data={
        "docs":["*"]
    },
    # Scripts
    entry_points={
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
