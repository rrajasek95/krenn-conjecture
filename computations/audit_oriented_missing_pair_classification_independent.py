#!/usr/bin/env python3
"""Independent exhaustive audit of the ordered missing-pair lemma.

This is intentionally standalone.  It enumerates every labelled triple of
directed nonloop pairs on six labelled sites, including repeated underlying
pairs and triples which leave sites unused.  It tests the nine coordinate-
monomial products directly at the level of their surviving pure words, then
checks that every surviving triple has exactly one of the two claimed support
types.
"""

from collections import Counter
from itertools import product


VERTICES = tuple(range(6))
DIRECTED_EDGES = tuple((u, v) for u in VERTICES for v in VERTICES if u != v)


def underlying(edge):
    return frozenset(edge)


def surviving_f_terms(edges, i, j):
    """Indices k for which p_i s_j F_k is a nonzero pure tensor.

    If u_i=v_j, the two one-site factors multiply to zero in the local
    square-zero algebra.  Otherwise F_k survives precisely when its two
    missing sites are {u_i,v_j}.
    """

    ui = edges[i][0]
    vj = edges[j][1]
    if ui == vj:
        return ()
    cross_pair = frozenset((ui, vj))
    return tuple(k for k, edge in enumerate(edges) if underlying(edge) == cross_pair)


def has_nine_product_table(edges):
    # Surviving terms with different k have different complement colours,
    # hence are linearly independent pure coordinate words.  Thus the exact
    # diagonal/cross product table is equivalent to these survivor lists.
    for i in range(3):
        for j in range(3):
            expected = (i,) if i == j else ()
            if surviving_f_terms(edges, i, j) != expected:
                return False
    return True


def support_type(edges):
    pairs = tuple(underlying(edge) for edge in edges)
    degrees = Counter(vertex for pair in pairs for vertex in pair)
    used = frozenset(degrees)

    if len(used) == 6 and sorted(degrees.values()) == [1] * 6:
        return "three_disjoint_pairs"

    if len(used) == 5 and sorted(degrees.values()) == [1, 1, 1, 1, 2]:
        meeting = [i for i in range(3) if any(pairs[i] & pairs[j] for j in range(3) if j != i)]
        isolated = [i for i in range(3) if i not in meeting]
        if len(meeting) != 2 or len(isolated) != 1:
            return "bad_five_vertex_shape"
        i, j = meeting
        common = next(iter(pairs[i] & pairs[j]))
        # The two incident edges must have opposite orientations at the
        # common vertex, i.e. form a directed path.
        i_points_out = edges[i][0] == common
        j_points_out = edges[j][0] == common
        if i_points_out == j_points_out:
            return "bad_meeting_orientation"
        return "directed_path_plus_disjoint_pair"

    return "unclaimed_shape"


def main():
    total = 0
    passing = []
    rejected_repeated = 0
    for edges in product(DIRECTED_EDGES, repeat=3):
        total += 1
        if len({underlying(edge) for edge in edges}) < 3:
            rejected_repeated += 1
        if has_nine_product_table(edges):
            passing.append(edges)

    counts = Counter(support_type(edges) for edges in passing)
    assert total == 30**3 == 27_000
    assert rejected_repeated > 0
    assert counts == {
        "three_disjoint_pairs": 720,
        "directed_path_plus_disjoint_pair": 4_320,
    }, counts

    # Independently check the compact condition used in the written proof,
    # after rather than before the literal product-table test.
    for edges in product(DIRECTED_EDGES, repeat=3):
        distinct = len({underlying(edge) for edge in edges}) == 3
        cross_condition = all(
            edges[i][0] == edges[j][1]
            or frozenset((edges[i][0], edges[j][1]))
            not in {underlying(edge) for edge in edges}
            for i in range(3)
            for j in range(3)
            if i != j
        )
        assert has_nine_product_table(edges) == (distinct and cross_condition)

    # A directed path uses three sites and its disjoint edge two more, so the
    # second type always leaves exactly one of the six sites unused.
    for edges in passing:
        if support_type(edges) == "directed_path_plus_disjoint_pair":
            assert len(set().union(*(set(edge) for edge in edges))) == 5

    print("oriented missing-pair classification independent audit: PASS")
    print(f"labelled directed triples checked: {total}")
    print(f"triples satisfying all nine products: {len(passing)}")
    print(f"three disjoint pairs: {counts['three_disjoint_pairs']}")
    print(
        "directed two-edge path plus disjoint pair: "
        f"{counts['directed_path_plus_disjoint_pair']}"
    )


if __name__ == "__main__":
    main()
