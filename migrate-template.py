#!/usr/bin/env python3
"""
Migrate AdvantageGuide blog posts to the new template design.

Changes:
1. Add blog.css stylesheet link
2. Remove inline <style> block (moved to blog.css)
3. Replace header with new site-header
4. Move hero image outside content column, make it bigger
5. Replace category banner with clean pill + read time
6. Add author card below byline
7. Replace author bio with new design
8. Replace related posts list with card grid
9. Replace footer with new site-footer
10. Replace back-to-top with new version
"""

import re
import glob
import os

BLOG_DIR = "/tmp/advantageguide/blog"

# ========== NEW HTML BLOCKS ==========

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

NEW_AUTHOR_BIO = '''    <div class="author-bio">
      <img src="/images/austin-edy.jpg" alt="Austin Edy" width="56" height="56" loading="lazy" />
      <div>
        <p class="name">Written by Austin Edy &middot; <span class="reviewed">Last reviewed March 2026</span></p>
        <p class="bio">Austin Edy has 10+ years in health technology and 5+ years of dedicated Medicare research, with experience scaling health tech startups from six-figure to nine-figure revenue. He founded AdvantageGuide after helping his parents navigate their benefits and discovering how much coverage goes unclaimed.</p>
      </div>
    </div>'''

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

NEW_BACK_TO_TOP = '''<button class="back-to-top" aria-label="Back to top" id="back-to-top">
  <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/></svg>
</button>
<script>
(function(){
  var btn = document.getElementById('back-to-top');
  window.addEventListener('scroll', function(){ btn.classList.toggle('visible', window.scrollY > 400); });
  btn.addEventListener('click', function(){ window.scrollTo({ top: 0, behavior: 'smooth' }); });
})();
</script>'''


def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Add blog.css link after styles.css (if not already present)
    if 'blog.css' not in html:
        html = html.replace(
            '<link href="/styles.css" rel="stylesheet" />',
            '<link href="/styles.css" rel="stylesheet" />\n  <link href="/blog.css" rel="stylesheet" />'
        )

    # 2. Remove inline <style> block (now in blog.css)
    # Match from <style> to </style> in the <head>
    html = re.sub(
        r'\n  <style>\s*body \{ font-family.*?</style>',
        '',
        html,
        flags=re.DOTALL
    )

    # 3. Replace old header + skip link with new header
    # Old skip link
    html = re.sub(
        r'<a href="#main-content"[^>]*class="sr-only[^"]*"[^>]*>Skip to main content</a>\n',
        '',
        html
    )
    # Old header
    html = re.sub(
        r'<header class="bg-white border-b border-gray-200 sticky top-0 z-40">.*?</header>',
        NEW_HEADER,
        html,
        flags=re.DOTALL
    )

    # 4. Extract hero image info, remove old hero, insert new hero before <main>
    hero_match = re.search(
        r'<div class="rounded-xl overflow-hidden mb-8">\s*<img src="([^"]*)" alt="([^"]*)"[^/]*/>\s*</div>',
        html,
        flags=re.DOTALL
    )
    if hero_match:
        hero_src = hero_match.group(1)
        hero_alt = hero_match.group(2)
        # Remove old hero
        html = re.sub(
            r'\s*<div class="rounded-xl overflow-hidden mb-8">.*?</div>',
            '',
            html,
            count=1,
            flags=re.DOTALL
        )
        # Insert new hero before main
        new_hero = f'''
<div class="hero-image">
  <img src="{hero_src}" alt="{hero_alt}" width="800" height="450" loading="eager" fetchpriority="high" />
</div>
'''
        html = html.replace('<main id="main-content">', new_hero + '<main id="main-content">')

    # 5. Replace old content wrapper with new class
    html = html.replace(
        '<div class="max-w-2xl mx-auto px-6 py-12">',
        '<div class="content-wrap">'
    )

    # 6. Replace category banner with clean pill + read time
    cat_match = re.search(
        r'<div class="rounded-xl mb-6 px-5 py-4 flex items-center justify-between"[^>]*>.*?'
        r'<span class="text-xs font-semibold[^"]*">([^<]*)</span>\s*'
        r'<span class="text-xs"[^>]*>(\d+ min read)</span>.*?</div>\s*</div>',
        html,
        flags=re.DOTALL
    )
    if cat_match:
        category = cat_match.group(1)
        read_time = cat_match.group(2)
        # Remove old banner
        html = re.sub(
            r'\s*<div class="rounded-xl mb-6 px-5 py-4 flex items-center justify-between".*?</svg>\s*</div>',
            f'''
    <div class="post-meta">
      <span class="category-pill">{category}</span>
      <span class="read-time">{read_time}</span>
    </div>''',
            html,
            count=1,
            flags=re.DOTALL
        )

    # 7. Update H1 class
    html = html.replace(
        'class="text-3xl font-extrabold text-gray-900 leading-tight mb-4"',
        'class="post-title"'
    )

    # 8. Update byline
    html = re.sub(
        r'<p class="text-sm text-gray-600 mb-\d+">(Published.*?)</p>',
        lambda m: f'<p class="post-byline">{m.group(1)}</p>',
        html
    )
    # Update the reviewed span class
    html = html.replace(
        '<span class="text-green-600 font-medium">',
        '<span class="reviewed">'
    )

    # 9. Add author card after byline (if not already present)
    if 'author-card' not in html:
        html = re.sub(
            r'(<p class="post-byline">.*?</p>)',
            r'''\1

    <div class="author-card">
      <img src="/images/austin-edy.jpg" alt="Austin Edy" width="44" height="44" loading="lazy" />
      <div>
        <div class="name">Austin Edy</div>
        <div class="role">Founder, AdvantageGuide &middot; 10+ years in health technology</div>
      </div>
    </div>''',
            html,
            count=1,
            flags=re.DOTALL
        )

    # 10. Replace old author bio
    html = re.sub(
        r'\s*<div class="mt-10 pt-6 border-t border-gray-200">\s*<div class="flex items-start gap-4">.*?Written by Austin Edy.*?</div>\s*</div>\s*</div>',
        '\n' + NEW_AUTHOR_BIO,
        html,
        count=1,
        flags=re.DOTALL
    )

    # 11. Replace "More from the blog" with card grid
    related_match = re.search(
        r'<div class="mt-8 pt-8 border-t border-gray-200">\s*'
        r'<p class="text-sm font-semibold text-gray-600 uppercase tracking-wider mb-4">More from the blog</p>\s*'
        r'<div class="space-y-1">(.*?)</div>\s*</div>',
        html,
        flags=re.DOTALL
    )
    if related_match:
        links_html = related_match.group(1)
        # Extract href and text from each link
        links = re.findall(r'href="([^"]*)"[^>]*><span>([^<]*)</span>', links_html)

        cards = []
        for href, title in links:
            cards.append(f'''        <a href="{href}" class="related-card">
          <span class="title">{title}</span>
          <svg class="chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </a>''')

        new_related = f'''    <div class="related-posts">
      <p class="related-posts-title">More from the blog</p>
      <div class="related-grid">
{chr(10).join(cards)}
      </div>
    </div>'''

        html = re.sub(
            r'\s*<div class="mt-8 pt-8 border-t border-gray-200">.*?More from the blog.*?</div>\s*</div>',
            '\n' + new_related,
            html,
            count=1,
            flags=re.DOTALL
        )

    # 12. Replace footer
    html = re.sub(
        r'<footer class="border-t border-gray-200 bg-white mt-8">.*?</footer>',
        NEW_FOOTER,
        html,
        count=1,
        flags=re.DOTALL
    )

    # 13. Replace back-to-top button and sticky bar
    html = re.sub(
        r'\s*<button id="back-to-top".*?</script>\s*\n\s*<div id="sticky-product-bar".*?</script>',
        '\n\n' + NEW_BACK_TO_TOP,
        html,
        count=1,
        flags=re.DOTALL
    )

    # 14. Update breadcrumb styling
    html = html.replace(
        'class="flex items-center gap-2 text-sm text-gray-600 mb-8"',
        'class="flex items-center gap-2 text-sm mb-8" style="color:var(--text-muted)"'
    )

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def main():
    files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
    # Skip index.html if it exists
    files = [f for f in files if not f.endswith("index.html")]

    migrated = 0
    skipped = 0
    errors = []

    for filepath in files:
        fname = os.path.basename(filepath)
        try:
            if migrate_file(filepath):
                migrated += 1
                print(f"  migrated: {fname}")
            else:
                skipped += 1
                print(f"  unchanged: {fname}")
        except Exception as e:
            errors.append((fname, str(e)))
            print(f"  ERROR: {fname} — {e}")

    print(f"\nDone: {migrated} migrated, {skipped} unchanged, {len(errors)} errors")
    if errors:
        for fname, err in errors:
            print(f"  {fname}: {err}")


if __name__ == "__main__":
    main()
