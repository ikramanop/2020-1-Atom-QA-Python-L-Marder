from .base import BasePage
from ui.locators.locators import CreateSegmentPageLocators


class CreateSegmentPage(BasePage):
    locators = CreateSegmentPageLocators()

    def create_segment(self):
        self.click(self.locators.ADD_SEGMENT)
        self.click(self.locators.CHECK_BOX)
        self.click(self.locators.SUBMIT_BUTTON)
        self.click(self.locators.CREATE_SEGMENT)
