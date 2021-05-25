import logging
import random
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.firefox.options import Options

from constants.base import CHROME, FIREFOX
from constants.text_base import TEXT_BASE_RUS


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


def create_driver(browser_name):
    """Create driver based on input driver name"""
    if browser_name == CHROME:
        return webdriver.Chrome()
    elif browser_name == FIREFOX:
        options = Options()
        options.add_argument('--headless')
        return webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unknown browser name: {browser_name}")
