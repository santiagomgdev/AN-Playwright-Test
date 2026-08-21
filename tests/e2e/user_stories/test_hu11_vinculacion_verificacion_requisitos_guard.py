import re

from playwright.sync_api import expect
from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
)

PLAN_SEGMENTO_ETAPAS_TARDIAS = "plan-basico"  # ver docs/known-issues.md


def test_hu11_verificacion_requisitos_redirige_al_home_sin_estar_en_esa_etapa(
    authenticated_page, datos_aspirante_nuevo
):
    """A diferencia de cargue-documentos/revision-sarlaft/decision-final/
    firma-electronica (que renderizan su pantalla igual sin importar la etapa
    real del backend), verificacion-requisitos tiene un guard extra que
    redirige silenciosamente a /autenticacion-autorizacion/usuarios. Esta
    prueba documenta el comportamiento actual como regresión — si algún día
    esta etapa empieza a renderizar igual que las demás, esta prueba debe
    fallar y avisar del cambio (ver docs/known-issues.md)."""
    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(authenticated_page, valor_ahorro_vista="50000")

    asociado_id = authenticated_page.url.rstrip("/").split("/")[-1]
    authenticated_page.goto(
        f"/vinculaciones/{PLAN_SEGMENTO_ETAPAS_TARDIAS}/verificacion-requisitos/{asociado_id}"
    )

    expect(authenticated_page).to_have_url(
        re.compile(r".*/autenticacion-autorizacion/usuarios.*")
    )
