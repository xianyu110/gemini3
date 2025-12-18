#!/usr/bin/env python3
"""
强力替换所有形式的旧链接（包括纯文本域名）
"""

import os
import re

ARTICLES_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材/articles"
NEW_LINK = "https://maynorai.top/list/#/home"

# 所有需要替换的域名和链接模式
OLD_PATTERNS = [
    # 完整URL
    r'https?://ai\.lanjingchat\.com[^\s\)]*',
    r'https?://xsimplechat\.com[^\s\)]*',
    r'https?://www\.gemini-chinese\.com[^\s\)]*',
    r'https?://chat\.aihuoya\.com[^\s\)]*',
    r'https?://gptokk\.com[^\s\)]*',
    r'https?://api\.xsimplechat\.com[^\s\)]*',
    
    # 纯域名（不带协议）
    r'ai\.lanjingchat\.com',
    r'xsimplechat\.com',
    r'www\.gemini-chinese\.com',
    r'gemini-chinese\.com',
    r'chat\.aihuoya\.com',
    r'gptokk\.com',
    r'api\.xsimplechat\.com',
    
    # 带括号的引用
    r'\(https?://ai\.lanjingchat\.com[^\)]*\)',
    r'\(https?://xsimplechat\.com[^\)]*\)',
]

def replace_all_patterns(content):
    """替换所有模式"""
    original = content
    
    for pattern in OLD_PATTERNS:
        # 检查是否是括号包裹的链接
        if pattern.startswith(r'\('):
            # 保留括号，只替换内容
            content = re.sub(pattern, f'({NEW_LINK})', content)
        else:
            content = re.sub(pattern, NEW_LINK, content)
    
    return content, content != original

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changed = replace_all_patterns(content)
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"✗ 错误: {filepath}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始强力替换所有旧链接...")
    print(f"📁 目标目录: {ARTICLES_DIR}")
    print(f"🔗 新链接: {NEW_LINK}\n")
    
    processed = 0
    
    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, filename)
            if process_file(filepath):
                processed += 1
                print(f"✓ {filename}")
    
    print(f"\n✅ 完成！共处理 {processed} 个文件")

if __name__ == "__main__":
    main()
