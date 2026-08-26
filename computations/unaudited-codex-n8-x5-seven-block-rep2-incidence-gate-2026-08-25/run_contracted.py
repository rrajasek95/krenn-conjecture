#!/usr/bin/env python3
"""Hard-watched modular runner for an exact contracted rep2 incidence stage."""

from __future__ import annotations

import argparse
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
METADATA = HERE / "rep2_contracted_incidence_metadata.json"
NATIVE_WALL_SECONDS = 30
RSS_CAP_BYTES = 8 * (1 << 30)


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


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def terminate_group(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("pure", "distinguished"), required=True)
    args = parser.parse_args()
    metadata = json.loads(METADATA.read_text())
    source_record = metadata["inputs"][args.stage]["block"]
    source = HERE / source_record["path"]
    assert sha256(source) == source_record["sha256"]
    output = HERE / f"results_rep2_contracted_{args.stage}_block_p32003.json"
    assert not output.exists()
    started = time.monotonic()
    process = subprocess.Popen(
        ["Singular", "-q", str(source)], text=True,
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
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    unit = process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout
    nonunit = process.returncode == 0 and "STATUS=NONUNIT_CONTRACTED_SUBSET" in stdout
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_CONTRACTED_RUN_V1",
        "status": "PASS_MODULAR_UNIT_DIAGNOSTIC" if unit else "TERMINAL_NONUNIT_DIAGNOSTIC" if nonunit else "INCOMPLETE_RESOURCE_GATE",
        "stage": args.stage, "ordering": "block", "ring": "p32003",
        "input_sha256": source_record["sha256"], "native_wall_seconds": NATIVE_WALL_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES, "observed_peak_rss_bytes": peak_rss,
        "wall_seconds": time.monotonic() - started, "returncode": process.returncode,
        "termination": termination, "stdout": stdout, "stderr": stderr,
        "unit_ideal": unit, "mathematical_coverage": False,
    }
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({key: result[key] for key in ("status", "stage", "wall_seconds", "observed_peak_rss_bytes", "termination")}, sort_keys=True))


if __name__ == "__main__":
    main()
