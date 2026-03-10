import re
from datetime import datetime


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def build_url(base: str, path: str) -> str:
    return f"{base.rstrip('/')}/{path.lstrip('/')}"