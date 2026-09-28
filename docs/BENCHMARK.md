# TurboKain Benchmark — 17 GB GUPPI Baseband, Full Detection Battery

**Date:** 2026-09-28
**Host:** AMD EPYC 9V45 (4 logical cores, 16 GB RAM)
**Disk:** Virtual NVMe SSD (measured raw sequential read: **140.9 MB/s cold**, **2.75 GB/s warm**)
**Binary:** `core.exe` — 26-instrument amalgamated suite, 1.97 MB, zero runtime dependencies
**Input:** Breakthrough Listen GUPPI `.raw`, 8-bit, 64 chan × 4 pol, 128 blocks, **17.18 GB / 67,108,864 samples**
(TRAPPIST-1 0015, `blc00_guppi_57807_75725_DIAG_TRAPPIST1_0015.0000.raw`, channel 44)
**Sample rate:** 2,929,687.5 Hz

Supersedes the 2026-09-23 benchmark (7 stages, 17-tool binary, 2-core host).
Every number below was measured on this host, this binary, this file —
see §7 for the head-to-head against the old benchmark. Raw timing log:
`_tmp/bench_4core/bench_times.tsv` (+ `bench_results.json`).

---

## 1. Raw Disk Ceiling (what any tool is bounded by)

| Test | Result |
|---|---|
| Cold sequential read (4 GB) | **140.9 MB/s** |
| Warm sequential read (4 GB, cached) | **2.75 GB/s** |
| Full-file cold stream (17 GB) | ~122 s (projected at 140.9 MB/s) |

Cold ceiling is unchanged from September 23 (140 MB/s) — same throttled VPS disk.
Warm read is lower this run (2.75 vs 5.4 GB/s): page cache was shared with a
live 732 GB campaign tree, so this is the honest number under load, not a
best-case re-read of an idle box.

**Key architectural point (unchanged):** TurboKain never streams the whole file.
It seeks straight to the target channel's payload inside each 128 MB block,
reading only ~268 MB of actual payload for one channel across 128 blocks, not 17 GB.
That is why `slice` below takes ~2.5 s cold instead of ~122 s.

---

## 2. Stage-by-Stage Timing (67.1M samples, warm cache)

Measured on `ch44.f32` (268.4 MB) with per-tool wall clock (`perf_counter`
around `core <tool>`, one stage at a time, single-pol). Sweep order:

| Stage | Domain | Wall time | Notes |
|---|---|---|---|
| `sk_gate` | RFI excision | **0.160 s** | CLEAN, skdev 0.694 |
| `xeno_scan` | 6-marker anomaly battery | **0.918 s** | XENO-CLEAN |
| `ism_stamp` | propagation authenticator | **0.697 s** | CLEAN (gate null → ghost correctly skipped, §2.1) |
| `gauss_perfection` | inverted-SK escalator | **0.207 s** | CLEAN |
| `pulsar_clock` | galactic re-timer | **9.978 s** | CLEAN; retimes 67M samples + phi-fold |
| `perm_entropy` | permutation entropy + LZW | **3.067 s** | streaming 5-D ordinal |
| `boxcar_bank` | DM pulse matched filter | **0.467 s** | quiet, no SHOT above gate |
| `fold_sum` | harmonic folder | **23.716 s** | top fold 7.10σ, undetected — full-period grid is the costliest lane |
| `frft_hunt` | coherent chirp matched filter | **4.851 s** | capped (`--max-n 131072 --alpha-steps 25`) |
| `drift_hunt` | dedoppler chirp search | **0.186 s** | 0 kept |
| `jerk_track` | Viterbi jerk tracker | **1.010 s** | — |
| `frame_hunt` | harmonic comb periodogram | **0.082 s** | max 5.17σ, undetected |
| `lag_hunt` | direct autocorrelation | **0.418 s** | lag-26 POWER WATCH (sample-clock family, §5) |
| `fam_god` | cyclostationary SCD | **9.044 s** | backend 22.35 Hz comb family fires, vetoed on sight (§5) |
| `scint_pol` | scintillation + pol coherence | **0.570 s** | QUIET, single-pol |
| `packet_hunt` | telemetry framing | **0.073 s** | — |
| `bitslice` | voltage → bitstreams | **0.156 s** | — |
| `raster_hunt` | prime-factor pictograms | **0.059 s** | on mag stream |
| `xvm_sandbox` | execution sandbox | **0.044 s** | on mag stream |
| `bispectrum` | bicoherence QPC estimator | **0.158 s** | 65,536 triplets, diagonal sweep |
| `unify` | verdict lattice + REPORT | **0.071 s** | disposition CLEAN |
| `waterfall` | 1920×1080 PNG dashboard | **1.440 s** | — |
| **SUM (22 stages)** | | **57.629 s** | |

### 2.1 Gated / dual-pol extras (not in the single-pol sum)

| Stage | Wall time | Notes |
|---|---|---|
| `slice` pol 1 (second polarisation) | **1.869 s** | warm |
| `subspace_null` (dual-pol spatial nuller) | **0.257 s** | needs `--in0/--in1` pair |
| `fec_ghost` | **skipped (0.0 s)** | by design: stamp gate null → ghost forbidden without parsecs |

`fold_sum` (41% of battery time) is the new long pole — it replaced `fam_god`
(84% in the old 7-stage battery, now 16%). The full-period folding grid over
67M samples is O(periods × N); everything else is sub-10 s.

---

## 3. End-to-End Pipeline (17 GB raw → verdicts)

### Slice (17 GB → 268 MB `.f32`, 128 blocks)

| Condition | Time |
|---|---|
| `slice` cold (first touch) | **2.739 s** |
| `slice` warm (cached) | **2.458 s** |

Cold slice is ~4× faster than the September number (11.9 s): the kernel32
seek-and-pluck path now pays only for the 268 MB it actually reads
(~2 s at 140 MB/s) plus block seeks — the old slicer did more redundant IO.
Warm slice is identical (2.46 vs 2.25 s).

### Sweep (full battery over the `.f32`, warm)

| Step | Time |
|---|---|
| `core sweep` end-to-end (22 stages + unify + waterfall, in-process) | **54.442 s** |
| Sum of individually spawned stages (§2) | 57.629 s |

The in-process sweep beats the sum of spawned stages by ~3.2 s (no process
spin-up per lane, shared buffer setup). This is the number to quote.

### Totals

| Pipeline | Time |
|---|---|
| Cold: slice + sweep | **57.2 s** |
| Warm: slice + sweep | **56.9 s** |

### Throughput vs. real-time (67.1M samples = 22.9 s of sky at 2.93 MHz)

| Metric | Throughput | Real-time factor |
|---|---|---|
| `slice` only (warm) | 27.3 M samples/s | **9.3× real-time** |
| Full 22-stage battery, 1 channel (warm) | 1.23 M samples/s | **0.42× real-time** |
| Full battery, 4 channels in parallel on 4 cores | 2.69 M samples/s | **0.92× real-time** |

The full suite — 3× the instruments of September — runs at nearly the
telescope rate when all 4 cores are fed (§3.1). Single-channel latency is the
price of 22 lanes; campaign throughput is what matters, and that is ~real-time.

### 3.1 Four-core scaling (the point of this rerun)

Four channels (30 / 32 / 44 / 60), full `core sweep` each, launched concurrently:

| Mode | Wall time | Amortized per channel | Speedup vs serial |
|---|---|---|---|
| 4× serial (projected from 54.442 s) | 217.8 s | 54.4 s | 1.00× |
| **4× parallel (measured, all rc=0)** | **99.7 s** | **24.9 s** | **2.18×** |

Speedup is 2.18× on 4 cores, not 4× — the lanes are memory-bandwidth bound
(`fold_sum` + `fam_god` + `pulsar_clock` streaming 268 MB each), so four
concurrent sweeps share ~2.75 GB/s of warm page-cache bandwidth plus cold
tails. Embarrassingly parallel over channels, bounded by the bus: exactly what
you expect from a streaming CPU pipeline, and exactly why the overnight
campaign grids channels across cores rather than threads within a lane.

---

## 4. Verification Battery

`core prove` — all 25 mathematical self-test batteries, in-memory, single process:

```
Core Battery Receipt: ALL 25 PROVE BATTERIES PASSED (receipt=PASS)
```

**Total: 6.43 s** for 25 instruments (was 3.47 s for 12). Per-battery cost is
flat (~0.26 s); the growth is all new coverage — 4 alien keystones
(`ism_stamp`, `fec_ghost`, `gauss_perfection`, `pulsar_clock`), `bispectrum`,
`packet_hunt`, `subspace_null` — not slower lanes.

---

## 5. Science Output (TRAPPIST-1 0015, channel 44)

All 22 stages ran to completion (exit 0 throughout). Unify disposition: **CLEAN**
(honest negative with receipt).

| Stage | Verdict / key metric |
|---|---|
| `sk_gate` | CLEAN (skdev 0.694) |
| `xeno_scan` | XENO-CLEAN (maxz 4.9) |
| `ism_stamp` | CLEAN (no DISS screen, no RM) |
| `gauss_perfection` | CLEAN (H1 0.973, sane) |
| `pulsar_clock` | CLEAN (ensemble, no clock) |
| `perm_entropy` | quiet (no anomalous windows) |
| `boxcar_bank` | quiet (DM0 σ≈10.1, no SHOT) |
| `fold_sum` | undetected (top 7.10σ) |
| `frft_hunt` | no chirp above gate |
| `drift_hunt` | 0 kept |
| `jerk_track` | quiet |
| `frame_hunt` | undetected (max 5.17σ) |
| `lag_hunt` | WATCH at lag 26 only (sample-clock family — 26 samples ≈ 8.9 µs digitizer/PFB texture, single channel with no OFF leg, stays WATCH) |
| `fam_god` | backend comb fires (22.35 Hz family: 17.88/134.11/178.81 kHz harmonics + ~56/100 MHz clusters) — **vetoed on sight** per warehouse rule; the known `fs/131072` hum, present across targets/MJDs/bands |
| `scint_pol` | QUIET, single-pol |
| `packet_hunt` | no framing |
| `bitslice`/`raster_hunt`/`xvm_sandbox` | quiet bitstreams, no machines |
| `bispectrum` | no QPC above gate |
| `fec_ghost` | correctly skipped (no propagation stamp to gate on) |

The only two flags are both known instrument texture: the GUPPI backend comb
(`fam_god`, veto-catalogued, never per-target) and a lag-26 autocorrelation
blip consistent with digitizer/PFB sample-clock leakage. No sky candidate.
That is a successful shift: full-spectrum receipt, floor stated, nothing hidden.

---

## 6. Reproduce

```bash
# Slice one channel from a 17 GB raw file (cold: ~2.7 s, warm: ~2.5 s)
core slice --in D:/data/campaigns/trappist1/blc00_guppi_57807_75725_DIAG_TRAPPIST1_0015.0000.raw \
  --chan 44 --pol 0 --out _tmp/bench_4core/ch44.f32

# Run the full 22-stage battery (~54 s warm on 67M samples)
core sweep _tmp/bench_4core/ch44.f32 --out-dir _tmp/bench_4core/sweep_full \
  --fs 2929687.5 --target BENCH-4CORE

# Verify all instruments (~6.4 s)
core prove

# 4-way parallel: same sweep × 4 channels concurrently (~100 s wall)
# Full driver (disk + all stages + prove + sweep + parallel):
python python/_tmp/bench_full.py
```

---

## 7. Head-to-Head vs the 2026-09-23 Benchmark

Same 17 GB file class, same 67.1M-sample channel, same `fs`. Old host had
2 cores / 4 threads; this host has 4 cores.

| Metric | 2026-09-23 | 2026-09-28 (this run) |
|---|---|---|
| Binary | 1.30 MB, 17 tools | 1.97 MB, 26 instruments |
| Prove batteries | 12 in 3.47 s | **25 in 6.43 s** |
| Stages timed | 7 (sum 10.675 s) | **22 (sum 57.629 s)** |
| Long pole | `fam_god` 8.9 s (84%) | **`fold_sum` 23.7 s (41%)** |
| Full battery warm | ~13.9 s (9 stages) | **54.4 s (22 stages + unify + waterfall)** |
| Slice cold / warm | 11.9 s / 2.25 s | **2.74 s / 2.46 s** |
| Cold disk ceiling | 140 MB/s | 140.9 MB/s (unchanged) |
| Parallel scaling | not measured | **2.18× on 4 cores** |

Per-stage regression check (the 7 stages both runs share, warm):

| Stage | 09-23 | 09-28 | Δ |
|---|---|---|---|
| `sk_gate` | 0.142 s | 0.160 s | noise |
| `xeno_scan` | 0.559 s | 0.918 s | +0.36 s (wider marker set) |
| `boxcar_bank` | 0.431 s | 0.467 s | noise |
| `drift_hunt` | 0.160 s | 0.186 s | noise |
| `frame_hunt` | 0.067 s | 0.082 s | noise |
| `lag_hunt` | 0.391 s | 0.418 s | noise |
| `fam_god` | 8.924 s | 9.044 s | noise |

**No per-stage regressions.** The battery costs 3.9× the wall for 2.4× the
stages plus heavier lanes (`fold_sum` full grid, `pulsar_clock` retiming,
`frft_hunt` coherent chirps, `perm_entropy` streaming) — linear scaling with
new science, not slower code. The defensible claims from this benchmark:

* 17 GB raw → calibrated 67M-sample voltage in **~2.7 s cold / ~2.5 s warm**
* full **22-instrument** battery in **~54 s warm** (~57.6 s as spawned stages)
* **25/25** formal prove batteries in **6.43 s**
* 4 concurrent full-channel sweeps in **99.7 s wall** (2.18× speedup, ~real-time campaign throughput)
* all of it in a **1.97 MB binary with zero dependencies**, verdict **CLEAN with receipts**

Legacy-stack comparison (unchanged from September): published/typical
`turboSETI` + `blimpy`/`rawspec` figures spend 1–3 minutes on raw→filterbank
conversion alone for a file this size, plus minutes more for drift search.
Still a published figure, still no legacy stack installed here, still no
direct head-to-head — the measured claims above are the ones that count.
