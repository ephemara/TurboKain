# TurboKain Benchmark — 17 GB GUPPI Baseband, Full Detection Battery

**Date:** 2026-09-23
**Host:** AMD EPYC 9V45 (VPS slice: 2 physical cores / 4 logical threads)
**Disk:** Virtual NVMe SSD (measured raw sequential read: **140 MB/s cold**, **5.4 GB/s warm**)
**Binary:** `tkc.exe` — 17-tool amalgamated suite, 1.30 MB, zero runtime dependencies
**Input:** Breakthrough Listen GUPPI `.raw`, 8-bit, 64 chan × 4 pol, 128 blocks, **17.18 GB / 67,108,864 samples**
**Sample rate:** 2,929,687.5 Hz

---

## 1. Raw Disk Ceiling (what any tool is bounded by)

| Test | Result |
|---|---|
| Cold sequential read (4 GB) | **140 MB/s** |
| Warm sequential read (4 GB, cached) | **5.4 GB/s** |
| Full-file cold stream (17 GB) | ~122 s (projected at 140 MB/s) |

**Key architectural point:** TurboKain never streams the whole file. It seeks straight to the
target channel's payload inside each 128 MB block, reading only what it needs (~268 MB of
actual payload for one channel across 128 blocks, not 17 GB).

---

## 2. Stage-by-Stage Timing (67M samples, warm cache)

Measured on `ch44.f32` (268 MB) with the standalone detector battery:

| Stage | Domain | Wall time | Internal detail |
|---|---|---|---|
| `sk_gate` | RFI excision | **0.142 s** | fft_loop = 92 ms |
| `xeno_scan` | 6-marker anomaly battery | **0.559 s** | — |
| `boxcar_bank` | DM pulse matched filter | **0.431 s** | decode 6 ms, detect 386 ms |
| `drift_hunt` | Dedoppler chirp search | **0.160 s** | stft 46 ms, grid 61 ms |
| `frame_hunt` | Harmonic comb periodogram | **0.067 s** | — |
| `lag_hunt` | Direct autocorrelation | **0.391 s** | — |
| `fam_god` | Cyclostationary SCD | **8.924 s** | scan 8,459 ms |
| **TOTAL (7 stages)** | | **10.675 s** | |

`fam_god` (3-decade FFT Accumulation Method) dominates at ~84% of detector time.

---

## 3. End-to-End Pipeline (17 GB raw → verdicts)

### Cold cache (fresh file, first touch)
| Step | Time |
|---|---|
| `slice` (17 GB → 268 MB `.f32`, 128 blocks) | **11.893 s** |
| `sweep` (9-stage detector battery) | **15.511 s** |
| **TOTAL** | **27.404 s** |

### Warm cache (data cached)
| Step | Time |
|---|---|
| `slice` | **2.246 s** |
| `sweep` (9 stages) | **13.881 s** |
| **TOTAL** | **16.127 s** |

### Throughput vs. real-time
| Metric | Throughput | Real-time factor |
|---|---|---|
| `slice` only (warm) | 29.9 M samples/s | **10.2× real-time** |
| Full pipeline (warm) | 4.16 M samples/s | **1.42× real-time** |
| Full pipeline (cold) | 2.45 M samples/s | **0.84× real-time** |

The full 9-stage battery runs **faster than the telescope can record** when data is in cache,
and is within ~16% of real-time even fully cold on a throttled VPS disk.

---

## 4. Verification Battery

`tkc prove` — all 12 mathematical self-test batteries, in-memory, single process:

```
Core Battery Receipt: ALL 12 PROVE BATTERIES PASSED (receipt=PASS)
```

**Total: 3.471 s** for 12 instruments including synthetic-noise bounds checks and
injected-signal recovery tests.

---

## 5. Science Output (Oumuamua 0011, channel 32)

All nine stages ran to completion and produced real tables. Verdict: **CLEAN** (honest negative).

| Stage | Verdict / key metric |
|---|---|
| `sk_gate` | CLEAN (skdev 1.145) |
| `xeno_scan` | XENO-CLEAN |
| `boxcar_bank` | no candidate above 14σ |
| `drift_hunt` | 0 kept |
| `frame_hunt` | no detection above gate |
| `lag_hunt` | all CLEAN |
| `fam_god` | no significant cyclic peak |
| `jerk_track` | jerk 34.2 Hz/s² (below sidereal anomaly gate) |
| `scint_pol` | SINGLE-POL, m=0.0 (no scintillation) |

---

## 6. Reproduce

```bash
# Slice one channel from a 17 GB raw file
tkc slice D:/data/raw/<file>.raw 32 ch32.f32 128 --pol 0

# Run the full 9-stage battery
tkc sweep ch32.f32 --out-dir reports/sweep/ --fs 2929687.5

# Verify all instruments
tkc prove
```

---

## 7. Notes on Legacy Comparison

The above are **measured, reproducible numbers** on this host. Legacy Python/NumPy pipelines
(`turboSETI` + `blimpy`/`rawspec` + `sigproc`) are typically reported to spend **1–3 minutes**
on the raw→filterbank conversion step alone for a file this size, then additional minutes for
the drift search. That is a **published/typical** figure, not something measured on this host —
no legacy stack is installed here, and no direct head-to-head was run.

The defensible claims from this benchmark are the ones measured above:
* 17 GB raw → calibrated voltage in **~2.2 s warm / ~11.9 s cold**
* full 9-instrument battery in **~14 s warm**
* 12/12 formal prove batteries in **3.47 s**
* all of it in a **1.30 MB binary with zero dependencies**
