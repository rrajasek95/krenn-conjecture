#!/usr/bin/env python3
r"""Exact support certificate for the 2+2+2 cofactor-graph boundary.

The six vertices are the directed half-edges of a triangle:

    0=01, 1=02, 2=10, 3=12, 4=20, 5=21.

Vertices with the same first digit form one of the classes U_0,U_1,U_2.
The three nonzero-cofactor components are the reverse pairs

    01--10, 02--20, 12--21.

Thus the other nine mixed pairs are holes whose complementary projected
K_4 matching tensors vanish.  On S_r=R\U_r the pure tensor is a nonzero
multiple of e_r^4.

The pure-K_4 extension-annihilator lemma supplies two support rules:

* every edge in S_r has no coefficient transverse to e_r at both ends;
* S_r has a target-aligned apex: at that vertex every incident coefficient
  has endpoint color r.

There are 4^3=64 apex triples.  The S_3 action on the class/color triangle
has twelve orbits.  For each orbit representative below, a tiny collection
of zero cofactor coefficients and nonzero pure target coefficients already
has no possible zero/nonzero support pattern.  This script checks those
five certificate types by exhaustive Boolean enumeration (at most 2^14
assignments per row).  The implication is exact over every field: a zero
sum of matching monomials cannot have exactly one nonzero summand, while a
nonzero pure coefficient must have at least one nonzero summand.
"""

from itertools import combinations, permutations, product


VERTICES = tuple(range(6))
LABEL = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}
DIRECTED_NAME = {0: "01", 1: "02", 2: "10", 3: "12", 4: "20", 5: "21"}
DIRECTED_VERTEX = {name: vertex for vertex, name in DIRECTED_NAME.items()}
CLASSES = {
    color: frozenset(vertex for vertex in VERTICES if LABEL[vertex] == color)
    for color in range(3)
}
PURE_SETS = {
    color: frozenset(VERTICES) - CLASSES[color] for color in range(3)
}
PLANES = {
    vertex: tuple(color for color in range(3) if color != LABEL[vertex])
    for vertex in VERTICES
}
GRAPH_EDGES = frozenset({(0, 2), (1, 4), (3, 5)})
MIXED_PAIRS = frozenset(
    edge
    for edge in combinations(VERTICES, 2)
    if LABEL[edge[0]] != LABEL[edge[1]]
)
ZERO_HOLES = MIXED_PAIRS - GRAPH_EDGES

# The three perfect matchings of four ordered sites, expressed in positions.
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def oriented_cell(i, j, color_i, color_j):
    """Return one canonical key for a projected edge coefficient."""

    if i < j:
        return i, j, color_i, color_j
    return j, i, color_j, color_i


def coefficient_terms(four_set, colors):
    """Return the three two-cell monomials in one K_4 coefficient."""

    sites = tuple(sorted(four_set))
    return tuple(
        tuple(
            oriented_cell(
                sites[i], sites[j], colors[sites[i]], colors[sites[j]]
            )
            for i, j in matching
        )
        for matching in MATCHINGS
    )


def target_transverse_cells():
    """Cells not killed by the three pure-tensor bottom-right equations."""

    cells = set()
    for i, j in combinations(VERTICES, 2):
        for color_i in PLANES[i]:
            for color_j in PLANES[j]:
                transverse_somewhere = any(
                    i in PURE_SETS[r]
                    and j in PURE_SETS[r]
                    and color_i != r
                    and color_j != r
                    for r in range(3)
                )
                if not transverse_somewhere:
                    cells.add((i, j, color_i, color_j))
    return frozenset(cells)


BASE_CELLS = target_transverse_cells()


def cells_after_apices(apices):
    """Apply the target-line condition at the three chosen apices."""

    allowed = set(BASE_CELLS)
    for r, apex in enumerate(apices):
        assert apex in PURE_SETS[r]
        for other in PURE_SETS[r] - {apex}:
            for cell in tuple(allowed):
                if {cell[0], cell[1]} != {apex, other}:
                    continue
                apex_color = cell[2] if cell[0] == apex else cell[3]
                if apex_color != r:
                    allowed.remove(cell)
    return frozenset(allowed)


def zero_constraint(hole, colors, allowed):
    """Live matching monomials in a zero complementary-K_4 coefficient."""

    assert tuple(sorted(hole)) in ZERO_HOLES
    four_set = frozenset(VERTICES) - frozenset(hole)
    sites = tuple(sorted(four_set))
    assert len(colors) == 4
    color_map = dict(zip(sites, colors))
    assert all(color_map[v] in PLANES[v] for v in sites)
    return tuple(
        term
        for term in coefficient_terms(four_set, color_map)
        if all(cell in allowed for cell in term)
    )


def pure_target_constraint(r, allowed):
    """Live monomials in the nonzero e_r^4 coefficient on S_r."""

    colors = {vertex: r for vertex in PURE_SETS[r]}
    return tuple(
        term
        for term in coefficient_terms(PURE_SETS[r], colors)
        if all(cell in allowed for cell in term)
    )


# Each zero entry is (mixed hole, colors on the sorted complementary K_4).
# Each pure entry is a color r whose e_r^4 coefficient is nonzero.
CERTIFICATE_TYPES = {
    "A": {
        "zero": (
            ((2, 4), (1, 2, 2, 1)),
            ((2, 4), (2, 1, 2, 1)),
            ((2, 5), (2, 1, 2, 1)),
            ((3, 4), (2, 1, 2, 1)),
        ),
        "pure": (1, 2),
        "shape": ((1, 1, 1, 1), (2, 2)),
    },
    "B": {
        "zero": (
            ((0, 5), (2, 0, 2, 0)),
            ((0, 5), (2, 2, 0, 0)),
            ((1, 5), (2, 0, 2, 0)),
            ((1, 5), (2, 2, 0, 0)),
        ),
        "pure": (0, 2),
        "shape": ((1, 1, 1, 1), (2, 2)),
    },
    "C": {
        "zero": (
            ((0, 4), (2, 2, 0, 0)),
            ((0, 5), (2, 2, 0, 0)),
            ((2, 4), (1, 2, 2, 1)),
            ((2, 5), (1, 2, 2, 1)),
        ),
        "pure": (0, 1, 2),
        "shape": ((1, 1, 1, 1), (2, 2, 2)),
    },
    "D": {
        "zero": (
            ((0, 5), (2, 0, 2, 0)),
            ((1, 5), (2, 2, 0, 0)),
            ((1, 5), (2, 2, 2, 0)),
            ((2, 4), (2, 1, 2, 1)),
            ((2, 5), (2, 1, 2, 1)),
        ),
        "pure": (0, 1, 2),
        "shape": ((2, 1, 1, 1, 1), (2, 2, 2)),
    },
    "E": {
        "zero": (
            ((0, 4), (2, 0, 2, 0)),
            ((0, 5), (2, 0, 2, 0)),
            ((0, 5), (2, 2, 0, 0)),
            ((1, 5), (2, 0, 2, 0)),
            ((1, 5), (2, 2, 2, 0)),
        ),
        "pure": (0, 2),
        "shape": ((1, 1, 2, 1, 1), (2, 2)),
    },
}


# Orbit representatives are triples (apex for S_0, apex for S_1,
# apex for S_2).  This is also the finite certificate table.
REPRESENTATIVE_TYPE = {
    (2, 0, 0): "A",
    (2, 0, 1): "D",
    (2, 1, 0): "C",
    (2, 1, 1): "A",
    (2, 1, 2): "B",
    (2, 1, 3): "C",
    (2, 4, 0): "C",
    (2, 4, 1): "D",
    (2, 4, 2): "B",
    (2, 5, 1): "D",
    (3, 1, 0): "E",
    (3, 4, 0): "E",
}


# Names used in the hand proof.  The first twelve are the entries of the
# three target 2-by-2 matrices; the last four occur in motifs D and E.
SCALAR_NAME = {
    (0, 2, 2, 2): "a",
    (0, 3, 2, 2): "b",
    (0, 4, 1, 1): "c",
    (0, 5, 1, 1): "d",
    (1, 2, 2, 2): "e",
    (1, 3, 2, 2): "f",
    (1, 4, 1, 1): "g",
    (1, 5, 1, 1): "h",
    (2, 4, 0, 0): "i",
    (2, 5, 0, 0): "j",
    (3, 4, 0, 0): "k",
    (3, 5, 0, 0): "l",
    (1, 2, 2, 0): "mu",
    (3, 4, 2, 0): "nu",
    (1, 3, 2, 0): "rho",
    (2, 4, 2, 0): "sigma",
}


def normalized_expression(*monomials):
    return tuple(sorted(tuple(sorted(monomial)) for monomial in monomials))


# Exact scalar expansions displayed in the companion mathematical note.
EXPECTED_EXPANSIONS = {
    "A": {
        "zero": tuple(
            normalized_expression(monomial)
            for monomial in (("d", "f"), ("b", "h"), ("b", "g"), ("a", "h"))
        ),
        "pure": (
            normalized_expression(("c", "h"), ("d", "g")),
            normalized_expression(("a", "f"), ("b", "e")),
        ),
    },
    "B": {
        "zero": tuple(
            normalized_expression(monomial)
            for monomial in (("f", "i"), ("e", "k"), ("b", "i"), ("a", "k"))
        ),
        "pure": (
            normalized_expression(("i", "l"), ("j", "k")),
            normalized_expression(("a", "f"), ("b", "e")),
        ),
    },
    "C": {
        "zero": tuple(
            normalized_expression(monomial)
            for monomial in (("e", "l"), ("e", "k"), ("d", "f"), ("c", "f"))
        ),
        "pure": (
            normalized_expression(("i", "l"), ("j", "k")),
            normalized_expression(("c", "h"), ("d", "g")),
            normalized_expression(("a", "f"), ("b", "e")),
        ),
    },
    "D": {
        "zero": (
            normalized_expression(("mu", "nu"), ("f", "i")),
            normalized_expression(("a", "k")),
            normalized_expression(("a", "nu")),
            normalized_expression(("b", "h")),
            normalized_expression(("b", "g")),
        ),
        "pure": (
            normalized_expression(("i", "l"), ("j", "k")),
            normalized_expression(("c", "h"), ("d", "g")),
            normalized_expression(("a", "f"), ("b", "e")),
        ),
    },
    "E": {
        "zero": (
            normalized_expression(("f", "j")),
            normalized_expression(("f", "i")),
            normalized_expression(("e", "k"), ("rho", "sigma")),
            normalized_expression(("b", "i")),
            normalized_expression(("b", "sigma")),
        ),
        "pure": (
            normalized_expression(("i", "l"), ("j", "k")),
            normalized_expression(("a", "f"), ("b", "e")),
        ),
    },
}


def permute_apices(apices, permutation):
    """Simultaneously permute site classes, target colors, and components."""

    answer = [None, None, None]
    for r, vertex in enumerate(apices):
        c, d = map(int, DIRECTED_NAME[vertex])
        moved = DIRECTED_VERTEX[f"{permutation[c]}{permutation[d]}"]
        answer[permutation[r]] = moved
    return tuple(answer)


def apex_orbits():
    all_triples = set(product(*(tuple(sorted(PURE_SETS[r])) for r in range(3))))
    orbits = []
    while all_triples:
        representative = min(all_triples)
        orbit = frozenset(
            permute_apices(representative, permutation)
            for permutation in permutations(range(3))
        )
        orbits.append((representative, orbit))
        all_triples -= orbit
    return tuple(orbits)


def support_is_possible(zero_terms, pure_terms, cells, mask):
    nonzero = {
        cell for index, cell in enumerate(cells) if (mask >> index) & 1
    }

    # A zero coefficient cannot have exactly one nonzero summand.
    for terms in zero_terms:
        count = sum(all(cell in nonzero for cell in term) for term in terms)
        if count == 1:
            return False

    # A nonzero coefficient has at least one nonzero summand.
    for terms in pure_terms:
        if not any(all(cell in nonzero for cell in term) for term in terms):
            return False

    return True


def audit_representative(apices, certificate_type):
    allowed = cells_after_apices(apices)
    certificate = CERTIFICATE_TYPES[certificate_type]
    zero_terms = tuple(
        zero_constraint(hole, colors, allowed)
        for hole, colors in certificate["zero"]
    )
    pure_terms = tuple(
        pure_target_constraint(r, allowed) for r in certificate["pure"]
    )
    expected_zero_shape, expected_pure_shape = certificate["shape"]
    assert tuple(map(len, zero_terms)) == expected_zero_shape
    assert tuple(map(len, pure_terms)) == expected_pure_shape

    def render(terms):
        assert all(cell in SCALAR_NAME for term in terms for cell in term)
        return normalized_expression(
            *(tuple(SCALAR_NAME[cell] for cell in term) for term in terms)
        )

    rendered = {
        "zero": tuple(render(terms) for terms in zero_terms),
        "pure": tuple(render(terms) for terms in pure_terms),
    }
    assert rendered == EXPECTED_EXPANSIONS[certificate_type]

    relevant_cells = tuple(
        sorted(
            {
                cell
                for constraint in zero_terms + pure_terms
                for term in constraint
                for cell in term
            }
        )
    )
    assert len(relevant_cells) <= 14
    survivors = sum(
        support_is_possible(zero_terms, pure_terms, relevant_cells, mask)
        for mask in range(1 << len(relevant_cells))
    )
    assert survivors == 0
    return len(relevant_cells), 1 << len(relevant_cells)


def main():
    assert len(BASE_CELLS) == 42
    assert len(MIXED_PAIRS) == 12
    assert len(ZERO_HOLES) == 9

    orbits = apex_orbits()
    assert len(orbits) == 12
    assert {representative for representative, _ in orbits} == set(
        REPRESENTATIVE_TYPE
    )
    assert sum(len(orbit) for _, orbit in orbits) == 64

    totals = {name: 0 for name in CERTIFICATE_TYPES}
    print("type  representative  orbit  cells  support assignments")
    for representative, orbit in orbits:
        certificate_type = REPRESENTATIVE_TYPE[representative]
        relevant_cells, assignments = audit_representative(
            representative, certificate_type
        )
        totals[certificate_type] += len(orbit)
        names = "(" + ",".join(DIRECTED_NAME[v] for v in representative) + ")"
        print(
            f" {certificate_type:1}    {names:12}"
            f" {len(orbit):5} {relevant_cells:6} {assignments:20}"
        )

    assert totals == {"A": 12, "B": 12, "C": 18, "D": 14, "E": 8}
    print("verified all 64 target-aligned apex placements")
    print("the 2+2+2 mixed-cofactor component pattern is impossible")


if __name__ == "__main__":
    main()
