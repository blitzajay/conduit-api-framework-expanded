from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def assert_loaded(self) -> None:
        self.page.get_by_text("conduit", exact=False).first.wait_for()
