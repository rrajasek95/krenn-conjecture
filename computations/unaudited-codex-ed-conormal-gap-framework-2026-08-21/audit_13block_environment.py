#!/usr/bin/env python3
"""Exact 13-block cap-pair environment and local KKT counterguard."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_blockwise_minimum_norm import (  # noqa: E402
    amplitudes, derivative_columns, in_sparse_rowspan, oriented,
    source_row, sparse_row_basis, require,
)


OUT = HERE / "results_13block_environment.json"
SITES = tuple(range(8))
COLOURS = tuple(range(3))
P, Q = 0, 1
RESIDUAL = tuple(range(2, 8))
LOCAL_EDGES = ((P, Q),) + tuple((P, a) for a in RESIDUAL) + tuple(
    (Q, a) for a in RESIDUAL)
LOCAL_LABELS = tuple((u, v, i, j) for u, v in LOCAL_EDGES
                     for i in COLOURS for j in COLOURS)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return

    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def hafnian(source, word, vertices):
    value = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for u, v in matching:
            term *= oriented(source, u, v, word[u], word[v])
        value += term
    return value


def local_decomposition(source, word):
    direct = oriented(source, P, Q, word[P], word[Q]) * hafnian(
        source, word, RESIDUAL)
    cross = Fraction(0)
    for a, b in combinations(RESIDUAL, 2):
        remaining = tuple(v for v in RESIDUAL if v not in (a, b))
        h4 = hafnian(source, word, remaining)
        rho = (
            oriented(source, P, a, word[P], word[a])
            * oriented(source, Q, b, word[Q], word[b])
            + oriented(source, P, b, word[P], word[b])
            * oriented(source, Q, a, word[Q], word[a])
        )
        cross += h4 * rho
    return direct + cross


def deterministic_source():
    source = {}
    for u, v in combinations(SITES, 2):
        for i in COLOURS:
            for j in COLOURS:
                # Dense small rational control, including signs and zeros.
                numerator = ((17 * u + 11 * v + 5 * i + 3 * j) % 5) - 2
                source[u, v, i, j] = Fraction(numerator, 3)
    return source


def decomposition_audit():
    source = deterministic_source()
    mismatches = []
    for word in product(COLOURS, repeat=8):
        actual = hafnian(source, word, SITES)
        rebuilt = local_decomposition(source, word)
        if actual != rebuilt:
            mismatches.append((word, actual, rebuilt))
    require(not mismatches, mismatches[:1])
    direct_matchings = tuple(perfect_matchings(RESIDUAL))
    cross_matchings = sum(
        sum(1 for _ in perfect_matchings(
            tuple(v for v in RESIDUAL if v not in (a, b))))
        for a in RESIDUAL for b in RESIDUAL if a != b)
    require(len(direct_matchings) == 15 and cross_matchings == 90,
            (len(direct_matchings), cross_matchings))
    return {
        "words_replayed": 3 ** 8,
        "perfect_matching_partition": {
            "direct_pq_times_H6": 15,
            "ordered_p_star_q_star_times_H4": 90,
            "total": 105,
        },
        "all_literal_coefficients_agree": True,
    }


def dense_rank(rows):
    sparse = [{index: value for index, value in enumerate(row) if value}
              for row in rows]
    return len(sparse_row_basis(sparse))


def response_row(source, a, b, alpha, beta):
    return [
        oriented(source, P, a, i, alpha)
        * oriented(source, Q, b, j, beta)
        + oriented(source, P, b, i, beta)
        * oriented(source, Q, a, j, alpha)
        for i in COLOURS for j in COLOURS]


def activity_rows(source):
    rows = []
    for colour in COLOURS:
        row = [Fraction(0)] * 9
        row[3 * colour + colour] = 1
        rows.append(row)
    rows.append([oriented(source, P, Q, i, j)
                 for i in COLOURS for j in COLOURS])
    return rows


def carrier_membership(source, kind, carrier):
    if kind == "star":
        allowed = {edge for edge in combinations(RESIDUAL, 2)
                   if carrier in edge}
    else:
        allowed = set(combinations(tuple(carrier), 2))
    rows = [response_row(source, a, b, alpha, beta)
            for a, b in combinations(RESIDUAL, 2) if (a, b) not in allowed
            for alpha in COLOURS for beta in COLOURS]
    rank = dense_rank(rows)
    memberships = [dense_rank(rows + [functional]) == rank
                   for functional in activity_rows(source)]
    return rank, memberships


def diagonal_counterguard():
    layers = {
        0: ((0, 1), (2, 3), (4, 5), (6, 7)),
        1: ((0, 2), (1, 3), (4, 6), (5, 7)),
        2: ((0, 3), (1, 4), (2, 7), (5, 6)),
    }
    source = {edge + (colour, colour): Fraction(1)
              for colour, matching in layers.items() for edge in matching}
    columns = derivative_columns(source, 8)
    label_index = {label: index for index, label in enumerate(LOCAL_LABELS)}
    rows = []
    for word in product(COLOURS, repeat=8):
        row = {label_index[label]: columns[label].get(word, 0)
               for label in LOCAL_LABELS if columns[label].get(word, 0)}
        rows.append(row)
    basis = sparse_row_basis(rows)
    local_source = source_row(source, LOCAL_LABELS)
    stationary = in_sparse_rowspan(basis, local_source)
    require(len(basis) == 106 and stationary, (len(basis), stationary))

    # The literal multiplier is one on each of the three pure words.
    pure_words = {(colour,) * 8 for colour in COLOURS}
    normal = {}
    for label in LOCAL_LABELS:
        normal[label_index[label]] = sum(
            columns[label].get(word, 0) for word in pure_words)
    normal = {index: value for index, value in normal.items() if value}
    require(normal == local_source, (normal, local_source))

    star_rank, star_membership = carrier_membership(source, "star", 2)
    triangle = (2, 3, 5)
    triangle_rank, triangle_membership = carrier_membership(
        source, "triangle", triangle)
    require((star_rank, star_membership) ==
            (1, [False, False, True, False]),
            (star_rank, star_membership))
    require((triangle_rank, triangle_membership) ==
            (2, [False, False, True, False]),
            (triangle_rank, triangle_membership))

    # Exact linear counterguard: local stationarity means every local J-kernel
    # vector has zero source pairing. There are 11 such directions.
    kernel_dimension = len(LOCAL_LABELS) - len(basis)
    require(kernel_dimension == 11, kernel_dimension)
    return {
        "source": "canonical second diagonal P=2 equality source",
        "target_scope": "hostile guard: five outputs, not the GHZ fibre",
        "local_variables": len(LOCAL_LABELS),
        "local_J_rank": len(basis),
        "local_kernel_dimension": kernel_dimension,
        "rank_after_adjoining_local_source_row": len(basis),
        "literal_multiplier": "lambda_00000000=lambda_11111111=lambda_22222222=1",
        "normal_equations_hold_cell_by_cell": True,
        "star_branch": {"pair": [P, Q], "centre": 2,
                        "response_rank": star_rank,
                        "membership_diag0_diag1_diag2_direct": star_membership},
        "triangle_branch": {"pair": [P, Q], "triangle": list(triangle),
                            "response_rank": triangle_rank,
                            "membership_diag0_diag1_diag2_direct":
                                triangle_membership},
        "nonzero_norm_pairing_tangent_exists": False,
        "counterguard": (
            "Both a canonical star blocker and a canonical triangle blocker "
            "coexist with the bare-fibre 13-block normal equations, but every local "
            "fibre tangent v obeys <A_local,v>=0. Blocker membership therefore "
            "does not itself manufacture the desired tangent. The GHZ mixed-"
            "row equations must be used to make the normal equations "
            "inconsistent or to construct a second-order integrable pair."
        ),
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-decomposition", action="store_true")
    args = parser.parse_args()
    decomposition = decomposition_audit()
    if args.mutate_decomposition:
        decomposition["perfect_matching_partition"]["total"] = 104
    require(decomposition["perfect_matching_partition"]["total"] == 105,
            decomposition)
    guard = diagonal_counterguard()
    payload = {
        "status": "PASS exact 13-block decomposition; blocker-to-tangent implication falsified locally",
        "environment": {
            "pair": [P, Q], "residual_sites": list(RESIDUAL),
            "fixed_residual_residual_blocks": 15,
            "variable_blocks": "A_pq plus six p-stars plus six q-stars",
            "block_count": 13, "scalar_cell_count": len(LOCAL_LABELS),
        },
        "exact_decomposition": (
            "For endpoint word (i,j), F_ij = A_pq[i,j]*H6 + "
            "sum_(a<b,alpha,beta) H4_(R\\{a,b}) * "
            "rho_ab^(alpha,beta)(E_ij), where rho is the two star-product "
            "sum. The map has degree one in A_pq and degree two in the stars."
        ),
        "decomposition_audit": decomposition,
        "real_KKT_normal_equations": {
            "objective": "(1/2)(||A_pq||^2+sum_a||A_pa||^2+sum_a||A_qa||^2)",
            "direct": "A_pq[i,j]=sum_u conjugate(H6[u])*lambda[i,j,u]",
            "p_star": (
                "A_pa[i,alpha]=sum_(b!=a,j,beta,u) "
                "conjugate(A_qb[j,beta]*H4[u])*lambda[i,j,alpha,beta,u]"
            ),
            "q_star": "the endpoint-swapped analogue of the p-star equation",
            "realification": "all equalities use the real inner product Re<.,.>",
            "bare_full_fibre": "alpha*A_local=J_local^*lambda; alpha=0 retained separately",
            "fixed_no_cap_stratum": (
                "If local incidence/rank-chart equalities are g=0, the correct "
                "equation is alpha*A_local=J_local^*lambda+Dg_local^*mu. "
                "Pivot nonvanishing is an open condition; its rank-drop "
                "boundary is not part of the attained interior chart."
            ),
        },
        "rho_order": (
            "rho is exactly the coefficient of the H4 complementary split "
            "and the mixed P-star/Q-star second derivative. It is not a row "
            "of the first derivative T_pq."
        ),
        "canonical_star_triangle_counterguard": guard,
        "terminal_conclusion": (
            "The 13-block localization correctly places rho, but one blocker "
            "membership plus correctly stated attained-interior normal equations "
            "cannot yield a stratum-preserving first-order tangent with nonzero "
            "norm pairing: KKT excludes it by definition. The live task is to "
            "show the GHZ+incidence KKT system inconsistent (possibly using "
            "rho at second order). If the stratum infimum is not attained, "
            "finite active-cap/rank-drop boundary and infinity are separate cases."
        ),
        "scope_guard": (
            "The unconstrained full exact-fibre norm minimum may lie on an "
            "active-cap source and does not preserve a hypothetical no-cap "
            "point. Likewise, deleting an invisible cell is valid on a fixed "
            "no-cap stratum only if the deletion path preserves its incidence "
            "and live-rank conditions."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("decomposition words", decomposition["words_replayed"])
    print("local rank/kernel", guard["local_J_rank"],
          guard["local_kernel_dimension"])
    print("star/triangle masks", guard["star_branch"], guard["triangle_branch"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
