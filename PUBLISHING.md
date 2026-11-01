# 发布与维护说明

## 架构与地址

Markdown 原文 → `scripts/prepare_docs.py` → 临时文档目录 `.build/docs` → MkDocs → `site/` → GitHub Pages。

对应项目网站：<https://chrjxj.github.io/test-markdown-site/>。
这是项目站点；账号首页 `https://chrjxj.github.io/` 由另一个同名仓库控制。

原有中英文周报保持原路径。首页自动按目录分组、文件名倒序展示文章；使用日期开头可让最新周报排在前面。支持中文/英文搜索、目录、表格、代码块、手机阅读。

## 首次发布：只需设置一次

1. 打开 <https://github.com/chrjxj/test-markdown-site/settings/pages>。
2. 在 Build and deployment 的 Source 选择 **GitHub Actions**。
3. 打开 <https://github.com/chrjxj/test-markdown-site/actions>。
4. 选择 **Build and deploy Markdown site**，点击 **Run workflow**，分支选择 main。
5. 等待 build、deploy 都变绿，再访问网站。

GitHub 插件没有 Pages 管理设置接口，因此首次启用需要仓库管理员在网页上完成。无需创建 PAT 或添加 Secrets；部署使用 GitHub 自动生成的 GITHUB_TOKEN 和 OIDC。

## 日常写作

在任意普通目录添加 UTF-8 的 `.md` 文件，第一行建议使用 `# 文章标题`。
提交到 main 后自动构建和发布；Pull Request 仅执行构建检查，不发布。

例：

```text
Weekly Market Update/
  2026-11-02-market-update.zh-CN.md
  2026-11-02-market-update.en.md
  images/
    market-chart.png
```

图片使用相对路径：`![市场图表](images/market-chart.png)`。
文章间也使用相对 Markdown 路径；空格建议写为 `%20`。
脚本保留目录结构，MkDocs 将内部 Markdown 链接转换为 HTML 链接。

根目录 `index.md` 为自动首页保留名，不要创建；根目录 README.md、PUBLISHING.md、AGENTS.md 不作为文章发布。
隐藏目录、scripts、node_modules、site、构建目录被排除。
支持复制 png/jpg/jpeg/gif/svg/webp/pdf/xlsx/csv/mp4 作为资源；Excel、CSV、PDF 为下载资源，不自动转换成网页。
如需增加资源类型，修改准备脚本的 ASSETS 集合。

## 本地验证与预览

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/prepare_docs.py
python -m mkdocs build --strict
python -m mkdocs serve
```

Windows 激活命令：`.venv\\Scripts\\activate`。
原文变化后重新执行准备脚本。不要直接编辑 .build/docs 或 site；这些目录可随时重建，不应提交。

## 故障处理

- **Pages 尚未启用 / configure-pages 失败**：确认 Settings → Pages → Source 为 GitHub Actions，再手动运行工作流。
- **Actions 无法运行**：检查 Settings → Actions → General 是否允许仓库使用 Actions 和官方 actions/*。
- **deploy 等待审批**：检查 Settings → Environments → github-pages 的审批规则。
- **build 失败**：打开失败步骤；严格构建遇到无效配置、缺失文件等警告会停止，请按日志修正。
- **404**：确认 deploy 成功；使用带 /test-markdown-site/ 的完整地址，首次部署后稍候再刷新。
- **更新未出现**：确认提交到了 main，并查看对应提交的工作流是否完成。
- **更换仓库名**：同步修改 mkdocs.yml 中 site_url、repo_url 以及文档中的链接。
