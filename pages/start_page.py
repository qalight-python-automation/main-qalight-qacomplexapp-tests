"""Encapsulate actions related to start page"""
import datetime
import logging
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from constants import start_page
from constants.create_post import TITLE_XPATH, POST_BODY_XPATH, SAVE_POST_BUTTON
from pages.base import BasePage
from pages.header import Header
from pages.profile_page import ProfilePage
from helpers.base import wait_until_ok


class StartPage(BasePage):
    """Class stores actions and verification related to start page"""

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.header = Header(driver)

    def fill_sign_in_fields(self, username, password):
        """Fill specified fields using passed values"""
        self.wait_until_send_keys(locator_type=By.XPATH, locator=start_page.SIGN_IN_LOGIN_FIELD_XPATH, data=username)
        self.logger.debug("Set login value: '%s'", username)

        self.wait_until_send_keys(locator_type=By.XPATH, locator=start_page.SIGN_IN_PASSWORD_FIELD_XPATH, data=password)
        self.logger.debug("Set password value: '%s'", password)

        # Click on Sign In
        self.wait_until_click(locator_type=By.XPATH, locator=start_page.SIGN_IN_BUTTON_XPATH)
        self.logger.debug("Clicked on sign in")

    def verify_invalid_credentials(self):
        """Check error message on invalid credentials"""
        error_message = self.wait_until_find(locator_type=By.XPATH, locator=start_page.INVALID_LOGIN_ERROR_XPATH)
        assert error_message.text == r"Invalid username pasword", f"Actual: {error_message.text}"
        self.logger.debug("Error message was verified")

    def fill_sign_up_username(self, username):
        """Fill specified field"""
        self.wait_until_send_keys(locator_type=By.ID, locator=start_page.SIGN_UP_LOGIN_FIELD_ID, data=username)
        self.logger.debug("Set login value: '%s'", username)

    def fill_sign_up_email(self, email):
        """Fill specified field"""
        self.wait_until_send_keys(locator_type=By.ID, locator=start_page.SIGN_UP_EMAIL_FIELD_ID, data=email)
        self.logger.debug("Set email value: '%s'", email)

    def fill_sign_up_password(self, password):
        """Fill specified field"""
        self.wait_until_send_keys(locator_type=By.ID, locator=start_page.SIGN_UP_PASSWORD_FIELD_ID, data=password)
        self.logger.debug("Set password value: '%s'", password)

    def sign_up_user(self, username, email, password):
        """Fill all required fields and press Sign Up button"""
        # Set login value
        self.fill_sign_up_username(username)

        # Set email value
        self.fill_sign_up_email(email)

        # Set password value
        self.fill_sign_up_password(password)

    @wait_until_ok(timeout=30)
    def click_sign_up_and_verify(self, username):
        """Click sign up button and verify the result"""
        # Click on sign up button
        self.wait_until_click(locator_type=By.XPATH, locator=start_page.SIGN_UP_BUTTON_XPATH)
        self.logger.debug("Clicked on sign up")

        # Verify
        self.verify_sign_up(username)

    def verify_sign_up(self, username):
        """Verify that sign up successful"""
        hello_message = self.wait_until_find(locator_type=By.XPATH, locator=start_page.HELLO_MESSAGE_XPATH).text
        assert hello_message == start_page.HELLO_MESSAGE_TEXT.format(username=username.lower()), f"Actual message: {hello_message}"
        self.logger.debug("Hello message was verified")

    def verify_error_message_text(self, error_xpath, error_text):
        """Find error and verify message"""
        # Wait until text appears
        self.wait_for_text(locator_type=By.XPATH, locator=error_xpath, text=error_text)
        # Get text from the element
        message = self.wait_until_find(locator_type=By.XPATH, locator=error_xpath).text
        assert message == error_text, f"Actual message: {message}"
        self.logger.debug("Error message was verified")

    def go_to_profile(self, username):
        """Click on profile"""
        self.header.go_to_profile_page(username)
        return ProfilePage(self.driver)

    def check_user_exists(self, username, password):
        """Try to login as user and return True if success otherwise False"""
        self.fill_sign_in_fields(username, password)
        try:
            self.verify_invalid_credentials()
        except (AssertionError, TimeoutException):
            self.header.sign_out()
            return True
        else:
            return False

    def register_user(self, user):
        """Register user"""
        self.sign_up_user(username=user.username, email=user.email, password=user.password)
        self.click_sign_up_and_verify(username=user.username)

    def register_user_and_create_post(self, user):
        """Register user and create post"""
        # Register user
        self.register_user(user)

        # Click "create post"
        sleep(1)
        self.header.create_post()

        # Fill all required fields
        sleep(1)
        self.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data=user.username)
        self.wait_until_send_keys(locator_type=By.XPATH, locator=POST_BODY_XPATH, data=str(datetime.datetime.now().timestamp()))
        self.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)

        # Sign out
        sleep(1)
        self.header.sign_out()
