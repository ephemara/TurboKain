# FRB121102 Scan 11 seg-0000 — Kain pipeline shakedown — 2026-09-22

First Kain-native look at repeating-FRB territory. No Python in the hot path.
One 17.2 GB GUPPI segment, three slices, five tools, one honest negative.

## Input

| field | value |
|---|---|
| file | `blc20_guppi_57991_49905_DIAG_FRB121102_0011.0000.raw` |
| path | `D:/data/raw/` (external tier, never in repo) |
| size | 17,180,721,152 B, 128 blocks, BLOCSIZE 134217728 |
| header | PROJID `AGBT17B_999_14`, OBSERVER `Vishal Gajjar`, SRC `DIAG_FRB121102` |
| geometry | OBSFREQ 6595.21 MHz, OBSBW −187.5 MHz, NCHAN 64, NPOL 4, NBITS 8, TBIN 3.41e-07 s, CHAN_BW −2.9296875 MHz |
| MJD | 57991.5776 = 2017-08-26 13:51:44 UT (the Gajjar storm night) |
| coverage this run | 16 blocks (~2 s), chans 44 + 30, pols 0 + 1 → 8,388,608 samples/slice (32 MB `.f32`) |

Slice bytes carry the standard receipt (`receipt=PASS sliced=16`). Probe-only
preflight on the full file passed quarantine before any bulk IO.

## Method

```
slice (ch/pol, 16 blocks) → sk_gate + boxcar_bank + fold_sum + fam_scan
boxcar geometry: --fs 2929687.5 --f0-mhz 6595.21 --bw-mhz 2.93 --dm-trials 64 --dm-max 2000 --thresh 14.0
boxcar cap: tool searches max 4,194,304 samples/run (half a slice) — coverage floor, not full slice
```

## Results

| tool | ch44 p0 | ch30 p0 | ch44 p1 |
|---|---|---|---|
| `sk_gate` | skdev 1.370, frac 4e-4, **CLEAN** | (slice only) | (slice only) |
| `boxcar_bank` best | 14.72σ DM 761.9 w1 t38453 **SHOT** | 14.74σ DM 1174.6 w1 t55330 **SHOT** | 15.64σ DM 1523.8 w1 t4779 **SHOT** |
| `fold_sum` (ch44p0) | best 3.26 Hz @8.30σ, **undetected** (16σ gate) | — | — |
| `fam_scan` (ch44p0) | Y2/Y4 top ratio 1.40–1.45, gate 3.0, **CLEAN** | — | — |

Full tables: `pulse*.csv` (512-row DM×width grids), `sk.md`, `fold.md` (top-8),
`fam.md` + `fam_cand.txt` (top-8 Y2/Y4). CSV mirrors alongside every md.

## Why the SHOTs are not bursts (receipt, not vibe)

1. **Width is 1 sample everywhere** (~0.34 µs). A C-band FRB at DM ~560 is
   milliseconds wide after dedispersion, spanning 1000s of our samples.
2. **Flat across DM.** Same timestamp fires at DM 730, 762, 794, 1683, 1714…
   A real dispersed pulse peaks at one DM and falls off. Flat = broadband
   impulse with no dispersion sweep.
3. **Wrong DM, different clock per lane.** Best DMs (762 / 1175 / 1524) sit
   nowhere near 121102's ~560, and each chan/pol trips at its own `t`
   (38453 vs 55330 vs 4779). A sky burst lands at one `t` across adjacent
   chans with a frequency-dependent delay. These don't coincide.
4. **Companion gates quiet.** SK spectral-kurtosis CLEAN on all legs, fold
   undetected (8.3σ vs 16σ gate), FAM ratios ~1.4 vs 3.0 gate. Impulsive in
   time, blank in spectrum and periodicity — digitizer/packet/RFI spikes,
   quarantined, not candidates.

No WATCH. No candidate. Single-file cap stays at I2 by rule; nothing here
would survive a 0010-vs-0011 cadence gate anyway.

## Floor and coverage (the actual product)

- pulse floor: 14σ gate, tops 14.7–15.6σ all w1 zero-DM-like impulses
- SK floor: deviant-bin frac 4e-4, skdev 1.37
- fold floor: 8.3σ max vs 16σ gate (top 3.26 Hz)
- FAM floor: max ratio 1.45 vs 3.0 gate
- coverage: 2 chans × 2 pols × 16/128 blocks × 4.19M/8.39M samples searched —
  roughly 1% of one segment of an 81-segment (1.38 TB) scan

## Timings (warm, per leg)

slice 0.38 s · sk_gate 0.16 s · boxcar 0.76–4.2 s · fold 0.75 s · fam 1.27 s.
Whole shakedown: seconds, every tool exit 0 with `receipt=PASS`.

## Tool versions

`slice 0.3.0` · `sk_gate 0.1.0` · `boxcar_bank 0.1.1` · `fold_sum 0.1.0` ·
`fam_scan 0.1.0`. C-band geometry passed by argv, no hardcoded paths.

## Next

Deeper `--start` blocks on this segment, full 128-block slice with tiled
boxcar (4M cap must be tiled, not truncated), chan sweep for the RFI-spike
census, 0010-vs-0011 `cadence_pair` gate, coherent-µs lane for the
microstructure space filterbanks can't reach.
