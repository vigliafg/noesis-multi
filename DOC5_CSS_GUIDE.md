# NOESIS810 — Documento 5: Guida CSS e Classi

> Fonte: `noesis810.html` righe 10–2357 — Aggiornato: 2026-03-27

---

## ORGANIZZAZIONE DEL CSS

Il CSS è inline nel `<style>` del `<head>`. È diviso in blocchi commentati:

| Blocco | Righe approx. | Contenuto |
|--------|---------------|-----------|
| Global & Utils | 10–30 | Reset base, `.hidden` |
| Library — Theming | 32–560 | Tutto il CSS della biblioteca |
| Loading Overlay | 556–590 | `#loading-overlay`, `.spinner` |
| Reader — Layout | 592–750 | `#reader-view`, `header`, `#container`, `#viewer`, `#bookmarks` |
| Reader — Toolbar buttons | 750–900 | `.btn`, `.toolbar`, `.toolbar-group`, `.toolbar-spacer` |
| User Bookmarks Drawer | 800–970 | `#userBookmarksDrawer`, `.ubm-*` |
| Status bar | ~970 | `#status`, `#statusMsg`, `#statusPath` |
| Typography Popup | ~1050 | `.typography-popup`, `.typography-row`, `.typography-controls` |
| Theme Popup | ~1200 | `.theme-popup`, `.theme-group`, `.theme-swatch` |
| Interface Popup | ~1300 | (usa stesse classi di typography-popup) |
| Zoom Popup | ~1400 | `.toolbar-zoom-popup`, `.zoom-sign` |
| Display Menu (accordion) | ~1450 | `.display-menu`, `.display-section-header`, `.display-section-body` |
| Extract Dropdown | ~1600 | `.extract-dropdown`, `.extract-menu`, `.extract-menu-item` |
| Highlight Dropdown | ~1650 | `.reader-highlight-dropdown`, `.reader-highlight-menu`, `.reader-hl-color-dot` |
| Floating Nav Buttons | ~1700 | `.floating-nav-btn` |
| Media Dialog / Fullscreen | ~1756 | `#readerMediaDialog`, `#readerMediaFullscreen` |
| Save Toast | ~1820 | `#saveToast` |
| Help System | ~1850 | `.help-banner`, `.help-overlay`, `.help-group`, `.help-row`, `.help-key`, `.help-desc` |
| Reader Highlights Styles | ~2050 | `.epubjs-hl`, `.hl-yellow`, `.hl-green`, `.hl-pink` (iniettati in iframe) |
| Media Tap (iframe inject) | ~2100 | Stili iniettati nell'iframe EPUB per clickable media |

---

## CSS CUSTOM PROPERTIES — BIBLIOTECA

Definite su `#library-view` (light) e `#library-view.lib-dark` (dark). Usate tramite `var(--lib-*)`.

| Proprietà | Light | Dark | Target |
|-----------|-------|------|--------|
| `--lib-bg` | `#f7f6f3` | `#1a1a20` | Background pagina biblioteca |
| `--lib-header-bg` | `rgba(247,246,243,0.92)` | `rgba(26,26,32,0.92)` | Header biblioteca (sticky) |
| `--lib-header-border` | `rgba(0,0,0,0.07)` | `rgba(255,255,255,0.07)` | Bordo inferiore header |
| `--lib-title-color` | `#000000` | `#e8e4dc` | Titolo "Noesis" |
| `--lib-subtitle` | `#000000` | `#a0a0b8` | Sottotitolo header |
| `--lib-import-border` | `rgba(0,0,0,0.35)` | `rgba(102,126,234,0.4)` | Bordo label import EPUB |
| `--lib-import-color` | `#000000` | `#8a9ef0` | Testo/icona import |
| `--lib-import-hover-bg` | `rgba(0,0,0,0.06)` | `rgba(102,126,234,0.12)` | Hover label import |
| `--lib-import-hover-border` | `#000000` | `#667eea` | Hover bordo import |
| `--lib-row-border` | `rgba(0,0,0,0.07)` | `rgba(255,255,255,0.08)` | Bordo tra righe libri |
| `--lib-cover-bg` | `#e8e6e0` | `#242430` | Background copertina placeholder |
| `--lib-cover-border` | `rgba(0,0,0,0.1)` | `rgba(255,255,255,0.08)` | Bordo copertina |
| `--lib-cover-icon` | `#000000` | `#8080a0` | Colore icona copertina placeholder |
| `--lib-cover-shadow` | `3px 3px 10px rgba(0,0,0,0.12)` | `3px 3px 10px rgba(0,0,0,0.5)` | Ombra copertina |
| `--lib-cover-shadow-hover` | con bordo `rgba(0,0,0,0.25)` | con bordo viola | Ombra copertina hover |
| `--lib-title-text` | `#000000` | (chiaro) | Titolo libro nella riga |
| `--lib-author` | `#000000` | (chiaro) | Autore nella riga |
| `--lib-stats` | `#000000` | (chiaro) | Testo statistiche |
| `--lib-badge-bg` | `rgba(0,0,0,0.07)` | (scuro) | Background badge capitoli/snapshot |
| `--lib-badge-color` | `#000000` | (chiaro) | Testo badge |
| `--lib-del-btn` | `#000000` | (chiaro) | Colore pulsante elimina libro |
| `--lib-chapter-border` | `rgba(0,0,0,0.15)` | (scuro) | Bordo entry capitolo |
| `--lib-chapter-border-hover` | `rgba(0,0,0,0.4)` | (scuro) | Hover bordo capitolo |
| `--lib-chapter-btn` | `#000000` | (chiaro) | Colore nome capitolo |
| `--lib-snap-count` | `#000000` | (chiaro) | Contatore snapshot |
| `--lib-snap-dot` | `#000000` | (chiaro) | Dot snapshot standard |
| `--lib-snap-dot-latest` | `#10b981` | `#10b981` | Dot snapshot più recente (verde) |
| `--lib-snap-desc` | `#000000` | (chiaro) | Descrizione snapshot |
| `--lib-snap-date` | `#000000` | (chiaro) | Data snapshot |
| `--lib-snap-hover-bg` | `rgba(0,0,0,0.05)` | (scuro) | Hover riga snapshot |
| `--lib-snap-has-bg` | `rgba(0,0,0,0.07)` | (scuro) | Background badge "N snaps" |
| `--lib-del-icon` | `#000000` | (chiaro) | Icona cestino |
| `--lib-empty-color` | `#000000` | (chiaro) | Testo stato vuoto |
| `--lib-toggle-color` | `#000000` | (chiaro) | Colore toggle tema |
| `--lib-toggle-hover` | `rgba(0,0,0,0.06)` | (scuro) | Hover toggle tema |

---

## CLASSI BIBLIOTECA — CATALOGO

### Layout Header

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.library-header` | `<div>` | Header fisso, flex row, padding, border-bottom |
| `.library-header-left` | `<div>` | Metà sinistra: titolo + sottotitolo |
| `.library-header-right` | `<div>` | Metà destra: pulsanti azione |
| `.library-title` | `<div>` | Contenitore icona + testo "Noesis" |
| `.library-subtitle` | `<p>` | Sottotitolo descrittivo |

### Grid Libri

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.library-grid` | `#bookGrid` | Grid CSS per le righe libro |
| `.book-row` | `<div>` | Contenitore riga singolo libro |
| `.book-header` | `<div>` | Header riga: copertina + info + badge |
| `.book-cover-thumb` | `<div>` | Contenitore thumbnail copertina (80×110px) |
| `.book-cover-img` | `<img>` | Immagine copertina effettiva |
| `.book-cover-placeholder` | `<div>` | Placeholder quando copertina assente |
| `.book-meta` | `<div>` | Flex column: titolo + autore + stats |
| `.book-title-row` | `<div>` | Flex row: titolo + pulsante elimina |
| `.book-title-btn` | `<button>` | Titolo cliccabile per aprire libro |
| `.book-author` | `<div>` | Nome autore |
| `.book-stats` | `<div>` | Flex row con badge |
| `.book-badge` | `<span>` | Badge singolo (es: "3 chapters") |
| `.book-badge.empty` | `<span>` | Badge quando valore = 0 |
| `.book-delete-btn` | `<button>` | Pulsante elimina libro (icona cestino) |

### Sezione Capitoli Estratti

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.chapters-section` | `<div>` | Contenitore espandibile capitoli per libro |
| `.chapters-list` | `<div>` | Lista chapter-entry |
| `.chapter-entry` | `<div>` | Riga singolo capitolo estratto |
| `.chapter-header` | `<div>` | Flex row: nome + snap count + elimina |
| `.chapter-name-btn` | `<button>` | Nome capitolo cliccabile → apre sn56.x |
| `.chapter-snap-count` | `<span>` | "N snapshots" |
| `.chapter-snap-count.has-snaps` | `<span>` | Variante con background quando N > 0 |
| `.chapter-delete-btn` | `<button>` | Elimina capitolo (visibile su hover) |
| `.snapshots-list` | `<div>` | Lista snapshot del capitolo |
| `.snapshot-item` | `<button>` | Riga singolo snapshot |
| `.snapshot-item.latest` | `<button>` | Variante snapshot più recente |
| `.snapshot-item-dot` | `<div>` | Dot indicatore (grigio/verde) |
| `.snapshot-item-desc` | `<span>` | Descrizione snapshot |
| `.snapshot-item-date` | `<span>` | Data snapshot |
| `.snapshot-delete-btn` | `<button>` | Elimina snapshot (visibile su hover) |
| `.no-chapters-note` | `<div>` | Placeholder "no chapters yet" |
| `.empty-state` | `<div>` | Stato biblioteca vuota (no libri) |

### Help Sistema

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.help-banner` | `<div>` | Banner primo avvio (inizialmente `.hidden`) |
| `.help-banner-icon` | `<span>` | Emoji/icona del banner |
| `.help-banner-body` | `<div>` | Corpo testo del banner |
| `.help-banner-title` | `<div>` | Titolo banner |
| `.help-banner-steps` | `<div>` | Lista step del banner |
| `.help-banner-step` | `<div>` | Singolo step |
| `.help-banner-close` | `<button>` | Pulsante chiudi banner (X) |
| `.help-overlay` | `<div>` | Overlay fullscreen help (nascosto) |
| `.help-overlay-box` | `<div>` | Box contenuto overlay |
| `.help-overlay-header` | `<div>` | Header overlay: titolo + chiudi |
| `.help-overlay-title` | `<span>` | Titolo overlay |
| `.help-overlay-close` | `<button>` | Pulsante chiudi overlay (X) |
| `.help-group` | `<div>` | Gruppo di voci help con titolo |
| `.help-group-title` | `<div>` | Titolo gruppo (es: "Keyboard") |
| `.help-row` | `<div>` | Riga singola: chiave + descrizione |
| `.help-key` | `<span>` | Etichetta chiave/pulsante (sinistra) |
| `.help-desc` | `<span>` | Descrizione estesa (destra) |

---

## CLASSI READER — CATALOGO

### Layout Principale

| Classe/ID | Elemento | Scopo |
|-----------|----------|-------|
| `header` | `<header>` | Toolbar reader: `position: relative`, `z-index: 700`, flex row |
| `#container` | `<div>` | Area sotto header: sidebar + viewer, `display: flex`, `flex: 1` |
| `#bookmarks` | `<nav>` | Sidebar TOC, `overflow-y: auto`, larghezza fissa |
| `#viewer` | `<div>` | Contenitore iframe EPUB, `flex: 1` |
| `#status` | `<div>` | Status bar inferiore |
| `#statusMsg` | `<span>` | Messaggio status sinistro |
| `#statusPath` | `<span>` | Breadcrumb path destro |

### Toolbar Buttons

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.btn` | `<button>` | Pulsante base toolbar |
| `.btn-icon` | `<button>` | Variante con solo icona |
| `.btn-primary` | `<button>` | Variante blu (es: toggle sidebar) |
| `.btn-warning` | `<button>` | Variante arancio/ambra (es: save state) |
| `.btn-success` | `<button>` | Variante verde (es: extract) |
| `.btn-help` | `<button>` | Variante speciale per pulsante `?` |
| `.toolbar` | `<div>` | Contenitore pulsanti (flex row, flex-wrap) |
| `.toolbar-group` | `<div>` | Raggruppamento logico di pulsanti |
| `.toolbar-spacer` | `<div>` | Spaziatore flex |

### User Bookmarks Drawer

| Classe/ID | Elemento | Scopo |
|-----------|----------|-------|
| `#userBookmarksDrawer` | `<div>` | Drawer slide-in da destra, `position: fixed` |
| `#ubmHeader` | `<div>` | Header drawer: titolo + new + chiudi |
| `#ubmList` | `<div>` | Lista scrollabile segnalibri |
| `.ubm-item` | `<div>` | Riga segnalibro: corpo + pulsante delete |
| `.ubm-item-body` | `<div>` | Parte cliccabile per navigare |
| `.ubm-chapter` | `<div>` | Nome capitolo (bold, truncated) |
| `.ubm-preview` | `<div>` | Anteprima testo (2 righe, clamp) |
| `.ubm-label` | `<div>` | Etichetta opzionale (blue, italic) |
| `.ubm-date` | `<div>` | Data/ora (grigio chiaro, 10px) |
| `.ubm-delete-btn` | `<button>` | Bottone × destra della riga |
| `.ubm-empty` | `<div>` | Placeholder lista vuota |
| `#ubmBadge` | `<span>` | Badge numerico sul pulsante segnalibri |

### Popup Tipografia / Interface

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.typography-popup` | `<div>` | Container popup (position absolute, z-index 300) |
| `.typography-row` | `<div>` | Riga: label + controls |
| `.typography-controls` | `<div>` | Flex row: pulsanti +/− + valore + reset |
| `.typography-value` | `<span>` | Valore numerico corrente |
| `.reset-btn` | `<button>` | Pulsante reset (rotazione CCW) |

**ID specifici popup:**
- `#typographyPopupMain` — popup tipografia, centrato horizontally
- `#interfacePopupMain` — popup interface settings, centrato
- `#themePopupMain` — popup tema

### Popup Tema

| Classe | Elemento | Scopo |
|--------|----------|-------|
| `.theme-popup` | `<div>` | Container popup tema |
| `.theme-group` | `<div>` | Gruppo di temi con label |
| `.theme-group-label` | `<div>` | Nome gruppo (es: "Dark/Black") |
| `.theme-swatches` | `<div>` | Grid swatches |
| `.theme-swatch` | `<div>` | Singolo campione tema (cerchio colorato) |
| `.theme-swatch.active` | `<div>` | Swatch attivo: bordo evidenziato |

### Display Menu (Accordion)

| Classe/ID | Elemento | Scopo |
|-----------|----------|-------|
| `.display-dropdown` | `<div>` | Container dropdown |
| `.display-menu` | `<div>` | Menu accordion |
| `.display-section-header` | `<div>` | Header sezione cliccabile |
| `.display-section-header.open` | `<div>` | Sezione espansa |
| `.display-section-body` | `<div>` | Corpo sezione (contenuto popup spostato) |
| `.display-sep` | `<div>` | Separatore tra sezioni |
| `.display-section-chevron` | `<i>` | Icona freccia (ruota 90° quando open) |

**ID specifici:**
- `#displayBtn` — pulsante trigger menu
- `#displayMenu` — menu container
- `#displaySecTypo`, `#displaySecThemes`, `#displaySecInterface` — header sezioni
- `#displayBodyTypo`, `#displayBodyThemes`, `#displayBodyInterface` — body sezioni

### Extract Dropdown

| Classe/ID | Elemento | Scopo |
|-----------|----------|-------|
| `.extract-dropdown` | `<div>` | Container dropdown estrazione |
| `.extract-menu` | `<div>` | Menu opzioni (position absolute) |
| `.extract-menu-item` | `<div>` | Opzione singola con `data-mode="current|tree"` |

### Highlight Dropdown

| Classe/ID | Elemento | Scopo |
|-----------|----------|-------|
| `.reader-highlight-dropdown` | `<div>` | Container dropdown highlight |
| `.reader-highlight-menu` | `<div>` | Menu selezione colore |
| `.reader-highlight-option` | `<div>` | Opzione colore con `data-color` |
| `.reader-hl-color-dot` | `<div>` | Punto colorato indicatore |
| `.reader-hl-color-dot.yellow` | — | Variante gialla |
| `.reader-hl-color-dot.green` | — | Variante verde |
| `.reader-hl-color-dot.pink` | — | Variante rosa |
| `.reader-hl-color-dot.remove` | — | Variante remove (strikethrough) |
| `.btn.hl-yellow` | `<button>` | Pulsante con colore giallo attivo |
| `.btn.hl-green` | `<button>` | Pulsante con colore verde attivo |
| `.btn.hl-pink` | `<button>` | Pulsante con colore rosa attivo |

### Floating Nav Buttons

| Classe/ID | Elemento | Scopo |
|-----------|----------|-------|
| `.floating-nav-btn` | `<button>` | Frecce prev/next: `position: fixed`, semi-trasparenti |
| `#floatingPrevBtn` | — | Freccia sinistra |
| `#floatingNextBtn` | — | Freccia destra |

### Media Preview

| ID | Elemento | Scopo |
|----|----------|-------|
| `#readerMediaDialog` | `<div>` | Dialog preview, `position: fixed`, `z-index: 9999` |
| `#readerMdPreviewBtn` | `<button>` | Pulsante "Preview" (viola) |
| `#readerMdExitBtn` | `<button>` | Pulsante "Exit" (grigio) |
| `#readerMediaFullscreen` | `<div>` | Overlay fullscreen, `z-index: 10000`, sfondo scuro |

Visibilità tramite classe `.visible` (non `.hidden`): `display: none` → `display: flex`.

### Save Toast

| ID | Elemento | Scopo |
|----|----------|-------|
| `#saveToast` | `<div>` | Toast notification, `position: fixed`, in basso |
| `#saveToastMsg` | `<span>` | Testo del toast |

Classi stato: `saving` (sfondo ambra), `saved` (sfondo verde), `error` (sfondo rosso).
Toggle visibilità tramite classe `.show`.

---

## CSS CUSTOM PROPERTY — READER

| Proprietà | Dove definita | Scopo |
|-----------|---------------|-------|
| `--ubm-bg` | `#userBookmarksDrawer` | Background drawer segnalibri (impostato da JS via `interfaceSettings.ubmDrawerColor`) |

---

## PATTERN CSS: Visibilità Elementi

Il codice usa **due pattern** distinti:

| Pattern | Implementazione | Usato per |
|---------|----------------|-----------|
| `display: none !important` via classe `.hidden` | Aggiunta/rimozione classe | Vista principale, overlay loading, floating buttons |
| `display: none` → `display: flex` via classe `.visible` | Aggiunta/rimozione classe | `#readerMediaDialog`, `#readerMediaFullscreen` |
| `display: none !important; visibility: hidden; opacity: 0` inline | Popup tipografia/tema (nascosti in DOM ma usati dal display accordion) | Popup legacy tenuti nel DOM |

> **Gotcha**: i popup `#typographyPopupMain`, `#themePopupMain`, `#interfacePopupMain` hanno `display: none !important` inline hardcoded. Sono stati spostati dentro il `#displayMenu` accordion. Il CSS del display menu sovrascrive queste proprietà con `position: relative !important` ecc. Non tentare di aprirli come popup floating: l'accordion li gestisce.

---

## RESPONSIVE — Media Queries

| Breakpoint | Selettore | Modifiche |
|------------|-----------|-----------|
| `max-width: 768px` | `.typography-popup` | min-width: 250px, padding ridotto |
| `max-width: 768px` | `.typography-controls button` | 40×40px, font 18px |
| `max-width: 600px` | `.library-header` | padding 14px 16px |
| `max-width: 600px` | `.library-grid` | padding 16px |
| `max-width: 600px` | `.book-cover-thumb` | 52×72px |
| `max-width: 600px` | `.chapters-section` | padding-left: 64px |
