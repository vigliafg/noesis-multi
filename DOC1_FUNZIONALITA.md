# NOESIS810 — Documento 1: Funzionalità per Ambiente

> Fonte: `noesis810.html` (6498 righe) — Aggiornato: 2026-03-27

---

## ARCHITETTURA GENERALE

L'applicazione è un singolo file HTML (SPA — Single Page Application) che espone due ambienti principali distinti, navigabili tramite show/hide del DOM:

| Ambiente | ID DOM | Attivazione |
|----------|--------|-------------|
| **Biblioteca** | `#library-view` | All'avvio e dopo "Back to Library" |
| **Lettore** | `#reader-view` | All'apertura di un libro dalla biblioteca |

Un terzo ambiente — l'**Editor Estratti** — viene aperto come finestra popup separata (sn56.x) con payload JSON.

---

## AMBIENTE 1 — BIBLIOTECA (`#library-view`)

### 1.1 Layout e Struttura UI

La biblioteca occupa l'intera viewport con layout flex verticale:
- **Header fisso** in cima con barra laterale sinistra (titolo + sottotitolo) e barra destra (pulsanti azione)
- **Area scrollabile** sotto l'header con griglia dei libri (`#bookGrid`)

L'header non scorre: rimane visibile durante lo scroll dei contenuti.

### 1.2 Tema Biblioteca

La biblioteca supporta **due temi** attivabili con il pulsante toggle nell'header:

| Tema | Classe CSS | Sfondo | Testo |
|------|-----------|--------|-------|
| **Chiaro** (default) | (nessuna) | `#f7f6f3` (bianco caldo) | `#000000` |
| **Scuro** | `.lib-dark` | `#1a1a20` (grigio scuro) | `#e8e4dc` |

I colori sono gestiti interamente tramite **CSS custom properties** (`--lib-*`) ridefinite a livello di selettore `.lib-dark`, senza JavaScript. Il toggle aggiunge/rimuove la classe sul `#library-view`.

### 1.3 Import Libri EPUB

- **Pulsante "Import EPUB"**: apre un file picker (`<input type="file" accept=".epub">`) per selezione singola o multipla
- I file EPUB vengono salvati in **IndexedDB** (database `EpubLibraryDB`, store `books`)
- Durante il salvataggio: l'app carica il file con epub.js, estrae metadati (titolo, autore), tenta di ottenere la **copertina** (blob URL) e salva il tutto

### 1.4 Griglia Libri — Struttura Riga

Ogni libro viene renderizzato come riga con:

| Elemento | Descrizione |
|----------|-------------|
| **Copertina** | Miniatura dell'immagine di copertina. Se assente: icona libro (Bootstrap Icons) |
| **Titolo** | Titolo EPUB estratto dai metadati |
| **Autore** | Autore EPUB estratto dai metadati |
| **Badge statistiche** | Numero capitoli estratti, numero snapshot totali |
| **Data aggiunta** | Timestamp formattato |
| **Pulsante Elimina** | Icona cestino; rimuove libro da IndexedDB |

I libri sono ordinati per **data di aggiunta decrescente** (più recenti in cima).

### 1.5 Espansione Capitoli Estratti

Per ogni libro, se esistono capitoli estratti in `noesisDB`, viene mostrata una **sezione espandibile** con l'elenco dei capitoli:

- Ogni capitolo mostra: titolo capitolo, numero di snapshot
- Ogni capitolo è ulteriormente espandibile per mostrare i **singoli snapshot** associati

Ogni snapshot mostra:
- Indicatore visivo (dot verde per il più recente, grigio per gli altri)
- Descrizione/label opzionale
- Data/ora creazione
- **Pulsante di apertura** → lancia l'editor sn56.x con i dati del snapshot
- **Pulsante elimina snapshot** → rimuove solo quel snapshot da noesisDB

### 1.6 Pulsanti Strumenti (Tools Dropdown)

Un menu dropdown con strumenti aggiuntivi:

| Strumento | Funzione |
|-----------|---------|
| **Import Snapshots** | Picker file/cartella per reimportare snapshot HTML dal disco in noesisDB |
| **Open Editor** | Apre l'editor sn56.x in modalità vuota (senza payload capitolo) |

### 1.7 Sistema Help Biblioteca

- **Banner contestuale**: appare la prima volta che si apre la biblioteca (tracciato in `localStorage`)
- **Overlay Help completo**: aperto con pulsante `?` nell'header. Spiega i pulsanti disponibili e le funzionalità della biblioteca
- Entrambi sono chiudibili; lo stato "visto" è persistente per sessione/dispositivo

---

## AMBIENTE 2 — LETTORE EPUB (`#reader-view`)

### 2.1 Layout Generale

Il lettore ha struttura fissa verticale:
- **Header toolbar** con tutti i controlli di lettura
- **Area contenuto**: a sinistra sidebar TOC (opzionale, slide-in), al centro il viewer EPUB in iframe
- **Pulsanti navigazione floating** a sinistra e destra del viewer (precedente/successivo pagina)

### 2.2 Modalità di Visualizzazione

| Modalità | Controllo | Comportamento |
|----------|-----------|---------------|
| **Pagina singola** | Pulsante `□` | Una colonna, pagina EPUB per schermata |
| **Doppia pagina** | Pulsante `⬜⬜` | Due pagine affiancate (spread) |
| **Scroll continuo** | Pulsante `≡` | Flusso verticale continuo, scrollabile |

Le modalità pagina/doppia usano il motore di paginazione di epub.js; la modalità scroll usa `flow: "scrolled-doc"`. Il cambio modalità distrugge e ricrea la rendition (`recreateRendition()`).

### 2.3 Navigazione

- **Frecce floating**: pulsanti `<` e `>` ai lati del viewer. Cambiano pagina (prev/next) o fanno scroll nelle rispettive direzioni
- **TOC Sidebar**: pannello a sinistra con l'indice del libro. Ogni voce è cliccabile per navigare direttamente. Le voci hanno indentazione gerarchica per sezioni/sottosezioni
- **Status bar**: mostra il **breadcrumb** della posizione corrente (Libro > Capitolo > Sottocapitolo), condensato se troppo lungo

### 2.4 Tipografia

Popup accessibile da pulsante toolbar:

| Controllo | Descrizione | Range/Default |
|-----------|-------------|---------------|
| **Font size** | Dimensione testo | 50%–300%, step 5%, default 100% |
| **Line height** | Altezza riga | Valori discreti: 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4 |

I controlli `+` e `−` modificano il valore corrente; `Reset` riporta al default. Le modifiche sono applicate in tempo reale alla rendition.

### 2.5 Temi di Lettura (15 Temi)

Popup con campioni (swatches) raggruppati per categoria:

| Gruppo | Temi |
|--------|------|
| **White** | White, Off-White |
| **Cream/Sepia** | Cream, Sepia, Warm Sepia |
| **Light Gray** | Light Gray, Silver, Slate |
| **Medium Gray** | Medium Gray, Stone |
| **Dark Gray** | Dark Gray, Charcoal |
| **Dark/Black** | Dark, Near Black, Black |

Il tema attivo è evidenziato con bordo colorato. Ogni tema definisce `background`, `color` (testo), e `a` (links) per la rendition epub.js.

### 2.6 Impostazioni Interfaccia (Interface Settings)

Un popup con color pickers e slider per personalizzare i colori dell'interfaccia:

| Impostazione | Target UI | Default |
|-------------|-----------|---------|
| **Toolbar Color** | Sfondo header toolbar (gradiente) | `#1e293b` (blu scuro) |
| **Sidebar Color** | Sfondo sidebar TOC | `rgba(30,41,59,0.95)` |
| **Nav Buttons Color** | Colore pulsanti `<` `>` floating | `#1e293b` |
| **Nav Buttons Opacity** | Opacità pulsanti floating | 0.7 (slider 0–1) |
| **Bookmark Drawer Color** | Sfondo drawer segnalibri | `#1e293b` |

Ogni impostazione ha un pulsante **Reset** individuale.

### 2.7 Zoom Pulsanti Toolbar (Button Zoom)

- Slider da 60% a 200% che ridimensiona tutti i pulsanti/testi dell'header toolbar
- Consente di adattare la toolbar a schermi di diverse dimensioni o preferenze utente
- Implementato via CSS `transform: scale()` o font-size percentuale sull'header

### 2.8 Segnalibri Utente

Drawer scorrevole (slide da destra) accessibile dal pulsante segnalibro:

| Funzione | Descrizione |
|----------|-------------|
| **Nuovo segnalibro** | Crea segnalibro alla posizione corrente (CFI + href) |
| **Lista segnalibri** | Ordine decrescente per data; più recenti in cima |
| **Dati segnalibro** | Capitolo (dal TOC), preview testo 100 caratteri, timestamp, label opzionale |
| **Navigazione** | Click su segnalibro → naviga a quella posizione |
| **Eliminazione** | Pulsante `×` su ogni segnalibro |
| **Badge counter** | Numero segnalibri mostrato sul pulsante toolbar |

I segnalibri sono persistiti in IndexedDB (store `books`, sotto il record del libro).

### 2.9 Highlights (Evidenziature)

| Colore | Classe CSS |
|--------|-----------|
| **Giallo** | highlight-yellow |
| **Verde** | highlight-green |
| **Rosa** | highlight-pink |

Workflow highlight:
1. L'utente seleziona testo nel viewer EPUB
2. epub.js emette evento `selected` con il CFI della selezione
3. Il pulsante highlight si attiva
4. Clic sul pulsante → selezione colore → applicazione `rendition.annotations.highlight(cfi)`
5. Highlight salvati come array `[{cfi, color}]` in `savedState` per ripristino

**Rimozione**: click "Remove" nel menu colori con testo selezionato.

### 2.10 Estrazione Capitoli

Due modalità disponibili via menu dropdown:

| Modalità | Descrizione |
|----------|-------------|
| **Extract Current** | Estrae solo la sezione corrispondente alla posizione corrente nel TOC |
| **Extract Tree** | Estrae il capitolo corrente + tutti i suoi sottocapitoli ricorsivamente |

Processo di estrazione:
1. Raccolta HTML del capitolo dalla rendition epub.js
2. Risoluzione immagini (contenute nello zip EPUB) → **base64 embedding** inline
3. Raccolta stili CSS dell'EPUB
4. Generazione di **due file HTML**: `noesis-extract-*` (pulito per lettura) e `noesis-origin-*` (raw con metadati)
5. Salvataggio snapshot in `noesisDB`
6. Download automatico dei file sul filesystem
7. Apertura editor sn56.x con payload JSON del capitolo estratto

### 2.11 Preview Media (Immagini e Tabelle)

- Le immagini nei testi EPUB sono **cliccabili** per visualizzarle in dialog a piena pagina
- Le tabelle sono **wrappate** in contenitori scrollabili orizzontalmente, con pulsante tap per preview fullscreen
- La comunicazione avviene via `postMessage` tra l'iframe EPUB e il parent window
- Il dialog media mostra: immagine o tabella, pulsante chiudi, pulsante "fullscreen"

### 2.12 Salvataggio Stato

Il pulsante "Save State" (o `Ctrl+S` implicito) persiste in IndexedDB:
- Posizione corrente (CFI + href)
- Font size, line height
- Tema selezionato
- Modalità scroll/pagina, doppia pagina
- Visibilità sidebar
- Zoom toolbar
- Colori interfaccia personalizzati
- Array highlights
- Timestamp ultimo salvataggio

Al riapertura del libro, lo stato viene automaticamente ripristinato.

### 2.13 Help Lettore

- **Banner** contestuale alla prima apertura (localStorage tracking)
- **Overlay help** completo con:
  - Lista tasti tastiera (es: `?` → apre help)
  - Descrizione di ogni pulsante toolbar
  - Spiegazione modalità di visualizzazione
- Attivabile con pulsante `?` o tasto `?` da tastiera

---

## AMBIENTE 3 — EDITOR ESTRATTI (sn56.x — Popup Esterno)

L'editor è un'applicazione separata aperta tramite `window.open('sn56.x', ...)` con un payload JSON passato.

Il payload include:
- `mode: "chapter"` — indica che si tratta di un capitolo EPUB estratto
- Titolo libro, titolo capitolo
- Contenuto HTML del capitolo
- Riferimento snapshot ID per aggiornamento noesisDB

L'editor riceve il payload e lo usa come contesto di lavoro per modifiche, annotazioni, esportazioni. Le comunicazioni tra editor e biblioteca avvengono tramite bridge `window.postMessage` / `IndexedDB` condiviso.

---

## OVERLAY DI CARICAMENTO

Un overlay (`#loading-overlay`) con spinner e messaggio testuale viene mostrato durante:
- Importazione file EPUB
- Apertura libro dalla biblioteca
- Operazioni di estrazione capitolo

Visibile a piena schermata sopra ogni altro elemento, con z-index elevato.
