#!/usr/bin/env python3
"""Exact bounded audit of the global Wick/apolar/Artinian route at n=8.

This is a census and counterguard, not an elimination of the Krenn fibre.
It uses only the standard library and exact rational arithmetic.
"""

from __future__ import annotations

import argparse
import ast
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb, factorial, prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_global_wick_apolar_survey.json"

PINS = {
    "computations/verify_global_wick_top_invariant_counterguard.py":
        "192c03668e56262315e685f49c29fafeed071faf2a292dfdc94544fd7a5f4183",
    "computations/verify_zeon_lefschetz.py":
        "06b9b42beabf1a96f2a18c0305e32fa3f1b085e628c0f6f951b8699b67d7c0c4",
    "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/results_branch0_dzero_support6_classification.json":
        "83a8977e93d5cbcc0b34741fd83150e02aa510b70969c6e1d91ed2c3adf7eb43",
    "computations/unaudited-codex-root-integration-2026-08-20/results_q_support8_orbit_incompatibility.json":
        "51588968fc737a69faa8134e4c1c27a631a4c9f622e7493fe7ac325053571015",
    "computations/unaudited-codex-tail-idempotent-remote-2026-08-21/results_tail_idempotent_remote.json":
        "b92370d3de3265d9e8840b69fef5871e5114f647bf25427569a77e0b42ff2866",
    "computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21/results_tail_remote_hafnian_contraction.json":
        "37497e633fc5c1b27dbea000b28fa04973b8da7f42294d3049cd73c9e0fc749b",
    "computations/unaudited-x4general-w40-2026-08-20/results_t3.json":
        "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
}

N = 8
COLORS = range(3)
SITES = tuple(range(N))
EDGES = tuple(combinations(SITES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


MATCHINGS = tuple(perfect_matchings(SITES))


def hafnian(weights, vertices=SITES):
    return sum(prod(weights[EDGE_INDEX[edge]] for edge in matching)
               for matching in perfect_matchings(tuple(vertices)))


def exact_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((i for i in range(row, len(work))
                      if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        for i in range(row + 1, len(work)):
            if not work[i][column]:
                continue
            scale = work[i][column] / value
            for j in range(column, width):
                work[i][j] -= scale * work[row][j]
        row += 1
        if row == len(work):
            break
    return row


def scalar_hessian(weights):
    """The 28 by 28 ordinary Hessian of the K8 perfect-matching form."""
    answer = []
    for left in EDGES:
        row = []
        for right in EDGES:
            if set(left) & set(right):
                row.append(Fraction(0))
            else:
                remaining = tuple(v for v in SITES
                                  if v not in left and v not in right)
                row.append(hafnian(weights, remaining))
        answer.append(row)
    return answer


def scalar_value_rank_control(target):
    # Deterministic rational point on Phi_8,4=target.  Only x_01 is solved.
    seed = 1
    weights = [Fraction(1 + ((seed + 3 * k + k * k) % 11))
               for k in range(len(EDGES))]
    distinguished = EDGE_INDEX[(0, 1)]
    weights[distinguished] = Fraction(0)
    rest = hafnian(weights)
    cofactor = hafnian(weights, (2, 3, 4, 5, 6, 7))
    require(cofactor, "chosen scalar cofactor vanished")
    weights[distinguished] = Fraction(target - rest, cofactor)
    require(hafnian(weights) == target, "scalar target solve failed")
    rank = exact_rank(scalar_hessian(weights))
    require(rank == 28, "scalar target value forced Hessian rank drop")
    return {
        "target": target,
        "solved_edge": "01",
        "solved_value": str(weights[distinguished]),
        "ordinary_hessian_rank": rank,
    }


def disjointness_matrix(n, k):
    subsets = tuple(combinations(range(n), k))
    return [[int(set(left).isdisjoint(right)) for right in subsets]
            for left in subsets]


def parse_fraction(value):
    return Fraction(value)


def load_w40():
    path = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
    raw = json.loads(path.read_text())["engine_audit"]["witness_B_integral"]["source"]
    source = {}
    for key, block in raw.items():
        edge = tuple(ast.literal_eval(key))
        source[edge] = [[parse_fraction(entry) for entry in row] for row in block]
    require(set(source) == set(EDGES), "W40 edge set changed")
    return source


def dense_source():
    return {
        edge: [[Fraction(1 + ((index + i + 2 * j + i * j) % 13))
                for j in COLORS] for i in COLORS]
        for index, edge in enumerate(EDGES)
    }


def b1_to_b3_rank(source):
    """Exact rank of multiplication by q from B_1 to B_3."""
    columns = tuple((site, color) for site in SITES for color in COLORS)
    rows = tuple((support, colors)
                 for support in combinations(SITES, 3)
                 for colors in product(COLORS, repeat=3))
    row_index = {row: index for index, row in enumerate(rows)}
    matrix = [[Fraction(0) for _ in columns] for _ in rows]
    for column, (site, color) in enumerate(columns):
        for left, right in EDGES:
            if site in (left, right):
                continue
            support = tuple(sorted((site, left, right)))
            for a, b in product(COLORS, repeat=2):
                assignment = {site: color, left: a, right: b}
                row = (support, tuple(assignment[v] for v in support))
                matrix[row_index[row]][column] += source[(left, right)][a][b]
    return exact_rank(matrix)


def remote_singleton_minor():
    """Find a literal 24 by 24 diagonal lambda minor for the remote point."""
    exceptional = {
        (0, 1, 0, 2): "1",
        (6, 7, 1, 2): "1",
        (0, 6, 0, 1): "-1/(5lambda)",
        (0, 1, 0, 1): "1/(5lambda)",
        (6, 7, 1, 0): "1/(5lambda)",
    }

    def cell(u, v, a, b):
        if u > v:
            u, v, a, b = v, u, b, a
        if a == b:
            return "lambda"
        return exceptional.get((u, v, a, b))

    columns = tuple((site, color) for site in SITES for color in COLORS)
    witnesses = {}
    for support in combinations(SITES, 3):
        for colors in product(COLORS, repeat=3):
            assignment = dict(zip(support, colors))
            vector = []
            for site, color in columns:
                value = None
                if site in support and assignment[site] == color:
                    left, right = (v for v in support if v != site)
                    value = cell(left, right,
                                 assignment[left], assignment[right])
                vector.append(value)
            nonzero = [index for index, value in enumerate(vector) if value]
            if (len(nonzero) == 1 and vector[nonzero[0]] == "lambda"
                    and nonzero[0] not in witnesses):
                witnesses[nonzero[0]] = [list(support), list(colors)]
    require(len(witnesses) == 24, "remote singleton minor lost a column")
    return {
        "rank": 24,
        "minor": "lambda^24",
        "rows_by_column": [witnesses[index] for index in range(24)],
        "field_guard": "105*lambda^4=1, hence lambda^24!=0",
    }


def laurent_n8_boundary():
    # Reconstruct the first vertex-to-triangle expansion of the prism seed.
    edges = {
        (0, 3): (0, 1), (1, 2): (0, -1), (4, 5): (0, 0),
        (1, 4): (1, 0), (0, 2): (1, 0), (3, 5): (1, 0),
        (2, 5): (2, 0), (0, 1): (2, 0), (3, 4): (2, 0),
    }
    vertex = 0
    incident = []
    for edge, (color, valuation) in edges.items():
        if vertex in edge:
            neighbor = edge[1] if edge[0] == vertex else edge[0]
            incident.append((color, neighbor, valuation))
    triangle = {color: 6 + color for color in COLORS}
    expanded = {edge: data for edge, data in edges.items() if vertex not in edge}
    for color, neighbor, valuation in incident:
        expanded[tuple(sorted((neighbor, triangle[color])))] = (color, valuation)
    for missing in COLORS:
        other = [color for color in COLORS if color != missing]
        expanded[tuple(sorted((triangle[other[0]], triangle[other[1]])))] = (missing, 0)
    vertices = tuple(range(1, 9))
    terms = []
    for matching in perfect_matchings(vertices):
        if not all(edge in expanded for edge in matching):
            continue
        word = {}
        valuation = 0
        for edge in matching:
            color, exponent = expanded[edge]
            valuation += exponent
            word[edge[0]] = word[edge[1]] = color
        terms.append((tuple(word[v] for v in vertices), valuation))
    terms.sort()
    require(len(terms) == 5, "n=8 Laurent boundary matching count changed")
    require(sum(value == 0 for _, value in terms) == 3,
            "n=8 Laurent boundary target head changed")
    require(all(value >= 0 for _, value in terms),
            "n=8 Laurent output acquired a pole")
    return [["".join(map(str, word)), valuation] for word, valuation in terms]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = file_sha(ROOT / relative)
        require(observed == expected, (relative, observed, expected))

    require(len(MATCHINGS) == 105, "K8 perfect matching count changed")
    b_dimensions = [comb(N, degree) * 3**degree for degree in range(N + 1)]
    require(b_dimensions == [1, 24, 252, 1512, 5670, 13608, 20412, 17496, 6561],
            "B Hilbert census changed")
    moment_dimensions = [comb(N, degree) * 3**degree
                         for degree in range(0, N + 1, 2)]
    require(moment_dimensions == [1, 252, 5670, 20412, 6561],
            "even moment census changed")

    # Degree-two apolar relations of the scalar K8 matching polynomial.
    symmetric_quadrics = comb(len(EDGES) + 1, 2)
    squares = len(EDGES)
    incident_pairs = N * comb(N - 1, 2)
    matching_differences = 2 * comb(N, 4)
    annihilator_degree_two = squares + incident_pairs + matching_differences
    require((symmetric_quadrics, annihilator_degree_two,
             symmetric_quadrics - annihilator_degree_two) == (406, 336, 70),
            "degree-two matching apolar census changed")
    numata_hilbert = [1, 28, 70, 28, 1]

    # Target intrinsic apolar algebra and its strongest possible quadratic maps.
    target_hilbert = [1] + [3 * comb(N, degree) for degree in range(1, N)] + [1]
    require(target_hilbert == [1, 24, 84, 168, 210, 168, 84, 24, 1],
            "target apolar Hilbert series changed")
    target_quadratic_ranks = [1]
    for degree in range(1, 5):
        matrix = disjointness_matrix(N, degree)
        require(exact_rank(matrix) == comb(N, degree),
                ("target disjointness rank", degree))
        target_quadratic_ranks.append(3 * comb(N, degree))
    require(target_quadratic_ranks == [1, 24, 84, 168, 210],
            "target quadratic Lefschetz ranks changed")

    scalar_controls = [scalar_value_rank_control(0),
                       scalar_value_rank_control(1)]
    require([entry["solved_value"] for entry in scalar_controls] ==
            ["-62875/1852", "-125749/3704"],
            "scalar Hessian control values changed")

    w40_rank = b1_to_b3_rank(load_w40())
    dense_rank = b1_to_b3_rank(dense_source())
    require((w40_rank, dense_rank) == (24, 24),
            "source multiplication control ranks changed")
    remote_rank = remote_singleton_minor()

    payload = {
        "status": "PASS exact global Wick/apolar negative survey",
        "artinian_encoding": {
            "algebra": "B=tensor_i(C+V_i), V_i^2=0, dim(V_i)=3",
            "hilbert_dimensions": b_dimensions,
            "q_dimension": b_dimensions[2],
            "top_dimension": b_dimensions[8],
            "identity": "[exp(q)]_8=q^4/4!=H_8(A)",
            "generic_top_monomials_per_word": len(MATCHINGS),
            "full_even_moment_dimensions": moment_dimensions,
            "full_even_moment_total": sum(moment_dimensions),
        },
        "representation_census": {
            "source": "direct_sum_(i<j) V_i tensor V_j; dimension 252",
            "target": "tensor_i V_i; dimension 6561",
            "map_degree": 4,
            "site_colour_weight": "wt(H_w)=product_i lambda_(i,w_i)",
            "linear_output_identities": 0,
            "reason": "tensor_i V_i is irreducible for product_i GL(V_i)",
        },
        "lowest_apolar_candidate": {
            "degree": 2,
            "operator": "d_M-d_M' for two 2-matchings M,M' on the same four sites",
            "scalar_matching_apolar_hilbert": numata_hilbert,
            "degree_two_census": {
                "ambient_symmetric_quadrics": symmetric_quadrics,
                "edge_squares": squares,
                "incident_edge_products": incident_pairs,
                "four_site_matching_differences": matching_differences,
                "annihilator_dimension": annihilator_degree_two,
                "quotient_dimension": 70,
            },
            "verdict": (
                "It annihilates every scalar coordinate polynomial H_w(A), "
                "but is not an equation in the output coordinates. "
                "Differentiating H_w(A)=delta_w at one fibre point is invalid."
            ),
        },
        "numata_scope": {
            "theorem_used": (
                "The apolar algebra of the K8 size-4 matching generating "
                "polynomial is strong Lefschetz; Hilbert vector [1,28,70,28,1]."
            ),
            "source_fibre_guard": (
                "Strong Lefschetz concerns the generic matching polynomial "
                "as a polynomial in edge variables, not a common root of the "
                "6561 coloured coefficient equations."
            ),
            "exact_value_controls": scalar_controls,
        },
        "target_intrinsic_apolar_test": {
            "hilbert": target_hilbert,
            "quadratic_element": "Theta=sum_(c,i<j) z_(ij,c)=L^2/2",
            "ranks_Theta^(4-k)_Gk_to_G(8-k)": target_quadratic_ranks,
            "Theta_fourth_socle_coefficient": 3 * factorial(8) // 2**4,
            "ordinary_hessian_det_at_ones": -343,
            "verdict": "maximal strong-Lefschetz/Jordan/Hessian pattern; no obstruction",
        },
        "source_multiplication_controls": {
            "map": "mu_q:B_1(24)->B_3(1512)",
            "W40_active_cap_rank": w40_rank,
            "dense_all_blocked_rank": dense_rank,
            "remote_counterpoint": remote_rank,
            "verdict": (
                "The first lower multiplication rank is maximal on an active "
                "cap source, an all-blocked source, and the remote counterpoint; "
                "it cannot detect clean-cap activity."
            ),
        },
        "family_evaluation_ledger": {
            "support6": (
                "The frozen artifact is a reduced diagonal/Q coefficient "
                "family. Every completion is still q in B_2, so the universal "
                "degree-two apolar operators vanish termwise; it does not "
                "supply a full 252-coordinate q for numerical mu_q ranks."
            ),
            "support8": (
                "The frozen artifact contains only a Q-support orbit, not "
                "coefficients. Universal Wick/apolar identities hold on every "
                "completion, but numerical Hessian/multiplication evaluation "
                "is not defined from that artifact."
            ),
            "W40_positive": "exact mu_q B1->B3 rank 24; active cap",
            "dense_positive": "exact mu_q B1->B3 rank 24; every carrier blocked",
            "remote_counterpoint": (
                "exact diagonal lambda^24 minor, with 105lambda^4=1; "
                "the point fails 138/360 of the 332 rows"
            ),
        },
        "top_only_closure_counterguard": {
            "n8_laurent_terms": laurent_n8_boundary(),
            "statement": (
                "A punctured Laurent family has output Delta_8,3 plus "
                "positive-t terms and nonsingular covariance. Therefore every "
                "polynomial top-output Wick-variety/catalecticant identity and "
                "every rational one regular at Delta also holds at Delta."
            ),
        },
        "ranked_verdict": [
            "TOP-ONLY polynomial/differential elimination: impossible by Laurent closure.",
            "INTRINSIC target apolar/Jordan/Hessian: false lead; target is maximally Lefschetz.",
            "NUMATA scalar matching apolarity: organizational only; target values 0 and 1 both admit full Hessian rank 28.",
            "GLOBAL low multiplication rank: false lead at degree one; active, blocked, and remote controls all have rank 24.",
            "SURVIVING lane: a relative identity for (q,q^2,q^3,q^4) retaining labelled edge/site incidence and a carrier response block; this is not supplied by current apolar theory.",
        ],
    }
    payload["input_hashes"] = PINS
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("global Wick/apolar Artinian survey: PASS")
    print("B dims:", b_dimensions)
    print("degree-2 apolar: 406 -> 70, annihilator 336")
    print("target Theta ranks:", target_quadratic_ranks)
    print("mu_q B1->B3 controls W40/dense/remote: 24/24/24")
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
