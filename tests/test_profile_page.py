"""Store Profile Page tests"""
from time import sleep

from selenium.webdriver.common.by import By

from conftest import BaseTest
from constants.create_post import TITLE_XPATH, POST_BODY_XPATH, SAVE_POST_BUTTON, SUCCESS_MESSAGE_TEXT, SUCCESS_MESSAGE_XPATH
from pages.base import generate_random_text
from constants import create_post as create_post_constants
from constants import start_page as start_page_constants


class TestProfilePage(BaseTest):
    """Store Profile Page tests"""

    def test_profile_page(self, start_page, register_user):
        """
        - Login as registred user
        - Go to profile page
        - Verify Post, Followers and Following number
        - Verify name in profile
        """
        # Login
        start_page.fill_sign_in_fields(register_user.username, register_user.password)

        # Go to profile page
        sleep(1)
        profile_page = start_page.go_to_profile(register_user.username)

        # Verify Post, Followers and Following number
        profile_page.verify_tab_info(username=register_user.username)
        self.logger.info("Verified Tabs information")

    def test_create_post(self, start_page, register_user):
        """
        - Login as user
        - Click "create post"
        - Fill all required fields
        - Click "Save New Post"
        - Verify post on profile page
        """
        # Login
        start_page.fill_sign_in_fields(register_user.username, register_user.password)

        # Click "create post"
        sleep(1)
        start_page.header.create_post()

        # Fill all required fields
        sleep(1)
        start_page.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data="My First Title")
        start_page.wait_until_send_keys(locator_type=By.XPATH, locator=POST_BODY_XPATH, data="Text" * 50)
        start_page.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)

        # Verify message
        start_page.wait_for_text(locator_type=By.XPATH, locator=SUCCESS_MESSAGE_XPATH, text=SUCCESS_MESSAGE_TEXT)

        # Go to profile page
        sleep(1)
        profile_page = start_page.go_to_profile(register_user.username)

        # Verify Post, Followers and Following number
        profile_page.verify_tab_info(username=register_user.username, posts_number=1)
        self.logger.info("Verified Tabs information")

    def test_chat_message(self, start_page, register_user):
        """
        - Login as user
        - Open chat
        - Send some message
        - Verify message text
        - Send one more message
        - Verify 1st and 2nd messages
        """
        # Login
        start_page.fill_sign_in_fields(register_user.username, register_user.password)
        self.logger.info("Logged in as %s", register_user.username)

        # Open chat
        chat = start_page.header.open_chat()
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

    def test_empty_post(self, start_page, register_user):
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
        start_page.fill_sign_in_fields(register_user.username, register_user.password)
        self.logger.info("Logged in as %s", register_user.username)

        # Click "create post"
        sleep(1)
        create_post = start_page.header.create_post()
        self.logger.info("Redirected to create post page")

        # Left title and text area empty
        sleep(1)
        start_page.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data="")
        start_page.wait_until_send_keys(locator_type=By.XPATH, locator=POST_BODY_XPATH, data="")
        self.logger.info("Left fields empty")

        # Click on "Save Post"
        start_page.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)
        self.logger.info("Clicked on 'Save post'")

        # Verify errors
        create_post.verify_empty_filed_message(locator_type=By.XPATH, locator=create_post_constants.TITLE_XPATH)
        self.logger.info("Error message was verified")

        # Fill title
        start_page.wait_until_send_keys(locator_type=By.XPATH, locator=TITLE_XPATH, data="Title")
        self.logger.info("Filled Title")

        # Click on "Save Post"
        start_page.wait_until_click(locator_type=By.XPATH, locator=SAVE_POST_BUTTON)
        self.logger.info("Clicked on 'Save post'")

        # Verify errors
        create_post.verify_empty_filed_message(locator_type=By.XPATH, locator=create_post_constants.POST_BODY_XPATH)
        self.logger.info("Error message was verified")
