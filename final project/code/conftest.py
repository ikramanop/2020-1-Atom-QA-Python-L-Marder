import pytest
import subprocess

from ui.ui_fixtures import *
from api.api_fixtures import *

from db.connector.connector import MySQLConnector

from db.models.models import User


def pytest_configure(config):
    if not hasattr(config, 'slaveinput'):
        try:
            subprocess.call(['docker-compose', 'up'], timeout=35, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.TimeoutExpired:
            subprocess.call(['docker', 'ps'])

    config.connection = MySQLConnector(
        hostname='127.0.0.1',
        port='3306',
        username='root',
        password='root',
        db='users'
    )
    if not hasattr(config, 'slaveinput'):
        config.connection.connect_master()

        config.connection.add_user(User(
            username='ikramanop',
            password='1234567890',
            email='asertolpas@gmail.com',
            access=1,
            active=0
        ))

        config.connection.add_user(User(
            username='zvozsky',
            password='1234567890',
            email='afjefnjsebnf@fsiejf.er',
            access=1,
            active=0
        ))

        config.connection.add_user(User(
            username='k12f2432',
            password='1234567890',
            email='njsebnf@fsif.er',
            access=1,
            active=0
        ))
    else:
        config.connection.connect_slave()


def pytest_unconfigure(config):
    if not hasattr(config, 'slaveinput'):
        subprocess.call(['docker-compose', 'down'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.call(['docker', 'ps'])


def pytest_addoption(parser):
    parser.addoption('--url', default='http://127.0.0.1:8082')
    parser.addoption('--selenoid', default='None')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    selenoid = request.config.getoption('--selenoid')

    if selenoid != 'None':
        url = 'http://myapp:8080'

    return {'url': url, 'selenoid': selenoid}


@pytest.fixture(scope='session')
def mysql_connection(config, request):
    connection = request.config.connection

    return connection
