# Noesis — Changelog

---

## v0.12.0 — noesis812.html

Versione di produzione. Comprende tutte le modifiche di v0.11.x (non rilasciate pubblicamente) più il redesign completo dell'interfaccia reader e della libreria.

---

### Reader — Nuova menubar

È stata introdotta una barra dei menu orizzontale (`nav.reader-menubar`) nella parte superiore dell'ambiente di lettura, che sostituisce visivamente la toolbar a icone precedente (ora nascosta come compatibilità interna).

Voci presenti:

| Voce | Funzione |
|------|----------|
| **Library** | Torna alla libreria |
| **TOC** | Apre/chiude il pannello Table of Contents |
| **Bookmarks** | Apre il pannello segnalibri |
| **Display** | Apre il pannello impostazioni visualizzazione |
| **Navigate** | Dropdown modalità di navigazione (vedi sotto) |
| **Annotate** | Attiva la modalità evidenziazione |
| **Extract** | Apre il menu estrazione capitolo |
| **Help** | Apre la guida contestuale del reader |

La toolbar precedente (`.toolbar`) è mantenuta nel DOM con `display: none` per compatibilità con il codice interno; non è visibile all'utente.

---

### Reader — Bottone Navigate redesignato

Il bottone **Navigate** nella menubar è ora informativo e interattivo:

- **Badge inline** sul bottone mostra sempre la modalità attiva: `Navigate [Page]` oppure `Navigate [Scroll]`
- Al clic appare un **dropdown** con due voci: **Page Mode** e **Scroll Mode**
- La modalità attiva è evidenziata in **grassetto blu** (`font-weight: 700; color: #1d4ed8`)
- Selezionando una voce diversa da quella attiva, la modalità viene cambiata immediatamente e il rendition viene ricreato
- Il badge si aggiorna in tempo reale al cambio di modalità

---

### Reader — Stampa multi-pagina corretta

Nella versione 810, la stampa dal menu del browser catturava soltanto la prima pagina del capitolo a causa della struttura CSS column-based di epub.js.

**Fix:** Prima della stampa (`beforeprint`), il contenuto completo degli iframe EPUB viene copiato in un contenitore temporaneo `#reader-print-container`. Le regole CSS di impaginazione a colonne e le trasformazioni di epub.js vengono rimosse per consentire il riflusso naturale del testo su più pagine. Il contenitore viene eliminato dopo la stampa (`afterprint`).

Comportamento:
- In stampa vengono nascosti `#library-view` e `#reader-view`
- Viene mostrato solo `#reader-print-container` con font di sistema, max-width 900px, line-height 1.6
- Tutti i capitoli negli iframe (anche in dual-page mode) vengono inclusi

---

### Reader — Pannello Display ridisegnato

Il pannello delle impostazioni di visualizzazione è stato ridisegnato con sfondo bianco e palette neutro-chiara, sostituendo il precedente sfondo dark (`#1e293b`).

Modifiche:
- Sfondo: da `#1e293b` a `white`
- Testo: da `#94a3b8` / `#e2e8f0` a `#374151`
- Sezioni attive: colore da `#93c5fd` a `#3b82f6`
- Bordi: da rgba-bianchi a rgba-neri leggeri
- Box shadow alleggerita da `0 8px 32px rgba(0,0,0,0.45)` a `0 4px 12px rgba(0,0,0,0.15)`
- Rimosso `backdrop-filter: blur` dai pannelli floating

---

### Library — Header ridisegnato

L'intestazione della libreria è stata completamente ridisegnata:

- **Sfondo fisso**: gradiente viola `#667eea → #764ba2` (non più condizionato dal tema chiaro/scuro)
- **Pulsanti header** unificati in classe `.lib-header-btn`: flat, senza bordo, testo bianco, hover con sottolineatura
- Rimozione dei bordi e degli sfondi variabili per tema dai pulsanti

---

### Library — Selezione tema con dropdown

Il precedente toggle singolo (icona luna/sole) è stato sostituito con un **dropdown temi**:

- Clic sul pulsante "Themes ▾" apre un menu con due voci: **Light** (icona sole) e **Dark** (icona luna)
- La selezione applica il tema immediatamente e chiude il dropdown
- Il dropdown si chiude anche cliccando fuori da esso

---

### Library — Pulsanti header rinominati

| v0.10 | v0.12 | Note |
|-------|-------|------|
| `#libThemeToggle` | `#libThemesBtn` + dropdown | Toggle sostituito da dropdown |
| `#importLabel` | `#libAddBooksBtn` | Aggiunge libri EPUB |
| `#importSnapshotsBtn` | `#libImportSnapshotsBtn` | Importa snapshot |
| `#libOpenEditorBtn` | `#libEditorBtn` | Apre editor sn56 standalone |

---

### CSS — Uniformità colori

In numerosi componenti (card libri, lista capitoli, TOC, highlight, form inputs) i colori di testo sono stati uniformati a `#374151` e i bordi `1px solid #ddd` sono stati sostituiti con `border: none` o `border: 1px solid transparent` per un aspetto più pulito.

---

---

## v0.11.x — noesis811.html *(non rilasciata pubblicamente)*

---

### Auto-save dinamico della posizione di lettura

La posizione di lettura viene ora salvata **automaticamente ogni 3 secondi** senza richiedere alcuna azione dall'utente.

**Come funziona:**

- Al caricamento di un libro viene avviato un timer (`startAutoSave`) che ogni 3 secondi calcola il CFI dell'elemento visivamente centrato nell'iframe epub
- Il CFI viene confrontato con l'ultimo salvato: se è cambiato, viene eseguita una scrittura leggera su IndexedDB (`savePositionOnly`) che aggiorna solo il campo `position` del record libro, preservando tutti gli altri dati
- Il timer viene fermato (`stopAutoSave`) alla chiusura del libro o al ritorno in libreria

**Calcolo del CFI al centro visivo (`_getCenterCfi`):**

- In **Scroll Mode**: usa `elementFromPoint(cx, cy)` sull'iframe per trovare l'elemento al centro dello schermo, poi calcola il CFI con `cfiFromElement`
- In **Page Mode**: usa `rendition.currentLocation().start.cfi` come fallback
- In entrambi i casi gestisce eccezioni silenziosamente

**Pausa durante la traduzione browser:**

Se il browser ha attivato la traduzione automatica della pagina (Chrome/Edge built-in translate), l'auto-save viene **sospeso** per evitare che le modifiche al DOM introdotte dalla traduzione producano CFI errati. Il rilevamento avviene tramite `_isBrowserTranslated()` che controlla le classi `translated-ltr`, `translated-rtl` e l'attributo `translated` su `<html>`.

---

### Separazione del salvataggio: posizione vs impostazioni visive

In v0.10 il salvataggio era un'unica operazione che scriveva tutto il record libro (tipografia, tema, modalità di navigazione, posizione, highlights). Ora è diviso in due operazioni indipendenti:

| Funzione | Cosa scrive | Quando |
|----------|-------------|--------|
| `savePositionOnly(cfi, href)` | Solo `savedState.position` | Ogni 3 secondi (auto) |
| `saveVisualSettings()` | Font size, line height, tema, scroll mode, dual page, button zoom, interface settings | Su richiesta utente (pulsante Save nel prompt) |
| `saveBookState()` | Chiama entrambe | Utilizzato internamente dove serve un salvataggio completo |

Questa separazione evita scritture IDB pesanti ad ogni cambio di pagina.

---

### Rimozione del pulsante "Save State"

Il pulsante manuale **Save** (`#saveStateBtn`) è stato rimosso dalla toolbar del reader. Il salvataggio avviene ora automaticamente per la posizione e tramite prompt contestuale per le impostazioni visive.

---

### Prompt salvataggio impostazioni display (`#displaySavePrompt`)

Un banner floating appare in basso al centro dello schermo quando l'utente chiude il pannello Display dopo aver modificato impostazioni visive non ancora salvate.

Comportamento:
- Appare con animazione slide-up e fade-in
- Rimane visibile per **8 secondi**, poi scompare automaticamente
- Pulsante **Save**: salva le impostazioni visive e mostra un toast di conferma
- Pulsante **×**: chiude il prompt senza salvare
- **Dirty check**: il prompt compare solo se le impostazioni sono effettivamente cambiate rispetto all'ultimo salvataggio (confronto con `_snapshotVisualState()`)
- Non compare se nessun libro è aperto

---

### Fix: stampa PDF nell'editor sn56

La stampa dal browser mentre l'editor sn56 era aperto produceva un PDF di una sola pagina a causa di `html, body { height: 100%; overflow: hidden; }` non sovrascritto in `@media print`.

**Fix** aggiunto al primo blocco `@media print` dell'editor:
```css
html, body { height: auto !important; overflow: visible !important; }
```

---

*Le versioni precedenti (noesis810.html e precedenti) non hanno un changelog strutturato in questo file.*
