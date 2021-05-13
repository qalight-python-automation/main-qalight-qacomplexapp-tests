"""Stores useful constants and link for Posts creation"""

TITLE_XPATH = "//*[@name='title']"
POST_BODY_XPATH = "//textarea[@id='post-body']"
SAVE_POST_BUTTON = "//button[@class='btn btn-primary']"

SUCCESS_MESSAGE_TEXT = "New post successfully created."
SUCCESS_MESSAGE_XPATH = f"//*[contains(text(), '{SUCCESS_MESSAGE_TEXT}')]"
