#!/usr/bin/env python3
"""hd139139_fine_spectral_sweep.py — Full 67.1-million-channel fine-spectral sweep of HD 139139."""

import h5py
import hdf5plugin
import numpy as np
import time

fp = "D:/data/hd139139/blc00_guppi_58666_04874_HD139139_0040.gpuspec.0000.h5"
print("Scanning 67,108,864 fine-spectral channels for high SNR peaks...")

chunk_size = 2097152  # 2M channels per chunk (32 chunks total)
top_peaks = []

with h5py.File(fp, "r") as h:
    d = h["data"]
    nchans = d.shape[2]
    fch1 = float(d.attrs["fch1"])
    foff = float(d.attrs["foff"])

    t0 = time.time()
    for chunk_idx in range(nchans // chunk_size):
        c_start = chunk_idx * chunk_size
        c_end = c_start + chunk_size
        sub = d[:, 0, c_start:c_end]  # (16, chunk_size)
        mean_spec = np.mean(sub, axis=0)  # time-integrated spectrum

        # Estimate background
        med = float(np.median(mean_spec))
        mad = float(np.median(np.abs(mean_spec - med)))
        sig = 1.4826 * mad if mad > 0 else 1.0
        z = (mean_spec - med) / sig

        # Find peaks > 10 sigma
        high_idx = np.where(z > 10.0)[0]
        for idx in high_idx:
            global_chan = c_start + idx
            freq_mhz = fch1 + global_chan * foff
            top_peaks.append((float(z[idx]), int(global_chan), float(freq_mhz)))

t_dur = time.time() - t0
print(f"Full 67M-channel pass completed in {t_dur:.1f}s!")
print(f"Total peaks > 10 sigma found: {len(top_peaks)}")

top_peaks.sort(key=lambda x: -x[0])
print("\nTop 25 Narrowband Peaks in HD 139139 (blc00, 14.75 - 14.94 GHz):")
print("  Rank  Global Chan       Freq (MHz)   SNR (sigma)")
print("  ------------------------------------------------")
for rank, (z, gchan, freq) in enumerate(top_peaks[:25], 1):
    print(f"  {rank:4d}  {gchan:11d}  {freq:15.6f}  {z:11.1f}")
