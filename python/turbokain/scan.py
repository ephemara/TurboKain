"""scan — the unified sweep driver.

One call takes an input (GUPPI ``.raw`` or a sliced ``.f32``) and runs the
detector bundle over it, collecting every stage's stdout, exit code, wall time
and output files into a single run directory:

    reports/<date>_<tag>_scan/
        manifest.json     provenance (input fingerprint, git rev, argv, host)
        summary.tsv        one row per (stream, tool) — the machine receipt
        logs/<...>.log     raw stdout+stderr per stage
        <stage outputs>    pulse.md / xeno.csv / ... as the tools wrote them

It does not re-implement detection and it does not decide dispositions — it
stages the exes and preserves the evidence. The human veto stays human.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .registry import Registry, Tool
from .runner import RunResult, host_info, git_rev, run_tool

F32_DETECTORS = [
    "sk_gate",
    "boxcar_bank",
    "fold_sum",
    "fam_god",
    "drift_hunt",
    "frame_hunt",
    "xeno_scan",
    "lag_hunt",
]


@dataclass
class ScanPlan:
    input: Path
    workdir: Path
    tools: list[str] = field(default_factory=lambda: list(F32_DETECTORS))
    chans: list[int] = field(default_factory=lambda: [0])
    pols: list[int] = field(default_factory=lambda: [0])
    blocks: int | None = None
    fs: str | None = None
    data_dir: str | None = None
    tag: str = "scan"
    timeout: float = 3600.0


def _head_sha256(path: Path, n: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read(n))
    return h.hexdigest()[:16]


def _fingerprint(path: Path) -> dict:
    st = path.stat()
    return {
        "path": str(path),
        "size": st.st_size,
        "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        "head_sha256_1MiB": _head_sha256(path),
    }


def _out_stem(workdir: Path, template: Tool, chan: int | None, pol: int | None) -> Path:
    parts = [template.stem]
    if chan is not None:
        parts.append(f"ch{chan}")
    if pol is not None:
        parts.append(f"p{pol}")
    return workdir / "_".join(parts)


def _detector_args(
    tool: Tool, inp: Path, out_stem: Path, fs: str | None
) -> list[str]:
    args: list[str] = []
    if tool.in_flag:
        args += [tool.in_flag, str(inp)]
    else:
        args += [str(inp)]
    if tool.out_flag:
        args += [tool.out_flag, str(out_stem)]
    if fs and tool.fs_flag:
        args += [tool.fs_flag, str(fs)]
    return args


def _slice_args(tool: Tool, raw: Path, chan: int, pol: int, out: Path, blocks: int | None) -> list[str]:
    args = ["--in", str(raw), "--chan", str(chan), "--pol", str(pol), "--out", str(out)]
    if blocks is not None:
        args += ["--blocks", str(blocks)]
    return args


def _write_log(workdir: Path, name: str, result: RunResult) -> Path:
    logs = workdir / "logs"
    logs.mkdir(exist_ok=True)
    path = logs / f"{name}.log"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(result.argv)}\n")
        fh.write(f"# cwd={result.cwd}  exit={result.returncode}  "
                 f"seconds={result.seconds:.3f}\n\n")
        fh.write(result.stdout)
        if result.stderr:
            fh.write("\n--- stderr ---\n")
            fh.write(result.stderr)
    return path


def run_scan(plan: ScanPlan, reg: Registry, root: Path) -> dict:
    plan.workdir.mkdir(parents=True, exist_ok=True)
    inp = plan.input
    if not inp.is_absolute():
        inp = (root / inp).resolve()
    if not inp.exists():
        raise FileNotFoundError(f"scan: input not found: {inp}")

    manifest: dict = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "tag": plan.tag,
        "git_rev": git_rev(root),
        "host": host_info(),
        "plan": {
            "input": str(inp),
            "tools": plan.tools,
            "chans": plan.chans,
            "pols": plan.pols,
            "blocks": plan.blocks,
            "fs": plan.fs,
            "workdir": str(plan.workdir),
        },
        "fingerprint": _fingerprint(inp),
        "stages": [],
    }
    rows: list[dict] = []

    suffix = inp.suffix.lower()
    is_raw = suffix in (".raw", ".fil") or suffix == ""
    streams: list[tuple[int | None, int | None, Path]] = []

    if is_raw:
        slicer = reg.get("slice")
        for chan in plan.chans:
            for pol in plan.pols:
                f32 = plan.workdir / f"ch{chan}_p{pol}.f32"
                args = _slice_args(slicer, inp, chan, pol, f32, plan.blocks)
                res = run_tool(
                    slicer, args, root=root, cwd=plan.workdir,
                    data_dir=plan.data_dir, timeout=plan.timeout,
                    expect_outputs=[f32],
                )
                log = _write_log(plan.workdir, f"slice_ch{chan}_p{pol}", res)
                manifest["stages"].append(
                    {"stage": "slice", "chan": chan, "pol": pol,
                     "argv": res.argv, "exit": res.returncode,
                     "seconds": res.seconds, "log": str(log)}
                )
                rows.append(
                    dict(chan=chan, pol=pol, tool="slice", exit=res.returncode,
                         seconds=res.seconds, receipt=res.receipt,
                         verdicts=",".join(res.verdicts),
                         outputs=str(f32) if f32.exists() else "", log=str(log))
                )
                if res.returncode != 0 or not f32.exists():
                    continue
                streams.append((chan, pol, f32))
    else:
        streams.append((None, None, inp))

    for chan, pol, f32 in streams:
        for name in plan.tools:
            try:
                tool = reg.get(name)
            except KeyError:
                rows.append(dict(chan=chan, pol=pol, tool=name, exit=127,
                                 seconds=0.0, receipt=None,
                                 verdicts="UNKNOWN-TOOL", outputs="", log=""))
                continue
            if tool.input_kind != "f32":
                rows.append(dict(chan=chan, pol=pol, tool=name, exit=0,
                                 seconds=0.0, receipt=None,
                                 verdicts="SKIPPED-NOT-F32", outputs="", log=""))
                continue
            out_stem = _out_stem(plan.workdir, tool, chan, pol)
            args = _detector_args(tool, f32, out_stem, plan.fs)
            res = run_tool(
                tool, args, root=root, cwd=plan.workdir,
                data_dir=plan.data_dir, timeout=plan.timeout,
            )
            log = _write_log(plan.workdir, f"{tool.stem}_ch{chan}_p{pol}", res)
            outs = sorted(
                str(p) for p in plan.workdir.glob(f"{out_stem.name}*")
            )
            manifest["stages"].append(
                {"stage": tool.stem, "chan": chan, "pol": pol, "argv": res.argv,
                 "exit": res.returncode, "seconds": res.seconds, "log": str(log)}
            )
            rows.append(
                dict(chan=chan, pol=pol, tool=tool.stem, exit=res.returncode,
                     seconds=res.seconds, receipt=res.receipt,
                     verdicts=",".join(res.verdicts),
                     outputs=";".join(outs), log=str(log))
            )

    summary = plan.workdir / "summary.tsv"
    cols = ["chan", "pol", "tool", "exit", "seconds", "receipt", "verdicts", "outputs", "log"]
    with open(summary, "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join("" if r.get(c) is None else str(r.get(c, "")) for c in cols) + "\n")

    manifest["summary"] = str(summary)
    manifest["row_count"] = len(rows)
    manifest["failures"] = [r for r in rows if r["exit"] not in (0,)]
    (plan.workdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def default_workdir(root: Path, tag: str) -> Path:
    day = datetime.now().strftime("%Y-%m-%d")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in tag) or "scan"
    return root / "reports" / f"{day}_{safe}_scan"
