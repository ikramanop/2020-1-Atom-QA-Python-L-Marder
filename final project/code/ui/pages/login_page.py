from .base_page import BasePage
from ui.locators.locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def login(self, login, password):
        login_field = self.find(self.locators.USERNAME)
        login_field.clear()
        login_field.send_keys(login)

        password_field = self.find(self.locators.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

        self.click(self.locators.LOGIN_BUTTON)
