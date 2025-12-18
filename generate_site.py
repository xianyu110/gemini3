#!/usr/bin/env python3
"""
生成完整的网站结构，包含所有文章页面和导航
"""

import os
import re
from pathlib import Path

# 配置
ARTICLES_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材/articles"
OUTPUT_DIR = "."
SITE_URL = "https://xianyu110.github.io/gemini3"
GITHUB_URL = "https://github.com/xianyu110/gemini3"
MAYNOR_URL = "https://maynorai.top/list/#/home"

# 文章分类
CATEGORIES = {
    "入门指南": [
        "gemini_what-is-gemini.html.md",
        "gemini_gemini-guide.html.md",
        "gemini_gemini-chinese-guide.html.md",
        "gemini_use-gemini-guide.html.md",
    ],
    "版本介绍": [
        "gemini_gemini3.html.md",
        "gemini_gemini-3.html.md",
        "gemini_gemini3-release.html.md",
        "gemini_gemini-2.5-pro.html.md",
    ],
    "访问方式": [
        "gemini_gemini-mirror-sites.html.md",
        "gemini_gemini3-latest-mirror-sites.html.md",
        "gemini_gemini3-cn-access-tutorial.html.md",
        "gemini_gemini-china.html.md",
    ],
    "功能特性": [
        "gemini_gemini-features.html.md",
        "gemini_gemini-ai-drawing.html.md",
        "gemini_gemini-ai-dialogue.html.md",
        "gemini_gemini-ai-assistant.html.md",
    ],
    "使用教程": [
        "gemini_gemini-registration.html.md",
        "gemini_gemini-installation.html.md",
        "gemini_gemini-api-guide.html.md",
    ],
    "对比评测": [
        "gemini_gemini-vs-gpt4.html.md",
    ],
}

def extract_title(content):
    """从文章内容中提取标题"""
    match = re.search(r'^#\s+(.+?)(?:\s+---)?$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未命名文章"

def extract_description(content):
    """从文章内容中提取描述"""
    # 移除标题和分隔线
    content = re.sub(r'^#.+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    
    # 获取第一段文字
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    if paragraphs:
        desc = paragraphs[0][:200]
        return desc + '...' if len(paragraphs[0]) > 200 else desc
    return "Gemini 3.0 使用指南"

def generate_article_html(filename, content, category):
    """生成单个文章的HTML页面"""
    title = extract_title(content)
    description = extract_description(content)
    
    # 转换Markdown到HTML（简单版本）
    html_content = content
    
    # 转换标题
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # 转换段落
    html_content = re.sub(r'\n\n', '</p><p>', html_content)
    html_content = '<p>' + html_content + '</p>'
    
    # 转换链接
    html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', html_content)
    
    # 转换粗体
    html_content = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html_content)
    
    # 转换列表
    html_content = re.sub(r'^\* (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.+</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
    
    # 清理
    html_content = html_content.replace('---', '')
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    
    article_slug = filename.replace('.md', '').replace('gemini_', '')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Gemini 3.0 完全指南</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="Gemini 3.0, {title}, AI代码生成, 谷歌AI, 人工智能教程">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{SITE_URL}/articles/{article_slug}.html">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{SITE_URL}/articles/{article_slug}.html">
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: #4285f4;
            --secondary-color: #34a853;
            --text-primary: #202124;
            --text-secondary: #5f6368;
            --border-color: #dadce0;
        }}
        
        body {{
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            line-height: 1.8;
            color: var(--text-primary);
            background: #fafafa;
        }}
        
        .header {{
            background: white;
            border-bottom: 1px solid var(--border-color);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        .nav {{
            display: flex;
            gap: 30px;
        }}
        
        .nav a {{
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .nav a:hover {{
            color: var(--primary-color);
        }}
        
        .container {{
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        
        .article {{
            background: white;
            border-radius: 12px;
            padding: 50px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        
        .breadcrumb {{
            color: var(--text-secondary);
            margin-bottom: 30px;
            font-size: 0.9rem;
        }}
        
        .breadcrumb a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        .category-tag {{
            display: inline-block;
            background: var(--primary-color);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-bottom: 20px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 30px;
            color: var(--text-primary);
        }}
        
        h2 {{
            font-size: 2rem;
            font-weight: 600;
            margin: 40px 0 20px 0;
            color: var(--text-primary);
        }}
        
        h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            margin: 30px 0 15px 0;
            color: var(--text-primary);
        }}
        
        p {{
            margin-bottom: 20px;
            line-height: 1.8;
        }}
        
        ul {{
            margin: 20px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin-bottom: 10px;
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .cta-box {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin: 40px 0;
        }}
        
        .cta-box h3 {{
            color: white;
            margin-bottom: 15px;
        }}
        
        .cta-btn {{
            display: inline-block;
            background: white;
            color: var(--primary-color);
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            margin-top: 15px;
            transition: transform 0.3s;
        }}
        
        .cta-btn:hover {{
            transform: translateY(-2px);
            text-decoration: none;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            margin-top: 60px;
        }}
        
        @media (max-width: 768px) {{
            .article {{
                padding: 30px 20px;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            .nav {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{SITE_URL}/" class="logo">
                <i class="fas fa-robot"></i> Gemini 3.0
            </a>
            <nav class="nav">
                <a href="{SITE_URL}/">首页</a>
                <a href="{SITE_URL}/tutorial.html">教程</a>
                <a href="{SITE_URL}/articles.html">文章</a>
                <a href="{GITHUB_URL}" target="_blank">GitHub</a>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <article class="article">
            <div class="breadcrumb">
                <a href="{SITE_URL}/">首页</a> / 
                <a href="{SITE_URL}/articles.html">文章</a> / 
                <span>{category}</span>
            </div>
            
            <span class="category-tag">{category}</span>
            
            {html_content}
            
            <div class="cta-box">
                <h3>🚀 立即体验 Gemini 3.0</h3>
                <p>开始你的 AI 代码生成之旅</p>
                <a href="{MAYNOR_URL}" class="cta-btn" target="_blank">
                    <i class="fas fa-external-link-alt"></i> 访问 MaynorAI
                </a>
            </div>
        </article>
    </div>
    
    <footer class="footer">
        <p>© 2025 Gemini 3.0 完全指南 | <a href="{GITHUB_URL}" target="_blank">GitHub</a></p>
    </footer>
</body>
</html>'''
    
    return html, article_slug

def generate_articles_index():
    """生成文章列表页面"""
    articles_html = ""
    
    for category, files in CATEGORIES.items():
        articles_html += f'<div class="category-section"><h2>{category}</h2><div class="articles-grid">'
        
        for filename in files:
            filepath = os.path.join(ARTICLES_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    title = extract_title(content)
                    description = extract_description(content)
                    article_slug = filename.replace('.md', '').replace('gemini_', '')
                    
                    articles_html += f'''
                    <div class="article-card">
                        <h3><a href="articles/{article_slug}.html">{title}</a></h3>
                        <p class="article-desc">{description[:150]}...</p>
                        <a href="articles/{article_slug}.html" class="read-more">阅读全文 →</a>
                    </div>
                    '''
        
        articles_html += '</div></div>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章列表 - Gemini 3.0 完全指南</title>
    <meta name="description" content="Gemini 3.0 完整教程文章列表，涵盖入门指南、版本介绍、访问方式、功能特性等全方位内容">
    <meta name="keywords" content="Gemini 3.0, AI教程, 谷歌AI, 人工智能, 代码生成">
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary-color: #4285f4;
            --secondary-color: #34a853;
            --text-primary: #202124;
            --text-secondary: #5f6368;
        }}
        
        body {{
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: #fafafa;
        }}
        
        .header {{
            background: white;
            border-bottom: 1px solid #dadce0;
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        .nav {{
            display: flex;
            gap: 30px;
        }}
        
        .nav a {{
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .nav a:hover {{
            color: var(--primary-color);
        }}
        
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        
        .category-section {{
            margin-bottom: 60px;
        }}
        
        .category-section h2 {{
            font-size: 2rem;
            margin-bottom: 30px;
            color: var(--text-primary);
        }}
        
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }}
        
        .article-card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .article-card h3 {{
            font-size: 1.3rem;
            margin-bottom: 15px;
        }}
        
        .article-card h3 a {{
            color: var(--text-primary);
            text-decoration: none;
        }}
        
        .article-card h3 a:hover {{
            color: var(--primary-color);
        }}
        
        .article-desc {{
            color: var(--text-secondary);
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        
        .read-more {{
            color: var(--primary-color);
            font-weight: 600;
            text-decoration: none;
        }}
        
        .read-more:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .articles-grid {{
                grid-template-columns: 1fr;
            }}
            
            .hero h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{SITE_URL}/" class="logo">
                <i class="fas fa-robot"></i> Gemini 3.0
            </a>
            <nav class="nav">
                <a href="{SITE_URL}/">首页</a>
                <a href="{SITE_URL}/tutorial.html">教程</a>
                <a href="{SITE_URL}/articles.html" class="active">文章</a>
                <a href="{GITHUB_URL}" target="_blank">GitHub</a>
            </nav>
        </div>
    </header>
    
    <div class="hero">
        <h1>📚 Gemini 3.0 文章列表</h1>
        <p>全面的教程和指南，助你掌握 AI 代码生成革命</p>
    </div>
    
    <div class="container">
        {articles_html}
    </div>
    
    <footer style="text-align: center; padding: 40px; color: #5f6368;">
        <p>© 2025 Gemini 3.0 完全指南 | <a href="{GITHUB_URL}" target="_blank" style="color: #4285f4;">GitHub</a></p>
    </footer>
</body>
</html>'''
    
    return html

def main():
    print("🚀 开始生成网站...")
    
    # 创建 articles 目录
    articles_dir = os.path.join(OUTPUT_DIR, "articles")
    os.makedirs(articles_dir, exist_ok=True)
    
    # 生成所有文章页面
    article_count = 0
    for category, files in CATEGORIES.items():
        for filename in files:
            filepath = os.path.join(ARTICLES_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    html, slug = generate_article_html(filename, content, category)
                    
                    output_path = os.path.join(articles_dir, f"{slug}.html")
                    with open(output_path, 'w', encoding='utf-8') as out:
                        out.write(html)
                    
                    article_count += 1
                    print(f"✓ 生成文章: {slug}.html")
    
    # 生成文章列表页
    articles_index_html = generate_articles_index()
    with open(os.path.join(OUTPUT_DIR, "articles.html"), 'w', encoding='utf-8') as f:
        f.write(articles_index_html)
    print(f"✓ 生成文章列表页: articles.html")
    
    print(f"\n✅ 完成！共生成 {article_count} 篇文章")
    print(f"📁 文章目录: {articles_dir}")
    print(f"🌐 网站地址: {SITE_URL}")

if __name__ == "__main__":
    main()
