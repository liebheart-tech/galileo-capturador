# Galileo V2.0 — Raven Final

Versión revisada del ZIP V1.7, sin alterar el proyecto Apps Script de la carpeta superior.

## Publicación y actualización
1. Exportar CSV y respaldo JSON en la versión anterior.
2. Reemplazar los archivos del sitio por el contenido de esta carpeta, conservando la misma URL, origen y ruta de GitHub Pages. Incluir `vendor/`, `app.js`, `core.js`, los audios y `sw.js`.
3. Cerrar todas las pestañas e instancias de la PWA y volver a abrir. La versión nueva del service worker espera el cierre de las páginas antiguas para no mezclar versiones durante un conteo. Una visita puede todavía mostrar la versión anterior mientras se instala la nueva; cerrar y abrir nuevamente. Confirmar v2.0 en el encabezado.
4. Abrir con conexión, permitir completar la instalación y probar en modo avión antes de una jornada offline.

Se mantiene la clave `galileo-capturador-v1`, el inventario original y la preferencia estricta V1.7. No borrar los datos del navegador para actualizar: eso elimina el inventario. Los datos pertenecen al origen; cambiar dominio o perfil exige exportar/importar JSON. No hay sincronización remota.

## Uso
- Cámara: dos decodificaciones coincidentes dentro de 1.2 segundos habilitan la lectura; cada código queda bloqueado durante la sesión hasta tocar **Otra caja igual**. Para contar otra caja con ese SKU, colocar la nueva caja y tocar el botón. No se interpreta una falla de decodificación como prueba de haber retirado una caja.
- Pistola Bluetooth: tocar el campo; Enter/Tab o 700 ms sin entrada registra la lectura. Cada escaneo repetido se conserva. Se requiere que el lector envíe teclas al campo de captura. No interceptamos controles ni forzamos el foco continuamente.
- Modo Trekkfit: patrón heredado `E` + 5 dígitos + guion + letra + guion + 2–4 dígitos. Fuera del patrón se exige aceptación o descarte tanto en cámara como en pistola. El patrón no valida existencia del producto en un catálogo.
- Universal: conserva caracteres, mayúsculas/minúsculas y ceros; limita a 512 caracteres y rechaza controles. No prueba que el código corresponda a un producto real.
- Sonido: una sola ruta después de persistir. El botón controla ambas entradas y se recuerda. AudioContext se reanuda durante interacción real; recursos precargados y decodificados localmente. Si el navegador bloquea audio, el contador y el mensaje siguen siendo la evidencia de guardado.
- Recuperación: respaldo JSON completo, importar JSON, o recuperar la copia anterior local. La copia anterior es una generación, cambia en cada mutación. Si JSON almacenado es corrupto, se bloquean nuevas escrituras hasta recuperación y se permite descargar el original. Nunca eliminarlo silenciosamente.
- Deshacer elimina solo el último registro persistido, sin rearmar la cámara para ese mismo código.

## CSV y Google Sheets
CSV UTF-8 con BOM, CRLF, comillas escapadas y una columna SKU. Importar en Sheets **desactivando «Convertir texto en números, fechas y fórmulas»**. Al pegar códigos, preformatear la columna como texto sin formato. CSV no tiene tipos: las comillas no garantizan conservar ceros en todos los importadores. Tampoco abrir CSV de códigos universales sin controlar la evaluación de fórmulas (`=`, `+`, `-`, `@`). JSON es el respaldo exacto y no ejecuta fórmulas. No se fabrican fórmulas `="..."` para forzar texto.

## Verificación
- `node --test tests/core.test.cjs`
- Servir por HTTP localhost: `python3 -m http.server 8765` dentro de esta carpeta.
- Con Playwright y sus navegadores: `node tests/browser.cjs` y `node tests/audio.cjs`. El script de navegador usa Chrome instalado en la ruta macOS indicada; adaptar esa ruta en otro sistema. Los recursos de producción no requieren Node, Python, Playwright ni internet externo.
- Resultados ejecutados están en `tests/*-results.txt`. Auditoría en `AUDITORIA.md`.

## Prueba física pendiente, antes de uso operativo
No se dispone de iPhone ni pistola física. Probar Safari y PWA instalada: permisos aceptados/denegados, bip automático Trekkfit/universal/manual tras apertura y tras volver del fondo, silencio, graznido único, 20 cajas iguales usando Otra caja igual, caja inmóvil 30 s, alternancia de SKU, selección de cámara, zoom y luz si existen, cierre mientras se pide permiso, rotación, pantalla pequeña y modo avión. Comparar conteo/historial/CSV/JSON antes y después de recargar. Verificar captura Bluetooth con Enter y con sufijo Tab. La audibilidad, calidad de reconocimiento y latencia real no se declaran certificadas por pruebas sin hardware.

Audio de cuervo y atribución: AUDIO_LICENSE.md. Biblioteca y licencia: vendor/. No se ha publicado el sitio ni reemplazado el despliegue existente.
