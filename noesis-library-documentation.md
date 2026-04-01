# Noesis Library — Documentazione Tecnica Completa

**Versione di riferimento:** noesis810.html  
**Data documento:** 2026-03-28  

---

## Indice

1. [Panoramica generale](#1-panoramica-generale)
2. [Architettura DOM e struttura visiva](#2-architettura-dom-e-struttura-visiva)
3. [Sistema di temi: light e dark](#3-sistema-di-temi-light-e-dark)
4. [Mappa completa della toolbar (header)](#4-mappa-completa-della-toolbar-header)
5. [La griglia dei libri — book-row](#5-la-griglia-dei-libri--book-row)
6. [La sezione capitoli estratti — chapters-section](#6-la-sezione-capitoli-estratti--chapters-section)
7. [La lista degli snapshot per capitolo](#7-la-lista-degli-snapshot-per-capitolo)
8. [Workflow: aggiunta di un libro](#8-workflow-aggiunta-di-un-libro)
9. [Workflow: apertura di un libro nel Reader](#9-workflow-apertura-di-un-libro-nel-reader)
10. [Workflow: apertura di un capitolo nell'Editor](#10-workflow-apertura-di-un-capitolo-nelleditor)
11. [Workflow: eliminazione di libri, capitoli e snapshot](#11-workflow-eliminazione-di-libri-capitoli-e-snapshot)
12. [Import Snapshots da disco](#12-import-snapshots-da-disco)
13. [Sistema Help — banner, overlay, pulsante ?](#13-sistema-help--banner-overlay-pulsante-)
14. [Loading overlay](#14-loading-overlay)
15. [Switch tra Library e Reader](#15-switch-tra-library-e-reader)
16. [Strutture di memorizzazione](#16-strutture-di-memorizzazione)
17. [Variabili e costanti globali rilevanti](#17-variabili-e-costanti-globali-rilevanti)
18. [Responsive e adattamento mobile](#18-responsive-e-adattamento-mobile)

---

## 1. Panoramica generale

La **Noesis Library** è la schermata principale (home) di `noesis810.html`. È il punto di ingresso dell'applicazione: la prima vista mostrata all'avvio, il luogo da cui si accede a tutte le altre funzionalità, e il registro centrale di tutto il lavoro di lettura e annotazione.

La Library è progettata come un **archivio editoriale gerarchico** con tre livelli di profondità:

```
Libro (EpubLibraryDB)
  └── Capitolo estratto (noesisDB)
        └── Snapshot (embedded in chapterRecord)
```

Caratteristiche fondamentali:

- **Zero-server**: tutto è locale. Nessun file viene caricato su server. I libri EPUB sono memorizzati come `ArrayBuffer` in IndexedDB, le copertine come base64, le annotazioni come HTML in `noesisDB`.
- **Dual-theme CSS**: tema light editoriale (sfondo `#f7f6f3`, ispirato alla carta) e tema dark gray (`#1a1a20`), entrambi governati da CSS custom properties. Il tema scelto persiste in `localStorage`.
- **Rendering gerarchico dinamico**: `loadLibraryBooks()` interroga entrambi i database in parallelo (`Promise.all`), aggrega i capitoli per libro (case-insensitive), e costruisce l'intera struttura DOM a runtime.
- **Font editoriale**: l'interfaccia Library usa `Georgia, 'Times New Roman', serif` per titoli e etichette, differenziandosi dal Reader e dall'Editor.

---

## 2. Architettura DOM e struttura visiva

```
#library-view
├── .library-header                  ← sticky, backdrop-blur, z-index 10
│   ├── .library-header-left
│   │   ├── .library-title           ← "Noesis" (italic, serif, 22px)
│   │   └── .library-subtitle        ← "Your reading archive…"
│   └── .library-header-right        ← flex row, gap 10px
│       ├── #libraryInput            ← <input file hidden> (accept .epub)
│       ├── #importLabel             ← "Add Book" (label → libraryInput)
│       ├── #importSnapshotsInput    ← <input file hidden, multiple> (.html,.htm)
│       ├── #importSnapshotsBtn      ← icona bi-cloud-arrow-up
│       ├── #libOpenEditorBtn        ← icona bi-pencil-square
│       ├── #libThemeToggle          ← icona bi-moon / bi-sun
│       ├── .lib-tools-dropdown
│       │   ├── #libToolsBtn         ← "Tools" con bi-wrench
│       │   └── #libToolsMenu        ← dropdown con 3 link esterni
│       └── #libHelpBtn              ← "?"
│
├── #bookGrid (.library-grid)        ← contenitore libri (max-width 1100px)
│   ├── .book-row                    ← per ogni libro
│   │   ├── .book-header
│   │   │   ├── .book-cover-thumb    ← 64×88px, cliccabile → Reader
│   │   │   ├── .book-meta
│   │   │   │   ├── .book-meta-title
│   │   │   │   ├── .book-meta-author
│   │   │   │   └── .book-meta-stats ← badges (N chapters, N snapshots)
│   │   │   └── .book-actions
│   │   │       └── .book-delete-btn ← trash icon
│   │   └── .chapters-section        ← rientrata 82px da sinistra
│   │       ├── .no-chapters-note    ← se nessun capitolo estratto
│   │       └── .chapter-entry       ← per ogni capitolo
│   │           ├── .chapter-entry-header
│   │           │   ├── .chapter-name-btn   ← cliccabile → Editor
│   │           │   ├── .chapter-snap-count ← "N snapshots"
│   │           │   └── .chapter-delete-btn ← appare su hover
│   │           └── .snapshots-list
│   │               └── .snapshot-item      ← per ogni snapshot
│   │                   ├── .snapshot-item-dot    ← punto colorato
│   │                   ├── .snapshot-item-desc   ← descrizione
│   │                   ├── .snapshot-item-date   ← data/ora
│   │                   └── .snapshot-delete-btn  ← appare su hover
│   └── .empty-state                 ← se libreria vuota
│
├── #libHelpBanner                   ← banner primo avvio (nascosto dopo)
└── #libHelpOverlay                  ← overlay guida pulsanti
```

### 2.1 Caratteristiche dell'header

L'header `.library-header` è **sticky** (`position: sticky; top: 0`) con `backdrop-filter: blur(12px)` e sfondo semi-trasparente (`rgba(247,246,243,0.92)` in light, `rgba(26,26,32,0.92)` in dark). Scorre via con il contenuto solo se il contenuto è abbastanza lungo, ma rimane sempre visibile nelle librerie normali. `z-index: 10` garantisce che rimanga sopra il testo dei libri durante lo scroll.

### 2.2 Griglia libri

`.library-grid` è un flex container verticale (`flex-direction: column`), con padding `28px 28px 48px`, larghezza massima `1100px` centrata con `margin: 0 auto`. I libri sono separati da bordi orizzontali (`border-bottom: 1px solid var(--lib-row-border)`), senza spazio aggiuntivo tra le righe.

### 2.3 Stato vuoto

Se `EpubLibraryDB` non contiene libri, `#bookGrid` mostra:
```html
<div class="empty-state">
  <i class="bi bi-book"></i>
  <p>Start by adding a book. Reading is the first step toward building knowledge.</p>
</div>
```
Icona 48px, testo centrato, colore `var(--lib-empty-color)`.

---

## 3. Sistema di temi: light e dark

La Library implementa un sistema di temi basato interamente su **CSS custom properties**, senza JavaScript per il rendering. Il toggle di tema aggiunge/rimuove la classe `.lib-dark` su `#library-view`.

### 3.1 Variabili CSS — confronto light vs dark

| Variabile | Light | Dark |
|---|---|---|
| `--lib-bg` | `#f7f6f3` | `#1a1a20` |
| `--lib-header-bg` | `rgba(247,246,243,0.92)` | `rgba(26,26,32,0.92)` |
| `--lib-header-border` | `rgba(0,0,0,0.07)` | `rgba(255,255,255,0.07)` |
| `--lib-title-color` | `#000000` | `#e8e4dc` |
| `--lib-subtitle` | `#000000` | `#a0a0b8` |
| `--lib-import-border` | `rgba(0,0,0,0.35)` | `rgba(102,126,234,0.4)` |
| `--lib-import-color` | `#000000` | `#8a9ef0` |
| `--lib-cover-bg` | `#e8e6e0` | `#242430` |
| `--lib-badge-bg` | `rgba(0,0,0,0.07)` | `rgba(102,126,234,0.12)` |
| `--lib-badge-color` | `#000000` | `#818cf8` |
| `--lib-chapter-border` | `rgba(0,0,0,0.15)` | `rgba(102,126,234,0.2)` |
| `--lib-snap-dot` | `#000000` | `#7c3aed` |
| `--lib-snap-dot-latest` | `#10b981` | `#10b981` (identico) |
| `--lib-snap-hover-bg` | `rgba(0,0,0,0.05)` | `rgba(124,58,237,0.12)` |

Il punto verde `#10b981` dello snapshot più recente è identico in entrambi i temi — è un indicatore universale.

### 3.2 Logica del toggle tema

```javascript
(function() {
  const libView = document.getElementById('library-view');
  const btn = document.getElementById('libThemeToggle');
  const icon = btn.querySelector('i');
  var dark = localStorage.getItem('noesis-lib-theme') === 'dark';
  
  function applyTheme() {
    if (dark) {
      libView.classList.add('lib-dark');
      icon.className = 'bi bi-sun';       // icona sole in dark mode
      btn.title = 'Switch to light theme';
    } else {
      libView.classList.remove('lib-dark');
      icon.className = 'bi bi-moon';      // icona luna in light mode
      btn.title = 'Switch to dark theme';
    }
  }
  
  applyTheme(); // Applicazione immediata al caricamento
  
  btn.addEventListener('click', function() {
    dark = !dark;
    localStorage.setItem('noesis-lib-theme', dark ? 'dark' : 'light');
    applyTheme();
  });
})();
```

La preferenza viene letta da `localStorage` al caricamento e applicata immediatamente, prima che il DOM sia visibile all'utente (nessun flash di tema sbagliato). La transizione `background 0.25s` su `#library-view` rende il cambio visivamente fluido.

---

## 4. Mappa completa della toolbar (header)

### 4.1 `#importLabel` / `#libraryInput` — Add Book

| Proprietà | Valore |
|---|---|
| Elemento | `<label for="libraryInput">` (styled as button) |
| File input | `#libraryInput` (hidden, `accept=".epub"`) |
| Stile | Border 1px, transparent bg, UPPERCASE, letter-spacing 0.05em |
| Icona | `bi-plus-lg` |
| Etichetta | "Add Book" |

**Comportamento al clic:**
```
Utente clicca label → apre file picker (accept .epub)
      ↓
libraryInput change event
      ↓
showLoading('Adding book to library...')
      ↓
saveBookToDB(file) — legge metadati EPUB, copertina, salva in IDB
      ↓
loadLibraryBooks() — ricarica la griglia
      ↓
hideLoading()
libraryInput.value = '' — reset per permettere re-import stesso file
```

Nessun feedback di completamento oltre alla ricomparsa del libro nella griglia.

---

### 4.2 `#importSnapshotsBtn` — Import Snapshots

| Proprietà | Valore |
|---|---|
| Icona | `bi-cloud-arrow-up` |
| Tooltip | "Import Snapshots from disk" |
| File input nascosto | `#importSnapshotsInput` (multiple, accept `.html,.htm`) |

Apre il flusso di import snapshot da disco. Descritto in dettaglio nella [sezione 12](#12-import-snapshots-da-disco).

---

### 4.3 `#libOpenEditorBtn` — Open Editor

| Proprietà | Valore |
|---|---|
| Icona | `bi-pencil-square` |
| Tooltip | "Open Editor — standalone" |
| Azione | `_openSn56(null)` |

Apre sn56.x in modalità **standalone** (editor vuoto, senza contesto libro/capitolo). Nessun payload viene trasmesso, quindi `_mode = 'standalone'` e nessun `_chapterId`. L'editor si apre in una nuova scheda tramite Blob URL.

---

### 4.4 `#libThemeToggle` — Toggle tema

| Proprietà | Valore |
|---|---|
| Icona | `bi-moon` (light mode) / `bi-sun` (dark mode) |
| Tooltip | Dinamico in base allo stato |
| Persistenza | `localStorage` → chiave `'noesis-lib-theme'` |
| Transizione CSS | `background 0.25s` su `#library-view` |

Descritto in dettaglio nella [sezione 3.2](#32-logica-del-toggle-tema).

---

### 4.5 `#libToolsBtn` / `#libToolsMenu` — Tools dropdown

| Proprietà | Valore |
|---|---|
| Icona | `bi-wrench` |
| Etichetta | "Tools" |
| Tipo | Dropdown con link esterni (`target="_blank"`) |

**Voci del menu:**

| Strumento | URL | Descrizione |
|---|---|---|
| noesis-epub-tools | `noesis-epub-tools.vercel.app` | Web app per editing e gestione di file EPUB |
| Pandoc Online | `pandoc.org/app` | Convertitore universale di formati documento (MD↔DOCX↔HTML↔EPUB↔LaTeX), via pandoc.wasm, senza upload |
| Mozilla PDF Viewer | `mozilla.github.io/pdf.js/web/viewer.html` | PDF.js browser-based, con supporto accessibilità |

**Logica apertura/chiusura:**
```javascript
toolsBtn.addEventListener('click', function(e) {
  e.stopPropagation();
  toolsMenu.classList.toggle('hidden');
});
document.addEventListener('click', function() {
  toolsMenu.classList.add('hidden'); // chiude su clic fuori
});
```

Il menu è un `div.lib-tools-menu` con `position: absolute; top: calc(100% + 6px); right: 0`, sfondo `#1e2535`, bordo radius 8px, box-shadow.

---

### 4.6 `#libHelpBtn` — Guida rapida

| Proprietà | Valore |
|---|---|
| Etichetta | `?` |
| Stile | `background: rgba(255,255,255,0.12)`, bordo semi-trasparente |
| Azione | `openOverlay('libHelpOverlay')` |

Apre l'overlay di guida completa che descrive tutti i controlli della Library. Descritto nella [sezione 13](#13-sistema-help--banner-overlay-pulsante-).

---

## 5. La griglia dei libri — book-row

### 5.1 Struttura di una .book-row

Ogni libro in biblioteca genera un `.book-row` costruito dinamicamente da `loadLibraryBooks()`. La struttura è:

```
.book-row
├── .book-header
│   ├── .book-cover-thumb (64×88px)
│   │   └── <img> oppure <i class="bi bi-book"> se no cover
│   ├── .book-meta
│   │   ├── .book-meta-title   (italic serif, max 2 righe con line-clamp)
│   │   ├── .book-meta-author  (UPPERCASE, 11px, system-ui)
│   │   └── .book-meta-stats   ← badges
│   │       ├── .book-meta-badge "N chapters"  (o "no extractions")
│   │       └── .book-meta-badge "N snapshots" (opzionale, se >0)
│   └── .book-actions
│       └── .book-delete-btn   (trash icon)
└── .chapters-section
    └── [capitoli estratti]
```

### 5.2 Copertina del libro

- Se `book.cover` è valorizzato (base64): `<img src="base64..." alt="Titolo">` con `object-fit: cover`.
- Se non c'è copertina: `<i class="bi bi-book">` (26px).

**Effetto hover sulla copertina:**
```css
.book-cover-thumb:hover {
  transform: scale(1.04) translateY(-2px);
  box-shadow: 4px 6px 18px rgba(0,0,0,0.22), 0 0 0 1px rgba(0,0,0,0.25);
  /* dark: box-shadow: 4px 6px 18px rgba(0,0,0,0.7), 0 0 0 1px rgba(102,126,234,0.35) */
}
```
Transizioni `box-shadow 0.2s` e `transform 0.18s`.

### 5.3 Badges statistiche

I badge `.book-meta-badge` sono contatori monospazio uppercase 10px:

| Condizione | Badge |
|---|---|
| 0 capitoli estratti | `"no extractions"` (classe `.empty`, sfondo più tenue) |
| N > 0 capitoli | `"N chapter"` / `"N chapters"` |
| N > 0 snapshot totali | `"N snapshot"` / `"N snapshots"` |

Il conteggio dei snapshot è la **somma** degli snapshot di tutti i capitoli estratti del libro:
```javascript
const totalSnaps = bookChapters.reduce((n, ch) => n + (ch.snapshots || []).length, 0);
```

### 5.4 Ordinamento libri

I libri sono ordinati per **data di aggiunta decrescente** (`addedAt` desc):
```javascript
books.sort((a, b) => b.addedAt - a.addedAt);
```
Il libro più recente appare in cima alla lista.

### 5.5 Associazione libri↔capitoli

L'associazione tra libri (`EpubLibraryDB`) e capitoli estratti (`noesisDB`) avviene per **corrispondenza del titolo del libro** (case-insensitive, trimmed):

```javascript
const chaptersByBook = {};
allChapters.forEach(ch => {
  const key = (ch.bookName || '').toLowerCase().trim();
  if (!chaptersByBook[key]) chaptersByBook[key] = [];
  chaptersByBook[key].push(ch);
});
// ...
const bookKey = (book.title || '').toLowerCase().trim();
const bookChapters = chaptersByBook[bookKey] || [];
```

I capitoli per ciascun libro sono poi ordinati per **data di creazione decrescente** (capitolo più recente in cima).

---

## 6. La sezione capitoli estratti — chapters-section

### 6.1 Posizionamento e design

`.chapters-section` è rientrata di `82px` da sinistra (che corrisponde approssimativamente alla larghezza della copertina 64px + gap 18px). Crea visivamente una gerarchia chiara: i capitoli appaiono "sotto" il loro libro.

Ogni `.chapter-entry` ha:
- Un bordo sinistro verticale (`2px solid var(--lib-chapter-border)`) che cambia colore su hover (`var(--lib-chapter-border-hover)`).
- `padding-left: 14px` per distanziare il contenuto dal bordo.
- `transition: border-color 0.2s`.

### 6.2 Header del capitolo — `.chapter-entry-header`

```
[Nome capitolo (btn)]   [N snapshots badge]   [🗑 delete (appare su hover)]
```

**`.chapter-name-btn`:**
- Pulsante senza bordi, color `var(--lib-chapter-btn)`.
- Testo 13px, system-ui, `white-space: nowrap`, `text-overflow: ellipsis`.
- Hover: colore `var(--lib-chapter-btn-hover)` con `transition: color 0.15s`.
- Clic → `_openExtractedEnv(ch, null)` → apre snapshot più recente nell'Editor.

**`.chapter-snap-count`:**
- Badge inline con testo "N snapshots" o "no snapshots".
- Se `snaps.length > 0`: classe `.has-snaps` → sfondo `var(--lib-snap-has-bg)`, colore `var(--lib-snap-has-color)`, padding 2px 6px, border-radius 3px.
- Se 0 snapshot: nessun badge speciale, solo testo "no snapshots" in grigio.

**`.chapter-delete-btn`:**
- `opacity: 0` di default.
- **Appare solo al hover** sull'intera `.chapter-entry`: `opacity: 1`.
- Hover sul pulsante: `color: #ef4444` + background rosso semi-trasparente.
- `transition: opacity 0.15s`.

### 6.3 Ordinamento snapshot per capitolo

Prima dell'ordinamento il codice separa gli snapshot `isOrigin` da quelli normali:
```javascript
const snaps = (ch.snapshots || []).slice().sort((a, b) => {
  if (a.isOrigin && !b.isOrigin) return 1;   // isOrigin → sempre in fondo
  if (!a.isOrigin && b.isOrigin) return -1;  // normali → in cima
  return new Date(b.createdAt) - new Date(a.createdAt); // più recente prima
});
```

**Regola:**
- Snapshot `isOrigin: true` (estratto automaticamente al momento dell'estrazione dal Reader) → sempre **in fondo** alla lista.
- Tutti gli altri snapshot → **dal più recente al più vecchio**.

---

## 7. La lista degli snapshot per capitolo

### 7.1 Struttura di uno snapshot-item

```
.snapshot-item [classe "latest" se il primo della lista]
├── .snapshot-item-dot   (cerchietto 5×5px)
├── .snapshot-item-desc  (descrizione testuale, ellipsis)
├── .snapshot-item-date  (data breve "Mar 27 14:25")
└── .snapshot-delete-btn (🗑, appare su hover)
```

### 7.2 Indicatore "latest"

Il primo elemento dell'array ordinato (`si === 0`) riceve la classe `.latest`:
```javascript
btn.className = 'snapshot-item' + (si === 0 ? ' latest' : '');
```

Effetto della classe `.latest`:
```css
.snapshot-item.latest .snapshot-item-dot {
  background: var(--lib-snap-dot-latest); /* #10b981 verde */
  opacity: 0.8;
}
.snapshot-item.latest .snapshot-item-desc {
  color: var(--lib-snap-desc-latest); /* testo leggermente più chiaro/evidenziato */
}
```

Il punto verde `#10b981` è identico sia in light che in dark mode — è il segnale universale "questo è il più recente".

### 7.3 Formato data

```javascript
const d = new Date(snap.createdAt);
const dateStr = d.toLocaleDateString([], { month: 'short', day: 'numeric' })
              + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
// Esempio: "Mar 27 14:25"
```

### 7.4 Hover e interazione

- Hover su `.snapshot-item`: `background: var(--lib-snap-hover-bg)`.
- Hover su `.snapshot-item-dot`: `opacity: 1` (da 0.5).
- Hover su `.snapshot-item-desc`: `color: var(--lib-snap-desc-hover)`.

### 7.5 Clic su uno snapshot

```javascript
btn.onclick = () => _openExtractedEnv(ch, snap.snapshotId);
```

`_openExtractedEnv(chapterRecord, snapshotId)` cerca lo snapshot specifico e apre sn56.x con il suo contenuto. Se `snapshotId` è `null` (clic sul nome capitolo), usa il primo snapshot dell'array ordinato (il più recente).

### 7.6 Delete dello snapshot

```javascript
btn.querySelector('.snapshot-delete-btn').onclick = async (e) => {
  e.stopPropagation();
  if (confirm(`Delete snapshot "${snap.description || '(no description)'}"?`)) {
    await deleteSnapshotFromDB(ch.chapterId, snap.snapshotId);
    loadLibraryBooks();
  }
};
```

`deleteSnapshotFromDB` filtra l'array `snapshots` del record capitolo e riscrive il record in `noesisDB`. La lista viene ricaricata immediatamente.

---

## 8. Workflow: aggiunta di un libro

### 8.1 Flusso completo

```
Utente clicca "Add Book"
      ↓
File picker si apre (accept .epub)
      ↓
Utente seleziona file .epub
      ↓
libraryInput change event
      ↓
showLoading('Adding book to library...')
      ↓
saveBookToDB(file):
  1. file.arrayBuffer()          ← legge il file come ArrayBuffer
  2. ePub(arrayBuffer)           ← crea istanza epub.js temporanea
  3. await book.ready
  4. book.loaded.metadata        ← estrae title, creator (author)
  5. book.coverUrl()             ← ottiene blob URL copertina
  6. fetch(coverUrl) → blob → FileReader → base64
  7. Costruisce bookRecord:
     { id, title, author, data: ArrayBuffer, cover: base64, addedAt }
  8. store.add(bookRecord)       ← scrive in EpubLibraryDB
      ↓
loadLibraryBooks()              ← ricarica la griglia
      ↓
hideLoading()
libraryInput.value = ''         ← reset file input
```

### 8.2 Dettaglio `saveBookToDB`

```javascript
const bookRecord = {
  id:      Date.now().toString(),           // chiave primaria
  title:   metadata.title || file.name.replace('.epub', ''),
  author:  metadata.creator || 'Unknown Author',
  data:    arrayBuffer,                     // file EPUB grezzo
  cover:   coverBase64,                     // null se assente
  addedAt: Date.now()
};
```

**Gestione copertina:**
- `book.coverUrl()` restituisce un Blob URL temporaneo.
- Il Blob URL viene convertito in base64 via `fetch → blob → FileReader.readAsDataURL()`.
- La base64 viene salvata come stringa nel record IDB, così la copertina è disponibile permanentemente senza dipendere da Blob URL (che scadono).
- Se la copertina non è presente o non è recuperabile: `cover: null`. In quel caso la UI mostra l'icona `bi-book`.

**Errore di versione DB:**
La funzione `openDB()` gestisce `VersionError`: se rilevato, cancella il database (`indexedDB.deleteDatabase(DB_NAME)`) e riapre. Questo previene blocchi da versioni incompatibili del database.

---

## 9. Workflow: apertura di un libro nel Reader

### 9.1 Trigger

Clic sul `.book-cover-thumb` (copertina miniatura) di qualsiasi libro nella griglia:

```javascript
bookRow.querySelector('.book-cover-thumb').onclick = () => openBookFromLibrary(book);
```

### 9.2 Flusso in `openBookFromLibrary(bookData)`

```
showLoading('Opening Book...')
      ↓
showReader()
  → nasconde #library-view
  → mostra #reader-view
      ↓
currentBookId = bookData.id
currentBookTitle = bookData.title
      ↓
loadAndApplyBookState(currentBookId)
  → Legge savedState da EpubLibraryDB
  → Ripristina: fontSize, lineHeight, theme, scrollMode,
    dualPageMode, sidebarVisible, buttonZoom, interfaceSettings,
    readerHighlights
  → Restituisce positionCFI (o null se primo accesso)
      ↓
loadUserBookmarksFromDB(currentBookId)
renderUbmList()
      ↓
Applica zoom toolbar, stato scroll/dual page, font info
applyInterfaceSettings()
      ↓
book = ePub(bookData.data)   ← costruisce il libro dall'ArrayBuffer in IDB
await book.ready
      ↓
recreateRendition()
  → Crea rendition in #viewer
  → Applica hook content (stili, highlights, media tap)
  → Ripristina posizione via CFI → href → default
  → applyTheme()
      ↓
Carica TOC → renderBookmarksSimple(nav.toc)
      ↓
Abilita extractChapterBtn, saveStateBtn
      ↓
hideLoading()
```

### 9.3 Il libro non viene "riaperto" ma "ricostruito"

I file EPUB non vengono mai decompresso su disco. L'`ArrayBuffer` memorizzato in IDB viene passato direttamente a `ePub()` che lo elabora in memoria. Ogni apertura del libro ricostruisce la struttura in-memory da zero.

---

## 10. Workflow: apertura di un capitolo nell'Editor

### 10.1 Trigger dal nome capitolo (snapshot più recente)

```javascript
entry.querySelector('.chapter-name-btn').onclick = () => {
  _openExtractedEnv(ch, null);
};
```

### 10.2 Trigger da snapshot specifico

```javascript
btn.onclick = () => _openExtractedEnv(ch, snap.snapshotId);
```

### 10.3 Funzione `_openExtractedEnv(chapterRecord, snapshotId)`

```javascript
function _openExtractedEnv(chapterRecord, snapshotId) {
  // Ordina: isOrigin in fondo, altri dal più recente
  const snaps = (chapterRecord.snapshots || []).slice().sort((a, b) => {
    if (a.isOrigin && !b.isOrigin) return 1;
    if (!a.isOrigin && b.isOrigin) return -1;
    return a.createdAt > b.createdAt ? -1 : 1;
  });
  
  const targetSnap = snapshotId
    ? snaps.find(s => s.snapshotId === snapshotId)
    : snaps[0] || null;                    // null → snapshot più recente
    
  const htmlContent = targetSnap
    ? targetSnap.content
    : '<p><em>No snapshots yet.</em></p>';
    
  _openSn56({
    mode:        'chapter',
    htmlContent: htmlContent,
    bookName:    chapterRecord.bookName    || '',
    chapterName: chapterRecord.chapterName || '',
    chapterId:   chapterRecord.chapterId   || ''
  });
}
```

### 10.4 Funzione `_openSn56(payload)`

```javascript
function _openSn56(payload) {
  const src = JSON.parse(document.getElementById('sn56Source').textContent);
  const island = payload
    ? '<script type="application/json" id="noesisPayload">'
      + JSON.stringify(payload) + '<\/script>'
    : '';
  const html = src.replace('<!-- SN56_PAYLOAD_SLOT -->', island);
  const url = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
  const w = window.open(url, '_blank', '');
  if (w) setTimeout(() => URL.revokeObjectURL(url), 60000);
  else alert('Please allow popups.');
}
```

L'editor sn56.x viene aperto in una nuova scheda come Blob URL, con il payload del capitolo/snapshot embedded in un data island JSON. La Library rimane aperta nella scheda originale.

---

## 11. Workflow: eliminazione di libri, capitoli e snapshot

### 11.1 Eliminazione libro

**Trigger:** clic su `.book-delete-btn` nella `.book-actions`.

```javascript
bookRow.querySelector('.book-delete-btn').onclick = async (e) => {
  e.stopPropagation();
  if (confirm(`Delete "${book.title}"?`)) {
    await deleteBook(book.id);
    loadLibraryBooks();
  }
};
```

**`deleteBook(id)`:**
```javascript
async function deleteBook(id) {
  const db = await openDB();
  // Elimina record da EpubLibraryDB (include savedState e userBookmarks embedded)
  await store.delete(id);
  // Se era il libro aperto nel Reader, resetta currentBookId
  if (currentBookId === id) { currentBookId = null; }
}
```

**Importante:** l'eliminazione del libro **non** elimina i capitoli estratti in `noesisDB`. Quelli rimangono in `noesisDB` con i loro snapshot, ma non vengono più visualizzati nella Library perché il match libreria↔capitoli avviene per titolo libro. Se il libro viene riaggiunte con lo stesso titolo, i capitoli estratti ricompaiono.

### 11.2 Eliminazione capitolo (con tutti i suoi snapshot)

**Trigger:** clic su `.chapter-delete-btn` (visibile solo su hover sul `.chapter-entry`).

```javascript
entry.querySelector('.chapter-delete-btn').onclick = async (e) => {
  e.stopPropagation();
  if (confirm(`Delete chapter "${ch.chapterName || 'Untitled'}" and all its snapshots?`)) {
    await deleteExtractedChapterFromDB(ch.chapterId);
    loadLibraryBooks();
  }
};
```

**`deleteExtractedChapterFromDB(chapterId)`:**
```javascript
async function deleteExtractedChapterFromDB(chapterId) {
  const db = await openNoesisDB();
  // Elimina l'intero record da noesisDB (include tutti gli snapshot embedded)
  await store.delete(chapterId);
}
```

### 11.3 Eliminazione snapshot singolo

**Trigger:** clic su `.snapshot-delete-btn` (visibile solo su hover sullo `.snapshot-item`).

```javascript
btn.querySelector('.snapshot-delete-btn').onclick = async (e) => {
  e.stopPropagation();
  if (confirm(`Delete snapshot "${snap.description || '(no description)'}"?`)) {
    await deleteSnapshotFromDB(ch.chapterId, snap.snapshotId);
    loadLibraryBooks();
  }
};
```

**`deleteSnapshotFromDB(chapterId, snapshotId)`:**
```javascript
async function deleteSnapshotFromDB(chapterId, snapshotId) {
  const record = await getExtractedChapterFromDB(chapterId);
  if (!record) return;
  // Filtra l'array snapshots rimuovendo quello con l'id specificato
  record.snapshots = (record.snapshots || []).filter(s => s.snapshotId !== snapshotId);
  // Riscrive il record aggiornato
  await saveExtractedChapterToDB(record);
}
```

**Nota:** se tutti gli snapshot di un capitolo vengono eliminati manualmente, il `chapterRecord` rimane in `noesisDB` con `snapshots: []`. Il capitolo continua ad apparire nella Library con il badge "no snapshots". Il capitolo può comunque essere aperto nell'editor (che mostrerà "No snapshots yet.").

---

## 12. Import Snapshots da disco

### 12.1 Scopo

La funzione **Import Snapshots** permette di reimportare in `noesisDB` i file HTML di snapshot precedentemente salvati dall'editor (file `noesis-clean-…html`, `noesis-annot-…html`, `noesis-origin-…html`). È il meccanismo di recupero quando `noesisDB` viene cancellato (es. pulizia browser) o quando si migra su un nuovo dispositivo.

### 12.2 Metodi di selezione file

**Desktop Chrome/Edge** (con `window.showDirectoryPicker`):
```javascript
const dirHandle = await window.showDirectoryPicker({ mode: 'read' });
for await (const entry of dirHandle.values()) {
  if (entry.kind === 'file' && /^noesis-(clean|annot|origin)-.*\.html?$/i.test(entry.name)) {
    const file = await entry.getFile();
    files.push(file);
  }
}
```
Apre un **folder picker**: l'utente seleziona la cartella Download e tutti i file snapshot validi vengono raccolti automaticamente con filtro regex.

**Android / Safari / browser senza `showDirectoryPicker`**:
```javascript
document.getElementById('importSnapshotsInput').click();
// oppure fallback se showDirectoryPicker lancia errore non-AbortError
```
Il `#importSnapshotsInput` è un file picker standard con `multiple` e `accept=".html,.htm"`. L'utente seleziona manualmente i file.

### 12.3 File accettati

Il filtro regex: `/^noesis-(clean|annot|origin)-.*\.html?$/i`

Accetta:
- `noesis-clean-…html` (snapshot pulito dall'editor)
- `noesis-annot-…html` (snapshot annotato dall'editor)
- `noesis-origin-…html` (snapshot originale dall'estrazione Reader)

### 12.4 Logica di processing — `_processSnapshotFiles(files)`

Per ogni file:

**Step 1 — Parsing metadati:**
```javascript
const parser = new DOMParser();
const doc = parser.parseFromString(text, 'text/html');

const chapterId   = doc.querySelector('meta[name="noesis-chapter-id"]')?.content   || '';
const bookName    = doc.querySelector('meta[name="noesis-book-name"]')?.content    || '';
const chapterName = doc.querySelector('meta[name="noesis-chapter-name"]')?.content || '';
const variant     = doc.querySelector('meta[name="noesis-snapshot-variant"]')?.content || 'clean';
const bodyContent = doc.body ? doc.body.innerHTML : text;
```

**Step 2 — Estrazione timestamp dal nome file:**
```javascript
const nameMatch = file.name.match(/^noesis-[a-z]+-(.+)__(.+)__(\d{8}_\d{6})(?:_([^.]+))?\.html?$/i);
// nameMatch[1] = bookSlug, [2] = chapterSlug, [3] = YYYYMMDD_HHMMSS, [4] = custom (opz.)
const tsRaw   = nameMatch ? nameMatch[3] : '';
const custom  = nameMatch ? (nameMatch[4] || '') : '';
```

**Step 3 — Costruzione descrizione:**
```javascript
const tsFmt = tsRaw ? tsRaw.substring(0,8) + '-' + tsRaw.substring(9,15) : '';
const description = variant + (tsFmt ? '-' + tsFmt : '') + (custom ? '-' + custom : '');
// Esempio: "clean-20260327-142530-primaLettura"
```

**Step 4 — Costruzione snapshot object:**
```javascript
const newSnap = {
  snapshotId: 'snap_' + Date.now() + '_' + Math.floor(Math.random() * 1e6),
  createdAt,        // ISO string dal timestamp nel nome file
  description,
  isOrigin: variant === 'origin',
  content: bodyContent
};
```

**Step 5 — Match su record esistente:**

Strategia a due livelli:
1. **Match preciso per `chapterId`**: usa `getExtractedChapterFromDB(chapterId)`.
2. **Fallback fuzzy** (se no `chapterId` o non trovato): cerca tra tutti i record IDB per `bookName + chapterName` case-insensitive.

```javascript
let record = chapterId ? await getExtractedChapterFromDB(chapterId) : null;
if (!record && bookName && chapterName) {
  const all = await getAllExtractedChapters();
  record = all.find(r =>
    r.bookName.toLowerCase().trim() === bookName.toLowerCase().trim() &&
    r.chapterName.toLowerCase().trim() === chapterName.toLowerCase().trim()
  ) || null;
}
```

**Step 6 — Inserimento o creazione:**

*Se record trovato:*
```javascript
const alreadyExists = record.snapshots.some(s => s.description === description);
if (!alreadyExists) {
  if (variant === 'origin') {
    record.snapshots.push(newSnap);    // origin → in fondo
  } else {
    record.snapshots.unshift(newSnap); // altri → in cima
  }
  await saveExtractedChapterToDB(record);
  imported++;
}
// Se già esiste (stessa description): skip silenzioso (deduplicazione)
```

*Se record non trovato:*
```javascript
const newRecord = {
  chapterId:   chapterId || 'ch_' + Date.now() + '_' + random,
  bookName:    bookName  || nameMatch?.[1]?.replace(/_/g, ' ') || 'Unknown Book',
  chapterName: chapterName || nameMatch?.[2]?.replace(/_/g, ' ') || 'Unknown Chapter',
  createdAt,
  snapshots: [newSnap]
};
await saveExtractedChapterToDB(newRecord);
created++;
imported++;
```

**Step 7 — Feedback:**
```javascript
const msg = imported === 0
  ? 'Nessun snapshot importato (file già presenti o non validi).'
  : `Import completato: ${imported} snapshot importati${created > 0 ? ', ' + created + ' nuovi capitoli creati' : ''}.`;
alert(msg);
```

### 12.5 Meccanismo di deduplicazione

La deduplicazione avviene per **corrispondenza esatta della `description`** dello snapshot. Due file con la stessa variante, stesso timestamp e stesso custom avranno la stessa description e uno dei due sarà ignorato. Questo previene duplicati quando si reimportano gli stessi file più volte.

---

## 13. Sistema Help — banner, overlay, pulsante ?

### 13.1 Banner primo avvio — `#libHelpBanner`

Il banner mostra all'utente le azioni chiave della Library. Viene mostrato la **prima volta** che l'utente accede alla Library (verifica via `localStorage`).

**Controllo:**
```javascript
var KEY_LIBRARY = 'noesis-help-seen-library';
// Il banner è always hidden nel markup (class="help-banner hidden")
// e viene mostrato solo se la chiave non è in localStorage
// (nel codice corrente il banner Library è commentato come disabilitato,
//  ma la logica di chiusura è attiva)
```

**Chiusura:**
```javascript
libBannerClose.addEventListener('click', function() {
  localStorage.setItem(KEY_LIBRARY, '1');
  document.getElementById('libHelpBanner').classList.add('hidden');
});
```

**Contenuto del banner:**
- ➕ Add Book — import any EPUB file from your device
- 📚 Book cover — click to open it in the Reader
- Chapters / Snapshots badges — quick stats shown on each book card
- Chapter name — reopens the latest snapshot in the Editor
- Snapshot row — click to open that exact version in the Editor
- 🌙 Theme — toggle light / dark library view
- Import Snapshots — reimport .html snapshot files saved by Noesis Editor
- Open Editor — open Noesis Editor in standalone mode (blank document)
- ? — open this guide at any time

### 13.2 Overlay guida completa — `#libHelpOverlay`

**Apertura:** clic su `#libHelpBtn` → `openOverlay('libHelpOverlay')` → aggiunge classe `.visible`.

**Chiusura:**
- Clic sul pulsante ✕ (`#libHelpOverlayClose`).
- Clic fuori dal contenuto dell'overlay (su `#libHelpOverlay` stesso).

**Struttura del contenuto:**

Il box `.help-overlay-box` con sfondo `#0f172a` e bordo radius 12px contiene quattro gruppi:

| Gruppo | Voci |
|---|---|
| Adding & Opening Books | Add Book, Book cover/title, Chapters·Snapshots badges, Delete book |
| Extracted Chapters | Chapter name, Snapshot count badge, Delete chapter |
| Snapshots | Snapshot row, Green dot, Delete snapshot |
| Interface | Theme toggle, Import Snapshots, Open Editor, Tools, ? |

**Dettaglio voce "Tools"** (testo integrale dall'overlay):
> Opens a dropdown menu with three external web tools: **noesis-epub-tools** — web app for editing and managing EPUB files; **Pandoc Online** — universal document format converter (Markdown, DOCX, HTML, LaTeX, EPUB, ODT and more), runs entirely in the browser via pandoc.wasm without uploading files; **Mozilla PDF Viewer** — PDF.js browser-based PDF reader with full accessibility support

---

## 14. Loading overlay

Il `#loading-overlay` è un overlay fisso (`position: fixed`) che copre l'intera viewport durante le operazioni asincrone (aggiunta libro, apertura libro):

```html
<div id="loading-overlay" class="hidden">
  <div class="spinner"></div>
  <div id="loading-msg">Processing...</div>
</div>
```

**Spinner:** cerchio `40×40px` con `border-top: 4px solid #667eea`, animazione `spin 1s linear infinite`.

**Funzioni:**
```javascript
function showLoading(msg) {
  loadingMsg.textContent = msg;
  loadingOverlay.classList.remove('hidden');
}
function hideLoading() {
  loadingOverlay.classList.add('hidden');
}
```

**Messaggi usati:**
- `'Adding book to library...'` — durante import EPUB
- `'Opening Book...'` — durante apertura dal click sulla copertina

---

## 15. Switch tra Library e Reader

La Library e il Reader condividono lo stesso documento HTML. La visibilità alternata è gestita con la classe `.hidden` (`display: none !important`).

### 15.1 `showLibrary()`

```javascript
function showLibrary() {
  readerView.classList.add('hidden');
  libraryView.classList.remove('hidden');

  // Distrugge le istanze epub.js per liberare memoria
  if (book) { book.destroy(); book = null; }
  if (rendition) { rendition.destroy(); rendition = null; }
  
  // Pulisce DOM residuo del Reader
  document.getElementById('toc').innerHTML = '';
  document.getElementById('viewer').innerHTML = '';
  
  // Reset stato globale
  currentBookId = null;
  setStatusPath('');
  document.getElementById('saveStateBtn').disabled = true;
  
  // Reset highlights
  readerHighlights = [];
  currentReaderHighlightColor = 'yellow';
  _readerPendingCfi = null;
  // Reset visual del pulsante highlight
  
  // Chiude drawer bookmarks, svuota lista bookmarks in memoria
  closeUbmDrawer();
  userBookmarks = [];
  renderUbmList();
  
  // Ricarica la griglia libri (per riflettere eventuali modifiche fatte nell'Editor)
  loadLibraryBooks();
}
```

**Nota critica:** `loadLibraryBooks()` viene chiamata ogni volta che si torna alla Library. Questo è deliberato: se l'utente ha lavorato nell'Editor e salvato snapshot in IDB, la Library deve mostrare gli snapshot aggiornati. Il costo è una doppia query IDB ad ogni ritorno.

### 15.2 `showReader()`

```javascript
function showReader() {
  libraryView.classList.add('hidden');
  readerView.classList.remove('hidden');
}
```

Minima — lo switch visivo senza alcun reset. Tutta la logica di inizializzazione Reader è in `openBookFromLibrary()`.

---

## 16. Strutture di memorizzazione

### 16.1 Database `EpubLibraryDB`

| Proprietà | Valore |
|---|---|
| Nome | `EpubLibraryDB` |
| Versione | 1 |
| Object Store | `books` |
| keyPath | `id` (timestamp string) |
| Indici | nessuno |

**Record completo di un libro:**

```javascript
{
  // ── Campi base (scritti da saveBookToDB) ──
  id:       "1711530000000",           // Date.now().toString()
  title:    "Ulysses",
  author:   "James Joyce",
  data:     ArrayBuffer,               // file EPUB grezzo (può essere svariati MB)
  cover:    "data:image/jpeg;base64,…", // copertina in base64, o null
  addedAt:  1711530000000,             // timestamp milliseconds

  // ── Campo aggiunto da saveBookState() ──
  savedState: {
    fontSize:       100,               // percentuale, 50-200
    lineHeight:     1.2,               // da preset
    theme:          'normal',          // chiave THEME_COLORS
    scrollMode:     false,
    dualPageMode:   false,
    sidebarVisible: false,
    buttonZoom:     100,               // 90-130
    interface: {
      toolbarColor:    '#667eea',
      sidebarColor:    '#ffffff',
      navButtonsColor: '#667eea',
      navOpacity:      0.7,
      ubmDrawerColor:  '#fffde7'
    },
    position: {
      cfi:       'epubcfi(/6/4[s3]!/4/2)',
      href:      'OEBPS/chapter3.xhtml',
      timestamp: 1711530000000
    },
    readerHighlights: [
      { cfi: 'epubcfi(…)', color: 'yellow' }
    ],
    savedAt: 1711530000000
  },

  // ── Campo aggiunto da saveUserBookmarksToDB() ──
  userBookmarks: [
    {
      id:        "1711530000001_abc12",
      chapter:   "Capitolo III",
      preview:   "…estratto testo…",
      label:     "Nota importante",
      cfi:       'epubcfi(/6/4[s3]!/4/2)',
      href:      'OEBPS/chapter3.xhtml',
      createdAt: 1711530000001
    }
  ]
}
```

### 16.2 Database `noesisDB`

| Proprietà | Valore |
|---|---|
| Nome | `noesisDB` |
| Versione | 1 |
| Object Store | `extractedChapters` |
| keyPath | `chapterId` |
| Indici | `bookName` (non unique), `chapterName` (non unique) |

**Record completo di un capitolo estratto:**

```javascript
{
  chapterId:   "ch_1711530000000_987654",   // generato all'estrazione
  bookName:    "Ulysses",                    // usato per match con EpubLibraryDB
  chapterName: "Proteus",
  createdAt:   "2026-03-27T14:25:30.000Z",  // ISO 8601

  snapshots: [
    // Ordine nell'array: annot più recente, poi clean, poi origin (in fondo)
    {
      snapshotId:  "snap_1711530000001_111222",
      createdAt:   "2026-03-27T15:00:00.000Z",
      bookName:    "Ulysses",
      chapterName: "Proteus",
      description: "annot-20260327-150000-primaLettura",
      isOrigin:    false,
      content:     "<p>HTML annotato…</p>"
    },
    {
      snapshotId:  "snap_1711530000002_333444",
      createdAt:   "2026-03-27T15:00:01.000Z",
      description: "clean-20260327-150000-primaLettura",
      isOrigin:    false,
      content:     "<p>HTML pulito…</p>"
    },
    {
      snapshotId:  "snap_1711530000000_000001",
      createdAt:   "2026-03-27T14:25:30.000Z",
      description: "origin-20260327-142530",
      isOrigin:    true,               // snapshot originale dall'estrazione
      content:     "<p>Testo originale EPUB…</p>"
    }
  ]
}
```

### 16.3 `localStorage`

| Chiave | Tipo | Uso |
|---|---|---|
| `'noesis-lib-theme'` | `'dark'` / `'light'` | Tema corrente della Library |
| `'noesis-help-seen-library'` | `'1'` | Flag: banner Library già mostrato |
| `'noesis-help-seen-reader'` | `'1'` | Flag: banner Reader già mostrato |

### 16.4 Relazione tra i database

La Library legge **entrambi** i database in parallelo al caricamento:

```javascript
const [books, allChapters] = await Promise.all([
  getAllBooks(),                             // EpubLibraryDB
  getAllExtractedChapters().catch(() => [])  // noesisDB (tollerato il fallimento)
]);
```

Il `.catch(() => [])` garantisce che se `noesisDB` non è accessibile (primo avvio, browser restrittivi), la Library mostri comunque i libri senza capitoli.

**Il collegamento tra i due database è solo logico**, tramite corrispondenza case-insensitive del titolo del libro (`book.title` ↔ `ch.bookName`). Non esiste chiave esterna referenziale.

**Conseguenze:**
- Eliminare un libro da `EpubLibraryDB` **non** elimina i capitoli in `noesisDB`.
- Se un libro viene rinominato (impossibile nell'app attuale, ma potenzialmente via import), il collegamento si spezza.
- Se si aggiunge un nuovo libro con lo stesso titolo, i capitoli del vecchio libro riappariranno sotto il nuovo.

---

## 17. Variabili e costanti globali rilevanti

### 17.1 Costanti database

```javascript
// EpubLibraryDB
const DB_NAME    = 'EpubLibraryDB';
const DB_VERSION = 1;
const STORE_NAME = 'books';

// noesisDB
const NOESIS_DB_NAME    = 'noesisDB';
const NOESIS_DB_VERSION = 1;
const NOESIS_STORE      = 'extractedChapters';
```

### 17.2 Variabili di stato globali usate dalla Library

```javascript
// Riferimenti DOM
const libraryView    = document.getElementById('library-view');
const readerView     = document.getElementById('reader-view');
const bookGrid       = document.getElementById('bookGrid');
const loadingOverlay = document.getElementById('loading-overlay');
const loadingMsg     = document.getElementById('loading-msg');

// Stato Reader (resettati da showLibrary)
let book = null;               // istanza epub.js
let rendition = null;          // istanza rendition
let currentBookId = null;      // id libro in EpubLibraryDB
let currentBookTitle = '';     // titolo per estrazione capitoli

// Highlights (resettati da showLibrary)
let readerHighlights = [];
let currentReaderHighlightColor = 'yellow';
let _readerPendingCfi = null;

// Bookmarks (resettati da showLibrary)
let userBookmarks = [];
```

---

## 18. Responsive e adattamento mobile

### 18.1 Breakpoint mobile

```css
@media (max-width: 600px) {
  .library-header    { padding: 14px 16px 12px; }
  .library-grid      { padding: 16px 16px 40px; }
  .book-header       { gap: 12px; }
  .book-cover-thumb  { width: 52px; height: 72px; }   /* ridotta da 64×88 */
  .chapters-section  { padding-left: 64px; }           /* ridotto da 82px */
}
```

### 18.2 Truncation testo

Il titolo del libro usa CSS line-clamp per limitare a 2 righe:
```css
.book-meta-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

Il nome capitolo usa `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` per stare su una sola riga.

La descrizione snapshot usa anch'essa `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`.

### 18.3 Header scrollabile su mobile

La toolbar `.library-header-right` è un `flex row` con `gap: 10px`. Su schermi molto stretti potrebbe traboccare — non è presente scroll orizzontale esplicito, ma il layout flex gestisce l'overflow naturalmente con il wrapping implicito.

### 18.4 Compatibilità Android — Import Snapshots

Il sistema rileva automaticamente la disponibilità di `window.showDirectoryPicker` (non disponibile su Android/Safari) e fa fallback al file picker standard `#importSnapshotsInput` con `multiple`. Il file input ha `e.target.value = ''` dopo ogni uso per permettere la re-selezione degli stessi file.

### 18.5 Classi CSS legacy

Le seguenti classi esistono nel CSS ma sono impostate a `display: none` — sono residui dell'architettura precedente (grid di card) mantenuti per compatibilità:

```css
.book-card   { display: none; }
.delete-btn  { display: none; }
.book-info   { display: none; }
.book-cover  { display: none; }
.book-title  { display: none; }
.book-author { display: none; }
```

L'architettura corrente usa esclusivamente `.book-row`, `.book-header`, `.book-meta` e i relativi elementi.

---

*Fine documentazione — noesis-library-documentation.md*
