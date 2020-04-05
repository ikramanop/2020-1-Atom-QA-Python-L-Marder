from ui.fixtures import *
import pytest


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com')
    parser.addoption('--selenoid', default='None')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    selenoid = request.config.getoption('--selenoid')

    return {'url': url, 'selenoid': selenoid}
