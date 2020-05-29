import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.reg_page import RegPage

from ui.pages.main_page import MainPage

from ui.pages.outer_page import OuterPage


@pytest.fixture(scope='function')
def base_page(sel_driver):
    return BasePage(sel_driver)


@pytest.fixture(scope='function')
def login_page(sel_driver):
    return LoginPage(sel_driver)


@pytest.fixture(scope='function')
def reg_page(sel_driver):
    return RegPage(sel_driver)


@pytest.fixture(scope='function')
def main_page(sel_driver):
    return MainPage(sel_driver)


@pytest.fixture(scope='function')
def outer_page(sel_driver):
    return OuterPage(sel_driver)


@pytest.fixture(scope='function')
def sel_driver(config):
    url = config['url']
    selenoid = config['selenoid']

    options = ChromeOptions()

    if selenoid == 'None':
        manager = ChromeDriverManager(version='80.*')
        driver = webdriver.Chrome(
            executable_path=manager.install(),
            options=options
        )

    else:
        capabilities = {
            'acceptInsecureCerts': True,
            'browserName': 'chrome',
            'version': '80.0'
        }

        driver = webdriver.Remote(
            command_executor='http://' + selenoid + '/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )

    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()
