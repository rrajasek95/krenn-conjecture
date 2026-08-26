#!/usr/bin/env python3
"""Replay the exact rank-one guard pivot contraction for representative 2."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-incidence-gate-2026-08-25"
PINS = {
    "generate_rep2_gates.py": "82c66df41b0eedbdf309dbf0432bdd4c33884323d8899195211c7abdc03f5b56",
    "generate_rep2_rank1_split.py": "03b1d2cdd98328056c8f7e9359047655abdda92f4d2d473442283ef3b066af77",
    "rep2_gate_metadata.json": "034e41e224f975f5022ed2c8c43f668c41325ce2b884d12ed6e0d26d2b4cd74b",
    "rep2_rank1_split_metadata.json": "4677d74bbf45054a13b6174af70bf4245a608e05623e2f4934e94055e369925c",
    "rep2_incidence_subset_metadata.json": "cd7834d1346531bd196d663d1ce9883a5ac8a052c35e1dbbb620e86f2c97d0bd",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


# Sparse integral polynomials.  A monomial is a sorted tuple of variable names.
Poly = dict[tuple[str, ...], int]


def const(value: int) -> Poly:
    return {} if value == 0 else {(): value}


def var(name: str) -> Poly:
    return {(name,): 1}


def add(left: Poly, right: Poly) -> Poly:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def neg(value: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in value.items()}


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, neg(right))


def mul(left: Poly, right: Poly) -> Poly:
    answer: Poly = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(sorted(lm + rm))
            answer[monomial] = answer.get(monomial, 0) + lc * rc
            if answer[monomial] == 0:
                del answer[monomial]
    return answer


def total(values) -> Poly:
    answer: Poly = {}
    for value in values:
        answer = add(answer, value)
    return answer


def swap12(triple: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(0 if value == 0 else 3 - value for value in triple)


def main() -> None:
    observed = {name: sha256(SOURCE / name) for name in PINS}
    assert observed == PINS
    gate = json.loads((SOURCE / "rep2_gate_metadata.json").read_text())
    split = json.loads((SOURCE / "rep2_rank1_split_metadata.json").read_text())
    subset = json.loads((SOURCE / "rep2_incidence_subset_metadata.json").read_text())
    assert gate["representative_id"] == split["representative_id"] == subset["representative_id"] == 2
    assert gate["stored_edge_guard"]["derived"] == [
        "A56^T=-A26*A57^T",
        "(I-A17*A26)*A57^T=0",
        "A06*A57^T=0",
    ]
    assert subset["variants"]["cap45_star1_three_term"]["factorization"] == "A04*K*[A35^T|A56|A57]"
    assert subset["variants"]["cap03_star6_two_sandwich"]["factorization"] == "A04^T*K*[A23^T|A35]"

    triples = tuple(itertools.product(range(3), repeat=3))
    orbits = []
    unseen = set(triples)
    while unseen:
        representative = min(unseen)
        orbit = {representative, swap12(representative)}
        orbits.append((representative, tuple(sorted(orbit))))
        unseen -= orbit
    assert len(orbits) == 14
    assert set().union(*(set(orbit) for _, orbit in orbits)) == set(triples)
    assert sum(len(orbit) for _, orbit in orbits) == 27

    v = [var(f"v{j}") for j in range(3)]
    w = [total(mul(var(f"a26_{i}{j}"), v[j]) for j in range(3)) for i in range(3)]
    q, zeta = var("q"), var("zeta")
    checks = 0
    largest_identity_terms = 0
    for s, t in itertools.product(range(3), repeat=2):
        inverse_v = sub(mul(q, v[s]), const(1))
        inverse_w = sub(mul(zeta, w[t]), const(1))
        for i in range(3):
            source_sum = total(mul(var(f"a06_{i}{j}"), v[j]) for j in range(3) if j != s)
            solved_a06 = neg(mul(q, source_sum))
            substituted_guard = add(source_sum, mul(solved_a06, v[s]))
            certificate = neg(mul(source_sum, inverse_v))
            assert substituted_guard == certificate
            checks += 1
            largest_identity_terms = max(largest_identity_terms, len(certificate))

            remainder = sub(v[i], total(mul(var(f"a17_{i}{j}"), w[j]) for j in range(3) if j != t))
            solved_a17 = mul(zeta, remainder)
            substituted_guard = sub(remainder, mul(solved_a17, w[t]))
            certificate = neg(mul(remainder, inverse_w))
            assert substituted_guard == certificate
            checks += 1
            largest_identity_terms = max(largest_identity_terms, len(certificate))

    result = {
        "schema": "KRENN_X5_REP2_RANK1_GUARD_PIVOT_CONTRACTION_AUDIT_V1",
        "status": "PASS_EXACT_LOCALIZED_EQUIVALENT_CONTRACTION",
        "representative_id": 2,
        "source_sha256": observed,
        "rank_zero_branch": "closed by the pinned structural cap67 argument",
        "rank_one_definitions": {
            "A57": "u*v^T",
            "w": "A26*v",
            "A56": "-u*w^T",
            "guards": ["A06*v=0", "A17*w=v"],
            "nonzero": ["u", "v", "w"],
            "w_nonzero_reason": "A17*w=v and v!=0",
        },
        "charts": {
            "failed_colour": 0,
            "coordinates": ["u_pivot", "v_pivot", "w_pivot"],
            "stabilizer": "the transposition 1<->2",
            "raw_charts": 27,
            "orbit_charts": len(orbits),
            "orbit_representatives": [list(rep) for rep, _ in orbits],
            "orbit_sizes": [len(orbit) for _, orbit in orbits],
            "coverage": "exact for rank(A57)=1 because u,v,w are all nonzero",
        },
        "elimination": {
            "localizers": ["q*v_s-1", "zeta*w_t-1"],
            "solved_entries": [
                "a06_i,s=-q*sum_{j!=s}(a06_i,j*v_j)",
                "a17_i,t=zeta*(v_i-sum_{j!=t}(a17_i,j*w_j))",
            ],
            "guard_equations_eliminated": 6,
            "source_variables_eliminated": 6,
            "certificate_identities_checked": checks,
            "largest_sparse_identity_terms": largest_identity_terms,
            "logic": "equivalent after localization, not merely a sufficient subset",
        },
        "reduced_full_gate_counts_per_chart": {
            "cap45_star1": {"variables": 98, "equations": 6578},
            "cap03_star6": {"variables": 100, "equations": 6578},
            "includes": "all 6561 full-X5 amplitudes, 9 adjoint equations, 6 incidence equations, and 2 inverse equations",
        },
        "scope": {
            "proved": "an exact finite localized atlas and six-variable/six-guard pivot elimination for either named incidence-failure branch",
            "not_proved": "unit ideal or contradiction on any reduced chart",
            "first_remaining_obligation": "show every reduced full-X5+adjoint+incidence chart is empty, or exhibit a chart point",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
