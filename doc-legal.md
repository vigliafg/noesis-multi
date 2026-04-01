# Analisi Legale — Privacy e Copyright

> Versione: **v810** | Diritto alla copia privata, GDPR, uso legale dei contenuti EPUB, traduzione browser e licenza MIT

---

## Premessa

Noesis è costruito sul principio fondamentale che **tutto avviene localmente, sul dispositivo dell'utente**. Questo allineamento strutturale supporta diritti riconosciuti legalmente: copia privata, rielaborazione personale e privacy della lettura. L'architettura non richiede violazioni normative.

*Le considerazioni seguenti sono di carattere generale e informativo. Per valutazioni specifiche alla propria situazione, consultare un professionista legale qualificato nella propria giurisdizione.*

---

## 1. Copyright e Diritto alla Copia Privata

### Il Principio della Copia Privata

| Giurisdizione | Norma | Contenuto |
|---|---|---|
| Italia | L. 633/1941, art. 71-sexies | Riproduzione privata su qualsiasi supporto per uso esclusivamente personale senza scopo di lucro |
| Unione Europea | Direttiva 2001/29/CE, art. 5.2.b | Eccezioni per riproduzioni da persona fisica per uso privato |
| USA | 17 U.S.C. § 107 – Fair Use | Uso personale non commerciale ammesso |
| UK | CDPA 1988, s. 28B | Copia privata per uso personale esplicitamente autorizzata |

### Noesis Non Copia, Distribuisce o Condivide Contenuti Protetti

- Nessuna trasmissione di contenuti a server esterni
- File EPUB rimane in `EpubLibraryDB` (IndexedDB locale)
- Database `noesisDB` completamente locale
- Snapshot salvati su filesystem locale dell'utente (v810)
- Nessuna funzionalità di condivisione peer-to-peer
- Nessun backup remoto o sincronizzazione cloud
- Non aggira sistemi DRM; file protetti non sono compatibili

### Annotazioni, Estratti e Snapshot come Uso Trasformativo

- Gli estratti non sostituiscono l'opera originale
- Inseriti in contesto di studio personale
- Non distribuiti pubblicamente
- Finalità didattica, non commerciale
- Gli snapshot conservano il **lavoro intellettuale dell'utente**, non una copia dell'opera

**Nota v810**: il salvataggio degli snapshot come file HTML locali (anziché solo in IndexedDB) non cambia l'analisi legale — i file rimangono sul dispositivo dell'utente, con le stesse garanzie della copia privata su supporto locale.

---

## 2. Traduzione nel Browser

### Come Funziona

Noesis non integra motori di traduzione proprietari, non chiama API esterne. Utilizza la **funzione di traduzione nativa del browser** (Chrome Translate, Firefox Translation, Edge Translator). Il testo viene processato localmente o tramite i servizi di traduzione già configurati dall'utente nel browser — non da Noesis.

### Legalità della Traduzione Personale

La distinzione giuridica fondamentale separa **traduzione privata** (non richiede autorizzazione) da **pubblicazione di una traduzione** (richiede autorizzazione dell'autore).

Funzionalmente equivalente a usare un dizionario o un servizio di traduzione automatica per capire un testo in lingua straniera — pratica universalmente accettata e non soggetta a restrizioni legali per uso personale.

### Diritto di Traduzione dell'Autore

Il diritto esclusivo di traduzione (art. 4 L. 633/1941; Convenzione di Berna, art. 8) riguarda **pubblicazione e distribuzione**. L'uso privato non configura violazione.

---

## 3. Produzione Locale di Documentazione e Versioning

### Proprietà del Documento

Tutto ciò che viene prodotto con Noesis (appunti, PDF, DOCX, MD, JSON, collezioni, snapshot) è **documento creato dall'utente**, non copia dell'opera originale. Contiene:

- Evidenziazioni e selezioni dell'utente
- Struttura e organizzazione personale
- Annotazioni e note proprie
- Eventualmente citazioni brevi in contesto di analisi (diritto di citazione)

### Gli Snapshot

Gli snapshot (v810: file HTML locali `noesis-clean-*.html`, `noesis-annot-*.html`) rappresentano istantanee del **lavoro personale di studio** dell'utente su quel capitolo estratto. Funzionalmente equivalenti a salvare versioni successive di file di appunti su disco locale. Rientrano pienamente nelle condizioni di copia privata.

### L'Export Non È Distribuzione

Esportare un PDF di appunti personali è equivalente a:
- Fotocopiare pagine per uso personale
- Trascrivere citazioni su un quaderno
- Preparare dispense personali

### Immagini Inline (Base64)

Le immagini convertite in base64 durante l'estrazione rientrano nella logica di copia privata: riprodotte dall'utente, per l'utente, sul dispositivo dell'utente, senza distribuzione.

---

## 4. Privacy e Protezione dei Dati Personali

### Zero Raccolta di Dati — Conformità by Design

Non esiste server Noesis, database remoto, sistema di analytics, sistema di login. L'assenza di trasmissione dati elimina la necessità di protezione lato server. Corrisponde al modello **privacy by design** riconosciuto dal GDPR (Regolamento UE 2016/679, art. 25).

### Conformità GDPR

| Requisito GDPR | Situazione Noesis |
|---|---|
| Base giuridica trattamento | Non applicabile — nessun trattamento |
| Consenso informato | Non richiesto — nessun dato raccolto |
| Diritto all'oblio | Automatico — l'utente cancella dal browser |
| Portabilità dati | N/A — i dati non escono dal dispositivo |
| Trasferimento extra-UE | Non applicabile — nessun trasferimento |
| DPO | Non applicabile |

L'utente è unico titolare dei propri dati con controllo completo.

### Dati di Lettura e Studio Restano Privati

- Nessuna piattaforma sa cosa stai leggendo
- Nessuna piattaforma sa cosa stai studiando
- Nessun algoritmo costruisce un profilo delle abitudini di lettura
- Nessun dato venduto ad advertiser
- Nessuna autorità può richiedere i dati (Noesis non li ha)

Questo tutela concretamente la **libertà intellettuale** riconosciuta dalla Dichiarazione Universale dei Diritti Umani (art. 19) e dalla Carta dei Diritti Fondamentali UE (art. 11).

### Storage Locale

| Store | Contenuto | Cancellazione |
|-------|-----------|---------------|
| `EpubLibraryDB` (IndexedDB) | File `.epub` completi, posizioni lettura, segnalibri | Impostazioni browser → Cancella dati di navigazione |
| `noesisDB` (IndexedDB) | Metadati capitoli estratti, lista snapshot | Impostazioni browser → Cancella dati di navigazione |
| `localStorage` | Preferenze tipografiche, tema, impostazioni UI | Impostazioni browser → Cancella dati di navigazione |
| Filesystem locale | File snapshot HTML, export documenti | Cancellazione file manuale dall'utente |

---

## 5. Nessuna Violazione di Termini di Servizio di Terze Parti

### Nessuna Connessione a Piattaforme Terze

Noesis lavora con file `.epub` che l'utente possiede indipendentemente. Non interagisce con Kindle Cloud Reader, Kobo Web o piattaforme analoghe. Nessun termine di servizio di piattaforme terze viene violato.

### Librerie CDN — Uso nei Termini di Licenza

| Libreria | Licenza | Utilizzo in Noesis |
|---|---|---|
| epub.js | BSD 2-Clause | Parsing/rendering EPUB |
| JSZip | MIT / GPLv3 | Decompressione EPUB e packaging ZIP |
| Bootstrap Icons | MIT | Icone SVG |
| Summernote | MIT | Editor WYSIWYG (sn56.x) |
| jQuery | MIT | DOM manipulation (sn56.x) |
| Turndown | MIT | Export Markdown (sn56.x) |
| html-docx-js | MIT | Export DOCX (sn56.x) |

Tutte le dipendenze hanno licenze permissive compatibili con applicazione distribuita sotto MIT.

---

## 6. Licenza MIT di Noesis: Diritti dell'Utente

La licenza MIT consente:

- Libertà di uso (personale o commerciale)
- Libertà di copia (quante volte necessario)
- Libertà di modifica (codice sorgente accessibile)
- Libertà di distribuzione (con nota copyright)
- Nessun obbligo di pagamento (canone, abbonamento, scadenza)
- Nessun obbligo di account (nessuna registrazione)

Unico requisito: mantenere la nota copyright nelle copie o distribuzioni sostanziali. Per uso personale non si applica nemmeno questo vincolo.

---

## 7. Sintesi: Perché Noesis è Legale per Uso Personale

| Aspetto | Situazione Legale | Motivo |
|---|---|---|
| Lettura EPUB posseduti legittimamente | Pienamente legale | Esercizio del diritto di proprietà sul file acquistato |
| Traduzione per uso personale | Pienamente legale | Distinzione tra traduzione privata e pubblicazione |
| Evidenziazione e annotazione | Pienamente legale | Pratica di studio tradizionale |
| Estrazione capitoli per uso personale | Pienamente legale | Copia privata (art. 71-sexies L. 633/1941) |
| Snapshot del lavoro di studio (file locali) | Pienamente legale | Copia privata locale; conservazione del lavoro intellettuale dell'utente |
| Raccolta citazioni per studio | Pienamente legale | Diritto di citazione e uso trasformativo |
| Produzione documenti di studio | Pienamente legale | Opera derivata personale, non distribuita |
| Export PDF/DOCX/MD per uso personale | Pienamente legale | Copia privata su supporto diverso |
| Assenza DRM bypass | Nessun rischio | Noesis non supporta file con DRM |
| Privacy dati (libri + snapshot locali) | Massima tutela | Nessun dato trasmesso, privacy by design |
| Conformità GDPR | Automatica | Nessun trattamento di dati personali |
| Licenza software | MIT | Uso libero senza restrizioni |

---

## 8. Cosa l'Utente Deve Tenere Presente

**L'utente dovrebbe**:
- Usare Noesis con file EPUB che possiede o ha diritto di usare (acquistati, open access, dominio pubblico, Creative Commons)
- Tenere i documenti prodotti per uso personale o, se condivisi, verificare la conformità al diritto di citazione
- Non usare Noesis per aggirare protezioni DRM (cosa che tecnicamente non supporta)

**L'utente non deve preoccuparsi di**:
- Leggere libri in lingue straniere con traduzione browser
- Evidenziare, annotare e raccogliere passaggi per studi propri
- Estrarre capitoli per appunti personali
- Salvare snapshot del proprio lavoro di studio come file locali
- Esportare documenti di studio in qualsiasi formato per uso proprio
- Condividere i propri appunti (non il libro) con colleghi nel rispetto del diritto di citazione

---

## Conclusione

Noesis è progettato architetturalmente e funzionalmente per rispettare il quadro legale esistente — sia a tutela dei titolari dei diritti d'autore sia degli utenti finali.

L'architettura completamente locale, estesa in v810 al versioning degli appunti tramite snapshot su filesystem, è una scelta etica e giuridica che posiziona Noesis dal lato del lettore, nel rispetto delle leggi.

Il diritto di leggere, comprendere, annotare, studiare e conservare la storia del proprio lavoro intellettuale — senza sorveglianza, senza data mining, senza dipendenza da piattaforme commerciali — è un diritto fondamentale che Noesis esercita concretamente.
