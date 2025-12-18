#!/usr/bin/env python3
"""
高级文章润色：优化格式、标点、排版
"""

import os
import re

ARTICLES_DIR = "/Users/chinamanor/Downloads/cursor编程/gemini3/素材/articles"

def advanced_polish(content):
    """高级润色处理"""
    
    # 1. 统一中英文之间的空格
    content = re.sub(r'([a-zA-Z0-9])([\u4e00-\u9fa5])', r'\1 \2', content)
    content = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z0-9])', r'\1 \2', content)
    
    # 2. 修复数字和单位之间的空格
    content = re.sub(r'(\d+)\s*([万亿千百十])', r'\1\2', content)
    content = re.sub(r'(\d+)\s*(token|TB|GB|MB|KB)', r'\1 \2', content)
    
    # 3. 统一标点符号（中文使用中文标点）
    content = re.sub(r'([^\w\s])(\s+)([^\w\s])', r'\1\3', content)
    
    # 4. 删除多余的 ​ 符号
    content = content.replace('​', '')
    
    # 5. 优化列表格式
    content = re.sub(r'\n-\s+', '\n- ', content)
    content = re.sub(r'\n\*\s+', '\n* ', content)
    
    # 6. 优化标题格式（确保标题后有空行）
    content = re.sub(r'(^#{1,6}\s+.+)\n([^#\n-])', r'\1\n\n\2', content, flags=re.MULTILINE)
    
    # 7. 删除行尾空格
    content = re.sub(r' +\n', '\n', content)
    
    # 8. 统一段落间距
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 9. 优化冒号后的格式
    content = re.sub(r'：\s*\n', '：\n', content)
    
    # 10. 删除开头和结尾的多余空行
    content = content.strip() + '\n'
    
    return content

def polish_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        polished_content = advanced_polish(content)
        
        if polished_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(polished_content)
            return True
        
        return False
    except Exception as e:
        print(f"✗ Error: {filepath}: {e}")
        return False

def main():
    """主函数"""
    print("✨ 开始高级润色...")
    print(f"📁 目标目录: {ARTICLES_DIR}\n")
    
    processed = 0
    
    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(ARTICLES_DIR, filename)
            if polish_file(filepath):
                processed += 1
                print(f"✓ {filename}")
    
    print(f"\n✅ 完成！共润色 {processed} 个文件")
    print("\n📝 润色内容包括：")
    print("  • 统一中英文间距")
    print("  • 优化标点符号")
    print("  • 规范列表格式")
    print("  • 优化标题排版")
    print("  • 删除多余符号")
    print("  • 统一段落间距")

if __name__ == "__main__":
    main()
