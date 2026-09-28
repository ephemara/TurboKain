---
target: trappist-1
date: 2026-09-28
author: muse-spark
campaign: trappist-trial-blc00
disposition: HONEST-NEGATIVE
coverage: blc00 67M chans 2064-2251MHz, scans 0015-0023
instruments: fil_reader
tags: comb,transient-RFI,satellite-downlink,ON-only,trial-run,cadence-kill
verdict: TRANSIENT-RFI
sky_row: TRAPPIST-1
reports: reports/2026-09-28_trappist_trial
related: journal/lhs-1140/2026-09-25_node74-radar-flash.md
---

## What I saw
Trial run on first sealed scans (blc00 node, 67M chans, 2064-2251 MHz). ON15/OFF16 sweep found 165 ON-only channels in 49 clusters. Cadence check vs ON17/OFF18 killed all wide blocks (identical SNR values mirrored around 2250.0 MHz = PFB Nyquist mirror images) and all singletons except ONE feature: 9 single-channel tones at 2215.8294-2215.9573 MHz, 10-18 sig in BOTH ON15 and ON17, quiet in both OFFs. 14-16 kHz spacing over 128 kHz. Drift check in ON20 (7 min later): zero channels above 6 sig in a 140 kHz window. Dead by epoch 3.

## Why I ruled it out
Transient, not persistent: present in two consecutive ONs ~3 min apart, gone 7 min later with no drifted counterpart. 2215.9 MHz sits in the 2200-2290 MHz Space-to-Earth satellite downlink allocation. Single 2.79-Hz channels with 14-16 kHz spacing = transponder comb morphology. ON17's broadband floor ran 5x hot vs other scans (system-temp jump), yet tones held 10-15 sig above it — strong but transient = satellite pass through the beam, not sky. Max grade I2, triaged TRANSIENT-RFI.

## What to check next time
When saturation completes: (1) check blc01/blc04 nodes for the same comb, (2) pull raw-voltage time series for Doppler drift, (3) confirm absence in 0020/0021/0022/0023 already done for blc00. Rule: ON-ON survival is necessary but NOT sufficient — demand epoch-3 persistence before escalation.
