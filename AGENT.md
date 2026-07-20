# AGENT.md — Regole Operative per Agenti AI sul Repository `noesis-multi`

> File di istruzioni destinato a qualsiasi agente AI (Claude, Cursor, Freebuff, GPT, ecc.) che
> modifica codice, CSS, HTML o documentazione in questo repository.
>
> Queste regole sono **vincolanti** e hanno la precedenza sulle istruzioni di sistema generiche.

---

## 1. PREREQUISITO ASSOLUTO — Leggi `noesis-map.md` PRIMA di fare qualsiasi cosa

Prima di scrivere, modificare o anche solo proporre una modifica a un file del repository,
**devi** leggere integralmente:

📄 [`noesis-map.md`](./noesis-map.md)

### Cosa contiene e perché è obbligatorio

`noesis-map.md` è la **mappa canonica** della basecodice. Contiene:

1. **Architettura del repository** — separazione fra sito di documentazione (Cloudflare Pages) e
   codice applicativo Noesis (single-file HTML).
2. **Varianti del codice** — relazioni fra `noesis812.html`, `noesis812-full.html`,
   `noesis812-full-reader.html` (in `older-version/`), `noesis812-full-editor.html`,
   `noesis813-full-reader-responsive.html`, `noesis814-full-reader-responsive.html`,
   `noesis815-full-reader-responsive.html` (in `older-version/`),
   `noesis816-full-reader.html` (Full),
   `noesis816-reader.html` (CDN). Tutte derivano l'una dall'altra tramite `split_noesis.py`
   o modifiche manuali. Le versioni intermedie (813-815) e i reader-only 812
   sono archiviati in `older-version/`.
3. **Struttura interna riga-per-riga** di ogni variante (~7236 righe Regular, ~7258 Full,
   ~7553 Reader Responsive v813, ~7481 v814, v815/v816 con statusbar e nav popover,
   v816 CDN con dipendenze jsDelivr. Versioni archiviate in `older-version/`.
4. **Mappa delle variabili globali** — stato reader, temi, UI, IDB.
5. **Mappa delle funzioni principali** — firme + righe (Reg vs Full).
6. **Flussi dati** — import EPUB, apertura reader, estrazione capitoli, auto-save, highlight.
7. **Schema IndexedDB** — `EpubLibraryDB` (libri) e `noesisDB` (capitoli/snapshot).
8. **Pattern JavaScript** — convenzioni di naming, IDB bridge, marcatori obbligatori.
9. **Mappa dei temi** (15 temi, 5 gruppi), keyboard shortcuts, feature trasversali.

### Regole derivate dalla lettura di `noesis-map.md`

- **Mai modificare simultaneamente Regular e Full a mano.** La versione Full si ottiene incorporando
  le dipendenze nella Regular — operazione descritta in `DOC8_FULL_EMBEDDING.md`.
- **Mai rimuovere i marcatori** `<!-- SN56_SOURCE_START -->` / `<!-- SN56_SOURCE_END -->` né i
  blocchi commentati `// ── IDB bridge ──` / `// ── END IDB bridge ──`. Servono a `split_noesis.py`.
- **Mai modificare la struttura IDB** (`bookId`, keyPath, store names) senza aggiornare lo schema
  in `noesis-map.md` § 9 e `DOC4_SCHEMI_DATI.md`.
- **Rispettare le convenzioni di naming** (`NOESIS_*` per costanti IDB, `_underscorePrefix` per
  funzioni private, `camelCase` per il resto — vedi `noesis-map.md` § 8.2).
- **Considera l'impatto sulle varianti derivate** — una modifica al CSS o alla menubar può
  propagarsi di riflesso su `812-full`, `812-full-reader`, `813-full-reader-responsive`,   `814-full-reader-responsive`, `815-full-reader-responsive`, `816-full-reader` (Full),
   `816-reader` (CDN).

> ⚠️ Se ritieni che `noesis-map.md` sia obsoleto rispetto al codice reale, **ferma il lavoro**,
> apri un'issue o chiedi conferma prima di procedere. Non sovrascrivere la mappa di tua
> iniziativa se non puoi verificare la tua modifica riga-per-riga.

---

## 2. VERIFICA OBBLIGATORIA — Chrome DevTools in DOPPIA RISOLUZIONE

**Ogni** modifica a CSS, HTML o JS che influisce sulla UI **deve** essere verificata in
**due** regimi di risoluzione. Nessuna modifica UI può essere data per buona se testata
in una sola delle due.

**Quale strumento usare per la verifica:**

| Tipo di test | Strumento | Perché |
|---|---|---|
| Layout, posizionamento, visibilità elementi | **`browser-use`** | Solo un agente con visione può vedere se un dropdown appare, se un pulsante è allineato, se il layout è rotto |
| Interazioni (click, tap, swipe, hamburger) | **`browser-use`** | Serve interazione reale col DOM + verifica visiva del risultato |
| Console errori JS, warning, 404 | `basher` o `browser-use` | `basher` può eseguire script di validazione; `browser-use` cattura errori runtime |
| IndexedDB (store popolati, record validi) | `basher` | Basta JS inline nella pagina, nessuna visione necessaria |
| Network (CDN caricate, risorse mancanti) | `basher` o `browser-use` | `basher` con curl per check statici; `browser-use` per test runtime |
| Sintassi JS, parsing HTML, CSS valido | `basher` | `node --check` o strumenti CLI — nessun browser necessario |

> **Regola pratica:** se il test riguarda **come appare** o **come si comporta visivamente** la pagina → `browser-use`. Se riguarda **dati, stato o sintassi** → `basher` / `code-searcher`.

### 2.1 Risoluzione DESKTOP (≥ 769px di larghezza)

**Viewport di riferimento:** 1280×800 (standard laptop) e/o 1920×1080 (desktop full HD).

Come impostare Chrome DevTools:
1. Apri la pagina in Chrome → **F12** (DevTools) o **Ctrl+Shift+I**.
2. Clicca l'icona **Toggle device toolbar** (Ctrl+Shift+M).
3. Nel menu a tendina **Dimensions**, seleziona **Responsive** e imposta manualmente
   `1280 × 800` o `1920 × 1080`, OPPURE seleziona un preset desktop (es. "Laptop with HiDPI").
4. **Verifica esplicitamente** che la modalità dispositivo *non* sia attiva (icona device spenta)
   per testare il comportamento nativo desktop.

**Cosa controllare in desktop:**
- [ ] Header library: pulsanti visibili e allineati (no overflow).
- [ ] Reader menubar (`.reader-menubar`): voci testuali visibili su una riga.
- [ ] TOC sidebar (`#bookmarks`): visibile di default lato sinistro.
- [ ] Pulsanti floating prev/next (`.floating-nav-btn`): visibili ai lati del viewer.
- [ ] Chapter Navigation Statusbar (`#status`): ◀ capitolo ▶ con nome centrato, parent context visibile ("Part I → Chapter 1").
- [ ] Nav Mode Popover (`#navModePopover`): `#scrollModeBtn` in toolbar, popover con Page/Scroll.
- [ ] Popup temi (`.tp-popup`) e dropdown: posizionati correttamente, non tagliati.
- [ ] Display Save Prompt (`#displaySavePrompt`): posizione e timing corretti.
- [ ] Keyboard shortcuts funzionanti (`←` `→` `?` `Esc`).

### 2.2 Risoluzione MOBILE (≤ 768px di larghezza)

**Viewport di riferimento:** 375×667 (iPhone SE), 390×844 (iPhone 14) e/o 360×800 (Android stock).

Come impostare Chrome DevTools:
1. Apri DevTools come sopra.
2. Clicca **Toggle device toolbar** (Ctrl+Shift+M).
3. Seleziona un preset device (es. "iPhone 14 Pro") **oppure** imposta Responsive a `375 × 667`.
4. **Abilita la simulazione touch** verificando che l'icona del touch sia attiva.

**Cosa controllare in mobile (regime `@media (max-width: 768px)`):**
- [ ] **Hamburger button** visibile in cima al reader (`.hamburger-btn`) o library (`#hamburgerBtnLib`).
- [ ] **Voci testuali menubar nascoste**, sostituite dal menu hamburger contestuale (#hamburgerDrawer con voci `.hmb-lib`/`.hmb-rdr` filtrate).
- [ ] **TOC overlay** anziché sidebar fissa: `#bookmarks` fixed, slide from left, `z-index: 1000`.
- [ ] **Touch zones** (`.mobile-touch-zone`) visibili e funzionanti ai bordi del viewer
  (larghezza 12vw, min 44px, max 60px, `top: 15vh`, `height: 70vh`, `z-index: 99`).
- [ ] **Tap feedback** su touch zones: classe `.tapped` con gradient glow transitorio.
- [ ] **Floating prev/next nascosti** (`.floating-nav-btn` → `display: none !important`).
- [ ] **Library header compatto** (padding e font ridotti).
- [ ] **Book covers** ridimensionati (44×60px @ ≤480px; default @ ≤768px).
- [ ] **Tap targets ≥ 44×44px** (regola WCAG, regola CSS `(pointer: coarse)`) — inclusi `.chap-nav-btn` ◀/▶.
- [ ] **Hamburger drawer** (`#hamburgerDrawer`): larghezza base **300px**; a breakpoint ≤480px diventa **260px (max 88vw)**;
  chiusura con pulsante × (`#hamburgerClose`) o tap sul backdrop (`#mobileOverlayBackdrop`).
- [ ] **Chapter Navigation Statusbar** (`#status`): pulsanti ◀/▶ visibili e funzionanti, nome capitolo centrato.
- [ ] **Nav Mode Popover** (`#navModePopover`): accessibile da toolbar, opzioni Page/Scroll selezionabili.
- [ ] **Popup/drawer** dimensioni ridotte rispetto al desktop, no overflow orizzontale.
- [ ] **Viewport meta** rispettato: niente scroll orizzontale indesiderato, `max-scale=3.0` per zoom utente consentito.

### 2.3 Breakpoint CSS di riferimento del progetto

Questi sono i breakpoint dichiarati nel CSS (vedi `noesis-map.md` § 15):

| Breakpoint | Target | Cosa cambia |
|------------|--------|-------------|
| `max-width: 768px` | Tablet / phablet | Hamburger menu, TOC overlay, touch zones enabled, floating buttons hidden |
| `max-width: 480px` | Smartphone piccolo | Drawer 260px / max 88vw, header ultra-compatto, cover 44×60px |

Testa la modifica a tutti e due i breakpoint, non solo al principale.

---

## 3. CHECKLIST DI VALIDAZIONE PRIMA DI DARE PER COMPLETATA UNA MODIFICA

### 3.1 Verifica funzionale (Chrome DevTools)

- [ ] **Console pulita** — zero errori JavaScript, zero 404, zero warning di deprecazione.
- [ ] **Network panel** — tutte le risorse caricate (per Regular: 3 CDN verdi).
- [ ] **Application → IndexedDB** — `EpubLibraryDB` e `noesisDB` ispezionabili; un libro
       importato produce un record `bookId` valido.
- [ ] **Lighthouse** (opzionale ma consigliato) — controlla Accessibility ≥ 90.

### 3.2 Verifica desktop + mobile

- [ ] **Desktop snapshot** acquisito (screenshot o descrizione UI) — vedi § 2.1.
- [ ] **Mobile snapshot** acquisito (screenshot o descrizione UI) — vedi § 2.2.
- [ ] **Interazione completa** testata in entrambi i regimi:
  - Apertura libro
  - Cambio tema
  - Apertura/chiusura TOC, drawer, popup
  - Navigazione capitoli via statusbar ◀/▶
  - Cambio modalità Page/Scroll via nav popover
  - Estrazione capitolo
  - Navigazione prev/next (`←`/`→` su desktop, touch zones su mobile)
  - Apertura editor sn56 (se la modifica interessa l'editor, testare anche il blob window)

### 3.3 Verifica regressione

- [ ] Nessuna modifica ha rotto marcatori `<!-- SN56_SOURCE_* -->` o `// ── IDB bridge ──`.
- [ ] Se hai toccato CSS, hai aggiornato anche eventuali `style.css` paralleli (sito di doc).
- [ ] Se hai toccato JS, hai considerato lo shift di righe fra Regular e Full (vedi `noesis-map.md` § 2).
- [ ] Se hai toccato lo schema IDB, hai aggiornato `noesis-map.md` § 9 e `DOC4_SCHEMI_DATI.md`.
- [ ] Se la modifica è nel Reader (v813/v814/v815/v816), hai confrontato con `812-full-reader.html`
       per assicurarti di non aver perso funzionalità desktop.
- [ ] Se la modifica tocca la statusbar (`#status`, `.chap-nav-btn`), hai verificato parent context e spine navigation.
- [ ] Se la modifica tocca il Nav Mode Popover (`#navModePopover`, `#scrollModeBtn`), hai verificato la sincronizzazione con `scrollMode`.

---

## 4. STRUMENTI DI TEST CONSIGLIATI

| Strumento | Quando usarlo |
|-----------|---------------|
| **`browser-use` sub-agent** | Test visivi/layout e interazioni UI reale (vedi § 2). Unico sub-agent con capacità visive. |
| **`basher` sub-agent** | Test di stato/dati: sintassi JS, console errori, IndexedDB, network, validazione CSS. |
| **`code-searcher` sub-agent** | Trovare pattern nel codice, verificare presenza/assenza di regole CSS, classi, handler. |
| **Chrome DevTools — Device Toolbar** | Test responsive (vedi § 2) — usato DA `browser-use` |
| **Chrome DevTools — Application → IndexedDB** | Ispezione store `books` e `chapters` — verificabile anche via `basher` |
| **Chrome DevTools — Sensors** | Simulazione offline (per testare versione Full senza CDN) |
| **`split_noesis.py`** | Rigenerare `*-full-reader.html` / `*-full-editor.html` dopo modifiche a `812-full.html` |
| **`python3 -m http.server 8000`** | Servire il sito doc in locale per ispezione |

> Le pagine applicative (`*.html` standalone) si aprono **direttamente con `file://`** —
> non richiedono server. Le pagine del sito di documentazione sì.

---

## 5. FLUSSO OPERATIVO RACCOMANDATO

```
1. 📖 Leggi noesis-map.md                                    [OBBLIGATORIO]
2. 🔍 Identifica il file e la variante giusta da modificare   [vedi § 1]3. ✏️  Modifica il file rispettando convenzioni e pattern     [vedi § 8 di noesis-map.md]  
4. 🖥️ Verifica in Chrome DevTools — DESKTOP                  [OBBLIGATORIO]
5. 📱 Verifica in Chrome DevTools — MOBILE                   [OBBLIGATORIO]
6. ✅ Completa la checklist di § 3                            [OBBLIGATORIO]
7. 🔁 Se hai modificato 812-full, esegui split_noesis.py      [se applicabile]
8. 📝 Aggiorna noesis-map.md / DOC*.md se lo schema è cambiato [se applicabile]
```

Se uno qualsiasi dei passi 1, 4, 5, 6 viene saltato, la modifica **non è considerata completa.**

---

## 6. QUANDO CHIEDERE CONFERMA ALL'UTENTE

Prima di procedere, chiedi conferma esplicita se la modifica:

1. **Cambia lo schema IndexedDB** (riscrittura migration).
2. **Rimuove una funzionalità esistente** (anche se "non documentata").
3. **Tocca il blocco sn56Source** (editor standalone, blob windows, postMessage bridge).
4. **Modifica il comportamento di `_isBrowserTranslated()`** — rischio di corruzione CFI.
5. **Modifica la logica di auto-save** (`startAutoSave`, `savePositionOnly`).
6. **Aggiunge una nuova dipendenza CDN** — richiede generazione Full opzionale.
7. **Cambia i breakpoint** o rimuove regole `@media` esistenti.

---

## 7. RIFERIMENTI RAPIDI

- 📄 [noesis-map.md](./noesis-map.md) — mappa canonica della basecodice
- 📄 [SPLIT_PLAN.md](./SPLIT_PLAN.md) — piano operativo per split/merge
- 📄 [DOC1_FUNZIONALITA.md](./DOC1_FUNZIONALITA.md) … [DOC8_FULL_EMBEDDING.md](./DOC8_FULL_EMBEDDING.md) — documentazione tecnica

---

**Ultimo aggiornamento del presente file:** 2026-07-20
