from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class ConsultarListasPage(BaseVinculacionPage):
    """/vinculaciones/:plan/consultar-listas/:asociadoId"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name="Consulta en Listas Restrictivas"
        )
        self.banner_identidad_validada = page.get_by_text(
            "Identidad validada", exact=False
        )
        # exact=True: "Coincidencia" sin esto hace match por substring con
        # "No coincidencia" (ambos contienen "coincidencia").
        self.radio_coincidencia = page.get_by_role(
            "radio", name="Coincidencia", exact=True
        )
        self.radio_no_coincidencia = page.get_by_role(
            "radio", name="No coincidencia", exact=True
        )
        self.radio_no_encontrado = page.get_by_role(
            "radio", name="No encontrado", exact=True
        )
        # exact=True: sin esto, "No" hace match por substring con
        # "No coincidencia"/"No encontrado" (strict mode violation).
        self.radio_pep_si = page.get_by_role("radio", name="Si", exact=True)
        self.radio_pep_no = page.get_by_role("radio", name="No", exact=True)
        self.input_archivo = page.locator("input[type='file']").first
        self.boton_confirmar = page.get_by_role("button", name="Confirmar")

    def confirmar_sin_coincidencias(self, archivo_path: str) -> None:
        self.radio_no_coincidencia.check()
        self.radio_pep_no.check()
        self.input_archivo.set_input_files(archivo_path)
        self.boton_confirmar.click()
