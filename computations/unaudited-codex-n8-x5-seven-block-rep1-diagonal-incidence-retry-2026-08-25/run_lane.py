#!/usr/bin/env python3
"""Run one byte-identical rep1 incidence lane with direct libproc RSS accounting."""

from __future__ import annotations

import argparse
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
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-diagonal-incidence-gate-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "36e39752896a052d8bfe75af29c39c4d8c09c090afb8a9692e818a63c9a811bf",
    PARENT / "results_modular_p00.json": "119d02ac5ea337303f34b9b4285821305169e7d9420cf976521c0b645ef936b3",
    PARENT / "gate_metadata.json": "97342352d9162253c0c27aefdeba81f25b1265751e4c29daf706f828f4c9572e",
}
CHARTS = ("p00", "p01", "p10", "p11", "p12")
RSS_CAP = 8 * 1024**3


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64),
        ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64),
        ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64),
        ("proc_start_abstime", ctypes.c_uint64), ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64),
        ("child_system_time", ctypes.c_uint64), ("child_pkg_idle_wkups", ctypes.c_uint64),
        ("child_interrupt_wkups", ctypes.c_uint64), ("child_pageins", ctypes.c_uint64),
        ("child_elapsed_abstime", ctypes.c_uint64), ("diskio_bytesread", ctypes.c_uint64),
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


def require_predecessor(chart, label):
    index = CHARTS.index(chart)
    if label == "Q":
        path = HERE / f"results_{chart}_p32003.json"
        expected = "UNIT_IDEAL_MODULAR"
    elif index:
        path = HERE / f"results_{CHARTS[index - 1]}_Q.json"
        expected = "UNIT_IDEAL_EXACT_Q"
    else:
        return
    record = json.loads(path.read_text())
    assert record["status"] == expected and record["mathematical_coverage"] is True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chart", choices=CHARTS)
    parser.add_argument("label", choices=("p32003", "Q"))
    args = parser.parse_args()
    for path, expected in PINS.items():
        assert sha256(path) == expected
    old = json.loads((PARENT / "results_modular_p00.json").read_text())
    assert old["status"] == "FAIL_CLOSED_RESOURCE_GATE" and old["termination"] == "WALL_CAP_60"
    assert old["mathematical_coverage"] is False and old["Q_launched"] is False
    require_predecessor(args.chart, args.label)

    metadata = json.loads((PARENT / "gate_metadata.json").read_text())
    source_record = metadata["inputs"][args.chart][args.label]
    source = PARENT / source_record["path"]
    assert sha256(source) == source_record["sha256"]
    native_wall = 180 if args.label == "p32003" else 300
    wrapper_wall = native_wall + 10

    started = time.monotonic()
    process = subprocess.Popen(
        ["/usr/local/bin/Singular", str(source)], cwd=HERE, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    peak = 0
    termination = None
    while process.poll() is None:
        elapsed = time.monotonic() - started
        peak = max(peak, rss_bytes(process.pid))
        if peak > RSS_CAP:
            termination = "RSS_CAP_8GIB"
        elif elapsed > native_wall:
            termination = f"NATIVE_WALL_CAP_{native_wall}"
        if termination:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            break
        time.sleep(0.1)
    stdout, stderr = process.communicate()
    wall = time.monotonic() - started
    unit = termination is None and process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout
    nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
    if unit:
        status = "UNIT_IDEAL_MODULAR" if args.label == "p32003" else "UNIT_IDEAL_EXACT_Q"
    elif nonunit:
        status = "NONUNIT_DIAGNOSTIC"
    elif termination:
        status = "FAIL_CLOSED_RESOURCE_GATE"
    else:
        status = "FAIL_CLOSED_PROCESS"
    result = {
        "schema": "KRENN_X5_REP1_DIAGONAL_INCIDENCE_RETRY_LANE_V1",
        "status": status,
        "mathematical_coverage": unit,
        "chart": args.chart,
        "ring": args.label,
        "native_wall_cap_seconds": native_wall,
        "wrapper_wall_cap_seconds": wrapper_wall,
        "rss_cap_bytes": RSS_CAP,
        "wall_seconds": wall,
        "observed_peak_rss_bytes": peak,
        "termination": termination,
        "returncode": process.returncode,
        "input_path": str(source.relative_to(ROOT)),
        "input_sha256": source_record["sha256"],
        "sealed_60s_failure_manifest_sha256": PINS[PARENT / "MANIFEST.sha256"],
        "sealed_60s_failure_result_sha256": PINS[PARENT / "results_modular_p00.json"],
        "stdout": stdout,
        "stderr": stderr,
    }
    atomic_json(HERE / f"results_{args.chart}_{args.label}.json", result)
    print(json.dumps({"chart": args.chart, "ring": args.label, "status": status, "wall": wall, "peak": peak}, sort_keys=True))
    if not unit:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
