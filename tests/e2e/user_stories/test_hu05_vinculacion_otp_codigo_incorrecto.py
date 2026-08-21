from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
    uc_generar_codigo_otp_email,
)
from pages.vinculaciones.validar_identidad_page import ValidarIdentidadPage


def test_hu05_codigo_otp_incorrecto_muestra_contador_de_intentos(
    authenticated_page, datos_aspirante_nuevo
):
    """Un código OTP inválido es rechazado por el backend real y el mensaje
    de error incluye el contador de intentos.

    "000000" es el código fijo VÁLIDO en testing.local (ver
    docs/known-issues.md) — se usa "111111" para forzar un código
    genuinamente incorrecto."""
    datos_aspirante_nuevo["modalidad_pago"] = "Caja"  # llega más rápido a validar-identidad

    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(authenticated_page, valor_ahorro_vista="50000")
    uc_generar_codigo_otp_email(authenticated_page)

    validar = ValidarIdentidadPage(authenticated_page)
    mensaje_error = validar.intentar_codigo_incorrecto("111111")

    assert "intento 1 de 5" in mensaje_error
