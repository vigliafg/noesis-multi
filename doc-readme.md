# README — Panoramica di Noesis

> Versione: **v810** | Licenza: MIT | Architettura: No Server | Stack: Vanilla JS

---

## Cos'è Noesis

Noesis è un **ambiente di studio integrato per libri EPUB**, progettato per funzionare come singola pagina HTML autocontenuta nel browser. Zero server, zero account, zero tracciamento. Funziona completamente offline dopo il primo caricamento.

La filosofia è sintetizzabile in un concetto: **Reading-to-Knowledge System** — non un semplice reader, ma un ambiente che trasforma la lettura in produzione attiva di conoscenza: annotazione, selezione, rielaborazione, versioning, esportazione.

---

## Screenshot

| My Library | Lettura (Reader) | Estrazione → Editor | Noesis Editor (sn56.x) |
|------------|-------------------|---------------------|------------------------|
| Libreria gerarchica con snapshot | Sidebar espandibile con indice | Estrazione apre direttamente in Editor | Toolbar, chunk, snapshot, export |

---

## Funzionalità Principali

### Lettura EPUB

- Rendering completo di file `.epub` tramite epub.js
- Sommario gerarchico espandibile (fino a 3 livelli)
- 3 modalità di visualizzazione: pagina singola, doppia pagina, scorrimento continuo
- 15 temi di lettura raggruppati in 5 categorie (chiari, caldi, grigi chiari, grigi scuri, notturni)
- Regolazione tipografica: font size, interlinea, layout
- Salvataggio automatico della posizione di lettura

### Annotazione e Studio

- Evidenziazione a 3 colori (giallo, verde, rosa) con rimozione selettiva
- Segnalibri personali con CFI (Canonical Fragment Identifiers), persistenti tra sessioni
- Traduzione integrata via funzione nativa del browser (zero API esterne)

### Estrazione Capitoli

- Modalità "solo corrente": estrae il capitolo attivo
- Modalità "corrente + sottolivelli": assembla automaticamente capitolo e tutti i sottolivelli annidati
- Output: il capitolo estratto si apre **direttamente in Noesis Editor (sn56.x)** con toolbar completa, evidenziazioni e opzioni di export

### Sistema Snapshot (doppia memorizzazione)

- Salvataggio dello stato del documento dall'Editor in qualsiasi momento
- **Doppia memorizzazione**: 
  - IndexedDB (`noesisDB`) per accesso rapido dalla Library
  - Filesystem locale (download automatico) come backup persistente
- Naming schema: `noesis-{TIPO}-{BOOK}__{CHAPTER}__{YYYYMMDD_HHMMSS}_{CUSTOM}.html`
- Varianti: `origin` (reimportabile, con meta tag), `clean` (senza highlight), `annot` (con highlight)
- Import Snapshots: reimportazione di file salvati con riconoscimento automatico tramite meta tag

### Editor WYSIWYG — sn56.x (Noesis Editor)

- Editor Summernote 0.9.1 embedded, aperto in nuovo tab via Blob URL
- **Due modalità**:
  - `chapter`: caricato con HTML del capitolo, contesto bibliografico, salvataggio in IDB + filesystem
  - `standalone`: editor vuoto, salvataggio solo su filesystem
- **Tre percorsi di accesso**:
  1. Library → Open Editor (standalone)
  2. Library → click capitolo/snapshot (chapter)
  3. Reader → Extract (chapter - si apre direttamente in Editor)
- Raccolta Chunk: selezione testo, immagini e tabelle dal documento
- Inspect Panel flottante per gestire e iniettare chunk
- **Excalidraw integrato**: diagrammi, flowchart e mappe mentali in tab dedicata; esporta SVG/PNG
- Export documento: TXT, MD, MD+ZIP, JSON, DOCX, PDF
- Export collezione: JSON, HTML, MD, MD+ZIP

### Libreria Gerarchica

- Vista catalogo con copertine, titoli, autori
- Gerarchia: Libro → Capitoli estratti → Snapshot versioni
- Badge contatori per estratti e snapshot per libro
- Accesso diretto a qualsiasi snapshot con un click

---

## Stack Tecnologico

| Componente | Tecnologia | Note |
|-----------|-----------|------|
| Linguaggio | HTML5 + CSS3 + JS vanilla | Nessun framework |
| EPUB parsing/rendering | epub.js 0.3.93 | CDN |
| Decompressione ZIP | JSZip 3.10.1 | CDN |
| Icone | Bootstrap Icons 1.11.3 | CDN |
| Editor WYSIWYG (sn56.x) | Summernote 0.9.1 lite | CDN, in sn56.x |
| DOM manipulation (sn56.x) | jQuery 3.7.1 | CDN, in sn56.x |
| Export Markdown (sn56.x) | Turndown | CDN, in sn56.x |
| Export DOCX (sn56.x) | html-docx-js | CDN, in sn56.x |
| Export ZIP (sn56.x) | JSZip | CDN, in sn56.x |
| Build | Python 3 (`build.py`) | Embedding sn56.x |
| Test E2E | Playwright @1.52.0 | |

---

## Persistenza Dati

| Store | Tipo | Contenuto |
|-------|------|-----------|
| `EpubLibraryDB` | IndexedDB | File EPUB binari (ArrayBuffer), metadati, posizione lettura, segnalibri |
| `noesisDB` | IndexedDB | Metadati capitoli estratti, snapshot (content HTML + metadata) |
| `localStorage` | Browser | Tema corrente, preferenze font, flag help |
| Filesystem locale | File HTML | Snapshot export (clean + annot), export vari |

**Privacy by design**: nessun byte lascia il dispositivo. Funziona offline dopo il primo caricamento.

---

## Installazione

### Metodo diretto (più semplice)

1. Scaricare `noesis810.html`
2. Doppio click sul file nel browser

### Server locale (consigliato per EPUB con risorse esterne)

```bash
python3 -m http.server 8000
# Aprire: http://localhost:8000/noesis810.html
```

---

## Browser Supportati

| Browser | Versione | Supporto |
|---------|----------|----------|
| Chrome / Edge | 90+ | Completo |
| Firefox | 88+ | Completo |
| Opera | 76+ | Completo |
| Safari | 14+ | Parziale (limitazioni IndexedDB) |

**Nota**: `showDirectoryPicker()` (import snapshot da cartella) richiede Chrome/Edge 86+. Su altri browser si usa il file picker standard.

---

## Workflow in 5 Passi

1. **Import EPUB** — Aggiungi il libro tramite "ADD BOOK" nella Library
2. **Leggi e annota** — Naviga via TOC, evidenzia (3 colori), aggiungi segnalibri
3. **Estrai il capitolo** — Click "Extract Chapter" → si apre direttamente in **Noesis Editor (sn56.x)**
4. **Snapshot** — Salva versioni del documento dall'Editor (IDB + filesystem)
5. **Editor e Export** — Edita con Summernote, raccogli chunk, esporta in DOCX, MD, PDF o altri formati

---

## Toolbar — Riferimento completo

### Library (toolbar header)

| Pulsante | ID | Funzione |
|----------|-----|----------|
| Add Book | `#importLabel` / `#libraryInput` | Apre il file picker per importare file EPUB. Salva in `EpubLibraryDB`. |
| Import Snapshots | `#importSnapshotsBtn` | Reimporta file snapshot HTML da disco in `noesisDB`. Supporta folder picker (Chrome/Edge) o file picker standard. |
| Open Editor | `#libOpenEditorBtn` | Apre Noesis Editor (sn56.x) in modalità *standalone* — editor vuoto senza contesto libro. |
| Toggle Theme | `#libThemeToggle` | Alterna tema chiaro/scuro. Preferenza salvata in `localStorage`. |
| Tools ▾ | `#libToolsBtn` / `#libToolsMenu` | Dropdown con strumenti esterni: noesis-epub-tools, Pandoc Online, Mozilla PDF Viewer. |
| Help | `#libHelpBtn` | Apre l'overlay di aiuto contestuale con guida ai controlli della Library. |

### Reader (toolbar principale)

| Pulsante | Funzione |
|----------|----------|
| Toggle Sidebar | Mostra/nasconde il TOC con indice gerarchico espandibile |
| User Bookmarks | Apre il cassetto segnalibri con badge contatore |
| Highlight ▾ | Dropdown colori: Giallo, Verde, Rosa, Nessuno/Rimuovi |
| Display Settings | Pannello accordion unificato: tipografia, 15 temi di lettura, colori interfaccia e opacità |
| Scroll Mode | Toggle scorrimento continuo ↔ navigazione paginata |
| % Zoom | Scala la dimensione dei pulsanti toolbar: 90%–130% |
| Save State | Salva manualmente posizione e preferenze del libro |
| Extract Chapter | Dropdown: solo corrente / corrente + sottolivelli |

> **Nota:** L'ambiente "Capitolo estratto" è ora **unificato** con il **Noesis Editor (sn56.x)**. Quando estrai un capitolo dal Reader, si apre direttamente nell'Editor con toolbar completa.

### Editor WYSIWYG

| Pulsante | Funzione |
|----------|----------|
| B I U S | Grassetto, corsivo, sottolineato, barrato |
| H1 H2 H3 | Intestazioni e paragrafo |
| • L 1.L | Lista puntata e lista numerata |
| 🖼️ | Inserimento immagine da file locale (base64 inline) |
| A− A+ | Font size (8–28px) |
| ⚙️ | Plugin tabelle: toolbar contestuale flottante |
| Print / PDF | Stampa nativa con @media print ottimizzato |
| </> | Copia HTML negli appunti |

### Editor — Sezione Chapter (bordo giallo)

| Pulsante | ID | Funzione |
|----------|-----|----------|
| New | `#chNewBtn` | Crea nuovo documento. Chiede conferma se contenuto corrente da salvare. |
| Import | `#chImportBtn` | Apre dialog per importare da IDB (snapshot esistenti) o da file HTML. |
| Save | `#chExportMainBtn` | Salva doppio snapshot (clean + annotated) + in IndexedDB. Download automatico di due file HTML. |
| More formats | `#chMoreBtn` | Export: TXT, MD, MD+ZIP, JSON, PDF, DOCX. |

### Editor — Sezione Collection (bordo azzurro)

| Pulsante | ID | Funzione |
|----------|-----|----------|
| Add [+N] | `#addChunkBtn` | Aggiunge selezione (testo/immagine/tabella) alla collezione. Badge mostra numero chunk. |
| Import JSON | — | Importa collezione da file JSON. Aggiunge ai chunk esistenti. |
| Export JSON | — | Esporta collezione come JSON con metadati. |
| More formats | `#colMoreBtn` | Export: MD, MD+ZIP, HTML standalone. |
| Inspect | `#inspectPanel` | Apre pannello flottante per gestione avanzata chunk (drag, inject, delete). |
| Clear | — | Svuota la collezione. Richiede conferma. |

### Editor — Tools

| Strumento | Funzione |
|-----------|----------|
| Excalidraw | Apre Noesis Excalidraw in nuovo tab — diagrammi, flowchart, mappe mentali. Esporta SVG/PNG. |

---

## Licenza

MIT License — uso personale e commerciale consentito senza restrizioni.
