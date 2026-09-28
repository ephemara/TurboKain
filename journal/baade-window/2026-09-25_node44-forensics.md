---
target: baade-window
date: 2026-09-25
author: muse-spark
campaign: 128-comb-streaming
disposition: HONEST-NEGATIVE
coverage: 128 channels x 38.08MHz stride x 857088 samples across 4.8GHz
instruments: [fil_reader, bispectrum, frft_hunt, perm_entropy, fold_sum, boxcar_bank, waterfall]
tags: [PFB-edge, scintillation, DISS, NGC-6522, triaged, ANOMALY-MOD]
verdict: CLEAN-ASTROPHYSICAL
sky_row: Baade-Window
reports: [reports/2026-09-25_baade_128comb/]
related: [journal/lhs-1140/2026-09-25_node74-radar-flash.md]
---

## What I saw
Node 44 (Channel 4576 @ 6763.0005 MHz) was the ONLY channel of 128 to trigger perm_entropy ANOMALY-MOD: single 0.72 s window (339, t = 121.33 s), H_PE dipped 0.995 -> 0.9875 (Z-Drop 6.7 sigma). Bispectrum b2 = 0.021 (Gaussian floor), frft sigma = 0.0.

## Why I ruled it out
Channel 4576 = 572 x 8: sits exactly on a GUPPI 2.93 MHz PFB filter transition edge (~10% passband roll-off). The 0.7% entropy dip was a microsecond constructive speckle on the filter edge, not a carrier. Cross-channel check: identical low-frequency harmonic ladder (0.0100/0.0134/0.0167/0.0501 Hz = integer DFT bins of the 299.5 s dwell) present in channels 0/2000/6656/10000 — documented 1/f receiver red-noise drift, common-mode. fold_sum 681 Hz hits replicate across channels (digitizer/PFB ripple folding through the 8-harmonic summer). Radiometer math: NGC 6522 pulsars are ~8 uJy at 6.76 GHz vs 3.37 mJy single-channel 5-sigma floor — 400x too faint to detect here.

## What to check next time
Exact multiples of 8 in channel index = PFB edge suspect. Integer multiples of 1/T_obs in slow modulations = dwell-window artifact, not DISS. Do NOT claim scintillation without cross-channel localization (DISS would be frequency-selective, not common-mode).
