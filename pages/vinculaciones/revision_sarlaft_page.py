from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class RevisionSarlaftPage(BaseVinculacionPage):
    """/vinculaciones/:plan/revision-sarlaft/:asociadoId

    Sub-asistente de 3 pasos: "1 Listas / 2 Documentos / 3 Concepto".
    Solo se mapeó el paso "Listas" (el que se muestra por defecto).
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.tab_listas = page.get_by_text("Listas", exact=True)
        self.tab_documentos = page.get_by_text("Documentos", exact=True)
        self.tab_concepto = page.get_by_text("Concepto", exact=True)
        self.combo_confirma_resultado_listas = page.locator(
            "[formcontrolname='confirmaResultadoListas'] [role='combobox']"
        )
        self.radio_pep_si = page.get_by_role("radio", name="Si")
        self.radio_pep_no = page.get_by_role("radio", name="No")
        self.boton_continuar = page.get_by_role("button", name="Continuar")

    def confirmar_listas(self, resultado: str, es_pep: bool) -> None:
        self.select_dropdown_option(self.combo_confirma_resultado_listas, resultado)
        (self.radio_pep_si if es_pep else self.radio_pep_no).check()
        self.boton_continuar.click()
