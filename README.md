# 社交媒体用户行为分析：中文实操教程

公开教程材料，不包含微博数据集、学生/教师Cookie或分析、采集的运行输出。
仅保留内容经过校验的Cookie步骤标签页教学界面。

- [课程网页](https://wybert.github.io/social-media-analysis-tutorials/)
- [HTML示例](https://wybert.github.io/social-media-analysis-tutorials/test.html)
- [Weibo Crawler](tutorials/01_weibo_crawler.ipynb)：登录weibo.cn，在本机代码格填写自己的Cookie，按月查询雷军微博、逐页解析、合并去重并保存CSV。
- [Pandas Analysis](tutorials/02_pandas_analysis.ipynb)
- [Plotting](tutorials/03_plotting.ipynb)
- [User Behavior Analysis](tutorials/04_user_behavior_analysis.ipynb)
- [Big Data with DuckDB](tutorials/05_big_data_with_duckdb.ipynb)

## 在本机运行

```sh
conda env create -f tutorials/requirements/environment.yml
conda activate user-behavior-class
```

也可使用 uv + venv：

```sh
uv venv --python 3.11 .venv
uv pip install --python .venv -r tutorials/requirements/requirements.txt
```

用VS Code打开整个仓库，选择课程Conda环境或项目 `.venv` 内核。
详细步骤见[环境与运行说明](tutorials/requirements/README.md)。分析数据由教师另行提供，放在
`tutorials/data/posts_two_weeks.parquet`；Pandas读写练习的小文件 `posts_preview.csv` 也放在同一目录。
原始数据、小CSV和分析输出不提交到公开仓库。

爬虫使用 `tutorials/assets/weibo_crawler/test.html` 练习HTML，登录 https://weibo.cn/
后按Notebook中的Network → Request Headers步骤获取自己的Cookie，只填写在本机Notebook中。
公开Notebook的Cookie为空，分享或提交前务必清空真实会话并移除采集输出。
月份循环默认关闭；开启后按月份翻页，每次新请求间隔30秒，异常即停止。

## 网页发布

GitHub Actions在Conda环境中将经过校验的Notebook转换为静态HTML，**不会执行Notebook、读取数据或抓微博**。
发布前检查数据文件、私有Cookie、匿名记录ID和分析、采集输出；仅允许与固定HTML文件完全一致的步骤教学界面。
网站入口为 `index.html`，课堂示例可直接访问 `test.html`。

参考原项目：[weiboUserCrawler](https://github.com/wybert/weiboUserCrawler)。历史截图用于讲解操作位置，不能当作当前采集结果。
