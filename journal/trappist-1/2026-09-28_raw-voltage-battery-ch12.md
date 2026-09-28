---
target: trappist-1
date: 2026-09-28
author: muse-spark
campaign: trappist-raw-trial
disposition: HONEST-NEGATIVE
coverage: blc00 ch12 2216MHz 8.4M samples ON15 vs OFF16
instruments: slice,perm_entropy,fold_sum,frft_hunt,fam_god,xeno_scan,boxcar_bank,waterfall
tags: raw-voltage,trial-run,thermal-floor,impulse-texture,cadence-clean
verdict: HONEST-NEGATIVE
sky_row: TRAPPIST-1
reports: reports/2026-09-28_trappist_trial
related: journal/trappist-1/2026-09-28_blc00-2215mhz-comb-trial.md
---

## What I saw
First raw-voltage trial: sliced coarse chan 12 (~2216 MHz, 2.93 MHz BW, 8.4M samples/leg) from ON15 vs OFF16 .raw. Ran 7 instruments: perm_entropy (64/2048 ANOMALY-CHAOS both legs, Z 2-4, scattered), fold_sum (no detection, best 5.98 sig), frft_hunt (8 WATCH 20-30 sig at alpha=960 edge, identical in OFF), fam_god (row hits with log10p=-9999 MAD-floor blowup, track CLEAN), xeno_scan (XENO-CLEAN), boxcar_bank (best 13.07 sig below 14 gate, CLEAN), waterfall (thermal floor, +0.5 dB margin, PASS).

## Why I ruled it out
Every above-gate signature reproduced identically in OFF16: perm scatter (receiver texture), frft alpha-edge lock at -515kHz/s (broadband impulse smear, not sidereal 0.1-1 Hz/s), fam -9999 (documented numerics). Waterfall shows only horizontal broadband impulse streaks + flat floor. Honest negative with 7 receipts.

## What to check next time
Slice is fast (~0.5 s per 8.4M samples) — the raw-voltage funnel is viable at scale. Broadband impulses deserve a dedicated census (rate/hr) as they set the frft false-alarm floor. Next: drift-rate-tracked chirp search across full 128 blocks + Stokes V via dual-pol slice.
