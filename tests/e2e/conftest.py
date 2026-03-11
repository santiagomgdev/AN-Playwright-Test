import pytest
from playwright.sync_api import Page


@pytest.fixture(autouse=True)
def go_to_home(authenticated_page: Page) -> None:
    authenticated_page.goto("/")