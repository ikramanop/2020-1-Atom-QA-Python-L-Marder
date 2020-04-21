from time import time

import pytest
from selenium.common.exceptions import NoSuchElementException

from ui.page.base import BasePage
from ui.page.login import LoginPage
from ui.page.main_page import MainPage
from ui.page.error_login import ErrorLoginPage
from ui.page.create_campaign import CreateCampaignPage
from ui.page.create_segment import CreateSegmentPage


class TestUI:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.error_login_page: ErrorLoginPage = request.getfixturevalue('error_login_page')
        self.create_campaign_page: CreateCampaignPage = request.getfixturevalue('create_campaign_page')
        self.create_segment_page: CreateSegmentPage = request.getfixturevalue('create_segment_page')

    @pytest.fixture(scope='function')
    def login(self):
        self.login_page.login('target_test_123@inbox.ru', 'qwerty1234')
        return self.main_page

    @pytest.fixture(scope='function')
    def create_segment(self, login):
        main_page = login
        main_page.click(main_page.locators.AUDS_LOCATOR)
        main_page.click(main_page.locators.CREATE_SEGMENT)
        name = str(time())
        self.create_segment_page.create_segment(name)
        yield self.main_page
        main_page.click(main_page.locators.cross_segment(name))
        main_page.click(main_page.locators.DELETE_SEGMENT)

    @pytest.fixture(scope='function')
    def create_campaign(self, login):
        main_page = login
        main_page.find(self.main_page.locators.EMPTY_CAMPAIGNS)
        main_page.click(self.main_page.locators.CREATE_CAMPAIGN)
        self.create_campaign_page.create_campaign()
        yield self.main_page
        main_page.click(main_page.locators.TOGGLE_BOX)
        main_page.click(main_page.locators.BANNER_LOCATOR)
        main_page.click(main_page.locators.BANNER_CHECKBOX)
        main_page.click(main_page.locators.BANNER_ACTIONS)
        main_page.click(main_page.locators.BANNER_DELETE)

    @pytest.mark.UI
    def test_login_positive(self):
        self.login_page.login('target_test_123@inbox.ru', 'qwerty1234')
        self.base_page.find(self.main_page.locators.EMPTY_CAMPAIGNS)
        assert self.driver.find_element(*self.main_page.locators.EMPTY_CAMPAIGNS)

    @pytest.mark.UI
    def test_login_negative(self):
        self.login_page.login('49868937324', 'sjhdfhjsefusef')
        self.base_page.find(self.error_login_page.locators.ERROR_LOCATOR)
        assert self.driver.find_element(*self.error_login_page.locators.ERROR_LOCATOR)

    @pytest.mark.UI
    def test_create_campaign(self, create_campaign):
        main_page = create_campaign
        main_page.find(main_page.locators.TOGGLE_BOX)
        assert self.driver.find_element(*main_page.locators.TOGGLE_BOX)
        assert self.driver.find_element(*main_page.locators.RELOAD_BUTTON)

    @pytest.mark.UI
    def test_segment_creation(self, create_segment):
        main_page = create_segment
        main_page.find(main_page.locators.LIST_OF_SEGMENTS)
        assert self.driver.find_element(*main_page.locators.LIST_OF_SEGMENTS)
        assert self.driver.find_element(*main_page.locators.SEGMENT_NAME)

    @pytest.mark.UI
    def test_segment_deletion(self, login):
        main_page = login
        main_page.click(main_page.locators.AUDS_LOCATOR)
        main_page.click(main_page.locators.CREATE_SEGMENT)
        name = str(time())
        self.create_segment_page.create_segment(name)
        main_page.click(main_page.locators.cross_segment(name))
        main_page.click(main_page.locators.DELETE_SEGMENT)
        self.driver.refresh()
        with pytest.raises(NoSuchElementException):
            assert self.driver.find_element(*main_page.locators.cross_segment(name))
        main_page.find(main_page.locators.S_CHEGO_NACHAT)
        assert self.driver.find_element(*main_page.locators.S_CHEGO_NACHAT)
        assert self.driver.find_element(*main_page.locators.CREATE_SEGMENT)
