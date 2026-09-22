# FRB121102 Scan 11 seg-0000 — FULL FILE — 2026-09-22

Full-segment Kain sweep. One chan/pol end to end, every block searched.
No Python in the hot path. Honest negative.

## Input

| field | value |
|---|---|
| file | `blc20_guppi_57991_49905_DIAG_FRB121102_0011.0000.raw` |
| size | 17,180,721,152 B, 128 blocks, BLOCSIZE 134217728 |
| geometry | OBSFREQ 6595.21 MHz, NCHAN 64, NPOL 4, NBITS 8, TBIN 3.41e-07 s |
| lane | chan 44, pol 0 → `frb_ch44_full.f32`, 67,108,864 samples (256 MB) |
| slice receipt | `receipt=PASS sliced=128` in 2.3 s (head 336 ms, read 431 ms, unpack 1235 ms) |

## Method

```
slice full 128 blocks (1×) → sk_gate + fold_sum + fam_scan on full 67M
boxcar_bank tiled 16×8 blocks (tool cap 4.19M samples/run) → full coverage, no truncation
boxcar geometry: --fs 2929687.5 --f0-mhz 6595.21 --bw-mhz 2.93 --dm-trials 64 --dm-max 2000 --thresh 14.0
```

## Results

| tool | result |
|---|---|
| `sk_gate` full 67M | skdev 1.370, frac 4e-4, **CLEAN** (0.15 s) |
| `fold_sum` full 67M | best 19.82 Hz @12.17σ, gate 16σ, **undetected** (24.3 s) |
| `fam_scan` full 67M | Y2/Y4 top ratio 1.11–1.13, gate 3.0, **CLEAN** (9.4 s) |
| `boxcar_bank` 16 tiles | **1/16 SHOT**, 15/16 CLEAN (see tile table) |

### Boxcar tiles (thresh 14.0σ, all bests width 1)

| tile | blocks | best σ | DM | t | verdict |
|---|---|---|---|---|---|
| 0 | 0–7 | 14.71 | 761.9 | 38453 | **SHOT** (the shakedown spike) |
| 1 | 8–15 | 11.42 | 1682.5 | 61935 | CLEAN |
| 2 | 16–23 | 12.95 | 1301.6 | 8185 | CLEAN |
| 3 | 24–31 | 11.14 | 857.1 | 42040 | CLEAN |
| 4 | 32–39 | 10.99 | 761.9 | 64439 | CLEAN |
| 5 | 40–47 | 12.36 | 0 | 21123 | CLEAN |
| 6 | 48–55 | 11.04 | 317.5 | 1113 | CLEAN |
| 7 | 56–63 | 11.86 | 984.1 | 52553 | CLEAN |
| 8 | 64–71 | 13.17 | 444.4 | 46728 | CLEAN |
| 9 | 72–79 | 13.90 | 1968.3 | 33178 | CLEAN |
| 10 | 80–87 | 10.78 | 1904.8 | 63996 | CLEAN |
| 11 | 88–95 | 10.04 | 1174.6 | 40863 | CLEAN |
| 12 | 96–103 | 12.87 | 698.4 | 19709 | CLEAN |
| 13 | 104–111 | 10.20 | 1555.6 | 6252 | CLEAN |
| 14 | 112–119 | 11.13 | 158.7 | 26672 | CLEAN |
| 15 | 120–127 | 11.53 | 476.2 | 26821 | CLEAN |

Per-tile CSVs: `pulse_tile_0.csv` … `pulse_tile_15.csv` (512 DM×width rows each).

## Why tile 0 is not a burst

Same three strikes as the shakedown: width 1 sample, flat across DM
(730–1714 all fire at t38453), no counterpart in SK/fold/FAM, and now —
**nothing like it in the other 120 blocks.** A repeater burst would be ms
wide at DM ~560 and would not sit alone as a single-sample spike in 67M
samples. Quarantined impulse, I2 max, no cadence survival.

## Floor and coverage (the product)

- pulse floor: 14σ gate; 15/16 tiles top 10.0–13.9σ, 1/16 at 14.71σ w1
- SK floor: frac 4e-4 full-file · fold floor: 12.17σ max · FAM floor: 1.13 max
- coverage: **100% of 1 segment** (128/128 blocks, chan 44 pol 0, all 67M
  samples across SK/fold/FAM, all 16 boxcar tiles) ≈ 1.2% of the 81-segment scan
- verdict: **no candidate, no WATCH.** Burst #94 is not in this subband.

## Timings (warm)

slice-full 2.3 s · sk 0.15 s · fold 24.3 s · fam 9.4 s · boxcar 16 tiles
(~3–4 s each). Full-segment sweep in about a minute plus fold.

## Tool versions

`slice 0.3.0` · `sk_gate 0.1.0` · `boxcar_bank 0.1.1` · `fold_sum 0.1.0` ·
`fam_scan 0.1.0`. Geometry by argv; raw stays on `D:/data/raw/`.

## Next

Same tiling on adjacent chans/pols (impulse census: is tile-0's spike
broadband?), `--start` depth already covered — done —, 0010-vs-0011
`cadence_pair` gate, µs-structure lane the filterbank era couldn't reach.
