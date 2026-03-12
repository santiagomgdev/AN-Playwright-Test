import json

import pytest
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page
from utils.api_client import ApiClient
from pages.login_page import LoginPage
from config import settings

AUTH_STATE_PATH = "reports/auth.json"
SESSION_STORAGE_PATH = "reports/session_storage.json"


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
) -> dict:
    """
    Inicia sesión en la aplicación una vez por sesión de prueba y guarda el estado de autenticación.
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    login = LoginPage(page)

    page.goto(settings.BASE_URL)
    page.wait_for_load_state("networkidle")
    login.login(settings.AUTH_USERNAME, settings.AUTH_PASSWORD)

    # Capture sessionStorage as a plain dict
    session_storage = page.evaluate("""
        () => {
            const data = {};
            for (let i = 0; i < sessionStorage.length; i++) {
                const key = sessionStorage.key(i);
                data[key] = sessionStorage.getItem(key);
            }
            return data;
        }
    """)

    with open(SESSION_STORAGE_PATH, "w") as f:
        json.dump(session_storage, f)

    context.storage_state(path=AUTH_STATE_PATH)
    context.close()

    return {
        "storage_state": AUTH_STATE_PATH,
        "session_storage": SESSION_STORAGE_PATH,
    }


@pytest.fixture
def authenticated_page(
    context: BrowserContext,
    browser_auth_state: dict,
) -> Generator[Page, None, None]:
    with open(browser_auth_state["session_storage"]) as f:
        session_data = json.load(f)

    injections = "\n".join([
        f"sessionStorage.setItem({json.dumps(k)}, {json.dumps(v)});"
        for k, v in session_data.items()
    ])

    context.add_init_script(f"""
        (function() {{
            const targetOrigin = '{settings.BASE_URL}';
            if (window.location.origin === targetOrigin) {{
                {injections}
            }}
        }})();
    """)

    page = context.new_page()
    page.goto(settings.BASE_URL)
    page.wait_for_load_state("networkidle")

    yield page