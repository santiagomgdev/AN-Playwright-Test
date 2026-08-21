from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class DecisionFinalPage(BaseVinculacionPage):
    """/vinculaciones/:plan/decision-final/:asociadoId — última etapa (13).

    Concepto de aprobación: APROBADA / DESISTIDA / NEGADA (combobox único,
    sin dropdown separado de "causal" pese a lo que sugiere el enum de
    dominio — la justificación es un solo campo de texto libre cuya
    etiqueta cambia según el concepto elegido).
    """

    CONCEPTO_APROBADA = "APROBADA"
    CONCEPTO_DESISTIDA = "DESISTIDA"
    CONCEPTO_NEGADA = "NEGADA"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.combo_concepto = page.get_by_role("combobox").first
        self.input_no_acta = page.get_by_role("textbox", name="No. Acta *")
        self.input_fecha_acta = page.locator("input[type='date']").first
        # Etiqueta cambia: "Observaciones del ente facultado *" (aprobada) vs
        # "Detalle de la decisión *" (desistida/negada). Se ubica por posición
        # ya que es el último textbox del formulario, no por label fijo.
        self.input_justificacion = page.get_by_role("textbox").last
        self.error_no_acta = page.get_by_text(
            "El número de acta debe ser un número válido de hasta 4 dígitos",
            exact=False,
        )
        self.error_observaciones = page.get_by_text(
            "Las observaciones solo pueden contener letras y espacios",
            exact=False,
        )
        self.boton_confirmar = page.get_by_role("button", name="Confirmar")
        self.boton_cancelar = page.get_by_role("button", name="Cancelar")

    def seleccionar_concepto(self, concepto: str) -> None:
        self.select_dropdown_option(self.combo_concepto, concepto)

    def diligenciar_decision(
        self,
        concepto: str,
        no_acta: str,
        fecha_acta_iso: str,
        justificacion: str,
    ) -> None:
        self.seleccionar_concepto(concepto)
        self.input_no_acta.fill(no_acta)
        self.input_fecha_acta.fill(fecha_acta_iso)
        self.input_justificacion.fill(justificacion)

    def confirmar(self) -> None:
        self.boton_confirmar.click()
