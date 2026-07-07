# Noesis — Reading-to-Knowledge System

> **A single-file HTML EPUB reader and integrated study environment. Zero servers, zero accounts, zero tracking. MIT licensed.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.12%20(noesis812)-6366f1)](CHANGELOG.md)
[![Stack](https://img.shields.io/badge/stack-Vanilla%20JS-f7df1e?logo=javascript)]()

---

## What is Noesis

Noesis is a **Reading-to-Knowledge System** — not just an EPUB reader, but a complete study environment that transforms reading into active knowledge production. It runs as a **single HTML file** openable directly in any browser (`file://`), with no server, no build step, and no framework.

**Core philosophy:** break the barrier between reading and intellectual output. Your annotations shouldn't be trapped in a closed database — they should become the foundation of your next document.

<p align="center">
  <strong>Import → Read & Annotate → Extract → Edit → Export</strong><br>
  <em>All inside your browser. Nothing leaves your device.</em>
</p>

---

## Key Features

### 📖 EPUB Reader

- **Three view modes**: single page, dual-page spread, continuous scroll
- **Hierarchical TOC sidebar** with collapsible sections and clickable navigation
- **15 reading themes** across 5 categories: white, cream/sepia, light gray, medium gray, dark/black
- **Typography controls**: font size (50%–200%), line height (stepped values), page layout
- **3-color highlighting** (yellow, green, pink) with selective removal
- **Persistent bookmarks** using CFI (Canonical Fragment Identifiers), restored across sessions
- **Auto-save reading position** every 3 seconds — never lose your place
- **Media preview**: click images or tables for fullscreen overlay
- **Correct multi-page printing** — captures all iframe content before print

### 📚 Library

- **Book grid** with covers, titles, authors, and statistics badges
- **Hierarchical archive**: Book → Extracted Chapters → Snapshots
- **Light/dark theme toggle** with CSS custom properties (no JS flicker)
- **Import EPUB** files via file picker (single or multiple), stored as ArrayBuffer in IndexedDB
- **Import Snapshots** from disk — reimport `.html` snapshot files into the Library with folder picker (Chrome/Edge) or standard file picker
- **Tools dropdown**: links to EPUB tools, Pandoc Online, and Mozilla PDF Viewer

### ✍️ Integrated WYSIWYG Editor (sn56.x)

- **Summernote 0.9.1** full WYSIWYG editing (bold, italic, headings, tables, images, links)
- **Two modes**: `chapter` (loaded with extracted EPUB content, saves to IndexedDB + filesystem) and `standalone` (blank editor)
- **Three entry points**: Library → Open Editor, Library → click chapter/snapshot, Reader → Extract
- **Dual snapshot system**: every save produces two HTML files — `clean` (no highlights) and `annotated` (with highlights)
- **Simultaneous storage**: IndexedDB for fast library access + filesystem download for backup
- **Export formats**: TXT, Markdown, MD+ZIP (with images), JSON, DOCX, PDF (via browser print)
- **Excalidraw integrated**: diagrams, flowcharts, and mind maps in a dedicated tab (SVG/PNG export)

### 🧩 Chunk Collection System

- Select text, images, or tables from the document and add them to a collection
- **Inspect Panel** (draggable, resizable, non-modal): manage chunks with checkboxes, inject them at cursor position
- Export collection as JSON, Markdown, MD+ZIP, or standalone HTML
- Touch-friendly: double-tap or long-press images on mobile to add to collection

### 🌍 Intelligent Translation

- **Streaming translation** in the Reader: native browser translation flows with you as you read
- **One-shot translation** in the Editor: translate entire sections with a single command
- **No external APIs** — uses the browser's built-in translation engine
- Auto-pauses position auto-save during translation to avoid CFI corruption

---

## Architecture

Noesis is a **Single Page Application** exposing two DOM views that toggle via show/hide:

```
#library-view          → Book catalog, import, chapter hierarchy
#reader-view           → EPUB reader with TOC sidebar, toolbar, floating nav
```

A third environment — the **Editor (sn56.x)** — opens as a separate window via Blob URL with a JSON payload. The editor source is embedded inside the main HTML as a JSON data island.

```
noesis810.html  (6498 lines)
├── <style>      (~2350 lines CSS)
├── HTML DOM     (library-view + reader-view)
└── <script>     (~3700 lines JS)
    ├── noesisDB module       → extracted chapters IndexedDB
    ├── mainDB module         → EPUB library IndexedDB
    ├── Core UI               → show/hide views, toast, library rendering
    └── Reader logic          → rendition, navigation, themes, highlights, extraction
```

### Data Persistence

| Store | Type | Contents |
|-------|------|----------|
| `EpubLibraryDB` | IndexedDB | EPUB files (ArrayBuffer), metadata, reading state, highlights, bookmarks |
| `noesisDB` | IndexedDB | Extracted chapter metadata and snapshots (HTML content) |
| `localStorage` | Browser | Theme preference, font defaults, help banner flags |
| Filesystem | HTML files | Snapshot exports (`clean` + `annot`), reimportable with meta tags |

**Privacy by design:** no data ever leaves your device. The app works fully offline after the first load.

---

## Quick Start

### Direct (simplest)

1. Download `noesis812.html` (or the latest version from [Releases](https://github.com/vigliafg/noesis-multi/releases))
2. Double-click to open in your browser

### Local server (recommended for EPUBs with external resources)

```bash
python3 -m http.server 8000
# Open: http://localhost:8000/noesis812.html
```

### Offline variant

Use `noesis812-full.html` (1.7 MB) — all CDN dependencies (Bootstrap Icons, JSZip, epub.js, sn56 Editor) are embedded as data URIs. Works completely offline with no network requests.

---

## Workflow

```
1. IMPORT   → Add your EPUB to the Library
2. READ     → Navigate via TOC, highlight (3 colors), bookmark key passages
3. EXTRACT  → Click "Extract Chapter" — opens directly in Noesis Editor
4. ANNOTATE → Edit with WYSIWYG toolbar, collect chunks, add notes
5. SAVE     → Dual snapshot (clean + annotated) saved to IDB and filesystem
6. EXPORT   → TXT, Markdown, DOCX, PDF, JSON, or MD+ZIP with images
```

---

## Two Variants

| Variant | File | Size | Dependencies | Use case |
|---------|------|------|-------------|----------|
| **Regular** | `noesis810.html` | ~300 KB | CDN (epub.js, JSZip, Bootstrap Icons) | Normal use with internet |
| **Full (offline)** | `noesis810-full.html` | ~1.7 MB | All embedded as data URIs | Airplane, offline, archival |

The Full variant is produced by embedding Bootstrap Icons as base64 fonts, JSZip and epub.js as inline scripts, and sn56 Editor with all its dependencies as data URIs. See `DOC8_FULL_EMBEDDING.md` for the technique.

---

## Tech Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| Language | HTML5 + CSS3 + Vanilla JS | No framework, no bundler |
| EPUB rendering | epub.js 0.3.93 | CDN / embedded in Full variant |
| ZIP decompression | JSZip 3.10.1 | CDN / embedded |
| Icons | Bootstrap Icons 1.11.3 | CDN / embedded as base64 font |
| Editor | Summernote 0.9.1 lite | CDN, loaded dynamically in sn56.x |
| Markdown export | Turndown | CDN, in sn56.x |
| DOCX export | html-docx-js | CDN, in sn56.x |
| Build embedding | Python 3 (`build.py`) | Embeds sn56.x into the main HTML |
| Diagrams | Excalidraw (fork) | `noesis-excalidraw.vercel.app` |
| E2E testing | Playwright 1.52 | Tests for extraction, bookmarks, highlights |

### JavaScript Patterns

- **No modules** — all code in global scope inside inline `<script>` tags
- **Event delegation** — single listener on `document` with `e.target` checks
- **Explicit global state** — `let` variables at file level
- **Async/await** for IndexedDB and file operations
- **Pure DOM manipulation** — `getElementById`, `innerHTML`, `classList`

---

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome / Edge | 90+ | Full |
| Firefox | 88+ | Full |
| Opera | 76+ | Full |
| Safari | 14+ | Partial (IndexedDB limitations) |

> **Note:** `showDirectoryPicker()` (folder picker for Import Snapshots) requires Chrome/Edge 86+. Other browsers fall back to the standard file picker.

---

## Project Structure

```
noesis-multi/
├── noesis810.html              # Main application (Regular variant, 6498 lines)
├── noesis810-full.html         # Fully-offline variant (1.7 MB)
├── noesis810.zip               # Distribution archives
├── noesis810-full.zip
├── CLAUDE.md                   # Developer guide for Claude Code
├── CHANGELOG.md                # Version history
├── build.py                    # Embed sn56.x into main HTML
├── DOC1_FUNZIONALITA.md        # Complete feature reference (Italian)
├── DOC2_WORKFLOW.md            # User workflows
├── DOC3_CODICE_TECNICO.md      # Code structure and patterns
├── DOC4_SCHEMI_DATI.md         # Data schemas (IndexedDB, localStorage)
├── DOC5_CSS_GUIDE.md           # CSS guide and theme system
├── DOC6_HTML_STRUTTURA.md      # HTML DOM structure
├── DOC7_PATTERN_ESTENSIONE.md  # Extension patterns
├── DOC8_FULL_EMBEDDING.md      # Full variant embedding technique
├── noesis-reader-documentation.md    # Reader technical docs (English)
├── noesis-library-documentation.md   # Library technical docs (English)
├── noesis-editor-sn56-documentation.md # Editor technical docs (English)
├── index.html                  # Documentation website (not the app)
├── style.css / site.js         # Shared styles for documentation pages
└── translations.js             # i18n support for documentation
```

---

## License

**MIT License** — free for personal and commercial use. See [LICENSE](LICENSE) for full text.

---

*"Un solo file. Zero barriere. Tutta la tua conoscenza, in ogni lingua."*  
*— One file. Zero barriers. All your knowledge, in every language.*
