import json

from socket_client.socket_client import SocketClient

from faker import Faker

fake = Faker()


class TestMock:

    def test_get_valid(self, mock_server):
        host, port = mock_server

        connection = SocketClient(host, port)

        response = json.loads(connection.request('GET', '/users/1', json=True))

        assert response['Status-Code'] == 200

    def test_get_invalid(self, mock_server):
        host, port = mock_server

        connection = SocketClient(host, port)

        response = json.loads(connection.request('GET', '/users/2', json=True))

        assert response['Status-Code'] == 404

    def test_post_valid(self, mock_server):
        host, port = mock_server

        connection = SocketClient(host, port)

        user_name = f'{fake.first_name()}_{fake.last_name()}'

        response_1 = json.loads(connection.request('POST', f'/users/2/{user_name}', json=True))

        assert response_1['Status-Code'] == 200
        assert response_1['Body'] == 'Added successfully'

        response_2 = json.loads(connection.request('GET', '/users/2', json=True))

        assert response_2['Status-Code'] == 200
        assert response_2['Body'] == user_name

    def test_post_invalid(self, mock_server):
        host, port = mock_server

        connection = SocketClient(host, port)

        response = json.loads(connection.request('POST', f'/users/1/jfheufhsufd', json=True))

        assert response['Status-Code'] == 403
