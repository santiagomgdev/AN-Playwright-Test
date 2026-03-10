from typing import Any
import requests
import urllib3
from utils.identity_client import IdentityClient
from config import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClient:
    def __init__(self, base_url: str = settings.API_BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.verify = settings.VERIFY_SSL
        self._identity = IdentityClient()

    def authenticate(self) -> None:
        self._identity.login()
        self._sync_token()

    def get(self, path: str, **kwargs) -> Any:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Any:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Any:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Any:
        return self._request("DELETE", path, **kwargs)

    def _sync_token(self) -> None:
        token = self._identity.get_valid_token()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> Any:
        self._sync_token()
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()