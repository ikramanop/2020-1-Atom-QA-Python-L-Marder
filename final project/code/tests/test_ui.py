from time import time, sleep

import allure
import pytest
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage

from ui.pages.reg_page import RegPage

from ui.pages.main_page import MainPage

from faker import Faker

from ui.pages.outer_page import OuterPage

from decorators import screenshot_on_failure


@allure.feature('UI')
@pytest.mark.UI
class TestUI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, sel_driver, config, request, mysql_connection):
        self.driver = sel_driver
        self.config = config
        self.mysql_connection = mysql_connection
        self.fake = Faker()
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.reg_page: RegPage = request.getfixturevalue('reg_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.outer_page: OuterPage = request.getfixturevalue('outer_page')

    @pytest.fixture(scope='function')
    def login_vk(self):
        self.login_page.login('ikramanop', '1234567890')
        yield self.main_page
        self.driver.get(self.config['url'])
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)

    @pytest.fixture(scope='function')
    def login_no_vk(self):
        self.login_page.login('k12f2432', '1234567890')
        yield self.main_page
        self.driver.get(self.config['url'])
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)

    @pytest.fixture(scope='function')
    def reg(self):
        self.login_page.click(self.login_page.locators.GOTO_REGISTER)
        username = str(time())[:16]
        yield self.reg_page, username
        self.mysql_connection.delete_user(username)

    @pytest.fixture(scope='function')
    def reg_logout(self):
        self.login_page.click(self.login_page.locators.GOTO_REGISTER)
        username = str(time())[:16]
        email = f'{username}@aa.aa'
        self.reg_page.register(username, email, '11')
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        self.login_page.click(self.login_page.locators.GOTO_REGISTER)
        yield self.reg_page, username, email
        self.mysql_connection.delete_user(username)

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Позитивный тест логина')
    def test_login_positive(self):
        """
        Тестируется форма логина.
        Происходит авторизация действительного пользователя.
        Шаги:
        1. Вводятся действительные данные пользователя.
        2. Нажимается кнопка логина.
        Ожидается, что загрузится главная страница.
        Проверяется нахождение на главной странице.
        """
        self.login_page.login('ikramanop', '1234567890')
        assert self.main_page.find(self.main_page.locators.MAIN_BLOCK)
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Негативный тест логина: несуществующий пользователь')
    def test_login_negative_invalid(self):
        """
        Тестируется форма логина.
        Происходит авторизация несуществующего пользователя.
        Шаги:
        1. Вводятся несуществующие данные пользователя.
        2. Нажимается кнопка логина.
        Ожидается, что появится соответствующее сообщение об ошибке.
        Проверяется наличие сообщения об ошибке.
        """
        self.login_page.login('123456', '11')

        elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)
        while elem.text == '':
            elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)

        assert elem.text == "Invalid username or password"

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Негативный тест логина: длина имени пользователя')
    @pytest.mark.parametrize('user', ['1234', '123456789000000000'])
    def test_login_negative_length(self, user):
        """
        Тестируется форма логина.
        Происходит авторизация пользователя с неккоректной длиной пользователя (короткое или длинное).
        Шаги:
        1. Вводятся данные пользователя с неккоректной длиной пользователя (короткое или длинное).
        2. Нажимается кнопка логина.
        Ожидается, что появится соответствующее сообщение об ошибке.
        Проверяется наличие сообщения об ошибке.
        """
        self.login_page.login('1234', '11')

        elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)
        while elem.text == '':
            elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)

        assert elem.text == "Incorrect username length"

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Негативный тест логина: пароль с пробелами')
    def test_login_negative_passwd_space(self):
        """
        Тестируется форма логина.
        Происходит авторизация пользователя с паролем с пробелами.
        Шаги:
        1. Вводятся данные пользователя с паролем с пробелами.
        2. Нажимается кнопка логина.
        Ожидается, что появится соответствующее сообщение об ошибке (пустой пароль).
        Проверяется наличие сообщения об ошибке.
        """
        self.login_page.login('ikramanop', '   ')

        elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)
        while elem.text == '':
            elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)

        assert elem.text == "Необходимо указать пароль для авторизации"

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Негативный тест логина: несколько ошибок')
    @pytest.mark.parametrize('user', ['1234', '123456789000000000'])
    def test_login_negative_multiple_errors(self, user):
        """
        Тестируется форма логина.
        Происходит авторизация пользователя с несколькими ошибками (длина и пустой пароль)
        Шаги:
        1. Вводятся данные пользователя с паролем с пробелами и неккоректной длиной имени пользователя.
        2. Нажимается кнопка логина.
        Ожидается, что появятся все сообщения о полученных ошибках в читаемом формате.
        Проверяется наличие сообщения об ошибке.
        """
        self.login_page.login(user, '   ')

        elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)
        while elem.text == '':
            elem = self.login_page.find(self.login_page.locators.LOGIN_ERROR)

        assert elem.text == "Incorrect username length\nНеобходимо указать пароль для авторизации"

    @screenshot_on_failure
    @allure.story('Логин')
    @allure.title('Тест логаута')
    def test_login_logout(self):
        """
        Тестируется логаут пользователя.
        Шаги:
        1. Происходит авторизация пользователя.
        2. Нажимается кнопка логаута.
        Ожидается, что конечной точкой будет страница логина.
        Проверка по форме логина.
        """
        self.login_page.login('ikramanop', '1234567890')

        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)

        assert self.login_page.find(self.login_page.locators.LOGIN_FORM)

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест данных: имя + вк')
    def test_mainpage_creds(self, login_vk):
        """
        Тестируется нахождение данных с именем пользователя и VK ID.
        Шаги:
        1. Вводятся данные пользователя с существующим VK ID.
        2. Нажимается кнопка логина.
        Ожидается наличие данных с именем пользователя и VK ID.
        Проверка по содержимому web-элемента.
        """
        main_page = login_vk

        elem = main_page.find(main_page.locators.LOGIN_NAME)

        assert elem.text == 'Logged as ikramanop\nVK ID: 315368721'

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест данных: только имя')
    def test_mainpage_creds_no_vk(self, login_no_vk):
        """
        Тестируется нахождение данных с именем пользователя и без VK ID.
        Шаги:
        1. Вводятся данные пользователя без VK ID.
        2. Нажимается кнопка логина.
        Ожидается наличие данных с именем пользователя и без VK ID.
        Проверка по содержимому web-элемента.
        """
        main_page = login_no_vk

        elem = main_page.find(main_page.locators.LOGIN_NAME)

        assert elem.text == 'Logged as k12f2432'

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест данных: кнопка "Home"')
    def test_mainpage_home(self, login_vk):
        """
        Тестирование кнопки "Home".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Нажимается кнопка "Home".
        Ожидается, что загрузится главная страница.
        Проверка по url страницы.
        """
        main_page = login_vk

        main_page.click(main_page.locators.HOME_BUTTON)

        assert self.driver.current_url == self.config['url'] + '/welcome/'

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Python"')
    def test_mainpage_python(self, login_vk):
        """
        Тестирование кнопки "Python".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Нажимается кнопка "Python".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию лого Python.
        """
        main_page = login_vk

        main_page.click(main_page.locators.PYTHON_BUTTON)

        elem = self.outer_page.find(self.outer_page.locators.PYTHON_LOGO)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Python history"')
    def test_mainpage_python_history(self, login_vk):
        """
        Тестирование кнопки "Python history".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Наводится курсор на "Python"
        3. Нажимается кнопка "Python history".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию заголовка "History of Python".
        """
        main_page = login_vk

        main_page.cursor_to(main_page.locators.PYTHON_BUTTON)

        main_page.click(main_page.locators.PYTHON_HISTORY_BUTTON)

        elem = self.outer_page.find(self.outer_page.locators.HISTORY_OF_PYTHON)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "About Flask"')
    def test_mainpage_about_flask(self, login_vk):
        """
        Тестирование кнопки "About Flask".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Наводится курсор на "Python"
        3. Нажимается кнопка "About Flask".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию лого Flask.
        """
        main_page = login_vk

        main_page.cursor_to(main_page.locators.PYTHON_BUTTON)

        main_page.click(main_page.locators.ABOUT_FLASK_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.FLASK_LOGO)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Download Centos7"')
    def test_mainpage_download_centos7(self, login_vk):
        """
        Тестирование кнопки "Download Centos7".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Наводится курсор на "Linux"
        3. Нажимается кнопка "Download Centos7".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию лого Centos.
        """
        main_page = login_vk

        main_page.cursor_to(main_page.locators.LINUX_SHADE)

        main_page.click(main_page.locators.DOWNLOAD_CENTOS_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.CENTOS_LOGO)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Tcpdump Example"')
    def test_mainpage_tcpdump_example(self, login_vk):
        """
        Тестирование кнопки "Tcpdump Example".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Наводится курсор на "Network"
        3. Нажимается кнопка "Tcpdump Example".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию заголовка "Tcpdump Examples".
        """
        main_page = login_vk

        main_page.cursor_to(main_page.locators.NETWORK_SHADE)

        main_page.click(main_page.locators.TCPDUMP_EXAMPLE_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.TCPDUMP_EXAMPLE)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Wireshark News"')
    def test_mainpage_wireshark_news(self, login_vk):
        """
        Тестирование кнопки "Wireshark News".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Наводится курсор на "Network"
        3. Нажимается кнопка "Wireshark News".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию лого Wireshark.
        """
        main_page = login_vk

        main_page.cursor_to(main_page.locators.NETWORK_SHADE)

        main_page.click(main_page.locators.WIRESHARK_NEWS_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.WIRESHARK_LOGO)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Wireshark Download"')
    def test_mainpage_wireshark_download(self, login_vk):
        """
        Тестирование кнопки "Wireshark Download".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Наводится курсор на "Network"
        3. Нажимается кнопка "Wireshark Download".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию заголовка "Download".
        """
        main_page = login_vk

        main_page.cursor_to(main_page.locators.NETWORK_SHADE)

        main_page.click(main_page.locators.WIRESHARK_DOWNLOAD_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.WIRESHARK_DOWNLOAD)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "What is an API?"')
    def test_mainpage_api(self, login_vk):
        """
        Тестирование кнопки "What is an API?".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Нажимается кнопка "What is an API?".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию заголовка "Application programming interface".
        """
        main_page = login_vk

        main_page.click(main_page.locators.API_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.API)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Future of internet"')
    def test_mainpage_future(self, login_vk):
        """
        Тестирование кнопки "Future of internet".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Нажимается кнопка "Future of internet".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию заголовка "What Will the Internet Be Like in the Next 50 Years?".
        """
        main_page = login_vk

        main_page.click(main_page.locators.FUTURE_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.FUTURE_OF_WEB)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Главная страница')
    @allure.title('Тест кнопки "Lets talk about SMTP?"')
    def test_mainpage_smtp(self, login_vk):
        """
        Тестирование кнопки "Lets talk about SMTP?".
        Шаги:
        1. Происходит авторизация пользователя.
        2. Нажимается кнопка "Lets talk about SMTP?".
        Ожидается, что загрузится соответсвующая страница.
        Проверка по наличию заголовка "SMTP".
        """
        main_page = login_vk

        main_page.click(main_page.locators.SMTP_BUTTON)

        while len(self.driver.window_handles) != 2:
            sleep(0.1)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        elem = self.outer_page.find(self.outer_page.locators.SMTP)

        assert elem is not None

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Позитивный тест логина')
    def test_reg_positive(self, reg):
        """
        Тестирование страницы регистрации.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся валидные для регистрации данные.
        3. Нажимается кнопка регистрации.
        Ожидается, пользователь будет зарегистрирован и откроется главная страница.
        Проверка по главной странице
        """
        reg_page, username = reg

        reg_page.register(username, 'ii@ii.ii', '11')

        assert self.main_page.find(self.main_page.locators.MAIN_BLOCK)

        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Позитивный тест регистрации')
    def test_reg_negative_mail_length(self, reg):
        """
        Тестируется форма регистрации.
        Ввод данных, валидных для регистрации.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся валидные для регистрации данные.
        3. Нажимается кнопка регистрации.
        Ожидается, пользователь будет зарегистрирован и откроется главная страница.
        Проверка по главной странице.
        """
        reg_page, username = reg

        reg_page.register(username, 'ii', '11')

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        assert elem.text == "Incorrect email length"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации: неккоректная почта')
    def test_reg_negative_mail_invalid(self, reg):
        """
        Тестируется форма регистрации.
        Ввод данных с неккоректной почтой.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся данные с неккоректной почтой.
        3. Нажимается кнопка регистрации.
        Ожидается, что будет выведена соответствующая ошибка.
        Проверка по сообщению.
        """
        reg_page, username = reg

        reg_page.register(username, '11@11.11', '11')

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        assert elem.text == "Invalid email address"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации: разные пароли')
    def test_reg_negative_password(self, reg):
        """
        Тестируется форма регистрации.
        Ввод данных с разными паролями.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся данные с разными паролями.
        3. Нажимается кнопка регистрации.
        Ожидается, что будет выведена соответствующая ошибка.
        Проверка по сообщению.
        """
        reg_page, username = reg

        reg_page.register(username, 'ii@ii.ii', '11', '1')

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        assert elem.text == "Passwords must match"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации: длина имени пользователя')
    @pytest.mark.parametrize('user', ['1', '111111111111111111111111'])
    def test_reg_negative_user_length(self, reg, user):
        """
        Тестируется форма регистрации.
        Ввод данных с неккоректной длиной логина.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся данные с неккоректной длиной логина (слишком короткий и слишком длинный)
        3. Нажимается кнопка регистрации.
        Ожидается, что будет выведена соответствующая ошибка.
        Проверка по сообщению.
        """
        reg_page, username = reg

        reg_page.register(user, 'ii@ii.ii', '11')

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        assert elem.text == "Incorrect username length"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации: существующий пользователь')
    def test_reg_negative_user_exists(self, reg_logout):
        """
        Тестируется форма регистрации.
        Ввод данных с существующем именем пользователя.
        Предварительные шаги:
        1. Добавляется пользователь.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся данные существующего пользователя.
        3. Нажимается кнопка регистрации.
        Ожидается, что будет выведена соответствующая ошибка.
        Проверка по сообщению.
        """
        reg_page, username, email = reg_logout

        reg_page.register(username, 'ii@ii.ii', '11')

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        assert elem.text == "User already exist"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации: занятая почта')
    def test_reg_negative_mail_taken(self, reg_logout):
        """
        Тестируется форма регистрации.
        Ввод данных с занятой почтой
        Предварительные шаги:
        1. Добавляется пользователь.
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся данные с уже занятой почтой.
        3. Нажимается кнопка регистрации.
        Ожидается, что будет выведена соответствующая ошибка.
        Проверка по сообщению.
        """
        reg_page, username, email = reg_logout

        reg_page.register('jkrb2u3yg', email, '11')

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        assert elem.text == "Email already taken"

    @screenshot_on_failure
    @allure.story('Регистрация')
    @allure.title('Негативный тест регистрации: несколько ошибок')
    @pytest.mark.parametrize('data',
                             enumerate([(str(time())[:16], '22', '1', '22'), (str(time())[:16], '22@22', '1', '22'),
                                        (str(time()), '22@22.22', '1', '22')]))
    def test_reg_negative_multiple_errors(self, reg, data):
        """
        Тестируется форма регистрации.
        Ввод данных с занятой почтой
        Шаги:
        1. Происходит переход на страницу регистрации.
        2. Вводятся данные с различными ошибками.
        3. Нажимается кнопка регистрации.
        Ожидается, что будут выведены все сообщения об ошибках в привычном виде.
        Проверка по сообщению.
        """
        reg_page, username = reg
        reg_page.register(*data[1])

        elem = reg_page.find(reg_page.locators.REG_ERROR)
        while elem.text == '':
            elem = reg_page.find(reg_page.locators.REG_ERROR)

        if data[0] == 0:
            assert elem.text == "Incorrect email length\nPasswords must match"
        if data[0] == 1:
            assert elem.text == "Invalid email address\nPasswords must match"
        if data[0] == 2:
            assert elem.text == "Incorrect username length\nPasswords must match"
