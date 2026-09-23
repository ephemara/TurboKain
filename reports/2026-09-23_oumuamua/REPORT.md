# 'OUMUAMUA REPORT — S-band ON/OFF cadence (first interstellar visitor)

Date: 2026-09-23. Target: 1I/'Oumuamua, MJD 58100 (2017-12-13), GBT S-band.
ON: `blc02_guppi_58100_78802_OUMUAMUA_0011.0000.raw` (17.18 GB, 120 blocks)
OFF: `blc02_guppi_58100_79116_OUMUAMUA_OFF_0012.0000.raw` (17.18 GB, 1° off)
Sub-band blc02: fch 2682.71 MHz, 8-bit, 64 ch × 4 pol, fs 2929687.5 Hz.
Manifest: `D:/data/download_manifest.csv`. Report dir: this folder.

## Why this target

Highest probe-prior per byte in the sky: the only interstellar object with
voltage data + a true ON/OFF cadence pair. At ~1 AU, even milliwatt leakage
shows. Bystander-optimal: an inert rock needs no transmitter; a visited
relay/probe does. S-band is quiet Hannah-country vs C-band sat hell.

## Coverage

| lane | scope | result |
|---|---|---|
| sk_gate triage | 64/64 chans × ON+OFF, full 120 blocks (128 tables) | **ALL CLEAN** |
| xeno_scan | ch44 p0, 16 blocks, ON+OFF | CLEAN/CLEAN (coh identical 1.39 both legs = common backend clock) |
| fold_sum (--fs fixed) | ch44, 16-blk + FULL 62.9M, ON+OFF | undetected (8.6/6.5 shakedown; 9.7/11.3 full vs 16 gate) |
| fam_god | ch44, 16-blk + FULL, ON+OFF | CLEAN ×4 |
| drift_hunt | ch44 p0 ON+OFF | 0 hits both (no drifting tones) |
| frame_hunt | ch44 p0 ON+OFF | undetected (4.4/7.1σ vs 40) |
| boxcar_bank | ch44: 30 tiles (15 ON + 15 OFF, full 120-block span) | 3 ON SHOT / 0 OFF (see §3) |
| cadence_pair | pulse ON vs OFF, σ≥14.0 | WATCH (1423 vs 1338) → DOWNGRADED (§3) |

## The 3 SHOTs (quarantined, with receipts)

| tile | dm | w | σ | t |
|---|---|---|---|---|
| on_t0 | 967.74 | 1 | 14.23 | 47233 |
| on_t12 | 774.19 | 1 | 14.02 | 36151 |
| on_t14 | 483.87 | 1 | 15.14 | 45570 |

All width-1, scattered DMs/times, 14.0–15.1σ over an 11–13σ w1 background
population present in BOTH legs (OFF tops 10.4–13.4, same shape). This is the
known single-sample impulse family (FRB precedent: same signature, same
verdict). No width>1 corroboration, no DM clustering, no companion gate
(SK/xeno/fold/fam/drift/frame all quiet), no narrowband, no periodicity.
3-vs-0 across 15+15 tiles at a threshold-edge gate: Fisher exact p≈0.22 —
NOT a significant ON excess. **Downgrade: QUARANTINE-impulse, not WATCH.**
The cadence WATCH stays on record above; this rationale is the veto feed
(re-scored and named, never hidden).

## Floor (what we did NOT do)

- 1 deep channel (ch44 p0) + SK triage on all 64. Other 63 chans unsearched
  by fold/fam/boxcar/drift/frame/xeno.
- pol0 only; pol1–3 untouched (impulse triage precedent: single-pol w1
  needs no pol follow-up; a real candidate would).
- blc02 sub-band only (187.5 MHz of ~750 MHz S-band; blc03–05 archived).
- boxcar 14.0σ gate over 11–13σ w1 background: threshold-edge population,
  single-epoch pair, no persistence evidence → I2 max regardless.

## Verdict

**Honest negative. No candidate, no WATCH (downgraded with receipts).**
'Oumuamua's S-band face is quiet to: SK 128/128, fold 11σ max full-file,
FAM CLEAN, zero drifters, frame 7σ max, and an impulse population
indistinguishable ON vs OFF. If it phones home, not in blc02 on this night,
not above this floor.
