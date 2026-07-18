# NOESIS-MAP — Mappa Completa della Basecodice

> **Ultimo aggiornamento:** 2026-07-17
> **Versione di riferimento:** noesis812 (v0.12)
> **Scopo:** Documento di riferimento completo per qualsiasi futura implementazione di codice sul repository noesis-multi.

---

## 1. ARCHITETTURA GENERALE DEL REPOSITORY

```
noesis-multi/
├── 🔷 LIVELLO 1: SITO WEB DI DOCUMENTAZIONE (Cloudflare Pages)
│   ├── index.html                    Landing page (5 lingue via translations.js)
│   ├── style.css                     CSS condiviso per tutte le pagine sito
│   ├── site.js                       JS condiviso (i18n, navigazione, interazioni)
│   ├── translations.js               i18n: EN, IT, FR, ES, DE (~5000 righe)
│   ├── navigation.html               Guida visuale alla menubar/interfaccia
│   ├── guida.html                    Guida utente passo-passo
│   ├── faq.html                      FAQ
│   ├── doc-*.html                    Documentazione tecnica (13 file)
│   ├── library.html / htmleditor.html / bookmark.html / snapshot.html
│   ├── collezioni.html / settings.html / approfondimenti.html
│   ├── promo.html / note.html
│   ├── terms.html / doc-legal.html
│   └── helpers.html                  Tool helper
│
├── 🔷 LIVELLO 2: CODICE APPLICATIVO NOESIS (single-file HTML)
│   ├── noesis812.html                ★ SORGENTE PRIMARIO — Regular (CDN, ~336 KB, 7236 righe)
│   │
│   ├── noesis812-full.html           ★ SORGENTE FULL — Offline (~1.7 MB, 7258 righe)
│   │   │                               Tutte le dipendenze embedded inline.
│   │   │                               È il file da cui derivano reader ed editor.
│   │   │
│   │   ├──[split_noesis.py]──▶ noesis812-full-reader.html   (793 KB, 6865 righe)
│   │   │                       Library + Reader, NO editor, NO snapshot UI
│   │   │
│   │   └──[split_noesis.py]──▶ noesis812-full-editor.html   (871 KB, 4441 righe)
│   │                           Editor sn56 standalone
│   │
│   └── noesis810.html / noesis810-full.html   Versione precedente (ancora presente)
│
├── 🔷 TOOL STANDALONE
│   ├── epubslimer.html / multiepubslimer.html   Riduzione dimensione EPUB
│   ├── epubsplitter.html                         Split EPUB in capitoli
│   └── extractchapter.html                       Estrazione capitoli standalone
│
├── 🔷 DOCUMENTAZIONE OFFLINE (Markdown)
│   ├── DOC1_FUNZIONALITA.md           Feature complete
│   ├── DOC2_WORKFLOW.md               Workflow utente
│   ├── DOC3_CODICE_TECNICO.md         Struttura codice
│   ├── DOC4_SCHEMI_DATI.md            Schema IndexedDB/localStorage
│   ├── DOC5_CSS_GUIDE.md              Guida CSS e temi
│   ├── DOC6_HTML_STRUTTURA.md         Struttura DOM
│   ├── DOC7_PATTERN_ESTENSIONE.md     Pattern estensione
│   ├── DOC8_FULL_EMBEDDING_812.md     Embedding versione Full
│   ├── SPLIT_PLAN.md                  Piano operativo split
│   └── IMPL_I18N_812.md               Guida aggiornamento i18n
│
├── 🔷 CONFIGURAZIONE / BUILD
│   ├── split_noesis.py                Script split (reader + editor dal full)
│   ├── build.sh                       Build script (Cloudflare)
│   ├── package.json                   Metadati
│   ├── wrangler.toml                  Cloudflare Wrangler
│   ├── CLAUDE.md                      Guida per AI assistant
│   ├── README.md                      README principale
│   ├── CHANGELOG.md                   Versioni
│   └── LICENSE                        MIT
```

---

## 2. STRUTTURA INTERNA DI `noesis812.html` (REGULAR, 7236 righe)

> **Nota sugli shift:** le differenze di riga tra Regular e Full non sono uniformi.
> Il blocco Bootstrap Icons embedded occupa ~6 righe contro 1 CDN → shift +6 nel CSS.
> Il blocco sn56Source embedded è più grande → shift negativo nell'HTML.
> JSZip ed epub.js inline sono più lunghi dei CDN → shift +8 nel JS.
> I blocchi interni al JS hanno offset variabili (es. NOESIS_DB_NAME shift +22)
> perché `"use strict"` e i commenti introduttivi occupano spazio diverso.

```
┌──────────────────────────────────────────────────────────────────┐
│  noesis812.html — Versione Regular (CDN)                        │
│  Dipendenze: Bootstrap Icons CDN, JSZip CDN, epub.js CDN        │
│  sn56Source: JSON blob con CDN references                       │
└──────────────────────────────────────────────────────────────────┘

RIGA    CONTENUTO
────    ──────────────────────────────────────────────────────────
1-8     <head> + meta (charset, viewport, no-scale, title)
9       <link> Bootstrap Icons CDN
10-2643 🟦 CSS INLINE (~2634 righe, 36% del file)
        │
        ├── 10-30     Global & Utils (reset, .hidden, flexbox)
        ├── 31-665    Library View (Light/Dark theme, header, grid, cover, meta,
        │             chapters, snapshots, responsive)
        ├── 666-878   Reader View base (header, toolbar, buttons)
        ├── 879-1078  User Bookmarks Drawer (.ubm-*)
        ├── 1079-1137 Extract Chapter Dropdown (.extract-menu)
        ├── 1138-1672 Theme Picker Popup (15 temi, 5 gruppi, swatch)
        ├── 1673-1828 Typography Popup (font size, line height)
        ├── 1829-1958 Save Toast + Media Dialog/Fullscreen
        ├── 1959-2007 ⭐ Display Save Prompt (v812) #displaySavePrompt
        ├── 2008-2078 Reader Highlight Dropdown
        ├── 2078-2251 Tooltip, Banner avvio, Help overlay
        ├── 2252-2411 15 set variabili CSS :root.theme-*
        └── 2412-2643 ⭐ Reader Menubar (v812) .reader-menubar, .rmb-item,
                      .rmb-navigate-menu, .rmb-item-active, responsive
────
2644     </head>
2646     <body>
2648-2653 Loading overlay (#loadingOverlay + spinner)

2655-2834 🟧 LIBRARY VIEW (#library-view)
        ├── 2656-2750  Header (gradiente viola fisso, no variabili tema):
        │              libAddBooksBtn, libImportSnapshotsBtn, libEditorBtn,
        │              libThemesBtn ▾ (Light/Dark), libToolsBtn ▾, libHelpBtn ?
        ├── 2658        #importSnapshotsInput (hidden file input)
        ├── 2660        #libInput (hidden EPUB file input)
        └── 2728        #bookGrid (popolato dinamicamente da JS)

2836-3249 🟧 READER VIEW (#reader-view, hidden)
        ├── 2837-2838  Header compatibilità (hidden)
        ├── 2840-2943  ⭐ nav.reader-menubar (v812) — 8 voci testuali:
        │              Library | TOC | Bookmarks | Display |
        │              Navigate [Page▾] | Annotate | Extract ▾ | Help
        ├── 2844-2845  .toolbar (nascosta, solo compatibilità)
        ├── 3195        #container (sidebar + viewer iframe)
        ├── 3196-3200   #bookmarks (TOC gerarchico)
        ├── 3202-3209   #floatingPrevBtn, #floatingNextBtn
        ├── 3211-3220   #userBookmarksDrawer
        ├── 3222-3225   #status (barra stato)
        ├── 3226-3231   #saveToast
        ├── 3232-3238   ⭐ #displaySavePrompt (v812)
        └── 3239-3249   #readerMediaDialog + #readerMediaFullscreen

3251-3256 🟧 DATI + DIPENDENZE CDN
        ├── 3251-3253  <!-- SN56_SOURCE_START/END --> + sn56Source JSON
        ├── 3255        <script src="jszip CDN">
        └── 3256        <script src="epub.js CDN">

3258-7234 🌿 JAVASCRIPT (~3970 righe, 55% del file)
        │
        ├── 3258-3270  "use strict" + intestazione
        │
        ├── 3271-3350  MODULO noesisDB (~80 righe)
        │   ├── 3271-3273  Costanti: NOESIS_DB_NAME='noesisDB', v1, store='chapters'
        │   ├── 3275-3290  openNoesisDB()
        │   ├── 3291-3301  saveExtractedChapterToDB(record)
        │   ├── 3302-3312  deleteExtractedChapterFromDB(chapterId)
        │   ├── 3313-3319  deleteSnapshotFromDB(chapterId, snapshotId)
        │   ├── 3320-3329  getExtractedChapterFromDB(chapterId)
        │   └── 3331-3350  IDB BRIDGE — postMessage handler (serve blob:null windows)
        │
        ├── 3354-3478  MODULO mainDB / EpubLibraryDB (~125 righe)
        │   ├── 3354-3356  Costanti: DB_NAME='EpubLibraryDB', v1, store='books'
        │   ├── 3359-3398  openDB()
        │   ├── 3399-3448  saveBookToDB(bookData) — salva EPUB ArrayBuffer + metadata
        │   ├── 3450-3461  getAllBooks()
        │   └── 3462-3478  deleteBook(bookId) — cascata su noesisDB
        │
        ├── 3480-4042  CORE UI (~560 righe)
        │   ├── 3480-3493  Variabili view globali, showLoading(), hideLoading()
        │   ├── 3495-3538  showLibrary()
        │   ├── 3539-3560  showReader(bookData)
        │   ├── 3545-3560  getAllExtractedChapters()
        │   ├── 3561-3576  _openSn56(payload) — JSON.parse sn56Source → Blob URL → window.open()
        │   ├── 3577-3620  _generateCleanHTML(), _buildExtractionTimestamp(), _autoDownloadHTML()
        │   ├── 3621-3642  _openExtractedEnv(chapterRecord, snapshotId)
        │   ├── 3643-3808  loadLibraryBooks() — renderizza griglia + capitoli + snapshot
        │   ├── 3812-3932  importSnapshotsFromDisk(), _processSnapshotFiles()
        │   └── 3933-4042  openBookFromLibrary(bookData)
        │
        ├── 4044-4431  STATO GLOBALE READER (~390 righe)
        │   ├── 4044-4061  Variabili: book, rendition, fontSize, lineHeight,
        │   │              scrollMode, dualPageMode, currentTheme, currentLocation,
        │   │              buttonZoom, _autoSaveTimer, _lastAutoSavedCfi, _dspTimer
        │   ├── 4064-4079  interfaceSettings + defaultInterfaceSettings
        │   ├── 4081-4089  currentBookId, currentBookTitle, readerHighlights[],
        │   │              currentReaderHighlightColor, _readerPendingCfi, HL_COLORS
        │   ├── 4092-4107  showToast(msg)
        │   ├── 4108-4139  _getCenterCfi() — CFI elemento al centro visivo
        │   ├── 4140-4148  _snapshotVisualState()
        │   ├── 4149-4182  savePositionOnly() — salva CFI in IDB
        │   ├── 4183-4220  saveVisualSettings() — salva tema/font/layout
        │   ├── 4221-4241  startAutoSave() — setInterval 3 sec
        │   ├── 4242-4252  stopAutoSave()
        │   ├── 4253-4273  _isBrowserTranslated(), _showDisplaySavePrompt(),
        │   │              _hideDisplaySavePrompt()
        │   ├── 4281-4346  saveBookState(), loadAndApplyBookState()
        │   ├── 4347-4411  setStatus(), updateFontInfo(), updateLineHeightInfo(),
        │   │              applyInterfaceSettings()
        │   └── 4412-4431  hexToRgba(), adjustColor(), navigateToHref()
        │
        ├── 4432-5091  ESTRAZIONE CAPITOLI (~660 righe)
        │   ├── 4432-4622  navigateToHref(), collectAllSubchapters() — ricorsione TOC
        │   ├── 4623-4879  extractMultipleSections() — capitolo + sottocapitoli
        │   └── 4880-5091  extractCurrentChapter() — solo capitolo corrente
        │
        ├── 5092-5504  TEMI + RENDITION (~410 righe)
        │   ├── 5200-5224  THEME_COLORS (15 oggetti: bg, color, header, toolbar, iframe)
        │   ├── 5225-5231  THEME_GROUPS (white, sepia, light gray, medium gray, black)
        │   ├── 5231-5306  applyTheme(), updateThemeSwatchActive(), buildThemePopup()
        │   └── 5307-5504  recreateRendition() — ricostruzione completa epub.js
        │
        ├── 5505-5856  TOC + SEGNALIBRI (~350 righe)
        │   ├── 5505-5598  findBreadcrumbInToc(), renderBookmarksSimple()
        │   ├── 5600        let userBookmarks = []
        │   ├── 5603-5652  saveUserBookmarksToDB(), loadUserBookmarksFromDB()
        │   ├── 5653-5741  renderUbmList()
        │   ├── 5742-5845  createUserBookmark() — CFI + label + anteprima
        │   └── 5846-5856  openUbmDrawer(), closeUbmDrawer()
        │
        ├── 5857-6692  EVENT HANDLERS (~835 righe)
        │   ├── Highlight (mouseup), media click, keyboard shortcuts
        │   ├── Toolbar: prev/next page, TOC toggle, scroll, dual page
        │   ├── Estrazione: dropdown Extract, font ±, line height, temi
        │   ├── Bookmark: drawer, nuovo, elimina, naviga
        │   ├── Display prompt: salva/dismiss, media dialog, stampa
        │   ├── Library: open/delete book, click capitolo/snapshot
        │   └── Import libri, import snapshot, open editor standalone
        │
        ├── 6693-6872  MENUBAR + INIZIALIZZAZIONE (~180 righe)
        │   ├── 6693-6841  Event delegation globale document.addEventListener
        │   │              Gestione menubar (.rmb-item click), highlight mode,
        │   │              Navigate dropdown, Annotate toggle
        │   ├── 6805-6841  Library tools dropdown, chiusura menu click esterno
        │   ├── 6846        _closeAllReaderMenus() — chiude TUTTI i menu aperti
        │   └── 6842-6872  document.addEventListener('DOMContentLoaded', ...)
        │                  Inizializzazione: carica libri, ripristina tema
        │
        └── 6873-7234  HANDLER FINALI (~360 righe)
            ├── 6873-6989  ⭐ Navigate Menubar: dropdown Page/Scroll, badge,
            │              shortcut tastiera, highlight mode, Extract dropdown,
            │              Display panel, Help overlay
            ├── 6990-7001  Editor Report help system
            ├── 7002-7204  Handler: Import Snapshots IIFE, Open Editor IIFE,
            │              Help overlay library, cleanup
            └── 7205-7234  ⭐ Stampa multi-pagina (v812):
                           window.addEventListener('beforeprint', ...)
                           window.addEventListener('afterprint', ...)
                           Gestisce #reader-print-container
                           (corregge il bug v810: stampava solo 1 pagina)
────
7235-7236 </body></html>
```

---

## 3. STRUTTURA INTERNA DI `noesis812-full.html` (FULL, 7258 righe)

```
┌──────────────────────────────────────────────────────────────────┐
│  noesis812-full.html — Versione Fully-Offline                   │
│  ZERO dipendenze CDN. Tutto embedded inline.                     │
│  CSS + HTML + JS bit-identici alla Regular dopo la riga 15.     │
└──────────────────────────────────────────────────────────────────┘

RIGA    CONTENUTO                                   DIFFERENZA vs REGULAR
────    ──────────────────────────────────────────  ───────────────────────
1-7     Doctype, <html>, <head>, meta              IDENTICO
8-14    🟦 <style> Bootstrap Icons CSS + font       ★ EMBEDDED
        @font-face { src: url("data:font/woff2;base64,...") }
        + tutte le classi .bi-*
        (~259 KB)                                   Regular: <link CDN>

15-2640 🟦 CSS applicativo principale               IDENTICO alla Regular
        Stessi commenti, stesse sezioni,
        stesse regole v812 (menubar, display prompt, print)

2641-3240 🟧 HTML strutturale                       IDENTICO alla Regular
        Library header, Reader menubar,
        Drawer, Toast, Display prompt, Media dialog

3241-3259 ⬜ SN56SOURCE BLOCK                        ★ EMBEDDED (no CDN refs)
        <!-- SN56_SOURCE_START -->                  (~912 KB)
        <script type="application/json" id="sn56Source">
          [JSON con HTML editor completo,
           tutte le dipendenze editor embedded]
        <!-- SN56_SOURCE_END -->                    Regular: JSON con CDN refs

3245-3263 🟩 <script> JSZip v3.10.1 inline          ★ EMBEDDED (~97 KB)
                                                   Regular: <script src="CDN">

3264-3265 🟩 <script> epub.js v0.3.93 inline         ★ EMBEDDED (~224 KB)
                                                   Regular: <script src="CDN">

3266-7256 🌿 JS applicativo Noesis                   IDENTICO alla Regular
        Stesse funzioni, stesse variabili,
        stessa logica. Bit-identical.
────
7257-7258 </body></html>
```

### RIEPILOGO DIFFERENZE REGULAR vs FULL

| Blocco | Regular (righe) | Full (righe) | Differenza |
|--------|-----------------|--------------|------------|
| Bootstrap Icons | CDN link (riga 9) | CSS inline + base64 font (8-14) | EMBEDDED |
| CSS applicativo | 10-2643 | 15-2640 | Identico, shift +6 |
| HTML strutturale | 2646-3249 | 2642-3240 | Identico, shift -4 |
| sn56Source | JSON con CDN refs | JSON con dipendenze embedded | EMBEDDED |
| JSZip | `<script src="CDN">` (3255) | `<script>` inline (3245-3263) | EMBEDDED |
| epub.js | `<script src="CDN">` (3256) | `<script>` inline (3264-3265) | EMBEDDED |
| JS applicativo | 3258-7234 | 3266-7256 | Identico, shift +8 |

---

## 4. MAPPA DELLE VARIABILI GLOBALI

### 4.1 Modulo noesisDB (IndexedDB: `noesisDB`)

| Variabile | Riga (Reg) | Riga (Full) | Tipo | Descrizione |
|-----------|-----------|-------------|------|-------------|
| `NOESIS_DB_NAME` | 3271 | 3293 | const | `'noesisDB'` |
| `NOESIS_DB_VERSION` | 3272 | 3294 | const | `1` |
| `NOESIS_STORE` | 3273 | 3295 | const | `'chapters'` |

**Store: `chapters`** — keyPath: `chapterId`
Record: `{ chapterId, bookName, chapterName, createdAt, snapshots: [{snapshotId, createdAt, description, content, isOrigin}] }`

### 4.2 Modulo mainDB / EpubLibraryDB (IndexedDB: `EpubLibraryDB`)

| Variabile | Riga (Reg) | Riga (Full) | Tipo | Descrizione |
|-----------|-----------|-------------|------|-------------|
| `DB_NAME` | 3354 | 3376 | const | `'EpubLibraryDB'` |
| `DB_VERSION` | 3355 | 3377 | const | `1` |
| `STORE_NAME` | 3356 | 3378 | const | `'books'` |

**Store: `books`** — keyPath: `bookId`
Record: `{ bookId, title, author, coverBase64, data (ArrayBuffer EPUB), highlights: [{cfi, color}], userBookmarks: [{cfi, label, timestamp, chapterName, textPreview}], readingState: { cfi, fontSize, lineHeight, scrollMode, dualPageMode, currentTheme, interfaceSettings } }`

### 4.3 Core UI — Variabili globali view

| Variabile | Riga (Reg) | Riga (Full) | Descrizione |
|-----------|-----------|-------------|-------------|
| `libraryView` | 3480 | 3502 | DOM element `#library-view` |
| `readerView` | 3481 | 3503 | DOM element `#reader-view` |
| `bookGrid` | 3482 | 3504 | DOM element `#bookGrid` |
| `loadingOverlay` | 3483 | 3505 | DOM element `#loading-overlay` |
| `loadingMsg` | 3484 | 3506 | DOM element `#loading-msg` |

### 4.4 Reader State — Variabili globali

| Variabile | Riga (Reg) | Riga (Full) | Tipo | Default | Descrizione |
|-----------|-----------|-------------|------|---------|-------------|
| `book` | 4044 | 4066 | let | `null` | Istanza epub.js |
| `rendition` | 4045 | 4067 | let | `null` | Istanza rendition epub.js |
| `fontSize` | 4046 | 4068 | let | `16` | Font size px |
| `lineHeight` | 4047 | 4069 | let | `1.5` | Line height |
| `lineHeights` | 4048 | 4070 | let | `[1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0]` |
| `scrollMode` | 4049 | 4071 | let | `false` | false=paginato, true=scroll |
| `dualPageMode` | 4050 | 4072 | let | `false` | false=single, true=dual (solo paginato) |
| `sidebarVisible` | 4051 | 4073 | let | `true` | TOC sidebar visibile |
| `currentTheme` | 4052 | 4074 | let | `'dayWhite'` | ID tema attivo |
| `currentLocation` | 4053 | 4075 | let | `null` | Ultima posizione CFI |
| `buttonZoom` | 4054 | 4076 | let | `1` | Scala pulsanti toolbar (0.6–1.5) |
| `_autoSaveTimer` | 4057 | 4079 | let | `null` | ID setInterval auto-save |
| `_lastAutoSavedCfi` | 4058 | 4080 | let | `null` | Ultimo CFI salvato |
| `_lastNavigatedCfi` | 4059 | 4081 | let | `null` | CFI destinazione navigazione |
| `_lastSavedVisualState` | 4060 | 4082 | let | `null` | Snapshot stato visuale |
| `_dspTimer` | 4061 | 4083 | let | `null` | Timer auto-hide prompt |
| `interfaceSettings` | 4064 | 4086 | let | `{...}` | Impostazioni interfaccia correnti |
| `currentBookId` | 4081 | 4103 | let | `null` | ID libro corrente in IDB |
| `currentBookTitle` | 4082 | 4104 | let | `''` | Titolo libro corrente |
| `readerHighlights` | 4085 | 4107 | let | `[]` | Highlight array `[{cfi, color}]` |
| `currentReaderHighlightColor` | 4086 | 4108 | let | `'yellow'` | Colore highlight attivo |
| `HL_COLORS` | 4087 | 4109 | const | `['yellow','green','pink']` |
| `_readerHlHasSelection` | 4088 | 4110 | let | `false` | Flag selezione attiva |
| `_readerPendingCfi` | 4089 | 4111 | let | `null` | CFI pending per highlight |
| `userBookmarks` | 5600 | 5622 | let | `[]` | Array segnalibri utente |
| `THEME_COLORS` | 5200 | 5222 | const | `[...15]` | 15 definizioni tema |
| `THEME_GROUPS` | 5225 | 5247 | const | `[...5]` | 5 gruppi temi |

### 4.5 Default settings

```javascript
// interfaceSettings default (riga ~4072 Reg / ~4094 Full)
const defaultInterfaceSettings = {
  toolbarItemScale: 1.0,
  navButtonScale: 1.0,
  readerBgColor: '#ffffff',
  readerTextColor: '#1a1a1a',
  readerLinkColor: '#2563eb'
};
```

---

## 5. MAPPA DELLE FUNZIONI PRINCIPALI

### 5.1 Database (noesisDB)

| Funzione | Riga (Reg) | Firma | Descrizione |
|----------|-----------|-------|-------------|
| `openNoesisDB` | 3275 | `async ()` | Apre/crea `noesisDB` |
| `saveExtractedChapterToDB` | 3291 | `async (record)` | Salva chapterRecord |
| `deleteExtractedChapterFromDB` | 3302 | `async (chapterId)` | Elimina capitolo |
| `deleteSnapshotFromDB` | 3313 | `async (chapterId, snapshotId)` | Elimina snapshot |
| `getExtractedChapterFromDB` | 3320 | `async (chapterId)` | Recupera record |
| `getAllExtractedChapters` | 3545 | `async ()` | Recupera TUTTI i capitoli (rimossa nel reader) |

### 5.2 Database (EpubLibraryDB)

| Funzione | Riga (Reg) | Firma | Descrizione |
|----------|-----------|-------|-------------|
| `openDB` | 3359 | `async ()` | Apre/crea `EpubLibraryDB` |
| `saveBookToDB` | 3399 | `async (bookData)` | Salva EPUB + metadata |
| `getAllBooks` | 3450 | `async ()` | Recupera tutti i libri |
| `deleteBook` | 3462 | `async (bookId)` | Elimina libro + capitoli associati |

### 5.3 Core UI

| Funzione | Riga (Reg) | Firma | Descrizione |
|----------|-----------|-------|-------------|
| `showLoading` | 3486 | `(msg)` | Mostra overlay caricamento |
| `hideLoading` | 3491 | `()` | Nasconde overlay |
| `showLibrary` | 3495 | `()` | Transizione a library-view |
| `showReader` | 3539 | `(bookData)` | Transizione a reader-view |
| `loadLibraryBooks` | 3643 | `async ()` | Renderizza griglia libri (versione completa: +capitoli+snapshot) |
| `openBookFromLibrary` | 3933 | `async (bookData)` | Carica EPUB da IDB → reader |

### 5.4 Editor / sn56

| Funzione | Riga (Reg) | Descrizione |
|----------|-----------|-------------|
| `_openSn56` | 3561 | Estrae JSON sn56Source, inietta payload, crea Blob URL, window.open() |
| `_generateCleanHTML` | 3577 | Rimuove background-color inline dall'HTML |
| `_buildExtractionTimestamp` | 3599 | Costruisce timestamp per nome file |
| `_autoDownloadHTML` | 3610 | Scarica file HTML via Blob + anchor click |
| `_openExtractedEnv` | 3621 | Apre capitolo/snapshot esistente nell'editor |

### 5.5 Snapshot / Import

| Funzione | Riga (Reg) | Descrizione |
|----------|-----------|-------------|
| `importSnapshotsFromDisk` | 3812 | Importa snapshot HTML da filesystem |
| `_processSnapshotFiles` | 3844 | Processa i file selezionati, legge meta tag |

### 5.6 Reader State

| Funzione | Riga (Reg) | Descrizione |
|----------|-----------|-------------|
| `showToast` | 4092 | Toast temporaneo |
| `_getCenterCfi` | 4108 | CFI dell'elemento al centro del reader |
| `_snapshotVisualState` | 4140 | Cattura stato visivo corrente |
| `savePositionOnly` | 4149 | Salva CFI in IDB |
| `saveVisualSettings` | 4183 | Salva impostazioni Display in IDB |
| `startAutoSave` | 4221 | Avvia timer 3 secondi per auto-save CFI |
| `stopAutoSave` | 4242 | Ferma timer auto-save |
| `_showDisplaySavePrompt` | 4261 | Mostra banner "Salva impostazioni?" |
| `saveBookState` | 4281 | Salva tutto lo stato del libro |
| `loadAndApplyBookState` | 4295 | Ripristina stato salvato |
| `applyInterfaceSettings` | 4383 | Applica impostazioni interfaccia al DOM |
| `updateFontInfo` | 4374 | Aggiorna display font size |
| `updateLineHeightInfo` | 4378 | Aggiorna display line height |
| `navigateToHref` | 4432 | Naviga a un href nella TOC |

### 5.7 Estrazione

| Funzione | Riga (Reg) | Descrizione |
|----------|-----------|-------------|
| `collectAllSubchapters` | 4623 | Ricorsione TOC per raccogliere sottocapitoli |
| `extractMultipleSections` | 4634 | Estrae capitolo + tutti i sottocapitoli |
| `extractCurrentChapter` | 4880 | Estrae solo il capitolo corrente |

### 5.8 Temi

| Funzione | Riga (Reg) | Descrizione |
|----------|-----------|-------------|
| `applyTheme` | 5231 | Applica tema di lettura (CSS variables) |
| `updateThemeSwatchActive` | 5257 | Aggiorna UI swatch attivo |
| `buildThemePopup` | 5265 | Costruisce HTML del popup temi |
| `recreateRendition` | 5307 | Ricostruzione completa rendition dopo cambio layout |

### 5.9 TOC / Segnalibri

| Funzione | Riga (Reg) | Descrizione |
|----------|-----------|-------------|
| `findBreadcrumbInToc` | 5516 | Breadcrumb nella TOC |
| `renderBookmarksSimple` | 5534 | Renderizza TOC gerarchico |
| `saveUserBookmarksToDB` | 5603 | Persiste bookmarks in IDB |
| `loadUserBookmarksFromDB` | 5631 | Carica bookmarks da IDB |
| `renderUbmList` | 5653 | Renderizza lista bookmark nel drawer |
| `createUserBookmark` | 5742 | Crea nuovo bookmark (CFI + label + preview) |
| `openUbmDrawer` | 5846 | Apre drawer bookmark |
| `closeUbmDrawer` | 5857 | Chiude drawer bookmark |

---

## 6. FLUSSI DATI PRINCIPALI

### 6.1 Flusso: Import EPUB → Library

```
User click "Add Books"
  → input[type=file] click()
  → FileReader.readAsArrayBuffer(file)
  → JSZip per estrarre cover image
  → saveBookToDB({title, author, coverBase64, data: ArrayBuffer})
  → loadLibraryBooks() → render book grid
```

### 6.2 Flusso: Apri Libro → Reader

```
User click book cover
  → openBookFromLibrary(bookData)
  → recupera ArrayBuffer da IDB
  → book = ePub(bookData.data)
  → rendition = book.renderTo("viewer", {width, height})
  → startAutoSave() — timer 3 sec
  → loadAndApplyBookState() — ripristina posizione, tema, font
  → renderBookmarksSimple() — TOC gerarchico
  → loadUserBookmarksFromDB()
```

### 6.3 Flusso: Estrai Capitolo → Editor

```
User click Extract (menubar)
  → extractCurrentChapter() o extractMultipleSections()
  → Estrae HTML dall'iframe del reader
  → _generateCleanHTML() — rimuove bg-color
  → saveExtractedChapterToDB({chapterId, bookName, chapterName, snapshots:[origin]})
  → _autoDownloadHTML() — scarica file clean + annot
  → _openSn56({mode:'chapter', bookName, chapterName, chapterId, htmlContent})
    → JSON.parse(sn56Source) — estrae HTML editor
    → Inietta payload come <script id="noesisPayload">
    → Blob URL → window.open()
```

### 6.4 Flusso: Auto-Save Posizione

```
startAutoSave() — chiamato all'apertura libro
  → setInterval(async () => {
      if (!_isBrowserTranslated()) {  // non salva durante traduzione
        const cfi = _getCenterCfi();  // elemento al centro visivo
        if (cfi !== _lastAutoSavedCfi) {
          savePositionOnly(cfi);
          _lastAutoSavedCfi = cfi;
        }
      }
    }, 3000);
```

### 6.5 Flusso: Salva Impostazioni Display

```
User modifica tema/font/layout nel pannello Display
User chiude il pannello Display
  → _showDisplaySavePrompt() — banner floating per 8 secondi
  → Se user clicca "Save":
    → saveVisualSettings() → salva in IDB
  → Se user ignora o clicca "Dismiss":
    → nessuna azione
```

### 6.6 Flusso: Highlight

```
User seleziona testo nel reader
  → mouseup event → _readerPendingCfi = selection.cfiRange
  → Se Annotate mode è attivo:
    → Aggiunge/rimuove highlight con colore corrente
    → readerHighlights.push({cfi, color})
    → Salva highlights nel record libro in EpubLibraryDB
```

---

## 7. DIPENDENZE ESTERNE

### 7.1 Versione Regular (CDN)

| Libreria | Versione | URL | Peso |
|----------|----------|-----|------|
| Bootstrap Icons | 1.11.3 | `cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css` | ~259 KB |
| JSZip | 3.10.1 | `cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js` | ~97 KB |
| epub.js | 0.3.93 | `cdn.jsdelivr.net/npm/epubjs@0.3.93/dist/epub.min.js` | ~224 KB |

### 7.2 Dipendenze Editor sn56 (nel blob)

| Libreria | Contesto |
|----------|----------|
| jQuery 3.7.1 | Necessario per Summernote |
| Summernote 0.9.1 (CSS + JS + font) | Editor WYSIWYG |
| Bootstrap Icons 1.11.3 (CSS + font) | Icone nella toolbar |
| Turndown (latest) | Export Markdown |
| html-docx-js (latest) | Export DOCX |
| JSZip (latest) | Export MD+ZIP con immagini |
| Excalidraw | Diagrammi (caricato da URL esterno) |

### 7.3 Ordine di caricamento OBBLIGATORIO

```
1. Bootstrap Icons CSS  (deve essere parsato prima del DOM)
2. JSZip                (DEVE precedere epub.js — epub.js UMD fa require("JSZip"))
3. epub.js              (usa window.JSZip come globale)
4. Codice applicativo   (usa ePub e JSZip come globali)
```

---

## 8. PATTERN JAVASCRIPT

### 8.1 Convenzioni

- **No modules**: tutto in scope globale, dentro `<script>` inline
- **`"use strict"`** alla prima riga JS (riga 3258 Reg / 3266 Full)
- **Event delegation**: un singolo `document.addEventListener('click', ...)` con check `e.target.closest()`
- **Stato globale esplicito**: tutte le variabili di stato sono `let` a livello file
- **Async/await** per tutte le operazioni IndexedDB e file
- **DOM manipulation pura**: `getElementById`, `innerHTML`, `classList`, `classList.add/remove/toggle`

### 8.2 Naming convention

| Tipo | Pattern | Esempio |
|------|---------|---------|
| Costanti DB | `UPPER_SNAKE` | `NOESIS_DB_NAME`, `DB_VERSION` |
| Variabili globali | `camelCase` | `currentTheme`, `scrollMode` |
| Funzioni pubbliche | `camelCase` | `openBookFromLibrary()` |
| Funzioni private | `_underscorePrefix` | `_openSn56()`, `_getCenterCfi()` |
| Elementi DOM | `camelCase` | `libraryView`, `bookGrid` |
| ID HTML/DOM | `camelCase` | `readerView`, `displaySavePrompt` |
| Classi CSS | `kebab-case` | `.reader-menubar`, `.lib-header-btn` |
| Store IDB | `pluralNoun` | `books`, `chapters` |

### 8.3 Commenti marcatore OBBLIGATORI (non rimuovere)

```html
<!-- SN56_SOURCE_START -->       ← delimita inizio blocco sn56Source
<script type="application/json" id="sn56Source">...</script>
<!-- SN56_SOURCE_END -->         ← delimita fine blocco sn56Source
```

```javascript
// ── IDB bridge: serve requests from child windows (blob:null context) ──
...
// ── END IDB bridge ────────────────────────────────────────────────────
```

```javascript
// ── Apri sn56.x con payload ──
_openSn56({ ... });
```

Questi marcatori sono usati da `split_noesis.py` per le operazioni di split. Se modificati, lo script di split si rompe.

---

## 9. PERSISTENZA DATI — Schema Completo

### 9.1 IndexedDB: `EpubLibraryDB` (DB_NAME)

```
Database: EpubLibraryDB v1
Store: books (keyPath: "bookId")

Record:
{
  bookId: string,              // generato: 'book_' + timestamp
  title: string,               // da metadata EPUB
  author: string,              // da metadata EPUB
  coverBase64: string|null,    // copertina come data URI (opzionale)
  data: ArrayBuffer,           // file EPUB completo
  highlights: [                // highlight nel reader
    { cfi: string, color: 'yellow'|'green'|'pink' }
  ],
  userBookmarks: [             // segnalibri utente (v812)
    {
      cfi: string,
      label: string,
      timestamp: string,       // ISO 8601
      chapterName: string,
      textPreview: string      // prime ~100 lettere del testo
    }
  ],
  readingState: {              // stato lettura (v812: auto-save + display prompt)
    cfi: string|null,          // ultima posizione
    fontSize: number,          // px (default 16)
    lineHeight: number,        // (default 1.5)
    scrollMode: boolean,       // false=paginato, true=scroll
    dualPageMode: boolean,     // false=single, true=dual
    currentTheme: string,      // ID tema (default 'dayWhite')
    interfaceSettings: {
      toolbarItemScale: number,   // 0.6–1.5
      navButtonScale: number,     // 0.6–1.5
      readerBgColor: string,      // hex
      readerTextColor: string,    // hex
      readerLinkColor: string     // hex
    },
    lastSaved: string          // ISO 8601
  }
}
```

### 9.2 IndexedDB: `noesisDB` (NOESIS_DB_NAME)

```
Database: noesisDB v1
Store: chapters (keyPath: "chapterId")

Record:
{
  chapterId: string,           // generato: 'ch_' + timestamp
  bookName: string,
  chapterName: string,
  createdAt: string,           // ISO 8601
  snapshots: [
    {
      snapshotId: string,      // 'snap_' + timestamp + '_' + random
      createdAt: string,       // ISO 8601
      bookName: string,
      chapterName: string,
      description: string,     // es: 'annot-20260422-143022-mia-etichetta'
      content: string,         // HTML completo del documento
      isOrigin: boolean        // true solo per il primo snapshot automatico
    }
  ]
}
```

### 9.3 localStorage

| Chiave | Tipo | Default | Descrizione |
|--------|------|---------|-------------|
| `noesisLibraryTheme` | `'light'\|'dark'` | `'light'` | Tema library |
| `noesisDefaultFontSize` | `number` | `16` | Font size predefinito |
| `noesisDefaultLineHeight` | `number` | `1.5` | Line height predefinito |
| `noesisHelpBannerDismissed` | `boolean` | `false` | Banner help library dismissed |
| `noesisReaderHelpDismissed` | `boolean` | `false` | Banner help reader dismissed |

### 9.4 File scaricati (naming convention)

```
Pattern: noesis-{TYPE}-{BOOKNAME}__{CHAPTERNAME}__{YYYYMMDD_HHMMSS}_{CUSTOM}.html

Tipi:
  clean-*    → senza background-color (per import pulito)
  annot-*    → con tutti gli highlight preservati
  origin-*   → primo snapshot automatico dopo estrazione

Meta tag nel file:
  <meta name="noesis-chapter-id" content="...">
  <meta name="noesis-book-name" content="...">
  <meta name="noesis-chapter-name" content="...">
  <meta name="noesis-snapshot-variant" content="clean|annot">
```

---

## 10. ARCHITETTURA VISTE

### 10.1 Due viste principali (toggle show/hide)

```
#library-view          → display: flex (default visibile)
#reader-view           → display: none + class .hidden

Transizione:
  showLibrary() → readerView.classList.add('hidden'), libraryView.classList.remove('hidden')
  showReader()  → libraryView.classList.add('hidden'), readerView.classList.remove('hidden')
```

### 10.2 Terzo ambiente: Editor sn56 (finestra separata)

```
APERTURA:
  1. JSON.parse(document.getElementById('sn56Source').textContent)
  2. Inietta payload come <script id="noesisPayload"> nel HTML estratto
  3. Blob URL → window.open('', '_blank')

COMUNICAZIONE:
  - Editor → Parent: postMessage({__noesisIDB: true, op, payload}, '*')
  - Parent ascolta: window.addEventListener('message', ...)
  - Opera su noesisDB (get/put chapter records)
  - Timeout 8 secondi per richiesta
```

---

## 11. TEMI DI LETTURA (15 temi, 5 gruppi)

```
Gruppo 1: WHITE
  dayWhite, daySolarized, nightWhite

Gruppo 2: CREAM/SEPIA
  creamClassic, creamWarm, sepiaVintage

Gruppo 3: LIGHT GRAY
  graySilver, grayCool, grayLavender

Gruppo 4: MEDIUM GRAY
  grayCharcoal, graySlate, grayGraphite

Gruppo 5: DARK/BLACK
  darkNavy, darkObsidian, darkAmoled
```

Ogni tema definisce: `bg`, `color`, `headerBg`, `headerColor`, `toolbarBg`, `toolbarColor`, `iframeBg`, `linkColor`, `borderColor`

---

## 12. FEATURE TRASVERSALI

### 12.1 Stampa Multi-Pagina (v812)

**Righe:** CSS 2626-2640, JS 7205-7234 (Reg) / CSS 2632-2640, JS 7227-7256 (Full)

**Elementi:** `#reader-print-container` — contenitore nascosto, visibile solo in `@media print`

**Flusso:**
```
window.addEventListener('beforeprint', ...)
  → Cattura TUTTO il contenuto dall'iframe del reader
  → Lo inietta in #reader-print-container
  → Mostra #reader-print-container, nasconde tutto il resto

window.addEventListener('afterprint', ...)
  → Ripristina la visibilità normale
  → Svuota #reader-print-container
```

Questo fix risolve il bug della v810 dove la stampa catturava solo la prima pagina del capitolo.

### 12.2 Traduzione Browser

**Righe:** `_isBrowserTranslated()` a 4253 (Reg) / 4275 (Full)

Noesis usa il **motore di traduzione integrato del browser** (Google Translate nei Chromium, DeepL in altri). Nessuna API esterna.

**Due modalità:**
- **Reader — streaming translation**: la traduzione nativa del browser scorre con la lettura. L'auto-save della posizione (`startAutoSave`) viene **sospeso** se `_isBrowserTranslated()` restituisce `true`, per evitare corruzione dei CFI (i nodi DOM vengono sostituiti dal traduttore).
- **Editor — one-shot translation**: traduzione dell'intera sezione con un comando singolo.

**Rilevamento traduzione attiva:**
```javascript
function _isBrowserTranslated() {
  // Verifica se il DOM dell'iframe è stato modificato dal traduttore
  const iframeDoc = document.querySelector('#viewer iframe')?.contentDocument;
  if (!iframeDoc) return false;
  return !!iframeDoc.querySelector('font[style*="vertical-align"]');
}
```

### 12.3 Excalidraw (Editor)

L'editor sn56 integra **Excalidraw** come tab dedicato per diagrammi, flowchart e mappe mentali.

- **Accesso:** pulsante dedicato nella toolbar dell'editor
- **Caricamento:** da URL esterno (`noesis-excalidraw.vercel.app`)
- **Export:** SVG e PNG
- **Riga CSS riferimento:** `.tb-btn-excalidraw` (~riga 894 Reg)

### 12.4 Keyboard Shortcuts

| Shortcut | Contesto | Azione | Riga (Reg) |
|----------|----------|--------|------------|
| `?` | Globale (non in input/textarea) | Apre Help overlay | 6762 |
| `Escape` | Globale | Chiude Help overlay, drawer, menu aperti | ~6846 |
| `←` / `→` | Reader (non in input) | Pagina precedente/successiva | ~5900 |
| `Escape` | Help overlay aperto | Chiude l'overlay | ~6762 |

### 12.5 _closeAllReaderMenus()

**Riga:** 6846 (Reg) / 6868 (Full)

Funzione di utilità chiamata da tutti gli handler della menubar per garantire che **un solo menu/dropdown sia aperto alla volta**:

```javascript
function _closeAllReaderMenus() {
  // Chiude dropdown Navigate (Page/Scroll)
  // Chiude dropdown Extract
  // Chiude pannello Display
  // Chiude pannello Annotate
  // Reset dello stato dei pulsanti toggle
}
```

Chiamata in cima a ogni handler di click sulla menubar, prima di aprire il menu richiesto.

---

## 13. MAPPA VARIANTI DERIVATE

### 13.1 `noesis812-full-reader.html` (6865 righe, 793 KB)

```
RIGA    CONTENUTO
────    ──────────────────────────────────────────────────────────
1-7     Doctype, <head>, meta
8-14    Bootstrap Icons CSS + font base64 (EMBEDDED, ~259 KB)
15-2640 CSS applicativo (← 6 classi .snapshot-* RIMOSSE da split)
2641-3240 HTML strutturale (← 3 pulsanti header RIMOSSI:
        importSnapshotsInput, libImportSnapshotsBtn, libEditorBtn)
3241-3244 JSZip v3.10.1 inline
3245-3246 epub.js v0.3.93 inline
3247-6863 JS applicativo (← funzioni rimosse: _openSn56,
        _openExtractedEnv, getAllExtractedChapters,
        importSnapshotsFromDisk, _processSnapshotFiles;
        ← IDB bridge rimosso;
        ← loadLibraryBooks() semplificata: solo libri, no capitoli/snapshot;
        ← IIFE Import Snapshots + Open Editor rimosse)
        ✅ Funzioni di estrazione PRESERVATE:
        extractCurrentChapter, extractMultipleSections,
        saveExtractedChapterToDB (salva ma non mostra in library)
6864-6865 </body></html>
```

### 13.2 `noesis812-full-editor.html` (4441 righe, 871 KB)

```
RIGA    CONTENUTO
────    ──────────────────────────────────────────────────────────
1       <!DOCTYPE html>
2-4441  <html lang="it"> — Documento HTML COMPLETO e autonomo
        │
        ├── <head>
        │   ├── Summernote CSS + font base64 (EMBEDDED)
        │   ├── Bootstrap Icons CSS + font base64 (EMBEDDED)
        │   └── CSS personalizzato (toolbar bottom, inspect panel, chunk collection)
        │
        ├── <body>
        │   ├── Header (#appHeader) con titolo dinamico
        │   ├── Help overlay (#editorHelpOverlay)
        │   ├── #editor-container → Summernote WYSIWYG
        │   ├── Bottom toolbar (#bottom-toolbar)
        │   │   ├── Chapter section: New, Import, Export, More
        │   │   ├── Collection section: +Add, Import, Export, More, Inspect, Clear
        │   │   └── Tools section: Excalidraw
        │   ├── Inspect panel (draggable, resizable, non-modal)
        │   ├── Import chapter dialog
        │   └── Fullscreen chunk overlay
        │
        └── <script>
            ├── jQuery (inline, EMBEDDED)
            ├── Summernote JS (inline, EMBEDDED)
            ├── JSZip (inline, EMBEDDED)
            ├── Turndown (inline, EMBEDDED)
            ├── html-docx-js (inline, EMBEDDED)
            ├── initEditor() — boot Summernote
            ├── Export: TXT, MD, MD+ZIP, JSON, PDF, DOCX, HTML
            ├── Chapter snapshot: dual clean+annot, IDB bridge
            ├── Chunk collection con inspect panel
            ├── Dropdown management
            └── IDB bridge (postMessage al parent per noesisDB)
4441    </html>
```

---

## 14. COMANDI UTILI

```bash
# Eseguire split
cd /home/vigliafg/Documenti/GitHub/noesis-multi
python3 split_noesis.py --version 812

# Verificare zero CDN nella versione Full
grep -c "cdn.jsdelivr.net\|code.jquery.com" noesis812-full.html
# Deve restituire 0

# Contare righe e dimensione
wc -l noesis812*.html
ls -lh noesis812*.html

# Trovare una funzione specifica
grep -n "function nomeFunzione" noesis812.html

# Trovare una variabile globale
grep -n "^    let varName\|^    const VAR_NAME" noesis812.html
```

---

## 15. NOTE PER IMPLEMENTAZIONI FUTURE

### 15.1 Cosa NON toccare

- I marcatori `<!-- SN56_SOURCE_START/END -->` — rompono split_noesis.py
- I marcatori `// ── IDB bridge` e `// ── END IDB bridge` — rompono split
- I marcatori `// ── Apri sn56.x con payload ──` — rompono split
- L'ordine JSZip → epub.js — epub.js dipende da JSZip come globale
- Le classi CSS `.snapshots-*` e `.snapshot-*` — rimosse dallo split

### 15.2 Dove aggiungere nuovo codice

| Cosa aggiungere | Dove metterlo |
|-----------------|---------------|
| Nuovo tema lettura | Array `THEME_COLORS` + gruppo in `THEME_GROUPS` + CSS `:root.theme-*` |
| Nuova impostazione reader | `interfaceSettings` + `defaultInterfaceSettings` + `applyInterfaceSettings()` |
| Nuovo pulsante menubar | HTML `nav.reader-menubar` + CSS `.rmb-item` + handler in event delegation |
| Nuovo pulsante library header | HTML header + CSS `.lib-header-btn` + handler |
| Nuovo store IDB | Nuova costante + funzioni open/save/get/delete |
| Nuova feature reader | Dopo la sezione esistente più affine (es. dopo TOC per nuovi pannelli) |

### 15.3 Pattern per aggiungere una feature

1. **CSS**: aggiungere regole nella sezione appropriata (o in fondo al blocco CSS)
2. **HTML**: aggiungere elementi statici nella view appropriata
3. **JS variabili**: dichiarare `let` nella sezione stato globale (righe ~4044+)
4. **JS funzioni**: aggiungere funzioni prima della event delegation
5. **JS handler**: collegare nell'event delegation globale (`document.addEventListener`)
6. **Testare split**: eseguire `split_noesis.py --version 812` e verificare
