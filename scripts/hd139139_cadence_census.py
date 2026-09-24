#!/usr/bin/env python3
"""hd139139_cadence_census.py — Full 65,536-channel ON/OFF cadence census for HD 139139."""

import h5py
import hdf5plugin
import numpy as np
import os
import sys

DATA_DIR = "D:/data/hd139139"
NODES = ["blc30", "blc20", "blc10", "blc00"]

print("================================================================================")
print(" HD 139139 ('The Random Transiter') — Full 65,536-Channel Ku-Band Cadence Census")
print(" Observations: AGBT19A_999_61 | Receiver: GBT Ku-Band (11.45 - 14.94 GHz)")
print(" Cadence: 3 ON Pointings (0040, 0042, 0044) vs 3 OFF Pointings (0039, 0041, 0043)")
print("================================================================================")

results = {}

for node in NODES:
    on_files = [
        f"{node}_guppi_58666_04874_HD139139_0040.gpuspec.0002.h5",
        f"{node}_guppi_58666_05511_HD139139_0042.gpuspec.0002.h5",
        f"{node}_guppi_58666_06151_HD139139_0044.gpuspec.0002.h5",
    ]
    off_files = [
        f"{node}_guppi_58666_04555_HD139139_0039.gpuspec.0002.h5",
        f"{node}_guppi_58666_05193_HD139139_0041.gpuspec.0002.h5",
        f"{node}_guppi_58666_05831_HD139139_0043.gpuspec.0002.h5",
    ]

    # Load 2D spectrograms and average across time for each scan
    on_specs = []
    for fn in on_files:
        fp = os.path.join(DATA_DIR, fn)
        with h5py.File(fp, "r") as h:
            d = h["data"][:, 0, :]  # shape: (279, 65536)
            on_specs.append(np.mean(d, axis=0))

    off_specs = []
    for fn in off_files:
        fp = os.path.join(DATA_DIR, fn)
        with h5py.File(fp, "r") as h:
            d = h["data"][:, 0, :]
            off_specs.append(np.mean(d, axis=0))

    on_mean = np.mean(on_specs, axis=0)
    off_mean = np.mean(off_specs, axis=0)

    fp0 = os.path.join(DATA_DIR, on_files[0])
    with h5py.File(fp0, "r") as h:
        fch1 = float(h["data"].attrs["fch1"])
        foff = float(h["data"].attrs["foff"])

    nchans = len(on_mean)
    freqs = fch1 + np.arange(nchans) * foff

    # 1. Differential Analysis (ON - OFF)
    diff = on_mean - off_mean
    med_diff = float(np.median(diff))
    mad_diff = float(np.median(np.abs(diff - med_diff)))
    sigma_diff = 1.4826 * mad_diff if mad_diff > 0 else 1.0
    z_diff = (diff - med_diff) / sigma_diff

    # 2. Raw Peak Analysis (ON peaks relative to local ON noise)
    on_med = float(np.median(on_mean))
    on_mad = float(np.median(np.abs(on_mean - on_med)))
    on_sigma = 1.4826 * on_mad if on_mad > 0 else 1.0
    z_on = (on_mean - on_med) / on_sigma

    off_med = float(np.median(off_mean))
    off_mad = float(np.median(np.abs(off_mean - off_med)))
    off_sigma = 1.4826 * off_mad if off_mad > 0 else 1.0
    z_off = (off_mean - off_med) / off_sigma

    # Find candidates with strong ON excess (z_diff > 6.0)
    hits_diff = np.where(z_diff > 6.0)[0]

    # Find narrow peaks with high raw ON power (z_on > 10.0)
    hits_raw = np.where(z_on > 10.0)[0]

    print(f"\n--------------------------------------------------------------------------------")
    print(f" NODE {node.upper()}: {freqs[0]:.2f} - {freqs[-1]:.2f} MHz (BW = {abs(freqs[-1]-freqs[0]):.1f} MHz)")
    print(f" Noise Floors: ON sigma={on_sigma:.2e}, OFF sigma={off_sigma:.2e}, Diff sigma={sigma_diff:.2e}")
    print(f" Peaks: {len(hits_raw)} raw ON peaks (>10 sigma), {len(hits_diff)} ON-excess channels (>6 sigma)")

    node_candidates = []

    # Check the top ON peaks
    all_hit_indices = np.unique(np.concatenate([hits_diff, hits_raw]))
    if len(all_hit_indices) > 0:
        # Sort by raw ON power descending
        ranked = all_hit_indices[np.argsort(-on_mean[all_hit_indices])]
        print(f" Top Significant Channels:")
        print(f" {'Chan':>6s} {'Freq (MHz)':>12s} {'ON z':>8s} {'OFF z':>8s} {'Diff z':>8s} {'ON/OFF Ratio':>12s} {'Verdict':>16s}")
        for idx in ranked[:15]:
            f_mhz = freqs[idx]
            zo = z_on[idx]
            zf = z_off[idx]
            zd = z_diff[idx]
            ratio = on_mean[idx] / max(1e-12, off_mean[idx])
            
            # Classification
            if zf > 5.0 and ratio < 2.0:
                verdict = "COMMON_RFI/CLOCK"
            elif ratio > 3.0 and zd > 6.0:
                verdict = "ON_CANDIDATE"
            elif zo > 20.0 and zf > 20.0:
                verdict = "SATURATED_RFI"
            else:
                verdict = "DRIFT_OR_FADE"
                
            print(f" {idx:6d} {f_mhz:12.4f} {zo:8.1f} {zf:8.1f} {zd:8.1f} {ratio:12.2f}x {verdict:>16s}")
            node_candidates.append({
                "chan": int(idx),
                "freq_mhz": float(f_mhz),
                "z_on": float(zo),
                "z_off": float(zf),
                "z_diff": float(zd),
                "ratio": float(ratio),
                "verdict": verdict
            })

    results[node] = {
        "freq_range": [float(freqs[0]), float(freqs[-1])],
        "candidates": node_candidates
    }

print("\n================================================================================")
print(" CENSUS COMPLETE ACROSS ALL 262,144 CHANNELS (4 NODES x 65,536 CHANNELS)")
print("================================================================================")
