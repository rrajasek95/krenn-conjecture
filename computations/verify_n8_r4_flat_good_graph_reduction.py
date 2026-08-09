#!/usr/bin/env python3
"""Exact graph/essential reduction of the N=8 all-flat r=4 frontier."""

from __future__ import annotations


N = 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def component_decompositions():
    types = sorted(
        [("P", size) for size in range(1, N + 1)]
        + [("C", size) for size in range(3, N + 1)]
    )
    rows = []

    def visit(start, left, chosen):
        if not left:
            rows.append(tuple(chosen))
            return
        for index in range(start, len(types)):
            if types[index][1] <= left:
                visit(index, left - types[index][1],
                      chosen + [types[index]])

    visit(0, N, [])
    return rows


def component_data(component):
    kind, size = component
    edges = size - 1 if kind == "P" else size
    isolates = int(kind == "P" and size == 1)
    if kind == "C" and size == 3:
        return edges, None, None, isolates
    if kind == "P":
        chords = max(size - 2, 0)
        covered = 0 if size <= 2 else 2 if size == 3 else size
    else:
        chords = 2 if size == 4 else size
        covered = size
    return edges, chords, covered, isolates


def minimum_complement_edges_for_cubic_sites(count):
    """Minimum edges giving `count` vertices complement degree at least 4."""

    if count <= 5:
        return count * (count - 1) // 2 + count * (5 - count)
    return 2 * count


def audit():
    minimum_edges = tuple(
        minimum_complement_edges_for_cubic_sites(count)
        for count in range(N + 1)
    )
    require(minimum_edges == (0, 4, 7, 9, 10, 10, 12, 14, 16),
            "the complement-degree extremal table changed")
    complement_budget = 8  # 28 physical pairs minus 20 selected pairs.
    max_cubic = max(count for count, edges in enumerate(minimum_edges)
                    if edges <= complement_budget)
    require(max_cubic == 2,
            "eight complement edges ceased to bound cubic sites by two")

    raw = []
    survivors = []
    for decomposition in component_decompositions():
        data = [component_data(component) for component in decomposition]
        if any(chords is None for _edges, chords, _covered, _isolates in data):
            continue
        good_edges = sum(edges for edges, _chords, _covered, _isolates in data)
        chords = sum(value for _edges, value, _covered, _isolates in data)
        covered = sum(value for _edges, _chords, value, _isolates in data)
        isolates = sum(value for _edges, _chords, _covered, value in data)
        if good_edges > N or chords > complement_budget:
            continue

        selected_bad = 20 - good_edges
        # A flat-wedge chord has rank >=2.  At each endpoint it is essential,
        # so at most one selected bad incidence remains.  Every other
        # noncubic site contributes at most two.  Cubic sites must be isolated
        # in the good graph, and the complement-degree bound permits at most
        # two of them.
        selected_essential_cap = (
            covered + 2 * (N - covered) + min(isolates, max_cubic)
        )
        row = (tuple(sorted(decomposition)), good_edges, chords, covered,
               isolates, selected_bad, selected_essential_cap)
        raw.append(row)
        if selected_bad <= selected_essential_cap:
            survivors.append(row)

    expected = {
        ((('P', 1), ('P', 1), ('P', 1), ('P', 1),
          ('P', 2), ('P', 2)), 2, 0, 0, 4, 18, 18),
        ((('P', 1), ('P', 1), ('P', 2), ('P', 2), ('P', 2)),
         3, 0, 0, 2, 17, 18),
        ((('P', 2), ('P', 2), ('P', 2), ('P', 2)),
         4, 0, 0, 0, 16, 16),
    }
    require(set(survivors) == expected,
            f"the refined r=4 survivor census changed: {survivors}")

    named_guards = {
        "C4+2K2": ((('C', 4), ('P', 2), ('P', 2)), 14, 12),
        "P3+2K2+K1": (
            (('P', 1), ('P', 2), ('P', 2), ('P', 3)), 16, 15
        ),
    }
    for name, (shape, bad, cap) in named_guards.items():
        row = next(value for value in raw if value[0] == shape)
        require((row[5], row[6]) == (bad, cap) and bad > cap,
                f"{name} stopped violating its essential cap")

    return minimum_edges, tuple(survivors), named_guards


def main():
    minimum_edges, survivors, named_guards = audit()
    print("N=8 all-flat r=4 good-graph reduction: PASS")
    print("complement cubic-site edge table:", minimum_edges)
    print("eliminated high-edge shapes:",
          {name: values[1:] for name, values in named_guards.items()})
    print("survivors:")
    for row in survivors:
        print(" ", row)


if __name__ == "__main__":
    main()
