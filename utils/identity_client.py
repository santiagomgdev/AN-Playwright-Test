from datetime import datetime, timedelta, timezone
from typing import Optional
import requests
import urllib3
from config import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IdentityClient:
    def __init__(self) -> None:
        self.token_endpoint = f"{settings.IDENTITY_SERVICE_URL}/connect/token"
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None

    def login(self) -> None:
        response = requests.post(
            self.token_endpoint,
            data={
                "grant_type": "password",
                "client_id": settings.OAUTH_CLIENT_ID,
                "client_secret": settings.OAUTH_CLIENT_SECRET,
                "username": settings.AUTH_USERNAME,
                "password": settings.AUTH_PASSWORD,
                "scope": settings.OAUTH_SCOPE,
            },
            verify=settings.VERIFY_SSL,
            timeout=10,
        )
        response.raise_for_status()
        token_data = response.json()

        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in", 3600)
        self.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        print(f"Token obtained for {settings.AUTH_USERNAME} (expires in {expires_in}s)")

    def is_token_expired(self) -> bool:
        if not self.token_expires_at:
            return True
        return datetime.now(timezone.utc) >= self.token_expires_at

    def get_valid_token(self) -> str:
        if not self.access_token or self.is_token_expired():
            self.login()
        return self.access_token

    def get_auth_header(self) -> dict:
        return {"Authorization": f"Bearer {self.get_valid_token()}"}