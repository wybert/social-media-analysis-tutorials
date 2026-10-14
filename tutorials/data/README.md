# 课堂数据由教师另行提供

公开仓库不包含本课原始微博数据、个人采集输出或原始数据的汇总文件。
爬虫教程另保留雷军公开微博前3页的30条展示样本。
请将教师提供的 `posts_two_weeks.parquet` 放在此目录，不提交GitHub。
Pandas教程还读取同源的8行小文件 `posts_preview.csv`，也由教师另行提供，不公开。
Notebook从tutorials目录启动时使用相对路径 `data/posts_two_weeks.parquet`；
从仓库根目录启动时使用 `tutorials/data/posts_two_weeks.parquet`。
