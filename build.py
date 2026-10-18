#!/usr/bin/env python3
"""Generate a static site with one page per message.

Usage:  python build.py
Input:  messages.csv  (columns: slug, message)  +  templates/
Output: dist/         (upload this folder to any static host)

Each message becomes dist/<slug>/index.html, served at yoursite.com/<slug>.
"""
import csv
import html
import shutil
from pathlib import Path
from string import Template

ROOT = Path(__file__).parent
SRC = ROOT / "messages.csv"
TPL = ROOT / "templates"
OUT = ROOT / "dist"
SITE_TITLE = "Messages"


def load_messages():
    with SRC.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("message") or "").strip()]
    messages, seen = [], set()
    for i, row in enumerate(rows, start=1):
        slug = (row.get("slug") or "").strip() or str(i)
        if slug in seen:
            raise SystemExit(f"Duplicate slug in messages.csv: {slug!r}")
        seen.add(slug)
        messages.append({"slug": slug, "text": row["message"].strip()})
    return messages


def to_paragraphs(text):
    """Blank line = new paragraph; single newline = line break."""
    paras = [p.strip() for p in text.replace("\r\n", "\n").split("\n\n") if p.strip()]
    return "\n".join(
        "<p>" + html.escape(p).replace("\n", "<br>") + "</p>" for p in paras
    )


def main():
    page_tpl = Template((TPL / "page.html").read_text(encoding="utf-8"))
    index_tpl = Template((TPL / "index.html").read_text(encoding="utf-8"))
    messages = load_messages()
    total = len(messages)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(TPL / "style.css", OUT / "style.css")

    for n, m in enumerate(messages, start=1):
        prev_m = messages[n - 2] if n > 1 else None
        next_m = messages[n] if n < total else None
        prev_link = (
            f'<a href="../{prev_m["slug"]}/" rel="prev">Previous</a>'
            if prev_m else "<span></span>"
        )
        next_link = (
            f'<a href="../{next_m["slug"]}/" rel="next">Next</a>'
            if next_m else "<span></span>"
        )
        first_line = m["text"].split("\n")[0]
        description = html.escape(first_line[:150])
        page = page_tpl.substitute(
            root="../",
            site_title=html.escape(SITE_TITLE),
            title=f"Message {n}",
            description=description,
            number=n,
            total=total,
            body=to_paragraphs(m["text"]),
            prev_link=prev_link,
            next_link=next_link,
        )
        d = OUT / m["slug"]
        d.mkdir()
        (d / "index.html").write_text(page, encoding="utf-8")

    items = "\n".join(
        f'<li><a href="{m["slug"]}/">Message {n}</a></li>'
        for n, m in enumerate(messages, start=1)
    )
    (OUT / "index.html").write_text(
        index_tpl.substitute(
            root="", site_title=html.escape(SITE_TITLE), items=items, total=total
        ),
        encoding="utf-8",
    )
    print(f"Built {total} pages in {OUT}/")


if __name__ == "__main__":
    main()
