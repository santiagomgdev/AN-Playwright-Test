from playwright.sync_api import expect
from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
)
from pages.vinculaciones.firma_electronica_page import FirmaElectronicaPage

PLAN_SEGMENTO_ETAPAS_TARDIAS = "plan-basico"  # ver docs/known-issues.md


def test_hu07_firma_electronica_sin_sobre_muestra_error(
    authenticated_page, datos_aspirante_nuevo
):
    """Navegar a firma-electronica para un asociado sin sobre de firma
    generado muestra un bloque de error crudo (UX conocida, no un bug de la
    prueba). Esta etapa renderiza su pantalla vía navegación directa aunque
    el asociado no esté realmente en esa etapa en backend (ver
    docs/known-issues.md) — no depende de OTP real ni mockeado."""
    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(authenticated_page, valor_ahorro_vista="50000")

    asociado_id = authenticated_page.url.rstrip("/").split("/")[-1]
    authenticated_page.goto(
        f"/vinculaciones/{PLAN_SEGMENTO_ETAPAS_TARDIAS}/firma-electronica/{asociado_id}"
    )

    firma = FirmaElectronicaPage(authenticated_page)
    expect(firma.heading_error).to_be_visible()
    expect(firma.texto_error_sin_sobre).to_be_visible()
