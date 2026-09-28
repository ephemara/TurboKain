---
target: lhs-1140
date: 2026-09-25
author: muse-spark
campaign: 128-comb-cadence
disposition: HONEST-NEGATIVE
coverage: 128 nodes x 11.72MHz stride across 1.5GHz (751-2251 MHz)
instruments: [fil_reader, perm_entropy, bispectrum, frft_hunt, waterfall]
eirp_floor_w: 4.2e11
tags: [radar-flash, ARSR-4, ON-only, triaged, water-hole, candidate-kill]
verdict: ATTRIBUTED-TERRESTRIAL
sky_row: LHS-1140
reports: [reports/2026-09-25_lhs1140_128comb/]
related: [journal/baade-window/2026-09-25_node44-forensics.md]
---

## What I saw
Node 74 @ 1384.277 MHz: 163.04 sigma in Scan 0002 (ON1), -0.05 sigma in Scan 0004 (ON2). Single ON-only burst — the only CANDIDATE-ON1 out of 128 coarse sub-bands. Time steps 12-13 spiked to 45x/23x baseline power (~1.1e12 vs 2.3e10), steps 0-11 and 14-15 dead quiet.

## Why I ruled it out
Waterfall showed two intense horizontal broadband swaths spanning the full >2.9 MHz passband at the burst timestamps — broadband flash, not a narrowband carrier. Bispectrum gave b2 = 0.992 phase-locked to the 2861 Hz GUPPI sampling clock (digitizer saturation signature). Frequency sits inside the FAA ARSR-4 L-band air-surveillance radar allocation (1215-1400 MHz) illuminating GBT sidelobes. No Doppler drift, no modulation (perm_entropy clean on the carrier itself).

## What to check next time
Cross-check L-band radar activity windows before flagging ON-only bursts. Compare against baade-window Node 44 entry: same surface symptom (isolated ON-only spike), opposite physics (there: PFB-edge scintillation speckle; here: broadband radar saturation). The discriminator is waterfall morphology (vertical carrier + horizontal swaths = radar) plus b2 ~ 1.0 clock lock.
