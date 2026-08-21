from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class VerificacionRequisitosPage(BaseVinculacionPage):
    """/vinculaciones/:plan/verificacion-requisitos/:asociadoId

    A diferencia de las demás etapas (que renderizan su shell aunque el
    asociado no esté realmente en esa etapa en backend), esta ruta tiene un
    guard adicional que redirige silenciosamente a /autenticacion-autorizacion/
    usuarios cuando se navega directo sin estar en la etapa real. Ver
    docs/known-issues.md — a confirmar con el equipo si es intencional.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
