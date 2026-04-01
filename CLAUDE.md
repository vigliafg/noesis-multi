# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Progetto

**Noesis** è un reader EPUB + ambiente di studio completo, scritto interamente in vanilla JavaScript senza framework né bundler. Funziona come singolo file HTML apribile direttamente nel browser (`file://`), senza server.

## File principali

| File | Ruolo |
|------|-------|
| `noesis810.html` | **Applicazione completa** (6498 righe). Contiene tutto: CSS, HTML, JS inline. Questa è la versione "Regular" (dipendenze CDN esterne). |
| `noesis810-full.html` | Variante fully-offline (1.7 MB): stesse funzionalità, tutte le dipendenze (Bootstrap Icons font, JSZip, epub.js, editor sn56) incorporate come data URI o inline. |
| `noesis810.zip` / `noesis810-full.zip` | Archivi di distribuzione delle due varianti. |
| `style.css`, `site.js`, `translations.js` | Condivisi tra le pagine web del sito (index.html, doc-*.html, ecc.) — **non** usati da noesis810.html. |
| `DOC*.md`, `doc-*.md` | Documentazione tecnica di riferimento — fonte di verità per architettura e workflow. |

## Struttura interna di `noesis810.html`

```
righe 1–9        <head> — meta, CDN Bootstrap Icons
righe 10–2357    CSS inline (~2350 righe): library-view, reader-view, popup, drawer, temi, media query
righe 2358–2830  HTML strutturale statico: #library-view, #reader-view, overlay, pannelli
righe 2831–3030  JS — modulo noesisDB (capitoli estratti) + IDB bridge per finestre blob
righe 3031–3157  JS — modulo mainDB (libri EPUB: EpubLibraryDB)
righe 3158–3830  JS — core UI: variabili globali, show/hide, toast, libreria
righe 3831–6498  JS — logica reader: rendition, navigazione, temi, highlights, TOC, estrazione capitoli, sn56
```

### Commento marcatore obbligatorio per sn56

La sezione `<script type="application/json" id="sn56Source">` è delimitata da:
```html
<!-- SN56_SOURCE_START -->
...
<!-- SN56_SOURCE_END -->
```
Questi marcatori servono a identificare il blocco durante la generazione della versione Full. Non rimuoverli.

## Dipendenze esterne (versione Regular)

- **epub.js v0.3.93** — rendering EPUB in iframe, navigazione, TOC, CFI
- **JSZip v3.10.1** — decompressione ZIP (EPUB) per estrazione immagini; deve precedere epub.js
- **Bootstrap Icons v1.11.3** — icone CSS (`bi-*`)

L'editor popup **sn56.x** carica a sua volta (dal blob): jQuery, Summernote, Turndown, html-docx-js, Excalidraw, Pandoc WASM.

## Persistenza dati

**IndexedDB — due database separati:**

| Database | Store | Contenuto |
|----------|-------|-----------|
| `EpubLibraryDB` | `books` | EPUB (ArrayBuffer), metadata, stato lettore, highlights `[{cfi,color}]`, bookmarks `[{cfi,label,timestamp}]` |
| `noesisDB` | `chapters` | Metadata capitoli estratti e snapshot; il contenuto HTML non è salvato in IDB — viene scaricato come file |

**localStorage:** tema corrente, font-size/line-height predefiniti, flag banner help.

**File scaricati** (naming convention):
`noesis-{TYPE}-{BOOKNAME}__{CHAPTERNAME}__{YYYYMMDD_HHMMSS}_{CUSTOM}.html`

## Architettura viste

L'app ha due viste principali nello stesso documento:

- `#library-view` — catalogo libri, griglia con cover, gerarchia capitoli/snapshot
- `#reader-view` — lettore EPUB con sidebar TOC, toolbar, pannelli drawer

La transizione è gestita mostrando/nascondendo le viste (nessun routing).

## Editor sn56.x (popup)

L'editor è incorporato in `noesis810.html` come JSON dentro `#sn56Source`. Al lancio:
1. La stringa JSON viene estratta e parsata
2. Viene costruito un payload con il contenuto del capitolo
3. Il payload viene iniettato come `<script type="application/json" id="noesisPayload">` nell'HTML dell'editor
4. L'HTML viene convertito in Blob URL e aperto in un nuovo tab (`window.open`)

Poiché il blob gira in contesto `blob:null`, non può accedere direttamente all'IndexedDB del parent. La comunicazione avviene via `postMessage` (IDB bridge, righe ~3000–3030): supporta operazioni `get` e `put` sullo store `chapters`.

## Generazione versione Full

La versione `noesis810-full.html` si ottiene da `noesis810.html` incorporando:
1. **Bootstrap Icons**: font woff2 → Base64 in `@font-face { src: url("data:font/woff2;base64,...") }`
2. **JSZip ed epub.js**: sorgente minificato incollato inline in `<script>` (senza `src`)
3. **sn56Source**: editor con tutte le sue dipendenze già incorporate come data URI

Non esiste uno script di build nel repo. La versione Full viene prodotta manualmente seguendo le tecniche descritte in `DOC8_FULL_EMBEDDING.md`.

## Pattern JavaScript

- **Nessun modulo**: tutto in scope globale dentro `<script>` inline
- **Event delegation**: un singolo listener su `document` con check su `e.target`
- **Stato globale esplicito**: variabili `let` a livello di file (`book`, `rendition`, `fontSize`, `currentTheme`, ecc.)
- **Async/await** per IndexedDB e operazioni su file
- **DOM manipulation pura**: `getElementById`, `innerHTML`, `classList`

## Come sviluppare

**Aprire l'app:**
```bash
# Direttamente nel browser (consigliato)
xdg-open noesis810.html

# Oppure con server locale per le pagine web del sito
python3 -m http.server 8000
```

Non esiste un processo di build, test automatici o linter configurato nel repo. Le modifiche si apportano direttamente ai file HTML.

## Documentazione interna

I file `DOC1_FUNZIONALITA.md` … `DOC8_FULL_EMBEDDING.md` sono la documentazione tecnica completa e aggiornata. Consultarli prima di modificare aree non familiari:

| File | Argomento |
|------|-----------|
| DOC1 | Funzionalità complete |
| DOC2 | Workflow utente (import, lettura, estrazione, editor) |
| DOC3 | Struttura del codice, variabili globali, pattern |
| DOC4 | Schemi dati IndexedDB e localStorage |
| DOC5 | Guida CSS e sistema di temi |
| DOC6 | Struttura HTML del DOM |
| DOC7 | Pattern per estendere le funzionalità |
| DOC8 | Tecnica di embedding per la versione Full |
