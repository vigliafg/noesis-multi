# NOESIS810 — Documento 4: Schemi Dati Completi

> Fonte: `noesis810.html` — lettura diretta del codice — Aggiornato: 2026-03-27

---

## 1. SCHEMA RECORD LIBRO — `EpubLibraryDB / books`

Il record viene creato da `saveBookToDB()` e aggiornato da `saveBookState()` e `saveUserBookmarksToDB()`.

```json
{
  "id":       "<number — autoIncrement IDB, chiave primaria>",
  "title":    "<string — titolo estratto da epub metadati>",
  "author":   "<string — autore estratto da epub metadati, può essere vuoto>",
  "data":     "<ArrayBuffer — contenuto binario del file .epub>",
  "cover":    "<string|null — blob URL della copertina, oppure null se assente>",
  "addedAt":  "<number — Date.now() al momento dell'import>",

  "savedState": {
    "fontSize":         "<number — percentuale font, default 100>",
    "lineHeight":       "<number — valore float, default 1.2>",
    "theme":            "<string — chiave tema, default 'normal', es: 'white', 'sepia', 'dark'>",
    "scrollMode":       "<boolean — true = scroll continuo, false = paginato>",
    "dualPageMode":     "<boolean — true = due pagine affiancate>",
    "sidebarVisible":   "<boolean — true = sidebar TOC aperta>",
    "buttonZoom":       "<number — percentuale zoom toolbar, default 100>",
    "interface": {
      "toolbarColor":    "<string — hex colore toolbar, default '#667eea'>",
      "sidebarColor":    "<string — hex colore sidebar, default '#ffffff'>",
      "navButtonsColor": "<string — hex colore frecce floating, default '#667eea'>",
      "navOpacity":      "<number — opacità frecce 0.0–1.0, default 0.7>",
      "ubmDrawerColor":  "<string — hex colore drawer segnalibri, default '#fffde7'>"
    },
    "position": {
      "cfi":       "<string|null — Canonical Fragment Identifier epub.js, es: 'epubcfi(/6/4!/4/2:10)'>",
      "href":      "<string|null — percorso relativo sezione EPUB, es: 'OEBPS/chapter01.xhtml'>",
      "timestamp": "<number — Date.now() della posizione salvata>"
    },
    "readerHighlights": [
      {
        "cfi":   "<string — CFI del testo evidenziato>",
        "color": "<string — 'yellow'|'green'|'pink'>"
      }
    ],
    "savedAt": "<number — Date.now() dell'ultimo save>"
  },

  "userBookmarks": [
    {
      "cfi":       "<string|null — CFI della posizione segnalibro>",
      "href":      "<string|null — href sezione EPUB>",
      "chapter":   "<string — label del capitolo estratta dal TOC>",
      "preview":   "<string — testo della pagina, max ~100 caratteri>",
      "label":     "<string — etichetta opzionale utente, può essere ''>",
      "createdAt": "<number — Date.now() al momento della creazione>"
    }
  ]
}
```

**Note importanti:**
- `savedState` è `undefined` finché l'utente non salva. Controllare sempre: `if (bookData.savedState)`
- `savedState.position` è `null` se la posizione non è stata mai catturata (es: primo avvio)
- `cover` è un blob URL: **non sopravvive tra sessioni del browser** diverso. All'import viene generato e salvato come stringa, ma un blob URL di una sessione precedente potrebbe non essere più valido. Il codice attuale salva il cover blob URL direttamente — potenziale gotcha
- `userBookmarks` è `undefined` su record vecchi (creati prima del modulo bookmark). Controllare: `Array.isArray(bookData.userBookmarks)`

---

## 2. SCHEMA RECORD CAPITOLO — `noesisDB / chapters`

Il record viene creato da `saveExtractedChapterToDB()` durante l'estrazione o l'import snapshot.

```json
{
  "chapterId":   "<string — chiave primaria: 'ch_TIMESTAMP_RANDOM' o estratto da meta tag>",
  "bookName":    "<string — titolo del libro EPUB di provenienza>",
  "chapterName": "<string — titolo del capitolo estratto>",
  "createdAt":   "<string — ISO 8601 datetime della prima estrazione>",

  "snapshots": [
    {
      "snapshotId":  "<string — 'snap_TIMESTAMP_RANDOM', univoco>",
      "createdAt":   "<string — ISO 8601 datetime della creazione snapshot>",
      "description": "<string — etichetta leggibile, es: 'clean-20260327-143022' o 'origin-...' >",
      "isOrigin":    "<boolean — true se variante 'origin' (con meta tag noesis-*)>",
      "content":     "<string — innerHTML del <body> dell'HTML estratto (può essere molto grande)>"
    }
  ]
}
```

**Ordinamento snapshots:**
- Gli snapshot `isOrigin: true` sono tenuti **in fondo** all'array (`.push`)
- Gli snapshot clean/annot sono in **cima** (`.unshift`)
- In `_openExtractedEnv()`: ordinati per `isOrigin asc`, poi `createdAt desc` prima di selezionare il target

**Generazione `chapterId`:**
- Se l'HTML contiene `<meta name="noesis-chapter-id">`: usa quel valore
- Altrimenti: `'ch_' + Date.now() + '_' + Math.floor(Math.random() * 1e6)`

---

## 3. SCHEMA PAYLOAD — Comunicazione verso sn56.x

Il payload JSON viene iniettato in `<script type="application/json" id="noesisPayload">` nel blob HTML di sn56.x.

```json
{
  "mode":        "chapter",
  "htmlContent": "<string — innerHTML del body del capitolo estratto>",
  "bookName":    "<string — titolo libro>",
  "chapterName": "<string — titolo capitolo>",
  "chapterId":   "<string — chapterId del record noesisDB>"
}
```

**Come viene letto da sn56.x:**
```javascript
// Dentro sn56.x, all'avvio:
const payloadEl = document.getElementById('noesisPayload');
const payload = payloadEl ? JSON.parse(payloadEl.textContent) : null;
if (payload && payload.mode === 'chapter') {
  // carica payload.htmlContent nell'editor
}
```

**Modalità senza payload:** `_openSn56()` chiamata senza argomenti → nessun `<script id="noesisPayload">` iniettato → sn56.x si apre in modalità standalone/blank.

---

## 4. SCHEMA META TAG — File HTML Snapshot (noesis-origin-*)

I file scaricati su disco e reimportabili contengono questi meta tag nel `<head>`:

```html
<!-- Presenti SOLO nella variante "origin" (includeNoesisMeta = true) -->
<meta name="noesis-chapter-id"       content="ch_1234567890_987654">
<meta name="noesis-book-name"        content="Il Nome del Libro">
<meta name="noesis-chapter-name"     content="Capitolo 3 — Titolo">
<meta name="noesis-snapshot-variant" content="origin">
```

La variante "extract" (clean) **non ha questi meta tag** e non è reimportabile automaticamente.

---

## 5. NAMING CONVENTION FILE HTML

### Pattern nome file
```
noesis-[variant]-[bookName]__[chapterName]__[YYYYMMDD_HHmmss].html
```

### Esempi
```
noesis-extract-Il_Signore_degli_Anelli__Libro_I__20260327_143022.html
noesis-origin-Il_Signore_degli_Anelli__Libro_I__20260327_143022.html
```

### Regex di riconoscimento (usata in `importSnapshotsFromDisk`)
```javascript
/^noesis-(clean|annot|origin)-.*\.html?$/i
```

### Regex di parsing nome file (usata in `_processSnapshotFiles`)
```javascript
/^noesis-[a-z]+-(.+)__(.+)__(\d{8}_\d{6})(?:_([^.]+))?\.html?$/i
//                   [1]=bookName  [2]=chapterName  [3]=timestamp  [4]=custom_suffix
```

---

## 6. SCHEMA VARIABILI GLOBALI — Valori Default Effettivi

Valori letti direttamente dal codice (righe 3711–3736):

```javascript
// Tipografia
fontSize    = 100       // percentuale
lineHeight  = 1.2       // valore float
lineHeights = [1, 1.2, 1.4, 1.6, 1.8, 2.0]  // valori disponibili

// Layout
scrollMode   = false
dualPageMode = false
sidebarVisible = false  // sidebar TOC chiusa all'avvio

// Tema
currentTheme = 'normal'  // chiave di default (NON 'white')

// Zoom
buttonZoom = 100

// Colori interfaccia default (effettivi, da riga 3730)
defaultInterfaceSettings = {
  toolbarColor:    '#667eea',   // viola-blu
  sidebarColor:    '#ffffff',   // bianco
  navButtonsColor: '#667eea',
  navOpacity:      0.7,
  ubmDrawerColor:  '#fffde7'   // giallo crema
}
```

> **Attenzione:** DOC3 riportava valori diversi (es: `sidebarVisible = true`, `currentTheme = 'white'`). I valori sopra sono quelli **reali** letti dal codice sorgente.

---

## 7. CHIAVI localStorage

| Chiave | Tipo | Valore | Scopo |
|--------|------|--------|-------|
| `"readerSeen"` | `"1"` o assente | Stringa | Traccia se il banner help reader è stato visto |
| `"librarySeen"` | `"1"` o assente | Stringa | Traccia se il banner help biblioteca è stato visto |
| `"libTheme"` | `"dark"` o assente | Stringa | Tema corrente biblioteca (chiaro/scuro) — se implementato |

---

## 8. SCHEMA OGGETTO `location` di epub.js

`currentLocation` è l'oggetto restituito da `rendition.currentLocation()` o dall'evento `relocated`:

```javascript
{
  start: {
    cfi:   "epubcfi(/6/4[chap01]!/4/2/2:10)",  // stringa CFI
    href:  "OEBPS/chapter01.xhtml",              // path sezione
    index: 0,                                    // indice spine
    displayed: {
      page:  1,   // pagina corrente nella sezione
      total: 5    // pagine totali nella sezione
    }
  },
  end: {
    cfi:   "epubcfi(/6/4[chap01]!/4/2/30:0)",
    href:  "OEBPS/chapter01.xhtml",
    index: 0,
    displayed: { page: 1, total: 5 }
  },
  atStart: false,
  atEnd:   false
}
```

**Usi nel codice:**
- `currentLocation.start.cfi` → salvataggio posizione, creazione bookmark, gestione highlight
- `currentLocation.start.href` → navigazione, ricerca TOC, estrazione capitolo
- `currentLocation.start.displayed.page / .total` → calcolo preview bookmark
