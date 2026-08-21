from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class ValidarIdentidadPage(BaseVinculacionPage):
    """/vinculaciones/:plan/validar-identidad/:asociadoId

    Dos pasos OTP secuenciales: email y luego celular.

    En testing.local el código de prueba es fijo: "000000" valida ambos
    pasos correctamente (confirmado en vivo). En dev.local ese mismo código
    fue rechazado durante una exploración anterior — no asumir que el
    bypass aplica a todos los ambientes (ver docs/known-issues.md).

    self.boton_generar_codigo/input_codigo_otp usan ".first": una vez que un
    paso queda confirmado, su botón/input desaparece del DOM, por lo que
    ".first" siempre apunta al paso todavía activo (no requiere distinguir
    email vs. celular explícitamente).

    Reenviar código está limitado por tiempo ("Debe esperar N segundos...").
    Con un código incorrecto real, tras varios intentos fallidos el paso
    queda bloqueado (ver docs/known-issues.md sobre el umbral variable).
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_generar_codigo = page.get_by_role(
            "button", name="Generar código"
        ).first
        self.boton_reenviar_codigo = page.get_by_role(
            "button", name="Reenviar código"
        ).first
        self.input_codigo_otp = page.get_by_role(
            "textbox", name="Ingresa el código OTP"
        ).first
        # El mensaje varía: "...o vencido, intento N de 5" en el caso normal,
        # o "...bloqueo por seguridad, estado cambia a negada" cuando el
        # backend corta de inmediato (ver docs/known-issues.md).
        self.alerta_error = page.get_by_text("Código incorrecto", exact=False)
        self.boton_confirmar = page.get_by_role("button", name="Confirmar")

    def generar_codigo(self) -> None:
        self.boton_generar_codigo.click()

    def ingresar_codigo(self, codigo: str) -> None:
        # ui-input no procesa fill() de forma confiable; se limpia primero
        # para que cada intento quede como un cambio de valor real.
        self.input_codigo_otp.fill("")
        self.input_codigo_otp.press_sequentially(codigo)
        self.page.keyboard.press("Enter")

    def intentar_codigo_incorrecto(self, codigo: str) -> str:
        """Devuelve el texto de la alerta de error mostrada (incluye "intento N de 5")."""
        self.ingresar_codigo(codigo)
        self.wait_for_load()
        self.alerta_error.wait_for()
        return self.alerta_error.inner_text()

    def validar_paso_con_codigo_fijo(self, codigo: str = "000000") -> None:
        """Genera y confirma un paso OTP (email o celular, según cuál esté
        activo) usando el código fijo de testing.local. No usar en dev.local
        (ver docstring de la clase)."""
        self.generar_codigo()
        self.wait_for_load()
        self.ingresar_codigo(codigo)
        self.wait_for_load()

    def confirmar(self) -> None:
        self.boton_confirmar.click()
