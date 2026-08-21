import re

from playwright.sync_api import expect
from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
)


def test_hu04_modalidad_caja_salta_evaluar_cupo_y_gestionar_pagaduria(
    authenticated_page, datos_aspirante_nuevo
):
    """Cuando modalidadPagoId corresponde a "Caja", el asistente omite
    Evaluar Cupo y Gestionar Pagaduría, yendo directo a Validar Identidad."""
    datos_aspirante_nuevo["modalidad_pago"] = "Caja"

    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(authenticated_page, valor_ahorro_vista="50000")

    expect(authenticated_page).to_have_url(re.compile(r".*validar-identidad/.*"))
    expect(authenticated_page).not_to_have_url(re.compile(r".*evaluar-cupo.*"))
    expect(authenticated_page).not_to_have_url(re.compile(r".*gestionar-pagaduria.*"))
