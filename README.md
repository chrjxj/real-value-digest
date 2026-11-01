# 投资研究与市场周报

本仓库使用 MkDocs Material 将 Markdown 自动生成为 HTML，通过 GitHub Actions 发布到 GitHub Pages。

网站地址：<https://chrjxj.github.io/test-markdown-site/>

## 首次启用

在仓库 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。
然后在 **Actions → Build and deploy Markdown site → Run workflow** 中选择 main 并运行。

详见 [发布与维护说明](PUBLISHING.md)。

## 更新内容

直接在现有目录（如 `Weekly Market Update/`）新增或修改 Markdown，然后提交到 main。
首页索引和侧边栏自动更新，无须手写 HTML 或维护文章清单。

## 本地预览

需要 Python 3.12：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/prepare_docs.py
python -m mkdocs serve
```

打开终端显示的本地地址。添加、删除文章或修改原文后，重新运行准备脚本。
