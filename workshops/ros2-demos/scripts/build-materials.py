#!/usr/bin/env python3
"""Build offline HTML and ZIP. Dependency: Python-Markdown."""
from pathlib import Path
from html import escape
import zipfile
import markdown

base = Path(__file__).resolve().parents[1]
root = base.parents[1]
pages = {'TUTORIAL.ko.md': 'index.html', 'README.md': 'overview.html',
         'INSTRUCTOR.md': 'instructor.html', 'RESULTS.md': 'results.html'}
css = '''body{font:17px/1.8 system-ui,sans-serif;color:#203044;max-width:1060px;margin:auto;padding:32px 24px}h1,h2,h3{line-height:1.35}h2{margin-top:2.5em;border-top:1px solid #ccd6df;padding-top:24px}a{color:#145ea5}pre{background:#eef3f7;padding:18px;overflow:auto;border-radius:8px;line-height:1.55}code{font-size:.9em}table{border-collapse:collapse;width:100%;display:block;overflow:auto}td,th{padding:10px;border:1px solid #cbd5df;text-align:left;vertical-align:top}th{background:#eef3f7}.toc{background:#f5f8fa;padding:16px 24px}.toc ul{padding-left:22px}nav{display:flex;gap:16px;flex-wrap:wrap}strong{color:#103f69}@media print{body{font-size:10pt;padding:0}nav,.toc{display:none}pre{white-space:pre-wrap;overflow-wrap:anywhere}h2,h3{break-after:avoid}tr,pre{break-inside:avoid}a{color:inherit}table{display:table;font-size:9pt}}'''
for source, target in pages.items():
    source_text = (base / source).read_text()
    title = source_text.splitlines()[0].lstrip('# ')
    html = markdown.markdown('[TOC]\n\n' + source_text,
                             extensions=['tables', 'fenced_code', 'toc'])
    for md, rendered in pages.items():
        html = html.replace(f'href="{md}"', f'href="{rendered}"')
    (base / target).write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{css}</style></head><body><nav><a href="index.html">실습서</a><a href="instructor.html">강사용 진행표</a><a href="results.html">제출 기록</a><a href="../../downloads/ros2-demos-workshop.zip">ZIP</a></nav><main>{html}</main></body></html>')
archive = root / 'downloads/ros2-demos-workshop.zip'
archive.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(base.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            z.write(path, path.relative_to(root))
print(f'Built {len(pages)} HTML pages and {archive.relative_to(root)}')
