"""Store header actions and helpers"""
import logging
from time import sleep

from selenium.webdriver.common.by import By

from pages.base import BasePage
from constants import header as header_constants
from pages.chat import Chat


class Header(BasePage):
    """Store header actions and helpers"""

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def go_to_profile_page(self, username):
        """Click on Profile Button"""
        self.wait_until_click(locator_type=By.XPATH, locator=header_constants.PROFILE_BUTTON_XPATH.format(username=username.lower()))

    def sign_out(self):
        """Click on Sign Out button"""
        self.wait_until_click(locator_type=By.XPATH, locator=header_constants.SIGN_OUT_BUTTON_XPATH)
        sleep(1)

    def create_post(self):
        """Click on Create Post"""
        self.wait_until_click(locator_type=By.XPATH, locator=header_constants.CREATE_POST_BUTTON_XPATH)

    def open_chat(self):
        """Click on Create Post"""
        sleep(1)
        self.wait_until_click(locator_type=By.XPATH, locator=header_constants.CHAT_BUTTON_XPATH)
        # sleep(1)
        return Chat(self.driver)
