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
from datetime import datetime

import click
from github import Github
from github.GithubException import GithubException

FORMAT_VERSION = 1
SCRUM_PATH = join(expanduser("~"), ".scrum")
TYPES = [
    ("bug", "E3000E"),
    ("docs", "7BB0A6"),
    ("test", "FD5B03"),
    ("chore", "8F6F40"),
    ("feature", "92F22A"),
    ("invalid", "63393E"),
    ("wontfix", "F29B34"),
    ("question", "8870FF"),
    ("refactor", "FEC606"),
    ("duplicate", "3D8EB9"),
    ("enhancement", "FF6766"),
    ("help-wanted", "EEFF6B"),
    ("performance", "2FE2D9"),
    ("infrastructure", "B3BB19"),
]
POINTS = [1, 2, 3, 5, 8, 13, 21, ]  # Black #000000
PRIORTIES = [
    ("lowest", "FFFFF7"),
    ("low", "D2D7D3"),
    ("medium", "FEC606"),
    ("high", "FF7416"),
    ("highest", "E3000E"),
]

# FIXME: This is an UGLY, UGGGGLLLYY hack scratch my own itch
REPOS = [
    "sherlock", "irene", "androguard", "mycroft", "moriarty", "anthea",
    "appknox.github.io", "molly"
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
        print("Label already exist, Attemting to edit it")
        label = repo.get_label(name)
        if label.color == color:
            return
        label.edit(name, color)
        print("Edited!\n")


def get_g():
    """
    Get the Github Object
    """
    with open(SCRUM_PATH, "r") as dot_scrum_file:
        dot_scrum = dot_scrum_file.read()
    dot_scrum = loads(dot_scrum)
    return Github(dot_scrum["api_key"], timeout=600000)


def _get_repos():
    """
    Get the repos that we are interested in
    """
    g = get_g()
    repos = []
    for repo in g.get_user().get_repos():
        if repo.name in REPOS:
            repos.append(repo)
    return repos


@scrum.command()
def delete_all_labels():
    """
    Delete all the labels
    """
    for repo in _get_repos():
        if repo.name not in REPOS:
            continue
        for label in repo.get_labels():
            print("deleting %s on %s" % (label.name, repo.name))
            label.delete()


@scrum.command()
def create_lables():
    for repo in _get_repos():
        if repo.name not in REPOS:
            continue
        for label in TYPES:
            name, color = label
            _apply_label(repo, "type:%s" % name, color)
        for label in PRIORTIES:
            name, color = label
            _apply_label(repo, "priority:%s" % name, color)
        for point in POINTS:
            _apply_label(repo, "point:%d" % point, "000000")


@scrum.command()
def ping():
    """
    docstring for ping
    """
    print("ping")
    g = get_g()
    repos = g.get_user().get_repos()
    repo_list = []
    for repo in repos:
        repo_list.append(repo)
    print(repo_list)
    print(len(repo_list))


@scrum.command()
def list_milestones():
    """
    List the open milestones
    """
    repos = _get_repos()
    for repo in repos:
        print(repo.name, ": ")
        for milestone in repo.get_milestones("open"):
            print(milestone.title)
        print("================")


@scrum.command()
@click.argument('date')
def create_milestones(date):
    """
    docstring for create_milestones
    """
    date = "%sT59:59:10Z" % date
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    for repo in _get_repos():
        repo.create_milestone(date, due_on=date_obj)
