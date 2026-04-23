# NOESIS812 — Documento 8: Sistema di Embedding della Versione Full

> Fonte: `noesis812-full.html` (7256 righe, 1.704 MB) — Aggiornato: 2026-04-22
> Versione di riferimento: `noesis812.html` Regular (7233 righe, ~332 KB)
> Documento precedente: `DOC8_FULL_EMBEDDING.md` (basato su noesis810)

---

## SCOPO DEL DOCUMENTO

Descrive la struttura di `noesis812-full.html`, variante di distribuzione completamente offline di Noesis 812, e le tre tecniche con cui tutte le dipendenze CDN vengono incorporate nel file HTML senza modificare il codice applicativo.

---

## DIFFERENZE TRA LE DUE VARIANTI

| Caratteristica | Regular (`noesis812.html`) | Full (`noesis812-full.html`) |
|----------------|----------------------------|------------------------------|
| Dimensione HTML | ~332 KB | ~1.704 MB |
| Righe | 7233 | 7256 |
| Dipendenze esterne | 3 CDN nel main + 7 CDN nel blob sn56Source | Zero — tutto inline |
| Funzionamento offline | Parziale (dopo cache) | Totale |
| Codice applicativo | — | Identico alla versione Regular |

---

## STRUTTURA DEL FILE FULL — MAPPA PER RIGHE

```
noesis812-full.html
│
├── [righe 1–7]     Doctype, <html>, <head>, meta tag
│                   IDENTICI alla versione Regular
│
├── [righe 8–14]    <style> BLOCCO 1 — Bootstrap Icons CSS + font embedded
│                   └── @font-face con src: url("data:font/woff2;base64,...")
│                       (font .woff2 codificato Base64 inline)
│                   └── Classi .bi-* (mapping Unicode code point → glifo)
│                   Peso: ~259 KB
│                   Regular equivalente:
│                   <link href="cdn.jsdelivr.net/...bootstrap-icons...">
│
├── [righe 15–2640] <style> BLOCCO 2 — CSS applicativo principale
│                   IDENTICO alla versione Regular
│                   Contiene le nuove regole v812:
│                   - .reader-menubar, .rmb-item, .rmb-navigate-menu (menubar reader)
│                   - .lib-header-btn, .lib-themes-dropdown (library header)
│                   - #reader-print-container, @media print (stampa multi-pagina)
│                   - #displaySavePrompt (prompt salvataggio impostazioni display)
│
├── [righe 2641–3240] <body> — HTML strutturale
│                   IDENTICO alla versione Regular
│                   Contiene le nuove strutture v812:
│                   - nav.reader-menubar (8 voci testo con dropdown Navigate)
│                   - #displaySavePrompt (banner floating)
│                   - Library header con dropdown temi (.lib-themes-menu)
│
├── [riga 3241]     <!-- SN56_SOURCE_START --> (commento marcatore)
│
├── [riga 3242]     <script type="application/json" id="sn56Source">
│                   └── Stringa JSON dell'editor popup completo
│                       con TUTTE le sue dipendenze incorporate come data URI
│                   Peso: ~912 KB
│                   (vedi sezione TECNICA 3 per dettaglio)
│
├── [riga 3243]     <!-- SN56_SOURCE_END --> (commento marcatore)
│
├── [righe 3245–3263] <script> — JSZip v3.10.1 sorgente minificato inline
│                   Regular equivalente:
│                   <script src="cdn.jsdelivr.net/npm/jszip@3.10.1/...">
│                   Peso: ~97 KB
│
├── [righe 3264–3265] <script> — epub.js (ePub.js) v0.3.93 sorgente minificato inline
│                   Regular equivalente:
│                   <script src="cdn.jsdelivr.net/npm/epubjs@0.3.93/...">
│                   Peso: ~224 KB
│
└── [righe 3266–7256] <script> — Codice applicativo Noesis
                    IDENTICO alla versione Regular
```

---

## TECNICA 1 — Font webfont come data URI nel CSS

### Problema
Bootstrap Icons richiede un file `.woff2` che il browser scarica da CDN al momento del parsing del CSS.

### Soluzione nella versione Full
Il file `.woff2` viene convertito in Base64 e incorporato direttamente nella dichiarazione `@font-face`:

```css
/* Regular — richiede rete */
@font-face {
  font-family: "bootstrap-icons";
  src: url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2")
       format("woff2");
}

/* Full — zero richieste HTTP */
@font-face {
  font-family: "bootstrap-icons";
  src: url("data:font/woff2;base64,d09GMgABAAAAAf1cAA...")
       format("woff2");
}
```

### Proprietà tecniche
- Il MIME type corretto nel data URI è `font/woff2` (non `application/font-woff2`)
- Il browser decodifica il Base64 in memoria al parsing CSS, senza I/O di rete
- La stringa Base64 di un font woff2 tipico è ~1.37× il peso binario del file originale
- Il CSS delle classi `.bi-*` segue immediatamente nello stesso `<style>` block

---

## TECNICA 2 — Librerie JS copiate inline nei tag `<script>`

### Problema
JSZip ed epub.js vengono caricati con `<script src="...">` che richiede connessione al CDN.

### Soluzione nella versione Full
Il contenuto minificato di ciascuna libreria viene incollato integralmente in un `<script>` senza attributo `src`:

```html
<!-- Regular -->
<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/epubjs@0.3.93/dist/epub.min.js"></script>

<!-- Full -->
<script>
/*!
 * JSZip v3.10.1
 * ...licenza...
 */
!function(e,t){ ... }(window,(function(){ ... }));
</script>

<script>
!function(t,e){"object"==typeof exports&&"object"==typeof module
?module.exports=e(require("JSZip")):"function"==typeof define&&define.amd
?define(["JSZip"],e):t.ePub=e(t.JSZip)}(window,(function(t){ ... }));
</script>
```

### Ordine obbligatorio
JSZip **deve precedere** epub.js: la versione UMD di epub.js usa `require("JSZip")` e si aspetta che `window.JSZip` sia già definito nello scope globale.

### Invariante rispetto alla versione Regular
Il codice applicativo Noesis che segue usa `ePub` e `JSZip` come globali in entrambe le versioni: il meccanismo di caricamento (CDN vs inline) è trasparente per il codice applicativo.

---

## TECNICA 3 — sn56Source blob con dipendenze incorporate

### Struttura del blob sn56Source

Il tag `<script type="application/json" id="sn56Source">` contiene l'intera applicazione editor popup serializzata come stringa JSON. Il tipo `application/json` impedisce al browser di eseguire il contenuto: è dati puri.

```html
<script type="application/json" id="sn56Source">
"<!DOCTYPE html>\n<html lang=\"it\">\n<head>..."
</script>
```

Il contenuto è una stringa JSON (con escape standard: `\"`, `\n`, `\\`) che, una volta de-serializzata con `JSON.parse()`, produce un documento HTML completo e autonomo.

### Come viene usato (invariante in entrambe le versioni)

```javascript
// Da _openSn56() — identico in Regular e Full
const src = JSON.parse(document.getElementById('sn56Source').textContent);
const island = payload
  ? `<script type="application/json" id="noesisPayload">${JSON.stringify(payload)}<\/script>`
  : '';
const html = src.replace('<!-- SN56_PAYLOAD_SLOT -->', island);
const blob = new Blob([html], {type: 'text/html'});
const url  = URL.createObjectURL(blob);
window.open(url, '_blank', '');
setTimeout(() => URL.revokeObjectURL(url), 60000);
```

### Dipendenze nell'editor — Regular vs Full

Nella versione Regular, il documento HTML dell'editor (dentro il blob sn56Source) referenzia CDN:

```html
<link href="https://cdn.jsdelivr.net/npm/summernote@0.9.1/dist/summernote-lite.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jszip@latest/dist/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/turndown/dist/turndown.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/html-docx-js/dist/html-docx.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/summernote@0.9.1/dist/summernote-lite.min.js"></script>
```

Nella versione Full, tutte e sette le dipendenze sono incorporate nel documento HTML usando le stesse Tecniche 1 e 2 descritte sopra, e l'intero documento risultante viene poi serializzato come stringa JSON nell'attributo `sn56Source`.

Il blob sn56Source è il blocco più pesante del file: **~912 KB** non compressi.

---

## MAPPA COMPLETA DELLE DIPENDENZE INCORPORATE

| Libreria | Versione | Tecnica | Contesto | Peso approx. |
|----------|----------|---------|----------|--------------|
| Bootstrap Icons CSS + font woff2 | 1.11.3 | CSS inline + data:font/woff2;base64 | App principale | ~259 KB |
| JSZip | 3.10.1 | `<script>` inline | App principale | ~97 KB |
| epub.js | 0.3.93 | `<script>` inline | App principale | ~224 KB |
| jQuery | 3.7.1 | `<script>` inline (nel blob sn56Source) | Editor popup | ~90 KB |
| Summernote CSS + font | 0.9.1 | CSS inline + data:font/woff2;base64 (nel blob sn56Source) | Editor popup | ~150 KB |
| Bootstrap Icons CSS + font woff2 | 1.11.3 | CSS inline + data:font/woff2;base64 (nel blob sn56Source) | Editor popup | ~259 KB |
| Summernote JS | 0.9.1 | `<script>` inline (nel blob sn56Source) | Editor popup | ~120 KB |
| Turndown JS | latest | `<script>` inline (nel blob sn56Source) | Editor popup | ~25 KB |
| JSZip | latest | `<script>` inline (nel blob sn56Source) | Editor popup | ~97 KB |
| html-docx-js | latest | `<script>` inline (nel blob sn56Source) | Editor popup | ~40 KB |

**Nota duplicati**: Bootstrap Icons e JSZip compaiono due volte; jQuery compare solo nell'editor popup. Il documento blob aperto con `window.open` ha uno scope JavaScript separato e non eredita i globali del parent.

---

## DIFFERENZE DI INTERFACCIA 812 vs 810 — IMPATTO SUL FULL EMBEDDING

Le modifiche di interfaccia introdotte in v0.11.x e v0.12.0 non introducono nuove dipendenze esterne. Il processo di full embedding rimane identico (4 sostituzioni, stessi blocchi). Le differenze sono documentate qui per completezza.

### Library Header ridisegnato (nessun impatto)

In 810, l'header della libreria usava variabili CSS di tema e pulsanti con bordo:

```html
<!-- 810: pulsanti con stile per-ID e bordo -->
<button id="libThemeToggle">...</button>
<label id="importLabel">Add Book</label>
<button id="importSnapshotsBtn">Import Snapshots</button>
<button id="libOpenEditorBtn">Open Editor</button>
<button id="saveStateBtn">Save</button>  <!-- rimosso in 812 -->
```

In 812, l'header ha sfondo gradiente fisso e usa la classe `.lib-header-btn` unificata:

```html
<!-- 812: classe unificata flat, sfondo gradiente viola fisso -->
<button id="libAddBooksBtn"         class="lib-header-btn">Add Books</button>
<button id="libImportSnapshotsBtn"  class="lib-header-btn">Import Snapshots</button>
<button id="libEditorBtn"           class="lib-header-btn">Open Editor</button>
<button id="libThemesBtn"           class="lib-header-btn">Themes ▾</button>
<button id="libToolsBtn"            class="lib-header-btn">Tools ▾</button>
<button id="libHelpBtn"             class="lib-header-btn">?</button>
```

Pulsante `#saveStateBtn` rimosso: sostituito dall'auto-save e dal prompt `#displaySavePrompt`.

**Impatto sul full embedding:** nessuno. Sono modifiche HTML/CSS senza nuove dipendenze esterne.

### Reader Menubar (nessun impatto)

In 812 è presente una nuova barra dei menu `nav.reader-menubar` con 8 voci testuali (Library, TOC, Bookmarks, Display, Navigate, Annotate, Extract, Help). La toolbar a icone precedente (`.toolbar`) è nascosta come compatibilità interna.

Il bottone **Navigate** mostra un badge inline con la modalità attiva (`[Page]`/`[Scroll]`) e apre un dropdown con le due opzioni, evidenziando quella corrente in grassetto blu.

**Impatto sul full embedding:** nessuno. Tutto implementato con HTML/CSS/JS vanilla.

### Stampa multi-pagina (nessun impatto)

In 812 è stato corretto il bug per cui la stampa catturava solo la prima pagina del capitolo. Il fix usa eventi `beforeprint`/`afterprint` del browser standard e un `<div id="reader-print-container">` mostrato solo in `@media print`.

**Impatto sul full embedding:** nessuno.

### Auto-save dinamico della posizione (nessun impatto)

In 812 (introdotto in 811) la posizione di lettura viene salvata automaticamente ogni 3 secondi tramite `setInterval` e IndexedDB nativo. Il prompt `#displaySavePrompt` appare quando si chiude il pannello Display dopo aver modificato impostazioni visive.

**Impatto sul full embedding:** nessuno.

---

## DIPENDENZE NON INCORPORABILI

Le seguenti funzionalità restano dipendenti dalla rete per definizione, in entrambe le versioni:

| Funzionalità | Motivo |
|---|---|
| Traduzione browser | Usa servizi del browser (Google Translate, DeepL) — non è codice Noesis |
| Link esterni nei contenuti EPUB | Sono URL nei testi dell'utente, non dipendenze applicative |

---

## INVARIANTI DI CODICE

Le righe 3266–7256 del file Full sono **bit-identiche** alle corrispondenti della versione Regular. Non esiste alcun flag, variabile o condizione che distingua i due percorsi di esecuzione a runtime.

---

## DIMENSIONI E COMPRESSIONE

| Metrica | Regular (812) | Full (812) |
|---------|---------------|------------|
| HTML non compresso | ~332 KB | ~1.704 MB |
| Righe | 7233 | 7256 |
| Rapporto di compressione atteso | ~80% | ~65% |

---

## PROCESSO DI AGGIORNAMENTO DELLE DIPENDENZE

Per aggiornare una dipendenza nella versione Full è necessario un intervento manuale:

1. Scaricare il nuovo `.min.js` o `.min.css` dalla sorgente ufficiale
2. Per file con font: convertire i `.woff2` in Base64 (`base64 -w0 file.woff2`) e sostituire le stringhe `data:font/woff2;base64,...` nel CSS
3. Sostituire il corpo del `<script>` o `<style>` corrispondente nel file HTML
4. Per dipendenze dell'editor: aggiornare le occorrenze nel blob `sn56Source`, rispettando l'escaping JSON (ogni `"` → `\"`, ogni `\n` reale → `\\n`, ogni `<\/script>` per evitare chiusura anticipata del tag)
5. Riverificare che l'ordine JSZip → epub.js sia mantenuto nei blocchi inline

### Alternativa: ricostruzione da script Python

È possibile ricostruire `noesis812-full.html` da `noesis810-full.html` (per i blocchi embedded) e da `noesis812.html` (per il codice applicativo), usando il seguente processo:

```python
# Estrai da 810-full: Bootstrap Icons block, sn56Source block, JSZip block, epub.js block
# Sostituisci in 812: CDN link, sn56Source CDN, JSZip CDN, epub.js CDN
```

I blocchi Bootstrap Icons, sn56Source, JSZip, epub.js sono **identici** tra 810-full e 812-full: il sorgente sn56 non è cambiato tra le due versioni.

---

## VERIFICA INTEGRITÀ

```bash
# Verificare zero CDN reference
grep -c "cdn.jsdelivr.net\|code.jquery.com" noesis812-full.html
# → deve restituire 0

# Contare righe e dimensione
wc -l noesis812-full.html
wc -c noesis812-full.html
```

---

## FILE CORRELATI

| File | Descrizione |
|------|-------------|
| `noesis812.html` | Versione Regular — sorgente di riferimento per il codice applicativo |
| `noesis812-full.html` | Versione Full — oggetto di questo documento |
| `noesis810-full.html` | Versione Full precedente — fonte dei blocchi embedded riutilizzati in 812-full |
| `DOC8_FULL_EMBEDDING.md` | Documento equivalente per noesis810 |
