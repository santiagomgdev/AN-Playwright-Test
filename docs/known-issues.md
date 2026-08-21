# Known Issues — Proceso de Vinculación

Hallazgos de la exploración en vivo contra los ambientes `dev.local` y
`testing.local` durante la construcción de la suite E2E de vinculaciones.
Cuando el comportamiento difiere entre ambientes se indica explícitamente.
Relevantes tanto para quien mantenga estas pruebas como para reportar al
equipo de backend/frontend.

## 1. Inconsistencia de segmento de plan en la URL

El segmento `:plan` de la ruta cambia de nombre a mitad del flujo sin razón
aparente:

- `registro-datos`, `evaluar-cupo`, `gestionar-pagaduria` → `basico` / `complementario`
- `validar-identidad` en adelante → `plan-basico` / `plan-complementario`

Los Page Objects y pruebas en esta suite ya asumen este cambio (ver
`PLAN_SEGMENTO_ETAPAS_TARDIAS` en los tests de HU tardías), pero es
probablemente un bug de ruteo que vale la pena reportar al equipo de frontend.

## 2. `verificacion-requisitos` tiene un guard más estricto que las demás etapas

Todas las etapas posteriores a validar-identidad (`cargue-documentos`,
`revision-sarlaft`, `decision-final`, `firma-electronica`) renderizan su
pantalla vía navegación directa por URL **sin importar la etapa real del
backend** — solo la confirmación/submit final es rechazada por el backend.

`verificacion-requisitos` es la excepción: navegar directo a esa ruta
redirige silenciosamente a `/autenticacion-autorizacion/usuarios`, incluso
para un asociado que sí debería poder verla. Cubierto por
`test_hu11_vinculacion_verificacion_requisitos_guard.py` como prueba de
regresión — si esto cambia, la prueba fallará y habrá que confirmar con el
equipo si el cambio fue intencional.

## 3. Validación de identidad (OTP): bypass fijo en testing.local, NO en dev.local

**Corrección respecto a una versión anterior de este documento**: sí existe
un código fijo de ambiente de pruebas, pero solo en `testing.local`.

- En **testing.local**, `"000000"` es aceptado como código válido tanto para
  el paso de email como para el de celular — confirmado en vivo (2026-08-21):
  ambos pasos quedan verificados y aparece el botón "Confirmar" para avanzar
  la etapa real. `uc_validar_identidad_completa` (en `uc_vinculacion.py`) usa
  este código para progresar el backend de verdad, no solo la UI.
- En **dev.local**, ese mismo código (`"000000"`, junto con `"123456"` y
  `"111111"`) fue rechazado durante una exploración anterior con validación
  real por email/SMS. No asumir que el bypass de testing.local aplica ahí.
- `ValidarIdentidadPage.boton_generar_codigo`/`input_codigo_otp` usan
  `.first`: una vez que un paso queda confirmado, su botón/input desaparece
  del DOM, por lo que `.first` siempre apunta al paso todavía activo sin
  necesidad de distinguir email/celular explícitamente.
- Para probar el camino de **código incorrecto**, usar un código distinto al
  fijo (esta suite usa `"111111"` en testing.local) — cubierto por
  `test_hu05_vinculacion_otp_codigo_incorrecto.py` y
  `test_hu06_vinculacion_otp_bloqueo_por_intentos.py`. El mensaje de error
  real incluye un contador de intentos (`"intento N de 5"`).
- **El umbral de bloqueo no depende solo del aspirante individual.** Tras uso
  intensivo del ambiente (dev.local) durante una misma sesión de pruebas, se
  observó que un aspirante *nuevo* (identificación, celular y email únicos)
  recibía bloqueo inmediato ("Código incorrecto, bloqueo por seguridad,
  estado cambia a negada") en el primer intento, en vez del contador
  incremental esperado. Esto sugiere un límite adicional a nivel de
  sesión/IP/navegador compartido en el backend de validación de identidad.
  `test_hu06_...` no asume una secuencia fija de mensajes por esta razón.
- **El backend exige progresión real de etapa** cuando no se usa el bypass:
  confirmado con un 409 al intentar confirmar decisión-final sobre un
  asociado cuya etapa real seguía en 4 (validar-identidad): `"El asociado no
  se encuentra en etapa de decisión final (etapa 13). Etapa actual: 4"`.

### Mitigaciones disponibles

1. **testing.local + código fijo `"000000"` (recomendado)**: avanza la etapa
   real del backend, no solo la UI. Es la base para construir cobertura
   real de `consultar-listas`, `formulario-vinculacion`,
   `cargue-documentos`, `verificacion-requisitos`, `revision-sarlaft` y
   `decision-final`.
2. **Mock de red (solo UI, no backend, para dev.local u otros ambientes sin
   bypass)**: `fixtures/otp_mock.py` (fixture `otp_bypass_mock`) intercepta
   las llamadas de `validacion-identidad` para forzar que el SPA se
   comporte como si el OTP estuviera validado. Permite probar la **UI y
   validaciones de formulario** de etapas posteriores (usado indirectamente
   vía navegación directa por URL en las HU 07–10), pero no avanza la etapa
   real del backend — cualquier submit final real (aprobar/negar/desistir,
   o completar cargue-documentos/verificacion-requisitos/revision-sarlaft
   end-to-end) seguirá bloqueado en ese caso.

**Verificado en vivo en testing.local (2026-08-21)** con la opción 1: un
mismo asociado avanzó realmente de validar-identidad → consultar-listas
(banner "Identidad validada: La identidad del asociado fue verificada
correctamente") y luego completó consultar-listas ("Consulta confirmada: La
información de consulta de listas fue guardada exitosamente"), reflejado en
el listado de `/vinculaciones` con la etapa real del backend actualizada.
De paso se encontraron y corrigieron dos bugs de locators en
`consultar_listas_page.py`: los radios "Coincidencia"/"No" hacían match por
substring con "No coincidencia"/"No encontrado" (faltaba `exact=True`).
