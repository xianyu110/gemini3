#!/usr/bin/env python3
import os
import re
from bs4 import BeautifulSoup

def fix_article_content(html_content, title):
    """修复文章内容的HTML结构"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 移除原有的内联样式
    for style_tag in soup.find_all('style'):
        style_tag.decompose()

    # 添加CSS链接
    head = soup.find('head')
    if head:
        # 添加JetBrains Mono字体
        font_link = soup.new_tag('link')
        font_link['rel'] = 'stylesheet'
        font_link['href'] = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap'
        head.append(font_link)

        # 添加CSS文件链接
        css_link = soup.new_tag('link')
        css_link['rel'] = 'stylesheet'
        css_link['href'] = '../assets/styles.css'
        head.append(css_link)

    # 找到文章容器
    article = soup.find('article')
    if not article:
        return str(soup)

    # 移除现有的内容区域
    for element in article.find_all(['p', 'div']):
        element_class = element.get('class') if hasattr(element, 'get') else None
        if element.text.strip().startswith(title) or (element_class and 'category-tag' in element_class):
            continue
        if element.text.strip() and not element_class:
            element.decompose()

    # 重新构建文章内容
    content_div = soup.new_tag('div', **{'class': 'article-content fade-in-up'})

    # 添加文章标题
    h1 = soup.new_tag('h1')
    h1.string = title
    content_div.append(h1)

    # 添加文章元信息
    meta_div = soup.new_tag('div', **{'class': 'article-meta'})
    meta_div.append(soup.new_tag('span'))
    meta_div.find('span').string = '<i class="fas fa-calendar"></i> 2025年12月18日'
    content_div.append(meta_div)

    # 重新解析和格式化文章内容
    raw_content = extract_raw_content(html_content)
    formatted_content = format_article_content(raw_content)
    content_div.append(BeautifulSoup(formatted_content, 'html.parser'))

    # 添加API中转站信息
    api_box = create_api_box(soup)
    content_div.append(api_box)

    # 添加相关文章推荐
    related_box = create_related_articles(soup)
    content_div.append(related_box)

    # 替换文章内容
    article.clear()
    article.append(content_div)

    return str(soup)

def extract_raw_content(html_content):
    """提取原始文章内容"""
    # 移除HTML标签，只保留文本内容
    text = re.sub(r'<[^>]+>', '', html_content)

    # 移除多余的空白字符
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)

    # 移除页眉页脚等无关内容
    lines = text.split('\n')
    content_start = False
    content_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('什么是 Gemini') or '简介' in line:
            content_start = True
        if content_start and ('©' in line or 'GitHub' in line):
            break
        if content_start:
            content_lines.append(line)

    return '\n'.join(content_lines)

def format_article_content(raw_text):
    """格式化文章内容为HTML"""
    html_parts = []
    lines = raw_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 标题处理
        if line in ['简介', '核心能力', '技术架构', '发展历程', '命名由来', '总结']:
            html_parts.append(f'<h2>{line}</h2>')
        elif line in ['🎨 多模态理解', '🧠 强大推理能力', '🔍 超长上下文', '诞生背景', '💫 多模态能力的融合']:
            html_parts.append(f'<h3>{line}</h3>')
        elif line.startswith('🚀') or line.startswith('🌐') or line.startswith('📊'):
            html_parts.append(f'<h4>{line}</h4>')
        elif line.startswith('•') or line.startswith('-'):
            html_parts.append(f'<li>{line[1:].strip()}</li>')
        elif line.endswith('：'):
            html_parts.append(f'<p><strong>{line}</strong></p>')
        else:
            # 普通段落
            html_parts.append(f'<p>{line}</p>')

    return ''.join(html_parts)

def create_api_box(soup):
    """创建API中转站信息框"""
    api_box = soup.new_tag('div', **{'class': 'api-info-box'})

    title = soup.new_tag('h3')
    title.string = '🚀 Gemini API 中转站'
    api_box.append(title)

    desc = soup.new_tag('p')
    desc.string = '国内用户专属福利！如果你在国内访问 Google API 遇到网络问题，推荐使用以下中转站：'
    api_box.append(desc)

    key_div = soup.new_tag('div', **{'class': 'api-key-display'})
    key_div.string = '推荐中转站： https://apipro.maynor1024.live/'
    api_box.append(key_div)

    features = soup.new_tag('p', **{'style': 'font-size: 0.9rem; opacity: 0.9;'})
    features.append('✅ 国内直连，无需翻墙<br>')
    features.append('✅ 兼容 OpenAI 格式<br>')
    features.append('✅ 支持多模型切换<br>')
    features.append('✅ 提供免费试用额度')
    api_box.append(features)

    link = soup.new_tag('a', **{
        'href': 'https://apipro.maynor1024.live/',
        'class': 'cta-btn',
        'target': '_blank'
    })
    link.string = ' 访问 API 中转站'
    api_box.append(link)

    return api_box

def create_related_articles(soup):
    """创建相关文章推荐"""
    section = soup.new_tag('section', **{'class': 'article-card'})

    title = soup.new_tag('h2')
    title.string = '📚 相关文章推荐'
    section.append(title)

    grid = soup.new_tag('div', **{'style': 'display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 25px;'})

    articles = [
        ('Gemini 3 正式发布', 'gemini3.html.html', 'Google Gemini 3 国内使用教程与功能评测'),
        ('Gemini API 开发指南', 'gemini-api-guide.html.html', '免费申请 API Key 与 Python/Node.js 接入教程'),
        ('Gemini 功能详解', 'gemini-features.html.html', '多模态、长上下文与代码能力全解析')
    ]

    for title, href, desc in articles:
        a = soup.new_tag('a', **{'href': href, 'style': 'text-decoration: none; color: inherit;'})
        div = soup.new_tag('div', **{
            'style': 'padding: 20px; border: 1px solid var(--border-color); border-radius: 8px; transition: var(--transition);'
        })

        h4 = soup.new_tag('h4', **{'style': 'color: var(--primary-color); margin-bottom: 10px;'})
        h4.string = title
        div.append(h4)

        p = soup.new_tag('p', **{'style': 'color: var(--text-secondary); font-size: 0.9rem;'})
        p.string = desc
        div.append(p)

        a.append(div)
        grid.append(a)

    section.append(grid)
    return section

def process_articles():
    """处理所有文章文件"""
    articles_dir = 'articles'

    for filename in os.listdir(articles_dir):
        if filename.endswith('.html.html'):
            filepath = os.path.join(articles_dir, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取标题
            title_match = re.search(r'<title>([^<]+)', content)
            title = title_match.group(1).replace(' - Gemini 3.0 完全指南', '').strip() if title_match else filename

            print(f"Processing: {filename} - {title}")

            # 修复内容
            fixed_content = fix_article_content(content, title)

            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

    print("All articles have been fixed!")

if __name__ == '__main__':
    process_articles()