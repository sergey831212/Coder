#!/usr/bin/env python3
import re

# Read all URLs
with open('/workspace/all_sitemap_urls.txt', 'r') as f:
    all_urls = [line.strip() for line in f if line.strip()]

# Categorize URLs
products = []
articles = []
authors = []
brands = []
categories = []

for url in all_urls:
    if '/articles/' in url:
        articles.append(url)
    elif '/authors/' in url:
        authors.append(url)
    elif '/brands/' in url:
        brands.append(url)
    elif re.search(r'arteria-farm\.com/[a-z_-]+/[a-z0-9_-]+', url):
        products.append(url)
    elif re.search(r'arteria-farm\.com/[a-z_-]+$', url):
        categories.append(url)

# Generate HTML lists
def generate_product_list(urls):
    html = ""
    for url in sorted(urls):
        name = url.split('/')[-1].replace('_', ' ').replace('-', ' ')
        # Capitalize first letter of each word
        name = ' '.join(word.capitalize() for word in name.split())
        html += f'<div class="product-item"><a href="{url}" target="_blank">{name}</a></div>\n'
    return html

def generate_link_list(urls, prefix=""):
    html = ""
    for url in sorted(urls):
        name = url.split('/')[-1].replace('_', ' ').replace('-', ' ')
        name = ' '.join(word.capitalize() for word in name.split())
        html += f'<li><a href="{url}" target="_blank">{name}</a></li>\n'
    return html

# Read template
with open('/workspace/sitemap_template.html', 'r') as f:
    template = f.read()

# Replace placeholders
html_content = template.replace('PRODUCTS_PLACEHOLDER', generate_product_list(products))
html_content = html_content.replace('ARTICLES_PLACEHOLDER', generate_link_list(articles))
html_content = html_content.replace('AUTHORS_PLACEHOLDER', generate_link_list(authors))
html_content = html_content.replace('BRANDS_PLACEHOLDER', generate_link_list(brands))
html_content = html_content.replace('CATEGORIES_PLACEHOLDER', generate_link_list(categories))

# Update stats
total_urls = len(all_urls)
html_content = re.sub(r'<div class="number">\d+</div>\s*<div class="label">Всего URL</div>', 
                      f'<div class="number">{total_urls}</div><div class="label">Всего URL</div>', html_content)
html_content = re.sub(r'<div class="number">\d+</div>\s*<div class="label">Товары</div>', 
                      f'<div class="number">{len(products)}</div><div class="label">Товары</div>', html_content)
html_content = re.sub(r'<div class="number">\d+</div>\s*<div class="label">Статьи</div>', 
                      f'<div class="number">{len(articles)}</div><div class="label">Статьи</div>', html_content)
html_content = re.sub(r'<div class="number">\d+</div>\s*<div class="label">Авторов</div>', 
                      f'<div class="number">{len(authors)}</div><div class="label">Авторов</div>', html_content)
html_content = re.sub(r'<div class="number">\d+</div>\s*<div class="label">Брендов</div>', 
                      f'<div class="number">{len(brands)}</div><div class="label">Брендов</div>', html_content)
html_content = re.sub(r'<div class="number">\d+</div>\s*<div class="label">Категорий</div>', 
                      f'<div class="number">{len(categories)}</div><div class="label">Категорий</div>', html_content)

# Write output
with open('/workspace/sitemap.html', 'w') as f:
    f.write(html_content)

print(f"Generated sitemap.html with:")
print(f"  - Total URLs: {total_urls}")
print(f"  - Products: {len(products)}")
print(f"  - Articles: {len(articles)}")
print(f"  - Authors: {len(authors)}")
print(f"  - Brands: {len(brands)}")
print(f"  - Categories: {len(categories)}")
