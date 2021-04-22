"""Store Start Page tests"""
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from conftest import BaseTest


class TestStartPage(BaseTest):
    """Tests for start page"""

    @pytest.fixture(scope="function")
    def setup(self):
        driver = webdriver.Chrome(executable_path='/home/wing/PycharmProjects/QAComplexApp/drivers/chromedriver')
        driver.implicitly_wait(time_to_wait=20)  # seconds
        yield driver
        driver.close()

    def test_empty_fields_login(self, setup):
        """
        - Open start page
        - Clear password and login fields
        - Click on Sign In
        - Verify error message
        """
        driver = setup

        # Open start page
        driver.get('https://qa-complex-app-for-testing.herokuapp.com/')
        self.logger.info("Open start page")

        # Clear password and login fields
        username_input_field = driver.find_element(by=By.XPATH, value='//input[@placeholder="Username"]')
        username_input_field.clear()

        password_input_field = driver.find_element(by=By.XPATH, value='//input[@placeholder="Password"]')
        password_input_field.clear()
        self.logger.info("Cleaned up input fields")

        # Click on Sign In
        sign_in_button = driver.find_element(by=By.XPATH, value='//button[@class="btn btn-primary btn-sm"]')
        sign_in_button.click()
        self.logger.info("Clicked on sign in")

        # Verify error message
        error_message = driver.find_element_by_xpath("//*[@class='alert alert-danger text-center']")
        assert error_message.text == r"Invalid username \ password", f"Actual: {error_message.text}"
        self.logger.info("Error message was verified")

    def test_invalid_credentials(self, setup):
        """
        - Open start page
        - Clear password and login fields
        - Set invalid values for login and password
        - Click on Sign In
        - Verify error message
        """
        driver = setup

        # Open start page
        driver.get('https://qa-complex-app-for-testing.herokuapp.com/')
        self.logger.info("Open start page")

        # Clear password and login fields
        username_input_field = driver.find_element(by=By.XPATH, value='//input[@placeholder="Username"]')
        username_input_field.clear()
        username_input_field.send_keys("Login123")
        self.logger.info("Set login value: 'Login123'")

        password_input_field = driver.find_element(by=By.XPATH, value='//input[@placeholder="Password"]')
        password_input_field.clear()
        password_input_field.send_keys("Pwd147")
        self.logger.info("Set password value: 'Pwd147'")

        # Click on Sign In
        sign_in_button = driver.find_element(by=By.XPATH, value='//button[@class="btn btn-primary btn-sm"]')
        sign_in_button.click()
        self.logger.info("Clicked on sign in")

        # Verify error message
        error_message = driver.find_element_by_xpath("//*[@class='alert alert-danger text-center']")
        assert error_message.text == r"Invalid username \ password", f"Actual: {error_message.text}"
        self.logger.info("Error message was verified")

    def test_registration(self, setup):
        """
        - Open start page
        - Set login, email and password fields with valid values
        - Click on sign up button
        - Verify that sign up successful
        """
        driver = setup

        # Open start page
        driver.get('https://qa-complex-app-for-testing.herokuapp.com/')
        self.logger.info("Open start page")

        # Set login value
        user_name = f"UserName{self.variety}"
        username_input_field = driver.find_element(by=By.ID, value='username-register')
        username_input_field.clear()
        username_input_field.send_keys(user_name)
        self.logger.info("Set login value: '%s'", user_name)

        # Set email value
        email = f"email{self.variety}@mail.com"
        email_input_field = driver.find_element(by=By.ID, value='email-register')
        email_input_field.clear()
        email_input_field.send_keys(email)
        self.logger.info("Set email value: '%s'", email)

        # Set password value
        password = f"UsrPwd{self.variety}"
        password_input_field = driver.find_element(by=By.ID, value='password-register')
        password_input_field.clear()
        password_input_field.send_keys(password)
        self.logger.info("Set password value: '%s'", password)

        # Sleep a bit to make button ready to click
        sleep(1)

        # Click on sign up button
        sign_in_button = driver.find_element(by=By.XPATH, value="//button[@type='submit']")
        sign_in_button.click()
        self.logger.info("Clicked on sign up")

        # Verify that sign up successful
        hello_message = driver.find_element_by_xpath("//h2").text
        assert hello_message == f"Hello {user_name.lower()}, your feed is empty.", f"Actual message: {hello_message}"
        self.logger.info("Hello message was verified")
