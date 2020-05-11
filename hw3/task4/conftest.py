import pytest

from ssh_connector.ssh_connector import SSHConnector


def pytest_addoption(parser):
    parser.addoption('--host', default='127.0.0.1')
    parser.addoption('--port', default='22')
    parser.addoption('--nginx-port', default=80)


@pytest.fixture(scope='session')
def config(request):
    host = request.config.getoption('--host')
    port = request.config.getoption('--port')
    nginx_port = request.config.getoption('--nginx-port')

    return {'host': host, 'port': port, 'nginx_port': nginx_port}


@pytest.fixture(scope='session')
def ssh_client(config):
    with SSHConnector(
            host=config['host'],
            port=config['port'],
            username='root',
            password='root'
    ) as client:
        yield client
