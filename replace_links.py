#!/usr/bin/env python3
"""
批量替换文章中的链接
"""

import os
import re

# 配置
ARTICLES_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材/articles"
NEW_LINK = "https://maynorai.top/list/#/home"

# 需要替换的旧链接列表
OLD_LINKS = [
    "https://ai.lanjingchat.com",
    "https://xsimplechat.com",
    "https://www.gemini-chinese.com",
    "https://chat.aihuoya.com",
    "https://gptokk.com",
    "http://ai.lanjingchat.com",
    "http://xsimplechat.com",
    "http://www.gemini-chinese.com",
    "http://chat.aihuoya.com",
    "http://gptokk.com",
]

def replace_links_in_file(filepath):
    """替换单个文件中的链接"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replaced_count = 0
        
        # 替换所有旧链接
        for old_link in OLD_LINKS:
            if old_link in content:
                count = content.count(old_link)
                content = content.replace(old_link, NEW_LINK)
                replaced_count += count
        
        # 如果有替换，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return replaced_count
        
        return 0
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return 0

def main():
    """主函数"""
    print("🚀 开始批量替换链接...")
    print(f"📁 目标目录: {ARTICLES_DIR}")
    print(f"🔗 新链接: {NEW_LINK}\n")
    
    total_files = 0
    total_replacements = 0
    
    # 遍历所有 .md 文件
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, filename)
            count = replace_links_in_file(filepath)
            
            if count > 0:
                total_files += 1
                total_replacements += count
                print(f"✓ {filename}: 替换了 {count} 个链接")
    
    print(f"\n✅ 完成！")
    print(f"📊 共处理 {total_files} 个文件")
    print(f"🔗 共替换 {total_replacements} 个链接")

if __name__ == "__main__":
    main()
