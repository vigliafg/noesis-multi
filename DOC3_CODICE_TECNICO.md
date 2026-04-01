# NOESIS810 — Documento 3: Descrizione Tecnica del Codice

> Fonte: `noesis810.html` (6498 righe) — Aggiornato: 2026-03-27
> Standard di riferimento: ES2020, IndexedDB L2, epub.js v0.3.x

---

## STRUTTURA DEL FILE

| Blocco | Righe | Contenuto |
|--------|-------|-----------|
| `<head>` | 1–9 | Meta, viewport, link Bootstrap Icons CDN |
| CSS globale | 10–2357 | ~2350 righe di stili inline (library, reader, popup, drawer, media, help, ecc.) |
| HTML strutturale | 2358–2830 | DOM statico: overlay loading, library-view, reader-view con tutti i pannelli |
| JavaScript (noesisDB) | 2831–3030 | Modulo database noesis (capitoli estratti) |
| JavaScript (IDB bridge) | 3000–3030 | window.message bridge per IDB da contesti blob |
| JavaScript (mainDB) | 3031–3157 | Modulo database principale (libri EPUB) |
| JavaScript (UI core) | 3158–3830 | Variabili globali, funzioni di show/hide, toast, libreria UI |
| JavaScript (reader) | 3831–6498 | Logica lettore: rendition, navigazione, stato, highlights, help, listeners |

---

## DIPENDENZE ESTERNE

| Libreria | Caricamento | Versione/Uso |
|----------|-------------|--------------|
| **epub.js** | `<script src="...">` (CDN o locale) | Rendering EPUB in iframe, navigazione, TOC, annotazioni |
| **JSZip** | incluso in epub.js o separato | Decompressione zip EPUB per estrazione immagini |
| **Bootstrap Icons** | CSS CDN (`cdn.jsdelivr.net`) | Icone UI (bi-book, bi-trash, ecc.) |

Nessun framework JS (React, Vue, Angular). Nessun bundler. Zero npm.

---

## VARIABILI GLOBALI — CATALOGO COMPLETO

### Costanti Database

```javascript
// Riga 3026–3028 — Database libri EPUB
const DB_NAME    = "EpubLibraryDB";
const DB_VERSION = 1;
const STORE_NAME = "books";

// Riga 2838–2840 — Database capitoli estratti
const NOESIS_DB      = "noesisDB";
const NOESIS_VERSION = 1;
const NOESIS_STORE   = "chapters";
```

### Riferimenti DOM (costanti, riga 3152–3156)

```javascript
const libraryView    = document.getElementById('library-view');
const readerView     = document.getElementById('reader-view');
const bookGrid       = document.getElementById('bookGrid');
const loadingOverlay = document.getElementById('loading-overlay');
const loadingMsg     = document.getElementById('loading-msg');
```

### Stato Lettore (let, riga 3709–3746)

```javascript
let book            = null;   // Istanza ePub.js Book
let rendition       = null;   // Istanza ePub.js Rendition
let fontSize        = 100;    // Percentuale font (50–300)
let lineHeight      = 1.6;    // Valore corrente line-height
let lineHeights     = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4];
let scrollMode      = false;  // true = flow scrolled-doc
let dualPageMode    = false;  // true = spread affiancato
let sidebarVisible  = true;   // TOC sidebar aperta
let currentTheme    = "white"; // Chiave tema THEME_COLORS
let currentLocation = null;   // Oggetto location epub.js
let buttonZoom      = 100;    // Scala toolbar (60–200)

let interfaceSettings = {     // Colori UI personalizzati
  toolbarColor:    "#1e293b",
  sidebarColor:    "#1e293b",
  navButtonsColor: "#1e293b",
  navOpacity:      0.7,
  ubmDrawerColor:  "#1e293b"
};

let currentBookId    = null;  // ID libro aperto
let currentBookTitle = null;  // Titolo libro aperto

let readerHighlights             = [];     // [{cfi, color}, ...]
let currentReaderHighlightColor  = "yellow";
let _readerHlHasSelection        = false;  // testo selezionato?
let _readerPendingCfi            = null;   // CFI da evento 'selected'

let userBookmarks = [];  // [{cfi, href, chapter, preview, label, timestamp}]
```

### Costanti Tema

```javascript
// Riga 4759 — 15 temi raggruppati
const THEME_COLORS = {
  white:      { background: "#ffffff", color: "#1a1a1a", a: "#1a5fa8" },
  offwhite:   { ... },
  cream:      { ... },
  sepia:      { ... },
  // ... 11 altri temi fino a black
};

// Riga 4784 — raggruppamento per categoria UI
const THEME_GROUPS = [
  { label: "White",       keys: ["white", "offwhite"] },
  { label: "Cream/Sepia", keys: ["cream", "sepia", "warmsepia"] },
  { label: "Light Gray",  keys: ["lightgray", "silver", "slate"] },
  { label: "Medium Gray", keys: ["medgray", "stone"] },
  { label: "Dark Gray",   keys: ["darkgray", "charcoal"] },
  { label: "Dark/Black",  keys: ["dark", "nearblack", "black"] },
];
```

---

## FUNZIONI — CATALOGO TECNICO COMPLETO

### MODULO: Database noesisDB

---

#### `openNoesisDB()` — riga 2845
```
Firma: openNoesisDB() → Promise<IDBDatabase>
```
- Apre (o crea) IndexedDB `"noesisDB"` versione 1
- `onupgradeneeded`: crea object store `"chapters"` con keyPath `"chapterId"`
- Ritorna Promise che risolve con l'istanza `IDBDatabase`
- Usata come dependency da tutte le funzioni noesisDB successive

---

#### `saveExtractedChapterToDB(record)` — riga 2866
```
Firma: saveExtractedChapterToDB(record: Object) → Promise<void>
```
- `record` ha forma: `{chapterId, bookId, bookTitle, chapterTitle, snapshots:[...]}`
- Apre transaction `readwrite` su `"chapters"`, esegue `put(record)`
- Idempotente: sovrascrive record esistente con stesso `chapterId`

---

#### `getExtractedChapterFromDB(chapterId)` — riga 2900
```
Firma: getExtractedChapterFromDB(chapterId: string) → Promise<Object|undefined>
```
- Transaction `readonly`, `get(chapterId)`
- Ritorna il record o `undefined` se non trovato

---

#### `deleteExtractedChapterFromDB(chapterId)` — riga 2922
```
Firma: deleteExtractedChapterFromDB(chapterId: string) → Promise<void>
```
- Transaction `readwrite`, `delete(chapterId)`
- Rimuove l'intero record capitolo con tutti i suoi snapshot

---

#### `deleteSnapshotFromDB(chapterId, snapshotId)` — riga 2943
```
Firma: deleteSnapshotFromDB(chapterId: string, snapshotId: string) → Promise<void>
```
- Legge il record capitolo
- Filtra `record.snapshots` rimuovendo quello con `snapshotId` corrispondente
- Se `snapshots` rimane vuoto → elimina l'intero record capitolo
- Altrimenti → `put(record aggiornato)`
- **Side effect**: chiama `loadLibraryBooks()` al completamento per aggiornare UI

---

#### `getAllExtractedChapters()` — riga 3216
```
Firma: getAllExtractedChapters() → Promise<Array<Object>>
```
- Transaction `readonly`, `getAll()` su store `"chapters"`
- Ritorna array di tutti i record capitolo nel database

---

### MODULO: Database EpubLibraryDB

---

#### `openDB()` — riga 3031
```
Firma: openDB() → Promise<IDBDatabase>
```
- Apre IndexedDB `"EpubLibraryDB"` versione 1
- `onupgradeneeded`: crea store `"books"` con keyPath `"id"`, autoIncrement `true`
- Ritorna Promise con `IDBDatabase`

---

#### `saveBookToDB(file)` — riga 3071
```
Firma: saveBookToDB(file: File) → Promise<void>
```
- Legge il file EPUB come `ArrayBuffer`
- Istanzia temporaneamente `new ePub()` per estrarre metadati:
  - `book.loaded.metadata` → `{title, creator}`
  - `book.loaded.cover` → URL copertina (blob)
- Record salvato: `{title, author, coverUrl, data: ArrayBuffer, dateAdded}`
- La chiave `id` è autogenerata da IDB (`autoIncrement`)

---

#### `getAllBooks()` — riga 3122
```
Firma: getAllBooks() → Promise<Array<Object>>
```
- Transaction `readonly`, `getAll()`
- Ritorna tutti i record libro (incluso ArrayBuffer EPUB)

---

#### `deleteBook(id)` — riga 3134
```
Firma: deleteBook(id: number) → Promise<void>
```
- Transaction `readwrite`, `delete(id)`
- **Side effect**: se `id === currentBookId`, reimposta variabili stato lettore a null
- Chiama `loadLibraryBooks()` per aggiornare griglia

---

### MODULO: UI Core

---

#### `showLoading(msg)` — riga 3158
```
Firma: showLoading(msg: string) → void
```
- Imposta `loadingMsg.textContent = msg`
- Rimuove classe `hidden` da `loadingOverlay`

---

#### `hideLoading()` — riga 3163
```
Firma: hideLoading() → void
```
- Aggiunge classe `hidden` a `loadingOverlay`

---

#### `showLibrary()` — riga 3167
```
Firma: showLibrary() → void
```
- Distrugge rendition e book (se esistenti): `rendition.destroy()`, `book.destroy()`
- Azzera tutte le variabili stato lettore
- Chiude drawer, popup, sidebar
- Nasconde `#reader-view`, mostra `#library-view`
- Chiama `loadLibraryBooks()`

---

#### `showReader()` — riga 3210
```
Firma: showReader() → void
```
- Nasconde `#library-view`
- Mostra `#reader-view`
- Aggiusta posizione top sidebar (`updateBookmarksTop()`)

---

#### `loadLibraryBooks()` — riga 3314
```
Firma: loadLibraryBooks() → Promise<void>
Dipendenze: getAllBooks(), getAllExtractedChapters()
```
- Carica in parallelo libri e capitoli estratti da IDB
- Crea mappa `chaptersByBookId` per lookup rapido
- Ordina libri per `dateAdded` decrescente
- Per ogni libro genera HTML riga con:
  - Copertina (img o icona Bootstrap)
  - Titolo, autore, data aggiunta
  - Badge capitoli/snapshot
  - Pulsante elimina libro
  - Sezione espandibile capitoli estratti (se presenti)
    - Per ogni capitolo: titolo, lista snapshot con dot indicator, pulsanti
- Inserisce HTML in `bookGrid.innerHTML`
- Riattacca event listener click (click delegation su `bookGrid`)

---

### MODULO: Estrazione Capitoli

---

#### `_openSn56(payload)` — riga 3232
```
Firma: _openSn56(payload?: Object) → void
```
- Apre finestra popup: `window.open("sn56.x", "_blank", "popup,width=1200,height=800")`
- Attende `load` sulla nuova finestra
- Chiama `newWin.initFromPayload(payload)` passando il payload JSON

---

#### `_generateCleanHTML(title, css, body, metaTags)` — riga 3248
```
Firma: _generateCleanHTML(title: string, css: string, body: string, metaTags: Object) → string
```
- Genera stringa HTML completa con:
  - `<!DOCTYPE html>`, `<html>`, `<head>` con `<meta charset>`, `<title>`, `<style>`
  - Meta tag custom `noesis-*` (bookId, chapterId, timestamp, variant)
  - `<body>` con contenuto capitolo
- Usata per generare entrambe le varianti (extract/origin)

---

#### `_buildExtractionTimestamp()` — riga 3270
```
Firma: _buildExtractionTimestamp() → string
```
- Genera timestamp ISO `YYYYMMDD-HHmmss`
- Usato come suffisso condiviso per nominare la coppia di file extract/origin

---

#### `_autoDownloadHTML(filename, htmlContent)` — riga 3281
```
Firma: _autoDownloadHTML(filename: string, htmlContent: string) → void
```
- Crea `Blob` con `text/html`
- Crea URL object temporaneo
- Simula click su `<a download="filename">` per avviare download automatico
- Revoca URL object dopo click

---

#### `_openExtractedEnv(chapterRecord, snapshotId)` — riga 3292
```
Firma: _openExtractedEnv(chapterRecord: Object, snapshotId: string) → void
```
- Recupera snapshot specifico da `chapterRecord.snapshots`
- Costruisce payload per sn56.x
- Chiama `_openSn56(payload)`

---

#### `collectAllSubchapters(tocEntry)` — riga 4182
```
Firma: collectAllSubchapters(tocEntry: TocItem) → Array<TocItem>
```
- Ricorsiva: raccoglie `tocEntry` + tutti i discendenti (depth-first)
- Usata da `extractMultipleSections` per modalità "Extract Tree"

---

#### `extractMultipleSections(tocEntries, overallTitle)` — riga 4193
```
Firma: extractMultipleSections(tocEntries: Array<TocItem>, overallTitle: string) → Promise<void>
```
- Per ogni voce TOC in `tocEntries`:
  - Naviga a quella sezione: `rendition.display(entry.href)`
  - Attende rendering iframe
  - Raccoglie HTML della sezione
- Concatena HTML di tutte le sezioni
- Procede come `extractCurrentChapter` per conversione immagini e generazione file

---

#### `extractCurrentChapter()` — riga 4439
```
Firma: extractCurrentChapter() → Promise<void>
Dipendenze: _buildExtractionTimestamp, _generateCleanHTML, _autoDownloadHTML,
            saveExtractedChapterToDB, _openSn56
```
Flusso interno:
1. Ottiene href corrente da `currentLocation.start.href`
2. Accede al documento iframe: `rendition.getContents()[0].document`
3. Clona il `<body>` del documento EPUB
4. Raccoglie tutti i tag `<link rel="stylesheet">` e `<style>` dall'iframe
5. Per ogni `<img>` nel clone:
   - Legge src relativo
   - Accede al file dallo zip EPUB via `book.archive.getBase64(path)`
   - Sostituisce `src` con `data:image/...;base64,...`
6. Serializza clone HTML → stringa
7. Genera timestamp condiviso
8. Chiama `_generateCleanHTML` × 2 (extract + origin)
9. Chiama `_autoDownloadHTML` × 2
10. Costruisce record snapshot per noesisDB
11. Chiama `saveExtractedChapterToDB`
12. Chiama `_openSn56(payload)`

---

### MODULO: Snapshot Import

---

#### `importSnapshotsFromDisk()` — riga 3483
```
Firma: importSnapshotsFromDisk() → void
```
- Crea `<input type="file" webkitdirectory accept=".html">` dinamicamente
- Attach listener `change` → chiama `_processSnapshotFiles(input.files)`
- Simula click per aprire picker

---

#### `_processSnapshotFiles(files)` — riga 3515
```
Firma: _processSnapshotFiles(files: FileList) → Promise<void>
```
- Itera su ogni `File` nella lista
- Legge contenuto come testo (`FileReader.readAsText`)
- Estrae meta tag `noesis-*` dal testo HTML (regex o DOMParser)
- Determina `chapterId` = `bookTitle__chapterTitle__timestamp`
- Se record esiste in noesisDB: append snapshot all'array
- Se non esiste: crea nuovo record
- Aggiorna noesisDB, poi chiama `loadLibraryBooks()`

---

### MODULO: Navigazione Reader

---

#### `navigateToHref(href)` — riga 3991
```
Firma: navigateToHref(href: string) → void
```
- Se `scrollMode`: chiama `rendition.display(href)` direttamente
- Se pagine: `rendition.display(href)` (epub.js gestisce paginazione)
- Usata da TOC click e user bookmarks

---

#### `findBreadcrumbInToc(items, targetHref, ancestorPath)` — riga 5069
```
Firma: findBreadcrumbInToc(items: Array<TocItem>, targetHref: string, ancestorPath?: string[]) → string[]|null
```
- Ricorsiva depth-first search nel TOC
- Confronta `item.href` (normalizzato senza fragment) con `targetHref`
- Ritorna array di label antenati + label corrente
- Usata da `setStatusPath` per costruire breadcrumb

---

#### `renderBookmarksSimple(toc)` — riga 5088
```
Firma: renderBookmarksSimple(toc: Array<TocItem>) → void
```
- Genera `<ul>` ricorsivo per ogni livello TOC
- Ogni `<li>` ha `data-href` e click listener → `navigateToHref(href)`
- Indentazione visiva con `padding-left` proporzionale al livello
- Inserisce in `#bookmarks` (sidebar DOM element)

---

### MODULO: Stato Libro

---

#### `openBookFromLibrary(bookData)` — riga 3604
```
Firma: openBookFromLibrary(bookData: Object) → Promise<void>
Dipendenze: showLoading, loadAndApplyBookState, recreateRendition (implicita),
            applyTheme, applyInterfaceSettings, loadUserBookmarksFromDB,
            renderBookmarksSimple, showReader, hideLoading, maybeShowBanner
```
- Entry point principale per apertura libro
- Vedi workflow dettagliato in DOC2

---

#### `saveBookState()` — riga 3765
```
Firma: saveBookState() → Promise<void>
Dipendenze: openDB, showToast
```
- Raccoglie snapshot completo dello stato corrente
- `savedState.position = { cfi: currentLocation?.start?.cfi, href: currentLocation?.start?.href }`
- `savedState.timestamp = Date.now()`
- Aggiorna record libro in IDB con `put`

---

#### `loadAndApplyBookState(bookId)` — riga 3854
```
Firma: loadAndApplyBookState(bookId: number) → Promise<Object|null>
Dipendenze: openDB
```
- Legge `book.savedState` da IDB
- Applica valori a variabili globali
- Ritorna `savedState` o `null` se non trovato
- La posizione (`cfi`/`href`) viene applicata separatamente dopo `rendition` creata

---

### MODULO: User Bookmarks

---

#### `loadUserBookmarksFromDB(bookId)` — riga 5185
```
Firma: loadUserBookmarksFromDB(bookId: number) → Promise<void>
```
- Legge `book.userBookmarks` da IDB
- Imposta variabile globale `userBookmarks = data || []`
- Chiama `renderUbmList()` e aggiorna badge counter

---

#### `saveUserBookmarksToDB()` — riga 5157
```
Firma: saveUserBookmarksToDB() → Promise<void>
```
- Scrive `userBookmarks` nel record libro in IDB (`book.userBookmarks = userBookmarks`)

---

#### `renderUbmList()` — riga 5207
```
Firma: renderUbmList() → void
```
- Genera HTML della lista segnalibri nel drawer `#userBookmarksDrawer`
- Ogni riga: capitolo, preview 100 char, data/ora formattata, pulsante `×`
- Click su riga → `navigateToHref(bm.href)` + `closeUbmDrawer()`
- Click su `×` → splice da `userBookmarks`, `saveUserBookmarksToDB()`, `renderUbmList()`

---

#### `createUserBookmark()` — riga 5296
```
Firma: createUserBookmark() → void
Dipendenze: findBreadcrumbInToc, saveUserBookmarksToDB, renderUbmList
```
- Costruisce oggetto segnalibro con dati correnti
- `userBookmarks.unshift(nuovo)` — più recente in cima
- Salva e ridisegna lista

---

#### `openUbmDrawer()` / `closeUbmDrawer()` — righe 5400 / 5411
```
Firma: openUbmDrawer() → void
       closeUbmDrawer() → void
```
- Toggle classe `open` su `#userBookmarksDrawer`
- Il drawer è `position: fixed` con transizione CSS `transform: translateX()`

---

### MODULO: Tema

---

#### `applyTheme()` — riga 4790
```
Firma: applyTheme() → void
Dipendenze: THEME_COLORS, rendition (globale)
```
- `const t = THEME_COLORS[currentTheme]`
- `rendition.themes.register(currentTheme, { body: { background: t.background, color: t.color }, a: { color: t.a } })`
- `rendition.themes.select(currentTheme)`

---

#### `updateThemeSwatchActive()` — riga 4816
```
Firma: updateThemeSwatchActive() → void
```
- Rimuove classe `active` da tutti gli swatch
- Aggiunge `active` allo swatch con `data-theme === currentTheme`

---

#### `buildThemePopup()` — riga 4824
```
Firma: buildThemePopup() → void
Dipendenze: THEME_GROUPS, THEME_COLORS
```
- Genera HTML del popup tema con gruppi e swatches
- Ogni swatch: `<div class="theme-swatch" data-theme="white" style="background:#fff;">` con tooltip
- Click swatch → `currentTheme = theme`, `applyTheme()`, `updateThemeSwatchActive()`, `saveBookState()`

---

### MODULO: Rendition e Layout

---

#### `recreateRendition()` — riga 4866
```
Firma: recreateRendition() → Promise<void>
Dipendenze: book (globale), applyTheme, applyInterfaceSettings
```
- Salva posizione corrente: `savedCfi = currentLocation?.start?.cfi`
- `rendition.destroy()`
- Ricrea `rendition = book.renderTo(element, options)` con nuovi parametri layout
- Riregistra hook `content.register`
- Riregistra eventi `relocated`, `selected`, `linkClicked`
- `rendition.display(savedCfi)` per ripristinare posizione
- Riapplica tema e highlights

---

#### `applyInterfaceSettings()` — riga 3942
```
Firma: applyInterfaceSettings() → void
Dipendenze: interfaceSettings (globale), hexToRgba, adjustColor
```
- Applica inline CSS a elementi DOM specifici:
  - `header.style.background = linear-gradient(...)` con `toolbarColor`
  - `#bookmarks.style.background = rgba(...)` con `sidebarColor`
  - `#floatingPrevBtn/.Next.style` con `navButtonsColor` + `navOpacity`
  - Variabile CSS `--ubm-bg` su `#userBookmarksDrawer` con `ubmDrawerColor`

---

#### `updateBookmarksTop()` — riga 5548
```
Firma: updateBookmarksTop() → void
```
- Legge `header.getBoundingClientRect().height`
- Imposta `bookmarks.style.top = altezza + "px"`
- Garantisce che sidebar parta esattamente sotto l'header (responsive)
- Chiamata su: DOMContentLoaded, resize, orientationchange, ResizeObserver su header

---

### MODULO: Helper Utilità

---

#### `hexToRgba(hex, alpha)` — riga 3971
```
Firma: hexToRgba(hex: string, alpha: number) → string
```
- Converte `"#1e293b"` → `"rgba(30,41,59,0.7)"`
- Supporta hex corto (#rgb) e lungo (#rrggbb)

---

#### `adjustColor(hex, percent)` — riga 3979
```
Firma: adjustColor(hex: string, percent: number) → string
```
- Schiarisce/scurisce colore hex di `percent` punti (range -100...+100)
- Usata per generare gradiente header dalla `toolbarColor` base

---

#### `showToast(msg, type, duration)` — riga 3749
```
Firma: showToast(msg: string, type: "saving"|"saved"|"error", duration?: number) → void
```
- Modifica testo e classe CSS del `#saveToast`
- Mostra il toast con classe `visible`
- Auto-nasconde dopo `duration` ms (default 2000)

---

#### `setStatus(msg)` — riga 3906
```
Firma: setStatus(msg: string) → void
```
- Imposta testo della status bar `#readerStatus`

---

#### `setStatusPath(fullPath)` — riga 3910
```
Firma: setStatusPath(fullPath: string[]) → void
```
- Riceve array di label (breadcrumb)
- Condensa: se stringa finale > N char, abbrevia sezioni intermedie con `…`
- Chiama `setStatus` con stringa formattata

---

#### `updateFontInfo()` / `updateLineHeightInfo()` — righe 3933 / 3937
```
Firma: updateFontInfo() → void
       updateLineHeightInfo() → void
```
- Aggiorna label numerica nel popup tipografia
- `updateFontInfo`: mostra `fontSize + "%"`
- `updateLineHeightInfo`: mostra valore corrente `lineHeight`

---

#### `getIframeSelection()` — riga 5997
```
Firma: getIframeSelection() → Selection|null
```
- Accede a `rendition.getContents()[0].window.getSelection()`
- Ritorna selezione testo dall'interno dell'iframe EPUB
- Necessaria perché `document.getSelection()` non include iframe cross-origin

---

#### `applyReaderHighlight()` — riga 6010
```
Firma: applyReaderHighlight() → void
Dipendenze: _readerPendingCfi, currentReaderHighlightColor, rendition, readerHighlights
```
- `rendition.annotations.highlight(cfi, {}, callback, "hl-"+color)`
- `readerHighlights.push({cfi, color})`
- Reset stato: `_readerHlHasSelection = false`, `_readerPendingCfi = null`

---

#### `removeReaderHighlight()` — riga 6044
```
Firma: removeReaderHighlight() → void
```
- Filtra `readerHighlights` per CFI pendente
- `rendition.annotations.remove(cfi, "highlight")`
- Aggiorna array globale

---

#### `setHlBtnColor(color)` — riga 5988
```
Firma: setHlBtnColor(color: string) → void
```
- Rimuove classi `hl-yellow`, `hl-green`, `hl-pink` dal pulsante
- Aggiunge classe `hl-` + color

---

#### `_closeAllReaderMenus()` — riga 6354
```
Firma: _closeAllReaderMenus() → void
```
- Chiude: popup tipografia, popup tema, popup zoom, popup interface, extract menu, highlight menu
- Collassa sezioni accordion del `#displayMenu`
- Chiamata su click esterno a qualunque menu

---

### MODULO: Help System

---

#### `maybeShowBanner(seenKey, bannerId)` — riga 6210
```
Firma: maybeShowBanner(seenKey: string, bannerId: string) → void
```
- `if (!localStorage.getItem(seenKey))` → rimuove classe `hidden` da `#bannerId`

---

#### `closeBanner(seenKey, bannerId)` — riga 6218
```
Firma: closeBanner(seenKey: string, bannerId: string) → void
```
- `localStorage.setItem(seenKey, "1")`
- Aggiunge `hidden` a `#bannerId`

---

#### `openOverlay(id)` / `closeOverlay(id)` — righe 6225 / 6229
```
Firma: openOverlay(id: string) → void
       closeOverlay(id: string) → void
```
- Toggle classe `hidden` sull'elemento `#id`

---

### MODULO: Media Handler (IIFE)

Riga 5423 — IIFE auto-eseguita che incapsula tutto il dialog media:

```javascript
(function() {
  const dialog = document.getElementById('readerMediaDialog');
  const fullscreen = document.getElementById('readerMediaFullscreen');

  function hideDialog() { ... }           // riga 5431
  function showDialog(type, data) { ... } // riga 5438
  function doPreview() { ... }            // riga 5448

  window.addEventListener('message', (e) => {
    if (e.data?.type === 'mediaTap') {
      showDialog(e.data.mediaType, e.data.data);
    }
  });
})();
```

- **Chiuso in IIFE**: nessuna contaminazione del namespace globale
- `hideDialog()`: svuota `dialog.innerHTML`, aggiunge `hidden`
- `showDialog(type, data)`:
  - Se `type === "image"`: `<img src="data:...">` nel dialog
  - Se `type === "table"`: clone del nodo tabella
  - Rimuove `hidden`, posiziona centrato
- `doPreview()`: copia contenuto in `#readerMediaFullscreen`, toglie `hidden`

---

## HOOK RENDITION — Iniezione nell'iframe EPUB

Riga 4922 — `rendition.hooks.content.register(contents => {...})`

Eseguito ogni volta che un capitolo EPUB viene caricato nell'iframe. Inietta:

1. **CSS custom reader** — stili per tabelle, highlights, media clickable
2. **Script media tap** — attacca `click` a ogni `<img>` e wrapper tabella nell'iframe
   - Al click: `parent.postMessage({type:"mediaTap", mediaType:"image", data:{src:img.src}}, "*")`
3. **Wrap tabelle** — ogni `<table>` viene wrappata in `<div class="table-wrapper">` scrollabile

---

## WINDOW MESSAGE BRIDGE (riga 3000–3030)

```javascript
window.addEventListener('message', async (e) => {
  if (e.data?.type !== 'idb-request') return;
  // Handler per richieste IDB da finestre blob (sn56.x)
  const { action, payload, requestId } = e.data;
  // switch su action: 'getChapter', 'saveChapter', 'deleteSnapshot', ecc.
  // risponde con: e.source.postMessage({type:'idb-response', requestId, data}, e.origin)
});
```

- Permette a sn56.x (aperto come popup) di accedere al noesisDB del parent
- Necessario perché i blob URL (`blob:`) sono cross-origin rispetto a `file://`
- Il bridge risponde con i dati richiesti via `postMessage` di ritorno

---

## CORRELAZIONI FRA FUNZIONI — GRAFO DIPENDENZE

```
DOMContentLoaded
    └── openDB + openNoesisDB (parallel)
    └── loadLibraryBooks
            ├── getAllBooks
            └── getAllExtractedChapters

openBookFromLibrary(bookData)
    ├── showLoading
    ├── loadAndApplyBookState
    │       └── openDB
    ├── recreateRendition
    │       ├── applyTheme
    │       │       └── THEME_COLORS
    │       ├── applyInterfaceSettings
    │       │       ├── hexToRgba
    │       │       └── adjustColor
    │       └── rendition.hooks.content.register
    │               → [injected into iframe]
    ├── renderBookmarksSimple(toc)
    │       └── findBreadcrumbInToc (usata da setStatusPath)
    ├── loadUserBookmarksFromDB
    │       └── renderUbmList
    └── showReader + hideLoading

saveBookState
    ├── openDB
    └── showToast

extractCurrentChapter
    ├── _buildExtractionTimestamp
    ├── _generateCleanHTML × 2
    ├── _autoDownloadHTML × 2
    ├── saveExtractedChapterToDB
    │       └── openNoesisDB
    └── _openSn56(payload)

deleteSnapshotFromDB(chapterId, snapshotId)
    ├── openNoesisDB
    ├── getExtractedChapterFromDB
    └── loadLibraryBooks  [side effect UI]

rendition 'relocated' event
    └── setStatusPath
            └── findBreadcrumbInToc

rendition 'selected' event
    └── [imposta _readerPendingCfi, _readerHlHasSelection]

click #readerHighlightBtn
    ├── Se selezione → applyReaderHighlight
    │       └── rendition.annotations.highlight
    └── Se no selezione → toggle menu colori
```

---

## NOTE TECNICHE RILEVANTI PER FUTURI SVILUPPATORI

1. **Zero framework, zero bundler**: tutto il codice è vanilla JS ES2020 in un singolo file. Non usare `import`/`export` senza un bundler.

2. **IndexedDB duale**: l'app mantiene due database separati (`EpubLibraryDB` per i libri, `noesisDB` per i capitoli). Non mescolare le due `openDB` calls.

3. **epub.js CFI**: la posizione nel libro è espressa come **Canonical Fragment Identifier** (es: `epubcfi(/6/4[chap01]!/4/2/2:10)`). Non è un semplice offset numerico. Per navigare a posizione salvata usare sempre `rendition.display(cfi)`.

4. **iframe cross-origin**: il testo EPUB è renderizzato in un iframe `blob:`. `document.getSelection()` non cattura selezioni al suo interno; usare `getIframeSelection()` che accede a `rendition.getContents()[0].window.getSelection()`.

5. **recreateRendition()**: deve essere chiamata ogni volta che si cambia `scrollMode` o `dualPageMode`, perché epub.js non supporta cambio layout in-place. Salvare sempre la posizione CFI prima e ripristinarla dopo.

6. **Hook content.register**: eseguito ad ogni capitolo caricato. Non è una registrazione one-shot. Tutti gli script/stili iniettati qui vengono re-iniettati ad ogni cambio capitolo.

7. **window.postMessage bridge**: sn56.x invia richieste IDB via `postMessage` al parent noesis810. Il handler in riga ~3000 deve rimanere attivo per tutta la vita della finestra. Non rimuovere quel listener.

8. **Naming snapshot**: il pattern `noesis-[variant]-[bookTitle]__[chapterTitle]__[YYYYMMDD-HHmmss].html` è usato per re-import da disco. Le regex di `_processSnapshotFiles` dipendono da questo formato esatto.

9. **CSS custom properties biblioteca**: il tema chiaro/scuro è gestito esclusivamente via `--lib-*` variables ridefinite su `.lib-dark`. Non esiste JavaScript coinvolto nel cambio tema biblioteca (solo toggle classe CSS).

10. **ResizeObserver su header**: `updateBookmarksTop()` usa un `ResizeObserver` sull'header per riposizionare la sidebar TOC quando l'header cambia altezza (es: zoom pulsanti). È necessario per prevenire sovrapposizioni.
