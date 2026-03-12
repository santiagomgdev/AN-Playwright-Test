from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.input_usuario = page.get_by_role("textbox", name="Usuario")
        self.input_contrasena = page.get_by_role("textbox", name="Contraseña")
        self.boton_enviar = page.get_by_role("button", name="Iniciar sesión")

    def login(self, username: str, password: str) -> None:
        self.input_usuario.fill(username)
        self.input_contrasena.fill(password)
        self.boton_enviar.click()
        # self.page.wait_for_url("**/vinculaciones**")

        self.page.wait_for_url(
            f"{self.base_url}/**",
            wait_until="networkidle",
        )

        self.page.wait_for_function(
            "() => !window.location.search.includes('code=')"
        )

        self.page.wait_for_load_state("networkidle")