import json
from time import time

import allure
import pytest
import requests


@pytest.mark.API
@allure.feature('API')
class TestApi:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, config, mysql_connection):
        self.client = api_client
        self.config = config
        self.connection = mysql_connection

    @pytest.fixture(scope='function')
    def reg_random(self):
        response, username = self.client.add_random_user()
        yield response, username
        self.client.request('GET', location=f"/api/del_user/{username}")

    @allure.title('Получение статуса приложения')
    def test_status(self):
        """
        Тестируется /api/status.
        Шаги:
        1. Отправляется GET-запрос на /api/status.
        Ожидается статус-код 200 и {'status': 'ok'} в ответе
        """
        response = requests.get('http://127.0.0.1:8082' + '/status')
        assert response.status_code == 200
        assert response.json()['status'] == 'ok'

    @allure.title('Отправка запросов к API без авторизации')
    @pytest.mark.parametrize('url', [('POST', 'api/add_user'), ('GET', 'api/del_user/ikramanop'),
                                     ('GET', 'api/block_user/ikramanop'), ('GET', 'api/accept_user/ikramanop')])
    def test_api_negative_session(self, url):
        """
        Тестируется каждый api-метод на вызов без авторизации.
        Шаги:
        1. Отправляется GET-запрос на каждый из представленных в ТЗ эндпоинтов.
        Ожидается статус-код 401 в ответе на каждый запрос.
        """
        assert requests.request(method=url[0], url=f'http://127.0.0.1:8082/{url[1]}').status_code == 401

    @allure.story('Добавление пользователя')
    @allure.title('Позитивный тест добавления пользователя')
    def test_add_user_positive(self, reg_random):
        """
        Тестируется добавление валидного пользователя через api.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на добавление валидного пользователя.
        В ответе ожидается сообщение и статус-код 201.
        """
        response, username = reg_random

        assert response.text == 'User was added!'
        assert response.status_code == 201

    @allure.story('Добавление пользователя')
    @allure.title('Тест добавления пользователя без данных')
    def test_add_user_negative(self):
        """
        Тестируется добавление пользователя без данных.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на добавление пользователя без данных.
        В ответе ожидается статус-код 400.
        """
        response = self.client.request('POST', location='/api/add_user')

        assert response.status_code == 400

    @allure.story('Добавление пользователя')
    @allure.title('Тест добавления пользователя с null значениями')
    @pytest.mark.parametrize('fields', [(str(time())[:16], '12345678', None),
                                        (str(time())[:15], None, f'{str(time())[:16]}@22.com'),
                                        (None, '12345678', f'{str(time())[:16]}@22.com')])
    def test_add_user_null(self, fields):
        """
        Тестируется добавление пользователя с null значениями в полях.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на добавление пользователя с null значениями.
        В ответе ожидается сообщение об ошибке и статус-код 400.
        """
        username = str(time())[:16]

        data = {
            'username': fields[0],
            'password': fields[1],
            'email': fields[2]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = self.client.request('POST', url='http://127.0.0.1:8082/api/add_user', data=json.dumps(data),
                                       headers=headers)

        assert response.status_code == 400
        assert response.text == 'User was not added'
        assert self.connection.get_user(username) is None

        self.client.request('GET', location=f"/api/del_user/{username}")

    @allure.story('Добавление пользователя')
    @allure.title('Тест добавления пользователя с пустыми полями')
    @pytest.mark.parametrize('fields', [(str(time())[:16], '12345678', ''),
                                        (str(time())[:15], '', f'{str(time())[:16]}@22.com'),
                                        ('', '12345678', f'{str(time())[:16]}@22.com')])
    def test_add_user_empty(self, fields):
        """
        Тестируется добавление пользователя с пустыми значениями в полях.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на добавление пользователя с пустыми значениями.
        В ответе ожидается сообщение об ошибке и статус-код 400.
        """
        username = str(time())[:16]

        data = {
            'username': fields[0],
            'password': fields[1],
            'email': fields[2]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = self.client.request('POST', url='http://127.0.0.1:8082/api/add_user', data=json.dumps(data),
                                       headers=headers)

        assert response.status_code == 400
        assert response.text == 'User not was added'
        assert self.connection.get_user(username) is None

        self.client.request('GET', location=f"/api/del_user/{username}")

    @allure.story('Добавление пользователя')
    @allure.title('Тест добавления существующего пользователя')
    def test_add_user_exists(self):
        """
        Тестируется добавление существующего пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на добавление существующего пользователя.
        В ответе ожидается статус-код 304.
        """
        username = str(time())[:16]
        data = {
            'username': username,
            'password': '12345678',
            'email': 'asertolpas@gmail.com'
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = self.client.request('POST', url='http://127.0.0.1:8082/api/add_user', data=json.dumps(data),
                                       headers=headers)

        assert response.status_code == 304

        self.client.request('GET', location=f"/api/del_user/{username}")

    @allure.story('Удаление пользователя')
    @allure.title('Позитивный тест удаления пользователя')
    def test_delete_user_positive(self):
        """
        Тестируется удаление пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на удаление пользователя.
        В ответе ожидается статус-код 204.
        """
        response, username = self.client.add_random_user()

        response = self.client.request('GET', location=f"/api/del_user/{username}")

        assert response.status_code == 204

    @allure.story('Удаление пользователя')
    @allure.title('Негативный тест удаления пользователя')
    def test_delete_user_negative(self):
        """
        Тестируется удаление несуществующего пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на удаление несуществующего пользователя.
        В ответе ожидается статус-код 404.
        """
        username = str(time())[:16]

        response = self.client.request('GET', location=f"/api/del_user/{username}")

        assert response.status_code == 404

    @allure.story('Блокировка пользователя')
    @allure.title('Позитивный тест блокировки пользователя')
    def test_block_user_positive(self, reg_random):
        """
        Тестируется блокировка пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на блокировку пользователя.
        В ответе ожидается статус-код 200 и сообщение.
        """
        response, username = reg_random

        response = self.client.request('GET', location=f'api/block_user/{username}')

        assert response.status_code == 200
        assert response.text == 'User was blocked!'

    @allure.story('Блокировка пользователя')
    @allure.title('Тест блокировки несуществующего пользователя')
    def test_block_user_negative(self):
        """
        Тестируется блокировка несующествующего пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на блокировку несуществующего пользователя.
        В ответе ожидается статус-код 404.
        """
        username = str(time())[:16]
        response = self.client.request('GET', location=f'api/block_user/{username}')

        assert response.status_code == 404

    @allure.story('Блокировка пользователя')
    @allure.title('Тест блокировки пользователя дважды')
    def test_block_user_twice(self, reg_random):
        """
        Тестируется блокировка пользователя дважды.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Блокируется пользователь.
        3. Отправляется повторный запрос на блокировку пользователя.
        В ответе ожидается статус-код 304.
        """
        response, username = reg_random

        self.client.request('GET', location=f'api/block_user/{username}')
        response = self.client.request('GET', location=f'api/block_user/{username}')

        assert response.status_code == 304

    @allure.story('Разблокировка пользователя')
    @allure.title('Позитивный тест разблокировки пользователя')
    def test_unlock_user_positive(self, reg_random):
        """
        Тестируется разблокировка пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Блокируется пользователь.
        3. Отправляется запрос на разблокировку пользователя.
        В ответе ожидается статус-код 200 и сообщение.
        """
        response, username = reg_random

        self.client.request('GET', location=f'api/block_user/{username}')
        response = self.client.request('GET', location=f'api/accept_user/{username}')

        assert response.status_code == 200
        assert response.text == 'User access granted!'

    @allure.story('Разблокировка пользователя')
    @allure.title('Тест разблокировки несуществующего пользователя')
    def test_unlock_user_negative(self):
        """
        Тестируется разблокировка несующествующего пользователя.
        Шаги:
        1. Происходит авторизация в приложении.
        2. Отправляется запрос на разблокировку несуществующего пользователя.
        В ответе ожидается статус-код 404.
        """
        username = str(time())[:16]

        response = self.client.request('GET', location=f'api/accept_user/{username}')

        assert response.status_code == 404

    @allure.story('Разблокировка пользователя')
    @allure.title('Тест разблокировки пользователя дважды')
    def test_unlock_user_twice(self, reg_random):
        """
        Тестируется блокировка пользователя дважды.
        Шаги:
        1. Происходит авторизация в приложении.
        3. Отправляется запрос на разблокировку пользователя.
        В ответе ожидается статус-код 304.
        """
        response, username = reg_random

        response = self.client.request('GET', location=f'api/accept_user/{username}')

        assert response.status_code == 304
