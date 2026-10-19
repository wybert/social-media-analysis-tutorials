# 社交媒体用户行为分析：中文实操教程

公开教程材料，不包含课堂原始微博数据集、学生/教师Cookie或个人采集输出。
保留Cookie步骤标签页和雷军公开微博前3页的30条课堂展示样本。

本课程学生和教师可在[课程首页](https://wybert.github.io/social-media-analysis-tutorials/)下载含数据的加密完整资料包；解压密码由教师通过课程渠道提供，不在网页、仓库或Release说明中公布。
含数据资料包分享至2026年10月25日23:59:59（北京时间）；使用限制见[数据使用声明](tutorials/DATA_USE_TERMS.md)。

- [课程网页](https://wybert.github.io/social-media-analysis-tutorials/)
- [课前安装与运行：八个步骤](https://wybert.github.io/social-media-analysis-tutorials/#getting-started)
- [HTML示例](https://wybert.github.io/social-media-analysis-tutorials/test.html)

## 课堂主线

1. [Weibo Crawler](tutorials/01_weibo_crawler.ipynb)：请求、解析与保存雷军微博。
2. [User Behavior Analysis](tutorials/02_user_behavior_analysis.ipynb)：用户记录、内容、公开表达与城市比较；在相应步骤学习Pandas和绘图。
3. [Big Data with DuckDB](tutorials/03_big_data_with_duckdb.ipynb)：直接查询Parquet、分组汇总与大数据处理。
4. [Spatial Analysis and User Behavior](tutorials/04_spatial_user_behavior.ipynb)：矢量与栅格、空间连接、分级设色与用户位置观测。
5. [Heatwave and User Expression](tutorials/05_heatwave_user_expression.ipynb)：热相关讨论、情感变化、城市差异与四川空间分布。
6. [Spatial Big Data with DuckDB](tutorials/06_spatial_big_data_duckdb.ipynb)：空间SQL、全国网格、城市间观测联系与Lonboard。

## 按需查阅

- [Pandas Analysis](tutorials/extent/02_pandas_analysis.ipynb)
- [Plotting](tutorials/extent/03_plotting.ipynb)

第一次下午依次打开01—03，第二次下午依次打开04—06；extent中的两本教程供按需查阅，无需先完成。

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
详细步骤见[环境与运行说明](tutorials/requirements/README.md)。完整加密包已包含
`tutorials/data/posts_two_weeks.parquet`与同目录的 `posts_preview.csv`，以及`data/spatial/`下的行政边界和天气缓存；公开源码下载不含这些数据。
解压后的数据、小CSV和分析输出不提交到公开仓库。

爬虫使用 `tutorials/assets/weibo_crawler/test.html` 练习HTML，登录 https://weibo.cn/
后按Notebook中的Network → Request Headers步骤获取自己的Cookie，填写在本机Notebook代码格，
或将 `tutorials/.env.example` 复制为 `.env` 并设置 `WEIBO_COOKIE`。两者任选其一；代码格非空时优先使用代码格。
公开Notebook的Cookie为空，分享或提交前务必清空真实会话并移除采集输出。
月份循环默认关闭；开启后课堂默认每月最多3页，每次新请求间隔30秒，异常即停止。

## 网页发布

GitHub Actions在Conda环境中将经过校验的Notebook转换为静态HTML，**不会执行Notebook、读取数据或抓微博**。
发布前检查数据文件、私有Cookie、匿名记录ID和个人采集输出；只保留完全匹配固定文件的步骤界面与30条雷军展示样本。
网站入口为 `index.html`，课堂示例可直接访问 `test.html`。

参考原项目：[weiboUserCrawler](https://github.com/wybert/weiboUserCrawler)。历史截图用于讲解操作位置，不能当作当前采集结果。
