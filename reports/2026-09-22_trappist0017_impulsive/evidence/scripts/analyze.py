#!/usr/bin/env python3
"""analyze.py — TRAPPIST-1 0017 impulsive-structure evidence generator.

Reads the .f32 slices produced by slice.exe (chan/pol extraction) and writes
one TSV row per slice with every quantity cited in REPORT.md, plus a
per-block persistence table and a value histogram per slice.

Usage:  python3 analyze.py <slices_dir> <out_dir>
Reproduce: re-run slice.exe per REPORT.md's slice commands, then this script.
"""
import sys, os, glob, json
import numpy as np

FS = 2929687.5          # GUPPI coarse-channel sample rate (Hz)
NEAR = 2000             # burst-grouping gap threshold (samples)
TAIL_NULL = 6.33e-5     # Gaussian P(|z|>4), the C/xeno_scan normaliser

def load(fp):
    return np.fromfile(fp, dtype=np.float32)

def stats(x):
    m = float(x.mean()); s = float(x.std())
    z = (x - m) / s if s > 0 else np.zeros_like(x)
    kurt = float((z**4).mean() - 3.0)
    tail = float((np.abs(z) > 4).mean() / TAIL_NULL)
    spikes = np.where(np.abs(z) > 10.0)[0]
    return m, s, kurt, tail, z, spikes

def bursts(spikes):
    if len(spikes) < 2:
        return np.array([])
    grp = np.split(spikes, np.where(np.diff(spikes) > NEAR)[0] + 1)
    return np.array([g.mean() for g in grp]), [len(g) for g in grp]

def phase_test(idx):
    c = np.bincount(idx % 8, minlength=8)
    e = len(idx) / 8.0
    return float(((c - e)**2 / e).sum())

def burst_fft(centers, n):
    if len(centers) < 16:
        return []
    sig = np.zeros(n, dtype=np.float32)
    sig[centers.astype(np.int64)] = 1.0
    seg = sig[:1 << 22]
    F = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1 / FS)
    lo, hi = 1, int(5000 / fr[1])
    band = F[lo:hi]
    top = np.argsort(band)[::-1][:5]
    return [(round(float(fr[lo + i]), 3), int(band[i])) for i in top]

def per_block(z, nblk=128):
    per = len(z) // nblk
    mx = [float(np.abs(z[b*per:(b+1)*per]).max()) for b in range(nblk)]
    return mx

def main():
    sd = sys.argv[1]; od = sys.argv[2]
    os.makedirs(od, exist_ok=True)
    rows = ["file\tchan\tn\tdistinct\tsd\tkurt\ttail_x_null\tspikes_gt10\tspike_rate_hz\tbursts\tburst_rate_hz\tspikes_per_burst\tphase_mod8_chi2\tburst_top_periods_hz"]
    persist = ["file\tchan\tblocks\tblocks_maxz_gt20\tmaxz_min\tmaxz_med\tmaxz_max"]
    hist = ["file\tchan\tvalue\tpct"]
    for fp in sorted(glob.glob(os.path.join(sd, "*.f32"))):
        base = os.path.basename(fp)[:-4]
        # name is  <tag>_ch<chan>
        tag, ch = base.rsplit("_ch", 1)
        x = load(fp)
        m, s, kurt, tail, z, sp = stats(x)
        d = len(np.unique(x))
        ct, sizes = bursts(sp) if len(sp) else (np.array([]), [])
        br = len(ct) / (len(x) / FS) if len(ct) else 0.0
        ph = phase_test(sp) if len(sp) else 0.0
        bf = burst_fft(ct, len(x)) if len(ct) else []
        rows.append("%s\t%s\t%d\t%d\t%.3f\t%.2f\t%.2f\t%d\t%.1f\t%d\t%.1f\t%.2f\t%.2f\t%s" % (
            tag, ch, len(x), d, s, kurt, tail, len(sp), len(sp)/(len(x)/FS),
            len(ct), br, (np.mean(sizes) if sizes else 0.0), ph,
            str(bf).replace("\t", " ")))
        mx = per_block(z)
        persist.append("%s\t%s\t%d\t%d\t%.1f\t%.1f\t%.1f" % (
            tag, ch, len(mx), int(sum(1 for v in mx if v > 20)), min(mx), float(np.median(mx)), max(mx)))
        v, c = np.unique(x, return_counts=True)
        for i in np.argsort(c)[::-1][:8]:
            hist.append("%s\t%s\t%d\t%.3f" % (tag, ch, int(v[i]), 100.0*c[i]/len(x)))
        del x, z
    open(os.path.join(od, "measurements.tsv"), "w").write("\n".join(rows) + "\n")
    open(os.path.join(od, "persistence_per_block.tsv"), "w").write("\n".join(persist) + "\n")
    open(os.path.join(od, "value_histograms.tsv"), "w").write("\n".join(hist) + "\n")
    print("wrote measurements.tsv (%d slices), persistence_per_block.tsv, value_histograms.tsv" % (len(rows)-1))

if __name__ == "__main__":
    main()
