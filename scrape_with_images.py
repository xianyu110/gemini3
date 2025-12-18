#!/usr/bin/env python3
"""
增强版爬虫：爬取文章并下载所有图片，更新图片链接
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import hashlib
import re

# 配置
BASE_URL = "https://www.gemini-cn.com"
START_URL = "https://www.gemini-cn.com/gemini/"
OUTPUT_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
ARTICLES_DIR = os.path.join(OUTPUT_DIR, "articles")

# 创建目录
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(ARTICLES_DIR, exist_ok=True)

# 图片URL映射（用于替换）
image_mapping = {}

def get_image_extension(url, content_type=None):
    """获取图片扩展名"""
    if content_type:
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        elif 'svg' in content_type:
            return '.svg'
    
    # 从URL获取
    parsed = urlparse(url)
    path = parsed.path.lower()
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
        if ext in path:
            return ext
    
    return '.jpg'  # 默认

def download_image(img_url, save_dir):
    """下载图片并返回本地路径"""
    try:
        # 检查是否已下载
        if img_url in image_mapping:
            return image_mapping[img_url]
        
        print(f"  📥 下载图片: {img_url[:80]}...")
        
        response = requests.get(img_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            # 生成唯一文件名
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:12]
            content_type = response.headers.get('content-type', '')
            ext = get_image_extension(img_url, content_type)
            
            filename = f"gemini_{url_hash}{ext}"
            filepath = os.path.join(save_dir, filename)
            
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # 记录映射
            relative_path = f"../素材/images/{filename}"
            image_mapping[img_url] = relative_path
            
            print(f"  ✓ 保存为: {filename}")
            return relative_path
        else:
            print(f"  ✗ 下载失败: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ✗ 下载失败: {e}")
        return None

def extract_images_from_content(content, base_url):
    """从内容中提取并下载所有图片"""
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img')
    
    downloaded_images = []
    
    for img in images:
        img_url = img.get('src') or img.get('data-src') or img.get('data-original')
        if img_url:
            # 转换为绝对URL
            full_url = urljoin(base_url, img_url)
            
            # 下载图片
            local_path = download_image(full_url, IMAGES_DIR)
            if local_path:
                downloaded_images.append({
                    'original_url': img_url,
                    'full_url': full_url,
                    'local_path': local_path,
                    'alt': img.get('alt', '')
                })
    
    return downloaded_images

def scrape_article(url):
    """爬取单篇文章"""
    try:
        print(f"\n📄 爬取文章: {url}")
        
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title = soup.find('h1')
        title_text = title.get_text().strip() if title else "未命名文章"
        
        # 提取主要内容
        content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if not content:
            print("  ✗ 未找到文章内容")
            return False
        
        # 提取并下载图片
        images = extract_images_from_content(str(content), BASE_URL)
        print(f"  📸 找到 {len(images)} 张图片")
        
        # 获取文章的纯文本内容
        article_text = content.get_text(separator='\n', strip=True)
        
        # 构建Markdown内容
        markdown_content = f"# {title_text}\n\n"
        markdown_content += "---\n\n"
        
        # 添加文章内容
        markdown_content += article_text + "\n\n"
        
        # 添加图片引用
        if images:
            markdown_content += "\n## 📸 文章图片\n\n"
            for idx, img in enumerate(images, 1):
                alt_text = img['alt'] or f"图片 {idx}"
                markdown_content += f"![{alt_text}]({img['local_path']})\n\n"
        
        # 保存文章
        filename = urlparse(url).path.replace('/', '_').strip('_') + '.md'
        filepath = os.path.join(ARTICLES_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  ✓ 保存文章: {filename}")
        return True
        
    except Exception as e:
        print(f"  ✗ 爬取失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始爬取文章和图片...")
    print(f"📁 输出目录: {OUTPUT_DIR}\n")
    
    # 获取文章列表
    try:
        response = requests.get(START_URL, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有文章链接
        article_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/gemini/' in href and href.endswith('.html'):
                full_url = urljoin(BASE_URL, href)
                article_links.add(full_url)
        
        print(f"📚 找到 {len(article_links)} 篇文章\n")
        
        # 爬取每篇文章
        success_count = 0
        for idx, article_url in enumerate(sorted(article_links), 1):
            print(f"\n[{idx}/{len(article_links)}]")
            if scrape_article(article_url):
                success_count += 1
            time.sleep(1)  # 礼貌延迟
        
        print(f"\n\n✅ 爬取完成！")
        print(f"📊 成功: {success_count}/{len(article_links)} 篇文章")
        print(f"📸 下载: {len(image_mapping)} 张图片")
        print(f"📁 保存位置: {OUTPUT_DIR}")
        
    except Exception as e:
        print(f"✗ 错误: {e}")

if __name__ == "__main__":
    main()
