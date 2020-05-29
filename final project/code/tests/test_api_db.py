from time import time

import allure
import pytest
import requests

from ui.pages.base_page import BasePage

from db.models.models import User
from requests.cookies import cookiejar_from_dict

from api.client.client import ApiClient


@pytest.mark.API_DB
@allure.feature('API_DB')
class TestDBUI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_connection, api_client, config):
        self.config = config
        self.connection = mysql_connection
        self.client = api_client

    @pytest.fixture(scope='function')
    def add_user(self):
        username = str(time())[:16]
        self.connection.add_user(
            User(
                username=username,
                password='1234567890',
                email=f'{username}@nusr.et',
                access=1,
                active=0
            )
        )

        yield username

        self.connection.delete_user(username)

    @pytest.fixture(scope='function')
    def add_user_empty(self):
        username = str(time())[:16]
        self.connection.add_user(User(
            username=username,
            password='',
            email=f'{username}@nusr.et',
            access=1,
            active=0
        ))

        yield username

        self.connection.delete_user(username)

    @pytest.fixture(scope='function')
    def add_user_blocked(self):
        username = str(time())[:16]
        self.connection.add_user(User(
            username=username,
            password='1234567890',
            email=f'{username}@nusr.et',
            access=0,
            active=0
        ))

        yield username

        self.connection.delete_user(username)

    @pytest.fixture(scope='function')
    def add_random(self):
        response, username = self.client.add_random_user()
        yield response, username
        self.client.request('GET', location=f"/api/del_user/{username}")

    @pytest.fixture(scope='function')
    def add_random_no_del(self):
        response, username = self.client.add_random_user()
        return response, username

    @pytest.fixture(scope='function')
    def add_random_null(self):
        response, username = self.client.add_random_user_null_password()
        yield response, username
        self.client.request('GET', location=f"/api/del_user/{username}")

    @pytest.fixture(scope='function')
    def add_random_empty(self):
        response, username = self.client.add_random_user_empty_password()
        yield response, username
        self.client.request('GET', location=f"/api/del_user/{username}")

    @pytest.fixture(scope='function')
    def reg_api(self):
        username = str(time())[:16]
        data = {
            'username': username,
            'email': f'{username}@jj.ek',
            'password': '333',
            'confirm': '333',
            'term': 'y',
            'submit': 'Register'
        }

        session = requests.Session()
        response = session.post('http://127.0.0.1:8082' + '/reg', data=data, allow_redirects=False)
        cookie = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
        session.cookies = cookiejar_from_dict(
            {
                'session': cookie
            }
        )
        session.get('http://127.0.0.1:8082' + '/welcome')

        yield username, session

        self.connection.delete_user(username)

    @allure.story('Добавление пользователя')
    @allure.title('Позитивный тест добавления пользователя')
    def test_add_user(self, add_random):
        """
        Тестируется добавление пользователя через API.
        Шаги:
        1. Через API добавляется пользователь.
        Ожидается, что в базе данных появится новый пользователь.
        """
        response, username = add_random
        assert self.connection.get_user(username) is not None

    @allure.story('Добавление пользователя')
    @allure.title('Негативный тест добавления пользователя: null пароль')
    def test_add_user_negative_null_password(self, add_random_null):
        """
        Тестируется добавление пользователя с null паролем через API.
        Шаги:
        1. Через API добавляется пользователь с null паролем.
        Ожидается, что в базе данных новый пользователь не появится.
        """
        response, username = add_random_null
        assert self.connection.get_user(username) is None

    @allure.story('Добавление пользователя')
    @allure.title('Негативный тест добавления пользователя: пустой пароль')
    def test_add_user_negative_empty_password(self, add_random_empty):
        """
        Тестируется добавление пользователя с пустым паролем через API.
        Шаги:
        1. Через API добавляется пользователь с пустым паролем.
        Ожидается, что в базе данных новый пользователь не появится.
        """
        response, username = add_random_empty
        assert self.connection.get_user(username) is None

    @allure.story('Удаление пользователя')
    @allure.title('Тест удаления пользователя')
    def test_delete_user(self, add_random_no_del):
        """
        Тестируется удаление пользователя через API.
        Шаги:
        1. Через API добавляется пользователь.
        2. Пользователь удаляется.
        Ожидается, что в базе данных не будет пользователя.
        """
        response, username = add_random_no_del
        self.client.request('GET', location=f"/api/del_user/{username}")
        assert self.connection.get_user(username) is None

    @allure.story('Блокировка пользователя')
    @allure.title('Тест блокировки пользователя')
    def test_block_user_api(self, add_user):
        """
        Тестируется блокировка пользователя через API.
        Шаги:
        1. Через API добавляется пользователь.
        2. Пользователь блокируется.
        Ожидается, что в базе данных пользователю проставится access = 0.
        """
        username = add_user
        self.client.request(method='GET', location=f'/api/block_user/{username}')
        assert self.connection.get_user(username).access == 0

    @allure.story('Разблокировка пользователя')
    @allure.title('Тест разблокировки пользователя')
    def test_accept_user_api(self, add_user):
        """
        Тестируется разблокировка пользователя через API.
        Шаги:
        1. Через API добавляется пользователь.
        2. Пользователь блокируется.
        3. Пользователь разблокируется.
        Ожидается, что в базе данных пользователю проставится access = 1.
        """
        username = add_user
        self.client.request(method='GET', location=f'/api/block_user/{username}')
        self.client.request(method='GET', location=f'/api/accept_user/{username}')
        assert self.connection.get_user(username).access == 1

    @allure.story('Логин')
    @allure.title('Позитивный тест логина')
    def test_login_api(self, add_user):
        """
        Тестируется логин пользователя через API.
        Шаги:
        1. Через базу данных добавляется пользователь.
        2. Происходит логин через API.
        Ожидается, что в базе данных пользователю проставится active = 1 и время входа.
        """
        username = add_user
        ApiClient(username, '1234567890', 'http://127.0.0.1:8082')
        assert self.connection.get_user(username).start_active_time is not None
        assert self.connection.get_user(username).active == 1

    @allure.story('Логин')
    @allure.title('Тест логина с пустым паролем')
    def test_login_api_empty_passwd(self, add_user_empty):
        """
        Тестируется логин пользователя с пустым паролем через API.
        Шаги:
        1. Через базу данных добавляется пользователь с пустым паролем.
        2. Происходит логин через API.
        Ожидается, что в авторизация не пойдёт и не проставятся поля active и start_active_time.
        """
        username = add_user_empty
        ApiClient(username, '', 'http://127.0.0.1:8082')
        assert self.connection.get_user(username).start_active_time is None
        assert self.connection.get_user(username).active == 0

    @allure.story('Логин')
    @allure.title('Тест логина заблокированного пользователя')
    def test_login_api_blocked(self, add_user_blocked):
        """
        Тестируется логин заблокированного пользователя через API.
        Шаги:
        1. Через базу данных добавляется заблокированный пользователь.
        2. Происходит логин через API.
        Ожидается, что пользователю не сможет авторизоваться и ему не проставится время входа.
        """
        username = add_user_blocked
        ApiClient(username, '1234567890', 'http://127.0.0.1:8082')
        assert self.connection.get_user(username).start_active_time is None

    @allure.story('Логин')
    @allure.title('Тест логаута')
    def test_logout_api(self, add_user):
        """
        Тестируется логаут пользователя через API.
        Шаги:
        1. Через базу данных добавляется пользователь.
        2. Происходит логин через API.
        3. Происходит логаут через API.
        Ожидается, что пользователю проставится active = 0.
        """
        username = add_user
        client = ApiClient(username, '1234567890', 'http://127.0.0.1:8082')
        client.logout()
        assert self.connection.get_user(username).active == 0

    @allure.story('Регистрация')
    @allure.title('Позитивный тест регистрации')
    def test_reg_api_login(self, reg_api):
        """
        Тестируется регистрация пользователя через API.
        Шаги:
        1. Происходит регистрация через API.
        Ожидается, что пользователь зарегистрируется и появится в базе, ему проставится active = 1 и время входа.
        """
        username, session = reg_api
        assert self.connection.get_user(username) is not None
        assert self.connection.get_user(username).active == 1
        assert self.connection.get_user(username).start_active_time is not None

    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации')
    @pytest.mark.parametrize('fields', [('333', '333', 'n'), ('333', '33', 'y'), ('333', '33', 'n')])
    def test_reg_api_negative(self, fields):
        """
        Тестируется регистрация пользователя с ошибками в соглашении и пароле через API.
        Шаги:
        1. Происходит регистрация пользователя с негативным соглашением через API.
        Ожидается, что пользователь не зарегистрируется и не появится в базе.
        """
        username = str(time())[:16]
        data = {
            'username': username,
            'email': f'{username}@jj.ek',
            'password': fields[0],
            'confirm': fields[1],
            'term': fields[2],
            'submit': 'Register'
        }

        session = requests.Session()
        response = session.post('http://127.0.0.1:8082' + '/reg', data=data, allow_redirects=False)
        cookie = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
        session.cookies = cookiejar_from_dict(
            {
                'session': cookie
            }
        )
        session.get('http://127.0.0.1:8082' + '/welcome')

        assert self.connection.get_user(username) is None

    @allure.story('Регистрация')
    @allure.title('Тест логаута после регистрации')
    def test_reg_api_logout(self, reg_api):
        """
        Тестируется регистрация пользователя через API.
        Шаги:
        1. Происходит регистрация через API.
        2. Происходит логаут через API.
        Ожидается, что проставится active = 0 и будет информация о времени входа.
        """
        username, session = reg_api
        session.get(url='http://127.0.0.1:8082' + '/logout')
        assert self.connection.get_user(username).active == 0
        assert self.connection.get_user(username).start_active_time is not None
