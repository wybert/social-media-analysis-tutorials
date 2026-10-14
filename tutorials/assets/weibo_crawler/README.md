# 爬虫课程图片与 HTML

| 文件 | 用途 |
|---|---|
| `monthly_crawl_flow.png` | 备用静态流程图；Notebook正文使用横向Mermaid流程图 |
| `leijun_profile_current.png` | 雷军公开用户页面，2026年10月13日截图 |
| `leijun_date_filter_current.png` | 实际日期筛选表单，示例范围为2026年9月1日至30日 |
| `leijun_month_result_current.png` | 上述月份的实际列表结果，观察正文、转发理由、互动栏和时间；截图中放大文字并限制大图片显示 |
| `cookie_steps_masked.gif` | 六步获取 Cookie 的操作示意：登录、打开 Network、刷新并选择请求、查看请求标头、复制完整值、粘贴到 Notebook；约30秒，循环播放 |
| `cookie_headers_masked.png` | Cookie 复制位置的静态示意，可停留查看 |
| `cookie_step_01_masked.png` 至 `cookie_step_06_masked.png` | 六个步骤的静态图，用于标签页视图 |
| `cookie_tabs.html` | 六个横向标签页，在同一个区域切换图片和说明；HTML、CSS及JavaScript自包含，无需联网或Python回调 |
| `2019_leijun_profile.png` | 2019年的用户页和Network操作截图，只用于定位操作位置，不代表当前布局 |
| `test.html` | 无需登录的公开教学网页，用于简短体验HTTP与HTML |
| `leijun_first3pages_preview.html` | 2026年10月14日查询雷军2026年9月微博前3页得到的30条课堂样本，预存于Notebook结果展示单元；不包含Cookie |
| `Gemini_Generated_Image_e5pqx0e5pqx0e5pq.jpeg` | 爬虫一般流程漫画，放在任务与流程图之后 |
| `Gemini_Generated_Image_83uvob83uvob83uv.jpeg` | 采集边界漫画，放在Cookie准备之前；正文补充法律名称与适用边界 |
| `Gemini_Generated_Image_8j31ik8j31ik8j31.jpeg` | 浏览器请求与HTML漫画，放在HTTP/HTML介绍之后；正文纠正404与网络失败的区别 |
| `ppt_html_source.png` / `ppt_html_browser.png` | HTML源码与浏览器显示的对照图片 |

教程中的主要图片以附件嵌入Notebook，可以随Notebook离线查看。截图不包含Cookie值。
Cookie 动图与静态图标明“操作示意”，请求头界面是示意界面，不是真实会话录屏；马赛克区域没有载入真实 Cookie。浏览器版本不同，按钮布局可能略有差别。
截图中的数字是当时页面的显示值，不作为课程分析数据；课堂结构示例也不是实际采集结果。

学生在自己的浏览器登录 `https://weibo.cn/`，通过 Network → Document请求 → Headers → Request Headers
获取自己的Cookie，填写到本机Notebook。分享Notebook前清空真实Cookie和采集输出。
