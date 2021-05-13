"""Stores base utils for Pages"""
import logging

from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

import time


def wait_until_ok(timeout, period=0.25):
    """Retry function with parameters"""

    def act_decorator(target_func):
        logger = logging.getLogger(__name__)

        def wrapper(*args, **kwargs):
            must_end = time.time() + timeout
            while True:
                try:
                    return target_func(*args, **kwargs)
                except (WebDriverException, AssertionError, TimeoutException) as error:
                    error_name = error if str(error) else error.__class__.__name__
                    logger.debug("Catch '%s'. Left %s seconds", error_name, (must_end - time.time()))
                    if time.time() >= must_end:
                        logger.warning("Waiting timed out after %s", timeout)
                        raise error
                    time.sleep(period)

        return wrapper

    return act_decorator


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=5)

    def wait_for_text(self, locator_type, locator, text):
        """Wait until text appears in element"""
        self.wait.until(EC.text_to_be_present_in_element((locator_type, locator), text))

    def wait_until_find(self, locator_type, locator):
        """Wait until element can be find"""
        self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        return self.driver.find_element(by=locator_type, value=locator)

    def wait_until_send_keys(self, locator_type, locator, data):
        """Wait until field enabled and send keys"""
        self.wait.until(EC.element_to_be_clickable((locator_type, locator)))
        field = self.driver.find_element(by=locator_type, value=locator)
        field.clear()
        field.send_keys(data)

    def wait_until_click(self, locator_type, locator):
        """Wait until button clickable and click"""
        self.wait.until(EC.element_to_be_clickable((locator_type, locator)))
        self.driver.find_element(by=locator_type, value=locator).click()


class User:

    def __init__(self, username="", password="", email=""):
        self.username = username
        self.password = password
        self.email = email
