"""reports.db — SQLite warehouse over reports/ + query/stats CLI backing.

Everything under ``reports/`` (21k+ CSVs, TSVs, verdict/manifest JSONs, plus a
file inventory of the PNG/MD/F32/BIN artifacts) lands in one queryable SQLite
database (default: ``<repo-root>/reports.db``). Incremental ingest is tracked
in the ``files`` ledger (relpath + mtime + size), so re-running ingest after a
new campaign only parses what changed.

Tables (one per tool contract; column names mirror the CSV headers, scaled-int
suffixes kept so units are never ambiguous — see VIEWS for real-unit helpers):

  scans       one row per report directory that held tabular data
  files       ingest ledger: every parsed file, its mtime/size/row count
  artifacts   inventory of non-tabular files (.png/.md/.f32/.bin/.log/...)
  sk          sk_gate output            (file,samples,nseg,skdev_x1e3,...)
  xeno        xeno_scan output          (...,maxz_x10,kurt_x100,...,verdict)
  fam         fam_god output            (tag,seg,rank,bin,alpha_hz_x100,...)
  pulse       boxcar_bank output        (dm,width,sigma_x100,t,verdict)
  drift       drift_hunt output         (freq_hz,drift_x100,sigma_x100,kind)
  frame       frame_hunt output         (rank,period_ms_x100,freq_hz_x100,...)
  fold        fold_sum output           (same shape as frame, other tool)
  lag         lag_hunt output           (rank,lag,...,kind,verdict)
  jerk        jerk_track output         (f0_hz,drift_hz_s,jerk_hz_s2,...)
  scint       scint_pol output          (class,m_med_x100,...,pol_verdict,...)
  evidence    unify evidence.csv        (tool,star,leg,chan,kind,...,verdict)
  stack       stack output              (freq_hz,shift_bins,sigma_x100,kind)
  packet      packet_hunt output        (file,...,ccsds_hits,barker_hits,...)
  raster      raster_hunt output        (p,q,sigma_x100,agree_x100,...,verdict)
  bits        bitslice output           (file,mode,stream,nbits,...,verdict)
  xvm         xvm_sandbox output        (file,nbits,...,score_x100,verdict)
  cadence     cadence_pair output       (on_file,off_file,kind,...,reason)
  ingest      slice/fil/h5 geometry rows(file,source,nchans,...,verdict)
  spectrum    bandpass spectrum rows   (bin_lo,freq_lo_mhz,mean,std,...)
  census      per-chan survey rows      (chan,freq_mhz,peak_over_base,xeno_fam)
  anomaly     ANOMALY_LEDGER.tsv rows
  stage_runs  summary.tsv rows          (chan,pol,tool,exit,seconds,...)
  lattice     verdicts.json ON/OFF lattice rows
  floors      verdicts.json sub-gate floors (scan_id,tool,best_subgate)
  documents   raw JSON docs (manifest/verdicts/campaign_digest/...)
  raw_csv     CSV rows with unknown headers (nothing is dropped)
  raw_tsv     TSV lines with freeform/log shape (nothing is dropped)

Every data row carries ``scan_id`` (FK -> scans) and ``source`` (repo-relative
CSV/TSV path) for provenance. stdlib only.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import time
from pathlib import Path

DB_NAME = "reports.db"
SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# schema
# ---------------------------------------------------------------------------

_SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY, value TEXT
);

CREATE TABLE IF NOT EXISTS scans (
  scan_id     INTEGER PRIMARY KEY,
  report_dir  TEXT UNIQUE,            -- repo-relative dir, e.g. reports/sweep
  campaign    TEXT,                   -- parent campaign dir name when nested
  target      TEXT,                   -- from manifest/verdicts when known
  disposition TEXT,                   -- from verdicts.json / manifest
  n_files     INTEGER DEFAULT 0,      -- tabular files parsed
  n_rows      INTEGER DEFAULT 0,      -- data rows stored
  n_artifacts INTEGER DEFAULT 0,      -- non-tabular files inventoried
  manifest_json TEXT,
  verdicts_json TEXT,
  ingested_at TEXT
);

CREATE TABLE IF NOT EXISTS files (
  file_id  INTEGER PRIMARY KEY,
  scan_id  INTEGER REFERENCES scans(scan_id),
  relpath  TEXT UNIQUE,               -- repo-relative file path
  kind     TEXT,                      -- table it landed in (or 'artifact')
  mtime    REAL,
  size     INTEGER,
  nrows    INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS artifacts (
  artifact_id INTEGER PRIMARY KEY,
  scan_id  INTEGER REFERENCES scans(scan_id),
  relpath  TEXT,
  kind     TEXT,                      -- png | md | f32 | bin | log | json | other
  size     INTEGER
);

CREATE TABLE IF NOT EXISTS sk (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  file TEXT, samples INTEGER, nseg INTEGER,
  skdev_x1e3 INTEGER, skfrac_x1e4 INTEGER, skflag INTEGER, verdict TEXT);
CREATE TABLE IF NOT EXISTS xeno (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  file TEXT, samples INTEGER, skdev_x1000 INTEGER, skfrac_x10000 INTEGER,
  skflag INTEGER, coh_x100 INTEGER, cohflag INTEGER, ladder_x100 INTEGER,
  ladderq INTEGER, dm_sign TEXT, dm_r2_x1000 INTEGER, impuls INTEGER,
  maxz_x10 INTEGER, kurt_x100 INTEGER, tailx_x100 INTEGER,
  lattice TEXT, verdict TEXT);
CREATE TABLE IF NOT EXISTS fam (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  tag TEXT, seg INTEGER, rank INTEGER, bin INTEGER,
  alpha_hz_x100 INTEGER, ratio_x100 INTEGER, log10p_x100 INTEGER, hit INTEGER);
CREATE TABLE IF NOT EXISTS pulse (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  dm REAL, width REAL, sigma_x100 INTEGER, t REAL, verdict TEXT);
CREATE TABLE IF NOT EXISTS drift (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  freq_hz REAL, drift_x100 REAL, sigma_x100 INTEGER, kind TEXT);
CREATE TABLE IF NOT EXISTS frame (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  rank INTEGER, period_ms_x100 REAL, freq_hz_x100 REAL,
  sigma_x100 INTEGER, detected INTEGER);
CREATE TABLE IF NOT EXISTS fold (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  rank INTEGER, period_ms_x100 REAL, freq_hz_x100 REAL,
  sigma_x100 INTEGER, detected INTEGER);
CREATE TABLE IF NOT EXISTS lag (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  rank INTEGER, lag INTEGER, period_ms_x100 REAL, freq_hz_x100 REAL,
  sigma_x100 INTEGER, persist_x100 INTEGER, fold_x100 INTEGER, fam_x100 INTEGER,
  kind TEXT, verdict TEXT);
CREATE TABLE IF NOT EXISTS jerk (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  f0_hz REAL, drift_hz_s REAL, jerk_hz_s2 REAL, score_x100 INTEGER,
  gain_db_x100 INTEGER, sidereal_anom INTEGER, verdict TEXT);
CREATE TABLE IF NOT EXISTS scint (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  class TEXT, m_med_x100 INTEGER, m_max_x100 INTEGER, tau_frames_x100 INTEGER,
  xcorr_x100 INTEGER, pol_verdict TEXT, dfreq_hz REAL, pol_env_corr_x100 INTEGER);
CREATE TABLE IF NOT EXISTS evidence (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  tool TEXT, star TEXT, leg TEXT, chan INTEGER, kind TEXT,
  freq_hz REAL, alpha_hz REAL, period_ms REAL, sigma REAL, verdict TEXT, src TEXT);
CREATE TABLE IF NOT EXISTS stack (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  freq_hz REAL, shift_bins INTEGER, sigma_x100 INTEGER, kind TEXT);
CREATE TABLE IF NOT EXISTS packet (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  file TEXT, samples INTEGER, baud REAL, sps REAL, bits INTEGER,
  ccsds_hits INTEGER, barker_hits INTEGER, frame_len INTEGER, verdict TEXT);
CREATE TABLE IF NOT EXISTS raster (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  p INTEGER, q INTEGER, sigma_x100 INTEGER, agree_x100 INTEGER,
  sync_k INTEGER, sync_score_x100 INTEGER, verdict TEXT);
CREATE TABLE IF NOT EXISTS bits (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  file TEXT, mode TEXT, stream TEXT, nbits INTEGER,
  ones_x1000 INTEGER, runs INTEGER, verdict TEXT);
CREATE TABLE IF NOT EXISTS xvm (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  file TEXT, nbits INTEGER, ones_x1000 INTEGER, distinct_count INTEGER,
  sub_x100 INTEGER, stk_ops INTEGER, stk_loops INTEGER, stk_depth INTEGER,
  stk_w INTEGER, ca_x1e6 INTEGER, acf_lag INTEGER, acf_z_x10 INTEGER,
  bm_L INTEGER, bm_z_x10 INTEGER, ras_w INTEGER, ras_h INTEGER, ras_z_x10 INTEGER,
  tag_steps INTEGER, tag_depth INTEGER, tag_fire INTEGER, jit_equiv INTEGER,
  mut_stk INTEGER, mut_bm_x10 INTEGER, score_x100 INTEGER, verdict TEXT);
CREATE TABLE IF NOT EXISTS cadence (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  on_file TEXT, off_file TEXT, kind TEXT, on_flag INTEGER, off_flag INTEGER,
  on_best REAL, off_best REAL, verdict TEXT, reason TEXT);
CREATE TABLE IF NOT EXISTS ingest (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  file TEXT, source_name TEXT, nchans INTEGER, nspec INTEGER, mode TEXT,
  out_n INTEGER, fs_hz REAL, tsamp_us REAL, fch1_x1e4 REAL, foff_hz_x1e3 REAL,
  verdict TEXT);
CREATE TABLE IF NOT EXISTS spectrum (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  bin_lo INTEGER, freq_lo_mhz REAL, mean REAL, std REAL, maxv REAL,
  median REAL, top3 TEXT);
CREATE TABLE IF NOT EXISTS census (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  chan INTEGER, freq_mhz REAL, peak_over_base REAL, xeno_fam TEXT);
CREATE TABLE IF NOT EXISTS anomaly (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  target TEXT, chan TEXT, freq_mhz REAL, cadence TEXT,
  stokes_v TEXT, disposition TEXT, waterfall TEXT);
CREATE TABLE IF NOT EXISTS stage_runs (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  chan TEXT, pol TEXT, tool TEXT, exit INTEGER, seconds REAL,
  receipt TEXT, verdicts TEXT, outputs TEXT, log TEXT);
CREATE TABLE IF NOT EXISTS lattice (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  star TEXT, leg TEXT, chan INTEGER, sk TEXT, xeno TEXT, fam TEXT,
  fold TEXT, boxcar TEXT, frame TEXT, drift TEXT, lag TEXT, jerk TEXT,
  scint TEXT);
CREATE TABLE IF NOT EXISTS floors (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  tool TEXT, best_subgate INTEGER);
CREATE TABLE IF NOT EXISTS documents (
  doc_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  kind TEXT,                        -- manifest | verdicts | campaign_digest | other
  doc_json TEXT);
CREATE TABLE IF NOT EXISTS raw_csv (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  header TEXT, line_no INTEGER, line_json TEXT);
CREATE TABLE IF NOT EXISTS raw_tsv (
  row_id INTEGER PRIMARY KEY, scan_id INTEGER, source TEXT,
  line_no INTEGER, line TEXT);
"""

_VIEWS = """
CREATE VIEW IF NOT EXISTS v_fam_hits AS
  SELECT s.report_dir AS scan, f.source, f.tag, f.seg, f.rank, f.bin,
         f.alpha_hz_x100 / 100.0 AS alpha_hz,
         f.ratio_x100 / 100.0 AS ratio, f.log10p_x100 / 100.0 AS log10p, f.hit
  FROM fam f JOIN scans s ON s.scan_id = f.scan_id WHERE f.hit = 1;

CREATE VIEW IF NOT EXISTS v_evidence_hits AS
  SELECT s.report_dir AS scan, e.*
  FROM evidence e JOIN scans s ON s.scan_id = e.scan_id
  WHERE e.verdict IS NOT NULL AND e.verdict NOT IN ('CLEAN','-','');

CREATE VIEW IF NOT EXISTS v_pulse_top AS
  SELECT s.report_dir AS scan, p.source, p.dm, p.width,
         p.sigma_x100 / 100.0 AS sigma, p.t, p.verdict
  FROM pulse p JOIN scans s ON s.scan_id = p.scan_id;

CREATE VIEW IF NOT EXISTS v_frame_top AS
  SELECT s.report_dir AS scan, f.source, f.rank,
         f.period_ms_x100 / 100.0 AS period_ms,
         f.freq_hz_x100 / 100.0 AS freq_hz,
         f.sigma_x100 / 100.0 AS sigma, f.detected
  FROM frame f JOIN scans s ON s.scan_id = f.scan_id;

CREATE VIEW IF NOT EXISTS v_scan_stats AS
  SELECT s.report_dir AS scan, s.target, s.disposition, s.n_files, s.n_rows,
         (SELECT COUNT(*) FROM evidence e
           WHERE e.scan_id = s.scan_id AND e.verdict NOT IN ('CLEAN','-','')) AS n_hits,
         (SELECT COUNT(*) FROM fam f WHERE f.scan_id = s.scan_id AND f.hit = 1) AS n_fam_hits,
         (SELECT MAX(sigma_x100) FROM pulse p WHERE p.scan_id = s.scan_id) AS pulse_max_x100,
         (SELECT MAX(sigma_x100) FROM frame f WHERE f.scan_id = s.scan_id) AS frame_max_x100,
         (SELECT MAX(sigma_x100) FROM fold f WHERE f.scan_id = s.scan_id) AS fold_max_x100
  FROM scans s;

CREATE VIEW IF NOT EXISTS v_tool_coverage AS
  SELECT 'sk' AS tool, COUNT(*) AS rows_, COUNT(DISTINCT source) AS files FROM sk UNION ALL
  SELECT 'xeno', COUNT(*), COUNT(DISTINCT source) FROM xeno UNION ALL
  SELECT 'fam', COUNT(*), COUNT(DISTINCT source) FROM fam UNION ALL
  SELECT 'pulse', COUNT(*), COUNT(DISTINCT source) FROM pulse UNION ALL
  SELECT 'drift', COUNT(*), COUNT(DISTINCT source) FROM drift UNION ALL
  SELECT 'frame', COUNT(*), COUNT(DISTINCT source) FROM frame UNION ALL
  SELECT 'fold', COUNT(*), COUNT(DISTINCT source) FROM fold UNION ALL
  SELECT 'lag', COUNT(*), COUNT(DISTINCT source) FROM lag UNION ALL
  SELECT 'jerk', COUNT(*), COUNT(DISTINCT source) FROM jerk UNION ALL
  SELECT 'scint', COUNT(*), COUNT(DISTINCT source) FROM scint UNION ALL
  SELECT 'evidence', COUNT(*), COUNT(DISTINCT source) FROM evidence UNION ALL
  SELECT 'stack', COUNT(*), COUNT(DISTINCT source) FROM stack UNION ALL
  SELECT 'packet', COUNT(*), COUNT(DISTINCT source) FROM packet UNION ALL
  SELECT 'raster', COUNT(*), COUNT(DISTINCT source) FROM raster UNION ALL
  SELECT 'bits', COUNT(*), COUNT(DISTINCT source) FROM bits UNION ALL
  SELECT 'xvm', COUNT(*), COUNT(DISTINCT source) FROM xvm UNION ALL
  SELECT 'cadence', COUNT(*), COUNT(DISTINCT source) FROM cadence UNION ALL
  SELECT 'census', COUNT(*), COUNT(DISTINCT source) FROM census UNION ALL
  SELECT 'anomaly', COUNT(*), COUNT(DISTINCT source) FROM anomaly UNION ALL
  SELECT 'stage_runs', COUNT(*), COUNT(DISTINCT source) FROM stage_runs UNION ALL
  SELECT 'lattice', COUNT(*), COUNT(DISTINCT source) FROM lattice;
"""

_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_evidence_verdict ON evidence(verdict);
CREATE INDEX IF NOT EXISTS idx_evidence_sigma ON evidence(sigma);
CREATE INDEX IF NOT EXISTS idx_evidence_scan ON evidence(scan_id);
CREATE INDEX IF NOT EXISTS idx_fam_hit ON fam(hit);
CREATE INDEX IF NOT EXISTS idx_fam_alpha ON fam(alpha_hz_x100);
CREATE INDEX IF NOT EXISTS idx_fam_scan ON fam(scan_id);
CREATE INDEX IF NOT EXISTS idx_pulse_sigma ON pulse(sigma_x100);
CREATE INDEX IF NOT EXISTS idx_pulse_scan ON pulse(scan_id);
CREATE INDEX IF NOT EXISTS idx_frame_sigma ON frame(sigma_x100);
CREATE INDEX IF NOT EXISTS idx_fold_sigma ON fold(sigma_x100);
CREATE INDEX IF NOT EXISTS idx_lag_sigma ON lag(sigma_x100);
CREATE INDEX IF NOT EXISTS idx_xeno_verdict ON xeno(verdict);
CREATE INDEX IF NOT EXISTS idx_sk_verdict ON sk(verdict);
CREATE INDEX IF NOT EXISTS idx_drift_scan ON drift(scan_id);
CREATE INDEX IF NOT EXISTS idx_jerk_scan ON jerk(scan_id);
CREATE INDEX IF NOT EXISTS idx_scint_scan ON scint(scan_id);
CREATE INDEX IF NOT EXISTS idx_files_relpath ON files(relpath);
CREATE INDEX IF NOT EXISTS idx_artifacts_scan ON artifacts(scan_id);
"""


# ---------------------------------------------------------------------------
# parsing helpers
# ---------------------------------------------------------------------------

def _int(v):
    if v is None:
        return None
    v = str(v).strip()
    if v in ("", "-", "None"):
        return None
    try:
        return int(float(v)) if "." in v and "e" not in v.lower() else int(v)
    except ValueError:
        try:
            return int(float(v))
        except ValueError:
            return None


def _float(v):
    if v is None:
        return None
    v = str(v).strip()
    if v in ("", "-", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _text(v):
    if v is None:
        return None
    v = str(v).strip()
    return v if v != "" else None


# header tuple -> (table, colmap). colmap maps table-col -> csv-col name.
# frame/fold share shapes; disambiguated by filename (see classify_csv).
_FRAME_A = ("rank", "freq_hz_x100", "period_ms_x100", "sigma_x100", "detected")
_FRAME_B = ("rank", "period_ms_x100", "freq_hz_x100", "sigma_x100", "detected")

_CSV_MAP = {
    ("file", "samples", "nseg", "skdev_x1e3", "skfrac_x1e4", "skflag", "verdict"):
        ("sk", None),
    ("file", "samples", "skdev_x1000", "skfrac_x10000", "skflag", "coh_x100",
     "cohflag", "ladder_x100", "ladderq", "dm_sign", "dm_r2_x1000", "impuls",
     "maxz_x10", "kurt_x100", "tailx_x100", "lattice", "verdict"):
        ("xeno", None),
    ("tag", "seg", "rank", "bin", "alpha_hz_x100", "ratio_x100", "log10p_x100", "hit"):
        ("fam", None),
    ("tag", "rank", "bin", "alpha_hz_x100", "ratio_x100", "hit"):
        ("fam", {"seg": None, "log10p_x100": None}),
    ("dm", "width", "sigma_x100", "t", "verdict"):
        ("pulse", None),
    ("freq_hz", "drift_x100", "sigma_x100", "kind"):
        ("drift", None),
    _FRAME_A: ("framefold", None),
    _FRAME_B: ("framefold", None),
    ("rank", "lag", "period_ms_x100", "freq_hz_x100", "sigma_x100",
     "persist_x100", "fold_x100", "fam_x100", "kind", "verdict"):
        ("lag", None),
    ("f0_hz", "drift_hz_s", "jerk_hz_s2", "score_x100", "gain_db_x100",
     "sidereal_anom", "verdict"):
        ("jerk", None),
    ("class", "m_med_x100", "m_max_x100", "tau_frames_x100", "xcorr_x100",
     "pol_verdict", "dfreq_hz", "pol_env_corr_x100"):
        ("scint", None),
    ("tool", "star", "leg", "chan", "kind", "freq_hz", "alpha_hz",
     "period_ms", "sigma", "verdict", "source"):
        ("evidence", None),
    ("freq_hz", "shift_bins", "sigma_x100", "kind"):
        ("stack", None),
    ("file", "samples", "baud", "sps", "bits", "ccsds_hits", "barker_hits",
     "frame_len", "verdict"):
        ("packet", None),
    ("p", "q", "sigma_x100", "agree_x100", "sync_k", "sync_score_x100", "verdict"):
        ("raster", None),
    ("file", "mode", "stream", "nbits", "ones_x1000", "runs", "verdict"):
        ("bits", None),
    ("file", "nbits", "ones_x1000", "distinct", "sub_x100", "stk_ops",
     "stk_loops", "stk_depth", "stk_w", "ca_x1e6", "acf_lag", "acf_z_x10",
     "bm_L", "bm_z_x10", "ras_w", "ras_h", "ras_z_x10", "tag_steps",
     "tag_depth", "tag_fire", "jit_equiv", "mut_stk", "mut_bm_x10",
     "score_x100", "verdict"):
        ("xvm", {"distinct_count": "distinct"}),
    ("on_file", "off_file", "kind", "on_flag", "off_flag", "on_best",
     "off_best", "verdict", "reason"):
        ("cadence", None),
    ("file", "source", "nchans", "nspec", "mode", "out_n", "fs_hz",
     "tsamp_us", "fch1_x1e4", "foff_hz_x1e3", "verdict"):
        ("ingest", {"source_name": "source"}),
    ("bin_lo", "freq_lo_mhz", "mean", "std", "max", "median", "top3(bin:val)"):
        ("spectrum", {"maxv": "max", "top3": "top3(bin:val)"}),
}


def classify_csv(header, filename):
    """Return (table, colmap) or (None, None) for unknown headers."""
    key = tuple(h.strip() for h in header)
    hit = _CSV_MAP.get(key)
    if hit is None:
        return None, None
    table, colmap = hit
    if table == "framefold":
        name = filename.lower()
        table = "fold" if "fold" in name else "frame"
    return table, colmap


# table -> {table-col: parser}
_PARSERS = {
    "sk": {"file": _text, "samples": _int, "nseg": _int, "skdev_x1e3": _int,
           "skfrac_x1e4": _int, "skflag": _int, "verdict": _text},
    "xeno": {"file": _text, "samples": _int, "skdev_x1000": _int,
             "skfrac_x10000": _int, "skflag": _int, "coh_x100": _int,
             "cohflag": _int, "ladder_x100": _int, "ladderq": _int,
             "dm_sign": _text, "dm_r2_x1000": _int, "impuls": _int,
             "maxz_x10": _int, "kurt_x100": _int, "tailx_x100": _int,
             "lattice": _text, "verdict": _text},
    "fam": {"tag": _text, "seg": _int, "rank": _int, "bin": _int,
            "alpha_hz_x100": _int, "ratio_x100": _int, "log10p_x100": _int,
            "hit": _int},
    "pulse": {"dm": _float, "width": _float, "sigma_x100": _int, "t": _float,
              "verdict": _text},
    "drift": {"freq_hz": _float, "drift_x100": _float, "sigma_x100": _int,
              "kind": _text},
    "frame": {"rank": _int, "period_ms_x100": _float, "freq_hz_x100": _float,
              "sigma_x100": _int, "detected": _int},
    "fold": {"rank": _int, "period_ms_x100": _float, "freq_hz_x100": _float,
             "sigma_x100": _int, "detected": _int},
    "lag": {"rank": _int, "lag": _int, "period_ms_x100": _float,
            "freq_hz_x100": _float, "sigma_x100": _int, "persist_x100": _int,
            "fold_x100": _int, "fam_x100": _int, "kind": _text, "verdict": _text},
    "jerk": {"f0_hz": _float, "drift_hz_s": _float, "jerk_hz_s2": _float,
             "score_x100": _int, "gain_db_x100": _int, "sidereal_anom": _int,
             "verdict": _text},
    "scint": {"class": _text, "m_med_x100": _int, "m_max_x100": _int,
              "tau_frames_x100": _int, "xcorr_x100": _int, "pol_verdict": _text,
              "dfreq_hz": _float, "pol_env_corr_x100": _int},
    "evidence": {"tool": _text, "star": _text, "leg": _text, "chan": _int,
                 "kind": _text, "freq_hz": _float, "alpha_hz": _float,
                 "period_ms": _float, "sigma": _float, "verdict": _text,
                 "src": "source"},
    "stack": {"freq_hz": _float, "shift_bins": _int, "sigma_x100": _int,
              "kind": _text},
    "packet": {"file": _text, "samples": _int, "baud": _float, "sps": _float,
               "bits": _int, "ccsds_hits": _int, "barker_hits": _int,
               "frame_len": _int, "verdict": _text},
    "raster": {"p": _int, "q": _int, "sigma_x100": _int, "agree_x100": _int,
               "sync_k": _int, "sync_score_x100": _int, "verdict": _text},
    "bits": {"file": _text, "mode": _text, "stream": _text, "nbits": _int,
             "ones_x1000": _int, "runs": _int, "verdict": _text},
    "xvm": {"file": _text, "nbits": _int, "ones_x1000": _int,
            "distinct_count": _int, "sub_x100": _int, "stk_ops": _int,
            "stk_loops": _int, "stk_depth": _int, "stk_w": _int,
            "ca_x1e6": _int, "acf_lag": _int, "acf_z_x10": _int,
            "bm_L": _int, "bm_z_x10": _int, "ras_w": _int, "ras_h": _int,
            "ras_z_x10": _int, "tag_steps": _int, "tag_depth": _int,
            "tag_fire": _int, "jit_equiv": _int, "mut_stk": _int,
            "mut_bm_x10": _int, "score_x100": _int, "verdict": _text},
    "cadence": {"on_file": _text, "off_file": _text, "kind": _text,
                "on_flag": _int, "off_flag": _int, "on_best": _float,
                "off_best": _float, "verdict": _text, "reason": _text},
    "ingest": {"file": _text, "source_name": _text, "nchans": _int,
               "nspec": _int, "mode": _text, "out_n": _int, "fs_hz": _float,
               "tsamp_us": _float, "fch1_x1e4": _float, "foff_hz_x1e3": _float,
               "verdict": _text},
    "spectrum": {"bin_lo": _int, "freq_lo_mhz": _float, "mean": _float,
                 "std": _float, "maxv": _float, "median": _float, "top3": _text},
}


# ---------------------------------------------------------------------------
# connect / init
# ---------------------------------------------------------------------------

def connect(db_path):
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    return con


def init_db(con):
    con.executescript(_SCHEMA)
    con.executescript(_VIEWS)
    con.execute("INSERT OR IGNORE INTO meta(key,value) VALUES('schema_version',?)",
                (str(SCHEMA_VERSION),))
    con.commit()


# ---------------------------------------------------------------------------
# ingest
# ---------------------------------------------------------------------------

ARTIFACT_SUFFIXES = {
    ".png": "png", ".md": "md", ".f32": "f32", ".bin": "bin",
    ".log": "log", ".json": "json", ".txt": "txt", ".py": "py",
}

_TABULAR_TSV = {
    "summary.tsv": "stage_runs",
    "census.tsv": "census",
    "ANOMALY_LEDGER.tsv": "anomaly",
}


def _scan_id(con, report_dir, campaign):
    con.execute(
        "INSERT OR IGNORE INTO scans(report_dir, campaign) VALUES(?,?)",
        (report_dir, campaign))
    return con.execute("SELECT scan_id FROM scans WHERE report_dir=?",
                       (report_dir,)).fetchone()[0]


def _already_current(con, relpath, mtime, size):
    row = con.execute("SELECT mtime, size FROM files WHERE relpath=?",
                      (relpath,)).fetchone()
    return row is not None and row[0] == mtime and row[1] == size


def _record_file(con, scan_id, relpath, kind, mtime, size, nrows):
    con.execute(
        """INSERT INTO files(scan_id, relpath, kind, mtime, size, nrows)
           VALUES(?,?,?,?,?,?)
           ON CONFLICT(relpath) DO UPDATE SET
             scan_id=excluded.scan_id, kind=excluded.kind,
             mtime=excluded.mtime, size=excluded.size, nrows=excluded.nrows""",
        (scan_id, relpath, kind, mtime, size, nrows))


def _delete_source_rows(con, table, relpath):
    con.execute(f"DELETE FROM {table} WHERE source=?", (relpath,))


def ingest_csv(con, scan_id, relpath, path, mtime, size):
    try:
        with open(path, newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh)
            try:
                header = next(reader)
            except StopIteration:
                _record_file(con, scan_id, relpath, "empty", mtime, size, 0)
                return ("empty", 0)
            table, colmap = classify_csv(header, path.name)
            if table is None:
                n = 0
                for i, row in enumerate(reader, start=2):
                    con.execute(
                        "INSERT INTO raw_csv(scan_id, source, header, line_no, line_json)"
                        " VALUES(?,?,?,?,?)",
                        (scan_id, relpath, ",".join(header), i,
                         json.dumps(row)))
                    n += 1
                _record_file(con, scan_id, relpath, "raw_csv", mtime, size, n)
                return ("raw_csv", n)
            # typed insert
            _delete_source_rows(con, table, relpath)
            parsers = _PARSERS[table]
            cols = list(parsers)
            idx_of = {h.strip(): i for i, h in enumerate(header)}
            batch, n = [], 0
            for row in reader:
                if not row or all(c.strip() == "" for c in row):
                    continue
                vals = []
                for tcol, spec in parsers.items():
                    csv_col = tcol if spec != "source" and not isinstance(spec, str) \
                        else (spec if isinstance(spec, str) else tcol)
                    if colmap and tcol in colmap:
                        mapped = colmap[tcol]
                        if mapped is None:
                            vals.append(None)
                            continue
                        csv_col = mapped
                    if tcol == "src":  # evidence.src <- csv 'source'
                        csv_col = "source"
                    parse_fn = _PARSERS[table][tcol]
                    if callable(parse_fn):
                        j = idx_of.get(csv_col)
                        vals.append(parse_fn(row[j]) if j is not None and j < len(row) else None)
                    else:  # pragma: no cover - defensive
                        vals.append(None)
                batch.append((scan_id, relpath, *vals))
                if len(batch) >= 2000:
                    con.executemany(
                        f"INSERT INTO {table}(scan_id, source, {','.join(cols)})"
                        f" VALUES({','.join(['?'] * (len(cols) + 2))})", batch)
                    n += len(batch)
                    batch = []
            if batch:
                con.executemany(
                    f"INSERT INTO {table}(scan_id, source, {','.join(cols)})"
                    f" VALUES({','.join(['?'] * (len(cols) + 2))})", batch)
                n += len(batch)
            _record_file(con, scan_id, relpath, table, mtime, size, n)
            return (table, n)
    except OSError:
        _record_file(con, scan_id, relpath, "unreadable", mtime, size, 0)
        return ("unreadable", 0)


def ingest_tsv(con, scan_id, relpath, path, mtime, size):
    name = path.name
    kind = _TABULAR_TSV.get(name)
    try:
        text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ("unreadable", 0)
    if kind == "stage_runs":
        con.execute("DELETE FROM stage_runs WHERE source=?", (relpath,))
        n = 0
        for row in csv.DictReader(
                (l for l in text if l.strip()), delimiter="\t"):
            con.execute(
                """INSERT INTO stage_runs(scan_id, source, chan, pol, tool, exit,
                                          seconds, receipt, verdicts, outputs, log)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (scan_id, relpath, (row.get("chan") or None),
                 (row.get("pol") or None), _text(row.get("tool")),
                 _int(row.get("exit")), _float(row.get("seconds")),
                 _text(row.get("receipt")), _text(row.get("verdicts")),
                 _text(row.get("outputs")), _text(row.get("log"))))
            n += 1
        _record_file(con, scan_id, relpath, "stage_runs", mtime, size, n)
        return ("stage_runs", n)
    if kind == "census":
        con.execute("DELETE FROM census WHERE source=?", (relpath,))
        n = 0
        for row in csv.DictReader(
                (l for l in text if l.strip() and not l.startswith("#")),
                delimiter="\t"):
            if "chan" not in (row or {}):
                continue
            con.execute(
                "INSERT INTO census(scan_id, source, chan, freq_mhz,"
                " peak_over_base, xeno_fam) VALUES(?,?,?,?,?,?)",
                (scan_id, relpath, _int(row.get("chan")),
                 _float(row.get("freq_mhz")), _float(row.get("peak_over_base")),
                 _text(row.get("xeno_fam"))))
            n += 1
        _record_file(con, scan_id, relpath, "census", mtime, size, n)
        return ("census", n)
    if kind == "anomaly":
        con.execute("DELETE FROM anomaly WHERE source=?", (relpath,))
        n = 0
        for row in csv.DictReader(
                (l for l in text if l.strip() and not l.startswith("#")),
                delimiter="\t"):
            con.execute(
                """INSERT INTO anomaly(scan_id, source, target, chan, freq_mhz,
                                       cadence, stokes_v, disposition, waterfall)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (scan_id, relpath, _text(row.get("target")),
                 _text(row.get("chan")), _float(row.get("freq_mhz")),
                 _text(row.get("cadence")), _text(row.get("stokes_v")),
                 _text(row.get("disposition")), _text(row.get("waterfall"))))
            n += 1
        _record_file(con, scan_id, relpath, "anomaly", mtime, size, n)
        return ("anomaly", n)
    # freeform / log-shaped TSV -> raw_tsv (skip comment-only fast path? no: keep all)
    con.execute("DELETE FROM raw_tsv WHERE source=?", (relpath,))
    batch = [(scan_id, relpath, i + 1, line[:4000])
             for i, line in enumerate(text)]
    con.executemany(
        "INSERT INTO raw_tsv(scan_id, source, line_no, line) VALUES(?,?,?,?)",
        batch)
    _record_file(con, scan_id, relpath, "raw_tsv", mtime, size, len(batch))
    return ("raw_tsv", len(batch))


def _loads_lenient(text):
    r"""json.loads + repair for unify's unescaped Windows paths.

    verdicts.json embeds `"dir":"D:\TurboKain\reports\..."` with bare
    backslashes (strictly invalid JSON: `\T` is not an escape). Repair only
    backslashes that do NOT start a valid escape sequence, leaving real
    escapes (\\n, \\t, \\uXXXX, ...) untouched.
    """
    import re
    try:
        return json.loads(text)
    except ValueError:
        pass
    fixed = re.sub(r'\\(?!["\\\\/bfnrtu])', r'\\\\', text)
    return json.loads(fixed)


def ingest_json(con, scan_id, relpath, path, mtime, size):
    try:
        doc = _loads_lenient(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        _record_file(con, scan_id, relpath, "unreadable", mtime, size, 0)
        return ("unreadable", 0)
    name = path.name.lower()
    kind = ("manifest" if name == "manifest.json"
            else "verdicts" if name == "verdicts.json"
            else "campaign_digest" if name in ("campaign_digest.json",)
            else "other")
    con.execute("DELETE FROM documents WHERE source=?", (relpath,))
    con.execute("INSERT INTO documents(scan_id, source, kind, doc_json)"
                " VALUES(?,?,?,?)",
                (scan_id, relpath, kind, json.dumps(doc)))
    if kind == "manifest":
        con.execute("UPDATE scans SET manifest_json=? WHERE scan_id=?",
                    (json.dumps(doc), scan_id))
        target = doc.get("target") or doc.get("campaign")
        disp = doc.get("disposition")
        if target or disp:
            con.execute(
                "UPDATE scans SET target=COALESCE(target,?),"
                " disposition=COALESCE(disposition,?) WHERE scan_id=?",
                (target, disp, scan_id))
    elif kind == "verdicts":
        con.execute("UPDATE scans SET verdicts_json=? WHERE scan_id=?",
                    (json.dumps(doc), scan_id))
        meta = doc.get("meta", {}) if isinstance(doc, dict) else {}
        if meta.get("target") and meta.get("target") != "UNKNOWN":
            con.execute("UPDATE scans SET target=? WHERE scan_id=?",
                        (meta["target"], scan_id))
        if doc.get("disposition"):
            con.execute("UPDATE scans SET disposition=? WHERE scan_id=?",
                        (doc["disposition"], scan_id))
        con.execute("DELETE FROM lattice WHERE source=?", (relpath,))
        for row in doc.get("lattice", []) or []:
            con.execute(
                """INSERT INTO lattice(scan_id, source, star, leg, chan, sk, xeno,
                                       fam, fold, boxcar, frame, drift, lag, jerk, scint)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (scan_id, relpath, _text(row.get("star")), _text(row.get("leg")),
                 _int(row.get("chan")), _text(row.get("sk")), _text(row.get("xeno")),
                 _text(row.get("fam")), _text(row.get("fold")),
                 _text(row.get("boxcar")), _text(row.get("frame")),
                 _text(row.get("drift")), _text(row.get("lag")),
                 _text(row.get("jerk")), _text(row.get("scint"))))
        con.execute("DELETE FROM floors WHERE source=?", (relpath,))
        for k, v in (doc.get("floors", {}) or {}).items():
            con.execute("INSERT INTO floors(scan_id, source, tool, best_subgate)"
                        " VALUES(?,?,?,?)", (scan_id, relpath, k, _int(v)))
    _record_file(con, scan_id, relpath, f"json:{kind}", mtime, size, 1)
    return (f"json:{kind}", 1)


def ingest_reports(root, con, subpath="reports", full=False, progress=None):
    """Walk root/subpath, ingest every new/changed tabular file.

    Returns dict(kind -> (files, rows)). Incremental unless full=True.
    """
    base = Path(root) / subpath
    if not base.exists():
        raise FileNotFoundError(f"ingest: not found: {base}")
    if full:
        for t in ("sk", "xeno", "fam", "pulse", "drift", "frame", "fold", "lag",
                  "jerk", "scint", "evidence", "stack", "packet", "raster",
                  "bits", "xvm", "cadence", "ingest", "spectrum", "census",
                  "anomaly", "stage_runs", "lattice", "floors", "documents",
                  "raw_csv", "raw_tsv", "artifacts", "files", "scans"):
            con.execute(f"DELETE FROM {t}")
        con.commit()
    stats = {}
    pending = 0

    def bump(kind, nrows):
        f, r = stats.get(kind, (0, 0))
        stats[kind] = (f + 1, r + nrows)

    # collect first so campaign grouping is stable
    all_paths = sorted(p for p in base.rglob("*") if p.is_file())
    t0 = time.time()
    for i, path in enumerate(all_paths):
        rel = path.relative_to(root).as_posix()
        # scan dir = parent for top-level files, else top-level campaign dir
        try:
            rel_to_base = path.relative_to(base)
            top = rel_to_base.parts[0]
            top_path = base / top
            scan_dir = top if top_path.is_dir() else "."
            scan_rel = (subpath + "/" + scan_dir).replace("\\", "/")
            campaign = top if scan_dir != top else None
            if len(rel_to_base.parts) == 1:
                scan_rel, campaign = subpath, None
        except ValueError:  # pragma: no cover - defensive
            scan_rel, campaign = subpath, None
        st = path.stat()
        mtime, size = st.st_mtime, st.st_size
        suffix = path.suffix.lower()
        if suffix in (".csv", ".tsv", ".json"):
            if _already_current(con, rel, mtime, size) and not full:
                kind = con.execute("SELECT kind FROM files WHERE relpath=?",
                                   (rel,)).fetchone()[0]
                bump(f"skip:{kind}", 0)
                continue
            scan_id = _scan_id(con, scan_rel, campaign)
            if suffix == ".csv":
                kind, n = ingest_csv(con, scan_id, rel, path, mtime, size)
            elif suffix == ".tsv":
                kind, n = ingest_tsv(con, scan_id, rel, path, mtime, size)
            else:
                kind, n = ingest_json(con, scan_id, rel, path, mtime, size)
            bump(kind, n)
        else:
            akind = ARTIFACT_SUFFIXES.get(suffix, "other")
            if _already_current(con, rel, mtime, size) and not full:
                bump("skip:artifact", 0)
                continue
            scan_id = _scan_id(con, scan_rel, campaign)
            con.execute("DELETE FROM artifacts WHERE relpath=?", (rel,))
            con.execute(
                "INSERT INTO artifacts(scan_id, relpath, kind, size)"
                " VALUES(?,?,?,?)", (scan_id, rel, akind, size))
            _record_file(con, scan_id, rel, "artifact", mtime, size, 0)
            bump("artifact", 0)
        pending += 1
        if pending >= 500:
            con.commit()
            pending = 0
        if progress and (i + 1) % 5000 == 0:
            progress(i + 1, len(all_paths), time.time() - t0)
    con.commit()

    # roll up per-scan counters
    for (scan_id,) in con.execute("SELECT scan_id FROM scans").fetchall():
        n_files = con.execute(
            "SELECT COUNT(*) FROM files WHERE scan_id=? AND kind NOT IN"
            " ('artifact','empty','unreadable')", (scan_id,)).fetchone()[0]
        n_art = con.execute(
            "SELECT COUNT(*) FROM artifacts WHERE scan_id=?", (scan_id,)).fetchone()[0]
        n_rows = 0
        for t in ("sk", "xeno", "fam", "pulse", "drift", "frame", "fold", "lag",
                  "jerk", "scint", "evidence", "stack", "packet", "raster",
                  "bits", "xvm", "cadence", "ingest", "spectrum", "census",
                  "anomaly", "stage_runs", "lattice", "floors", "documents",
                  "raw_csv", "raw_tsv"):
            n_rows += con.execute(
                f"SELECT COUNT(*) FROM {t} WHERE scan_id=?", (scan_id,)).fetchone()[0]
        con.execute(
            "UPDATE scans SET n_files=?, n_rows=?, n_artifacts=?,"
            " ingested_at=datetime('now') WHERE scan_id=?",
            (n_files, n_rows, n_art, scan_id))
    con.commit()
    con.executescript(_INDEXES)
    con.executescript(_VIEWS)
    return stats


# ---------------------------------------------------------------------------
# statistics + canned queries (the "proper statistics" half)
# ---------------------------------------------------------------------------

def db_totals(con):
    out = {}
    out["scans"] = con.execute("SELECT COUNT(*) FROM scans").fetchone()[0]
    out["files_parsed"] = con.execute(
        "SELECT COUNT(*) FROM files WHERE kind NOT IN"
        " ('artifact','empty','unreadable')").fetchone()[0]
    out["artifacts"] = con.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]
    out["coverage"] = [dict(r) for r in
                       con.execute("SELECT * FROM v_tool_coverage ORDER BY rows_ DESC")]
    return out


def _quantiles(con, table, col, where=""):
    q = f"SELECT {col} AS v FROM {table} {where} ORDER BY {col}"
    vals = [r[0] for r in con.execute(q) if r[0] is not None]
    if not vals:
        return {"n": 0}
    import statistics as _s

    def pct(p):
        k = (len(vals) - 1) * p / 100
        lo, hi = int(k), min(int(k) + 1, len(vals) - 1)
        return vals[lo] + (vals[hi] - vals[lo]) * (k - lo)
    return {"n": len(vals), "min": vals[0], "p50": pct(50),
            "p90": pct(90), "p99": pct(99), "max": vals[-1],
            "mean": _s.fmean(vals)}


def verdict_counts(con, table):
    return [dict(r) for r in con.execute(
        f"SELECT verdict, COUNT(*) AS n FROM {table}"
        " WHERE verdict IS NOT NULL GROUP BY verdict ORDER BY n DESC LIMIT 20")]


def compute_stats(con):
    """Full statistics payload: distributions, verdict census, top hits."""
    s = {"totals": db_totals(con)}
    s["evidence_verdicts"] = verdict_counts(con, "evidence")
    s["xeno_verdicts"] = verdict_counts(con, "xeno")
    s["sk_verdicts"] = verdict_counts(con, "sk")
    s["lag_verdicts"] = verdict_counts(con, "lag")
    s["jerk_verdicts"] = verdict_counts(con, "jerk")
    s["scint_classes"] = [dict(r) for r in con.execute(
        "SELECT class AS verdict, COUNT(*) AS n FROM scint"
        " GROUP BY class ORDER BY n DESC LIMIT 20")]
    s["cadence_verdicts"] = verdict_counts(con, "cadence")
    s["packet_verdicts"] = verdict_counts(con, "packet")
    s["raster_verdicts"] = verdict_counts(con, "raster")
    s["pulse_sigma"] = _quantiles(con, "pulse", "sigma_x100")
    s["frame_sigma"] = _quantiles(con, "frame", "sigma_x100")
    s["fold_sigma"] = _quantiles(con, "fold", "sigma_x100")
    s["lag_sigma"] = _quantiles(con, "lag", "sigma_x100")
    s["fam_ratio"] = _quantiles(con, "fam", "ratio_x100")
    s["xeno_maxz"] = _quantiles(con, "xeno", "maxz_x10")
    s["n_fam_hits"] = con.execute("SELECT COUNT(*) FROM fam WHERE hit=1").fetchone()[0]
    s["n_evidence_hits"] = con.execute(
        "SELECT COUNT(*) FROM evidence WHERE verdict NOT IN ('CLEAN','-','')"
        " AND verdict IS NOT NULL").fetchone()[0]
    s["top_evidence"] = [dict(r) for r in con.execute(
        "SELECT scan, tool, star, leg, chan, kind, freq_hz, alpha_hz,"
        " period_ms, sigma, verdict, source FROM v_evidence_hits"
        " ORDER BY sigma DESC LIMIT 25")]
    s["top_fam"] = [dict(r) for r in con.execute(
        "SELECT * FROM v_fam_hits ORDER BY ratio DESC LIMIT 25")]
    s["top_scans"] = [dict(r) for r in con.execute(
        "SELECT * FROM v_scan_stats ORDER BY n_rows DESC LIMIT 15")]
    s["hits_by_tool"] = [dict(r) for r in con.execute(
        "SELECT tool, verdict, COUNT(*) AS n FROM evidence"
        " GROUP BY tool, verdict ORDER BY n DESC LIMIT 30")]
    s["floors_median"] = [dict(r) for r in con.execute(
        "SELECT tool, COUNT(*) AS n, AVG(best_subgate) AS mean_gate,"
        " MIN(best_subgate) AS min_gate, MAX(best_subgate) AS max_gate"
        " FROM floors GROUP BY tool ORDER BY tool")]
    return s


def format_stats(s):
    L = []
    t = s["totals"]
    L.append(f"scans: {t['scans']}  tabular files: {t['files_parsed']}"
             f"  artifacts: {t['artifacts']}")
    L.append("")
    L.append("rows per tool (rows / files):")
    for r in t["coverage"]:
        L.append(f"  {r['tool']:10} {r['rows_']:>10} / {r['files']:<6}")
    L.append("")
    L.append(f"fam hardware hits (hit=1): {s['n_fam_hits']}"
             f"   evidence non-clean rows: {s['n_evidence_hits']}")
    for key in ("evidence_verdicts", "xeno_verdicts", "sk_verdicts",
                "lag_verdicts", "jerk_verdicts", "scint_classes",
                "cadence_verdicts", "packet_verdicts", "raster_verdicts"):
        rows = s[key]
        if rows:
            L.append(f"{key}: " + ", ".join(
                f"{r['verdict']}={r['n']}" for r in rows[:8]))
    L.append("")
    for key in ("pulse_sigma", "frame_sigma", "fold_sigma", "lag_sigma",
                "fam_ratio", "xeno_maxz"):
        q = s[key]
        if q.get("n"):
            L.append(f"{key}: n={q['n']} min={q['min']} p50={q['p50']:.1f}"
                     f" p90={q['p90']:.1f} p99={q['p99']:.1f} max={q['max']}"
                     f" mean={q['mean']:.1f}")
    L.append("")
    L.append("top evidence rows by sigma:")
    for r in s["top_evidence"][:15]:
        L.append(f"  sigma={r['sigma']} {r['verdict']} {r['tool']}/{r['kind']}"
                 f" {r['scan']} :: {r['source']}")
    L.append("")
    L.append("top fam hits by ratio:")
    for r in s["top_fam"][:10]:
        L.append(f"  ratio={r['ratio']} alpha={r['alpha_hz']}Hz"
                 f" {r['scan']} :: {r['source']}")
    L.append("")
    L.append("biggest scans by row count:")
    for r in s["top_scans"][:10]:
        L.append(f"  {r['n_rows']:>9} rows  hits={r['n_hits']} fam={r['n_fam_hits']}"
                 f"  {r['scan']}")
    if s["floors_median"]:
        L.append("")
        L.append("sub-gate floors (mean over verdicts.json files):")
        for r in s["floors_median"]:
            L.append(f"  {r['tool']:22} n={r['n']:<5} mean={r['mean_gate']:.0f}"
                     f" min={r['min_gate']} max={r['max_gate']}")
    return "\n".join(L)


def top_hits(con, min_sigma=0, verdict=None, limit=50):
    q = ("SELECT scan, tool, star, leg, chan, kind, freq_hz, alpha_hz,"
         " period_ms, sigma, verdict, source FROM v_evidence_hits WHERE sigma >= ?")
    args = [min_sigma]
    if verdict:
        q += " AND verdict = ?"
        args.append(verdict)
    q += " ORDER BY sigma DESC LIMIT ?"
    args.append(limit)
    return [dict(r) for r in con.execute(q, args)]


def run_query(con, sql, limit=200):
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchmany(limit)
    return cols, [tuple(r) for r in rows]


# ---------------------------------------------------------------------------
# unified search engine (backs `tk db search` and the pi search tool)
#
# Every searchable table declares how the global filters map onto its
# columns. Scores are normalized to real (un-scaled) units per table; the
# unit travels with each row as `score_unit` so cross-table sorting stays
# honest and documented.
# ---------------------------------------------------------------------------

# table -> spec. Keys: score (SQL expr or None), score_unit, freq (Hz expr or
# None), verdict (col name, 'HITMAP:name' pseudo, or None), text_cols,
# extra_cols (carried into `raw`), chan_col, star_col, leg_col, tool_col.
# HITMAP pseudo-cols: fam:hit (1->HIT,0->CLEAN), frame/fold:detected,
# drift:kind, stack:kind, scint:class, census:xeno_fam, anomaly:disposition,
# lattice:cells (any cell LIKE).
_SEARCH_SPECS = {
    "evidence": {"score": "t.sigma", "score_unit": "sigma",
                 "freq": "t.freq_hz", "verdict": "verdict",
                 "text_cols": ["tool", "star", "leg", "kind", "verdict", "src"],
                 "chan_col": "chan", "star_col": "star", "leg_col": "leg",
                 "tool_col": "tool",
                 "extra_cols": ["tool", "star", "leg", "chan", "kind",
                                  "freq_hz", "alpha_hz", "period_ms", "sigma"]},
    "fam": {"score": "t.ratio_x100 / 100.0", "score_unit": "ratio",
              "freq": "t.alpha_hz_x100 / 100.0", "verdict": "HITMAP:hit",
              "text_cols": ["tag"],
              "extra_cols": ["tag", "seg", "rank", "bin",
                               "alpha_hz_x100", "ratio_x100", "log10p_x100", "hit"]},
    "pulse": {"score": "t.sigma_x100 / 100.0", "score_unit": "sigma",
                "freq": None, "verdict": "verdict",
                "text_cols": ["verdict"],
                "extra_cols": ["dm", "width", "sigma_x100", "t"]},
    "frame": {"score": "t.sigma_x100 / 100.0", "score_unit": "sigma",
                "freq": "t.freq_hz_x100 / 100.0", "verdict": "HITMAP:detected",
                "text_cols": [],
                "extra_cols": ["rank", "period_ms_x100", "freq_hz_x100",
                                 "sigma_x100", "detected"]},
    "fold": {"score": "t.sigma_x100 / 100.0", "score_unit": "sigma",
               "freq": "t.freq_hz_x100 / 100.0", "verdict": "HITMAP:detected",
               "text_cols": [],
               "extra_cols": ["rank", "period_ms_x100", "freq_hz_x100",
                                "sigma_x100", "detected"]},
    "lag": {"score": "t.sigma_x100 / 100.0", "score_unit": "sigma",
              "freq": "t.freq_hz_x100 / 100.0", "verdict": "verdict",
              "text_cols": ["kind", "verdict"],
              "extra_cols": ["rank", "lag", "period_ms_x100", "freq_hz_x100",
                               "sigma_x100", "persist_x100", "fold_x100",
                               "fam_x100", "kind"]},
    "drift": {"score": "t.sigma_x100", "score_unit": "sigma_x100",
                "freq": "t.freq_hz", "verdict": "HITMAP:kind",
                "text_cols": ["kind"],
                "extra_cols": ["freq_hz", "drift_x100", "sigma_x100", "kind"]},
    "jerk": {"score": "t.score_x100 / 100.0", "score_unit": "score",
               "freq": "t.f0_hz", "verdict": "verdict",
               "text_cols": ["verdict"],
               "extra_cols": ["f0_hz", "drift_hz_s", "jerk_hz_s2", "score_x100",
                                "gain_db_x100", "sidereal_anom"]},
    "scint": {"score": "t.m_max_x100 / 100.0", "score_unit": "m_max",
                "freq": "t.dfreq_hz", "verdict": "HITMAP:class",
                "text_cols": ["class", "pol_verdict"],
                "extra_cols": ["class", "m_med_x100", "m_max_x100",
                                 "tau_frames_x100", "xcorr_x100", "pol_verdict",
                                 "dfreq_hz", "pol_env_corr_x100"]},
    "xeno": {"score": "t.maxz_x10 / 10.0", "score_unit": "maxz",
               "freq": None, "verdict": "verdict",
               "text_cols": ["lattice", "verdict", "file"],
               "extra_cols": ["file", "samples", "skdev_x1000", "skfrac_x10000",
                                "skflag", "coh_x100", "ladder_x100", "impuls",
                                "maxz_x10", "kurt_x100", "tailx_x100", "lattice"]},
    "sk": {"score": "t.skdev_x1e3 / 1000.0", "score_unit": "skdev",
             "freq": None, "verdict": "verdict",
             "text_cols": ["verdict", "file"],
             "extra_cols": ["file", "samples", "nseg", "skdev_x1e3",
                              "skfrac_x1e4", "skflag"]},
    "stack": {"score": "t.sigma_x100", "score_unit": "sigma_x100",
                "freq": "t.freq_hz", "verdict": "HITMAP:kind",
                "text_cols": ["kind"],
                "extra_cols": ["freq_hz", "shift_bins", "sigma_x100", "kind"]},
    "packet": {"score": "(t.ccsds_hits + t.barker_hits)", "score_unit": "hits",
                 "freq": None, "verdict": "verdict",
                 "text_cols": ["verdict", "file"],
                 "extra_cols": ["file", "samples", "baud", "sps", "bits",
                                  "ccsds_hits", "barker_hits", "frame_len"]},
    "raster": {"score": "t.sigma_x100 / 100.0", "score_unit": "sigma",
                 "freq": None, "verdict": "verdict",
                 "text_cols": ["verdict"],
                 "extra_cols": ["p", "q", "sigma_x100", "agree_x100",
                                  "sync_k", "sync_score_x100"]},
    "cadence": {"score": None, "score_unit": "none",
                  "freq": None, "verdict": "verdict",
                  "text_cols": ["kind", "verdict", "reason"],
                  "extra_cols": ["on_file", "off_file", "kind", "on_flag",
                                   "off_flag", "on_best", "off_best", "reason"]},
    "bits": {"score": None, "score_unit": "none",
               "freq": None, "verdict": "verdict",
               "text_cols": ["mode", "verdict", "file"],
               "extra_cols": ["file", "mode", "stream", "nbits",
                                "ones_x1000", "runs"]},
    "xvm": {"score": "t.score_x100 / 100.0", "score_unit": "score",
              "freq": None, "verdict": "verdict",
              "text_cols": ["verdict", "file"],
              "extra_cols": ["file", "nbits", "score_x100", "tag_fire",
                               "stk_depth", "acf_z_x10", "bm_z_x10", "ras_z_x10"]},
    "census": {"score": "t.peak_over_base", "score_unit": "peak_over_base",
                 "freq": "t.freq_mhz * 1000000.0", "verdict": "HITMAP:xeno_fam",
                 "text_cols": ["xeno_fam"], "chan_col": "chan",
                 "extra_cols": ["chan", "freq_mhz", "peak_over_base", "xeno_fam"]},
    "anomaly": {"score": None, "score_unit": "none",
                  "freq": "t.freq_mhz * 1000000.0",
                  "verdict": "HITMAP:disposition",
                  "text_cols": ["target", "cadence", "disposition"],
                  "extra_cols": ["target", "chan", "freq_mhz", "cadence",
                                   "stokes_v", "disposition", "waterfall"]},
    "lattice": {"score": None, "score_unit": "none",
                  "freq": None, "verdict": "HITMAP:cells",
                  "text_cols": ["star", "leg", "sk", "xeno", "fam", "fold",
                                  "boxcar", "frame", "drift", "lag", "jerk", "scint"],
                  "chan_col": "chan", "star_col": "star", "leg_col": "leg",
                  "extra_cols": ["star", "leg", "chan", "sk", "xeno", "fam",
                                   "fold", "boxcar", "frame", "drift", "lag",
                                   "jerk", "scint"]},
    "spectrum": {"score": "t.maxv", "score_unit": "max_power",
                   "freq": "t.freq_lo_mhz * 1000000.0", "verdict": None,
                   "text_cols": [],
                   "extra_cols": ["bin_lo", "freq_lo_mhz", "mean", "std",
                                    "maxv", "median"]},
}

SEARCHABLE_TABLES = sorted(_SEARCH_SPECS)

# verdict aliases that map onto binary HITMAP pseudo-columns
_HIT_WORDS = ("HIT", "DETECTED", "SHOT", "WATCH", "PERIODIC", "FLAG",
              "STRONG", "CANDIDATE", "LOCKED", "FRAMED", "RASTER", "SPIKY")
_CLEAN_WORDS = ("CLEAN", "QUIET", "NOISE", "NO-PACKETS", "COMMON", "-", "")


def _hitmap_clause(table, col, verdict):
    """Build (sql, params) matching a user verdict against a HITMAP pseudo-col."""
    v = verdict.upper()
    is_hit = any(w in v for w in _HIT_WORDS)
    is_clean = (not is_hit) or any(w in v for w in _CLEAN_WORDS)
    if col in ("hit", "detected"):
        if is_hit and not is_clean:
            return ("t.%s = 1" % col, [])
        if is_clean and not is_hit:
            return ("t.%s = 0" % col, [])
        return ("t.%s = ?" % col, [1 if is_hit else 0])
    if col == "cells":
        cells = ["sk", "xeno", "fam", "fold", "boxcar", "frame",
                 "drift", "lag", "jerk", "scint"]
        ors = " OR ".join("t.%s LIKE ?" % c for c in cells)
        return ("(%s)" % ors, ["%%%s%%" % verdict] * len(cells))
    # text pseudo-cols (kind/class/disposition/xeno_fam): substring match
    return ("t.%s LIKE ?" % col, ["%%%s%%" % verdict])


def _build_where(table, spec, f):
    """WHERE clauses for one table from the normalized filter dict."""
    w, p = [], []
    if f.get("scan_contains"):
        w.append("s.report_dir LIKE ?")
        p.append("%%%s%%" % f["scan_contains"])
    if f.get("source_contains"):
        w.append("t.source LIKE ?")
        p.append("%%%s%%" % f["source_contains"])
    if f.get("verdict") and spec.get("verdict"):
        vc = spec["verdict"]
        if vc.startswith("HITMAP:"):
            clause, cparams = _hitmap_clause(table, vc[7:], f["verdict"])
            w.append(clause)
            p.extend(cparams)
        else:
            w.append("t.%s = ?" % vc)
            p.append(f["verdict"])
    elif f.get("verdict"):
        return None, None  # table cannot answer a verdict filter -> skip
    if f.get("min_score") is not None or f.get("max_score") is not None:
        if not spec.get("score"):
            return None, None  # table has no score -> skip
        if f.get("min_score") is not None:
            w.append("(%s) >= ?" % spec["score"])
            p.append(f["min_score"])
        if f.get("max_score") is not None:
            w.append("(%s) <= ?" % spec["score"])
            p.append(f["max_score"])
    if f.get("freq_min") is not None or f.get("freq_max") is not None:
        if not spec.get("freq"):
            return None, None
        if f.get("freq_min") is not None:
            w.append("(%s) >= ?" % spec["freq"])
            p.append(f["freq_min"])
        if f.get("freq_max") is not None:
            w.append("(%s) <= ?" % spec["freq"])
            p.append(f["freq_max"])
    if f.get("chan") is not None:
        if not spec.get("chan_col"):
            return None, None
        w.append("t.%s = ?" % spec["chan_col"])
        p.append(f["chan"])
    if f.get("star"):
        if not spec.get("star_col"):
            return None, None
        w.append("t.%s LIKE ?" % spec["star_col"])
        p.append("%%%s%%" % f["star"])
    if f.get("leg"):
        if not spec.get("leg_col"):
            return None, None
        w.append("t.%s LIKE ?" % spec["leg_col"])
        p.append("%%%s%%" % f["leg"])
    if f.get("tool"):
        if not spec.get("tool_col"):
            return None, None
        w.append("t.%s = ?" % spec["tool_col"])
        p.append(f["tool"])
    if f.get("text"):
        cols = spec.get("text_cols", [])
        if not cols:
            return None, None
        ors = " OR ".join("t.%s LIKE ?" % c for c in cols)
        w.append("(%s)" % ors)
        p.extend(["%%%s%%" % f["text"]] * len(cols))
    return w, p


def search_tables(con, filters, tables=None, limit=25, offset=0,
                  order="score_desc"):
    """Fan-out search over measurement tables; merged + globally sorted.

    filters: verdict, min_score, max_score, tool, star, leg, chan,
             freq_min, freq_max (Hz), scan_contains, source_contains, text.
    Returns {rows, total, per_table, tables_searched, tables_skipped}.
    """
    tables = tables or SEARCHABLE_TABLES
    tables = [t for t in tables if t in _SEARCH_SPECS]
    per_table, skipped, merged = {}, [], []
    want = limit + offset
    for table in tables:
        spec = _SEARCH_SPECS[table]
        w, p = _build_where(table, spec, filters)
        if w is None:
            skipped.append(table)
            continue
        where = ("WHERE " + " AND ".join(w)) if w else ""
        n = con.execute(
            "SELECT COUNT(*) FROM %s t JOIN scans s ON s.scan_id=t.scan_id %s"
            % (table, where), p).fetchone()[0]
        per_table[table] = n
        if not n:
            continue
        score_sel = ("(%s) AS _score" % spec["score"]) if spec["score"] else "NULL AS _score"
        freq_sel = ("(%s) AS _freq" % spec["freq"]) if spec["freq"] else "NULL AS _freq"
        extra = list(spec["extra_cols"])
        vcol = spec.get("verdict")
        if vcol and not vcol.startswith("HITMAP:") and vcol not in extra:
            extra = extra + [vcol]  # verdict must ride along for display/filter echo
        cols = ["t.row_id", "s.report_dir", "t.source"] + \
            ["t." + c for c in extra]
        if spec.get("score"):
            order_col = "_score"
        else:
            order_col = "t.row_id"
        direction = "DESC" if order == "score_desc" else "ASC"
        # NULL scores always last regardless of direction
        nulls = "CASE WHEN _score IS NULL THEN 1 ELSE 0 END, "
        q = ("SELECT %s, %s, %s FROM %s t JOIN scans s ON s.scan_id=t.scan_id "
             "%s ORDER BY %s%s %s LIMIT ?"
             % (", ".join(cols), score_sel, freq_sel, table, where,
                nulls, order_col, direction))
        for r in con.execute(q, p + [want]):
            # sqlite Row keys are bare column names ('row_id', not 't.row_id')
            row = dict(r)
            scan, source = row.get("report_dir"), row.get("source")
            raw = {c: row.get(c) for c in extra}
            vcol = spec.get("verdict")
            if vcol and not vcol.startswith("HITMAP:"):
                verdict_val = row.get(vcol)
            elif vcol == "HITMAP:hit":
                verdict_val = "HIT" if row.get("hit") else "CLEAN"
            elif vcol == "HITMAP:detected":
                verdict_val = "HIT" if row.get("detected") else "CLEAN"
            else:
                verdict_val = row.get(vcol[7:]) if vcol else None
            merged.append({
                "table": table, "row_id": row.get("row_id"),
                "scan": scan, "source": source,
                "verdict": verdict_val,
                "score": row.get("_score"),
                "score_unit": spec["score_unit"],
                "freq_hz": row.get("_freq"),
                "raw": raw,
            })
    total = sum(per_table.values())
    reverse = (order == "score_desc")
    merged.sort(key=lambda r: (r["score"] is None,
                               -(r["score"] or 0) if reverse else (r["score"] or 0)))
    return {"rows": merged[offset:offset + limit], "total": total,
            "per_table": per_table, "tables_searched": sorted(per_table),
            "tables_skipped": skipped}


def describe_schema(con):
    """Tables + columns (+ views) for agent discovery."""
    tables = {}
    for (name,) in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            " ORDER BY name"):
        tables[name] = [r[1] for r in
                        con.execute("PRAGMA table_info(%s)" % name).fetchall()]
    views = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name").fetchall()]
    return {"tables": tables, "views": views,
            "searchable": SEARCHABLE_TABLES,
            "score_units": {t: _SEARCH_SPECS[t]["score_unit"] for t in SEARCHABLE_TABLES}}


def scan_info(con, report_dir):
    """One-scan dossier: counters, disposition, top hits, notes."""
    row = con.execute("SELECT * FROM scans WHERE report_dir=?",
                      (report_dir,)).fetchone()
    if row is None:
        # fuzzy: substring match
        rows = con.execute("SELECT report_dir FROM scans WHERE report_dir LIKE ?"
                           " ORDER BY report_dir",
                           ("%%%s%%" % report_dir,)).fetchall()
        return {"match": None,
                "candidates": [r[0] for r in rows]}
    scan_id = row["scan_id"]
    counts = {}
    for t in list(_SEARCH_SPECS) + ["stage_runs", "documents"]:
        try:
            counts[t] = con.execute("SELECT COUNT(*) FROM %s WHERE scan_id=?" % t,
                                    (scan_id,)).fetchone()[0]
        except Exception:
            pass
    top = search_tables(con, {}, tables=["evidence", "fam", "pulse", "frame"],
                        limit=10)
    # restrict merged rows to this scan (search fans out globally)
    top["rows"] = [r for r in top["rows"] if r["scan"] == report_dir][:10]
    notes = list_notes(con, target_type="scan", target_ref=report_dir)
    return {"match": dict(row), "counts": counts,
            "top_rows": top["rows"], "notes": notes}


def db_status(con, root):
    """Freshness: files on disk vs files ledger + db vitals."""
    import os
    root = Path(root)
    ledger = {r[0]: (r[1], r[2]) for r in
              con.execute("SELECT relpath, mtime, size FROM files").fetchall()}
    new, changed = [], []
    base = root / "reports"
    if base.exists():
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() not in (".csv", ".tsv", ".json"):
                continue
            rel = p.relative_to(root).as_posix()
            try:
                st = p.stat()
            except OSError:
                continue
            if rel not in ledger:
                if len(new) < 50:
                    new.append(rel)
            elif ledger[rel] != (st.st_mtime, st.st_size):
                if len(changed) < 50:
                    changed.append(rel)
    db_path = Path(con.execute("PRAGMA database_list").fetchone()[2])
    try:
        db_bytes = db_path.stat().st_size
    except OSError:
        db_bytes = None
    total_rows = con.execute(
        "SELECT SUM(n_rows) FROM scans").fetchone()[0] or 0
    last = con.execute(
        "SELECT MAX(ingested_at) FROM scans").fetchone()[0]
    return {"db_path": str(db_path), "db_bytes": db_bytes,
            "scans": con.execute("SELECT COUNT(*) FROM scans").fetchone()[0],
            "files_ledgered": len(ledger), "total_rows": total_rows,
            "last_ingested": last, "new_files": new,
            "n_new": len(new), "changed_files": changed, "n_changed": len(changed),
            "fresh": not new and not changed}


# ---------------------------------------------------------------------------
# analyst notes — the writable layer (measurements stay read-only)
# ---------------------------------------------------------------------------

_NOTES_DDL = """
CREATE TABLE IF NOT EXISTS analyst_notes (
  note_id     INTEGER PRIMARY KEY,
  created     TEXT DEFAULT (datetime('now')),
  target_type TEXT,     -- evidence_row | scan | source | general
  target_ref  TEXT,     -- row_id | report_dir | source path | free label
  note        TEXT,
  author      TEXT
);
"""

NOTE_TARGETS = ("evidence_row", "scan", "source", "general")


def add_note(con, target_type, target_ref, note, author=None):
    if target_type not in NOTE_TARGETS:
        raise ValueError("target_type must be one of %s" % (list(NOTE_TARGETS),))
    if not note or not note.strip():
        raise ValueError("note text is required")
    con.execute(_NOTES_DDL)
    cur = con.execute(
        "INSERT INTO analyst_notes(target_type, target_ref, note, author)"
        " VALUES(?,?,?,?)",
        (target_type, str(target_ref), note.strip(), author))
    con.commit()
    return cur.lastrowid


def list_notes(con, target_type=None, target_ref=None, limit=50):
    con.execute(_NOTES_DDL)
    q = "SELECT note_id, created, target_type, target_ref, note, author"
    q += " FROM analyst_notes"
    w, p = [], []
    if target_type:
        w.append("target_type = ?")
        p.append(target_type)
    if target_ref is not None:
        w.append("target_ref = ?")
        p.append(str(target_ref))
    if w:
        q += " WHERE " + " AND ".join(w)
    q += " ORDER BY note_id DESC LIMIT ?"
    p.append(limit)
    return [dict(r) for r in con.execute(q, p)]


def remove_note(con, note_id):
    con.execute(_NOTES_DDL)
    cur = con.execute("DELETE FROM analyst_notes WHERE note_id=?", (note_id,))
    con.commit()
    return cur.rowcount
