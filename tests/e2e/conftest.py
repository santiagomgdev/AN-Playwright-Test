import pytest
from playwright.sync_api import Page
from utils.helpers import timestamp


@pytest.fixture
def go_to_home(authenticated_page: Page) -> None:
    """Navigate to home page. Use this fixture explicitly in tests that need it."""
    authenticated_page.goto("/")


@pytest.fixture
def datos_aspirante_nuevo() -> dict:
    """Datos de un aspirante sintético único por ejecución (evita choques de
    identificación duplicada en la base de datos compartida de dev.local)."""
    sufijo = timestamp()
    sufijo_numerico = sufijo.replace("_", "")
    return {
        "identificacion": f"9{sufijo_numerico[-9:]}",
        "tipo_identificacion": "CEDULA DE CIUDADANIA",
        "primer_apellido": "AUTOMATION",
        # El campo de nombre solo acepta letras (ver docs/known-issues.md).
        "primer_nombre": "TEST",
        "fecha_nacimiento_iso": "1990-01-01",
        # Único por ejecución: el backend parece limitar intentos de OTP por
        # celular/email compartido, no solo por aspirante (ver docs/known-issues.md).
        "celular": f"300{sufijo_numerico[-7:]}",
        "email": f"qa.automation.{sufijo}@example.com",
        "modalidad_pago": "Nómina",
        "ocupacion": "EMPLEADO(a)",
    }