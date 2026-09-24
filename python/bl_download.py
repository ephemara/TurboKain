#!/usr/bin/env python3
"""bl_download.py — one-stop CLI for the Breakthrough Listen Open Data Archive.

No AWS credentials. No requester-pays. The archive exposes a public JSON API
and public HTTP mirrors; this wraps both so an agent (or human) never has to
rediscover the endpoints, the query parameters, or the aria2c speed trick.

    API:    https://seti.berkeley.edu/opendata/api/query-files
    hosts:  https://storage.googleapis.com/gbt_guppi/   (~65 MB/s, few targets)
            http://blpd0.ssl.berkeley.edu/...           (~4 MB/s/conn,
                                                         ~90 MB/s with aria2c -x16)

Commands
--------
    targets                     list every target in the archive (grep-able)
    query                       query files, print a table, do not download
    get                         query files and download them
    from-manifest               download every URL in a manifest (csv/txt)

Examples
--------
    # what's available
    python python/bl_download.py targets --grep SGR
    python python/bl_download.py targets --grep '^HIP' | head

    # inspect a target's raw voltage
    python python/bl_download.py query --target MESSIER031 \
        --file-types 'baseband data' --limit 8

    # pull nearby-star ON/OFF pairs, 4 files, into the D: tier
    python python/bl_download.py get --target HIP57328 \
        --file-types 'baseband data' --limit 4 \
        --outdir D:/data/raw --jobs 3 --conns 16

    # download a saved manifest (append-only record of what you pulled)
    python python/bl_download.py from-manifest D:/data/download_manifest.csv \
        --outdir D:/data/raw

    # everything at once: every HIP baseband file, size-capped
    python python/bl_download.py get --target HIP --file-types 'baseband data' \
        --max-gb 17 --limit 200 --manifest D:/data/hip_manifest.csv \
        --outdir D:/data/raw

Notes
-----
* `size` from the API is BYTES (the upstream docs mislabel it GB); this tool
  reports GB.
* The API caps `limit` at 10000 rows; for a wider sweep page with --time-start
  / --time-end or run several --target prefixes.
* Download speed lives and dies by aria2c. If aria2c is missing we fall back to
  a single-threaded urllib copy and say so loudly.
* Resume is on by default (aria2c --continue / HTTP Range).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = os.environ.get("BL_API", "https://seti.berkeley.edu/opendata/api")
GCS = "storage.googleapis.com/gbt_guppi"
UA = {"User-Agent": "SetiYeti-bl_download/1.0"}


# --------------------------------------------------------------------------
# API helpers
# --------------------------------------------------------------------------
def api_get(path: str, params: dict | None = None, timeout: int = 120):
    url = f"{API}/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def list_targets(grep: str | None = None):
    data = api_get("list-targets")
    targets = [t for t in data if t]
    if grep:
        rx = re.compile(grep, re.I)
        targets = [t for t in targets if rx.search(t)]
    return sorted(targets)


def query_files(**kw):
    """Return the list of file dicts. Unknown/None params are dropped."""
    params = {k: v for k, v in kw.items() if v not in (None, "", [])}
    out = api_get("query-files", params)
    if out.get("result") != "success":
        raise RuntimeError(f"API error: {out.get('result')} {out.get('message','')}")
    return out.get("data", [])


# --------------------------------------------------------------------------
# selection / display
# --------------------------------------------------------------------------
def host_of(url: str) -> str:
    if GCS in url:
        return "gcs"
    try:
        return urllib.parse.urlparse(url).netloc
    except Exception:
        return "?"


def gb(n: int) -> float:
    return n / 1e9


def select(rows, match=None, prefer="any", sort="url"):
    if match:
        rx = re.compile(match)
        rows = [r for r in rows if rx.search(r["url"].split("/")[-1])]
    if prefer == "gcs":
        rows = [r for r in rows if host_of(r["url"]) == "gcs"]
    elif prefer == "blpd":
        rows = [r for r in rows if host_of(r["url"]) != "gcs"]
    if sort == "url":
        rows = sorted(rows, key=lambda r: r["url"])
    elif sort == "size":
        rows = sorted(rows, key=lambda r: r["size"])
    elif sort == "time":
        rows = sorted(rows, key=lambda r: r.get("mjd") or 0)
    # de-dupe by filename, preferring a GCS URL if both exist
    seen, out = {}, []
    for r in rows:
        fn = r["url"].split("/")[-1]
        if fn not in seen or host_of(r["url"]) == "gcs":
            seen[fn] = r
    for r in rows:
        fn = r["url"].split("/")[-1]
        if seen[fn] is r:
            out.append(r)
    return out


def print_table(rows):
    if not rows:
        print("  (no files)")
        return
    tot = sum(r["size"] for r in rows)
    print(f"  {len(rows)} files, {gb(tot):.1f} GB total")
    print(f"  {'target':22s} {'type':13s} {'freq MHz':>10s} {'GB':>7s} {'host':22s} file")
    for r in rows:
        print(f"  {str(r['target'])[:22]:22s} {str(r.get('file_type',''))[:13]:13s} "
              f"{(r.get('center_freq') or 0):10.2f} {gb(r['size']):7.2f} "
              f"{host_of(r['url'])[:22]:22s} {r['url'].split('/')[-1][:56]}")


# --------------------------------------------------------------------------
# download
# --------------------------------------------------------------------------
def have_aria2() -> str | None:
    return shutil.which("aria2c")


def download(urls, outdir, jobs=3, conns=16, dry_run=False):
    os.makedirs(outdir, exist_ok=True)
    if dry_run:
        for u in urls:
            print(f"  [dry-run] {u}  ->  {os.path.join(outdir, u.split('/')[-1])}")
        return 0
    aria = have_aria2()
    if aria:
        lst = os.path.join(outdir, ".bl_download_urls.txt")
        with open(lst, "w", encoding="utf-8") as f:
            f.write("\n".join(urls) + "\n")
        cmd = [aria, "-i", lst, "-d", outdir, "-j", str(jobs), "-x", str(conns),
               "-s", str(conns), "-k", "1M", "--file-allocation=none",
               "--continue=true", "--console-log-level=warn",
               "--summary-interval=30", "--auto-file-renaming=false",
               "--allow-overwrite=false"]
        print(f"  aria2c: {jobs} files x {conns} conns -> {outdir}")
        try:
            return subprocess.call(cmd)
        finally:
            try:
                os.remove(lst)
            except OSError:
                pass
    # fallback: stdlib, single connection, resumable
    print("  !! aria2c not found on PATH — falling back to single-connection urllib.")
    print("     Expect ~4 MB/s instead of ~90 MB/s. Install aria2c for speed.")
    rc = 0
    for u in urls:
        dst = os.path.join(outdir, u.split("/")[-1])
        try:
            _urllib_fetch(u, dst)
        except Exception as e:  # noqa: BLE001
            rc = 1
            print(f"  FAIL {u}: {e}")
    return rc


def _urllib_fetch(url, dst):
    pos = os.path.getsize(dst) if os.path.exists(dst) else 0
    hdr = dict(UA)
    if pos:
        hdr["Range"] = f"bytes={pos}-"
    req = urllib.request.Request(url, headers=hdr)
    with urllib.request.urlopen(req, timeout=120) as r, open(dst, "ab" if pos else "wb") as f:
        if pos and r.status != 206:
            f.seek(0)
            f.truncate()
        total = int(r.headers.get("Content-Length", 0)) + (pos if r.status == 206 else 0)
        done = pos
        t0 = time.time()
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            done += len(chunk)
            if done % (64 << 20) < (1 << 20):
                rate = done / max(1e-9, time.time() - t0) / 1e6
                print(f"\r    {os.path.basename(dst)[:40]} {done/1e9:6.2f}/{total/1e9:.2f} GB "
                      f"{rate:5.1f} MB/s", end="", flush=True)
    print()


def write_manifest(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["target", "size_bytes", "url", "filename"])
        for r in rows:
            w.writerow([r["target"], r["size"], r["url"], r["url"].split("/")[-1]])
    print(f"  manifest -> {path} ({len(rows)} rows)")


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------
def cmd_targets(a):
    ts = list_targets(a.grep)
    for t in ts:
        print(t)
    print(f"# {len(ts)} targets", file=sys.stderr)


def _query_args(a):
    return dict(target=a.target, telescopes=a.telescope, **{"file-types": a.file_types},
                **{"freq-start": a.freq_start, "freq-end": a.freq_end,
                   "time-start": a.time_start, "time-end": a.time_end,
                   "pos-ra": a.pos_ra, "pos-dec": a.pos_dec, "pos-rad": a.pos_rad,
                   "minSize": a.min_gb, "maxSize": a.max_gb,
                   "limit": a.limit, "cadence": "true" if a.cadence else None})


def cmd_query(a):
    rows = select(query_files(**_query_args(a)), a.match, a.prefer, a.sort)
    if a.json:
        print(json.dumps(rows, indent=2))
    else:
        print_table(rows)


def cmd_get(a):
    rows = select(query_files(**_query_args(a)), a.match, a.prefer, a.sort)
    if a.limit and len(rows) > a.limit:
        rows = rows[: a.limit]
    print_table(rows)
    if not rows:
        return 1
    if a.manifest:
        write_manifest(rows, a.manifest)
    urls = [r["url"] for r in rows]
    return download(urls, a.outdir, a.jobs, a.conns, a.dry_run)


def cmd_from_manifest(a):
    urls = []
    with open(a.path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "," in line:  # csv manifest
                parts = next(csv.reader([line]))
                for p in parts:
                    if p.startswith("http"):
                        urls.append(p)
                        break
            elif line.startswith("http"):
                urls.append(line)
    if not urls:
        print("no URLs found in manifest", file=sys.stderr)
        return 1
    print(f"  {len(urls)} URLs from {a.path}")
    return download(urls, a.outdir, a.jobs, a.conns, a.dry_run)


# --------------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(
        prog="bl_download.py",
        description="Breakthrough Listen Open Data Archive downloader (no AWS needed).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Examples", 1)[-1])
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("targets", help="list archive targets")
    t.add_argument("--grep", help="regex filter on target name")
    t.set_defaults(fn=cmd_targets)

    def add_query(sp):
        sp.add_argument("--target", required=True,
                        help="substring match; 'HIP' returns all HIP targets")
        sp.add_argument("--file-types", default="baseband data",
                        help="comma-sep: 'baseband data',filterbank,HDF5,data")
        sp.add_argument("--telescope", help="GBT, Parkes, APF")
        sp.add_argument("--freq-start", type=float, help="MHz")
        sp.add_argument("--freq-end", type=float, help="MHz")
        sp.add_argument("--time-start", type=float, help="MJD")
        sp.add_argument("--time-end", type=float, help="MJD")
        sp.add_argument("--pos-ra", type=float, help="deg")
        sp.add_argument("--pos-dec", type=float, help="deg")
        sp.add_argument("--pos-rad", type=float, help="deg")
        sp.add_argument("--min-gb", type=float)
        sp.add_argument("--max-gb", type=float)
        sp.add_argument("--limit", type=int, default=50)
        sp.add_argument("--cadence", action="store_true",
                        help="collapse ABAB cadences into one entry")
        sp.add_argument("--match", help="regex filter on filename")
        sp.add_argument("--prefer", choices=["any", "gcs", "blpd"], default="any",
                        help="gcs = fast Google host; blpd = the big mirror")
        sp.add_argument("--sort", choices=["url", "size", "time"], default="url")
        sp.add_argument("--json", action="store_true")

    def add_dl(sp):
        sp.add_argument("--outdir", default=os.environ.get("SETIYETI_DATA", "data") + "/raw")
        sp.add_argument("--jobs", type=int, default=3, help="concurrent downloads")
        sp.add_argument("--conns", type=int, default=16, help="connections per file")
        sp.add_argument("--dry-run", action="store_true")

    q = sub.add_parser("query", help="query files, print a table, do not download")
    add_query(q); q.set_defaults(fn=cmd_query)

    g = sub.add_parser("get", help="query files and download them")
    add_query(g); add_dl(g)
    g.add_argument("--manifest", help="write a CSV manifest of what was selected")
    g.set_defaults(fn=cmd_get)

    m = sub.add_parser("from-manifest", help="download every URL in a manifest")
    m.add_argument("path")
    add_dl(m); m.set_defaults(fn=cmd_from_manifest)
    return p


def main():
    a = build_parser().parse_args()
    try:
        sys.exit(a.fn(a) or 0)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
