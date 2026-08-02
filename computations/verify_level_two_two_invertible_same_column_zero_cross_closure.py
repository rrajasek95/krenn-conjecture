#!/usr/bin/env python3
"""Close the same-column 2I+2R+2Z zero-cross boundary.

Assume the two rank-one endpoint matrices miss the same selected column and
their potential sum is zero.  The rank-one cross block is then free.  An
exact signed-potential census leaves 19 support envelopes.  Eighteen have
at most 52 active differential columns.  In the sole 60-column envelope,
the four rank-one/zero potentials vanish and the four I-to-R blocks have the
common-factor grid M_it=p_i v_t^T.  Four rectangle syzygies meet the five
vertex gauges in one dimension, so this final envelope also has rank at
most 52.

Standard library only; assertions remain live under -O and -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
BOUNDARY = run_path(str(
    HERE / "verify_level_two_two_invertible_same_column_potential_boundary.py"
))
LINEAR = run_path(str(
    HERE / "verify_level_two_one_sided_overlap_collapse.py"
))

SITES = tuple(range(6))
COLOURS = (0, 1)
INVERTIBLE = (0, 1)
RANK_ONE = (2, 3)
ZERO = (4, 5)
EDGES = tuple(combinations(SITES, 2))
CORE_EDGES = frozenset(combinations(INVERTIBLE + RANK_ONE, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}
COMPLEMENT_MATCHINGS = {
    pair: BOUNDARY["perfect_matchings"](
        site for site in SITES if site not in pair
    )
    for pair in EDGES
}
E10 = ((0, 0), (1, 0))
ZERO_MATRIX = ((0, 0), (0, 0))


def zero_cross_admissible(potential):
    if not BOUNDARY["zero_sum"](potential[2], potential[3]):
        return False
    return all(
        not BOUNDARY["zero_sum"](potential[u], potential[v])
        for u, v in CORE_EDGES
        if (u, v) != (2, 3)
    )


def support_value(optional, pair, colours):
    u, v = pair
    _, colour_at_v = colours
    if pair == (0, 1):
        return True
    if u in INVERTIBLE and v in RANK_ONE:
        return colour_at_v == 0
    if pair == (2, 3):
        return True
    return pair in optional


def cofactor_may_live(optional, pair, word):
    return any(
        all(
            support_value(
                optional,
                matching_edge,
                (word[matching_edge[0]], word[matching_edge[1]]),
            )
            for matching_edge in matching
        )
        for matching in COMPLEMENT_MATCHINGS[pair]
    )


def active_cells(optional):
    answer = set()
    for cell in CELLS:
        u, v, a, b = cell
        if any(
            word[u] == a
            and word[v] == b
            and cofactor_may_live(optional, (u, v), word)
            for word in product(COLOURS, repeat=6)
        ):
            answer.add(cell)
    return frozenset(answer)


EXCEPTIONAL_OPTIONAL = frozenset(
    ((2, 4), (2, 5), (3, 4), (3, 5), (4, 5))
)


def audit_potential_envelopes():
    admissible = 0
    envelopes = {}
    representatives = {}
    for potential in BOUNDARY["signed_partitions"](6):
        if not zero_cross_admissible(potential):
            continue
        admissible += 1
        optional = BOUNDARY["canonical_optional_edges"](
            BOUNDARY["optional_edges"](potential)
        )
        envelopes.setdefault(optional, potential)
        representatives.setdefault(optional, []).append(potential)

    require(admissible == 236,
            ("zero-cross admissible census changed", admissible))
    require(len(envelopes) == 19,
            ("zero-cross envelope census changed", len(envelopes)))

    exceptional = BOUNDARY["canonical_optional_edges"](EXCEPTIONAL_OPTIONAL)
    require(exceptional in envelopes, "exceptional zero-cross envelope vanished")
    require(representatives[exceptional] == [
        (1, 1, 0, 0, 0, 0),
        (1, 2, 0, 0, 0, 0),
    ], ("exceptional potential types changed", representatives[exceptional]))

    counts = {optional: len(active_cells(optional)) for optional in envelopes}
    histogram = dict(sorted(Counter(counts.values()).items()))
    require(histogram == {
        4: 1, 16: 2, 20: 2, 28: 3, 32: 2,
        40: 4, 44: 1, 52: 3, 60: 1,
    }, ("zero-cross active-cell histogram changed", histogram))
    require(counts[exceptional] == 60,
            "exceptional zero-cross active count changed")
    require(max(
        count for optional, count in counts.items() if optional != exceptional
    ) == 52, "a nonexceptional zero-cross envelope reached rank 55")
    return envelopes, exceptional, histogram


# Sparse formal polynomials; monomials are sorted tuples of variable names.
def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = {}
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] = (
                    updated.get(monomial, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not updated[monomial]:
                    del updated[monomial]
        answer = updated
    return answer


def formal_block(pair):
    if pair in ((0, 2), (0, 3), (1, 2), (1, 3)):
        return tuple(tuple(constant(E10[a][b]) for b in COLOURS)
                     for a in COLOURS)
    if pair in ((0, 4), (0, 5), (1, 4), (1, 5)):
        return tuple(tuple(constant(0) for _b in COLOURS)
                     for _a in COLOURS)
    return tuple(
        tuple(variable(f"m{pair[0]}{pair[1]}{a}{b}") for b in COLOURS)
        for a in COLOURS
    )


FORMAL_BLOCKS = {pair: formal_block(pair) for pair in EDGES}


def formal_hafnian(vertices, word):
    answer = constant(0)
    for matching in BOUNDARY["perfect_matchings"](tuple(sorted(vertices))):
        term = constant(1)
        for pair in matching:
            term = multiply(
                term,
                FORMAL_BLOCKS[pair][word[pair[0]]][word[pair[1]]],
            )
        answer = add(answer, term)
    return answer


def rectangle_tangent(rank_one, output):
    tangent = [constant(0) for _cell in CELLS]
    tangent[CELL_INDEX[0, rank_one, 1, output]] = constant(1)
    tangent[CELL_INDEX[1, rank_one, 1, output]] = constant(-1)
    return tangent


def apply_formal_differential(tangent):
    answer = []
    for word in product(COLOURS, repeat=6):
        value = constant(0)
        for cell, coefficient in zip(CELLS, tangent):
            if not coefficient:
                continue
            u, v, a, b = cell
            if (word[u], word[v]) != (a, b):
                continue
            complement = tuple(site for site in SITES if site not in (u, v))
            value = add(value, multiply(
                coefficient, formal_hafnian(complement, word)
            ))
        answer.append(value)
    return answer


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def audit_rectangle_syzygies():
    tangents = []
    identities = 0
    for rank_one in RANK_ONE:
        for output in COLOURS:
            tangent = rectangle_tangent(rank_one, output)
            require(not any(apply_formal_differential(tangent)),
                    ("rectangle tangent left the formal kernel",
                     rank_one, output))
            tangents.append([next(iter(value.values()), Q(0))
                             for value in tangent])
            identities += 64
    require(identities == 256, "rectangle identity census changed")
    require(rational_rank(tangents) == 4,
            "the four rectangle tangents became dependent")
    return tangents, identities


def numeric_packet():
    packet = {}
    for edge_index, pair in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            if pair in ((0, 2), (0, 3), (1, 2), (1, 3)):
                value = E10[a][b]
            elif pair in ((0, 4), (0, 5), (1, 4), (1, 5)):
                value = 0
            else:
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            packet[pair[0], pair[1], a, b] = value
    return packet


def gauge_tangent(packet, mu):
    return [
        (mu[u] + mu[v]) * packet[u, v, a, b]
        for u, v, a, b in CELLS
    ]


def audit_kernel_dimension(rectangles):
    packet = numeric_packet()
    derivative = LINEAR["differential"](packet)
    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        gauge = gauge_tangent(packet, mu)
        require(not any(LINEAR["matrix_vector_product"](derivative, gauge)),
                ("vertex gauge left the differential kernel", basis))
        gauges.append(gauge)
    require(rational_rank(gauges) == 5, "vertex gauges lost dimension five")
    require(rational_rank(rectangles) == 4,
            "rectangle space lost dimension four")
    require(rational_rank(gauges + rectangles) == 8,
            "gauge/rectangle sum lost dimension eight")

    # A gauge in the rectangle space vanishes on these seven dense-open
    # edges.  They force mu_0=-mu_1 and mu_2=...=mu_5=0, leaving exactly
    # the one common direction K_2(v_2)+K_3(v_3).
    zero_edges = ((0, 1), (2, 3), (2, 4), (2, 5),
                  (3, 4), (3, 5), (4, 5))
    incidence = [
        [int(vertex in pair) for vertex in SITES]
        for pair in zero_edges
    ]
    require(rational_rank(incidence) == 5,
            "dense-open zero-edge incidence rank changed")

    ranks = (
        rational_rank(derivative),
        LINEAR["rank_mod"](derivative, 101),
        LINEAR["rank_mod"](derivative, 1_000_003),
    )
    require(ranks == (43, 43, 43),
            ("exceptional calibration rank changed", ranks))
    return ranks


def main():
    envelopes, exceptional, histogram = audit_potential_envelopes()
    rectangles, identities = audit_rectangle_syzygies()
    ranks = audit_kernel_dimension(rectangles)
    print("2I+2R+2Z same-column zero-cross closure: all checks passed")
    print(f"  support envelopes              : {len(envelopes)}")
    print(f"  active-cell histogram          : {histogram}")
    print(f"  exceptional optional edges     : {sorted(exceptional)}")
    print(f"  rectangle identities           : {identities}/256")
    print("  gauge/rectangle dimensions     : 5+4-1=8")
    print(f"  exceptional calibration ranks  : {ranks}")
    print("  universal differential bound   : 52")


if __name__ == "__main__":
    main()
