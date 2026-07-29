#!/usr/bin/env python3
"""Exact audit for the two-K4 unique-cross-perfect-matching obstruction.

There are two complementary certificates here.

* For a cross graph consisting of one four-edge matching, the script checks
  the 34 maximal Cartesian boxes of live K4 words and the resulting star-box
  contradiction.
* Every bipartite graph with a unique perfect matching embeds in the maximal
  upper-triangular graph.  On that graph the script builds the full Boolean
  support formula for arbitrary 3 by 3 cross matrices.  Nonzero off-diagonal
  block constants need a supported cross monomial, while every zero cross
  fibre is forbidden from having exactly one supported monomial.  The formula
  is UNSAT for all six relative colourings of the two K4 factorizations.

The second test is support-only: it is a necessary condition over arbitrary
complex coefficients and makes no rank, sign, or genericity assumption.
"""

from __future__ import annotations

import hashlib
import itertools

from pysat.formula import IDPool
from pysat.solvers import Solver


COLORS = tuple(range(3))
LOCAL_VERTICES = tuple(range(4))
GLOBAL_VERTICES = tuple(range(8))
FACTORS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
EDGE_COLOR = {
    tuple(sorted(edge)): color
    for color, factor in enumerate(FACTORS)
    for edge in factor
}
TRIANGULAR_EDGES = tuple(
    (left, right)
    for left in LOCAL_VERTICES
    for right in LOCAL_VERTICES
    if left <= right
)
TRIANGULAR_EDGE_SET = frozenset(TRIANGULAR_EDGES)
COLORINGS = tuple(itertools.product(COLORS, repeat=8))
OFF_DIAGONAL_CONSTANTS = frozenset(
    (left_color,) * 4 + (right_color,) * 4
    for left_color in COLORS
    for right_color in COLORS
    if left_color != right_color
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(GLOBAL_VERTICES))


def local_internal_color(
    edge: tuple[int, int], right_color_permutation: tuple[int, int, int]
) -> int:
    u, v = edge
    if u < 4 and v < 4:
        return EDGE_COLOR[u, v]
    assert u >= 4 and v >= 4
    return right_color_permutation[EDGE_COLOR[u - 4, v - 4]]


def cross_terms(
    coloring: tuple[int, ...],
    right_color_permutation: tuple[int, int, int],
) -> tuple[tuple[tuple[int, int, int, int], ...], ...]:
    """All nonzero-crossing matching monomials compatible with ``coloring``."""
    answer = []
    for matching in MATCHINGS:
        cross = []
        compatible = True
        for u, v in matching:
            if u < 4 <= v:
                edge = (u, v - 4)
                if edge not in TRIANGULAR_EDGE_SET:
                    compatible = False
                    break
                cross.append((u, v - 4, coloring[u], coloring[v]))
            elif (u < 4 and v < 4) or (u >= 4 and v >= 4):
                color = local_internal_color((u, v), right_color_permutation)
                if coloring[u] != color or coloring[v] != color:
                    compatible = False
                    break
            else:
                raise AssertionError("matching edges use increasing endpoints")
        if compatible and cross:
            answer.append(tuple(sorted(cross)))
    assert len(answer) == len(set(answer))
    return tuple(answer)


def is_live_word(word: tuple[int, int, int, int]) -> bool:
    return any(
        word[u] == color and word[v] == color
        for (u, v), color in EDGE_COLOR.items()
    )


def box_words(box: tuple[frozenset[int], ...]):
    return itertools.product(*box)


def is_live_box(box: tuple[frozenset[int], ...]) -> bool:
    return all(is_live_word(word) for word in box_words(box))


def factor_color_permutation(vertex_permutation: tuple[int, ...]):
    answer = []
    for color in COLORS:
        u, v = FACTORS[color][0]
        image = tuple(
            sorted((vertex_permutation[u], vertex_permutation[v]))
        )
        answer.append(EDGE_COLOR[image])
    assert sorted(answer) == list(COLORS)
    return tuple(answer)


def transform_box(box, vertex_permutation):
    color_permutation = factor_color_permutation(vertex_permutation)
    image = [None] * 4
    for vertex in LOCAL_VERTICES:
        image[vertex_permutation[vertex]] = frozenset(
            color_permutation[color] for color in box[vertex]
        )
    return tuple(image)


def correction_colors(box: tuple[frozenset[int], ...]) -> frozenset[int]:
    answer = set()
    for color in COLORS:
        active = {vertex for vertex in LOCAL_VERTICES if color in box[vertex]}
        if len(active) == 4 or any(set(edge) <= active for edge in FACTORS[color]):
            answer.add(color)
    return frozenset(answer)


def star_box(center: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(COLORS)
        if vertex == center
        else frozenset({EDGE_COLOR[tuple(sorted((center, vertex)))]})
        for vertex in LOCAL_VERTICES
    )


def audit_live_boxes_and_bare_matching() -> None:
    nonempty_subsets = tuple(
        frozenset(color for color in COLORS if mask >> color & 1)
        for mask in range(1, 1 << len(COLORS))
    )
    live_boxes = tuple(
        box
        for box in itertools.product(nonempty_subsets, repeat=4)
        if is_live_box(box)
    )
    maximal = tuple(
        box
        for box in live_boxes
        if not any(
            box != larger
            and all(box[v] <= larger[v] for v in LOCAL_VERTICES)
            for larger in live_boxes
        )
    )
    assert len(maximal) == 34

    representatives = (
        (
            frozenset({0}),
            frozenset({0, 1, 2}),
            frozenset({2}),
            frozenset({1}),
        ),
        (
            frozenset({0}),
            frozenset({0, 1}),
            frozenset({0}),
            frozenset({0, 1}),
        ),
        (
            frozenset({0}),
            frozenset({0, 1}),
            frozenset({0, 1, 2}),
            frozenset({1}),
        ),
        (
            frozenset({0}),
            frozenset({0}),
            frozenset({0, 1, 2}),
            frozenset({0, 1, 2}),
        ),
    )
    expected_orbit_sizes = (4, 12, 12, 6)
    expected_correction_counts = (3, 2, 2, 1)
    covered = set()
    for representative, orbit_size, correction_count in zip(
        representatives,
        expected_orbit_sizes,
        expected_correction_counts,
        strict=True,
    ):
        orbit = {
            transform_box(representative, permutation)
            for permutation in itertools.permutations(LOCAL_VERTICES)
        }
        assert len(orbit) == orbit_size
        assert orbit <= set(maximal)
        assert all(
            len(correction_colors(box)) == correction_count for box in orbit
        )
        covered.update(orbit)
    assert covered == set(maximal)

    stars = {star_box(center) for center in LOCAL_VERTICES}
    assert stars == {
        box for box in maximal if correction_colors(box) == frozenset(COLORS)
    }

    # If the cross graph is exactly a four-edge matching P, row and column
    # support boxes must both be stars.  A correction (r,s) can then use only
    # P({alpha,i_r})={beta,j_s}.  Exhaust all P and both star centers.
    for matching_permutation in itertools.permutations(LOCAL_VERTICES):
        for left_center, right_center in itertools.product(
            LOCAL_VERTICES, repeat=2
        ):
            possible = set()
            for left_color, right_color in itertools.product(COLORS, repeat=2):
                if left_color == right_color:
                    continue
                left_neighbor = next(
                    vertex
                    for vertex in LOCAL_VERTICES
                    if vertex != left_center
                    and EDGE_COLOR[
                        tuple(sorted((left_center, vertex)))
                    ]
                    == left_color
                )
                right_neighbor = next(
                    vertex
                    for vertex in LOCAL_VERTICES
                    if vertex != right_center
                    and EDGE_COLOR[
                        tuple(sorted((right_center, vertex)))
                    ]
                    == right_color
                )
                image = {
                    matching_permutation[left_center],
                    matching_permutation[left_neighbor],
                }
                if image == {right_center, right_neighbor}:
                    possible.add((left_color, right_color))
            assert possible != {
                (left_color, right_color)
                for left_color in COLORS
                for right_color in COLORS
                if left_color != right_color
            }


def has_directed_cycle(arcs: frozenset[tuple[int, int]]) -> bool:
    for length in range(2, 5):
        for cycle in itertools.permutations(LOCAL_VERTICES, length):
            if cycle[0] != min(cycle):
                continue
            if all(
                (cycle[index], cycle[(index + 1) % length]) in arcs
                for index in range(length)
            ):
                return True
    return False


def topological_order(arcs: frozenset[tuple[int, int]]) -> tuple[int, ...]:
    for order in itertools.permutations(LOCAL_VERTICES):
        position = {vertex: index for index, vertex in enumerate(order)}
        if all(position[u] < position[v] for u, v in arcs):
            return order
    raise AssertionError("acyclic graph has no topological order")


def audit_unique_matching_triangularization() -> None:
    off_diagonal_pairs = tuple(
        (left, right)
        for left in LOCAL_VERTICES
        for right in LOCAL_VERTICES
        if left != right
    )
    permutations = tuple(itertools.permutations(LOCAL_VERTICES))
    unique_count = 0
    for mask in range(1 << len(off_diagonal_pairs)):
        edges = {(index, index) for index in LOCAL_VERTICES}
        edges.update(
            edge
            for bit, edge in enumerate(off_diagonal_pairs)
            if mask >> bit & 1
        )
        perfect = [
            permutation
            for permutation in permutations
            if all((left, permutation[left]) in edges for left in LOCAL_VERTICES)
        ]
        arcs = frozenset(edge for edge in edges if edge[0] != edge[1])
        unique = len(perfect) == 1
        assert unique == (not has_directed_cycle(arcs))
        if unique:
            unique_count += 1
            order = topological_order(arcs)
            position = {vertex: index for index, vertex in enumerate(order)}
            assert all(position[left] <= position[right] for left, right in edges)
    # The normalized unique-matching graphs are exactly the labelled DAGs.
    assert unique_count == 543


class SupportFormula:
    def __init__(self, right_color_permutation: tuple[int, int, int]):
        self.right_color_permutation = right_color_permutation
        self.pool = IDPool()
        self.cell = {
            (left, right, left_color, right_color): self.pool.id(
                ("cell", left, right, left_color, right_color)
            )
            for left, right in TRIANGULAR_EDGES
            for left_color, right_color in itertools.product(COLORS, repeat=2)
        }
        assert len(self.cell) == 90
        self.clauses: list[list[int]] = []
        self.fibre_terms: dict[
            tuple[int, ...],
            tuple[tuple[tuple[int, int, int, int], ...], ...],
        ] = {}
        self._add_nonzero_diagonal_blocks()

    def _add_nonzero_diagonal_blocks(self) -> None:
        for vertex in LOCAL_VERTICES:
            self.clauses.append(
                [
                    self.cell[vertex, vertex, left_color, right_color]
                    for left_color, right_color in itertools.product(
                        COLORS, repeat=2
                    )
                ]
            )

    def encode_fibre(self, coloring: tuple[int, ...]) -> None:
        terms = cross_terms(coloring, self.right_color_permutation)
        self.fibre_terms[coloring] = terms
        witnesses = []
        for term_number, term in enumerate(terms):
            witness = self.pool.id(("term", coloring, term_number))
            witnesses.append(witness)
            literals = [self.cell[cell] for cell in term]
            # witness <=> conjunction(literals)
            self.clauses.extend([-witness, literal] for literal in literals)
            self.clauses.append([witness] + [-literal for literal in literals])

        if coloring in OFF_DIAGONAL_CONSTANTS:
            # T_0 has coefficient one and the target coefficient is zero.
            self.clauses.append(witnesses)
        else:
            # The cross sector must vanish, so it cannot have one nonzero term.
            for witness in witnesses:
                self.clauses.append(
                    [-witness]
                    + [other for other in witnesses if other != witness]
                )

    def encode_all_fibres(self) -> None:
        for coloring in COLORINGS:
            self.encode_fibre(coloring)

    def dimacs_digest(self) -> str:
        payload = "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in self.clauses
        )
        return hashlib.sha256(payload.encode()).hexdigest()


def rup_conflict(clauses: list[list[int]], candidate: list[int]) -> bool:
    """Check reverse-unit-propagation for one proposed learned clause."""
    assignment: dict[int, bool] = {}
    for literal in candidate:
        variable = abs(literal)
        value = literal < 0  # assume the negation of every candidate literal
        if variable in assignment and assignment[variable] != value:
            return True
        assignment[variable] = value

    changed = True
    while changed:
        changed = False
        for clause in clauses:
            unassigned = []
            satisfied = False
            for literal in clause:
                variable = abs(literal)
                if variable not in assignment:
                    unassigned.append(literal)
                elif assignment[variable] == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unassigned:
                return True
            if len(unassigned) == 1:
                literal = unassigned[0]
                variable = abs(literal)
                value = literal > 0
                if variable in assignment:
                    if assignment[variable] != value:
                        return True
                else:
                    assignment[variable] = value
                    changed = True
    return False


def verify_glucose_drup(
    base_clauses: list[list[int]], proof_lines: list[str]
) -> int:
    """Independently verify the additive DRUP portion of a Glucose proof.

    Deletion records may be ignored: retaining clauses only strengthens unit
    propagation.  Every added clause must be RUP, and the last one must be the
    empty clause.
    """
    clauses = [list(clause) for clause in base_clauses]
    additions = []
    for line in proof_lines:
        if line.startswith("d "):
            continue
        literals = [int(token) for token in line.split()]
        assert literals and literals[-1] == 0
        clause = literals[:-1]
        assert rup_conflict(clauses, clause)
        clauses.append(clause)
        additions.append(clause)
    assert additions and additions[-1] == []
    return len(additions)


CANONICAL_CORE_TARGETS = (
    "00001111",
    "00002222",
    "11112222",
)
CANONICAL_CORE_ZEROS = (
    "00012101",
    "00012221",
    "00000100",
    "00002100",
    "00002221",
    "01001100",
    "01012101",
    "01012121",
    "01012202",
    "01111112",
    "01111121",
    "01112112",
    "01112122",
    "10002100",
    "10002111",
    "11012202",
    "00002122",
    "01110021",
)


def word(text: str) -> tuple[int, ...]:
    return tuple(map(int, text))


def audit_canonical_small_core() -> None:
    formula = SupportFormula((0, 1, 2))
    for text in CANONICAL_CORE_TARGETS + CANONICAL_CORE_ZEROS:
        coloring = word(text)
        terms = cross_terms(coloring, (0, 1, 2))
        formula.fibre_terms[coloring] = terms
        witnesses = []
        for term_number, term in enumerate(terms):
            witness = formula.pool.id(("term", coloring, term_number))
            witnesses.append(witness)
            literals = [formula.cell[cell] for cell in term]
            formula.clauses.extend([-witness, literal] for literal in literals)
            formula.clauses.append(
                [witness] + [-literal for literal in literals]
            )
        if text in CANONICAL_CORE_TARGETS:
            formula.clauses.append(witnesses)
        else:
            formula.clauses.extend(
                [-witness]
                + [other for other in witnesses if other != witness]
                for witness in witnesses
            )
    assert sum(map(len, formula.fibre_terms.values())) == 47
    assert formula.pool.top == 137
    assert len(formula.clauses) == 226
    with Solver(name="cadical195", bootstrap_with=formula.clauses) as solver:
        assert not solver.solve()


def audit_full_triangular_formulas() -> None:
    rows = []
    for right_color_permutation in itertools.permutations(COLORS):
        formula = SupportFormula(right_color_permutation)
        formula.encode_all_fibres()
        # Every colouring has the unique four-cross diagonal monomial.  The
        # remaining terms are the compatible two-cross matchings.
        assert all(terms for terms in formula.fibre_terms.values())
        assert all(
            sum(len(term) == 4 for term in terms) == 1
            for terms in formula.fibre_terms.values()
        )
        with Solver(
            name="cadical195", bootstrap_with=formula.clauses
        ) as solver:
            assert not solver.solve()
        with Solver(
            name="glucose4", with_proof=True, bootstrap_with=formula.clauses
        ) as solver:
            assert not solver.solve()
            drup_additions = verify_glucose_drup(
                formula.clauses, solver.get_proof()
            )
        rows.append(
            (
                "".join(map(str, right_color_permutation)),
                formula.pool.top,
                len(formula.clauses),
                sum(map(len, formula.fibre_terms.values())),
                formula.dimacs_digest(),
                drup_additions,
            )
        )

    expected = {
        "012": (
            8676,
            47454,
            8586,
            "d21f736e401dde811a760199de892f1b49d56560da8a896decaa6caac5d21f0d",
        ),
        "021": (
            8676,
            47453,
            8586,
            "2c3556b254b66916892110e26905b877ac2aa3a691e26f81968ff089d04e4ccc",
        ),
        "102": (
            8676,
            47453,
            8586,
            "6c5e63308763551fb30924916221864469f1656eaf79989853cfcfd453711827",
        ),
        "120": (
            8676,
            47453,
            8586,
            "5a85e3b3deef9046e27dfe26a5ef171c9560bcd382b7d30a246b016ffd036d18",
        ),
        "201": (
            8676,
            47453,
            8586,
            "62e56e47016f5861286badb3f577f2ea7d093cbe0fdba5792204855842ec2217",
        ),
        "210": (
            8676,
            47454,
            8586,
            "446cdf25a92181375efb463d7ccb53b73a5772f7cdf6ec1779b7ada529a3b1cc",
        ),
    }
    assert {
        permutation: (variables, clauses, terms, digest)
        for permutation, variables, clauses, terms, digest, _ in rows
    } == expected
    for permutation, variables, clauses, terms, digest, drup_additions in rows:
        print(
            f"sigma={permutation}: UNSAT; variables={variables}; "
            f"clauses={clauses}; terms={terms}; "
            f"RUP-additions={drup_additions}; sha256={digest}"
        )


def main() -> None:
    assert len(MATCHINGS) == 105
    assert (
        sum(
            not is_live_word(word)
            for word in itertools.product(COLORS, repeat=4)
        )
        == 30
    )
    audit_live_boxes_and_bare_matching()
    audit_unique_matching_triangularization()
    audit_canonical_small_core()
    audit_full_triangular_formulas()
    print("PASS: every two-K4 cross graph with a unique perfect matching is excluded")


if __name__ == "__main__":
    main()
