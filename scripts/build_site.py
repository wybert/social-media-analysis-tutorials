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
from IPython.core.inputtransformer2 import TransformerManager
from nbconvert import HTMLExporter
from course_release import ARCHIVE_URL, EXPIRES_AT, MATERIAL_VERSION

TITLES = {
    '01_weibo_crawler': ('Weibo Crawler', '第1节：按月份搜集雷军微博，请求、解析、翻页与CSV保存'),
    'extent/02_pandas_analysis': ('Pandas Analysis', '按需查阅：读表、筛选、分组、合并、文本、时间与SQL'),
    'extent/03_plotting': ('Plotting', '按需查阅：Matplotlib、Pandas绘图与交互式绘图'),
    '02_user_behavior_analysis': ('User Behavior Analysis', '第2节：用户记录、内容与公开表达；Pandas和绘图随分析步骤讲解'),
    '03_big_data_with_duckdb': ('Big Data with DuckDB', '第3节：直接查询Parquet、汇总后绘图、查询计划与多核'),
    '04_spatial_user_behavior': ('Spatial Analysis and User Behavior', '第4节：矢量与栅格、空间连接、分级设色与用户位置观测'),
    '05_heatwave_user_expression': ('Heatwave and User Expression', '第5节：热相关讨论、情感变化、城市差异与四川空间分布'),
    '06_spatial_big_data_duckdb': ('Spatial Big Data with DuckDB', '第6节：空间SQL、全国网格汇总、城市间观测联系与Lonboard'),
}

MAIN_LESSONS = ('01_weibo_crawler', '02_user_behavior_analysis', '03_big_data_with_duckdb',
                '04_spatial_user_behavior', '05_heatwave_user_expression', '06_spatial_big_data_duckdb')
REFERENCES = ('extent/02_pandas_analysis', 'extent/03_plotting')

SETUP_GUIDE = '''<section id="getting-started"><h2>课前准备：从安装到运行</h2>
<p>请在自己的电脑上使用桌面版VS Code。网页用于阅读；运行代码需要下载资料并选择本机Python环境。</p>
<ol class="setup">
<li><strong>安装Visual Studio Code。</strong>前往<a href="https://code.visualstudio.com/download">VS Code官方下载页</a>，选择自己的操作系统并安装。</li>
<li><strong>安装Python和Jupyter扩展。</strong>在VS Code左侧打开Extensions（扩展），分别搜索并安装Microsoft发布的
<a href="https://marketplace.visualstudio.com/items?itemName=ms-python.python">Python</a>和
<a href="https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter">Jupyter</a>。扩展负责编辑和执行Notebook，Python运行环境在下一步安装。</li>
<li><strong>安装Miniconda。</strong>Miniconda提供Python和Conda；课程环境会使用Python 3.11，无需再单独安装Python。
可在<a href="https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/">清华镜像目录</a>选择安装包：
<div class="table-scroll"><table><thead><tr><th>电脑类型</th><th>安装包</th></tr></thead><tbody>
<tr><td>Windows，Intel / AMD 64位</td><td><a href="https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Windows-x86_64.exe">Windows x86_64 .exe</a></td></tr>
<tr><td>Mac，Apple M系列芯片</td><td><a href="https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-MacOSX-arm64.pkg">macOS ARM64 .pkg</a></td></tr>
<tr><td>Mac，Intel芯片</td><td><a href="https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-MacOSX-x86_64.pkg">macOS x86_64 .pkg</a></td></tr>
<tr><td>Windows ARM设备</td><td>镜像暂未提供原生ARM版。Windows 11 ARM可尝试上面的x86_64安装包，依靠系统的<a href="https://learn.microsoft.com/windows/arm/apps-on-arm-x86-emulation">x64兼容机制</a>；课程环境尚未在此类设备上实测。</td></tr>
</tbody></table></div>
Mac可在“关于本机”查看芯片类型；Windows可在“设置 → 系统 → 系统信息”查看系统类型。安装完成后重新打开VS Code。</li>
<li><strong>下载课程资料。</strong>点击本页上方“下载所有资料（含数据，需密码）”，解压密码由教师提供。
只下载“仅下载教程”或GitHub源码的同学还需另行取得课堂数据。</li>
<li><strong>完整解压。</strong>将整个资料包解压到自己的课程文件夹，不要只拖出单个Notebook。
如果系统工具不能解压AES加密ZIP，Windows可使用<a href="https://www.7-zip.org/download.html">7-Zip</a>。
解压后应能看到<code>social-media-analysis-classroom</code>文件夹，其中有<code>README.md</code>和<code>tutorials</code>。</li>
<li><strong>用VS Code打开整个文件夹。</strong>选择“File → Open Folder / 文件 → 打开文件夹”，打开上一步的
<code>social-media-analysis-classroom</code>。资源管理器中应直接显示<code>tutorials</code>。</li>
<li><strong>在VS Code终端创建环境。</strong>选择“Terminal → New Terminal / 终端 → 新建终端”，确认当前目录包含<code>tutorials</code>，依次执行：
<pre><code>conda env create -f tutorials/requirements/environment.yml
conda activate user-behavior-class</code></pre>
首次创建需要下载依赖，请等待命令完成。若Windows提示找不到conda，在开始菜单打开“Anaconda Prompt (Miniconda3)”，运行
<code>conda init powershell</code>，然后关闭并重新打开VS Code及其终端。</li>
<li><strong>打开Notebook并选择内核。</strong>先打开<code>tutorials/01_weibo_crawler.ipynb</code>，点击右上角“Select Kernel / 选择内核”，
选择“Python Environments / Python环境”中的<code>user-behavior-class</code>（必要时先点“Select Another Kernel / 选择其他内核”）。
点击代码格左侧运行按钮，或按<code>Shift + Enter</code>，从上到下执行。第一次下午依次使用01—03，第二次下午依次使用04—06；<code>extent</code>中的两本为补充资料。</li>
</ol><p>其他环境选择、可选模型依赖及常见问题见<a href="environment.html">环境与运行说明</a>。
Notebook操作也可参考<a href="https://code.visualstudio.com/docs/datascience/jupyter-notebooks">VS Code官方指南</a>。</p></section>'''

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
                    for node in ast.walk(ast.parse(TransformerManager().transform_cell(cell.source))):
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
    for name in ('environment.yml', 'requirements.txt', 'requirements-nlp.txt', 'README.md'):
        shutil.copy2(root / 'tutorials/requirements' / name, tutorials / 'requirements' / name)
    shutil.copy2(root / 'tutorials/.env.example', tutorials / '.env.example')
    shutil.copy2(root / 'tutorials/DATA_USE_TERMS.md', tutorials / 'DATA_USE_TERMS.md')
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
        destination = tutorials / (stem + '.html')
        destination.parent.mkdir(parents=True, exist_ok=True)
        notebook = nbformat.read(source, as_version=4)
        body, _ = HTMLExporter(template_name='lab', embed_images=True).from_notebook_node(notebook)
        body = preserve_mermaid_source(body, notebook)
        # 网页中的参考链接打开HTML教程；Notebook自身仍保留.ipynb相对链接。
        body = re.sub(r'''(href=["'])((?:\.\.?/|extent/)*0[1-6]_[A-Za-z0-9_]+)\.ipynb(?=[#"'])''',
                      r'\1\2.html', body)
        home = '../../index.html' if '/' in stem else '../index.html'
        navigation = ('<nav style="padding:16px;font:16px sans-serif;border-bottom:1px solid #ddd">'
                      f'<a href="{home}">返回课程首页</a> · '
                      f'<a href="{source.name}" download>下载本页Notebook</a></nav>')
        body = re.sub(r'(<body\b[^>]*>)', r'\1' + navigation, body, count=1)
        destination.write_text(body, encoding='utf-8')
        shutil.copy2(source, destination.with_suffix('.ipynb'))
        links[stem] = f'<li><a href="tutorials/{stem}.html">{escape(title)}</a><p>{escape(description)}</p></li>'
    downloads = out / 'downloads'
    downloads.mkdir()
    with zipfile.ZipFile(downloads / 'tutorials.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            rel = p.relative_to(root).as_posix()
            if rel.startswith('tutorials/') or rel == 'README.md':
                archive.write(p, rel)
    shutil.copy2(downloads / 'tutorials.zip', downloads / f'tutorials-{MATERIAL_VERSION}.zip')
    index = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>社交媒体用户行为分析 · 中文实操教程</title><style>
    body{margin:0;background:#fafaf7;color:#172334;font:17px/1.8 system-ui,-apple-system,sans-serif}
    main{max-width:880px;margin:auto;padding:48px 24px}h1{font-size:34px;line-height:1.4;margin:0 0 18px}
    h2{font-size:24px;margin-top:36px}a{color:#1257a0;text-underline-offset:4px}p{margin:8px 0 18px}
    ul,ol{padding-left:24px}li{padding:12px 0;border-bottom:1px solid #ddd}.lessons>li>a{font-size:22px;font-weight:600}
    li p{margin:4px 0;color:#536173}code{background:#e9edf0;padding:2px 5px}footer{margin-top:40px;color:#536173}
    pre{overflow:auto;background:#e9edf0;padding:14px;line-height:1.6}pre code{padding:0}
    .table-scroll{overflow:auto}table{border-collapse:collapse;width:100%;margin:12px 0;font-size:15px}
    td,th{text-align:left;vertical-align:top;padding:8px;border:1px solid #cbd3da}.setup>li{padding-left:6px}
    </style></head><body><main><h1>社交媒体用户行为分析</h1>
    <p>两次下午课，依次学习微博爬虫、用户行为分析、DuckDB、空间分析、热浪相关表达和空间大数据分析。第二节在分析步骤中学习Pandas与绘图；
    两本专题教程可按需查阅，无需先完成。网页可以直接阅读，
    代码请下载后在自己的 Conda 或 uv + venv 环境中运行。</p>
    <p><a id="classroom-download" href="''' + ARCHIVE_URL + '''">下载所有资料（含数据，需密码）</a> ·
    <a href="downloads/tutorials-''' + MATERIAL_VERSION + '''.zip">仅下载教程（不含数据）</a> ·
    <a href="environment.html">环境与运行说明</a> ·
    <a href="https://github.com/wybert/social-media-analysis-tutorials">GitHub 仓库</a></p>
    <p id="materials-version">资料版本：''' + MATERIAL_VERSION + '''。六本主教程（01—06）；Pandas和Plotting位于extent补充目录。
    请将新下载的压缩包解压到一个新文件夹，再打开其中的tutorials，避免与旧文件混在一起。</p>
    ''' + SETUP_GUIDE + '''
    <h2>第一次下午：社交媒体用户行为分析</h2><ul class="lessons">''' + ''.join(links[k] for k in MAIN_LESSONS[:3]) + '''</ul>
    <h2>第二次下午：用户时空行为分析</h2><ul class="lessons">''' + ''.join(links[k] for k in MAIN_LESSONS[3:]) + '''</ul>
    <h2>按需查阅</h2><ul class="lessons">''' + ''.join(links[k] for k in REFERENCES) + '''</ul>
    <h2>数据与登录配置</h2><p>爬虫教程保留雷军公开微博前3页的请求、解析与采集示范输出，便于对照操作和结果；
    公开源码与无需密码的教程下载包不包含课堂数据、个人Cookie或.env登录配置。</p>
    <p>本课程学生和教师可下载AES-256加密的完整资料包，解压密码由教师在课堂提供。
    请完整解压并保留目录结构：8本Notebook（6本主课、2本补充）、配套资源、环境配置和数据均已放好，
    数据位于<code>tutorials/data/posts_two_weeks.parquet</code>，小CSV读写示例位于同目录；行政边界和天气缓存位于<code>tutorials/data/spatial/</code>。
    系统解压工具若不支持AES加密ZIP，请使用<a href="https://www.7-zip.org/download.html">7-Zip</a>或其他支持AES-256 ZIP的工具。</p>
    <p id="classroom-window">含数据资料包分享至2026年10月25日23:59:59（北京时间）。
    密码不能阻止取得资料后再次转发；已下载副本也不会自动失效。
    下载和使用前请阅读<a href="tutorials/DATA_USE_TERMS.md">课堂数据使用与有限分享声明</a>，仅限本课程教学与作业，不得擅自转载或再分发。</p>
    <p>爬虫练习使用本地HTML；
    学生登录 <a href="https://weibo.cn/">weibo.cn</a> 后，在本机Notebook的代码格中填写自己的 Cookie，
    或在 <code>tutorials/.env</code> 中设置 <code>WEIBO_COOKIE</code>，两者任选其一；
    课堂先检查第一页，再读取该月份前3页。</p>

    </main><script>
    if (Date.now() > Date.parse("''' + EXPIRES_AT + '''")) {
      const link = document.getElementById('classroom-download');
      link.removeAttribute('href');
      link.textContent = '含数据资料包下载已结束';
    }
    </script></body></html>'''
    (out / 'index.html').write_text(index, encoding='utf-8')
    print(f'静态页面已生成：{len(TITLES)}本教程、HTML例子、雷军30条展示样本；目录 {out.name}')


if __name__ == '__main__':
    assert (Path(sys.prefix) / 'conda-meta').exists() or sys.prefix != sys.base_prefix, '请选择安装课程依赖的 Conda 或 venv 内核'
    root = Path(__file__).resolve().parents[1]
    build(root)
