from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class CargueDocumentosPage(BaseVinculacionPage):
    """/vinculaciones/:plan/cargar-documentos/:asociadoId

    5 documentos requeridos, cada uno PENDIENTE -> CARGADO. Confirmar solo
    se habilita con 5 de 5 cargados. Requisitos: PDF/JPG/PNG, <=5MB, 1 archivo
    por documento.
    """

    DOCUMENTOS_REQUERIDOS = [
        "Fotocopia legible del documento original",
        "Último desprendible de pago del salario o pensión",
        "Formatos aprobación pagaduría",
        "Resultado consulta listas restrictivas",
        "Registro de verificación y aprobación",
    ]

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name="Cargue de Documentos Vinculación"
        )
        self.aviso_cargue_pendiente = page.get_by_text(
            "Debe cargar todos los documentos para habilitar la confirmación",
            exact=False,
        )
        self.progreso_documentos = page.get_by_text(
            "de 5 documentos", exact=False
        )
        self.boton_confirmar = page.get_by_role("button", name="Confirmar")

    def cargar_documento(self, nombre_documento: str, archivo_path: str) -> None:
        fila = self.page.get_by_text(nombre_documento, exact=False).locator(
            "xpath=ancestor::*[.//input[@type='file'] or .//button[contains(., 'Seleccionar')]][1]"
        )
        fila.locator("input[type='file']").set_input_files(archivo_path)

    def confirmar(self) -> None:
        self.boton_confirmar.click()
