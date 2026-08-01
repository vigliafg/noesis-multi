#!/usr/bin/env python3
"""Create CDN editor v6: keep SUMMERNOTE CSS embedded, only Bootstrap Icons + JS libs via CDN."""
import re

with open('noesis816-full-editor-responsive.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Bootstrap Icons CSS → CDN (SOLO questo blocco CSS embedded) ──
bi_marker = '/*!\n * Bootstrap Icons v1.11.3'
bi_start = content.find(bi_marker)
if bi_start == -1:
    bi_marker = '/*! * Bootstrap Icons v1.11.3'
    bi_start = content.find(bi_marker)
if bi_start != -1:
    style_open = content.rfind('<style>', 0, bi_start)
    style_close = content.find('</style>', bi_start)
    if style_open != -1 and style_close != -1:
        block = content[style_open:style_close + len('</style>')]
        print(f"Bootstrap Icons block: {len(block)} chars → CDN link (111 chars)")
        content = content[:style_open] + '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">\n' + content[style_close + len('</style>'):]
        print("✅ Bootstrap Icons CSS → CDN link")

# ── 2. NON toccare il Summernote CSS embedded (contiene @font-face icone necessarie) ──
sn_check = content.find('@font-face{font-display:auto;font-family:summernote')
if sn_check != -1:
    print("✅ Summernote CSS embedded PRESERVATO (contiene icone toolbar)")
else:
    print("⚠️  Summernote CSS embedded non trovato!")

# ── 3. Add jQuery + Summernote JS CDN BEFORE SN56_PAYLOAD_SLOT ──
slot = content.find('<!-- SN56_PAYLOAD_SLOT -->')
if slot == -1:
    print("ERROR: SN56_PAYLOAD_SLOT not found!"); exit(1)

cdn_js = '<script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/summernote@0.8.20/dist/summernote.min.js"></script>\n'
content = content[:slot] + cdn_js + content[slot:]
print("✅ jQuery + Summernote JS CDN BEFORE inline scripts")

# ── Write ──
with open('noesis816-editor.html', 'w', encoding='utf-8') as f:
    f.write(content)

full_size = 904124
cdn_size = len(content)
print(f"\n✅ Created noesis816-editor.html")
print(f"   Full: {full_size:,} bytes → CDN: {cdn_size:,} bytes ({(1-cdn_size/full_size)*100:.0f}% smaller)")
