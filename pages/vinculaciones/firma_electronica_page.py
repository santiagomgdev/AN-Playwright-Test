from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class FirmaElectronicaPage(BaseVinculacionPage):
    """/vinculaciones/:plan/firma-electronica/:asociadoId

    Cuando no existe un "sobre" de firma para el asociado, la página muestra
    un bloque de error crudo (sin estilo de toast): heading "Error en firma
    electronica:" + párrafo "No se encontró un sobre de firma para el asociado."
    Esto es UX conocida/documentada, no un bug de la prueba.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name="Firma Electrónica Vinculación"
        )
        self.heading_error = page.get_by_role(
            "heading", name="Error en firma electronica:"
        )
        self.texto_error_sin_sobre = page.get_by_text(
            "No se encontró un sobre de firma para el asociado.", exact=False
        )
        self.tabla_estado_sobre = page.get_by_role(
            "table", name="Estado del sobre"
        )
        self.boton_cancelar = page.get_by_role("button", name="Cancelar")
