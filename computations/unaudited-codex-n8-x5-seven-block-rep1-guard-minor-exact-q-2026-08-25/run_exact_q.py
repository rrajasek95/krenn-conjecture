#!/usr/bin/env python3
"""Materialize and run the one independently approved exact-Q rep1 chart."""
import ctypes, hashlib, json, os, signal, subprocess, time
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
MODULAR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-diagnostic-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-diagnostic-referee-2026-08-25"
SOURCE_P = PRODUCER / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing"
SOURCE_Q = HERE / "rep1_minor_i0_p00_x0_y0_d01_Q.sing"
SINGULAR = Path("/usr/local/bin/Singular")
PINS = {
    PRODUCER / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    SOURCE_P: "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49",
    MODULAR / "MANIFEST.sha256": "df0964395da2742bf1df6cd322dcdbe7e5d13113d0c8967b12176e5ed2a98351",
    MODULAR / "result.json": "24edfc0c4680b57d0ec7ea0df62485ceb9f08062ff6153ed608839cdf988766c",
    REFEREE / "EXACT_Q_HELD_PLAN.json": "a7841d169a1d07c43785eaf498b502f2aff54b4745646173756ab47ea74551fd",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}
EXPECTED_Q = "53f741ca9173877ef1bc21dba2546a82102a32140221068de1301d0b4635dadb"
NATIVE_WALL, RSS_CAP = 240, 8 * 1024**3


class RUsageInfoV2(ctypes.Structure):
    _fields_ = [
        ("uuid", ctypes.c_uint8 * 16), ("user_time", ctypes.c_uint64), ("system_time", ctypes.c_uint64),
        ("pkg_idle_wkups", ctypes.c_uint64), ("interrupt_wkups", ctypes.c_uint64), ("pageins", ctypes.c_uint64),
        ("wired_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64), ("phys_footprint", ctypes.c_uint64),
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
    return record.resident_size if LIBPROC.proc_pid_rusage(pid, 2, ctypes.byref(record)) == 0 else 0


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20): h.update(chunk)
    return h.hexdigest()


def atomic_text(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(value); os.replace(tmp, path)


def atomic_json(path, value):
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
assert not (HERE / "result.json").exists(), "fresh result required"
source = SOURCE_P.read_text()
assert source.count("ring r=32003,") == 1 and "ring r=0," not in source
source_q = source.replace("ring r=32003,", "ring r=0,", 1)
assert hashlib.sha256(source_q.encode()).hexdigest() == EXPECTED_Q
atomic_text(SOURCE_Q, source_q)
assert sha256(SOURCE_Q) == EXPECTED_Q

started = time.monotonic()
process = subprocess.Popen([str(SINGULAR), str(SOURCE_Q)], cwd=HERE, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
print(json.dumps({"event":"STARTED","singular_pid":process.pid}), flush=True)
peak, termination = 0, None
while process.poll() is None:
    peak = max(peak, rss_bytes(process.pid)); elapsed = time.monotonic() - started
    if peak > RSS_CAP: termination = "RSS_CAP_8GIB"
    elif elapsed > NATIVE_WALL: termination = "NATIVE_WALL_CAP_240"
    if termination:
        try: os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        time.sleep(0.2)
        if process.poll() is None:
            try: os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError: pass
        break
    time.sleep(0.1)
stdout, stderr = process.communicate(); wall = time.monotonic() - started
unit = termination is None and process.returncode == 0 and all(token in stdout for token in
       ("INPUT_GENERATORS=6577", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"))
nonunit = termination is None and process.returncode == 0 and "STATUS=NONUNIT_OR_UNRESOLVED" in stdout
status = ("UNIT_IDEAL_EXACT_Q_LOCALIZED_CHART" if unit else "NONUNIT_EXACT_Q_DIAGNOSTIC" if nonunit else
          "FAIL_CLOSED_RESOURCE_GATE" if termination else "FAIL_CLOSED_PROCESS")
result = {
    "schema":"KRENN_X5_REP1_GUARD_MINOR_EXACT_Q_ONE_LANE_V1", "status":status,
    "localized_chart_closed":unit, "representative_closed":False,
    "chart":"all-equal-y/i0/p00/x0/y0/d01", "field":"Q",
    "native_wall_cap_seconds":240, "wrapper_wall_cap_seconds":250, "rss_cap_bytes":RSS_CAP,
    "wall_seconds":wall, "observed_peak_rss_bytes":peak, "termination":termination,
    "returncode":process.returncode, "source_Q_sha256":EXPECTED_Q,
    "pins":{str(path):digest for path,digest in PINS.items()}, "stdout":stdout, "stderr":stderr,
    "second_lane_launched":False, "modular_relaunch":False, "automatic_relaunch":False,
  }
atomic_json(HERE / "result.json", result)
print(json.dumps({"event":"TERMINAL","status":status,"wall":wall,"peak":peak},sort_keys=True))
