# Architettura Tecnica

> Versione: **v810** | Stack: Vanilla JS | Architettura: No Server

---

## Struttura Generale

Noesis è una **Single-File HTML Application (SFA)**: tutto il codice (HTML, CSS, JavaScript) risiede in un unico file `noesis810.html`. Questa scelta architettonica garantisce portabilità assoluta, zero build step obbligatorio e funzionamento offline nativo.

```
noesis810.html
├── <head>: dipendenze CDN + CSS inline
├── <body>: Library View | Reader View
└── <script>:
    ├── Business logic (vanilla JS)
    ├── #sn56Source (JSON blob — sorgente Editor sn56.x)
    └── IndexedDB + IDB Bridge
```

---

## Stack Tecnologico

**Filosofia**: Vanilla JavaScript puro — zero framework runtime, zero build pipeline obbligatoria, stabilità nel tempo.

### Dipendenze CDN (noesis810.html)

| Libreria | Versione | Utilizzo |
|---------|---------|---------|
| epub.js | 0.3.93 | Parsing e rendering EPUB |
| JSZip | 3.10.1 | Decompressione archivi `.epub` |
| Bootstrap Icons | 1.11.3 | Icone SVG via font |

### Dipendenze CDN (sn56.x — Editor Embedded)

| Libreria | Versione | Utilizzo |
|---------|---------|---------|
| Summernote lite | 0.9.1 | Editor WYSIWYG con toolbar |
| jQuery | 3.7.1 | DOM manipulation (richiesto da Summernote) |
| Turndown | latest | Conversione HTML → Markdown |
| html-docx-js | latest | Generazione documenti DOCX |
| JSZip | latest | Packaging ZIP per export MD+ZIP |
| Bootstrap Icons | 1.11.3 | Icone UI (già presente nel parent) |

### Strumenti Integrati (v810)

| Strumento | Tipo | Note |
|-----------|------|------|
| Excalidraw (fork Noesis) | Tool Editor | Aperto in nuovo tab; diagrammi, flowchart, mind map; export SVG/PNG; salvataggio localStorage |
| Pandoc Online | Tool Library | `pandoc.wasm` nel browser; conversioni MD/DOCX/HTML/LaTeX/EPUB; nessun upload |
| Mozilla PDF Viewer | Tool Library | Visualizzatore PDF basato su PDF.js |

### Browser API Utilizzate

- `showDirectoryPicker()` / `showSaveFilePicker()` — File System Access API (Chrome/Edge 86+)
- `URL.createObjectURL()` / `URL.revokeObjectURL()` — Blob URL management
- `IndexedDB` — Storage persistente locale
- `window.postMessage()` — Comunicazione cross-window
- `File API` — Upload/download
- `DOM Range API` — Selezione testo e inject chunk al cursore
- `CFI (Canonical Fragment Identifiers)` — Posizionamento EPUB.js

---

## Architettura Multi-View

Due view principali gestite come sezioni DOM nascoste/visibili:

```
noesis810.html
├── #library-view    ← Catalogo, gestione snapshot, toolbar
└── #reader-view     ← Rendering EPUB, TOC, annotazioni, extract
```

Nessun router framework: state gestito tramite funzioni JavaScript.

L'Editor (sn56.x) si apre in un **nuovo tab separato** tramite Blob URL (vedi sezione "Embedding sn56.x").

---

## Embedding sn56.x

L'Editor è un file HTML separato (`sn56.15-baseline.html`) che viene **embedded come stringa JSON** in `noesis810.html` tramite il processo di build.

### Processo Build (build.py)

```python
# build.py
sorgente = open('sn56.15-baseline.html').read()
json_str = json.dumps(sorgente)  # Escape automatico caratteri speciali
# Sostituisce blocco <!-- SN56_SOURCE_START ... SN56_SOURCE_END -->
# in noesis810.html con il JSON risultante
```

Il JSON risultante viene memorizzato in un elemento `<script type="application/json" id="sn56Source">`.

### Launch sn56.x — _openSn56(payload)

```javascript
function _openSn56(payload) {
  // 1. Recupera sorgente editor
  const src = JSON.parse(document.getElementById('sn56Source').textContent);

  // 2. Costruisce data island con payload
  const island = payload
    ? '<script type="application/json" id="noesisPayload">'
      + JSON.stringify(payload) + '<\/script>'
    : '';

  // 3. Inietta payload nel sorgente (sostituzione placeholder)
  const html = src.replace('<!-- SN56_PAYLOAD_SLOT -->', island);

  // 4. Crea Blob URL e apre in nuovo tab
  const url = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
  const w = window.open(url, '_blank');

  // 5. Revoca URL dopo 60s (cleanup memoria)
  if (w) setTimeout(() => URL.revokeObjectURL(url), 60000);
}
```

### Struttura Payload

```json
{
  "mode": "chapter | standalone",
  "bookName": "Nome libro",
  "chapterName": "Nome capitolo",
  "chapterId": "ch_1711270422_123456",
  "snapshotId": "snap_1711270422_654321",
  "htmlContent": "<html>...</html>"
}
```

### Boot sn56.x

```javascript
function _bootPayload() {
  const el = document.getElementById('noesisPayload');
  if (!el) { _mode = 'standalone'; return; }

  const payload = JSON.parse(el.textContent);
  _mode        = payload.mode        || 'standalone';
  _bookName    = payload.bookName    || '';
  _chapterName = payload.chapterName || '';
  _chapterId   = payload.chapterId   || '';

  // Carica contenuto in Summernote
  $('#editor').summernote('code', payload.htmlContent);
}
```

### I tre percorsi di accesso all'Editor

**Percorso 1 — Library → Open Editor (standalone):**
- Trigger: click "Open Editor" nella toolbar Library
- Payload: `null`
- Risultato: editor vuoto, nessun chapterId, salvataggio solo su filesystem

**Percorso 2 — Library → capitolo/snapshot (chapter):**
- Trigger: click su nome capitolo o snapshot nella griglia
- Payload: `{mode: 'chapter', htmlContent, bookName, chapterName, chapterId}`
- Risultato: editor con contenuto caricato, salvataggio in IDB + filesystem

**Percorso 3 — Reader → Extract (chapter immediato):**
- Trigger: click "Extract" nel Reader
- Azioni parallele: genera chapterId, salva origin snapshot in IDB, scarica 2 file HTML, apre editor
- Payload: `{mode: 'chapter', htmlContent, bookName, chapterName, chapterId}`

---

## IDB Bridge — Comunicazione Cross-Window

sn56.x viene eseguito in un contesto `blob:null`, che **non può accedere direttamente a IndexedDB** della finestra principale per ragioni di sicurezza. Il bridge risolve questo tramite `postMessage`.

### Flusso

```
sn56.x (blob:null)                    noesis810.html (main window)
      |                                        |
      |  postMessage({                         |
      |    __noesisIDB: true,                  |
      |    op: 'get' | 'put',                  |
      |    payload: { chapterId, ... }         |
      |  })                                    |
      |   ─────────────────────────────────►   |
      |                                        |  Esegue operazione IDB
      |                                        |  su noesisDB
      |   ◄─────────────────────────────────   |
      |  postMessage({                         |
      |    __noesisIDBResponse: true,          |
      |    result | error                      |
      |  })                                    |
```

**Operazioni supportate**:

| Op | Funzione |
|----|----------|
| `get` | Recupera chapterRecord da noesisDB (metadati + lista snapshot) |
| `put` | Aggiorna chapterRecord in noesisDB |

---

## Persistenza Dati

### EpubLibraryDB (Libri)

**Database**: `EpubLibraryDB` | **Version**: 1 | **ObjectStore**: `books` (keyPath: `id`)

```javascript
{
  id: 'book_uuid',
  title: 'Titolo',
  author: 'Autore',
  coverUrl: 'data:image/jpeg;base64,...',   // base64 per persistenza
  arrayBuffer: ArrayBuffer,                  // file EPUB binario
  tableOfContents: [...],
  spine: [...],
  metadata: {...},
  bookState: {
    position: { start: { cfi: '...' } },
    fontSize: 100,
    lineHeight: 1.6,
    theme: 'normal',
    readerHighlights: [{ cfi, color }],
    userBookmarks: [{ label, cfi, createdAt }]
  }
}
```

### noesisDB (Estratti + Metadati Snapshot)

**Database**: `noesisDB` | **Version**: 1 | **ObjectStore**: `extractedChapters` (keyPath: `chapterId`)

```javascript
{
  chapterId: 'ch_1711270422_123456',      // Primary key
  bookName: 'Nome libro',                  // Indexed
  chapterName: 'Nome capitolo',            // Indexed
  createdAt: '2026-03-24T14:30:22.000Z',
  snapshots: [
    {
      snapshotId: 'snap_timestamp_random',
      createdAt: '2026-03-24T...',
      description: 'clean-20260324-143022',  // label per UI
      isOrigin: false
      // NOTA: content HTML NON è in IDB — è sui file su filesystem
    }
  ]
}
```

**Indici**: `bookName` (non-unique), `chapterName` (non-unique)

### localStorage

- Tema corrente (`theme`)
- Font size, interlinea
- Flag help overlay visualizzato
- Tema Library (`lib-theme`)

---

## Sistema Snapshot (Filesystem-Based)

A differenza delle versioni precedenti (v703-704) dove il content HTML era salvato in IndexedDB, **v810 salva i file HTML direttamente su filesystem** tramite download automatico.

### Naming Convention (14 tipi)

```
noesis-{TIPO}-{BOOKNAME}__{CHAPTERNAME}__{YYYYMMDD_HHMMSS}_{CUSTOM}.{EXT}
```

| Tipo | Descrizione |
|------|-------------|
| `origin` | Primo snapshot; contiene meta tag per reimporto |
| `clean` | Snapshot senza highlight |
| `annot` | Snapshot con highlight inline |
| `extract` | HTML grezzo estratto (senza toolbar Noesis) |
| `html` | Export HTML standalone |
| `docx` | Export DOCX |
| `text` | Export TXT |
| `markdown` | Export Markdown |
| `mdzip` | Export Markdown + immagini ZIP |
| `jsondoc` | Export JSON documento |
| `collection` | Export collezione chunk JSON |
| `colhtml` | Export collezione HTML |
| `colmd` | Export collezione Markdown |
| `colzip` | Export collezione Markdown + immagini ZIP |

### Meta Tag (file `origin` — reimportabili)

```html
<meta name="noesis-chapter-id"       content="ch_...">
<meta name="noesis-book-name"        content="...">
<meta name="noesis-chapter-name"     content="...">
<meta name="noesis-snapshot-variant" content="origin|clean|annot">
```

### Parsing Nome File (Import)

```javascript
const match = file.name.match(
  /^noesis-[a-z]+-(.+)__(.+)__(\d{8}_\d{6})(?:_([^.]+))?\.html?$/i
);
// match[1] = bookName (underscore → spazio)
// match[2] = chapterName
// match[3] = timestamp YYYYMMDD_HHMMSS
// match[4] = custom label (opzionale)
```

---

## Sistema di Estrazione EPUB

### Flusso Tecnico

```
rendition.currentLocation()
    ↓
Localizza capitolo corrente in spine
    ↓
(modalità tree: individua tutti i sottolivelli dalla spine)
    ↓
Carica file HTML da EPUB via JSZip
    ↓
Estrai body content
    ↓
Conversione immagini → base64 inline
  img.src = ArrayBuffer → btoa() → data:image/[type];base64,[data]
    ↓
Riscrittura link interni come ancore locali
    ↓
Genera chapterId: ch_[timestamp]_[random]
    ↓
Salva chapterRecord in noesisDB (metadati)
    ↓
_openSn56({ mode:'chapter', htmlContent, bookName, chapterName, chapterId })
    ↓
Nuovo tab — sn56.x — Summernote carica contenuto
```

---

## Sistema di Temi (Reader)

15 temi implementati come **CSS custom properties** su `:root`:

```css
:root {
  --bg-color: #ffffff;
  --text-color: #1a1a1a;
  --sidebar-bg: #f5f5f5;
  --toolbar-bg: #f0f0f0;
  --link-color: #2563eb;
  --border-color: #e0e0e0;
}
```

Applicazione dinamica: `document.documentElement.style.setProperty('--bg-color', value)`
Persistenza: `localStorage.setItem('theme', themeKey)`

**Gruppi temi**:

```javascript
const THEME_GROUPS = {
  'Chiari':       ['normal', 'softwhite'],
  'Caldi':        ['cream', 'sepia', 'parchment'],
  'Grigi chiari': ['gray', 'coolgray', 'warmgray'],
  'Grigi scuri':  ['midgray', 'slate', 'darkgray'],
  'Notturni':     ['charcoal', 'dark', 'midnight', 'truedark']
};
```

Rendering Reader tramite: `rendition.themes.register('custom', cssObj)` + `rendition.themes.select('custom')`

---

## Sistema di Highlight (Reader)

Basato su **EPUB CFI Annotations** di epub.js:

```javascript
rendition.annotations.highlight(cfiRange, {}, handler, 'yellow');
// cfiRange: es. "epubcfi(/6/4[chap1]!/4/2/1,:0,:10)"
```

Highlights persistiti nel `bookState.readerHighlights` array in `EpubLibraryDB`.

---

## Export System (sn56.x)

| Formato | Tecnologia | Note |
|---------|-----------|------|
| DOCX | html-docx-js | Generazione XML OOXML direttamente nel browser |
| Markdown | Turndown | Conversione HTML → MD con configurazione custom |
| MD+ZIP | Turndown + JSZip | Immagini base64 estratte e archiviate separatamente |
| JSON | JSON.stringify | Struttura dati documento |
| PDF | `window.print()` | CSS `@media print` ottimizzati per A4 |
| TXT | innerText | Estrazione testo puro |

## Sistema Chunk Collection (sn56.x)

### Struttura dati

```javascript
var _collection = []; // Array in-memory di chunk

// Un chunk:
{
  id: "1711530000000_123456789",  // univoco
  content: "<p>HTML del chunk</p>",
  type: "text" | "image" | "table",
  bookName: "Nome libro",
  chapterName: "Nome capitolo",
  timestamp: 1711530000000
}
```

### Metodi di aggiunta

- **Pulsante [+]**: aggiunge testo selezionato, immagine tracciata, o tabella
- **Doppio tap immagine**: aggiunge direttamente
- **Long press (600ms)** su immagine: aggiunge direttamente (Android)

### Inspect Panel

Pannello flottante non modale:
- Draggable via header
- Resizable via handle
- Azioni per chunk: Inject al cursore, Fullscreen, Delete
- Selezione multipla + Inject di gruppo

### Export Collezione

| Formato | Note |
|---------|------|
| JSON | Backup/import completo |
| HTML | Pagina standalone |
| Markdown | Immagini omesse |
| MD+ZIP | Immagini estratte |

---

## Sicurezza e Privacy

| Aspetto | Implementazione |
|---------|----------------|
| Zero server | Nessun backend; tutto locale |
| IndexedDB isolato | Accessibile solo dallo stesso dominio/protocollo |
| Blob URL isolation | sn56.x in `blob:null` context, isolato per design |
| Nessun analytics | Zero librerie di tracciamento |
| Nessuna auth | Zero credenziali da compromettere |
| CDN only | Unico contatto di rete al primo caricamento |
| No DRM support | File protetti non compatibili |

---

## Limitazioni Note e Workaround

| Limitazione | Causa | Workaround |
|------------|-------|-----------|
| Alcuni EPUB non si renderizzano | CORS con `file://` | Usare server locale Python |
| `showDirectoryPicker()` non disponibile | Browser non supportato | Fallback su file picker standard |
| File EPUB molto grandi (>100MB) | RAM parsing in memoria | Dipende dalla memoria del dispositivo |
| PDF qualità variabile | Print CSS approximation | Usare stampa nativa del browser |
| No sync cross-device | Offline-first by design | Esportare JSON collezioni manualmente |
| Snapshot accumulano spazio | File HTML completi su disco | Cancellazione manuale dalla Library o dal filesystem |
