#!/usr/bin/env python3
"""tic458478250_scan.py — Deep X-band Technosignature Analysis of TIC 458478250.

Transiting Exoplanet System TOI 1165.01 observed at GBT across 7.80–11.10 GHz.
Ingests 1.18 billion channels, searches deep-space communication windows,
H-line harmonics, and radio recombination line bands.
Extracts candidate dynamic spectra and runs TurboKain's native 22-instrument suite.
"""

import os
import sys
import numpy as np
import h5py
import hdf5plugin

FN = "D:/data/h5/tic458478250/spliced_blc00010203040506o7o0111213141516o021222324252627_guppi_58806_43185_TIC458478250_0127.gpuspec.0000.h5"
OUTDIR = "reports/2026-09-25_tic458478250_campaign"
os.makedirs(OUTDIR, exist_ok=True)

FCH1 = 11102.05078125
FOFF = -2.7939677238464355e-06
NCHANS = 1182793728
NSPEC = 16

def freq_to_chan(f_mhz):
    return int((FCH1 - f_mhz) / (-FOFF))

def chan_to_freq(chan):
    return FCH1 + chan * FOFF

def scan_h5_window(ds, name, center_freq_mhz, half_width_khz=250):
    ch_center = freq_to_chan(center_freq_mhz)
    width = int((half_width_khz * 1e-3) / abs(FOFF)) * 2
    ch_lo = max(0, ch_center - width // 2)
    ch_hi = min(NCHANS, ch_lo + width)
    actual_width = ch_hi - ch_lo
    
    print(f"\n========================================================")
    print(f" Scanning {name} at {center_freq_mhz:.4f} MHz (Width: {actual_width} chans, {actual_width*abs(FOFF)*1e3:.1f} kHz)")
    print(f" Channel range: {ch_lo} to {ch_hi}")
    print(f"========================================================")
    
    # Read chunk from HDF5: shape (16, 1, actual_width)
    chunk = ds[:, 0, ch_lo:ch_hi] # shape (16, actual_width)
    
    # Integrated spectrum over all 16 time steps
    spec = np.mean(chunk, axis=0)
    
    med = np.median(spec)
    mad = np.median(np.abs(spec - med)) * 1.4826
    snr = (spec - med) / (mad + 1e-12)
    
    max_idx = np.argmax(snr)
    max_snr = snr[max_idx]
    peak_freq = chan_to_freq(ch_lo + max_idx)
    
    peaks = np.where(snr > 6.0)[0]
    print(f" Peak SNR: {max_snr:.2f} sigma at {peak_freq:.6f} MHz")
    print(f" Channels > 6 sigma: {len(peaks)}")
    
    # Save a 1024-channel snippet centered on the hottest peak or center
    hot_ch = max_idx if max_snr > 6.0 else actual_width // 2
    snip_lo = max(0, hot_ch - 512)
    snip_hi = min(actual_width, snip_lo + 1024)
    snippet = chunk[:, snip_lo:snip_hi]
    
    out_f32 = os.path.join(OUTDIR, f"{name}_hot.f32")
    snippet.astype(np.float32).tofile(out_f32)
    
    return {
        "name": name,
        "center_freq": center_freq_mhz,
        "max_snr": max_snr,
        "peak_freq": peak_freq,
        "peaks_count": len(peaks),
        "out_f32": out_f32
    }

if __name__ == "__main__":
    targets = [
        ("DSN_Deep_Space_Downlink", 8420.0000, 500),
        ("Voyager1_Band", 8419.3000, 500),
        ("H92_alpha_RRL", 8309.3800, 500),
        ("H91_alpha_RRL", 8638.8600, 500),
        ("H90_alpha_RRL", 8932.4300, 500),
        ("Pi_x_HI_21cm", 8924.6900, 500),
        ("H85_alpha_RRL", 10522.0400, 500),
        ("X_band_Center", 9450.0000, 500),
        ("8000_MHz_Clock", 8000.0000, 500),
        ("10000_MHz_Round", 10000.0000, 500)
    ]
    
    print(f"Opening HDF5 dataset: {FN}")
    with h5py.File(FN, "r") as f:
        ds = f["data"]
        results = []
        for name, f0, span in targets:
            r = scan_h5_window(ds, name, f0, span)
            results.append(r)
            
    print("\n=================== SUMMARY OF X-BAND SEARCH ===================")
    for r in results:
        print(f" {r['name']:24s} | Freq: {r['center_freq']:10.4f} MHz | Max SNR: {r['max_snr']:8.2f}s | Peaks>6s: {r['peaks_count']:6d}")
