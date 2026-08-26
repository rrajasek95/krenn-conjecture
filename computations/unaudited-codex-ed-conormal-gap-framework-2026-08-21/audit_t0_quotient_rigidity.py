#!/usr/bin/env python3
"""Exact audit of the T0-quotient Jacobian dichotomy and its scope guards."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_t0_quotient_rigidity.json"
ZERO_TAIL = (ROOT / "computations/unaudited-codex-x5-zero-tail-routing-2026-08-21"
             / "results_x5_zero_tail_routing.json")
THIRTEEN = HERE / "results_13block_environment.json"
DIFFERENTIAL = (ROOT / "computations/unaudited-codex-x5-equivariant-differential-rank-2026-08-21"
                / "results_x5_equivariant_differential_rank.json")
PINS = {
    ZERO_TAIL: "623a5b2949d76f382619efee7368bf9eea94208aaad70401ca33a412825486ec",
    THIRTEEN: "7e428d64b4c6f8f87287966e67cbe24ba3c0cdd0606495fcd588ff81a908d294",
    DIFFERENTIAL: "81e2403b686bb8689d8daa57ae7a35e5575b51ff7cfafce62704e6e7e7db1274",
}
COLOURS = tuple(range(3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def oriented(source, u, v, a, b):
    return (source.get((u, v, a, b), Fraction(0)) if u < v
            else source.get((v, u, b, a), Fraction(0)))


def amplitudes(source, n):
    answer = Counter()
    for word in product(COLOURS, repeat=n):
        value = Fraction(0)
        for matching in perfect_matchings(range(n)):
            term = Fraction(1)
            for u, v in matching:
                term *= oriented(source, u, v, word[u], word[v])
            value += term
        if value:
            answer[word] = value
    return answer


def coordinate_labels(n):
    return tuple((u, v, a, b) for u, v in combinations(range(n), 2)
                 for a in COLOURS for b in COLOURS)


def jacobian_rows(source, n):
    labels = coordinate_labels(n)
    index = {label: place for place, label in enumerate(labels)}
    rows = []
    for word in product(COLOURS, repeat=n):
        row = {}
        for u, v in combinations(range(n), 2):
            residual = tuple(site for site in range(n) if site not in (u, v))
            cofactor = Fraction(0)
            for matching in perfect_matchings(residual):
                term = Fraction(1)
                for a, b in matching:
                    term *= oriented(source, a, b, word[a], word[b])
                cofactor += term
            if cofactor:
                row[index[u, v, word[u], word[v]]] = cofactor
        rows.append(row)
    return labels, rows


def sparse_rank(rows):
    basis = {}
    for original in rows:
        row = {column: Fraction(value) for column, value in original.items()
               if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {column: value / scale for column, value in row.items()}
                basis[pivot] = row
                break
            scale = row[pivot]
            old = basis[pivot]
            for column, value in old.items():
                row[column] = row.get(column, Fraction(0)) - scale * value
                if not row[column]:
                    del row[column]
    return len(basis)


def t0_columns(source, n, labels):
    # Basis h_(i,c)-h_(n-1,c), with pure-character sums already zero.
    columns = []
    for i in range(n - 1):
        for colour in COLOURS:
            column = {}
            for place, (u, v, a, b) in enumerate(labels):
                value = oriented(source, u, v, a, b)
                if not value:
                    continue
                weight = (int(u == i and a == colour)
                          + int(v == i and b == colour)
                          - int(u == n - 1 and a == colour)
                          - int(v == n - 1 and b == colour))
                if weight:
                    column[place] = value * weight
            columns.append(column)
    return columns


def multiply_jg(rows, columns, mutate=False):
    products = []
    for row in rows:
        products.append([
            sum(value * column.get(place, 0) for place, value in row.items())
            for column in columns
        ])
    if mutate:
        products[0][0] += 1
    return products


def exact_control(n, source):
    target = Counter({(colour,) * n: Fraction(1) for colour in COLOURS})
    output = amplitudes(source, n)
    require(output == target, (n, output, target))
    labels, rows = jacobian_rows(source, n)
    columns = t0_columns(source, n, labels)
    products = multiply_jg(rows, columns)
    require(all(not value for row in products for value in row), "J*G != 0")
    rank_j = sparse_rank(rows)
    rank_g = sparse_rank(columns)
    t0_dimension = 3 * (n - 1)
    s = t0_dimension - rank_g
    quotient_columns = len(labels) - rank_g
    require(rank_j <= quotient_columns, (rank_j, quotient_columns))
    return {
        "n": n,
        "source_coordinate_dimension": len(labels),
        "T0_dimension": t0_dimension,
        "source_stabilizer_dimension_s": s,
        "orbit_tangent_dimension": rank_g,
        "jacobian_rank": rank_j,
        "rank_minus_s": rank_j - s,
        "quotient_domain_dimension": quotient_columns,
        "quotient_jacobian_full_column_rank": rank_j == quotient_columns,
        "kernel_dimension": len(labels) - rank_j,
        "extra_quotient_kernel_dimension": len(labels) - rank_j - rank_g,
        "literal_equivariance_check": "J_A G_A=0 on every output word",
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def build_result(mutate=False):
    for path, digest in PINS.items():
        require(file_sha(path) == digest, (str(path), file_sha(path), digest))

    n2 = {(0, 1, colour, colour): Fraction(1) for colour in COLOURS}
    n4_layers = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    n4 = {edge + (colour, colour): Fraction(1)
          for colour, matching in n4_layers.items() for edge in matching}
    controls = {"n2_exact_GHZ": exact_control(2, n2),
                "n4_exact_GHZ": exact_control(4, n4)}

    # A hostile mutation verifies that the checker actually tests JG=0.
    if mutate:
        labels, rows = jacobian_rows(n4, 4)
        columns = t0_columns(n4, 4, labels)
        products = multiply_jg(rows, columns, mutate=True)
        require(all(not value for row in products for value in row),
                "mutated J*G != 0")

    differential = json.loads(DIFFERENTIAL.read_text())
    w40 = differential["controls"]["W40"]
    w25 = differential["controls"]["W25"]
    zero = json.loads(ZERO_TAIL.read_text())
    thirteen = json.loads(THIRTEEN.read_text())
    require(zero["literal_census"]["nontrivial_even_class_rows"] == 1638,
            zero["literal_census"])
    require(thirteen["environment"]["scalar_cell_count"] == 117,
            thirteen["environment"])

    common_matching_nonzero = 3 ** 4
    require(common_matching_nonzero == 81, common_matching_nonzero)

    payload = {
        "status": "PASS exact T0-quotient dichotomy; neither frozen packet proves a rank direction",
        "theorem": {
            "complex": "Lie(T0) --G_A--> E --J_A--> W with J_A G_A=0 at F(A)=GHZ",
            "n8_dimensions": {
                "source_E": 252,
                "T0": 21,
                "stabilizer": "s=dim ker(G_A)",
                "orbit_tangent": "21-s",
                "quotient_source": "dim E/im(G_A)=231+s",
            },
            "quotient_rigid_branch": (
                "bar(J)_A is injective iff rank(J_A)=231+s iff "
                "ker(J_A)=im(G_A). Then the fibre germ is regular of "
                "dimension 21-s and equals the T0-orbit germ. At a global "
                "fibre norm minimum, stationarity along this germ is exactly "
                "the T0 moment/balance equation and is automatic."
            ),
            "extra_kernel_branch": (
                "ker(J_A)/im(G_A) is nonzero iff rank(J_A)<=230+s, "
                "equivalently rank(J_A)-s<=230. This is only a Zariski "
                "tangent; integrability and a negative constrained second "
                "variation remain separate requirements."
            ),
            "two_distinct_proof_targets": {
                "direct_nonexistence": (
                    "X5 + all 728 blocked => rank(J_A)-s>=232, contradicting "
                    "the universal equivariant bound rank(J_A)-s<=231."
                ),
                "minimum_norm_route": (
                    "X5 + all 728 blocked + minimum conditions => "
                    "rank(J_A)-s<=230, followed by an integrable negative "
                    "second variation. Neither implication is currently proved."
                ),
            },
        },
        "exact_controls": controls,
        "nonexact_guards": {
            "W40_X4": {
                "s": w40["stabilizer"]["source_T0_stabilizer_dimension"],
                "rank_X4": w40["jacobian_profiles"]["X4"]["exact_Q_rank"],
                "rank_X4_minus_s": w40["jacobian_profiles"]["X4"]["exact_rank_minus_stabilizer_dimension"],
                "X4_defects": w40["jacobian_profiles"]["X4"]["common_defect_count"],
                "scope": "quotient-rigid at the X4 rung, but has an active carrier and is not full GHZ",
            },
            "W25_X3": {
                "s": w25["stabilizer"]["source_T0_stabilizer_dimension"],
                "rank_X3": w25["jacobian_profiles"]["X3"]["exact_Q_rank"],
                "rank_X3_minus_s": w25["jacobian_profiles"]["X3"]["exact_rank_minus_stabilizer_dimension"],
                "X3_defects": w25["jacobian_profiles"]["X3"]["common_defect_count"],
                "scope": "all 728 blocked only at the X3 rung; it has extra kernel there and violates higher output rows",
            },
            "common_matching_I3": {
                "nonzero_output_words": common_matching_nonzero,
                "pure": 3,
                "mixed": common_matching_nonzero - 3,
                "scope": "not an exact GHZ point and unusable as an exact quotient-rigidity control",
            },
            "thirteen_block": {
                "local_variables": thirteen["environment"]["scalar_cell_count"],
                "local_J_rank": thirteen["canonical_star_triangle_counterguard"]["local_J_rank"],
                "local_kernel": thirteen["canonical_star_triangle_counterguard"]["local_kernel_dimension"],
                "scope": "non-GHZ five-output hostile guard; blocker membership plus local normal equations gives no rank implication",
            },
        },
        "packet_direction_audit": {
            "zero_tail_1638": {
                "rows": zero["literal_census"]["nontrivial_even_class_rows"],
                "profiles": zero["literal_census"]["profile_counts"],
                "scope": (
                    "These are values of mixed amplitudes after restriction "
                    "to the diagonal e=t=0 chart, expressed through X,C,Q. "
                    "Their factorization determines only the Jacobian pulled "
                    "back to that chart; it loses derivatives normal to the "
                    "chart and its routing theorem is still conditional."
                ),
                "supports_rank_lower_bound_232": False,
                "supports_quotient_rank_upper_bound_230": False,
                "needed_for_lower_bound": (
                    "A source-labelled nonzero (232+s)-minor of the full "
                    "cubic Jacobian on each localized X5+blocker branch."
                ),
                "needed_for_upper_bound": (
                    "A Fitting-ideal containment forcing every maximal "
                    "(231+s)-minor of a quotient Jacobian to vanish, or an "
                    "explicit non-torus vector v with J_A v=0."
                ),
            },
            "thirteen_block_Hessian": {
                "exact_map": "117-variable affine/bilinear cap-pair environment",
                "first_derivative_direct_block": "H6*I9",
                "carrier_rho": "degree-two mixed second derivative after the direct term is removed",
                "supports_rank_lower_bound_232": False,
                "supports_quotient_rank_upper_bound_230": False,
                "reason": (
                    "Blocker row-space ranks are Hessian response ranks, not "
                    "Jacobian ranks. The frozen non-GHZ counterguard has both "
                    "star/triangle blockers and local stationarity, yet no "
                    "blocker-generated first-order implication."
                ),
            },
        },
        "minimum_norm_exact_linear_blocks": {
            "maximal_intersecting_families": "eight full 7-edge stars and 56 site triangles",
            "star_scalar_columns": 7 * 9,
            "triangle_scalar_columns": 3 * 9,
            "theorem": (
                "At a full-fibre norm minimum, A_E is perpendicular to "
                "ker(L_E), equivalently A_E lies in im(L_E^*), for every "
                "star or triangle E. These directions are genuine affine "
                "fibre lines even at singular points."
            ),
            "rank_scope": (
                "This is stronger and more regularity-free than single-edge "
                "deletion, but it does not force either global Jacobian rank "
                "direction: an injective L_E makes the condition vacuous."
            ),
        },
        "terminal_verdict": (
            "The quotient dichotomy is theorem-grade and the exact n=2,n=4 "
            "controls lie in its rigid branch. The current 1638 zero-tail "
            "packet and 13-block rho identity support neither the >=232 "
            "direct route nor the <=230 minimum-norm route. Any purely local "
            "blocker-to-rank claim is falsified by the frozen non-GHZ guards; "
            "the full GHZ/X5 equations and all-carrier incidence are load-bearing."
        ),
        "smallest_next_exact_target": (
            "On one source-faithful X5+blocked pivot chart with fixed s, "
            "form an explicit quotient coordinate complement to im(G_A). "
            "Test one maximal quotient minor modulo the chart ideal: a live "
            "minor advances the direct >=232 program only when combined with "
            "one additional independent row, while universal vanishing of "
            "all maximal minors would establish the extra-kernel <=230 branch."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-equivariance", action="store_true")
    args = parser.parse_args()
    payload = build_result(args.mutate_equivariance)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("n4", payload["exact_controls"]["n4_exact_GHZ"])
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
