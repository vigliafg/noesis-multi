#!/usr/bin/env python3
"""Create noesis816.html (CDN) from noesis816-full.html (embedded).
Replaces inline JSZip+epub.js with CDN <script src> tags and adds book.archive.request() fallback."""

with open('noesis816-full.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Find and replace the inline JSZip+epub.js block ──
jszip_start = content.find('.JSZip=e()')
if jszip_start == -1:
    print("ERROR: JSZip block not found!")
    exit(1)

# Find the <script> tag that contains the JSZip code
script_open = content.rfind('<script>', 0, jszip_start)
if script_open == -1:
    print("ERROR: <script> before JSZip not found!")
    exit(1)

# Find the app code start (our application code, after epub.js)
app_start = content.find('// --- ERROR HANDLING ---', jszip_start)
if app_start == -1:
    print("ERROR: App code start not found!")
    exit(1)

# Find the <script> tag that starts the app code
app_script = content.rfind('<script>', 0, app_start)
if app_script == -1:
    print("ERROR: App <script> tag not found!")
    exit(1)

# The block to remove is from the JSZip <script> opening to just before the app <script>
block_to_replace = content[script_open:app_script]
print(f"Removing inline JSZip+epub.js block: {len(block_to_replace):,} chars")

# Replace with CDN script tags
cdn_tags = '<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/epubjs@0.3.93/dist/epub.min.js"></script>\n'
content = content[:script_open] + cdn_tags + content[app_script:]
print(f"✅ Replaced with CDN tags ({len(cdn_tags)} chars)")

# ── 2. Add CDN fallback to findAndLoadImage ──
# Find the JSZip lookup section
old_code = """      for (const tryPath of pathsToTry) {
        if (!tryPath) continue;
        const normalizedPath = tryPath.replace(/^\\//, '');
        const zipFile = zip.files[normalizedPath];
        if (zipFile && !zipFile.dir) {
          try {
            const arrayBuffer = await zipFile.async('arraybuffer');
            return { data: arrayBuffer, path: normalizedPath };
          } catch (e) {
            console.warn('Error reading file:', normalizedPath, e);
          }
        }
      }
      return null;"""

new_code = """      for (const tryPath of pathsToTry) {
        if (!tryPath) continue;
        const normalizedPath = tryPath.replace(/^\\//, '');

        // Try JSZip first (embedded version)
        if (zip) {
          const zipFile = zip.files[normalizedPath];
          if (zipFile && !zipFile.dir) {
            try {
              const arrayBuffer = await zipFile.async('arraybuffer');
              return { data: arrayBuffer, path: normalizedPath };
            } catch (e) {
              console.warn('Error reading file:', normalizedPath, e);
            }
          }
        }

        // Fallback: use book.archive.request() (CDN version only)
        if (!zip) {
          try {
            var archivePath = normalizedPath.startsWith('/') ? normalizedPath : '/' + normalizedPath;
            var imgData = await book.archive.request(archivePath);
            if (imgData) {
              var arrayBuffer = imgData instanceof ArrayBuffer ? imgData : new TextEncoder().encode(imgData).buffer;
              return { data: arrayBuffer, path: normalizedPath };
            }
          } catch (e) {
            // CDN request failed, continue trying other paths
          }
        }
      }
      return null;"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Added CDN fallback (book.archive.request) to findAndLoadImage")
else:
    print("⚠️  Could not find the findAndLoadImage loop — trying alternate pattern...")
    # Try the pattern from noesis816-reader.html (slightly different indentation)
    alt_old = """      for (const tryPath of pathsToTry) {
        if (!tryPath) continue;
        const normalizedPath = tryPath.replace(/^\\//, '');

        // Try JSZip first (embedded version)
        if (zip) {
          const zipFile = zip.files[normalizedPath];
          if (zipFile && !zipFile.dir) {
            try {
              const arrayBuffer = await zipFile.async('arraybuffer');
              return { data: arrayBuffer, path: normalizedPath };
            } catch (e) {
              console.warn('Error reading file:', normalizedPath, e);
            }
          }
        }

        // Fallback: use book.archive.request() (CDN version only)
        if (!zip) {
          try {
            var archivePath = normalizedPath.startsWith('/') ? normalizedPath : '/' + normalizedPath;
            var imgData = await book.archive.request(archivePath);
            if (imgData) {
              var arrayBuffer = imgData instanceof ArrayBuffer ? imgData : new TextEncoder().encode(imgData).buffer;
              return { data: arrayBuffer, path: normalizedPath };
            }
          } catch (e) {
            // CDN request failed, continue trying other paths
          }
        }
      }
      return null;"""
    if alt_old in content:
        print("   CDN fallback already present — skipping")
    else:
        print("   ERROR: Could not find findAndLoadImage loop in noesis816-full.html!")

# ── Write ──
with open('noesis816.html', 'w', encoding='utf-8') as f:
    f.write(content)

full_size = len(open('noesis816-full.html', 'rb').read())
cdn_size = len(content.encode('utf-8'))
print(f"\n✅ Created noesis816.html")
print(f"   Full (embedded): {full_size:,} bytes")
print(f"   CDN:             {cdn_size:,} bytes")
print(f"   Reduction:       {(1-cdn_size/full_size)*100:.0f}% smaller")
