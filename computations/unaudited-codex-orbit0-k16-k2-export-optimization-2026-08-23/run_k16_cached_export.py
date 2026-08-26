#!/usr/bin/env python3
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path("computations/unaudited-codex-orbit0-k16-k2-export-optimization-2026-08-23")
OUT = Path("computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23")
SHARDS = OUT / "shards"
BIN = ROOT / "export_k16_cached_profiles"
SRC = ROOT / "export_k16_cached_profiles.rs"
N = 24_097_095
NSHARD = 64
WORKERS = 8
KEY_CAP = 250_000
STOP_SCHEDULING = 450.0
HARD_GATE = 600.0
RSS_LIMIT_KIB = 16 * 1024 * 1024
FREE_FLOOR = 32 * 1024**3


def sha(path, chunk=8 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                return h.hexdigest()
            h.update(b)


def atomic_json(path, obj):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def ranges():
    return [(i, N * i // NSHARD, N * (i + 1) // NSHARD) for i in range(NSHARD)]


def prefix(i):
    return SHARDS / f"shard_{i:02d}_attempt_0"


def accepted_path(i):
    return SHARDS / f"shard_{i:02d}.accepted.json"


def validate_accepted(i, lo, hi):
    p = accepted_path(i)
    if not p.exists():
        return None
    try:
        x = json.loads(p.read_text())
        assert x["status"] == "PASS_ACCEPTED_K16_CACHED_SHARD"
        assert x["shard"] == i and x["source_range"] == [lo, hi]
        assert x["source_sha256"] == sha(SRC) and x["binary_sha256"] == sha(BIN)
        assert x["kernel_sha256"] == sha(x["kernel_path"])
        for q in x["part_files"]:
            assert os.path.getsize(q["path"]) == q["bytes"]
            assert sha(q["path"]) == q["sha256"]
        return x
    except Exception:
        return None


def validate_finished_shard(i, lo, hi):
    pre = prefix(i)
    kernel_path = Path(str(pre) + ".kernel.json")
    k = json.loads(kernel_path.read_text())
    assert k["status"] == "PASS_COMPLETE_K16_CACHED_SHARD"
    assert k["source_range"] == [lo, hi]
    assert k["source_rows"] == hi - lo
    parts = k["parts"]
    verify = subprocess.run(
        [str(BIN), "verify", str(lo), str(hi), str(parts), str(pre)],
        text=True, capture_output=True, check=True,
    )
    verify_path = Path(str(pre) + ".verify.txt")
    verify_path.write_text(verify.stdout)
    files = []
    for part in range(parts):
        p = Path(f"{pre}.part{part:06d}.bin")
        files.append({"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)})
    x = {
        "status": "PASS_ACCEPTED_K16_CACHED_SHARD",
        "shard": i,
        "source_range": [lo, hi],
        "source_sha256": sha(SRC),
        "binary_sha256": sha(BIN),
        "kernel_path": str(kernel_path),
        "kernel_sha256": sha(kernel_path),
        "verify_path": str(verify_path),
        "verify_sha256": sha(verify_path),
        "kernel": k,
        "part_files": files,
        "part_bytes": sum(q["bytes"] for q in files),
    }
    atomic_json(accepted_path(i), x)
    return x


def launch(i, lo, hi):
    pre = prefix(i)
    for suffix in (".kernel.json", ".verify.txt"):
        if Path(str(pre) + suffix).exists():
            raise RuntimeError(f"orphan output blocks fresh shard {i}: {pre}{suffix}")
    if list(SHARDS.glob(pre.name + ".part*.bin")) or list(SHARDS.glob(pre.name + ".part*.tmp")):
        raise RuntimeError(f"orphan parts block fresh shard {i}")
    log_path = Path(str(pre) + ".run.log")
    log = open(log_path, "wb")
    proc = subprocess.Popen(
        [str(BIN), "run", str(lo), str(hi), str(KEY_CAP), str(pre), "reserved"],
        stdout=log, stderr=subprocess.STDOUT,
    )
    return {"i": i, "lo": lo, "hi": hi, "proc": proc, "log": log,
            "log_path": log_path, "started": time.monotonic()}


def rss_kib(active):
    pids = [str(x["proc"].pid) for x in active.values() if x["proc"].poll() is None]
    if not pids:
        return 0
    try:
        q = subprocess.run(["ps", "-o", "rss=", "-p", ",".join(pids)],
                           text=True, capture_output=True, check=True)
        return sum(int(x) for x in q.stdout.split())
    except Exception:
        return None


def terminate(active):
    for x in active.values():
        if x["proc"].poll() is None:
            x["proc"].terminate()
    end = time.monotonic() + 5
    while time.monotonic() < end and any(x["proc"].poll() is None for x in active.values()):
        time.sleep(.1)
    for x in active.values():
        if x["proc"].poll() is None:
            x["proc"].kill()


def aggregate(accepted, elapsed, max_rss, free_start, free_end, scheduled):
    fields = ["source_rows", "pivotable_source_rows", "generated_k18_parents",
              "pivotable_k18_parents", "outgoing_pivot_uses",
              "emitted_records_local_unique", "parts"]
    sums = {f: sum(x["kernel"][f] for x in accepted) for f in fields}
    sums["signed_weight_scaled"] = str(sum(int(x["kernel"]["signed_weight_scaled"]) for x in accepted))
    hist = {}
    for x in accepted:
        for k, v in x["kernel"]["denominator_histogram"].items():
            hist[k] = hist.get(k, 0) + v
    complete = len(accepted) == NSHARD
    if complete:
        assert sums["source_rows"] == N
        assert sums["pivotable_source_rows"] == 24_003_767
        assert sums["generated_k18_parents"] == 1_559_270_244
        assert sums["generated_k18_parents"] // 12 == 129_939_187
        assert sums["pivotable_k18_parents"] == 807_499_618
    return {
        "status": "PASS_COMPLETE_64_SHARD_K16_CACHED_EXPORT" if complete else "UNRESOLVED_GATE_PARTIAL_K16_CACHED_EXPORT",
        "scope": "export only; no merge, charge, cleanup, row collection, or K21 tails",
        "complete": complete,
        "accepted_shards": len(accepted),
        "scheduled_this_run": scheduled,
        "ranges": [[x["shard"], *x["source_range"]] for x in accepted],
        "scale_U": "400591699200",
        "workers": WORKERS,
        "key_cap": KEY_CAP,
        "stop_scheduling_seconds": STOP_SCHEDULING,
        "hard_gate_seconds": HARD_GATE,
        "elapsed_seconds": elapsed,
        "max_observed_worker_rss_kib": max_rss,
        "rss_observation_scope": "sum of active exporter processes; parent runner excluded; null if ps unavailable",
        "free_bytes_start": free_start,
        "free_bytes_end": free_end,
        "part_bytes": sum(x["part_bytes"] for x in accepted),
        "totals": sums,
        "denominator_histogram": dict(sorted(hist.items())),
        "source_sha256": sha(SRC),
        "binary_sha256": sha(BIN),
    }


def main():
    begun = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    SHARDS.mkdir(parents=True, exist_ok=True)
    free_start = shutil.disk_usage(OUT).free
    if free_start < 100 * 1024**3:
        raise RuntimeError(f"preflight free space too small: {free_start}")
    jobs = ranges()
    accepted = []
    pending = []
    for job in jobs:
        x = validate_accepted(*job)
        if x is None:
            pending.append(job)
        else:
            accepted.append(x)
    active = {}
    scheduled = 0
    max_rss = 0
    try:
        while pending or active:
            elapsed = time.monotonic() - begun
            if elapsed >= HARD_GATE:
                terminate(active)
                break
            free = shutil.disk_usage(OUT).free
            if free < FREE_FLOOR:
                terminate(active)
                raise RuntimeError(f"free-space floor reached: {free}")
            while pending and len(active) < WORKERS and elapsed < STOP_SCHEDULING:
                i, lo, hi = pending.pop(0)
                x = launch(i, lo, hi)
                active[i] = x
                scheduled += 1
            observed = rss_kib(active)
            if observed is not None:
                max_rss = max(max_rss, observed)
                if observed > RSS_LIMIT_KIB:
                    terminate(active)
                    raise RuntimeError(f"worker RSS cap exceeded: {observed} KiB")
            done = [i for i, x in active.items() if x["proc"].poll() is not None]
            for i in done:
                x = active.pop(i); x["log"].close()
                if x["proc"].returncode != 0:
                    raise RuntimeError(f"shard {i} failed rc={x['proc'].returncode}; see {x['log_path']}")
                accepted.append(validate_finished_shard(i, x["lo"], x["hi"]))
                print(f"ACCEPT shard={i} total={len(accepted)}/64 elapsed={time.monotonic()-begun:.3f}s", flush=True)
            if not done:
                time.sleep(.25)
            if not active and pending and time.monotonic() - begun >= STOP_SCHEDULING:
                break
    finally:
        for x in active.values():
            x["log"].close()
    accepted.sort(key=lambda x: x["shard"])
    result = aggregate(accepted, time.monotonic()-begun, max_rss, free_start,
                       shutil.disk_usage(OUT).free, scheduled)
    atomic_json(OUT / "results_k16_cached_export.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["complete"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
