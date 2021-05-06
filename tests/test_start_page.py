"""Store Start Page tests"""

import pytest
from selenium import webdriver
from conftest import BaseTest

from constants import start_page as start_page_constants
from pages.start_page import StartPage


class TestStartPage(BaseTest):
    """Tests for start page"""

    @pytest.fixture(scope="function")
    def setup(self):
        driver = webdriver.Chrome(executable_path='/home/wing/PycharmProjects/QAComplexApp/drivers/chromedriver')
        # Open start page
        driver.get(start_page_constants.START_PAGE_URL)
        start_page = StartPage(driver)
        yield start_page
        driver.close()

    def test_empty_fields_login(self, setup):
        """
        - Open start page
        - Clear password and login fields
        - Click on Sign In
        - Verify error message
        """
        start_page = setup

        # Clear password and login fields
        start_page.fill_sign_in_fields(username="", password="")

        # Verify error message
        start_page.verify_invalid_credentials()

    def test_invalid_credentials(self, setup):
        """
        - Open start page
        - Clear password and login fields
        - Set invalid values for login and password
        - Click on Sign In
        - Verify error message
        """
        start_page = setup

        # Clear password and login fields
        start_page.fill_sign_in_fields(username="Login123", password="Pwd147")

        # Verify error message
        start_page.verify_invalid_credentials()

    def test_registration(self, setup):
        """
        - Open start page
        - Set login, email and password fields with valid values
        - Click on sign up button
        - Verify that sign up successful
        """
        start_page = setup

        # Set login, email and password fields with valid values
        username = f"UserName{self.variety}"
        start_page.sign_up_user(username=username, email=f"email{self.variety}@mail.com", password=f"UsrPwd{self.variety}")
        self.logger.info("Filled all required fields for user '%s'", username)

        # Verify that sign up successful
        start_page.click_sign_up_and_verify(username=username)
        self.logger.info("Sign Up was verified based on Hello message")

    def test_invalid_reg_login(self, setup):
        """
        - Open start page
        - Set invalid login value
        - Verify error message
        """
        start_page = setup

        # Set login value
        user_name = "User!Nam3#"
        start_page.fill_sign_up_username(user_name)
        self.logger.info("Set login value: '%s'", user_name)

        # Verify error message
        start_page.verify_error_message_text(error_xpath=start_page_constants.SIGN_UP_INVALID_LOGIN_ERROR_XPATH,
                                             error_text=start_page_constants.SIGN_UP_INVALID_LOGIN_ERROR_TEXT)
        self.logger.info("Error message was verified")

    def test_invalid_reg_pass(self, setup):
        """
        - Open start page
        - Set invalid password value
        - Verify error message
        """
        start_page = setup

        # Set password value
        password = "123"
        start_page.fill_sign_up_password(password)
        self.logger.info("Set password value: '%s'", password)

        # Verify error message
        start_page.verify_error_message_text(error_text=start_page_constants.SIGN_UP_PASSWORD_TOO_SHORT_ERROR_TEXT,
                                             error_xpath=start_page_constants.SIGN_UP_PASSWORD_TOO_SHORT_ERROR_XPATH)
        self.logger.info("Error message was verified")

    def test_invalid_reg_email(self, setup):
        """
        - Open start page
        - Set invalid email value
        - Verify error message
        """
        start_page = setup

        # Set email value
        email = "mail"
        start_page.fill_sign_up_email(email)
        self.logger.info("Set email value: '%s'", email)

        # Verify error message
        start_page.verify_error_message_text(error_xpath=start_page_constants.SIGN_UP_INVALID_EMAIL_ERROR_XPATH,
                                             error_text=start_page_constants.SIGN_UP_INVALID_EMAIL_ERROR_TEXT)
        self.logger.info("Error message was verified")
