# Implementazione i18n v812 — IT / FR / ES / DE

Questo documento guida l'applicazione delle stesse modifiche già fatte nella sezione `en:` di `translations.js` per le sezioni **IT** (righe 1128–2213), **FR** (righe 2214–3315), **ES** (righe 3316–4444), **DE** (righe 4445–fine).

**Termini tecnici da mantenere invariati in tutte le lingue:**
`Library`, `TOC`, `Navigate`, `Annotate`, `Extract`, `Display`, `Bookmarks`, `Help`, `EpubLibraryDB`, `noesisDB`, `CFI`, `Themes ▾`

---

## Come applicare le modifiche

Per ogni lingua, trovare la chiave nella sezione corrispondente e sostituire il valore con il testo proposto. Le righe indicate si riferiscono allo stato attuale del file (potrebbero variare di poche unità dopo le modifiche EN già applicate).

---

## 1. Sezione IT (riga ~1128)

### footer.license (riga 1157)
```
DA: 'MIT License · Vanilla JS · No Server · Noesis — Reading-to-Knowledge System · v810',
A:  'MIT License · Vanilla JS · No Server · Noesis — Reading-to-Knowledge System · v812',
```

### index.hero.badge (riga 1174)
```
DA: 'v810 · Reading-to-Knowledge System',
A:  'v812 · Reading-to-Knowledge System',
```

### index.img.readerbtn / index.img.readerbtn.caption (righe 1233–1234)
```
DA: 'Toolbar Noesis Reading',
A:  'Menubar Noesis Reading',

DA: '← Library · Sidebar · Segnalibri · Highlight (giallo) · Display · Scroll · % · Save State (arancio) · Extract Chapter (verde) · ?',
A:  'Library · TOC · Segnalibri · Display · Navigate [Page/Scroll] · Annotate · Extract · Help',
```

### index.card.sidebar.h / .p (righe 1235–1236)
```
DA: 'Toggle Sidebar',
A:  'TOC',

DA: 'Mostra/nasconde il TOC gerarchico espandibile fino a 3 livelli.',
A:  'Apre/chiude il pannello TOC dalla menubar del reader. Supporta fino a 3 livelli di annidamento.',
```

### index.callout.snapshot (riga 1245)
```
DA: '<strong>v810 — Save Snapshot su filesystem</strong> — ...',
A:  '<strong>v812 — Save Snapshot su filesystem</strong> — ...',
```

### index.download.badge (riga 1294)
```
DA: 'v810 · MIT License · Vanilla JS',
A:  'v812 · MIT License · Vanilla JS',
```

### guida.hero.p (riga 1339)
```
DA: '... con le funzioni aggiornate v810.',
A:  '... con le funzioni aggiornate v812.',
```

### guida.card.sidebar.h / .p (righe 1359–1360)
```
DA: 'Sidebar TOC',
A:  'TOC',

DA: 'Clicca il pulsante Sidebar per aprire l\'indice gerarchico espandibile. Clicca un capitolo per navigarci direttamente.',
A:  'Clicca <strong>TOC</strong> nella menubar per aprire l\'indice gerarchico espandibile. Clicca un capitolo per navigarci direttamente.',
```

### guida.card.highlight.p (riga ~1363) — se presente
```
DA: '... scegli il colore nel dropdown Highlight: ...',
A:  '... fai clic su <strong>Annotate</strong> nella menubar per attivare la modalità annotazione e scegli il colore: ...',
```

### guida.card.savestate.h / .p (righe 1365–1366)
```
DA: 'Save State',
A:  'Salvataggio automatico',

DA: 'Clicca <strong>Save State</strong> per salvare posizione + tutte le preferenze associate a quel libro.',
A:  'La posizione di lettura viene salvata automaticamente ogni 3 secondi. Le impostazioni Display (tema, tipografia) vengono salvate per ogni libro tramite un prompt floating che appare alla chiusura del pannello Display dopo modifiche.',
```

### guida.f4.p (riga 1379)
```
DA: '... funzioni più potenti della v810. ...',
A:  '... funzioni più potenti della v812. ...',
```

### library.btn.theme.h / .p (righe 1485–1486)
```
DA: 'Toggle Theme',
A:  'Themes ▾',

DA: 'Alterna tra il tema chiaro e il tema scuro della Library. La preferenza viene salvata in localStorage e ripristinata al prossimo avvio.',
A:  'Apre un dropdown per selezionare il tema della Library: <strong>Light</strong> o <strong>Dark</strong>. La selezione viene applicata immediatamente e salvata in localStorage.',
```

### reading.toolbar.label / .h2 / .p (righe 1515–1517)
```
DA: 'Toolbar',
A:  'Menubar',

DA: 'La bottoniera del <em>Reader</em>',
A:  'La <em>menubar</em> del Reader',

DA: 'La toolbar del Noesis Reading raccoglie tutti gli strumenti di lettura e annotazione. È sempre visibile in cima allo schermo.',
A:  'La menubar del Noesis Reading raccoglie tutti i controlli di lettura e annotazione. È sempre visibile in cima allo schermo.',
```

### reading.img.buttons / .caption (righe 1518–1519)
```
DA: 'Bottoniera Noesis Reading',
A:  'Menubar Noesis Reading',

DA: '← Library · Sidebar · Segnalibri · Highlight (giallo) · Display · Scroll · % · Save State (arancio) · Extract Chapter (verde) · ?',
A:  'Library · TOC · Segnalibri · Display · Navigate [Page] · Annotate · Extract · Help',
```

### reading.btn.library.h / .p (righe 1520–1521)
```
DA: '← Library',
A:  'Library',

DA: 'Torna alla Noesis Library senza perdere lo stato del libro corrente. La posizione viene ripristinata alla prossima apertura tramite Save State.',
A:  'Torna alla Noesis Library. La posizione di lettura viene salvata automaticamente ogni 3 secondi — nessuna azione manuale richiesta.',
```

### reading.btn.sidebar.h / .p (righe 1522–1523)
```
DA: 'Sidebar',
A:  'TOC',

DA: 'Apre/chiude il TOC gerarchico espandibile. ...',
A:  'Apre/chiude il pannello dell\'indice gerarchico (Table of Contents). Supporta fino a 3 livelli di annidamento. Clicca una voce per navigare direttamente a quella sezione.',
```

### reading.btn.highlight.h / .p (righe 1526–1527)
```
DA: 'Highlight',
A:  'Annotate',

DA: 'Dropdown con 3 colori: ...',
A:  'Attiva o disattiva la modalità annotazione. Quando attiva, il testo selezionato viene evidenziato con il colore scelto. Il selettore colori (Giallo / Verde / Rosa) è accessibile nel pannello annotazioni. Gli highlight sono CFI-based e sopravvivono al ricaricamento della pagina.',
```

### reading.btn.scroll.h / .p (righe 1530–1531)
```
DA: 'Modalità scroll',
A:  'Navigate',

DA: 'Alterna tra modalità paginata e scorrimento continuo. In modalità paginata, usa i tasti freccia o swipe per girare pagina.',
A:  'Apre un dropdown per passare tra <strong>Modalità Pagina</strong> e <strong>Modalità Scroll</strong>. Un badge mostra sempre la modalità attiva: Navigate [Page] o Navigate [Scroll]. Cambiando modalità il rendition viene ricreato immediatamente.',
```

### reading.btn.extract.h / .p (righe 1536–1537)
```
DA: 'Extract Chapter',
A:  'Extract',

DA: 'Pulsante principale di estrazione. Dropdown con due opzioni: solo capitolo corrente, o corrente + tutti i sottolivelli. Apre Noesis Editor in un nuovo tab con il contenuto già caricato.',
A:  'Dropdown di estrazione: solo capitolo corrente, o corrente + tutti i sottolivelli. Apre Noesis Editor in un nuovo tab con il contenuto già caricato.',
```

### reading.modes.p (riga 1540)
```
DA: '... con il pulsante Scroll nella toolbar.',
A:  '... tramite <strong>Navigate</strong> nella menubar.',
```

### reading.display.tip (riga 1579)
```
DA: '... tramite il pulsante <strong>Save State</strong>. ...',
A:  '... tramite il prompt floating che appare alla chiusura del pannello Display dopo aver apportato modifiche. ...',
```

### reading.bookmark.create.p (riga 1600)
```
DA: 'Clicca il pulsante <strong>🔖 Segnalibri</strong> nella toolbar → ...',
A:  'Clicca <strong>Bookmarks</strong> nella menubar → ...',
```

### reading.savestate.h2 / .p (righe 1608–1609)
```
DA: 'Save State — <em>salva tutto</em>',
A:  'Salvataggio automatico — <em>sempre sincronizzato</em>',

DA: 'Il pulsante <strong>💾 Save State</strong> salva manualmente la posizione di lettura corrente ...',
A:  'La posizione di lettura viene salvata <strong>automaticamente ogni 3 secondi</strong> senza alcuna azione dell\'utente. Le impostazioni Display (tema, tipografia, layout) vengono salvate per ogni libro tramite un prompt floating che appare per 8 secondi alla chiusura del pannello Display dopo modifiche.',
```

### reading.savestate.what.p (riga 1611)
```
DA: 'Posizione CFI esatta nel testo, font size, line height, modalità pagina (singola/doppia), tema di lettura, colori interfaccia e modalità scroll.',
A:  'Posizione: auto-salvata ogni 3 secondi (CFI dell\'elemento al centro visivo del reader). Impostazioni Display: font size, line height, modalità pagina (singola/doppia), tema di lettura, colori interfaccia e modalità scroll — salvate su richiesta tramite il prompt Display.',
```

### reading.savestate.perbook.p (riga 1613)
```
DA: '... in <code>noesisLibraryDB</code>. ...',
A:  '... in <code>EpubLibraryDB</code>. ...',
```

### reading.extract.p (riga 1656)
```
DA: 'Il pulsante Extract Chapter nella toolbar apre un dropdown ...',
A:  'Il pulsante Extract nella menubar apre un dropdown ...',
```

---

## 2. Sezione FR (riga ~2214)

### footer.license (riga 2243)
```
DA: '... · v810',
A:  '... · v812',
```

### index.hero.badge (riga 2262)
```
DA: 'v810 · Reading-to-Knowledge System',
A:  'v812 · Reading-to-Knowledge System',
```

### index.img.readerbtn / .caption (righe 2321–2322)
```
DA: 'Barre d\'outils Noesis Reading',
A:  'Barre de menu Noesis Reading',

DA: '← Library · Sidebar · Signets · Surlignage (jaune) · Affichage · Défilement · % · Save State (orange) · Extraire chapitre (vert) · ?',
A:  'Library · TOC · Signets · Affichage · Navigate [Page/Scroll] · Annotate · Extract · Help',
```

### index.card.sidebar.h / .p (righe 2323–2324)
```
DA: 'Basculer la Sidebar',
A:  'TOC',

DA: 'Affiche/masque la table des matières hiérarchique développable jusqu\'à 3 niveaux.',
A:  'Ouvre/ferme le panneau TOC depuis la barre de menu du lecteur. Prend en charge jusqu\'à 3 niveaux d\'imbrication.',
```

### index.callout.snapshot (riga 2333)
```
DA: '<strong>v810 — Sauvegarder un instantané ...</strong>',
A:  '<strong>v812 — Sauvegarder un instantané ...</strong>',
```

### index.download.badge (riga 2382)
```
DA: 'v810 · MIT License · Vanilla JS',
A:  'v812 · MIT License · Vanilla JS',
```

### guida.hero.p (riga 2429)
```
DA: '... avec les fonctionnalités mises à jour v810.',
A:  '... avec les fonctionnalités mises à jour v812.',
```

### guida.card.sidebar.h / .p (righe 2449–2450)
```
DA: 'Sidebar TOC',
A:  'TOC',

DA: 'Cliquez sur le bouton Sidebar pour ouvrir l\'index hiérarchique développable. Cliquez sur un chapitre pour y naviguer directement.',
A:  'Cliquez sur <strong>TOC</strong> dans la barre de menu pour ouvrir l\'index hiérarchique développable. Cliquez sur un chapitre pour y naviguer directement.',
```

### guida.card.savestate.h / .p (righe 2455–2456)
```
DA: 'Save State',
A:  'Sauvegarde automatique',

DA: 'Cliquez sur <strong>Save State</strong> pour sauvegarder la position + toutes les préférences associées à ce livre.',
A:  'La position de lecture est sauvegardée automatiquement toutes les 3 secondes. Les paramètres d\'affichage (thème, typographie) sont sauvegardés par livre via un bandeau flottant qui apparaît à la fermeture du panneau Affichage après des modifications.',
```

### guida.f4.p (riga 2469)
```
DA: '... fonctionnalités les plus puissantes de la v810. ...',
A:  '... fonctionnalités les plus puissantes de la v812. ...',
```

### library.btn.theme.h / .p (righe 2577–2578)
```
DA: 'Basculer le thème',
A:  'Themes ▾',

DA: 'Bascule entre le thème clair et sombre de la Library. La préférence est sauvegardée dans localStorage et restaurée au prochain lancement.',
A:  'Ouvre un menu déroulant pour sélectionner le thème de la Library : <strong>Light</strong> ou <strong>Dark</strong>. La sélection s\'applique immédiatement et est sauvegardée dans localStorage.',
```

### reading.toolbar.label / .h2 / .p (righe 2609–2611)
```
DA: 'Barre d\'outils',
A:  'Barre de menu',

DA: 'La barre de boutons du <em>Reader</em>',
A:  'La <em>barre de menu</em> du Reader',

DA: 'La barre d\'outils de Noesis Reading regroupe tous les outils de lecture et d\'annotation. Elle est toujours visible en haut de l\'écran.',
A:  'La barre de menu de Noesis Reading regroupe tous les contrôles de lecture et d\'annotation. Elle est toujours visible en haut de l\'écran.',
```

### reading.img.buttons / .caption (righe 2612–2613)
```
DA: 'Barre de boutons Noesis Reading',
A:  'Barre de menu Noesis Reading',

DA: '← Library · Sidebar · Signets · Surlignage (jaune) · Affichage · Défilement · % · Save State (orange) · Extract Chapter (vert) · ?',
A:  'Library · TOC · Signets · Affichage · Navigate [Page] · Annotate · Extract · Help',
```

### reading.btn.library.h / .p (righe 2614–2615)
```
DA: '← Library',
A:  'Library',

DA: 'Retourne à Noesis Library sans perdre l\'état du livre courant. La position est restaurée à la prochaine ouverture via Save State.',
A:  'Retourne à Noesis Library. La position de lecture est sauvegardée automatiquement toutes les 3 secondes — aucune action manuelle requise.',
```

### reading.btn.sidebar.h / .p (righe 2616–2617)
```
DA: 'Sidebar',
A:  'TOC',

DA: 'Ouvre/ferme la TOC hiérarchique développable. ...',
A:  'Ouvre/ferme le panneau de la table des matières hiérarchique. Prend en charge jusqu\'à 3 niveaux d\'imbrication. Cliquez sur une entrée pour naviguer directement vers cette section.',
```

### reading.btn.highlight.h / .p (righe 2620–2621)
```
DA: 'Surlignage',
A:  'Annotate',

DA: 'Menu déroulant avec 3 couleurs : ...',
A:  'Active ou désactive le mode annotation. Lorsqu\'il est actif, le texte sélectionné est mis en évidence avec la couleur choisie. Le sélecteur de couleur (Jaune / Vert / Rose) est accessible dans le panneau d\'annotation. Les surlignages sont basés sur CFI et survivent au rechargement.',
```

### reading.btn.scroll.h / .p (righe 2624–2625)
```
DA: 'Mode défilement',
A:  'Navigate',

DA: 'Bascule entre mode paginé et défilement continu. En mode paginé, utilisez les touches fléchées ou le swipe pour tourner les pages.',
A:  'Ouvre un menu déroulant pour basculer entre <strong>Mode Page</strong> et <strong>Mode Défilement</strong>. Un badge indique toujours le mode actif : Navigate [Page] ou Navigate [Scroll]. Changer de mode recrée le rendu immédiatement.',
```

### reading.btn.extract.h / .p (righe 2630–2631)
```
DA: 'Extract Chapter',
A:  'Extract',

DA: 'Bouton principal d\'extraction. Menu déroulant avec deux options : chapitre courant seulement, ou courant + tous les sous-niveaux. ...',
A:  'Menu déroulant d\'extraction : chapitre courant seulement, ou courant + tous les sous-niveaux. Ouvre Noesis Éditeur dans un nouvel onglet avec le contenu déjà chargé.',
```

### reading.modes.p (riga 2634)
```
DA: '... avec le bouton Défilement dans la barre d\'outils.',
A:  '... via <strong>Navigate</strong> dans la barre de menu.',
```

### reading.display.tip (riga 2673)
```
DA: '... via le bouton <strong>Save State</strong>. ...',
A:  '... via le bandeau flottant qui apparaît à la fermeture du panneau Affichage après des modifications. ...',
```

### reading.bookmark.create.p (riga 2694)
```
DA: 'Cliquez sur le bouton <strong>🔖 Signets</strong> dans la barre d\'outils → ...',
A:  'Cliquez sur <strong>Bookmarks</strong> dans la barre de menu → ...',
```

### reading.savestate.h2 / .p (righe 2702–2703)
```
DA: 'Save State — <em>tout sauvegarder</em>',
A:  'Sauvegarde automatique — <em>toujours synchronisé</em>',

DA: 'Le bouton <strong>💾 Save State</strong> sauvegarde manuellement la position de lecture courante ...',
A:  'La position de lecture est sauvegardée <strong>automatiquement toutes les 3 secondes</strong> sans aucune action de l\'utilisateur. Les paramètres d\'affichage (thème, typographie, mise en page) sont sauvegardés par livre via un bandeau flottant qui apparaît 8 secondes à la fermeture du panneau Affichage après des modifications.',
```

### reading.savestate.what.p (riga 2705)
```
DA: 'Position CFI exacte dans le texte, taille de police, ...',
A:  'Position : sauvegardée automatiquement toutes les 3 secondes (CFI de l\'élément au centre visuel du lecteur). Paramètres d\'affichage : taille de police, hauteur de ligne, mode de page (unique/double), thème de lecture, couleurs d\'interface et mode de défilement — sauvegardés à la demande via le bandeau Affichage.',
```

### reading.savestate.perbook.p (riga 2707)
```
DA: '... dans <code>noesisLibraryDB</code>. ...',
A:  '... dans <code>EpubLibraryDB</code>. ...',
```

### reading.extract.p (riga 2750)
```
DA: 'Le bouton Extract Chapter dans la barre d\'outils ouvre un menu déroulant ...',
A:  'Le bouton Extract dans la barre de menu ouvre un menu déroulant ...',
```

---

## 3. Sezione ES (riga ~3316)

### footer.license (riga 3345)
```
DA: '... · v810',
A:  '... · v812',
```

### index.hero.badge (riga 3354)
```
DA: 'v810 · Reading-to-Knowledge System',
A:  'v812 · Reading-to-Knowledge System',
```

### index.img.readerbtn / .caption (righe 3596–3597)
```
DA: 'Toolbar de lectura de Noesis',
A:  'Barra de menú de lectura de Noesis',

DA: '← Biblioteca · Sidebar · Marcadores · Resaltado (amarillo) · Display · Scroll · % · Guardar Estado (naranja) · Extraer Capítulo (verde) · ?',
A:  'Library · TOC · Marcadores · Display · Navigate [Page/Scroll] · Annotate · Extract · Help',
```

### index.card.sidebar.h / .p (righe 3598–3599)
```
DA: 'Alternar Sidebar',
A:  'TOC',

DA: 'Muestra/oculta el TOC jerárquico expandible hasta 3 niveles.',
A:  'Abre/cierra el panel TOC desde la barra de menú del lector. Soporta hasta 3 niveles de anidación.',
```

### index.callout.snapshot (riga 3608)
```
DA: '<strong>v810 — Guardar Instantáneo ...</strong>',
A:  '<strong>v812 — Guardar Instantáneo ...</strong>',
```

### index.download.badge (righe 3400 e 3543 — duplicato, verificare)
```
DA: 'v810 · Licencia MIT · Vanilla JS',
A:  'v812 · Licencia MIT · Vanilla JS',
```
> Nota: in ES esistono due occorrenze di `index.download.badge` (righe 3400 e 3543). Aggiornare entrambe.

### guida.hero.p (riga 3447)
```
DA: '... con características v810 actualizadas.',
A:  '... con características v812 actualizadas.',
```

### guida.card.sidebar.h / .p (righe 3467–3468)
```
DA: 'TOC Lateral',
A:  'TOC',

DA: 'Clic en el botón Sidebar para abrir el índice jerárquico expandible. Clic en un capítulo para navegar directamente.',
A:  'Clic en <strong>TOC</strong> en la barra de menú para abrir el índice jerárquico expandible. Clic en un capítulo para navegar directamente.',
```

### guida.card.savestate.h / .p (righe 3473–3474)
```
DA: 'Guardar Estado',
A:  'Guardado automático',

DA: 'Clic en <strong>Guardar Estado</strong> para guardar posición + todas las preferencias asociadas a ese libro.',
A:  'La posición de lectura se guarda automáticamente cada 3 segundos. La configuración de pantalla (tema, tipografía) se guarda por libro mediante un aviso flotante que aparece al cerrar el panel Pantalla tras realizar cambios.',
```

### guida.f4.p (riga 3487)
```
DA: '... más poderosas de v810. ...',
A:  '... más poderosas de v812. ...',
```

### library.btn.theme.h / .p (righe 3707–3708)
```
DA: 'Cambiar Tema',
A:  'Themes ▾',

DA: 'Alterna entre el tema claro y oscuro de la Biblioteca. La preferencia se guarda en localStorage y se restaura en el próximo lanzamiento.',
A:  'Abre un menú desplegable para seleccionar el tema de la Biblioteca: <strong>Light</strong> o <strong>Dark</strong>. La selección se aplica inmediatamente y se guarda en localStorage.',
```

### reading.toolbar.label / .h2 / .p (righe 3737–3739)
```
DA: 'Toolbar',
A:  'Barra de menú',

DA: 'La botonera del <em>Lector</em>',
A:  'La <em>barra de menú</em> del Lector',

DA: 'La toolbar de Noesis Lectura reúne todas las herramientas de lectura y anotación. Siempre es visible en la parte superior de la pantalla.',
A:  'La barra de menú de Noesis Lectura reúne todos los controles de lectura y anotación. Siempre es visible en la parte superior de la pantalla.',
```

### reading.img.buttons / .caption (righe 3740–3741)
```
DA: 'Botones de lectura de Noesis',
A:  'Barra de menú de Noesis Lectura',

DA: '← Biblioteca · Sidebar · Marcadores · Resaltado (amarillo) · Display · Scroll · % · Guardar Estado (naranja) · Extraer Capítulo (verde) · ?',
A:  'Library · TOC · Marcadores · Display · Navigate [Page] · Annotate · Extract · Help',
```

### reading.btn.library.h / .p (righe 3742–3743)
```
DA: '← Biblioteca',
A:  'Library',

DA: 'Regresa a Noesis Biblioteca sin perder el estado del libro actual. La posición se restaura en la próxima apertura vía Guardar Estado.',
A:  'Regresa a Noesis Library. La posición de lectura se guarda automáticamente cada 3 segundos — sin ninguna acción manual.',
```

### reading.btn.sidebar.h / .p (righe 3744–3745)
```
DA: 'Sidebar',
A:  'TOC',

DA: 'Abre/cierra el TOC jerárquico expandible. ...',
A:  'Abre/cierra el panel de la tabla de contenidos jerárquica. Soporta hasta 3 niveles de anidación. Clic en cualquier entrada para navegar directamente a esa sección.',
```

### reading.btn.highlight.h / .p (righe 3748–3749)
```
DA: 'Resaltado',
A:  'Annotate',

DA: 'Menú desplegable con 3 colores: ...',
A:  'Activa o desactiva el modo de anotación. Cuando está activo, el texto seleccionado se resalta con el color elegido. El selector de color (Amarillo / Verde / Rosa) está disponible en el panel de anotación. Los resaltados son basados en CFI y persisten al recargar.',
```

### reading.btn.scroll.h / .p (righe 3752–3753)
```
DA: 'Modo scroll',
A:  'Navigate',

DA: 'Alterna entre modo paginado y scroll continuo. ...',
A:  'Abre un menú desplegable para cambiar entre <strong>Modo Página</strong> y <strong>Modo Desplazamiento</strong>. Un indicador muestra siempre el modo activo: Navigate [Page] o Navigate [Scroll]. Cambiar de modo recrea el renderizado de inmediato.',
```

### reading.btn.extract.h / .p (righe 3758–3759)
```
DA: 'Extraer Capítulo',
A:  'Extract',

DA: 'Botón principal de extracción. Menú desplegable con dos opciones: ...',
A:  'Menú desplegable de extracción: solo capítulo actual, o actual + todos los subniveles. Abre Noesis Editor en una nueva pestaña con el contenido ya cargado.',
```

### reading.modes.p (riga 3762)
```
DA: '... con el botón Scroll en la toolbar.',
A:  '... vía <strong>Navigate</strong> en la barra de menú.',
```

### reading.display.tip (riga 3801)
```
DA: '... vía el botón <strong>Guardar Estado</strong>. ...',
A:  '... vía el aviso flotante que aparece al cerrar el panel de Pantalla tras realizar cambios. ...',
```

### reading.bookmark.create.p (riga 3822)
```
DA: 'Clic en el botón <strong>🔖 Marcadores</strong> en la toolbar → ...',
A:  'Clic en <strong>Bookmarks</strong> en la barra de menú → ...',
```

### reading.savestate.h2 / .p (righe 3830–3831)
```
DA: 'Guardar Estado — <em>guardar todo</em>',
A:  'Guardado automático — <em>siempre sincronizado</em>',

DA: 'El botón <strong>💾 Guardar Estado</strong> guarda manualmente la posición de lectura actual ...',
A:  'La posición de lectura se guarda <strong>automáticamente cada 3 segundos</strong> sin ninguna acción del usuario. La configuración de pantalla (tema, tipografía, diseño) se guarda por libro mediante un aviso flotante que aparece 8 segundos al cerrar el panel Pantalla tras realizar cambios.',
```

### reading.savestate.what.p (riga 3833)
```
DA: 'Posición CFI exacta en el texto, tamaño de fuente, ...',
A:  'Posición: guardada automáticamente cada 3 segundos (CFI del elemento en el centro visual del lector). Configuración de pantalla: tamaño de fuente, altura de línea, modo de página (simple/doble), tema de lectura, colores de interfaz y modo de scroll — guardados a petición vía el aviso de Pantalla.',
```

### reading.savestate.perbook.p (riga 3835)
```
DA: '... en <code>noesisLibraryDB</code>. ...',
A:  '... en <code>EpubLibraryDB</code>. ...',
```

### reading.extract.p (riga 3878)
```
DA: 'El botón Extraer Capítulo en la toolbar abre un menú desplegable ...',
A:  'El botón Extract en la barra de menú abre un menú desplegable ...',
```

---

## 4. Sezione DE (riga ~4445)

### footer.license (riga 4474)
```
DA: '... · v810',
A:  '... · v812',
```

### index.hero.badge (riga 4493)
```
DA: 'v810 · Reading-to-Knowledge System',
A:  'v812 · Reading-to-Knowledge System',
```

### index.img.readerbtn / .caption (righe 4552–4553)
```
DA: 'Noesis Reading Toolbar',
A:  'Noesis Reading Menüleiste',

DA: '← Bibliothek · Sidebar · Lesezeichen · Hervorhebung (gelb) · Anzeige · Scrollen · % · Status speichern (orange) · Kapitel extrahieren (grün) · ?',
A:  'Library · TOC · Lesezeichen · Anzeige · Navigate [Page/Scroll] · Annotate · Extract · Help',
```

### index.card.sidebar.h / .p (righe 4554–4555)
```
DA: 'Sidebar umschalten',
A:  'TOC',

DA: 'Zeigt/verbirgt die erweiterbare hierarchische TOC bis zu 3 Ebenen.',
A:  'Öffnet/schließt das TOC-Panel über die Menüleiste des Readers. Unterstützt bis zu 3 Verschachtelungsebenen.',
```

### index.callout.snapshot (riga 4564)
```
DA: '<strong>v810 — Snapshot ins Dateisystem speichern</strong>',
A:  '<strong>v812 — Snapshot ins Dateisystem speichern</strong>',
```

### index.download.badge (riga 4613)
```
DA: 'v810 · MIT-Lizenz · Vanilla JS',
A:  'v812 · MIT-Lizenz · Vanilla JS',
```

> Nota: La sezione DE non ha chiavi `guida.card.*` o `guida.f4.p` — queste chiavi mancanti ricadono sulla sezione EN già aggiornata. Non serve aggiungere voci DE per queste chiavi a meno che non si voglia tradurle.

### library.btn.theme.h / .p (righe 4808–4809)
```
DA: 'Theme umschalten',
A:  'Themes ▾',

DA: 'Wechselt zwischen hellem und dunklem Bibliothek-Theme. Die Präferenz wird in localStorage gespeichert und beim nächsten Start wiederhergestellt.',
A:  'Öffnet ein Dropdown zur Auswahl des Bibliothek-Themes: <strong>Light</strong> oder <strong>Dark</strong>. Die Auswahl wird sofort angewendet und in localStorage gespeichert.',
```

### reading.toolbar.label / .h2 / .p (righe 4840–4842)
```
DA: 'Toolbar',
A:  'Menüleiste',

DA: 'Die <em>Reader</em>-Buttonleiste',
A:  'Die <em>Reader</em>-Menüleiste',

DA: 'Die Noesis Reading-Toolbar sammelt alle Lese- und Annotationswerkzeuge. Sie ist immer oben auf dem Bildschirm sichtbar.',
A:  'Die Noesis Reading-Menüleiste enthält alle Lese- und Annotationssteuerelemente. Sie ist immer oben auf dem Bildschirm sichtbar.',
```

### reading.img.buttons / .caption (righe 4843–4844)
```
DA: 'Noesis Reading-Buttonleiste',
A:  'Noesis Reading-Menüleiste',

DA: '← Bibliothek · Sidebar · Lesezeichen · Hervorhebung (gelb) · Anzeige · Scrollen · % · Status speichern (orange) · Kapitel extrahieren (grün) · ?',
A:  'Library · TOC · Lesezeichen · Anzeige · Navigate [Page] · Annotate · Extract · Help',
```

### reading.btn.library.h / .p (righe 4845–4846)
```
DA: '← Bibliothek',
A:  'Library',

DA: 'Kehrt zur Noesis Bibliothek zurück, ohne den aktuellen Buchzustand zu verlieren. Position wird beim nächsten Öffnen via Status speichern wiederhergestellt.',
A:  'Kehrt zur Noesis Library zurück. Die Leseposition wird automatisch alle 3 Sekunden gespeichert — kein manuelles Eingreifen erforderlich.',
```

### reading.btn.sidebar.h / .p (righe 4847–4848)
```
DA: 'Sidebar',
A:  'TOC',

DA: 'Öffnet/schließt die erweiterbare hierarchische TOC. ...',
A:  'Öffnet/schließt das hierarchische Inhaltsverzeichnis-Panel (Table of Contents). Unterstützt bis zu 3 Verschachtelungsebenen. Klicken Sie auf einen Eintrag, um direkt zu diesem Abschnitt zu navigieren.',
```

### reading.btn.highlight.h / .p (righe 4851–4852)
```
DA: 'Hervorhebung',
A:  'Annotate',

DA: 'Dropdown mit 3 Farben: ...',
A:  'Aktiviert oder deaktiviert den Annotationsmodus. Wenn aktiv, wird der ausgewählte Text mit der gewählten Farbe hervorgehoben. Die Farbauswahl (Gelb / Grün / Rosa) ist im Annotationspanel zugänglich. Hervorhebungen basieren auf CFI und überstehen Seiten-Neuladen.',
```

### reading.btn.scroll.h / .p (righe 4855–4856)
```
DA: 'Scroll-Modus',
A:  'Navigate',

DA: 'Umschalten zwischen Seitenmodus und kontinuierlichem Scrollmodus. Im Seitenmodus Pfeiltasten oder Wischen zum Umblättern verwenden.',
A:  'Öffnet ein Dropdown zum Wechsel zwischen <strong>Seitenmodus</strong> und <strong>Scroll-Modus</strong>. Ein Badge zeigt immer den aktiven Modus: Navigate [Page] oder Navigate [Scroll]. Ein Moduswechsel erstellt den Rendition sofort neu.',
```

### reading.btn.extract.h / .p (righe 4861–4862)
```
DA: 'Kapitel extrahieren',
A:  'Extract',

DA: 'Haupt-Extraktionsbutton. Dropdown mit zwei Optionen: nur aktuelles Kapitel oder aktuell + alle Unterniveaus. ...',
A:  'Extraktions-Dropdown: nur aktuelles Kapitel oder aktuell + alle Unterniveaus. Öffnet Noesis Editor in einem neuen Tab mit bereits geladenem Inhalt.',
```

### reading.modes.p (riga 4865)
```
DA: '... mit der Scroll-Schaltfläche in der Toolbar wechseln.',
A:  '... über <strong>Navigate</strong> in der Menüleiste wechseln.',
```

### reading.display.tip (riga 4904)
```
DA: '... via <strong>Status speichern</strong>-Schaltfläche gespeichert. ...',
A:  '... über das schwebende Eingabefeld gespeichert, das 8 Sekunden lang erscheint, wenn das Anzeige-Panel nach Änderungen geschlossen wird. ...',
```

### reading.bookmark.create.p (riga 4925)
```
DA: 'Klicken Sie auf die <strong>🔖 Lesezeichen</strong>-Schaltfläche in der Toolbar → ...',
A:  'Klicken Sie auf <strong>Bookmarks</strong> in der Menüleiste → ...',
```

### reading.savestate.h2 / .p (righe 4933–4934)
```
DA: 'Status speichern — <em>alles speichern</em>',
A:  'Automatisches Speichern — <em>immer synchronisiert</em>',

DA: 'Die <strong>💾 Status speichern</strong>-Schaltfläche speichert manuell die aktuelle Leseposition ...',
A:  'Die Leseposition wird <strong>automatisch alle 3 Sekunden</strong> gespeichert, ohne dass der Benutzer etwas tun muss. Anzeigeeinstellungen (Thema, Typografie, Layout) werden pro Buch über ein schwebendes Eingabefeld gespeichert, das 8 Sekunden lang erscheint, wenn das Anzeige-Panel nach Änderungen geschlossen wird.',
```

### reading.savestate.what.p (riga 4936)
```
DA: 'Exakte CFI-Position im Text, Schriftgröße, ...',
A:  'Position: automatisch alle 3 Sekunden gespeichert (CFI des Elements in der visuellen Mitte des Readers). Anzeigeeinstellungen: Schriftgröße, Zeilenhöhe, Seitenmodus (einzel/doppelt), Lesethema, Oberflächenfarben und Scroll-Modus — auf Anfrage über das Anzeige-Eingabefeld gespeichert.',
```

### reading.savestate.perbook.p (riga 4938)
```
DA: '... in <code>noesisLibraryDB</code>. ...',
A:  '... in <code>EpubLibraryDB</code>. ...',
```

### reading.extract.p (riga 4981)
```
DA: 'Die Kapitel extrahieren-Schaltfläche in der Toolbar öffnet ein Dropdown ...',
A:  'Die Extract-Schaltfläche in der Menüleiste öffnet ein Dropdown ...',
```

---

## Note finali

- Le chiavi `reading.btn.percent.*` e `reading.btn.savestate.*` vanno **mantenute** nelle sezioni IT/FR/ES/DE (per compatibilità), ma le corrispondenti card HTML in `navigation.html` sono già state rimosse (modifica unica condivisa da tutte le lingue).
- Le modifiche strutturali a `navigation.html` (rimozione card % Progress e Save State), `library.html` (icona tema) e `index.html` (badge hardcoded) sono già state applicate e valgono per tutte le lingue.
- `doc-ui.html` è hardcoded in italiano: già aggiornato nella fase EN.
