#!/usr/bin/env python3
"""hd139139_clean_search.py — Non-harmonic candidate screening for HD 139139."""

import h5py
import hdf5plugin
import numpy as np

fp = "D:/data/hd139139/blc00_guppi_58666_04874_HD139139_0040.gpuspec.0000.h5"

with h5py.File(fp, "r") as h:
    d = h["data"]
    fch1 = float(d.attrs["fch1"])
    foff = float(d.attrs["foff"])
    nchans = d.shape[2]

    # Search for all peaks > 15 sigma across 67M channels
    chunk_size = 4194304  # 4M channels per chunk
    non_harmonic_hits = []

    for c_start in range(0, nchans, chunk_size):
        c_end = min(nchans, c_start + chunk_size)
        sub = d[:, 0, c_start:c_end]
        mean_spec = np.mean(sub, axis=0)

        med = float(np.median(mean_spec))
        mad = float(np.median(np.abs(mean_spec - med)))
        sig = 1.4826 * mad if mad > 0 else 1.0
        z = (mean_spec - med) / sig

        high_idx = np.where(z > 15.0)[0]
        for idx in high_idx:
            gchan = c_start + idx
            freq_mhz = fch1 + gchan * foff
            
            # Check distance to nearest 2.9296875 MHz harmonic from 14748.535 MHz
            pfb_harm = 2.9296875
            dist_to_pfb = abs((freq_mhz - 14750.0) % pfb_harm)
            if dist_to_pfb > pfb_harm / 2:
                dist_to_pfb = pfb_harm - dist_to_pfb

            # Check distance to DC center (14750.0 MHz)
            dist_to_dc = abs(freq_mhz - 14750.0)

            # Filter out DC +/- 500 kHz and PFB boundaries (+/- 10 kHz)
            if dist_to_dc > 0.6 and dist_to_pfb > 0.010:
                non_harmonic_hits.append((float(z[idx]), int(gchan), float(freq_mhz), float(dist_to_pfb)))

print(f"Total non-harmonic peaks (>15 sigma, away from LO & PFB boundaries): {len(non_harmonic_hits)}")
non_harmonic_hits.sort(key=lambda x: -x[0])

if len(non_harmonic_hits) > 0:
    print("\nTop Non-Harmonic Spectral Peaks:")
    print("  Rank  Global Chan       Freq (MHz)   SNR (sigma)   Dist to PFB (MHz)")
    print("  ------------------------------------------------------------------")
    for r, (z, gchan, freq, dist_pfb) in enumerate(non_harmonic_hits[:20], 1):
        print(f"  {r:4d}  {gchan:11d}  {freq:15.6f}  {z:11.1f}   {dist_pfb:15.4f}")
else:
    print("\nALL channels outside local oscillator DC and PFB picket-fence harmonics are CLEAN.")
