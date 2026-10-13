# 爬虫课程图片与 HTML

| 文件 | 用途 |
|---|---|
| `monthly_crawl_flow.png` | 登录、按月翻页、解析、去重和CSV保存的流程图 |
| `leijun_profile_current.png` | 雷军公开用户页面，2026年10月13日截图 |
| `leijun_date_filter_current.png` | 实际日期筛选表单，示例范围为2026年9月1日至30日 |
| `leijun_month_result_current.png` | 上述月份的实际列表结果，观察正文、转发理由、互动栏和时间；截图中放大文字并限制大图片显示 |
| `2019_leijun_profile.png` | 2019年的用户页和Network操作截图，只用于定位操作位置，不代表当前布局 |
| `test.html` | 无需登录的公开教学网页，用于简短体验HTTP与HTML |
| `ppt_html_source.png` / `ppt_html_browser.png` | HTML源码与浏览器显示的对照图片 |

教程中的主要图片以附件嵌入Notebook，可以随Notebook离线查看。截图不包含Cookie值。
截图中的数字是当时页面的显示值，不作为课程分析数据；课堂结构示例也不是实际采集结果。

学生在自己的浏览器登录 `https://weibo.cn/`，通过 Network → Document请求 → Headers → Request Headers
获取自己的Cookie，填写到本机Notebook。分享Notebook前清空真实Cookie和采集输出。
