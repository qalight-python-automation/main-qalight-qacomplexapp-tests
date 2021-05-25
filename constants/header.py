"""Store locators and useful links for Header element"""

SIGN_OUT_BUTTON_XPATH = '//button[@class="btn btn-sm btn-secondary"]'
PROFILE_BUTTON_XPATH = "//*[@href='/profile/{username}'and @class='mr-2']/img[@data-original-title='My Profile']"
CREATE_POST_BUTTON_XPATH = "//*[@href='/create-post']"
CHAT_BUTTON_XPATH = "//*[@data-icon='comment']"
SEARCH_BUTTON_XPATH = ".//*[@data-icon='search']"
SEARCH_FIELD_XPATH = ".//input[@id='live-search-field']"
SEARCH_RESULTS_XPATH = ".//a[@class='list-group-item list-group-item-action']"
LINK_TO_POST_AUTHOR_XPATH = ".//*[@href='/profile/{username}']"
