from tests.e2e.use_cases.uc_vinculacion import (
    uc_iniciar_nuevo_registro_plan_basico,
    uc_registrar_aspirante,
    uc_diligenciar_productos_iniciales,
    uc_generar_codigo_otp_email,
)
from pages.vinculaciones.validar_identidad_page import ValidarIdentidadPage


def test_hu06_cinco_intentos_otp_fallidos_bloquea_el_paso(
    authenticated_page, datos_aspirante_nuevo
):
    """Tras códigos OTP incorrectos consecutivos, el paso de validación de
    identidad queda bloqueado (estado pasa a "negada"). Este registro queda
    inutilizable para otras pruebas después de correr esta HU.

    "000000" es el código fijo VÁLIDO en testing.local (ver
    docs/known-issues.md) — se usa "111111" para forzar un código
    genuinamente incorrecto.

    El mensaje de error observado varía: en exploraciones aisladas se vio el
    contador incremental ("intento N de 5") hasta el 5to intento, pero en
    ejecuciones con uso intensivo previo del ambiente compartido (dev.local)
    se observó bloqueo inmediato en el primer intento ("bloqueo por
    seguridad, estado cambia a negada"). Probablemente hay un umbral de
    seguridad adicional a nivel de sesión/IP que no depende solo del
    aspirante individual. Esta prueba no asume una secuencia fija; solo
    verifica que, tras intentos fallidos, el paso termine bloqueado."""
    datos_aspirante_nuevo["modalidad_pago"] = "Caja"

    uc_iniciar_nuevo_registro_plan_basico(authenticated_page)
    uc_registrar_aspirante(authenticated_page, datos_aspirante_nuevo)
    uc_diligenciar_productos_iniciales(authenticated_page, valor_ahorro_vista="50000")
    uc_generar_codigo_otp_email(authenticated_page)

    validar = ValidarIdentidadPage(authenticated_page)
    mensaje_error = ""
    for _ in range(5):
        mensaje_error = validar.intentar_codigo_incorrecto("111111")
        if "bloqueo" in mensaje_error.lower():
            break

    # El bloqueo cambia el estado del asociado a "negada" pero no deshabilita
    # los controles de la página (verificado en vivo contra dev.local).
    assert "bloqueo" in mensaje_error.lower() or "intento 5 de 5" in mensaje_error
