# Drift + Frame shakedown on 17 GB TRAPPIST scans — REPORT

**Date:** 2026-09-22 · **Tools:** `drift_hunt` 09 + `frame_hunt` 10 (both re-proven
post-change: drift 4/4, frame 9/9) · **Data:** `D:/data/raw/` blc04 full scans

## Coverage

| scan | file | point | blocks |
|---|---|---|---|
| ON 0017 | blc04_guppi_57807_75885_DIAG_TRAPPIST1_0017.0001.raw | TRAPPIST-1 | 128 (~23 s) |
| OFF 0018 | blc04_guppi_57807_75965_DIAG_TRAPPIST1_OFF_0018.0000.raw | ~1 deg off | 128 (~23 s) |

Channels **60, 63** (kurt-storm band) + **32** (quiet control), pol 0, full
67,108,864 samples each → `slices/` (6 × 256 MB .f32).

- **drift:** 16 tiles × 4,194,304 samples (1.43 s) per slice = **96 runs**,
  grid ±2000 Hz/s @ 100 step, nfft 4096, gate 8σ. `drift_summary.tsv`.
- **frame:** 4 tiles × 16,777,216 samples (5.7 s) per slice = **24 runs**,
  dec 512, block-normalised (524288), gate 40σ. `frame_summary.tsv`.

## Results

- **drift: 96/96 tiles kept=0.** No fast drifter anywhere at 8σ.
- **frame: 24/24 tiles detected=0.** Maxima 2.3–22σ vs the 40σ gate.

## Analysis (the interesting part is below the gate)

**Strongest feature in the whole campaign: ON ch63 tile 1 (blocks ~32–63,
mid-scan) — a ~100 ms family at 17–22σ**
(99.6/45.2/62.2/35.5/49.7/27.6/124.5/83.0 ms — harmonics of ~25 ms / 40 Hz).
It is **tile-local**: the three adjacent tiles report 41 ms@5σ, 498 ms@7σ,
6.75 ms@9σ. A continuous link (§3.2: present block 0 through 127) does not
do that. Below gate by ~2×. Verdict: transient quasi-periodicity, worth a
re-look, not a candidate.

**OFF ch63 tiles 0–1 share an ~18 ms family at 7–11σ** (56 Hz neighbourhood),
gone in tiles 2–3. Same story: local in time, sub-gate, and OFF-present
(terrestrial class by cadence even if it ever crossed gate).

**The kurt-storm channel (ch60) is boring in frame space (≤8σ).** Consistent
with the resolved verdict: the storm is aperiodic impulses + a 1430 Hz
spectral comb (0.7 ms period — deliberately below our 1 ms floor). Impulses
have no rhythm; the comb lives in frequency, not in the envelope. Two
instruments agreeing that the storm is structureless in time is itself a
receipt.

**The 179 Hz backend hum appears in no top-8 table** (searched 559/279
period rows across all 24). Either its envelope depth is below ~5σ on these
slices or it lives in voltage phase the envelope discards. Follow-up, not a
contradiction: the hum was a voltage-spectrum measurement.

## Verdict

**Honest negative with floors.** No drifting tone ≥8σ resolvable at
~500 Hz/s tiles; no frame period ≥40σ in any 5.7 s tile of either scan.
Nothing is ON-only over gate; the two strongest sub-gate families are
tile-local (transient) or OFF-present (terrestrial class). Nothing here
clears I3; nothing to escalate.

## Method note (self-caught)

The first sweep of this campaign searched tile 0 of every file N times:
`--skip-samples` offset the decode buffer but the read always started at
byte 0 (identical numbers tile-to-tile gave it away). Fixed with a real
`SetFilePointer` seek, verified adjacent-tiles-differ / same-tile-reproduces
bitwise, both tools re-proven, full sweep re-run, stale dupes deleted. The
numbers above are the re-run.

## Follow-ups

1. Pols 1–3 (this was pol 0 only) and the ch57–62 band sweep.
2. ch63 ~100 ms / ~18 ms families at lower gate for characterisation
   (power-supply / backend periodicity census — veto training data, M1).
3. Minute-scale chained tiles for sidereal-rate drift (M3); current tiles
   are blind below ~500 Hz/s by resol physics.
4. 179 Hz hum: targeted voltage-spectrum check vs envelope-depth upper limit.
