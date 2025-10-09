// Simple service worker for caching static assets
const CACHE_NAME = 'aether-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/src/css/style.css',
    '/src/css/responsive.css',
    '/src/js/script.js',
    '/public/assets/logo/logo.png',
    '/public/assets/logo/Aether.png',
    '/public/assets/fonts/MonaSansExpanded-Regular.woff2',
    '/public/favicon.ico'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            }
        )
    );
});