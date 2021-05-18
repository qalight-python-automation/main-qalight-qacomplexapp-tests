import logging
import random
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from constants import start_page as start_page_constants
from constants.header import SIGN_OUT_BUTTON_XPATH
from constants.start_page import START_PAGE_URL
from pages.base import User
from pages.start_page import StartPage


def pytest_runtest_setup(item):
    """Prepare test"""
    log = logging.getLogger(item.name)
    item.cls.logger = log
    item.cls.variety = str(random.randint(10000000, 99999999))


class BaseTest:
    """BaseTest class for inheritance. Implements test class default variables."""
    # Defined to fix `unresolved attribute` warning
    # Default values to provide autocomplete
    logger = logging.getLogger(__name__)
    variety = str(random.randint(10000000, 99999999))


@pytest.fixture(scope="function")
def start_page():
    driver = webdriver.Chrome(executable_path='/home/wing/PycharmProjects/QAComplexApp/drivers/chromedriver')
    driver.implicitly_wait(5)
    # Open start page
    driver.get(start_page_constants.START_PAGE_URL)
    start_page = StartPage(driver)
    yield start_page
    driver.close()


@pytest.fixture(scope="function")
def register_user(start_page):
    variety = str(random.randint(10000000, 99999999))
    user = User()
    user.username = f"UserName{variety}"
    user.email = f"email{variety}@mail.com"
    user.password = f"UsrPwd{variety}"
    start_page.sign_up_user(username=user.username, email=user.email, password=user.password)
    start_page.click_sign_up_and_verify(username=user.username)
    start_page.header.sign_out()
    return user
