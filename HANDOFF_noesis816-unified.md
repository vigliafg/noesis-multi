# Noesis816 Unified — Handoff Document

**Data:** 2026-07-21  
**Stato:** Lavoro interrotto — test end-to-end parzialmente completato, 1 bug fixato, 1 bug ancora da verificare nel browser

---

## 1. OBIETTIVO

Ricostruire la versione **unificata** `noesis816-full.html` che include Reader + Editor in un unico file, come nella versione 812. Il file deve essere generato unendo `noesis816-full-reader.html` (base) + `noesis816-full-editor.html` (embedding JSON).

---

## 2. FILE COINVOLTI

| File | Ruolo |
|------|-------|
| `noesis816-full.html` | **File unificato** (~1.79 MB, 7764 righe) — è il target del lavoro |
| `noesis816-full-reader.html` | Reader standalone — base HTML |
| `noesis816-full-editor.html` | Editor standalone — viene JSON-encodato e embeddato come `sn56Source` |
| `doc-workflow.html` | Documentazione architettura unificata (già aggiornata) |
| `AGENT.md` | Documentazione agente (da aggiornare) |
| `noesis-map.md` | Mappa del progetto (da aggiornare) |
| `CHANGELOG.md` | Changelog (da aggiornare) |
| `Goldman-Cecil Medicine 27ed 2024 Slim.epub` | EPUB di test (~60 MB) |

---

## 3. ARCHITETTURA DELLA VERSIONE UNIFICATA

```
noesis816-full.html
├── Library View (reader)
│   ├── libAddBooksBtn → ADD BOOKS
│   ├── libEditorBtn  → EDITOR (apre editor vuoto)
│   └── Grid dei libri caricati
├── Reader View (reader)
│   ├── Toolbar: Annotate, Extract, Display, Navigate
│   ├── Extract dropdown:
│   │   ├── "Current chapter only" (download)
│   │   ├── "Current + all sublevels" (download)
│   │   └── "Open in Editor" → extractOpenEditor ✨
│   ├── Hamburger menu: ... Editor (hmb-rdr)
│   └── epub.js reader (iframe)
├── Embedded Editor (sn56Source JSON + _openSn56)
│   ├── <script type="application/json" id="sn56Source">...</script>
│   ├── _openSn56(payload) → window.open + document.write
│   ├── Boot script: legge #noesisPayload e carica in Summernote
│   └── IDB bridge: postMessage per IndexedDB dalla finestra editor
└── Shared
    ├── NOESIS_DB_NAME = 'noesisDB'
    ├── NOESIS_DB_VERSION = 1
    ├── NOESIS_STORE = 'extractedChapters'
    └── extractCurrentChapter() → {title, chapterId, html, css: allStyles}
```

---

## 4. COMPONENTI CHIAVE E LORO POSIZIONE NEL FILE

### 4.1 sn56Source (riga 7756-7758)
```html
<!-- SN56_SOURCE_START -->
<script type="application/json" id="sn56Source">"<!DOCTYPE html>\n<html ..."</script>
<!-- SN56_SOURCE_END -->
```
Contiene l'intero `noesis816-full-editor.html` come stringa JSON. Il placeholder `<!-- SN56_PAYLOAD_SLOT -->` (2 occorrenze) viene sostituito a runtime con il payload del capitolo.

### 4.2 _openSn56 (riga ~3789)
```javascript
function _openSn56(payload) {
  var srcEl = document.getElementById('sn56Source');
  if (!srcEl) { alert('Editor source not found.'); return; }
  try {
    // Apre finestra vuota IN MODO SINCRONO per evitare popup blocker
    var w = window.open('', '_blank');
    if (!w) { alert('Popup blocked...'); return; }
    var sourceHtml = JSON.parse(srcEl.textContent);
    if (payload) {
      // Inietta <script id="noesisPayload"> + boot script
      ...
    }
    w.document.write(sourceHtml);
    w.document.close();
  } catch(e) { ... }
}
```

### 4.3 extractCurrentChapter (riga ~4996)
- Funzione `async`, restituisce `{title, chapterId, html, css: allStyles}`
- ⚠️ **BUG FIXATO:** `cssContent` → `allStyles` (la variabile `cssContent` non era definita)
- Il valore di ritorno (`_result`) viene usato da `extractOpenEditor` per passare i dati all'editor

### 4.4 extractOpenEditor (riga ~6796)
- Gestore click: chiama `extractCurrentChapter()` e poi `_openSn56()`
- ⚠️ **BUG FIXATO:** L'elemento HTML `id="extractOpenEditor"` non esisteva nel DOM (solo il JS c'era)
- Aggiunto `<div class="extract-menu-item" id="extractOpenEditor" data-mode="editor">` nel menu Extract

### 4.5 libEditorBtn
- Pulsante EDITOR nella header della libreria
- Apre l'editor vuoto (senza payload capitolo) chiamando `_openSn56()`

### 4.6 IDB Bridge (riga ~3820)
```javascript
window.addEventListener('message', function(e) {
  if (!e.data || !e.data.__noesisIDB) return;
  // get/put/delete su IndexedDB via postMessage
});
```
Permette alla finestra editor di accedere a IndexedDB del reader.

---

## 5. BUG FIXATI OGGI

| # | Bug | Fix | Stato |
|---|-----|-----|-------|
| 1 | `ReferenceError: cssContent is not defined` in `extractCurrentChapter` | `cssContent` → `allStyles` (riga 5250) | ✅ Fixato |
| 2 | `extractOpenEditor` elemento HTML mancante nel DOM | Aggiunto `<div class="extract-menu-item" id="extractOpenEditor" data-mode="editor">` | ✅ Fixato |
| 3 | IDB bridge usava `'NoesisDB'` hardcoded invece di `NOESIS_DB_NAME` | Usa le costanti `NOESIS_DB_NAME`/`NOESIS_DB_VERSION`/`NOESIS_STORE` | ✅ Fixato in sessione precedente |

---

## 6. COSA FUNZIONA (VERIFICATO NEL BROWSER)

✅ `noesis816-full.html` viene servito correttamente da `http://localhost:8765`  
✅ La libreria si carica senza errori JavaScript fatali  
✅ `document.getElementById('sn56Source')` esiste  
✅ `typeof _openSn56 === 'function'`  
✅ `typeof extractCurrentChapter === 'function'`  
✅ `document.getElementById('libEditorBtn')` esiste  
✅ `_openSn56({title:'Test', ...})` apre una nuova finestra "Noesis Editor" con successo  
✅ EPUB caricato e aperto nel reader  
✅ TOC navigazione funzionante  

---

## 7. COSA RESTA DA VERIFICARE / COMPLETARE

### 7.1 Test end-to-end completo (PRIORITÀ MASSIMA)
**Comando per avviare il server:**
```bash
cd /home/vigliafg/Documenti/GitHub/noesis-multi
python3 -m http.server 8765
```

**Procedura di test manuale:**
1. Apri `http://localhost:8765/noesis816-full.html` in Chrome
2. Controlla Console (F12) per errori
3. Clicca **ADD BOOKS** → carica `Goldman-Cecil Medicine 27ed 2024 Slim.epub`
4. Aspetta che appaia nella libreria (10-15 secondi)
5. Clicca sul libro per aprire il reader
6. Apri il TOC e naviga a un capitolo (es. PREFACE)
7. Clicca sul dropdown **Extract** nella toolbar
8. Verifica che appaia la voce **"Open in Editor"** (con icona matita)
9. Clicca **"Open in Editor"**
10. Verifica che:
    - Si apra una NUOVA FINESTRA con l'editor
    - L'editor contenga il testo del capitolo
    - Non ci siano errori in console

### 7.2 Test del pulsante EDITOR nella libreria
- Cliccare **EDITOR** (vicino a ADD BOOKS) deve aprire una finestra editor vuota

### 7.3 Test hamburger menu → Editor
- In reader view, aprire hamburger menu → verificare presenza voce "Editor"

### 7.4 Verifica IDB bridge
- Dall'editor aperto, verificare che possa leggere/scrivere IndexedDB

### 7.5 Verifica errori console
Errori noti e accettabili:
- `Blocked script execution in 'about:srcdoc'` — dall'iframe epub.js, non critico
- `TypeError: Cannot read properties of undefined (reading 'packaging')` — epub.js, non critico
- `Error loading stylesheet: ../../../style/css/common.css` — dall'EPUB, non critico

Errori da controllare:
- Qualsiasi `ReferenceError` o `SyntaxError`
- Errori in `_openSn56` o `extractCurrentChapter`

---

## 8. COMANDI UTILI

```bash
# Avviare server HTTP
python3 -m http.server 8765 &

# Verificare marker nel file
grep -n "extractOpenEditor\|_openSn56\|sn56Source\|hmbEditor" noesis816-full.html

# Contare riferimenti
grep -c "SN56_PAYLOAD_SLOT" noesis816-full.html

# Verificare che il fix cssContent sia presente
grep "css: allStyles" noesis816-full.html

# Commit e push
git add noesis816-full.html [altri file]
git commit -m "fix: ..."
git push
```

---

## 9. DOCUMENTAZIONE DA AGGIORNARE (DOPO IL TEST)

| Documento | Cosa aggiornare |
|-----------|----------------|
| `AGENT.md` | Aggiungere riferimenti a noesis816-full.html (unificato) |
| `noesis-map.md` | Mappare la nuova architettura unificata |
| `CHANGELOG.md` | Registrare la creazione della versione unificata |
| `index.html` | Verificare che la homepage linki noesis816-full.html |

---

## 10. PROCESSO DI RIGENERAZIONE (SE NECESSARIO)

Se serve rigenerare `noesis816-full.html` da zero (es. dopo modifiche a reader o editor):

```python
# Pseudocodice del merge
reader = read('noesis816-full-reader.html')
editor = read('noesis816-full-editor.html')

# Aggiungi placeholder payload all'editor
editor = editor.replace('<body>', '<body>\n<!-- SN56_PAYLOAD_SLOT -->', 1)

# JSON-encode e escape </ 
editor_json = json.dumps(editor).replace('</', '<\\/')

# Inserisci sn56Source prima di </body>
sn56_block = f'<script type="application/json" id="sn56Source">{editor_json}</script>'
reader = reader.replace('</body>', sn56_block + '\n</body>', 1)

# Aggiungi _openSn56, libEditorBtn, extractOpenEditor, IDB bridge, hmbEditor
# ... (vedi merge script completo in _create_cdn_v6.py per riferimento)

write('noesis816-full.html', reader)
```

---

## 11. PUNTI DI ATTENZIONE

1. **Popup blocker:** `_openSn56` chiama `window.open('', '_blank')` in modo sincrono. Funziona in Chrome se chiamato entro ~1s dal click utente. `extractCurrentChapter()` è async e può richiedere tempo → possibile race condition.

2. **Payload loader nell'editor:** Il boot script iniettato cerca `.note-editing-area .note-editable`, `[contenteditable=true]`, o `#summernote`. Se Summernote ha un selettore diverso, il contenuto non verrà caricato.

3. **Dimensione file:** 1.79 MB — attenzione ai limiti di upload/hosting.

4. **I due handler sul menu item:** `extractOpenEditor` ha sia `addEventListener('click')` dedicato che `onclick` generico (perché ha classe `.extract-menu-item`). Il generico ignora `data-mode="editor"` (no-op) quindi non ci sono conflitti.

---

**Fine documento.** Per riprendere il lavoro: avviare il server HTTP, aprire `noesis816-full.html` nel browser, eseguire il test end-to-end descritto nella sezione 7.1.
