import os
import sys
import unicodedata
from pathlib import Path
from datetime import datetime

ignore_list = {'.git', '.github', 'index.html', '.nojekyll'}

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in ('F', 'W'):
            count += 2
        else:
            count += 1
    return count

def format_filename(name, max_width):
    if get_east_asian_width_count(name) <= max_width:
        return name
    
    ellipsis = "..."
    ellipsis_width = get_east_asian_width_count(ellipsis)
    available_width = max_width - ellipsis_width
    
    truncated = ""
    current_width = 0
    
    for char in name:
        char_width = get_east_asian_width_count(char)
        if current_width + char_width > available_width:
            break
        truncated += char
        current_width += char_width
    
    return truncated + ellipsis

def generate_index(directory, base_dir):
    output_file = directory / "index.html"
    
    if directory == base_dir:
        display_path = "/"
    else:
        display_path = "/" + str(directory.relative_to(base_dir)).replace("\\", "/") + "/"
    

    items = []
    for item in directory.iterdir():
        if item.name in ignore_list:
            continue
            
        mtime = datetime.fromtimestamp(item.stat().st_mtime)
        date_str = mtime.strftime("%d-%b-%Y %H:%M")
        
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
            'original_name': name
        })
    
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

    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

    max_display_width = max(item['display_width'] for item in items) if items else 0
    max_display_width = min(max_display_width, 50)
    
    html_content = f"""<html>
<head><title>Index of {display_path}</title></head>
<body>
<h1>Index of {display_path}</h1><hr><pre><a href="../">../</a>
"""

    for item in items:
        formatted_name = format_filename(item['original_name'], max_display_width)
        
        name_display_width = get_east_asian_width_count(formatted_name)
        name_spacing = " " * (max_display_width - name_display_width + 50 - max_display_width)
        date_spacing = " " * (20 - len(item['date']))
        
        html_content += f'<a href="{item["path"]}">{formatted_name}</a>{name_spacing}{item["date"]}{date_spacing}{item["size"]}\n'

    html_content += """</pre><hr></body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    
    for item in items:
        if item['is_dir']:
            generate_index(directory / item['name'].rstrip('/'), base_dir)

if __name__ == "__main__":
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    
    base_dir = target_dir
    
    generate_index(target_dir, base_dir)
    
