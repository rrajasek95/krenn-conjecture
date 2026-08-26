#!/usr/bin/env python3
"""Run the one independently approved rep1 guard-minor modular diagnostic."""
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
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-referee-2026-08-25"
SOURCE = PRODUCER / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing"
SINGULAR = Path("/usr/local/bin/Singular")
PINS = {
    PRODUCER / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    SOURCE: "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49",
    REFEREE / "FINAL_MANIFEST.sha256": "16226d5f15d9f0d2d419095ec3842a7122ad77b40c1abe83bc9afe1b45b7800c",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}
NATIVE_WALL = 300
RSS_CAP = 8 * 1024**3


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64),
        ("system_time", ctypes.c_uint64), ("pkg_idle_wkups", ctypes.c_uint64),
        ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64),
        ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64),
        ("phys_footprint", ctypes.c_uint64), ("proc_start_abstime", ctypes.c_uint64),
        ("proc_exit_abstime", ctypes.c_uint64), ("child_user_time", ctypes.c_uint64),
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
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
assert not (HERE / "result.json").exists(), "fresh atomic output required"

started = time.monotonic()
process = subprocess.Popen([str(SINGULAR), str(SOURCE)], cwd=HERE, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           start_new_session=True)
print(json.dumps({"event": "STARTED", "singular_pid": process.pid}), flush=True)
peak = 0
termination = None
while process.poll() is None:
    peak = max(peak, rss_bytes(process.pid))
    elapsed = time.monotonic() - started
    if peak > RSS_CAP:
        termination = "RSS_CAP_8GIB"
    elif elapsed > NATIVE_WALL:
        termination = "NATIVE_WALL_CAP_300"
    if termination:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        time.sleep(0.2)
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        break
    time.sleep(0.1)

stdout, stderr = process.communicate()
wall = time.monotonic() - started
unit = termination is None and process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout and "UNIT_REMAINDER=0" in stdout
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status = ("UNIT_IDEAL_MODULAR_DIAGNOSTIC" if unit else
          "NONUNIT_MODULAR_DIAGNOSTIC" if nonunit else
          "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS")
result = {
    "schema": "KRENN_X5_REP1_GUARD_MINOR_ONE_LANE_DIAGNOSTIC_V1",
    "status": status,
    "mathematical_coverage": False,
    "diagnostic_only": True,
    "chart": "all-equal-y/i0/p00/x0/y0/d01",
    "field": "F_32003",
    "native_wall_cap_seconds": NATIVE_WALL,
    "wrapper_wall_cap_seconds": 310,
    "rss_cap_bytes": RSS_CAP,
    "wall_seconds": wall,
    "observed_peak_rss_bytes": peak,
    "termination": termination,
    "returncode": process.returncode,
    "pins": {str(path): digest for path, digest in PINS.items()},
    "stdout": stdout,
    "stderr": stderr,
    "second_lane_launched": False,
    "exact_Q_launched": False,
}
atomic_json(HERE / "result.json", result)
print(json.dumps({"event": "TERMINAL", "status": status, "wall": wall, "peak": peak}, sort_keys=True))
