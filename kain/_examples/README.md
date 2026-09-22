# kain/ — Kain-native signal tooling for SETIYETI

First rule of this directory, per project consensus: **replace nothing.**
Every `.kn` file here must earn its place the SETIYETI way — behind an
identical CLI/CSV contract, proven against the existing prove harness,
before it touches real data. Research first. Receipts always.

## What lives here

| File | What | Status |
|---|---|---|
| `lane_sieve.kn` | Per-lane quarantine sieve over quantized voltage codes (example 01) | Built, receipt PASS |
| `cadence_pair.kn` | ON/OFF cadence gate as authority/mirror + resonate tripwire + pulse clock (example 02) | Built, receipt PASS |

## Example 01: lane_sieve.kn

Mirrors the hard-won repo rule: *"Quarantine bad lanes before analysis —
per-lane RMS + range/diversity; a dark digitizer must be quarantined, not
scanned."* Synthetic deterministic input (LCG codes + one planted dark lane
+ one planted hot lane), so a passing run **is** the noise-matched receipt.

Fastest-Kain idioms used (taken from `benchmark/cases/simd_lane_mix`,
the 10.5x-vs-Rust case):

- **Int-domain quantized codes** — the backend-matched representation, not floats
- **`ptr<Int>` + `alloc_zeroed` + `collapse`/`observe`/`decay`** — explicit
  ownership, zero GC, arena-friendly streaming buffers
- **`converge` spec/fast lanes** — scalar reference + AVX2 runtime intrinsic
  (`runtime_simd_i32_domain_dot_avx2_mod`), capability-gated; main() runs
  both on the live buffer and exits 2 on any divergence
- **`law` predicates as quarantine gates** (`qrms_ok`, `diverse_ok`)
- **`main() -> Int` exit-code contract**: 0 proven pass, 1 mask mismatch,
  2 spec/fast divergence

### Build & run (uses the installed Kain, seconds — no Bazel needed)

```bat
set "PATH=D:\kain\.kain\bin;C:\scoop\apps\llvm\current\bin;C:\scoop\apps\python312\current;%PATH%"
set PYO3_PYTHON=C:\scoop\apps\python312\current\python.exe
kain.exe build E:\setiyeti\kain\lane_sieve.kn --target llvm -o sieve.exe
sieve.exe [lanes] [samples]     :: defaults: 16 lanes x 8192 samples
```

Expected receipt (defaults): 14 PASS, lane 3 QUARANTINE (rms+diversity),
lane 7 QUARANTINE (rms), `receipt=PASS mask=3,7`, exit 0.

## Example 02: cadence_pair.kn

The ON/OFF cadence gate as compiler-owned semantics — the construct mapping
the project asked about:

- **entangle**: ON authority → record mirror, OFF authority → record mirror
  (`single_writer`; the mirrors are the citable row, still append-only
  downstream — Kain feeds the record, never rewrites it)
- **resonate**: tripwire on every `hot_mask` mutation, both pointings
- **pulse**: `clock_driver every 8 ms` pacing integration epochs
- **law**: the WATCH gate itself (`cadence_watch_lane`, `cadence_terrestrial_lane`)
- **patch**: journaled integrations; **world**: the two pointings

Deterministic receipt: ON sees lane 2 alone + lane 5 in common with OFF.
Live run:

```
cadence: on_mask=36 off_mask=32 epochs=2,1
verdicts: lane2=WATCH lane5=TERRESTRIAL rest=CLEAN
mirrors: on=36 off=32
telemetry: resonate+3 entangle+6 patch+6 pulse+21 trips=2,1 ticks=22
cadence: receipt=PASS watch=lane2 terrestrial=lane5
```

Every layer proved it fired: 3 tripwires, 6 propagations (3 patches ×
2 fields), 6 journal entries, 21 clock ticks. Exit 0.

```bat
kain.exe build E:\setiyeti\kain\cadence_pair.kn --target llvm -o cadence.exe
```

## Next candidates (in value order, all CPU — no GPU needed)

1. `sk_gate.kn` — per-bin spectral kurtosis + deviant-fraction gate (repo rule:
   per-bin only, ≥2% bins). Pure `simd_lane_mix`-shaped math.
2. `boxcar_bank.kn` — `transient_dm.py`'s sweep as converge lanes.
3. `fold_sum.kn` — `pulsar_fold.py` harmonic sums as parallel actor fanout
   (`parallel_reduce` won 26x vs Rust on this shape).
4. `file_sieve.kn` — this sieve reading real `.f32` via `--data-dir`
   (byte backend plugs into `fill_buffer`; never hardcode `D:/`).

## Discipline

- No hardcoded `D:/` or `E:/` paths in committed code. `--data-dir` /
  `$SETIYETI_DATA`, same as everything else in this repo.
- New tool checklist: `.kn` → build → prove harness parity → identical
  CLI/CSV contract → catalog row. A scan with no manifest never happened;
  a Kain exe with no receipt never ships.
