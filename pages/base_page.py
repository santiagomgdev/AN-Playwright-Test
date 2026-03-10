from playwright.sync_api import Page
from config import settings


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = settings.BASE_URL

    def navigate(self, path: str = "") -> None:
        self.page.goto(f"{self.base_url}/{path.lstrip('/')}")

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("networkidle")