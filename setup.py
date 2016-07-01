#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: setup.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2016-06-29
"""

from setuptools import setup

setup(
    name='scrum',
    description="A scrum CLI tool & Python wrapper to manage Issues, Labels & Milestones in multiple repositories on GitHub",  # NOQA
    url='https://github.com/dhilipsiva/scrum',
    version='0.0.1',
    py_modules=['scrum'],
    author='dhilipsiva',
    author_email='dhilipsiva@gmail.com',
    install_requires=[
        'Click',
        'PyGithub'
    ],
    entry_points='''
        [console_scripts]
        scrum=scrum.cli:scrum
    ''',
)
