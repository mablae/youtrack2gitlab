# Skeleton of a CLI

import click
import gitlab
import youtrack2gitlab
import requests
from bs4 import BeautifulSoup
from pprint import pprint


@click.command('y2g_projects')
def cli():
    git = gitlab.Gitlab(youtrack2gitlab.config['gitlab']['host'])
    git.login(youtrack2gitlab.config['gitlab']['username'], youtrack2gitlab.config['gitlab']['password'])

    for project in git.getall(git.getprojects):
        pprint(project)
