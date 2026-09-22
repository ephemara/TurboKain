# HIP 57328 ON+OFF — Full-Pair Campaign — 2026-09-22

2-bit blc2 pair (4.2 GB each, 128 blocks): scans 0003 ON + 0004 OFF.
Chans 8/32/56, pol 0, full depth: 66.1M samples/leg-chan. All five detectors
+ cadence on all three pairs. First campaign with the full battery + gates.

## Detections (both pipelines agree)

| structure | where | strength |
|---|---|---|
| ~5.66 Hz periodicity + subharmonic ladder (/2 /3 /4 /5) | ALL chans, BOTH legs | 26–134σ (Kain), 4289σ + ladder (oracle) |
| Y2 cyclic line @178.81 Hz, bin 2 | ALL chans, BOTH legs | log10p −29…−1402 |

## Non-detections (floors)

SK quiet all six (frac ≤ 0.0014). Boxcar ≤ 11.55σ (gate 14) all six. Xeno
micro-battery CLEAN all six (no coh/ladder/DM/impuls). Single-pointing cap
respected throughout.

## Cadence (9 pairs)

| kind | ch8 | ch32 | ch56 |
|---|---|---|---|
| sk | CLEAN | CLEAN | CLEAN |
| fold | COMMON | COMMON | COMMON |
| fam | COMMON | COMMON | COMMON |

Zero WATCH (nothing ON-only). The two structures are common-mode in both
legs: scored COMMON, never blocked by us.

## Attribution read (for the veto, not from it)

Common to all chans, both legs, both pols implied (p0 measured): backend
oscillator complex. The 178.81 Hz line sits inside the catalogued 179 Hz
hum family (1186 catalog mentions); the ~5.67 Hz wobble (176 ms period)
rides with it, likely same machinery (5.67×32 ≈ 181). Xeno silence
constrains the physics: stationary power wobble, no packets, no combs, no
dispersion, no shots — consistent with rotating/pumping machinery, not
traffic (which would be noise-like to power detectors, not thousands of σ
in them). Veto scores STRUCTURE high + EARTH high → BLOCK with catalog +
multichan + ON+OFF receipt; the 5.67 Hz line specifically is veto review
(38 catalog mentions to audit).

Files: 6× `.f32` (gitignored, 264 MB each), sk/fam/fold/pulse/xeno tables
per leg-chan, 9 cadence verdicts. CSV mirrors partial (md tables are the
record; backfill flagged for future runs).
