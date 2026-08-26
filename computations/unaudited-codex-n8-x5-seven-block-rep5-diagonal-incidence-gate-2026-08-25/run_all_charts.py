#!/usr/bin/env python3
"""Sequential modular then exact-Q runner for all five rep5 incidence charts."""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
CHARTS = ("p00", "p01", "p10", "p11", "p12")
RSS_CAP = 8 * 1024**3


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64),
        ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64),
        ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64),
        ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64),
        ("child_system_time", ctypes.c_uint64), ("child_pkg_idle_wkups", ctypes.c_uint64), ("child_interrupt_wkups", ctypes.c_uint64),
        ("child_pageins", ctypes.c_uint64), ("child_elapsed_abstime", ctypes.c_uint64), ("diskio_bytesread", ctypes.c_uint64),
        ("diskio_byteswritten", ctypes.c_uint64),
    ]


LIBPROC = ctypes.CDLL("/usr/lib/libproc.dylib")
LIBPROC.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIBPROC.proc_pid_rusage.restype = ctypes.c_int


def rss_bytes(pid):
    record = RUsageInfoV2()
    return record.resident_size if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) == 0 else 0


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def run_one(chart, label, wall_cap):
    metadata = json.loads((HERE / "gate_metadata.json").read_text())
    source_record = metadata["inputs"][chart][label]
    source = HERE / source_record["path"]
    assert sha256(source) == source_record["sha256"]
    started = time.monotonic()
    process = subprocess.Popen(["/usr/local/bin/Singular", source.name], cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    peak = 0
    termination = None
    while process.poll() is None:
        elapsed = time.monotonic() - started
        peak = max(peak, rss_bytes(process.pid))
        if peak > RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif elapsed > wall_cap:
            termination = f"WALL_CAP_{wall_cap}"
        if termination:
            try: os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError: pass
            break
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    unit = termination is None and process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout
    nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    status = ("UNIT_IDEAL_MODULAR" if label == "p32003" else "UNIT_IDEAL_EXACT_Q") if unit else "NONUNIT_DIAGNOSTIC" if nonunit else "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS"
    result = {"schema": "KRENN_X5_REP5_DIAGONAL_INCIDENCE_RUN_V1", "status": status, "mathematical_coverage": unit, "chart": chart, "ring": label, "wall_seconds": wall, "wall_cap_seconds": wall_cap, "rss_cap_bytes": RSS_CAP, "observed_peak_rss_bytes": peak, "termination": termination, "returncode": process.returncode, "input_sha256": source_record["sha256"], "stdout": stdout, "stderr": stderr}
    atomic_json(HERE / f"results_{label}_{chart}.json", result)
    print(json.dumps({"chart": chart, "ring": label, "status": status, "wall": wall, "peak": peak}, sort_keys=True), flush=True)
    return unit


def main():
    for chart in CHARTS:
        if not run_one(chart, "p32003", 60):
            raise SystemExit(f"fail closed at modular {chart}")
        if not run_one(chart, "Q", 120):
            raise SystemExit(f"fail closed at Q {chart}")


if __name__ == "__main__":
    main()
