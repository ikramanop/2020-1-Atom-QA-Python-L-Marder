from .base import BasePage
from ui.locators.locators import CreateCampaignPageLocators
import os


class CreateCampaignPage(BasePage):
    locators = CreateCampaignPageLocators()

    def create_campaign(self):
        self.click(self.locators.TRAFFIC_LOCATOR)
        link_field = self.find(self.locators.ENTER_LINK)
        link_field.clear()
        link_field.send_keys('https://www.kwejk.pl/')
        self.click(self.locators.BUDGET_LOCATOR)
        budget_per_day = self.find(self.locators.BUDGET_PER_DAY_FIELD)
        budget_per_day.clear()
        budget_per_day.send_keys('123')
        budget_overall = self.find(self.locators.BUDGET_OVERALL_FIELD)
        budget_overall.clear()
        budget_overall.send_keys('123000')
        self.move_to(self.locators.BANNER_LOCATOR)
        self.click(self.locators.BANNER_LOCATOR)
        self.find(self.locators.HISTOGRAM_LOCATOR)
        self.move_to(self.locators.UPLOAD_IMAGE_BUTTON)
        upload_image = self.find(self.locators.UPLOAD_IMAGE_BUTTON)
        upload_image.send_keys(
            os.path.join(os.path.sep.join((os.path.realpath(__file__).split(os.path.sep)[:-3])), 'static',
                         'EUmSleGXsAEcdEH.png'))
        self.click(self.locators.SAVE_IMAGE_BUTTON)
        self.click(self.locators.CREATE_BUTTON)
