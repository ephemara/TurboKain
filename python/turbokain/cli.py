"""tk — unified CLI over the TurboKain Kain exes.

    tk list                      what exes we can drive, and their catalog status
    tk prove [TOOL ...]          run the built-in prove harness on each exe
    tk run TOOL [args ...]       pass-through exec (inherit stdio)
    tk scan INPUT [options]      unified sweep -> reports/<date>_<tag>_scan/
    tk doctor                    environment + registry drift check
    tk catalog                   show catalog.tsv rows (status/prove/receipt)

stdlib only. See README.md.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .registry import load_registry
from .runner import repo_root, run_passthrough, run_selftest
from .scan import F32_DETECTORS, ScanPlan, default_workdir, run_scan
from . import db as dbmod


# --- pretty ----------------------------------------------------------------
def _c(code: str, text: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


GREEN, RED, YEL, DIM, BOLD = "32", "31", "33", "2", "1"

# registry aliases — never double-count these in listings
ALIASES = {"fam", "boxcar"}


def _fmt_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "  ".join("-" * w for w in widths)
    body = "\n".join(
        "  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)) for r in rows
    )
    return f"{_c(BOLD, line)}\n{sep}\n{body}"


def _catalog_rows(root: Path) -> dict[str, dict[str, str]]:
    path = root / "catalog.tsv"
    if not path.exists():
        return {}
    with open(path, newline="", encoding="utf-8") as fh:
        return {
            row.get("tool", ""): row
            for row in csv.DictReader(fh, delimiter="\t")
            if row.get("tool")
        }


# --- commands --------------------------------------------------------------
def cmd_list(args: argparse.Namespace) -> int:
    root = repo_root()
    reg = load_registry(root)
    cat = _catalog_rows(root)
    rows = []
    for name in reg.names():
        if name in ALIASES:
            continue  # aliases
        tool = reg.tools[name]
        row = cat.get(tool.name, {})
        status = row.get("status", "-")
        prove = "yes" if tool.selftest is not None else ("run" if tool.selftest == () else "manual")
        rows.append([name, tool.kind, tool.input_kind, prove, status, tool.exe])
    print(_fmt_table(["tool", "kind", "input", "self-test", "catalog", "exe"], rows))
    if reg.missing:
        print(_c(YEL, f"\nnot built: {', '.join(reg.missing)}"))
    if reg.unregistered:
        print(_c(DIM, f"unregistered exes: {', '.join(p.name for p in reg.unregistered)}"))
    print(f"\nroot: {root}")
    return 0


def cmd_prove(args: argparse.Namespace) -> int:
    root = repo_root()
    reg = load_registry(root)
    names = args.tools or [n for n in reg.names() if n not in ALIASES]
    failures = 0
    rows = []
    for name in names:
        try:
            tool = reg.get(name)
        except KeyError:
            rows.append([name, "UNKNOWN", "-", "-", "-"])
            failures += 1
            continue
        if tool.selftest is None:
            rows.append([name, _c(DIM, "manual"), "-", "-", "no self-test flag"])
            continue
        res = run_selftest(tool, root=root, data_dir=args.data_dir, timeout=args.timeout)
        rcpt = res.receipt
        if rcpt is True or (rcpt is None and res.returncode == 0 and "FAIL" not in res.stdout.upper()):
            status = _c(GREEN, "PASS")
        else:
            status = _c(RED, "FAIL")
            failures += 1
        verdicts = ",".join(res.verdicts) or "-"
        rows.append([
            name, status, f"{res.seconds:.2f}s", f"exit={res.returncode}",
            (verdicts + (f" receipt={rcpt}" if rcpt is not None else "")),
        ])
        if args.verbose:
            print(f"\n--- {name} ---")
            print(res.tail(20))
    print(_fmt_table(["tool", "result", "time", "exit", "verdicts"], rows))
    if failures:
        print(_c(RED, f"\n{failures} self-test(s) failed"))
        return 1
    print(_c(GREEN, "\nall self-tests passed"))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    root = repo_root()
    reg = load_registry(root)
    try:
        tool = reg.get(args.tool)
    except KeyError as exc:
        print(f"tk: {exc}", file=sys.stderr)
        return 2
    return run_passthrough(tool, args.args, root=root, data_dir=args.data_dir)


def _parse_ints(spec: str) -> list[int]:
    return [int(x.strip()) for x in spec.split(",") if x.strip() != ""]


def cmd_scan(args: argparse.Namespace) -> int:
    root = repo_root()
    reg = load_registry(root)
    inp = Path(args.input)
    if not inp.is_absolute():
        inp = (root / inp).resolve()
    tag = args.tag or inp.stem
    workdir = Path(args.work) if args.work else default_workdir(root, tag)
    if not workdir.is_absolute():
        workdir = (root / workdir).resolve()
    tools = args.tools.split(",") if args.tools else list(F32_DETECTORS)
    plan = ScanPlan(
        input=inp,
        workdir=workdir,
        tools=[t.strip() for t in tools if t.strip()],
        chans=_parse_ints(args.chan),
        pols=_parse_ints(args.pol),
        blocks=args.blocks,
        fs=args.fs,
        data_dir=args.data_dir,
        tag=tag,
        timeout=args.timeout,
    )
    if args.dry_run:
        print(f"input : {plan.input}")
        print(f"workdir: {plan.workdir}")
        print(f"chans : {plan.chans}  pols: {plan.pols}  blocks: {plan.blocks}")
        print(f"tools : {', '.join(plan.tools)}")
        return 0
    print(_c(BOLD, f"tk scan -> {workdir}"))
    manifest = run_scan(plan, reg, root)
    print(f"stages : {len(manifest['stages'])}")
    print(f"summary: {manifest['summary']}")
    print(f"failures: {len(manifest['failures'])}")
    for row in manifest["failures"]:
        print(_c(RED, f"  {row['tool']} ch={row['chan']} pol={row['pol']} exit={row['exit']}"))
    return 1 if manifest["failures"] else 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root = repo_root()
    reg = load_registry(root)
    import os

    print(_c(BOLD, "tk doctor"))
    print(f"root        : {root}")
    print(f"exes found  : {len([n for n in reg.names() if n not in ALIASES])}")
    if reg.missing:
        print(_c(YEL, f"not built   : {', '.join(reg.missing)}"))
    if reg.unregistered:
        print(_c(YEL, f"unregistered: {', '.join(p.name for p in reg.unregistered)}"))
    for var in ("KAIN_HOME", "KAIN_STDLIB_PATH", "KAIN_RUNTIME_LIB_PATH", "SETIYETI_DATA"):
        val = os.environ.get(var)
        print(f"{var:20}: {val or _c(DIM, '(unset)')}")
    cat = _catalog_rows(root)
    reg_names = {t.name for t in reg.tools.values()}
    missing_rows = sorted(n for n in reg.tools if n not in ALIASES and n not in cat)
    if missing_rows:
        print(_c(YEL, f"no catalog row: {', '.join(missing_rows)}"))
    return 0


def cmd_catalog(args: argparse.Namespace) -> int:
    root = repo_root()
    cat = _catalog_rows(root)
    if not cat:
        print("no catalog.tsv", file=sys.stderr)
        return 1
    rows = []
    for name, row in cat.items():
        rows.append([
            name, row.get("kind", "-"), row.get("status", "-"),
            (row.get("prove", "") or "-")[:48],
            (row.get("receipt", "") or "-")[:48],
        ])
    print(_fmt_table(["tool", "kind", "status", "prove", "receipt"], rows))
    sky = root / "sky_catalog.tsv"
    if sky.exists():
        print()
        print("SKY - sky_catalog.tsv (target | coverage | disposition):")
        srows = []
        for line in sky.read_text(encoding="utf-8").splitlines()[1:]:
            if not line.strip():
                continue
            f = line.split("\t")
            f += ["-"] * (12 - len(f))
            srows.append([f[0], f[6], f[8]])
        print(_fmt_table(["target", "coverage", "disposition"], srows))
    return 0


# --- db -------------------------------------------------------------------
def _db_path(root, override):
    from pathlib import Path as _P

    return _P(override) if override else (root / dbmod.DB_NAME)


def cmd_db_ingest(args) -> int:
    import time as _t

    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    dbmod.init_db(con)
    t0 = _t.time()

    def progress(done, total, secs):
        print(f"  ... {done}/{total} files ({secs:.0f}s)", flush=True)

    try:
        stats = dbmod.ingest_reports(root, con, subpath=args.path,
                                     full=args.full, progress=progress)
    except FileNotFoundError as exc:
        print(f"tk db: {exc}", file=sys.stderr)
        return 2
    dt = _t.time() - t0
    tot_f = sum(f for f, _ in stats.values())
    tot_r = sum(r for _, r in stats.values())
    if args.json:
        import json as _json
        print(_json.dumps({"files": tot_f, "rows": tot_r, "seconds": round(dt, 1),
                           "by_kind": {k: {"files": f, "rows": r}
                                         for k, (f, r) in stats.items()}}))
        return 0
    print(f"ingested {tot_f} files -> {tot_r} rows in {dt:.1f}s")
    for kind in sorted(stats):
        f, r = stats[kind]
        print(f"  {kind:16} files={f:<7} rows={r}")
    print(f"db: {_db_path(root, args.db)}")
    return 0


def cmd_db_stats(args) -> int:
    import json as _json

    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    try:
        s = dbmod.compute_stats(con)
    except Exception as exc:  # empty / missing schema
        print(f"tk db: {exc} (run `tk db ingest` first)", file=sys.stderr)
        return 1
    if args.json:
        print(_json.dumps(s, indent=1, default=str))
    else:
        print(dbmod.format_stats(s))
    return 0



def cmd_db_query(args) -> int:
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    sql = args.sql.strip()
    if not sql.lower().lstrip("(").startswith("select"):
        print("tk db query: SELECT only (read-only warehouse)", file=sys.stderr)
        return 2
    try:
        cols, rows = dbmod.run_query(con, sql, limit=args.limit)
    except Exception as exc:
        print(f"tk db query: {exc}", file=sys.stderr)
        return 1
    print("\t".join(cols))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))
    if len(rows) == args.limit:
        print(f"-- capped at {args.limit} rows (use --limit N) --")
    return 0


def cmd_db_hits(args) -> int:
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    try:
        rows = dbmod.top_hits(con, min_sigma=args.min_sigma,
                              verdict=args.verdict, limit=args.limit)
    except Exception as exc:
        print(f"tk db: {exc} (run `tk db ingest` first)", file=sys.stderr)
        return 1
    if not rows:
        print("no hits above gate")
        return 0
    cols = list(rows[0].keys())
    print("\t".join(cols))
    for r in rows:
        print("\t".join("" if r[c] is None else str(r[c]) for c in cols))
    return 0


def cmd_db_search(args) -> int:
    import json as _json
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    tables = [t.strip() for t in args.tables.split(",") if t.strip()] if args.tables else None
    filters = {
        "verdict": args.verdict,
        "min_score": args.min_score,
        "max_score": args.max_score,
        "tool": args.tool,
        "star": args.star,
        "leg": args.leg,
        "chan": args.chan,
        "freq_min": args.freq_min,
        "freq_max": args.freq_max,
        "scan_contains": args.scan,
        "source_contains": args.source,
        "text": args.text,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    try:
        res = dbmod.search_tables(con, filters, tables=tables,
                                  limit=args.limit, offset=args.offset,
                                  order=args.order)
    except Exception as exc:
        print(f"tk db search: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(_json.dumps(res, indent=1, default=str))
        return 0
    print(f"total={res['total']} searched=[{','.join(res['tables_searched'])}]"
          + (f" skipped=[{','.join(res['tables_skipped'])}]" if res["tables_skipped"] else ""))
    for r in res["rows"]:
        print(f"{r['table']} scan={r['scan']} score={r['score']} {r['score_unit']}"
              f" verdict={r['verdict']} freq_hz={r['freq_hz']} src={r['source']} row={r['row_id']}")
    return 0


def cmd_db_schema(args) -> int:
    import json as _json
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    try:
        print(_json.dumps(dbmod.describe_schema(con), indent=1, default=str))
    except Exception as exc:
        print(f"tk db schema: {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_db_status(args) -> int:
    import json as _json
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    try:
        st = dbmod.db_status(con, root)
    except Exception as exc:
        print(f"tk db status: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(_json.dumps(st, indent=1, default=str))
    else:
        print(f"db: {st['db_path']} ({(st['db_bytes'] or 0) / 1e6:.1f} MB)")
        print(f"scans={st['scans']} files={st['files_ledgered']} rows~{st['total_rows']} last={st['last_ingested']}")
        print(f"fresh={st['fresh']} new={st['n_new']} changed={st['n_changed']}")
        for f in st["new_files"][:20]:
            print(f"  NEW {f}")
        for f in st["changed_files"][:20]:
            print(f"  CHANGED {f}")
    return 0


def cmd_db_scan(args) -> int:
    import json as _json
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    try:
        info = dbmod.scan_info(con, args.name)
    except Exception as exc:
        print(f"tk db scan: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(_json.dumps(info, indent=1, default=str))
        return 0
    if info.get("match") is None:
        print(f"no exact match for {args.name!r}; candidates:")
        for c in info.get("candidates", [])[:20]:
            print(f"  {c}")
        return 1
    print(f"scan: {info['match']['report_dir']}")
    for t, n in sorted(info["counts"].items()):
        if n:
            print(f"  {t:12} {n}")
    print("top rows:")
    for r in info["top_rows"]:
        print(f"  {r['table']} score={r['score']} {r['score_unit']} verdict={r['verdict']} src={r['source']}")
    if info.get("notes"):
        print("notes:")
        for n in info["notes"]:
            print(f"  [{n['note_id']}] {n['note']}")
    return 0


def cmd_db_note(args) -> int:
    import json as _json
    root = repo_root()
    con = dbmod.connect(_db_path(root, args.db))
    cmd = args.note_cmd
    if cmd == "add":
        try:
            nid = dbmod.add_note(con, args.target_type, args.target_ref,
                                 args.note, author=args.author)
        except Exception as exc:
            print(f"tk db note add: {exc}", file=sys.stderr)
            return 1
        print(f"note {nid} added")
        return 0
    if cmd == "list":
        rows = dbmod.list_notes(con, target_type=args.target_type,
                                target_ref=args.target_ref, limit=args.limit)
        print(_json.dumps(rows, indent=1, default=str))
        return 0
    if cmd == "remove":
        n = dbmod.remove_note(con, args.note_id)
        print(f"removed {n}")
        return 0
    print(f"tk db note: unknown subcommand {cmd!r}", file=sys.stderr)
    return 2


# --- entry -----------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tk",
        description="TurboKain Python driver — wrap the Kain exes, harvest receipts.",
    )
    p.add_argument("--data-dir", default=None, help="sets $SETIYETI_DATA for wrapped exes")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("list", help="list driveable exes + catalog status")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("prove", help="run each exe's built-in self-test")
    sp.add_argument("tools", nargs="*", help="tool names (default: all with a self-test)")
    sp.add_argument("--timeout", type=float, default=600.0)
    sp.add_argument("-v", "--verbose", action="store_true")
    sp.set_defaults(func=cmd_prove)

    sp = sub.add_parser("run", help="pass-through exec of one exe")
    sp.add_argument("tool")
    sp.add_argument("args", nargs=argparse.REMAINDER)
    sp.set_defaults(func=cmd_run)

    sp = sub.add_parser("scan", help="unified sweep over raw/.f32")
    sp.add_argument("input")
    sp.add_argument("--chan", default="0", help="comma list, e.g. 57,60,63")
    sp.add_argument("--pol", default="0", help="comma list, e.g. 0,1,2,3")
    sp.add_argument("--blocks", type=int, default=None)
    sp.add_argument("--tools", default=None, help="comma list (default: f32 detector bundle)")
    sp.add_argument("--fs", default=None, help="sample rate passed to detectors")
    sp.add_argument("--tag", default=None)
    sp.add_argument("--work", default=None)
    sp.add_argument("--timeout", type=float, default=3600.0)
    sp.add_argument("--dry-run", action="store_true")
    sp.set_defaults(func=cmd_scan)

    sp = sub.add_parser("doctor", help="environment + registry drift")
    sp.set_defaults(func=cmd_doctor)

    sp = sub.add_parser("catalog", help="show catalog.tsv")
    sp.set_defaults(func=cmd_catalog)

    dbp = sub.add_parser("db", help="SQLite warehouse over reports/")
    dbsub = dbp.add_subparsers(dest="db_cmd", required=True)

    sp = dbsub.add_parser("ingest", help="parse reports/ into reports.db")
    sp.add_argument("path", nargs="?", default="reports")
    sp.add_argument("--db", default=None, help="db file (default: <root>/reports.db)")
    sp.add_argument("--full", action="store_true", help="drop all tables and re-parse")
    sp.add_argument("--json", action="store_true", help="machine-readable summary")
    sp.set_defaults(func=cmd_db_ingest)

    sp = dbsub.add_parser("stats", help="warehouse statistics")
    sp.add_argument("--db", default=None)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_db_stats)

    sp = dbsub.add_parser("query", help="run a SELECT and print TSV")
    sp.add_argument("sql")
    sp.add_argument("--db", default=None)
    sp.add_argument("--limit", type=int, default=200)
    sp.set_defaults(func=cmd_db_query)

    sp = dbsub.add_parser("hits", help="top evidence hits by sigma")
    sp.add_argument("--db", default=None)
    sp.add_argument("--min-sigma", type=float, default=0.0)
    sp.add_argument("--verdict", default=None)
    sp.add_argument("--limit", type=int, default=50)
    sp.set_defaults(func=cmd_db_hits)

    sp = dbsub.add_parser("search", help="multi-table fan-out search")
    sp.add_argument("--db", default=None)
    sp.add_argument("--tables", default=None, help="comma list (default: all searchable)")
    sp.add_argument("--verdict", default=None)
    sp.add_argument("--min-score", type=float, default=None)
    sp.add_argument("--max-score", type=float, default=None)
    sp.add_argument("--tool", default=None, help="evidence tool name (e.g. fam)")
    sp.add_argument("--star", default=None)
    sp.add_argument("--leg", default=None)
    sp.add_argument("--chan", type=int, default=None)
    sp.add_argument("--freq-min", type=float, default=None, help="Hz")
    sp.add_argument("--freq-max", type=float, default=None, help="Hz")
    sp.add_argument("--scan", default=None, help="substring of report_dir")
    sp.add_argument("--source", default=None, help="substring of source path")
    sp.add_argument("--text", default=None, help="free text over text columns")
    sp.add_argument("--order", default="score_desc", choices=["score_desc", "score_asc"])
    sp.add_argument("--limit", type=int, default=25)
    sp.add_argument("--offset", type=int, default=0)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_db_search)

    sp = dbsub.add_parser("schema", help="tables + columns + views as JSON")
    sp.add_argument("--db", default=None)
    sp.set_defaults(func=cmd_db_schema)

    sp = dbsub.add_parser("status", help="freshness: disk vs ledger + vitals")
    sp.add_argument("--db", default=None)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_db_status)

    sp = dbsub.add_parser("scan", help="one-scan dossier")
    sp.add_argument("name", help="report_dir or substring")
    sp.add_argument("--db", default=None)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_db_scan)

    sp = dbsub.add_parser("note", help="analyst annotations (writable layer)")
    sp.add_argument("--db", default=None)
    nsub = sp.add_subparsers(dest="note_cmd", required=True)
    np = nsub.add_parser("add", help="attach a note")
    np.add_argument("target_type", choices=list(dbmod.NOTE_TARGETS))
    np.add_argument("target_ref", help="row_id | report_dir | source | label")
    np.add_argument("note")
    np.add_argument("--author", default=None)
    np = nsub.add_parser("list", help="list notes")
    np.add_argument("--target-type", default=None)
    np.add_argument("--target-ref", default=None)
    np.add_argument("--limit", type=int, default=50)
    np = nsub.add_parser("remove", help="delete a note by id")
    np.add_argument("note_id", type=int)
    sp.set_defaults(func=cmd_db_note)
    return p


def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252; never let a glyph kill a scan.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(_c(RED, f"tk: {exc}"), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\ntk: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
