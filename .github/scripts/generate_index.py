#!/usr/bin/env python3
"""
GitHub Actions 用索引页生成脚本
生成与 Apache 风格相同的精简目录列表，并为所有子目录递归生成索引
确保路径显示为绝对路径（以斜杠开头）
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# 要忽略的文件和文件夹列表
ignore_list = {'.git', '.github', 'index.html', '.nojekyll'}

def generate_index(directory, base_dir):
    """为指定目录生成索引页面"""
    output_file = directory / "index.html"
    
    # 计算相对于基目录的路径，确保以斜杠开头
    if directory == base_dir:
        display_path = "/"
    else:
        display_path = "/" + str(directory.relative_to(base_dir)) + "/"
    
    print(f"正在为目录 {display_path} 生成索引...")
    print(f"输出文件: {output_file}")

    # 收集文件和文件夹
    items = []
    for item in directory.iterdir():
        if item.name in ignore_list:
            continue
            
        # 获取修改时间
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
            'name_length': len(name),
            'is_dir': is_dir
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

    # 找到最长的文件名长度
    max_name_length = max(item['name_length'] for item in items)
    
    # 生成精简的 HTML 内容
    html_content = f"""<html>
<head><title>Index of {display_path}</title></head>
<body>
<h1>Index of {display_path}</h1><hr><pre><a href="../">../</a>
"""

    # 添加每个项目
    for item in items:
        # 计算需要的空格数量以确保对齐
        name_spacing = " " * (max_name_length - item['name_length'] + 50 - max_name_length)
        date_spacing = " " * (20 - len(item['date']))
        
        html_content += f'<a href="{item["path"]}">{item["name"]}</a>{name_spacing}{item["date"]}{date_spacing}{item["size"]}\n'

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
