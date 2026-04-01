# NOESIS810 — Documento 7: Pattern di Estensione

> Come aggiungere nuove funzionalità rispettando l'architettura esistente
> Aggiornato: 2026-03-27

---

## PATTERN A — Aggiungere un Pulsante alla Toolbar del Reader

Questo è il caso più comune. Richiede modifiche in 4 punti.

### Step 1 — HTML: inserire il pulsante nella `.toolbar`

Aprire `noesis810.html` e trovare la sezione `.toolbar` dentro `<header>` (riga ~2536). Inserire il pulsante nel punto logico della barra. Le `.toolbar-spacer` separano i gruppi visivi.

```html
<!-- Esempio: nuovo pulsante "Note" dopo il pulsante bookmark -->
<button class="btn btn-icon" id="notesBtn" title="Notes"
  data-tip="Open notes panel">
  <i class="bi bi-journal-text"></i>
</button>
```

**Classi disponibili per il pulsante:**

| Classe aggiuntiva | Effetto visivo |
|-------------------|----------------|
| (nessuna) | Sfondo trasparente / bianco semi-trasparente |
| `.btn-primary` | Blu |
| `.btn-warning` | Arancio/ambra |
| `.btn-success` | Verde |
| `.btn-help` | Stile speciale "?" |

**Attributo `data-tip`:** mostra un tooltip al hover (implementato via CSS `::after` già presente).

### Step 2 — JS: registrare il listener

Nel blocco `DOMContentLoaded` (riga ~5496), aggiungere:

```javascript
document.getElementById('notesBtn').addEventListener('click', () => {
  // logica del pulsante
  toggleNotesPanel();
});
```

### Step 3 — JS: gestire `_closeAllReaderMenus()`

Se il pulsante apre un popup/panel, aggiungere la chiusura in `_closeAllReaderMenus()` (riga ~6354):

```javascript
function _closeAllReaderMenus() {
  // ... chiusure esistenti ...

  // Aggiungere:
  const notesPanel = document.getElementById('notesPanel');
  if (notesPanel) notesPanel.classList.add('hidden');
}
```

Questo garantisce che il panel si chiuda quando l'utente clicca altrove.

### Step 4 — Persistenza: aggiungere a `savedState` (se ha stato)

Se il pulsante ha uno stato da salvare (es: aperto/chiuso, un valore), aggiungerlo in `saveBookState()` (riga ~3789) e in `loadAndApplyBookState()` (riga ~3879):

```javascript
// In saveBookState(), dentro stateToSave:
const stateToSave = {
  // ... campi esistenti ...
  notesPanelVisible: notesPanelVisible,  // AGGIUNTO
};

// In loadAndApplyBookState(), dopo aver letto s:
notesPanelVisible = (s.notesPanelVisible !== undefined) ? !!s.notesPanelVisible : false;
```

---

## PATTERN B — Aggiungere un Tema di Lettura

I temi sono definiti in due oggetti: `THEME_COLORS` e `THEME_GROUPS` (riga ~4759).

### Step 1 — Aggiungere la definizione colori

```javascript
// In THEME_COLORS (riga ~4759):
const THEME_COLORS = {
  // ... temi esistenti ...

  // Nuovo tema:
  lavender: {
    background: '#f0ebff',
    color:      '#1a1030',
    a:          '#5b21b6'
  },
};
```

### Step 2 — Aggiungere al gruppo UI

```javascript
// In THEME_GROUPS (riga ~4784):
const THEME_GROUPS = [
  // ... gruppi esistenti ...

  // Aggiungere al gruppo esistente o crearne uno nuovo:
  { label: "Pastels", keys: ["lavender"] },
];
```

### Step 3 — Nessun altro cambiamento necessario

`buildThemePopup()` legge `THEME_GROUPS` e genera automaticamente gli swatches. `applyTheme()` usa `THEME_COLORS[currentTheme]` direttamente. Il nuovo tema sarà disponibile nel popup e salvato in `savedState.theme`.

---

## PATTERN C — Aggiungere una Sezione al Display Menu (Accordion)

Il `#displayMenu` è un accordion con sezioni header/body. Per aggiungere una nuova sezione:

### Step 1 — HTML: aggiungere header e body

Dentro `#displayMenu` (riga ~2586), dopo l'ultima `.display-sep`:

```html
<div class="display-sep"></div>
<!-- Nuova sezione -->
<div class="display-section-header" id="displaySecNotes">
  <i class="bi bi-journal-text" style="font-size:13px;"></i>
  Notes
  <i class="bi bi-chevron-right display-section-chevron"></i>
</div>
<div class="display-section-body" id="displayBodyNotes"></div>
```

### Step 2 — JS: spostare il contenuto dentro il body

Il body della sezione è inizialmente vuoto. Spostare un popup o creare contenuto direttamente:

```javascript
// Opzione A: spostare un popup esistente (stessa tecnica dei popup tipografia)
const notesPopup = document.getElementById('notesPopup');
document.getElementById('displayBodyNotes').appendChild(notesPopup);

// Opzione B: creare contenuto inline
document.getElementById('displayBodyNotes').innerHTML = `
  <div style="padding: 8px 12px;">
    <!-- contenuto HTML -->
  </div>
`;
```

### Step 3 — JS: registrare il click sull'header

Trovare il codice che gestisce i click sugli header del display menu (riga ~5860 circa, sezione gestione `displayBtn`). Aggiungere handler per il nuovo header seguendo lo stesso pattern degli altri.

---

## PATTERN D — Aggiungere un Campo alla Biblioteca per ogni Libro

Se si vuole mostrare un dato aggiuntivo per ogni libro nella griglia.

### Step 1 — Aggiungere il campo al record IDB

In `saveBookToDB()` (riga ~3071), aggiungere il campo al record:

```javascript
const record = {
  id: ...,
  title: ...,
  // AGGIUNTO:
  rating: 0,  // default
};
```

### Step 2 — Aggiungere alla struttura HTML generata

In `loadLibraryBooks()` (riga ~3314), dentro il template HTML di ogni riga libro, aggiungere il rendering del nuovo campo:

```javascript
// Dentro la generazione HTML del libro:
const ratingHtml = `<div class="book-rating">${'★'.repeat(book.rating || 0)}</div>`;
// Inserirlo nel template della riga
```

### Step 3 — Aggiungere CSS per il nuovo elemento

Nel blocco CSS biblioteca (prima di riga 555), aggiungere stile che rispetti le custom properties:

```css
.book-rating {
  font-size: 12px;
  color: var(--lib-stats);
  margin-top: 2px;
}
```

---

## PATTERN E — Aggiungere un Elemento al Drawer Segnalibri

Per aggiungere pulsanti o sezioni extra nel drawer `#userBookmarksDrawer`.

### Step 1 — HTML: aggiungere dentro `#ubmHeader` o dopo `#ubmList`

```html
<!-- Dentro #ubmHeader, prima di #ubmCloseBtn: -->
<button id="ubmExportBtn" title="Export bookmarks">
  <i class="bi bi-download"></i>
</button>

<!-- Oppure dopo #ubmList come sezione separata: -->
<div id="ubmFooter" style="padding: 8px; border-top: 1px solid rgba(0,0,0,0.08);">
  <!-- contenuto -->
</div>
```

### Step 2 — JS: listener

```javascript
document.getElementById('ubmExportBtn').addEventListener('click', () => {
  const json = JSON.stringify(userBookmarks, null, 2);
  _autoDownloadHTML('bookmarks.json', json);  // o altra logica export
});
```

### Step 3 — Colori

Il drawer usa `--ubm-bg` come variabile CSS per il background (impostata da `interfaceSettings.ubmDrawerColor`). I nuovi elementi erediteranno automaticamente il colore background. Per colori testo, usare valori assoluti o variabili CSS aggiuntive.

---

## PATTERN F — Iniettare Stili o Script nell'iframe EPUB

Per modificare il comportamento del documento EPUB renderizzato.

La posizione corretta è dentro `rendition.hooks.content.register` (riga ~4922):

```javascript
rendition.hooks.content.register((contents) => {
  // contents.document = documento nell'iframe
  // contents.window   = window dell'iframe

  // Aggiungere CSS:
  const style = contents.document.createElement('style');
  style.textContent = `
    /* stili custom iniettati nell'iframe */
    p { letter-spacing: 0.02em; }
  `;
  contents.document.head.appendChild(style);

  // Aggiungere script (inline):
  contents.document.querySelectorAll('p').forEach(p => {
    p.addEventListener('dblclick', () => {
      // doppio click su paragrafo
    });
  });

  // Comunicare con parent tramite postMessage:
  contents.window.addEventListener('customEvent', (e) => {
    window.postMessage({ type: 'customEvent', data: e.detail }, '*');
  });
});
```

**Importante**: questo hook viene eseguito ad ogni caricamento di capitolo. Tutto ciò che si inietta deve essere idempotente o tenere conto di possibili re-esecuzioni.

---

## PATTERN G — Aggiungere una Nuova Variante di Estrazione

Per aggiungere un terzo tipo di estrazione (oltre "current" e "tree") al menu dropdown.

### Step 1 — HTML: aggiungere voce al menu

In `#extractMenu` (riga ~2666):

```html
<div class="extract-menu-item" data-mode="annotated">
  <i class="bi bi-pen"></i>
  <span>Current + annotations</span>
</div>
```

### Step 2 — JS: gestire il nuovo `data-mode`

Trovare il listener `.extract-menu-item` (riga ~6145):

```javascript
document.querySelectorAll('.extract-menu-item').forEach(item => {
  item.addEventListener('click', async () => {
    const mode = item.dataset.mode;
    document.getElementById('extractMenu').classList.add('hidden');

    if (mode === 'current') {
      await extractCurrentChapter();
    } else if (mode === 'tree') {
      // estrazione tree esistente
    } else if (mode === 'annotated') {
      // AGGIUNTO:
      await extractCurrentChapterWithAnnotations();
    }
  });
});
```

### Step 3 — Implementare la funzione

Creare `extractCurrentChapterWithAnnotations()` seguendo il pattern di `extractCurrentChapter()`: raccoglie HTML, processa immagini, chiama `_generateCleanHTML`, `_autoDownloadHTML`, `saveExtractedChapterToDB`, `_openSn56`.

---

## PATTERN H — Aggiungere Comunicazione con sn56.x

Per inviare dati aggiuntivi da noesis810 a sn56.x o riceverne.

### Inviare dati aggiuntivi (noesis810 → sn56.x)

Aggiungere campi al payload in `_openExtractedEnv()` o nel punto dove si chiama `_openSn56()`:

```javascript
_openSn56({
  mode:        'chapter',
  htmlContent: html,
  bookName:    bookName,
  chapterName: chapterName,
  chapterId:   chapterId,
  // AGGIUNTO:
  customField: valoreDaPassare,
});
```

sn56.x deve leggere `payload.customField` dopo il parse del `#noesisPayload`.

### Ricevere dati da sn56.x (sn56.x → noesis810)

Il window bridge (riga ~3000) gestisce messaggi tipo `idb-request`. Per aggiungere un nuovo tipo di messaggio:

```javascript
// Nel handler window.addEventListener('message'):
if (e.data?.type === 'idb-request') {
  const { action } = e.data;

  if (action === 'getChapter') { /* ... */ }
  // AGGIUNTO:
  if (action === 'myNewAction') {
    // gestisci la richiesta
    const result = await myFunction(e.data.payload);
    e.source.postMessage({
      type: 'idb-response',
      requestId: e.data.requestId,
      data: result
    }, e.origin || '*');
  }
}
```

---

## CHECKLIST PRE-MODIFICA

Prima di qualsiasi modifica al codice, verificare:

- [ ] Ho letto le sezioni rilevanti del file sorgente (non basarmi solo sulla documentazione)
- [ ] Il nuovo ID è univoco (controllare DOC6 per ID esistenti)
- [ ] Le nuove classi CSS non confliggono con classi esistenti (controllare DOC5)
- [ ] Se aggiungo stato persistito: aggiornato sia `saveBookState()` che `loadAndApplyBookState()`
- [ ] Se aggiungo un popup/panel: aggiunto `_closeAllReaderMenus()`
- [ ] Se inietto nell'iframe: il codice è idempotente (può essere eseguito N volte)
- [ ] Se modifico il payload sn56.x: verificato che sn56.x gestisca il campo opzionalmente (retrocompatibilità)
- [ ] Se modifico schemi IDB: vecchi record senza il nuovo campo non causano errori (usare `|| defaultValue`)
- [ ] Se aggiungo chiamate IDB: usare `await openDB()` (non tenere riferimento fisso al DB tra chiamate)

---

## ERRORI COMUNI DA EVITARE

| Errore | Conseguenza | Soluzione corretta |
|--------|-------------|-------------------|
| Usare `document.getSelection()` per testo EPUB | Restituisce sempre vuoto | Usare `getIframeSelection()` |
| Modificare `spread`/`flow` senza `recreateRendition()` | Layout non aggiornato | Chiamare sempre `recreateRendition()` |
| Salvare blob URL copertina in un campo persistito a lungo termine | URL invalido alla riapertura | Salvare l'ArrayBuffer o il path, non il blob URL |
| Tenere riferimento a `db` tra chiamate async | IDB connection potrebbe essere chiusa | Chiamare `openDB()` ogni volta |
| Aggiungere listener dentro `loadLibraryBooks()` senza rimuoverli | Memory leak e listener duplicati | Usare event delegation su `#bookGrid` o rimuovere listener vecchi |
| Modificare `innerHTML` di container con listener | Perde tutti i listener figli | Usare event delegation o riattaccare listener dopo |
| Chiamare `rendition.display()` prima che epub.js sia pronto | Promise rejection silenziosa | Verificare che `rendition` sia non-null |
