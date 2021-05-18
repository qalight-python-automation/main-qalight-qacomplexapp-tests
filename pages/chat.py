"""Store chat actions and helpers"""
import logging
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pages.base import BasePage
from constants import chat as chat_constants


class Chat(BasePage):
    """Store chat actions and helpers"""

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def send_message(self, message_text):
        """Send text message"""
        self.wait_until_send_keys(locator_type=By.XPATH, locator=chat_constants.CHAT_INPUT_FIELD_XPATH, data=message_text)
        self.driver.find_element(by=By.XPATH, value=chat_constants.CHAT_INPUT_FIELD_XPATH).send_keys(Keys.ENTER)

    def verify_messages(self, messages):
        """Verify self sent messages"""
        actual_messages = self.wait_until_find_elements(locator_type=By.XPATH, locator=chat_constants.SELF_CHAT_MESSAGES_XPATH)
        actual_messages_text = [actual_message.text for actual_message in actual_messages]
        assert messages == actual_messages_text, f"Actual: {actual_messages_text}, Expected: {messages}"
