/* Pure inventory and reader logic; shared by browser and executed tests. */
(function(root){'use strict';
const KEY='galileo-capturador-v1', BACKUP=KEY+'-recovery';
const pattern=/^E\d{5}-[A-Z]-\d{2,4}$/i;
function validate(rows){if(!Array.isArray(rows)||rows.some(x=>typeof x!=='string'))throw Error('Inventario inválido; se conserva el original.');return rows.slice()}
class Inventory{
 constructor(storage){this.storage=storage;this.rows=[];this.raw=null;this.blocked=false;this.error='';try{this.raw=storage.getItem(KEY);this.rows=validate(JSON.parse(this.raw||'[]'))}catch(e){this.blocked=true;this.error=e.message}}
 commit(next){if(this.blocked)throw Error('Recuperá el inventario antes de guardar.');if(this.storage.getItem(KEY)!==this.raw)throw Error('El inventario cambió en otra pestaña. Recargá antes de continuar.');if(this.raw!==null)this.storage.setItem(BACKUP,this.raw);const value=JSON.stringify(validate(next));this.storage.setItem(KEY,value);this.raw=value;this.rows=next.slice();return true}
 add(code){return this.commit([...this.rows,code])} undo(){if(!this.rows.length)return false;return this.commit(this.rows.slice(0,-1))} clear(){return this.commit([])}
 restore(rows){const next=validate(rows);const original=this.storage.getItem(KEY);if(original!==null)this.storage.setItem(BACKUP,original);const value=JSON.stringify(next);this.storage.setItem(KEY,value);this.rows=next;this.raw=value;this.blocked=false;this.error=''}
}
function code(raw){const s=String(raw).trim();if(!s||s.length>512||/[\x00-\x1f\x7f]/.test(s))throw Error('Código vacío, demasiado largo o con caracteres de control.');return s}
function suspicious(s,strict){return strict&&!pattern.test(s)}
function csv(rows){return '\ufeffSKU\r\n'+rows.map(x=>'"'+x.replace(/"/g,'""')+'"').join('\r\n')+'\r\n'}
class Gate{
 constructor(){this.state='idle';this.seen=new Set();this.candidate='';this.hits=0;this.at=0}
 transition(next){const allowed={idle:['starting'],starting:['running','stopping','idle'],running:['stopping'],stopping:['idle']};if(!allowed[this.state].includes(next))throw Error('Transición inválida '+this.state+' → '+next);this.state=next}
 observe(s,now){if(this.state!=='running'||this.seen.has(s))return false;if(this.candidate!==s||now-this.at>1200){this.candidate=s;this.hits=1}else this.hits++;this.at=now;return this.hits>=2}
 lock(s){this.seen.add(s);this.candidate='';this.hits=0} rearm(){this.seen.clear();this.candidate='';this.hits=0}
}
const api={KEY,BACKUP,pattern,Inventory,code,suspicious,csv,Gate};if(typeof module!=='undefined')module.exports=api;else root.Galileo=api;
})(typeof globalThis!=='undefined'?globalThis:this);
