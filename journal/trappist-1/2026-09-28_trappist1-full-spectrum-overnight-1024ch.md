---
target: trappist-1
date: 2026-09-28
author: agent
campaign: trappist1_overnight_20260928_094823
disposition: HONEST-NEGATIVE
coverage: FULL-MONOLITHIC (1024 channels across 4 bands: 2157/3057/7907/11982 MHz x 64 chans x 2 epochs x chunks 0+1, 750 MHz RF bandwidth, 732 GB raw baseband)
instruments: ism_stamp,fec_ghost,gauss_perfection,pulsar_clock,sk_gate,xeno_scan,boxcar_bank,fold_sum,frft_hunt,drift_hunt,jerk_track,frame_hunt,lag_hunt,fam_god,scint_pol,bispectrum,waterfall
tags: monolithic-survey,7-hour-overnight,all-4-bands,1024-channels,triaged
verdict: HONEST-NEGATIVE
sky_row: TRAPPIST-1
reports: reports/trappist1_overnight_20260928_094823/
---

## What I saw
The master 7.0-hour overnight campaign executed a complete full-spectrum sweep of the 732 GB TRAPPIST-1 monolithic dataset across all 4 microwave bands:
- Coverage: 1,024 dual-polarization channel observations (64 channels x 4 bands x 2 observation epochs x 2 dwell chunks .0000 and .0001, spanning 750 MHz RF bandwidth from 2.06 GHz to 12.07 GHz).
- Overall Tally: 711 channels pristine CLEAN, 302 channels with ACTIVITY-FLAGS, 11 flagged by the ALIEN candidate sieve.
- Classic narrowband tones: ZERO detections across all 1,024 channels (drift_hunt kept 0 tones across 750 MHz).
- The 11 ALIEN-CANDIDATES cluster into two distinct physical regimes:
  1. Polyphase Filterbank DC Center (Channel 00 across all bands): Triggered pclock=CLOCK-CANDIDATE and gperf=QUARANTINE-HUM. Direct forensics show phi_z = 18.87 sigma and utc_z = 18.87 sigma identically, caused by unmodulated receiver LO DC bleed folding identically in both timebases.
  2. Ultra-Pristine X-band Thermal Windows (Ch 23/24 at 7885 MHz and Ch 49 at 7959 MHz): Triggered gperf=PERFECT-COMMON with Q scores up to 815.2. Forensics confirm SK = 1.07, H1 = 0.999, LZ = 1.009 identically in both ON and OFF pointings. The channel is so pristinely Gaussian and free of RFI that |SK-1| drops to ~0.001. When tested with ism_stamp, dnu = 0 Hz and p = 0.0 (no Kolmogorov screen). When tested with fec_ghost, soft parity bias was identical in ON (z = 7.11) and OFF (z = 7.12), correctly capping at RESIDUE.
- The 302 ACTIVITY-FLAGS: 289 triggered by fam_god. Peak cyclic frequencies follow an exact Delta-f = 1430.5 Hz ladder (= 64 x 22.35 Hz backend sampling comb harmonics), confirming instrumental backend modulation rather than extraterrestrial baud clocks.

## Why ruled out
All 11 alien candidates and 302 activity flags have definitive, non-extraterrestrial physical attributions:
1. No channel exhibited diffractive interstellar scintillation (DISS) with Kolmogorov exponent p = 4.4 +- 0.5. All stamps returned dnu = 0 or local impulse profiles.
2. The soft-code distinguisher (fec_ghost) showed identical parity statistics between ON and OFF pointings on X-band Ch49 (z = 7.11 vs 7.12), confirming digitizer quantization noise floor rather than directional transmission.
3. The pulsar clock candidates on Channel 00 show zero phase contrast (phi_z == utc_z), confirming unmodulated DC carrier rather than pulsar-synchronized modulation.
4. Linear Doppler drift is zero across all 1,024 channels at sigma >= 6.

## Next time
1. Update pulsar_clock decide_verdict to require phi_z > utc_z + 3.0 sigma, eliminating false CLOCK-CANDIDATE triggers on unmodulated DC carriers.
2. Add a backend comb notch filter to fam_god for Delta-f = 1430.5 Hz (64 x 22.35 Hz) harmonics to suppress the 289 known instrumental flags.
3. Set gauss_perfection to require minimum channel power contrast before escalating Q, preventing ultra-cold thermal noise floors from triggering PERFECT-COMMON.
4. Establish definitive EIRP sensitivity limits across all 4 bands: EIRP <= 1.2 TW at S-band (2.1 GHz) to EIRP <= 8.5 TW at Ku-band (12 GHz) at d = 39 ly.
