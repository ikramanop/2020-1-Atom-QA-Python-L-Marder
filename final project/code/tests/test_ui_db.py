from time import time

import allure
import pytest
from decorators import screenshot_on_failure

from ui.pages.base_page import BasePage

from ui.pages.login_page import LoginPage

from ui.pages.reg_page import RegPage

from ui.pages.main_page import MainPage

from db.models.models import User


@pytest.mark.UI_DB
@allure.feature('UI_DB')
class TestDBUI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_connection, config, request):
        self.config = config
        self.connection = mysql_connection
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.reg_page: RegPage = request.getfixturevalue('reg_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

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
    def reg_ui(self):
        username = str(time())[:16]
        self.login_page.click(self.login_page.locators.GOTO_REGISTER)
        self.reg_page.register(username, f'{username}@kfe.ww', '1234567890')

        yield username, self.main_page

        self.connection.delete_user(username)

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Тестирование логина')
    def test_login_ui(self, add_user):
        """
        Тестируется форма логина.
        Шаги:
        1. В базу добавляется пользователь.
        2. Происходит авторизация пользователя.
        Ожидается, что в базе проставится active = 1 и время входа.
        """
        username = add_user
        self.login_page.login(username, '1234567890')
        assert self.connection.get_user(username).start_active_time is not None
        assert self.connection.get_user(username).active == 1

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Тестирование логаута')
    def test_logout_ui(self, add_user):
        """
        Тестируется кнопка логаута.
        Шаги:
        1. В базу добавляется пользователь.
        2. Происходит авторизация пользователя.
        3. На главной странице нажимается кнопка логаута
        Ожидается, что в базе проставится active = 0.
        """
        username = add_user
        self.login_page.login(username, '1234567890')
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        assert self.connection.get_user(username).active == 0

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Тестирование логина за заблокированного пользователя')
    def test_login_ui_blocked(self, add_user_blocked):
        """
        Тестируется форма логина с заблокированным пользователем.
        Шаги:
        1. В базу добавляется пользователь.
        2. Происходит авторизация пользователя.
        Ожидается, что в на странице появится сообщение об ошибке.
        """
        username = add_user_blocked
        self.login_page.login(username, '1234567890')

        elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)
        while elem.text == '':
            elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)

        assert elem.text == "Ваша учетная запись заблокирована"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Тестирование логина после регистрации')
    def test_reg_ui_login(self, reg_ui):
        """
        Тестируется форма регистрации и логин после регистрации.
        Шаги:
        1. Переход на форму регистрации.
        2. Регистрируется пользователь.
        Ожидается, что в базе появится пользователь, ему проставится active = 1 и время входа.
        """
        username, main_page = reg_ui

        assert self.connection.get_user(username) is not None
        assert self.connection.get_user(username).active == 1
        assert self.connection.get_user(username).start_active_time is not None

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Тестирование логаута после регистрации')
    def test_reg_ui_logout(self, reg_ui):
        """
        Тестируется форма регистрации и логаут после регистрации.
        Шаги:
        1. Переход на форму регистрации.
        2. Регистрируется пользователь.
        3. На главной странице нажимается кнопка логаута.
        Ожидается, что в базе появится пользователь, ему проставится active = 1.
        """
        username, main_page = reg_ui
        main_page.click(main_page.locators.LOGOUT_BUTTON)
        assert self.connection.get_user(username).active == 0
        assert self.connection.get_user(username).start_active_time is not None
