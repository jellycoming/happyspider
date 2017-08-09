# coding=utf-8

import sys
from setuptools import setup, find_packages


assert sys.version_info >= (2, 7), 'Requires python 2.7 or later version.'


setup(
    name='happyspider',
    version='1.0.0',
    url='https://github.com/jellycoming/happyspider',
    author='jellycoming',
    author_email='',
    description='A simple spider framework.',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    entry_points={
        'console_scripts': ['happyspider = happyspider.cmdline:execute']
    },
    install_requires=[
    ],
)