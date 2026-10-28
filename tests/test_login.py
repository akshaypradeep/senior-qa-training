
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_login_success(page: Page):
    login_page = LoginPage(page)

    # Open the login page
    login_page.open()

    # Login with valid credentials
    login_page.login("student", "Password123")

    # Verify successful login
    expect(page).to_have_url(
        "https://practicetestautomation.com/logged-in-successfully/"
    )

    expect(
        page.get_by_role(
            "heading",
            name="Logged In Successfully"
        )
    ).to_be_visible()


def test_login_invalid_password(page: Page):
    login_page = LoginPage(page)

    # Open the login page
    login_page.open()

    # Login with an invalid password
    login_page.login("student", "WrongPassword123")

    # Verify the error message
    expect(login_page.error_message).to_be_visible()

    expect(login_page.error_message).to_contain_text(
        "Your password is invalid!"
    )

