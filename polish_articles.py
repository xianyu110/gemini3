#!/usr/bin/env python3
"""
删除 Source 行并润色文章
"""

import os
import re

ARTICLES_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材/articles"

def polish_article(filepath):
    """处理单个文章文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 删除 Source: 行（包括前后的空行）
        content = re.sub(r'\n+Source: https://www\.gemini-cn\.com[^\n]*\n+', '\n\n', content)
        
        # 删除多余的分隔线（连续的 --- 只保留一个）
        content = re.sub(r'(\n---\n)+', '\n\n---\n\n', content)
        
        # 删除文章开头多余的空行
        content = re.sub(r'^\n+', '', content)
        
        # 统一段落间距（确保段落之间有适当的空行）
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 如果有修改，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始处理文章...")
    print(f"📁 目标目录: {ARTICLES_DIR}\n")
    
    processed_count = 0
    
    # 遍历所有 .md 文件
    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, filename)
            if polish_article(filepath):
                processed_count += 1
                print(f"✓ {filename}")
    
    print(f"\n✅ 完成！共处理 {processed_count} 个文件")

if __name__ == "__main__":
    main()
