from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class GestionarPagaduriaPage(BaseVinculacionPage):
    """/vinculaciones/:plan/gestionar-pagaduria/:asociadoId

    Feature legacy NgRx (no signalStore). Branching de negocio real:
    relacion.requiereGestionPrevia y gestion.resultado ("PREAPROBADO" vs otros)
    determinan la siguiente etapa vía etapaNuevaId devuelto por backend.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name="Gestión Descuento Entidad Pagadora"
        )
        self.boton_relacionar_pagaduria = page.get_by_role(
            "button", name="Relacionar pagaduría"
        )
        self.boton_gestionar_descuentos = page.get_by_role(
            "button", name="Gestionar descuentos"
        )
        self.combo_pagaduria = page.get_by_role("combobox").first
        self.input_archivo = page.locator("input[type='file']")
        self.radio_resultado_aprobado = page.get_by_role("radio", name="Aprobado")
        self.radio_resultado_rechazado = page.get_by_role("radio", name="Rechazado")
        self.input_no_radicado = page.get_by_role("textbox", name="No.Radicado")
        self.boton_confirmar = page.get_by_role("button", name="Confirmar")
        self.boton_guardar = page.get_by_role("button", name="Guardar")
        self.boton_cancelar = page.get_by_role("button", name="Cancelar")

    def relacionar_pagaduria(self, pagaduria: str, archivo_path: str) -> None:
        self.select_dropdown_option(self.combo_pagaduria, pagaduria)
        self.input_archivo.set_input_files(archivo_path)
        self.boton_confirmar.click()

    def gestionar_descuento(self, aprobado: bool, no_radicado: str) -> None:
        self.boton_gestionar_descuentos.click()
        (self.radio_resultado_aprobado if aprobado else self.radio_resultado_rechazado).check()
        self.input_no_radicado.fill(no_radicado)
        self.boton_guardar.click()
