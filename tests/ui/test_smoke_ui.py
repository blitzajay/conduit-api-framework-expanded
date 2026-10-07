import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.ui
def test_home_page_loads(page, ui_base_url):
    page.goto(ui_base_url)
    HomePage(page).assert_loaded()


@pytest.mark.ui
def test_user_can_login_through_ui(page, ui_base_url, registered_user):
    login_page = LoginPage(page)
    login_page.open(ui_base_url)
    login_page.login(registered_user["email"], registered_user["password"])

    page.get_by_text(registered_user["username"], exact=False).first.wait_for()
