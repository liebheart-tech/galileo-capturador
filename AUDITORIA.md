# Auditoría V1.7 → V2.0

Inspeccionados los siete archivos originales: index.html (UI/lógica), sw.js, manifest.webmanifest, dos iconos PNG, beep-ok.mp3, raven-alert.wav. La solicitud pegada acaba literalmente en «Si no dispones de un iPhone físico,»; no se inventaron requisitos posteriores. Recursos PNG verificados por formato y dimensiones; MP3 original preservado byte a byte; WAV sustituido con procedencia documentada.

## Hallazgos demostrados y corrección

| Gravedad | Evidencia V1.7 | Cambio V2.0 |
|---|---|---|
| CRÍTICO | register hace rows.push antes de persist y renderiza aun si falla; Deshacer principal y Limpiar ignoran resultado | Escritura antes de publicar estado. Fallas dejan conteo e historial intactos |
| ALTO | JSON inválido se captura sin mensaje; elementos no string se filtran silenciosamente | Bloquear mutaciones ante corrupción, conservar original, exportación y restauración |
| ALTO | register manual/pistola no verifica camera-strict | Validación común para ambas entradas, aceptación explícita |
| ALTO | Dos pestañas pueden sobrescribir inventarios sin detectar cambios | Comprobación de snapshot y aviso storage. No equivale a transacción distribuida: evitar conteo simultáneo en varias pestañas |
| ALTO | onMiss rearma tras 2600 ms sin decodificar aunque una caja siga delante | Bloqueo por sesión y rearme explícito; doble consenso de lectura |
| ALTO | stop durante start no espera la adquisición; nuevo inicio puede competir con cierre viejo | Máquina de estados, token de sesión, esperar inicio antes de liberar y reabrir |
| ALTO | Motor se descarga de CDN, ausente de ASSETS | Biblioteca fija local incluida en precache, sin dependencia externa durante captura |
| MEDIO | unlockAudio prepara AudioContext, pero bip real usa otro Audio HTML no desbloqueado; fallback sintetiza sonido | Ambos sonidos usan buffers del mismo AudioContext reanudado por gesto. Sin fallback sintetizado |
| MEDIO | cameraSound solo silencia en cámara; audio original de cuervo sin procedencia en ZIP | Preferencia global persistida; grabación real licenciada y trazable |
| MEDIO | uppercase y eliminar espacios altera códigos universales de entrada manual | Conservar texto original salvo espacios externos; rechazar controles |
| MEDIO | CSV citado no impide conversión de números ni evaluación de fórmulas en Sheets | Exportación literal exacta y requisito explícito de importar como texto; respaldo JSON |
| MEDIO | SW elimina todos los caches del origen y usa caches.match global | Solo borrar caches Galileo; buscar en caché de versión activa; actualización espera cierre de clientes |
| MEDIO | Input global intercepta Tab/Enter en otros controles; recover cada 450 ms roba foco | Captura en campo dedicado, navegación de teclado preservada; cámara excluye pistola |
| BAJO | Variables cámara sin uso, oldCrowSound, warningSound con código inalcanzable, estilos redundantes | Reescritura modular y eliminación del motor legado |
| BAJO | Texto pide retirar 1 s; código usa 2.6 s; selector de cámara ausente | Instrucción explícita de repetición y selector tras permiso |

## Pitido: límite de la atribución causal
El original llama a playAccepted tanto desde lectura automática como confirmación manual. No existe una rama que elimine el bip únicamente para SKU Trekkfit. Sí está demostrado que el desbloqueo actúa sobre un objeto de audio diferente; la confirmación manual tiene un gesto de usuario y el callback automático no. Es una explicación técnica coherente con el síntoma de Safari, pero la causa exacta en el dispositivo reportado no fue reproducida. También pueden intervenir preferencias, estado del navegador o carga. V2 unifica los caminos y valida decodificación de ambos archivos; no afirma una reproducción física que no se ejecutó.

## Motor
Se mantiene html5-qrcode **2.3.8**, distribuido localmente con Apache-2.0. El bundle contiene decodificadores ZXing y los identificadores CODE_128, CODE_39, CODE_93, EAN_13, EAN_8, UPC_A, UPC_E e ITF. Configuración limitada a esos formatos, 15 fps y dos resultados coincidentes en 1.2 s. BarcodeDetector experimental se deshabilita para usar el camino consistente del bundle. Añadir otra biblioteca ZXing no demuestra una mejora y aumenta complejidad sin benchmark físico. Limitaciones: consenso no garantiza autenticidad, Code39 no siempre aporta checksum, una etiqueta mal impresa puede no decodificar y una etiqueta distinta con el mismo SKU requiere rearme explícito. No hay medición física que permita prometer menor latencia. Fuente técnica: https://scanapp.org/html5-qrcode-docs/docs/intro y bundle local.

## Seguridad y persistencia
Renderizado con textContent; no insertar códigos con innerHTML. Sin transmisión de inventario ni llamadas a CDN durante uso. No se cifra almacenamiento local; cualquier script del mismo origen o persona con acceso al perfil puede leerlo. Escritura transaccional en memoria respecto a setItem exitoso; copia de una generación antes de mutaciones. localStorage tiene cuotas y no es almacenamiento invulnerable al borrado del navegador. Snapshot evita sobreescrituras secuenciales entre pestañas, pero localStorage no ofrece compare-and-swap atómico entre procesos: operar una sesión a la vez. JSON exportado sigue siendo el respaldo durable. No se cambia clave ni se borran inventarios al instalar el SW.

## Resultado de pruebas y límites
12 pruebas Node aprobadas. Flujos de interfaz aprobados en Chrome instalado y WebKit 26.5 con cámara y AudioContext simulados: SKU válido/inválido, universal, aceptación/descarte, sonido activado/desactivado, deshacer, recarga, duplicados, repetición explícita, permiso denegado y cierre durante inicio. Chrome aprobó recarga offline real con motor local. WebKit tuvo error interno de navegación offline en el motor automatizado; offline WebKit no verificado. Ambos motores decodifican los MP3/WAV reales mediante Web Audio (ver resultados). No se verificó reconocimiento óptico con cámara física ni sonido audible en iPhone. La revisión a 390×844 px muestra controles contenidos en panel desplazable; pantallas menores y teclado/rotación requieren prueba física.

Service worker: lista de recursos comprobada por prueba y navegación offline real en Chrome. Actualización entre despliegues V1.7/V2 no ejecutada sobre el dominio publicado. No se certifica producción en hardware hasta completar la lista física de README.
