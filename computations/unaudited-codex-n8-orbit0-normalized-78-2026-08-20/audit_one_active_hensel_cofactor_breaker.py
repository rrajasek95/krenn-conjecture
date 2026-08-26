#!/usr/bin/env python3
"""Smooth one-active branch and its exact 00000101 cofactor exclusion.

The first half gives a stronger obstruction to any self-pair-count lemma:
there is a smooth F3 point with only one active Q_s Q_sbar, hence a char-0
Hensel branch.  The second half shows why this does not survive the next
mixed orbit.  On the same-colour diagonal locus, the profile-(6,2) row is
x^d_uv times the pure Hafnian cofactor of colour c.  At the point, sixteen
nonanchor cofactors are units, and their complement cannot support permanent
-1 in four of the six 2x2 blocks of any other colour.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_one_active_hensel_cofactor_breaker.json"
PRIME = 3
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ANCHORS = ((0, 1), (2, 3), (4, 5), (6, 7))
POINT = (
    (2, 1, 1, 2),
    (1, 1, 2, 0),
    (1, 0, 2, 2),
    (2, 2, 0, 1),
    (0, 2, 1, 1),
    (2, 2, 2, 2),
)
TRIANGLES = ((0, 1, 3), (0, 2, 4), (1, 2, 5), (3, 4, 5))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        result.extend(((first, second),) + tail
                      for tail in perfect_matchings(rest))
    return tuple(result)


PM = {size: perfect_matchings(tuple(range(size))) for size in (6, 8)}


def bits(index):
    return tuple((index >> (3 - site)) & 1 for site in range(4))


def at(blocks, edge_index, left, right):
    return blocks[edge_index][2 * left + right]


def permanent(block):
    return block[0] * block[3] + block[1] * block[2]


def triangle(blocks, first, second, third):
    return sum(at(blocks, first, x, y)
               * at(blocks, second, 1 - x, z)
               * at(blocks, third, 1 - y, 1 - z)
               for x, y, z in product((0, 1), repeat=3))


def q_value(blocks, index):
    s = bits(index)
    return (
        at(blocks, 0, s[0], s[1]) * at(blocks, 5, s[2], s[3])
        + at(blocks, 1, s[0], s[2]) * at(blocks, 4, s[1], s[3])
        + at(blocks, 2, s[0], s[3]) * at(blocks, 3, s[1], s[2])
    )


def cell(blocks, u, v):
    left_pair, left_clone = divmod(u, 2)
    right_pair, right_clone = divmod(v, 2)
    if left_pair == right_pair:
        return 1
    return at(blocks, EDGE_INDEX[(left_pair, right_pair)],
              left_clone, right_clone)


def hafnian_on_vertices(blocks, vertices):
    total = 0
    local_matchings = perfect_matchings(tuple(vertices))
    for matching in local_matchings:
        term = 1
        for u, v in matching:
            term *= cell(blocks, u, v)
        total += term
    return total


def pure_hafnian(blocks):
    return hafnian_on_vertices(blocks, tuple(range(8)))


def q_jacobian_row(blocks, index):
    s = bits(index)
    row = [0] * 24
    pairings = ((0, 5, (0, 1, 2, 3)),
                (1, 4, (0, 2, 1, 3)),
                (2, 3, (0, 3, 1, 2)))
    for first, second, sites in pairings:
        i, j, k, l = sites
        va = at(blocks, first, s[i], s[j])
        vb = at(blocks, second, s[k], s[l])
        row[4 * first + 2 * s[i] + s[j]] += vb
        row[4 * second + 2 * s[k] + s[l]] += va
    return row


def base_jacobian_rows(blocks):
    rows = []
    for edge, block in enumerate(blocks):
        a, b, c, d = block
        row = [0] * 24
        row[4 * edge:4 * edge + 4] = (d, c, b, a)
        rows.append(row)
    for first, second, third in TRIANGLES:
        row = [0] * 24
        for x, y, z in product((0, 1), repeat=3):
            va = at(blocks, first, x, y)
            vb = at(blocks, second, 1 - x, z)
            vc = at(blocks, third, 1 - y, 1 - z)
            row[4 * first + 2 * x + y] += vb * vc
            row[4 * second + 2 * (1 - x) + z] += va * vc
            row[4 * third + 2 * (1 - y) + (1 - z)] += va * vb
        rows.append(row)
    return rows


def rref_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(len(rows[0])):
        chosen = next((index for index in range(pivot_row, len(rows))
                       if rows[index][column]), None)
        if chosen is None:
            continue
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime
                           for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [(rows[index][j] - factor * rows[pivot_row][j])
                           % prime for j in range(len(rows[index]))]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(tuple(row) for row in rows), tuple(pivots)


def determinant_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    answer = 1
    for column in range(len(rows)):
        chosen = next((index for index in range(column, len(rows))
                       if rows[index][column]), None)
        if chosen is None:
            return 0
        if chosen != column:
            rows[column], rows[chosen] = rows[chosen], rows[column]
            answer = -answer
        pivot = rows[column][column]
        answer = answer * pivot % prime
        inverse = pow(pivot, -1, prime)
        for index in range(column + 1, len(rows)):
            factor = rows[index][column] * inverse % prime
            rows[index] = [(rows[index][j] - factor * rows[column][j])
                           % prime for j in range(len(rows[index]))]
    return answer % prime


def main():
    require(len(PM[8]) == 105 and len(PM[6]) == 15,
            "perfect-matching census changed")
    permanents = tuple(permanent(block) % PRIME for block in POINT)
    triangles = tuple(triangle(POINT, *triple) % PRIME
                      for triple in TRIANGLES)
    q_values = tuple(q_value(POINT, index) % PRIME for index in range(16))
    h_value = pure_hafnian(POINT) % PRIME
    active = tuple(index for index in range(8)
                   if q_values[index] * q_values[15 - index] % PRIME)
    require(permanents == (2,) * 6 and triangles == (2,) * 4,
            "pairconstant equations failed")
    require(q_values == (0, 0, 0, 0, 0, 0, 1, 0,
                         0, 1, 0, 0, 0, 0, 0, 0),
            "one-active Q vector changed")
    require(active == (6,) and h_value == 1,
            "one-active/H-unit control changed")

    inactive = tuple(index for index in range(8) if index != 6)
    rank_histogram = Counter()
    canonical_choice = inactive
    canonical_rows = None
    canonical_pivots = None
    for mask in range(1 << len(inactive)):
        choice = tuple(index if not (mask >> position) & 1 else 15 - index
                       for position, index in enumerate(inactive))
        require(all(q_values[index] == 0 for index in choice),
                "inactive pair unexpectedly has a nonzero factor")
        rows = base_jacobian_rows(POINT) + [q_jacobian_row(POINT, index)
                                            for index in choice]
        reduced, pivots = rref_mod(rows, PRIME)
        rank_histogram[len(pivots)] += 1
        if choice == canonical_choice:
            canonical_rows = rows
            canonical_pivots = pivots
    require(rank_histogram == {17: 128},
            "not every inactive-factor branch is smooth")
    require(canonical_rows is not None and len(canonical_pivots) == 17,
            "canonical branch was not captured")
    minor = tuple(tuple(row[column] for column in canonical_pivots)
                  for row in canonical_rows)
    determinant = determinant_mod(minor, PRIME)
    require(determinant != 0, "canonical Hensel minor vanished")

    # Literal pure cofactors.  The normalized anchor cofactors are exactly
    # the four t_ijk rows; the remaining 24 are detected by 00000101.
    cofactors = {}
    values = {}
    for u in range(8):
        for v in range(u + 1, 8):
            edge = (u, v)
            remaining = tuple(site for site in range(8)
                              if site not in edge)
            values[edge] = cell(POINT, u, v) % PRIME
            cofactors[edge] = hafnian_on_vertices(POINT, remaining) % PRIME
    require(all(cofactors[edge] == 0 for edge in ANCHORS),
            "an anchor cofactor is nonzero")
    nonanchors = tuple(edge for edge in cofactors if edge not in ANCHORS)
    gradient_support = tuple(edge for edge in nonanchors if cofactors[edge])
    gradient_zero = tuple(edge for edge in nonanchors if not cofactors[edge])
    require(len(gradient_support) == 16 and len(gradient_zero) == 8,
            "nonanchor cofactor support changed")
    euler = sum(values[edge] * cofactors[edge]
                for edge in cofactors) % PRIME
    require(euler == 4 * h_value % PRIME,
            "degree-four Euler identity failed")

    # Verify the diagonal-locus factorization combinatorially: for six sites
    # of colour c and the nonanchor pair e of colour d, every same-colour
    # perfect matching must contain e, leaving exactly the cofactor matchings.
    factorization_counts = Counter()
    for exceptional in nonanchors:
        same_colour_matchings = []
        for matching in PM[8]:
            if all(((u in exceptional) == (v in exceptional))
                   for u, v in matching):
                same_colour_matchings.append(matching)
        require(len(same_colour_matchings) == 15
                and all(exceptional in matching
                        for matching in same_colour_matchings),
                f"00000101 factorization failed at {exceptional}")
        factorization_counts[len(same_colour_matchings)] += 1
    require(factorization_counts == {15: 24},
            "profile-(6,2) factorization census changed")

    # If a second colour d satisfies the 00000101 rows, all its cells on
    # gradient_support vanish because those cofactors are 3-adic units.
    # Inventory the only positions left in each 2x2 superpair block.
    allowed_by_block = defaultdict(list)
    for u, v in gradient_zero:
        i, x = divmod(u, 2)
        j, y = divmod(v, 2)
        allowed_by_block[(i, j)].append((x, y))
    allowed_by_block = {edge: tuple(sorted(allowed_by_block[edge]))
                        for edge in EDGES}
    require(allowed_by_block == {
        (0, 1): ((0, 1), (1, 0)),
        (0, 2): ((1, 1),),
        (0, 3): ((0, 1),),
        (1, 2): ((1, 0),),
        (1, 3): ((0, 0),),
        (2, 3): ((0, 1), (1, 0)),
    }, "cofactor-complement block positions changed")
    impossible_blocks = tuple(edge for edge, positions
                              in allowed_by_block.items()
                              if not ({(0, 0), (1, 1)} <= set(positions)
                                      or {(0, 1), (1, 0)} <= set(positions)))
    require(impossible_blocks == ((0, 2), (0, 3), (1, 2), (1, 3)),
            "permanent obstruction blocks changed")

    # Must-fire control: allowing one complementary entry in block 02 is
    # enough to remove that block from the purely support-theoretic list.
    hostile_allowed = dict(allowed_by_block)
    hostile_allowed[(0, 2)] = ((0, 0), (1, 1))
    hostile_impossible = tuple(edge for edge, positions
                               in hostile_allowed.items()
                               if not ({(0, 0), (1, 1)} <= set(positions)
                                       or {(0, 1), (1, 0)} <= set(positions)))
    require((0, 2) not in hostile_impossible
            and hostile_impossible != impossible_blocks,
            "cofactor-support mutation did not fire")

    result = {
        "status": "UNAUDITED smooth one-active branch plus 00000101 exclusion",
        "field": "F_3",
        "edge_order": [list(edge) for edge in EDGES],
        "blocks_flattened_row_major": [list(block) for block in POINT],
        "permanents_mod3": list(permanents),
        "triangles_mod3": list(triangles),
        "Q_0000_through_1111_mod3": list(q_values),
        "active_complement_pair_representatives": list(active),
        "pure_H_mod3": h_value,
        "inactive_factor_branches": 128,
        "jacobian_rank_histogram": dict(rank_histogram),
        "canonical_imposed_Q_indices": list(canonical_choice),
        "canonical_jacobian_shape": [17, 24],
        "canonical_pivot_columns": list(canonical_pivots),
        "canonical_minor_determinant_mod3": determinant,
        "hensel_consequence": (
            "Every choice of one vanishing factor in each of the seven "
            "inactive complement pairs has full row rank 17. In particular "
            "there is a Z_3/characteristic-zero lift with exactly one active "
            "self pair and H a unit."
        ),
        "cofactor_orbit": {
            "representative": "00000101",
            "profile": [6, 2],
            "formula_on_diagonal_locus": (
                "H_word=x^d_uv * partial(H_c)/partial(x^c_uv), c!=d"
            ),
            "literal_nonanchor_edges": 24,
            "same_colour_matchings_per_edge": 15,
        },
        "anchor_cofactors_mod3": {f"{u}{v}": cofactors[(u, v)]
                                   for u, v in ANCHORS},
        "nonanchor_gradient_support": [list(edge)
                                       for edge in gradient_support],
        "nonanchor_gradient_zero": [list(edge) for edge in gradient_zero],
        "nonanchor_gradient_support_size": len(gradient_support),
        "euler_check_mod3": euler,
        "allowed_second_colour_positions_by_block": {
            f"{i}{j}": [list(position) for position in positions]
            for (i, j), positions in allowed_by_block.items()
        },
        "second_colour_permanent_impossible_blocks": [list(edge)
                                                       for edge in impossible_blocks],
        "conclusion": (
            "The 78 pairconstant rows admit a smooth characteristic-zero "
            "branch with only one active self pair, so no positive self-pair "
            "lower bound beyond one is valid. But the next 00000101 orbit "
            "kills this branch in any full diagonal mixed solution: its "
            "cofactor units force a second colour into support on which four "
            "required block permanents are zero."
        ),
        "scope": (
            "The cofactor exclusion is exact on the same-colour diagonal "
            "locus (all cross-colour cells zero), after anchor normalization. "
            "In the full normalized algebra, 00000101 also has explicit "
            "cross-colour tail terms which must be controlled separately."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("one-active Hensel/cofactor breaker: PASS")
    print("Q support / active / H:", sum(q_values[index] != 0
                                         for index in range(16)), active, h_value)
    print("Hensel branch ranks:", rank_histogram)
    print("gradient support / impossible blocks:",
          len(gradient_support), impossible_blocks)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
