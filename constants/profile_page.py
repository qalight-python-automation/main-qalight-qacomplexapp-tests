"""Storre useful constants and links for Profile Page"""

PROFILE_NAME = "//h2"

# TABS
POSTS_TAB_ACTIVE_XPATH = "//*[@href='/profile/{username}' and @class='profile-nav-link nav-item nav-link active']"
FOLLOWERS_TAB_XPATH = "//*[@href='/profile/{username}/followers' and @class='profile-nav-link nav-item nav-link ']"
FOLLOWING_TAB_XPATH = "//*[@href='/profile/{username}/following' and @class='profile-nav-link nav-item nav-link ']"

FOLLOW_USER_BUTTON_XPATH = ".//button[contains(text(), 'Follow')]"
SUCCESS_FOLLOW_MESSAGE_XPATH = ".//div[contains(text(), 'Successfully followed {username}')]"
FOLLOWING_USER_XPATH = ".//a[@href='/profile/{username}']"
