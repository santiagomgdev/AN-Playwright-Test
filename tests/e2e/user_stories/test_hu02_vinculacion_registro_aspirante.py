import re

from playwright.sync_api import expect
from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
)


def test_hu02_registrar_aspirante_nuevo_lleva_a_productos_iniciales(
    authenticated_page, datos_aspirante_nuevo
):
    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)

    expect(authenticated_page).to_have_url(
        re.compile(r".*registro-datos/productos-iniciales/.*")
    )
    expect(
        authenticated_page.get_by_text("Aspirante Creado exitosamente", exact=False)
    ).to_be_visible()
