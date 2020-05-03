import pytest

from mock import mock

from faker import Faker

from socket_client.socket_client import SocketClient


def pytest_addoption(parser):
    parser.addoption('--host', default='127.0.0.1')
    parser.addoption('--port', default='5000')


@pytest.fixture(scope='session')
def config(request):
    host = request.config.getoption('--host')
    port = request.config.getoption('--port')

    return {'host': host, 'port': int(port)}


@pytest.fixture(scope='session')
def mock_server(config):
    server = mock.run_mock(config['host'], config['port'])

    fake = Faker()

    connection = SocketClient(config['host'], config['port'])
    connection.request('POST', f'/users/1/{fake.first_name()}_{fake.last_name()}')

    yield server._kwargs['host'], server._kwargs['port']

    connection.request('POST', '/shutdown')
