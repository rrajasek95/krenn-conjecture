#!/usr/bin/env python3
"""Bounded one-prime round-635 SpaSM gate; never expands the CEGAR system."""

from __future__ import annotations

import hashlib
import json
import os
import re
import resource
import signal
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PORTFOLIO = ROOT / "computations/unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24"
BRIDGE = HERE / "target/release/cegar635_spasm_bridge"
SPASM = ROOT / "computations/toolkit/vendor/spasm-build-x86/tools/solve"
CHECKPOINT = PORTFOLIO / "tree635_checkpoint.bin"
VECTORS = PORTFOLIO / "tree635_vectors.bin"
TREE_RESULT = PORTFOLIO / "results_tree_round635.json"
PRIME = 1_073_741_827
WALL = 180.0
RSS_BYTES = 8 * 1024**3
PINS = {
    CHECKPOINT: "761804372a3f7e12b1915dd2718f7f69ef00b799dc6f90cd083b2fa7d2fc3c88",
    VECTORS: "dd74d7392a005fb9c7726d9a0cc5c86e5b16d987bcb707d1c3a0f90e6e4d9e40",
    TREE_RESULT: "f0441129b01ad8c2af9ae90ed2c02834ddd35dbb3d11f4e26081cdd41e215702",
    ROOT / "computations/unaudited-codex-n8-affine251-orbit-membership-2026-08-24/src/main.rs":
        "241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0",
    HERE / "src/main.rs": "dbcb02373f8c82586af06ac5f87e20ce6f1935d3709caf7934abb2d03757e622",
    BRIDGE: "76d52f1bb42e0c445e996bb0316eb6eab7f202c3424c5ef89d1c04acd6170b51",
    ROOT / "computations/toolkit/vendor/spasm/tools/solve.c":
        "c06d07ff6a311b88721c13ab10ca8aececb07f4f7eed07118d58e96214909758",
    SPASM: "c7991174857aa1ee77c6d125c33fed7e71d9353e7606d068230708da9602ff18",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def run(command: list[str], timeout: float, stdout_path: Path, stderr_path: Path) -> tuple[float, int]:
    started = time.monotonic()
    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        process = subprocess.Popen(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                   env=dict(os.environ, OMP_NUM_THREADS="8"), start_new_session=True)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            raise RuntimeError(f"wall gate: {' '.join(command)}")
    return time.monotonic() - started, process.returncode


def solve(label: str, matrix: Path, rhs: Path, solution: Path, timeout: float) -> dict:
    temporary = solution.with_suffix(".sms.tmp")
    temporary.unlink(missing_ok=True)
    command = [str(SPASM), "-p", str(PRIME), "--dense-block-size=10000",
               "-m", str(matrix), "-r", str(rhs), "-o", str(temporary)]
    stdout = HERE / f"spasm_{label}.stdout.log"
    stderr = HERE / f"spasm_{label}.stderr.log"
    elapsed, returncode = run(command, timeout, stdout, stderr)
    if returncode != 0:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"SpaSM {label} rc={returncode}")
    text = stderr.read_text(errors="replace")
    ranks = re.findall(r"rank = (\d+)", text)
    if len(ranks) != 1 or "WARNING: no solution" in text:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"SpaSM {label} missing rank or solution")
    os.replace(temporary, solution)
    return {
        "command": command, "elapsed_seconds": elapsed, "rank": int(ranks[0]),
        "solution_sha256": sha(solution), "solution_bytes": solution.stat().st_size,
        "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr),
    }


def verify(label: str, solution: Path, timeout: float) -> dict:
    output = HERE / f"results_solution_audit_{label}.json"
    command = [str(BRIDGE), "--mode", "verify", "--checkpoint", str(CHECKPOINT),
               "--vectors", str(VECTORS), "--solution", str(solution), "--output", str(output)]
    elapsed, returncode = run(command, timeout, HERE / f"verify_{label}.stdout.log",
                              HERE / f"verify_{label}.stderr.log")
    if returncode != 0:
        raise RuntimeError(f"solution verifier {label} rc={returncode}")
    result = json.loads(output.read_text())
    assert result["status"] == "PASS" and result["target_value"] == 1
    assert result["cached_columns_annihilated"] == 222_676
    return {"elapsed_seconds_process": elapsed, "result": result, "result_sha256": sha(output)}


def main() -> None:
    pins = {}
    for path, expected in PINS.items():
        actual = sha(path)
        assert actual == expected, f"stale pin: {path} {actual} != {expected}"
        pins[str(path.relative_to(ROOT))] = actual
    tree = json.loads(TREE_RESULT.read_text())
    assert tree["rounds_completed"] == 635 and tree["column_orbits_exposed"] == 222_676
    assert tree["prime"] == PRIME and tree["rounds"][-1]["solve_seconds"] == 6.230818

    matrix = HERE / "matrix_cegar635_left_orientation.sms"
    rhs = HERE / "rhs_cegar635_minus_target.sms"
    metadata = HERE / "export_cegar635.json"
    export_command = [str(BRIDGE), "--mode", "export", "--checkpoint", str(CHECKPOINT),
                      "--vectors", str(VECTORS), "--matrix", str(matrix), "--rhs", str(rhs),
                      "--metadata", str(metadata)]
    gate_started = time.monotonic()
    export_elapsed, returncode = run(export_command, WALL, HERE / "export.stdout.log", HERE / "export.stderr.log")
    if returncode != 0:
        raise RuntimeError(f"export rc={returncode}")
    remaining = WALL - (time.monotonic() - gate_started)
    if remaining <= 0:
        raise RuntimeError("export exhausted end-to-end wall")
    cold = solve("cold", matrix, rhs, HERE / "solution_cold.sms", remaining)
    cold_export_solve = time.monotonic() - gate_started
    remaining = WALL - cold_export_solve
    if remaining <= 0:
        raise RuntimeError("cold export+solve exceeded end-to-end wall")
    cold_audit = verify("cold", HERE / "solution_cold.sms", remaining)
    cold_gate_total = time.monotonic() - gate_started
    assert cold_gate_total < WALL

    warm_started = time.monotonic()
    warm = solve("warm", matrix, rhs, HERE / "solution_warm.sms", WALL)
    warm_audit = verify("warm", HERE / "solution_warm.sms", WALL - (time.monotonic() - warm_started))
    warm_total = time.monotonic() - warm_started
    assert warm_total < WALL

    export = json.loads(metadata.read_text())
    assert export["status"] == "PASS" and export["equations_cached_columns"] == 222_676
    assert cold["rank"] == warm["rank"]
    raw_peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    peak_bytes = int(raw_peak if os.uname().sysname == "Darwin" else raw_peak * 1024)
    assert 0 < peak_bytes < RSS_BYTES
    rust_solve = 6.230818
    materially_faster = warm["elapsed_seconds"] <= 0.8 * rust_solve
    report = {
        "schema": "KRENN_AFFINE251_D12_CEGAR635_SPASM_GATE_V1",
        "status": "PASS_EXACT_NOT_PROMOTED" if not materially_faster else "PASS_EXACT_PROMOTED",
        "scope": {"degree": 12, "round": 635, "prime": PRIME, "second_prime_run": False,
                  "full_closure_run": False},
        "pins": pins,
        "resource_contract": {"cold_end_to_end_wall_seconds": WALL, "rss_acceptance_limit_bytes": RSS_BYTES,
                              "rss_enforcement": "post-run getrusage rejection; sandbox rejects setrlimit",
                              "observed_cumulative_child_peak_rss_bytes": peak_bytes},
        "export": export,
        "matrix_sha256": sha(matrix), "matrix_bytes": matrix.stat().st_size,
        "rhs_sha256": sha(rhs), "rhs_bytes": rhs.stat().st_size,
        "cold": cold, "cold_solution_audit": cold_audit,
        "warm": warm, "warm_solution_audit": warm_audit,
        "timing_comparison": {
            "export_process_seconds": export_elapsed,
            "cold_export_plus_solve_seconds": cold_export_solve,
            "cold_export_solve_verify_seconds": cold_gate_total,
            "warm_solve_seconds": warm["elapsed_seconds"],
            "warm_solve_plus_verify_seconds": warm_total,
            "rust_tree_round635_solve_seconds": rust_solve,
            "materially_faster_definition": "warm SpaSM solve <= 80% of Rust tree solve",
            "materially_faster": materially_faster,
        },
        "promotion": "PROMOTE_SPASM_WARM_SOLVER" if materially_faster else "DO_NOT_PROMOTE",
        "hostile_contracts": {
            "exact_222676_columns": True, "target_fixed_to_one": True,
            "both_spasm_solutions_replayed_over_every_cached_column": True,
            "cache_internal_fingerprint_and_checkpoint_order_verified": True,
        },
    }
    output = HERE / "results_cegar635_spasm_gate.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
