import pytest
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page
from utils.api_client import ApiClient
from pages.login_page import LoginPage
from config import settings

AUTH_STATE_PATH = "reports/auth.json"


# -----------------------------------------------
# API auth fixture — HTTP Bearer token
# Usado por: tests/api/ y tests/integration/
# -----------------------------------------------

@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    client = ApiClient()
    client.authenticate()
    return client


# -----------------------------------------------
# E2E auth fixture — estado de autenticación del navegador
# Usado por: tests/e2e/
# -----------------------------------------------

@pytest.fixture(scope="session")
def browser_auth_state(
    browser: Browser,
    browser_context_args: dict,
) -> str:
    """
    Inicia sesión en la aplicación una vez por sesión de prueba y guarda el estado de autenticación.
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    login = LoginPage(page)

    page.goto(settings.BASE_URL)
    # login.wait_for_load()
    login.login(settings.AUTH_USERNAME, settings.AUTH_PASSWORD)

    context.storage_state(path=AUTH_STATE_PATH)
    context.close()

    return AUTH_STATE_PATH


@pytest.fixture
def authenticated_page(
    browser: Browser,
    browser_context_args: dict,
    browser_auth_state: str,
) -> Generator[Page, None, None]:
    """
    Proporciona una página autenticada para pruebas E2E.
    """
    context: BrowserContext = browser.new_context(
        storage_state=browser_auth_state,
        **browser_context_args
    )
    page = context.new_page()

    yield page

    context.close()