#!/usr/bin/env python3
"""Construct the pointed occurrence in the nonlinear Gram-feature algebra.

The linear actual Gram image is endpoint indicators plus residual-edge
incidence.  In a fixed endpoint fibre, h-1 edges of a marked perfect
matching force its final edge.  Thus one endpoint indicator times h-1 edge
indicators is the marked delta function.  This is a coefficient-algebra
identity only; it does not assert a physical multiplicative PP/Hasse lift.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RANK_CHECKER = ROOT / "computations/verify_uniform_actual_gram_rank_pointed_selector_no_go.py"
RANK_LEDGER = "c668d82dddfdabc2bf09d9fbf9610271924ade2eace804e9c97deb3784fb2b37"
EXPECTED_LEDGER_SHA256 = (
    "8fadec78a8ad69eea8862b6015eb66a0d7e086e6fffb739aeac285a9d3d37553"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_rank_checker():
    spec = importlib.util.spec_from_file_location("gram_rank", RANK_CHECKER)
    require(spec is not None and spec.loader is not None, RANK_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pointed_monomial_audit(h: int, rank_checker) -> dict[str, object]:
    n = 2 * h + 2
    marked_endpoints = (n - 2, n - 1)
    residual = tuple(range(n - 2))
    marked_matching = tuple((index, index + 1)
                            for index in range(0, len(residual), 2))
    selected_edges = frozenset(marked_matching[:-1])

    live = []
    fixed_endpoint_completions = 0
    for p, s, matching in rank_checker.occurrences(h):
        endpoint_factor = int((p, s) == marked_endpoints)
        edge_factor = int(selected_edges <= matching)
        value = endpoint_factor * edge_factor
        if endpoint_factor and edge_factor:
            fixed_endpoint_completions += 1
        if value:
            live.append((p, s, tuple(sorted(matching))))

    require(fixed_endpoint_completions == 1 and len(live) == 1,
            (h, fixed_endpoint_completions, live[:3]))
    require(live[0] == (marked_endpoints[0], marked_endpoints[1],
                        tuple(marked_matching)),
            (h, live[0], marked_matching))

    # A proper subproduct with d chosen marked edges has exactly
    # (2(h-d)-1)!! completions in the fixed endpoint fibre.
    completion_counts = []
    for degree in range(h):
        chosen = frozenset(marked_matching[:degree])
        count = sum(
            int((p, s) == marked_endpoints and chosen <= matching)
            for p, s, matching in rank_checker.occurrences(h)
        )
        expected = 1
        for odd in range(1, 2 * (h - degree), 2):
            expected *= odd
        require(count == expected, (h, degree, count, expected))
        completion_counts.append(count)

    return {
        "h": h,
        "sites": n,
        "marked_endpoints": list(marked_endpoints),
        "marked_matching": [list(edge) for edge in marked_matching],
        "selected_edge_factors": [list(edge) for edge in marked_matching[:-1]],
        "total_feature_degree": h,
        "fixed_endpoint_completion_counts_by_edge_degree_0_to_h_minus_1":
            completion_counts,
        "pointed_support": len(live),
    }


def audit() -> tuple[dict[str, object], str]:
    rank_checker = load_rank_checker()
    _rank_ledger, rank_digest = rank_checker.audit()
    require(rank_digest == RANK_LEDGER, (rank_digest, RANK_LEDGER))
    cases = [pointed_monomial_audit(h, rank_checker) for h in (2, 3, 4)]
    ledger = {
        "pinned_linear_gram_rank_ledger": rank_digest,
        "identity": "Q_(p,s) * product_(e in F minus e0) X_e = delta_(p,s,F)",
        "bounded_literal_checks": cases,
        "uniform_proof": (
            "inside the fixed endpoint fibre, a perfect matching containing "
            "h-1 edges of F has only two unmatched residual vertices, so its "
            "last edge is forced"
        ),
        "h3_selector": "Q_(p,s) * X_e1 * X_e2",
        "physical_scope": (
            "pointwise multiplication in the coefficient feature algebra is "
            "not yet a source-labelled multiplicative PP/Hasse lift; at h=3 "
            "that missing lift is exactly one cubic totalization with its "
            "proper faces and augmented readouts"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "h3", "uniform"),
                        default="all")
    args = parser.parse_args()
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    if args.mode in ("all", "h3"):
        print("h3 pointed feature monomial:", ledger["h3_selector"])
    if args.mode in ("all", "uniform"):
        print("uniform pointed feature degree: h")
    print("physical cubic lift: OPEN")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
