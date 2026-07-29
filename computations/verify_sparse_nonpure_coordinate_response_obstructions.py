#!/usr/bin/env python3
"""Exact audits for two sparse non-pure six-site response obstructions.

The first audit exhausts physical support graphs with no perfect matching.
The second builds a necessary support CNF for a quadratic containing
arbitrary same-colour coordinate cells and arbitrary complex weights.  A
small deterministic DPLL implementation proves all 17 directed-row orbits
unsatisfiable.  PySAT/CaDiCaL, when installed, independently replays the
same CNFs.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
DIRECTED_EDGES = tuple((u, v) for u in U for v in U if u != v)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    output = []
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            output.append((edge(u, v),) + matching)
    return tuple(output)


PM6 = perfect_matchings(U)
PM4 = {
    pair: perfect_matchings(tuple(u for u in U if u not in pair))
    for pair in EDGES
}


# Canonical directed-row triples, modulo site permutations, target-colour
# permutations, and simultaneous reversal of every row (p <-> s).
ROW_ORBITS = (
    ((0, 1), (0, 1), (0, 1)),
    ((0, 1), (0, 1), (0, 2)),
    ((0, 1), (0, 1), (1, 0)),
    ((0, 1), (0, 1), (1, 2)),
    ((0, 1), (0, 1), (2, 3)),
    ((0, 1), (0, 2), (0, 3)),
    ((0, 1), (0, 2), (1, 0)),
    ((0, 1), (0, 2), (1, 2)),
    ((0, 1), (0, 2), (1, 3)),
    ((0, 1), (0, 2), (3, 0)),
    ((0, 1), (0, 2), (3, 1)),
    ((0, 1), (0, 2), (3, 4)),
    ((0, 1), (1, 0), (2, 3)),
    ((0, 1), (1, 2), (2, 0)),
    ((0, 1), (1, 2), (2, 3)),
    ((0, 1), (1, 2), (3, 4)),
    ((0, 1), (2, 3), (4, 5)),
)

ROW_ORBIT_SIZES = (
    30, 720, 90, 720, 1080, 720, 1440, 720, 4320,
    2160, 2160, 4320, 1080, 240, 2160, 4320, 720,
)


def canonical_rows(rows: tuple[tuple[int, int], ...]):
    best = None
    for colour_permutation in permutations(COLOURS):
        permuted = tuple(rows[i] for i in colour_permutation)
        for reverse in (False, True):
            directed = tuple(
                (v, u) if reverse else (u, v)
                for u, v in permuted
            )
            relabel = {}
            code = []
            for u, v in directed:
                for site in (u, v):
                    if site not in relabel:
                        relabel[site] = len(relabel)
                code.append((relabel[u], relabel[v]))
            candidate = tuple(code)
            if best is None or candidate < best:
                best = candidate
    assert best is not None
    return best


def audit_row_orbits():
    counts = Counter(
        canonical_rows(rows)
        for rows in product(DIRECTED_EDGES, repeat=3)
    )
    assert tuple(sorted(counts)) == ROW_ORBITS
    assert tuple(counts[rows] for rows in ROW_ORBITS) == ROW_ORBIT_SIZES
    assert sum(ROW_ORBIT_SIZES) == 30**3 == 27_000


def matching_mask(matching) -> int:
    return sum(1 << EDGE_INDEX[e] for e in matching)


PM6_MASKS = tuple(matching_mask(matching) for matching in PM6)
PM4_MASKS = {
    pair: tuple(matching_mask(matching) for matching in matchings)
    for pair, matchings in PM4.items()
}


def has_mask(graph_mask: int, matching_mask_value: int) -> bool:
    return graph_mask & matching_mask_value == matching_mask_value


def audit_termwise_no_perfect_matching_boundary():
    """Exhaust the collision-free physical-support boundary.

    A diagonal one-site response on row pair (a_i,b_i) needs a two-edge
    matching after deleting those sites.  Every off-diagonal product with
    distinct row sites needs no such matching when four-site coefficients
    are collision-free.  No perfect-matching-free six-vertex graph has
    three directed row pairs with those properties.
    """

    graph_count = 0
    diagonal_survivors = [0] * len(ROW_ORBITS)
    complete_survivors = [0] * len(ROW_ORBITS)
    for graph_mask in range(1 << len(EDGES)):
        if any(has_mask(graph_mask, matching) for matching in PM6_MASKS):
            continue
        graph_count += 1
        cofactor = {
            pair: any(has_mask(graph_mask, matching) for matching in matchings)
            for pair, matchings in PM4_MASKS.items()
        }
        for orbit, rows in enumerate(ROW_ORBITS):
            if not all(cofactor[edge(u, v)] for u, v in rows):
                continue
            diagonal_survivors[orbit] += 1
            valid = all(
                i == j
                or rows[i][0] == rows[j][1]
                or not cofactor[edge(rows[i][0], rows[j][1])]
                for i in COLOURS
                for j in COLOURS
            )
            if valid:
                complete_survivors[orbit] += 1

    assert graph_count == 7_945
    assert diagonal_survivors == [
        2081, 821, 2081, 821, 166, 453, 821, 309, 130,
        453, 130, 18, 166, 309, 130, 18, 4,
    ]
    assert sum(diagonal_survivors) == 8_911
    assert complete_survivors == [0] * len(ROW_ORBITS)
    return graph_count, sum(diagonal_survivors)


def support_variable(colour: int, physical_edge: tuple[int, int]) -> int:
    """Variables 1,...,45 record nonzero same-colour q cells."""
    return 1 + 15 * colour + EDGE_INDEX[physical_edge]


def canonical_clause(clause):
    # All generated clauses are non-tautological.  Sorting and deduplication
    # make the ledger independent of incidental construction order.
    literals = tuple(sorted(set(clause)))
    assert all(-literal not in literals for literal in literals)
    return literals


def build_support_cnf(rows, include_zero_hafnian_rules=True):
    """Build a necessary support CNF for the same-colour q ansatz.

    Auxiliary z_(c,P,M) is equivalent to saying that both q cells of the
    two-matching M on U-P are active.  A required nonzero pure coefficient
    needs at least one z.  A required zero pure coefficient cannot have
    exactly one z.  A mixed 2+2 word has one possible matching, so its two
    differently coloured cells may not both be active.
    """

    clauses = []
    variable_count = 45
    matching_active = {}

    for colour in COLOURS:
        for pair in EDGES:
            auxiliaries = []
            for matching in PM4[pair]:
                variable_count += 1
                z = variable_count
                auxiliaries.append(z)
                cells = tuple(support_variable(colour, e) for e in matching)
                # z iff the two cells in this matching are active.
                for cell in cells:
                    clauses.append((-z, cell))
                clauses.append((z,) + tuple(-cell for cell in cells))
            matching_active[colour, pair] = tuple(auxiliaries)

    assert variable_count == 180

    def zero_hafnian(pair, colour):
        if not include_zero_hafnian_rules:
            return
        auxiliaries = matching_active[colour, pair]
        # If one matching is supported, a second must be available to
        # cancel it.  This is only a necessary condition and deliberately
        # grants every possible complex cancellation among 2 or 3 terms.
        for index, z in enumerate(auxiliaries):
            others = auxiliaries[:index] + auxiliaries[index + 1 :]
            clauses.append((-z,) + others)

    def constrain_sampled_block(pair, target_colour=None):
        if target_colour is not None:
            clauses.append(matching_active[target_colour, pair])
        for colour in COLOURS:
            if colour != target_colour:
                zero_hafnian(pair, colour)

        # A word with two c's and two d's has the unique matching consisting
        # of its c-pair and d-pair.  No cancellation is possible.
        for first_edge, second_edge in PM4[pair]:
            for first_colour, second_colour in permutations(COLOURS, 2):
                clauses.append((
                    -support_variable(first_colour, first_edge),
                    -support_variable(second_colour, second_edge),
                ))
                clauses.append((
                    -support_variable(first_colour, second_edge),
                    -support_variable(second_colour, first_edge),
                ))

    for i, (a, b) in enumerate(rows):
        constrain_sampled_block(edge(a, b), target_colour=i)
        for j in COLOURS:
            if i == j:
                continue
            p_site = rows[i][0]
            s_site = rows[j][1]
            if p_site == s_site:
                continue  # the product is zero in one local square-zero factor
            constrain_sampled_block(edge(p_site, s_site))

    canonical = tuple(sorted({canonical_clause(clause) for clause in clauses}))
    return canonical, variable_count


def simplify(clauses, assignment):
    residual = []
    units = []
    for clause in clauses:
        undecided = []
        satisfied = False
        for literal in clause:
            variable = abs(literal)
            if variable in assignment:
                if assignment[variable] == (literal > 0):
                    satisfied = True
                    break
            else:
                undecided.append(literal)
        if satisfied:
            continue
        if not undecided:
            return None, None
        residual_clause = tuple(undecided)
        residual.append(residual_clause)
        if len(residual_clause) == 1:
            units.append(residual_clause[0])
    return tuple(residual), tuple(units)


def dpll(clauses):
    """Return (satisfiable, visited_nodes) by deterministic exact DPLL."""

    visited = 0

    def recurse(current, assignment):
        nonlocal visited
        visited += 1
        assignment = dict(assignment)

        while True:
            current, units = simplify(current, assignment)
            if current is None:
                return False
            assert units is not None
            if not units:
                break
            for literal in units:
                variable = abs(literal)
                value = literal > 0
                if variable in assignment and assignment[variable] != value:
                    return False
                assignment[variable] = value

        if not current:
            return True

        # Pure-literal elimination preserves satisfiability.
        polarities = {}
        for clause in current:
            for literal in clause:
                polarities.setdefault(abs(literal), set()).add(literal > 0)
        pure = tuple(
            (variable, next(iter(values)))
            for variable, values in polarities.items()
            if len(values) == 1
        )
        if pure:
            assignment.update(pure)
            return recurse(current, assignment)

        shortest = min(current, key=len)
        frequencies = Counter(abs(literal) for clause in current for literal in clause)
        variable = max((abs(literal) for literal in shortest), key=frequencies.get)
        for value in (False, True):
            branch = dict(assignment)
            branch[variable] = value
            if recurse(current, branch):
                return True
        return False

    return recurse(tuple(clauses), {}), visited


def cnf_digest(clauses):
    payload = "".join(
        " ".join(str(literal) for literal in clause) + " 0\n"
        for clause in clauses
    )
    return sha256(payload.encode("ascii")).hexdigest()


def audit_same_colour_common_square_boundary():
    clause_counts = []
    node_counts = []
    digests = []
    try:
        from pysat.solvers import Solver
    except ImportError:  # The in-repository DPLL remains the primary audit.
        Solver = None

    for rows in ROW_ORBITS:
        clauses, variables = build_support_cnf(rows)
        assert variables == 180
        satisfiable, nodes = dpll(clauses)
        assert not satisfiable
        if Solver is not None:
            with Solver(name="cadical195", bootstrap_with=clauses) as solver:
                assert not solver.solve()
        clause_counts.append(len(clauses))
        node_counts.append(nodes)
        digests.append(cnf_digest(clauses))

    assert clause_counts == [
        435, 462, 435, 486, 513, 489, 489, 489, 540,
        540, 516, 567, 567, 489, 564, 615, 642,
    ]
    assert node_counts == [
        3566, 1050, 3566, 1258, 731, 470, 446, 292, 232,
        219, 183, 64, 181, 365, 175, 7, 24,
    ]

    # A positive control: dropping all zero-hafnian support rules admits a
    # support assignment in the first orbit.  The UNSAT result is therefore
    # not an artefact of the target clauses alone or of the DPLL routine.
    relaxed, _variables = build_support_cnf(
        ROW_ORBITS[0], include_zero_hafnian_rules=False
    )
    relaxed_satisfiable, _nodes = dpll(relaxed)
    assert relaxed_satisfiable

    ledger = sha256("\n".join(digests).encode("ascii")).hexdigest()
    assert ledger == "b71aa65a4a08354100e302acea5914de0e12808f8ca80a2539a1dccf52976afc"
    return clause_counts, node_counts, ledger


def main():
    audit_row_orbits()
    graphs, diagonal_cases = audit_termwise_no_perfect_matching_boundary()
    clauses, nodes, ledger = audit_same_colour_common_square_boundary()
    print("directed one-site row orbits: 17 / 27000")
    print(
        "termwise PM-free graphs:", graphs,
        "diagonal graph/orbit cases:", diagonal_cases,
        "complete cases: 0",
    )
    print("same-colour support CNF clause counts:", clauses)
    print("deterministic DPLL node counts:", nodes)
    print("CNF ledger SHA-256:", ledger)
    print("sparse non-pure coordinate response obstructions: PASS")


if __name__ == "__main__":
    main()
