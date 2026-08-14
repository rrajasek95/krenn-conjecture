#!/usr/bin/env python3
"""Identify every hyperbolic collision residual with one standard module.

Fix a missing vertex a and a doubled vertex b.  The remaining m vertices
index the two neighbours of b in a collision monomial.  A coordinate-linear
transvection a->b with weights c_u produces coefficient c_u+c_v on a
collision whose two b-neighbours are u,v.  The residual matching tail is
irrelevant.  Thus the complete collision sector is controlled by the
signless vertex-edge incidence map of K_m.

Over characteristic zero this map has rank m.  Its constant vertex line is
the symmetric collision row and its augmentation-zero subspace is an
(m-1)-dimensional standard module.  The physical root residual is the image
of e_0-e_1.  At h=3 (m=6) it has twelve +1 and twelve -1 terms, exactly the
splitter in the pinned collision audit.

The calculation also proves a uniform no-go: no completion by further
coordinate-linear endpoint transvections can make the complete response
tangent, even modulo the symmetric collision row, while retaining the two
prescribed local root coefficients +1,-1.  A positive repair must therefore
be occurrence-dependent (or a higher Tate/PP comparison), not another
ordinary site transvection.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py":
        "b8d02d77213bbb21d68dbad0aa4d6d1263625de012e413547723999d8d87fada",
}
EXPECTED_LEDGER_SHA256 = (
    "4d2c766d7ab263c368d7b336e81a8a08ca31aecdb0b67b0abe75bae680a2b247"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or rows[row][column] == 0:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def incidence_audit(m: int) -> dict[str, object]:
    require(m >= 4 and m % 2 == 0, m)
    pairs = tuple(combinations(range(m), 2))
    tails_per_pair = odd_double_factorial(m - 3)
    # All tail copies of one neighbour pair are identical columns.  Work on
    # the compressed pair module and restore tail multiplicities in counts
    # and pairings; this keeps the uniform audit small even at large order.
    coordinates = pairs

    columns = tuple(
        tuple(Q(int(vertex in pair)) for pair in coordinates)
        for vertex in range(m)
    )
    require(rank(columns) == m,
            ("signless K_m incidence rank changed", m, rank(columns)))

    constant = tuple(Q(1) for _ in coordinates)
    symmetric = tuple(Q(2) for _ in coordinates)
    ones_image = tuple(sum(column[row] for column in columns)
                       for row in range(len(coordinates)))
    require(ones_image == symmetric,
            ("constant vertex line stopped giving symmetric collision", m))

    standard_basis = tuple(
        tuple(columns[vertex][row] - columns[m - 1][row]
              for row in range(len(coordinates)))
        for vertex in range(m - 1)
    )
    require(rank(standard_basis) == m - 1
            and rank((symmetric,) + standard_basis) == m,
            ("trivial plus standard decomposition changed", m))
    require(all(dot(vector, constant) == 0 for vector in standard_basis),
            ("standard collision line stopped being centered", m))

    residual = tuple(columns[0][row] - columns[1][row]
                     for row in range(len(coordinates)))
    positive_pairs = sum(value == 1 for value in residual)
    negative_pairs = sum(value == -1 for value in residual)
    zero_pairs = sum(value == 0 for value in residual)
    positive = positive_pairs * tails_per_pair
    negative = negative_pairs * tails_per_pair
    zero = zero_pairs * tails_per_pair
    expected_nonzero = (m - 2) * tails_per_pair
    collision_coordinate_count = len(coordinates) * tails_per_pair
    require((positive, negative) == (expected_nonzero, expected_nonzero)
            and zero == collision_coordinate_count - 2 * expected_nonzero,
            ("root residual support changed", m, positive, negative, zero))
    norm = tails_per_pair * dot(residual, residual)
    require(norm == 2 * expected_nonzero
            and dot(residual, symmetric) == 0,
            ("root residual normalization changed", m, norm))
    dual = tuple(value / norm for value in residual)
    require(tails_per_pair * dot(dual, residual) == 1
            and tails_per_pair * dot(dual, symmetric) == 0,
            ("normalized standard dual changed", m))

    # If J(c) is constant, injectivity forces c itself to be constant:
    # J(c)=lambda*1=J((lambda/2)*1).  Hence no vector with prescribed
    # c_0=1,c_1=-1 can become tangent, even modulo the symmetric row.
    # Verify the constrained augmented linear system by rank: equations
    # J(c)-lambda*1=0 together with c_0=1,c_1=-1 are inconsistent.
    equation_rows = []
    rhs = []
    for row in range(len(coordinates)):
        equation_rows.append([columns[vertex][row] for vertex in range(m)]
                             + [-constant[row]])
        rhs.append(Q(0))
    equation_rows.append([Q(1), Q(0)] + [Q(0)] * (m - 2) + [Q(0)])
    rhs.append(Q(1))
    equation_rows.append([Q(0), Q(1)] + [Q(0)] * (m - 2) + [Q(0)])
    rhs.append(Q(-1))
    coefficient_columns = tuple(
        tuple(row[column] for row in equation_rows)
        for column in range(m + 1)
    )
    augmented = coefficient_columns + (tuple(rhs),)
    require(rank(coefficient_columns) + 1 == rank(augmented),
            ("prescribed-root tangent system became consistent", m))

    return {
        "remaining_vertices_m": m,
        "collision_coordinates": collision_coordinate_count,
        "tail_matchings_per_neighbor_pair": tails_per_pair,
        "signless_incidence_rank": rank(columns),
        "decomposition_dimensions": {"trivial": 1, "standard": m - 1},
        "root_residual_histogram": {
            "+1": positive, "-1": negative, "0": zero,
        },
        "root_residual_norm": str(norm),
        "normalized_dual_denominator": str(norm),
        "prescribed_local_root_tangent_mod_symmetric": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    orders = tuple(incidence_audit(m) for m in (4, 6, 8, 10, 12, 14, 16))
    require(orders[1]["collision_coordinates"] == 45
            and orders[1]["root_residual_histogram"]
            == {"+1": 12, "-1": 12, "0": 21}
            and orders[1]["normalized_dual_denominator"] == "24",
            "the pinned h3 splitter was not recovered")
    ledger = {
        "theorem": "uniform hyperbolic collision standard-representation gate",
        "pins": PINS,
        "orders": orders,
        "uniform_identity": (
            "For a missing/doubled collision sector with m remaining "
            "vertices, every coordinate-linear endpoint transvection has "
            "coefficient c_u+c_v on neighbour pair {u,v}, independently "
            "of the perfect-matching tail.  The signless K_m incidence has "
            "rank m and splits as the symmetric collision line plus an "
            "(m-1)-dimensional centered standard module."
        ),
        "root_residual": (
            "The incomplete hyperbolic root is J(e_0-e_1).  It has "
            "(m-2)(m-3)!! coefficients +1, the same number -1, and "
            "normalized dual denominator 2(m-2)(m-3)!!."
        ),
        "no_go": (
            "No completion by additional coordinate-linear endpoint "
            "transvections can make the complete response tangent, even "
            "modulo the symmetric collision row, while retaining the "
            "prescribed local coefficients +1 and -1.  Injectivity of the "
            "signless incidence forces every tangent-mod-symmetric weight "
            "vector to be constant."
        ),
        "shortest_positive_datum": (
            "an occurrence-dependent collision splitter or higher "
            "Tate/PP comparison carrying the standard module; another "
            "ordinary site/root transvection cannot close the residual"
        ),
        "scope": (
            "exact characteristic-zero collision coefficient module, "
            "uniform in even order.  This does not prove that the standard "
            "dual extends through the complete augmented source map."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("collision transvections: TRIVIAL PLUS STANDARD REPRESENTATION")
    print("h3 residual: 12 POSITIVE, 12 NEGATIVE, DUAL DENOMINATOR 24")
    print("coordinate-linear tangent completion: IMPOSSIBLE UNIFORMLY")
    print("needed: OCCURRENCE-DEPENDENT TATE/PP COLLISION SPLITTER")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
