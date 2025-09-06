#!/usr/bin/env python3
"""
GitHub Actions 用索引页生成脚本
生成类似 Debian 目录列表的页面
"""

import os
import sys
import math
from pathlib import Path
from datetime import datetime

def format_size(size_bytes):
    """格式化文件大小为易读格式"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KiB", "MiB", "GiB", "TiB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def get_file_icon(filename, is_dir=False):
    """根据文件类型返回对应的SVG图标"""
    if is_dir:
        return '''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-folder-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M9 3a1 1 0 0 1 .608 .206l.1 .087l2.706 2.707h6.586a3 3 0 0 1 2.995 2.824l.005 .176v8a3 3 0 0 1 -2.824 2.995l.176 .005h-14a3 3 0 0 1 -2.995 -2.824l-.005 -.176v-11a3 3 0 0 1 2.824 -2.995l.176 -.005h4z" stroke-width="0" fill="currentColor"/>
        </svg>'''
    
    ext = os.path.splitext(filename)[1].lower()
    
    # 根据文件扩展名返回不同的图标
    if ext in ['.txt', '.md', '.rst']:
        return '''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-file-text" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M14 3v4a1 1 0 0 0 1 1h4"/>
            <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"/>
            <path d="M9 9l1 0"/>
            <path d="M9 13l6 0"/>
            <path d="M9 17l6 0"/>
        </svg>'''
    elif ext in ['.html', '.htm']:
        return '''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-file-type-html" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M14 3v4a1 1 0 0 0 1 1h4"/>
            <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4"/>
            <path d="M2 21v-6"/>
            <path d="M5 15v6"/>
            <path d="M2 18h3"/>
            <path d="M20 15v6h2"/>
            <path d="M13 21v-6l2 3l2 -3v6"/>
            <path d="M7.5 15h3"/>
            <path d="M9 15v6"/>
        </svg>'''
    elif ext in ['.zip', '.gz', '.tar', '.rar']:
        return '''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-file-zip" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M6 20.735a2 2 0 0 1 -1 -1.735v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2h-1"/>
            <path d="M11 17a2 2 0 0 1 2 2v2a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1v-2a2 2 0 0 1 2 -2z"/>
            <path d="M11 5l-1 0"/>
            <path d="M13 7l-1 0"/>
            <path d="M11 9l-1 0"/>
            <path d="M13 11l-1 0"/>
            <path d="M11 13l-1 0"/>
            <path d="M13 15l-1 0"/>
        </svg>'''
    elif ext in ['.pdf']:
        return '''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-file" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M14 3v4a1 1 0 0 0 1 1h4"/>
            <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"/>
        </svg>'''
    else:
        return '''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-file" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <path d="M14 3v4a1 1 0 0 0 1 1h4"/>
            <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"/>
        </svg>'''

def generate_debian_style_index(target_dir):
    """生成类似Debian风格的目录索引页面"""
    # 获取目录信息
    target_dir = Path(target_dir)
    items = []
    total_size = 0
    dir_count = 0
    file_count = 0
    
    # 收集文件和文件夹信息
    for item in target_dir.iterdir():
        if item.name.startswith('.'):
            continue
            
        is_dir = item.is_dir()
        size = item.stat().st_size if not is_dir else 0
        mtime = item.stat().st_mtime
        mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
        mtime_display = datetime.fromtimestamp(mtime).strftime('%m/%d/%Y %I:%M:%S %p +00:00')
        
        items.append({
            'name': item.name,
            'path': str(item.relative_to(target_dir)),
            'is_dir': is_dir,
            'size': size,
            'mtime': mtime,
            'mtime_str': mtime_str,
            'mtime_display': mtime_display
        })
        
        if is_dir:
            dir_count += 1
        else:
            file_count += 1
            total_size += size
    
    # 排序：文件夹在前，按名称排序
    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    
    # 计算最大文件大小（用于进度条）
    max_size = max([item['size'] for item in items if not item['is_dir']], default=0)
    
    # 生成HTML内容
    html_content = f'''<!DOCTYPE html>
<html>
    <head>
        <title>{target_dir.name}</title>
        <link rel="canonical" href="/{target_dir.name}/" />
        <meta charset="utf-8">
        <meta name="color-scheme" content="light dark">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ padding: 0; margin: 0; box-sizing: border-box; }}
            body {{
                font-family: Inter, system-ui, sans-serif;
                font-size: 16px;
                text-rendering: optimizespeed;
                background-color: #f3f6f7;
                min-height: 100vh;
            }}
            img,svg {{ vertical-align: middle; z-index: 1; }}
            img {{ max-width: 100%; max-height: 100%; border-radius: 5px; }}
            td img {{ max-width: 1.5em; max-height: 2em; object-fit: cover; }}
            body,a,svg,.layout.current,.layout.current svg,.go-up {{ color: #333; text-decoration: none; }}
            #layout-list, #layout-grid {{ cursor: pointer; }}
            .wrapper {{ max-width: 1200px; margin-left: auto; margin-right: auto; }}
            header,.meta {{ padding-left: 5%; padding-right: 5%; }}
            td a {{ color: #006ed3; text-decoration: none; }}
            td a:hover {{ color: #0095e4; }}
            td a:visited {{ color: #800080; }}
            td a:visited:hover {{ color: #b900b9; }}
            th:first-child,td:first-child {{ width: 5%; }}
            th:last-child,td:last-child {{ width: 5%; }}
            .size,.timestamp {{ font-size: 14px; }}
            .grid .size {{ font-size: 12px; margin-top: .5em; color: #496a84; }}
            header {{ padding-top: 15px; padding-bottom: 15px; box-shadow: 0px 0px 20px 0px rgb(0 0 0 / 10%); }}
            .breadcrumbs {{ text-transform: uppercase; font-size: 10px; letter-spacing: 1px; color: #939393; margin-bottom: 5px; padding-left: 3px; }}
            h1 {{ font-size: 20px; font-family: Poppins, system-ui, sans-serif; font-weight: normal; white-space: nowrap; overflow-x: hidden; text-overflow: ellipsis; color: #c5c5c5; }}
            h1 a,th a {{ color: #000; }}
            h1 a {{ padding: 0 3px; margin: 0 1px; }}
            h1 a:hover {{ background: #ffffc4; }}
            h1 a:first-child {{ margin: 0; }}
            header,main {{ background-color: white; }}
            main {{ margin: 3em auto 0; border-radius: 5px; box-shadow: 0 2px 5px 1px rgb(0 0 0 / 5%); }}
            .meta {{ display: flex; gap: 1em; font-size: 14px; border-bottom: 1px solid #e5e9ea; padding-top: 1em; padding-bottom: 1em; }}
            #summary {{ display: flex; gap: 1em; align-items: center; margin-right: auto; }}
            .filter-container {{ position: relative; display: inline-block; margin-left: 1em; }}
            #search-icon {{ color: #777; position: absolute; height: 1em; top: .6em; left: .5em; }}
            #filter {{ padding: .5em 1em .5em 2.5em; border: none; border: 1px solid #CCC; border-radius: 5px; font-family: inherit; position: relative; z-index: 2; background: none; }}
            .layout,.layout svg {{ color: #9a9a9a; }}
            table {{ width: 100%; border-collapse: collapse; }}
            tbody tr,tbody tr a,.entry a {{ transition: all .15s; }}
            tbody tr:hover,.grid .entry a:hover {{ background-color: #f4f9fd; }}
            th,td {{ text-align: left; }}
            th {{ position: sticky; top: 0; background: white; white-space: nowrap; z-index: 2; text-transform: uppercase; font-size: 14px; letter-spacing: 1px; padding: .75em 0; }}
            td {{ white-space: nowrap; }}
            td:nth-child(2) {{ width: 75%; }}
            td:nth-child(2) a {{ padding: 1em 0; display: block; }}
            td:nth-child(3),th:nth-child(3) {{ padding: 0 20px 0 20px; min-width: 150px; }}
            td .go-up {{ text-transform: uppercase; font-size: 12px; font-weight: bold; }}
            .name,.go-up {{ word-break: break-all; overflow-wrap: break-word; white-space: pre-wrap; }}
            .listing .icon-tabler {{ color: #454545; }}
            .listing .icon-tabler-folder-filled {{ color: #ffb900 !important; }}
            .sizebar {{ position: relative; padding: 0.25rem 0.5rem; display: flex; }}
            .sizebar-bar {{ background-color: #dbeeff; position: absolute; top: 0; right: 0; bottom: 0; left: 0; z-index: 0; height: 100%; pointer-events: none; }}
            .sizebar-text {{ position: relative; z-index: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
            footer {{ padding: 40px 20px; font-size: 12px; text-align: center; }}
            .caddy-logo {{ display: inline-block; height: 2.5em; margin: 0 auto; }}
            @media (max-width: 600px) {{
                .hideable {{ display: none; }}
                td:nth-child(2) {{ width: auto; }}
                th:nth-child(3),td:nth-child(3) {{ padding-right: 5%; text-align: right; }}
                h1 {{ color: #000; }}
                h1 a {{ margin: 0; }}
                #filter {{ max-width: 100px; }}
            }}
            @media (prefers-color-scheme: dark) {{
                html {{ background: black; }}
                body {{ background: linear-gradient(180deg, rgb(34 50 66) 0%, rgb(26 31 38) 100%); background-attachment: fixed; }}
                body,a,svg,.layout.current,.layout.current svg,.go-up {{ color: #ccc; }}
                h1 a,th a {{ color: white; }}
                h1 {{ color: white; }}
                h1 a:hover {{ background: hsl(213deg 100% 73% / 20%); }}
                header,main {{ background-color: #101720; }}
                tbody tr:hover,.grid .entry a:hover {{ background-color: #162030; color: #fff; }}
                th {{ background-color: #18212c; }}
                td a,.listing .icon-tabler {{ color: #abc8e3; }}
                td a:hover,td a:hover .icon-tabler {{ color: white; }}
                td a:visited {{ color: #cd53cd; }}
                td a:visited:hover {{ color: #f676f6; }}
                #search-icon {{ color: #7798c4; }}
                #filter {{ color: #ffffff; border: 1px solid #29435c; }}
                .meta {{ border-bottom: 1px solid #222e3b; }}
                .sizebar-bar {{ background-color: #1f3549; }}
            }}
        </style>
    </head>
    <body>
        <header>
            <div class="wrapper">
                <div class="breadcrumbs">Folder Path</div>
                <h1>
                    <a href="../">/</a><a href="">{target_dir.name}</a>/
                </h1>
            </div>
        </header>
        <div class="wrapper">
            <main>
                <div class="meta">
                    <div id="summary">
                        <span class="meta-item"><b>{dir_count}</b> directories</span>
                        <span class="meta-item"><b>{file_count}</b> files</span>
                        <span class="meta-item"><b>{format_size(total_size)}</b> total</span>
                    </div>
                    <a id="layout-list" class="layout current">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-layout-list" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v2a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z"/>
                            <path d="M4 14m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v2a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z"/>
                        </svg>
                        List
                    </a>
                    <a id="layout-grid" class="layout">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-layout-grid" width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M4 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/>
                            <path d="M14 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/>
                            <path d="M4 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/>
                            <path d="M14 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"/>
                        </svg>
                        Grid
                    </a>
                </div>
                <div class="listing">
                    <table aria-describedby="summary">
                        <thead>
                            <tr>
                                <th></th>
                                <th>
                                    <a href="?sort=namedirfirst&order=desc" class="icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-caret-up" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                            <path d="M18 14l-6 -6l-6 6h12"/>
                                        </svg>
                                    </a>
                                    <a href="?sort=name&order=asc">Name</a>
                                    <div class="filter-container">
                                        <svg id="search-icon" xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-search" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                            <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0"/>
                                            <path d="M21 21l-6 -6"/>
                                        </svg>
                                        <input type="search" placeholder="Search" id="filter">
                                    </div>
                                </th>
                                <th>
                                    <a href="?sort=size&order=asc">Size</a>
                                </th>
                                <th class="hideable">
                                    <a href="?sort=time&order=asc">Modified</a>
                                </th>
                                <th class="hideable"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td></td>
                                <td>
                                    <a href="..">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-corner-left-up" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                            <path d="M18 18h-6a3 3 0 0 1 -3 -3v-10l-4 4m8 0l-4 -4"/>
                                        </svg>
                                        <span class="go-up">Up</span>
                                    </a>
                                </td>
                                <td></td>
                                <td class="hideable"></td>
                                <td class="hideable"></td>
                            </tr>
    '''
    
    # 添加文件和文件夹行
    for item in items:
        size_display = "—" if item['is_dir'] else format_size(item['size'])
        size_bar_width = f"{(item['size'] / max_size * 100):.1f}%" if not item['is_dir'] and max_size > 0 else "0%"
        
        html_content += f'''
                            <tr class="file">
                                <td></td>
                                <td>
                                    <a href="./{item['path']}">
                                        {get_file_icon(item['name'], item['is_dir'])}
                                        <span class="name">{item['name']}{'/' if item['is_dir'] else ''}</span>
                                    </a>
                                </td>
                                <td class="size" data-size="{item['size']}">
        '''
        
        if not item['is_dir']:
            html_content += f'''
                                    <div class="sizebar">
                                        <div class="sizebar-bar" style="width: {size_bar_width}"></div>
                                        <div class="sizebar-text">{size_display}</div>
                                    </div>
            '''
        else:
            html_content += f'{size_display}'
            
        html_content += f'''
                                </td>
                                <td class="timestamp hideable">
                                    <time datetime="{item['mtime_str']}">{item['mtime_display']}</time>
                                </td>
                                <td class="hideable"></td>
                            </tr>
        '''
    
    # 添加页脚和JavaScript
    html_content += '''
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
        <footer>
            Served with
            <a rel="noopener noreferrer" href="https://caddyserver.com">
                <svg class="caddy-logo" viewBox="0 0 379 114" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" fill-rule="evenodd" clip-rule="evenodd" stroke-linecap="round" stroke-linejoin="round">
                    <!-- Caddy logo SVG代码（此处省略以节省空间） -->
                </svg>
            </a>
        </footer>
        <script>
            const filterEl = document.getElementById('filter');
            filterEl?.focus({ preventScroll: true });

            function initPage() {
                // populate and evaluate filter
                if (!filterEl?.value) {
                    const filterParam = new URL(window.location.href).searchParams.get('filter');
                    if (filterParam) {
                        filterEl.value = filterParam;
                    }
                }
                filter();

                // fill in size bars
                let largest = 0;
                document.querySelectorAll('.size').forEach(el => {
                    largest = Math.max(largest, Number(el.dataset.size));
                });
                document.querySelectorAll('.size').forEach(el => {
                    const size = Number(el.dataset.size);
                    const sizebar = el.querySelector('.sizebar-bar');
                    if (sizebar) {
                        sizebar.style.width = `${size/largest * 100}%`;
                    }
                });
            }

            function filter() {
                if (!filterEl) return;
                const q = filterEl.value.trim().toLowerCase();
                document.querySelectorAll('tr.file').forEach(function(el) {
                    if (!q) {
                        el.style.display = '';
                        return;
                    }
                    const nameEl = el.querySelector('.name');
                    const nameVal = nameEl.textContent.trim().toLowerCase();
                    if (nameVal.indexOf(q) !== -1) {
                        el.style.display = '';
                    } else {
                        el.style.display = 'none';
                    }
                });
            }

            const filterElem = document.getElementById("filter");
            if (filterElem) {
                filterElem.addEventListener("keyup", filter);
            }

            document.getElementById("layout-list").addEventListener("click", function() {
                queryParam('layout', '');
            });
            document.getElementById("layout-grid").addEventListener("click", function() {
                queryParam('layout', 'grid');
            });

            window.addEventListener("load", initPage);

            function queryParam(k, v) {
                const qs = new URLSearchParams(window.location.search);
                if (!v) {
                    qs.delete(k);
                } else {
                    qs.set(k, v);
                }
                const qsStr = qs.toString();
                if (qsStr) {
                    window.location.search = qsStr;
                } else {
                    window.location = window.location.pathname;
                }
            }

            function localizeDatetime(e, index, ar) {
                if (e.textContent === undefined) {
                    return;
                }
                var d = new Date(e.getAttribute('datetime'));
                if (isNaN(d)) {
                    d = new Date(e.textContent);
                    if (isNaN(d)) {
                        return;
                    }
                }
                e.textContent = d.toLocaleString();
            }
            var timeList = Array.prototype.slice.call(document.getElementsByTagName("time"));
            timeList.forEach(localizeDatetime);
        </script>
    </body>
</html>'''
    
    return html_content

def main():
    # 获取命令行参数，如果没有则默认为当前目录
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    output_file = target_dir / "index.html"
    
    print(f"正在为目录 {target_dir} 生成索引...")
    print(f"输出文件: {output_file}")
    
    # 生成HTML内容
    html_content = generate_debian_style_index(target_dir)
    
    # 写入index.html文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功生成 {output_file}")

if __name__ == "__main__":
    main()
