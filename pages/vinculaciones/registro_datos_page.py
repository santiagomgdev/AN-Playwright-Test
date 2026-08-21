from playwright.sync_api import Page
from pages.vinculaciones.base_vinculacion_page import BaseVinculacionPage


class DatosInicialesPage(BaseVinculacionPage):
    """/vinculaciones/:plan/registro-datos/datos-iniciales[/:asociadoId]

    Al escribir la identificación y buscar, si el aspirante no existe (404 en
    /asociados/legacy/identificacion/{id}) se revela el resto del formulario
    para registrar uno nuevo.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.input_identificacion = page.get_by_role(
            "textbox", name="No. Identificación *"
        )
        self.boton_buscar = page.locator("i.bi-search").first
        self.combo_tipo_identificacion = page.locator(
            "[formcontrolname='tipoIdentificacion'] [role='combobox']"
        )
        self.input_primer_apellido = page.get_by_role(
            "textbox", name="Primer apellido *"
        )
        self.input_segundo_apellido = page.get_by_role(
            "textbox", name="Segundo apellido"
        )
        self.input_primer_nombre = page.get_by_role(
            "textbox", name="Primer nombre *"
        )
        self.input_segundo_nombre = page.get_by_role(
            "textbox", name="Segundo nombre"
        )
        # Único input type="date" en el formulario de datos iniciales.
        self.input_fecha_nacimiento = page.locator("input[type='date']").first
        self.input_celular = page.get_by_role("textbox", name="Celular *")
        self.input_email = page.get_by_role("textbox", name="Email *")
        self.combo_modalidad_pago = page.locator(
            "[formcontrolname='modalidadPago'] [role='combobox']"
        )
        self.combo_ocupacion = page.locator(
            "[formcontrolname='ocupacion'] [role='combobox']"
        )
        self.boton_continuar = page.get_by_role("button", name="Continuar")

    def navigate(self, plan: str = "basico", path: str = "") -> None:
        super().navigate(f"vinculaciones/{plan}/registro-datos/datos-iniciales")

    def buscar_identificacion(self, identificacion: str) -> None:
        # El componente ui-input no habilita el botón de búsqueda con
        # fill() (set de valor directo) — requiere eventos de teclado reales.
        self.input_identificacion.press_sequentially(identificacion)
        self.boton_buscar.click()

    def registrar_aspirante_nuevo(
        self,
        identificacion: str,
        tipo_identificacion: str,
        primer_apellido: str,
        primer_nombre: str,
        fecha_nacimiento_iso: str,
        celular: str,
        email: str,
        modalidad_pago: str,
        ocupacion: str,
    ) -> None:
        """Modalidad de pago debe ser "Caja" o "Nómina" (controla el salto de etapas)."""
        self.buscar_identificacion(identificacion)
        self.select_dropdown_option(self.combo_tipo_identificacion, tipo_identificacion)
        # ui-input no procesa fill() de forma confiable (ver buscar_identificacion).
        self.input_primer_apellido.press_sequentially(primer_apellido)
        self.input_primer_nombre.press_sequentially(primer_nombre)
        self.input_fecha_nacimiento.fill(fecha_nacimiento_iso)
        self.input_celular.press_sequentially(celular)
        self.input_email.press_sequentially(email)
        self.select_dropdown_option(self.combo_modalidad_pago, modalidad_pago)
        self.select_dropdown_option(self.combo_ocupacion, ocupacion)
        # Deja que se resuelvan validaciones asíncronas (p.ej. duplicidad de
        # identificación) antes de que el botón Continuar quede habilitado.
        self.wait_for_load()
        self.boton_continuar.click()


class ProductosInicialesPage(BaseVinculacionPage):
    """/vinculaciones/:plan/registro-datos/productos-iniciales/:asociadoId"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Productos Iniciales")
        self.combo_oficina_vincula = page.locator(
            "[formcontrolname='oficinaVincula'] [role='combobox']"
        )
        self.combo_oficina_tramita = page.locator(
            "[formcontrolname='oficinaTramita'] [role='combobox']"
        )
        self.boton_continuar = page.get_by_role("button", name="Continuar")

    def fila_producto(self, nombre_producto: str):
        return self.page.locator("table tbody tr", has_text=nombre_producto)

    def diligenciar_valor_inicial(self, nombre_producto: str, valor: str) -> None:
        # Espera a que carguen los valores por defecto calculados por el
        # backend (Aportes/Fondo Mutual) antes de diligenciar, de lo
        # contrario ese cálculo asíncrono sobrescribe lo digitado.
        self.wait_for_load()
        fila = self.fila_producto(nombre_producto)
        # ui-input (con máscara de moneda) no procesa fill() de forma confiable;
        # requiere click explícito para enfocar antes de escribir.
        campo_valor = fila.locator("[formcontrolname='valor'] input")
        campo_valor.click()
        campo_valor.press_sequentially(valor)

    def seleccionar_oficinas(self, oficina_vincula: str, oficina_tramita: str) -> None:
        self.select_dropdown_option(self.combo_oficina_vincula, oficina_vincula)
        self.select_dropdown_option(self.combo_oficina_tramita, oficina_tramita)

    def continuar(self) -> None:
        self.boton_continuar.click()
