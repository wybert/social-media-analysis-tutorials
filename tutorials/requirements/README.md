# 环境与运行准备

准备 Python 3.11、VS Code，以及 VS Code 的 Python 和 Jupyter 扩展。Conda 与 uv + venv 两种方式任选一种。下面的命令都从项目根目录运行；如果终端位于 `tutorials`，将配置路径中的 `tutorials/` 去掉。

## 1. Conda

```sh
conda env create -f tutorials/requirements/environment.yml
conda activate user-behavior-class
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

- 在 VS Code 打开整个课程目录，保留 `tutorials` 及其 `assets`、`config`、`data` 子目录。
- 完整加密资料包中的 `posts_two_weeks.parquet` 与 `posts_preview.csv` 已放入 `tutorials/data/`。仅下载公开教程时，需另行取得课堂数据并放到此目录；爬虫Notebook保留雷军公开微博前3页的30条展示样本。
- 用 `Shift+Enter` 运行当前代码格；首次使用或重启内核后从初始化开始按顺序执行。
- 看到 `NameError` 时先检查前面的定义格是否已运行；看到 `ModuleNotFoundError` 时先核对所选内核和依赖安装位置。
- 修改代码后重跑相关单元格与后续依赖格。先在练习空白格作答，再展开参考答案。
- 微博月份循环默认关闭；按爬虫教程登录 `weibo.cn`，将自己的 Cookie 填到本机代码格，或将 `tutorials/.env.example` 复制为同目录的 `.env` 并设置 `WEIBO_COOKIE`。代码格非空时优先使用代码格；否则读取 `.env`；两处都为空会提示补充。先检查一页，再启动每月最多3页的课堂循环。分享 Notebook 前清空真实 Cookie 和个人采集输出，不分享 `.env`。

运行另外两本 `student_notebooks` 或 `full_notebooks` 时，需要教师提供的完整课程目录，包括 `scripts`、`data/map_assets` 和 `data/geography`。五本 `tutorials` 可直接使用含数据的完整加密包运行，也可使用公开教程包与另行提供的数据。

## 4. 使用范围

环境包含 Pandas、NumPy、Matplotlib、Plotly、DuckDB、Requests、Beautiful Soup、PyArrow 和 Jupyter，以及完整课程使用的统计与地图依赖。hvPlot、Altair 是拓展介绍，需要使用时再安装。

当前课程网页供阅读和下载，代码在本地 Python 环境执行。JupyterLite 使用浏览器内核，文件、网络请求及运行资源与本地环境不同；现有教程不作为可直接运行的 JupyterLite 版本提供。

## 5. 用户行为分析的模型选做题

04中的7.4（BERTopic主题发现）和7.5（预训练情感分类）需要额外依赖。原有课程代码不需要安装这些依赖。Conda用户可保留基础环境，另建副本：

```sh
conda create -n user-behavior-nlp --clone user-behavior-class
conda run -n user-behavior-nlp python -m pip install -r tutorials/requirements/requirements-nlp.txt
```

uv用户可运行`uv pip install --python .venv -r tutorials/requirements/requirements-nlp.txt`。切换环境后，从04的准备单元重新开始运行；主题题与情感题互不依赖。

首次加载需下载两套模型权重，建议课前完成。参考答案固定模型版本，下载后复用本机缓存，在CPU上处理300条、30条帖子；无需API Key，也不向在线推理服务发送文本。主题模型的句向量可能按编码器长度上限截断，情感题显式限制为256个token。

句向量模型使用[paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)（Apache-2.0）；情感分类模型使用[tabularisai/multilingual-sentiment-analysis](https://huggingface.co/tabularisai/multilingual-sentiment-analysis)（CC-BY-NC-4.0）。模型权重由各自模型页面提供，不随课程数据包分发。后者含中文的五级情感倾向标签，在合成文本上训练；其分数不能作为中文微博准确率或用户心理量表。
