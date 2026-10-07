from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/login")

    def login(self, email: str, password: str) -> None:
        self.page.get_by_placeholder("Email").fill(email)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
