#!/usr/bin/env python3
"""Reconstruct and replay the exact-Q dual for the closed K0--K9 tail component."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EDGES = HERE / "k5_k9_column_output_closure_layer4_edges.tsv"
COLUMNS = HERE / "k9_incidence_closure_layer4_columns.tsv"
TARGET = HERE / "k9_k12_tail_rows.tsv"
CLOSURE = HERE / "results_joint_incidence_full_layer5.json"
MOD_RESULTS = {
    1009: HERE / "results_closed_markowitz_p1009_dual.json",
    1013: HERE / "results_closed_markowitz_p1013_dual.json",
}
MOD_DUALS = {
    1009: HERE / "closed_markowitz_dual_p1009.tsv",
    1013: HERE / "closed_markowitz_dual_p1013.tsv",
}
OUT = HERE / "results_closed_component_exact_dual_audit.json"
PINS = {
    EDGES: "97e6b061456e03a4c3db6ff68175fb8bfa6f0af904a72577cbfeefc68df0a344",
    COLUMNS: "22e789dad1d71dbc7d6b40dab839b39042f3819bbfb782fb8b88d7cdae6d8ae5",
    TARGET: "4e214b40aede42b09c4c3dfc05c2969541f1a9dd6271f7eb53b36303478ba3ae",
    CLOSURE: "a99af72f3ac5f3c08aea933ce85dab5271c6761d1ae0ff1cec6297d5297f48c4",
    MOD_RESULTS[1009]: "d927f51006fa6389e0c37ef6bb7b9006d16e24ab9b5f137f5fca7b12fcf48459",
    MOD_RESULTS[1013]: "3435908dd940353660fe9e3bfd890bef0b649806f3ef207fba9a9410acd03be4",
    MOD_DUALS[1009]: "10313c011777a7d17ebb846df8b61a7c87949e48993b9a298f52459e7df20a07",
    MOD_DUALS[1013]: "064dfd664f827c26123432c6db5ad2ae503355c2b3bbfb0ef2547c055d0631db",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def read_modular_dual(prime: int) -> dict[tuple[int, str], int]:
    answer = {}
    with MOD_DUALS[prime].open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tvalue", "dual header changed")
        for line in handle:
            degree, row, value = line.rstrip("\n").split("\t")
            value = int(value)
            require(0 < value < prime, "noncanonical modular dual value")
            key = (int(degree), row)
            require(key not in answer, "duplicate modular dual row")
            answer[key] = value
    return answer


def main() -> None:
    for path, digest in PINS.items():
        require(sha256(path) == digest, f"pin changed: {path.name}")
    closure = json.loads(CLOSURE.read_text())
    require(closure["sample_unique_new_columns"] == 0, "component is not incidence-closed")
    require(closure["existing_columns"] == 837883, "closed column census changed")
    for prime, path in MOD_RESULTS.items():
        result = json.loads(path.read_text())
        require(result["status"] == "PROVED_NO_SOLUTION_MOD_PRIME" and result["prime"] == prime, "bad modular result")
        require(result["pivots"] == 371451 and result["dual_support"] == 70, "modular elimination census changed")

    modular = {prime: read_modular_dual(prime) for prime in MOD_DUALS}
    require(set(modular[1009]) == set(modular[1013]) and len(modular[1009]) == 70, "dual supports differ")
    exact = {}
    for key in modular[1009]:
        residues = []
        for prime in (1009, 1013):
            value = modular[prime][key]
            residues.append(value if value <= prime // 2 else value - prime)
        require(residues[0] == residues[1], f"signed reconstruction differs at {key}")
        exact[key] = residues[0]
    require(min(exact.values()) == -32 and max(exact.values()) == 32, "exact coefficient range changed")

    checked_columns = 0
    checked_edges = 0
    current_column = None
    current_pairing = 0
    with EDGES.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\tdegree\trow\tmultiplicity", "edge header changed")
        for line in handle:
            column, degree, row, value = line.rstrip("\n").split("\t")
            column = int(column)
            if current_column is None:
                require(column == 0, "edge ledger does not start at column zero")
                current_column = column
            elif column != current_column:
                require(column == current_column + 1, "edge column gap/order changed")
                require(current_pairing == 0, f"exact dual fails column {current_column}")
                checked_columns += 1
                current_column = column
                current_pairing = 0
            current_pairing += exact.get((int(degree), row), 0) * int(value)
            checked_edges += 1
    require(current_column == 837882 and current_pairing == 0, "exact dual fails final column")
    checked_columns += 1
    require(checked_columns == 837883 and checked_edges == 8342855, "matrix replay census changed")

    target_pairing = 0
    target_intersection = 0
    with TARGET.open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tcoefficient", "target header changed")
        for line in handle:
            degree, row, coefficient = line.rstrip("\n").split("\t")
            value = exact.get((int(degree), row), 0)
            if value:
                target_intersection += 1
                target_pairing += value * int(coefficient)
    require(target_intersection == 7 and target_pairing == -4608, "exact target pairing changed")

    degree_histogram = Counter(degree for degree, _ in exact)
    coefficient_histogram = Counter(exact.values())
    payload = {
        "status": "PASS_EXACT_Q_CLOSED_COMPONENT_DUAL",
        "cutoff": 10,
        "closed_component_rows": sum(closure["joint_rows_by_degree"].values()),
        "closed_component_columns": checked_columns,
        "weighted_edges_checked": checked_edges,
        "incidence_frontier_columns": closure["sample_unique_new_columns"],
        "dual_terms": len(exact),
        "dual_degree_histogram": dict(sorted(degree_histogram.items())),
        "dual_coefficient_histogram": {str(key): value for key, value in sorted(coefficient_histogram.items())},
        "dual_target_support_intersection": target_intersection,
        "exact_target_pairing": target_pairing,
        "all_closed_source_columns_annihilated_over_Z": True,
        "conclusion": "The exact K9 residual R_tail is not in the complete cutoff-10 mixed-source image over Q.",
        "scope": (
            "This closes only the exponent-one cutoff ladder: it reaffirms H0*H1*H2 not in I_mix. "
            "It is not radical nonmembership, localized nonmembership, or a Krenn-Gu conjecture verdict."
        ),
        "pins": {path.name: digest for path, digest in PINS.items()},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
