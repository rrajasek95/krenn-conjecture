#!/usr/bin/env python3
"""Strict independent audit/runner for the bounded D10/D11 SpaSM gate."""

from __future__ import annotations

import argparse
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
AFF = ROOT / "computations/unaudited-codex-n8-affine251-orbit-membership-2026-08-24"
PROVIDER = ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p32003.ms"
EXPORTER = HERE / "target/release/export_affine251_spasm"
SPASM = ROOT / "computations/toolkit/vendor/spasm-build-x86/tools/solve"
PRIMES = (1073741827, 1073741789)
PINS = {
    "provider": (PROVIDER, "75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff"),
    "retained_source": (AFF / "src/main.rs", "241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0"),
    "checkpoint_d10": (AFF / "closure_d10.bin", "2a05d97ce8d58d9d25ac8fddd01eba2ff87b2367949f6d573c0923ea653e4fa2"),
    "checkpoint_d11": (AFF / "closure_d11.bin", "2d9c7b2907b813834ed226c258a7f681fdd6cb8836cff9ad74c148eb1e76ef6f"),
    "result_d10_1073741827": (AFF / "results_d10_p1073741827.json", "f99cadda242f4c58ecad173629a4bb143a3636dc0f8c02136a8cced3cd300289"),
    "result_d10_1073741789": (AFF / "results_d10_p1073741789.json", "02e40c529d6fb57c6fdb11f0f8c358b7cb4dd656eae85349064125c1b6774503"),
    "result_d11_1073741827": (AFF / "results_d11_p1073741827.json", "23173bb78d82664f785a2748b5d85a0a69b535f22bd8aba27f47cbc3da18ef5f"),
    "result_d11_1073741789": (AFF / "results_d11_p1073741789.json", "f97263757f6d73b81617d47a35bb6c82828c55bce61bfb723c53722c792d71d0"),
    "dual_d10_1073741827": (AFF / "dual_d10_p1073741827.tsv", "27b47b61238044c739daa5941ad80782d249cdea4e115e07043472b507eb0d87"),
    "dual_d10_1073741789": (AFF / "dual_d10_p1073741789.tsv", "f2ef521abdfd94df3f17898d62d4e1989897d2721d27eef80eb8bf7de3dd9a63"),
    "dual_d11_1073741827": (AFF / "dual_d11_p1073741827.tsv", "caf4639d57d50e8147d4c38f0b5ebd76a087fed29cd9c68f8691b3ef478cd905"),
    "dual_d11_1073741789": (AFF / "dual_d11_p1073741789.tsv", "248d19889904a50572893f0e0652ac26f405d1d5b8cd0f27881d8531c6add863"),
    "spasm_source": (ROOT / "computations/toolkit/vendor/spasm/tools/solve.c", "c06d07ff6a311b88721c13ab10ca8aececb07f4f7eed07118d58e96214909758"),
    "spasm_binary": (SPASM, "c7991174857aa1ee77c6d125c33fed7e71d9353e7606d068230708da9602ff18"),
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def pin_inputs() -> dict[str, dict[str, str]]:
    out = {}
    for name, (path, expected) in PINS.items():
        actual = sha(path)
        if expected != "PLACEHOLDER" and actual != expected:
            raise AssertionError(f"stale pin {name}: {actual} != {expected}")
        out[name] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return out


def parse_dual(path: Path, prime: int, row_count: int):
    lines = path.read_text().splitlines()
    head = lines[0].split()
    assert head[:2] == ["KRENN_AFFINE251_ORBIT_DUAL_V1", str(prime)]
    support, pairing = map(int, head[2:])
    dual = {}
    for line in lines[1:]:
        tag, row, _hex, value = line.split()
        row, value = int(row), int(value)
        assert tag == "ROW" and 0 <= row < row_count and 0 < value < prime and row not in dual
        dual[row] = value
    assert len(dual) == support and 0 < pairing < prime
    return dual, pairing


def verify_matrix_and_duals(matrix: Path, metadata: dict, degree: int, expected: dict[int, dict]):
    row_count = metadata["row_orbits"]
    col_count = metadata["column_orbits"]
    duals = {p: parse_dual(AFF / f"dual_d{degree}_p{p}.tsv", p, row_count) for p in PRIMES}
    sums = {p: {} for p in PRIMES}
    nnz = 0
    last = (0, 0)
    with matrix.open() as stream:
        assert stream.readline().strip() == f"{col_count} {row_count} M"
        for raw in stream:
            i, j, value = map(int, raw.split())
            if (i, j, value) == (0, 0, 0):
                break
            assert 1 <= i <= col_count and 1 <= j <= row_count and value
            assert (i, j) > last
            last = (i, j)
            nnz += 1
            for p in PRIMES:
                coefficient = duals[p][0].get(j - 1)
                if coefficient is not None:
                    sums[p][i] = (sums[p].get(i, 0) + value * coefficient) % p
        else:
            raise AssertionError("matrix terminator missing")
        assert not stream.read().strip()
    assert nnz == metadata["matrix_nnz"]
    target = metadata["target_row_id_zero_based"]
    audit = {}
    for p in PRIMES:
        assert not any(sums[p].values())
        assert duals[p][0].get(target, 0) == duals[p][1] == expected[p]["target_pairing"]
        audit[str(p)] = {"all_columns_annihilated": True, "dual_support": len(duals[p][0]), "target_pairing": duals[p][1]}
    return audit


def run_spasm(matrix: Path, rhs: Path, degree: int, prime: int, wall: float, rss_gib: float):
    tmp = HERE / f"solution_d{degree}_p{prime}.sms.tmp"
    final = HERE / f"solution_d{degree}_p{prime}.sms"
    stdout_path = HERE / f"spasm_d{degree}_p{prime}.stdout.log"
    stderr_path = HERE / f"spasm_d{degree}_p{prime}.stderr.log"
    tmp.unlink(missing_ok=True)
    final.unlink(missing_ok=True)
    spasm_command = [str(SPASM), "-p", str(prime), "--dense-block-size=10000", "-m", str(matrix), "-r", str(rhs), "-o", str(tmp)]
    command = spasm_command
    env = dict(os.environ, OMP_NUM_THREADS="8")
    rss_bytes = int(rss_gib * 1024**3)
    started = time.monotonic()
    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout, stderr=stderr,
                                   start_new_session=True)
        while process.poll() is None:
            elapsed = time.monotonic() - started
            if elapsed >= wall:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                tmp.unlink(missing_ok=True)
                raise RuntimeError(f"SpaSM wall gate degree={degree} prime={prime} elapsed={elapsed:.3f}")
            time.sleep(0.2)
    elapsed = time.monotonic() - started
    if process.returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"SpaSM failed degree={degree} prime={prime} rc={process.returncode}")
    stderr = stderr_path.read_text()
    matches = re.findall(r"rank = (\d+)", stderr)
    assert len(matches) == 1
    warnings = re.findall(r"WARNING: no solution for row (\d+)", stderr)
    assert warnings == ["0"]
    raw_peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    peak_bytes = int(raw_peak if os.uname().sysname == "Darwin" else raw_peak * 1024)
    assert 0 < peak_bytes < rss_bytes
    os.replace(tmp, final)
    return {
        "command": spasm_command, "resource_measurement": "wait4/getrusage cumulative child maximum",
        "rank": int(matches[0]), "rhs_consistent": False,
        "elapsed_seconds": elapsed, "peak_rss_bytes": peak_bytes,
        "stdout_sha256": sha(stdout_path), "stderr_sha256": sha(stderr_path),
        "solution_sha256": sha(final), "solution_size": final.stat().st_size,
    }


def hostile_selftests(base: dict) -> int:
    mutations = [
        ("rank", base["rank"] + 1), ("rhs_consistent", True),
        ("prime", 1073741783), ("matrix_nnz", base["matrix_nnz"] - 1),
        ("dual_verified", False), ("degree", 12),
    ]
    rejected = 0
    for key, value in mutations:
        forged = dict(base, **{key: value})
        try:
            assert forged["degree"] in (10, 11)
            assert forged["prime"] in PRIMES
            assert forged["rank"] == forged["expected_rank"]
            assert forged["rhs_consistent"] is forged["expected_member"]
            assert forged["matrix_nnz"] == forged["expected_nnz"]
            assert forged["dual_verified"] is True
        except AssertionError:
            rejected += 1
    assert rejected == len(mutations)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, choices=(10, 11), required=True)
    parser.add_argument("--wall-seconds", type=float, default=300)
    parser.add_argument("--rss-gib", type=float, default=8)
    parser.add_argument("--skip-export", action="store_true")
    args = parser.parse_args()
    pins = pin_inputs()
    assert EXPORTER.exists()
    degree = args.degree
    expected = {p: json.loads((AFF / f"results_d{degree}_p{p}.json").read_text()) for p in PRIMES}
    for p, data in expected.items():
        assert data["prime"] == p and data["degree"] == degree
        assert data["status"] == "COMPLETE_NONMEMBER_MOD_PRIME" and data["member_mod_prime"] is False
    matrix = HERE / f"matrix_d{degree}_integer_AT.sms"
    rhs = HERE / f"rhs_d{degree}_target.sms"
    metadata_path = HERE / f"export_d{degree}.json"
    if not args.skip_export:
        cmd = [str(EXPORTER), "--input", str(PROVIDER), "--checkpoint", str(AFF / f"closure_d{degree}.bin"),
               "--matrix", str(matrix), "--rhs", str(rhs), "--metadata", str(metadata_path),
               "--degree", str(degree), "--prime", str(PRIMES[0]), "--workers", "8",
               "--wall-seconds", str(int(args.wall_seconds)), "--rss-gib", str(int(args.rss_gib))]
        subprocess.run(cmd, cwd=ROOT, check=True)
    metadata = json.loads(metadata_path.read_text())
    assert metadata["degree"] == degree and metadata["status"] == "PASS"
    for p in PRIMES:
        data = expected[p]
        assert metadata["row_orbits"] == data["row_orbits"]
        assert metadata["column_orbits"] == data["column_orbits"]
        assert metadata["matrix_nnz"] == data["matrix_nnz"]
    assert metadata["max_abs_integer_coefficient"] < min(PRIMES) // 2
    dual_audit = verify_matrix_and_duals(matrix, metadata, degree, expected)
    runs = {}
    for p in PRIMES:
        run = run_spasm(matrix, rhs, degree, p, args.wall_seconds, args.rss_gib)
        assert run["rank"] == expected[p]["rank"]
        assert run["rhs_consistent"] is expected[p]["member_mod_prime"]
        runs[str(p)] = run
    hostile_base = {
        "degree": degree, "prime": PRIMES[0], "rank": runs[str(PRIMES[0])]["rank"],
        "expected_rank": expected[PRIMES[0]]["rank"], "rhs_consistent": False,
        "expected_member": False, "matrix_nnz": metadata["matrix_nnz"],
        "expected_nnz": expected[PRIMES[0]]["matrix_nnz"], "dual_verified": True,
    }
    report = {
        "schema": "KRENN_AFFINE251_SPASM_EQUIVALENCE_V1", "status": "PASS",
        "degree": degree, "primes": list(PRIMES), "pins": pins,
        "exporter_sha256": sha(EXPORTER), "matrix_sha256": sha(matrix), "rhs_sha256": sha(rhs),
        "export": metadata, "dual_audit": dual_audit, "spasm_runs": runs,
        "equivalence": {
            "rank_exact": True, "target_residual_nonzero_exact": True,
            "solution_or_dual": "retained dual independently annihilates every exported column and separates target",
            "member_mod_prime": False,
        },
        "hostile_mutations_rejected": hostile_selftests(hostile_base),
    }
    output = HERE / f"results_spasm_equivalence_d{degree}.json"
    tmp = output.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
