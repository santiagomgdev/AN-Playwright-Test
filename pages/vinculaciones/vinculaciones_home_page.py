from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class VinculacionesHomePage(BaseVinculacionPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Gestión de Vinculaciones")
        self.boton_nuevo_registro = page.get_by_role("button", name="Nuevo Registro")
        self.input_identificacion = page.get_by_role(
            "textbox", name="Numero documento"
        )

    def navigate(self, path: str = "vinculaciones") -> None:
        super().navigate(path)

    def buscar_por_identificacion(self, identificacion: str) -> None:
        self.input_identificacion.fill(identificacion)
        self.page.keyboard.press("Enter")
        self.wait_for_load()

    def fila_por_identificacion(self, identificacion: str):
        return self.page.locator("table tbody tr", has_text=identificacion)

    def abrir_registro(self, identificacion: str, accion: str = "Ver") -> None:
        fila = self.fila_por_identificacion(identificacion)
        fila.locator("ui-menu button").click()
        self.page.get_by_role("button", name=accion).click()
