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
    return 0


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
