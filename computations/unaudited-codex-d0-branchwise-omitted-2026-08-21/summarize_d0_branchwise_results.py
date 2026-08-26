#!/usr/bin/env python3
"""Freeze the modular minimal-packet census and exact-Q terminal results."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def basis_record(name):
    path = HERE / f"{name}.manifest.json"
    data = json.loads(path.read_text())
    stage = data["stages"][-1]
    basis = stage.get("basis") or {}
    return {"manifest": path.name, "manifest_sha256": digest(path),
            "status": stage["status"], "unit": basis.get("unit"),
            "basis_length": basis.get("parsed_length")}


def main():
    singles = []
    pairs = []
    for branch in (0, 1):
        for edge in (1, 2, 3, 4):
            record = basis_record(
                f"screen_factor{branch}_cofactor_{edge}_3_p1073741827")
            record.update(branch=branch, cofactors=[edge])
            singles.append(record)
        for tag in ("1_2", "1_3", "1_4", "2_3", "2_4", "3_4"):
            record = basis_record(
                f"screen_factor{branch}_subset_{tag}_p1073741827")
            record.update(branch=branch,
                          cofactors=[int(value) for value in tag.split("_")])
            pairs.append(record)
    require_nonunit = singles + pairs
    if any(record["status"] != "completed" or record["unit"] is not False
           for record in require_nonunit):
        raise RuntimeError("singleton/pair census changed")

    units = []
    for prime, cases in (
        (1073741827, ((0,"1_2_3"),(0,"1_2_4"),(1,"1_3_4"),(1,"2_3_4"))),
        (536870909, ((0,"1_2_3"),(0,"1_2_4"),(1,"1_3_4"),(1,"2_3_4"))),
    ):
        for branch, tag in cases:
            record = basis_record(
                f"screen_factor{branch}_subset_{tag}_p{prime}")
            if record["status"] != "completed" or record["unit"] is not True:
                raise RuntimeError("triple unit census changed")
            record.update(branch=branch, prime=prime,
                          cofactors=[int(value) for value in tag.split("_")])
            units.append(record)

    greedy = [
        basis_record("greedy_factor0_c1_p1073741827"),
        basis_record("greedy_retry_factor1_c2_p1073741827"),
    ]
    if any(record["status"] != "completed" or record["unit"] is not True
           for record in greedy):
        raise RuntimeError("greedy core unit changed")
    greedy[0].update(branch=0, compatibility_index=1)
    greedy[1].update(branch=1, compatibility_index=2)

    exact_audit = HERE / "results_d0_exact_char0_core_audit.json"
    exact = json.loads(exact_audit.read_text())
    result = {
        "status": "UNAUDITED D0 branchwise census and exact cores PASS",
        "singletons": singles,
        "pairs": pairs,
        "two_prime_minimal_triple_units": units,
        "greedy_source_cores": greedy,
        "exact_audit": {"path": exact_audit.name,
                        "file_sha256": digest(exact_audit),
                        "logical_sha256": exact["logical_sha256"]},
        "exact_msolve_runs": [
            {"branch": 0, "elapsed_seconds": 17.17,
             "command": "msolve -f d0_factor0_exact_char0_core.msolve -o d0_factor0_exact_char0_core.out -t 4 -v 1 -l 2"},
            {"branch": 1, "elapsed_seconds": 32.52,
             "command": "msolve -f d0_factor1_exact_char0_core.msolve -o d0_factor1_exact_char0_core.out -t 4 -v 1 -l 2"},
        ],
        "scope": (
            "Exact [-1] closes only the two reconstructed degree-21 factors "
            "inside the D0=0,C0!=0,selected-pivot-open chart. It does not prove "
            "the 450-term eliminant exhausts the saturated source projection."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    target = HERE / "results_d0_branchwise_summary.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 branchwise summary PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
