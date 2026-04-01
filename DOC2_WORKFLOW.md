# NOESIS810 — Documento 2: Workflow dell'Applicazione

> Fonte: `noesis810.html` (6498 righe) — Aggiornato: 2026-03-27

---

## WORKFLOW 1 — Prima apertura dell'applicazione

```
Apertura noesis810.html nel browser
    │
    ▼
DOMContentLoaded event
    │
    ├── openDB()                    → IndexedDB "EpubLibraryDB" (books store)
    ├── openNoesisDB()              → IndexedDB "noesisDB" (capitoli + snapshot)
    ├── Setup tutti i listener DOM  → event delegation completa
    ├── loadLibraryBooks()          → legge tutti i libri da IDB, renderizza griglia
    │
    ▼
Mostra #library-view
    │
    ▼
maybeShowBanner("librarySeen", "libBanner")
    │
    ├── Se MAI mostrato → mostra banner help biblioteca (primo uso)
    └── Se già mostrato → nessun banner
```

---

## WORKFLOW 2 — Import di un libro EPUB

```
Utente clicca "Import EPUB" (pulsante nell'header biblioteca)
    │
    ▼
Apre file picker nativo (<input type="file" accept=".epub">)
    │
    ▼
Utente seleziona uno o più file .epub
    │
    ▼
event 'change' su #libraryInput
    │
    ▼
Per ogni file selezionato:
    │
    ├── showLoading("Importing...")
    │
    ├── saveBookToDB(file)
    │       ├── Legge file come ArrayBuffer
    │       ├── Apre EPUB con ePub.js (Book.open)
    │       ├── Carica metadati (title, author)
    │       ├── Tenta estrazione copertina (cover URL blob)
    │       ├── Salva in IDB: {id, title, author, coverUrl, data, dateAdded}
    │       └── Chiude istanza Book temporanea
    │
    ├── hideLoading()
    │
    └── loadLibraryBooks()   → aggiorna griglia UI con nuovo libro
```

**Errori gestiti**: file corrotti, EPUB senza metadati, copertina non disponibile (fallback: icona).

---

## WORKFLOW 3 — Apertura di un libro dalla Biblioteca

```
Utente clicca sulla copertina/titolo di un libro nella griglia
    │
    ▼
openBookFromLibrary(bookData)
    │
    ├── showLoading("Opening book...")
    │
    ├── currentBookId = bookData.id
    ├── currentBookTitle = bookData.title
    │
    ├── Crea istanza ePub.js: book = ePub(bookData.data)
    │       (bookData.data = ArrayBuffer EPUB da IndexedDB)
    │
    ├── loadAndApplyBookState(bookId)
    │       ├── Legge savedState da IDB per questo libro
    │       ├── Ripristina: fontSize, lineHeight, theme, scrollMode,
    │       │              dualPageMode, sidebarVisible, buttonZoom,
    │       │              interfaceSettings (colori), readerHighlights
    │       └── Salva posizione (CFI/href) per navigazione post-render
    │
    ├── Crea rendition:
    │       ├── scrollMode=false → spread/pagina singola
    │       └── scrollMode=true  → flow "scrolled-doc"
    │
    ├── rendition.hooks.content.register → injetta:
    │       ├── Stili CSS custom reader
    │       ├── Script media tap handler (immagini + tabelle)
    │       └── Wrapper tabelle scorrevoli
    │
    ├── rendition.display(savedCFI)   → naviga a posizione salvata
    │       └── (o display() senza arg → inizio libro se nessuno stato)
    │
    ├── Ripristina highlights: rendition.annotations.highlight(cfi) per ognuno
    │
    ├── Carica TOC: book.navigation.toc → renderBookmarksSimple(toc)
    │
    ├── Carica user bookmarks: loadUserBookmarksFromDB(bookId)
    │
    ├── applyTheme()
    ├── applyInterfaceSettings()
    │
    ├── showReader()   → nasconde #library-view, mostra #reader-view
    │
    ├── hideLoading()
    │
    └── maybeShowBanner("readerSeen", "readerBanner")
            └── Mostra banner help se prima volta nel reader
```

---

## WORKFLOW 4 — Lettura e Navigazione

### 4a — Navigazione per pagina
```
Utente clicca freccia AVANTI (#floatingNextBtn)
    │
    ▼
rendition.next()
    │
    ▼
epub.js carica sezione successiva nell'iframe
    │
    ▼
evento 'relocated' emesso da rendition
    │
    ▼
Callback relocated:
    ├── currentLocation = location
    ├── setStatusPath(breadcrumb)   → aggiorna status bar con Libro > Cap > Sez
    └── (salvataggio posizione differito su saveState esplicito)
```

### 4b — Navigazione via TOC Sidebar
```
Utente clicca voce TOC nella sidebar
    │
    ▼
navigateToHref(href)
    │
    ├── scrollMode=false → rendition.display(href)
    └── scrollMode=true  → rendition.display(href) (idem, epub.js gestisce)
    │
    ▼
iframe aggiornato → evento 'relocated' → breadcrumb aggiornato
```

---

## WORKFLOW 5 — Personalizzazione Tema

```
Utente clicca pulsante Tema nella toolbar
    │
    ▼
Toggle popup tema (.theme-popup)
    │
    ▼
Utente clicca su uno swatch colore
    │
    ▼
currentTheme = chiave tema selezionato
    │
    ▼
applyTheme()
    ├── rendition.themes.register(nome, {body: {background, color}, a: {color}})
    └── rendition.themes.select(nome)
    │
    ▼
updateThemeSwatchActive()   → aggiorna bordo swatch attivo nel popup
    │
    ▼
(tema sarà salvato in savedState al prossimo saveBookState())
```

---

## WORKFLOW 6 — Estrazione Capitolo Corrente

```
Utente clicca "Extract Chapter" nella toolbar
    │
    ▼
Toggle #extractMenu (dropdown con opzioni)
    │
    ▼
Utente sceglie "Extract Current" o "Extract Tree"
    │
    ▼
extractCurrentChapter()   [o extractMultipleSections per tree]
    │
    ├── Determina sezione corrente da currentLocation (href/CFI)
    │
    ├── Raccoglie HTML del capitolo dal documento nell'iframe
    │
    ├── Raccoglie CSS (link + style tags) dall'iframe
    │
    ├── Risolve immagini:
    │       ├── Apre zip EPUB (JSZip o ePub.js book.archive)
    │       ├── Per ogni <img src="...">: legge blob dallo zip
    │       └── Converte in base64 data URL → sostituisce src inline
    │
    ├── _buildExtractionTimestamp()  → timestamp condiviso (per naming pair)
    │
    ├── _generateCleanHTML(...)
    │       └── Genera HTML standalone con:
    │               - <!DOCTYPE>, <meta charset>, <meta noesis-*>
    │               - CSS embedded
    │               - Contenuto capitolo con immagini base64
    │
    ├── Genera due varianti:
    │       ├── "noesis-extract-[book]__[chapter]__[ts].html"  → leggibile
    │       └── "noesis-origin-[book]__[chapter]__[ts].html"   → raw/metadati
    │
    ├── _autoDownloadHTML() × 2   → download automatico entrambi i file
    │
    ├── saveExtractedChapterToDB(record)
    │       └── Salva in noesisDB: {chapterId, bookId, bookTitle, chapterTitle,
    │               htmlContent, timestamp, snapshots:[...]}
    │
    └── _openSn56(payload)
            └── window.open("sn56.x", "_blank", "popup,...")
                    con payload JSON serializzato:
                    {mode:"chapter", bookTitle, chapterTitle, html, snapshotId}
```

---

## WORKFLOW 7 — Salvataggio e Ripristino Stato

### 7a — Salvataggio manuale
```
Utente clicca "Save State" (#saveStateBtn)
    │
    ▼
showToast("Saving...", "saving")
    │
    ▼
saveBookState()
    ├── Raccoglie tutti i valori correnti:
    │       fontSize, lineHeight, currentTheme, scrollMode, dualPageMode,
    │       sidebarVisible, buttonZoom, interfaceSettings, readerHighlights,
    │       currentLocation (CFI + href), timestamp = Date.now()
    │
    ├── Apre IDB transaction su store "books"
    ├── get(currentBookId) → libro esistente
    ├── Aggiunge/sovrascrive libro.savedState = {tutte le proprietà}
    └── put(libro) → aggiorna record
    │
    ▼
showToast("Saved ✓", "saved")
```

### 7b — Ripristino automatico all'apertura
```
loadAndApplyBookState(bookId)
    │
    ├── get(bookId) da IDB → libro.savedState
    │
    ├── Se savedState esiste:
    │       ├── fontSize = savedState.fontSize (o default 100)
    │       ├── lineHeight = savedState.lineHeight (o default 1.6)
    │       ├── currentTheme = savedState.currentTheme (o "white")
    │       ├── scrollMode, dualPageMode, sidebarVisible, buttonZoom
    │       ├── interfaceSettings (colori toolbar, sidebar, ecc.)
    │       └── readerHighlights = savedState.readerHighlights || []
    │
    └── savedPosition = {cfi, href} per rendition.display() successivo
```

---

## WORKFLOW 8 — Gestione Segnalibri Utente

### 8a — Creazione segnalibro
```
Utente clicca "New Bookmark" nel drawer
    │
    ▼
createUserBookmark()
    ├── cfi = currentLocation.start.cfi
    ├── href = currentLocation.start.href
    ├── chapter = findBreadcrumbInToc(toc, href) → label capitolo
    ├── preview = 100 caratteri da posizione corrente (page-based)
    ├── timestamp = Date.now()
    │
    ├── userBookmarks.unshift({cfi, href, chapter, preview, label:"", timestamp})
    │
    ├── saveUserBookmarksToDB()   → aggiorna IDB
    └── renderUbmList()           → aggiorna lista UI nel drawer
```

### 8b — Navigazione a segnalibro
```
Utente clicca su riga segnalibro nel drawer
    │
    ▼
navigateToHref(bookmark.href)   [o rendition.display(bookmark.cfi)]
    │
    ▼
closeUbmDrawer()   → chiude drawer
```

---

## WORKFLOW 9 — Highlight Testo

```
Utente seleziona testo nel viewer EPUB
    │
    ▼
epub.js emette evento 'selected' sulla rendition
    │
    ├── _readerPendingCfi = cfi della selezione
    └── _readerHlHasSelection = true → attiva pulsante highlight
    │
    ▼
Utente clicca pulsante "Highlight" nella toolbar
    │
    ├── Se _readerHlHasSelection = true:
    │       └── Mostra menu colori (yellow/green/pink/remove)
    │
    └── Se nessuna selezione:
            └── Toggle menu colori (cambia solo colore predefinito)
    │
    ▼
Utente clicca colore (es: "yellow")
    │
    ├── applyReaderHighlight()
    │       ├── rendition.annotations.highlight(_readerPendingCfi, {}, callback, "highlight-yellow")
    │       └── readerHighlights.push({cfi: _readerPendingCfi, color: "yellow"})
    │
    └── _readerHlHasSelection = false → reset stato
    │
    ▼
Highlight visibile nel testo
    │
    ▼
(Al prossimo saveBookState: highlights salvati in IDB)
    │
    ▼
(Al prossimo openBookFromLibrary: highlights ripristinati via rendition.annotations.highlight())
```

---

## WORKFLOW 10 — Import Snapshot da Disco

```
Utente clicca "Import Snapshots" nel menu strumenti biblioteca
    │
    ▼
importSnapshotsFromDisk()
    ├── Apre file picker (accept: .html, directory)
    │
    ▼
Utente seleziona file/cartella con HTML snapshot noesis
    │
    ▼
_processSnapshotFiles(files)
    │
    Per ogni file selezionato:
    ├── Legge contenuto HTML
    ├── Estrae meta tag noesis (book, chapter, timestamp, variant)
    ├── Determina chapterId (book__chapter__ts)
    │
    ├── getExtractedChapterFromDB(chapterId)
    │       ├── Se esiste → aggiunge snapshot all'array esistente
    │       └── Se non esiste → crea nuovo record chapter
    │
    └── saveExtractedChapterToDB(record aggiornato)
    │
    ▼
loadLibraryBooks()   → aggiorna griglia con nuovi snapshot importati
```

---

## WORKFLOW 11 — Apertura Snapshot dalla Biblioteca

```
Utente clicca pulsante snapshot nella riga capitolo della griglia
    │
    ▼
_openExtractedEnv(chapterRecord, snapshotId)
    │
    ├── Ordina snapshot: isOrigin in fondo, altri per data decrescente
    ├── Recupera snapshot target (o più recente se null)
    ├── Costruisce payload JSON:
    │       {mode:"chapter", htmlContent, bookName, chapterName, chapterId}
    │
    └── _openSn56(payload)
            └── window.open("sn56.x", "_blank", popup)
                    con payload trasmesso alla finestra editor
```

---

## WORKFLOW 11b — Lanzamento Editor sn56.x (_openSn56)

```
_openSn56(payload)
    │
    ├── 1. Recupera sorgente: JSON.parse(#sn56Source.textContent)
    │
    ├── 2. Se payload esiste:
    │       serializza in <script id="noesisPayload"> + JSON.stringify(payload)
    │       altrimenti: lascia placeholder vuoto
    │
    ├── 3. Inietta nel template: src.replace('<!-- SN56_PAYLOAD_SLOT -->', island)
    │
    ├── 4. Crea Blob URL: URL.createObjectURL(new Blob([html], {type:'text/html'}))
    │
    ├── 5. Apre finestra: window.open(url, '_blank', '')
    │
    └── 6. Cleanup: setTimeout(URL.revokeObjectURL(url), 60000)
```

### Boot Editor (lato sn56.x)

```
_bootPayload()
    │
    ├── Se #noesisPayload NON esiste:
    │       _mode = 'standalone' → editor vuoto
    │
    └── Se #noesisPayload ESISTE:
            ├── payload = JSON.parse(textContent)
            ├── _mode = payload.mode ('chapter')
            ├── _bookName = payload.bookName
            ├── _chapterName = payload.chapterName
            ├── _chapterId = payload.chapterId
            │
            └── $('#editor').summernote('code', payload.htmlContent)
```

### IDB Bridge (comunicazione cross-window)

```
sn56.x → postMessage({__noesisIDB:true, op:'get'|'put', payload})
    │
    ▼
noesis810.html: window.addEventListener('message')
    │
    ├── op='get': getExtractedChapterFromDB(chapterId) → reply(result)
    ├── op='put': saveExtractedChapterToDB(record) → reply(result)
    │
    ▼
sn56.x: Promise resolve/reject
```

---

## WORKFLOW 12 — Ritorno alla Biblioteca

```
Utente clicca "Back to Library" (freccia ← nell'header reader)
    │
    ▼
showLibrary()
    ├── rendition?.destroy()     → smonta EPUB dall'iframe
    ├── book?.destroy()          → libera risorse ePub.js
    ├── rendition = null, book = null
    ├── currentBookId = null, currentBookTitle = null
    ├── userBookmarks = []
    ├── readerHighlights = []
    ├── currentLocation = null
    │
    ├── Chiude tutti i popup/drawer aperti
    │
    ├── Nasconde #reader-view
    └── Mostra #library-view
    │
    ▼
loadLibraryBooks()   → refresh griglia biblioteca
```

---

## WORKFLOW 13 — Preview Media da EPUB (postMessage Bridge)

```
Utente tocca/clicca immagine o tabella nel viewer EPUB (iframe)
    │
    ▼
Script iniettato nell'iframe (via rendition.hooks.content.register):
    └── postMessage({type:"mediaTap", mediaType:"image"|"table", data:...})
        verso window.parent
    │
    ▼
window.addEventListener("message") nel parent (noesis810)
    │
    ├── Verifica origin (sicurezza)
    └── IIFE media handler:
            ├── showDialog("image"|"table", data)
            │       ├── Posiziona #readerMediaDialog centrato
            │       ├── Se immagine: <img src="base64...">
            │       └── Se tabella: clone del nodo tabella
            │
            └── Pulsante "Fullscreen":
                    ├── Mostra #readerMediaFullscreen
                    └── Copia contenuto dialog in overlay fullscreen
    │
    ▼
Utente chiude dialog: hideDialog() → rimuove contenuto, nasconde dialog
```

---

## TABELLA RIEPILOGATIVA DATI PERSISTITI

| Dato | Storage | Store/Key | Quando scritto | Quando letto |
|------|---------|-----------|----------------|--------------|
| File EPUB (ArrayBuffer) | IndexedDB | `EpubLibraryDB/books` | Import EPUB | Apertura libro |
| Metadati libro (title, author, cover) | IndexedDB | `EpubLibraryDB/books` | Import EPUB | Griglia biblioteca |
| Stato lettura (posizione, tema, ecc.) | IndexedDB | `EpubLibraryDB/books[id].savedState` | Save State | Apertura libro |
| Capitoli estratti + snapshot | IndexedDB | `noesisDB/chapters` | Estrazione | Griglia biblioteca, apertura editor |
| Stato banner "visto" | localStorage | `librarySeen`, `readerSeen` | Chiusura banner | Apertura ambienti |
| Tema biblioteca (chiaro/scuro) | (in-memory) | — | Toggle tema | Ricarica pagina = reset |
