import pytest

from client.client import OrmConnector


def pytest_addoption(parser):
    parser.addoption('--host', default='127.0.0.1')
    parser.addoption('--port', default='3306')
    parser.addoption('--user', default='root')
    parser.addoption('--password', default='root')
    parser.addoption('--db', default='None')


@pytest.fixture(scope='session')
def config(request):
    host = request.config.getoption('--host')
    port = request.config.getoption('--port')
    user = request.config.getoption('--user')
    password = request.config.getoption('--password')
    db = request.config.getoption('--db')

    return {'host': host, 'port': int(port), 'user': user, 'password': password, 'db': db}


@pytest.fixture(scope='session')
def connector(config):
    connector = OrmConnector(
        host=config['host'],
        port=config['port'],
        username=config['user'],
        password=config['password'],
        db_name=config['db']
    )
    yield connector
    connector.sql(f"DROP DATABASE `{config['db']}`")
