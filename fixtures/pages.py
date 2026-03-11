import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage


@pytest.fixture
def base_page(page: Page) -> BasePage:
    return BasePage(page)