import pytest
from typing import Dict
from config import settings
from fixtures import (
    api_client,
    browser_auth_state,
    authenticated_page,
    base_url,
    base_page,
)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    return {
        **browser_context_args,
        "base_url": settings.BASE_URL,
        "ignore_https_errors": not settings.VERIFY_SSL,
    }