# 社交媒体用户行为分析：中文实操教程

公开教程材料，不包含微博数据集、学生/教师Cookie或Notebook运行输出。

- [课程网页](https://wybert.github.io/social-media-analysis-tutorials/)
- [HTML示例](https://wybert.github.io/social-media-analysis-tutorials/test.html)
- [Weibo Crawler](tutorials/01_weibo_crawler.ipynb)：先登录weibo.cn，配置自己的Cookie，固定只采前两页；三道短练习。
- [Pandas Analysis](tutorials/02_pandas_analysis.ipynb)
- [Plotting](tutorials/03_plotting.ipynb)
- [User Behavior Analysis](tutorials/04_user_behavior_analysis.ipynb)
- [Big Data with DuckDB](tutorials/05_big_data_with_duckdb.ipynb)

## 在本机运行

```sh
conda env create -f requirements/environment.yml
conda activate user-behavior-class
```

用VS Code打开整个仓库，选择该Conda内核。分析数据由教师另行提供，放在
`tutorials/data/posts_two_weeks.parquet`；原始数据和分析输出不提交到公开仓库。

爬虫使用 `tutorials/assets/weibo_crawler/test.html` 练习HTML，登录 https://weibo.cn/
后按Notebook中的Network → Request Headers步骤获取自己的Cookie。
公开配置模板为空；生成的 `tutorials/config/weibo_cookie.local.json` 仅在本机使用并被gitignore排除。
采集默认关闭；开启后只访问第1、2页，页间30秒，异常即停止。

## 网页发布

GitHub Actions在Conda环境中将无输出Notebook转换为静态HTML，**不会执行Notebook、读取数据或抓微博**。
发布前检查数据文件、私有Cookie、匿名记录ID和运行输出；检测到这些内容会中止构建。
网站入口为 `index.html`，课堂示例可直接访问 `test.html`。

参考原项目：[weiboUserCrawler](https://github.com/wybert/weiboUserCrawler)。历史截图用于讲解操作位置，不能当作当前采集结果。
