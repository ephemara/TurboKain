# TurboKain Scientific Waterfall & Diagnostic HUD Gallery

This gallery showcases 1920×1080 multi-panel diagnostic PNG dashboards generated directly by **`waterfall.kn`** (TurboKain Tool 16) through native Kain. 

Every image is serialized natively via LLVM with uncompressed Deflate, table-driven CRC-32, and Adler-32. Each dashboard unifies 2D dynamic spectra with three synchronized 1D projections ($P(f)$, $P(t)$, $SK(f)$), full mission provenance, a 10-instrument detector matrix, and harvested candidate logs.

---

## The Gallery

### 1. `01_proxima_b_drifting_carrier_turbo.png`
* **Scenario**: Extraterrestrial candidate narrowband drifting beacon from an exoplanet.
* **Colormap**: Google/NASA `turbo`.
* **Diagnostics**:
  - **Panel 1 ($P(f)$)**: Narrow carrier peak (+4.5 dB above median) detected and pinpointed with a golden callout pin at **1420.6 MHz**.
  - **Panel 2 ($P(t, f)$)**: Linear Doppler drift trajectory crossing the time domain with an overlaid tracking vector, target crosshairs, and candidate badge (`CAND #1: 1420.6MHz`).
  - **Panel 3 ($P(t)$)**: Stable Gaussian thermal noise envelope (no broadband pulsed contamination).
  - **Panel 4 ($SK(f)$)**: Clean $SK \approx 1.0$ nominal Gaussian noise baseline across off-carrier channels.

---

### 2. `02_psr_b0329_periodic_pulses_inferno.png`
* **Scenario**: Radio pulsar PSR B0329+54 pulse train.
* **Colormap**: Astronomical `inferno`.
* **Diagnostics**:
  - **Panel 2 ($P(t, f)$)**: Periodic broadband horizontal pulse bars flashing across the entire 2.9 MHz band at exact 0.12s intervals.
  - **Panel 3 ($P(t)$)**: Massive periodic power spikes soaring from the 22.3 dB baseline up to **36.3 dB** (+14 dB impulsive excursion).
  - **Panel 4 ($SK(f)$)**: Broadband Spectral Kurtosis elevation indicating non-Gaussian impulsive statistics across the entire band.

---

### 3. `03_terrestrial_rfi_comb_turbo.png`
* **Scenario**: Local terrestrial clock interference (local oscillator leakage with square-wave duty cycle).
* **Colormap**: Google/NASA `turbo`.
* **Diagnostics**:
  - **Panel 1 ($P(f)$)**: Three sharp, stationary clock harmonic spikes at fixed frequencies (+13.9 dB above median).
  - **Panel 2 ($P(t, f)$)**: Vertical stationary lines with zero Doppler drift ($\dot{f} = 0.0$ Hz/s) blinking with the clock duty cycle.
  - **Panel 4 ($SK(f)$)**: Channel kurtosis spiking far above the red dashed threshold ($SK > 1.8$), immediately identifying and flagging the channels as terrestrial RFI.

---

### 4. `04_frb_121102_dispersed_chirp_inferno.png`
* **Scenario**: Fast Radio Burst (FRB 121102 repeater) with astrophysical interstellar plasma dispersion ($t(f) \propto \text{DM}/f^2$).
* **Colormap**: Astronomical `inferno`.
* **Diagnostics**:
  - **Panel 2 ($P(t, f)$)**: Parabolic sweep trajectory sweeping across the 2.9 MHz frequency band.
  - **Panel 3 ($P(t)$)**: Localized energy transient centered at the burst arrival time.
  - **Panel 4 ($SK(f)$)**: Spectral Kurtosis elevated specifically across the swept dispersion band (53.7% flagged channels).

---

### 5. `05_sgr_a_star_real_sky_inferno.png`
* **Scenario**: Real telescope data from the archive (Galactic Center Sgr A* / unified demo scan, 66+ million float samples, 264 MB).
* **Colormap**: Astronomical `inferno`.
* **Diagnostics**:
  - **Panel 1 ($P(f)$)**: Real GUPPI baseband bandpass structure showing telescope sensitivity curve.
  - **Panel 2 ($P(t, f)$)**: Full 22.5s observation dynamic spectrum computed from 1024-point Hann-windowed STFTs.
  - **Panel 6 (Telemetry HUD)**: Live harvested verdicts from the sweep: `[FAM_GOD] HIT` ($\alpha = 178.8$ Hz), `[FOLD_SUM] HIT` ($P = 58.7$ ms).
  - **Panel 7 (Candidate Log)**: Actual harvested candidate rows from `evidence.csv`:
    - `#01 fam FAM f=178.8Hz sig=1.1 HIT`
    - `#02 fold FOLD f=17.0Hz sig=365.3 HIT`
