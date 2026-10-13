"""只从无输出的公开Notebook构建静态课程网页，绝不执行数据分析或爬虫。"""
from pathlib import Path
from html import escape
import json
import re
import shutil
import subprocess
import sys
import zipfile
import nbformat
from nbconvert import HTMLExporter

TITLES = {
    '01_weibo_crawler': ('Weibo Crawler', '网页请求与HTML解析、Cookie与前两页采集'),
    '02_pandas_analysis': ('Pandas Analysis', '读表、筛选、分组、合并、文本、时间与SQL'),
    '03_plotting': ('Plotting', '常用图形、子图与交互式绘图介绍'),
    '04_user_behavior_analysis': ('User Behavior Analysis', '记录贡献、讨论内容、公开表达与城市汇总'),
    '05_big_data_with_duckdb': ('Big Data with DuckDB', '直接查询Parquet、汇总后绘图、查询计划与多核'),
}


def audit(root):
    """未来重新部署时也拒绝数据文件、私有配置和Notebook运行输出。"""
    if (root / '.git').is_dir():
        result = subprocess.run(['git', 'ls-files'], cwd=root, check=True, capture_output=True, text=True)
        files = [root / name for name in result.stdout.splitlines()]
    else:
        files = [p for p in root.rglob('*') if p.is_file() and '_site' not in p.parts]
    for p in files:
        rel = p.relative_to(root).as_posix()
        if p.suffix.lower() in {'.parquet', '.csv', '.duckdb', '.sqlite', '.db', '.cookie', '.har'}:
            raise ValueError(f'公开材料不能包含数据或会话文件：{rel}')
        if '.local.' in p.name or '/output/' in '/' + rel or rel.startswith('data/'):
            raise ValueError(f'公开材料不能包含本地配置或运行结果：{rel}')
        if rel.startswith('tutorials/data/') and rel != 'tutorials/data/README.md':
            raise ValueError(f'数据目录只允许保留说明：{rel}')
        if p.suffix == '.ipynb':
            notebook = nbformat.read(p, as_version=4)
            assert all(not c.get('outputs') and c.get('execution_count') is None
                       for c in notebook.cells if c.cell_type == 'code'), rel
        if p.suffix in {'.json', '.ipynb', '.md', '.py', '.html', '.yml'}:
            text = p.read_text(encoding='utf-8')
            assert not re.search(r'(?:_T_WM|SCF|SUB|SUBP|SSOLoginState|ALF)\s*=\s*[^;\s"<>]{8,}', text), rel
            assert not re.search(r'\b[up]_[a-f0-9]{20}\b', text), rel
    return files


def build(root):
    files = audit(root)
    out = root / '_site'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    (out / '.nojekyll').touch()
    tutorials = out / 'tutorials'
    tutorials.mkdir()
    shutil.copytree(root / 'tutorials/assets', tutorials / 'assets')
    shutil.copy2(root / 'tutorials/assets/weibo_crawler/test.html', out / 'test.html')
    shutil.copy2(root / 'tutorials/assets/weibo_crawler/test.html', tutorials / 'test.html')
    shutil.copytree(root / 'tutorials/config', tutorials / 'config',
                    ignore=shutil.ignore_patterns('*.local.json'))
    (tutorials / 'data').mkdir()
    shutil.copy2(root / 'tutorials/data/README.md', tutorials / 'data/README.md')
    (tutorials / 'requirements').mkdir()
    for name in ('environment.yml', 'requirements.txt', 'README.md'):
        shutil.copy2(root / 'tutorials/requirements' / name, tutorials / 'requirements' / name)
    environment_page = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(
        (root / 'tutorials/requirements/README.md').read_text(encoding='utf-8'))])
    environment_html, _ = HTMLExporter(template_name='lab').from_notebook_node(environment_page)
    environment_html = re.sub(r'(<body\b[^>]*>)',
                              r'\1<nav style="padding:16px"><a href="index.html">返回课程首页</a></nav>',
                              environment_html, count=1)
    (out / 'environment.html').write_text(environment_html, encoding='utf-8')
    links = []
    for stem, (title, description) in TITLES.items():
        source = root / 'tutorials' / (stem + '.ipynb')
        notebook = nbformat.read(source, as_version=4)
        body, _ = HTMLExporter(template_name='lab', embed_images=True).from_notebook_node(notebook)
        navigation = ('<nav style="padding:16px;font:16px sans-serif;border-bottom:1px solid #ddd">'
                      '<a href="../index.html">返回课程首页</a> · '
                      f'<a href="{stem}.ipynb" download>下载本页Notebook</a></nav>')
        body = re.sub(r'(<body\b[^>]*>)', r'\1' + navigation, body, count=1)
        (tutorials / (stem + '.html')).write_text(body, encoding='utf-8')
        shutil.copy2(source, tutorials / source.name)
        links.append(f'<li><a href="tutorials/{stem}.html">{escape(title)}</a><p>{escape(description)}</p></li>')
    downloads = out / 'downloads'
    downloads.mkdir()
    with zipfile.ZipFile(downloads / 'tutorials.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            rel = p.relative_to(root).as_posix()
            if rel.startswith('tutorials/') or rel == 'README.md':
                archive.write(p, rel)
    index = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>社交媒体用户行为分析 · 中文实操教程</title><style>
    body{margin:0;background:#fafaf7;color:#172334;font:17px/1.8 system-ui,-apple-system,sans-serif}
    main{max-width:880px;margin:auto;padding:48px 24px}h1{font-size:34px;line-height:1.4;margin:0 0 18px}
    h2{font-size:24px;margin-top:36px}a{color:#1257a0;text-underline-offset:4px}p{margin:8px 0 18px}
    ul{padding-left:24px}li{padding:12px 0;border-bottom:1px solid #ddd}li a{font-size:22px;font-weight:600}
    li p{margin:4px 0;color:#536173}code{background:#e9edf0;padding:2px 5px}footer{margin-top:40px;color:#536173}
    </style></head><body><main><h1>社交媒体用户行为分析</h1>
    <p>学习网页采集、表格分析、绘图、用户行为分析与 DuckDB。网页可以直接阅读，
    代码请下载后在自己的 Conda 或 uv + venv 环境中运行。</p>
    <p><a href="downloads/tutorials.zip">下载全部教程</a> ·
    <a href="environment.html">环境与运行说明</a> ·
    <a href="https://github.com/wybert/social-media-analysis-tutorials">GitHub 仓库</a></p>
    <h2>教程顺序</h2><ul>''' + ''.join(links) + '''</ul>
    <h2>数据与登录配置</h2><p>公开材料不包含微博数据集、采集结果或 Cookie。
    Pandas、绘图、用户行为和 DuckDB 教程的课堂数据由教师另行提供，放入
    <code>tutorials/data/posts_two_weeks.parquet</code>。Pandas读写练习还需要同目录的
    <code>posts_preview.csv</code>，由同一份数据取前8行保存。爬虫练习使用本地 HTML；
    学生登录 <a href="https://weibo.cn/">weibo.cn</a> 后使用自己的本地 Cookie 配置；采集只读前两页。</p>

    </main></body></html>'''
    (out / 'index.html').write_text(index, encoding='utf-8')
    print(f'静态页面已生成：5本教程、HTML例子、无数据下载包；目录 {out.name}')


if __name__ == '__main__':
    assert (Path(sys.prefix) / 'conda-meta').exists() or sys.prefix != sys.base_prefix, '请选择安装课程依赖的 Conda 或 venv 内核'
    root = Path(__file__).resolve().parents[1]
    build(root)
