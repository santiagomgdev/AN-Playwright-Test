# Instalación

## Requisitos previos

Verificar la instalación de las siguientes herramientas:

```bash
python --version    # Must be 3.10 or higher
pip --version       # Must be present
git --version       # Must be present
```

## Entorno virtual

Para isolar las dependencias del proyecto:

```bash
python -m venv venv

# Para activar el entorno virtual:

# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

## Instalación de dependencias

Instalar las dependencias necesarias para el proyecto:

```bash
pip install -r requirements.txt
```

## Instalación de Navegadores

```bash
# Solo funciona para SO ubuntu, fedora solo puede usar chromium y firefox
playwright install
```

## Configuración de variables de entorno

```bash
cp .env.example .env
# Posterior al comando, se requiere editar el archivo .env con las credenciales y configuraciones necesarias.
```
