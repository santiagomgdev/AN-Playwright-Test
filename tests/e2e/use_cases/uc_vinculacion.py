"""
Casos de uso atómicos para el asistente de vinculación. Sin aserciones -
las historias de usuario en tests/e2e/user_stories/ componen estas funciones
y agregan la verificación final.
"""

from playwright.sync_api import Page
from pages.vinculaciones.vinculaciones_home_page import VinculacionesHomePage
from pages.vinculaciones.planes_page import PlanesVinculacionPage
from pages.vinculaciones.registro_datos_page import (
    DatosInicialesPage,
    ProductosInicialesPage,
)
from pages.vinculaciones.evaluar_cupo_page import EvaluarCupoPage
from pages.vinculaciones.gestionar_pagaduria_page import GestionarPagaduriaPage
from pages.vinculaciones.validar_identidad_page import ValidarIdentidadPage
from pages.vinculaciones.consultar_listas_page import ConsultarListasPage
from pages.vinculaciones.formulario_vinculacion_page import FormularioVinculacionPage
from pages.vinculaciones.cargue_documentos_page import CargueDocumentosPage
from pages.vinculaciones.revision_sarlaft_page import RevisionSarlaftPage
from pages.vinculaciones.decision_final_page import DecisionFinalPage


def uc_iniciar_nuevo_registro_plan_basico(page: Page) -> None:
    home = VinculacionesHomePage(page)
    home.navigate()
    home.boton_nuevo_registro.click()
    planes = PlanesVinculacionPage(page)
    planes.seleccionar_plan_basico()


def uc_registrar_aspirante(page: Page, datos: dict) -> None:
    """datos: identificacion, tipo_identificacion, primer_apellido, primer_nombre,
    fecha_nacimiento_iso, celular, email, modalidad_pago, ocupacion."""
    datos_iniciales = DatosInicialesPage(page)
    datos_iniciales.registrar_aspirante_nuevo(
        identificacion=datos["identificacion"],
        tipo_identificacion=datos["tipo_identificacion"],
        primer_apellido=datos["primer_apellido"],
        primer_nombre=datos["primer_nombre"],
        fecha_nacimiento_iso=datos["fecha_nacimiento_iso"],
        celular=datos["celular"],
        email=datos["email"],
        modalidad_pago=datos["modalidad_pago"],
        ocupacion=datos["ocupacion"],
    )


def uc_diligenciar_productos_iniciales(page: Page, valor_ahorro_vista: str) -> None:
    productos = ProductosInicialesPage(page)
    # Seleccionar oficinas primero: dispara un recálculo asíncrono de los
    # valores por defecto que puede sobrescribir el valor digitado si se
    # diligencia antes (ver docs/known-issues.md).
    productos.seleccionar_oficinas("PRINCIPAL", "PRINCIPAL")
    productos.diligenciar_valor_inicial("Ahorro a la Vista", valor_ahorro_vista)
    productos.continuar()


def uc_diligenciar_evaluar_cupo(page: Page, sueldo: str) -> None:
    cupo = EvaluarCupoPage(page)
    cupo.diligenciar_cupo(es_pensionado=False, sueldo=sueldo)
    cupo.guardar()


def uc_relacionar_pagaduria(page: Page, pagaduria: str, archivo_path: str) -> None:
    pagaduria_page = GestionarPagaduriaPage(page)
    pagaduria_page.relacionar_pagaduria(pagaduria, archivo_path)


def uc_generar_codigo_otp_email(page: Page) -> None:
    validar = ValidarIdentidadPage(page)
    validar.generar_codigo()


def uc_validar_identidad_completa(page: Page) -> None:
    """Completa los dos pasos OTP (email y celular) con el código fijo de
    testing.local ("000000") y confirma. Solo funciona en testing.local —
    dev.local no acepta este código (ver docs/known-issues.md)."""
    validar = ValidarIdentidadPage(page)
    validar.validar_paso_con_codigo_fijo()
    validar.validar_paso_con_codigo_fijo()
    validar.confirmar()


def uc_confirmar_consulta_listas_sin_coincidencias(page: Page, archivo_path: str) -> None:
    listas = ConsultarListasPage(page)
    listas.confirmar_sin_coincidencias(archivo_path)


def uc_diligenciar_formulario_vinculacion_completo(page: Page) -> None:
    """Completa las 4 secciones con Guardar propio (Datos personales, Datos
    laborales, Información financiera, Referencias). "Beneficiarios" es
    opcional y no se diligencia."""
    formulario = FormularioVinculacionPage(page)

    formulario.abrir_seccion_datos_personales()
    formulario.diligenciar_informacion_personal(
        fecha_expedicion_iso="2010-01-01",
        pais_nacionalidad="COLOMBIA",
        pais_expedicion="COLOMBIA",
        region_expedicion="ANTIOQUIA",
        localidad_expedicion="BELLO",
        genero="MASCULINO",
    )
    formulario.diligenciar_informacion_contacto(
        direccion_residencia="CALLE 123 45 67",
        barrio_conjunto="CENTRO",
        pais_residencia="COLOMBIA",
        region_residencia="ANTIOQUIA",
        localidad_residencia="BELLO",
        zona_vivienda="Urbana",
        tipo_vivienda="Propia",
        estrato="3",
    )
    formulario.diligenciar_informacion_adicional(
        estado_civil="Soltero(a)",
        nivel_estudio="Universitario",
        ocupacion="EMPLEADO",
        codigo_ciiu="COMERCIO",
        numero_personas_cargo="0",
    )
    formulario.guardar_datos_personales()
    page.wait_for_load_state("networkidle")

    formulario.acordeon_datos_laborales.click()
    formulario.diligenciar_datos_laborales(
        tipo_contrato="Término Indefinido",
        fecha_ingreso_iso="2020-01-01",
        cargo="ANALISTA",
        nombre_empresa="EMPRESA DE PRUEBA SAS",
        direccion_empresa="CALLE 1 2 3",
        pais_empresa="COLOMBIA",
        region_empresa="ANTIOQUIA",
        localidad_empresa="BELLO",
    )
    formulario.guardar_datos_laborales()
    page.wait_for_load_state("networkidle")

    formulario.acordeon_informacion_financiera.click()
    formulario.diligenciar_informacion_financiera(
        sueldo="2500000",
        total_activos="10000000",
        origen_fondos="SALARIO",
        administra_recursos_publicos=False,
        opera_moneda_extranjera=False,
    )
    formulario.guardar_informacion_financiera()
    page.wait_for_load_state("networkidle")

    formulario.acordeon_referencias.click()
    formulario.diligenciar_referencia_familiar(
        nombres_apellidos="REFERENCIA FAMILIAR TEST",
        direccion="CALLE 1 2 3",
        celular="3001112233",
        parentesco="HERMANOS",
    )
    formulario.diligenciar_referencia_personal(
        nombres_apellidos="REFERENCIA PERSONAL TEST",
        direccion="CALLE 4 5 6",
        celular="3004445566",
    )
    formulario.guardar_referencias()
    page.wait_for_load_state("networkidle")


def uc_cargar_documentos_requeridos(page: Page, archivo_path: str) -> None:
    cargue = CargueDocumentosPage(page)
    for documento in cargue.DOCUMENTOS_REQUERIDOS:
        cargue.cargar_documento(documento, archivo_path)
    cargue.confirmar()


def uc_confirmar_revision_sarlaft_listas(page: Page) -> None:
    sarlaft = RevisionSarlaftPage(page)
    sarlaft.confirmar_listas(resultado="No coincidencia", es_pep=False)


def uc_diligenciar_decision_final(page: Page, concepto: str, justificacion: str) -> None:
    decision = DecisionFinalPage(page)
    decision.diligenciar_decision(
        concepto=concepto,
        no_acta="1234",
        fecha_acta_iso="2026-01-01",
        justificacion=justificacion,
    )
