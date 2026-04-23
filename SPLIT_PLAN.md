# SPLIT_PLAN — Noesis: Split della versione Full

Piano operativo riutilizzabile per tutte le versioni presenti e future di Noesis.
Descrive come generare i due file derivati dal sorgente `noesisNNN-full.html`.

---

## Architettura dei file

| File | Dimensione tipica | Contenuto |
|------|-------------------|-----------|
| `noesisNNN-full.html` | ~1.7 MB | **Sorgente** — Library + Reading + Editor (sn56). Tutte le dipendenze embedded. |
| `noesisNNN-full-reader.html` | ~790 KB | **Output** — Library + Reading. Nessun editor, nessuna UI snapshot. |
| `noesisNNN-full-editor.html` | ~870 KB | **Output** — Editor sn56 standalone. Estratto dal JSON `sn56Source`. |

Il file full è l'unico che va modificato manualmente; reader ed editor si rigenerano con lo script.

---

## Generazione automatica

```bash
cd <repo>
python3 split_noesis.py --version 812
```

Produce `noesis812-full-reader.html` e `noesis812-full-editor.html` nella stessa cartella.
Alla fine lo script esegue automaticamente le verifiche e riporta `✅ All checks passed` per ciascun file.

---

## Tabella inclusioni / esclusioni

| Elemento | Full | Reader | Editor |
|----------|------|--------|--------|
| Library (griglia libri) | ✓ | ✓ | — |
| Reader EPUB (rendition, TOC, highlights) | ✓ | ✓ | — |
| Estrazione capitoli → IDB + download file | ✓ | ✓ | — |
| Auto-lancio editor dopo estrazione | ✓ | ✗ rimosso | — |
| sn56Source block (~912 KB) | ✓ | ✗ rimosso | estratto |
| IDB bridge postMessage (`__noesisIDB`) | ✓ | ✗ rimosso | built-in |
| Import Snapshots (pulsante + input file) | ✓ | ✗ rimosso | — |
| Pulsante "Open Editor" in library header | ✓ | ✗ rimosso | — |
| Schede capitoli estratti in library | ✓ | ✗ rimosso | — |
| Salvataggio IDB capitoli estratti (`noesisDB`) | ✓ | ✓ | — |
| Editor sn56 standalone | — | — | ✓ |

---

## Operazioni eseguite sul reader (ordine)

### Step 1 — Rimozione blocco sn56Source

Marcatori obbligatori nel sorgente full (non rimuovere):

```html
<!-- SN56_SOURCE_START -->
<script type="application/json" id="sn56Source">...</script>
<!-- SN56_SOURCE_END -->
```

### Step 2 — Rimozione funzioni JS

| Funzione | Pattern di ricerca |
|----------|--------------------|
| `_openSn56` | `function _openSn56(` |
| `_openExtractedEnv` | `function _openExtractedEnv(` |
| `getAllExtractedChapters` | `async function getAllExtractedChapters(` |
| `importSnapshotsFromDisk` | `function importSnapshotsFromDisk(` |
| `_processSnapshotFiles` | `async function _processSnapshotFiles(` |

L'algoritmo conta le parentesi graffe dalla prima `{` fino alla chiusura bilanciata: gestisce correttamente template literal `${}`.

### Step 3 — Rimozione IDB bridge

Il blocco è delimitato da marcatori obbligatori (mantenere nel sorgente):

```js
    // ── IDB bridge: serve requests from child windows (blob:null context) ──
    ...
    // ── END IDB bridge ────────────────────────────────────────────────────
```

### Step 4 — Rimozione chiamate `_openSn56` dalle funzioni di estrazione

Due occorrenze, una in `extractCurrentChapter()` e una in `extractMultipleSections()`.
Entrambe sono marcate con il commento (mantenere nel sorgente):

```js
        // ── Apri sn56.x con payload ──
        _openSn56({ ... });
```

Lo script rimuove dal commento fino alla fine di `});` incluso, per due volte.

### Step 5 — Semplificazione `loadLibraryBooks()`

Rimozione del rendering di capitoli estratti e snapshot, mantenendo solo i libri:

| Operazione | Pattern di ricerca |
|------------|--------------------|
| Replace `Promise.all(...)` → `getAllBooks()` | Stringa esatta di 4 righe |
| Rimozione blocco `chaptersByBook` | Commento `// Group chapters by bookName` |
| Rimozione variabili badge capitoli | Commento `// Find extracted chapters for this book` → stop prima di `bookRow.innerHTML` |
| Rimozione riga stats nel template innerHTML | Stringa esatta `<div class="book-meta-stats">${chBadge}${snapBadge}</div>` |
| Rimozione `<div class="chapters-section">` dal template | Stringa esatta |
| Rimozione blocco "Build chapters section" | Commento `// Build chapters section` → stop prima di `bookGrid.appendChild(bookRow)` |

### Step 6 — Rimozione elementi HTML dalla library header

| ID elemento | Tag |
|-------------|-----|
| `importSnapshotsInput` | `<input>` (void) |
| `libImportSnapshotsBtn` | `<button>` |
| `libEditorBtn` | `<button>` |

### Step 7 — Rimozione handler IIFE (Import Snapshots + Open Editor)

```js
// ── Handler: Import Snapshots ─
(function() {
    ...
    })();
```

Anchor di inizio: `// ── Handler: Import Snapshots ─`
Anchor di fine (incluso): `    })();\n`

### Step 8 — Rimozione regole CSS snapshot

Classi rimosse (brace-counting per trovare la chiusura di ciascuna regola):

- `.snapshots-list`
- `.snapshot-item`
- `.snapshot-item-dot`
- `.snapshot-item-desc`
- `.snapshot-item-date`
- `.snapshot-delete-btn`

### Step 9 — Aggiornamento testo subtitle library

```
"books, extracted chapters &amp; snapshots"  →  "books"
```

---

## Operazione per l'editor

Lo script trova il tag `<script type="application/json" id="sn56Source">`, estrae il contenuto, lo decodifica con `json.loads()` e scrive la stringa HTML risultante nel file di output.

Il file editor:
- È già fully-embedded (Bootstrap Icons, JSZip, epub.js, jQuery, Summernote, Excalidraw, Pandoc WASM tutti inline)
- Si apre nel browser come editor vuoto standalone (nessun `noesisPayload` → editor in bianco)
- Il bridge IDB invia postMessage a `window.opener` → timeout silenzioso → "Saved to disk only"

---

## Marcatori obbligatori da mantenere nel sorgente full

Questi marcatori **non devono essere rimossi** dal sorgente `noesisNNN-full.html` poiché lo script li usa come anchor stabili:

```html
<!-- SN56_SOURCE_START -->
<!-- SN56_SOURCE_END -->
```

```js
    // ── IDB bridge: serve requests from child windows (blob:null context) ──
    // ── END IDB bridge ────────────────────────────────────────────────────
```

```js
        // ── Apri sn56.x con payload ──    (2 occorrenze)
```

```js
// ── Handler: Import Snapshots ─
```

---

## Verifiche automatiche

Lo script esegue le verifiche automaticamente dopo ogni output.

### Reader — pattern assenti (devono risultare 0)

```
sn56Source · _openSn56 · importSnapshotsBtn · libEditorBtn · __noesisIDB
getAllExtractedChapters · _openExtractedEnv · importSnapshotsFromDisk
_processSnapshotFiles · chaptersByBook
```

### Reader — pattern presenti (devono esistere)

```
extractCurrentChapter · extractMultipleSections · loadLibraryBooks
saveExtractedChapterToDB · openNoesisDB
```

### Editor — controlli

- Zero riferimenti `cdn.jsdelivr.net` e `code.jquery.com`
- Almeno 1 URI `data:font/woff2;base64`

### Verifica manuale rapida (terminale)

```bash
# Reader — tutto deve restituire 0
grep -c "sn56Source\|_openSn56\|importSnapshotsBtn\|libEditorBtn\|__noesisIDB" noesis812-full-reader.html

# Editor — deve restituire 0
grep -c "cdn\.jsdelivr\.net\|code\.jquery\.com" noesis812-full-editor.html

# Dimensioni
wc -c noesis812-full-reader.html   # ~810.000 byte (~790 KB)
wc -c noesis812-full-editor.html   # ~892.000 byte (~871 KB)
```

---

## Adattamento a una nuova versione

Quando si rilascia `noesisNNN-full.html` con N > 812:

1. Verificare che i marcatori obbligatori (sezione sopra) siano ancora presenti nel sorgente
2. Eseguire lo script con `--version NNN`
3. Se qualche step produce `⚠`, identificare il pattern cambiato e aggiornare lo script
4. Aggiornare questo documento se il processo è cambiato strutturalmente

Le situazioni che richiedono intervento manuale sullo script sono:

| Situazione | Cosa aggiornare |
|------------|----------------|
| Funzione rinominata | Aggiornare la lista `for fn in [...]` in `build_reader()` |
| Commento marcatore modificato | Aggiornare la stringa anchor nel passo corrispondente |
| Nuovo elemento HTML da rimuovere | Aggiungere l'ID alla lista `for eid in [...]` |
| Nuovo blocco CSS snapshot | Aggiungere la classe a `targets` in `remove_snapshot_css()` |
| Template `bookRow.innerHTML` modificato | Aggiornare le stringhe esatte in `simplify_load_library_books()` |

---

## File prodotti (versione 812)

| File | Dimensione | Data |
|------|------------|------|
| `noesis812-full.html` | 1.704 KB | 2026-04-22 |
| `noesis812-full-reader.html` | 793 KB | 2026-04-22 |
| `noesis812-full-editor.html` | 871 KB | 2026-04-22 |
