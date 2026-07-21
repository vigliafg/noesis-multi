# NOESIS-MAP — Mappa Completa della Basecodice

> **Ultimo aggiornamento:** 2026-07-21
> **Versione di riferimento:** noesis816-full-reader / noesis816-full-editor (v0.16.1)
> **Scopo:** Documento di riferimento completo per qualsiasi futura implementazione di codice sul repository noesis-multi.
>
> **Cronologia versioni responsive:**
> - v0.13 (813): hamburger menu, TOC overlay, touch zone navigation
> - v0.14 (814): hamburger contestuale, toolbar pulita, dead CSS rimosso
> - v0.15 (815): statusbar con spine prev/next, parent context TOC, WCAG tap targets
> - v0.16 (816): nav mode popover in toolbar, chapter boundary detection, rifiniture mobile. Varianti CDN: `noesis816-reader.html`, `noesis816-editor.html`
> - v0.16 EDITOR: toolbar testuale stile reader, hamburger menu responsive, dropdown fix, inspect panel mobile. Variante CDN: `noesis816-editor.html`

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
│   │   ├──[split_noesis.py]──▶ older-version/noesis812-full-reader.html   (793 KB, 6865 righe)
│   │   │                       Library + Reader, NO editor, NO snapshot UI
│   │   │
│   │   └──[split_noesis.py]──▶ older-version/noesis812-full-editor.html   (871 KB, 4441 righe)
│   │                           Editor sn56 standalone (v0.12, ora archiviato)
│   │
│   └── noesis810.html / noesis810-full.html   Versione precedente (ancora presente)
│
├── noesis816-full-editor.html              ★ EDITOR v0.16 — FULL (basecode canonica)
│                           Versione responsive con toolbar testuale (stile reader),
│                           hamburger menu mobile, dropdown fix, inspect panel 95vw.
│                           Dipendenze: jQuery, Summernote-lite, Bootstrap Icons,
│                           Turndown, JSZip — tutte embedded inline (904 KB).
│
├── noesis816-editor.html                   ★ EDITOR v0.16 — CDN
│                           Versione con Bootstrap Icons, jQuery e Summernote-lite
│                           da CDN jsDelivr. CSS Summernote e JS custom inline.
│                           Derivata da noesis816-full-editor.html (627 KB, -31%).
│
├── older-version/                         📦 Versioni intermedie archiviate
│   ├── noesis813-full-reader-responsive.html   v0.13 — hamburger menu, TOC overlay
│   ├── noesis814-full-reader-responsive.html   v0.14 — hamburger contestuale
│   ├── noesis815-full-reader-responsive.html   v0.15 — statusbar spine, WCAG
│   ├── noesis812-full-reader.html              reader-only split (v0.12)
│   ├── noesis812-full-reader-responsive.html   reader responsive derivato
│   ├── noesis812-full-editor.html              editor standalone (v0.12, pre-responsive)
│   └── noesis812-full-reader.zip               archivio compresso
│
├── noesis816-reader.html                  ★ READER v0.16.1 — CDN
│                           Versione con dipendenze CDN jsDelivr (Bootstrap Icons,
│                           JSZip, epub.js). CSS e JS applicativo inline.
│                           ★ v0.16.1: Contextual Annotate Popup — popup fluttuante
│                           vicino al testo selezionato, 4 colori, 1 click per evidenziare.
│
└── noesis816-full-reader.html             ★ READER v0.16.1 — FULL (basecode canonica)
│                           Versione con tutte le dipendenze embedded inline
│                           (zero richieste HTTP). Basecode canonica del reader.
│                           ★ v0.16.1: Contextual Annotate Popup — redesign completo
│                           del sistema di highlight con popup contestuale.
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
| `currentReaderHighlightColor` | ~ | ~ | let | `'yellow'` | Colore highlight attivo (yellow/green/pink/remove) |
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

### 5.10 Chapter Navigation (⭐ v815/v816)

| Funzione | Riga (816) | Descrizione |
|----------|------------|-------------|
| `setStatus(msg)` | ~4288 | Imposta il testo nella statusbar |
| `setStatusPath(fullPath)` | ~4292 | Mostra breadcrumb con parent context ("Part I → Chapter 1") |
| `_findSpineIndex(href)` | ~4310 | Cerca indice di un href nello spine EPUB |
| `goPrevChapter()` | ~4321 | Naviga al capitolo precedente via spine |
| `goNextChapter()` | ~4330 | Naviga al capitolo successivo via spine |
| `updateChapterNav()` | ~4339 | Aggiorna stato disabled dei pulsanti prev/next |

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

### 6.6 Flusso: Contextual Annotate Popup (v0.16.1)

```
User seleziona testo nel reader
  → epub.js 'selected' event → _readerPendingCfi = cfiRange
  → setTimeout 60ms → _showCtxAnnotatePopup()
  → Popup appare centrato sotto la riga selezionata (4 pallini colore)
  → User clicca un colore → applyReaderHighlight() / removeReaderHighlight()
  → Popup si chiude, highlight applicato/rimosso
  → Salva highlights nel record libro in EpubLibraryDB

Annullamento:
  → User clicca fuori → iframe selectionchange → _hideCtxAnnotatePopup()
  → Popup sparisce senza annotare

Il vecchio readerHighlightMenu è mantenuto nascosto (display:none) per compatibilità.
Il pallino colore (rmbAnnotateColor / hmbAnnotateColor) mostra il colore attivo
sia in desktop (menubar) che in mobile (hamburger drawer).
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

### 12.6 Chapter Navigation Statusbar (⭐ v815/v816)

**Elementi:** `#status` flex container, `#statusPrevBtn`, `#statusChapterName`, `#statusNextBtn`

**CSS:** `.chap-nav-btn` — pulsanti ◀/▶ 44×44px tap target (WCAG), border:none, bg transparent

**Flusso:**
```
User click ◀ o ▶ nella statusbar
  → goPrevChapter() / goNextChapter()
  → _findSpineIndex(href) — cerca href corrente nello spine
  → rendition.display(spine.items[idx ± 1].href)
  → L'evento 'relocated' chiama updateChapterNav()
    → disabilita ◀ se primo capitolo, ▶ se ultimo
    → setStatusPath() con breadcrumb TOC
```

### 12.7 Nav Mode Popover (⭐ v816)

**Elementi:** `#scrollModeBtn` (bottone toolbar), `#navModePopover` (dropdown popover)

**CSS:** `.nav-mode-popover` — position:absolute, bg white, border-radius 6px, box-shadow. `.open` per mostrare.

**Flusso:**
```
User click #scrollModeBtn
  → Toggle #navModePopover.open
User click Page Mode / Scroll Mode
  → Imposta scrollMode, chiama _syncNavModeBtn()
  → recreateRendition() con nuovo layout
Click esterno → chiude popover
```

**Nota:** Nella v816 il Navigate dropdown nella menubar esiste ancora come indicatore testuale (`.rmb-nav-item` Page/Scroll), ma l'interazione primaria è stata spostata nel popover della toolbar.

---

## 13. MAPPA VARIANTI DERIVATE

### 13.1 `older-version/noesis812-full-reader.html` (6865 righe, 793 KB)

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

### 13.2 `older-version/noesis812-full-editor.html` (4441 righe, 871 KB) — v0.12

> **Nota:** Questa è la versione pre-responsive archiviata in `older-version/`.
> La versione corrente è `noesis816-full-editor.html` (v0.16, ~904 KB) con UI responsive.

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
        │   ├── Bottom toolbar (#bottom-toolbar) con icone Bootstrap
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

### 13.3 `noesis816-full-editor.html` (v0.16, ~904 KB) — FULL Responsive

```
┌──────────────────────────────────────────────────────────────────┐
│  noesis816-full-editor.html — Versione Fully-Offline Responsive │
│  Basecode canonica dell'editor. ZERO dipendenze CDN.             │
│  Derivato da noesis812-full-editor.html + trasformazione UI.     │
└──────────────────────────────────────────────────────────────────┘

DIFFERENZE PRINCIPALI vs v0.12:

🎨 TOOLBAR TESTUALE (stile reader):
  - Bottoni .btn-editor: solo testo, 15px, white bg, border, 4px radius
  - Varianti: primary (blu), success (verde), warning (arancio), info (azzurro)
  - Header: titolo nascosto (display:none, resta in DOM per JS),
    hamburger ☰ allineato a sinistra, pulsante help ? a destra

🍔 HAMBURGER MENU (mobile ≤768px):
  - #hamburgerDrawerEditor: slide-in da sinistra, 300px, backdrop scuro
  - 10 voci: Chapter (New, Import, Export, More), Collection (Add, Inspect,
    Clear, More), Tools (Excalidraw)
  - Dropdown "More": menu spostato in document.body con stopPropagation
    per evitare conflitti di chiusura
  - Contatore chunk sincronizzato (#drawerChunkCounter) su voce "Add Chunk"

📱 BOTTOM TOOLBAR:
  - Visibile solo in desktop (>768px): #bottom-toolbar visibile
  - Mobile (≤768px): #bottom-toolbar, #bottom-toolbar * → display: none !important

🔽 DROPDOWN FIX:
  - _closeAllDropdowns(): resetta display + transform inline
  - Comportamento: tap fuori chiude, nuovo dropdown sostituisce precedente,
    scelta opzione esegue + chiude

📐 INSPECT PANEL MOBILE:
  - width: 95vw, left: 2.5vw, right: 2.5vw → margini laterali uniformi

📦 DIPENDENZE (tutte embedded inline):
  - Bootstrap Icons v1.11.3 (CSS + font base64)
  - Summernote-lite v0.8.20 (CSS + font + JS)
  - jQuery v3.7.1, JSZip, Turndown, html-docx-js
  - Custom JS: initEditor(), export, chapter snapshot, chunk collection
```

### 13.4 `noesis816-editor.html` (v0.16, ~627 KB) — CDN

```
┌──────────────────────────────────────────────────────────────────┐
│  noesis816-editor.html — Versione CDN                           │
│  Bootstrap Icons, jQuery e Summernote-lite da jsDelivr.         │
│  CSS Summernote e JS custom inline.                             │
└──────────────────────────────────────────────────────────────────┘

CDN LINKS:
  <link>  bootstrap-icons@1.11.3 (CSS)
  <script> jquery@3.7.1 (JS, caricato PRIMA degli script inline)
  <script> summernote@0.8.20/dist/summernote-lite.min.js

EMBEDDED (inline):
  - Summernote-lite CSS + @font-face (necessario per icone toolbar)
  - Bootstrap Icons → rimosso, sostituito da CDN
  - jQuery → rimosso, sostituito da CDN
  - Summernote JS → rimosso, sostituito da CDN
  - JSZip, Turndown, html-docx-js → mantenuti inline
  - Custom JS → invariato

DIMENSIONE: 627 KB vs 904 KB full (-31%)
```

---

## 15. STRUTTURA INTERNA DI `older-version/noesis813-full-reader-responsive.html` (7553 righe)

> **Base:** older-version/noesis812-full-reader.html (reader-only split)
> **Modifiche v812→v813:** mobile responsive layout, hamburger menu, TOC overlay,
> swipe navigation, mobile touch zones per page-turn.

```
┌──────────────────────────────────────────────────────────────────┐
│  older-version/noesis813-full-reader-responsive.html                          │
│  Reader + Library responsive. Fully offline (embedded).         │
│  NO editor, NO snapshot UI, NO IDB bridge.                     │
└──────────────────────────────────────────────────────────────────┘

RIGA       CONTENUTO
────       ──────────────────────────────────────────────────────────
1-7        <head> + meta (viewport con max-scale=3.0)
8-14       🟦 Bootstrap Icons CSS + font base64 (EMBEDDED, ~259 KB)

15-2845    🟦 CSS APPLICATIVO (~2830 righe)
           │
           ├── 15-38     Global & Utils (reset, .hidden, flexbox)
           ├── 39-89     Light theme (default, CSS variables)
           ├── 90-146    Gray Dark Light theme
           ├── 147-197   Header
           ├── 198-230   Unified Library Header Buttons
           ├── 231-277   Themes Dropdown
           ├── 278-333   Tools Dropdown, Book row, Book header
           ├── 334-431   Cover, Book meta, Book actions
           ├── 432-573   Extracted chapters section
           ├── 574-678   Responsive base (max-width: 600px, 768px)
           ├── 679-1192  Reader View base + header + toolbar
           ├── 834-1078  User Bookmarks Drawer (.ubm-*)
           ├── 1079-1137 Extract Chapter Dropdown
           ├── 1138-1214 Theme Picker Popup
           ├── 1215-1389 Typography Popup + Save Toast
           ├── 1390-1460 ⭐ Floating Navigation Buttons
           │   ├── 1391-1412  .floating-nav-btn: fixed, 25px×200px, semi-trasparente
           │   ├── 1424-1429  #floatingPrevBtn (left:0), #floatingNextBtn (right:0)
           │   ├── 1433        .floating-nav-btn.hidden { display:none !important }
           │   ├── 1438        @media (≤768px): 22px×180px, font 18px
           │   └── 1446        @media (≤480px): 20px×150px, font 16px
           ├── 1461-1756  Media Dialog + Display Save Prompt + Highlight
           ├── 1757-2033  Reader Menubar (.rmb-*)
           ├── 2034-2207  Custom tooltip, Banner avvio, Help overlay
           ├── 2208-2367  Library help banner
           ├── 2368-2603  Reader Menubar (regole complete)
           │
           ├── 2598-2845 ⭐⭐ MOBILE RESPONSIVE — v813 (~250 righe)
           │   ├── 2598        .mobile-touch-zone { display: none } — hidden default
           │   ├── 2602-2607   Intestazione: v813-responsive (touch zones)
           │   ├── 2609-2618   Touch targets: WCAG 44×44px su (pointer: coarse)
           │   ├── 2620-2634   Hamburger menu button (hidden desktop)
           │   ├── 2635-2693   Hamburger drawer (slide from left, 300px)
           │   ├── 2694-2708   Mobile overlay backdrop
           │   ├── 2709-2827   @media (≤768px) — Tablet:
           │   │   ├── Menubar: hamburger visibile, voci testuali nascoste
           │   │   ├── #bookmarks → TOC overlay (fixed, slide left, z-index 1000)
           │   │   ├── #viewer → width 100%
           │   │   ├── .floating-nav-btn → display:none!important
           │   │   ├── ⭐ .mobile-touch-zone — edge-tap zones:
           │   │   │   display:flex, fixed, top:15vh, height:70vh,
           │   │   │   width:12vw (min 44px, max 60px), z-index 99
           │   │   │   ::after: chevron indicators (subtle borders)
           │   │   │   .tapped: gradient glow feedback
           │   │   ├── Library header: compact (padding/font ridotti)
           │   │   ├── Reader header: compact
           │   │   └── Popup/Drawer: dimensioni ridotte
           │   └── 2828-2844   @media (≤480px) — Smartphone:
           │       ├── #bookmarks: 280px/max 90vw
           │       ├── Library header: 8px 10px, title 16px
           │       ├── Book covers: 44×60px
           │       └── #hamburgerDrawer: 260px/max 88vw
           └── 2845        END MOBILE RESPONSIVE
────
2846        </style>
2847        </head>
2848        <body>

2850-2878  🟧 OVERLAY GLOBALI
           ├── 2850-2853   #loadingOverlay + spinner
           ├── 2854-2855   #mobileOverlayBackdrop — backdrop scuro mobile
           └── 2857-2870   #hamburgerDrawer — menu mobile slide-in
               ├── 2860        #hamburgerClose ×
               ├── 2862-2869   8 voci (Library, TOC, Bookmarks, Display,
               │               Navigate, Annotate, Extract, Help)
               └── Mappate a .rmb-item corrispondenti

2874-3035  🟧 LIBRARY VIEW (#library-view)
           ├── 2879-2953   Header:
           │   ├── 2889-2890  #hamburgerBtnLib (mobile only)
           │   ├── 2893       #libAddBooksBtn
           │   ├── 2905-2923  #libThemesDropdown, #libToolsDropdown
           │   └── 2945       #libHelpBtn
           ├── 2950        #bookGrid — griglia libri
           ├── 2955-2973   #libHelpBanner
           └── 2975-3008   #libHelpOverlay

3037-3039  🟧 SN56 SOURCE (JSON vuoto/minimale, solo 2 ref)
3040-3041  🟩 JSZip v3.10.1 inline
3042-3043  🟩 epub.js v0.3.93 inline

3045-7553  🌿 JAVASCRIPT (~4508 righe, 60% del file)
           │
           ├── 3045-3057  "use strict" + error handler globale
           │
           ├── 3058-3337  MODULO noesisDB (~280 righe)
           │   ├── 3058-3060  Costanti: NOESIS_DB_NAME, v1, 'chapters'
           │   ├── 3062-3077  openNoesisDB()
           │   ├── 3078-3088  saveExtractedChapterToDB()
           │   ├── 3089-3099  deleteExtractedChapterFromDB()
           │   ├── 3100-3106  deleteSnapshotFromDB()
           │   └── 3107-3116  getExtractedChapterFromDB()
           │   ⚠️ NO IDB bridge (rimosso nello split reader)
           │
           ├── 3119-3243  MODULO mainDB / EpubLibraryDB (~125 righe)
           │   ├── 3119-3121  Costanti: DB_NAME, v1, 'books'
           │   ├── 3124-3163  openDB()
           │   ├── 3164-3213  saveBookToDB()
           │   ├── 3215-3226  getAllBooks()
           │   └── 3227-3243  deleteBook()
           │
           ├── 3245-3498  CORE UI (~250 righe)
           │   ├── 3245-3258  Variabili view: libraryView, readerView, bookGrid, ...
           │   ├── 3259-3278  showLoading(), hideLoading(), showLibrary()
           │   ├── 3279-3305  showReader(bookData)
           │   ├── 3310-3320  _generateCleanHTML()
           │   ├── 3323-3328  _buildExtractionTimestamp()
           │   ├── 3330-3339  _autoDownloadHTML()
           │   ├── 3341-3369  loadLibraryBooks() — SOLO libri, no capitoli/snapshot
           │   └── 3370-3498  openBookFromLibrary(bookData)
           │
           ├── 3500-3960  STATO GLOBALE READER (~460 righe)
           │   ├── 3500-3520  Variabili: book, rendition, fontSize, lineHeight,
           │   │              scrollMode, dualPageMode, sidebarVisible,
           │   │              currentTheme, currentLocation, buttonZoom,
           │   │              _autoSaveTimer, _lastAutoSavedCfi, _dspTimer
           │   ├── 3522-3537  interfaceSettings + defaultInterfaceSettings
           │   ├── 3539-3547  currentBookId, currentBookTitle,
           │   │              readerHighlights[], HL_COLORS
           │   ├── 3550-3564  showToast(msg)
           │   ├── 3565-3596  _getCenterCfi()
           │   ├── 3597-3605  _snapshotVisualState()
           │   ├── 3606-3639  savePositionOnly()
           │   ├── 3640-3677  saveVisualSettings()
           │   ├── 3678-3698  startAutoSave() / stopAutoSave()
           │   ├── 3699-3730  _isBrowserTranslated(), display save prompt
           │   ├── 3731-3806  saveBookState(), loadAndApplyBookState()
           │   ├── 3807-3871  setStatus(), updateFontInfo(), updateLineHeightInfo(),
           │   │              applyInterfaceSettings()
           │   ├── 3872-3891  hexToRgba(), adjustColor()
           │   ├── 3892-3960  _syncNavModeBtn(), updateInterfaceControls()
           │   │              ⭐ shouldShowButtons → touch zone visibility toggle
           │   └── 3936-3938  scrollMode=false, sidebarVisible=false
           │
           ├── 3961-4600  ESTRAZIONE CAPITOLI (~640 righe)
           │   ├── 3961-4140  navigateToHref(), collectAllSubchapters()
           │   ├── 4141-4398  extractMultipleSections()
           │   └── 4399-4600  extractCurrentChapter()
           │
           ├── 4601-5000  TEMI + RENDITION (~400 righe)
           │   ├── 4709-4733  THEME_COLORS (15 temi)
           │   ├── 4734-4740  THEME_GROUPS (5 gruppi)
           │   ├── 4740-4815  applyTheme(), updateThemeSwatchActive(), buildThemePopup()
           │   └── 4816-5000  recreateRendition()
           │
           ├── 5001-5350  TOC + SEGNALIBRI (~350 righe)
           │   ├── 5001-5094  renderBookmarksSimple()
           │   ├── 5095-5148  saveUserBookmarksToDB(), loadUserBookmarksFromDB()
           │   ├── 5149-5237  renderUbmList()
           │   ├── 5238-5341  createUserBookmark()
           │   └── 5342-5350  openUbmDrawer(), closeUbmDrawer()
           │
           ├── 5351-6148  EVENT HANDLERS (~800 righe)
           │   ├── 5351-5600  Highlight, media click, keyboard shortcuts
           │   ├── 5601-5800  Toolbar: prev/next, TOC toggle, scroll, dual page
           │   ├── 5801-6000  Estrazione, font, line height, temi
           │   ├── 6001-6100  Bookmark drawer, Library theme toggle
           │   └── 6101-6148  Floating nav button click handlers:
           │       floatingPrevBtn.onclick = () => rendition.prev()
           │       floatingNextBtn.onclick = () => rendition.next()
           │
           ├── 6149-6180  ⭐ MOBILE TOUCH ZONES — v813 (~30 righe)
           │   ├── 6149        // ── Mobile Touch Zones: edge-tap page navigation ──
           │   ├── 6150-6177   (function initMobileTouchZones() { ... })()
           │   │   ├── getElementById('touchZonePrev/Next')
           │   │   ├── _handleZoneTap(direction, el, e):
           │   │   │   • check selezione testo (window.getSelection())
           │   │   │   • check scrollMode || sidebarVisible
           │   │   │   • debounce 350ms
           │   │   │   • feedback visivo (.tapped class, 250ms)
           │   │   │   • rendition.prev() / rendition.next()
           │   │   └── listener 'click' + 'touchend' su entrambe le zone
           │   └── 6178        fine IIFE
           │
           ├── 6181-6228  Floating nav button visibility toggle
           │
           ├── 6230-7080  MENUBAR + INIZIALIZZAZIONE (~850 righe)
           │   ├── 6230-6480  Event delegation globale document.addEventListener
           │   │              Gestione .rmb-item, highlight mode,
           │   │              Navigate dropdown, Annotate, Extract, Help
           │   ├── 6481-6662  Library: tools dropdown, localStorage keys
           │   ├── 6663-6692  localStorage: chiavi e helper banner
           │   ├── 6693-6730  Reader help overlay
           │   ├── 6731-6770  Library theme toggle
           │   └── 6771-7080  Editor Report help, Navigate Menubar completo
           │
           └── 7081-7553  ⭐⭐ MOBILE RESPONSIVE HANDLERS (~470 righe)
               ├── 7081-7090   State variabili: _isMobile(), _drawerOpen, _touchStartX/Y
               ├── 7091-7104   _closeAllDrawers()
               ├── 7105-7125   openHamburger(), closeHamburger()
               ├── 7126-7196   openTocOverlay() — trasforma #bookmarks in overlay
               │               spostamento DOM + stili inline
               ├── 7197-7225   closeTocOverlay() — ripristina #bookmarks
               ├── 7226-7238   Backdrop click → close all drawers
               ├── 7239-7296   Hamburger items → trigger .rmb-item action
               ├── 7297-7310   Override TOC button on mobile → openTocOverlay()
               ├── 7311-7368   ⭐ Swipe navigation (mobile):
               │   ├── touchstart/touchend su #viewer
               │   ├── threshold 50px, check selezione testo
               │   ├── edge swipe (dx>50) → openTocOverlay()
               │   └── swipe ← → rendition.prev/next()
               ├── 7369-7456   initLibraryMobileDropdown()
               ├── 7457-7505   updateMobileHeader()
               └── 7506-7549   Init: DOMContentLoaded → initSwipeNavigation(),
                                initLibraryMobileDropdown(), updateMobileHeader()
────
7554-7555  </body></html>
```

### 15.1 DIFFERENZE CHIAVE vs older-version/noesis812-full-reader.html

| Feature | 812 reader | 813 responsive |
|---------|-----------|----------------|
| Viewport meta | `no-scale` | `max-scale=3.0` (pinch-zoom) |
| Mobile menu | ❌ | Hamburger drawer (slide-in left) |
| TOC su mobile | Sidebar fissa | Overlay slide-in |
| Floating nav buttons | Visibili (nascosti via .hidden) | Nascosti su ≤768px |
| Edge-tap navigation | ❌ | ✅ Touch zones (v813) |
| Swipe navigation | ❌ | ✅ 50px threshold |
| Mobile backdrop | ❌ | ✅ #mobileOverlayBackdrop |
| Library dropdown mobile | ❌ | ✅ Touch-friendly |
| Righe totali | 6865 | 7553 (+688) |

### 15.2 NUOVI ELEMENTI DOM (v813 responsive)

| ID / Classe | Tipo | Riga | Ruolo |
|-------------|------|------|-------|
| `#mobileOverlayBackdrop` | div | 2854 | Sfondo scuro overlay mobile |
| `#hamburgerDrawer` | div | 2857 | Menu hamburger slide-in (300px) |
| `#hamburgerClose` | button | 2860 | × chiudi hamburger |
| `#hamburgerBtn` | button | 3065 | ☰ nella reader menubar (mobile) |
| `#hamburgerBtnLib` | button | 2889 | ☰ nella library header (mobile) |
| `.hmb-item` | div ×8 | 2862-2869 | Voci hamburger (Library, TOC, ...) |
| `#touchZonePrev` | div | 3379 | Zona touch sinistra page-turn |
| `#touchZoneNext` | div | 3380 | Zona touch destra page-turn |

### 15.3 NUOVE FUNZIONI MOBILE (v813)

| Funzione | Riga | Descrizione |
|----------|------|-------------|
| `_isMobile()` | 7088 | `() => window.innerWidth <= 768` |
| `_closeAllDrawers()` | 7091 | Chiude hamburger + TOC overlay |
| `openHamburger()` | 7105 | Apre drawer hamburger con backdrop |
| `closeHamburger()` | 7110 | Chiude drawer hamburger |
| `openTocOverlay()` | 7126 | Trasforma #bookmarks in overlay mobile |
| `closeTocOverlay()` | 7197 | Ripristina #bookmarks in sidebar |
| `initSwipeNavigation()` | 7311 | Touch handler swipe ← → su #viewer |
| `initLibraryMobileDropdown()` | 7369 | Dropdown touch-friendly library |
| `updateMobileHeader()` | 7457 | Aggiorna header mobile |
| `initMobileTouchZones()` | 6150 | IIFE: touch zone edge-tap navigation |
| `_handleZoneTap(dir, el, e)` | 6155 | Handler interno: debounce, check stato, feedback |

### 15.4 FLUSSO: Mobile Page Navigation

```
SU MOBILE (≤768px), modalità paginata, sidebar chiusa:

OPZIONE 1 — Edge Tap (Touch Zones):
  User tocca bordo sinistro/destro schermo
    → touchend/click su #touchZonePrev o #touchZoneNext
    → _handleZoneTap():
      1. Check: testo selezionato? → return
      2. Check: scrollMode || sidebarVisible? → return
      3. Check: debounce 350ms? → return
      4. Aggiunge classe .tapped (glow animation 250ms)
      5. rendition.prev() o rendition.next()

OPZIONE 2 — Swipe:
  User swipa ← o → su #viewer
    → touchstart: registra _touchStartX, _touchStartY
    → touchend: calcola dx, dy
    → Check: |dx| > 50 && |dx| > |dy| → è swipe orizzontale
    → Check: testo selezionato? → return
    → Edge + dx > 50 → openTocOverlay()
    → dx < -50 → rendition.next()
    → dx > 50 → rendition.prev()
```

### 15.5 BREAKPOINT RESPONSIVE

| Breakpoint | Target | Cosa cambia |
|------------|--------|-------------|
| `(pointer: coarse)` | Touch devices | Touch target 44×44px |
| `max-width: 768px` | Tablet | Hamburger visibile, TOC overlay, touch zones attive, floating btn nascosti |
| `max-width: 480px` | Smartphone | Drawer 260px, cover 44×60px, font ridotti |
| `max-width: 600px` | Library grid | Griglia 1 colonna |

### 15.6 VARIABILI DI STATO MOBILE

| Variabile | Riga | Tipo | Default | Descrizione |
|-----------|------|------|---------|-------------|
| `_drawerOpen` | ~7086 | let | `false` | Stato drawer hamburger |
| `_tocOverlayOpen` | ~7087 | let | `false` | Stato TOC overlay |
| `_touchStartX` | ~7088 | let | `null` | Coord X touchstart swipe |
| `_touchStartY` | ~7089 | let | `null` | Coord Y touchstart swipe |
| `_touchIsEdge` | ~7090 | let | `false` | Swipe partito dal bordo |
| `_tzDebounce` | ~6158 | let | `null` | Timer debounce touch zone |

---

## 16. COMANDI UTILI

```bash
# Eseguire split
cd /home/vigliafg/Documenti/GitHub/noesis-multi
python3 split_noesis.py --version 812

# Verificare zero CDN nella versione Full
grep -c "cdn.jsdelivr.net\|code.jquery.com" noesis812-full.html
# Deve restituire 0

# Contare righe e dimensione
wc -l older-version/noesis812*.html older-version/noesis813*.html
ls -lh older-version/noesis812*.html older-version/noesis813*.html

# Trovare una funzione specifica
grep -n "function nomeFunzione" older-version/noesis813-full-reader-responsive.html

# Trovare una variabile globale
grep -n "^    let varName\|^    const VAR_NAME" older-version/noesis813-full-reader-responsive.html

# Verificare struttura responsive
grep -n "MOBILE RESPONSIVE\|END MOBILE\|touchZone\|hamburger\|@media" older-version/noesis813-full-reader-responsive.html
```

---

## 17. NOTE PER IMPLEMENTAZIONI FUTURE

### 17.1 Cosa NON toccare

- I marcatori `<!-- SN56_SOURCE_START/END -->` — rompono split_noesis.py
- I marcatori `// ── IDB bridge` e `// ── END IDB bridge` — rompono split
- I marcatori `// ── Apri sn56.x con payload ──` — rompono split
- L'ordine JSZip → epub.js — epub.js dipende da JSZip come globale
- Le classi CSS `.snapshots-*` e `.snapshot-*` — rimosse dallo split
- I marcatori `MOBILE RESPONSIVE` e `END MOBILE RESPONSIVE` — delimitano il blocco responsive
- I marcatori `MOBILE RESPONSIVE HANDLERS` e `END MOBILE RESPONSIVE HANDLERS` — delimitano JS mobile

### 17.2 Dove aggiungere nuovo codice nella v813

| Cosa aggiungere | Dove metterlo |
|-----------------|---------------|
| Nuovo tema lettura | `THEME_COLORS` + `THEME_GROUPS` + CSS `:root.theme-*` |
| Nuova impostazione reader | `interfaceSettings` + `applyInterfaceSettings()` |
| Nuovo pulsante menubar | HTML `nav.reader-menubar` + `.rmb-item` + handler + voce hamburger `.hmb-item` |
| Nuova feature mobile | Dentro `MOBILE RESPONSIVE HANDLERS` (JS) + `MOBILE RESPONSIVE` (CSS) |
| Nuovo breakpoint | Dentro `RESPONSIVE BREAKPOINTS` (~riga 2709) |
| Nuovo pulsante library | HTML `#library-view header` + CSS `.lib-header-btn` + handler |

### 17.3 Pattern per estendere la v813 → v814

1. **CSS mobile**: aggiungere regole dentro `@media (max-width: 768px)` o nuovo breakpoint
2. **HTML mobile**: aggiungere elementi tra i marcatori MOBILE RESPONSIVE
3. **JS mobile**: aggiungere funzioni tra `// ── State ──` e `// ── END MOBILE RESPONSIVE HANDLERS ──`
4. **JS globale**: aggiungere nel flusso principale JS, prima degli event handler
5. **Testare**: aprire il file nel browser, testare a diverse larghezze (DevTools responsive mode)

---

## 18. MAPPA DIFFERENZIALE: v813-responsive vs v812-full (MADRE)

> **Scopo:** Guida per il merge futuro delle feature mobile responsive dalla v813
> nella versione madre `noesis812-full.html` (o `noesis814-full.html`).
> **File confrontati:** `noesis813-full-reader-responsive.html` (820 KB, 7553 righe)
> vs `noesis812-full.html` (1.7 MB, 7258 righe).

### 18.1 PREMESSA: Catena di derivazione

```
noesis812-full.html  (MADRE — completo: editor, snapshot, IDB bridge)
    │
    ├─[split_noesis.py]──▶ older-version/noesis812-full-reader.html (reader-only split)
    │                       RIMOSSO: editor sn56, snapshot UI, IDB bridge
    │
    └─[modifiche manuali]──▶ older-version/noesis813-full-reader-responsive.html
                             AGGIUNTO: mobile responsive ~720 righe
```

La v813 eredita tutte le RIMOZIONI dello split PIÙ le AGGIUNTE mobile.
Per il merge nella MADRE, le rimozioni vanno **IGNORATE** (sono feature
dello split), mentre le aggiunte vanno **PORTATE** nella madre.

---

### 18.2 RIEPILOGO QUANTITATIVO

| Metrica | v812-full (MADRE) | v813-responsive | Delta |
|---------|-------------------|-----------------|-------|
| Righe totali | 7,258 | 7,553 | +295 |
| Dimensione | 1.7 MB | 820 KB | -880 KB |
| CSS (righe) | ~2,640 | ~2,830 | +190 |
| HTML (righe) | ~600 | ~630 | +30 |
| JS (righe) | ~3,990 | ~4,508 | +518 |
| Editor sn56 | SI (912 KB) | NO (0 ref) | RIMOSSO |
| Mobile features | NO (0 ref) | SI (~720 righe) | AGGIUNTO |

---

### 18.3 CATEGORIA A: RIMOSSO DALLO SPLIT (da IGNORARE nel merge)

Queste feature sono state rimosse da `split_noesis.py` per creare il reader-only.
**NON vanno riportate** — la MADRE le ha già.

#### A.1 HTML rimosso

| Elemento | Riga 812-full | Ruolo |
|----------|---------------|-------|
| `<!-- SN56_SOURCE_START/END -->` | 3241, 3259 | Delimitatori blocco editor embedded |
| `<script id="sn56Source">` | 3242-3258 | JSON con HTML editor completo (~912 KB) |
| `#importSnapshotsInput` | 2678 | Input file nascosto per import snapshot |
| `#libImportSnapshotsBtn` | 2679 | Pulsante "Import Snapshots" |
| `#libEditorBtn` | 2684 | Pulsante "Open Editor" |

#### A.2 JS rimosso

| Funzione / Blocco | Riga 812-full | Ruolo |
|-------------------|---------------|-------|
| `_openSn56()` | ~3561 | Apri editor sn56 in finestra blob |
| `_openExtractedEnv()` | ~3621 | Apri snapshot esistente nell'editor |
| `getAllExtractedChapters()` | ~3545 | Recupera capitoli/snapshot da noesisDB |
| `importSnapshotsFromDisk()` | ~3812 | Importa file HTML snapshot da disco |
| `_processSnapshotFiles()` | ~3844 | Processa file snapshot selezionati |
| **IDB Bridge** (postMessage) | ~3331-3350 | Handler messaggi da finestre blob:null |
| IIFE Import Snapshots | ~7002 | Inizializzazione import snapshot |
| IIFE Open Editor | ~7050 | Inizializzazione apertura editor |
| `loadLibraryBooks()` (semplificata) | - | Mostra solo libri, no capitoli/snapshot |

#### A.3 CSS rimosso

| Blocco | Ruolo |
|--------|-------|
| 6 classi `.snapshot-*` | Stili per UI snapshot (rimosse dallo split) |

---

### 18.4 CATEGORIA B: AGGIUNTO PER MOBILE (da PORTARE nel merge)

Queste sono le feature nuove della v813 che vanno integrate nella MADRE.
Ordinate per priorità e dipendenza.

#### B.1 Viewport Meta — PRIORITA: ALTA

```diff
- <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
+ <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0">
```

**Riga:** 6 in entrambi i file. **Impatto:** permette pinch-zoom su mobile.

#### B.2 CSS: Blocco MOBILE RESPONSIVE (~250 righe) — PRIORITA: ALTA

**Righe 813:** 2598-2845 (tra Reader Menubar e `</style>`)
**Da inserire nella MADRE:** prima di `</style>`, dopo il blocco Reader Menubar.

Il blocco include:
- `.mobile-touch-zone { display: none }` — default nascosto
- `@media (pointer: coarse)` — touch targets WCAG 44x44px
- `.hamburger-btn` — pulsante hamburger
- `#hamburgerDrawer` + `.hmb-item` — drawer slide-in 300px
- `#mobileOverlayBackdrop` — sfondo overlay scuro
- `@media (max-width: 768px)` — Tablet: hamburger visibile, TOC overlay, viewer full-width, floating btn nascosti, touch zones attive, header compact
- `@media (max-width: 480px)` — Smartphone: drawer 260px, cover 44x60px

**ATTENZIONE:** le righe 1438 e 1446 (nel blocco Floating Nav Buttons)
contengono `@media` per i floating buttons a 768px e 480px.
Queste vanno **mantenute** ma il blocco a 2742 (`.floating-nav-btn { display: none !important }`)
le sovrascrive su mobile. Verificare che non ci siano conflitti.

#### B.3 HTML: Nuovi elementi DOM — PRIORITA: ALTA

| # | Elemento | Dove inserirlo nella MADRE |
|---|----------|---------------------------|
| 1 | `<div id="mobileOverlayBackdrop"></div>` | Subito dopo `<body>`, prima di `#loadingOverlay` |
| 2 | `<div id="hamburgerDrawer">` con 8 `.hmb-item` + `#hamburgerClose` | Dopo `#mobileOverlayBackdrop` |
| 3 | `<button id="hamburgerBtnLib">…</button>` | Dentro `#library-view header`, prima degli altri pulsanti |
| 4 | `<button id="hamburgerBtn">…</button>` | Dentro `#reader-view nav.reader-menubar`, primo elemento |
| 5 | `<div id="touchZonePrev" class="mobile-touch-zone left"></div>` | In `#reader-view`, dopo `#floatingNextBtn` |
| 6 | `<div id="touchZoneNext" class="mobile-touch-zone right"></div>` | Dopo `#touchZonePrev` |

#### B.4 JS: Modifiche puntuali — PRIORITA: ALTA

**B.4.1 — Blocco shouldShowButtons** (riga 813: ~3962):
Dopo `floatingPrevBtn/NextBtn.classList.toggle('hidden', ...)` aggiungere:
```javascript
        const tzPrev = document.getElementById('touchZonePrev');
        const tzNext = document.getElementById('touchZoneNext');
        if (tzPrev) tzPrev.classList.toggle('hidden', !shouldShowButtons);
        if (tzNext) tzNext.classList.toggle('hidden', !shouldShowButtons);
```

**B.4.2 — Touch Zone IIFE** (riga 813: ~6149):
Dopo i floating button click handler, aggiungere IIFE con:
- `_handleZoneTap()`: debounce 350ms, check selezione testo, check scrollMode/sidebarVisible
- Listener `click` + `touchend` su `#touchZonePrev` e `#touchZoneNext`
- Chiama `rendition.prev()` / `rendition.next()`

#### B.5 JS: Blocco MOBILE RESPONSIVE HANDLERS (~470 righe) — PRIORITA: MEDIA

**Righe 813:** 7081-7549
**Da inserire nella MADRE:** prima di `</script>`, dopo tutti gli handler esistenti.

Contiene:
- `_isMobile()`, `_closeAllDrawers()`
- `openHamburger()`, `closeHamburger()`
- `openTocOverlay()`, `closeTocOverlay()` — trasforma #bookmarks in overlay
- `initSwipeNavigation()` — swipe left/right 50px threshold
- `initLibraryMobileDropdown()` — dropdown touch-friendly
- `updateMobileHeader()`
- Inizializzazione su `DOMContentLoaded`

**Conflitto potenziale:** il TOC button override su mobile potrebbe interferire
con l'event delegation esistente per `.rmb-item[data-panel="toc"]`.

#### B.6 Variabili di stato mobile — PRIORITA: MEDIA

| Variabile | Riga 813 | Dove dichiarare nella MADRE |
|-----------|----------|-----------------------------|
| `_tocOverlayOpen` | ~7185 | Sezione STATO GLOBALE READER (~4050) |
| `_touchStartX/Y` | ~7186 | idem |
| `_touchIsEdge` | ~7187 | idem |
| `_isMobile` | ~7188 | idem |

---

### 18.5 CATEGORIA C: MODIFICATO (cambiamenti a codice condiviso)

#### C.1 Floating Nav Buttons CSS

Nella v813, `@media (max-width: 768px)` e `@media (max-width: 480px)` per
i floating buttons (righe 1438, 1446) sono **identiche** a quelle nella MADRE.
Nessuna azione necessaria.

#### C.2 Gestione #bookmarks (TOC)

La v813 modifica `#bookmarks` in overlay mobile via `openTocOverlay()`:
- Sposta l'elemento nel DOM (`document.body.appendChild`)
- Applica stili inline (position: fixed, z-index: 1000, transform)
- `closeTocOverlay()` ripristina la posizione originale

Nella MADRE, `#bookmarks` e una sidebar fissa. Questo override e innocuo
perche si attiva solo su `_isMobile()`. Nessun conflitto atteso.

---

### 18.6 CHECKLIST MERGE (15 step)

```
[ ] 1. Viewport meta: max-scale=3.0, rimuovere user-scalable=no
[ ] 2. CSS: copiare blocco MOBILE RESPONSIVE (righe 2598-2845) prima di </style>
[ ] 3. HTML: aggiungere #mobileOverlayBackdrop dopo <body>
[ ] 4. HTML: aggiungere #hamburgerDrawer con 8 .hmb-item
[ ] 5. HTML: aggiungere #hamburgerBtnLib nel library header
[ ] 6. HTML: aggiungere #hamburgerBtn nel reader menubar
[ ] 7. HTML: aggiungere #touchZonePrev e #touchZoneNext nel reader-view
[ ] 8. JS:  toggle touch zone in shouldShowButtons
[ ] 9. JS:  IIFE initMobileTouchZones dopo floating btn handlers
[ ] 10. JS: copiare MOBILE RESPONSIVE HANDLERS (7081-7549) prima di </script>
[ ] 11. JS: verificare no conflitti event delegation TOC button
[ ] 12. JS: dichiarare variabili mobile nella sezione STATO GLOBALE READER
[ ] 13. Test: DevTools responsive mode, breakpoint 768px e 480px
[ ] 14. Test: hamburger, TOC overlay, touch zones, swipe
[ ] 15. Test: editor sn56 funziona ancora (non deve rompersi)
```

---

### 18.7 MAPPA VISUALE DEL MERGE

```
noesis812-full.html (MADRE) — punti di inserimento
═══════════════════════════════════════════════════

1-7      <head> + meta
         [x] viewport: max-scale=3.0, no user-scalable

8-14     Bootstrap Icons CSS embedded
15-2640  CSS applicativo
         [+] MOBILE RESPONSIVE block (2598-2845) prima di </style>

2642     <body>
         [+] #mobileOverlayBackdrop
         [+] #hamburgerDrawer

2648     #loadingOverlay (esistente)

2655     #library-view
         [+] #hamburgerBtnLib nello header

2836     #reader-view
         [+] #hamburgerBtn nella reader-menubar
         [+] #touchZonePrev, #touchZoneNext dopo floating buttons

3241     <!-- SN56_SOURCE_START --> (NON toccare)
3259     <!-- SN56_SOURCE_END --> (NON toccare)

3266     <script>
         ... tutto il JS esistente (NON toccare) ...
         [+] toggle touch zone in shouldShowButtons
         [+] IIFE initMobileTouchZones
         [+] MOBILE RESPONSIVE HANDLERS block
7256     </script>
```

### 18.8 NOTE TECNICHE

1. **Nessuna nuova dipendenza:** tutte le feature mobile usano solo DOM API standard.
2. **Backward compatibility:** gated da `_isMobile()` e media queries CSS. Desktop invariato.
3. **Ordine CSS:** il blocco MOBILE RESPONSIVE va in fondo al `<style>` per precedenza.
4. **Ordine JS:** MOBILE RESPONSIVE HANDLERS va in fondo al `<script>`, dopo tutto.
5. **sn56Source:** NON toccare. Le feature mobile non interagiscono con l'editor.
6. **Dimensione finale MADRE:** ~1.7 MB + ~15 KB = ~1.71 MB.

---

## 16. STRUTTURA INTERNA DI `older-version/noesis814-full-reader-responsive.html` (7481 righe, 820K)

> **Base:** older-version/noesis813-full-reader-responsive.html (copia esatta)
> **Modifiche v813→v814:** menu hamburger contestuale, toolbar library pulita, dead CSS rimosso,
> rimozione `initLibraryMobileDropdown()` in conflitto.

### 16.1 RIEPILOGO MODIFICHE

| # | Modifica | Dettaglio |
|---|----------|-----------|
| 1 | **Hamburger contestuale** | `openHamburger()` rileva la vista attiva e mostra/nasconde voci via classi `.hmb-lib` / `.hmb-rdr` |
| 2 | **Voci library nell'hamburger** | Add Books, Theme: Light, Theme: Dark, Tools, Refresh Library, Help |
| 3 | **Voci reader nell'hamburger** | Library, TOC, Bookmarks, Display, Navigate, Annotate, Extract, Help |
| 4 | **Voci condivise contestuali** | Library (refresh o showLibrary), Help (libHelpBtn o rmbHelp) |
| 5 | **Toolbar library pulita** | Rimosso testo `library-title` ("Noesis") e `library-subtitle` da `.library-header-left` |
| 6 | **Hamburger a estrema sinistra** | `#hamburgerBtnLib` spostato in `.library-header-left` |
| 7 | **Rimossa `initLibraryMobileDropdown()`** | Nascondeva pulsanti THEMES/TOOLS/HELP su mobile in conflitto con hamburger |
| 8 | **CSS mobile: pulsanti nascosti** | `#libThemesBtn, #libToolsBtn, #libHelpBtn { display: none !important }` su ≤768px (i container dropdown restano visibili) |
| 9 | **CSS morto rimosso** | Regole `.library-title`, `.library-subtitle`, `.library-title i`, `.library-title span` eliminate |
| 10 | **File più snello** | Da 7553 a 7481 righe (-72), da 824K a 820K |

### 16.2 HAMBURGER DRAWER — HTML

```html
<div id="hamburgerDrawer">
  <div class="hamburger-header">
    <span class="hamburger-title">Noesis</span>
    <button class="hamburger-close" id="hamburgerClose">✕</button>
  </div>
  <!-- .hmb-lib = library only, .hmb-rdr = reader only, no class = both -->
  <div class="hamburger-item" id="hmbLibrary">Library</div>
  <div class="hamburger-item hmb-lib" id="hmbAddBooks">Add Books</div>
  <div class="hamburger-item hmb-lib" id="hmbLibThemeLight">Theme: Light</div>
  <div class="hamburger-item hmb-lib" id="hmbLibThemeDark">Theme: Dark</div>
  <div class="hamburger-item hmb-lib" id="hmbLibTools">Tools</div>
  <div class="hamburger-item hmb-lib" id="hmbLibRefresh">Refresh Library</div>
  <div class="hamburger-item hmb-rdr" id="hmbToc">TOC</div>
  <div class="hamburger-item hmb-rdr" id="hmbBookmarks">Bookmarks</div>
  <div class="hamburger-item hmb-rdr" id="hmbDisplay">Display</div>
  <div class="hamburger-item hmb-rdr" id="hmbNavigate">Navigate</div>
  <div class="hamburger-item hmb-rdr" id="hmbAnnotate">Annotate</div>
  <div class="hamburger-item hmb-rdr" id="hmbExtract">Extract</div>
  <div class="hamburger-item" id="hmbHelp">Help</div>
</div>
```

### 16.3 HAMBURGER — LOGICA JS

```javascript
// openHamburger() — contestuale
function openHamburger() {
  const isLibrary = !libraryView.classList.contains('hidden');
  document.querySelectorAll('#hamburgerDrawer .hamburger-item').forEach(function(item) {
    if (item.classList.contains('hmb-lib')) {
      item.style.display = isLibrary ? 'flex' : 'none';
    } else if (item.classList.contains('hmb-rdr')) {
      item.style.display = isLibrary ? 'none' : 'flex';
    } else {
      item.style.display = 'flex';  // shared: always visible
    }
  });
  // ...open drawer...
}

// Tre gruppi di handler:
// 1. hamburgerReaderMap — mappa hmb-rdr → rmb* (con dropdown workaround)
// 2. hamburgerLibHandlers — click diretti su pulsanti library
// 3. Shared items (Library, Help) — dispatch contestuale
```

### 16.4 NOTE TECNICHE v814

1. **Nessuna nuova dipendenza.** Stesse dipendenze della v813.
2. **Dropdown visibili su mobile:** i pulsanti sono nascosti (`display: none`) ma i container
   dropdown (`#libThemesDropdown`, `#libToolsDropdown`) restano nel layout, quindi i menu
   aperti dall'hamburger appaiono correttamente.
3. **Backward compatibility:** `initLibraryMobileDropdown()` rimosso — non più necessario.
4. **CSS morto ripulito:** `.library-title`, `.library-subtitle` non più presenti.
5. **Hamburger condiviso:** stesso drawer per library e reader, voci filtrate dinamicamente.

---

## 19. EVOLUZIONE RESPONSIVE BRANCH — RIEPILOGO v813→v816

> Tutte le varianti responsive derivano da `older-version/noesis812-full-reader.html` (reader-only split).
> Ogni versione aggiunge miglioramenti incrementali mantenendo la struttura fully-offline.

### Timeline

```
older-version/noesis812-full-reader.html (v0.12, 6865 righe)
  │  Reader + Library, NO editor, NO snapshot UI
  │
  ├──▶ older-version/noesis813 (v0.13, ~7553 righe)
  │      + hamburger menu, + TOC overlay mobile, + touch zones
  │      + viewer 100% width su mobile, - floating nav btn desktop
  │
  ├──▶ older-version/noesis814 (v0.14)
  │      + hamburger contestuale (reader vs library)
  │      + toolbar pulita (solo icone attive)
  │      - dead CSS rimosso dalla v813
  │
  ├──▶ older-version/noesis815 (v0.15)
  │      + ⭐ statusbar con spine prev/next
  │      + ⭐ parent context TOC ("Part I → Chapter 1")
  │      + ⭐ WCAG tap targets 44×44px su mobile (.chap-nav-btn)
  │
  └──▶ noesis816 (v0.16) ★ CURRENT
         + nav mode popover in toolbar (#navModePopover)
         + chapter boundary detection in scroll mode
         + hamburger contestuale raffinato
         + statusbar tooltip full path (hover)
         + rifiniture CSS mobile
```

### Cambiamenti v813 → v814

| Modifica | Descrizione |
|----------|-------------|
| Hamburger contestuale | Due hamburger: `#hamburgerBtnLib` (library) e `#hamburgerBtn` (reader) |
| Toolbar pulita | Solo pulsanti attivi visibili; rimossi dead buttons |
| Dead CSS | Rimosso CSS non referenziato (`.library-title`, `.library-subtitle`) |
| `initLibraryMobileDropdown()` | Rimosso — gestione unificata nell'hamburger drawer |

### Cambiamenti v814 → v815

| Modifica | Descrizione |
|----------|-------------|
| ⭐ **Chapter Navigation Statusbar** | Nuovo `#status` con ◀/▶ spine nav, `#statusChapterName` centrato |
| ⭐ **Parent Context TOC** | `setStatusPath()` mostra "Parent → Chapter" invece del solo nome |
| ⭐ **WCAG Tap Targets** | `.chap-nav-btn` a 44×44px su `pointer: coarse` |
| `_findSpineIndex()` | Cerca href corrente nello spine EPUB |
| `goPrevChapter()` / `goNextChapter()` | Naviga capitoli via `rendition.display(spine.items[idx±1].href)` |
| `updateChapterNav()` | Disabilita ◀ al primo capitolo, ▶ all'ultimo |

### Cambiamenti v815 → v816

| Modifica | Descrizione |
|----------|-------------|
| ⭐ **Nav Mode Popover** | `#navModePopover` in toolbar, `#scrollModeBtn` con label dinamica |
| **Menubar Navigate semplificato** | `.rmb-nav-item` Page/Scroll diventano indicatori testuali |
| **`_syncNavModeBtn()`** | Sincronizza popover con stato `scrollMode` globale |
| **Statusbar Tooltip** | `#statusPath[data-full]:hover::after` mostra path completo |
| **Chapter Boundary Detection** | In scroll mode rileva cambio capitolo → aggiorna statusbar |

### Nuovi elementi HTML (v815+)

```html
<!-- Statusbar chapter navigation (v815+) -->
<div id="status">
  <button id="statusPrevBtn" class="chap-nav-btn" disabled>◀</button>
  <span id="statusChapterName">Select an EPUB file…</span>
  <button id="statusNextBtn" class="chap-nav-btn" disabled>▶</button>
</div>

<!-- Nav Mode Popover (v816) -->
<button id="scrollModeBtn" class="btn btn-icon nav-mode-btn">
  <span class="nav-mode-label">Page Mode</span>
</button>
<div id="navModePopover" class="nav-mode-popover">
  <div id="navOptPage" class="nav-mode-option active">Page Mode</div>
  <div id="navOptScroll" class="nav-mode-option">Scroll Mode</div>
</div>
```

### Flusso: Chapter Navigation via Spine

```
User click ◀ o ▶ nella statusbar
  → goPrevChapter() / goNextChapter()
  → _findSpineIndex(loc.start.href) — cerca href nello spine
  → rendition.display(book.spine.items[idx ± 1].href)
  → epub.js 'relocated' event → updateChapterNav()
    → disabled state aggiornato (primo/ultimo capitolo)
    → setStatusPath() con breadcrumb TOC
```

### Flusso: Parent Context Display

```
rendition.on('relocated', ...)
  → findBreadcrumbInToc(book.navigation.toc, loc.start.href, '')
  → setStatusPath("Part I › Chapter 1")
    → Split per ' › '
    → Se parts.length > 1:
      statusChapterName.textContent = parts[parts.length-2] + ' → ' + parts[parts.length-1]
      (es. "Part I → Chapter 1")
    → updateChapterNav()
```
