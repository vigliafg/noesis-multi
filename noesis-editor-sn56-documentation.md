# Noesis Editor (sn56.x) — Documentazione Tecnica Completa

**Versione di riferimento:** noesis810.html  
**Data documento:** 2026-03-27  

---

## Indice

1. [Panoramica generale](#1-panoramica-generale)  
2. [Architettura tecnica e struttura del file](#2-architettura-tecnica-e-struttura-del-file)  
3. [I tre percorsi di accesso all'editor](#3-i-tre-percorsi-di-accesso-alleditor)  
4. [Interfaccia utente — layout e componenti](#4-interfaccia-utente--layout-e-componenti)  
5. [Bottoniera inferiore — sezione Chapter](#5-bottoniera-inferiore--sezione-chapter)  
6. [Bottoniera inferiore — sezione Collection](#6-bottoniera-inferiore--sezione-collection)  
7. [Bottoniera Summernote (toolbar WYSIWYG)](#7-bottoniera-summernote-toolbar-wysiwyg)  
8. [Doppia memorizzazione degli snapshot: clean e annotated](#8-doppia-memorizzazione-degli-snapshot-clean-e-annotated)  
9. [Memorizzazione simultanea IDB + filesystem](#9-memorizzazione-simultanea-idb--filesystem)  
10. [Gestione della collezione di chunks](#10-gestione-della-collezione-di-chunks)  
11. [Pannello Inspect — gestione visuale dei chunks](#11-pannello-inspect--gestione-visuale-dei-chunks)  
12. [IDB Bridge — comunicazione postMessage con il parent](#12-idb-bridge--comunicazione-postmessage-con-il-parent)  
13. [Strutture dati in memoria e in IndexedDB](#13-strutture-dati-in-memoria-e-in-indexeddb)  
14. [Workflow completo — dalla Library all'editor e ritorno](#14-workflow-completo--dalla-library-alleditor-e-ritorno)  
15. [Import di snapshot da disco nella Library](#15-import-di-snapshot-da-disco-nella-library)  
16. [Sistema di naming dei file](#16-sistema-di-naming-dei-file)  
17. [Dipendenze esterne](#17-dipendenze-esterne)  

---

## 1. Panoramica generale

**Noesis Editor** (codename **sn56.x**, talvolta riferito come "Summernote Editor") è l'ambiente di annotazione e studio di Noesis. È un editor WYSIWYG HTML completo, basato su **Summernote-lite 0.9.1**, che opera in una finestra separata (contesto `blob:null`) aperta dinamicamente da `noesis810.html`.

Caratteristiche principali:

- **Zero-server, zero-installazione.** Il codice sorgente dell'editor è interamente contenuto all'interno di `noesis810.html` come stringa JSON dentro un `<script type="application/json" id="sn56Source">`. Viene estratto a runtime e iniettato in un Blob URL.
- **Due modalità operative:** `chapter` (capitolo estratto da un EPUB, con chapterId e contesto bibliografico) e `standalone` (editor vuoto senza contesto, aperto direttamente dalla Library).
- **Raccolta chunks:** sistema di selezione e accumulo di frammenti di testo, immagini e tabelle in una collezione in-memory, esportabile in più formati.
- **Doppio snapshot simultaneo:** ogni salvataggio produce due versioni del documento (clean e annotated) scaricate automaticamente come coppia di file HTML, e salvate contemporaneamente in IndexedDB.
- **IDB Bridge:** poiché il contesto `blob:null` blocca l'accesso diretto a IndexedDB in alcuni browser (Chrome desktop), tutte le operazioni IDB vengono delegate al parent window tramite `postMessage`.

---

## 2. Architettura tecnica e struttura del file

### 2.1 Embedding come JSON data island

L'intero HTML di sn56.x è embedded in `noesis810.html` tra i marker:

```html
<!-- SN56_SOURCE_START -->
<script type="application/json" id="sn56Source">"<!DOCTYPE html>…"</script>
<!-- SN56_SOURCE_END -->
```

Il contenuto è una stringa JSON (con escape di tutti i caratteri speciali: backtick → `\`, `</script>` → `<\/script>`, newline → `\n`). Questo elimina qualsiasi problema di nesting nei template literal.

Un file ausiliario `build.py` automatizza l'aggiornamento della stringa quando sn56.x viene modificato separatamente.

### 2.2 Funzione di lancio: `_openSn56(payload)`

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

**Meccanismo:**

1. Decodifica la stringa JSON per ottenere l'HTML sorgente di sn56.x.
2. Se c'è un payload, lo serializza in un `<script type="application/json" id="noesisPayload">` e lo inserisce nel placeholder `<!-- SN56_PAYLOAD_SLOT -->`.
3. Crea un Blob URL dall'HTML risultante.
4. Apre la finestra con `window.open(url, '_blank', '')` — il terzo argomento esplicito è necessario per preservare `window.opener` su Chrome.
5. Revoca il Blob URL dopo 60 secondi (la finestra è già caricata).

### 2.3 Lettura del payload all'avvio (boot dell'editor)

All'interno di sn56.x, dopo che Summernote è inizializzato (`initEditor()`), viene eseguita la funzione `_bootPayload()`:

```javascript
function _bootPayload() {
  var payloadEl = document.getElementById('noesisPayload');
  if (!payloadEl) return; // standalone: editor vuoto
  var payload = JSON.parse(payloadEl.textContent);
  _mode        = payload.mode        || 'standalone';
  _bookName    = payload.bookName    || '';
  _chapterName = payload.chapterName || '';
  _chapterId   = payload.chapterId   || '';
  if (payload.htmlContent) {
    $('#editor').summernote('code', payload.htmlContent);
  }
  // Aggiorna titolo header
  // In modalità chunks: disabilita snapshot export
  // Toast informativo (una volta per sessione, in chapter mode)
}
```

### 2.4 Caricamento dinamico di jQuery e Summernote

sn56.x non include jQuery e Summernote inline: li carica dinamicamente via CDN in cascata:

```javascript
loadScript('https://code.jquery.com/jquery-3.7.1.min.js', function() {
  loadScript('https://cdn.jsdelivr.net/npm/summernote@0.9.1/dist/summernote-lite.min.js', function() {
    initEditor();
  });
});
```

---

## 3. I tre percorsi di accesso all'editor

### 3.1 Percorso 1 — Library → Open Editor (payload null)

**Trigger:** clic sul pulsante **"Open Editor"** (`#libOpenEditorBtn`, icona `bi-pencil-square`) nella toolbar della Library.

**Codice:**
```javascript
openEditorBtn.addEventListener('click', function() { _openSn56(null); });
```

**Comportamento:**

- `_openSn56` riceve `null` come payload.
- Il placeholder `<!-- SN56_PAYLOAD_SLOT -->` rimane vuoto nell'HTML generato.
- In `_bootPayload()`, `payloadEl` è `null` → la funzione esce immediatamente.
- Le variabili globali mantengono i valori di default: `_mode = 'standalone'`, `_bookName = ''`, `_chapterName = ''`, `_chapterId = ''`.
- L'editor si apre **vuoto** con titolo header `"Noesis Editor"`.
- Il pulsante **Save** (export clean + annotated) è abilitato ma non salverà in IDB (nessun `_chapterId`).
- L'utente può importare manualmente un file HTML dall'Import dialog.

**Caso d'uso:** scrittura libera, note personali, documenti indipendenti dai libri.

---

### 3.2 Percorso 2 — Library → capitolo estratto → snapshot specifico (payload chapter)

**Trigger:** clic su un **nome di capitolo** nella sezione estratta di un libro (apre il più recente snapshot) oppure clic su uno **snapshot specifico** nella lista sotto il capitolo.

**Codice:**
```javascript
// Clic su nome capitolo → snapshot più recente
entry.querySelector('.chapter-name-btn').onclick = () => {
  _openExtractedEnv(ch, null);
};

// Clic su snapshot specifico
btn.onclick = () => _openExtractedEnv(ch, snap.snapshotId);
```

**Funzione intermediaria `_openExtractedEnv`:**
```javascript
function _openExtractedEnv(chapterRecord, snapshotId) {
  // Ordina: isOrigin in fondo, gli altri dal più recente
  const snaps = (chapterRecord.snapshots || []).slice().sort(...);
  const targetSnap = snapshotId
    ? snaps.find(s => s.snapshotId === snapshotId)
    : snaps[0] || null;
  const htmlContent = targetSnap ? targetSnap.content : '<p><em>No snapshots yet.</em></p>';
  _openSn56({
    mode:        'chapter',
    htmlContent: htmlContent,
    bookName:    chapterRecord.bookName    || '',
    chapterName: chapterRecord.chapterName || '',
    chapterId:   chapterRecord.chapterId   || ''
  });
}
```

**Payload trasmesso:**
```json
{
  "mode": "chapter",
  "htmlContent": "<p>Contenuto HTML del capitolo/snapshot...</p>",
  "bookName": "Nome del libro",
  "chapterName": "Nome del capitolo",
  "chapterId": "ch_1234567890_987654"
}
```

**Comportamento nell'editor:**

- Il contenuto HTML viene caricato in Summernote.
- L'header mostra `chapterName` (o `bookName` come fallback).
- `_chapterId` è valorizzato → Save salva in IDB + filesystem.
- L'Import dialog mostrerà la lista degli snapshot IDB filtrata per questo `chapterId`.

**Caso d'uso:** riaprire un capitolo precedentemente annotato per continuare il lavoro, confrontare snapshot, riprendere da un punto specifico.

---

### 3.3 Percorso 3 — Reader → estrazione capitolo (payload chapter immediato)

**Trigger:** clic sul pulsante **"Extract"** (`#extractChapterBtn`) nel Reader, che apre il menu di estrazione (solo capitolo corrente oppure + livelli annidati).

**Codice (estratto dalla funzione di estrazione):**
```javascript
// Crea chapterId univoco
const _chapterId = 'ch_' + Date.now() + '_' + Math.floor(Math.random() * 1e6);

// Salva in IDB con snapshot origin
const _firstSnapshot = {
  snapshotId: 'snap_' + ts + '_' + random,
  createdAt: now.toISOString(),
  description: 'origin-' + timestamp,
  isOrigin: true,
  content: htmlContent
};
const _chapterRecord = {
  chapterId: _chapterId,
  bookName: currentBookTitle,
  chapterName: chapterTitle,
  createdAt: new Date().toISOString(),
  snapshots: [_firstSnapshot]
};
await saveExtractedChapterToDB(_chapterRecord);

// Scarica coppia di file HTML
_autoDownloadHTML(`noesis-extract-${book}__${ch}__${ts}.html`, ...);
setTimeout(() => _autoDownloadHTML(`noesis-origin-${book}__${ch}__${ts}.html`, ...), 1500);

// Apre l'editor
_openSn56({
  mode: 'chapter',
  htmlContent: htmlContent,
  bookName: currentBookTitle,
  chapterName: chapterTitle,
  chapterId: _chapterId
});
```

**Sequenza di azioni simultanee al momento dell'estrazione:**

1. Viene generato un `chapterId` univoco (`ch_` + timestamp + random).
2. Un record `chapterRecord` viene scritto in `noesisDB` con il primo snapshot contrassegnato `isOrigin: true`.
3. Due file HTML vengono scaricati automaticamente nella cartella Download:
   - `noesis-extract-…html` (leggibile offline, senza meta tag noesis)
   - `noesis-origin-…html` (con meta tag noesis, reimportabile in Library) — scaricato con 1,5s di ritardo per evitare conflitti
4. L'editor viene aperto con il contenuto del capitolo e il `chapterId` fresco.

**Caso d'uso:** il flusso primario di Noesis — leggo un EPUB nel Reader, estraggo un capitolo interessante, l'editor si apre immediatamente con il testo pronto per l'annotazione.

---

## 4. Interfaccia utente — layout e componenti

### 4.1 Struttura visiva

```
┌─────────────────────────────────────────────┐
│ HEADER (blu #0a84ff)                        │
│ "Nome capitolo / Noesis Editor"    [?]      │
├─────────────────────────────────────────────┤
│                                             │
│   SUMMERNOTE TOOLBAR (generata da Summ.)    │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│   AREA EDITOR WYSIWYG (.note-editable)      │
│   (altezza dinamica, occupa tutto lo spazio │
│   disponibile tra toolbar e bottom bar)     │
│                                             │
├─────────────────────────────────────────────┤
│ BOTTOM TOOLBAR (nero #111)                  │
│ [CHAPTER section] [COLLECTION section]      │
│                   [TOOLS section]           │
└─────────────────────────────────────────────┘
```

### 4.2 Header

- **Colore:** `#0a84ff` (blu iOS)
- **Titolo (`#appHeaderTitle`):** in modalità chapter mostra `chapterName` o `bookName`; in standalone mostra `"Noesis Editor"`.
- **Pulsante `?` (`#editorHelpBtn`):** apre l'overlay di aiuto contestuale con la descrizione di tutti i pulsanti.

### 4.3 Help overlay

Overlay modale a schermo intero (sfondo scuro, box dark) con sezioni collassate per:
- Chapter (New, Import, Save, More formats)
- Collection (Add, Import JSON, Export JSON, More formats, Inspect, Clear)
- Inspect Panel
- Tools

---

## 5. Bottoniera inferiore — sezione Chapter

La sezione **Chapter** è identificata visivamente da un bordo giallo-arancio e label verticale "CHAPTER" in giallo.

### 5.1 New — `#chNewBtn` (grigio scuro)

**Icona:** `bi-plus-square`

**Comportamento:**
- Se l'editor è vuoto: resetta immediatamente.
- Se l'editor ha contenuto: mostra `confirm("Salvare il documento corrente prima di crearne uno nuovo?")`.
  - Se confermato: invoca programmaticamente `chExportMainBtn.click()` per eseguire il doppio salvataggio.
- Dopo: svuota Summernote, azzera `_bookName`, `_chapterName`, `_chapterId`, `_mode = 'standalone'`, svuota la collezione, aggiorna il titolo header.

---

### 5.2 Import — `#chImportBtn` (arancione `#ff9f0a`)

**Icona:** `bi-folder2-open`

**Comportamento:** apre l'**Import Chapter Dialog** (`#chImportOverlay`).

#### Import Chapter Dialog

Il dialog è un overlay modale con:

**Sezione IDB (se `_chapterId` è valorizzato):**
- Chiama `_idbPost('get', { chapterId: _chapterId })` per recuperare il record IDB.
- Divide gli snapshot in due gruppi tramite `_groupSnapshots()`:
  - **ANNOTATED:** snapshot la cui `description` non inizia con "clean" (include `annot-`, `origin-`, ecc.)
  - **CLEAN:** snapshot la cui `description` inizia con "clean"
- Entrambi i gruppi sono ordinati per data decrescente (più recente in cima).
- Ogni riga mostra: punto colorato (verde se più recente), timestamp formattato `DD/MM/YY HH:MM`, descrizione (con ★ se `isOrigin`).
- Clic su una riga → `_loadFromSnapshot(snap)` carica il contenuto nel editor e aggiorna le variabili di contesto.

**Sezione file da disco:**
- Pulsante "Import from file (any HTML)" in fondo al dialog.
- Apre il file picker (`#chImportFileInput`, accetta `.html,.htm`).
- Il file viene letto come testo; vengono estratti i meta tag `noesis-*` per ricostruire il contesto (bookName, chapterName, chapterId).
- Il meta `noesis-snapshot-variant` determina se applicare la pulizia dei background-color (`clean`) o preservarli (`annotated`).

---

### 5.3 Save — `#chExportMainBtn` (verde `#30d158`)

**Icona:** `bi-file-earmark-arrow-down`

Questo è il pulsante centrale del sistema di memorizzazione. Genera **due file HTML simultanei** e **due record snapshot in IDB**. Descritto in dettaglio nella sezione 8 e 9.

---

### 5.4 More formats — `#chMoreBtn` (rosso `#ff453a`)

**Icona:** `bi-three-dots`

Apre un dropdown menu con esportazioni alternative del documento completo:

| Voce | Funzione | Formato | Mime |
|------|----------|---------|------|
| Export TXT | `exportTXT()` | `.txt` | `text/plain` |
| Export Markdown | `exportMD()` | `.md` | `text/markdown` |
| Export MD + images ZIP | `exportMDZip()` | `.zip` | — |
| Export JSON doc | `exportDocJSON()` | `.json` | `application/json` |
| Print / PDF | `exportPDF()` | browser print | — |
| Export DOCX | `exportDOCX()` | `.docx` | — |

**Naming:** tutti usano `_promptCustom(tipo, ext)` che mostra un prompt con la parte automatica `noesis-{tipo}-book__chapter__TS` e permette di aggiungere un'etichetta custom.

**Dettagli implementativi:**

- `exportTXT()`: estrae il testo da tutti i tag `p, h1-h6, li` con newline tra i paragrafi.
- `exportMD()`: usa la libreria **TurndownService** per convertire l'HTML in Markdown.
- `exportMDZip()`: converte in Markdown, estrae le immagini base64 in `images/img_001.png` ecc., crea uno ZIP con JSZip.
- `exportDocJSON()`: wrappa l'HTML grezzo in `{ "html": "…" }` come JSON.
- `exportPDF()`: copia il contenuto in `#print-container` (visibile solo in print), applica normalizzazioni CSS su tabelle/immagini, lancia `window.print()`.
- `exportDOCX()`: usa la libreria **html-docx-js** (`window.htmlDocx.asBlob()`).

---

## 6. Bottoniera inferiore — sezione Collection

La sezione **Collection** è identificata da un bordo azzurro-ciano e label verticale "COLLECTION" in azzurro.

### 6.1 Add `[+ N]` — `#addChunkBtn`

**Colore:** definito inline (sfondo con bordo)  
**Etichetta:** `+` con badge numerico `#chunkCounter` (rosso, posizionato in alto a destra del pulsante)

Aggiunge alla collezione il contenuto attualmente selezionato. Supporta tre modalità di selezione:

**Caso 1 — Immagine:**
- L'immagine deve essere stata preventivamente "tracciata" tramite un `mousedown` (desktop) o `touchstart` (Android) sull'`<img>` nell'area `.note-editable`. Il riferimento è tenuto in `_selectedImg`.
- Al clic di `[+]`: usa `_selectedImg.outerHTML`.

**Caso 2 — Tabella:**
- Analogamente, il `mousedown` su `TD`, `TH`, `TABLE`, `TR` o qualsiasi elemento dentro `table` imposta `_selectedTable`.
- Al clic di `[+]`: usa `_selectedTable.parentElement.outerHTML` se il wrapper non è l'editor stesso, altrimenti `_selectedTable.outerHTML`.

**Caso 3 — Selezione testo:**
- Usa `window.getSelection()` con `getRangeAt(0).cloneContents()` per estrarre l'HTML della selezione.

**Shortcut gestuali (Android):**
- **Doppio tap su immagine:** aggiunge direttamente senza passare da `[+]`.
- **Long press su immagine (600ms):** aggiunge direttamente.

**Funzione `_enrichChunk(chunk)`:**
- Determina il tipo: `'table'` se `/<table[\s>]/i`, `'image'` se `/<img[\s>]/i`, altrimenti `'text'`.
- Aggiunge `bookName`, `chapterName`, `timestamp`.

**Funzione `_saveChunk(chunk)`:**
- Assegna un `id` univoco: `Date.now() + '_' + random`.
- Aggiunge al array `_collection`.

---

### 6.2 Import JSON — pulsante blu `#0a84ff`

**Icona:** `bi-upload`

Apre il file picker `#collectionImportInput` (accetta `.json`).

Il file JSON può essere:
- Un array diretto di chunks: `[{...}, {...}]`
- Un oggetto con campo `chunks`: `{ "version": 1, "chunks": [...] }`

I chunks importati vengono **aggiunti** alla collezione esistente (non sostituiti). Ogni chunk riceve un nuovo `id` univoco.

---

### 6.3 Export JSON — pulsante verde `#32d74b`

**Icona:** `bi-download`

Chiama `_exportCollectionJson()`. Produce:

```json
{
  "version": 1,
  "exportedAt": "2026-03-27T10:00:00.000Z",
  "bookName": "…",
  "chapterName": "…",
  "chunks": [
    {
      "id": "1711530000000_123456789",
      "content": "<p>Testo selezionato</p>",
      "type": "text",
      "bookName": "…",
      "chapterName": "…",
      "timestamp": 1711530000000
    }
  ]
}
```

---

### 6.4 More formats collection — `#colMoreBtn` (arancione `#ff9f0a`)

**Icona:** `bi-three-dots`

Dropdown con tre opzioni:

| Voce | Funzione | Formato | Note |
|------|----------|---------|------|
| Export Markdown | `_exportCollectionMd()` | `.md` | Immagini omesse, tabelle come HTML raw |
| Export MD + images ZIP | `_exportCollectionMdZip()` | `.zip` | Immagini base64 estratte in `images/` |
| Export HTML collection | `_exportCollectionHtml()` | `.html` | Pagina HTML standalone con tutti i chunk |

**`_exportCollectionHtml()`** produce una pagina HTML autonoma con tutti i chunk come `<div class="chunk">`, con stile CSS inline per leggibilità.

---

### 6.5 Inspect — pulsante viola `#5e5ce6`

**Icona:** `bi-eye`

Apre il pannello `#inspectPanel` (float non modale). Descritto in dettaglio nella sezione 11.

---

### 6.6 Clear — pulsante rosso `#ff453a`

**Icona:** `bi-trash`

- Se la collezione è vuota: mostra toast "Collection already empty".
- Se non vuota: `confirm("Clear the collection? (N chunks)")` → `_clearCollection()` → aggiorna contatore.

---

## 7. Bottoniera Summernote (toolbar WYSIWYG)

La toolbar di Summernote-lite è posizionata sopra l'area di editing. È generata automaticamente da Summernote secondo la configurazione passata in `initEditor()`.

### 7.1 Configurazione gruppi toolbar

```javascript
toolbar: [
  ['style',    ['style']],             // Stile paragrafo: p, h1-h6, blockquote, pre
  ['font',     ['bold', 'italic', 'underline', 'strikethrough',
                'superscript', 'subscript', 'clear']],
  ['fontname', ['fontname']],          // Famiglia font
  ['fontsize', ['fontsize']],          // Dimensione font
  ['color',    ['color']],             // Colore testo e sfondo
  ['para',     ['ul', 'ol', 'paragraph']], // Liste e allineamento
  ['height',   ['height']],            // Interlinea
  ['table',    ['table']],             // Inserimento e modifica tabelle
  ['insert',   ['link', 'picture', 'video', 'hr']],
  ['view',     ['fullscreen', 'codeview', 'help']]
]
```

### 7.2 Stili paragrafo disponibili

`['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre']`

### 7.3 Font disponibili

`Arial, Arial Black, Comic Sans MS, Courier New, Georgia, Times New Roman, Verdana, system-ui`

### 7.4 Altezza dinamica dell'editor

La funzione `_calcEditorHeight()` calcola l'altezza disponibile per `.note-editable` sottraendo dall'altezza della finestra:
- Altezza header app
- Altezza toolbar Summernote
- Altezza statusbar Summernote  
- Altezza bottom toolbar
- Padding container (16px)

Il ricalcolo avviene automaticamente al `resize` e al cambio di orientamento.

### 7.5 Upload immagini inline

Il callback `onImageUpload` di Summernote converte ogni file caricato in base64 via `FileReader` e lo inserisce direttamente nell'HTML come `<img src="data:image/...;base64,...">`. Le immagini sono quindi completamente embedded nel documento.

---

## 8. Doppia memorizzazione degli snapshot: clean e annotated

Ogni volta che l'utente preme il pulsante **Save** (`#chExportMainBtn`), vengono prodotti **simultaneamente** due snapshot distinti.

### 8.1 Il prompt e la costruzione dei nomi file

Prima di qualsiasi export viene mostrato un **unico prompt** che mostra la base automatica del nome file:

```
noesis-clean-TitoloLibro__NomeCapitolo__20260327_142530  →  aggiungi etichetta (invio per saltare):
```

Il risultato dell'etichetta (può essere vuoto) viene usato per entrambi i file.

### 8.2 Schema di naming

```
noesis-{tipo}-{bookSlug}__{chapterSlug}__{YYYYMMDD_HHMMSS}[_{etichetta}].html
```

Esempi:
```
noesis-clean-Ulysses__Proteus__20260327_142530.html
noesis-annot-Ulysses__Proteus__20260327_142530.html
noesis-clean-Ulysses__Proteus__20260327_142530_primaLettura.html
noesis-annot-Ulysses__Proteus__20260327_142530_primaLettura.html
```

### 8.3 Differenza clean vs annotated

**Clean (`noesis-clean-`):**
- Il contenuto del documento viene processato con due regex che rimuovono tutti gli stili `background-color` inline:
  ```javascript
  .replace(/background-color\s*:[^;'"]+[;]/gi, '')
  .replace(/background-color\s*:[^"']+(?=["'])/gi, '')
  ```
- Risultato: testo privo di evidenziazioni colorate, adatto alla lettura e alla reimportazione "pulita".
- Contiene il meta tag `<meta name="noesis-snapshot-variant" content="clean">`.

**Annotated (`noesis-annot-`):**
- Il contenuto viene usato esattamente com'è, inclusi tutti i colori di evidenziazione, grassetti, corsivi e qualsiasi stile applicato durante l'annotazione.
- Contiene il meta tag `<meta name="noesis-snapshot-variant" content="annot">`.

### 8.4 Struttura HTML comune (sharedHead)

Entrambi i file condividono lo stesso `<head>`:
```html
<!DOCTYPE html>
<html lang="it"><head>
<meta charset="UTF-8">
<meta name="noesis-chapter-id"    content="{_chapterId}">
<meta name="noesis-book-name"     content="{_bookName}">
<meta name="noesis-chapter-name"  content="{_chapterName}">
<title>{chapterName || bookName || 'Chapter'}</title>
<style>
body{max-width:750px;margin:auto;padding:20px;font-family:system-ui;line-height:1.6;}
img,figure{max-width:100%;height:auto;}
table{width:100%;table-layout:fixed;border-collapse:collapse;}
td,th{border:1px solid #ccc;padding:6px;word-break:break-word;}
</style>
```

I meta tag `noesis-*` sono fondamentali: permettono la **reimportazione dei file nella Library** tramite il sistema "Import Snapshots" (sezione 15).

### 8.5 I due snapshot in IDB

In parallelo al download dei file, vengono creati e salvati in IDB due oggetti snapshot:

```javascript
var _snapAnnot = {
  snapshotId: 'snap_' + ts + '_' + random1,
  createdAt: now,
  bookName: _bookName,
  chapterName: _chapterName,
  description: 'annot-' + tsStr + descSuffix,  // es: 'annot-20260327-142530-primaLettura'
  content: docContent   // HTML annotato as-is
};
var _snapClean = {
  snapshotId: 'snap_' + (ts+1) + '_' + random2,
  createdAt: now,
  bookName: _bookName,
  chapterName: _chapterName,
  description: 'clean-' + tsStr + descSuffix,  // es: 'clean-20260327-142530-primaLettura'
  content: cleanContent  // HTML con background rimossi
};
```

L'ordine di inserimento nell'array `record.snapshots`:
```javascript
record.snapshots.unshift(_snapClean);   // inserito secondo
record.snapshots.unshift(_snapAnnot);   // inserito primo → appare in cima
```

**Il snapshot annotated è sempre più in cima del clean** perché è il più "ricco" e tipicamente quello che si vuole riaprire per continuare ad annotare.

---

## 9. Memorizzazione simultanea IDB + filesystem

### 9.1 Il doppio output del pulsante Save

Ogni pressione del pulsante Save produce **quattro output simultanei**:

| # | Destinazione | File/Oggetto | Tipo | Descrizione |
|---|---|---|---|---|
| 1 | Filesystem (Download) | `noesis-clean-…html` | HTML | Versione senza background-color |
| 2 | Filesystem (Download) | `noesis-annot-…html` | HTML | Versione annotata as-is |
| 3 | IndexedDB (`noesisDB`) | snapshot `annot-…` | JSON in IDB | Stesso contenuto del file annot |
| 4 | IndexedDB (`noesisDB`) | snapshot `clean-…` | JSON in IDB | Stesso contenuto del file clean |

Gli output 1 e 2 avvengono tramite `download(filename, '﻿' + html, 'text/html;charset=utf-8')` (BOM UTF-8 preposto).  
Gli output 3 e 4 avvengono tramite `_idbPost('put', { record: record })`.

### 9.2 Perché la doppia memorizzazione?

- **IDB** permette la navigazione rapida nella Library senza doversi ricordare dove si trovano i file su disco. Gli snapshot sono immediatamente accessibili dall'interfaccia Library.
- **Filesystem** è la copia di backup persistente e portabile. Se l'IDB viene cancellato (pulizia del browser, cambio device, migrazione), i file su disco permettono la **reimportazione** tramite il meccanismo "Import Snapshots".
- I due sistemi si completano: IDB per la fluidità di workflow, filesystem per la resilienza e la portabilità.

### 9.3 Gestione del caso `!_chapterId`

Se l'editor è in modalità `standalone` (nessun `_chapterId`), il blocco IDB viene saltato:
```javascript
if (_chapterId) {
  // ... logica IDB
}
```
Il save produce solo i file su filesystem, senza salvare in IDB. L'utente vede il toast `"⚠️ Saved to disk only — Library not updated"` se il save IDB fallisce per altri motivi.

### 9.4 Gestione errori IDB

In caso di fallimento del save IDB (timeout postMessage, opener non disponibile, errore IndexedDB), viene mostrato il toast `"⚠️ Saved to disk only — Library not updated"`. I file su disco vengono comunque scaricati (il download avviene prima della chiamata IDB).

---

## 10. Gestione della collezione di chunks

### 10.1 Struttura dati in memoria

La collezione è tenuta in un array JavaScript globale `_collection`:

```javascript
var _collection = []; // Array di chunk objects

// Struttura di un chunk:
{
  id:          "1711530000000_123456789",  // univoco, generato al momento del salvataggio
  content:     "<p>HTML del chunk</p>",    // HTML grezzo
  type:        "text" | "image" | "table", // auto-rilevato
  bookName:    "Nome del libro",
  chapterName: "Nome del capitolo",
  timestamp:   1711530000000,             // Date.now()
  label:       "Etichetta opzionale"      // non usata nell'UI corrente
}
```

La collezione è **in-memory only**: non viene persistita in IDB né in localStorage tra sessioni. Viene resettata ad ogni apertura di sn56.x. La persistenza è delegata all'export JSON.

### 10.2 Ciclo di vita di un chunk

```
Selezione nell'editor
       ↓
Clic [+] / doppio tap immagine / long press
       ↓
_enrichChunk() — aggiunge type, bookName, chapterName, timestamp
       ↓
_saveChunk()   — assegna id, push in _collection
       ↓
_updateCounter() — aggiorna badge numerico
       ↓
[Opzionale] _openInspect() per visualizzare/gestire
       ↓
[Export] JSON / MD / HTML
       ↓
[Opzionale] Inject in editor / Delete
```

### 10.3 Aggiunta alla collezione — tutti i metodi

**Metodo 1: pulsante `[+]`**
- Testo: via `window.getSelection()`.
- Immagine: via `_selectedImg` (tracciato da mousedown/touchstart).
- Tabella: via `_selectedTable` (tracciato da mousedown su elementi tabella).

**Metodo 2: doppio clic su immagine**
- Gestito da `dblclick` su `.note-editable`.
- Funziona su desktop e su Android Chrome.

**Metodo 3: long press su immagine (600ms)**
- Timer avviato su `touchstart`, cancellato su `touchend`/`touchmove`.
- Pensato per Android dove il doppio tap può essere interpretato diversamente.

### 10.4 Export della collezione — tutti i formati

| Formato | Funzione | Nome file | Note |
|---|---|---|---|
| JSON | `_exportCollectionJson()` | `noesis-collection-…json` | Struttura completa con metadati |
| Markdown | `_exportCollectionMd()` | `noesis-colmd-…md` | Immagini omesse, tabelle come HTML |
| MD + ZIP | `_exportCollectionMdZip()` | `noesis-colzip-…zip` | Immagini estratte in `images/` |
| HTML standalone | `_exportCollectionHtml()` | `noesis-colhtml-…html` | Pagina pronta per il browser |

---

## 11. Pannello Inspect — gestione visuale dei chunks

### 11.1 Caratteristiche del pannello

Il pannello `#inspectPanel` è un elemento **fixed non modale** (non blocca l'editor sottostante):
- Posizionato al centro schermo alla prima apertura.
- **Draggable** tramite l'header (`#inspectHeader`, cursor grab).
- **Resizable** tramite handle nell'angolo basso-destra (`#inspectResizeHandle`, icona ⊞).
- Dimensioni iniziali: `min(90vw, 720px)` × `85vh`, minimo `260px` × `200px`.
- Supporta sia mouse che touch per drag e resize (gestione unificata con `e.touches[0]`).

### 11.2 Struttura visiva

```
┌─────────────────────────────────────────────┐ ← drag header
│ 🔵 Collection — N chunks            [✕]    │
├─────────────────────────────────────────────┤
│ Chunk #1 — Text · NomeLibro › NomeCapitolo  │
│ [☐] [preview testo]           [↓] [⛶] [✕] │
│ Chunk #2 — Image                            │
│ [☐] [preview immagine]        [↓] [⛶] [✕] │
│ Chunk #3 — Table                            │
│ [☐] [preview tabella]         [↓] [⛶] [✕] │
├─────────────────────────────────────────────┤
│ N selected  [All] [None]  [→ Inject in Ed.] │ ← footer
└──────────────────────────────────────────── ⊞ ← resize handle
```

### 11.3 Azioni per ogni chunk

Ogni chunk ha tre pulsanti nella colonna destra (`chunk-actions`):

| Pulsante | Classe CSS | Colore | Azione |
|---|---|---|---|
| ↓ (Inserisci qui) | `chunk-insert-here` | verde `#30d158` | Inject al cursore salvato |
| ⛶ (Fullscreen) | `chunk-fs` | giallo `#ffd60a` | Apre overlay fullscreen |
| ✕ (Delete) | `chunk-del` | giallo `#ffd60a` | Rimuove dalla collezione |

### 11.4 Inject al cursore

Il pulsante "↓" (`chunk-insert-here`) usa un sistema di salvataggio/ripristino del cursore:

1. All'apertura del pannello Inspect: `$('#editor').summernote('saveRange')` salva la posizione del cursore.
2. Al clic di "↓" per un chunk specifico:
   - `$('#editor').summernote('restoreRange')` ripristina il cursore.
   - Crea un `<div>` temporaneo con `innerHTML = chunk.content`.
   - Itera sui `childNodes` in ordine inverso e li inserisce con `insertNode`.
   - `$('#editor').summernote('saveRange')` aggiorna il cursore alla nuova posizione.

Il pulsante "Inject into Editor" nel footer inserisce **tutti i chunks selezionati** in sequenza.

### 11.5 Chunk fullscreen

L'overlay `#chunkFsOverlay` apre il contenuto di un singolo chunk in fullscreen (sfondo nero, contenuto bianco con scroll). Chiudibile con il pulsante ✕ o clic fuori dall'overlay.

### 11.6 Selezione multipla e inject di gruppo

- Checkbox per ogni chunk (accent-color `#0a84ff`).
- Pulsanti **All** / **None** per selezione rapida.
- Il footer mostra "N selected".
- "Inject into Editor" è disabilitato finché almeno un chunk non è selezionato.
- L'inject di gruppo concatena i contenuti con `\n` e li assegna tramite `summernote('code', current + html)`.

---

## 12. IDB Bridge — comunicazione postMessage con il parent

### 12.1 Il problema

Il contesto `blob:null` (finestre aperte con Blob URL) in Chrome desktop ha restrizioni su IndexedDB che causano un `SecurityError`. È quindi impossibile accedere direttamente a `noesisDB` dall'editor.

### 12.2 Architettura del bridge

**Lato sn56.x (child)** — `_idbPost(op, payload)`:
```javascript
function _idbPost(op, payload) {
  return new Promise(function(resolve, reject) {
    var target = window.opener || window.parent;
    if (!target || target === window) { reject(new Error('No opener/parent')); return; }
    var id = ++_idbCallbackId;
    _idbCallbacks[id] = { resolve, reject };
    target.postMessage({ __noesisIDB: true, id: id, op: op, payload: payload }, '*');
    setTimeout(function() {
      if (_idbCallbacks[id]) { delete _idbCallbacks[id]; reject(new Error('IDB timeout')); }
    }, 8000);
  });
}
```

**Lato noesis810.html (parent)** — handler `message`:
```javascript
window.addEventListener('message', function(e) {
  var d = e.data;
  if (!d || !d.__noesisIDB) return;
  var { id, op, payload } = d;
  function reply(result, error) {
    try { e.source.postMessage({ __noesisIDBResponse: true, id, result: result || null, error: error || null }, '*'); }
    catch(err) {}
  }
  if (op === 'get') {
    getExtractedChapterFromDB(payload.chapterId).then(r => reply(r)).catch(err => reply(null, err.message));
  } else if (op === 'put') {
    saveExtractedChapterToDB(payload.record).then(r => reply(r)).catch(err => reply(null, err.message));
  } else {
    reply(null, 'Unknown op: ' + op);
  }
});
```

### 12.3 Operazioni supportate

| Operazione | Payload | Descrizione |
|---|---|---|
| `get` | `{ chapterId: "ch_…" }` | Recupera un chapterRecord da noesisDB |
| `put` | `{ record: {...} }` | Salva/aggiorna un chapterRecord in noesisDB |

### 12.4 Timeout e gestione errori

Il bridge ha un timeout di **8 secondi**. Se entro 8s non arriva risposta, la Promise viene rifiettata con `Error('IDB timeout')`. In tal caso l'editor mostra il toast di warning e il save va solo su filesystem.

---

## 13. Strutture dati in memoria e in IndexedDB

### 13.1 Database `noesisDB` (IndexedDB)

- **Nome:** `noesisDB`
- **Versione:** 1
- **Object store:** `extractedChapters`
  - **keyPath:** `chapterId`
  - **Indici:** `bookName` (non unique), `chapterName` (non unique)

### 13.2 `chapterRecord` (la struttura in IDB)

```javascript
{
  chapterId:   "ch_1711530000000_987654",   // chiave primaria, generata all'estrazione
  bookName:    "Ulysses",
  chapterName: "Proteus",
  createdAt:   "2026-03-27T14:25:30.000Z",  // ISO 8601

  snapshots: [
    // Snapshot più recente per primo (eccetto isOrigin che è in fondo)
    {
      snapshotId:  "snap_1711530000001_111222",
      createdAt:   "2026-03-27T15:00:00.000Z",
      bookName:    "Ulysses",          // ridondante ma utile
      chapterName: "Proteus",
      description: "annot-20260327-150000-primaLettura",
      isOrigin:    false,              // assente o false per snapshot normali
      content:     "<p>HTML…</p>"
    },
    {
      snapshotId:  "snap_1711530000002_333444",
      description: "clean-20260327-150000-primaLettura",
      isOrigin:    false,
      content:     "<p>HTML senza background…</p>"
    },
    {
      snapshotId:  "snap_1711530000000_000001",
      description: "origin-20260327_142530",
      isOrigin:    true,               // snapshot automatico all'estrazione
      content:     "<p>HTML originale non modificato…</p>"
    }
  ]
}
```

### 13.3 Ordine di visualizzazione degli snapshot nella Library

L'ordinamento applicato in `_openExtractedEnv` e nella Library è:
1. Snapshot con `isOrigin: false` prima (più recenti in cima per data).
2. Snapshot con `isOrigin: true` in fondo (snapshot originale all'estrazione).

Nella Library, l'ultimo snapshot in ordine (primo nell'array dopo l'ordinamento) è contrassegnato con la classe CSS `latest` e un punto verde.

### 13.4 Database `EpubLibraryDB` (IndexedDB)

- **Nome:** `EpubLibraryDB`
- **Versione:** 1
- **Object store:** `books`
  - **keyPath:** `id` (timestamp string)
  - Nessun indice

**Struttura record libro:**
```javascript
{
  id:       "1711530000000",         // Date.now().toString()
  title:    "Ulysses",
  author:   "James Joyce",
  data:     ArrayBuffer,             // file EPUB grezzo
  cover:    "data:image/jpeg;base64,…",  // copertina in base64
  addedAt:  1711530000000
}
```

### 13.5 Variabili globali sn56.x

```javascript
var _collection  = [];         // Array chunks in memoria
var _bookName    = '';         // Nome libro corrente
var _chapterName = '';         // Nome capitolo corrente
var _chapterId   = '';         // ID univoco del capitolo in IDB
var _mode        = 'standalone'; // 'chapter' | 'standalone'
var _toastShown  = false;      // guard per toast one-time

var _selectedImg   = null;     // Ultima immagine tracciata da mousedown
var _selectedTable = null;     // Ultima tabella tracciata da mousedown

var _inspectSelected = {};     // { chunkId: boolean } selezioni nel panel
var _savedRange = null;        // Range Summernote salvato prima di Inspect

var _idbCallbacks  = {};       // Callback pending per IDB bridge
var _idbCallbackId = 0;        // Counter per ID messaggi IDB bridge
```

---

## 14. Workflow completo — dalla Library all'editor e ritorno

### 14.1 Workflow tipico di studio (percorso Reader)

```
1. Library: clic sulla copertina del libro
      ↓
2. Reader: lettura del testo con epub.js
      ↓
3. Reader: clic "Extract" → scelta tipo estrazione
      ↓
4. Automaticamente (in parallelo):
   a) noesisDB: scritto chapterRecord con snapshot "origin-..."
   b) Download: noesis-extract-…html (leggibile offline)
   c) Download: noesis-origin-…html (con meta tag, 1.5s ritardo)
   d) nuova tab: sn56.x aperto con payload chapter
      ↓
5. Editor: lavoro di annotazione (WYSIWYG Summernote)
   - Highlight testo con colori
   - Aggiunte note, commenti
   - Raccolta chunks nella collezione
      ↓
6. Editor: clic Save
   a) Prompt etichetta opzionale
   b) Download: noesis-clean-…html
   c) Download: noesis-annot-…html
   d) IDB bridge: salva snapshots clean + annot in noesisDB
      ↓
7. Library (dopo reload): il capitolo mostra N snapshots
   - snap "annot-…" (il più recente, punto verde)
   - snap "clean-…"
   - snap "origin-…" (in fondo, origine della sessione)
      ↓
8. Ritorno al lavoro: clic su snap nella Library
   → _openExtractedEnv() → _openSn56() con payload del snap
```

### 14.2 Workflow standalone

```
1. Library: clic "Open Editor"
      ↓
2. sn56.x si apre vuoto (mode: standalone)
      ↓
3. Import dialog: importa file HTML da disco
   - Se file ha meta tag noesis-*: contesto ricostruito automaticamente
   - Altrimenti: prompt per bookName e chapterName
      ↓
4. Lavoro nell'editor
      ↓
5. Save: produce clean + annot
   - Se _chapterId è stato estratto dai meta tag: anche IDB
   - Altrimenti: solo filesystem
```

---

## 15. Import di snapshot da disco nella Library

Il sistema **Import Snapshots** (`#importSnapshotsBtn` nella Library) permette di reimportare file HTML salvati su disco in `noesisDB`, ricostruendo la struttura della Library.

### 15.1 File accettati

Il filtro regex sui nomi file è:
```
/^noesis-(clean|annot|origin)-.*\.html?$/i
```

Sono quindi accettati: `noesis-clean-…html`, `noesis-annot-…html`, `noesis-origin-…html`.

### 15.2 Metodo di selezione file

- **Desktop Chrome/Edge** (con `window.showDirectoryPicker`): apre un **folder picker** che scansiona tutti i file della cartella.
- **Android / Safari** (senza `showDirectoryPicker`): apre il file picker standard (`#importSnapshotsInput`, `multiple`).

### 15.3 Logica di processing (`_processSnapshotFiles`)

Per ogni file:

1. **Parsing HTML:** usa `DOMParser` per estrarre meta tag `noesis-chapter-id`, `noesis-book-name`, `noesis-chapter-name`, `noesis-snapshot-variant`.
2. **Estrazione timestamp dal nome file:** regex `noesis-{tipo}-{book}__{ch}__{YYYYMMDD_HHMMSS}[_{custom}].html`.
3. **Costruzione snapshot object** con `snapshotId` nuovo (non riusa quello originale, per evitare conflitti).
4. **Match su chapterRecord esistente:**
   - Prima per `chapterId` (match esatto).
   - Fallback: match case-insensitive su `bookName + chapterName`.
5. **Se record trovato:** aggiunge snapshot (se non già presente per description). Origin va in fondo, altri in cima.
6. **Se record non trovato:** crea nuovo `chapterRecord` con il file come primo snapshot.
7. **Deduplicazione:** non importa snapshot con `description` identica a uno già presente.

### 15.4 Lo snapshot "origin"

Il file `noesis-origin-…html` è lo snapshot automatico generato al momento dell'estrazione. È contrassegnato con `isOrigin: true` nell'IDB. È sempre posizionato in fondo alla lista e serve come punto di partenza immutabile del testo originale (prima di qualsiasi annotazione).

---

## 16. Sistema di naming dei file

### 16.1 Funzioni di costruzione nome

**`_buildTimestamp()`:**
```
YYYYMMDD_HHMMSS  (es: 20260327_142530)
```

**`_buildFileBase(tipo, custom)`:**
```
noesis-{tipo}-{bookSlug}__{chapterSlug}__{timestamp}[_{custom}]
```
- `bookSlug`: max 40 caratteri, solo `[a-zA-Z0-9_]`
- `chapterSlug`: max 40 caratteri, solo `[a-zA-Z0-9_]`
- `custom`: opzionale, solo `[a-zA-Z0-9_\-]`

### 16.2 Tipi di file per categoria

| Tipo | Suffisso | Contesto |
|------|---------|---------|
| `clean` | `.html` | Chapter export — versione senza background |
| `annot` | `.html` | Chapter export — versione annotata |
| `extract` | `.html` | Estrazione automatica dal Reader (no meta) |
| `origin` | `.html` | Estrazione automatica dal Reader (con meta) |
| `text` | `.txt` | Chapter export TXT |
| `markdown` | `.md` | Chapter export Markdown |
| `mdzip` | `.zip` | Chapter export MD + immagini |
| `jsondoc` | `.json` | Chapter export JSON |
| `docx` | `.docx` | Chapter export DOCX |
| `collection` | `.json` | Collection export JSON |
| `colmd` | `.md` | Collection export Markdown |
| `colzip` | `.zip` | Collection export MD + immagini |
| `colhtml` | `.html` | Collection export HTML |

---

## 17. Dipendenze esterne

### 17.1 Incluse via CDN (caricate dinamicamente all'avvio di sn56.x)

| Libreria | Versione | URL | Uso |
|---|---|---|---|
| jQuery | 3.7.1 | `code.jquery.com` | Base per Summernote |
| Summernote-lite | 0.9.1 | `cdn.jsdelivr.net/npm/summernote@0.9.1` | Editor WYSIWYG |
| Bootstrap Icons | 1.11.3 | `cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3` | Icone UI (condivisa con noesis810) |
| TurndownService | latest | `cdn.jsdelivr.net/npm/turndown` | HTML→Markdown |
| JSZip | latest | `cdn.jsdelivr.net/npm/jszip@latest` | Generazione ZIP |
| html-docx-js | latest | `cdn.jsdelivr.net/npm/html-docx-js` | Esportazione DOCX |

### 17.2 Incluse in noesis810.html (usate anche dal Reader)

| Libreria | Versione | Uso |
|---|---|---|
| JSZip | 3.10.1 | Già presente nel parent |
| epub.js | 0.3.93 | Reader EPUB |
| Bootstrap Icons | 1.11.3 | Icone Library e Reader |

### 17.3 Strumento opzionale integrato (Tools section)

| Strumento | URL | Descrizione |
|---|---|---|
| Noesis Excalidraw | `noesis-excalidraw.vercel.app` | Fork di Excalidraw per diagrammi e mappe mentali |

---

*Fine documentazione — noesis-editor-sn56-documentation.md*
