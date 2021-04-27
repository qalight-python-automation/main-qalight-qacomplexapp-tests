"""Store locators and useful constants for Start Page"""

# Links
START_PAGE_URL = 'https://qa-complex-app-for-testing.herokuapp.com/'

# Locators
SIGN_IN_LOGIN_FIELD_XPATH = '//input[@placeholder="Username"]'
SIGN_IN_PASSWORD_FIELD_XPATH = '//input[@placeholder="Password"]'
SIGN_IN_BUTTON_XPATH = '//button[@class="btn btn-primary btn-sm"]'
INVALID_LOGIN_ERROR_XPATH = "//*[@class='alert alert-danger text-center']"

SIGN_UP_LOGIN_FIELD_ID = 'username-register'
SIGN_UP_EMAIL_FIELD_ID = 'email-register'
SIGN_UP_PASSWORD_FIELD_ID = 'password-register'
SIGN_UP_BUTTON_XPATH = "//button[@type='submit']"
HELLO_MESSAGE_XPATH = "//h2"
HELLO_MESSAGE_TEXT = "Hello {username}, your feed is empty."
SIGN_UP_INVALID_LOGIN_ERROR_TEXT = "Username can only contain letters and numbers."
SIGN_UP_INVALID_LOGIN_ERROR_XPATH = f"//*[contains(text(), '{SIGN_UP_INVALID_LOGIN_ERROR_TEXT}')]"
SIGN_UP_PASSWORD_TOO_SHORT_ERROR_TEXT = 'Password must be at least 12 characters.'
SIGN_UP_PASSWORD_TOO_SHORT_ERROR_XPATH = f"//*[contains(text(), '{SIGN_UP_PASSWORD_TOO_SHORT_ERROR_TEXT}')]"
SIGN_UP_INVALID_EMAIL_ERROR_TEXT = 'You must provide a valid email address.'
SIGN_UP_INVALID_EMAIL_ERROR_XPATH = f"//*[contains(text(), '{SIGN_UP_INVALID_EMAIL_ERROR_TEXT}')]"
