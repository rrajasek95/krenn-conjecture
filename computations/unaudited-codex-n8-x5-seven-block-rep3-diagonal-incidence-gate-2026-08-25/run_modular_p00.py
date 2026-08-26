#!/usr/bin/env python3
"""Run exactly the rep3 e0/A37[00] modular incidence gate fail closed."""

from __future__ import annotations

import hashlib
import json
import os
import ctypes
import signal
import subprocess
import time
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
INPUT = HERE / "rep3_e0_p00_p32003.sing"
RSS_CAP = 8 * 1024**3


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16),
        ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64),
        ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64),
        ("pageins", ctypes.c_uint64), ("wired_size", ctypes.c_uint64),
        ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64),
        ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64),
        ("child_user_time", ctypes.c_uint64), ("child_system_time", ctypes.c_uint64),
        ("child_pkg_idle_wkups", ctypes.c_uint64), ("child_interrupt_wkups", ctypes.c_uint64),
        ("child_pageins", ctypes.c_uint64), ("child_elapsed_abstime", ctypes.c_uint64),
        ("diskio_bytesread", ctypes.c_uint64), ("diskio_byteswritten", ctypes.c_uint64),
    ]


LIBPROC = ctypes.CDLL("/usr/lib/libproc.dylib")
LIBPROC.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
LIBPROC.proc_pid_rusage.restype = ctypes.c_int


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def rss_bytes(pid):
    record = RUsageInfoV2()
    return record.resident_size if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) == 0 else 0


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    metadata = json.loads((HERE / "gate_metadata.json").read_text())
    expected = metadata["inputs"]["p00"]["p32003"]["sha256"]
    assert sha256(INPUT) == expected
    started = time.monotonic()
    process = subprocess.Popen(
        ["/usr/local/bin/Singular", INPUT.name], cwd=HERE, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    peak_rss = 0
    termination = None
    while process.poll() is None:
        wall = time.monotonic() - started
        observed = rss_bytes(process.pid)
        peak_rss = max(peak_rss, observed)
        if observed > RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif wall > 60:
            termination = "WALL_CAP_60"
        if termination:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            break
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    returncode = process.returncode
    if termination:
        status, coverage = "FAIL_CLOSED_RESOURCE_GATE", False
    elif returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout:
        status, coverage = "UNIT_IDEAL_MODULAR", True
    elif returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout:
        status, coverage = "NONUNIT_MODULAR_DIAGNOSTIC", False
    else:
        status, coverage = "FAIL_CLOSED_PROCESS", False
    result = {
        "schema": "KRENN_X5_REP3_DIAGONAL_INCIDENCE_MODULAR_P00_V1",
        "status": status,
        "mathematical_coverage": coverage,
        "ring": "p32003",
        "chart": {"coordinate": 0, "nonzero_outside_entry": "A37[0,0]"},
        "wall_seconds": wall,
        "rss_cap_bytes": RSS_CAP,
        "observed_peak_rss_bytes": peak_rss,
        "termination": termination,
        "returncode": returncode,
        "input_sha256": expected,
        "stdout": stdout,
        "stderr": stderr,
        "Q_launched": False,
    }
    atomic_json(HERE / "results_modular_p00.json", result)
    print(json.dumps({"status": status, "wall_seconds": wall, "Q_launched": False}, sort_keys=True))


if __name__ == "__main__":
    main()
