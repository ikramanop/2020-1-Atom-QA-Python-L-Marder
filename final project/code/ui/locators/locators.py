from selenium.webdriver.common.by import By


class BaseLocators:
    pass


class LoginPageLocators:
    LOGIN_BUTTON = (By.XPATH, '//input[@id="submit"]')
    USERNAME = (By.XPATH, '//input[@id="username"]')
    PASSWORD = (By.XPATH, '//input[@id="password"]')

    LOGIN_ERROR = (By.XPATH, '//div[@id="flash"]')

    LOGIN_FORM = (By.XPATH, '//div[@class="uk-card uk-card-default uk-card-hover uk-card-body uk-width-large"]')
    GOTO_REGISTER = (By.XPATH, '//a[@href="/reg"]')


class RegPageLocators:
    REG_BUTTON = (By.XPATH, '//input[@id="submit"]')
    USERNAME = (By.XPATH, '//input[@id="username"]')
    EMAIL = (By.XPATH, '//input[@id="email"]')
    PASSWORD = (By.XPATH, '//input[@id="password"]')
    PASSWORD_CONFIRM = (By.XPATH, '//input[@id="confirm"]')
    CHECKBOX = (By.XPATH, '//input[@id="term"]')

    REG_ERROR = (By.XPATH, '//div[@id="flash"]')

    REG_FORM = (By.XPATH, 'uk-card uk-card-default uk-card-hover uk-card-body uk-width-large')
    GOTO_LOGIN = (By.XPATH, '//a[@href="/login"]')


class MainPageLocators:
    MAIN_BLOCK = (By.XPATH, '//div[@class="uk-grid uk-margin-large-top uk-width-1-2 uk-container-center"]')
    NAVBAR_BLOCK = (By.XPATH, '//nav[@class="uk-navbar"]')

    API_BUTTON = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    FUTURE_BUTTON = (
        By.XPATH,
        '//a[@href="https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"]')
    SMTP_BUTTON = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')

    HOME_BUTTON = (By.XPATH, '//li/a[@href="/"]')
    PYTHON_BUTTON = (By.XPATH, '//li/a[@href="https://www.python.org/"]')
    PYTHON_HISTORY_BUTTON = (By.XPATH, '//li/a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    ABOUT_FLASK_BUTTON = (By.XPATH, '//li/a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    LINUX_SHADE = (By.XPATH, '//li/a[@href and contains(text(), "Linux")]')
    DOWNLOAD_CENTOS_BUTTON = (By.XPATH, '//li/a[@href="https://getfedora.org/ru/workstation/download/"]')
    NETWORK_SHADE = (By.XPATH, '//li/a[@href and contains(text(), "Network")]')
    TCPDUMP_EXAMPLE_BUTTON = (By.XPATH, '//li/a[@href="https://hackertarget.com/tcpdump-examples/"]')
    WIRESHARK_NEWS_BUTTON = (By.XPATH, '//li/a[@href="https://www.wireshark.org/news/"]')
    WIRESHARK_DOWNLOAD_BUTTON = (By.XPATH, '//li/a[@href="https://www.wireshark.org/#download"]')

    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')
    LOGIN_NAME = (By.XPATH, '//div[@id="login-name"]')


class OuterPageLocators:
    PYTHON_LOGO = (By.XPATH, '//img[@class="python-logo"]')
    HISTORY_OF_PYTHON = (By.XPATH, '//h1[contains(text(), "History of Python")]')
    FLASK_LOGO = (By.XPATH, '//img[@alt="Flask: web development, one drop at a time"]')
    CENTOS_LOGO = (By.XPATH, '//img[@src="/centos-design/images/centos-logo-white.png"]')
    TCPDUMP_EXAMPLE = (By.XPATH, '//h1[contains(text(), "Tcpdump Examples")]')
    WIRESHARK_LOGO = (By.XPATH, '//a[@href="/"]/img')
    WIRESHARK_DOWNLOAD = (By.XPATH, '//h1[contains(text(), "Download")]')
    API = (By.XPATH, '//h1[contains(text(), "Application programming interface")]')
    FUTURE_OF_WEB = (By.XPATH, '//h1[contains(text(), "What Will the Internet Be Like in the Next 50 Years?")]')
    SMTP = (By.XPATH, '//h1[contains(text(), "SMTP")]')
