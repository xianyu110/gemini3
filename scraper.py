#!/usr/bin/env python3
"""
Web scraper for Gemini guide website
Scrapes articles and images from the provided URL
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Configuration
BASE_URL = "https://www.gemini-cn.com"
START_URL = "https://www.gemini-cn.com/gemini/"
OUTPUT_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材"

# Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "articles"), exist_ok=True)

def download_image(img_url, save_dir):
    """Download an image from URL"""
    try:
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            # Get filename from URL
            filename = os.path.basename(urlparse(img_url).path)
            if not filename:
                filename = f"image_{hash(img_url)}.jpg"
            
            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded image: {filename}")
            return filepath
    except Exception as e:
        print(f"✗ Failed to download image {img_url}: {e}")
    return None

def scrape_article(url):
    """Scrape a single article page"""
    try:
        print(f"\n📄 Scraping: {url}")
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.find('h1')
        title_text = title.get_text().strip() if title else "Untitled"
        
        # Extract main content
        content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if content:
            # Download images in the article
            images = content.find_all('img')
            for img in images:
                img_url = img.get('src') or img.get('data-src')
                if img_url:
                    full_img_url = urljoin(BASE_URL, img_url)
                    download_image(full_img_url, os.path.join(OUTPUT_DIR, "images"))
            
            # Save article content
            filename = urlparse(url).path.replace('/', '_').strip('_') + '.md'
            filepath = os.path.join(OUTPUT_DIR, "articles", filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title_text}\n\n")
                f.write(f"Source: {url}\n\n")
                f.write("---\n\n")
                f.write(content.get_text(separator='\n', strip=True))
            
            print(f"✓ Saved article: {filename}")
            return True
    except Exception as e:
        print(f"✗ Failed to scrape {url}: {e}")
    return False

def main():
    """Main scraping function"""
    print("🚀 Starting web scraper...")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    # Scrape the main page
    try:
        response = requests.get(START_URL, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article links
        article_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/gemini/' in href and href.endswith('.html'):
                full_url = urljoin(BASE_URL, href)
                article_links.add(full_url)
        
        print(f"\n📚 Found {len(article_links)} articles to scrape")
        
        # Scrape each article
        for i, article_url in enumerate(article_links, 1):
            print(f"\n[{i}/{len(article_links)}]", end=" ")
            scrape_article(article_url)
            time.sleep(1)  # Be polite, don't hammer the server
        
        print("\n\n✅ Scraping completed!")
        print(f"📁 Files saved to: {OUTPUT_DIR}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
