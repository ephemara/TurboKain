"""inject_cal — §7.1 injection-recovery harness (stdlib only).

Generates small synthetic .f32 baseband files (unit-variance Gaussian noise
plus scaled signals) and runs the four TRAPPIST-1 pilot keystones behind
core.exe to measure coded-traffic response vs. SNR.

  python python/inject_cal.py [--n 1048576] [--out reports/2026-09-28_injection_cal] [--fs 2929687.5] [--quick]

Signals (real float32 time series, documented stand-ins, NOT full LDPC):
  noise      : N(0,1) only (false-alarm control)
  coded_Xdb  : BPSK +-1 with chunk-wise even parity (taps [0,7,23,41,53,61],
               parity at 63, chunk 64 -> weight-7 even dual) + N(0,1),
               signal scaled to X dB (X in -6,-3,0,+3)
  uncoded_0db: same bits WITHOUT parity enforcement (coding control)
  cw_0db     : sine at 0.13*fs, tone power = noise power (energy control)

Scale note: real GUPPI-derived .f32 spans [-128,127] with std~2 (8-bit
digitizer units), but all four keystones self-normalize (MAD/moment
units), so unit-variance synthetic noise is a valid null. Verified:
real-slice and synthetic-noise control runs must agree on CLEAN.

Runs per case (all through core.exe, exit codes recorded):
  gauss_perfection --in case --off noise_off
  ism_stamp        --in case --off noise_off
  fec_ghost        --in case --off noise_off --stamp <real stamp csv>  (gated)
  fec_ghost        --in case --off noise_off --stamp <NON-NULL stub>   (ungated parity response)
  drift_hunt       --in case  (energy/tone control)

Outputs in <out>/: *.f32, per-case tool dirs, summary.csv, SUMMARY.md.
Writes NOTHING outside <out> (repo rule: no source-dir pollution).
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import struct
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "core.exe"
FS_DEFAULT = "2929687.5"
TAPS = [0, 7, 23, 41, 53, 61]
CHUNK = 64
PAR = 63


def gauss(rng: random.Random) -> float:
    # Box-Muller, unit variance. NOTE: caller must reuse ONE rng instance;
    # a fresh Random(seed) per sample repeats the same draw (constant file).
    u1 = max(rng.random(), 1e-12)
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def gen_bits(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    return [1 if rng.random() < 0.5 else -1 for _ in range(n)]


def enforce_parity(bits: list[int]) -> None:
    for c0 in range(0, len(bits), CHUNK):
        if c0 + PAR >= len(bits):
            break
        par = 1
        for t in TAPS:
            par *= bits[c0 + t]
        bits[c0 + PAR] = par  # product over TAPS+[PAR] is +1 (even)


def write_f32(path: Path, xs: list[float]) -> None:
    with open(path, "wb") as fh:
        fh.write(struct.pack("<%df" % len(xs), *xs))


def run(cmd: list[str], timeout: float = 600.0) -> tuple[int, float, str]:
    t0 = time.time()
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        tail = (cp.stdout + cp.stderr)[-1500:]
        return cp.returncode, time.time() - t0, tail
    except subprocess.TimeoutExpired:
        return 124, time.time() - t0, "TIMEOUT"


def file_verdict(csv_path: Path) -> tuple[str, dict]:
    """Ghost/stamp/gperf CSVs repeat the FILE verdict on every row; row 0 carries it."""
    if not csv_path.exists():
        return "NO-CSV", {}
    with open(csv_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return "EMPTY", {}
    r0 = rows[0]
    v = r0.get("verdict", r0.get("kind", "?"))
    return v, r0


def ghost_zgate(md_path: Path) -> str:
    """Parse 'z_x100=.. gate_x100=..' from a ghost .md receipt."""
    try:
        txt = md_path.read_text(encoding="utf-8")
    except OSError:
        return "?/?"
    import re
    m = re.search(r"z_x100=(-?\d+)\s+gate_x100=(\d+)", txt)
    return f"{int(m.group(1)) / 100:.2f}/{int(m.group(2)) / 100:.2f}" if m else "?/?"


def drift_hits(csv_path: Path) -> str:
    if not csv_path.exists():
        return "NO-CSV"
    with open(csv_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return "0 hits"
    mx = max(float(r.get("sigma_x100", "nan") or "nan") for r in rows)
    mx = mx if mx == mx else float("nan")
    return f"{len(rows)} hits best_sig={mx / 100:.2f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1048576)
    ap.add_argument("--out", default="reports/2026-09-28_injection_cal")
    ap.add_argument("--fs", default=FS_DEFAULT)
    ap.add_argument("--quick", action="store_true",
                    help="smoke: noise + coded_0db only, n=262144")
    args = ap.parse_args()
    n = 262144 if args.quick else args.n
    out = (ROOT / args.out)
    out.mkdir(parents=True, exist_ok=True)
    if not CORE.exists():
        print(f"missing {CORE}; build core first", file=sys.stderr)
        return 2

    snrs = [0] if args.quick else [-6, -3, 0, 3]
    cases: list[tuple[str, str]] = [("noise", "false-alarm control")]
    for s in snrs:
        cases.append((f"coded_{s:+d}db".replace("+", "p").replace("-", "m"), f"parity-coded BPSK at {s} dB"))
    if not args.quick:
        cases.append(("uncoded_0db", "uncoded BPSK control at 0 dB"))
        cases.append(("cw_0db", "sine-tone energy control at 0 dB"))

    print(f"[inject] n={n} cases={len(cases)} out={out}", flush=True)
    # OFF leg: independent noise, shared by all cases (ONE rng, reused).
    r_off = random.Random(20260928)
    write_f32(out / "noise_off.f32", [gauss(r_off) for _ in range(n)])

    f32: dict[str, Path] = {}
    r_n = random.Random(777)
    f32["noise"] = out / "noise.f32"
    write_f32(f32["noise"], [gauss(r_n) for _ in range(n)])
    for name, _desc in cases:
        if name == "noise":
            continue
        p = out / f"{name}.f32"
        f32[name] = p
        if name.startswith("coded_"):
            db = int(name.split("_")[1].replace("p", "+").replace("m", "-").replace("db", ""))
            amp = 10.0 ** (db / 20.0)
            bits = gen_bits(n, 1000 + db)
            enforce_parity(bits)
            r_c = random.Random(2000 + db)
            write_f32(p, [amp * float(b) + gauss(r_c) for b in bits])
        elif name == "uncoded_0db":
            bits = gen_bits(n, 4242)  # parity NOT enforced
            r_u = random.Random(4343)
            write_f32(p, [float(b) + gauss(r_u) for b in bits])
        elif name == "cw_0db":
            f = 0.13 * float(args.fs)
            r_w = random.Random(5150)
            a = math.sqrt(2.0)  # tone power = 1 = noise power
            write_f32(p, [a * math.sin(2.0 * math.pi * f * i / float(args.fs)) + gauss(r_w)
                          for i in range(n)])
    # NON-NULL stub for ungated parity-response run (ghost_stamp_ok looks for NON-NULL).
    stub = out / "stamp_stub_nonnull.txt"
    stub.write_text("ism_stamp v0\nEXPONENT=4.41\nVERDICT=NON-NULL\n", encoding="utf-8")

    rows = []
    for name, desc in cases:
        inp, offp = f32[name], out / "noise_off.f32"
        cdir = out / name
        cdir.mkdir(exist_ok=True)
        r: dict[str, str] = {"case": name, "desc": desc}
        rc, dt, _ = run([str(CORE), "gauss_perfection", "--in", str(inp),
                         "--off", str(offp), "--fs", args.fs,
                         "--out", str(cdir / "gperf.md"), "--csv", str(cdir / "gperf.csv")])
        v, b0 = file_verdict(cdir / "gperf.csv")
        r.update(gperf=f"{v} q={b0.get('q_x100', '?')} (rc={rc},{dt:.0f}s)")
        rc, dt, _ = run([str(CORE), "ism_stamp", "--in", str(inp),
                         "--off", str(offp), "--fs", args.fs,
                         "--out", str(cdir / "stamp"), "--csv", str(cdir / "stamp.csv")])
        v, _b0 = file_verdict(cdir / "stamp.csv")
        r.update(stamp=f"{v} (rc={rc},{dt:.0f}s)")
        rc, dt, _ = run([str(CORE), "fec_ghost", "--in", str(inp),
                         "--off", str(offp), "--stamp", str(cdir / "stamp.csv"),
                         "--fs", args.fs,
                         "--out", str(cdir / "ghost_gated.md"), "--csv", str(cdir / "ghost_gated.csv")])
        v, _b0 = file_verdict(cdir / "ghost_gated.csv")
        r.update(ghost_gated=f"{v} z/gate={ghost_zgate(cdir / 'ghost_gated.md')} (rc={rc},{dt:.0f}s)")
        rc, dt, _ = run([str(CORE), "fec_ghost", "--in", str(inp),
                         "--off", str(offp), "--stamp", str(stub),
                         "--fs", args.fs,
                         "--out", str(cdir / "ghost_open.md"), "--csv", str(cdir / "ghost_open.csv")])
        v, _b0 = file_verdict(cdir / "ghost_open.csv")
        r.update(ghost_open=f"{v} z/gate={ghost_zgate(cdir / 'ghost_open.md')} (rc={rc},{dt:.0f}s)")
        rc, dt, _ = run([str(CORE), "drift_hunt", "--in", str(inp),
                         "--fs", args.fs,
                         "--out", str(cdir / "drift.md"), "--csv", str(cdir / "drift.csv")])
        r.update(drift=f"{drift_hits(cdir / 'drift.csv')} (rc={rc},{dt:.0f}s)")
        rows.append(r)
        print(f"[inject] {name}: " + " | ".join(f"{k}={v}" for k, v in r.items() if k != "desc"),
              flush=True)

    with open(out / "summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["case", "desc", "gperf", "stamp", "ghost_gated",
                                           "ghost_open", "drift"])
        w.writeheader()
        w.writerows(rows)
    md = ["# Injection calibration (§7.1) — summary", "",
          f"n={n} per file, fs={args.fs}, {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} UTC.",
          "Coded = BPSK + chunk-64 weight-7 even parity (simplified stand-in, not full LDPC).",
          "Ghost gate ≈6.6σ; drift gate 8σ. z/gate shown as sigma units.",
          "",
          "| case | gperf | stamp | ghost gated | ghost open | drift |",
          "|---|---|---|---|---|---|"]
    for r in rows:
        md.append("| " + " | ".join(r[k] for k in ("case", "gperf", "stamp", "ghost_gated",
                                                   "ghost_open", "drift")) + " |")
    md += ["", "## Reading guide",
           "- ghost_gated shows the pipeline-as-flown behavior (stamp-gated; expect RESIDUE caps).",
           "- ghost_open shows raw parity response behind a NON-NULL stub (detector physics).",
           "- uncoded_0db vs coded_0db isolates parity from mere BPSK energy.",
           "- cw_0db checks the energy (drift) control still fires on tones."]
    (out / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[inject] done -> {out / 'SUMMARY.md'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
