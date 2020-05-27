from .base_page import BasePage
from ui.locators.locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    def new_window_url(self, locator):
        self.click(locator)

        main_window = self.driver.window_handles[0]
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)

        url = self.driver.current_url

        self.driver.close()
        self.driver.switch_to.window(main_window)

        return url
