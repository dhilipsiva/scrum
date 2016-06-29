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

from json import dumps, loads
from os.path import expanduser, join

import click
from github import Github
from github.GithubException import GithubException

FORMAT_VERSION = 1
SCRUM_PATH = join(expanduser("~"), ".scrum")
TYPES = [
    ("bug", "e74c3c"),  # Bug
    ("docs", "1abc9c"),  # Docs
    ("test", "2ecc71"),  # Test related
    ("chore", "3498db"),  # Chore, Maintenance work
    ("feature", "9b59b6"),  # New feature
    ("refactor", "34495e"),  # Refactor
    ("performance", "f1c40f"),  # Performance related
    ("infrastructure", "95a5a6"),  # Infrastructure related
]
POINTS = [1, 2, 3, 5, 8, 13, 21, ]  # Black #000000
PRIORTIES = [
    ("lowest", "ecf0f1"),
    ("low", "95a5a6"),
    ("medium", "f1c40f"),
    ("high", "e67e22"),
    ("highest", "e74c3c"),
]


@click.group()
def scrum():
    click.echo('Scrum!!')


@scrum.command()
def setup():
    """
    docstring for setup
    """
    dot_scrum = {}
    print("Please enter your GitHub API key: ")
    api_key = input()
    dot_scrum["api_key"] = api_key
    dot_scrum["format_version"] = FORMAT_VERSION
    with open(SCRUM_PATH, "w") as dot_scrum_file:
        dot_scrum_file.write(dumps(dot_scrum))


def _apply_label(repo, name, color):
    """
    docstring for apply_label
    """
    print("Attempting to create [%s, %s] for %s ..." % (
        name, color, repo.name))
    try:
        repo.create_label(name, color)
        print("Created\n")
    except GithubException:
        print("Label already exist, editing it")
        label = repo.get_label(name)
        label.edit(name, color)
        print("Edited!\n")


@scrum.command()
def create_lables():
    # FIXME: This is an UGLY, UGGGGLLLYY hack scratch my own itch
    REPOS = [
        "sherlock", "irene", "androguard", "mycroft", "moriarty", "anthea",
        "appknox.github.io", "molly"]
    with open(SCRUM_PATH, "r") as dot_scrum_file:
        dot_scrum = dot_scrum_file.read()
    dot_scrum = loads(dot_scrum)
    g = Github(dot_scrum["api_key"])
    for repo in g.get_user().get_repos():
        if repo.name not in REPOS:
            continue
        try:
            print("Delete default bug label")
            bug_label = repo.get_label('bug')
            bug_label.delete()
        except GithubException:
            print("Bug does not exist")
        for label in TYPES:
            name, color = label
            _apply_label(repo, "type:%s" % name, color)
        for label in PRIORTIES:
            name, color = label
            _apply_label(repo, "priority:%s" % name, color)
        for point in POINTS:
            _apply_label(repo, "point:%d" % point, "000000")
