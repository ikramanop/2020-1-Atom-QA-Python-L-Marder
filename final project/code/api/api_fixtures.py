import pytest

from api.client.client import ApiClient
from api.client.vk_api_client import VkApiClient


@pytest.fixture(scope='function')
def api_client(config, mysql_connection):
    client = ApiClient('ikramanop', '1234567890', 'http://127.0.0.1:8082')

    return client


@pytest.fixture(scope='function')
def vk_api_client(config):
    client = VkApiClient('127.0.0.1', '5000')

    return client
