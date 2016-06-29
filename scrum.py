#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: scrum.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2016-06-29
"""

from json import dumps
from os.path import expanduser, join

import click

FORMAT_VERSION = 1


@click.command()
def scrum():
    """Example script."""
    click.echo('Hello World!')


@click.group()
def scrum_util():
    """
    docstring for scrum
    """
    pass


@scrum_util.command()
def setup():
    """
    docstring for setup
    """
    dot_scrum = {}
    print("Please enter your GitHub API key: ")
    api_key = input()
    dot_scrum["api_key"] = api_key
    dot_scrum["format_version"] = FORMAT_VERSION
    dot_scrum_path = join(expanduser("~"), ".scrum")
    dot_scrum_file = open(dot_scrum_path, "w")
    dot_scrum_file.write(dumps(dot_scrum))
