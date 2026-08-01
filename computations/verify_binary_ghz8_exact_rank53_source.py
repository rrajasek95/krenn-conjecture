#!/usr/bin/env python3
"""Verify an exact rational binary GHZ8 source with residual rank 53.

This is an exact existence result, not a rank-55 construction and not a
classification of the binary GHZ8 fibre.  The source has 45 nonzero cells.
Twenty-six small rational cells are chosen freely and the other nineteen are
obtained from a triangular rational chart.  Fraction arithmetic verifies all
256 matching-tensor coefficients and the differential ranks after every one
of the 28 endpoint-pair deletions.

Standard library only; all assertions remain live under ``python3 -O`` and
``python3 -I -S``.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product


VERTICES = tuple(range(8))
COLOURS = (0, 1)
EDGES = tuple(combinations(VERTICES, 2))
WORDS8 = tuple(product(COLOURS, repeat=8))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class LaurentPolynomial:
    """Sparse Laurent polynomials over Q, sufficient for the chart audit."""

    __slots__ = ("terms", "variable_count")

    def __init__(self, terms, variable_count):
        self.variable_count = variable_count
        self.terms = {
            tuple(exponent): Q(coefficient)
            for exponent, coefficient in terms.items()
            if coefficient
        }

    @classmethod
    def constant(cls, value, variable_count):
        zero = (0,) * variable_count
        return cls({zero: Q(value)} if value else {}, variable_count)

    @classmethod
    def variable(cls, index, variable_count):
        exponent = [0] * variable_count
        exponent[index] = 1
        return cls({tuple(exponent): Q(1)}, variable_count)

    def _coerce(self, other):
        if isinstance(other, LaurentPolynomial):
            require(
                other.variable_count == self.variable_count,
                "incompatible Laurent polynomial rings",
            )
            return other
        return LaurentPolynomial.constant(other, self.variable_count)

    def __bool__(self):
        return bool(self.terms)

    def __neg__(self):
        return LaurentPolynomial(
            {exponent: -coefficient for exponent, coefficient in self.terms.items()},
            self.variable_count,
        )

    def __add__(self, other):
        other = self._coerce(other)
        terms = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            terms[exponent] = terms.get(exponent, Q(0)) + coefficient
            if not terms[exponent]:
                del terms[exponent]
        return LaurentPolynomial(terms, self.variable_count)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        terms = {}
        for left_exponent, left_coefficient in self.terms.items():
            for right_exponent, right_coefficient in other.terms.items():
                exponent = tuple(
                    left + right
                    for left, right in zip(left_exponent, right_exponent)
                )
                terms[exponent] = (
                    terms.get(exponent, Q(0))
                    + left_coefficient * right_coefficient
                )
        return LaurentPolynomial(terms, self.variable_count)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._coerce(other)
        require(len(other.terms) == 1, "chart denominator is not a monomial")
        ((denominator_exponent, denominator_coefficient),) = other.terms.items()
        return LaurentPolynomial(
            {
                tuple(
                    left - right
                    for left, right in zip(exponent, denominator_exponent)
                ): coefficient / denominator_coefficient
                for exponent, coefficient in self.terms.items()
            },
            self.variable_count,
        )

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def __eq__(self, other):
        other = self._coerce(other)
        return self.terms == other.terms


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


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6, 8)
    for vertices in combinations(VERTICES, size)
}


def named_cell(name):
    """Decode xUVab as the oriented cell (U,V,a,b)."""

    require(len(name) == 5 and name[0] == "x", f"bad cell name {name}")
    cell = tuple(int(character) for character in name[1:])
    require(cell[0] < cell[1], f"bad cell orientation {name}")
    return cell


DEFAULT_PARAMETERS = {
    "x1600": Q(-1, 20),
    "x5700": Q(1, 60),
    "x5701": Q(49, 1000),
    "x0400": Q(-3, 2),
    "x1611": Q(6, 5),
    "x3700": Q(7, 5),
    "x2601": Q(-23, 50),
    "x0500": Q(-43, 125),
    "x0600": Q(-1, 2),
    "x0610": Q(3, 40),
    "x6701": Q(27, 100),
    "x0611": Q(7, 8),
    "x6710": Q(1, 5),
    "x4610": Q(-73, 50),
    "x0601": Q(7, 10),
    "x0510": Q(-47, 30),
    "x2600": Q(13, 6),
    "x5711": Q(-59, 24),
    "x0311": Q(-137, 50),
    "x5601": Q(-47, 24),
    "x6711": Q(-137, 2000),
    "x6700": Q(-41, 60),
    # Edge 07 is dead for the eight-site tensor on this support, but its four
    # cells are retained because they affect deletion packets.
    "x0700": Q(-3),
    "x0711": Q(-11, 4),
    "x0701": Q(9, 4),
    "x0710": Q(10),
}


def parameterized_source(parameters):
    """Evaluate the 26-parameter rational chart.

    Every named parameter must be nonzero.  The formulas are valid on the
    open set where their displayed denominators are nonzero.  They solve the
    28 potentially supported tensor equations triangularly; all other tensor
    coefficients vanish from the support pattern alone.
    """

    cells = {}

    def put(name, value):
        cells[named_cell(name)] = value

    def get(name):
        return cells[named_cell(name)]

    require(
        set(parameters) == set(DEFAULT_PARAMETERS),
        "parameter names do not match the rational chart",
    )
    require(all(parameters.values()), "chart parameters must be nonzero")
    for name, value in parameters.items():
        put(name, value)

    # The two pure coefficients.
    put("x2411", 1 / (get("x0311") * get("x1611") * get("x5711")))
    put("x1500", 1 / (get("x0400") * get("x2600") * get("x3700")))

    # Five binomial equations; a sixth supported binomial is their
    # compatibility consequence.
    put("x1201", -get("x1600") * get("x2411") / get("x4610"))
    put("x1200", -get("x1500") * get("x2601") / get("x5601"))
    put("x1401", -get("x1200") * get("x4610") / get("x2600"))
    put("x2611", -get("x1201") * get("x5601") / get("x1500"))
    put("x4611", -get("x1401") * get("x2601") / get("x1200"))

    # Four more binomial equations at the two colour-one shores.
    put("x0101", -get("x0500") * get("x1611") / get("x5601"))
    put("x0111", -get("x0510") * get("x1611") / get("x5601"))
    put("x1710", -get("x1611") * get("x5700") / get("x5601"))
    put("x1711", -get("x1611") * get("x5701") / get("x5601"))

    # The remaining eight equations are affine-linear in the new cell.
    put(
        "x0201",
        -(
            get("x0500") * get("x1201") * get("x4610")
            + get("x0500") * get("x1600") * get("x2411")
            + get("x0600") * get("x1500") * get("x2411")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x0211",
        -(
            get("x0510") * get("x1201") * get("x4610")
            + get("x0510") * get("x1600") * get("x2411")
            + get("x0610") * get("x1500") * get("x2411")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x0100",
        -(
            get("x0201") * get("x1401") * get("x5601")
            + get("x0201") * get("x1500") * get("x4611")
            + get("x0500") * get("x1201") * get("x4611")
            + get("x0500") * get("x1401") * get("x2611")
            + get("x0601") * get("x1500") * get("x2411")
        )
        / (get("x2411") * get("x5601")),
    )
    put(
        "x0110",
        -(
            get("x0211") * get("x1401") * get("x5601")
            + get("x0211") * get("x1500") * get("x4611")
            + get("x0510") * get("x1201") * get("x4611")
            + get("x0510") * get("x1401") * get("x2611")
            + get("x0611") * get("x1500") * get("x2411")
        )
        / (get("x2411") * get("x5601")),
    )
    put(
        "x2710",
        -(
            get("x1201") * get("x4610") * get("x5700")
            + get("x1500") * get("x2411") * get("x6700")
            + get("x1600") * get("x2411") * get("x5700")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x2711",
        -(
            get("x1201") * get("x4610") * get("x5701")
            + get("x1500") * get("x2411") * get("x6701")
            + get("x1600") * get("x2411") * get("x5701")
        )
        / (get("x1500") * get("x4610")),
    )
    put(
        "x1700",
        -(
            get("x1201") * get("x4611") * get("x5700")
            + get("x1401") * get("x2611") * get("x5700")
            + get("x1401") * get("x2710") * get("x5601")
            + get("x1500") * get("x2411") * get("x6710")
            + get("x1500") * get("x2710") * get("x4611")
        )
        / (get("x2411") * get("x5601")),
    )
    put(
        "x1701",
        -(
            get("x1201") * get("x4611") * get("x5701")
            + get("x1401") * get("x2611") * get("x5701")
            + get("x1401") * get("x2711") * get("x5601")
            + get("x1500") * get("x2411") * get("x6711")
            + get("x1500") * get("x2711") * get("x4611")
        )
        / (get("x2411") * get("x5601")),
    )

    require(len(cells) == 45, "source support changed")
    require(all(cells.values()), "source has an accidental zero cell")
    return cells


def source():
    """Return the small-rational rank-53 specialization of the chart."""

    return parameterized_source(DEFAULT_PARAMETERS)


def verify_parameterized_chart():
    """Verify all 256 tensor identities in the Laurent function field."""

    names = tuple(sorted(DEFAULT_PARAMETERS))
    parameters = {
        name: LaurentPolynomial.variable(index, len(names))
        for index, name in enumerate(names)
    }
    verify_matching_tensor(parameterized_source(parameters))


def coefficient(cells, vertices, local_word):
    assignment = dict(zip(vertices, local_word))
    answer = Q(0)
    for matching in MATCHINGS[tuple(vertices)]:
        term = Q(1)
        for u, v in matching:
            term *= cells.get((u, v, assignment[u], assignment[v]), 0)
        answer += term
    return answer


def verify_matching_tensor(cells):
    for word in WORDS8:
        expected = Q(1) if len(set(word)) == 1 else Q(0)
        require(
            coefficient(cells, VERTICES, word) == expected,
            f"matching-tensor failure at {word}",
        )


def differential_matrix(cells, deleted):
    remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted)
    words = tuple(product(COLOURS, repeat=6))
    columns = tuple(
        (u, v, a, b)
        for u, v in combinations(remaining, 2)
        for a, b in product(COLOURS, repeat=2)
    )
    matrix = []
    for word in words:
        assignment = dict(zip(remaining, word))
        row = []
        for u, v, a, b in columns:
            if (assignment[u], assignment[v]) != (a, b):
                row.append(Q(0))
                continue
            cofactor_vertices = tuple(
                vertex for vertex in remaining if vertex not in (u, v)
            )
            cofactor_word = tuple(assignment[vertex] for vertex in cofactor_vertices)
            row.append(coefficient(cells, cofactor_vertices, cofactor_word))
        matrix.append(row)
    return matrix


def field_rank(matrix):
    rows = [list(row) for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, height) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for index in range(rank + 1, height):
            multiple = rows[index][column]
            if multiple:
                rows[index] = [
                    left - multiple * right
                    for left, right in zip(rows[index], rows[rank])
                ]
        rank += 1
        if rank == height:
            break
    return rank


def rank_profile(cells):
    profile = {}
    for deleted in EDGES:
        matrix = differential_matrix(cells, deleted)
        full_rank = field_rank(matrix)
        # Rows 0 and 63 are the two pure outputs; removing them realizes the
        # mixed-output quotient because both pure vectors lie in im(dPsi).
        mixed_rank = field_rank(matrix[1:-1])
        profile[deleted] = (full_rank, mixed_rank)
    return profile


def main():
    cells = source()
    verify_parameterized_chart()
    verify_matching_tensor(cells)
    profile = rank_profile(cells)

    require(
        all(full == mixed + 2 for full, mixed in profile.values()),
        "pure-output rank drop is not uniformly two",
    )
    require(profile[3, 4] == (53, 51), "rank-53 deletion changed")

    histogram = Counter(profile.values())
    expected_histogram = Counter(
        {
            (14, 12): 1,
            (23, 21): 3,
            (27, 25): 1,
            (28, 26): 2,
            (29, 27): 2,
            (32, 30): 2,
            (33, 31): 1,
            (35, 33): 1,
            (36, 34): 1,
            (39, 37): 1,
            (40, 38): 1,
            (42, 40): 4,
            (43, 41): 1,
            (45, 43): 2,
            (46, 44): 2,
            (51, 49): 2,
            (53, 51): 1,
        }
    )
    require(histogram == expected_histogram, "exact rank histogram changed")
    print("verified 26-parameter chart identically over a Laurent function field")
    print("verified exact 45-cell rational binary GHZ8 matching tensor")
    print("verified exact full/mixed residual ranks after all 28 deletions")
    print(f"maximum rank {max(full for full, _ in profile.values())} at (3, 4)")
    print("rank-pair histogram:", sorted(histogram.items()))


if __name__ == "__main__":
    main()
