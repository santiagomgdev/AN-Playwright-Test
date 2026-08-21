from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class PlanesVinculacionPage(BaseVinculacionPage):
    """/vinculaciones/planes — selección del tipo de plan al iniciar un registro nuevo."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Selección Tipo de Plan")
        self.card_plan_basico = page.get_by_text("Plan Básico", exact=True)
        self.card_plan_complementario = page.get_by_text(
            "Plan Complementario", exact=True
        )

    def navigate(self, path: str = "vinculaciones/planes") -> None:
        super().navigate(path)

    def seleccionar_plan_basico(self) -> None:
        self.card_plan_basico.click()
        self.wait_for_load()

    def seleccionar_plan_complementario(self) -> None:
        self.card_plan_complementario.click()
        self.wait_for_load()
