"""Store profile page helpers and actions"""
import logging

from selenium.webdriver.common.by import By

from constants import profile_page as profile_page_constants
from pages.base import BasePage


class ProfilePage(BasePage):
    """Store profile page helpers and actions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def verify_tab_info(self, username, posts_number=0, followers_number=0, following_number=0):
        """Get text from all tabs and verify expected numbers"""
        # Verify posts number
        message = self.wait_until_find(locator_type=By.XPATH,
                                       locator=profile_page_constants.POSTS_TAB_ACTIVE_XPATH.format(username=username.lower())).text
        expected_message = f"Posts: {posts_number}"
        assert message == expected_message, f"Actual: {message}, Expected: {expected_message}"

        # Verify followers number
        message = self.wait_until_find(locator_type=By.XPATH,
                                       locator=profile_page_constants.FOLLOWERS_TAB_XPATH.format(username=username.lower())).text
        expected_message = f"Followers: {followers_number}"
        assert message == expected_message, f"Actual: {message}, Expected: {expected_message}"

        # Verify following number
        message = self.wait_until_find(locator_type=By.XPATH,
                                       locator=profile_page_constants.FOLLOWING_TAB_XPATH.format(username=username.lower())).text
        expected_message = f"Following: {following_number}"
        assert message == expected_message, f"Actual: {message}, Expected: {expected_message}"
