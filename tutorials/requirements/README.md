# 环境与运行准备

准备 Python 3.11、VS Code，以及 VS Code 的 Python 和 Jupyter 扩展。Conda 与 uv + venv 两种方式任选一种。下面的命令都从项目根目录运行；如果终端位于 `tutorials`，将配置路径中的 `tutorials/` 去掉；位于`tutorials/extent`时，配置路径使用`../requirements/`。

## 1. Conda

```sh
conda env create -f tutorials/requirements/environment.yml
conda activate user-behavior-class
```

已有课程环境需要更新时，运行：

```sh
conda env update -n user-behavior-class -f tutorials/requirements/environment.yml
```

打开 Notebook，在右上角内核选择器中选择 `user-behavior-class`。配置中的 `PYTHONNOUSERSITE=1` 避免读取本机用户目录中另行安装的同名包。

## 2. uv + venv

先按 [uv 官方安装说明](https://docs.astral.sh/uv/getting-started/installation/)安装 uv，再运行：

```sh
uv venv --python 3.11 .venv
uv pip install --python .venv -r tutorials/requirements/requirements.txt
```

`--python .venv` 将依赖安装到指定虚拟环境，不受终端中其他已激活环境影响。在 VS Code 的内核选择器中选择“Python Environments”，再选择项目的 `.venv`：macOS/Linux 为 `.venv/bin/python`，Windows 为 `.venv\Scripts\python.exe`。依赖文件已包含 `ipykernel`。

如果使用 JupyterLab，可直接用虚拟环境的解释器启动：

```sh
# macOS / Linux
.venv/bin/python -m jupyterlab
```

```powershell
# Windows PowerShell
.\.venv\Scripts\python.exe -m jupyterlab
```

已有其他 venv 时，也可用 `uv pip install --python 虚拟环境目录 -r tutorials/requirements/requirements.txt` 安装同一套依赖。

## 3. 数据与 Notebook 操作

- 在 VS Code 打开整个课程目录，保留 `tutorials` 及其 `extent`、`assets`、`config`、`data` 子目录。课堂依次打开01爬虫、02用户行为分析、03 DuckDB；Pandas和绘图专题位于`extent`，按需查阅。
- 完整加密资料包中的 `posts_two_weeks.parquet` 与 `posts_preview.csv` 已放入 `tutorials/data/`。仅下载公开教程时，需另行取得课堂数据并放到此目录；爬虫Notebook保留雷军公开微博前3页的30条展示样本。
- 用`Shift+Enter`运行当前代码格；首次使用或重启内核后，从头按顺序执行。库、分析参数和输出目录在首次使用的步骤中引入；单独跳到后面的代码格可能缺少前面的变量。
- 单个表格放在代码格最后一行即可显示。同格显示多张表、或在分支和循环中显示结果时使用`display(...)`。
- 派生CSV和图形写入`tutorials/output/`下各教程的子目录，原始数据保留在`tutorials/data/`。
- 看到 `NameError` 时先检查前面的定义格是否已运行；看到 `ModuleNotFoundError` 时先核对所选内核和依赖安装位置。
- 修改代码后重跑相关单元格与后续依赖格。先在练习空白格作答，再展开参考答案。
- 微博月份循环默认关闭；按爬虫教程登录 `weibo.cn`，将自己的 Cookie 填到本机代码格，或将 `tutorials/.env.example` 复制为同目录的 `.env` 并设置 `WEIBO_COOKIE`。代码格非空时优先使用代码格；否则读取 `.env`；两处都为空会提示补充。先检查一页，再启动每月最多3页的课堂循环。分享 Notebook 前清空真实 Cookie 和个人采集输出，不分享 `.env`。

运行另外两本 `student_notebooks` 或 `full_notebooks` 时，需要教师提供的完整课程目录，包括 `scripts`、`data/map_assets` 和 `data/geography`。八本 `tutorials`（01—06主课与extent中的两本补充）可直接使用含数据的完整加密包运行，也可使用公开教程包与另行提供的数据。

## 4. 使用范围

环境包含 Pandas、NumPy、Matplotlib、Plotly、DuckDB、Requests、Beautiful Soup、PyArrow 和 Jupyter，以及完整课程使用的统计与地图依赖。hvPlot、Altair 是拓展介绍，需要使用时再安装。

03（DuckDB）使用JupySQL提供的`%%sql`查询单元，并通过`duckdb-engine`连接DuckDB；两者已纳入基础依赖。遇到“Cell magic %%sql not found”时，先检查所选内核和依赖，再运行03教程第4节的`%load_ext sql`与连接单元。`%%sql`通常放在代码格第一行，SQL注释使用`--`；计时时在其前面加一行`%%time`。Python显示与绘图代码放到下一格。简单图形使用`%sqlplot`，交互图使用Plotly；`%sqlplot`底层依赖Matplotlib，环境中已包含，无需直接编写Matplotlib代码。查询仍在本机执行，不需要远程数据库账号。

当前课程网页供阅读和下载，代码在本地 Python 环境执行。JupyterLite 使用浏览器内核，文件、网络请求及运行资源与本地环境不同；现有教程不作为可直接运行的 JupyterLite 版本提供。

## 5. 用户行为分析的模型选做题

02中的7.4（BERTopic主题发现）和7.5（预训练情感分类）需要额外依赖。原有课程代码不需要安装这些依赖。Conda用户可保留基础环境，另建副本：

```sh
conda create -n user-behavior-nlp --clone user-behavior-class
conda run -n user-behavior-nlp python -m pip install -r tutorials/requirements/requirements-nlp.txt
```

uv用户可运行`uv pip install --python .venv -r tutorials/requirements/requirements-nlp.txt`。切换环境后，从02的准备单元重新开始运行；主题题与情感题互不依赖。

首次加载需下载两套模型权重，建议课前完成。参考答案固定模型版本，下载后复用本机缓存，在CPU上处理300条、30条帖子；无需API Key，也不向在线推理服务发送文本。主题模型的句向量可能按编码器长度上限截断，情感题显式限制为256个token。

句向量模型使用[paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)（Apache-2.0）；情感分类模型使用[tabularisai/multilingual-sentiment-analysis](https://huggingface.co/tabularisai/multilingual-sentiment-analysis)（CC-BY-NC-4.0）。模型权重由各自模型页面提供，不随课程数据包分发。后者含中文的五级情感倾向标签，在合成文本上训练；其分数不能作为中文微博准确率或用户心理量表。

## 6. Mac与Windows

代码使用`pathlib.Path`拼接相对路径，不要求填写用户目录或盘符。保留完整文件夹结构：主讲教程支持从项目根目录或`tutorials`启动，`extent`中的专题还支持从自身目录启动。Pandas和PyArrow可以直接接收Path；DuckDB的SQL文件路径在连接文件时转换为正斜杠并转义单引号。

日期刻度使用`ZoneInfo('Asia/Shanghai')`；基础环境显式包含Python时区数据包（Conda的`python-tzdata`、pip的`tzdata`），用于没有系统IANA时区库的环境。参见[Python时区数据说明](https://docs.python.org/3.11/library/zoneinfo.html#data-sources)。Matplotlib绘图前选择当前电脑已安装的中文字体，没有匹配字体时使用英文图题；Plotly在浏览器中显示交互图。

教程按跨平台方式编写。当前运行验证在macOS的课程Conda环境完成，尚未做Windows实机整本运行验证；Windows同学应使用同一份环境配置、数据与目录结构。

## 7. 第二次下午：04—06时空分析

依次打开`04_spatial_user_behavior.ipynb`、`05_heatwave_user_expression.ipynb`和`06_spatial_big_data_duckdb.ipynb`，每本可从空内核独立运行，继续读取`tutorials/data/posts_two_weeks.parquet`。05另用`data/spatial/chengdu_weather_20220812_25.csv`的14行真实ERA5缓存；课堂不实时请求天气数据。

环境已加入GeoPandas、Shapely、pyproj与Lonboard 0.13。已有Conda环境先执行本页第1节的更新命令，安装后重启Notebook内核。uv用户重新运行第2节的依赖安装命令。

06首次执行`INSTALL spatial`需要网络，以获取与当前DuckDB匹配的扩展；`LOAD spatial`对每个新连接执行。Lonboard使用Jupyter Widget/WebGL，在VS Code安装Jupyter扩展并运行对应代码格；缺少Widget显示时先核对课程内核、重启内核并重新运行，不能仅根据静态网页判断Widget运行情况。

04使用GeoPandas的`plot()`绘制静态地图，Plotly展示交互式点线与高德瓦片；05使用GeoPlot、Cartopy绘制行政区和KDE静态图；06使用Lonboard的网格面、比例圆点和城市联系弧线。地图展示0.02度格子边界，另比较0.04度合并结果，颜色表示每格记录数。

示例通过高德栅格瓦片读取底图，不调用高德JS API，因此不需要填写JS API Key。在线底图仍需要网络；统计计算与静态图可离线完成。分级设色使用的mapclassify、05使用的GeoPlot与Cartopy、度量转换使用的xyconvert均已写入依赖配置；xyconvert为纯Python/NumPy包，通过环境配置中的pip段安装。

微博源位置已确认为GCJ-02。高德底图、原始网格和随资料提供的DataV行政边界直接叠加，不重复偏移；原始GCJ-02不强行标记EPSG:4326，因此Lonboard可能提示缺少正式CRS。需要米制度量时，先用gcj2wgs近似转换副本，再声明EPSG:4326并投影。原始数据不回写，保留高德底图与DataV边界的标注和署名。

四川省界、市州界与成都区县界已缓存在`data/spatial/boundaries/`，课堂无需实时请求边界接口。边界为学习交流参考快照，缓存日期不等于行政区划生效日期；地图底图瓦片仍需联网。
