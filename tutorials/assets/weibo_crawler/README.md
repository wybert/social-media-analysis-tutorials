# 爬虫教学网页与截图

`test.html` 根据 `slides/社交媒体用户大数据分析.pptx` 第12页的记事本源码截图恢复。标题、正文、链接文字、加粗标签和结构保留；语言标记由原截图的 `cn` 修正为 `zh-CN`，链接协议由 HTTP 改为 HTTPS。使用浏览器直接打开可查看页面，在 VS Code 中打开可查看源码。

原线上地址为 `https://wybert.github.io/training/test.html`，2026-10-12 实际请求返回404。恢复后的HTML链接更新为课程站点 `https://wybert.github.io/social-media-analysis-tutorials/test.html`。本目录保留可本地打开的恢复件；PPT源码截图中的旧地址用于说明历史来源。HTML用于标签、属性与文本提取，不是新增微博数据集。

| 文件 | 来源与用途 |
|---|---|
| `ppt_html_source.png` | PPT第12页原源码截图，图像未改动 |
| `ppt_html_browser.png` | PPT第12页原浏览器截图，图像未改动 |
| `2019_leijun_profile.png` | `references/weiboUserCrawler/Peek 2019-08-23 10-33.gif` 第72帧，直接导出，不含Cookie值 |

三张图同时作为附件嵌在 `tutorials/01_weibo_crawler.ipynb`，Notebook 显示图片不依赖外部图床。2019截图只说明当时的操作位置，不保证当前布局相同；截图中的互动数量未转为课程数据。

原源码和其他动图存在硬编码或可见的旧Cookie，不复制进教学版或学生答案。真实微博解析需使用本人获得的实际页面，当前目录不包含虚构微博HTML或帖子。
