"""h5_reader — TurboKain Breakthrough Listen HDF5 filterbank ingest at slice parity.

Ingest container for Breakthrough Listen .h5 filterbank files (blimpy layout +
bitshuffle/gzip compression). Extracts per-channel, band-mean, or full-spectrum
streams as IEEE-754 32-bit float LE (.f32) time series for downstream TurboKain
detectors.

CLI contract mirrors fil_reader and slice:
  h5_reader <file.h5> [chan] [out.f32]
  h5_reader --in <file.h5> --chan N --out x.f32 [--pol P] [--out-md m.md] [--csv c.csv]
  h5_reader --in <file.h5> --chan-lo A --chan-hi B --mean --out light.f32
  h5_reader --in <file.h5> --spec T --out spec.f32
  h5_reader --prove
  no --out -> probe-only (header, geometry, sample rate, compression).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

# Ensure turbokain parent is on sys.path
_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))


def _load_h5():
    try:
        import h5py
    except ImportError:
        sys.stderr.write("h5_reader: error: h5py is required to read HDF5 files\n")
        sys.exit(2)
    try:
        import hdf5plugin  # registers bitshuffle filter
    except ImportError:
        pass  # non-bitshuffle HDF5 can still be read
    import numpy as np
    return h5py, np


def _format_1dp(val: float) -> str:
    """Format float to 1 decimal place matching TurboKain convention."""
    if math.isnan(val) or math.isinf(val):
        return "0.0"
    return f"{val:.1f}"


def _clean_attr(val: Any) -> Any:
    """Unpack numpy scalars, arrays, or bytes into standard python primitives."""
    if hasattr(val, "shape") and getattr(val, "ndim", 0) > 0:
        return [_clean_attr(x) for x in val]
    if hasattr(val, "item"):
        try:
            val = val.item()
        except ValueError:
            pass
    if isinstance(val, bytes):
        val = val.decode("utf-8", errors="replace")
    return val


def probe_h5(path: str | Path) -> dict[str, Any]:
    """Read metadata and determine dataset layout from a BL HDF5 filterbank file."""
    h5py, np = _load_h5()
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with h5py.File(path, "r") as f:
        # Locate main dataset
        if "data" in f:
            ds = f["data"]
        else:
            candidates = []
            def _find(name, obj):
                if isinstance(obj, h5py.Dataset) and obj.dtype.kind in "fiu":
                    candidates.append((obj.size, name))
            f.visititems(_find)
            if not candidates:
                raise ValueError(f"No numeric dataset found in {path}")
            candidates.sort(reverse=True)
            ds = f[candidates[0][1]]

        attrs = {}
        # Merge root attributes first, then dataset attributes (dataset wins)
        for k, v in f.attrs.items():
            attrs[k] = _clean_attr(v)
        for k, v in ds.attrs.items():
            attrs[k] = _clean_attr(v)

        raw_shape = ds.shape
        dtype = ds.dtype

        # Extract standard BL filterbank header fields
        fch1 = float(attrs.get("fch1", 0.0))
        foff = float(attrs.get("foff", 0.0))
        tsamp = float(attrs.get("tsamp", 0.0))
        tstart = float(attrs.get("tstart", 0.0))
        src_raj = float(attrs.get("src_raj", 0.0))
        src_dej = float(attrs.get("src_dej", 0.0))
        source_name = str(attrs.get("source_name", "UNKNOWN"))
        datatype = int(attrs.get("data_type", 1))
        nchans = int(attrs.get("nchans", 0))
        nbits = int(attrs.get("nbits", 0))
        nifs = int(attrs.get("nifs", 1))

        # Infer nbits from dtype if missing
        if nbits <= 0:
            if dtype.kind == "f":
                nbits = dtype.itemsize * 8
            elif dtype.kind in ("u", "i"):
                nbits = dtype.itemsize * 8
            else:
                nbits = 32

        # Verify axis layout against nchans (pitfall: gpuspec axes can be transposed)
        # Canonical layout: (time/nspec, feed/pol, frequency/nchans) or (time/nspec, freq)
        transpose_order = None
        if len(raw_shape) == 3:
            s0, s1, s2 = raw_shape
            if nchans > 0:
                if s2 == nchans:
                    # Canonical: (time, feed, freq)
                    nspec, nifs_dim, nc = s0, s1, s2
                elif s0 == nchans:
                    # Transposed: (freq, feed, time) -> transpose to (2, 1, 0)
                    transpose_order = (2, 1, 0)
                    nspec, nifs_dim, nc = s2, s1, s0
                elif s1 == nchans:
                    # Transposed: (feed, freq, time) or similar -> transpose
                    transpose_order = (2, 0, 1)
                    nspec, nifs_dim, nc = s2, s0, s1
                else:
                    # Default assumption: s2 is nchans
                    nspec, nifs_dim, nc = s0, s1, s2
            else:
                nspec, nifs_dim, nc = s0, s1, s2
                nchans = nc
            if nifs_dim > 0:
                nifs = nifs_dim
        elif len(raw_shape) == 2:
            s0, s1 = raw_shape
            if nchans > 0:
                if s1 == nchans:
                    nspec, nc = s0, s1
                elif s0 == nchans:
                    transpose_order = (1, 0)
                    nspec, nc = s1, s0
                else:
                    nspec, nc = s0, s1
            else:
                nspec, nc = s0, s1
                nchans = nc
            nifs = 1
        elif len(raw_shape) == 1:
            nspec = 1
            nchans = raw_shape[0]
            nifs = 1
        else:
            raise ValueError(f"Unexpected dataset dimensionality: {raw_shape}")

        if nchans <= 0:
            nchans = raw_shape[-1]

        fs_hz = (1.0 / tsamp) if tsamp > 0.0 else 1.0

        # Detect compression
        comp = ds.compression
        filters = ds._filters if hasattr(ds, "_filters") else {}
        if "32008" in filters or 32008 in filters or comp == "unknown":
            comp = "bitshuffle"
        elif comp is None:
            comp = "none"

        return {
            "path": str(path),
            "source_name": source_name,
            "nchans": nchans,
            "nspec": nspec,
            "nifs": nifs,
            "nbits": nbits,
            "dtype": str(dtype),
            "fch1_mhz": fch1,
            "foff_hz": foff * 1e6 if abs(foff) < 1.0 else foff,
            "foff_mhz": foff,
            "tsamp_s": tsamp,
            "tstart_mjd": tstart,
            "src_raj": src_raj,
            "src_dej": src_dej,
            "fs_hz": fs_hz,
            "datatype": datatype,
            "compression": str(comp),
            "raw_shape": list(raw_shape),
            "transpose_order": transpose_order,
            "chunks": list(ds.chunks) if ds.chunks else None,
        }


def extract_h5(
    path: str | Path,
    mode: str = "chan",
    chan: int = 0,
    pol: int = 0,
    chan_lo: int = -1,
    chan_hi: int = -1,
    spec: int = 0,
    out_path: str | Path | None = None,
) -> tuple[dict[str, Any], Any]:
    """Extract a time series or spectrum from BL HDF5 filterbank.

    mode: 'chan' (single channel vs time),
          'mean' (band-averaged channel lightcurve),
          'spec' (full spectrum at time index)
    """
    h5py, np = _load_h5()
    meta = probe_h5(path)
    nchans = meta["nchans"]
    nspec = meta["nspec"]
    nifs = meta["nifs"]
    t_order = meta["transpose_order"]

    if pol < 0 or pol >= nifs:
        pol = 0

    with h5py.File(path, "r") as f:
        ds = f["data"] if "data" in f else f[list(f.keys())[0]]

        if mode == "chan":
            if chan < 0 or chan >= nchans:
                raise ValueError(f"Channel {chan} out of range (0..{nchans - 1})")
            if len(meta["raw_shape"]) == 3:
                if t_order == (2, 1, 0):
                    data = ds[chan, pol, :].astype(np.float32)
                elif t_order == (2, 0, 1):
                    data = ds[pol, chan, :].astype(np.float32)
                else:
                    data = ds[:, pol, chan].astype(np.float32)
            elif len(meta["raw_shape"]) == 2:
                if t_order == (1, 0):
                    data = ds[chan, :].astype(np.float32)
                else:
                    data = ds[:, chan].astype(np.float32)
            else:
                data = ds[:].astype(np.float32)

        elif mode == "mean":
            if chan_lo < 0:
                chan_lo = 0
            if chan_hi < 0 or chan_hi >= nchans:
                chan_hi = nchans - 1
            if chan_lo > chan_hi:
                raise ValueError(f"chan-lo ({chan_lo}) > chan-hi ({chan_hi})")

            # Chunked read to keep memory usage low on huge datasets
            chunk_size = 4096
            out_blocks = []
            for t_start in range(0, nspec, chunk_size):
                t_end = min(t_start + chunk_size, nspec)
                if len(meta["raw_shape"]) == 3:
                    if t_order == (2, 1, 0):
                        blk = ds[chan_lo:chan_hi + 1, pol, t_start:t_end]
                        blk_mean = blk.mean(axis=0)
                    else:
                        blk = ds[t_start:t_end, pol, chan_lo:chan_hi + 1]
                        blk_mean = blk.mean(axis=-1)
                elif len(meta["raw_shape"]) == 2:
                    if t_order == (1, 0):
                        blk = ds[chan_lo:chan_hi + 1, t_start:t_end]
                        blk_mean = blk.mean(axis=0)
                    else:
                        blk = ds[t_start:t_end, chan_lo:chan_hi + 1]
                        blk_mean = blk.mean(axis=-1)
                else:
                    blk_mean = ds[chan_lo:chan_hi + 1].mean(axis=0, keepdims=True)
                out_blocks.append(blk_mean.astype(np.float32))
            data = np.concatenate(out_blocks)

        elif mode == "spec":
            if spec < 0 or spec >= nspec:
                raise ValueError(f"Spectrum index {spec} out of range (0..{nspec - 1})")
            if len(meta["raw_shape"]) == 3:
                if t_order == (2, 1, 0):
                    data = ds[:, pol, spec].astype(np.float32)
                else:
                    data = ds[spec, pol, :].astype(np.float32)
            elif len(meta["raw_shape"]) == 2:
                if t_order == (1, 0):
                    data = ds[:, spec].astype(np.float32)
                else:
                    data = ds[spec, :].astype(np.float32)
            else:
                data = ds[:].astype(np.float32)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    if out_path:
        out_p = Path(out_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        data.tofile(out_p)

    return meta, data


def prove() -> int:
    """Synthetic roundtrip prove test: write HDF5 -> probe -> extract -> verify."""
    h5py, np = _load_h5()
    cwd = Path.cwd()
    scratch_h5 = cwd / "_tmp_h5prove.h5"
    scratch_f32 = cwd / "_tmp_h5prove.f32"

    total = 0
    npass = 0

    try:
        # 1. Synthesize known test filterbank
        # 16 time steps x 1 pol x 32 channels ramp
        ns = 16
        nc = 32
        data = np.zeros((ns, 1, nc), dtype=np.float32)
        for t in range(ns):
            for c in range(nc):
                data[t, 0, c] = float(t * 100 + c)

        with h5py.File(scratch_h5, "w") as f:
            ds = f.create_dataset(
                "data",
                data=data,
                chunks=(4, 1, nc),
                compression="gzip",
                compression_opts=1,
            )
            ds.attrs["fch1"] = 1420.0
            ds.attrs["foff"] = -0.05
            ds.attrs["tsamp"] = 0.5  # fs = 2.0 Hz
            ds.attrs["tstart"] = 59000.0
            ds.attrs["nchans"] = nc
            ds.attrs["nbits"] = 32
            ds.attrs["nifs"] = 1
            ds.attrs["source_name"] = "PROVE_SYNTH"
            ds.attrs["data_type"] = 1

        # Test 1: Probe metadata
        total += 1
        meta = probe_h5(scratch_h5)
        if (
            meta["nchans"] == 32
            and meta["nspec"] == 16
            and abs(meta["fs_hz"] - 2.0) < 1e-4
            and meta["source_name"] == "PROVE_SYNTH"
        ):
            npass += 1
        else:
            sys.stderr.write(f"[prove] T1 failed: meta={meta}\n")

        # Test 2: Channel extraction
        total += 1
        _, chan7 = extract_h5(scratch_h5, mode="chan", chan=7, out_path=scratch_f32)
        expected_chan7 = np.array([t * 100 + 7 for t in range(ns)], dtype=np.float32)
        readback_f32 = np.fromfile(scratch_f32, dtype=np.float32)
        if np.allclose(chan7, expected_chan7) and np.allclose(readback_f32, expected_chan7):
            npass += 1
        else:
            sys.stderr.write("[prove] T2 channel extraction mismatch\n")

        # Test 3: Band-mean extraction
        total += 1
        _, mean_val = extract_h5(scratch_h5, mode="mean", chan_lo=0, chan_hi=31, out_path=scratch_f32)
        # mean across 0..31 is t*100 + 15.5
        expected_mean = np.array([t * 100 + 15.5 for t in range(ns)], dtype=np.float32)
        if np.allclose(mean_val, expected_mean):
            npass += 1
        else:
            sys.stderr.write("[prove] T3 band-mean extraction mismatch\n")

        # Test 4: Spectrum extraction
        total += 1
        _, spec3 = extract_h5(scratch_h5, mode="spec", spec=3, out_path=scratch_f32)
        expected_spec3 = np.array([300 + c for c in range(nc)], dtype=np.float32)
        if np.allclose(spec3, expected_spec3):
            npass += 1
        else:
            sys.stderr.write("[prove] T4 spectrum extraction mismatch\n")

    finally:
        if scratch_h5.exists():
            scratch_h5.unlink(missing_ok=True)
        if scratch_f32.exists():
            scratch_f32.unlink(missing_ok=True)

    print(f"[prove] {npass}/{total}")
    if npass == total:
        print("receipt=PASS prove=4/4")
        return 0
    else:
        print("receipt=FAIL prove=FAIL")
        return 1


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="TurboKain BL HDF5 filterbank ingest at slice parity",
        add_help=False,
    )
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--prove", action="store_true")
    parser.add_argument("--in", dest="in_path", type=str, default="")
    parser.add_argument("--out", dest="out_path", type=str, default="")
    parser.add_argument("--out-md", dest="out_md", type=str, default="")
    parser.add_argument("--csv", dest="csv_path", type=str, default="")
    parser.add_argument("--chan", type=int, default=-1)
    parser.add_argument("--pol", type=int, default=0)
    parser.add_argument("--chan-lo", type=int, default=-1)
    parser.add_argument("--chan-hi", type=int, default=-1)
    parser.add_argument("--mean", action="store_true")
    parser.add_argument("--spec", type=int, default=-1)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--data-dir", type=str, default="")
    parser.add_argument("positional", nargs="*")

    args = parser.parse_args(argv)

    if args.help:
        print(__doc__)
        return 1

    if args.prove:
        return prove()

    in_path = args.in_path
    want_chan = args.chan
    out_path = args.out_path

    # Positional shorthand: h5_reader <file> [chan] [out.f32]
    pos = args.positional
    if pos:
        if not in_path and len(pos) >= 1:
            in_path = pos[0]
        if len(pos) >= 2:
            if want_chan < 0 and pos[1].isdigit():
                want_chan = int(pos[1])
            elif not out_path:
                out_path = pos[1]
        if len(pos) >= 3 and not out_path:
            out_path = pos[2]

    if not in_path:
        sys.stderr.write("h5_reader: no input. usage: h5_reader --in <file.h5> [--out x.f32]\n")
        return 2

    # Probe metadata
    try:
        meta = probe_h5(in_path)
    except Exception as e:
        sys.stderr.write(f"h5_reader: open/probe fail: {e}\n")
        return 2

    nchans = meta["nchans"]
    nspec = meta["nspec"]
    src_name = meta["source_name"]
    nbits = meta["nbits"]
    tsamp = meta["tsamp_s"]
    fch1 = meta["fch1_mhz"]
    foff = meta["foff_mhz"]
    tstart = meta["tstart_mjd"]
    fs_hz = meta["fs_hz"]
    datatype = meta["datatype"]
    comp = meta["compression"]

    tsamp_us = int(tsamp * 1_000_000.0)
    fch1_x1e4 = int(fch1 * 10_000.0)
    foff_hz_x1e3 = int(foff * 1_000_000_000.0)
    tstart_x1e6 = int(tstart * 1_000_000.0)
    fs_s = _format_1dp(fs_hz)

    # Probe-only mode
    if not out_path and not args.out_md and not args.csv_path:
        print(f"h5_reader: {in_path}")
        print(
            f"  source={src_name} nchans={nchans} nbits={nbits} nspec={nspec} (exact)"
        )
        print(
            f"  fch1_mhz_x1e4={fch1_x1e4} foff_hz_x1e3={foff_hz_x1e3} tsamp_us={tsamp_us} tstart_x1e6={tstart_x1e6}"
        )
        print(f"  fs_hz={fs_s} datatype={datatype} compression={comp}")
        print("  verdict=PROBED receipt=PASS")
        return 0

    # Determine mode
    mode = "chan"
    ex_chan = want_chan
    ex_lo = args.chan_lo
    ex_hi = args.chan_hi

    if args.spec >= 0:
        mode = "spec"
    elif args.mean or args.chan_lo >= 0 or args.chan_hi >= 0:
        mode = "mean"
        if ex_lo < 0:
            ex_lo = 0
        if ex_hi < 0:
            ex_hi = nchans - 1

    if mode == "chan" and ex_chan < 0:
        ex_chan = nchans // 2

    try:
        meta, data = extract_h5(
            in_path,
            mode=mode,
            chan=ex_chan,
            pol=args.pol,
            chan_lo=ex_lo,
            chan_hi=ex_hi,
            spec=args.spec,
            out_path=out_path,
        )
    except Exception as e:
        sys.stderr.write(f"h5_reader: extraction error: {e}\n")
        return 2

    out_n = len(data)

    # Tables
    if mode == "chan":
        modeline = f"chan={ex_chan}"
    elif mode == "mean":
        modeline = f"band {ex_lo}-{ex_hi} mean"
    else:
        modeline = f"spec={args.spec}"

    md = "| file | source | nchans | nspec | mode | out_n | fs_hz | verdict |\n"
    md += "|---|---|---|---|---|---|---|---|\n"
    md += f"| {in_path} | {src_name} | {nchans} | {nspec} | {modeline} | {out_n} | {fs_s} | EXTRACTED-exact |\n"

    csv_line = (
        f"file,source,nchans,nspec,mode,out_n,fs_hz,tsamp_us,fch1_x1e4,foff_hz_x1e3,verdict\n"
        f"{in_path},{src_name},{nchans},{nspec},{modeline},{out_n},{fs_s},{tsamp_us},{fch1_x1e4},{foff_hz_x1e3},EXTRACTED-exact\n"
    )

    if args.out_md:
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"h5_reader: wrote {args.out_md}")

    if args.csv_path:
        Path(args.csv_path).parent.mkdir(parents=True, exist_ok=True)
        with open(args.csv_path, "w", encoding="utf-8") as f:
            f.write(csv_line)
        print(f"h5_reader: wrote {args.csv_path}")

    if args.json:
        payload = {
            "file": in_path,
            "source": src_name,
            "nchans": nchans,
            "nspec": nspec,
            "mode": modeline,
            "out_n": out_n,
            "fs_hz": fs_hz,
            "verdict": "EXTRACTED-exact",
        }
        print(json.dumps(payload))

    print(f"h5_reader: {out_path} n={out_n} fs_hz={fs_s} receipt=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
