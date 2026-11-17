
import os
import pytest

from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


# Fixture 1: Reusable LoginPage object
@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


# Fixture 2: Capture screenshot when a test fails
@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    yield

    report = getattr(request.node, "rep_call", None)

    if report and report.failed:
        os.makedirs("reports", exist_ok=True)

        screenshot_path = (
            f"reports/{request.node.name}.png"
        )

        page.screenshot(
            path=screenshot_path,
            full_page=True
        )

        print(f"\nScreenshot saved: {screenshot_path}")


# Test Case 1: Successful login
def test_login_success(login_page: LoginPage):

    login_page.open()

    login_page.login("student", "Password123")

    expect(login_page.page).to_have_url(
        "https://practicetestautomation.com/logged-in-successfully/"
    )

    expect(
        login_page.page.get_by_role(
            "heading",
            name="Logged In Successfully"
        )
    ).to_be_visible()

    expect(
        login_page.page.get_by_role(
            "link",
            name="Log out"
        )
    ).to_be_visible()


# Test Case 2: Parameterized invalid login
@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        (
            "wronguser",
            "Password123",
            "Your username is invalid!"
        ),
        (
            "student",
            "WrongPassword123",
            "Your password is invalid!"
        ),
        (
            "wronguser",
            "WrongPassword123",
            "Your username is invalid!"
        ),
    ],
    ids=[
        "invalid-username",
        "invalid-password",
        "both-invalid"
    ]
)
def test_invalid_login(
    login_page: LoginPage,
    username: str,
    password: str,
    expected_message: str
):

    login_page.open()

    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()

    expect(login_page.error_message).to_contain_text(
        expected_message
    )

