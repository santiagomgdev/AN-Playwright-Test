from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class BaseVinculacionPage(BasePage):
    """
    Base para los Page Objects del asistente de vinculación.

    El segmento de plan en la URL es inconsistente en la app real: aparece como
    "basico"/"complementario" en las primeras etapas (registro-datos, evaluar-cupo,
    gestionar-pagaduria) y cambia a "plan-basico"/"plan-complementario" desde
    validar-identidad en adelante. Ver docs/known-issues.md.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def select_dropdown_option(self, trigger: Locator, option_text: str) -> None:
        """
        Los combobox personalizados (ui-select-group / ui-select-option) no exponen
        las opciones via role="option", por lo que no se puede usar get_by_role.
        Se abre el combobox y se hace click en el texto exacto de la opción.
        """
        trigger.click()
        self.page.get_by_text(option_text, exact=True).click()
