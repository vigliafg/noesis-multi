# NOESIS810 — Documento 6: Struttura HTML Statica

> Fonte: `noesis810.html` righe 2358–2920 — Aggiornato: 2026-03-27
> Notazione: `#id`, `.classe`, `[attr]` come riferimenti CSS/JS standard

---

## ALBERO DOM COMPLETO (Elementi Statici)

```
<body>
│
├── #loading-overlay                          (riga ~2358)
│   ├── .spinner
│   └── #loading-msg
│
├── #library-view                             (riga 2365)
│   ├── .library-header
│   │   ├── .library-header-left
│   │   │   ├── .library-title
│   │   │   │   ├── <i class="bi bi-book">
│   │   │   │   └── <span>Noesis</span>
│   │   │   └── <p class="library-subtitle">
│   │   └── .library-header-right
│   │       ├── <input type="file" #libraryInput accept=".epub">      (hidden)
│   │       ├── <label for="libraryInput" #importLabel>               (pulsante visibile Add Book)
│   │       ├── <input type="file" #importSnapshotsInput accept=".html,.htm" multiple>  (hidden)
│   │       ├── <button #importSnapshotsBtn>
│   │       ├── <button #libOpenEditorBtn>
│   │       ├── <button #libThemeToggle>
│   │       ├── .lib-tools-dropdown #libToolsDropdown
│   │       │   ├── <button #libToolsBtn>
│   │       │   └── .lib-tools-menu.hidden #libToolsMenu
│   │       │       ├── <a href="https://noesis-epub-tools.vercel.app/" .lib-tools-item>
│   │       │       ├── <a href="https://pandoc.org/app" .lib-tools-item>
│   │       │       └── <a href="https://mozilla.github.io/pdf.js/..." .lib-tools-item>
│   │       └── <button #libHelpBtn>?</button>
│   │
│   ├── #bookGrid.library-grid                (riga 2418 — CONTENUTO DINAMICO)
│   │   └── <!-- libri iniettati da loadLibraryBooks() -->
│   │
│   ├── .help-banner.hidden #libHelpBanner    (riga 2422)
│   │   ├── <span .help-banner-icon>💡
│   │   ├── .help-banner-body
│   │   │   ├── .help-banner-title
│   │   │   └── .help-banner-steps
│   │   │       └── .help-banner-step × N
│   │   └── <button .help-banner-close #libBannerClose>✕
│   │
│   └── .help-overlay #libHelpOverlay         (riga 2442)
│       └── .help-overlay-box
│           ├── .help-overlay-header
│           │   ├── <span .help-overlay-title>
│           │   └── <button .help-overlay-close #libHelpOverlayClose>✕
│           └── .help-group × 4
│               ├── .help-group-title
│               └── .help-row × N
│                   ├── <span .help-key>
│                   └── <span .help-desc>
│
└── #reader-view.hidden                       (riga 2525)
    │
    ├── <header>                              (riga 2527)
    │   ├── <button #backToLibraryBtn>
    │   ├── <strong>EPUB Reader</strong>
    │   ├── <input type="file" #fileInput accept=".epub">   (hidden — legacy)
    │   ├── <span #fileName>No file selected</span>
    │   │
    │   ├── .toolbar
    │   │   ├── <button .btn.btn-icon.btn-primary #toggleSidebarBtn>
    │   │   │
    │   │   ├── <button .btn.btn-icon #userBookmarksBtn>
    │   │   │   └── <span #ubmBadge style="display:none">0
    │   │   │
    │   │   ├── .reader-highlight-dropdown
    │   │   │   ├── <button .btn.btn-icon.hl-yellow #readerHighlightBtn>
    │   │   │   └── .reader-highlight-menu #readerHighlightMenu
    │   │   │       ├── .reader-highlight-option[data-color="yellow"]
    │   │   │       │   ├── <input type="radio" name="readerHlColor" value="yellow" #rhlYellow checked>
    │   │   │       │   ├── .reader-hl-color-dot.yellow
    │   │   │       │   └── <label for="rhlYellow">
    │   │   │       ├── .reader-highlight-option[data-color="green"]
    │   │   │       ├── .reader-highlight-option[data-color="pink"]
    │   │   │       └── .reader-highlight-option[data-color="remove"]
    │   │   │
    │   │   ├── .toolbar-spacer
    │   │   │
    │   │   ├── .display-dropdown #displayDropdownWrap
    │   │   │   ├── <button .btn.btn-icon #displayBtn>
    │   │   │   └── .display-menu #displayMenu
    │   │   │       ├── .display-section-header #displaySecTypo
    │   │   │       ├── .display-section-body #displayBodyTypo       (← popup tipografia spostato qui via JS)
    │   │   │       ├── .display-sep
    │   │   │       ├── .display-section-header #displaySecThemes
    │   │   │       ├── .display-section-body #displayBodyThemes     (← popup tema spostato qui via JS)
    │   │   │       ├── .display-sep
    │   │   │       ├── .display-section-header #displaySecInterface
    │   │   │       └── .display-section-body #displayBodyInterface  (← popup interface spostato qui via JS)
    │   │   │
    │   │   ├── <button .btn.btn-icon #typographyBtn>   (HIDDEN in produzione — legacy JS hook)
    │   │   ├── <button .btn.btn-icon #themeBtn>        (HIDDEN in produzione — legacy JS hook)
    │   │   │
    │   │   ├── .toolbar-spacer
    │   │   │
    │   │   ├── .toolbar-group
    │   │   │   └── <button .btn.btn-icon #scrollModeBtn>
    │   │   │
    │   │   ├── .toolbar-group
    │   │   │   ├── .zoom-btn-wrap
    │   │   │   │   ├── <button .btn.btn-icon #zoomBtn>%
    │   │   │   │   └── .toolbar-zoom-popup #zoomPopupMain
    │   │   │   │       ├── <label #zoomPopupLabelMain>100%
    │   │   │   │       ├── <span .zoom-sign>+
    │   │   │   │       ├── <input type="range" #zoomSliderMain min="90" max="130" step="10">
    │   │   │   │       └── <span .zoom-sign>−
    │   │   │   └── <button .btn.btn-icon #interfaceBtn>
    │   │   │
    │   │   ├── .toolbar-spacer
    │   │   │
    │   │   ├── <button .btn.btn-icon.btn-warning #saveStateBtn>
    │   │   │
    │   │   ├── .toolbar-spacer
    │   │   │
    │   │   ├── .extract-dropdown
    │   │   │   ├── <button .btn.btn-icon.btn-success #extractChapterBtn>
    │   │   │   └── .extract-menu #extractMenu
    │   │   │       ├── .extract-menu-item[data-mode="current"]
    │   │   │       └── .extract-menu-item[data-mode="tree"]
    │   │   │
    │   │   └── <button .btn.btn-icon.btn-help #readerHelpBtn>?
    │   │
    │   ├── #typographyPopupMain.typography-popup    (style="display:none!important" — gestito da accordion)
    │   │   ├── <h3>Typography
    │   │   ├── .typography-row  ← Font Size
    │   │   │   └── .typography-controls
    │   │   │       ├── <button #fontMinus1>
    │   │   │       ├── <span .typography-value #fontInfo>100%
    │   │   │       ├── <button #fontPlus1>
    │   │   │       └── <button .reset-btn #fontReset>
    │   │   ├── .typography-row  ← Line Height
    │   │   │   └── .typography-controls
    │   │   │       ├── <button #lineHeightMinus>
    │   │   │       ├── <span .typography-value #lineHeightInfo>1.2
    │   │   │       ├── <button #lineHeightPlus>
    │   │   │       └── <button .reset-btn #lineHeightReset>
    │   │   └── .typography-row  ← Page View
    │   │       └── .typography-controls
    │   │           ├── <button #singlePageBtn>
    │   │           └── <button #dualPageBtn>
    │   │
    │   ├── #themePopupMain.theme-popup              (style="display:none!important")
    │   │   └── <h3>Reading Themes
    │   │       └── <!-- swatches popolati da buildThemePopup() -->
    │   │
    │   └── #interfacePopupMain.typography-popup     (style="display:none!important")
    │       ├── <h3>Interface Settings
    │       ├── .typography-row  ← Toolbar Color
    │       │   └── .typography-controls
    │       │       ├── <input type="color" #toolbarColorPicker>
    │       │       └── <button #toolbarColorReset>
    │       ├── .typography-row  ← Sidebar Color
    │       │   └── .typography-controls
    │       │       ├── <input type="color" #sidebarColorPicker>
    │       │       └── <button #sidebarColorReset>
    │       ├── .typography-row  ← Nav Buttons Color
    │       │   └── .typography-controls
    │       │       ├── <input type="color" #navButtonsColorPicker>
    │       │       └── <button #navButtonsColorReset>
    │       ├── .typography-row  ← Nav Opacity
    │       │   └── .typography-controls
    │       │       ├── <input type="range" #navOpacitySlider min="0" max="1" step="0.05">
    │       │       └── <button #navOpacityReset>
    │       └── .typography-row  ← Bookmark Drawer Color
    │           └── .typography-controls
    │               ├── <input type="color" #ubmDrawerColorPicker>
    │               └── <button #ubmDrawerColorReset>
    │
    ├── (Reader Banner e Help Overlay — simili a biblioteca)
    │   ├── .help-banner.hidden #readerHelpBanner
    │   │   └── .help-banner-close #readerBannerClose
    │   └── .help-overlay #readerHelpOverlay
    │       └── .help-overlay-box
    │           ├── .help-overlay-header
    │           │   └── <button .help-overlay-close #readerHelpOverlayClose>
    │           └── .help-group × 3 (Navigation, Appearance, Saving, Keyboard)
    │
    ├── #container                                   (riga 2874)
    │   ├── <nav #bookmarks translate="yes">
    │   │   └── <ul #toc>  ← TOC iniettato da renderBookmarksSimple()
    │   └── <div #viewer>  ← iframe EPUB iniettato da epub.js
    │
    ├── <button #floatingPrevBtn .floating-nav-btn.hidden>
    ├── <button #floatingNextBtn .floating-nav-btn.hidden>
    │
    ├── #userBookmarksDrawer                         (riga 2889)
    │   ├── #ubmHeader
    │   │   ├── <h3>My Bookmarks
    │   │   ├── <button #ubmNewBtn>New Bookmark
    │   │   └── <button #ubmCloseBtn>✕
    │   └── #ubmList
    │       └── .ubm-empty  (o lista .ubm-item generata dinamicamente)
    │
    └── #status                                      (riga 2901)
        ├── <span #statusMsg>
        ├── <span #statusSep .hidden-sep> ›
        └── <span #statusPath>

(Fuori da #reader-view, figli diretti di <body>:)
├── #saveToast                                       (riga 2904)
│   ├── <i class="bi bi-floppy">
│   └── <span #saveToastMsg>
├── #readerMediaDialog                               (riga 2910)
│   ├── <button #readerMdPreviewBtn>Preview
│   └── <button #readerMdExitBtn>Exit
├── #readerMediaFullscreen                           (riga 2916)
│   └── <!-- contenuto iniettato dinamicamente -->
└── <script type="application/json" #sn56Source>    (riga ~2920+)
    └── <!-- JSON sorgente di sn56.x per _openSn56() -->

### Struttura Payload JSON (#noesisPayload)

Il payload viene iniettato nell'editor al lancio:

```json
{
  "mode": "chapter | standalone",
  "bookName": "Nome del libro",
  "chapterName": "Nome capitolo",
  "chapterId": "ch_1711530000000_123456",
  "htmlContent": "<html>...</html>"
}
```

### Placeholder nel template sn56.x

Il template HTML di sn56.x contiene il placeholder:
```html
<!-- SN56_PAYLOAD_SLOT -->
```

Questo viene sostituito dinamicamente da `_openSn56()` con:
```html
<script type="application/json" id="noesisPayload">{"mode":"chapter",...}</script>
```
Se il payload è `null`, il placeholder rimane vuoto (modalità standalone).

---

## NOTE IMPORTANTI SULLA STRUTTURA

### 1. I popup tipografia/tema/interface sono nel DOM ma invisibili

I tre popup (`#typographyPopupMain`, `#themePopupMain`, `#interfacePopupMain`) **esistono fisicamente dentro `<header>`** ma sono nascosti con `display: none !important` hardcoded inline. Il sistema `#displayMenu` accordion sposta il loro **contenuto** (non l'elemento) dentro i `.display-section-body` tramite `appendChild`. Questo significa:

- I listener JS sui pulsanti (`#fontPlus1`, ecc.) funzionano perché i pulsanti **non vengono clonati**, solo spostati nel DOM
- Se si aggiunge un nuovo popup dello stesso tipo, deve seguire lo stesso pattern (spostamento nodo)

### 2. `#typographyBtn` e `#themeBtn` esistono ma sono nascosti visivamente

Rimangono nel DOM per mantenere la compatibilità con i listener JS già registrati su di essi (`click` → toggle popup). I popup stessi sono ora gestiti dall'accordion. Non eliminare questi pulsanti.

### 3. `#sn56Source` è un `<script type="application/json">`

Contiene il sorgente HTML completo di sn56.x come stringa JSON. `_openSn56()` lo legge con `document.getElementById('sn56Source').textContent`, vi inietta il payload, e crea un blob URL. **Non è JavaScript eseguito**, è solo storage di testo nel DOM.

### 4. Struttura dinamica dentro `#bookGrid`

Il contenuto di `#bookGrid` è interamente generato da `loadLibraryBooks()`. La struttura di ogni libro è:

```html
<div class="book-row" data-book-id="[id]">
  <div class="book-header">
    <div class="book-cover-thumb">
      <!-- Se ha copertina: -->
      <img class="book-cover-img" src="[blob-url]" alt="Cover">
      <!-- Se no copertina: -->
      <div class="book-cover-placeholder">
        <i class="bi bi-book"></i>
      </div>
    </div>
    <div class="book-meta">
      <div class="book-title-row">
        <button class="book-title-btn">[Titolo]</button>
        <button class="book-delete-btn"><i class="bi bi-trash"></i></button>
      </div>
      <div class="book-author">[Autore]</div>
      <div class="book-stats">
        <span class="book-badge">[N] chapters</span>
        <span class="book-badge">[N] snapshots</span>
      </div>
    </div>
  </div>
  <!-- Se ci sono capitoli estratti: -->
  <div class="chapters-section">
    <div class="chapters-list">
      <div class="chapter-entry">
        <div class="chapter-header">
          <button class="chapter-name-btn">[Titolo Capitolo]</button>
          <span class="chapter-snap-count has-snaps">[N] snapshots</span>
          <button class="chapter-delete-btn"><i class="bi bi-trash"></i></button>
        </div>
        <div class="snapshots-list">
          <button class="snapshot-item latest">  <!-- .latest solo sul più recente -->
            <div class="snapshot-item-dot"></div>
            <span class="snapshot-item-desc">[descrizione]</span>
            <span class="snapshot-item-date">[data]</span>
            <button class="snapshot-delete-btn"><i class="bi bi-trash"></i></button>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
```

### 5. Struttura TOC generata da `renderBookmarksSimple()`

```html
<ul>  <!-- livello 1 -->
  <li>
    <button data-href="OEBPS/chapter01.xhtml" style="padding-left: 8px;">[Titolo]</button>
    <ul>  <!-- livello 2 -->
      <li>
        <button data-href="OEBPS/chapter01.xhtml#sec1" style="padding-left: 16px;">[Titolo]</button>
      </li>
    </ul>
  </li>
</ul>
```

---

## ID COMPLETO — QUICK REFERENCE

Tutti gli ID statici per riferimento rapido:

| ID | Tipo | Ambiente |
|----|------|----------|
| `loading-overlay` | div | globale |
| `loading-msg` | div | globale |
| `library-view` | div | biblioteca |
| `libraryInput` | input[file] | biblioteca |
| `importLabel` | label | biblioteca |
| `importSnapshotsInput` | input[file] | biblioteca |
| `importSnapshotsBtn` | button | biblioteca |
| `libOpenEditorBtn` | button | biblioteca |
| `libThemeToggle` | button | biblioteca |
| `libToolsDropdown` | div | biblioteca |
| `libToolsBtn` | button | biblioteca |
| `libToolsMenu` | div | biblioteca |
| `libHelpBtn` | button | biblioteca |
| `bookGrid` | div | biblioteca |
| `libHelpBanner` | div | biblioteca |
| `libBannerClose` | button | biblioteca |
| `libHelpOverlay` | div | biblioteca |
| `libHelpOverlayClose` | button | biblioteca |
| `reader-view` | div | reader |
| `backToLibraryBtn` | button | reader |
| `fileInput` | input[file] | reader (legacy) |
| `fileName` | span | reader |
| `toggleSidebarBtn` | button | reader |
| `userBookmarksBtn` | button | reader |
| `ubmBadge` | span | reader |
| `readerHighlightBtn` | button | reader |
| `readerHighlightMenu` | div | reader |
| `rhlYellow` | input[radio] | reader |
| `rhlGreen` | input[radio] | reader |
| `rhlPink` | input[radio] | reader |
| `rhlRemove` | input[radio] | reader |
| `displayDropdownWrap` | div | reader |
| `displayBtn` | button | reader |
| `displayMenu` | div | reader |
| `displaySecTypo` | div | reader |
| `displayBodyTypo` | div | reader |
| `displaySecThemes` | div | reader |
| `displayBodyThemes` | div | reader |
| `displaySecInterface` | div | reader |
| `displayBodyInterface` | div | reader |
| `typographyBtn` | button | reader (hidden) |
| `themeBtn` | button | reader (hidden) |
| `scrollModeBtn` | button | reader |
| `zoomBtn` | button | reader |
| `zoomPopupMain` | div | reader |
| `zoomPopupLabelMain` | label | reader |
| `zoomSliderMain` | input[range] | reader |
| `interfaceBtn` | button | reader |
| `saveStateBtn` | button | reader |
| `extractChapterBtn` | button | reader |
| `extractMenu` | div | reader |
| `readerHelpBtn` | button | reader |
| `typographyPopupMain` | div | reader (hidden) |
| `fontMinus1` | button | reader |
| `fontInfo` | span | reader |
| `fontPlus1` | button | reader |
| `fontReset` | button | reader |
| `lineHeightMinus` | button | reader |
| `lineHeightInfo` | span | reader |
| `lineHeightPlus` | button | reader |
| `lineHeightReset` | button | reader |
| `singlePageBtn` | button | reader |
| `dualPageBtn` | button | reader |
| `themePopupMain` | div | reader (hidden) |
| `interfacePopupMain` | div | reader (hidden) |
| `toolbarColorPicker` | input[color] | reader |
| `toolbarColorReset` | button | reader |
| `sidebarColorPicker` | input[color] | reader |
| `sidebarColorReset` | button | reader |
| `navButtonsColorPicker` | input[color] | reader |
| `navButtonsColorReset` | button | reader |
| `navOpacitySlider` | input[range] | reader |
| `navOpacityReset` | button | reader |
| `ubmDrawerColorPicker` | input[color] | reader |
| `ubmDrawerColorReset` | button | reader |
| `readerHelpBanner` | div | reader |
| `readerBannerClose` | button | reader |
| `readerHelpOverlay` | div | reader |
| `readerHelpOverlayClose` | button | reader |
| `bookmarks` | nav | reader |
| `toc` | ul | reader |
| `viewer` | div | reader |
| `floatingPrevBtn` | button | reader |
| `floatingNextBtn` | button | reader |
| `userBookmarksDrawer` | div | reader |
| `ubmHeader` | div | reader |
| `ubmNewBtn` | button | reader |
| `ubmCloseBtn` | button | reader |
| `ubmList` | div | reader |
| `status` | div | reader |
| `statusMsg` | span | reader |
| `statusSep` | span | reader |
| `statusPath` | span | reader |
| `saveToast` | div | globale |
| `saveToastMsg` | span | globale |
| `readerMediaDialog` | div | globale |
| `readerMdPreviewBtn` | button | globale |
| `readerMdExitBtn` | button | globale |
| `readerMediaFullscreen` | div | globale |
| `sn56Source` | script[type=application/json] | globale |
