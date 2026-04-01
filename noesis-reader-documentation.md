# Noesis Reader — Documentazione Tecnica Completa

**Versione di riferimento:** noesis810.html  
**Data documento:** 2026-03-27  

---

## Indice

1. [Panoramica generale](#1-panoramica-generale)
2. [Architettura e layout dell'interfaccia](#2-architettura-e-layout-dellinterfaccia)
3. [Ciclo di vita: dalla Library al Reader](#3-ciclo-di-vita-dalla-library-al-reader)
4. [Mappa completa della toolbar del Reader](#4-mappa-completa-della-toolbar-del-reader)
5. [Sidebar TOC — Indice del libro](#5-sidebar-toc--indice-del-libro)
6. [Pannello User Bookmarks (Drawer)](#6-pannello-user-bookmarks-drawer)
7. [Sistema di evidenziazione (Highlight)](#7-sistema-di-evidenziazione-highlight)
8. [Menu Display — Typography, Themes, Interface](#8-menu-display--typography-themes-interface)
9. [Modalità di navigazione](#9-modalità-di-navigazione)
10. [Sistema di temi di lettura](#10-sistema-di-temi-di-lettura)
11. [Interazione con media: immagini e tabelle](#11-interazione-con-media-immagini-e-tabelle)
12. [Estrazione capitolo — funzione Extract](#12-estrazione-capitolo--funzione-extract)
13. [Save State — salvataggio stato di lettura](#13-save-state--salvataggio-stato-di-lettura)
14. [Sistema Help — banner, overlay, tasto ?](#14-sistema-help--banner-overlay-tasto-)
15. [Strutture di memorizzazione](#15-strutture-di-memorizzazione)
16. [Variabili globali del Reader](#16-variabili-globali-del-reader)
17. [Dipendenze tecniche](#17-dipendenze-tecniche)

---

## 1. Panoramica generale

Il **Noesis Reader** è l'ambiente di lettura EPUB integrato in `noesis810.html`. Opera nella stessa finestra dell'applicazione, in alternativa alla Library (le due viste si escludono a vicenda tramite `display: none / block`).

Caratteristiche principali:

- **Rendering EPUB via epub.js 0.3.93**: pagine EPUB renderizzate all'interno di iframe, con gestione completa di spine, TOC, CFI (Canonical Fragment Identifier) e rendition hooks.
- **Zero-server, zero-upload**: tutto avviene nel browser. I file EPUB sono letti da IndexedDB (dove sono stati salvati dalla Library) e ricostruiti in memoria.
- **Stato di lettura persistente**: posizione, tema, tipografia, highlights, bookmarks e impostazioni di interfaccia vengono salvati per ciascun libro in IndexedDB e ripristinati automaticamente alla riapertura.
- **Due modalità di lettura**: paginata (← →) e scroll continuo, entrambe con piena compatibilità touch/Android.
- **Estrazione capitoli**: funzione principale del Reader che esporta il capitolo corrente (o un albero di capitoli annidati) come documento HTML autonomo con immagini embedded in base64, aprendo contemporaneamente l'editor sn56.x.

---

## 2. Architettura e layout dell'interfaccia

### 2.1 Struttura DOM del Reader

```
#reader-view
├── <header>                         ← toolbar principale (gradient viola)
│   ├── #backToLibraryBtn            ← ← Library
│   ├── <strong>EPUB Reader</strong>
│   ├── #fileName                    ← nome libro corrente
│   ├── .toolbar                     ← gruppo pulsanti
│   │   ├── #toggleSidebarBtn        ← sidebar TOC
│   │   ├── #userBookmarksBtn        ← bookmarks personali
│   │   ├── .reader-highlight-dropdown
│   │   │   ├── #readerHighlightBtn  ← evidenzia
│   │   │   └── #readerHighlightMenu ← picker colore
│   │   ├── #displayBtn              ← menu Display (accordion)
│   │   │   └── #displayMenu
│   │   │       ├── #displaySecTypo  → #displayBodyTypo
│   │   │       ├── #displaySecThemes → #displayBodyThemes
│   │   │       └── #displaySecInterface → #displayBodyInterface
│   │   ├── #scrollModeBtn           ← toggle pagine/scroll
│   │   ├── #zoomBtn + #zoomPopupMain ← zoom toolbar
│   │   ├── #saveStateBtn            ← salva stato
│   │   ├── .extract-dropdown
│   │   │   ├── #extractChapterBtn   ← estrai capitolo
│   │   │   └── #extractMenu         ← current / tree
│   │   └── #readerHelpBtn           ← ?
│   │
│   │  [Popup DOM — presenti nell'<header> ma nascosti]:
│   ├── #typographyPopupMain         ← popup tipografia (legacy)
│   └── #interfacePopupMain          ← popup interfaccia (legacy)
│
├── #readerHelpBanner                ← banner primo avvio
├── #readerHelpOverlay               ← overlay guida pulsanti
├── #container
│   ├── #bookmarks (nav)             ← sidebar TOC (laterale sinistra)
│   └── #viewer                     ← area rendering EPUB (iframe)
├── #floatingPrevBtn                 ← ← pagina (sovrapposta)
├── #floatingNextBtn                 ← pagina → (sovrapposta)
├── #userBookmarksDrawer             ← pannello bookmark personali (slide)
└── #status                          ← barra di stato inferiore
    ├── #statusMsg
    ├── #statusSep
    └── #statusPath
```

### 2.2 Il popup DOM nascosti (Legacy Architecture)

Il codice contiene tre popup originariamente autonomi (`typographyPopupMain`, `themePopupMain`, `interfacePopupMain`) che ancora esistono nel DOM ma sono stati integrati nel menu **Display** accordion. L'architettura è la seguente:

- I popup originali rimangono nel DOM con `display: none !important` via CSS.
- `initDisplayMenu()` li "adotta" dinamicamente: quando una sezione dell'accordion viene aperta per la prima volta, il popup corrispondente viene fisicamente spostato (`appendChild`) nel `displayBodyXxx` e i suoi stili vengono azzerati per adattarsi al contenitore.
- Tutta la logica JavaScript dei popup (event listeners, valori, aggiornamenti) rimane intatta senza modifiche.

### 2.3 Barra di stato

La barra `#status` in fondo al Reader mostra:
- `#statusMsg`: messaggio di stato corrente (es. "Book opened: …", "Extracting chapter…")
- `#statusSep` + `#statusPath`: breadcrumb gerarchico del capitolo corrente (es. `Parte II › Capitolo 3 › Sezione 3.1`). Se il percorso ha più di 2 livelli viene condensato: `Parte II › … › Sezione 3.1`.

---

## 3. Ciclo di vita: dalla Library al Reader

### 3.1 Apertura di un libro

```
Utente clicca copertina libro in Library
      ↓
openBookFromLibrary(bookData)
      ↓
showLoading('Opening Book...')
      ↓
showReader()  ←  nasconde #library-view, mostra #reader-view
      ↓
currentBookId = bookData.id
currentBookTitle = bookData.title
      ↓
loadAndApplyBookState(currentBookId)
  → Ripristina: fontSize, lineHeight, currentTheme, scrollMode,
    dualPageMode, sidebarVisible, buttonZoom, interfaceSettings,
    readerHighlights, positionCFI
      ↓
loadUserBookmarksFromDB(currentBookId)
renderUbmList()
      ↓
Applica zoom toolbar, scroll mode btn, dual page btn,
font info, interface settings
      ↓
book = ePub(bookData.data)   ← crea istanza epub.js dall'ArrayBuffer in IDB
await book.ready
      ↓
recreateRendition()
  → Crea rendition nel #viewer
  → Registra hooks.content per stili, highlights, tabelle, media
  → Ripristina posizione (CFI → href → currentLocation → start)
  → applyTheme()
      ↓
Carica TOC, renderizza sidebar
      ↓
Abilita extractChapterBtn, saveStateBtn
      ↓
Mostra/nasconde floating nav buttons
      ↓
hideLoading()
```

### 3.2 Chiusura del Reader (ritorno alla Library)

```
Utente clicca "← Library"  (#backToLibraryBtn)
      ↓
showLibrary()
  → nasconde #reader-view
  → mostra #library-view
  → loadLibraryBooks()  (ricarica la lista)
```

Non viene eseguito alcun salvataggio automatico al ritorno. Il salvataggio è esclusivamente manuale (pulsante **Save State**).

### 3.3 Inizializzazione della rendition — `recreateRendition()`

Questa funzione è il cuore del rendering. Viene chiamata:
- All'apertura del libro
- Al cambio modalità scroll (paginate ↔ scroll)
- Al toggle sidebar (per aggiornare il padding)
- Al cambio dual page mode

```javascript
rendition = book.renderTo('viewer', {
  width: '100%',
  height: '100%',
  spread: (dualPageMode && !scrollMode) ? 'auto' : 'none',
  flow: scrollMode ? 'scrolled' : 'paginated',
  manager: 'default'  // Sempre 'default' — previene scroll offset issues
});
```

**Hooks registrati su ogni pagina:**

```javascript
rendition.hooks.content.register((contents) => {
  // 1. Stili CSS inline: max-width immagini, padding laterale, tabelle scroll-wrap, classi highlight
  // 2. Ripristino highlights salvati (readerHighlights array) con timeout 120ms
  // 3. Wrapping di tutte le <table> in .epub-table-scroll-wrap per scroll orizzontale
  // 4. Listener tap/click su immagini → postMessage({epubMediaTap: true, type:'img', data:{src,alt}})
  // 5. Listener tap su .epub-table-scroll-wrap → postMessage({epubMediaTap: true, type:'table', data:{html}})
  // 6. setTimeout(applyTheme, 50) → applica tema dopo il layout
});
```

**Padding laterale dinamico:**

Il padding del corpo del libro è calcolato a seconda dello stato dell'interfaccia:
```
basePadding = 40px   (margine bianco sempre presente)
buttonWidth = 25px   (aggiunto se floating buttons visibili, cioè !scrollMode && !sidebarVisible)
totalPadding = 40 o 65 px
```

---

## 4. Mappa completa della toolbar del Reader

La toolbar è un `<header>` con `background: linear-gradient(135deg, #667eea, #764ba2)` (personalizzabile dall'utente). I pulsanti sono della classe `.btn` con varianti di colore.

### Layout lineare da sinistra a destra

```
[← Library] [EPUB Reader] [fileName]  |  [Sidebar] [Bookmarks] [Highlight] [Display] | [Scroll] [% Zoom] | [Save State] | [Extract ▾] [?]
```

---

### 4.1 `#backToLibraryBtn` — Torna alla Library

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn` (background `#3b82f6`) |
| Icona | `bi-arrow-left` |
| Etichetta | "Library" |
| Azione | `showLibrary()` — ritorno alla Library senza salvataggio |
| Stato | Sempre abilitato |

---

### 4.2 `#toggleSidebarBtn` — Sidebar TOC

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon .btn-primary` (min-width 64px) |
| Icona | `bi-layout-sidebar` |
| Azione | Toggle visibilità sidebar `#bookmarks` |
| Effetto collaterale | Nasconde/mostra floating nav buttons; ricrea rendition per aggiornare padding |
| Stato | Disabilitato finché nessun libro è aperto |

**Dettaglio comportamento:**

```javascript
sidebarVisible = !sidebarVisible;
bookmarks.classList.toggle('hidden', !sidebarVisible);
// Se non in scroll mode: toggle floating buttons, ricrea rendition
// rendition.resize() via requestAnimationFrame + setTimeout(50ms)
```

La sidebar è posizionata dinamicamente tramite `ResizeObserver` sull'header: `bookmarks.style.top = (headerHeight + 20) + 'px'`.

---

### 4.3 `#userBookmarksBtn` — Bookmarks personali

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon` (background `rgba(251,191,36,0.25)`) |
| Icona | `bi-bookmark-star` (giallo ambra) |
| Badge | `#ubmBadge` — contatore bookmarks salvati (nascosto se 0) |
| Azione | Toggle drawer `#userBookmarksDrawer` |
| Stato | Sempre visibile, interazioni attive solo con libro aperto |

---

### 4.4 `#readerHighlightBtn` — Evidenziazione testo

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon` con classe dinamica `hl-yellow/hl-green/hl-pink/hl-remove` |
| Icona | `bi-highlighter` |
| Colore pulsante | Riflette il colore corrente selezionato |

**Comportamento smart:**
- Se c'è una selezione attiva (`_readerPendingCfi` valorizzato da evento `selected` di epub.js): applica o rimuove l'highlight immediatamente.
- Se non c'è selezione: apre il menu picker `#readerHighlightMenu`.

**Menu picker colori:**

| Opzione | Classe CSS | Classe highlight |
|---|---|---|
| Yellow | `hl-yellow` | `epub-hl-yellow` → `background: #ffeb3b` |
| Green | `hl-green` | `epub-hl-green` → `background: #a5d6a7` |
| Pink | `hl-pink` | `epub-hl-pink` → `background: #f8bbd9` |
| Remove | `hl-remove` | Rimuove annotation |

Il picker si chiude automaticamente al clic fuori. Il bordo blu del pulsante (`outline: 2px solid #3b82f6`) indica che c'è una selezione pending.

---

### 4.5 `#displayBtn` — Menu Display (accordion)

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon` |
| Icona | `bi-eye` |
| Azione | Toggle menu `#displayMenu` (dropdown accordion dark) |
| Contenuto | Tre sezioni collassabili: Typography, Themes, Interface |

Il menu è un dropdown `position: absolute`, sfondo `#1e293b`, bordo radius 10px. Le tre sezioni sono accordion: clic sull'header → apre il body corrispondente (chiudendo gli altri). Il contenuto delle sezioni viene "adottato" dai popup legacy al primo utilizzo.

#### Sezione Typography

Controlli:

| Controllo | ID pulsanti | Range | Default | Azione |
|---|---|---|---|---|
| Font Size | `fontMinus1` / `fontPlus1` / `fontReset` | 50% – 200%, step 1% | 100% | `applyTheme()` |
| Line Height | `lineHeightMinus` / `lineHeightPlus` / `lineHeightReset` | [1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.5, 3.0] | 1.2 | `applyTheme()` |
| Page View | `singlePageBtn` / `dualPageBtn` | single / dual | single | `recreateRendition()` |

- **Dual page mode**: disponibile solo in modalità paginata (non scroll). Usa `spread: 'auto'` nella rendition.
- Il valore corrente è mostrato nei badge `#fontInfo` e `#lineHeightInfo`.
- Tutti i reset riportano ai default e ricalcolano il tema.

#### Sezione Themes

Griglia di 15 swatch di colore organizzati in 5 gruppi. Descritti nel dettaglio nella [sezione 10](#10-sistema-di-temi-di-lettura).

#### Sezione Interface

| Controllo | ID | Default | Effetto |
|---|---|---|---|
| Toolbar Color | `toolbarColorPicker` | `#667eea` | Gradient header |
| Sidebar Color | `sidebarColorPicker` | `#ffffff` | Background sidebar |
| Nav Buttons Color | `navButtonsColorPicker` | `#667eea` | Floating nav buttons |
| Nav Opacity | `navOpacitySlider` | `0.7` | Opacity floating nav |
| Bookmark Drawer Color | `ubmDrawerColorPicker` | `#fffde7` | Background drawer |

Tutti hanno un pulsante reset (↺) che ripristina il valore di default. I cambiamenti sono applicati live tramite `applyInterfaceSettings()`.

---

### 4.6 `#scrollModeBtn` — Modalità scroll

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon` |
| Icona | `bi-arrow-down-up` |
| Stato attivo | Classe `.active` (verde) |
| Azione | Toggle `scrollMode` → `recreateRendition()` |

Al toggle:
- Scroll mode ON: `flow: 'scrolled'`, floating nav buttons nascosti, dual page disabilitato.
- Scroll mode OFF: `flow: 'paginated'`, floating nav buttons visibili (se sidebar chiusa).

---

### 4.7 `#zoomBtn` + `#zoomPopupMain` — Zoom toolbar buttons

| Proprietà | Valore |
|---|---|
| Etichetta | `%` |
| Popup | `#zoomPopupMain` (slider range) |
| Range | 90% – 130%, step 10% |
| Default | 100% |
| Variabile CSS | `--toolbar-btn-scale` sulla `.toolbar` |

Il popup si apre al clic e si chiude al clic fuori. Il valore viene applicato via CSS custom property che scala tutti i pulsanti della toolbar.

---

### 4.8 `#saveStateBtn` — Salva stato lettura

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon .btn-warning` (arancione, min-width 80px) |
| Icona | `bi-floppy` |
| Azione | `saveBookState()` |
| Feedback | Toast `#saveToast` |
| Stato | Disabilitato finché nessun libro è aperto |

Descritto in dettaglio nella [sezione 13](#13-save-state--salvataggio-stato-di-lettura).

---

### 4.9 `#extractChapterBtn` — Estrai capitolo

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon .btn-success` (verde) |
| Icona | `bi-file-earmark-arrow-down` + `bi-chevron-down` |
| Azione | Toggle dropdown `#extractMenu` |
| Stato | Disabilitato finché nessun libro è aperto |

**Dropdown menu `#extractMenu`:**

| Opzione | `data-mode` | Funzione | Descrizione |
|---|---|---|---|
| Current chapter only | `current` | `extractCurrentChapter()` | Estrae solo il capitolo foglia corrente |
| Current + all sublevels | `tree` | `collectAllSubchapters()` + `extractMultipleSections()` | Estrae il capitolo e tutti i sotto-capitoli annidati, mergiandoli in un unico documento |

Descritto in dettaglio nella [sezione 12](#12-estrazione-capitolo--funzione-extract).

---

### 4.10 `#readerHelpBtn` — Guida rapida

| Proprietà | Valore |
|---|---|
| Classe CSS | `.btn .btn-icon .btn-help` |
| Etichetta | `?` |
| Azione | `openOverlay('readerHelpOverlay')` |
| Keyboard shortcut | Tasto `?` (quando il Reader è visibile) |

---

### 4.11 Floating nav buttons (fuori toolbar)

| ID | Icona | Azione |
|---|---|---|
| `#floatingPrevBtn` | `bi-chevron-left` | `rendition.prev()` |
| `#floatingNextBtn` | `bi-chevron-right` | `rendition.next()` |

Visibili solo in modalità paginata **e** sidebar chiusa. Posizionati in overlay sovrapposto al viewer. Colore e opacità personalizzabili dal menu Interface.

---

## 5. Sidebar TOC — Indice del libro

### 5.1 Struttura

Il `<nav id="bookmarks">` è un pannello laterale sinistro con lista gerarchica dell'indice EPUB. È costruito dalla funzione `renderBookmarksSimple(toc)` dopo il caricamento del libro.

### 5.2 Rendering gerarchico

La funzione `createList(items, level, ancestorPath)` crea ricorsivamente una struttura `<ul>/<li>`:

- **Livello 1:** `ul` senza classi
- **Livello 2:** `ul.sub.level-2`
- **Livello 3+:** `ul.sub`

Ogni `<li>` ha:
- Classe `expandable` se ha sotto-voci, `leaf` se è foglia.
- Attributo `translate="yes"` per il supporto alla traduzione automatica del browser.
- Testo = `item.label` (nome del capitolo/sezione).

**Clic su una voce TOC:**
1. Se `item.href`: naviga tramite `navigateToHref(item.href)` e aggiorna `statusPath` con il breadcrumb completo.
2. Se ha sotto-voci: toggle classe `open` per espandere/collassare.

### 5.3 Navigazione `navigateToHref(href)`

La funzione gestisce due casi distinti:

**In modalità paginata:**
- Prova direttamente `rendition.display(target)`.
- Se fallisce: smart resolution — estrae `fileName` dall'href, cerca nella spine per nome file, poi riprova con o senza anchor.

**In modalità scroll:**
- La navigazione in scroll mode è problematica perché la ricreazione automatica della rendition causa backward-scroll.
- Soluzione: distrugge la rendition corrente, ricrea una nuova con `flow: 'scrolled'` ma sempre `manager: 'default'` (non `continuous`), naviga al `spineItem.href`.
- Questo previene il comportamento di auto-loading di capitoli adiacenti.

### 5.4 Posizionamento dinamico

Il top della sidebar viene calcolato dinamicamente tramite `ResizeObserver` sull'header e `window.resize` + `orientationchange`:

```javascript
bookmarks.style.top = (header.getBoundingClientRect().height + 20) + 'px';
```

---

## 6. Pannello User Bookmarks (Drawer)

### 6.1 Struttura

Il drawer `#userBookmarksDrawer` è un pannello che scivola dall'alto (con animazione CSS) subito sotto l'header, senza nascondere il contenuto sottostante. Il suo colore di sfondo è personalizzabile (default `#fffde7`, giallo pallido).

```
#userBookmarksDrawer
├── #ubmHeader
│   ├── <h3> My Bookmarks
│   ├── #ubmNewBtn (+New Bookmark)
│   └── #ubmCloseBtn (✕)
└── #ubmList
    ├── .ubm-item (per ogni bookmark)
    │   ├── .ubm-item-body (cliccabile → naviga)
    │   │   ├── .ubm-chapter  (titolo capitolo, max 55 char)
    │   │   ├── .ubm-preview  (estratto testo, max 100 char)
    │   │   ├── .ubm-label    (se presente: "🏷 etichetta")
    │   │   └── .ubm-date     (data creazione)
    │   └── .ubm-delete-btn (✕)
    └── .ubm-empty  (se lista vuota)
```

### 6.2 Creazione di un bookmark — `createUserBookmark()`

La funzione raccoglie automaticamente:

1. **CFI e href correnti** tramite `rendition.currentLocation().start`.
2. **Titolo del capitolo**: ricerca nel TOC tramite `findBreadcrumbInToc()`, prende l'ultimo segmento del percorso.
3. **Preview del testo** (100 caratteri): estrae il testo completo del documento iframe, calcola l'offset basato sulla posizione della pagina (`loc.start.displayed.page / total`), prende 100 caratteri iniziando 400 posizioni dopo l'offset. Questo garantisce un preview del testo visibile alla posizione corrente.
4. **Etichetta opzionale**: `window.prompt('Optional label…')`.

**Struttura di un bookmark:**
```javascript
{
  id:        "1711530000000_abc12",    // timestamp + random
  chapter:   "Capitolo III",           // nome capitolo (max 55 char)
  preview:   "…testo del libro…",      // estratto testo (100 char)
  label:     "Punto importante",        // etichetta utente (opzionale)
  cfi:       "epubcfi(/6/4[s3]!/4/2)", // posizione CFI precisa
  href:      "OEBPS/chapter3.xhtml",   // fallback href
  createdAt: 1711530000000             // timestamp
}
```

### 6.3 Navigazione da un bookmark

Clic sul body del bookmark:
1. Se `bm.cfi`: `rendition.display(bm.cfi)` — navigazione precisa alla posizione.
2. Altrimenti se `bm.href`: `navigateToHref(bm.href)` — navigazione al capitolo.
3. Chiude il drawer.

### 6.4 Persistenza

I bookmarks vengono salvati dentro il record del libro in `EpubLibraryDB`, come campo `userBookmarks: []` dell'oggetto book. Vengono caricati in memoria (`userBookmarks` array) all'apertura del libro e riscritti ad ogni modifica (aggiunta, eliminazione).

**Non** vengono inclusi nel `savedState` — hanno una propria logica di persistenza separata.

### 6.5 Badge sul pulsante

Il badge numerico `#ubmBadge` sul pulsante `#userBookmarksBtn` mostra il numero di bookmark. È nascosto (`display: none`) se `userBookmarks.length === 0`.

---

## 7. Sistema di evidenziazione (Highlight)

### 7.1 Principio di funzionamento

Il sistema di highlight usa le **annotazioni di epub.js** (`rendition.annotations.highlight()`) identificate da **CFI** (Canonical Fragment Identifier). I CFI sono forniti dall'evento `rendition.on('selected', ...)` che scatta quando l'utente seleziona testo nel viewer iframe.

### 7.2 Flusso di selezione e applicazione

```
Utente seleziona testo nel viewer iframe
      ↓
epub.js emette evento 'selected' con cfiRange
      ↓
_readerPendingCfi = cfiRange
_readerHlHasSelection = true
→ Il pulsante Highlight mostra bordo blu
      ↓
Utente clicca pulsante Highlight
      ↓
Se hasSelection:
  → applyReaderHighlight() OPPURE removeReaderHighlight()
  → _readerPendingCfi = null
  → Bordo blu rimosso
Altrimenti:
  → Apre il menu picker colori
```

### 7.3 Applicazione e rimozione

**Applicazione (`applyReaderHighlight`):**
```javascript
// Deduplicazione: rimuove highlight preesistente stesso CFI
readerHighlights = readerHighlights.filter(h => h.cfi !== cfi);
rendition.annotations.remove(cfi, 'highlight');
// Aggiunge nuovo
readerHighlights.push({ cfi: cfi, color: currentReaderHighlightColor });
rendition.annotations.highlight(cfi, {}, () => {}, 'epub-hl-' + currentReaderHighlightColor);
// Pulisce selezione negli iframe
```

**Rimozione (`removeReaderHighlight`):**
```javascript
rendition.annotations.remove(cfi, 'highlight');
readerHighlights = readerHighlights.filter(h => h.cfi !== cfi);
```

### 7.4 Persistenza e ripristino

Gli highlight sono salvati nell'array `readerHighlights: [{cfi, color}]` e inclusi nel `savedState` del libro in IDB.

Al ripristino (apertura libro o cambio pagina), l'hook `rendition.hooks.content.register` ripristina tutti gli highlight con un timeout di 120ms per garantire che epub.js abbia completato il layout:

```javascript
readerHighlights.forEach(hl => {
  try {
    rendition.annotations.remove(hl.cfi, 'highlight');
    rendition.annotations.highlight(hl.cfi, {}, () => {}, 'epub-hl-' + hl.color);
  } catch(e) { /* CFI stale — ignora */ }
});
```

I CFI stale (non più validi, es. dopo ricompilazione del libro) vengono ignorati silenziosamente.

### 7.5 Classi CSS degli highlight

Iniettate nell'iframe via style tag nell'hook content:
```css
.epub-hl-yellow { background-color: #ffeb3b !important; }
.epub-hl-green  { background-color: #a5d6a7 !important; }
.epub-hl-pink   { background-color: #f8bbd9 !important; }
```

### 7.6 Colore corrente del pulsante

Il pulsante Highlight cambia colore per riflettere la modalità corrente:
- `hl-yellow`: background giallo (#ffeb3b)
- `hl-green`: background verde (#a5d6a7)
- `hl-pink`: background rosa (#f8bbd9)
- `hl-remove`: stile "rimozione" (indicato visivamente)

---

## 8. Menu Display — Typography, Themes, Interface

### 8.1 Architettura accordion

Il menu `#displayMenu` è un accordion a tre sezioni che si apre come dropdown dropdown dal pulsante `#displayBtn`. È implementato dalla funzione `initDisplayMenu()`.

**Logica di apertura/chiusura:**

```javascript
// Apertura menu principale
displayBtn.addEventListener('click', () => {
  _closeAllReaderMenus(); // chiude tutti gli altri menu aperti
  displayMenu.classList.toggle('open');
});

// Clic su header sezione
headerEl.addEventListener('click', () => {
  var isOpen = body.classList.contains('open');
  SECTIONS.forEach(s => _toggle(s, false)); // chiude tutte
  if (!isOpen) _toggle(sec, true);           // apre solo questa
});
```

**Adozione dei popup legacy (`_embedPopup`):**

Al primo utilizzo di ogni sezione, il popup legacy corrispondente viene "adottato":
```javascript
function _embedPopup(sec) {
  if (sec._embedded) return; // già fatto
  sec._embedded = true;
  var popup = document.getElementById(sec.popupId);
  var body  = document.getElementById(sec.bodyId);
  // Reset tutti gli stili floating del popup
  popup.style.display    = 'block';
  popup.style.position   = 'relative';
  popup.style.boxShadow  = 'none';
  // ... altri reset
  var h3 = popup.querySelector('h3');
  if (h3) h3.style.display = 'none'; // nasconde titolo ridondante
  body.appendChild(popup); // sposta fisicamente nel corpo accordion
}
```

### 8.2 Interazione con altri menu

La funzione `_closeAllReaderMenus()` chiude tutti i menu aperti contemporaneamente:
- `typographyPopupMain`, `themePopupMain`, `interfacePopupMain`
- `extractMenu`
- `readerHighlightMenu`
- `displayMenu` (con tutti i corpi sezione)

Viene chiamata:
- All'apertura del Display menu
- Quando il pulsante Extract viene cliccato (se Display era aperto)
- Quando il pulsante Highlight viene cliccato (se Display era aperto)

---

## 9. Modalità di navigazione

### 9.1 Navigazione paginata (default)

```
flow: 'paginated', manager: 'default', spread: 'none' (o 'auto' se dual page)
```

- **← / → frecce tastiera**: `rendition.prev()` / `rendition.next()`
- **Floating nav buttons**: visibili se sidebar è chiusa
- **Dual page**: spread 'auto' — epub.js distribuisce il contenuto su due colonne
- Breadcrumb aggiornato automaticamente sull'evento `rendition.on('relocated', ...)`

### 9.2 Modalità scroll continuo

```
flow: 'scrolled', manager: 'default'
```

- Il contenuto si estende verticalmente senza interruzioni di pagina.
- I floating nav buttons vengono nascosti.
- Il dual page è disabilitato e forzato a single.
- La navigazione tramite TOC usa una procedura speciale (ricrea rendition con manager 'default') per evitare il backward-scroll.

### 9.3 Breadcrumb automatico

L'evento `rendition.on('relocated', (location) => {...})` scatta ad ogni cambio pagina. Usa `findBreadcrumbInToc(book.navigation.toc, location.start.href, '')` per costruire il percorso completo, che viene poi condensato in `statusPath`.

Algoritmo di condensazione:
- ≤ 2 livelli: mostra tutto (es. `Parte II › Capitolo 3`)
- > 2 livelli: `Parte II › … › Sezione 3.1`
- Il full path è mantenuto in `data-full` per accessibilità.

### 9.4 Navigazione da link interni EPUB

I link interni all'EPUB (es. note a piè di pagina, rimandi) sono intercettati dall'evento `rendition.on('linkClicked', (href) => navigateToHref(href))`.

### 9.5 Keyboard shortcut

```javascript
document.addEventListener('keydown', (e) => {
  // ? → toggle overlay help Reader (solo se Reader visibile)
});
```
Arrow keys (← →) per la navigazione pagine sono gestite nativamente da epub.js in modalità paginata.

---

## 10. Sistema di temi di lettura

### 10.1 Struttura dati `THEME_COLORS`

15 temi definiti come oggetti `{bg, fg, label, group}`:

| Gruppo | Temi | Sfondo | Testo |
|---|---|---|---|
| White | normal (White) | `#ffffff` | `#000000` |
| White | softwhite (Soft White) | `#fafafa` | `#1a1a1a` |
| Cream / Sepia | cream | `#fdf6e3` | `#3b2e1a` |
| Cream / Sepia | sepia | `#f4ecd8` | `#3b2e1a` |
| Cream / Sepia | parchment | `#eee5d3` | `#33291a` |
| Light Gray | gray | `#e5e7eb` | `#1f2937` |
| Light Gray | coolgray | `#dfe3e8` | `#1c2530` |
| Light Gray | warmgray | `#e8e4df` | `#2c2419` |
| Medium Gray | midgray | `#b0b8c1` | `#1a1f26` |
| Medium Gray | slate | `#94a3b8` | `#0f172a` |
| Dark Gray | darkgray | `#4b5563` | `#f3f4f6` |
| Dark Gray | charcoal | `#374151` | `#e5e7eb` |
| Dark / Black | dark | `#1a1a1a` | `#d4d4d4` |
| Dark / Black | midnight | `#0f1117` | `#c8cdd3` |
| Dark / Black | truedark (True Black) | `#000000` | `#b8b8b8` |

### 10.2 Applicazione del tema — `applyTheme()`

```javascript
rendition.themes.register('custom', {
  body: {
    'background': `${active.bg} !important`,
    'color': `${active.fg} !important`,
    'font-size': `${fontSize}% !important`,
    'line-height': `${lineHeight} !important`
  },
  'p, div, span, li, h1, h2, h3, h4, h5, h6': {
    'font-size': `${fontSize}% !important`,
    'color': `${active.fg} !important`,
    'line-height': `${lineHeight} !important`
  }
});
rendition.themes.select('custom');
```

Il tema è applicato all'interno dell'iframe via il sistema di theming di epub.js. Le variazioni di fontSize e lineHeight sono incluse nello stesso tema CSS.

### 10.3 Swatch attiva

Nella griglia temi la swatch attiva riceve la classe `.active` (bordo/indicatore). Aggiornata da `updateThemeSwatchActive()` al cambio tema.

---

## 11. Interazione con media: immagini e tabelle

### 11.1 Wrapping delle tabelle

Ogni `<table>` presente nel contenuto EPUB viene wrappata in un `<div class="epub-table-scroll-wrap">` con:
```css
.epub-table-scroll-wrap {
  display: block;
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.epub-table-scroll-wrap table {
  table-layout: auto !important;
  width: auto !important;
}
```

Questo permette lo scroll orizzontale su mobile per tabelle larghe.

### 11.2 Sistema Media Tap (postMessage)

Quando l'utente tocca/clicca un'immagine o una tabella nell'iframe EPUB, viene inviato un `postMessage` al parent:

```javascript
window.parent.postMessage({
  epubMediaTap: true,
  type: 'img',    // o 'table'
  data: { src, alt }  // o { html }
}, '*');
```

**Nel parent (`noesis810.html`):**

```
postMessage ricevuto
      ↓
pending = { type, data }
Mostra #readerMediaDialog (posizionato al centro viewport)
  → [Preview] [Exit]
```

Clic **Preview**:
- Se immagine: `fsContent.innerHTML = <img src="…">` in `#readerMediaFullscreen`
- Se tabella: `fsContent.innerHTML = tableHTML` in `#readerMediaFullscreen`
- `fsCaption.textContent = alt` (per immagini)
- Apre overlay fullscreen

Clic **Exit**: nasconde dialog, annulla pending.

### 11.3 Overlay fullscreen media

`#readerMediaFullscreen` è un overlay a schermo intero (sfondo scuro) che mostra l'immagine o la tabella in dimensioni massime. Chiudibile tramite `#readerFsClose` (✕).

**Prevenzione gesture iOS**: le immagini nell'iframe hanno `webkitTouchCallout: 'none'` e `userSelect: 'none'` per evitare il menu contestuale iOS.

**Gestione touchMoved**: sia per immagini che per tabelle, un flag `touchMoved` previene che un drag/scroll venga interpretato come tap.

---

## 12. Estrazione capitolo — funzione Extract

### 12.1 Modalità "Current chapter only" — `extractCurrentChapter()`

**Flusso:**

```
1. Ottieni posizione corrente: rendition.currentLocation()
2. Ricava currentHref → currentSpineItem dalla spine
3. Cerca nell'TOC: trovaTocEntry() → chapterTitle
4. Carica la section: section.load(book.load.bind(book))
5. Clona il documento: doc.cloneNode(true)
6. Per ogni <img> nel clone:
   - Skip se già base64 o URL assoluto
   - findAndLoadImage(src, sectionPath):
     * Costruisce percorso relativo dalla section
     * Normalizza (risolve ../ e ./)
     * Prova varianti: con/senza slash iniziale, path originale, match per filename
     * Legge da zip: zip.files[normalizedPath].async('arraybuffer')
   - Rilevamento MIME type dai magic bytes (PNG, GIF, JPEG, WebP, SVG)
   - Converte in base64 (in chunk da 32KB per evitare stack overflow su mobile)
   - Sostituisce src con data URL
7. Estrae CSS:
   - Tag <style> inline
   - Fogli CSS linkati (caricati tramite book.archive.request())
   - Computed styles (fontFamily, fontSize, lineHeight)
8. htmlContent = clonedDoc.body.innerHTML
9. Genera chapterId, firstSnapshot (isOrigin: true)
10. Salva chapterRecord in noesisDB
11. Scarica coppia file: noesis-extract-…html + noesis-origin-…html
12. Apre sn56.x con payload chapter
```

### 12.2 Modalità "Current + all sublevels" — `extractMultipleSections()`

**Algoritmo:**

```
1. findTocEntry() → trova il capitolo corrente nel TOC
2. collectAllSubchapters(tocEntry):
   → Raccolta ricorsiva: [root, child1, child2, grandchild1, ...]
3. extractMultipleSections(allEntries, overallTitle):
   → Set<baseHref> per deduplicare sezioni (un file spine può apparire in più voci TOC)
   → Per ogni tocEntry NON già processato:
     * Stesso algoritmo di findAndLoadImage
     * CSS estratto SOLO dalla prima sezione
     * HTML del body aggiunto a combinedHTML
     * Separatore: <div class="section-divider"><h2>label</h2></div>
4. overallTitle = "NomeTitoloRoot (Complete)"
5. Stesso finale: chapterId, IDB, file disk, sn56.x
```

**Deduplicazione sezioni:** ogni `href` viene normalizzato rimuovendo l'anchor (`#`). Un Set mantiene traccia dei base path già elaborati, evitando di duplicare il contenuto di sezioni che appaiono più volte nel TOC sotto voci diverse.

### 12.3 Output dell'estrazione (identico per entrambe le modalità)

Ogni estrazione produce **quattro output simultanei**:

| # | Output | Descrizione |
|---|---|---|
| 1 | `noesisDB` — chapterRecord con snapshot `origin-…` | Snapshot originale in IDB per accesso dalla Library |
| 2 | `noesis-extract-…html` | File HTML leggibile offline, senza meta tag noesis |
| 3 | `noesis-origin-…html` (con 1.5s delay) | File HTML con meta tag noesis, reimportabile in Library |
| 4 | sn56.x in nuova tab | Editor aperto con il contenuto estratto |

### 12.4 Conversione immagini in base64

La conversione usa chunk da 32768 byte (`0x8000`) per evitare stack overflow su dispositivi Android con memoria limitata:

```javascript
const bytes = new Uint8Array(imgData);
const chunkSize = 0x8000;
let binary = '';
for (let i = 0; i < bytes.length; i += chunkSize) {
  const chunk = bytes.subarray(i, i + chunkSize);
  binary += String.fromCharCode.apply(null, chunk);
}
const base64 = btoa(binary);
```

---

## 13. Save State — salvataggio stato di lettura

### 13.1 Cosa viene salvato

La funzione `saveBookState()` crea un oggetto `stateToSave` che comprende:

```javascript
{
  // 1. Tipografia
  fontSize: 100,           // 50-200%
  lineHeight: 1.2,         // da array preset

  // 2. Tema
  theme: 'normal',         // chiave THEME_COLORS

  // 3. Modalità navigazione
  scrollMode: false,
  dualPageMode: false,
  sidebarVisible: false,

  // 4. Zoom toolbar
  buttonZoom: 100,         // 90-130%

  // 5. Impostazioni interfaccia
  interface: {
    toolbarColor: '#667eea',
    sidebarColor: '#ffffff',
    navButtonsColor: '#667eea',
    navOpacity: 0.7,
    ubmDrawerColor: '#fffde7'
  },

  // 6. Posizione di lettura
  position: {
    cfi:  'epubcfi(/6/4[s3]!/4/2)',  // posizione CFI precisa
    href: 'OEBPS/chapter3.xhtml',     // href fallback
    timestamp: 1711530000000
  },

  // 7. Highlights
  readerHighlights: [
    { cfi: 'epubcfi(…)', color: 'yellow' },
    { cfi: 'epubcfi(…)', color: 'green' }
  ],

  savedAt: 1711530000000
}
```

### 13.2 Dove viene salvato

Lo stato è scritto nel **record del libro in `EpubLibraryDB`** come campo `savedState`:

```javascript
const updatedBook = {
  id: bookData.id,
  title: bookData.title,
  author: bookData.author,
  data: bookData.data,           // ArrayBuffer EPUB (non modificato)
  cover: bookData.cover,
  addedAt: bookData.addedAt,
  savedState: stateToSave        // ← aggiunto/aggiornato
};
store.put(updatedBook);
```

I `userBookmarks` sono salvati separatamente (nella stessa store, ma aggiornati in un'operazione separata tramite `saveUserBookmarksToDB()`).

### 13.3 Toast di feedback

Il Save State usa il sistema toast `#saveToast`:
- "Saving…" (durante il salvataggio, con timeout 4s)
- "State saved ✓" (al completamento, 2.5s)
- "Save failed" (in caso di errore, 3s)

### 13.4 Ripristino — `loadAndApplyBookState(bookId)`

Viene chiamato all'apertura del libro, **prima** di creare la rendition. Ripristina tutte le variabili di stato in memoria. Se non c'è `savedState` (primo accesso al libro), applica i default.

La **posizione CFI** viene restituita come valore di ritorno e applicata dopo che la rendition è creata e pronta:

```javascript
const savedPosition = await loadAndApplyBookState(currentBookId);
// ...crea rendition, applyTheme...
if (savedPosition && savedPosition.cfi) {
  try { await rendition.display(savedPosition.cfi); }
  catch (e) { await rendition.display(); } // fallback all'inizio
}
```

---

## 14. Sistema Help — banner, overlay, tasto ?

### 14.1 Banner primo avvio

Il banner `#readerHelpBanner` è mostrato la prima volta che si entra nel Reader (primo accesso assoluto). Viene nascosto al clic di ✕ e la chiave `'noesis-help-seen-reader'` viene scritta in `localStorage` per non mostrarlo più.

**Contenuto:**
- "☰ Sidebar — table of contents & bookmarks"
- "👁 Display — typography, themes & interface"
- "💾 Save State — save position & settings"
- "📄 Extract — extract chapter for annotation"
- "? — open this guide at any time"

### 14.2 Help overlay completo

L'overlay `#readerHelpOverlay` si apre tramite il pulsante `?` o il tasto `?` da tastiera (solo se Reader visibile). È strutturato in gruppi:

| Gruppo | Contenuto |
|---|---|
| Navigation & View | Sidebar, Bookmarks, Scroll Mode, % Zoom |
| Appearance & Reading | Display (Typography/Themes/Interface), Highlight |
| Saving & Extraction | Save State, Extract (current / +sublevels) |
| Keyboard | ← →, ? |

Chiudibile tramite pulsante ✕, clic fuori dall'overlay, o tasto `?`.

### 14.3 Tasto tastiera `?`

```javascript
document.addEventListener('keydown', function(e) {
  if (e.key !== '?' || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  var readerVisible = !readerView.classList.contains('hidden');
  if (readerVisible) {
    var ro = document.getElementById('readerHelpOverlay');
    if (ro.classList.contains('visible')) closeOverlay('readerHelpOverlay');
    else openOverlay('readerHelpOverlay');
  }
});
```

---

## 15. Strutture di memorizzazione

### 15.1 Database `EpubLibraryDB` — i libri

**Nome:** `EpubLibraryDB` · **Versione:** 1 · **Store:** `books` (keyPath: `id`)

```javascript
// Record libro completo
{
  id:           "1711530000000",          // timestamp string (chiave)
  title:        "Ulysses",
  author:       "James Joyce",
  data:         ArrayBuffer,              // file EPUB grezzo (~MB)
  cover:        "data:image/jpeg;base64,…", // copertina base64
  addedAt:      1711530000000,

  // Aggiunto da saveBookState()
  savedState: {
    fontSize:       100,
    lineHeight:     1.2,
    theme:          'normal',
    scrollMode:     false,
    dualPageMode:   false,
    sidebarVisible: false,
    buttonZoom:     100,
    interface: {
      toolbarColor:    '#667eea',
      sidebarColor:    '#ffffff',
      navButtonsColor: '#667eea',
      navOpacity:      0.7,
      ubmDrawerColor:  '#fffde7'
    },
    position: {
      cfi:       'epubcfi(/6/4[s3]!/4/2/10)',
      href:      'OEBPS/chapter3.xhtml',
      timestamp: 1711530000000
    },
    readerHighlights: [
      { cfi: 'epubcfi(…)', color: 'yellow' }
    ],
    savedAt: 1711530000000
  },

  // Aggiunto da saveUserBookmarksToDB()
  userBookmarks: [
    {
      id:        "1711530000001_abc12",
      chapter:   "Capitolo III",
      preview:   "…testo estratto…",
      label:     "Nota importante",
      cfi:       'epubcfi(/6/4[s3]!/4/2)',
      href:      'OEBPS/chapter3.xhtml',
      createdAt: 1711530000001
    }
  ]
}
```

**Gestione errori di versione:** se il database ha una versione incompatibile (`VersionError`), viene cancellato (`deleteDatabase()`) e ricreato automaticamente.

### 15.2 Database `noesisDB` — capitoli estratti

**Nome:** `noesisDB` · **Versione:** 1 · **Store:** `extractedChapters` (keyPath: `chapterId`)

Usato **esclusivamente** dall'estrazione: il Reader scrive qui alla fine di ogni estrazione, ma non legge mai da questo database durante la sessione di lettura. La Library legge questo database per mostrare i capitoli estratti e i loro snapshot.

```javascript
{
  chapterId:   "ch_1711530000000_987654",
  bookName:    "Ulysses",
  chapterName: "Proteus",
  createdAt:   "2026-03-27T14:25:30.000Z",
  snapshots: [
    {
      snapshotId:  "snap_1711530000001_111222",
      createdAt:   "2026-03-27T14:25:30.000Z",
      bookName:    "Ulysses",
      chapterName: "Proteus",
      description: "origin-20260327-142530",
      isOrigin:    true,
      content:     "<p>…HTML capitolo estratto…</p>"
    }
  ]
}
```

### 15.3 `localStorage`

| Chiave | Tipo | Uso |
|---|---|---|
| `'noesis-help-seen-reader'` | `'1'` | Flag primo accesso Reader (banner visto) |
| `'noesis-help-seen-library'` | `'1'` | Flag primo accesso Library (banner visto) |
| `'noesis-lib-theme'` | `'dark'` / `'light'` | Tema corrente della Library |

---

## 16. Variabili globali del Reader

```javascript
// ── Stato corrente libro ──
let book = null;               // istanza epub.js Book
let rendition = null;          // istanza epub.js Rendition

// ── Tipografia ──
let fontSize = 100;            // percentuale, 50-200
let lineHeight = 1.2;          // da preset array
let lineHeights = [1, 1.2, 1.4, 1.6, 1.8, 2.0]; // stepped values

// ── Modalità navigazione ──
let scrollMode = false;        // false = paginato, true = scroll
let dualPageMode = false;      // spread: 'auto' in paginate
let sidebarVisible = false;    // visibilità sidebar TOC

// ── Tema ──
let currentTheme = 'normal';   // chiave THEME_COLORS

// ── Posizione ──
let currentLocation = null;    // { start: { cfi, href } }

// ── Interfaccia ──
let buttonZoom = 100;          // zoom pulsanti toolbar, 90-130%
let interfaceSettings = {
  toolbarColor: '#667eea',
  sidebarColor: '#ffffff',
  navButtonsColor: '#667eea',
  navOpacity: 0.7,
  ubmDrawerColor: '#fffde7'
};
let defaultInterfaceSettings = { ...interfaceSettings }; // immutabile

// ── Libro corrente ──
let currentBookId = null;      // id del libro in EpubLibraryDB
let currentBookTitle = '';     // titolo per estrazione e UI

// ── Highlights ──
let readerHighlights = [];           // [{cfi, color}] - persistiti
let currentReaderHighlightColor = 'yellow';
let _readerHlHasSelection = false;   // selezione attiva in iframe
let _readerPendingCfi = null;        // CFI dalla selezione corrente

// ── User Bookmarks ──
let userBookmarks = [];        // [{id, chapter, preview, label, cfi, href, createdAt}]
```

---

## 17. Dipendenze tecniche

### 17.1 Librerie esterne (caricate in noesis810.html)

| Libreria | Versione | URL | Uso nel Reader |
|---|---|---|---|
| epub.js | 0.3.93 | `cdn.jsdelivr.net/npm/epubjs@0.3.93` | Rendering EPUB, spine, TOC, CFI, annotations |
| JSZip | 3.10.1 | `cdn.jsdelivr.net/npm/jszip@3.10.1` | Accesso agli asset del file EPUB (immagini, CSS) |
| Bootstrap Icons | 1.11.3 | `cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3` | Tutte le icone dell'interfaccia |

### 17.2 API Browser utilizzate

| API | Uso |
|---|---|
| `IndexedDB` | `EpubLibraryDB` (libri, stato, bookmarks) e `noesisDB` (capitoli estratti) |
| `localStorage` | Flag help banner, tema Library |
| `URL.createObjectURL / Blob` | Creazione Blob URL per sn56.x |
| `window.open(url, '_blank', '')` | Apertura sn56.x (terzo argomento esplicito per preservare opener) |
| `postMessage` | Comunicazione Reader→parent per media tap; IDB bridge sn56.x→parent |
| `ResizeObserver` | Aggiornamento dinamico top sidebar al resize header |
| `FileReader` | Non usato nel Reader direttamente (usato in Library per import EPUB) |
| `DOMParser` | Import snapshot da file HTML |
| `window.showDirectoryPicker` | Folder picker per import snapshot (solo desktop Chrome/Edge) |

### 17.3 epub.js — eventi utilizzati

| Evento | Handler | Uso |
|---|---|---|
| `rendition.on('relocated', ...)` | `setStatusPath` | Aggiornamento breadcrumb ad ogni cambio pagina |
| `rendition.on('selected', ...)` | `_readerPendingCfi = cfiRange` | Cattura selezione per highlight |
| `rendition.on('linkClicked', ...)` | `navigateToHref` | Intercettazione link interni EPUB |
| `rendition.hooks.content.register(...)` | Styles, highlights, tabelle, media | Injector per ogni pagina caricata |

---

*Fine documentazione — noesis-reader-documentation.md*
