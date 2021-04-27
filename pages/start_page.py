"""Encapsulate actions related to start page"""
import logging
from time import sleep

from selenium.webdriver.common.by import By

from constants import start_page


class StartPage:
    """Class stores actions and verification related to start page"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def fill_sign_in_fields(self, username, password):
        """Fill specified fields using passed values"""
        username_input_field = self.driver.find_element(by=By.XPATH, value=start_page.SIGN_IN_LOGIN_FIELD_XPATH)
        username_input_field.clear()
        username_input_field.send_keys(username)
        self.logger.info("Set login value: '%s'", username)

        password_input_field = self.driver.find_element(by=By.XPATH, value=start_page.SIGN_IN_PASSWORD_FIELD_XPATH)
        password_input_field.clear()
        password_input_field.send_keys(password)
        self.logger.info("Set password value: '%s'", password)

        # Click on Sign In
        sign_in_button = self.driver.find_element(by=By.XPATH, value=start_page.SIGN_IN_BUTTON_XPATH)
        sign_in_button.click()
        self.logger.debug("Clicked on sign in")

    def verify_invalid_credentials(self):
        """Check error message on invalid credentials"""
        error_message = self.driver.find_element_by_xpath(start_page.INVALID_LOGIN_ERROR_XPATH)
        assert error_message.text == r"Invalid username \ password", f"Actual: {error_message.text}"
        self.logger.debug("Error message was verified")

    def fill_sign_up_username(self, username):
        """Fill specified field"""
        username_input_field = self.driver.find_element(by=By.ID, value=start_page.SIGN_UP_LOGIN_FIELD_ID)
        username_input_field.clear()
        username_input_field.send_keys(username)
        self.logger.debug("Set login value: '%s'", username)

    def fill_sign_up_email(self, email):
        """Fill specified field"""
        email_input_field = self.driver.find_element(by=By.ID, value=start_page.SIGN_UP_EMAIL_FIELD_ID)
        email_input_field.clear()
        email_input_field.send_keys(email)
        self.logger.debug("Set email value: '%s'", email)

    def fill_sign_up_password(self, password):
        """Fill specified field"""
        password_input_field = self.driver.find_element(by=By.ID, value=start_page.SIGN_UP_PASSWORD_FIELD_ID)
        password_input_field.clear()
        password_input_field.send_keys(password)
        self.logger.debug("Set password value: '%s'", password)

    def sign_up_user(self, username, email, password):
        """Fill all required fields and press Sign Up button"""
        # Set login value
        self.fill_sign_up_username(username)

        # Set email value
        self.fill_sign_up_email(email)

        # Set password value
        self.fill_sign_up_password(password)

        # Sleep a bit to make button ready to click
        sleep(1)

        # Click on sign up button
        sign_in_button = self.driver.find_element(by=By.XPATH, value=start_page.SIGN_UP_BUTTON_XPATH)
        sign_in_button.click()
        self.logger.debug("Clicked on sign up")

    def verify_sign_up(self, username):
        """Verify that sign up successful"""
        hello_message = self.driver.find_element_by_xpath(start_page.HELLO_MESSAGE_XPATH).text
        assert hello_message == start_page.HELLO_MESSAGE_TEXT.format(username=username.lower()), f"Actual message: {hello_message}"
        self.logger.debug("Hello message was verified")

    def verify_error_message_text(self, error_xpath, error_text):
        """Find error and verify message"""
        message = self.driver.find_element_by_xpath(error_xpath).text
        assert message == error_text, f"Actual message: {message}"
        self.logger.debug("Error message was verified")
