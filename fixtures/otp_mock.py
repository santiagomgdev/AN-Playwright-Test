import pytest
from playwright.sync_api import Page, Route


class OtpBypassMock:
    """
    Intercepta las llamadas de red de validar-identidad para forzar un estado
    "validado" en el frontend sin depender de un código OTP real.

    LIMITACIÓN CONOCIDA (ver docs/known-issues.md): esto solo engaña al SPA
    para que navegue a las siguientes etapas y renderice sus pantallas. El
    backend NO avanza la etapa real del aspirante — un intento de confirmar
    decisión final (u otra etapa que el backend valide) sobre un asociado
    mockeado así devuelve 409 ("El asociado no se encuentra en etapa de
    decisión final. Etapa actual: 4"). Útil solo para pruebas de UI/validación
    de formularios en etapas posteriores, NO para pruebas end-to-end que
    dependan de progresión real de backend.
    """

    def __init__(self) -> None:
        self.validado_email = False
        self.validado_celular = False

    def _handle(self, route: Route) -> None:
        request = route.request
        url = request.url

        if request.method == "POST" and url.endswith("/valida"):
            if "celular" in url or self.validado_email:
                self.validado_celular = True
            else:
                self.validado_email = True
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"succes": true, "data": {"es_validado": true}}',
            )
            return

        if request.method == "POST" and "/otp" in url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"succes": true, "data": {"fecha_generacion": "2026-01-01T00:00:00Z"}}',
            )
            return

        if request.method == "GET":
            completo = self.validado_email and self.validado_celular
            route.fulfill(
                status=200,
                content_type="application/json",
                body=(
                    '{"succes": true, "data": {'
                    f'"es_validado": {str(completo).lower()}, '
                    f'"validacion_completa": {str(completo).lower()}'
                    "}}"
                ),
            )
            return

        route.continue_()

    def install(self, page: Page) -> None:
        page.route("**/validacion-identidad/**", self._handle)


@pytest.fixture
def otp_bypass_mock(page: Page) -> OtpBypassMock:
    mock = OtpBypassMock()
    mock.install(page)
    return mock
