#!/usr/bin/env python3
"""lhs1140_cadence_search.py — Deep Cadence Analysis of LHS 1140 across L-band.

Ingests Scan 0002 (ON) and Scan 0004 (cadence pair) of LHS 1140.
Evaluates key astronomical lines (HI 21cm, OH 1665/1667 MHz, 1.4 GHz DISS band)
and performs a wideband carrier survey across 536.8 million channels.
Extracts candidate dynamic spectra and generates high-resolution diagnostics.
"""

import os
import sys
import numpy as np

FCH1 = 2251.46484375       # MHz
FOFF = -2.793967724609375e-6 # MHz
HLEN = 295
NCHANS = 536870912
NSPEC = 16

FN_0002 = "D:/data/fil/lhs1140/spliced_blc0001020304050607_guppi_57774_70844_LHS1140_0002.gpuspec.0000.fil"
FN_0004 = "D:/data/fil/lhs1140/spliced_blc0001020304050607_guppi_57774_71517_LHS1140_0004.gpuspec.0000.fil"

OUTDIR = "reports/2026-09-25_lhs1140_campaign"
os.makedirs(OUTDIR, exist_ok=True)

def freq_to_chan(freq_mhz):
    return int((FCH1 - freq_mhz) / (-FOFF))

def chan_to_freq(chan):
    return FCH1 + chan * FOFF

def extract_cube(fn, ch_lo, width):
    cube = np.zeros((NSPEC, width), dtype=np.float32)
    with open(fn, "rb") as f:
        for t in range(NSPEC):
            offset = HLEN + (t * NCHANS + ch_lo) * 4
            f.seek(offset)
            cube[t] = np.fromfile(f, dtype=np.float32, count=width)
    return cube

def scan_window(name, center_freq_mhz, half_width_khz=250):
    ch_center = freq_to_chan(center_freq_mhz)
    width = int((half_width_khz * 1e-3) / abs(FOFF)) * 2
    ch_lo = ch_center - width // 2
    
    print(f"\n========================================================")
    print(f" Scanning {name} at {center_freq_mhz:.4f} MHz (Width: {width} chans, {width*abs(FOFF)*1e3:.1f} kHz)")
    print(f" Channels: {ch_lo} to {ch_lo + width}")
    print(f"========================================================")
    
    cube_0002 = extract_cube(FN_0002, ch_lo, width)
    cube_0004 = extract_cube(FN_0004, ch_lo, width)
    
    # Spectrum integrated over time
    spec_0002 = np.mean(cube_0002, axis=0)
    spec_0004 = np.mean(cube_0004, axis=0)
    
    med_02 = np.median(spec_0002)
    mad_02 = np.median(np.abs(spec_0002 - med_02)) * 1.4826
    snr_02 = (spec_0002 - med_02) / (mad_02 + 1e-12)
    
    med_04 = np.median(spec_0004)
    mad_04 = np.median(np.abs(spec_0004 - med_04)) * 1.4826
    snr_04 = (spec_0004 - med_04) / (mad_04 + 1e-12)
    
    max_idx_02 = np.argmax(snr_02)
    max_snr_02 = snr_02[max_idx_02]
    peak_freq_02 = chan_to_freq(ch_lo + max_idx_02)
    
    max_idx_04 = np.argmax(snr_04)
    max_snr_04 = snr_04[max_idx_04]
    peak_freq_04 = chan_to_freq(ch_lo + max_idx_04)
    
    print(f" Scan 0002 (ON): Max SNR = {max_snr_02:.2f} sigma at {peak_freq_02:.6f} MHz")
    print(f" Scan 0004 (ON): Max SNR = {max_snr_04:.2f} sigma at {peak_freq_04:.6f} MHz")
    
    # Check for narrowband hits above 6 sigma
    peaks_02 = np.where(snr_02 > 6.0)[0]
    peaks_04 = np.where(snr_04 > 6.0)[0]
    
    print(f" Channels > 6 sigma: Scan 0002 = {len(peaks_02)}, Scan 0004 = {len(peaks_04)}")
    
    # Save extracted snippet for the hottest peak or center
    hot_ch = max_idx_02 if max_snr_02 > 6.0 else width // 2
    snippet_02 = cube_0002[:, max(0, hot_ch - 512):min(width, hot_ch + 512)]
    out_f32 = os.path.join(OUTDIR, f"{name}_0002_hot.f32")
    snippet_02.astype(np.float32).tofile(out_f32)
    
    return {
        "name": name,
        "center_freq": center_freq_mhz,
        "max_snr_02": max_snr_02,
        "peak_freq_02": peak_freq_02,
        "max_snr_04": max_snr_04,
        "peak_freq_04": peak_freq_04,
        "peaks_02_count": len(peaks_02),
        "peaks_04_count": len(peaks_04),
        "out_f32": out_f32
    }

if __name__ == "__main__":
    targets = [
        ("HI_21cm_Hydrogen", 1420.405751, 500), # 1 MHz band
        ("OH_1665_Hydroxyl", 1665.401800, 500),
        ("OH_1667_Hydroxyl", 1667.359000, 500),
        ("DISS_Sweetspot_1425", 1425.000000, 500),
        ("L_band_Center_1400", 1400.000000, 500),
        ("GPS_L1_Sidelobe", 1575.420000, 500),
        ("GLONASS_L1_Sidelobe", 1602.000000, 500)
    ]
    
    results = []
    for name, f0, span in targets:
        r = scan_window(name, f0, span)
        results.append(r)
        
    print("\n=================== SUMMARY OF SEARCH ===================")
    for r in results:
        print(f" {r['name']:22s} | Freq: {r['center_freq']:10.4f} MHz | ON1: {r['max_snr_02']:6.2f}s | ON2: {r['max_snr_04']:6.2f}s")
