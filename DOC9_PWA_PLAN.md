# DOC9 — PWA Implementation Plan

## Obiettivo

Rendere le 3 versioni CDN di Noesis v816 installabili come Progressive Web App:

| Versione | File |
|----------|------|
| COMPLETE | `noesis816.html` |
| Reader | `noesis816-reader.html` |
| Editor | `noesis816-editor.html` |

## Approccio scelto: Opzione A — File separati

File esterni condivisi (service worker, icone) + manifest dedicati per ogni app.
Più robusto del SW inline via Blob, pieno supporto browser.

---

## Fase 1 — Icone

Creare 2 PNG quadrati:

| File | Dimensione | Note |
|------|:---:|------|
| `icon-192.png` | 192×192 | Android/Chrome minimo |
| `icon-512.png` | 512×512 | Splash screen + desktop |

Generare da un SVG semplice con sfondo viola (`#7c3aed`) e l'emoji 📚 centrata, poi rasterizzare a 192px e 512px.

---

## Fase 2 — Manifest (3 file)

Template identico, differiscono solo `name`, `short_name`, `start_url`.

### `manifest-complete.json`

```json
{
  "name": "Noesis COMPLETE",
  "short_name": "Noesis",
  "description": "EPUB reader + editor — read, annotate, extract, write",
  "start_url": "/noesis816.html",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#0f0f18",
  "theme_color": "#7c3aed",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### `manifest-reader.json`

Stesso JSON con:
- `"name": "Noesis Reader"`
- `"short_name": "Reader"`
- `"start_url": "/noesis816-reader.html"`
- `"description": "EPUB reader — read and annotate in any language"`

### `manifest-editor.json`

Stesso JSON con:
- `"name": "Noesis Editor"`
- `"short_name": "Editor"`
- `"start_url": "/noesis816-editor.html"`
- `"description": "WYSIWYG editor — write, format, export documents"`

---

## Fase 3 — Service Worker (`sw.js`)

Unico file condiviso. Strategia: **cache-first** per dipendenze CDN jsDelivr.

```javascript
const CACHE = 'noesis-v1';
const CDN_URLS = [
  'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js',
  'https://cdn.jsdelivr.net/npm/epubjs@0.3.93/dist/epub.min.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(CDN_URLS))
  );
});

self.addEventListener('fetch', e => {
  const url = e.request.url;
  // Cache-first per CDN jsDelivr
  if (CDN_URLS.some(cdn => url.startsWith(cdn.split('@')[0]))) {
    e.respondWith(
      caches.match(e.request).then(r => r || fetch(e.request))
    );
  }
  // Tutto il resto: network-only (IndexedDB locale non ha bisogno di cache)
});
```

---

## Fase 4 — Tag HTML nei 3 file CDN

### Nel `<head>` (dopo il `<title>`)

```html
<!-- PWA Manifest -->
<link rel="manifest" href="/manifest-XXX.json">
<meta name="theme-color" content="#7c3aed">

<!-- Apple iOS -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Noesis XXX">
<link rel="apple-touch-icon" href="/icon-192.png">
```

Dove `XXX`:
- COMPLETE → `complete`, `COMPLETE`
- Reader → `reader`, `Reader`
- Editor → `editor`, `Editor`

### Prima di `</body>`

```html
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js');
  });
}
</script>
```

---

## Fase 5 — Persistent Storage (da valutare)

IndexedDB (`EpubLibraryDB`, `noesisDB`) in una tab browser normale è in modalità
*"best-effort"*: il browser può cancellare i dati in caso di spazio disco insufficiente.

Con la PWA installata, possiamo richiedere lo **storage persistente**:

```javascript
// Da chiamare dopo l'installazione o al primo avvio
if (navigator.storage && navigator.storage.persist) {
  const persisted = await navigator.storage.persist();
  if (persisted) {
    console.log('Storage persistente concesso — dati IndexedDB protetti');
  }
}
```

Se concesso, il browser **garantisce** di non cancellare automaticamente
i dati IndexedDB. Su Chrome, le PWA installate ottengono questa autorizzazione
automaticamente senza prompt all'utente.

### Priorità differita

- **Impatto**: basso (1 chiamata API, ~5 righe)
- **Rischio**: nullo — se non supportata, semplicemente non fa nulla
- **Da fare dopo**: aver verificato che il Service Worker e i manifest funzionano

> ⚠️ **Da valutare in un secondo momento** — non bloccante per il rollout PWA iniziale.

---

## Fase 6 — Test

| Test | Strumento |
|------|-----------|
| Manifest valido | Chrome DevTools → Application → Manifest |
| SW registrato | DevTools → Application → Service Workers |
| `beforeinstallprompt` | Chrome Android: visita, attendi 30s, interagisci |
| Installazione desktop | Chrome → ⋮ → "Installa Noesis..." |
| iOS "Aggiungi a Home" | Safari → Share → Aggiungi a Home |
| Offline (CDN cache) | Installa, poi airplane mode → reload |

---

## Fase 7 — Sezione "Install as App" in index.html

Aggiungere nella pagina download una breve sezione:

> 📱 **Install as App** — Apri `noesis816.html` in Chrome. Dal menu (⋮) seleziona *"Installa Noesis..."* per averla come app standalone sul desktop o nella home del telefono.

---

## Riepilogo file

| File | Azione |
|------|--------|
| `sw.js` | **Nuovo** — Service Worker condiviso |
| `manifest-complete.json` | **Nuovo** |
| `manifest-reader.json` | **Nuovo** |
| `manifest-editor.json` | **Nuovo** |
| `icon-192.png` | **Nuovo** |
| `icon-512.png` | **Nuovo** |
| `noesis816.html` | **Modificato** — tag PWA |
| `noesis816-reader.html` | **Modificato** — tag PWA |
| `noesis816-editor.html` | **Modificato** — tag PWA |
| `index.html` | **Modificato** — sezione "Install as App" |

**Totale: 6 nuovi file, 4 modificati. ~1 ora di lavoro (più persistent storage da valutare).**
