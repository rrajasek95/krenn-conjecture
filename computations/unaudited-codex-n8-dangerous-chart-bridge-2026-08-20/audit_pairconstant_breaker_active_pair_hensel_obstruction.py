#!/usr/bin/env python3
"""Smooth F3 obstruction to the proposed >=3-active-pair char0 lemma."""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_pairconstant_breaker_active_pair_hensel_obstruction.json"
PRIME = 3
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
# Flattened 2x2 blocks in edge order, entries represented in F3.
POINT = (
    (0, 1, 2, 0),
    (0, 1, 2, 0),
    (0, 1, 2, 2),
    (1, 0, 1, 2),
    (1, 0, 0, 2),
    (1, 0, 0, 2),
)
# For complement pair i <-> 15-i, impose one factor at these indices.
IMPOSED_Q_ZEROS = (0, 13, 3, 10, 6, 7)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def at(blocks, edge_index, left, right):
    return blocks[edge_index][2 * left + right]


def permanent(block):
    return block[0] * block[3] + block[1] * block[2]


def triangle(blocks, first, second, third):
    return sum(
        at(blocks, first, ri, rj)
        * at(blocks, second, 1 - ri, rk)
        * at(blocks, third, 1 - rj, 1 - rk)
        for ri, rj, rk in product(range(2), repeat=3)
    )


TRIANGLES = (
    (0, 1, 3),  # supervertices 0,1,2
    (0, 2, 4),  # 0,1,3
    (1, 2, 5),  # 0,2,3
    (3, 4, 5),  # 1,2,3
)


def bits(index):
    return tuple((index >> (3 - site)) & 1 for site in range(4))


def transversal_q(blocks, index):
    s = bits(index)
    return (
        at(blocks, 0, s[0], s[1]) * at(blocks, 5, s[2], s[3])
        + at(blocks, 1, s[0], s[2]) * at(blocks, 4, s[1], s[3])
        + at(blocks, 2, s[0], s[3]) * at(blocks, 3, s[1], s[2])
    )


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def pure_hafnian(blocks):
    total = 0
    for matching in PM8:
        term = 1
        for left_site, right_site in matching:
            left_pair, left_clone = divmod(left_site, 2)
            right_pair, right_clone = divmod(right_site, 2)
            if left_pair == right_pair:
                factor = 1  # normalized M0 anchor
            else:
                edge = EDGE_INDEX[left_pair, right_pair]
                factor = at(blocks, edge, left_clone, right_clone)
            term *= factor
        total += term
    return total


def variable(edge, left, right):
    return 4 * edge + 2 * left + right


def jacobian_rows(blocks):
    rows = []
    # Six equations per(M_ij)+1=0.
    for edge, block in enumerate(blocks):
        a, b, c, d = block
        row = [0] * 24
        for offset, value in enumerate((d, c, b, a)):
            row[4 * edge + offset] = value
        rows.append(row)
    # Four equations tau_ijk-2=0.
    for first, second, third in TRIANGLES:
        row = [0] * 24
        for ri, rj, rk in product(range(2), repeat=3):
            va = at(blocks, first, ri, rj)
            vb = at(blocks, second, 1 - ri, rk)
            vc = at(blocks, third, 1 - rj, 1 - rk)
            row[variable(first, ri, rj)] += vb * vc
            row[variable(second, 1 - ri, rk)] += va * vc
            row[variable(third, 1 - rj, 1 - rk)] += va * vb
        rows.append(row)
    # Six chosen equations Q_s=0, leaving only complement pairs 1 and 4
    # potentially active.
    pairings = (
        (0, 5, (0, 1, 2, 3)),
        (1, 4, (0, 2, 1, 3)),
        (2, 3, (0, 3, 1, 2)),
    )
    for index in IMPOSED_Q_ZEROS:
        s = bits(index)
        row = [0] * 24
        for first, second, sites in pairings:
            i, j, k, ell = sites
            va = at(blocks, first, s[i], s[j])
            vb = at(blocks, second, s[k], s[ell])
            row[variable(first, s[i], s[j])] += vb
            row[variable(second, s[k], s[ell])] += va
        rows.append(row)
    return tuple(tuple(value % PRIME for value in row) for row in rows)


def rref_mod(matrix, prime):
    rows = [list(row) for row in matrix]
    pivot_columns = []
    pivot_row = 0
    for column in range(len(rows[0])):
        chosen = next((index for index in range(pivot_row, len(rows))
                       if rows[index][column] % prime), None)
        if chosen is None:
            continue
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % prime, -1, prime)
        rows[pivot_row] = [value * inverse % prime
                           for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column] % prime:
                continue
            factor = rows[index][column] % prime
            rows[index] = [(rows[index][j] - factor * rows[pivot_row][j])
                           % prime for j in range(len(rows[index]))]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(tuple(row) for row in rows), tuple(pivot_columns)


def determinant_mod(matrix, prime):
    rows = [list(row) for row in matrix]
    answer = 1
    for column in range(len(rows)):
        chosen = next((index for index in range(column, len(rows))
                       if rows[index][column] % prime), None)
        if chosen is None:
            return 0
        if chosen != column:
            rows[column], rows[chosen] = rows[chosen], rows[column]
            answer = -answer
        pivot = rows[column][column] % prime
        answer = answer * pivot % prime
        inverse = pow(pivot, -1, prime)
        for index in range(column + 1, len(rows)):
            factor = rows[index][column] * inverse % prime
            for j in range(column, len(rows)):
                rows[index][j] = (rows[index][j]
                                  - factor * rows[column][j]) % prime
    return answer % prime


def main() -> None:
    require(len(PM8) == 105, "PM8 census changed")
    permanent_values = tuple(permanent(block) % PRIME for block in POINT)
    triangle_values = tuple(triangle(POINT, *triple) % PRIME
                            for triple in TRIANGLES)
    q_values = tuple(transversal_q(POINT, index) % PRIME
                     for index in range(16))
    active_pairs = tuple(index for index in range(8)
                         if q_values[index] * q_values[15 - index] % PRIME)
    h_value = pure_hafnian(POINT) % PRIME
    require(permanent_values == (2,) * 6,
            "a permanent is not -1 modulo 3")
    require(triangle_values == (2,) * 4,
            "a triangle contraction is not 2 modulo 3")
    require(all(q_values[index] == 0 for index in IMPOSED_Q_ZEROS),
            "an imposed transversal factor is nonzero")
    require(q_values == (0, 1, 1, 0, 1, 1, 0, 0,
                         0, 2, 0, 1, 2, 0, 1, 1),
            "transversal value vector changed")
    require(active_pairs == (1, 4) and h_value == 2,
            "two-active-pair/H unit control changed")
    require(sum(q_values[index] * q_values[15 - index]
                for index in range(16)) % PRIME == 2 * h_value % PRIME,
            "sum Q_s Q_sbar = 2H identity failed")

    jacobian = jacobian_rows(POINT)
    _reduced, pivots = rref_mod(jacobian, PRIME)
    require(len(jacobian) == len(pivots) == 16,
            "branch Jacobian is not full row rank")
    minor = tuple(tuple(row[column] for column in pivots)
                  for row in jacobian)
    determinant = determinant_mod(minor, PRIME)
    require(determinant != 0, "canonical Jacobian minor vanished")

    hostile = list(map(list, POINT))
    hostile[2][3] = 1
    hostile = tuple(map(tuple, hostile))
    require(tuple(triangle(hostile, *triple) % PRIME
                  for triple in TRIANGLES) != triangle_values,
            "single-entry mutation did not change a triangle equation")

    result = {
        "status": "UNAUDITED exact smooth-F3 / char0 support-lemma obstruction",
        "field": "F_3",
        "edge_order": [list(edge) for edge in EDGES],
        "blocks_flattened_row_major": [list(block) for block in POINT],
        "equations": {
            "permanent_plus_one": 6,
            "triangle_minus_two": 4,
            "imposed_transversal_Q_zero": list(IMPOSED_Q_ZEROS),
            "total": 16,
        },
        "permanent_values_mod3": list(permanent_values),
        "triangle_values_mod3": list(triangle_values),
        "Q_0000_through_1111_mod3": list(q_values),
        "active_complement_pair_representatives": list(active_pairs),
        "pure_H_mod3": h_value,
        "jacobian_shape": [16, 24],
        "jacobian_rank_mod3": len(pivots),
        "canonical_nonzero_minor_columns": list(pivots),
        "canonical_minor_determinant_mod3": determinant,
        "hensel_consequence": (
            "Fixing the eight nonpivot variables at arbitrary 3-adic lifts, "
            "the invertible 16x16 Jacobian minor gives a Z_3 solution by "
            "multivariate Hensel/implicit-function lifting. The six imposed "
            "Q factors remain exactly zero, while Q_1 Q_14, Q_4 Q_11, and "
            "H remain 3-adic units. Thus the corresponding saturated "
            "finite-type Q-scheme is nonempty, hence has a point over C."
        ),
        "conclusion": (
            "The characteristic-zero lemma 'per=-1, tau=2, H nonzero "
            "implies at least three active complement self-pairs' is false. "
            "There is a characteristic-zero component with exactly two."
        ),
        "scope": (
            "This obstructs the one-colour support lower bound and therefore "
            "the bare 3-colours-into-8 pigeonhole proof using only the 78 "
            "pair-constant rows plus the smallest 48-word breaker orbit. It "
            "does not yet give three mutually breaker-compatible live "
            "colours and does not obstruct adding the other five breaker "
            "orbits or full mixed equations."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("pairconstant/breaker active-pair Hensel obstruction: PASS")
    print("active pairs / H mod3:", active_pairs, h_value)
    print("Jacobian rank / minor determinant:", len(pivots), determinant)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
