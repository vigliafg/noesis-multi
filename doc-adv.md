# Posizionamento e Punti di Forza

> Versione: **v810** | Analisi strategica e differenziatori chiave

---

## Il Concetto: Reading-to-Knowledge System

Noesis si autodefinisce un **Reading-to-Knowledge System**, non semplicemente un reader. La differenza è sostanziale: mentre un reader consente di leggere, un Reading-to-Knowledge System trasforma la lettura in un processo attivo di produzione di conoscenza — annotazione, selezione, rielaborazione, versioning, esportazione.

**Domande che Noesis risponde**:
- Perché interrompere la lettura per prendere appunti su un'altra app?
- Perché le evidenziazioni rimangono nel libro senza diventare documento di studio?
- Perché usare tre strumenti diversi per leggere, studiare ed esportare?
- Perché non poter tornare a versioni precedenti del proprio lavoro di studio?

Risposta: Noesis unifica questi strumenti in un singolo file HTML nel browser.

---

## Il Panorama degli EPUB Reader: Confronto

### Categoria 1 — Reader Desktop Tradizionali
*Calibre, Adobe Digital Editions, Kobo Desktop*

| Dimensione | Noesis v810 | Reader tradizionali |
|---|---|---|
| Installazione | Non richiesta (HTML) | App nativa |
| Gestione libreria | IndexedDB browser | File system locale |
| Traduzione integrata | Via browser (zero API) | Non presente |
| Annotazioni | Highlight 3 colori | Highlight e note |
| Raccolta chunk | Sistema collezioni | Assente |
| Estrazione capitoli | Con gerarchia e assemblaggio automatico | Assente |
| Versioning studio | Snapshot su filesystem | Assente |
| Export multiplo | 7 formati doc + 4 formati collezione | Limitato |
| Editor integrato | Summernote WYSIWYG (sn56.x) | Assente |
| Privacy | Zero server | Locale |
| Multipiattaforma | Qualsiasi browser moderno | Per OS specifico |

**Vantaggio Noesis**: va oltre la lettura con workflow di studio integrato e versioning del proprio lavoro.

---

### Categoria 2 — Reader Web-based con Account
*Kindle Cloud Reader, Kobo Web, Google Play Books*

| Dimensione | Noesis v810 | Reader web con account |
|---|---|---|
| Account richiesto | No | Sì, obbligatorio |
| File propri (.epub) | Qualsiasi | Solo acquistati sulla piattaforma |
| Privacy | Zero server | Dati su cloud |
| Offline | Sì | Parziale o no |
| DRM | No (non supportato) | Dipende dalla piattaforma |
| Traduzione | Browser nativo | Solo alcune piattaforme |
| Export/estrazione | Sì (7+4 formati) | Non permesso |
| Versioning appunti | Snapshot su filesystem | Assente |
| Costo | Gratis | Abbonamento/acquisto |

**Vantaggio Noesis**: libertà totale — file propri, nessuna dipendenza da piattaforma, nessun abbonamento, nessun tracking.

---

### Categoria 3 — App Mobili di Lettura
*Moon+ Reader Pro, Lithium, ReadEra (Android)*

| Dimensione | Noesis v810 | App mobili |
|---|---|---|
| Browser-based | Sì | App nativa |
| Highlight | 3 colori | Spesso multicolore |
| Dizionario | ✕ | Dizionari offline |
| Export capitoli | Con gerarchia | Raramente |
| Editor WYSIWYG | Summernote completo | Assente |
| Export DOCX/MD/PDF | Sì | Raramente |
| Versioning lavoro | Snapshot su filesystem | Assente |
| Ottimizzato desktop | Sì | Progettato per mobile |
| Costo | Gratis | Spesso a pagamento |

**Vantaggio Noesis**: produzione di documenti di studio (editor, export multiplo, snapshot). Progettato per chi studia a un computer.

---

### Categoria 4 — Strumenti di Annotazione
*Hypothesis, Readwise, Kindle Highlights*

| Dimensione | Noesis v810 | Strumenti annotazione |
|---|---|---|
| Integrazione con reader | Tutto in un file | Plugin/estensione separata |
| Raccolta highlight | Sì | Core feature |
| Versioning appunti | Snapshot locale su filesystem | Versioning cloud |
| Flashcard/spaced repetition | Assente | In alcuni |
| Export | 7 doc + 4 collezione | Markdown, Notion, ecc. |
| Privacy | Offline totale | Cloud con account |
| Costo | Gratis | Abbonamento mensile |

**Vantaggio Noesis**: self-contained, gratuito, offline totale.
**Svantaggio**: nessuna spaced repetition, nessuna integrazione diretta con Notion/Obsidian.

---

### Categoria 5 — Editor di Documenti
*Microsoft Word, Google Docs, LibreOffice Writer*

| Dimensione | Noesis Editor (sn56.x) | Editor documenti |
|---|---|---|
| Scopo | Studio da EPUB | Scrittura generale |
| Import da EPUB | Diretto | Non supportato |
| Versioning contenuto | Snapshot su filesystem | Cronologia revisioni |
| Collaborazione | Assente | Google Docs |
| Export | 7 formati doc | Multipli |
| Costo | Gratis | Microsoft 365 a pagamento |
| Offline | Totale | Parziale (Google Docs) |

**Vantaggio Noesis**: editor integrato nel flusso lettura — nessun copia-incolla tra app.

---

## Punti di Forza — Analisi Funzione per Funzione

### 1. Lettura Multilingue senza API Esterne

**Problema**: i reader con traduzione usano API di terze parti (Google Translate, DeepL) con costi, limiti di caratteri e invio dati a server esterni.

**Soluzione**: sfrutta la traduzione nativa del browser (Chrome Translate, Firefox Translation, Edge Translator). Zero costi, zero invio dati, zero limiti.

**Punto unico**: nessun reader EPUB concorrente offre traduzione gratuita e illimitata con questo livello di privacy.

---

### 2. Sistema di Raccolta Chunk

**Problema**: evidenziare è passivo — le evidenziazioni rimangono nel libro senza diventare documento.

**Soluzione**: il sistema chunk raccoglie attivamente testo, immagini e tabelle in collezione strutturata. Esportabili come JSON (backup, condivisione), importabili nell'editor (sn56.x).

**Punto unico**: il flusso lettura → raccolta → documento è completamente integrato, senza applicazioni esterne.

---

### 3. Estrazione Capitoli con Gerarchia Automatica

**Problema**: estrarre un capitolo EPUB significa copiare manualmente testo perdendo immagini, formattazione e struttura.

**Soluzione**: l'estrattore comprende la gerarchia TOC. Un click estrae un capitolo singolo oppure l'intero ramo (capitolo + tutti i sottolivelli annidati), ottenendo documento HTML standalone con immagini base64 inline e toolbar di studio completa.

**Punto unico**: nessun altro reader EPUB offre estrazione gerarchica con assemblaggio automatico di sezioni annidate.

---

### 4. Sistema di Versioning a Snapshot su Filesystem

**Problema**: il lavoro di studio su un capitolo estratto non è mai recuperabile se modificato. Non esiste "torna alla versione precedente" nei reader EPUB.

**Soluzione v810**: il sistema Snapshot salva lo stato del documento come **file HTML su filesystem locale**, con naming schema strutturato che include libro, capitolo, timestamp e variante. Ogni snapshot è scaricato automaticamente (2 file: `clean` + `annot`). Il file `origin` è rimportabile nella Library tramite parsing dei meta tag.

**Evoluzione rispetto a v704**: in v704 gli snapshot erano salvati in IndexedDB (interni, non esportabili). In v810 sono file reali sul disco, visibili nel filesystem, portabili, archiviabili in Git o cloud storage a scelta dell'utente.

**Punto unico**: versioning del documento di studio offline, su file reali, senza cloud e senza account — più vicino al paradigma di un sistema di controllo versione che a una funzione di "salva".

---

### 5. Libreria Gerarchica come Archivio di Conoscenza

**Problema**: la libreria mostra solo i libri — per accedere al lavoro su un capitolo bisogna navigare su più livelli.

**Soluzione**: la libreria gerarchica mostra in un'unica vista l'intera struttura dell'archivio: per ogni libro, i capitoli estratti; per ogni capitolo, gli snapshot salvati con descrizione e timestamp. Click diretto su qualsiasi versione.

**Punto unico**: la libreria diventa un archivio di conoscenza navigabile, non solo catalogo di libri.

---

### 6. Editor WYSIWYG Embedded (Summernote sn56.x)

**Problema**: per creare un documento di studio da EPUB si apre Word/Google Docs, si copia testo, si rincollano immagini — operazioni manuali e time-consuming.

**Soluzione**: l'Editor sn56.x (Summernote) è parte del sistema, riceve il contenuto estratto come punto di partenza. Supporta tabelle con toolbar flottante, immagini base64 inline, chunk collection con Inspect Panel.

**Evoluzione rispetto a v704**: in v704 l'editor usava `contenteditable + execCommand` (tecnicamente deprecato). In v810, sn56.x usa Summernote 0.9.1, un editor maturo con API più robuste, embedded tramite build.py come blob URL isolato.

**Punto unico**: le immagini come base64 rendono il documento completamente autocontenuto — funziona offline, inviabile via email, nessun path rotto se spostato.

---

### 7. Zero Server, Zero Tracking, Zero Account

**Problema**: la maggior parte dei tool di lettura richiedono account, inviano dati ai server, applicano DRM, vendono dati di lettura.

**Soluzione**: architettura totalmente locale. Libri in `EpubLibraryDB`, metadati estratti in `noesisDB`, snapshot su filesystem locale. Nessun byte lascia il dispositivo.

**Punto unico**: possibile usare Noesis con materiali riservati, testi NDA o documenti personali senza rischio di data leakage.

---

### 8. Export Multiplo (7 Formati Documento + 4 Formati Collezione)

**Problema**: molti reader offrono export solo in un formato, o richiedono tool di terze parti.

**Soluzione v810**: export diretto dall'Editor (sn56.x):
- **Documento**: TXT, MD, MD+ZIP, JSON, DOCX, PDF
- **Collezione chunk**: JSON, HTML, MD, MD+ZIP

Il percorso da "libro EPUB" a "post WordPress pronto" o "documento Word condivisibile" è interamente in Noesis.

---

### 9. Excalidraw Integrato nell'Editor

**Problema**: durante la rielaborazione del testo estratto, la creazione di diagrammi o schemi visivi richiede di aprire strumenti esterni (draw.io, Figma, ecc.) e reimportare manualmente.

**Soluzione v810**: Excalidraw (fork Noesis) è accessibile direttamente dalla toolbar dell'Editor. Apre una tab dedicata per creare diagrammi, flowchart, mappe mentali e schizzi visivi. L'output (SVG o PNG) viene esportato e può essere inserito nel documento come immagine base64 inline.

**Punto unico**: workflow visivo completamente integrato nel flusso di studio — dal testo al diagramma, senza uscire dall'app.

---

### 10. Quindici Temi con Gruppi Semantici

**Problema**: la maggior parte dei reader offre 3 opzioni (bianco/seppia/scuro).

**Soluzione**: 15 temi raggruppati in 5 categorie semantiche (chiari, caldi, grigi chiari, grigi scuri, notturni), con anteprima visiva a swatches.

---

## Dove Noesis Non Compete (e lo sa)

| Area | Strumento migliore | Motivo |
|---|---|---|
| Grandi librerie (1000+ libri) | Calibre | Gestione avanzata metadati, plugin, conversione formati |
| Spaced repetition / flashcard | Anki + Readwise | Algoritmi SM2, integrazione Kindle |
| Collaborazione in tempo reale | Google Docs | Commenti, revisioni multi-utente |
| Lettura mobile ottimizzata | Moon+ Reader | Touch, rotazione, luminosità adattiva |
| DRM books | Adobe Digital Editions | Standard per ebook con DRM |
| Integrazione PKM (Notion/Obsidian) | Readwise | Sincronizzazione diretta |

---

## Il Pubblico Ideale

Noesis è costruito per chi:

1. **Legge per studiare o creare**, non solo per piacere
2. **Rispetta la propria privacy**, non vuole i propri libri su server di terzi
3. **Lavora su desktop/laptop**, dove la produzione di documenti è naturale
4. **Vuole tornare a versioni precedenti** del proprio lavoro senza dipendenza da cloud
5. **Legge in più lingue** o vuole avvicinarsi a testi stranieri
6. **Vuole uno strumento gratuito** senza abbonamenti o account
7. **Apprezza la semplicità tecnica**: un file HTML, zero installazioni

---

## Sintesi del Posizionamento

Noesis occupa il quadrante **studio + privacy locale**: area poco presidiata dove lettura, annotazione, estrazione, versioning e produzione di documenti avvengono interamente lato client, senza dipendere da nessun servizio esterno.

Con v810, il sistema Snapshot su filesystem e l'editor sn56.x (Summernote) rafforzano ulteriormente questo posizionamento: Noesis non è più solo un reader con strumenti di studio, ma un **archivio di conoscenza personale** dove ogni libro porta con sé la storia del proprio lavoro di lettura — sotto forma di file reali, portabili, indipendenti da qualsiasi piattaforma.

---

*Noesis non è per tutti. È per chi capisce il valore di uno strumento che ti rispetta come lettore e come creatore di conoscenza.*
