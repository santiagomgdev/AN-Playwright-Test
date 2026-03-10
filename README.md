# QA Suite

## Conceptos

La estructura general de las pruebas en Playwright se divide en los siguientes apartados:

### Acciones

- Las pruebas inician con la navegación de la página a través de la URL, de esta forma la prueba puede interactuar con los elementos de la página; esta navegación está sujeta a las redirecciones y/o errores en el recurso accedido.

```python
page.goto("https://playwright.dev/")

# Ejemplo Nexus
page.goto("https://???/")
```

- Las pruebas se componen a través de interacciones, los cuales permiten realizar acciones usando [Locators API](https://playwright.dev/python/docs/locators), estos representan una forma de acceder a los elementos de una página.

```python
# Playwright va a esperar a que el elemento sea accionable (si esa palabra existe)
# Crear un locator
get_started = page.get_by_role("link", name="Get started")

# Hacer click en el locator
get_started.click()

# Realizar las operaciones anteriores en una sola linea
# Ejemplo Nexus
page.get_by_role("link", name="???").click
```

### Aserciones

- Las aserciones son una forma de comprobar que las pruebas cumplan con una serie de condiciones esperadas.

```python
# Espera a que la página contenga el título "Playwright"
import re
from playwright.sync_api import expect

expect(page).to_have_title(re.compile("Playwright"))

# Ejemplo Nexus
# Probar las siguientes aserciones:

# expect(locator).to_be_checked() Checkbox is checked
# expect(locator).to_be_enabled() Control is enabled
# expect(locator).to_be_visible() Element is visible
# expect(locator).to_contain_text() Element contains text
# expect(locator).to_have_attribute() Element has attribute
# expect(locator).to_have_count() List of elements has given length
# expect(locator).to_have_text() Element matches text
# expect(locator).to_have_value() Input element has value
# expect(page).to_have_title() Page has title
# expect(page).to_have_url() Page has URL
```

### Fixtures

- Las pruebas se basan en el concepto de Fixtures, los cuales representan datos de prueba reutilizables en las pruebas generales en donde estas se requieran; bajo este concepto, las páginas se usan como fixtures, lo cuál permite aislarlas de las pruebas por el contexto del navegador, esto permite ejecutar cada prueba en un perfil de navegador distinto.

```python
from playwright.sync_api import Page

def test_example_test(page: Page):
  pass
  # "page" pertenece a un contexto de navegador aislado para esta prueba, lo que significa que cualquier cambio en la página no afectará a otras pruebas.

def test_another_test(page: Page):
  pass
  # "page" es una nueva instancia de página, completamente independiente de la prueba anterior, lo que garantiza que las pruebas no interfieran entre sí.
  
# Ejemplo Nexus
```

- Para usar fixtures:

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    
    print("before the test runs")

    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")
    yield
    
    print("after the test runs")

def test_main_navigation(page: Page):
    # Assertions use the expect API.
    expect(page).to_have_url("https://playwright.dev/")

# Ejemplo Nexus
```

## Estructura del Proyecto

Las pruebas E2E validan el flujo completo de la aplicación y el modelo de negocio, integrando todos los componentes del sistema; las pruebas de integración validan que los componentes individuales del sistema se comuniquen entre si de forma adecuada, asegurando que los datos se transmitan correctamente.

```txt
qa/
├── config/                  # Configuraciones de entorno y constantes
├── docs/                    # Referencias y guías de comandos
│   ├── installation.md
│   ├── codegen.md
│   ├── debug.md
│   └── trace-viewer.md
├── fixtures/                # Fixtures compartidos de pytest
│   ├── auth.py              # Fixtures relacionadas con autenticación
│   ├── common.py            # Fixtures genéricas reutilizables
│   └── pages.py             # Fixtures de Page Objects
├── pages/                   # Page Objects para UI tests
│   └── base_page.py
├── reports/                 # Informes de ejecución (HTML, traces, etc.)
├── tests/
│   ├── conftest.py          # Fixtures específicas de cada capa
│   ├── e2e/
│   │   ├── conftest.py
│   │   ├── use_cases/
│   │   └── user_stories/
│   ├── integration/
│   │   ├── conftest.py
│   │   ├── use_cases/
│   │   └── user_stories/
│   └── api/
│       └── conftest.py
└── utils/
    ├── api_client.py        # Cliente HTTP para API tests
    └── helpers.py
```

---

### Casos de Uso

Los casos de uso son pruebas atómicas que validan un comportamiento específico, estas pruebas se ubican en la carpeta `use_cases/` y deben ser lo más aisladas posible, sin depender de otras funcionalidades.

```python
# tests/e2e/use_cases/uc_login.py
def uc_user_can_log_in(page, credentials):
    page.goto("/login")
    page.get_by_label("Email").fill(credentials["email"])
    page.get_by_label("Password").fill(credentials["password"])
    page.get_by_role("button", name="Sign in").click()

```

### Historias de Usuario

Las historias de usuario son pruebas de nivel HU que importan y componen casos de uso para validar un flujo completo desde la perspectiva del usuario, estas pruebas se ubican en la carpeta `user_stories/` y deben enfocarse en el resultado final del flujo.

```python
# tests/e2e/user_stories/test_hu_01_onboarding.py
from tests.e2e.use_cases.uc_login import uc_user_can_log_in

def test_hu_01_user_completes_onboarding(page, credentials):
    uc_user_can_log_in(page, credentials)
    # ... continue the user story
```

---

## Variables de Entorno

```bash
# Copiar el archivo de ejemplo para configurar las variables de entorno
cp .env.example .env
```

---

## Instalación

Ver [`docs/installation.md`](docs/installation.md) para la guía completa.

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

---

## Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas por carpeta
pytest tests/e2e/
pytest tests/integration/
pytest tests/api/

# Solo casos de uso
pytest tests/e2e/use_cases/

# Solo historias de usuario
pytest tests/e2e/user_stories/

# Headed mode
pytest --headed

# Seleccionar navegador
pytest --browser chromium
pytest --browser webkit
pytest --browser firefox

# Ejecución paralela
pytest --numprocesses auto

# Generar reporte HTML
pytest --html=reports/html/report.html
```

---

## Trace Viewer

Ver [`docs/trace-viewer.md`](docs/trace-viewer.md) para la guía completa.

```bash
# Grabar un trace durante la ejecución de las pruebas
playwright show-trace reports/traces/trace.zip
```

---

## Debug Mode

Ver [`docs/debug.md`](docs/debug.md) para la guía completa.

```bash
# Ejecutar pruebas en modo debug con Playwright Inspector
PWDEBUG=1 pytest tests/e2e/ --headed

# Ejecutar pruebas con un retraso entre acciones para observar el comportamiento
pytest --slowmo 500
```

---

## Codegen

Ver [`docs/codegen.md`](docs/codegen.md) para la guía completa.

```bash
# Generar código para una URL específica
playwright codegen $BASE_URL

# Generar código usando un contexto de navegador con sesión autenticada
playwright codegen --load-storage=auth.json $BASE_URL
```
