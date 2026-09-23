# python — TurboKain orchestration layer

Python is now **sanctioned glue** in this repo. It never detects anything:
every lane stays a native Kain `.exe` with its own byte-identical CLI/CSV
contract. Python discovers those exes, drives them with a stable interface,
runs their prove harnesses, chains them into one unified scan, and preserves
the receipts. See the *"Python is allowed"* section in `AGENTS.md`.

```
python/
  tk.py                  entry point (run this)
  turbokain/
    registry.py          tool table: exe path, kind, input kind, self-test argv
    runner.py            subprocess harness, receipt parsing, provenance
    scan.py              unified sweep driver (slice -> detectors -> summary)
    cli.py               `tk` subcommands
  README.md
```

**stdlib only** — no `pip install`, no venv, works on the VPS as-is.

## Commands

```bash
python python/tk.py list            # every driveable exe + catalog status
python python/tk.py prove           # run all built-in self-tests, exit 1 on fail
python python/tk.py prove boxcar_bank frame_hunt
python python/tk.py run TOOL [args] # pass-through exec (interactive, inherit stdio)
python python/tk.py doctor          # env vars, missing exes, registry drift
python python/tk.py catalog         # status/prove/receipt from catalog.tsv
python python/tk.py scan INPUT ...  # unified sweep
```

On Windows, `python\tk.cmd` is a one-line shim for the same thing.

## `tk scan` — the unified sweep

Takes a GUPPI `.raw` (slices first, then detects) or a sliced `.f32` (detects
directly) and runs the detector bundle, writing one run directory:

```
reports/2026-09-23_<tag>_scan/
  manifest.json     input fingerprint (size/mtime/head-sha256), git rev, host, argv
  summary.tsv       one row per (chan, pol, tool): exit, seconds, receipt, verdicts, outputs
  logs/*.log        raw stdout + stderr per stage
  pulse.md pulse.csv xeno.md ...   the tools' own outputs
```

```bash
# raw -> slice chan 60 pol 0 (8 blocks) -> full detector bundle
python python/tk.py scan D:/data/raw/blc00_..._0000.raw \
    --chan 60 --pol 0 --blocks 8 --tag trappist0017

# already-sliced file, pick your lanes
python python/tk.py scan leg.f32 --tools boxcar_bank,fold_sum,frame_hunt

# see the plan without running anything
python python/tk.py scan leg.f32 --dry-run
```

`summary.tsv` is the machine receipt; `manifest.json` is the provenance
sidecar. No dispositions are decided here — detector verdicts are recorded,
the human veto stays human-fed.

## Programmatic use

```python
import sys; sys.path.insert(0, "python")
from turbokain import load_registry, repo_root, run_tool, ScanPlan, run_scan

root = repo_root()
reg = load_registry(root)
res = run_tool(reg.get("boxcar_bank"), ["--prove"], root=root)
print(res.ok, res.receipt, res.verdicts)
```

## Adding a tool

1. Build the Kain exe (`cd kain/core && kain build tool.kn --target llvm`).
2. Add its `Tool(...)` row in `turbokain/registry.py` (exe path, kind,
   `input_kind`, self-test argv, in/out flags).
3. Add it to `F32_DETECTORS` in `scan.py` if it consumes `.f32` and should ride
   the default bundle.
4. Log it in `memory.tsv` and give it a `catalog.tsv` row, as always.

## Rules that did not change

- Detector logic lives in Kain. Python must not grow a second implementation
  of a lane.
- Thresholds are data, never baked into the wrapper.
- No hardcoded drive letters: the registry is repo-relative, data paths come
  from `--data-dir` / `$SETIYETI_DATA`.
- Every run writes a receipt; a scan is not done until `summary.tsv` exists.
