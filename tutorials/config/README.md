# 本地微博 Cookie 配置

先访问 https://weibo.cn/ 并用自己的账号登录，按爬虫 Notebook 的 Network → Headers → Request Headers 步骤取得当前请求的 Cookie。

可以运行 Notebook 中的隐藏输入配置函数，也可以复制 `weibo_cookie.example.json` 为 `weibo_cookie.local.json`：`cookie` 填自己的完整 Cookie 字符串，`user_id` 填准备采集的公开账号数字 ID。不要填 Cookie 字段名冒号，不要复制响应中的 Set-Cookie。`user_id` 是目标用户，可以与登录用户不同。

本地配置文件不上传 GitHub，不随公开教程发布。macOS/Linux 上 Notebook 保存函数将它设为仅当前用户可读写（0600）。公开模板始终保持两个空字符串。Cookie 失效后，用自己当前会话的值更新本地文件。

采集开关默认关闭；开启后只请求目标用户第1、2页，不按总页数继续遍历。
