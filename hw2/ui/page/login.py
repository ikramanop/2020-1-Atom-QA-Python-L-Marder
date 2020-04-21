from .base import BasePage
from ui.locators.locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def login(self, login, password):
        self.click(self.locators.LOGIN_BUTTON)

        self.wait(timeout=1)

        login_field = self.find(self.locators.LOGIN_FIELD)
        login_field.clear()
        login_field.send_keys(login)

        password_field = self.find(self.locators.PASSWD_FIELD)
        password_field.clear()
        password_field.send_keys(password)

        self.click(self.locators.ENTER_BUTTON)
