"""Store create post page helpers and actions"""
import logging

from selenium.webdriver.common.by import By

from constants import create_post as create_post_constants
from pages.base import BasePage


class CreatePostPage(BasePage):
    """Store create post page helpers and actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def verify_empty_filed_message(self, locator_type, locator):
        """Verify error message as attribute of the field"""
        field = self.driver.find_element(by=locator_type, value=locator)
        assert field.get_attribute("validationMessage") == create_post_constants.EMPTY_FIELDS_ERROR, \
            f"Actual: {field.get_attribute('validationMessage')}, Expected: {create_post_constants.EMPTY_FIELDS_ERROR}"
