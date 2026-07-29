#!/usr/bin/env python3
"""Explore rank-two Gram constraints for one-cell perturbations of sparse q.

This is a discovery script, not a promoted verifier.  It enumerates all
endpoint-ordered cells that leave z*(q+t*e)^[3] unchanged, identifies the
ones that disturb the seven-entry contradiction, and prints the exact
coefficient equations on the six distinguished modes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product


SITES = tuple(range(8))
COLOURS = tuple(range(3))
Q0 = (
    (2, 3, 0, 0),
    (4, 5, 0, 0),
    (6, 7, 0, 0),
    (0, 1, 1, 1),
    (3, 6, 1, 1),
    (5, 7, 1, 1),
    (0, 2, 2, 2),
    (1, 4, 2, 2),
    (5, 6, 2, 2),
)
Z = (
    (0, 1, 0, 0),
    (2, 4, 1, 1),
    (3, 7, 2, 2),
)

# A,B,C,D,E,F in the fixed-q note.
DIST_MODES = ((0, 0), (1, 0), (2, 1), (4, 1), (3, 2), (7, 2))
SELECTED_WORDS = (
    (0,) * 8,
    (1,) * 8,
    (2,) * 8,
    (0, 2, 0, 0, 2, 2, 2, 2),
    (2, 0, 2, 1, 0, 0, 1, 2),
    (0, 2, 1, 1, 2, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 1, 2),
)


def disjoint(cells):
    endpoints = [x for u, v, _, _ in cells for x in (u, v)]
    return len(endpoints) == len(set(endpoints))


def word_of(cells):
    word = [None] * 8
    for u, v, cu, cv in cells:
        word[u], word[v] = cu, cv
    assert all(x is not None for x in word)
    return tuple(word)


def power_terms(cells, degree):
    """Return (word/partial-colouring, contains-extra) terms.

    The final cell in ``cells`` is regarded as the extra cell.
    """
    result = []
    for chosen in combinations(range(len(cells)), degree):
        selected = tuple(cells[i] for i in chosen)
        if not disjoint(selected):
            continue
        fixed = {}
        for u, v, cu, cv in selected:
            fixed[u], fixed[v] = cu, cv
        result.append((fixed, len(cells) - 1 in chosen))
    return result


def z_times_extra_q2(extra):
    out = Counter()
    for zcell in Z:
        for pair in combinations(Q0, 2):
            cells = (zcell, extra) + pair
            if disjoint(cells):
                out[word_of(cells)] += 1
    return out


def f_map(extra):
    """word -> list (Gram mode pair, coefficient exponent in t)."""
    out = defaultdict(list)
    cells = Q0 + (extra,)
    for fixed, has_extra in power_terms(cells, 3):
        u, v = sorted(set(SITES) - set(fixed))
        for cu, cv in product(COLOURS, repeat=2):
            word = tuple(cu if x == u else cv if x == v else fixed[x]
                         for x in SITES)
            out[word].append((((u, cu), (v, cv)), int(has_extra)))
    return out


def q4_map(extra):
    out = defaultdict(Counter)
    cells = Q0 + (extra,)
    for fixed, has_extra in power_terms(cells, 4):
        word = tuple(fixed[x] for x in SITES)
        out[word][int(has_extra)] += 1
    return out


def fmt_mode(mode):
    return f"{mode[0]}:{mode[1]}"


def fmt_equation(contributors, qcoeff, target):
    terms = []
    for (x, y), exp in contributors:
        terms.append(("t*" if exp else "") + f"R[{fmt_mode(x)},{fmt_mode(y)}]")
    for exp, coeff in sorted(qcoeff.items()):
        prefix = "a*t" if exp else "a"
        terms.append(prefix if coeff == 1 else f"{coeff}*{prefix}")
    return " + ".join(terms) + f" = {target}/4"


def orthogonality_closes(nonzero_pairs, zero_edges):
    """Return whether known nonzero vectors force a 2D Gram contradiction."""
    vertices = set(x for pair in nonzero_pairs for x in pair)
    parent = {x: x for x in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x, y = find(x), find(y)
        if x != y:
            parent[y] = x
            return True
        return False

    relevant_zeros = {(x, y) for x, y in zero_edges if x in vertices and y in vertices}
    while True:
        changed = False
        classes = defaultdict(set)
        for x in vertices:
            classes[find(x)].add(x)
        # Every pair of nonzero vectors orthogonal to the same nonzero
        # vector is proportional.
        for centre in tuple(classes):
            neighbours = set()
            for x, y in relevant_zeros:
                if find(x) == centre:
                    neighbours.add(find(y))
                if find(y) == centre:
                    neighbours.add(find(x))
            neighbours = list(neighbours)
            for other in neighbours[1:]:
                changed |= union(neighbours[0], other)
        # An isotropic class equals its own orthogonal complement.
        classes = defaultdict(set)
        for x in vertices:
            classes[find(x)].add(x)
        for centre in tuple(classes):
            isotropic = any(find(x) == centre and find(y) == centre
                            for x, y in relevant_zeros)
            if not isotropic:
                continue
            for x, y in relevant_zeros:
                if find(x) == centre:
                    changed |= union(x, y)
                elif find(y) == centre:
                    changed |= union(y, x)
        if not changed:
            break

    for x, y in nonzero_pairs:
        if any({x, y} == {u, v} for u, v in relevant_zeros):
            return True
        if find(x) == find(y):
            if any(find(u) == find(x) and find(v) == find(x)
                   for u, v in relevant_zeros):
                return True
    return False


def singleton_zero_edges(fmap, qmap):
    edges = set()
    for word, contributors in fmap.items():
        if len(set(word)) == 1 or qmap[word] or len(contributors) != 1:
            continue
        edges.add(tuple(contributors[0][0]))
    return edges


def main():
    base = set(Q0)
    all_cells = tuple(
        (u, v, cu, cv)
        for u in SITES for v in SITES if u < v
        for cu in COLOURS for cv in COLOURS
        if (u, v, cu, cv) not in base
    )
    invisible = tuple(e for e in all_cells if not z_times_extra_q2(e))
    assert len(all_cells) == 243
    assert len(invisible) == 99

    changed = []
    for extra in invisible:
        fmap = f_map(extra)
        qmap = q4_map(extra)
        signature = tuple(
            i for i, word in enumerate(SELECTED_WORDS)
            if len(fmap[word]) != 1 or qmap[word]
        )
        if signature:
            changed.append((extra, signature, fmap, qmap))
    assert len(changed) == 33
    mono = [item for item in changed if item[0][2] == item[0][3]]
    assert len(mono) == 18

    print("all cells / invisible / changed / changed monochromatic:",
          len(all_cells), len(invisible), len(changed), len(mono))
    print("\nmonochromatic branch-closure summary")
    for extra, signature, fmap, qmap in mono:
        altered_pures = [i for i in signature if i < 3]
        assert len(altered_pures) == 1
        altered = altered_pures[0]
        base_pairs = [fmap[SELECTED_WORDS[i]][0][0]
                      for i in range(3) if i != altered]
        branches = []
        for contributor, _ in fmap[SELECTED_WORDS[altered]]:
            branches.append(orthogonality_closes(
                base_pairs + [contributor], singleton_zero_edges(fmap, qmap)))
        print(extra, signature, "pure contributors",
              len(fmap[SELECTED_WORDS[altered]]), "branches", branches,
              "singleton zeros", len(singleton_zero_edges(fmap, qmap)))
    print("\nasymmetric closure summary")
    for extra, signature, fmap, qmap in changed:
        if extra[2] == extra[3]:
            continue
        pure_pairs = [fmap[SELECTED_WORDS[i]][0][0] for i in range(3)]
        closes = orthogonality_closes(
            pure_pairs, singleton_zero_edges(fmap, qmap))
        print(extra, signature, "closes", closes,
              "singleton zeros", len(singleton_zero_edges(fmap, qmap)))
    for extra, signature, fmap, qmap in changed:
        kind = "mono" if extra[2] == extra[3] else "asym"
        print("\n", extra, kind, "changed", signature)
        # Print all equations whose contributors lie wholly on distinguished
        # modes, together with the original seven even when altered.
        printed = set()
        for word in SELECTED_WORDS:
            target = int(len(set(word)) == 1)
            print(" selected", word, fmt_equation(fmap[word], qmap[word], target))
            printed.add(word)
        useful = []
        for word, contributors in fmap.items():
            if word in printed:
                continue
            if all(x in DIST_MODES and y in DIST_MODES for x, y in contributors):
                target = int(len(set(word)) == 1)
                useful.append((word, contributors, qmap[word], target))
        print(" distinguished-only extra equations:", len(useful))
        for word, contributors, qcoeff, target in useful:
            print("  ", word, fmt_equation(contributors, qcoeff, target))


if __name__ == "__main__":
    main()
