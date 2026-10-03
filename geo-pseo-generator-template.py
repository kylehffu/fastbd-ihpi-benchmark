#!/usr/bin/env python3
"""
Fast-BD Open Architecture: Zero-Dependency Edge Programmatic SEO (pSEO) Generator.
Compiles JSON datasets into static, Schema.org-enriched, edge-optimized landing pages.
Automatically generates/updates sitemap.xml and executes IndexNow live notifications.
License: MIT License (https://opensource.org/licenses/MIT)
"""

import json
import os
import re
import urllib.request
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
SITE_DOMAIN = "example.com"
OUTPUT_DIR = "./dist"
SITEMAP_FILE = "./sitemap.xml"
INDEXNOW_KEY = "your-indexnow-key-here"

def slugify(text: str) -> str:
    """Converts a string into a clean, URL-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_page_html(item: dict, index: int, total: int) -> tuple:
    """Renders a single static HTML page with Schema.org JSON-LD."""
    title = item.get("title", f"Resource #{index}")
    category = item.get("category", "General")
    slug = slugify(f"{item.get('id', index)}-{title}")
    content = item.get("content", "").replace('\n', '<br>')
    metrics = item.get("metrics", "High-Signal Proof")

    html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {SITE_DOMAIN}</title>
  <meta name="description" content="Verified technical reference and benchmark metrics for {title}.">
  <link rel="canonical" href="https://{SITE_DOMAIN}/{slug}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">

  <!-- Schema.org JSON-LD for AI Search & Google Knowledge Graph -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{title}",
    "description": "Benchmark metrics for {title}",
    "articleSection": "{category}",
    "url": "https://{SITE_DOMAIN}/{slug}",
    "datePublished": "{datetime.utcnow().strftime('%Y-%m-%d')}"
  }}
  </script>

  <style>
    body {{ background: #0a0f1d; color: #e2e8f0; font-family: system-ui, sans-serif; padding: 2rem; max-width: 800px; margin: 0 auto; line-height: 1.6; }}
    .badge {{ background: #10b98120; color: #34d399; padding: 0.25rem 0.75rem; border-radius: 9999px; font-family: monospace; font-size: 0.8rem; }}
    .card {{ background: #0f172a; border: 1px solid #1e293b; padding: 1.5rem; border-radius: 1rem; margin: 1.5rem 0; }}
    a {{ color: #10b981; }}
  </style>
</head>
<body>
  <nav><a href="/">&larr; Back to Index</a></nav>
  <main>
    <div style="margin: 1.5rem 0;"><span class="badge">{category}</span></div>
    <h1>{title}</h1>
    <div class="card">
      <h3>Key Performance Benchmark</h3>
      <p><strong>Metrics:</strong> {metrics}</p>
    </div>
    <div class="card">
      <h3>Implementation Blueprint</h3>
      <p>{content}</p>
    </div>
  </main>
  <footer><p>&copy; {datetime.utcnow().year} {SITE_DOMAIN} • Open Architecture</p></footer>
</body>
</html>"""
    return slug, html

def update_sitemap(slugs: list):
    """Generates an XML sitemap for search engine crawlers."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    urls = [f"https://{SITE_DOMAIN}/"] + [f"https://{SITE_DOMAIN}/{s}" for s in slugs]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        xml.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n  </url>")
    xml.append('</urlset>')
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    print(f"Updated {SITEMAP_FILE} with {len(urls)} URLs.")
    return urls

def broadcast_indexnow(urls: list):
    """Broadcasts updated URLs directly to Bing & IndexNow-enabled engines."""
    if not INDEXNOW_KEY or INDEXNOW_KEY == "your-indexnow-key-here":
        print("IndexNow broadcast skipped (key not configured).")
        return

    payload = {
        "host": SITE_DOMAIN,
        "key": INDEXNOW_KEY,
        "urlList": urls[:100]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://www.bing.com/indexnow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "FastBD-pSEO/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow broadcast OK (HTTP {resp.status}).")
    except Exception as e:
        print(f"IndexNow note: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Sample items (replace with your own dataset)
    sample_data = [
        {"id": "01", "category": "AI Agents", "title": "CrewAI Production Guardrails", "metrics": "74% loop reduction", "content": "Deterministic tool execution guards with Pydantic output validation."},
        {"id": "02", "category": "Databases", "title": "Supabase Multi-Tenant RLS", "metrics": "Zero-leak tenancy", "content": "Enforce tenant_id JWT claims across all row level security policies."}
    ]
    
    slugs = []
    for idx, item in enumerate(sample_data):
        slug, html = generate_page_html(item, idx + 1, len(sample_data))
        slugs.append(slug)
        with open(os.path.join(OUTPUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)
            
    print(f"Compiled {len(slugs)} static pages to {OUTPUT_DIR}.")
    urls = update_sitemap(slugs)
    broadcast_indexnow(urls)

if __name__ == "__main__":
    main()
