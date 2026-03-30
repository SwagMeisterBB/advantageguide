#!/usr/bin/env python3
"""
Migrate non-blog pages to DESIGN.md color system.

Replaces old hardcoded hex values with new DESIGN.md values across:
- index.html, about.html, contact.html, privacy.html, terms.html, blog/index.html
- Also updates favicon SVG data URIs
"""

import glob
import os
import re

ROOT = "/tmp/advantageguide"

# Color mapping: old → new
COLOR_MAP = {
    "#1B5E7E": "#1E5FAD",
    "#1b5e7e": "#1E5FAD",
    "#154D68": "#154A8A",
    "#154d68": "#154A8A",
    "#0f3d54": "#0E3A6E",
    "#FAFAF8": "#FDFAF6",
    "#fafaf8": "#FDFAF6",
    "#374151": "#3D3935",
    "#111827": "#2A2623",
    "#6b7280": "#8A8580",
    "#9CA3AF": "#B5B0AB",
    "#9ca3af": "#B5B0AB",
    "#E5E7EB": "#E5E0DA",
    "#e5e7eb": "#E5E0DA",
    "#F3F4F6": "#F0EDE8",
    "#f3f4f6": "#F0EDE8",
    "#EDF4F8": "#EDE8F4",
}

# URL-encoded versions for favicon data URIs
URL_COLOR_MAP = {
    "%231B5E7E": "%231E5FAD",
    "%231b5e7e": "%231E5FAD",
}

# Files to migrate (NOT blog posts — those are already done)
FILES = [
    os.path.join(ROOT, "index.html"),
    os.path.join(ROOT, "about.html"),
    os.path.join(ROOT, "contact.html"),
    os.path.join(ROOT, "privacy.html"),
    os.path.join(ROOT, "terms.html"),
    os.path.join(ROOT, "blog", "index.html"),
]

# New header HTML
NEW_HEADER = '''<a href="#main-content" class="skip-link">Skip to main content</a>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="header-logo">
      <div class="logo-icon">
        <svg width="16" height="16" fill="none" stroke="#fff" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
      </div>
      AdvantageGuide
    </a>
    <nav class="header-nav" aria-label="Main">
      <a href="/blog/">Blog</a>
      <a href="/" class="btn-header">Find My Products</a>
    </nav>
  </div>
</header>'''

NEW_FOOTER = '''<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <p class="footer-copy">&copy; 2026 AdvantageGuide. For informational use only. Always consult your care team.</p>
      <div class="footer-links">
        <a href="/about.html">About</a>
        <a href="/contact.html">Contact</a>
        <a href="/privacy.html">Privacy</a>
        <a href="/terms.html">Terms</a>
      </div>
    </div>
    <a href="/" style="font-size:0.75rem;color:var(--brand)">Back to AdvantageGuide</a>
  </div>
</footer>'''


def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Add blog.css link if not present
    if 'blog.css' not in html:
        html = html.replace(
            '<link href="/styles.css" rel="stylesheet" />',
            '<link href="/styles.css" rel="stylesheet" />\n  <link href="/blog.css" rel="stylesheet" />'
        )

    # 2. Replace all hardcoded colors
    for old, new in COLOR_MAP.items():
        html = html.replace(old, new)

    # 3. Replace URL-encoded colors (favicon data URIs)
    for old, new in URL_COLOR_MAP.items():
        html = html.replace(old, new)

    # 4. Replace old header with new (skip homepage — it has a different header with "nav-brand" button)
    fname = os.path.basename(filepath)
    if fname != "index.html" or "blog" in filepath:
        # Old skip link
        html = re.sub(
            r'<a href="#main-content"[^>]*class="sr-only[^"]*"[^>]*>Skip to main content</a>\n',
            '',
            html
        )
        # Old header — match the Tailwind header pattern
        html = re.sub(
            r'<header class="bg-white[^"]*sticky top-0 z-40">.*?</header>',
            NEW_HEADER,
            html,
            flags=re.DOTALL
        )

    # 5. Replace old footer with new (skip homepage — it has a more elaborate footer)
    if fname != "index.html" or "blog" in filepath:
        html = re.sub(
            r'<footer class="border-t border-gray-200 bg-white[^"]*">.*?</footer>',
            NEW_FOOTER,
            html,
            flags=re.DOTALL
        )

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    migrated = 0
    for filepath in FILES:
        if not os.path.exists(filepath):
            print(f"  skip (missing): {filepath}")
            continue
        fname = os.path.relpath(filepath, ROOT)
        if migrate_file(filepath):
            migrated += 1
            print(f"  migrated: {fname}")
        else:
            print(f"  unchanged: {fname}")

    print(f"\nDone: {migrated} files updated")


if __name__ == "__main__":
    main()
