"""Store Profile Page tests"""
from time import sleep

import pytest
from selenium.webdriver.common.by import By

from conftest import BaseTest
from constants.base import FIREFOX, CHROME
from constants.create_post import TITLE_XPATH, POST_BODY_XPATH, SAVE_POST_BUTTON, SUCCESS_MESSAGE_TEXT, SUCCESS_MESSAGE_XPATH
from constants.header import SEARCH_BUTTON_XPATH, SEARCH_FIELD_XPATH, SEARCH_RESULTS_XPATH, LINK_TO_POST_AUTHOR_XPATH
from constants.profile_page import FOLLOW_USER_BUTTON_XPATH, SUCCESS_FOLLOW_MESSAGE_XPATH, FOLLOWING_TAB_XPATH, FOLLOWING_USER_XPATH
from helpers.base import create_driver, User, generate_random_text
from constants import create_post as create_post_constants
from constants import start_page as start_page_constants
from pages.start_page import StartPage


@pytest.mark.parametrize("browser_name", [CHROME])
class TestProfilePage(BaseTest):
    """Store Profile Page tests"""

    @pytest.fixture(scope="function")
    def register_user(self, browser_name):
        driver = create_driver(browser_name)
        driver.implicitly_wait(5)
        # Open start page
        driver.get(start_page_constants.START_PAGE_URL)
        self.start_page = StartPage(driver)
        user = User()
        user.username = f"UserName{self.variety}"
        user.email = f"email{self.variety}@mail.com"
        user.password = f"UsrPwd{self.variety}"
        self.start_page.sign_up_user(username=user.username, email=user.email, password=user.password)
        self.start_page.click_sign_up_and_verify(username=user.username)
        self.start_page.header.sign_out()
        yield user
        driver.close()

    @pytest.fixture(scope="function")
    def register_user_and_user_with_post(self, browser_name):
        driver = create_driver(browser_name)
        driver.implicitly_wait(5)

        # Open start page
        driver.get(start_page_constants.START_PAGE_URL)
        self.start_page = StartPage(driver)

        # Create user with post
        self.user_with_post = User()
        self.user_with_post.username = "UserWithPosR"
        self.user_with_post.email = "user_with_posr@mail.com"
        self.user_with_post.password = "user_with_post_1234"
        if not self.start_page.check_user_exists(self.user_with_post.username, self.user_with_post.password):
            sleep(1)
            self.start_page.register_user_and_create_post(self.user_with_post)

        # Create one more user for following
        user = User()
        user.username = f"UserName{self.variety}"
        user.email = f"email{self.variety}@mail.com"
        user.password = f"UsrPwd{self.variety}"
        self.start_page.register_user(user)

        yield user
        driver.close()

    def test_profile_page(self, register_user):
        """
        - Login as registred user
        - Go to profile page
        - Verify Post, Followers and Following number
        - Verify name in profile
        """
        # Login
        self.start_page.fill_sign_in_fields(register_user.username, register_user.password)

        # Go to profile page
        sleep(1)
        profile_page = self.start_page.go_to_profile(register_user.username)

        # Verify Post, Followers and Following number
        profile_page.verify_tab_info(username=register_user.username)
        self.logger.info("Verified Tabs information")

    def test_create_post(self, register_user):
        """
        - Login as user
        - Click "create post"
        - Fill all required fields
        - Click "Save New Post"
        - Verify post on profile page
        """
        # Login
        self.start_page.fill_sign_in_fields(register_user.username, register_user.password)

        # Click "create post"
        sleep(1)
        self.start_page.header.create_post()

        # Fill all required fields
        sleep(1)
        self.start_page.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data="My First Title")
        self.start_page.wait_until_send_keys(locator_type=By.XPATH, locator=POST_BODY_XPATH, data="Text" * 50)
        self.start_page.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)

        # Verify message
        self.start_page.wait_for_text(locator_type=By.XPATH, locator=SUCCESS_MESSAGE_XPATH, text=SUCCESS_MESSAGE_TEXT)

        # Go to profile page
        sleep(1)
        profile_page = self.start_page.go_to_profile(register_user.username)

        # Verify Post, Followers and Following number
        profile_page.verify_tab_info(username=register_user.username, posts_number=1)
        self.logger.info("Verified Tabs information")

    def test_chat_message(self, register_user):
        """
        - Login as user
        - Open chat
        - Send some message
        - Verify message text
        - Send one more message
        - Verify 1st and 2nd messages
        """
        # Login
        self.start_page.fill_sign_in_fields(register_user.username, register_user.password)
        self.logger.info("Logged in as %s", register_user.username)

        # Open chat
        chat = self.start_page.header.open_chat()
        self.logger.info("Chat was opened")

        # Send some message
        message1 = generate_random_text(7)
        chat.send_message(message1)
        self.logger.info("Sent message: %s", message1)

        # Verify message text
        chat.verify_messages([message1])
        self.logger.info("Message text was verified")

        # Send one more message
        message2 = generate_random_text(12)
        chat.send_message(message2)
        self.logger.info("Sent message: %s", message2)

        # Verify messages text
        chat.verify_messages([message1, message2])
        self.logger.info("Messages text was verified")

    def test_empty_post(self, register_user):
        """
        - Login as user
        - Click on "Create Post"
        - Left title and text area empty
        - Click on "Save Post"
        - Verify errors
        - Fill title
        - Click on "Save Post"
        - Verify errors
        """
        # Login
        self.start_page.fill_sign_in_fields(register_user.username, register_user.password)
        self.logger.info("Logged in as %s", register_user.username)

        # Click "create post"
        sleep(1)
        create_post = self.start_page.header.create_post()
        self.logger.info("Redirected to create post page")

        # Left title and text area empty
        sleep(1)
        self.start_page.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data="")
        self.start_page.wait_until_send_keys(locator_type=By.XPATH, locator=POST_BODY_XPATH, data="")
        self.logger.info("Left fields empty")

        # Click on "Save Post"
        self.start_page.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)
        self.logger.info("Clicked on 'Save post'")

        # Verify errors
        create_post.verify_empty_filed_message(locator_type=By.XPATH, locator=create_post_constants.TITLE_XPATH)
        self.logger.info("Error message was verified")

        # Fill title
        self.start_page.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data="Title")
        self.logger.info("Filled Title")

        # Click on "Save Post"
        self.start_page.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)
        self.logger.info("Clicked on 'Save post'")

        # Verify errors
        create_post.verify_empty_filed_message(locator_type=By.XPATH, locator=create_post_constants.POST_BODY_XPATH)
        self.logger.info("Error message was verified")

    def test_follow_user(self, register_user_and_user_with_post):
        """
        Pre-condition:
          - Create user if not exists
          - Create post
          - Logout
          - Create one more user
          - Login as user
        Steps:
          - Search for post
          - Click on search result
          - Click on username
          - Click on follow
          - Forward back to "My Profile" and verify following
        """
        # Click on search button
        sleep(1)
        self.start_page.header.wait_until_click(locator_type=By.XPATH, locator=SEARCH_BUTTON_XPATH)
        self.logger.info("Clicked on search button")

        # Input search value
        sleep(1)
        self.start_page.wait_until_send_keys(locator_type=By.XPATH, locator=SEARCH_FIELD_XPATH, data=self.user_with_post.username)
        self.logger.info("Search for title")

        # Find post
        sleep(1)
        results = self.start_page.wait_until_find_elements(locator_type=By.XPATH, locator=SEARCH_RESULTS_XPATH)
        for result in results:
            self.logger.info("Checking %s", result.text.strip())
            if f"{self.user_with_post.username} by {self.user_with_post.username.lower()}" in result.text:
                sleep(1)
                result.click()
            else:
                raise AssertionError(f"Post with title {self.user_with_post.username} not found")
        self.logger.info("Found required post")

        # Go to user page
        sleep(1)
        self.start_page.wait_until_click(locator_type=By.XPATH, locator=LINK_TO_POST_AUTHOR_XPATH.format(username=self.user_with_post.username.lower()))
        self.logger.info("Forward to user profile")

        # Click on follow
        sleep(1)
        self.start_page.wait_until_click(locator_type=By.XPATH, locator=FOLLOW_USER_BUTTON_XPATH.format(username=self.user_with_post.username.lower()))
        self.logger.info("Clicked on follow")

        # Verify message
        sleep(1)
        self.start_page.wait_until_find(locator_type=By.XPATH, locator=SUCCESS_FOLLOW_MESSAGE_XPATH.format(username=self.user_with_post.username.lower()))
        self.logger.info("User was followed")

        # Verify following user
        sleep(1)
        profile_page = self.start_page.go_to_profile(register_user_and_user_with_post.username)
        profile_page.verify_tab_info(username=register_user_and_user_with_post.username, following_number=1)
        self.logger.info("Tab info was verified")

        sleep(1)
        profile_page.wait_until_click(locator_type=By.XPATH, locator=FOLLOWING_TAB_XPATH.format(username=register_user_and_user_with_post.username.lower()))
        profile_page.wait_until_find_elements(locator_type=By.XPATH, locator=FOLLOWING_USER_XPATH.format(username=self.user_with_post.username.lower()))
        self.logger.info("Following user was verified")
