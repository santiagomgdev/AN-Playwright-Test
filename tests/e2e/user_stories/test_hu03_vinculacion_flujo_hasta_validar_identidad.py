import re

from playwright.sync_api import expect
from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
    uc_diligenciar_evaluar_cupo,
    uc_relacionar_pagaduria,
)

ARCHIVO_SOPORTE = "fixtures/data/soporte_generico.pdf"


def test_hu03_flujo_modalidad_nomina_pasa_por_cupo_y_pagaduria(
    authenticated_page, datos_aspirante_nuevo
):
    """Modalidad de pago = Nómina no se salta ninguna etapa: registro-datos ->
    productos-iniciales -> evaluar-cupo -> gestionar-pagaduria -> validar-identidad."""
    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(authenticated_page, valor_ahorro_vista="50000")

    expect(authenticated_page).to_have_url(re.compile(r".*evaluar-cupo/.*"))
    uc_diligenciar_evaluar_cupo(authenticated_page, sueldo="2500000")

    expect(authenticated_page).to_have_url(re.compile(r".*gestionar-pagaduria/.*"))
    uc_relacionar_pagaduria(
        authenticated_page, pagaduria="SECRETARIA DE EDUCACION DE BUCARAMANGA",
        archivo_path=ARCHIVO_SOPORTE,
    )

    expect(authenticated_page).to_have_url(re.compile(r".*validar-identidad/.*"))
