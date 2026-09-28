---
target: trappist-1
date: 2026-09-28
author: agent
campaign: 2026-09-28_trappist_alien
disposition: ATTRIBUTED-TERRESTRIAL
coverage: PARTIAL (blc00 Ch36 dual-pol x 32 blocks ON 0017 + OFF 0016, 5.7 s each leg)
instruments: ism_stamp,fec_ghost,gauss_perfection,pulsar_clock,boxcar_bank,fam_god,lag_hunt,xeno_scan,subspace_null,waterfall
tags: backend-comb,impulsive-ingress,ON-only,first-light,triaged
verdict: ATTRIBUTED-TERRESTRIAL
reports: reports/2026-09-28_trappist_alien/on_sweep/,reports/2026-09-28_trappist_alien/off_sweep/
---

## What I saw
First-light run of the full alien suite (ism_stamp / fec_ghost / gauss_perfection / pulsar_clock, all built today) on TRAPPIST-1 blc00 L-band Ch36, ON 0017 vs OFF 0016, 32 blocks x 16.7M samples dual-pol.
- ON is an impulsive storm: boxcar 256 SHOTs ALL DM=0 w=1-2 sigma~5000+, xeno XENO-STRONG (kurt 1375, tailx 4), SK flag=1 dev=46.2, OFF has 0 SHOTs and stamp m=0.0 (quiet).
- FAM ladder on ON: 1072.8 / 3218.6 / 4649.1 / 6079.6 / 7510.1 / 8940.6 / 10371.2 / 11801.7 Hz = EXACTLY 48,144,208,272,336,400,464,528 x 22.35 Hz backend comb fundamental. LAG WATCH n=7 sig=76.3 rides the same train.
- Alien lanes: stamp CLEAN (m=1.2 spiky, xcorr=0.91 broadband-simultaneous, dnu=0, no dispersion), ghost CLEAN both legs (ON z=572, OFF z=528, gate 666), gperf CLEAN, pclock CLEAN (phi=utc). Ghost correctly auto-skipped in sweep (stamp null).

## Why ruled out
Three independent terrestrial receipts: (1) DM=0 + w=1-2 + sigma~5000 + ON-only + xcorr 0.91 = near-field impulsive ingress, same family as the 0017 S-band rail-hitting event, now seen in L-band; (2) FAM ladder = integer harmonics of the known 22.35 Hz backend comb (48x-528x), not a baud comb; (3) no ISM stamp (dnu=0, no exponent, no RM swing beyond local) and no code ghost on either leg. Common-mode+unstructured = block; ON-only+unstructured-impulsive = terrestrial ingress.

## Next time
- Nominate 1430.5 Hz (=64x22.35) explicitly in the RFI catalog as backend-comb territory; FAM should carry a hum-harmonic mask so N-harmonic ladders auto-quarantine instead of HIT.
- boxcar SHOTs at sigma>1000 with w<=2 and DM=0 deserve an automatic TERRESTRIAL-IMPULSE label (rail-check via peak sample) rather than SHOT.
- Revisit Ch36 with longer dwell (128 blocks) to push ghost gate down; current floor z~572/666 on impulsive RFI.
- S-band blc02 Ch36 (2157 MHz, the subspace_null 8-block case) still needs the same alien-suite pass when that raw is on disk.
