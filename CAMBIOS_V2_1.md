# Galileo V2.1 — Raven Refined

Actualización sobre V2.0 con la misma clave de inventario local.

## Cambios
- Visor compacto panorámico: video `object-fit: cover` en una ventana baja, sin deformar la imagen. El motor sigue recibiendo el video completo.
- Zoom inicial solicitado de 1.7× si la pista de cámara admite zoom, ajustado a los límites del dispositivo. Si falla, el usuario puede intentarlo manualmente.
- Selector Trekkfit / Universal explícito en la página principal y en la cámara. Ambos se sincronizan y guardan la preferencia existente.
- Respaldo JSON, recuperación local e importación JSON ocultos en «Ajustes y recuperación», con explicaciones. No se eliminaron.
- El inicio de cámara ya no espera la carga del audio.
- Caché del service worker actualizado para evitar recursos viejos.

## Publicación
Exportar primero CSV y respaldo JSON del conteo actual. Copiar archivos de la raíz del paquete a la raíz del repositorio, manteniendo la carpeta `vendor/`. Cerrar y reabrir todas las pestañas para que el service worker nuevo se active.

## Límites
Las pruebas de lógica se ejecutaron con Node.js. No se ejecutaron pruebas físicas de cámara ni sonido en Safari iOS. El zoom 1.7× depende de las capacidades reales de la cámara y de Safari. La confirmación de dos lecturas sigue activa y el mismo SKU requiere habilitar «Otra caja igual» para evitar duplicados.
