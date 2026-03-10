import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL: str               = os.getenv("BASE_URL", "http://localhost:3000")
API_BASE_URL: str           = os.getenv("API_BASE_URL", "http://localhost:3000/api")
AUTH_USERNAME: str          = os.getenv("AUTH_USERNAME", "")
AUTH_PASSWORD: str          = os.getenv("AUTH_PASSWORD", "")
HEADLESS: bool              = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO: int                = int(os.getenv("SLOW_MO", "0"))
BROWSERS: list[str]         = os.getenv("BROWSERS", "chromium").split(",")

IDENTITY_SERVICE_URL: str   = os.getenv("IDENTITY_SERVICE_URL", "")
OAUTH_CLIENT_ID: str        = os.getenv("OAUTH_CLIENT_ID", "")
OAUTH_CLIENT_SECRET: str    = os.getenv("OAUTH_CLIENT_SECRET", "")
OAUTH_SCOPE: str            = os.getenv("OAUTH_SCOPE", "")
VERIFY_SSL: bool            = os.getenv("VERIFY_SSL", "false").lower() == "true"