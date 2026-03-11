import pytest
from playwright.sync_api import Page
from utils.api_client import ApiClient


@pytest.fixture
def integration_page(authenticated_page: Page) -> Page:
    authenticated_page.goto("/")
    return authenticated_page


@pytest.fixture(scope="session")
def integration_api_client(api_client: ApiClient) -> ApiClient:
    return api_client