"""构建公开课程网页，仅保留经校验的固定教学界面，不执行数据分析或爬虫。"""
from pathlib import Path
import ast
import hashlib
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
    '01_weibo_crawler': ('Weibo Crawler', '第1节：按月份搜集雷军微博，请求、解析、翻页与CSV保存'),
    '02_pandas_analysis': ('Pandas Analysis', '按需查阅：读表、筛选、分组、合并、文本、时间与SQL'),
    '03_plotting': ('Plotting', '按需查阅：Matplotlib、Pandas绘图与交互式绘图'),
    '04_user_behavior_analysis': ('User Behavior Analysis', '第2节：用户记录、内容与公开表达；Pandas和绘图随分析步骤讲解'),
    '05_big_data_with_duckdb': ('Big Data with DuckDB', '第3节：直接查询Parquet、汇总后绘图、查询计划与多核'),
}

MAIN_LESSONS = ('01_weibo_crawler', '04_user_behavior_analysis', '05_big_data_with_duckdb')
REFERENCES = ('02_pandas_analysis', '03_plotting')

COOKIE_TABS_CODE = '''# 显示六步操作标签页；不发送网页请求，也不读取 Cookie。
from pathlib import Path
from IPython.display import HTML, display
# 兼容从 tutorials 目录或项目根目录打开 Notebook。
tab_file = Path('assets/weibo_crawler/cookie_tabs.html')
if not tab_file.is_file():
    tab_file = Path('tutorials/assets/weibo_crawler/cookie_tabs.html')
display(HTML(filename=str(tab_file)))'''

COOKIE_LOAD_ASSIGNMENT = "COOKIE = COOKIE.strip() or (dotenv_values(TUTORIAL_DIR / '.env', interpolate=False).get('WEIBO_COOKIE') or '').strip()"
CRAWL_RESULT_CODE = '''# 展示本次采集的整张表；30条课堂样本会全部显示，不发送新的请求。
if not posts.empty:
    display(posts)
else:
    print('尚无采集结果；填写 Cookie 后运行请求、解析、翻页和保存单元。')'''

# 经本次课程更新审核的已有教学输出；源码与输出必须同时完全匹配。
CRAWLER_SAVED_OUTPUTS = {
    "919edc9b": "21722c81bbaad4b8ada35bb7219984b94bd99bcaf7ac0fd88b2fcf4e33e3d70c",
    "1d0950a3": "94282215923bd101108642bd83be1dcbb1bfa17a6a50a6cfb5f860f029ecd644",
    "583e1e34": "c33b7de3208d08d83436d3712b6396dfaf49ed1ea77c4a592ccf710aa86bf227",
    "f678d4c7": "86149b5acd0be5bd32a5aa7154931248f843dfe2db62877ab692626a81ef1da1",
    "29c35f25": "adfeaec2b77c2f46fbf3d5cd3eb073dd8b2a793d0d725de81d206be72bdb9cd7",
    "2eca888f": "b00bfae8d0320d0be67670b8f844d5baee550a4ae508aad5fea1d86ff02d5afb",
    "3b2d272b": "971424908215b16baab36502d536a456926b6c7d942bb10992dc836a5a6bab62",
    "247e0794": "1ce81093f98667148626378265d91dab6ec042fe5bbe3f3e2fad145033134d36",
    "f3d75216": "b0b1f2dbe1cc23c2eee6a0809018cde00bbdb36635b3b59b33448703fd3b1ca5"
}


def approved_crawler_output(cell):
    expected = CRAWLER_SAVED_OUTPUTS.get(cell.get('id'))
    if not expected:
        return False
    payload = json.dumps({'source': cell.source, 'outputs': cell.get('outputs', [])},
                         ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest() == expected


def audit(root):
    """拒绝数据、私有配置和分析输出；仅允许完全匹配固定HTML文件的教学界面。"""
    if (root / '.git').is_dir():
        result = subprocess.run(['git', 'ls-files'], cwd=root, check=True, capture_output=True, text=True)
        files = [root / name for name in result.stdout.splitlines()]
    else:
        files = [p for p in root.rglob('*') if p.is_file() and '_site' not in p.parts]
    for p in files:
        rel = p.relative_to(root).as_posix()
        if p.name == '.env' or (p.name.startswith('.env.') and p.name != '.env.example'):
            raise ValueError(f'公开材料不能包含登录配置：{rel}')
        if p.name == '.env.example':
            entries = [line.strip() for line in p.read_text(encoding='utf-8').splitlines()
                       if line.strip() and not line.lstrip().startswith('#')]
            assert entries == ['WEIBO_COOKIE=""'], f'公开.env模板必须为空：{rel}'
        if p.suffix.lower() in {'.parquet', '.csv', '.duckdb', '.sqlite', '.db', '.cookie', '.har'}:
            raise ValueError(f'公开材料不能包含数据或会话文件：{rel}')
        if '.local.' in p.name or '/output/' in '/' + rel or rel.startswith('data/'):
            raise ValueError(f'公开材料不能包含本地配置或运行结果：{rel}')
        if rel.startswith('tutorials/data/') and rel != 'tutorials/data/README.md':
            raise ValueError(f'数据目录只允许保留说明：{rel}')
        if p.suffix == '.ipynb':
            notebook = nbformat.read(p, as_version=4)
            for cell in notebook.cells:
                if cell.cell_type == 'code':
                    assert cell.get('execution_count') is None, rel
                    if cell.metadata.get('course_ui') == 'cookie_tabs':
                        assert p.name == '01_weibo_crawler.ipynb', rel
                        assert ast.dump(ast.parse(cell.source)) == ast.dump(ast.parse(COOKIE_TABS_CODE)), rel
                        expected = (root / 'tutorials/assets/weibo_crawler/cookie_tabs.html').read_text(encoding='utf-8')
                        outputs = cell.get('outputs', [])
                        assert len(outputs) == 1 and outputs[0].output_type == 'display_data', rel
                        assert set(outputs[0].data) == {'text/html', 'text/plain'}, rel
                        assert outputs[0].data['text/html'] == expected, rel
                        assert outputs[0].data['text/plain'] in {
                            '获取Cookie的六步标签页（会话值已遮挡）', '<IPython.core.display.HTML object>'}, rel
                    elif cell.metadata.get('course_ui') == 'crawl_result_example':
                        assert p.name == '01_weibo_crawler.ipynb', rel
                        assert ast.dump(ast.parse(cell.source)) == ast.dump(ast.parse(CRAWL_RESULT_CODE)), rel
                        expected = (root / 'tutorials/assets/weibo_crawler/leijun_first3pages_preview.html').read_text(encoding='utf-8')
                        outputs = cell.get('outputs', [])
                        assert len(outputs) == 1 and outputs[0].output_type == 'display_data', rel
                        assert dict(outputs[0].data) == {'text/html': expected,
                            'text/plain': '雷军微博前三页采集示例：30条（2026-10-14）'}, rel
                    elif p.name == '01_weibo_crawler.ipynb' and approved_crawler_output(cell):
                        pass  # 已审核的本课示范输出，不允许任意新输出。
                    else:
                        assert not cell.get('outputs'), rel
                if cell.cell_type == 'code' and cell.source.strip():
                    for node in ast.walk(ast.parse(cell.source)):
                        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'COOKIE' for t in node.targets):
                            is_blank = isinstance(node.value, ast.Constant) and node.value.value == ''
                            is_local_load = p.name == '01_weibo_crawler.ipynb' and ast.dump(node) == ast.dump(ast.parse(COOKIE_LOAD_ASSIGNMENT).body[0])
                            assert is_blank or is_local_load, f'公开Notebook只允许空COOKIE及固定的本地.env读取表达式：{rel}'
        if p.suffix in {'.json', '.ipynb', '.md', '.py', '.html', '.yml'}:
            text = p.read_text(encoding='utf-8')
            assert not re.search(r'(?:_T_WM|SCF|SUB|SUBP|SSOLoginState|ALF)\s*=\s*[^;\s"<>]{8,}', text), rel
            assert not re.search(r'\b[up]_[a-f0-9]{20}\b', text), rel
    return files


def preserve_mermaid_source(html, notebook):
    """转义完整Mermaid源码，防止导出时将节点中的<br/>当成HTML标签。"""
    diagrams = []
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            diagrams.extend(re.findall(r'^```mermaid[^\S\n]*\n(.*?)^```[^\S\n]*$',
                                       cell.source, flags=re.M | re.S))
    if not diagrams:
        return html
    sources = iter(diagrams)
    def replace(match):
        return match[1] + '\n' + escape(next(sources), quote=False) + match[2]
    html, count = re.subn(r'(<pre\b[^>]*\bclass="mermaid"[^>]*>).*?(</pre>)',
                         replace, html, flags=re.S)
    assert count == len(diagrams), 'Mermaid导出数量与Notebook源码不一致'
    return html


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
    (tutorials / 'data').mkdir()
    shutil.copy2(root / 'tutorials/data/README.md', tutorials / 'data/README.md')
    (tutorials / 'requirements').mkdir()
    for name in ('environment.yml', 'requirements.txt', 'README.md'):
        shutil.copy2(root / 'tutorials/requirements' / name, tutorials / 'requirements' / name)
    shutil.copy2(root / 'tutorials/.env.example', tutorials / '.env.example')
    environment_page = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(
        (root / 'tutorials/requirements/README.md').read_text(encoding='utf-8'))])
    environment_html, _ = HTMLExporter(template_name='lab').from_notebook_node(environment_page)
    environment_html = re.sub(r'(<body\b[^>]*>)',
                              r'\1<nav style="padding:16px"><a href="index.html">返回课程首页</a></nav>',
                              environment_html, count=1)
    (out / 'environment.html').write_text(environment_html, encoding='utf-8')
    links = {}
    for stem, (title, description) in TITLES.items():
        source = root / 'tutorials' / (stem + '.ipynb')
        notebook = nbformat.read(source, as_version=4)
        body, _ = HTMLExporter(template_name='lab', embed_images=True).from_notebook_node(notebook)
        body = preserve_mermaid_source(body, notebook)
        # 网页中的参考链接打开HTML教程；Notebook自身仍保留.ipynb相对链接。
        body = re.sub(r'''(href=["'])(0[1-5]_[A-Za-z0-9_]+)\.ipynb(?=[#"'])''', r'\1\2.html', body)
        navigation = ('<nav style="padding:16px;font:16px sans-serif;border-bottom:1px solid #ddd">'
                      '<a href="../index.html">返回课程首页</a> · '
                      f'<a href="{stem}.ipynb" download>下载本页Notebook</a></nav>')
        body = re.sub(r'(<body\b[^>]*>)', r'\1' + navigation, body, count=1)
        (tutorials / (stem + '.html')).write_text(body, encoding='utf-8')
        shutil.copy2(source, tutorials / source.name)
        links[stem] = f'<li><a href="tutorials/{stem}.html">{escape(title)}</a><p>{escape(description)}</p></li>'
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
    <p>依次学习微博爬虫、用户行为分析、DuckDB与大数据处理。第二节在分析步骤中学习Pandas与绘图；
    两本专题教程可按需查阅，无需先完成。网页可以直接阅读，
    代码请下载后在自己的 Conda 或 uv + venv 环境中运行。</p>
    <p><a href="downloads/tutorials.zip">下载全部教程</a> ·
    <a href="environment.html">环境与运行说明</a> ·
    <a href="https://github.com/wybert/social-media-analysis-tutorials">GitHub 仓库</a></p>
    <h2>课堂主线</h2><ul>''' + ''.join(links[k] for k in MAIN_LESSONS) + '''</ul>
    <h2>按需查阅</h2><ul>''' + ''.join(links[k] for k in REFERENCES) + '''</ul>
    <h2>数据与登录配置</h2><p>爬虫教程保留雷军公开微博前3页的请求、解析与采集示范输出，便于对照操作和结果；
    公开材料不包含课堂原始微博数据集、个人 Cookie 或 .env 登录配置。
    Pandas、绘图、用户行为和 DuckDB 教程的课堂数据由教师另行提供，放入
    <code>tutorials/data/posts_two_weeks.parquet</code>。Pandas读写练习还需要同目录的
    <code>posts_preview.csv</code>，由同一份数据取前8行保存。爬虫练习使用本地 HTML；
    学生登录 <a href="https://weibo.cn/">weibo.cn</a> 后，在本机Notebook的代码格中填写自己的 Cookie，
    或在 <code>tutorials/.env</code> 中设置 <code>WEIBO_COOKIE</code>，两者任选其一；
    课堂先检查第一页，再读取该月份前3页。</p>

    </main></body></html>'''
    (out / 'index.html').write_text(index, encoding='utf-8')
    print(f'静态页面已生成：5本教程、HTML例子、雷军30条展示样本；目录 {out.name}')


if __name__ == '__main__':
    assert (Path(sys.prefix) / 'conda-meta').exists() or sys.prefix != sys.base_prefix, '请选择安装课程依赖的 Conda 或 venv 内核'
    root = Path(__file__).resolve().parents[1]
    build(root)
