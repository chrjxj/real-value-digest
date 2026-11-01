"""Stage repository articles/assets and generate the home page without modifying sources."""
from pathlib import Path
import re
import shutil
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / ".build" / "docs"
EXCLUDED = {".git", ".github", ".venv", ".build", "site", "scripts", "node_modules", "__pycache__"}
ASSETS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf", ".xlsx", ".csv", ".mp4"}
SKIP = {"README.md", "PUBLISHING.md", "AGENTS.md"}

def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    articles = []
    for source in sorted(ROOT.rglob("*")):
        relative = source.relative_to(ROOT)
        if any(part.startswith(".") or part in EXCLUDED for part in relative.parts):
            continue
        if not source.is_file() or source.is_symlink():
            continue
        if source.suffix.lower() not in ASSETS | {".md"}:
            continue
        if relative.as_posix() in SKIP:
            continue
        if relative.as_posix() == "index.md":
            raise SystemExit("Root index.md is reserved for the generated index; move it into an article folder.")
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if source.suffix.lower() == ".md":
            match = re.search(r"^#\s+(.+)$", source.read_text(encoding="utf-8"), re.MULTILINE)
            title = match.group(1).strip() if match else source.stem
            title = title.replace("[", "\\[").replace("]", "\\]")
            language = " · 中文" if ".zh-CN." in source.name else " · English" if ".en." in source.name else ""
            articles.append((relative, title + language))
    lines = ["# 投资研究与市场周报", "", "按目录浏览研究文档与中英文市场周报。可使用顶部搜索查找全文。", ""]
    groups = {}
    for relative, title in articles:
        groups.setdefault(relative.parent.as_posix(), []).append((relative, title))
    for group, entries in sorted(groups.items()):
        lines += ["## " + ("其他文章" if group == "." else group), ""]
        for relative, title in sorted(entries, key=lambda entry: entry[0].as_posix(), reverse=True):
            lines.append(f"- [{title}]({quote(relative.as_posix(), safe='/')})")
        lines.append("")
    if not articles:
        lines += ["暂无文章。将 Markdown 文件放入仓库后提交即可。", ""]
    (DEST / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Prepared {len(articles)} articles in {DEST}")

if __name__ == "__main__":
    main()
