#!/usr/bin/env python3
r"""Common-q Euler/two-chart closure of the five rootless ridge classes.

For v in D={1,...,5}, let h_v be the decorated four-site hafnian on
D\{v}.  This checker enlarges the exact response-companion module of
``verify_h3_rootless_five_ridge_response_bianchi_cokernel.py`` by all
literal first/second K4 Euler incidences and, more strongly, by a complete
componentwise identification of the two chart copies.

For each chart and v the source-labelled basis is

    r_v, H_v, A_{v,e}=q_e d_e h_v, B_{v,M}=q_M,

with 1+1+6+3=11 coordinates.  The genuine relations are

    -r_v+B_{v,M},       A_{v,e}-B_{v,M(e)},
    -H_v+sum_M B_{v,M}, -2H_v+sum_e A_{v,e}.

After adjoining every componentwise two-chart difference, the integral
cokernel is still Z^5.  Its v-th primitive functional has weights

    r:1, H:3, A:1, B:1

on both charts.  Thus no existing common-q Euler or two-chart response
identity gives a nonzero relation among the five H_v, or a reduced ridge
augmentation.  This does not exclude a new higher source-resolution/Tor
face outside the displayed identity class.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "2d614b0889a3a76f1786bb31e699fa2fd3574df75ce74a9e86eec41715da5aae"
PINS = {
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
    "computations/verify_h3_pure_unary_cofactor_incidence_attachment.py":
        "3295183db431e14733eceea645a28113eccd086eebbf256afaa7127cc826b8cd",
    "computations/verify_h3_full_nine_connecting_class_rigidity.py":
        "3c2ba4a4101cae9803d5af645ac73ec9f5af36432cface62ff7da34dfe5b1f04",
    "computations/verify_h3_reset_lane_ores_descent_lock.py":
        "5a904ba0537c150d248808a3aa463bd2431b4450239747440a2316f37b5c1e16",
    "computations/verify_h3_single_koszul_cell_face_star_no_go.py":
        "5b94a8b213213ce64dd8536baf638e619a4773a2dfc4a2318e1820742f8f8165",
}

ODD = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
CHARTS = ("D", "L")
ZERO = Q(0)
ONE = Q(1)

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Monomial = tuple[Edge, ...]
Polynomial = Counter[Monomial]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def perfect_matchings(vertices) -> tuple[Matching, ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        remainder = tuple(v for v in vertices if v not in (first, second))
        for tail in perfect_matchings(remainder):
            result.append(((first, second),) + tail)
    return tuple(result)


def hafnian(vertices) -> Polynomial:
    return Counter({tuple(sorted(matching)): ONE
                    for matching in perfect_matchings(vertices)})


def derivative(polynomial: Polynomial, selected: Edge) -> Polynomial:
    answer: Polynomial = Counter()
    for monomial, coefficient in polynomial.items():
        if selected in monomial:
            reduced = list(monomial)
            reduced.remove(selected)
            answer[tuple(reduced)] += coefficient
    return +answer


def multiply_edge(polynomial: Polynomial, selected: Edge) -> Polynomial:
    return Counter({tuple(sorted(monomial + (selected,))): coefficient
                    for monomial, coefficient in polynomial.items()})


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return +answer


def scale(value: int, polynomial: Polynomial) -> Polynomial:
    return Counter({monomial: value * coefficient
                    for monomial, coefficient in polynomial.items()
                    if value * coefficient})


def rank(columns: list[list[int | Q]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def determinant(matrix: list[list[int]]) -> int:
    """Fraction-free Bareiss determinant."""
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant not square")
    work = [row[:] for row in matrix]
    sign = 1
    denominator = 1
    for pivot_index in range(size - 1):
        pivot_row = next((row for row in range(pivot_index, size)
                          if work[row][pivot_index]), None)
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row], work[pivot_index]
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (work[row][column] * pivot
                             - work[row][pivot_index]
                             * work[pivot_index][column])
                require(numerator % denominator == 0,
                        "Bareiss division stopped being exact")
                work[row][column] = numerator // denominator
            work[row][pivot_index] = 0
        denominator = pivot
    return sign * work[-1][-1]


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), ZERO)


def common_q_polynomials():
    """Verify every literal K4 cofactor/Euler identity."""
    records = []
    all_h_supports = []
    for v in ODD:
        face = tuple(site for site in ODD if site != v)
        edges = tuple(combinations(face, 2))
        matchings = perfect_matchings(face)
        h = hafnian(face)
        require(len(edges) == 6 and len(matchings) == len(h) == 3,
                ("K4 census changed", v))

        first = {}
        containing = {}
        for selected in edges:
            lifted = multiply_edge(derivative(h, selected), selected)
            require(len(lifted) == 1, ("edge has non-private K4 route", v, selected))
            matching = next(iter(lifted))
            require(selected in matching and matching in matchings,
                    ("edge route lost its matching", v, selected))
            first[selected] = lifted
            containing[selected] = matching

        first_euler = add(*first.values())
        second = {matching: Counter({matching: ONE}) for matching in matchings}
        second_euler = add(*second.values())
        require(first_euler == scale(2, h), ("first K4 Euler failed", v))
        require(second_euler == h, ("second K4 Euler failed", v))
        require(all(first[selected] == second[containing[selected]]
                    for selected in edges),
                ("incidence-to-matching identity failed", v))

        supports = set(h)
        require(all(set(monomial) and
                    set(site for edge_pair in monomial for site in edge_pair)
                    == set(face) for monomial in supports),
                ("face monomial lost its vertex label", v))
        all_h_supports.append(supports)
        records.append({
            "v": v,
            "decorated_face_word": "".join(str(MIDDLE[site]) for site in face),
            "edges": [list(edge_pair) for edge_pair in edges],
            "matchings": [[list(edge_pair) for edge_pair in matching]
                          for matching in matchings],
            "first_Euler": "sum_e A_(v,e)=2H_v",
            "second_Euler": "sum_M B_(v,M)=H_v",
            "incidences": 6,
        })

    for left, right in combinations(all_h_supports, 2):
        require(left.isdisjoint(right),
                "different deleted-site hafnians share a labelled monomial")
    return records


def toric_independence_guard():
    """A five-cycle specialization proves h_1,...,h_5 independent."""
    cycle = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))
    specialized = []
    exponent_rows = []
    for v in ODD:
        h = hafnian(site for site in ODD if site != v)
        survivor = [monomial for monomial in h
                    if all(edge_pair in cycle for edge_pair in monomial)]
        require(len(survivor) == 1, ("cycle specialization not monomial", v))
        monomial = survivor[0]
        specialized.append(monomial)
        exponent_rows.append([int(edge_pair in monomial) for edge_pair in cycle])
    det = determinant(exponent_rows)
    require(abs(det) == 2, ("cycle exponent determinant changed", det))
    return {
        "nonzero_edges": [list(edge_pair) for edge_pair in cycle],
        "specialized_h": [[list(edge_pair) for edge_pair in monomial]
                          for monomial in specialized],
        "exponent_matrix": exponent_rows,
        "determinant": det,
        "conclusion": "h_1,...,h_5 are algebraically independent over Q",
    }


def sparse_column(dimension, index, entries):
    column = [0] * dimension
    for key, value in entries.items():
        column[index[key]] += value
    return column


def integral_module():
    basis = []
    local_data = {}
    for v in ODD:
        face = tuple(site for site in ODD if site != v)
        edges = tuple(combinations(face, 2))
        matchings = perfect_matchings(face)
        local_data[v] = (edges, matchings)
        for chart in CHARTS:
            basis.append((v, chart, "r", ()))
            basis.append((v, chart, "H", ()))
            basis.extend((v, chart, "A", edge_pair) for edge_pair in edges)
            basis.extend((v, chart, "B", matching) for matching in matchings)
    index = {key: position for position, key in enumerate(basis)}
    dimension = len(basis)
    require(dimension == 110 and len(index) == dimension,
            "five-ridge doubled basis changed")

    relations = []
    selected_relations = []
    relation_counts = Counter()
    for v in ODD:
        edges, matchings = local_data[v]
        matching_for_edge = {
            edge_pair: next(matching for matching in matchings
                            if edge_pair in matching)
            for edge_pair in edges
        }
        for chart in CHARTS:
            key = lambda kind, label=(): (v, chart, kind, label)
            for matching in matchings:
                column = sparse_column(dimension, index, {
                    key("r"): -1,
                    key("B", matching): 1,
                })
                relations.append(column)
                selected_relations.append(column)
                relation_counts["matching_routes"] += 1
            for edge_pair in edges:
                column = sparse_column(dimension, index, {
                    key("A", edge_pair): 1,
                    key("B", matching_for_edge[edge_pair]): -1,
                })
                relations.append(column)
                selected_relations.append(column)
                relation_counts["edge_matching_incidence"] += 1
            second_euler = sparse_column(dimension, index, {
                key("H"): -1,
                **{key("B", matching): 1 for matching in matchings},
            })
            relations.append(second_euler)
            selected_relations.append(second_euler)
            relation_counts["second_Euler"] += 1
            first_euler = sparse_column(dimension, index, {
                key("H"): -2,
                **{key("A", edge_pair): 1 for edge_pair in edges},
            })
            relations.append(first_euler)
            relation_counts["first_Euler"] += 1

        # Grant the strongest possible componentwise comparison of the two
        # source-labelled chart copies.  Actual committed comparison rows
        # form a submodule of this one.
        for kind, label in (("r", ()), ("H", ())):
            relations.append(sparse_column(dimension, index, {
                (v, "L", kind, label): 1,
                (v, "D", kind, label): -1,
            }))
            relation_counts["chart_identifications"] += 1
        for edge_pair in edges:
            relations.append(sparse_column(dimension, index, {
                (v, "L", "A", edge_pair): 1,
                (v, "D", "A", edge_pair): -1,
            }))
            relation_counts["chart_identifications"] += 1
        for matching in matchings:
            relations.append(sparse_column(dimension, index, {
                (v, "L", "B", matching): 1,
                (v, "D", "B", matching): -1,
            }))
            relation_counts["chart_identifications"] += 1

        chart_ridge_difference = sparse_column(dimension, index, {
            (v, "L", "r", ()): 1,
            (v, "D", "r", ()): -1,
        })
        selected_relations.append(chart_ridge_difference)

    require(len(selected_relations) == 105,
            "selected unit-pivot relation count changed")
    selected_rank = rank(selected_relations)
    available_rank = rank(relations)
    require(selected_rank == available_rank == 105,
            ("Euler/chart module rank changed", selected_rank, available_rank))

    covectors = []
    clean = []
    pure_h = []
    for v in ODD:
        covector = [0] * dimension
        for chart in CHARTS:
            covector[index[(v, chart, "r", ())]] = 1
            covector[index[(v, chart, "H", ())]] = 3
            edges, matchings = local_data[v]
            for edge_pair in edges:
                covector[index[(v, chart, "A", edge_pair)]] = 1
            for matching in matchings:
                covector[index[(v, chart, "B", matching)]] = 1
        require(all(dot(covector, column) == 0 for column in relations),
                ("primitive mass failed to kill existing relation", v))
        covectors.append(covector)

        clean_column = sparse_column(dimension, index, {
            (v, "D", "r", ()): -1,
        })
        require(dot(covector, clean_column) == -1,
                ("clean ridge escaped primitive mass", v))
        clean.append(clean_column)

        h_column = sparse_column(dimension, index, {
            (v, "D", "H", ()): 1,
        })
        require(dot(covector, h_column) == 3,
                ("aggregate cofactor lost mass three", v))
        pure_h.append(h_column)

    require(rank(covectors) == 5, "primitive mass functionals lost rank")
    require(rank(relations + clean) == 110,
            "clean ridge augmentations failed to fill cokernel")
    require(rank(relations + pure_h) == 110,
            "five aggregate h classes acquired a relation")

    # Give a solver-independent integral certificate.  The selected 21
    # relation columns in each 22-row v-block plus -r_D form a unimodular
    # square matrix.  Therefore the relation cokernel is torsion-free Z,
    # and the five-site direct sum is Z^5.
    local_determinants = []
    for v in ODD:
        local_rows = [position for position, key in enumerate(basis)
                      if key[0] == v]
        local_columns = [column for column in selected_relations
                         if any(column[row] for row in local_rows)]
        require(len(local_columns) == 21, ("local relation count changed", v))
        local_columns.append(clean[ODD.index(v)])
        square = [[column[row] for column in local_columns]
                  for row in local_rows]
        det = determinant(square)
        require(abs(det) == 1, ("local integral certificate not unimodular", v, det))
        local_determinants.append(det)

    return {
        "ambient_rank": dimension,
        "relation_columns": len(relations),
        "relation_counts": dict(sorted(relation_counts.items())),
        "selected_unit_pivot_columns": len(selected_relations),
        "available_rank": available_rank,
        "rank_with_clean_ridges": rank(relations + clean),
        "rank_with_five_H_classes": rank(relations + pure_h),
        "primitive_cokernel_rank": rank(covectors),
        "local_unimodular_determinants": local_determinants,
        "cokernel": "Z^5",
        "primitive_functional": "lambda_v(r,H,A,B)=(1,3,1,1) on both charts",
        "pure_H_intersection": "relation span intersects span{H_1,...,H_5} in 0",
    }


def main() -> None:
    pin_dependencies()
    polynomials = common_q_polynomials()
    toric = toric_independence_guard()
    module = integral_module()
    ledger = {
        "pins": PINS,
        "odd_word": "12112",
        "common_q_polynomials": polynomials,
        "toric_independence_guard": toric,
        "integral_module": module,
        "readout_scope": {
            "anchor_incidence_of_clean_ridge": -1,
            "w": 0,
            "target": 0,
            "ordinary_residue_required": 0,
        },
        "verdict": (
            "all literal K4 cofactor Euler/incidence relations, even after "
            "complete componentwise two-chart identification, leave the "
            "five companion sums as a primitive Z^5 cokernel"
        ),
        "minimal_new_operation": (
            "a source-labelled higher relative/Tor face with nonzero "
            "lambda_v mass and zero ridge-independent target/w/ordinary-residue"
        ),
        "scope_guard": (
            "complete for the committed common-q K4 Euler/incidence and "
            "literal two-chart comparison class in these five fine degrees; "
            "not a computation of the full nonlinear source resolution"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED", ("pin ledger digest", digest))
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest changed", digest))
    print("h=3 five-ridge common-q Euler/two-chart module: PASS")
    print("available rank 105 in rank-110 module; primitive coker Z^5")
    print("five H classes are independent modulo all displayed identities")
    print("cycle specialization exponent determinant:", toric["determinant"])
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
