#!/usr/bin/env python3
"""One authorized exact-Q retry with native wall/RSS watchdogs and distinct output."""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rep2_rank1_Q.sing"
OUTPUT = HERE / "results_rep2_rank1_Q_retry300.json"
SOURCE_SHA256 = "5c5d29c4e06611c469a3fd1cafdc59f83698f1256e670fa683e6b1bf84cdf631"
SINGULAR = Path("/usr/local/bin/Singular")
SINGULAR_SHA256 = "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88"
NATIVE_WALL_SECONDS = 300
RSS_CAP_BYTES = 8 * (1 << 30)
EXPECTED_STDOUT = "INPUT_GENERATORS=6582\nGROEBNER_SIZE=1\nUNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


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


def rss_bytes(pid):
    record = RUsageInfoV2()
    status = LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record))
    return record.resident_size if status == 0 else 0


def terminate_group(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass


def main():
    assert sha256(SOURCE) == SOURCE_SHA256
    assert sha256(SINGULAR) == SINGULAR_SHA256
    assert not OUTPUT.exists(), "distinct retry output already exists"
    started = time.monotonic()
    process = subprocess.Popen(
        [str(SINGULAR), "-q", str(SOURCE)], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    peak_rss = 0
    termination = None
    while process.poll() is None:
        elapsed = time.monotonic() - started
        observed = rss_bytes(process.pid)
        peak_rss = max(peak_rss, observed)
        if observed > RSS_CAP_BYTES:
            termination = "RSS_CAP"
            terminate_group(process)
            break
        if elapsed > NATIVE_WALL_SECONDS:
            termination = "NATIVE_WALL_CAP"
            terminate_group(process)
            break
        time.sleep(0.2)
    stdout, stderr = process.communicate()
    elapsed = time.monotonic() - started
    unit = process.returncode == 0 and stdout == EXPECTED_STDOUT
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_RANK1_Q_RETRY300_V1",
        "status": "PASS_RATIONAL_UNIT_IDEAL" if unit else "INCOMPLETE_RESOURCE_GATE",
        "representative_id": 2,
        "rank_branch": "rank_le_one",
        "ring": "Q",
        "algorithm": "slimgb",
        "input_sha256": SOURCE_SHA256,
        "singular_sha256": SINGULAR_SHA256,
        "supersedes_failure": False,
        "preserved_timeout120_sha256": "c254b996535894c0948f1918e739aba8e362b9e6e0d3835a0c089423214cd90b",
        "native_wall_seconds": NATIVE_WALL_SECONDS,
        "wrapper_wall_seconds": 310,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "rss_enforcement": "live libproc proc_pid_rusage resident_size; SIGTERM process group above 8GiB",
        "observed_peak_rss_bytes": peak_rss,
        "wall_seconds": elapsed,
        "returncode": process.returncode,
        "termination": termination,
        "stdout": stdout,
        "stderr": stderr,
        "unit_ideal": unit,
        "mathematical_coverage": unit,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, OUTPUT)
    print(json.dumps({key: result[key] for key in (
        "status", "wall_seconds", "observed_peak_rss_bytes", "returncode", "termination", "unit_ideal"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
