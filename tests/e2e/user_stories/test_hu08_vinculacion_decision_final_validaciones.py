from playwright.sync_api import expect
from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
)
from pages.vinculaciones.decision_final_page import DecisionFinalPage

PLAN_SEGMENTO_ETAPAS_TARDIAS = "plan-basico"  # ver docs/known-issues.md


def _ir_a_decision_final(page, datos_aspirante_nuevo):
    uc_iniciar_nuevo_registro_plan_basico(page)
    uc_registrar_aspirante(page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(page, valor_ahorro_vista="50000")
    asociado_id = page.url.rstrip("/").split("/")[-1]
    page.goto(f"/vinculaciones/{PLAN_SEGMENTO_ETAPAS_TARDIAS}/decision-final/{asociado_id}")
    return DecisionFinalPage(page)


def test_hu08_no_acta_rechaza_valor_no_numerico(authenticated_page, datos_aspirante_nuevo):
    """Validación de formulario en decisión-final es del lado del cliente y no
    requiere que el asociado esté realmente en etapa 13 (ver docs/known-issues.md
    sobre el 409 al confirmar). Prueba solo la regla de "No. Acta"."""
    decision = _ir_a_decision_final(authenticated_page, datos_aspirante_nuevo)

    decision.seleccionar_concepto(DecisionFinalPage.CONCEPTO_APROBADA)
    decision.input_no_acta.fill("abc")
    decision.input_no_acta.blur()

    expect(decision.error_no_acta).to_be_visible()


def test_hu09_observaciones_rechaza_caracteres_no_alfabeticos(
    authenticated_page, datos_aspirante_nuevo
):
    decision = _ir_a_decision_final(authenticated_page, datos_aspirante_nuevo)

    decision.seleccionar_concepto(DecisionFinalPage.CONCEPTO_APROBADA)
    decision.input_justificacion.fill("Aprobado - cumple requisitos 123.")
    decision.input_justificacion.blur()

    expect(decision.error_observaciones).to_be_visible()


def test_hu10_concepto_negada_cambia_etiqueta_de_justificacion(
    authenticated_page, datos_aspirante_nuevo
):
    """Al elegir NEGADA (o DESISTIDA) la etiqueta del campo de texto cambia de
    "Observaciones del ente facultado" a "Detalle de la decisión"."""
    decision = _ir_a_decision_final(authenticated_page, datos_aspirante_nuevo)

    decision.seleccionar_concepto(DecisionFinalPage.CONCEPTO_NEGADA)

    expect(
        authenticated_page.get_by_text("Detalle de la decisión", exact=False)
    ).to_be_visible()
