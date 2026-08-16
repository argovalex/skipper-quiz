// PWA service worker — caches the app shell so it installs and opens offline.
// Content, config and videos are always fetched live (network), never cached here.
const SHELL = 'skipper-shell-v1';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icon.svg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== SHELL).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;                    // never cache POST (checkout, progress)
  const url = new URL(req.url);
  // Only serve the app shell from cache; everything else (API, videos, fonts) goes to network.
  const isShell = url.origin === location.origin && !url.pathname.startsWith('/api');
  if (!isShell) return;
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(SHELL).then(c => c.put(req, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
