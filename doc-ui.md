# UI — Riferimento Pulsanti

> Versione: **v810** | Mappa completa di tutti i controlli dell'interfaccia per ambiente

---

## Architettura degli Ambienti

Noesis opera in tre ambienti distinti:

1. **LIBRARY** — Catalogo gerarchico libri, estratti e snapshot
2. **READER** — Lettura EPUB con annotazione e estrazione
3. **EDITOR (sn56.x)** — Editor WYSIWYG con chunk, snapshot e export

L'Editor si apre in un **nuovo tab** tramite Blob URL e comunica con la Library tramite `postMessage` per l'accesso a IndexedDB.

---

## LIBRARY — Catalogo Gerarchico

Punto di ingresso dell'app. Mostra tutti i libri importati con la loro gerarchia di estratti e snapshot.

### Header Controls

| Controllo | ID / Classe | Icona | Funzione |
|-----------|------------|-------|----------|
| Toggle Tema | `#libThemeToggle` | `bi-moon` / `bi-sun` | Alterna modalità light/dark; salva in localStorage |
| Add Book | `#importLabel` | — | Apre file picker per import `.epub`; salva in `EpubLibraryDB` |
| Import Snapshots | `#importSnapshotsBtn` | `bi-cloud-upload` | Reimporta file snapshot HTML da disco in `noesisDB` |
| Open Editor | `#libOpenEditorBtn` | — | Apre sn56.x in modalità `standalone` (editor vuoto) |
| Tools ▾ | — | `bi-tools` | Dropdown con strumenti esterni |

### Dropdown Tools (Library)

| Strumento | Funzione |
|-----------|----------|
| noesis-epub-tools | Editor e gestione avanzata file EPUB |
| **Pandoc Online** | Convertitore formato documento via `pandoc.wasm` nel browser — Markdown, DOCX, HTML, LaTeX, EPUB, ODT e altri. Nessun upload di file. |
| Mozilla PDF Viewer | Lettore PDF basato su PDF.js |

### Struttura Riga Libro

- **Copertina** — Click → apre il libro nel Reader (ripristina ultima posizione)
- **Titolo / Autore** — Informativo
- **Badge estratti** — Numero di capitoli estratti per quel libro
- **Badge snapshot** — Numero totale di snapshot per quel libro
- **Pulsante elimina** (`bi-trash`) — Rimuove il libro con conferma

### Gerarchia Estratti

Per ogni libro vengono mostrati i capitoli estratti con le rispettive versioni:

- **Nome capitolo** — Click → apre il capitolo nell'Editor con l'ultimo snapshot
- **Contatore snapshot** — Numero di versioni salvate
- **Lista snapshot** (dal più recente) — Ogni riga riporta descrizione e timestamp
  - Click su snapshot → apre quella versione specifica nell'Editor

---

## READER — Ambiente di Lettura

### Toolbar Principale

| Controllo | ID | Funzione |
|-----------|-----|----------|
| Back to Library | — | Torna alla Library View |
| Nome file | `#fileName` | Mostra titolo libro corrente (informativo) |
| Extract Chapter | `#extractBtn` | Apre menu estrazione capitolo |
| Highlights | `#readerHighlightBtn` | Apre menu colori highlight |
| Display | `#displayBtn` | Apre pannello unificato Tipografia + Temi + Interfaccia |
| Bookmarks | `#userBookmarksBtn` | Apre drawer segnalibri personali |
| Save State | `#saveStateBtn` | Salva posizione + tema + impostazioni correnti |

### Sidebar — Sommario (TOC)

- Toggle sidebar (`bi-layout-sidebar`) — Mostra/nasconde il pannello laterale
- TOC gerarchico espandibile fino a 3 livelli
- Click su voce → navigazione diretta al capitolo (`rendition.display(href)`)

### Pannello Display (Unificato)

Il pannello `#displayBtn` riunisce tre sezioni collassabili:

**Tipografia**
- Font size: slider o pulsanti A− / A+
- Interlinea: slider o pulsanti
- Layout: pagina singola / doppia colonna

**Temi di Lettura** (15 temi in 5 gruppi)

| Gruppo | Temi |
|--------|------|
| Chiari | White, Soft White |
| Caldi | Cream, Sepia, Parchment |
| Grigi chiari | Gray, Cool Gray, Warm Gray |
| Grigi scuri | Mid Gray, Slate, Dark Gray |
| Notturni | Charcoal, Dark, Midnight, True Black |

**Interfaccia**
- Color picker toolbar
- Color picker sidebar
- Color picker pulsanti navigazione
- Slider opacità (0–100%)

### Menu Extract Chapter

Tre modalità di estrazione:

| Modalità | Funzione |
|----------|----------|
| `current` | Estrae solo il contenuto del capitolo corrente |
| `tree` | Estrae capitolo corrente + tutti i sottolivelli annidati |

Output: documento HTML standalone con immagini base64 inline, aperto in sn56.x.

### Menu Highlights (Reader)

Usa le **EPUB CFI Annotations** di epub.js:

| Colore | CSS class |
|--------|-----------|
| Giallo | `highlight-yellow` |
| Verde | `highlight-green` |
| Rosa | `highlight-pink` |
| Rimuovi | Rimuove l'annotazione CFI attiva |

### Drawer Segnalibri Personali

- Pulsante "Aggiungi segnalibro" — Cattura CFI corrente con label personalizzabile
- Lista segnalibri con data e label
- Click su segnalibro → navigazione alla posizione CFI
- Elimina segnalibro individuale
- Badge contatore sull'icona

---

## EDITOR (sn56.x) — Noesis Editor / Summernote Editor

L'Editor viene aperto come **blob URL in un nuovo tab** dalla Library o dal Reader. Comunica con la finestra principale tramite `postMessage` per accedere a IndexedDB (IDB Bridge).

### Layout interfaccia

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER (#0a84ff blu)                                        │
│ "Nome capitolo / Noesis Editor"              [?] Help      │
├─────────────────────────────────────────────────────────────┤
│ SUMMERNOTE TOOLBAR (generata da Summernote)                │
├─────────────────────────────────────────────────────────────┤
│ AREA EDITOR WYSIWYG (.note-editable)                       │
│ (altezza dinamica, occupa tutto lo spazio disponibile)     │
├─────────────────────────────────────────────────────────────┤
│ BOTTOM TOOLBAR (#111 nero)                                 │
│ [CHAPTER] [COLLECTION] [TOOLS]                              │
└─────────────────────────────────────────────────────────────┘
```

### I tre percorsi di accesso

1. **Library → Open Editor** — Apre editor vuoto (modalità standalone)
2. **Library → click nome capitolo/snapshot** — Apre con snapshot più recente o specifico (modalità chapter)
3. **Reader → Extract** — Estrae capitolo e apre immediatamente in editor (modalità chapter)

### Modalità operative

| Modalità | Caratteristiche |
|----------|-----------------|
| **chapter** | Contenuto HTML caricato, contesto bibliografico (bookName, chapterName, chapterId), salvataggio in IDB + filesystem |
| **standalone** | Editor vuoto, nessun contesto, salvataggio solo su filesystem |

### Bottoniera inferiore — Chapter Section (bordo giallo)

| Controllo | Funzione |
|-----------|----------|
| New (`#chNewBtn`) | Crea nuovo documento, chiede conferma se contenuto corrente |
| Import (`#chImportBtn`) | Apre dialog per importare da IDB o file HTML |
| Save (`#chExportMainBtn`) | Salva doppio snapshot (clean + annotated) + in IDB |
| More formats (`#chMoreBtn`) | Export: TXT, MD, MD+ZIP, JSON, PDF, DOCX |

### Bottoniera inferiore — Collection Section

| Controllo | Funzione |
|-----------|----------|
| Add (`#addChunkBtn`) | Aggiunge selezione (testo/img/tabella) alla collezione |
| Import JSON | Importa collezione da file JSON |
| Export JSON | Esporta collezione come JSON |
| More formats | Export: MD, MD+ZIP, HTML standalone |
| Inspect (`#inspectPanel`) | Apre pannello flottante per gestione chunk |
| Clear | Svuota la collezione |

### Inspect Panel — Pannello Chunk

Pannello flottante draggable/resizable per gestione avanzata chunk:
- Lista chunk con anteprima
- Selezione multipla checkbox
- Azioni: Inject al cursore, Fullscreen, Delete
- Inject di gruppo per tutti i chunk selezionati

### Sistema Snapshot (doppia memorizzazione)

Il pulsante **Save** genera quattro output simultanei:

| # | Destinazione | File/Oggetto | Descrizione |
|---|---|---|---|
| 1 | Filesystem | `noesis-clean-…html` | HTML senza background-color |
| 2 | Filesystem | `noesis-annot-…html` | HTML con highlight preservati |
| 3 | IndexedDB | snapshot `annot-…` | JSON in IDB |
| 4 | IndexedDB | snapshot `clean-…` | JSON in IDB |

**Schema naming:** `noesis-{tipo}-{BOOK}__{CHAPTER}__{YYYYMMDD_HHMMSS}[_{label}].html`

### Toolbar Summernote

Formattazione testo:

| Funzione | Comando |
|----------|---------|
| Bold | `bold` |
| Italic | `italic` |
| Underline | `underline` |
| Strikethrough | `strikethrough` |
| Heading H1, H2, H3 | `formatBlock` |
| Paragrafo | `formatBlock p` |
| Lista puntata | `insertUnorderedList` |
| Lista numerata | `insertOrderedList` |
| Font size | 8–28px |
| Inserisci immagine | Base64 inline |
| Inserisci tabella | Plugin tabella con toolbar flottante |

**Tabelle**: toolbar contestuale flottante per aggiunta/rimozione righe e colonne.

### Chunk Collection

| Controllo | Funzione |
|-----------|----------|
| Seleziona testo/immagine/tabella | Aggiunge elemento alla collezione chunk |
| Badge contatore | Mostra numero di chunk raccolti |
| Inspect Panel (flottante) | Apre pannello di gestione chunk |

**Inspect Panel** — Pannello flottante ridimensionabile:
- Lista chunk raccolti con anteprima
- Riordina chunk tramite drag
- Inietta chunk singolo al cursore
- Assembla tutti i chunk nel documento
- Elimina chunk dalla collezione

### Save Snapshot

Genera automaticamente due file scaricati su disco:

| File | Variante | Contenuto |
|------|---------|-----------|
| `noesis-clean-...html` | `clean` | Documento senza highlight (solo testo e struttura) |
| `noesis-annot-...html` | `annot` | Documento con highlight inline |

**Naming schema**:
```
noesis-{VARIANT}-{BOOKNAME}__{CHAPTERNAME}__{YYYYMMDD_HHMMSS}_{CUSTOM}.html
```

**Meta tag nei file `origin`** (reimportabili):
```html
<meta name="noesis-chapter-id"       content="ch_...">
<meta name="noesis-book-name"        content="...">
<meta name="noesis-chapter-name"     content="...">
<meta name="noesis-snapshot-variant" content="origin|clean|annot">
```

### Tools (Editor)

| Strumento | Funzione |
|-----------|----------|
| **Excalidraw** (`bi-diagram-3`) | Apre Noesis Excalidraw in un nuovo tab — fork di Excalidraw per diagrammi, flowchart, mappe mentali e schizzi visivi. Esportabile come SVG o PNG; salvataggio locale nel browser. |

---

### Export Documento

| Formato | Descrizione |
|---------|-------------|
| TXT | Testo puro |
| MD | Markdown (via Turndown) |
| MD+ZIP | Markdown + immagini estratte in archivio ZIP |
| JSON | Documento come struttura JSON |
| DOCX | Microsoft Word (via html-docx-js) |
| PDF | Stampa nativa browser con CSS ottimizzati per A4 |

### Export Collezione

| Formato | Descrizione |
|---------|-------------|
| JSON | Chunk come array JSON (importabile) |
| HTML | Chunk come documento HTML standalone |
| MD | Chunk in Markdown |
| MD+ZIP | Chunk in Markdown + immagini ZIP |

---

## Riepilogo Icone Bootstrap Icons

| Ambiente | Funzione | Icona |
|----------|----------|-------|
| Library | Toggle Tema | `bi-moon` / `bi-sun` |
| Library | Elimina libro | `bi-trash` |
| Library | Import Snapshots | `bi-cloud-upload` |
| Reader | Toggle Sidebar | `bi-layout-sidebar` |
| Reader | Segnalibri | `bi-bookmark-star` |
| Reader | Display Panel | `bi-sliders` |
| Reader | Highlights | `bi-highlighter` |
| Reader | Save State | `bi-floppy2` |
| Editor | Snapshot | `bi-camera` (viola) |
| Editor | History | `bi-clock-history` (viola scuro) |
| Editor | Collezione | `bi-collection-fill` |
| Editor | Tabella | `bi-table` |
| Editor | Immagine | `bi-image` |
| Editor | Stampa | `bi-printer` |
| Editor | Excalidraw | `bi-diagram-3` |
| Library | Tools dropdown | `bi-tools` |
