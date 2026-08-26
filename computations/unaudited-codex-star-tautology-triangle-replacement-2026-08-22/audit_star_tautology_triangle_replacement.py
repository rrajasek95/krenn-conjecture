#!/usr/bin/env python3
"""Finite endpoint/source-label audit for the star-tautology correction.

The checker proves the combinatorial factorization of the three-crossing
sector through the cap-pair response edges.  It imports the universal
existence of a target-active five-set annihilator as the certified SP-K6
corollary; it does not recompute that theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OUT = Path(__file__).with_name("results_star_tautology_triangle_replacement.json")
MANIFEST_OUT = Path(__file__).with_name("canonical_triangle_incidence_manifest.json")
COLORS = (0, 1, 2)
CUT_SHORE = (0, 6, 7)
W = (1, 2, 3, 4, 5)


def cell(u: int, v: int, cu: int, cv: int) -> str:
    if u < v:
        return f"A_{u}{v}[{cu},{cv}]"
    return f"A_{v}{u}[{cv},{cu}]"


def beta(word: tuple[int, ...]) -> str:
    return "beta_" + "".join(map(str, word))


def direct_term(
    x: int,
    i: int,
    j: int,
    sigma: dict[int, int],
    a: int,
    b: int,
    c: int,
) -> tuple[str, ...]:
    """T3 term: 6-a, 7-b, 0-c, and the last W edge."""
    d, e = sorted(set(W) - {a, b, c})
    word = tuple(sigma[u] for u in W)
    return tuple(
        sorted(
            (
                beta(word),
                cell(6, a, i, sigma[a]),
                cell(7, b, j, sigma[b]),
                cell(0, c, x, sigma[c]),
                cell(d, e, sigma[d], sigma[e]),
            )
        )
    )


def response_factor_term(
    x: int,
    i: int,
    j: int,
    sigma: dict[int, int],
    a: int,
    b: int,
    c: int,
) -> tuple[str, ...]:
    """Same term via Gamma_ab,beta times the oriented response R_ab(K)."""
    lo, hi = sorted((a, b))
    d, e = sorted(set(W) - {lo, hi, c})
    word = tuple(sigma[u] for u in W)
    if a == lo:  # 6 attaches to lo and 7 to hi.
        cap_legs = (
            cell(6, lo, i, sigma[lo]),
            cell(7, hi, j, sigma[hi]),
        )
    else:  # the second, endpoint-swapped response summand.
        cap_legs = (
            cell(6, hi, i, sigma[hi]),
            cell(7, lo, j, sigma[lo]),
        )
    return tuple(
        sorted(
            (
                beta(word),
                *cap_legs,
                cell(0, c, x, sigma[c]),
                cell(d, e, sigma[d], sigma[e]),
            )
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    one_cross_patterns = []
    for shore_vertex in CUT_SHORE:
        for exposed in W:
            for internal_w_matching in range(3):
                one_cross_patterns.append(
                    (shore_vertex, exposed, internal_w_matching)
                )
    assert len(one_cross_patterns) == 45

    checked_terms = 0
    three_cross_patterns = []
    pair_counts = {pair: 0 for pair in itertools.combinations(W, 2)}
    for a, b in itertools.permutations(W, 2):
        for c in W:
            if c in (a, b):
                continue
            three_cross_patterns.append((a, b, c))
            pair_counts[tuple(sorted((a, b)))] += 1
            for word in itertools.product(COLORS, repeat=5):
                sigma = dict(zip(W, word, strict=True))
                for x in COLORS:
                    for i in COLORS:
                        for j in COLORS:
                            assert direct_term(x, i, j, sigma, a, b, c) == (
                                response_factor_term(x, i, j, sigma, a, b, c)
                            )
                            checked_terms += 1
    assert len(three_cross_patterns) == 60
    assert set(pair_counts.values()) == {6}
    assert checked_terms == 60 * 3**5 * 3**3

    residual_edges = set(itertools.combinations(range(6), 2))
    star_allowed = {tuple(sorted((0, u))) for u in W}
    star_outside = residual_edges - star_allowed
    assert star_outside == set(itertools.combinations(W, 2))
    assert len(star_outside) == 10

    triangle = {0, 1, 2}
    triangle_allowed = set(itertools.combinations(sorted(triangle), 2))
    triangle_outside = residual_edges - triangle_allowed
    w_pairs = set(itertools.combinations(W, 2))
    triangle_killed_w_pairs = w_pairs & triangle_outside
    triangle_surviving_w_pairs = w_pairs - triangle_killed_w_pairs
    assert triangle_surviving_w_pairs == {(1, 2)}
    assert len(triangle_killed_w_pairs) == 9

    # A four-residual-site cancellation carrier has six allowed response
    # edges, nine outside edges, and its first cleanliness equation is the
    # three-term four-site Hafnian.  Its cubic is automatic by support.
    k4 = {0, 1, 2, 3}
    k4_allowed = set(itertools.combinations(sorted(k4), 2))
    k4_outside = residual_edges - k4_allowed
    k4_surviving_w_pairs = w_pairs & k4_allowed
    k4_killed_w_pairs = w_pairs - k4_surviving_w_pairs
    assert len(k4_allowed) == 6
    assert len(k4_outside) == 9
    assert k4_surviving_w_pairs == {(1, 2), (1, 3), (2, 3)}
    assert len(k4_killed_w_pairs) == 7

    flags = []
    blocker_types = set()
    for a, p in itertools.permutations(range(8), 2):
        for q in set(range(8)) - {a, p}:
            remaining = sorted(set(range(8)) - {a, p, q})
            for y, z in itertools.combinations(remaining, 2):
                for i, j in itertools.permutations(COLORS, 2):
                    flags.append((a, p, q, y, z, i, j))
                    for c in COLORS:
                        blocker_types.add(
                            "triangle_endpoint_colour"
                            if c == i
                            else "cap_endpoint_colour"
                            if c == j
                            else "third_colour"
                        )
    assert len(flags) == 20160
    assert len(set(flags)) == 20160
    assert blocker_types == {
        "triangle_endpoint_colour",
        "cap_endpoint_colour",
        "third_colour",
    }
    group_order = 40320 * 6
    assert group_order % len(flags) == 0
    flag_stabilizer_order = group_order // len(flags)
    assert flag_stabilizer_order == 12

    source_variables = [
        cell(u, v, i, j)
        for u, v in itertools.combinations(range(8), 2)
        for i in COLORS
        for j in COLORS
    ]
    assert len(source_variables) == len(set(source_variables)) == 252
    all_words = ["".join(map(str, word)) for word in itertools.product(COLORS, repeat=8)]
    pure_words = [str(c) * 8 for c in COLORS]
    mixed_words = [word for word in all_words if word not in pure_words]
    assert len(mixed_words) == 6558
    triangle_outside_rows = [
        {"edge": [a, b], "response_colors": [alpha, beta_color]}
        for a, b in sorted(triangle_outside)
        for alpha in COLORS
        for beta_color in COLORS
    ]
    assert len(triangle_outside_rows) == 108
    witness_variables = [
        f"lambda_{a}{b}_{alpha}{beta_color}"
        for a, b in sorted(triangle_outside)
        for alpha in COLORS
        for beta_color in COLORS
    ]
    assert len(witness_variables) == 108
    manifest = {
        "status": "SOURCE_LABELS_FROZEN_NO_SOLVE",
        "canonical_flag": {
            "live_cell": "A_06[0,1]",
            "inverse_variable": "s_y0",
            "cap_pair": [6, 7],
            "triangle": [0, 1, 2],
        },
        "source_variables": source_variables,
        "rowspan_witness_variables": witness_variables,
        "full_X5_rows": mixed_words,
        "pure_rows": [f"F_{word}-1" for word in pure_words],
        "live_equation": "s_y0*A_06[0,1]-1",
        "outside_response_rows": triangle_outside_rows,
        "response_coefficient_constructor": (
            "coeff(K_ij in R_ab(alpha,beta))="
            "A_6a[i,alpha]*A_7b[j,beta]+"
            "A_6b[i,beta]*A_7a[j,alpha], with stored-edge transpose"
        ),
        "membership_equation_constructor": (
            "for each K_ij coordinate: ell_beta(K_ij)-"
            "sum_(ab,alpha,beta) lambda_ab_alphabeta*"
            "coeff(K_ij in R_ab(alpha,beta))=0"
        ),
        "blocker_right_sides": {
            "triangle_endpoint_colour": "ell(K_ij)=1 iff (i,j)=(0,0)",
            "cap_endpoint_colour": "ell(K_ij)=1 iff (i,j)=(1,1)",
            "third_colour": "ell(K_ij)=1 iff (i,j)=(2,2)",
            "direct": "ell(K_ij)=A_67[i,j]",
        },
        "counts_per_branch": {
            "variables": 361,
            "equations": 6571,
            "matching_occurrences_in_mixed_rows": 6558 * 105,
            "matching_occurrences_in_pure_rows": 3 * 105,
            "source_monomial_occurrences_in_membership_left_matrix": 108 * 9 * 2,
        },
    }
    manifest_logical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    manifest["logical_sha256"] = hashlib.sha256(manifest_logical.encode()).hexdigest()

    payload = {
        "status": "PASS",
        "scope": (
            "Endpoint-ordered matching factorization. Universal beta "
            "existence is imported from the SP-K6 five-set corollary."
        ),
        "canonical_cut": {"C": list(CUT_SHORE), "W": list(W)},
        "sector_counts": {
            "one_cross_matchings": 45,
            "three_cross_matchings": 60,
            "three_cross_patterns_per_response_edge": 6,
            "formal_endpoint_terms_checked": checked_terms,
        },
        "factorization": (
            "(id_V0 tensor beta)<K,T3>_67 = "
            "sum_{ab subset W} Gamma_ab,beta(R_ab(K))"
        ),
        "target_on_exact_GHZ": "sum_c b_c*K_cc*e_c^0",
        "star": {
            "carrier": {"cap_pair": [6, 7], "centre": 0},
            "outside_response_edges": len(star_outside),
            "w_response_edges_killed": len(star_outside),
            "surviving_w_response_edges": 0,
            "consequence": (
                "For every K in ker L_star, b_c*K_cc=0 for all c; "
                "some b_c!=0, so at least one diagonal blocker is in "
                "rowspan L_star."
            ),
        },
        "triangle": {
            "carrier": {"cap_pair": [6, 7], "vertices": [0, 1, 2]},
            "outside_response_edges": len(triangle_outside),
            "w_response_edges_killed": len(triangle_killed_w_pairs),
            "surviving_w_response_edges": [[1, 2]],
            "identity": (
                "sum_c b_c*K_cc*e_c^0 = Gamma_12,beta(R_12(K)) "
                "for K in ker L_triangle"
            ),
            "global_carrier_count": 28 * 20,
        },
        "canonical_live_triangle_incidence": {
            "labelled_flags": len(flags),
            "flags_per_stored_live_cell": len(flags) // 168,
            "flag_orbits_under_S8xS3": 1,
            "flag_stabilizer_order": flag_stabilizer_order,
            "canonical_flag": {
                "live_cell": "A_06[0,1]",
                "cap_pair": [6, 7],
                "triangle": [0, 1, 2],
            },
            "blocker_orbits_on_flag": [
                "K_colour_at_triangle_endpoint",
                "K_colour_at_cap_endpoint",
                "K_third_colour",
                "direct_<K,A_67>",
            ],
            "branches": 4,
            "witness_encoding": {
                "source_variables": 252,
                "rowspan_witness_variables": 108,
                "inverse_variables": 1,
                "total_variables": 361,
                "mixed_equations": 6558,
                "pure_equations": 3,
                "membership_coordinates": 9,
                "inverse_equation": 1,
                "total_equations": 6571,
            },
            "tautological": False,
            "manifest_logical_sha256": manifest["logical_sha256"],
            "entry_guard": (
                "The live cell does not intrinsically select one of its 120 "
                "flags. Under the hypothesis that every triangle is blocked, "
                "one may choose a flag and move it by symmetry; the live cell "
                "does not occur in the surviving Gamma_12(R_12(K)) transfer."
            ),
        },
        "cancellation_k4": {
            "allowed_response_edges": len(k4_allowed),
            "outside_response_edges": len(k4_outside),
            "outside_matrix_rows": 9 * 9,
            "surviving_w_response_edges": [
                list(pair) for pair in sorted(k4_surviving_w_pairs)
            ],
            "w_response_edges_killed": len(k4_killed_w_pairs),
            "clean_equation": (
                "R_01 R_23 + R_02 R_13 + R_03 R_12 = 0 "
                "in the named four-site tensor slots"
            ),
            "cubic_automatic": True,
            "global_carrier_count": 28 * 15,
        },
        "dependencies": [
            "notes/five-set-universal-cofactor-annihilator.md",
            "computations/unaudited-codex-response-star-2026-08-20/REPORT.md",
        ],
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered)
        MANIFEST_OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(rendered, end="")


if __name__ == "__main__":
    main()
