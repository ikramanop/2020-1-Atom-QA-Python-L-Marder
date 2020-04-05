import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from ui.page.base import BasePage
from ui.page.login import LoginPage
from ui.page.main_page import MainPage

from ui.page.error_login import ErrorLoginPage
from ui.page.create_campaign import CreateCampaignPage
from ui.page.create_segment import CreateSegmentPage


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver)


@pytest.fixture(scope='function')
def error_login_page(driver):
    return ErrorLoginPage(driver)


@pytest.fixture(scope='function')
def create_campaign_page(driver):
    return CreateCampaignPage(driver)


@pytest.fixture(scope='function')
def create_segment_page(driver):
    return CreateSegmentPage(driver)


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    selenoid = config['selenoid']

    options = ChromeOptions()

    if selenoid == 'None':
        manager = ChromeDriverManager(version='80.*')
        driver = webdriver.Chrome(executable_path=manager.install(),
                                  options=options
                                  )
    else:
        capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': '80.0',
                        }

        driver = webdriver.Remote(command_executor='http://' + selenoid + '/wd/hub/',
                                  options=options,
                                  desired_capabilities=capabilities
                                  )

    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.close()

