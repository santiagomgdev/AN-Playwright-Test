from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.usuario_input = page.get_by_role("textbox", name="Usuario")
        self.contrasena_input = page.get_by_role("textbox", name="Contraseña")
        self.boton_enviar = page.get_by_role("button", name="Iniciar sesión")

    def login(self, username: str, password: str) -> None:
        self.usuario_input.fill(username)
        self.contrasena_input.fill(password)
        self.boton_enviar.click()
        self.page.wait_for_url("**/vinculaciones**")