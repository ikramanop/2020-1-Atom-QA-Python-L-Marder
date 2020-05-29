from .base_page import BasePage
from ui.locators.locators import RegPageLocators


class RegPage(BasePage):
    locators = RegPageLocators()

    def register(self, login, email, password, confirm=None):
        if confirm is None:
            confirm = password

        login_field = self.find(self.locators.USERNAME)
        login_field.clear()
        login_field.send_keys(login)

        email_field = self.find(self.locators.EMAIL)
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.find(self.locators.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

        confirm_field = self.find(self.locators.PASSWORD_CONFIRM)
        confirm_field.clear()
        confirm_field.send_keys(confirm)

        self.click(self.locators.CHECKBOX)

        self.click(self.locators.REG_BUTTON)
