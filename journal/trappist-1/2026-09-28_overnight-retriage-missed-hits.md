---
target: trappist-1
date: 2026-09-28
author: agent
campaign: trappist1_overnight_20260928_094823-retriage
disposition: HONEST-NEGATIVE
coverage: RETRO-Triage over 1024 chan dirs (warehouse + targeted ON/OFF re-slices, 32-block, same fs)
instruments: fold_sum,lag_hunt,drift_hunt,packet_hunt,boxcar_bank,waterfall,xeno_scan,sk_gate
tags: retriage,missed-hits,fold-ON-only,lag-ON-only,impulse-storm,triage-bug,WATCH
verdict: HONEST-NEGATIVE-WITH-3-WATCH
reports: reports/trappist1_overnight_20260928_094823/
---

## What I saw
Re-mined the 1,024-channel overnight (reports/trappist1_overnight_20260928_094823, 732 GB, 4 bands x 2 epochs x 2 chunks) because its triage only read the FIRST ROW of 6 lanes (sk/xeno/box/drift/fam/jerk) and never looked at fold, lag, packet, raster, scint, frame at all. Two of its column reads are out-of-range (drift col-4 on a 4-col CSV, so on_drift=CLEAN 1024/1024 by construction). The warehouse already held the full tables, so I cross-matched every lane against summary.tsv CLEAN labels and re-sliced raw ON/OFF pairs from D:/data/campaigns/trappist1 for cadence checks (32-block slices, same as campaign; slices in _tmp/retriage, deleted f32s were re-cut from raw).

Missed hits that survive ON-vs-OFF:

1. Ku Ep2 ck0 ch45 (12.022 GHz) fold 23.2σ @1250.52 Hz with a full harmonic ladder (1250/625/417/313 Hz = 1, 1/2, 1/3, 1/4). ON pol0 detected=1; OFF pol0 9.8σ detected=0 at a different freq; ON pol1 10.3σ not-detected; Ep1 same channel 1.4σ; neighbors ch43/44/46/47 all <=11.4σ not-detected. Waterfall is thermal (no tone, P(t) flat) — pure power-envelope periodicity. ON-only, single-epoch, single-pol, single-chunk.
2. S Ep1 ck1 ch58 (2.235 GHz) fold 21.65σ @1635.2 Hz. ON pol0 21.6 detected=1, ON pol1 7.9σ at the SAME freq (polarized trace, not single-pol glitch), OFF 7.7σ, same-epoch chunk0 5.7σ. Chunk-transient (~5 s timescale), single-epoch.
3. S Ep1 ck0 ch12 (2.100 GHz) lag 53.7σ PERIODIC @108.5 kHz (lag 27 samples). Re-sliced: ON 53.7σ POWER/PERIODIC vs OFF 2.2σ CLEAN — 25x ON-only contrast. Strongest non-storm lag hit in the whole campaign.
4. S-band Ep2 impulse storm (0017 vs 0018, the known Ch36-storm epoch): ~100+ channels SHOT in Ep2 only. Deepest sample ch04: ON DM0 w=1..128 all SHOT peaking 23100σ at t=48181 vs OFF 8.3σ CLEAN (2800x). Per-channel t differs (48180/55440/30484...), SK-FLAG skdev 53.3, xeno SK+IMP kurt 2526 maxz 90, scint SPIKY, lag PERIODIC ~108-117 kHz. Broadband ON-only ingress — same family as the journaled Ch36 storm, but the overnight report never attributed it (left as generic ACTIVITY-FLAG among 302 fam-comb flags).

Demoted on re-check:
5. Drift lane: 247 dedop rows were hidden by the col-4 bug. Brightest non-DC ku Ep1 ck0 ch34 183σ stationary @1400390529 Hz re-slices to ON 183 vs OFF 173 at the SAME freq — COMMON terrestrial, ruled out. Ch00 DC hum (400kσ) already known PFB LO bleed.
6. Packet lane: 7x BARKER-PERIODIC-LOCKED + 10x CCSDS-SNIP were never triaged. Brightest sc Ep1 ck1 ch32 (278 hits, stride 5663) re-slices to ON-lock vs OFF 247-hits-no-lock; s Ep1 ck1 ch31 (116 vs 114) flips lock on a 2-hit difference. Both legs sit on a high floor (~250/~115 raw) from the known Barker false-hit family — lock is FRAGILE, not a sky frame. Do not promote without a second epoch at the same stride.

## Why ruled out
Nothing promotes past WATCH/RESIDUE. Ku ch45 and S ch58 folds are ON-only but single-epoch, single-chunk (ch58 dual-pol trace is the most interesting detail and still only one 5-s chunk), with zero drift tone, zero ISM stamp (dnu=0), zero ghost, zero xeno, and no repeat in the other epoch — exactly what a pointing-dependent RFI burst or a recorder artifact looks like, and nothing like a persistent sky transmitter. The lag 108 kHz hit is powerful but lone-lane (fold/xeno/drift quiet on that channel). The Ep2 storm is DM0 + ON-only + SK+IMP + SPIKY = near-field ingress, matching the already-attributed Ch36 storm receipts. Packet locks fail the robustness test (OFF nearly identical raw counts). Drift ch34 is in both legs. Grade: 3x WATCH (folds + lag) + storm ATTRIBUTED-TERRESTRIAL + packet NOISE-FAMILY + drift COMMON.

## Next time
1. Fix trappist1_overnight_master.py read_verdict indices (drift col 3 kind not col 4; audit every lane) and triage ALL lanes — fold detected, lag PERIODIC/XENO, packet FRAMED/LOCKED, raster SYNC/PICTORIAL, scint SPIKY, sk FLAG — not just first-row sk/xeno/box/fam. A CLEAN label must mean all lanes quiet, not 6 first-rows quiet.
2. Stop deleting OFF slices before unify can cadence-gate; sweep ON-only + single-pointing unify caps everything at listed-structures, so ON-only vs COMMON is never actually tested in-campaign.
3. Promote ku ch45 (1250 Hz ladder), s ch58 (1635 Hz dual-pol chunk flash), s ch12 (108.5 kHz lag) to the re-observe list: same RF, both pols, both epochs, 128-block dwell, with ISM stamp + ghost on the re-cut. If any repeats at the same freq/period in a second epoch it becomes a real candidate; until then they are WATCH.
4. Add Barker-floor calibration to packet_hunt (report expected false-lock rate at 1M bits) so 278-vs-247 stops looking like a detection.
