#!/usr/bin/env python3
"""journal.py — TurboKain science journal backend (LLM memory layer).

Markdown files are source of truth (git-tracked):
    journal/<target>/YYYY-MM-DD_<slug>.md   (YAML frontmatter + body)

`journal/_index.db` (SQLite FTS5, gitignored, regenerable) indexes them for
`search`. The .pi extension `turbokain-journal` wraps this CLI
(binary-wrapping pattern, same as `tk db`).

Schema (frontmatter keys):
    target (required), date (required), author (required),
    campaign, disposition, coverage, instruments (csv/list),
    eirp_floor_w (float), tags (csv/list), verdict,
    sky_row, reports (csv), related (csv)

Commands:
    write    --target T --title S --body MD [--disposition D ...]
    read     <path>
    list     [--target T] [--tag G] [--disposition D]
    search   [--text Q] [--target T] [--tag G] [--disposition D]
             [--instrument I] [--limit N]
    ingest   [--full]
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JOURNAL_DIR = os.path.join(ROOT, "journal")
INDEX_DB = os.path.join(JOURNAL_DIR, "_index.db")

REQUIRED = ("target", "title")  # date/author auto-default (today/agent)
KNOWN = (
    "target", "date", "author", "campaign", "disposition", "coverage",
    "instruments", "eirp_floor_w", "tags", "verdict",
    "sky_row", "reports", "related",
)


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:64] or "entry"


def split_frontmatter(text: str):
    """Return (meta dict, body str). Frontmatter is a simple `key: value` block."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        if k in KNOWN:
            meta[k] = v.strip()
    return meta, body


def as_list(v: str) -> str:
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
    parts = [p.strip().strip("'\"") for p in v.split(",")]
    return ",".join(p for p in parts if p)


def connect() -> sqlite3.Connection:
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    con = sqlite3.connect(INDEX_DB)
    con.execute(
        """CREATE TABLE IF NOT EXISTS entries(
        path TEXT PRIMARY KEY, target TEXT, date TEXT, author TEXT,
        campaign TEXT, disposition TEXT, coverage TEXT, instruments TEXT,
        eirp_floor_w REAL, tags TEXT, verdict TEXT, title TEXT, body TEXT)"""
    )
    con.execute(
        """CREATE VIRTUAL TABLE IF NOT EXISTS journal_fts
        USING fts5(path, title, body, tags)"""
    )
    return con


def ingest_file(con: sqlite3.Connection, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    meta, body = split_frontmatter(text)
    rel = os.path.relpath(path, JOURNAL_DIR).replace(os.sep, "/")
    title = os.path.splitext(os.path.basename(rel))[0]
    try:
        eirp = float(meta.get("eirp_floor_w", "") or 0) or None
    except ValueError:
        eirp = None
    row = (
        rel, meta.get("target", ""), meta.get("date", ""),
        meta.get("author", ""), meta.get("campaign", ""),
        meta.get("disposition", ""), meta.get("coverage", ""),
        as_list(meta.get("instruments", "")), eirp,
        as_list(meta.get("tags", "")), meta.get("verdict", ""),
        title, body,
    )
    con.execute("DELETE FROM entries WHERE path=?", (rel,))
    con.execute(
        """INSERT INTO entries(path,target,date,author,campaign,disposition,
        coverage,instruments,eirp_floor_w,tags,verdict,title,body)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        row,
    )
    con.execute("DELETE FROM journal_fts WHERE path=?", (rel,))
    con.execute(
        "INSERT INTO journal_fts(path,title,body,tags) VALUES(?,?,?,?)",
        (rel, title, body, as_list(meta.get("tags", ""))),
    )


def cmd_write(a: argparse.Namespace) -> int:
    missing = [k for k in REQUIRED if not getattr(a, k, None)]
    if missing:
        print(f"journal write: missing required field(s): {', '.join(missing)}", file=sys.stderr)
        return 2
    target = a.target.strip().lower().replace(" ", "-")
    day = a.date or datetime.date.today().isoformat()
    a.date = day
    if not a.author:
        a.author = "agent"
    slug = slugify(a.title)
    tdir = os.path.join(JOURNAL_DIR, target)
    os.makedirs(tdir, exist_ok=True)
    fname = f"{day}_{slug}.md"
    fpath = os.path.join(tdir, fname)
    if os.path.exists(fpath) and not a.overwrite:
        print(f"journal write: exists (use --overwrite): journal/{target}/{fname}", file=sys.stderr)
        return 1
    lines = ["---"]
    for k in KNOWN:
        v = getattr(a, k, None)
        if v:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(a.body or "")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    con = connect()
    ingest_file(con, fpath)
    con.commit()
    con.close()
    print(f"wrote journal/{target}/{fname}")
    return 0


def cmd_ingest(a: argparse.Namespace) -> int:
    con = connect()
    if a.full:
        con.execute("DELETE FROM entries")
        con.execute("DELETE FROM journal_fts")
    n = 0
    for dirpath, _dirs, files in os.walk(JOURNAL_DIR):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            ingest_file(con, os.path.join(dirpath, fn))
            n += 1
    con.commit()
    con.close()
    print(f"ingested {n} entries -> journal/_index.db")
    return 0


def _filters(a: argparse.Namespace):
    where = []
    params: list = []
    if getattr(a, "target", None):
        where.append("e.target=?")
        params.append(a.target.strip().lower())
    if getattr(a, "tag", None):
        where.append("e.tags LIKE ?")
        params.append(f"%{a.tag}%")
    if getattr(a, "disposition", None):
        where.append("e.disposition=?")
        params.append(a.disposition)
    if getattr(a, "instrument", None):
        where.append("e.instruments LIKE ?")
        params.append(f"%{a.instrument}%")
    return where, params


def fts_escape(text: str) -> str:
    """Quote user text as an FTS5 phrase so hyphens/quotes can't break MATCH."""
    return '"' + text.replace('"', '""') + '"'


def cmd_search(a: argparse.Namespace) -> int:
    con = connect()
    where, params = _filters(a)
    if a.text:
        q = "SELECT e.path,e.target,e.date,e.disposition,e.tags,"
        q += "snippet(journal_fts,2,'[',']','...',24) FROM journal_fts f JOIN entries e ON e.path=f.path"
        w = ["journal_fts MATCH ?"]
        p = [fts_escape(a.text)]
        if where:
            w += [x.replace("e.", "e.") for x in where]
            p += params
        q += " WHERE " + " AND ".join(w)
    else:
        q = "SELECT path,target,date,disposition,tags,substr(body,1,160) FROM entries e"
        p = params
        if where:
            q += " WHERE " + " AND ".join(where)
    q += " ORDER BY date DESC LIMIT ?"
    p = p + [min(max(a.limit or 25, 1), 200)]
    try:
        rows = con.execute(q, p).fetchall()
    except sqlite3.OperationalError as e:
        print(f"journal search: query failed ({e}); run `journal ingest --full` first", file=sys.stderr)
        return 1
    con.close()
    if not rows:
        print("no matching entries")
        return 0
    for path, target, date, disp, tags, snip in rows:
        snip = " ".join((snip or "").split())
        print(f"{path} | {target} | {date} | {disp} | [{tags}]")
        if snip:
            print(f"  ...{snip}")
    print(f"-- {len(rows)} row(s)")
    return 0


def cmd_list(a: argparse.Namespace) -> int:
    con = connect()
    where, params = _filters(a)
    q = "SELECT path,target,date,disposition,tags FROM entries e"
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY date DESC, path ASC"
    rows = con.execute(q, params).fetchall()
    con.close()
    for path, target, date, disp, tags in rows:
        print(f"{path} | {target} | {date} | {disp} | [{tags}]")
    print(f"-- {len(rows)} row(s)")
    return 0


def cmd_read(a: argparse.Namespace) -> int:
    p = a.path
    if not os.path.isabs(p):
        rel = p.replace("\\", "/")
        if rel == "journal" or rel.startswith("journal/"):
            rel = rel[len("journal/"):]
        p = os.path.join(JOURNAL_DIR, rel)
    if not os.path.exists(p):
        print(f"journal read: not found: {a.path}", file=sys.stderr)
        return 1
    with open(p, "r", encoding="utf-8") as f:
        sys.stdout.write(f.read())
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="journal")
    sub = ap.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("write")
    w.add_argument("--target", required=True)
    w.add_argument("--title", required=True)
    w.add_argument("--body", default="")
    w.add_argument("--date")
    w.add_argument("--author", default="agent")
    for k in ("campaign", "disposition", "coverage", "instruments",
              "eirp_floor_w", "tags", "verdict", "sky_row",
              "reports", "related"):
        w.add_argument("--" + k.replace("_", "-"), dest=k, default="")
    w.add_argument("--overwrite", action="store_true")
    w.set_defaults(fn=cmd_write)

    r = sub.add_parser("read")
    r.add_argument("path")
    r.set_defaults(fn=cmd_read)

    l = sub.add_parser("list")
    l.add_argument("--target", default="")
    l.add_argument("--tag", default="")
    l.add_argument("--disposition", default="")
    l.set_defaults(fn=cmd_list)

    s = sub.add_parser("search")
    s.add_argument("--text", default="")
    s.add_argument("--target", default="")
    s.add_argument("--tag", default="")
    s.add_argument("--disposition", default="")
    s.add_argument("--instrument", default="")
    s.add_argument("--limit", type=int, default=25)
    s.set_defaults(fn=cmd_search)

    i = sub.add_parser("ingest")
    i.add_argument("--full", action="store_true")
    i.set_defaults(fn=cmd_ingest)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
