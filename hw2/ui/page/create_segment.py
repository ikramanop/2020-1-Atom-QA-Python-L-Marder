from .base import BasePage
from ui.locators.locators import CreateSegmentPageLocators


class CreateSegmentPage(BasePage):
    locators = CreateSegmentPageLocators()

    def create_segment(self, name):
        self.click(self.locators.ADD_SEGMENT)
        self.click(self.locators.CHECK_BOX)
        self.click(self.locators.SUBMIT_BUTTON)
        name_input = self.find(self.locators.NAME_FIELD)
        name_input.clear()
        name_input.send_keys(name)
        self.click(self.locators.CREATE_SEGMENT)
