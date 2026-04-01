# NOESIS810 — Documento 8: Sistema di Embedding della Versione Full

> Fonte: `noesis810-full.html` (6520 righe, 1.7 MB) — Aggiornato: 2026-03-30
> Versione di riferimento: `noesis810.html` Regular (6498 righe, 313 KB)

---

## SCOPO DEL DOCUMENTO

Descrive la struttura di `noesis810-full.html`, variante di distribuzione completamente offline di Noesis, e le tre tecniche con cui tutte le dipendenze CDN vengono incorporate nel file HTML senza modificare il codice applicativo.

---

## DIFFERENZE TRA LE DUE VARIANTI

| Caratteristica | Regular (`noesis810.html`) | Full (`noesis810-full.html`) |
|----------------|----------------------------|------------------------------|
| Dimensione HTML | 313 KB | 1.700 KB |
| ZIP scaricabile | 64 KB | 591 KB |
| Righe | 6498 | 6520 |
| Dipendenze esterne | 3 CDN nel main + 6 CDN nel blob sn56Source | Zero — tutto inline |
| Funzionamento offline | Parziale (dopo cache) | Totale |
| Codice applicativo | — | Identico alla versione Regular |

---

## STRUTTURA DEL FILE FULL — MAPPA PER RIGHE

```
noesis810-full.html
│
├── [righe 1–7]     Doctype, <html>, <head>, meta tag
│                   IDENTICI alla versione Regular
│
├── [righe 8–14]    <style> BLOCCO 1 — Bootstrap Icons CSS + font embedded
│                   └── @font-face con src: url("data:font/woff2;base64,...")
│                       (font .woff2 codificato Base64 inline)
│                   └── Classi .bi-* (mapping Unicode code point → glifo)
│                   Peso: ~260 KB
│                   Regular equivalente: <link href="cdn.jsdelivr.net/...bootstrap-icons...">
│
├── [righe 15–2359] <style> BLOCCO 2 — CSS applicativo principale
│                   IDENTICO alla versione Regular
│                   Peso: ~59 KB
│
├── [righe 2360–2928] <body> — HTML strutturale
│                   IDENTICO alla versione Regular
│
├── [riga 2929]     <!-- SN56_SOURCE_START --> (commento marcatore)
│
├── [riga 2930]     <script type="application/json" id="sn56Source">
│                   └── Stringa JSON dell'editor popup completo
│                       con TUTTE le sue dipendenze incorporate come data URI
│                   Peso: ~916 KB
│                   (vedi sezione TECNICA 3 per dettaglio)
│
├── [riga 2931]     <!-- SN56_SOURCE_END --> (commento marcatore)
│
├── [righe 2933–2947] <script> — JSZip v3.10.1 sorgente minificato inline
│                   Regular equivalente:
│                   <script src="cdn.jsdelivr.net/npm/jszip@3.10.1/...">
│                   Peso: ~98 KB
│
├── [righe 2948–2951] <script> — epub.js (ePub.js) v0.3.93 sorgente minificato inline
│                   Regular equivalente:
│                   <script src="cdn.jsdelivr.net/npm/epubjs@0.3.93/...">
│                   Peso: ~224 KB
│
└── [righe 2952–6520] <script> — Codice applicativo Noesis
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
Il codice applicativo Noesis che segue (righe 2952+) usa `ePub` e `JSZip` come globali in entrambe le versioni: il meccanismo di caricamento (CDN vs inline) è trasparente per il codice applicativo.

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
// → src è la stringa HTML dell'editor

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
<script src="https://cdn.jsdelivr.net/npm/jszip@latest/dist/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/turndown/dist/turndown.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/html-docx-js/dist/html-docx.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/summernote@0.9.1/dist/summernote-lite.min.js"></script>
```

Nella versione Full, tutte e sei le dipendenze sono incorporate nel documento HTML usando le stesse Tecniche 1 e 2 descritte sopra (font come data URI, JS come inline script), e l'intero documento risultante — già con le dipendenze embedded — viene poi serializzato come stringa JSON nell'attributo `sn56Source`.

Il blob sn56Source è il blocco più pesante del file: **~916 KB** non compressi, che diventano ~580 KB nello zip.

---

## MAPPA COMPLETA DELLE DIPENDENZE INCORPORATE

| Libreria | Versione | Tecnica | Contesto | Peso approx. |
|----------|----------|---------|----------|--------------|
| Bootstrap Icons CSS + font woff2 | 1.11.3 | CSS inline + data:font/woff2;base64 | App principale | ~260 KB |
| JSZip | 3.10.1 | `<script>` inline | App principale | ~98 KB |
| epub.js | 0.3.93 | `<script>` inline | App principale | ~224 KB |
| Summernote CSS + font | 0.9.1 | CSS inline + data:font/woff2;base64 (nel blob sn56Source) | Editor popup | ~150 KB |
| Bootstrap Icons CSS + font woff2 | 1.11.3 | CSS inline + data:font/woff2;base64 (nel blob sn56Source) | Editor popup | ~260 KB |
| Summernote JS | 0.9.1 | `<script>` inline (nel blob sn56Source) | Editor popup | ~120 KB |
| Turndown JS | latest | `<script>` inline (nel blob sn56Source) | Editor popup | ~25 KB |
| JSZip | latest | `<script>` inline (nel blob sn56Source) | Editor popup | ~98 KB |
| html-docx-js | latest | `<script>` inline (nel blob sn56Source) | Editor popup | ~40 KB |

**Nota duplicati**: Bootstrap Icons e JSZip compaiono due volte perché il contesto dell'editor popup (documento blob aperto con `window.open`) ha uno scope JavaScript separato e non eredita i globali del parent.

---

## DIPENDENZE NON INCORPORABILI

Le seguenti funzionalità restano dipendenti dalla rete per definizione, in entrambe le versioni:

| Funzionalità | Motivo |
|---|---|
| Traduzione browser | Usa servizi del browser (Google Translate, DeepL) — non è codice Noesis |
| Link esterni nei contenuti EPUB | Sono URL nei testi dell'utente, non dipendenze applicative |

---

## INVARIANTI DI CODICE

Le righe 2952–6520 del file Full sono **bit-identiche** alle corrispondenti della versione Regular. Non esiste alcun flag, variabile o condizione che distingua i due percorsi di esecuzione a runtime. L'unica differenza è cosa è già presente nel DOM/scope globale quando il codice applicativo viene eseguito:

- In Regular: `JSZip` e `ePub` arrivano dal CDN (già parsati prima che il main script parta, per via dell'ordinamento dei tag `<script>`)
- In Full: `JSZip` e `ePub` arrivano dai blocchi inline immediatamente precedenti, con lo stesso effetto

---

## DIMENSIONI E COMPRESSIONE

| Metrica | Regular | Full |
|---------|---------|------|
| HTML non compresso | 313 KB | 1.700 KB |
| ZIP (deflate) | 64 KB | 591 KB |
| Rapporto di compressione | ~80% | ~65% |

Il file Full si comprime bene nonostante le dimensioni perché:
- Il Base64 ha un alfabeto di 64 caratteri → alta ripetitività → deflate efficiente
- I sorgenti JS minificati hanno keyword ripetute comprimibili

---

## PROCESSO DI AGGIORNAMENTO DELLE DIPENDENZE

Per aggiornare una dipendenza nella versione Full è necessario un intervento manuale:

1. Scaricare il nuovo `.min.js` o `.min.css` dalla sorgente ufficiale
2. Per file con font: convertire i `.woff2` in Base64 (`base64 -w0 file.woff2`) e sostituire le stringhe `data:font/woff2;base64,...` nel CSS
3. Sostituire il corpo del `<script>` o `<style>` corrispondente nel file HTML
4. Per dipendenze dell'editor: aggiornare le occorrenze nel blob `sn56Source`, rispettando l'escaping JSON (ogni `"` → `\"`, ogni `\n` reale → `\\n`, ogni `<\/script>` per evitare chiusura anticipata del tag)
5. Riverificare che l'ordine JSZip → epub.js sia mantenuto nei blocchi inline

---

## FILE CORRELATI

| File | Descrizione |
|------|-------------|
| `noesis810.html` | Versione Regular — sorgente di riferimento per il codice applicativo |
| `noesis810-full.html` | Versione Full — oggetto di questo documento |
| `noesis810-full.zip` | Distribuzione compressa della versione Full |
| `noesis-full-Deps.zip` | Sorgenti originali delle librerie incorporate (per verifica e ricostruzione) |
