"""Exact finite audit for the diagonal-edge n=6, q=3 obstruction.

Suppose the three color layers have supports P_i.  The hafnian cofactor
identities force pairwise-exclusive edge covers R_i contained in P_i, and
every edge of R_i must extend to a P_i-perfect matching.  A coloring with
two vertices of each color forbids a rainbow perfect matching in the P_i.

After shrinking each R_i to an inclusion-minimal edge cover, this script
does two exhaustive, exact checks:

1. Up to relabeling the six vertices and permuting the colors, there are
   exactly ten triples of pairwise-disjoint minimal edge covers with no
   rainbow perfect matching.
2. None of those ten triples extends to supports P_i satisfying all the
   conditions above.

The second check is propositional SAT only; no floating-point calculation
or assumption about signs of the complex weights is involved.
"""

from __future__ import annotations

import itertools

from pysat.solvers import Solver


VERTICES = tuple(range(6))
EDGES = tuple(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ALL_VERTICES = (1 << len(VERTICES)) - 1


def edge_mask(edges: tuple[tuple[int, int], ...] | list[tuple[int, int]]) -> int:
    return sum(1 << EDGE_INDEX[tuple(sorted(edge))] for edge in edges)


def mask_edges(mask: int) -> tuple[tuple[int, int], ...]:
    return tuple(edge for index, edge in enumerate(EDGES) if mask & (1 << index))


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        v = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((min(u, v), max(u, v)),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(VERTICES)
MATCHING_MASKS = tuple(edge_mask(list(matching)) for matching in MATCHINGS)


def is_edge_cover(mask: int) -> bool:
    covered = 0
    for index, (u, v) in enumerate(EDGES):
        if mask & (1 << index):
            covered |= (1 << u) | (1 << v)
    return covered == ALL_VERTICES


def is_minimal_edge_cover(mask: int) -> bool:
    if not is_edge_cover(mask):
        return False
    return all(not is_edge_cover(mask ^ (1 << index)) for index in range(15) if mask & (1 << index))


MINIMAL_COVERS = tuple(mask for mask in range(1 << 15) if is_minimal_edge_cover(mask))


def has_rainbow_matching(covers: tuple[int, int, int]) -> bool:
    for matching in MATCHINGS:
        for color_order in itertools.permutations(range(3)):
            if all(covers[color] & (1 << EDGE_INDEX[edge]) for color, edge in zip(color_order, matching, strict=True)):
                return True
    return False


def permuted_mask(mask: int, vertex_permutation: tuple[int, ...]) -> int:
    image = 0
    for index, (u, v) in enumerate(EDGES):
        if mask & (1 << index):
            edge = tuple(sorted((vertex_permutation[u], vertex_permutation[v])))
            image |= 1 << EDGE_INDEX[edge]
    return image


VERTEX_PERMUTATIONS = tuple(itertools.permutations(VERTICES))


def canonical_triple(covers: tuple[int, int, int]) -> tuple[int, int, int]:
    """Canonicalize under S_6 on vertices and S_3 on colors."""
    return min(
        tuple(sorted(permuted_mask(mask, permutation) for mask in covers))
        for permutation in VERTEX_PERMUTATIONS
    )


def classify_cover_triples() -> dict[tuple[int, int, int], tuple[int, int, int]]:
    representatives: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for covers in itertools.combinations(MINIMAL_COVERS, 3):
        if covers[0] & covers[1] or covers[0] & covers[2] or covers[1] & covers[2]:
            continue
        if has_rainbow_matching(covers):
            continue
        representatives.setdefault(canonical_triple(covers), covers)
    return representatives


def support_variable(color: int, edge: tuple[int, int]) -> int:
    return 1 + 15 * color + EDGE_INDEX[edge]


def supports_exist(covers: tuple[int, int, int]) -> bool:
    """SAT check for compatible supersets P_i of the three R_i."""
    clauses: list[list[int]] = []

    # R_i is present in P_i and absent from the other two color supports.
    for color, cover in enumerate(covers):
        for edge in mask_edges(cover):
            clauses.append([support_variable(color, edge)])
            for other_color in range(3):
                if other_color != color:
                    clauses.append([-support_variable(other_color, edge)])

    # No P-rainbow perfect matching.
    for matching in MATCHINGS:
        for color_order in itertools.permutations(range(3)):
            clauses.append(
                [
                    -support_variable(color, edge)
                    for color, edge in zip(color_order, matching, strict=True)
                ]
            )

    # Each edge of R_i extends to a P_i-perfect matching.  For a fixed edge
    # on K6, the four remaining vertices have exactly three pairings.  The
    # auxiliary variable selects one supported pairing.
    next_variable = 46
    for color, cover in enumerate(covers):
        for edge in mask_edges(cover):
            remaining = tuple(vertex for vertex in VERTICES if vertex not in edge)
            choices = perfect_matchings(remaining)
            selectors = []
            for pairing in choices:
                selector = next_variable
                next_variable += 1
                selectors.append(selector)
                for complement_edge in pairing:
                    clauses.append([-selector, support_variable(color, complement_edge)])
            clauses.append(selectors)

    with Solver(name="g4", bootstrap_with=clauses) as solver:
        return solver.solve()


def format_cover(mask: int) -> str:
    return "{" + ",".join(f"{u}{v}" for u, v in mask_edges(mask)) + "}"


def main() -> None:
    representatives = classify_cover_triples()
    assert len(MINIMAL_COVERS) == 171
    assert len(representatives) == 10

    print(f"minimal edge covers: {len(MINIMAL_COVERS)}")
    print(f"S6 x S3 orbits of admissible cover triples: {len(representatives)}")
    for orbit, covers in enumerate(sorted(representatives.values()), start=1):
        result = supports_exist(covers)
        rendered = " ".join(format_cover(mask) for mask in covers)
        print(f"orbit {orbit:2d}: {rendered}: {'SAT' if result else 'UNSAT'}")
        assert not result
    print("VERIFIED: no diagonal n=6, q=3 realization exists")


if __name__ == "__main__":
    main()
