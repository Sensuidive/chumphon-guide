// offline copy of the guide; a new build changes VER so phones fetch the update
const VER = 'cg-5436497cf1', FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-180.png", "img/hero.jpg", "img/logo.png", "img/padi.png", "img/shop_map.png", "img/site_hin_chedi_en.jpg", "img/site_hin_chedi_th.jpg", "img/site_hin_lak_ngam_en.jpg", "img/site_hin_lak_ngam_th.jpg", "img/site_hin_pae_en.jpg", "img/site_hin_pae_th.jpg", "img/site_ngam_noi_en.jpg", "img/site_ngam_noi_th.jpg", "img/site_ngam_yai_top_en.jpg", "img/site_ngam_yai_top_th.jpg", "img/site_ngam_yai_wall_en.jpg", "img/site_ngam_yai_wall_th.jpg", "img/site_prab_site_en.jpg", "img/site_prab_site_th.jpg", "img/site_sam_laem_en.jpg", "img/site_sam_laem_th.jpg", "img/site_suntud_en.jpg", "img/site_suntud_th.jpg", "img/squad.jpg", "img/turtle_ST-001.jpg", "img/where_en.jpg", "img/where_th.jpg"];
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(VER).then(c => c.addAll(FILES))); });
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VER).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const u = new URL(e.request.url), mine = u.origin === location.origin, font = /fonts\.(googleapis|gstatic)\.com$/.test(u.hostname);
  if (!mine && !font) return;
  // pages: network first so updates show, cache when offline; images and fonts: cache first
  if (e.request.mode === 'navigate') { const app = u.pathname.endsWith('/') && !/\/(en|th)\//.test(u.pathname), key = app ? 'index.html' : e.request;
    e.respondWith(fetch(e.request).then(r => { const c2 = r.clone(); caches.open(VER).then(c => c.put(key, c2)); return r; }).catch(() => caches.match(key).then(h => h || caches.match('index.html')))); return; }
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request).then(r => { if (r.ok || r.type === 'opaque') { const c2 = r.clone(); caches.open(VER).then(c => c.put(e.request, c2)); } return r; })));
});
