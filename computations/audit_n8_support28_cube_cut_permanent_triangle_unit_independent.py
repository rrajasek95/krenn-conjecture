#!/usr/bin/env python3
"""Exact coefficient-fibre exclusion for the first global support-28 guard.

The support was printed by ``search_n8_global_occurrence_cnf.py`` in its
pair-target, minimum-support-18 SAT run on 2026-08-14.  At occurrence level it
has no mixed singleton.  This checker descends to the diagonal coefficient
fibre and proves that fibre empty over every characteristic-zero field.

The decisive three rows are 00110022, 00210102, and 00112002.  After removing
their supported complementary pair factors they are the three permanents of
one 2-by-3 matrix.  Their standard permanent-triangle identity has a monomial
right side, hence is a unit after localizing every declared support cell.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product


N = 8
COLORS = (0, 1, 2)
VERTICES = tuple(range(N))
EDGES = tuple((left, right) for left in VERTICES
              for right in range(left + 1, N))
TARGET_EDGE = (0, 1)

# Literal solver output, with every one of the 28 graph edges live.
SUPPORT = {
    (0, 1): (1, 2),
    (0, 2): (1,),
    (0, 3): (2,),
    (0, 4): (0, 1),
    (0, 5): (0, 1, 2),
    (0, 6): (0,),
    (0, 7): (0, 2),
    (1, 2): (2,),
    (1, 3): (1,),
    (1, 4): (0, 2),
    (1, 5): (0,),
    (1, 6): (0, 1, 2),
    (1, 7): (0, 1),
    (2, 3): (1, 2),
    (2, 4): (0,),
    (2, 5): (0, 2),
    (2, 6): (0, 1),
    (2, 7): (0, 1, 2),
    (3, 4): (0, 1, 2),
    (3, 5): (0, 1),
    (3, 6): (0, 2),
    (3, 7): (0,),
    (4, 5): (2,),
    (4, 6): (1,),
    (4, 7): (1, 2),
    (5, 6): (1, 2),
    (5, 7): (1,),
    (6, 7): (2,),
}

# The witness is the three-coordinate cut system on the affine cube.  The
# slightly nonbinary vertex order is the literal order printed by the solver.
CUBE_BITS = {
    0: (0, 0, 0),
    1: (0, 1, 1),
    2: (0, 1, 0),
    3: (0, 0, 1),
    4: (1, 1, 0),
    5: (1, 1, 1),
    6: (1, 0, 0),
    7: (1, 0, 1),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def variable(colour, endpoints):
    endpoints = edge(*endpoints)
    return f"q{colour}_{endpoints[0]}{endpoints[1]}"


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


# Sparse integer polynomials; a monomial is a sorted tuple of variable names.
def polynomial(*terms):
    answer = Counter()
    for coefficient, monomial in terms:
        monomial = tuple(sorted(monomial))
        answer[monomial] += coefficient
        if not answer[monomial]:
            del answer[monomial]
    return dict(answer)


def add(*polynomials):
    answer = Counter()
    for item in polynomials:
        answer.update(item)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def scale(coefficient, source):
    return {monomial: coefficient * value
            for monomial, value in source.items() if coefficient * value}


def multiply(left, right):
    answer = Counter()
    for first, first_value in left.items():
        for second, second_value in right.items():
            answer[tuple(sorted(first + second))] += first_value * second_value
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def monomial(*variables):
    return {tuple(sorted(variables)): 1}


def hafnian_coefficient(word):
    """Literal coefficient of the fixed eight-site diagonal hafnian row."""
    answer = Counter()
    for matching in MATCHINGS:
        cells = []
        for endpoints in matching:
            left, right = endpoints
            if word[left] != word[right]:
                break
            colour = word[left]
            if colour not in SUPPORT[endpoints]:
                break
            cells.append(variable(colour, endpoints))
        else:
            answer[tuple(sorted(cells))] += 1
    return dict(answer)


def occurrence_histogram():
    counts = Counter()
    for word in product(COLORS, repeat=N):
        # The occurrence CNF inventories precisely the potentially nonzero
        # diagonal words.  An odd colour class has no compatible matching and
        # is identically zero before support is considered.
        if any(word.count(colour) % 2 for colour in COLORS):
            continue
        counts[len(hafnian_coefficient(word))] += 1
    return tuple(sorted(counts.items()))


def support_signature(support):
    return tuple(sum(1 << colour for colour in support[endpoints])
                 for endpoints in EDGES)


def transform_support(support, vertex_permutation, swap_colours):
    answer = {}
    for endpoints, colours in support.items():
        moved_edge = edge(*(vertex_permutation[vertex]
                            for vertex in endpoints))
        moved_colours = tuple(sorted(
            (2 if colour == 1 else 1 if colour == 2 else 0)
            if swap_colours else colour
            for colour in colours
        ))
        answer[moved_edge] = moved_colours
    return answer


def canonical_orbit():
    signatures = set()
    best = None
    best_maps = []
    for swap_endpoints in (False, True):
        for tail in permutations(range(2, N)):
            moved = {
                0: 1 if swap_endpoints else 0,
                1: 0 if swap_endpoints else 1,
                **{old: new for old, new in zip(range(2, N), tail)},
            }
            for swap_colours in (False, True):
                transformed = transform_support(
                    SUPPORT, moved, swap_colours
                )
                signature = support_signature(transformed)
                signatures.add(signature)
                datum = (swap_endpoints, tail, swap_colours)
                if best is None or signature < best:
                    best = signature
                    best_maps = [datum]
                elif signature == best:
                    best_maps.append(datum)
    expected = (
        6, 1, 2, 3, 4, 5, 7,
        7, 4, 5, 2, 3, 1,
        3, 2, 5, 4, 6,
        1, 6, 7, 5,
        7, 6, 4,
        1, 3,
        2,
    )
    require(best == expected, ("canonical support signature moved", best))
    require(len(signatures) == 720 and len(best_maps) == 4,
            (len(signatures), len(best_maps)))
    require(best_maps[0] ==
            (False, (3, 5, 4, 7, 2, 6), False), best_maps[0])
    return best, len(signatures), 2880 // len(signatures), best_maps[0]


def supervertex_design_crosscheck():
    """Bridge the printed cube-cut model to the parallel K4 design normal form."""
    left = (0, 1, 2, 3)
    right = (4, 6, 7, 5)
    factor_colour = {
        frozenset((0, 1)): 0,
        frozenset((2, 3)): 0,
        frozenset((0, 2)): 2,
        frozenset((1, 3)): 2,
        frozenset((0, 3)): 1,
        frozenset((1, 2)): 1,
    }
    design = {}
    for index in range(4):
        design[edge(left[index], right[index])] = COLORS
    for first in range(4):
        for second in range(first + 1, 4):
            colour = factor_colour[frozenset((first, second))]
            complement = tuple(item for item in COLORS if item != colour)
            design[edge(left[first], left[second])] = complement
            design[edge(right[first], right[second])] = complement
            design[edge(left[first], right[second])] = (colour,)
            design[edge(left[second], right[first])] = (colour,)
    require(len(design) == 28 and design[TARGET_EDGE] == (1, 2), design)

    action = {
        0: 0,
        1: 1,
        **dict(zip(range(2, N), (5, 7, 2, 4, 6, 3))),
    }
    require(transform_support(SUPPORT, action, False) == design,
            "printed support did not map to the K4 design normal form")
    return (False, (5, 7, 2, 4, 6, 3), False)


def complementary_pairing(colour, minor_vertices):
    """Find supported singleton factors in the two other colours."""
    complement = set(VERTICES).difference(minor_vertices)
    others = tuple(item for item in COLORS if item != colour)
    for first_colour, second_colour in (others, tuple(reversed(others))):
        for first_pair in combinations(sorted(complement), 2):
            second_pair = tuple(sorted(complement.difference(first_pair)))
            if (first_colour in SUPPORT[edge(*first_pair)]
                    and second_colour in SUPPORT[edge(*second_pair)]):
                return (first_colour, first_pair,
                        second_colour, second_pair)
    return None


def permanent_triangles():
    """All support patterns yielding the three-minor Laurent unit."""
    answer = []
    for colour in COLORS:
        for rows in combinations(VERTICES, 2):
            available = tuple(vertex for vertex in VERTICES
                              if vertex not in rows)
            for columns in combinations(available, 3):
                if not all(colour in SUPPORT[edge(row, column)]
                           for row in rows for column in columns):
                    continue
                completions = {
                    pair: complementary_pairing(colour, rows + pair)
                    for pair in combinations(columns, 2)
                }
                if all(completions.values()):
                    answer.append((colour, rows, columns, completions))
    return tuple(answer)


def word_for_minor(colour, rows, columns, completion):
    word = [None] * N
    for vertex in rows + columns:
        word[vertex] = colour
    first_colour, first_pair, second_colour, second_pair = completion
    for vertex in first_pair:
        word[vertex] = first_colour
    for vertex in second_pair:
        word[vertex] = second_colour
    require(None not in word, word)
    return tuple(word)


def audit_selected_unit(triangle):
    colour, rows, columns, completions = triangle
    require((colour, rows, columns) == (0, (0, 1), (4, 5, 6)),
            (colour, rows, columns))
    left, right = rows
    first, second, third = columns

    a = variable(colour, edge(left, first))
    b = variable(colour, edge(left, second))
    c = variable(colour, edge(left, third))
    d = variable(colour, edge(right, first))
    e = variable(colour, edge(right, second))
    f = variable(colour, edge(right, third))

    expected_words = ((0, 0, 1, 1, 0, 0, 2, 2),
                      (0, 0, 2, 1, 0, 1, 0, 2),
                      (0, 0, 1, 1, 2, 0, 0, 2))
    pairs = ((first, second), (first, third), (second, third))
    minors = (
        add(monomial(a, e), monomial(b, d)),
        add(monomial(a, f), monomial(c, d)),
        add(monomial(b, f), monomial(c, e)),
    )
    prefactors = []
    source_rows = []
    for pair, expected_word, expected_minor in zip(
            pairs, expected_words, minors, strict=True):
        completion = completions[pair]
        word = word_for_minor(colour, rows, pair, completion)
        require(word == expected_word, (word, expected_word))
        first_colour, first_pair, second_colour, second_pair = completion
        prefactor = monomial(variable(first_colour, first_pair),
                             variable(second_colour, second_pair))
        coefficient = hafnian_coefficient(word)
        require(coefficient == multiply(prefactor, expected_minor),
                (word, coefficient, multiply(prefactor, expected_minor)))
        require(len(coefficient) == 2, (word, coefficient))
        prefactors.append(prefactor)
        source_rows.append(coefficient)

    u_first, u_second, u_third = prefactors
    row_first, row_second, row_third = source_rows
    common = multiply(multiply(u_first, u_second), u_third)

    # c*E_first + b*E_second - a*E_third = 2*b*c*d.
    # Clear the three supported pair prefactors so the identity lives in the
    # ordinary polynomial ring before localization.
    lhs = add(
        multiply(monomial(c), multiply(u_second,
                                       multiply(u_third, row_first))),
        multiply(monomial(b), multiply(u_first,
                                       multiply(u_third, row_second))),
        scale(-1, multiply(monomial(a), multiply(
            u_first, multiply(u_second, row_third)))),
    )
    rhs = scale(2, multiply(monomial(b, c, d), common))
    require(lhs == rhs and len(rhs) == 1, (lhs, rhs))

    supported_variables = {
        variable(colour_item, endpoints)
        for endpoints, colours in SUPPORT.items()
        for colour_item in colours
    }
    rhs_monomial, rhs_coefficient = next(iter(rhs.items()))
    require(rhs_coefficient == 2
            and set(rhs_monomial) <= supported_variables,
            (rhs_coefficient, rhs_monomial))
    return {
        "words": tuple("".join(map(str, word)) for word in expected_words),
        "row_term_counts": tuple(map(len, source_rows)),
        "rhs_coefficient": rhs_coefficient,
        "rhs_monomial_degree": len(rhs_monomial),
    }


def main():
    require(tuple(sorted(SUPPORT)) == EDGES, "support is not the full K8")
    require(SUPPORT[TARGET_EDGE] == (1, 2), SUPPORT[TARGET_EDGE])
    require(Counter(map(len, SUPPORT.values())) == {1: 12, 2: 12, 3: 4},
            Counter(map(len, SUPPORT.values())))
    for endpoints in EDGES:
        expected = tuple(colour for colour in COLORS
                         if CUBE_BITS[endpoints[0]][colour]
                         != CUBE_BITS[endpoints[1]][colour])
        require(SUPPORT[endpoints] == expected,
                ("cube-cut description failed", endpoints,
                 SUPPORT[endpoints], expected))
    require(tuple(sum(colour in colours for colours in SUPPORT.values())
                  for colour in COLORS) == (16, 16, 16),
            "colour support sizes moved")
    require(len(MATCHINGS) == 105, len(MATCHINGS))
    histogram = occurrence_histogram()
    require(histogram == ((0, 1332), (2, 204), (4, 54),
                          (6, 48), (24, 3)), histogram)

    canonical = canonical_orbit()
    design_map = supervertex_design_crosscheck()
    triangles = permanent_triangles()
    triangle_colours = Counter(item[0] for item in triangles)
    require(len(triangles) == 96 and triangle_colours == {0: 32, 1: 32, 2: 32},
            (len(triangles), triangle_colours))
    selected = audit_selected_unit(triangles[0])

    print("support-28 cube-cut coefficient fibre: EMPTY")
    print("canonical orbit size / stabilizer", canonical[1], canonical[2])
    print("canonical map", canonical[3])
    print("parallel K4-design map", design_map)
    print("occurrence histogram", histogram)
    print("permanent triangles", len(triangles), tuple(sorted(
        triangle_colours.items())))
    print("selected Laurent unit", selected)
    print("consequence: three mixed source rows generate 1 after support localization")


if __name__ == "__main__":
    main()
