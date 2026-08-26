#!/usr/bin/env python3
from __future__ import annotations
import ctypes, hashlib, json, os, signal, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rep2_corrected_all_equal_y_Q.sing"
CLEAR = HERE / "FRESH_CLEARANCE.json"
ATT = HERE / "attempt_exact_q"
REF = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-modular-terminal-referee-2026-08-25"
PLAN = REF / "EXACT_Q_SAME_CHART_HELD_PLAN.json"
MOD = ROOT / "computations/unaudited-codex-n8-x5-rep2-corrected-all-equal-y-modular-held-2026-08-25/FINAL_MANIFEST.sha256"
SINGULAR = Path("/usr/local/Cellar/singular/4.4.1p5_3/bin/Singular")
GTIMEOUT = Path("/usr/local/Cellar/coreutils/9.11/bin/gtimeout")
PINS = {
    SOURCE: "5574a13572a1d68e60cffd97645b143123ee7fdf0c190861f63b796d2f0e1baf",
    PLAN: "f5f2942a59a810cacd369bc1d82cbafc663b579baf804148e488399ce95f9118",
    MOD: "61a0cce060ff20eba9fe2b3438f468a636ca97a92f41283c72da90aa39ef5415",
    REF / "FINAL_MANIFEST.sha256": "0409a7bccf9440470a6bc44f4a93b888f603509568c8a31055d8fb77eefbb84e",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}
NATIVE = 480
WRAPPER = 510
RSS_CAP_KIB = 8 * 1024 * 1024
PROC_PIDTASKINFO = 4

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def atomic(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("xb") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)

def atom_json(path: Path, value: object) -> None:
    atomic(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())

class Info(ctypes.Structure):
    _fields_ = [
        ("virtual_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64),
        ("total_user", ctypes.c_uint64), ("total_system", ctypes.c_uint64),
        ("threads_user", ctypes.c_uint64), ("threads_system", ctypes.c_uint64),
        ("policy", ctypes.c_int32), ("faults", ctypes.c_int32),
        ("pageins", ctypes.c_int32), ("cow_faults", ctypes.c_int32),
        ("messages_sent", ctypes.c_int32), ("messages_received", ctypes.c_int32),
        ("syscalls_mach", ctypes.c_int32), ("syscalls_unix", ctypes.c_int32),
        ("csw", ctypes.c_int32), ("threadnum", ctypes.c_int32),
        ("numrunning", ctypes.c_int32), ("priority", ctypes.c_int32),
    ]

LIB = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
LIST, PPATH, PINFO = LIB.proc_listpids, LIB.proc_pidpath, LIB.proc_pidinfo
LIST.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int]; LIST.restype = ctypes.c_int
PPATH.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]; PPATH.restype = ctypes.c_int
PINFO.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]; PINFO.restype = ctypes.c_int

def pids() -> list[int]:
    n = LIST(1, 0, None, 0); assert n > 0
    a = (ctypes.c_int * (n // 4 + 64))()
    got = LIST(1, 0, a, ctypes.sizeof(a)); assert got > 0
    return [x for x in a[:got // 4] if x > 0]

def pathname(pid: int) -> str:
    b = ctypes.create_string_buffer(4096)
    n = PPATH(pid, b, len(b))
    return b.value.decode(errors="replace") if n > 0 else ""

def census() -> dict:
    matches = []
    for pid in pids():
        if pid == os.getpid(): continue
        path = pathname(pid); base = Path(path).name.lower()
        if "singular" in base or "sparse_d12" in base:
            matches.append({"pid": pid, "path": path})
    return {"observer": "Darwin libproc", "matches": matches, "pass": not matches}

def group_rss(pgid: int) -> tuple[int, int]:
    total = members = 0
    for pid in pids():
        try:
            if os.getpgid(pid) != pgid: continue
        except (ProcessLookupError, PermissionError):
            continue
        info = Info(); size = ctypes.sizeof(info)
        if PINFO(pid, PROC_PIDTASKINFO, 0, ctypes.byref(info), size) == size:
            total += info.resident_size // 1024; members += 1
    if not members: raise OSError("no observable process-group member")
    return total, members

def terminate(proc: subprocess.Popen) -> None:
    try: os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError: return
    try: proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try: os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError: pass

for path, digest in PINS.items():
    assert sha(path) == digest, (path, sha(path), digest)
assert SOURCE.stat().st_size == 1861246 and not ATT.exists()
clearance = json.loads(CLEAR.read_text()); now = time.time()
assert clearance["schema"] == "KRENN_X5_REP2_SAME_CHART_EXACT_Q_CLEARANCE_V1"
assert clearance["status"] == "EXPLICIT_MANAGER_AND_RESOURCE_CLEARANCE"
assert clearance["plan_sha256"] == PINS[PLAN] and clearance["source_sha256"] == PINS[SOURCE]
assert all(clearance[k] is True for k in ("manager_clearance", "resource_clearance", "no_overlap_confirmed", "launch_exactly_once"))
assert len(clearance["nonce"]) >= 16
assert clearance["issued_unix_seconds"] <= now <= clearance["expires_unix_seconds"]
assert clearance["expires_unix_seconds"] - clearance["issued_unix_seconds"] <= 900

ATT.mkdir()
preflight = census()
atom_json(ATT / "preflight.json", {
    "schema": "KRENN_X5_REP2_SAME_CHART_EXACT_Q_PREFLIGHT_V1",
    "clearance_sha256": sha(CLEAR), "census": preflight,
})
if not preflight["pass"]:
    atom_json(ATT / "result.json", {"schema": "KRENN_X5_REP2_SAME_CHART_EXACT_Q_RESULT_V1", "status": "STOPPED_COMPETING_PROCESS_ZERO_ARITHMETIC"})
    raise SystemExit(2)
atomic(ATT / SOURCE.name, SOURCE.read_bytes())
assert sha(ATT / SOURCE.name) == PINS[SOURCE]

outtmp, errtmp = ATT / "stdout.log.tmp", ATT / "stderr.log.tmp"
started = time.monotonic(); samples = []; breach = None
with outtmp.open("xb") as out, errtmp.open("xb") as err:
    proc = subprocess.Popen(
        [str(GTIMEOUT), "--signal=TERM", "--kill-after=10", str(NATIVE), str(SINGULAR), "-q", str(ATT / SOURCE.name)],
        stdout=out, stderr=err, start_new_session=True,
    )
    while proc.poll() is None:
        elapsed = time.monotonic() - started
        try: rss, members = group_rss(proc.pid)
        except OSError:
            try: proc.wait(timeout=.5); break
            except subprocess.TimeoutExpired: breach = "RSS_OBSERVER_FAILURE"; terminate(proc); break
        samples.append({"elapsed_seconds": round(elapsed, 6), "rss_kib": rss, "members": members})
        if rss >= RSS_CAP_KIB: breach = "RSS_CAP"; terminate(proc); break
        if elapsed >= WRAPPER: breach = "WRAPPER_WALL_CAP"; terminate(proc); break
        time.sleep(.25)
    returncode = proc.wait(); out.flush(); os.fsync(out.fileno()); err.flush(); os.fsync(err.fileno())
os.replace(outtmp, ATT / "stdout.log"); os.replace(errtmp, ATT / "stderr.log")
if breach is None and returncode == 124: breach = "NATIVE_WALL_CAP"
elif breach is None and returncode != 0: breach = "SINGULAR_NONZERO"
parsed = {}
for line in (ATT / "stdout.log").read_text(errors="replace").splitlines():
    if "=" not in line: continue
    key, value = line.split("=", 1)
    if key in {"INPUT_VARIABLES", "INPUT_GENERATORS", "GROEBNER_SIZE", "UNIT_REMAINDER", "STATUS"}: parsed[key] = value
expected = {"INPUT_VARIABLES": "91", "INPUT_GENERATORS": "6577", "GROEBNER_SIZE": "1", "UNIT_REMAINDER": "0", "STATUS": "UNIT_IDEAL"}
unit = breach is None and returncode == 0 and parsed == expected
watchdog = {
    "schema": "KRENN_X5_REP2_SAME_CHART_EXACT_Q_WATCHDOG_V1",
    "status": "PASS" if breach is None else "TERMINAL_FAILURE", "elapsed_seconds": round(time.monotonic() - started, 6),
    "returncode": returncode, "breach": breach, "native_wall_seconds": NATIVE, "wrapper_wall_seconds": WRAPPER,
    "rss_limit_kib": RSS_CAP_KIB, "peak_rss_kib": max((x["rss_kib"] for x in samples), default=None), "samples": samples,
    "stdout_sha256": sha(ATT / "stdout.log"), "stderr_sha256": sha(ATT / "stderr.log"),
    "logs_atomic": not outtmp.exists() and not errtmp.exists(), "automatic_relaunch": False, "second_lane": False,
}
atom_json(ATT / "watchdog.json", watchdog)
result = {
    "schema": "KRENN_X5_REP2_SAME_CHART_EXACT_Q_RESULT_V1",
    "status": "UNIT_IDEAL_EXACT_Q_REP2_SAME_CHART" if unit else "TERMINAL_NONUNIT_OR_FAILURE",
    "field": "Q", "chart": "all-equal-y/i0/p00/x0/y0/d01", "source_sha256": sha(ATT / SOURCE.name),
    "source_bytes": SOURCE.stat().st_size, "parsed_stdout": parsed, "returncode": returncode, "breach": breach,
    "unit_ideal": unit, "same_chart_closed": unit, "rep2_closed": False, "family_closed": False,
    "automatic_relaunch": False, "second_lane": False, "preflight_sha256": sha(ATT / "preflight.json"),
    "watchdog_sha256": sha(ATT / "watchdog.json"),
}
atom_json(ATT / "result.json", result)
print(json.dumps({"status": result["status"], "result_sha256": sha(ATT / "result.json")}, sort_keys=True))
raise SystemExit(0 if unit else 1)
