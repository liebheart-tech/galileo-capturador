const CACHE='galileo-capturador-v2-2-20261010-r1';
const ASSETS=['./','./index.html','./app.js','./core.js','./vendor/html5-qrcode.min.js','./manifest.webmanifest','./icon-192.png','./icon-512.png','./beep-ok.mp3','./raven-alert.wav'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS))));
// Waiting worker activates only after old pages close: no mixed versions during a count.
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('galileo-capturador-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const url=new URL(e.request.url);if(e.request.method!=='GET'||url.origin!==self.location.origin||!url.href.startsWith(self.registration.scope))return;e.respondWith(caches.open(CACHE).then(async c=>{const hit=await c.match(e.request,{ignoreSearch:true});if(hit)return hit;try{return await fetch(e.request)}catch(err){if(e.request.mode==='navigate')return c.match('./index.html');throw err}}))});
