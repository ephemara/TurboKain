---
target: tic-458478250
date: 2026-09-25
author: muse-spark
campaign: 128-comb-xband
disposition: HONEST-NEGATIVE
coverage: 128 nodes x 25.82MHz stride across 3.3GHz (7.80-11.10 GHz)
instruments: [h5_reader, bispectrum, frft_hunt, perm_entropy, waterfall]
eirp_floor_w: 3.4e13
tags: [LO-intermod, 2861Hz-clock, DSN-band, H90a, triaged]
verdict: ATTRIBUTED-INTERMOD-RFI
sky_row: TIC-458478250
reports: [reports/2026-09-25_tic458478250_128comb/]
related: []
---

## What I saw
1.18B-channel X-band sweep, 128 coarse nodes. Two hot carriers: DSN window 8419.9219 MHz (31,363 sigma) and H90a window 8932.6172 MHz (135,841 sigma). 120/128 nodes clean thermal floor (1.3-5.3 sigma). 8 elevated nodes total.

## Why I ruled it out
Bispectrum: b2 = 0.999, biphase exactly 0.0 deg, full HARMONIC-2F ladder (1,1,2)...(7,7,14) locked to f0 = 2861.0 Hz GUPPI sampling clock. frft_hunt: drift 0.00 Hz/s on both (sidereal X-band demands 0.6-2.0 Hz/s from Earth rotation). Zero-drift + perfect clock phase lock = internal ADC spur, twice over.

## What to check next time
Any b2 > 0.9 with phi_B = 0.0 exactly is the digitizer until proven otherwise. The 2861 Hz comb is the first thing to test on any new X-band target — check journal tag LO-intermod before burning waterfall renders.
