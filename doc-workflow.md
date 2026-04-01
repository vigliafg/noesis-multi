# Workflow — Flussi d'uso

> Versione: **v810** | Pattern di utilizzo per 4 profili utente

---

## Pipeline Generale

```
LIBRARY → READER → ESTRAZIONE → EDITOR (sn56.x) → EXPORT
Import     Lettura    Capitolo     Summernote        PDF/DOCX/MD
.epub      Annota     HTML doc     Chunk + Snapshot  Filesystem
IDB        Highlight  Filesystem   Blob URL
Gerarchia  Segnalibri              IDB Bridge
```

---

## Fase 1 — LIBRARY (Catalogo)

Punto di ingresso dell'app. Interfaccia con tema scuro editoriale che mostra l'archivio completo di libri, estratti e snapshot.

**Struttura gerarchica visualizzata**:

```
Libro (copertina + metadati)
  └── Capitolo estratto (data creazione)
        ├── Snapshot 1 (descrizione + timestamp) ← più recente
        ├── Snapshot 2 ...
        └── Snapshot N (origin) ← primo snapshot
```

**Punti di accesso**:

| Azione | Risultato |
|--------|-----------|
| Click copertina libro | Apre Reader, ripristina ultima posizione |
| Click nome capitolo | Apre sn56.x con snapshot più recente |
| Click nome snapshot | Apre sn56.x con quella versione specifica |
| Click "Open Editor" | Apre sn56.x in modalità standalone |
| Click "Import Snapshots" | Reimporta file snapshot da disco |

---

## Fase 2 — READER (Lettura)

Ambiente di lettura completo basato su epub.js.

**Strumenti durante la lettura**:

- **TOC Sidebar** — Navigazione gerarchica al capitolo desiderato
- **Highlight** — 3 colori (giallo/verde/rosa) via EPUB CFI annotations; persistenti nel book state
- **Traduzione** — Nativa del browser, zero API esterne, zero limiti
- **Segnalibri** — Salva posizione corrente con label custom; CFI-based, persistenti
- **Display Panel** — Unificato: tipografia (font size, interlinea, layout) + 15 temi + colori interfaccia
- **Save State** — Snapshot posizione + tema + impostazioni (salva in `EpubLibraryDB`)

**Decisione chiave**: prima di estrarre, l'utente può evidenziare le sezioni importanti. Le evidenziazioni saranno presenti nel documento estratto.

---

## Fase 3 — ESTRAZIONE CAPITOLO

Trasforma il capitolo corrente in un documento HTML standalone pronto per lo studio.

**Modalità di estrazione**:

| Modalità | Funzione |
|----------|----------|
| `current` | Solo il capitolo corrente |
| `tree` | Capitolo corrente + tutti i sottolivelli annidati (assemblaggio automatico) |

**Processo tecnico**:
1. Recupero HTML dalla spine EPUB tramite JSZip
2. Conversione immagini → base64 inline
3. Riscrittura link interni come ancore locali
4. Generazione `chapterId` univoco (`ch_timestamp_random`)
5. Salvataggio record in `noesisDB` (metadati + snapshot origin)
6. Download automatico 2 file: `noesis-extract-*.html` e `noesis-origin-*.html`
7. Apertura in sn56.x tramite Blob URL con payload JSON

**Output**: sn56.x si apre in nuovo tab in **modalità chapter** con il documento caricato in Summernote.

---

## Fase 3b — RACCOLTA CHUNK

Durante la lettura del documento estratto in sn56.x, è possibile raccogliere frammenti:

- **Tipi di chunk**: testo selezionato, immagini, tabelle
- **Badge contatore** real-time sull'icona Inspect
- **Import/Export** collezione come JSON (backup portabile)
- **Riutilizzo**: una collezione JSON può essere importata in sessioni future

**Metodi di raccolta**:
- Seleziona → click pulsante [+]
- Doppio tap su immagine
- Long press (600ms) su immagine (Android)

**Gestione avanzata**: Inspect Panel per riordinare, iniettare al cursore, o assemblare tutti i chunk nel documento.

---

## Fase 3c — SNAPSHOT (Versioning doppio: IDB + Filesystem)

Il sistema snapshot salva lo stato del documento sia in **IndexedDB** (per accesso rapido dalla Library) che su **filesystem** (backup persistente).

**Salvataggio snapshot**:

1. Click su Save nell'Editor
2. Opzionale: inserire etichetta personalizzata
3. Generazione automatica di **due file** scaricati su disco:

| File generato | Variante | Contenuto |
|---|---|---|
| `noesis-clean-...html` | `clean` | Documento senza background-color (evidenziazioni rimosse) |
| `noesis-annot-...html` | `annot` | Documento con highlight inline preservati |

4. **Contemporaneamente**: salvataggio di due snapshot in IndexedDB (noesisDB)

**Naming schema**:
```
noesis-{VARIANT}-{BOOKNAME}__{CHAPTERNAME}__{YYYYMMDD_HHMMSS}_{CUSTOM}.html
```

**Esempio**:
```
noesis-clean-Harrison_Manual__Chapter_01__20260324_143022.html
noesis-annot-Harrison_Manual__Chapter_01__20260324_143022.html
```

**Primo snapshot (origin)**: il file generato all'estrazione contiene meta tag speciali (`noesis-chapter-id`, `noesis-book-name`, `noesis-chapter-name`, `noesis-snapshot-variant`) che lo rendono **reimportabile** nella Library.

---

## Fase 3d — IMPORT SNAPSHOTS (Workflow Reimporto)

Permette di recuperare snapshot precedentemente salvati su disco e reinserirli nella gerarchia della Library.

**Trigger**: click "Import Snapshots" in Library

**Flusso**:
1. Desktop (Chrome/Edge): `showDirectoryPicker()` → seleziona cartella
2. Android/Safari: file picker multi-file
3. Filtro automatico: solo file matching `noesis-(clean|annot|origin)-*.html`
4. Per ogni file: parsing meta tag (`noesis-chapter-id`, `noesis-book-name`, ecc.)
5. Match su `chapterId` (primary) o `bookName + chapterName` (fallback)
6. Inserimento in `noesisDB` con deduplication automatica
7. Aggiornamento UI Library

---

## Fase 4 — EDITOR sn56.x (Noesis Editor / Summernote Editor)

Editor WYSIWYG basato su Summernote-lite 0.9.1, comunicante con la Library tramite **IDB Bridge** (`postMessage`) per l'accesso a IndexedDB.

### Modalità operative

| Modalità | Attivazione | Caratteristiche |
|----------|-------------|-----------------|
| **chapter** | Da Reader (Extract) o Library (click snapshot) | Caricato con HTML del capitolo, contesto bibliografico (bookName, chapterName, chapterId), salvataggio in IDB + filesystem |
| **standalone** | Library → "Open Editor" | Editor vuoto, nessun contesto, salvataggio solo su filesystem |

### Funzionalità editing

- Formattazione testo completa (H1-H6, bold, italic, underline, strikethrough, liste)
- Tabelle con toolbar flottante contestuale
- Inserimento immagini (base64 inline, documento autocontenuto)
- Font size 8–28px
- **Excalidraw**: apre fork Noesis di Excalidraw in nuovo tab per creare diagrammi, flowchart e mappe mentali; esporta SVG/PNG inseribili nel documento

### Gestione chunk (Inspect Panel flottante)

- Visualizza tutti i chunk raccolti
- Riordina, elimina, inietta al cursore o assembla nel documento
- Selezione multipla + inject di gruppo

---

## Fase 5 — EXPORT

### Export Documento

| Formato | Utilizzo tipico |
|---------|----------------|
| TXT | Testo puro per appunti rapidi |
| MD | Markdown per blog, GitHub, Obsidian |
| MD+ZIP | Markdown + immagini per sistemi PKM |
| JSON | Struttura dati per elaborazioni successive |
| DOCX | Word per peer review, condivisione formale |
| PDF | Stampa ottimizzata A4 via print dialog nativo |

### Export Collezione

| Formato | Utilizzo tipico |
|---------|----------------|
| JSON | Backup chunk, condivisione, reimporto |
| HTML | Documento chunk standalone |
| MD | Chunk in Markdown |
| MD+ZIP | Chunk Markdown + immagini estratte |

---

## Persistenza Dati (v810)

| Store | Tipo | Contenuto |
|-------|------|-----------|
| `EpubLibraryDB` | IndexedDB | EPUB binari, metadati, posizione lettura, segnalibri per libro |
| `noesisDB` | IndexedDB | Metadati capitoli estratti, lista snapshot (senza HTML content) |
| `localStorage` | Browser | Tema, font size, interlinea, impostazioni UI |
| **Filesystem locale** | File HTML | Snapshot (`clean`/`annot`/`origin`) ed export documenti/collezioni |

**Nota v810**: i file HTML completi dei snapshot non sono più memorizzati in IndexedDB (come in v703-704), ma scaricati su filesystem. `noesisDB` mantiene solo i metadati (ID, nome, timestamp, descrizione) per popolare la Library.

---

## Profili Utente — Workflow Dettagliati

### Studente — Workflow Rapido

1. Import manuale del libro di testo
2. Naviga via TOC al capitolo da studiare
3. Evidenzia concetti chiave (colore per categoria)
4. Estrai capitolo con sottolivelli (`tree`)
5. In sn56.x: salva snapshot "Lettura iniziale" → 2 file su disco
6. Raccogli definizioni/formule importanti come chunk
7. Salva snapshot "Dopo raccolta"
8. Assembla chunk nel documento con Inspect Panel
9. Esporta PDF per stampa o DOCX per condivisione
10. Reimporta snapshots dalla cartella se necessario

### Ricercatore — Workflow Approfondito

1. Import articolo/monografia
2. Attiva traduzione browser (per testi in lingua straniera)
3. Seleziona grafici e citazioni rilevanti → chunk
4. Estrai capitolo → salva snapshot "Prima revisione"
5. Esporta collezione JSON come backup
6. Continua analisi, aggiungi annotazioni
7. Salva snapshot "Annotazioni complete"
8. Apri Editor → struttura report con titoli, tabelle, immagini
9. Esporta DOCX per peer review

### Blogger/Creator — Workflow Veloce

1. Leggi contenuto del libro
2. Seleziona passaggi rilevanti → chunk
3. Estrai capitolo → salva snapshot "Materiale raccolto"
4. In Editor: componi review con WYSIWYG
5. Esporta MD per blog tecnico o copia HTML per CMS (WordPress, Ghost)

### Lettore Multilingue — Workflow Linguistico

1. Import testo in lingua straniera
2. Attiva traduzione browser nativa (doppio riferimento: originale + tradotto)
3. Evidenzia vocabolario nuovo (rosa) e concetti (giallo)
4. Estrai capitolo → salva snapshot "Sessione 1 — Vocabolario"
6. Raccogli frasi difficili come chunk
7. Esporta collezione JSON come archivio vocabolario personale

---

## Note Operative

- **CORS**: usare server locale (`python3 -m http.server 8000`) invece del protocollo `file://` per EPUB con risorse esterne
- **Backup**: esportare periodicamente le collezioni come JSON per prevenire perdita annotazioni
- **Snapshot**: salvare prima di modifiche importanti per poter tornare a versioni precedenti
- **Immagini**: la conversione base64 garantisce documenti autocontenuti (nessun path rotto se il file viene spostato)
- **Import Snapshots**: i file `noesis-origin-*` contengono i meta tag necessari per il reimporto corretto; i file `clean`/`annot` richiedono che il capitolo esista già in `noesisDB`
