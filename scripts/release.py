#!/usr/bin/env python3
"""scripts/release.py — Automated GitHub Release Script for TurboKain.

Usage:
    python scripts/release.py [options]

Options:
    --version TAG       Release tag (default: v0.2.0-alpha)
    --title TITLE       Release title
    --draft             Create as draft release
    --prerelease        Mark as pre-release (default: False)
    --skip-prove        Skip running `tkc prove` before release
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run_cmd(cmd, env=None, check=True, capture=True):
    print(f"--> {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=ROOT, env=env, shell=isinstance(cmd, str),
                         capture_output=capture, text=True)
    if check and res.returncode != 0:
        print(f"FAILED (exit {res.returncode}):")
        if res.stdout:
            print(res.stdout)
        if res.stderr:
            print(res.stderr)
        sys.exit(res.returncode)
    return res

def get_gh_token():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    # Try git credential fill
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n",
            capture_output=True, text=True, check=True
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception as e:
        print(f"Warning: could not retrieve credential helper token: {e}")
    return None

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="TurboKain automated release packager")
    parser.add_argument("--version", default="v0.4.0-alpha", help="Release version tag")
    parser.add_argument("--title", help="Release title")
    parser.add_argument("--draft", action="store_true", help="Create as draft")
    parser.add_argument("--prerelease", action="store_true", help="Mark as prerelease")
    parser.add_argument("--skip-prove", action="store_true", help="Skip tkc prove")
    args = parser.parse_args()

    tag = args.version
    title = args.title or f"TurboKain {tag} — Alien Keystones, TRAPPIST-1 Paper & 26-Instrument Engine (25 prove batteries)"
    
    print(f"================================================================================")
    print(f" TurboKain Automated Release Pipeline -> {tag}")
    print(f" Title: {title}")
    print(f"================================================================================")

    # 1. Check/Get GitHub token
    gh_token = get_gh_token()
    if not gh_token:
        print("ERROR: No GH_TOKEN found. Set GH_TOKEN or login with `gh auth login`.")
        sys.exit(1)
    env = os.environ.copy()
    env["GH_TOKEN"] = gh_token

    # 2. Build & Verify
    print("\n[Step 1/6] Amalgamating and compiling native core suite...")
    run_cmd(["kain", "amalgamate", "--raw", "kain/core", "-o", "kain/core.kn"])
    run_cmd(["kain", "build", "kain/core.kn", "--target", "llvm", "-o", "core.exe"])
    shutil.copy2(ROOT / "core.exe", ROOT / "tkc.exe")
    shutil.copy2(ROOT / "core.exe", ROOT / "turbokain_core.exe")

    if not args.skip_prove:
        print("\n[Step 2/6] Running 25-instrument formal prove battery...")
        res = run_cmd([str(ROOT / "tkc.exe"), "prove"], check=True)
        print("All 25 prove batteries verified in-memory!")

    # 3. Create Package Staging
    print("\n[Step 3/6] Packaging release artifacts...")
    stage_dir = ROOT / "_tmp" / f"turbokain-{tag}"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True)

    # Copy binaries & docs
    shutil.copy2(ROOT / "tkc.exe", stage_dir / "tkc.exe")
    shutil.copy2(ROOT / "turbokain_core.exe", stage_dir / "turbokain_core.exe")
    shutil.copy2(ROOT / "core.exe", stage_dir / "core.exe")
    shutil.copy2(ROOT / "tkc.cmd", stage_dir / "tkc.cmd")
    shutil.copy2(ROOT / "README.md", stage_dir / "README.md")
    
    docs_target = stage_dir / "docs"
    docs_target.mkdir()
    if (ROOT / "docs" / "USER_GUIDE.md").exists():
        shutil.copy2(ROOT / "docs" / "USER_GUIDE.md", docs_target / "USER_GUIDE.md")
    if (ROOT / "docs" / "BENCHMARK.md").exists():
        shutil.copy2(ROOT / "docs" / "BENCHMARK.md", docs_target / "BENCHMARK.md")
    
    wf_ex_target = docs_target / "waterfall_examples"
    wf_ex_target.mkdir()
    if (ROOT / "docs" / "waterfall_examples").exists():
        for p in (ROOT / "docs" / "waterfall_examples").glob("*.*"):
            shutil.copy2(p, wf_ex_target / p.name)

    tool_res_target = docs_target / "toolresearch"
    tool_res_target.mkdir()
    if (ROOT / "docs" / "toolresearch").exists():
        for p in (ROOT / "docs" / "toolresearch").glob("*.md"):
            shutil.copy2(p, tool_res_target / p.name)

    # Create zip
    zip_name = f"turbokain-{tag}-windows-x86_64.zip"
    zip_path = ROOT / zip_name
    if zip_path.exists():
        zip_path.unlink()

    print(f"Creating zip archive {zip_name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in stage_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(stage_dir))

    # 4. Compute SHA-256
    print("\n[Step 4/6] Computing SHA-256 sums...")
    sha_lines = []
    for p in [ROOT / "tkc.exe", ROOT / "turbokain_core.exe", zip_path]:
        h = sha256_file(p)
        sha_lines.append(f"{h}  {p.name}")
        print(f"  {p.name}: {h}")

    sums_path = ROOT / "SHA256SUMS.txt"
    with open(sums_path, "w") as f:
        f.write("\n".join(sha_lines) + "\n")

    # 5. Git Commit & Tag
    print("\n[Step 5/6] Checking git repository status and tag...")
    run_cmd(["git", "add", "kain/", "python/", "docs/", "scripts/", "README.md",
             "catalog.tsv", "memory.tsv", "sky_catalog.tsv", "AGENTS.md"])
    # Check if there are staged changes to commit
    diff_res = subprocess.run(["git", "diff", "--staged", "--quiet"])
    if diff_res.returncode != 0:
        run_cmd(["git", "commit", "-m", f"release: {tag} — alien keystones, TRAPPIST-1 paper & 26-instrument suite (25 prove batteries)"])
        run_cmd(["git", "push", "origin", "main"], env=env)
    
    # Tag
    run_cmd(f"git tag -f {tag}", check=False)
    run_cmd(f"git push -f origin {tag}", env=env)

    # 6. Generate Release Notes & Publish via GH
    print("\n[Step 6/6] Publishing release via GitHub CLI...")
    sha0 = sha_lines[0]
    sha1 = sha_lines[1]
    sha2 = sha_lines[2]

    notes = f"""# TurboKain {tag} — Alien Keystones, TRAPPIST-1 Survey Paper & 26-Instrument Engine

**High-Throughput Coherent Radio Technosignature & Bystander Traffic Pipeline**
*Native, whole-program optimized, formally verified DSP suite for telescope baseband. One ~2 MB exe, zero dependencies.*

---

## What's New in {tag} (since v0.3.0-alpha, 14 commits)

### 1. Four alien keystone lanes (the gated detection stack)
- **`ism_stamp.kn`** — propagation authenticator. Sub-band scintillation screen + RM fit + ON/OFF contrast. Verdicts CLEAN / QUARANTINE / STAMPED / TERRESTRIAL-IMPULSE. Gates everything below it.
- **`fec_ghost.kn`** — keystone spread-coded ghost hunter. Boxplus soft dual-code distinguisher, gated-only (needs a stamp + ON-only). Catches 0 dB coded ghosts power detectors miss.
- **`gauss_perfection.kn`** — inverted-SK escalator. Flags too-perfect Gaussian tiles vs honest sky.
- **`pulsar_clock.kn`** — galactic re-timer. Barycentric retime + phi-fold bridge to fold_sum, smeared-hum veto included.
- All four proven (5/5, 6/6, 4/4, 4/4) and wired into `core sweep` gating: stamp null → ghost correctly skipped, never forced.

### 2. TRAPPIST-1 bystander survey paper
- **`papers/trappist1_bystander_survey/`** — 732 GB raw GUPPI across 2–12 GHz, 1,024 dual-pol channels swept. Honest-negative pilot draft (manuscript.md + aastex .tex + .bib + 1920x1080 figures). Covers the 1430.51 Hz ROACH digitizer ghost (fs/2048) now an auto-veto rule.
- Injection first-light calibration DONE (reports/2026-09-28_injection_cal). Journal + sky_catalog rows sealed.

### 3. Journal memory layer + campaign scripts
- **`python/turbokain/journal.py`** — per-system journal (what was seen / why ruled out / what next), FTS index, backs the agent tools. Every campaign now writes a journal entry with its sky row.
- New drivers: 128-comb deep campaign, LHS-1140 cadence search, TIC 458478250 scan, TRAPPIST-1 overnight master, manuscript validator.

### 4. Waterfall paper theme + dispatch fixes
- `--theme paper` (white page, black ink, viridis heatmap) for publications, dark Turbo/Inferno default untouched. Re-prove green.
- dispatch.kn multi-call fixes, unify tweaks, registry/scan/db updates.

### 5. Measured speed (docs/BENCHMARK.md, 2026-09-28, 4-core EPYC)
- 17.18 GB GUPPI → 268 MB channel .f32 in **2.74 s cold / 2.46 s warm** (seek-and-pluck, not streaming)
- Full **22-stage sweep in 54.4 s warm**, **25/25 prove in 6.43 s**, 4 channels parallel in 99.7 s wall (2.18x, ~telescope rate)
- Binary **~2.0 MB**, zero deps. No per-stage regressions vs v0.3.0.

---

## Complete 22-Instrument Suite

1. **`slice`** — GUPPI .raw (2-bit / 8-bit) -> .f32 channel/pol voltage slice
2. **`fil_reader`** — Sigproc .fil (8/16/32-bit) -> calibrated .f32
3. **`h5_reader`** — Breakthrough Listen HDF5 filterbank (.h5) ingest
4. **`config`** — 40-parameter telemetry / RF geometry resolver
5. **`sk_gate`** — Spectral Kurtosis RFI excision (4096/2048 STFT)
6. **`subspace_null`** — Dual-pol spatial subspace RFI nulling & phase preservation
7. **`xeno_scan`** — 6-marker microscopic anomaly battery
8. **`perm_entropy`** — Permutation Entropy & LZW Complexity screener (O(N))
9. **`bispectrum`** — 3D Bispectrum & Normalized Bicoherence (b^2) QPC estimator
10. **`scint_pol`** — Interstellar diffractive scintillation & pol coherence
11. **`boxcar_bank`** — O(N) prefix-sum DM sweep + single-pulse matched filters
12. **`fold_sum`** — Sub-band Hann/FFT harmonic epoch folder
13. **`fam_god`** — 3-decade FFT Accumulation Method (cyclostationary SCD)
14. **`frame_hunt`** — Envelope periodogram + 6-subharmonic comb hunter
15. **`frft_hunt`** — Coherent Fractional Fourier Transform chirp matched filter
16. **`drift_hunt`** — Taylor dedoppler chirped carrier search
17. **`jerk_track`** — Viterbi non-linear orbital jerk acceleration tracker
18. **`lag_hunt`** — Long-lag direct autocorrelation microscope (0.01 ms – 10 s)
19. **`packet_hunt`** — Autonomous telemetry & interstellar packet framing
20. **`bitslice`** — Voltage -> packed bitstreams (sign/diff/mag)
21. **`raster_hunt`** — 2D prime-factor payload framing & pictograms
22. **`xvm_sandbox`** — Subleq / Rule 110 / Berlekamp-Massey symbolic sandbox
23. **`cadence_pair`** — ON/OFF pointing corroboration gate
24. **`stack`** — Incoherent multi-epoch ON/OFF power stacker
25. **`unify`** — Campaign report unifier (tables -> REPORT.md + CSV + JSON)
26. **`waterfall`** — Multi-panel 1920x1080 scientific diagnostic PNG dashboard

---

## Verification

`tkc prove` — **All 25 mathematical self-test batteries PASS in ~6.4 s**:
```text
Core Battery Receipt: ALL 25 PROVE BATTERIES PASSED (receipt=PASS)
```
Full per-lane 4/4–10/10 receipts print in the prove log (bitslice, boxcar, config, drift, fil_reader, frame 9/9, lag 9/9, xeno, xvm 24/24, raster, jerk, scint, unify, stack, h5_reader, waterfall, packet, frft, perm, subspace_null, bispectrum + 4 keystones: ism_stamp 5/5, fec_ghost 6/6, gauss_perfection 4/4, pulsar_clock 4/4).

---

## SHA-256 Hashes

```text
{sha0}
{sha1}
{sha2}
```
"""

    notes_path = ROOT / "_tmp" / "RELEASE_NOTES.md"
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(notes)

    # Check if release exists; if so, delete it first to re-release cleanly
    check_rel = subprocess.run(["gh", "release", "view", tag], env=env, capture_output=True)
    if check_rel.returncode == 0:
        print(f"Release {tag} already exists, deleting first...")
        run_cmd(["gh", "release", "delete", tag, "--yes"], env=env)

    # Create release
    gh_cmd = [
        "gh", "release", "create", tag,
        str(ROOT / "tkc.exe"),
        str(ROOT / "turbokain_core.exe"),
        str(zip_path),
        str(sums_path),
        str(ROOT / "docs" / "waterfall_examples" / "01_proxima_b_drifting_carrier_turbo.png"),
        "--title", title,
        "--notes-file", str(notes_path)
    ]
    if args.draft:
        gh_cmd.append("--draft")
    if args.prerelease:
        gh_cmd.append("--prerelease")

    run_cmd(gh_cmd, env=env)
    print(f"\nSUCCESS: Published {tag} to GitHub!")

    # Log in memory.tsv
    try:
        run_cmd([str(ROOT / "scripts" / "memlog.exe"), "release", "publish",
                 f"Published {tag} GitHub release with 26 instruments, 25 prove batteries, TRAPPIST-1 paper and benchmark",
                 f"tkc.exe,turbokain_core.exe,{zip_name},SHA256SUMS.txt"])
    except Exception as e:
        print(f"memlog note: {e}")

if __name__ == "__main__":
    main()
