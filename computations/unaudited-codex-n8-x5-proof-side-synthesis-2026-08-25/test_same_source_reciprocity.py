#!/usr/bin/env python3
"""Exact source-labelled response reciprocity and clean-cap counterguard.

This is a symbolic, four-site check.  It neither reads D12 nor solves an
ideal.  The central identity compares two *physical cap pairs on the same
source*, retaining endpoint order.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
UPSTREAM = REPO / "computations/unaudited-codex-triangle-five-set-annihilator-2026-08-22/results_triangle_five_set_annihilator.json"
UPSTREAM_SHA256 = "6cd93663ed6bf392a24ee74cc1546cdcaa8b8124d07012910df69920bbf9abae"
COLORS = range(3)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def xvar(u: int, v: int, cu: int, cv: int) -> tuple[int, int, int, int]:
    """Literal stored-edge label with named endpoint colours."""
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return u, v, cu, cv


def product(left, right):
    return tuple(sorted((left, right)))


def response_basis_pairing(p, q, a, b, i, j, alpha, beta):
    """<E_ab^(alpha,beta), R_ab^pq(E_pq^(i,j))> as a source polynomial."""
    return Counter({
        product(xvar(p, a, i, alpha), xvar(q, b, j, beta)): 1,
        product(xvar(p, b, i, beta), xvar(q, a, j, alpha)): 1,
    })


def switched_basis_pairing(p, q, a, b, i, j, alpha, beta):
    """<E_pq^(i,j), R_pq^ab(E_ab^(alpha,beta))>."""
    return Counter({
        product(xvar(a, p, alpha, i), xvar(b, q, beta, j)): 1,
        product(xvar(a, q, alpha, j), xvar(b, p, beta, i)): 1,
    })


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield ((first, second),) + tail


def zero_matrix():
    return [[0 for _ in COLORS] for _ in COLORS]


def identity_matrix():
    return [[int(i == j) for j in COLORS] for i in COLORS]


def e00_matrix():
    answer = zero_matrix()
    answer[0][0] = 1
    return answer


def transpose(matrix):
    return [[matrix[j][i] for j in COLORS] for i in COLORS]


def install(blocks, u, v, matrix):
    blocks[(u, v)] = matrix
    blocks[(v, u)] = transpose(matrix)


def get_block(blocks, u, v):
    return blocks.get((u, v), zero_matrix())


def response(blocks, p, q, a, b, covector):
    answer = zero_matrix()
    pa, qb = get_block(blocks, p, a), get_block(blocks, q, b)
    pb, qa = get_block(blocks, p, b), get_block(blocks, q, a)
    for alpha in COLORS:
        for beta in COLORS:
            answer[alpha][beta] = sum(
                covector[i][j] * (
                    pa[i][alpha] * qb[j][beta]
                    + pb[i][beta] * qa[j][alpha]
                )
                for i in COLORS for j in COLORS
            )
    return answer


def pairing(covector, vector):
    return sum(covector[i][j] * vector[i][j] for i in COLORS for j in COLORS)


def main() -> None:
    assert sha256(UPSTREAM) == UPSTREAM_SHA256
    upstream = json.loads(UPSTREAM.read_text())
    assert upstream["status"] == "PASS triangle annihilator leaves one opposite-edge response"

    # Prove the response-reciprocity identity on every disjoint named pair of
    # physical edges and every pair of matrix-coordinate covectors.  This is
    # equality of literal two-monomial source polynomials, not numerical tests.
    configurations = 0
    basis_pairings = 0
    for p, q in itertools.combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in (p, q))
        for a, b in itertools.combinations(residual, 2):
            configurations += 1
            for i, j, alpha, beta in itertools.product(COLORS, repeat=4):
                left = response_basis_pairing(p, q, a, b, i, j, alpha, beta)
                right = switched_basis_pairing(p, q, a, b, i, j, alpha, beta)
                assert left == right
                basis_pairings += 1
    assert configurations == 420 and basis_pairings == 34_020

    # The direct blocker cannot enter the cyclic five-set survivor: every
    # matching containing pq lies in the one-crossing sector, which beta kills.
    p, q, t = 6, 7, 0
    five_set = frozenset((1, 2, 3, 4, 5))
    cap_cut = frozenset((p, q, t))
    all_matchings = tuple(matchings(tuple(range(8))))
    assert len(all_matchings) == 105
    direct_matchings = [matching for matching in all_matchings if (p, q) in matching]
    crossing_count = lambda matching: sum((u in cap_cut) != (v in cap_cut) for u, v in matching)
    assert len(direct_matchings) == 15
    assert {crossing_count(matching) for matching in direct_matchings} == {1}
    assert all(any((u in five_set) != (v in five_set) for u, v in matching)
               for matching in direct_matchings)

    # Rebuild the retained formal hostile source.  It proves that the natural
    # strengthening "the reciprocal five-set covector is automatically an
    # active clean cap" fails at the first activity equation.
    blocks = {}
    install(blocks, 6, 1, identity_matrix())
    install(blocks, 7, 2, identity_matrix())
    install(blocks, 0, 3, e00_matrix())
    install(blocks, 4, 5, e00_matrix())
    install(blocks, 6, 7, identity_matrix())
    K = identity_matrix()
    L = e00_matrix()  # Theta_(0,beta,0) for beta=evaluation at 00000.
    response_12 = response(blocks, 6, 7, 1, 2, K)
    response_67_switched = response(blocks, 1, 2, 6, 7, L)
    assert response_12 == identity_matrix()
    assert pairing(L, response_12) == pairing(K, response_67_switched) == 1
    assert pairing(L, get_block(blocks, 1, 2)) == 0  # s_12(L)
    kappa = [L[c][c] for c in COLORS]
    assert kappa == [1, 0, 0]
    residual = (0, 3, 4, 5, 6, 7)
    residual_responses = {
        (a, b): response(blocks, 1, 2, a, b, L)
        for a, b in itertools.combinations(residual, 2)
    }
    nonzero_response_edges = {
        edge: matrix for edge, matrix in residual_responses.items()
        if matrix != zero_matrix()
    }
    assert nonzero_response_edges == {(6, 7): e00_matrix()}
    assert upstream["hostile_source_guard"]["R_12_of_K"] == "I3"
    assert upstream["hostile_source_guard"]["delta_beta"] == [1, 0, 0]

    result = {
        "schema": "KRENN_X5_SAME_SOURCE_RESPONSE_RECIPROCITY_AUDIT_V1",
        "status": "PASS_EXACT_RECIPROCITY_AND_FIRST_FALSE_CLEAN_CAP_EQUATION",
        "proved_lemma": {
            "identity": "<L,R_ab^pq(K)> = <K,R_pq^ab(L)>",
            "scope": "all disjoint named physical pairs, arbitrary 3x3 covectors, arbitrary endpoint-ordered source blocks",
            "source_monomials_per_basis_identity": 2,
            "physical_pair_configurations": configurations,
            "basis_coordinate_identities": basis_pairings,
            "interpretation": (
                "The opposite-edge term in the cyclic five-set identity is an exact "
                "response row for the switched physical cap pair on the same source."
            ),
        },
        "conditional_diagonal_branch_corollary": {
            "hypotheses": [
                "b_d*ell_d - Theta_(t,beta,d) R_ab^pq lies in rowspan L_T^pq",
                "ell_d lies in rowspan L_T^pq (one of the three coloured blocker branches)",
            ],
            "conclusion": (
                "R_pq^ab(L_(t,beta,d)) lies in rowspan L_T^pq, where "
                "L_(t,beta,d) is the covector represented by Theta_(t,beta,d)"
            ),
            "proof": "subtract the two row-space identities, then apply exact response reciprocity",
            "branches": [
                "triangle_endpoint_colour",
                "cap_endpoint_colour",
                "third_colour",
            ],
            "does_not_yet_prove": "activity or vanishing cap error for the switched covector L",
        },
        "direct_branch_first_missing_term": {
            "direct_pq_matchings": len(direct_matchings),
            "crossing_sector": "T1 only",
            "consequence": (
                "the five-set annihilator kills every direct-pair term before the "
                "opposite-edge survivor is formed; no s=<K,A_pq> cancellation row exists"
            ),
            "first_literal_matching": "67|01|23|45",
        },
        "first_false_clean_cap_strengthening": {
            "candidate": "the reciprocal five-set covector L is automatically an active clean cap for pair ab",
            "counterguard_scope": "source-faithful formal contraction, deliberately not normalized X5",
            "cap_pair": [1, 2],
            "L": "E00",
            "s_L": 0,
            "kappa_L": kappa,
            "nonzero_response_edges": ["67"],
            "r_squared_and_cap_error": "zero by single-edge support",
            "failed_first_equations": ["s_L != 0", "kappa_0*kappa_1*kappa_2 != 0"],
            "reciprocal_identity_still_holds": True,
            "conclusion": (
                "same-source reciprocity is proved, but cleanliness/activity does not "
                "follow formally; normalized X5 or an additional pure-row identity is load-bearing"
            ),
        },
        "upstream_triangle_identity_sha256": UPSTREAM_SHA256,
        "guards": {
            "degree_twelve_read": False,
            "ideal_solve": False,
            "claim_for_normalized_X5_from_counterguard": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_same_source_reciprocity.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_same_source_reciprocity.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
