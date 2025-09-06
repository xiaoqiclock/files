#!/usr/bin/env python3
"""
GitHub Actions 用索引页生成脚本
生成与 Apache 风格相同的精简目录列表，并为所有子目录递归生成索引
修复长文件名末尾缺少 > 符号的问题
"""

import os
import sys
import unicodedata
from pathlib import Path
from datetime import datetime

# 要忽略的文件和文件夹列表
ignore_list = {'.git', '.github', 'index.html', '.nojekyll'}

def get_east_asian_width_count(text):
    """计算字符串的显示宽度，正确处理东亚字符"""
    count = 0
    for c in text:
        # 使用unicodedata判断字符宽度
        if unicodedata.east_asian_width(c) in ('F', 'W'):
            count += 2  # 全角字符
        else:
            count += 1  # 半角字符
    return count

def format_filename(name, max_width):
    """格式化文件名，长文件名添加省略号和 > 符号，符合 Apache 行为"""
    name_width = get_east_asian_width_count(name)
    if name_width <= max_width:
        return name
    
    # 截断文件名并添加省略号和 > 符号，符合 Apache 行为
    ellipsis = ">"
    ellipsis_width = 1  # > 符号宽度为1
    
    # 计算可用宽度（减去 > 符号的宽度）
    available_width = max_width - ellipsis_width
    
    truncated = ""
    current_width = 0
    
    # 找到最后一个可以完全显示的字符位置
    last_valid_index = 0
    for i, char in enumerate(name):
        char_width = get_east_asian_width_count(char)
        if current_width + char_width > available_width:
            break
        truncated += char
        current_width += char_width
        last_valid_index = i
    
    # 如果截断后还有空间，尝试添加省略号
    if current_width + 3 <= available_width:  # 3 是三个点的宽度
        truncated = name[:last_valid_index + 1] + "..."
    else:
        # 如果没有足够空间添加三个点，只添加一个点
        if current_width + 1 <= available_width:
            truncated = name[:last_valid_index] + "."
        else:
            # 如果连一个点都加不下，直接截断
            truncated = name[:last_valid_index]
    
    return truncated + ellipsis

def generate_index(directory, base_dir):
    """为指定目录生成索引页面"""
    output_file = directory / "index.html"
    
    # 计算相对于基目录的路径，确保以斜杠开头
    if directory == base_dir:
        display_path = "/"
    else:
        display_path = "/" + str(directory.relative_to(base_dir)).replace("\\", "/") + "/"
    
    print(f"正在为目录 {display_path} 生成索引...")
    print(f"输出文件: {output_file}")

    # 收集文件和文件夹
    items = []
    for item in directory.iterdir():
        if item.name in ignore_list:
            continue
            
        # 获取文件的修改时间（不是当前时间）
        mtime = datetime.fromtimestamp(item.stat().st_mtime)
        date_str = mtime.strftime("%d-%b-%Y %H:%M")
        
        # 确定是文件还是目录
        is_dir = item.is_dir()
        name = item.name + "/" if is_dir else item.name
        size = "-" if is_dir else str(item.stat().st_size)
        
        items.append({
            'name': name,
            'path': name,
            'date': date_str,
            'size': size,
            'is_dir': is_dir,
            'display_width': get_east_asian_width_count(name),
            'original_name': name  # 保存原始名称
        })
    
    # 如果没有项目，只生成基本的索引页面
    if not items:
        html_content = f"""<html>
<head><title>Index of {display_path}</title></head>
<body>
<h1>Index of {display_path}</h1><hr><pre><a href="../">../</a>
</pre><hr></body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return

    # 按名称排序，文件夹在前
    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

    # 找到最长的显示宽度，但限制最大宽度
    max_display_width = max(item['display_width'] for item in items) if items else 0
    max_display_width = min(max_display_width, 50)  # 限制最大宽度，类似Apache
    
    # 生成精简的 HTML 内容
    html_content = f"""<html>
<head><title>Index of {display_path}</title></head>
<body>
<h1>Index of {display_path}</h1><hr><pre><a href="../">../</a>
"""

    # 添加每个项目
    for item in items:
        # 格式化文件名（长文件名添加省略号和 > 符号）
        formatted_name = format_filename(item['original_name'], max_display_width)
        
        # 计算需要的空格数量以确保对齐
        name_display_width = get_east_asian_width_count(formatted_name)
        name_spacing = " " * (max_display_width - name_display_width + 50 - max_display_width)
        date_spacing = " " * (20 - len(item['date']))
        
        html_content += f'<a href="{item["path"]}">{formatted_name}</a>{name_spacing}{item["date"]}{date_spacing}{item["size"]}\n'

    html_content += """</pre><hr></body>
</html>"""

    # 写入 index.html 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功生成 {output_file}")
    
    # 递归为子目录生成索引
    for item in items:
        if item['is_dir']:
            generate_index(directory / item['name'].rstrip('/'), base_dir)

# 主程序
if __name__ == "__main__":
    # 获取命令行参数，如果没有则默认为当前目录
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    
    # 设置基目录（用于计算显示路径）
    base_dir = target_dir
    
    # 生成索引页面
    generate_index(target_dir, base_dir)
    
    print("所有目录的索引页面生成完成！")
