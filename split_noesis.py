#!/usr/bin/env python3
"""
split_noesis.py — Split noesisNNN-full.html into reader and editor variants.

Usage:
  cd <repo>
  python3 split_noesis.py --version 812

Output:
  noesisNNN-full-reader.html  — Library + Reading (no editor, no snapshot UI)
  noesisNNN-full-editor.html  — Standalone sn56 editor (extracted from sn56Source JSON)

See SPLIT_PLAN.md for the full operational guide.
"""

import re
import sys
import json
import argparse

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def log(msg):
    print(f"  {msg}")


def remove_marked_block(code, start_marker, end_marker):
    """Remove everything between start_marker and end_marker (inclusive)."""
    s = code.find(start_marker)
    e = code.find(end_marker)
    if s == -1 or e == -1:
        log(f"⚠ markers not found: {start_marker[:40]!r}")
        return code
    e += len(end_marker)
    result = code[:s].rstrip() + '\n' + code[e:].lstrip('\n')
    log(f"✓ removed marked block [{start_marker[:30]}…] ({e - s:,} chars)")
    return result


def remove_js_function(code, func_name):
    """
    Remove a JS function definition (sync or async) by counting braces.
    Finds the line containing 'function <func_name>(' and removes the entire
    function body, walking forward with brace depth counting.
    Works correctly for functions with template literals because `${...}` braces balance.
    """
    start = -1
    for prefix in (f'function {func_name}(', f'async function {func_name}('):
        idx = code.find(prefix)
        if idx != -1:
            # Include any preceding 'async ' keyword on the same line
            line_start = code.rindex('\n', 0, idx) + 1
            start = line_start
            break

    if start == -1:
        log(f"⚠ function {func_name} not found")
        return code

    brace = code.find('{', start)
    if brace == -1:
        log(f"⚠ no opening brace for {func_name}")
        return code

    depth, pos, end = 0, brace, -1
    while pos < len(code):
        c = code[pos]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = pos + 1
                break
        pos += 1

    if end == -1:
        log(f"⚠ unclosed brace for {func_name}")
        return code

    result = code[:start].rstrip('\n') + '\n' + code[end:].lstrip('\n')
    log(f"✓ removed function {func_name} ({end - start:,} chars)")
    return result


def remove_html_element_by_id(code, element_id):
    """Remove an HTML element identified by its id attribute."""
    attr = f'id="{element_id}"'
    pos = code.find(attr)
    if pos == -1:
        log(f"⚠ #{element_id} not found")
        return code

    start = code.rindex('<', 0, pos)
    m = re.match(r'<(\w+)', code[start:])
    if not m:
        log(f"⚠ #{element_id} tag name not detected")
        return code
    tag = m.group(1).lower()

    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    if tag in VOID:
        end = code.find('>', start) + 1
    else:
        close = f'</{tag}>'
        # Simple find (header buttons never contain nested same-tag elements)
        end = code.find(close, pos) + len(close)

    if end <= start:
        log(f"⚠ #{element_id} closing tag not found")
        return code

    result = code[:start] + code[end:]
    log(f"✓ removed <{tag}#{element_id}> ({end - start} chars)")
    return result


def remove_exact_block(code, block_text, label=''):
    """Remove the first occurrence of block_text (exact match)."""
    label = label or block_text[:50].replace('\n', '↵')
    if block_text not in code:
        log(f"⚠ block not found: {label!r}")
        return code
    result = code.replace(block_text, '', 1)
    log(f"✓ removed block: {label}")
    return result


def replace_exact(code, old_text, new_text, label=''):
    """Replace the first occurrence of old_text with new_text."""
    label = label or old_text[:50].replace('\n', '↵')
    if old_text not in code:
        log(f"⚠ text not found: {label!r}")
        return code
    result = code.replace(old_text, new_text, 1)
    log(f"✓ replaced: {label}")
    return result


def remove_anchor_to_anchor(code, start_anchor, end_anchor, include_end=False, label=''):
    """
    Remove text from start_anchor to (but not including) end_anchor.
    If include_end=True, also removes end_anchor itself.
    """
    s = code.find(start_anchor)
    if s == -1:
        log(f"⚠ start anchor not found: {start_anchor[:40]!r}")
        return code
    # Walk back to start of the line
    line_start = code.rindex('\n', 0, s) + 1
    e = code.find(end_anchor, s)
    if e == -1:
        log(f"⚠ end anchor not found: {end_anchor[:40]!r}")
        return code
    if include_end:
        e += len(end_anchor)
    result = code[:line_start] + code[e:]
    removed = e - line_start
    log(f"✓ removed anchor-to-anchor [{label or start_anchor[:30]}…] ({removed:,} chars)")
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  EDITOR BUILD
# ─────────────────────────────────────────────────────────────────────────────

def build_editor(code):
    """Extract the sn56Source JSON and return it as a standalone HTML string."""
    START = '<script type="application/json" id="sn56Source">'
    END   = '</script>'
    s = code.find(START)
    if s == -1:
        sys.exit("ERROR: sn56Source not found in source file")
    content_start = s + len(START)
    content_end   = code.find(END, content_start)
    json_str = code[content_start:content_end].strip()
    html = json.loads(json_str)
    log(f"✓ extracted sn56Source JSON → {len(html):,} chars")
    return html


# ─────────────────────────────────────────────────────────────────────────────
#  READER BUILD
# ─────────────────────────────────────────────────────────────────────────────

def build_reader(code):
    r = code

    # ── Step 1: Remove sn56Source block (~912 KB) ──────────────────────────
    r = remove_marked_block(r, '<!-- SN56_SOURCE_START -->', '<!-- SN56_SOURCE_END -->')

    # ── Step 2: Remove JS functions ────────────────────────────────────────
    for fn in ['_openSn56', '_openExtractedEnv', 'getAllExtractedChapters',
               'importSnapshotsFromDisk', '_processSnapshotFiles']:
        r = remove_js_function(r, fn)

    # ── Step 3: Remove IDB bridge listener (between its own markers) ───────
    r = remove_marked_block(r,
        '    // ── IDB bridge: serve requests from child windows (blob:null context) ──',
        '    // ── END IDB bridge ────────────────────────────────────────────────────')

    # ── Step 4: Remove _openSn56 calls from extract functions ──────────────
    # Both occurrences share the same comment anchor, so remove them one by one.
    # Each removal uses remove_anchor_to_anchor: from the comment to the closing });
    for i in range(2):
        anchor = '        // ── Apri sn56.x con payload ──'
        s = r.find(anchor)
        if s == -1:
            anchor = '      // ── Apri sn56.x con payload ──'  # extractMultipleSections indent
            s = r.find(anchor)
        if s == -1:
            log(f"⚠ _openSn56 call anchor #{i+1} not found")
            continue
        line_start = r.rindex('\n', 0, s) + 1
        # Find the closing }); of the _openSn56({ ... }); call
        open_brace = r.find('{', r.find('_openSn56(', s))
        depth, pos = 0, open_brace
        end = -1
        while pos < len(r):
            if r[pos] == '{':
                depth += 1
            elif r[pos] == '}':
                depth -= 1
                if depth == 0:
                    # skip ); after }
                    end = r.find(');', pos) + 2
                    break
            pos += 1
        if end == -1:
            log(f"⚠ _openSn56 call #{i+1} closing ); not found")
            continue
        # Remove from comment line start to end of );
        r = r[:line_start] + r[end:].lstrip('\n')
        log(f"✓ removed _openSn56 call #{i+1}")

    # ── Step 5: Simplify loadLibraryBooks ──────────────────────────────────
    r = simplify_load_library_books(r)

    # ── Step 6: Remove HTML elements from library header ───────────────────
    for eid in ['importSnapshotsInput', 'libImportSnapshotsBtn', 'libEditorBtn']:
        r = remove_html_element_by_id(r, eid)

    # ── Step 7: Remove handler IIFE (Import Snapshots + Open Editor) ───────
    r = remove_anchor_to_anchor(r,
        start_anchor='// ── Handler: Import Snapshots ─',
        end_anchor='    })();\n',
        include_end=True,
        label='Import Snapshots + Editor handler IIFE')

    # ── Step 8: Remove snapshot CSS rules ──────────────────────────────────
    r = remove_snapshot_css(r)

    # ── Step 9: Fix library subtitle ───────────────────────────────────────
    r = r.replace(
        'books, extracted chapters &amp; snapshots',
        'books'
    )
    log("✓ updated library subtitle")

    return r


def simplify_load_library_books(code):
    """
    Remove chapter/snapshot rendering from loadLibraryBooks():
    - Replace Promise.all([getAllBooks(), getAllExtractedChapters()]) with getAllBooks()
    - Remove chaptersByBook building block
    - Remove chapter badge variable declarations (up to just before bookRow.innerHTML)
    - Fix bookRow.innerHTML template (remove badge stats row + chapters-section div)
    - Remove the "Build chapters section" block
    """
    log("  Simplifying loadLibraryBooks()...")

    # 1. Replace Promise.all destructuring with simple getAllBooks()
    code = replace_exact(code,
        "        const [books, allChapters] = await Promise.all([\n"
        "          getAllBooks(),\n"
        "          getAllExtractedChapters().catch(() => [])\n"
        "        ]);",
        "        const books = await getAllBooks();",
        label="Promise.all → getAllBooks()")

    # 2. Remove the chaptersByBook building block
    code = remove_anchor_to_anchor(code,
        start_anchor='// Group chapters by bookName (case-insensitive)',
        end_anchor='        });\n',
        include_end=True,
        label='chaptersByBook building block')

    # 3. Remove chapter badge variable declarations
    #    From "// Find extracted chapters" to JUST BEFORE "bookRow.innerHTML"
    #    (keeps the innerHTML assignment intact)
    code = remove_anchor_to_anchor(code,
        start_anchor='// Find extracted chapters for this book',
        end_anchor='          bookRow.innerHTML',
        include_end=False,
        label='"Find extracted chapters" variables → stop before bookRow.innerHTML')

    # 4. Remove "${chBadge}${snapBadge}" stats row from bookRow.innerHTML template
    code = remove_exact_block(code,
        '                <div class="book-meta-stats">${chBadge}${snapBadge}</div>\n',
        label='badge stats row in bookRow.innerHTML')

    # 5. Remove <div class="chapters-section"></div> from bookRow.innerHTML template
    code = remove_exact_block(code,
        '            <div class="chapters-section"></div>\n',
        label='chapters-section div in bookRow.innerHTML')

    # 6. Remove the "Build chapters section" block
    #    From "// Build chapters section" to just before "bookGrid.appendChild(bookRow)"
    code = remove_anchor_to_anchor(code,
        start_anchor='// Build chapters section',
        end_anchor='          bookGrid.appendChild(bookRow)',
        include_end=False,
        label='"Build chapters section" block')

    return code


def remove_snapshot_css(code):
    """Remove CSS rule blocks whose selector starts with snapshot-related class names."""
    targets = [
        '.snapshots-list',
        '.snapshot-item',
        '.snapshot-item-dot',
        '.snapshot-item-desc',
        '.snapshot-item-date',
        '.snapshot-delete-btn',
    ]
    for cls in targets:
        while True:
            m = re.search(r'\n[ \t]*' + re.escape(cls) + r'[^{}\n]*\{', code)
            if not m:
                break
            rule_start = m.start() + 1   # skip leading \n
            brace_open = m.end() - 1
            depth, pos = 0, brace_open
            rule_end = -1
            while pos < len(code):
                if code[pos] == '{':
                    depth += 1
                elif code[pos] == '}':
                    depth -= 1
                    if depth == 0:
                        rule_end = pos + 1
                        break
                pos += 1
            if rule_end == -1:
                break
            code = code[:rule_start] + code[rule_end:]
            log(f"✓ removed CSS rule for {cls}")
    return code


# ─────────────────────────────────────────────────────────────────────────────
#  VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def verify_reader(code):
    print("\n  ── Reader verification ──")
    # These must be absent (count == 0)
    absent = ['sn56Source', '_openSn56', 'importSnapshotsBtn',
              'libEditorBtn', '__noesisIDB', 'getAllExtractedChapters',
              '_openExtractedEnv', 'importSnapshotsFromDisk', '_processSnapshotFiles',
              'chaptersByBook', '_openSn56']
    # These must be present
    present = ['extractCurrentChapter', 'extractMultipleSections',
               'loadLibraryBooks', 'saveExtractedChapterToDB', 'openNoesisDB']
    all_ok = True
    for p in absent:
        n = code.count(p)
        if n > 0:
            print(f"    ⚠ FAIL (still present {n}×): {p}")
            all_ok = False
        else:
            print(f"    ✓ absent: {p}")
    for p in present:
        if p not in code:
            print(f"    ⚠ FAIL (missing): {p}")
            all_ok = False
        else:
            print(f"    ✓ present: {p}")
    size_kb = len(code.encode()) / 1024
    print(f"  Size: {size_kb:.0f} KB")
    if all_ok:
        print("  ✅ All checks passed")
    return all_ok


def verify_editor(code):
    print("\n  ── Editor verification ──")
    all_ok = True
    cdn_n = len(re.findall(r'cdn\.jsdelivr\.net', code))
    jquery_n = len(re.findall(r'code\.jquery\.com', code))
    font_n = len(re.findall(r'data:font/woff2;base64', code))
    for label, n, want_zero in [
        ('cdn.jsdelivr.net refs', cdn_n, True),
        ('code.jquery.com refs', jquery_n, True),
    ]:
        if want_zero and n > 0:
            print(f"    ⚠ FAIL: {n} {label} remain")
            all_ok = False
        else:
            print(f"    ✓ zero {label}")
    if font_n == 0:
        print("    ⚠ WARN: no embedded font found")
    else:
        print(f"    ✓ {font_n} embedded font data URI(s)")
    size_kb = len(code.encode()) / 1024
    print(f"  Size: {size_kb:.0f} KB")
    if all_ok:
        print("  ✅ All checks passed")
    return all_ok


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Split noesisNNN-full.html into reader and editor files.')
    parser.add_argument('--version', required=True,
                        help='Version number (e.g. 812)')
    args = parser.parse_args()
    ver = args.version

    base = f'noesis{ver}-full.html'
    reader_out = f'noesis{ver}-full-reader.html'
    editor_out = f'noesis{ver}-full-editor.html'

    print(f"Reading {base}...")
    with open(base, 'r', encoding='utf-8') as f:
        source = f.read()
    print(f"  {len(source):,} chars  |  {source.count(chr(10)):,} lines")

    # ── Editor ──────────────────────────────────────────────────────────────
    print(f"\n── Building {editor_out} ────────────────────────────────────")
    editor_html = build_editor(source)
    with open(editor_out, 'w', encoding='utf-8') as f:
        f.write(editor_html)
    print(f"\n✓ Written {editor_out}")
    verify_editor(editor_html)

    # ── Reader ──────────────────────────────────────────────────────────────
    print(f"\n── Building {reader_out} ────────────────────────────────────")
    reader_html = build_reader(source)
    with open(reader_out, 'w', encoding='utf-8') as f:
        f.write(reader_html)
    print(f"\n✓ Written {reader_out}")
    verify_reader(reader_html)

    print("\n✅ Done.")


if __name__ == '__main__':
    main()
