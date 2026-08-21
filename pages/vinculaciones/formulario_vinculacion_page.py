from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class FormularioVinculacionPage(BaseVinculacionPage):
    """/vinculaciones/:plan/formulario-vinculacion/:asociadoId

    Formulario más grande del asistente: 4 acordeones de nivel superior con
    "Guardar" independiente cada uno (Datos personales, Datos laborales,
    Información financiera, Referencias) más "Beneficiarios" (opcional, sin
    explorar). "Datos personales" tiene 3 sub-acordeones propios sin Guardar
    individual — se guardan juntos con el Guardar de "Datos personales".

    Los combobox de ubicación (país/región/localidad) son en cascada: hay
    que seleccionar país y región antes de que "localidad" tenga opciones
    (dispara `GET /localidades?region_id=...`). El orden de aparición en el
    DOM no coincide con el orden de dependencia real.

    "Referencias" reutiliza los mismos formcontrolname (nombresApellidos,
    direccion, celular) para la referencia familiar (índice 0, con
    parentescoId) y la personal (índice 1, sin parentesco) — hay que
    indexar con .nth().
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Formulario de Vinculación")
        self.acordeon_datos_personales = page.get_by_text(
            "Datos personales", exact=True
        )
        self.acordeon_datos_laborales = page.get_by_text(
            "Datos laborales", exact=True
        )
        self.acordeon_informacion_financiera = page.get_by_text(
            "Información financiera", exact=True
        )
        self.acordeon_referencias = page.get_by_text("Referencias", exact=True)

        # --- Datos personales > Información personal ---
        self.sub_informacion_personal = page.get_by_text(
            "Información personal", exact=True
        )
        self.input_fecha_expedicion = page.locator(
            "[formcontrolname='fechaExpedicion'] input"
        )
        self.combo_pais_nacionalidad = page.locator(
            "[formcontrolname='paisNacionalidadId'] [role='combobox']"
        )
        self.combo_pais_expedicion = page.locator(
            "[formcontrolname='paisExpedicionId'] [role='combobox']"
        )
        self.combo_region_expedicion = page.locator(
            "[formcontrolname='regionExpedicionId'] [role='combobox']"
        )
        self.combo_localidad_expedicion = page.locator(
            "[formcontrolname='localidadExpedicionId'] [role='combobox']"
        )
        self.combo_genero = page.locator(
            "[formcontrolname='generoId'] [role='combobox']"
        )

        # --- Datos personales > Información de contacto ---
        self.sub_informacion_contacto = page.get_by_text(
            "Información de contacto", exact=True
        )
        self.input_direccion_residencia = page.locator(
            "[formcontrolname='direccionResidencia'] input"
        )
        self.input_barrio_conjunto = page.locator(
            "[formcontrolname='barrioConjunto'] input"
        )
        self.combo_pais_residencia = page.locator(
            "[formcontrolname='paisResidenciaId'] [role='combobox']"
        )
        self.combo_region_residencia = page.locator(
            "[formcontrolname='regionResidenciaId'] [role='combobox']"
        )
        self.combo_localidad_residencia = page.locator(
            "[formcontrolname='localidadResidenciaId'] [role='combobox']"
        )
        self.combo_zona_vivienda = page.locator(
            "[formcontrolname='zonaVivienda'] [role='combobox']"
        )
        self.combo_tipo_vivienda = page.locator(
            "[formcontrolname='tipoVivienda'] [role='combobox']"
        )
        self.combo_estrato = page.locator(
            "[formcontrolname='estrato'] [role='combobox']"
        )

        # --- Datos personales > Información adicional ---
        self.sub_informacion_adicional = page.get_by_text(
            "Información adicional", exact=True
        )
        self.combo_estado_civil = page.locator(
            "[formcontrolname='estadoCivilId'] [role='combobox']"
        )
        self.combo_nivel_estudio = page.locator(
            "[formcontrolname='nivelEstudioId'] [role='combobox']"
        )
        self.input_ocupacion = page.locator("[formcontrolname='ocupacion'] input")
        self.combo_codigo_ciiu = page.locator(
            "[formcontrolname='codigoCiiuId'] [role='combobox']"
        )
        self.input_numero_personas_cargo = page.locator(
            "[formcontrolname='numeroPersonasCargo'] input"
        )
        self.boton_guardar_datos_personales = page.get_by_role(
            "button", name="Guardar"
        ).first

        # --- Datos laborales ---
        self.combo_tipo_contrato = page.locator(
            "[formcontrolname='tipoContratoId'] [role='combobox']"
        )
        self.input_fecha_ingreso = page.locator(
            "[formcontrolname='fechaIngreso'] input"
        )
        self.input_cargo = page.locator("[formcontrolname='cargo'] input")
        self.input_nombre_empresa = page.locator(
            "[formcontrolname='nombreEmpresa'] input"
        )
        self.input_direccion_empresa = page.locator(
            "[formcontrolname='direccionEmpresa'] input"
        )
        self.combo_pais_empresa = page.locator(
            "[formcontrolname='paisEmpresaId'] [role='combobox']"
        )
        self.combo_region_empresa = page.locator(
            "[formcontrolname='regionEmpresaId'] [role='combobox']"
        )
        self.combo_localidad_empresa = page.locator(
            "[formcontrolname='localidadEmpresaId'] [role='combobox']"
        )
        self.combo_decreto_docente = page.locator(
            "[formcontrolname='decretoDocente'] [role='combobox']"
        )

        # --- Información financiera ---
        self.input_sueldo = page.locator("[formcontrolname='sueldo'] input")
        self.input_otros_ingresos = page.locator(
            "[formcontrolname='otrosIngresos'] input"
        )
        self.input_gastos = page.locator("[formcontrolname='gastos'] input")
        self.input_otros_gastos = page.locator(
            "[formcontrolname='otrosGastos'] input"
        )
        self.input_total_activos = page.locator(
            "[formcontrolname='totalActivos'] input"
        )
        self.input_total_patrimonio = page.locator(
            "[formcontrolname='totalPatrimonio'] input"
        )
        self.input_total_pasivos = page.locator(
            "[formcontrolname='totalPasivos'] input"
        )
        self.input_origen_fondos = page.locator(
            "[formcontrolname='origenFondos'] input"
        )
        # exact=True: "No" hace match por substring con otras opciones si no.
        self.radio_administra_recursos_si = page.locator(
            "[formcontrolname='administraRecursosPublicos']"
        ).get_by_role("radio", name="Si", exact=True)
        self.radio_administra_recursos_no = page.locator(
            "[formcontrolname='administraRecursosPublicos']"
        ).get_by_role("radio", name="No", exact=True)
        self.radio_opera_moneda_extranjera_si = page.locator(
            "[formcontrolname='realizaOperacionesMonedaExtranjera']"
        ).get_by_role("radio", name="Si", exact=True)
        self.radio_opera_moneda_extranjera_no = page.locator(
            "[formcontrolname='realizaOperacionesMonedaExtranjera']"
        ).get_by_role("radio", name="No", exact=True)

        # --- Referencias: .nth(0)=familiar (con parentesco), .nth(1)=personal ---
        self.input_nombres_apellidos_referencia = page.locator(
            "[formcontrolname='nombresApellidos'] input"
        )
        self.input_direccion_referencia = page.locator(
            "[formcontrolname='direccion'] input"
        )
        self.input_celular_referencia = page.locator(
            "[formcontrolname='celular'] input"
        )
        self.combo_parentesco = page.locator(
            "[formcontrolname='parentescoId'] [role='combobox']"
        )

    def abrir_seccion_datos_personales(self) -> None:
        self.acordeon_datos_personales.click()

    def diligenciar_informacion_personal(
        self,
        fecha_expedicion_iso: str,
        pais_nacionalidad: str,
        pais_expedicion: str,
        region_expedicion: str,
        localidad_expedicion: str,
        genero: str,
    ) -> None:
        self.sub_informacion_personal.click()
        self.input_fecha_expedicion.fill(fecha_expedicion_iso)
        self.select_dropdown_option(self.combo_pais_nacionalidad, pais_nacionalidad)
        self.select_dropdown_option(self.combo_pais_expedicion, pais_expedicion)
        self.select_dropdown_option(self.combo_region_expedicion, region_expedicion)
        self.select_dropdown_option(
            self.combo_localidad_expedicion, localidad_expedicion
        )
        self.select_dropdown_option(self.combo_genero, genero)

    def diligenciar_informacion_contacto(
        self,
        direccion_residencia: str,
        barrio_conjunto: str,
        pais_residencia: str,
        region_residencia: str,
        localidad_residencia: str,
        zona_vivienda: str,
        tipo_vivienda: str,
        estrato: str,
    ) -> None:
        self.sub_informacion_contacto.click()
        self.input_direccion_residencia.press_sequentially(direccion_residencia)
        self.input_barrio_conjunto.press_sequentially(barrio_conjunto)
        self.select_dropdown_option(self.combo_pais_residencia, pais_residencia)
        self.select_dropdown_option(self.combo_region_residencia, region_residencia)
        self.select_dropdown_option(
            self.combo_localidad_residencia, localidad_residencia
        )
        self.select_dropdown_option(self.combo_zona_vivienda, zona_vivienda)
        self.select_dropdown_option(self.combo_tipo_vivienda, tipo_vivienda)
        self.select_dropdown_option(self.combo_estrato, estrato)

    def diligenciar_informacion_adicional(
        self,
        estado_civil: str,
        nivel_estudio: str,
        ocupacion: str,
        codigo_ciiu: str,
        numero_personas_cargo: str,
    ) -> None:
        self.sub_informacion_adicional.click()
        self.select_dropdown_option(self.combo_estado_civil, estado_civil)
        self.select_dropdown_option(self.combo_nivel_estudio, nivel_estudio)
        self.input_ocupacion.press_sequentially(ocupacion)
        self.combo_codigo_ciiu.click()
        self.page.get_by_role("textbox").last.press_sequentially(codigo_ciiu)
        self.page.wait_for_timeout(800)
        self.page.locator("div.cursor-pointer, ui-select-option").first.click()
        self.input_numero_personas_cargo.press_sequentially(numero_personas_cargo)

    def guardar_datos_personales(self) -> None:
        self.boton_guardar_datos_personales.click()

    def diligenciar_datos_laborales(
        self,
        tipo_contrato: str,
        fecha_ingreso_iso: str,
        cargo: str,
        nombre_empresa: str,
        direccion_empresa: str,
        pais_empresa: str,
        region_empresa: str,
        localidad_empresa: str,
    ) -> None:
        self.select_dropdown_option(self.combo_tipo_contrato, tipo_contrato)
        self.input_fecha_ingreso.fill(fecha_ingreso_iso)
        self.input_cargo.press_sequentially(cargo)
        self.input_nombre_empresa.press_sequentially(nombre_empresa)
        self.input_direccion_empresa.press_sequentially(direccion_empresa)
        self.select_dropdown_option(self.combo_pais_empresa, pais_empresa)
        self.select_dropdown_option(self.combo_region_empresa, region_empresa)
        self.select_dropdown_option(self.combo_localidad_empresa, localidad_empresa)

    def guardar_datos_laborales(self) -> None:
        self.page.get_by_role("button", name="Guardar").first.click()

    def diligenciar_informacion_financiera(
        self,
        sueldo: str,
        total_activos: str,
        origen_fondos: str,
        administra_recursos_publicos: bool,
        opera_moneda_extranjera: bool,
    ) -> None:
        self.input_sueldo.press_sequentially(sueldo)
        self.input_total_activos.press_sequentially(total_activos)
        self.input_origen_fondos.press_sequentially(origen_fondos)
        (
            self.radio_administra_recursos_si
            if administra_recursos_publicos
            else self.radio_administra_recursos_no
        ).check()
        (
            self.radio_opera_moneda_extranjera_si
            if opera_moneda_extranjera
            else self.radio_opera_moneda_extranjera_no
        ).check()

    def guardar_informacion_financiera(self) -> None:
        self.page.get_by_role("button", name="Guardar").first.click()

    def diligenciar_referencia_familiar(
        self, nombres_apellidos: str, direccion: str, celular: str, parentesco: str
    ) -> None:
        self.input_nombres_apellidos_referencia.nth(0).press_sequentially(
            nombres_apellidos
        )
        self.input_direccion_referencia.nth(0).press_sequentially(direccion)
        self.input_celular_referencia.nth(0).press_sequentially(celular)
        self.select_dropdown_option(self.combo_parentesco, parentesco)

    def diligenciar_referencia_personal(
        self, nombres_apellidos: str, direccion: str, celular: str
    ) -> None:
        self.input_nombres_apellidos_referencia.nth(1).press_sequentially(
            nombres_apellidos
        )
        self.input_direccion_referencia.nth(1).press_sequentially(direccion)
        self.input_celular_referencia.nth(1).press_sequentially(celular)

    def guardar_referencias(self) -> None:
        self.page.get_by_role("button", name="Guardar").first.click()
