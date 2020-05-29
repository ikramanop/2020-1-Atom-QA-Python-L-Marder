import functools

import allure
from allure_commons.types import AttachmentType


def screenshot_on_failure(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except:
            allure.attach(self.base_page.driver.get_screenshot_as_png(), name='Screenshot',
                          attachment_type=AttachmentType.PNG)
            raise

    return wrapper