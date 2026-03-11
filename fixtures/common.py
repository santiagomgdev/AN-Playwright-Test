import pytest
from config import settings


@pytest.fixture(scope="session")
def base_url() -> str:
    return settings.BASE_URL