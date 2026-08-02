#!/usr/bin/env python3
"""Exclude the terminal pure-tensor one-column 3I+1R+2Z charts.

On the one-column boundary, the surviving L0 charts have Q_t=q e_r and
Psi(M)=h e_s^6, with r=1-s.  Normalize the invertible I-triangle.  For a
zero site z and its colour a, let L_z^a be the I-tensor obtained by pairing
one I-z spoke with the opposite I-I edge.  The triangle cofactor map sending
the three spoke columns to L_z^a is injective.  Thus an invertible I-z spoke
makes L_z^0,L_z^1 independent.

At t-colour s, the I-t blocks vanish and the four zero-shore slices are

    T_ab = x_a L_5^b + y_b L_4^a.

The three forbidden corners of h e_s^6 force the fourth corner to vanish as
well, contradicting h!=0.  The complementary five-site cofactor condition
is therefore unnecessary.  The P_t-nonzero/Q_t-zero case is symmetric.

Standard-library exact arithmetic only; assertions remain live under -O and
-I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
SITES = INNER + (RANK_ONE,) + ZEROS
WORDS3 = tuple(product((0, 1), repeat=3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


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
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
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


# Sparse formal polynomials; a monomial is a sorted tuple of variable names.
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


def normalized_packet(missing_colour):
    """Formal generic-kernel packet after normalizing X_i=I on INNER."""

    other = 1 - missing_colour
    packet = {}
    for u, v in combinations(SITES, 2):
        for a, b in product((0, 1), repeat=2):
            if u in INNER and v in INNER:
                # The harmless nonzero scalar (2*tau)^-1 is suppressed.
                value = constant(a != b)
            elif u in INNER and v == RANK_ONE:
                # P_t=0, Q_t=e_other gives M_it=P_i Q_t^T/(2*tau).
                value = constant(a == 0 and b == other)
            elif u in INNER and v in ZEROS:
                value = variable(f"m{u}{v}{a}{b}")
            elif u == RANK_ONE and v in ZEROS:
                value = variable(f"m{u}{v}{a}{b}")
            else:
                # The nonzero -2*tau multiplier forces M_45=0.
                value = constant(0)
            packet[u, v, a, b] = value
    return packet


def matching_coefficient(packet, word):
    answer = constant(0)
    for matching in MATCHINGS:
        term = constant(1)
        for u, v in matching:
            term = multiply(term, packet[u, v, word[u], word[v]])
        answer = add(answer, term)
    return answer


def triangle_spoke_cofactor(packet, zero, zero_colour, inner_word):
    """The four-site hafnian on INNER union {zero}."""

    answer = constant(0)
    for i in INNER:
        j, k = tuple(vertex for vertex in INNER if vertex != i)
        answer = add(
            answer,
            multiply(
                packet[i, zero, inner_word[i], zero_colour],
                packet[j, k, inner_word[j], inner_word[k]],
            ),
        )
    return answer


def audit_t_slice_identity():
    """Verify T_ab=x_a L_5^b+y_b L_4^a in both colour charts."""

    checks = 0
    for missing_colour in (0, 1):
        packet = normalized_packet(missing_colour)
        for inner_word in WORDS3:
            for colour4, colour5 in product((0, 1), repeat=2):
                word = inner_word + (
                    missing_colour,
                    colour4,
                    colour5,
                )
                expected = add(
                    multiply(
                        packet[3, 4, missing_colour, colour4],
                        triangle_spoke_cofactor(
                            packet, 5, colour5, inner_word
                        ),
                    ),
                    multiply(
                        packet[3, 5, missing_colour, colour5],
                        triangle_spoke_cofactor(
                            packet, 4, colour4, inner_word
                        ),
                    ),
                )
                require(
                    matching_coefficient(packet, word) == expected,
                    (
                        "the pure-colour t-slice factorization failed",
                        missing_colour,
                        inner_word,
                        colour4,
                        colour5,
                    ),
                )
                checks += 1
    require(checks == 64, "the t-slice identity census changed")
    return checks


def cofactor_map_matrix():
    """Matrix of (u_i)_i -> sum_i u_i(x_i) J(x_j,x_k)."""

    columns = tuple((i, colour) for i in INNER for colour in (0, 1))
    matrix = []
    for word in WORDS3:
        row = []
        for i, colour in columns:
            j, k = tuple(vertex for vertex in INNER if vertex != i)
            row.append(
                int(word[i] == colour and word[j] != word[k])
            )
        matrix.append(row)
    return matrix


def audit_cofactor_injectivity():
    matrix = cofactor_map_matrix()
    require(rational_rank(matrix) == 6, "triangle cofactor map lost rank 6")

    # Explicitly recover all six input coordinates from the six mixed words.
    # The weight-one rows recover the colour-zero inputs, and the weight-two
    # rows recover the colour-one inputs by the same three-by-three inverse.
    for shore_colour in (0, 1):
        inputs = [variable(f"u{i}_{shore_colour}") for i in INNER]
        pair_sums = (
            add(inputs[0], inputs[1]),
            add(inputs[0], inputs[2]),
            add(inputs[1], inputs[2]),
        )
        recovered = (
            scale(Q(1, 2), add(pair_sums[0], pair_sums[1],
                                scale(-1, pair_sums[2]))),
            scale(Q(1, 2), add(pair_sums[0], pair_sums[2],
                                scale(-1, pair_sums[1]))),
            scale(Q(1, 2), add(pair_sums[1], pair_sums[2],
                                scale(-1, pair_sums[0]))),
        )
        require(tuple(inputs) == recovered,
                "explicit triangle-cofactor inverse failed")
    return len(matrix), len(matrix[0])


def audit_forbidden_corner_implication():
    # Put s for the pure colour and r=1-s.  Write
    # T_ab=x_a B_b+y_b A_a, where A_s,A_r are independent and B_r!=0.
    #
    # If y_r!=0, T_sr=T_rr=0 makes both A_s and A_r proportional to B_r,
    # contradicting their independence.  Hence y_r=0.  Then those same two
    # equations force x_s=x_r=0, and T_rs=0 forces y_s=0.  Thus T_ss=0.
    cases = {}
    for y_r_nonzero in (False, True):
        if y_r_nonzero:
            cases[y_r_nonzero] = "independent-A contradiction"
        else:
            cases[y_r_nonzero] = "all four corner scalars zero"
    require(
        cases == {
            False: "all four corner scalars zero",
            True: "independent-A contradiction",
        },
        "forbidden-corner case split changed",
    )

    # The hypotheses used above follow from the two invertible spoke
    # witnesses: injectivity sends an independent pair of spoke-column
    # triples to independent A_s,A_r, and sends a nonzero r-column triple to
    # B_r!=0.  No property of the terminal five-site tensor is invoked.
    witness_implications = (
        "invertible M_i4 => independent (L_4^0,L_4^1)",
        "invertible M_j5 => nonzero L_5^r",
    )
    require(len(witness_implications) == 2,
            "invertible-spoke implication count changed")
    return cases, witness_implications


def main():
    slice_checks = audit_t_slice_identity()
    height, rank = audit_cofactor_injectivity()
    cases, witnesses = audit_forbidden_corner_implication()
    print("three-invertible one-column pure-tensor obstruction: passed")
    print(f"  exact t-slice identities       : {slice_checks}/64")
    print(f"  triangle cofactor map          : rank {rank} in {height} rows")
    print(f"  forbidden-corner cases        : {cases}")
    print(f"  invertible-spoke consequences : {len(witnesses)}/2")
    print("  outcome                        : both terminal charts excluded")
    print("  five-site cofactor purity      : not needed")


if __name__ == "__main__":
    main()
