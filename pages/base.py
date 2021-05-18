"""Stores base utils for Pages"""
import logging
import os
import random

from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

import time

from constants.text_base import TEXT_BASE_RUS

from skimage import io as image_io
from skimage.metrics import structural_similarity


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
    def __init__(self, driver: webdriver.Chrome):
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

    def wait_until_find_elements(self, locator_type, locator):
        """Wait until element can be find"""
        self.wait.until(EC.presence_of_element_located((locator_type, locator)))
        return self.driver.find_elements(by=locator_type, value=locator)

    def verify_element_image(self, locator_type, locator, expected_image_path):
        """Get screen shot"""
        self.driver.save_screenshot(filename="screenshot.png")
        try:
            element = self.wait_until_find(locator_type=locator_type, locator=locator)

            # Find crop area
            top = element.rect["y"]
            bottom = element.rect["y"] + element.rect["height"]
            left = element.rect["x"]
            right = element.rect["x"] + element.rect["width"]

            # Crop image
            image = Image.open("screenshot.png")
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save("cropped_screen_shot.png")

            # Compare images
            actual = image_io.imread("cropped_screen_shot.png")
            expected = image_io.imread(expected_image_path)
            assert structural_similarity(actual, expected, multichannel=True) == 1
        except Exception as exception:
            raise exception
        else:
            os.remove("cropped_screen_shot.png")
        finally:
            os.remove("screenshot.png")


class User:

    def __init__(self):
        self.__username = ""
        self.__password = ""
        self.__email = ""

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @username.deleter
    def username(self):
        self.__username = ""

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @email.deleter
    def email(self):
        self.__email = ""

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @password.deleter
    def password(self):
        self.__password = ""


def generate_random_text(word_count=3):
    """Generate random text based on input text"""
    input_text_lst = TEXT_BASE_RUS.replace("\n", "").split(" ")
    generated_text_lst = []
    for _ in range(word_count):
        generated_text_lst.append(random.choice(input_text_lst))
    generated_text = ' '.join(generated_text_lst)
    return generated_text
