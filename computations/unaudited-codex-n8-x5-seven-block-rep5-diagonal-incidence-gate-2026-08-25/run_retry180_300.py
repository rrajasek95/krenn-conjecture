#!/usr/bin/env python3
"""One resource-only rep5 retry: modular 180/190, Q 300/310, RSS 8 GiB."""

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
SEALED_MANIFEST_SHA = "4651d21012e34a6237edc3d8fcf391185b6d7422d345a079e2b873952b5c57e4"
SEALED_FAILURE_SHA = "1572f7573f8fab7a907ad2aefd52e0c1c6596461878a4c0bfc9f9dc4ad7c2c94"
SEALED_METADATA_SHA = "e34d3650a7d60121882c55884b7ded9654089f10bda8a2212ef9c2cc62723712"


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


def run_one(metadata, chart, label):
    native = 180 if label == "p32003" else 300
    wrapper = 190 if label == "p32003" else 310
    source_record = metadata["inputs"][chart][label]
    source = HERE / source_record["path"]
    assert sha256(source) == source_record["sha256"]
    started = time.monotonic()
    process = subprocess.Popen(
        ["/usr/local/bin/gtimeout", str(wrapper), "/usr/local/bin/Singular", source.name],
        cwd=HERE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    peak = 0
    termination = None
    while process.poll() is None:
        elapsed = time.monotonic() - started
        # gtimeout is the direct process; Singular is its child. proc_pid_rusage
        # on the group leader may undercount, so sum the process-group RSS via ps.
        ps = subprocess.run(["ps", "-o", "rss=", "-g", str(process.pid)], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
        group_rss = sum(int(item) for item in ps.stdout.split() if item.isdigit()) * 1024
        peak = max(peak, group_rss, rss_bytes(process.pid))
        if peak > RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif elapsed > native:
            termination = f"NATIVE_WALL_CAP_{native}"
        if termination:
            try: os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError: pass
            break
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    unit = termination is None and process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout
    nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    if unit:
        status = "UNIT_IDEAL_MODULAR" if label == "p32003" else "UNIT_IDEAL_EXACT_Q"
    elif nonunit:
        status = "NONUNIT_DIAGNOSTIC"
    else:
        status = "FAIL_CLOSED_RESOURCE_GATE" if termination or process.returncode == 124 else "FAIL_CLOSED_PROCESS"
    result = {
        "schema": "KRENN_X5_REP5_DIAGONAL_INCIDENCE_RETRY_V1",
        "status": status, "mathematical_coverage": unit, "chart": chart, "ring": label,
        "native_wall_cap_seconds": native, "wrapper_wall_cap_seconds": wrapper,
        "wall_seconds": wall, "rss_cap_bytes": RSS_CAP, "observed_peak_rss_bytes": peak,
        "termination": termination if termination else "WRAPPER_WALL_CAP" if process.returncode == 124 else None,
        "returncode": process.returncode, "input_sha256": source_record["sha256"],
        "sealed_failure_manifest_sha256": SEALED_MANIFEST_SHA,
        "stdout": stdout, "stderr": stderr,
    }
    atomic_json(HERE / f"results_retry_{label}_{chart}.json", result)
    print(json.dumps({"chart": chart, "ring": label, "status": status, "wall": wall, "peak": peak}, sort_keys=True), flush=True)
    return unit


def main():
    assert sha256(HERE / "MANIFEST.sha256") == SEALED_MANIFEST_SHA
    assert sha256(HERE / "results_p32003_p00.json") == SEALED_FAILURE_SHA
    assert sha256(HERE / "gate_metadata.json") == SEALED_METADATA_SHA
    previous = json.loads((HERE / "results_p32003_p00.json").read_text())
    assert previous["status"] == "FAIL_CLOSED_RESOURCE_GATE" and previous["mathematical_coverage"] is False
    metadata = json.loads((HERE / "gate_metadata.json").read_text())
    for chart in CHARTS:
        if not run_one(metadata, chart, "p32003"):
            raise SystemExit(f"fail closed at modular {chart}")
        if not run_one(metadata, chart, "Q"):
            raise SystemExit(f"fail closed at Q {chart}")


if __name__ == "__main__":
    main()
