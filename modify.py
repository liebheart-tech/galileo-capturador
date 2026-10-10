from pathlib import Path
p=Path(__file__).parent
html=(p/'index.html').read_text()
html=html.replace('v2.0 · Raven Final','v2.1 · Raven Refined')
import re
# Replace both switches with clear segmented controls, retain ids for mode display
for prefix in ('camera-','main-'):
    pattern=r'<label class="mode">.*?</label>'
    replacement=f'''<div class="mode-picker" role="group" aria-label="Tipo de lectura"><div class="mode-picker-heading">Tipo de lectura</div><div class="mode-options"><button type="button" id="{prefix}mode-trekkfit" class="mode-option" aria-pressed="true">🛡 Trekkfit</button><button type="button" id="{prefix}mode-universal" class="mode-option" aria-pressed="false">▥ Universal</button></div><div class="mode-explanation" id="{prefix}mode-description">Solo guarda automáticamente SKU Trekkfit válidos.</div></div>'''
    html,n=re.subn(pattern,replacement,html,count=1)
    assert n==1,(prefix,'switch not found')
# Settings block
html=html.replace('<button id="sound-toggle" class="secondary">🔊 Sonido: sí</button> <button id="backup" class="secondary">Respaldo JSON</button><button id="recover-backup" class="secondary" type="button">Recuperar copia anterior</button><input id="restore" type="file" accept="application/json" aria-label="Restaurar respaldo JSON" style="font-size:14px;margin-top:10px">', '''<button id="sound-toggle" class="secondary" type="button">🔊 Sonido: sí</button><details class="advanced"><summary>⚙️ Ajustes y recuperación</summary><p class="note">Estos controles son para proteger o recuperar tu inventario. No necesitás utilizarlos para escanear.</p><div class="advanced-actions"><button id="backup" class="secondary" type="button">Descargar respaldo JSON</button><p class="note">Guarda una copia completa de tu conteo actual para restaurarlo más adelante.</p><button id="recover-backup" class="secondary" type="button">Recuperar estado anterior</button><p class="note">Intenta restaurar el estado local anterior al último cambio. No es un historial de días anteriores.</p><label for="restore" class="note">Restaurar desde un archivo JSON</label><input id="restore" type="file" accept=".json,application/json" aria-label="Restaurar respaldo JSON"></div></details>''')
# clear style and add deliberate scoped rules at end
css='''
/* Galileo 2.1 — visual de cámara, sin reglas contradictorias */
#camera-box{padding:max(10px,env(safe-area-inset-top)) 10px max(10px,env(safe-area-inset-bottom))}
#camera-panel{width:min(100%,560px);max-height:calc(100dvh - 20px);overflow:auto;padding:14px}
#camera-reader{position:relative;width:100%;height:clamp(128px,22dvh,170px)!important;min-height:0!important;max-height:none!important;overflow:hidden;border-radius:12px;background:#070e1b}
#camera-reader video{width:100%!important;height:100%!important;min-height:0!important;max-height:none!important;object-fit:cover!important;object-position:center!important}
#camera-reader>div{width:100%!important;max-width:100%!important}
#camera-reader #qr-shaded-region{display:none!important}
#camera-panel .row{gap:8px}
#camera-panel #camera-zoom-row{margin-top:8px}
#camera-panel #camera-zoom{width:min(44%,180px);accent-color:#5796ff}
#camera-review[hidden],#manual-review[hidden]{display:none!important}
.mode-picker{background:#102039;border:1px solid #344c6c;border-radius:14px;padding:12px;margin:12px 0}
.mode-picker-heading{font-size:13px;font-weight:700;color:#c6d5ea;margin-bottom:9px}
.mode-options{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.mode-option{min-height:44px;background:#223550;color:#bac9df;border:1px solid #405475;border-radius:10px;font-size:14px;padding:10px 6px}
.mode-option[aria-pressed="true"]{background:#3869d6;color:#fff;border-color:#85a8ff;box-shadow:inset 0 0 0 1px #91b1ff}
.mode-explanation{font-size:12px;color:#b5c2d7;line-height:1.5;margin-top:9px}
.advanced{background:#142238;border:1px solid #344c6c;border-radius:14px;padding:14px;margin:14px 0}
.advanced summary{cursor:pointer;font-weight:700;list-style-position:inside}
.advanced-actions{padding-top:10px;display:grid;gap:7px}
.advanced-actions button{width:100%}
.advanced-actions p{margin:0 0 8px}
.advanced-actions input[type=file]{font-size:13px;padding:10px;width:100%;min-width:0}
#camera-repeat{min-height:46px}
@media(max-width:420px){#camera-panel{padding:10px}#camera-reader{height:clamp(120px,19dvh,148px)!important}#camera-panel .note{font-size:12px}#camera-review .row{flex-wrap:wrap}#camera-review .row button{flex:1 1 135px}}
'''
html=html.replace('</style></head>','\n'+css+'</style></head>')
(p/'index.html').write_text(html)
js=(p/'app.js').read_text()
old="function settings(){for(const prefix of ['','main-']){const id=prefix?'main-strict':'camera-strict';$(id).checked=strict;$(prefix+'mode-title').textContent=strict?'Modo Trekkfit':'Modo universal';$(prefix+'mode-description').textContent=strict?'Solo acepta automáticamente SKU válidos.':'Permite registrar códigos de otros formatos.'}for(const id of ['sound-toggle','camera-sound'])$(id).textContent=sound?'🔊 Sonido: sí':'🔇 Sonido: no'}\nfor(const id of ['camera-strict','main-strict'])$(id).onchange=e=>{strict=e.target.checked;try{localStorage.setItem('galileo-strict-v17',String(strict))}catch(err){status('No se pudo guardar la preferencia',true)}settings()};"
new="""function settings(){for(const prefix of ['camera-','main-']){const t=$(prefix+'mode-trekkfit'),u=$(prefix+'mode-universal');t.setAttribute('aria-pressed',String(strict));u.setAttribute('aria-pressed',String(!strict));$(prefix+'mode-description').textContent=strict?'Modo Trekkfit activo: solo guarda automáticamente SKU válidos; otros requieren aprobación.':'Modo universal activo: permite guardar códigos de distintos formatos.'}for(const id of ['sound-toggle','camera-sound'])$(id).textContent=sound?'🔊 Sonido: sí':'🔇 Sonido: no'}
for(const prefix of ['camera-','main-'])for(const [suffix,enabled] of [['mode-trekkfit',true],['mode-universal',false]])$(prefix+suffix).onclick=()=>{strict=enabled;try{localStorage.setItem('galileo-strict-v17',String(strict))}catch(err){status('No se pudo guardar la preferencia',true)}settings()};"""
assert old in js
js=js.replace(old,new)
# zoom set after camera starts. apply actual zoom and report supported setting
old="z.min=caps.zoom.min;z.max=caps.zoom.max;z.step=caps.zoom.step||.1;z.value=caps.zoom.min;z.disabled=false;$('camera-zoom-label').textContent=z.value+'×'"
new="""z.min=caps.zoom.min;z.max=caps.zoom.max;z.step=caps.zoom.step||.1;const min=Number(caps.zoom.min),max=Number(caps.zoom.max);const requested=Math.min(max,Math.max(min,1.7));z.value=String(requested);z.disabled=false;try{await reader.applyVideoConstraints({advanced:[{zoom:requested}]});const applied=reader.getRunningTrackSettings?.()?.zoom;$('camera-zoom-label').textContent=(typeof applied==='number'?applied:requested).toFixed(1)+'×'}catch(e){$('camera-zoom-label').textContent='Zoom manual disponible';$('camera-hint').textContent='No se pudo aplicar zoom inicial; ajustalo manualmente.'}"""
assert old in js
js=js.replace(old,new)
# when camera opens, audio doesn't need to block start
js=js.replace('if(sounds.loading)await sounds.loading;if(token!==serial)return;', 'if(token!==serial)return;')
# fix zoom UI always correct if unsupported
js=js.replace("else $('camera-zoom-label').textContent='No disponible';", "else {z.disabled=true;$('camera-zoom-label').textContent='No disponible';}")
# keep pending camera manual approval even when closed? current stopCamera hides review, correct.
(p/'app.js').write_text(js)
sw=(p/'sw.js').read_text().replace('galileo-capturador-v2-20261010-r1','galileo-capturador-v2-1-20261010-r1')
(p/'sw.js').write_text(sw)
