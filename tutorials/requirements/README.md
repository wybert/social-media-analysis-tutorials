# Python 环境

在 VS Code 打开整个课程目录，然后在项目根目录的终端运行：

```sh
conda env create -f tutorials/requirements/environment.yml
conda activate user-behavior-class
```

如果终端已经位于 `tutorials` 目录，配置文件路径改为 `requirements/environment.yml`。

打开 Notebook，点击右上角的内核选择器，选择 `user-behavior-class` 环境。VS Code 需要安装 Python 和 Jupyter 扩展；安装 Conda 包不会自动安装这些编辑器扩展。

环境包含网页请求与解析、Pandas、Matplotlib、Plotly、DuckDB、空间分析示例和 Jupyter 所需的依赖。hvPlot 和 Altair 是绘图库拓展介绍，未列入默认环境。

配置中的 `PYTHONNOUSERSITE=1` 让环境不读取本机用户目录中另行安装的 Python 包，避免同名包互相干扰。

课堂数据由教师另行提供，放入 `tutorials/data/`。微博采集需要填写自己的登录配置，默认关闭。
