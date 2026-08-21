from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class EvaluarCupoPage(BaseVinculacionPage):
    """/vinculaciones/:plan/evaluar-cupo/:asociadoId

    Se salta cuando modalidadPagoId == "Caja" (ver registro_datos_page).
    Los 6 campos de moneda comparten el mismo accessible name ("$ 0,00"),
    por lo que se distinguen por orden en el DOM.
    """

    CAMPO_SUELDO = 0
    CAMPO_BONIFICACIONES = 1
    CAMPO_AUXILIOS = 2
    CAMPO_PRIMA_TECNICA = 3
    CAMPO_DESCUENTO_SALUD_PENSION = 4
    CAMPO_TOTAL_DEDUCCIONES = 5

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Cálculo del Cupo")
        self.radio_pensionado_si = page.get_by_role("radio", name="Sí")
        self.radio_pensionado_no = page.get_by_role("radio", name="No")
        self.campos_moneda = page.get_by_role("textbox", name="$ 0,00")
        self.boton_calcular = page.get_by_role("button", name="Calcular Cupo")
        self.boton_guardar = page.get_by_role("button", name="Guardar")

    def diligenciar_cupo(
        self, es_pensionado: bool, sueldo: str, total_deducciones: str = "1000"
    ) -> None:
        """"Sueldo básico" y "Total deducciones de nómina" son ambos
        obligatorios (*) aunque el segundo no lo parezca a simple vista.
        "0" no es un valor válido para total_deducciones — la máscara de
        moneda no lo formatea y el campo queda inválido (ver
        docs/known-issues.md)."""
        (self.radio_pensionado_si if es_pensionado else self.radio_pensionado_no).check()
        # ui-input (con máscara de moneda) no procesa fill() de forma confiable.
        self.campos_moneda.nth(self.CAMPO_SUELDO).press_sequentially(sueldo)
        self.campos_moneda.nth(self.CAMPO_TOTAL_DEDUCCIONES).press_sequentially(
            total_deducciones
        )
        self.boton_calcular.click()

    def guardar(self) -> None:
        self.boton_guardar.click()
