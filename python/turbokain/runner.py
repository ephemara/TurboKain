"""runner — invoke a Kain exe, capture the receipt.

Kain tools are plain native processes with a stable stdout contract and a
``receipt=PASS`` / ``verdict=...`` line. We wrap them, never re-implement them.
Exit codes matter most: 0 pass, non-zero is a hard fail (a few tools return 0
on a usage message — treat empty input as user error, not proof).
"""

from __future__ import annotations

import os
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from .registry import Registry, Tool


# --- repo discovery --------------------------------------------------------
def repo_root(start: Path | None = None) -> Path:
    """Walk up until we find this repo's markers."""
    here = (start or Path(__file__)).resolve()
    for cand in [here, *here.parents]:
        if (cand / "AGENTS.md").exists() and (cand / "catalog.tsv").exists():
            return cand
    # fallback: python/turbokain/ -> repo root is two up
    return Path(__file__).resolve().parents[2]


def tool_env(root: Path, data_dir: str | None = None) -> dict[str, str]:
    env = dict(os.environ)
    # Kain runtime discovery — never rewrite the toolchain, just be explicit.
    env.setdefault("KAIN_HOME", str(Path(os.environ.get("KAIN_HOME", r"D:\kain\.kain"))))
    if data_dir:
        env["SETIYETI_DATA"] = data_dir
    return env


# --- receipts --------------------------------------------------------------
VERDICT_RE = re.compile(
    r"\b(PASS|FAIL|CLEAN|WATCH|STRONG|DETECTED|UNDETECTED|QUARANTINE|"
    r"INTERESTING|ARTIFACT-[A-Z]+|XENO-[A-Z]+|CANDIDATE|TERRESTRIAL)\b"
)


def scan_verdicts(text: str) -> list[str]:
    """Heuristic verdict tokens from stdout/md (order-preserving, deduped)."""
    out: list[str] = []
    for m in VERDICT_RE.finditer(text):
        v = m.group(1)
        if v not in out:
            out.append(v)
    return out


def receipt_pass(text: str) -> bool | None:
    """``receipt=PASS`` / ``--prove`` summary. None when the tool has no marker."""
    if re.search(r"receipt\s*=\s*PASS", text, re.I):
        return True
    if re.search(r"receipt\s*=\s*FAIL", text, re.I):
        return False
    return None


@dataclass
class RunResult:
    tool: str
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str
    seconds: float
    cwd: Path
    outputs: list[Path] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    @property
    def verdicts(self) -> list[str]:
        return scan_verdicts(self.stdout + "\n" + self.stderr)

    @property
    def receipt(self) -> bool | None:
        return receipt_pass(self.stdout + "\n" + self.stderr)

    def tail(self, n: int = 12) -> str:
        lines = [ln for ln in (self.stdout or "").splitlines() if ln.strip()]
        return "\n".join(lines[-n:])


def find_core_exe(root: Path) -> Path | None:
    for cand in [root / "core.exe", root / "kain" / "core.exe", root / "kain" / "core" / "core.exe"]:
        if cand.exists():
            return cand
    return None


def run_tool(
    tool: Tool,
    args: Sequence[str] = (),
    *,
    root: Path,
    cwd: Path | None = None,
    data_dir: str | None = None,
    timeout: float | None = None,
    expect_outputs: Sequence[Path] = (),
) -> RunResult:
    exe = tool.resolve(root)
    if exe.exists():
        argv = [str(exe), *[str(a) for a in args]]
    else:
        core_exe = find_core_exe(root)
        if core_exe is not None:
            argv = [str(core_exe), tool.name, *[str(a) for a in args]]
        else:
            raise FileNotFoundError(
                f"{tool.name}: exe missing at {exe} and core.exe not found — build it first "
                f"(cd {exe.parent} && kain build {exe.stem}.kn --target llvm)"
            )
    t0 = time.perf_counter()
    proc = subprocess.run(
        argv,
        cwd=str(cwd or root),
        env=tool_env(root, data_dir),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    dt = time.perf_counter() - t0
    outputs = [Path(p) for p in expect_outputs if Path(p).exists()]
    return RunResult(
        tool=tool.name,
        argv=argv,
        returncode=proc.returncode,
        stdout=proc.stdout or "",
        stderr=proc.stderr or "",
        seconds=dt,
        cwd=Path(cwd or root),
        outputs=outputs,
    )


def run_passthrough(
    tool: Tool,
    args: Sequence[str],
    *,
    root: Path,
    data_dir: str | None = None,
) -> int:
    """Run a tool with inherited stdio (interactive / heavy scans)."""
    exe = tool.resolve(root)
    if exe.exists():
        argv = [str(exe), *[str(a) for a in args]]
    else:
        core_exe = find_core_exe(root)
        if core_exe is not None:
            argv = [str(core_exe), tool.name, *[str(a) for a in args]]
        else:
            print(f"tk: {tool.name}: exe missing at {exe} and core.exe not found", file=sys.stderr)
            return 127
    return subprocess.call(argv, cwd=str(root), env=tool_env(root, data_dir))


def run_selftest(
    tool: Tool,
    *,
    root: Path,
    data_dir: str | None = None,
    timeout: float | None = 600.0,
) -> RunResult:
    """Run the tool's built-in prove harness (or its no-argv self-check)."""
    if tool.selftest is None:
        # No flag: the tool proves by running with known data. We still run it
        # with no argv so the caller sees the usage/self-check banner.
        args: list[str] = []
    else:
        args = list(tool.selftest)
    return run_tool(tool, args, root=root, data_dir=data_dir, timeout=timeout)


# --- provenance ------------------------------------------------------------
def git_rev(root: Path) -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            or "unknown"
        )
    except Exception:
        return "unknown"


def host_info() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "node": platform.node(),
    }
