import pytest
from playwright.sync_api import Page


@pytest.fixture
def go_to_home(authenticated_page: Page) -> None:
    """Navigate to home page. Use this fixture explicitly in tests that need it."""
    authenticated_page.goto("/")