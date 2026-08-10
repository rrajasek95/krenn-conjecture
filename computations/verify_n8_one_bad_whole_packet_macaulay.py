#!/usr/bin/env python3
"""Bounded whole-packet Macaulay test for the two sharp one-bad orbits.

The four normalized star rows turn the response packet into four four-site
hafnian equations.  This checker leaves all 135 cells of q unrestricted and
constructs only the fine-multidegree connected component containing 1 in the
degree-D Macaulay matrix.  Thus it is a whole-ideal calculation, not a support
enumeration.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from itertools import combinations, product

from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix


SITES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
VARIABLE_DATA = tuple((u, v, a, b) for u, v in EDGES for a in COLORS for b in COLORS)


def variable(u: int, v: int, a: int, b: int) -> int:
    if u > v:
        u, v, a, b = v, u, b, a
    return 9 * EDGE_INDEX[u, v] + 3 * a + b


def matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    return tuple(
        ((u, vertices[j]),) + rest
        for j in range(1, len(vertices))
        for rest in matchings(vertices[1:j] + vertices[j + 1 :])
    )


MATCHINGS4 = {u: matchings(u) for u in combinations(SITES, 4)}
MATCHINGS6 = matchings(SITES)
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def packet_generators(orbit: int) -> list[Polynomial]:
    """Return 324 response and 729 top scalar coefficient equations."""
    require(orbit in (0, 1), orbit)
    c_holes = (2, 4) if orbit == 0 else (4, 2)
    specs = (
        ((0, 1, 2, 4), 0),
        ((0, 1, 3, 5), 1),
        (tuple(sorted(set(SITES) - {3, c_holes[1]})), None),
        (tuple(sorted(set(SITES) - {c_holes[0], 5})), None),
    )
    out: list[Polynomial] = []
    for sites, target in specs:
        for word in product(COLORS, repeat=4):
            color = dict(zip(sites, word, strict=True))
            row: defaultdict[Monomial, int] = defaultdict(int)
            for matching in MATCHINGS4[sites]:
                monomial = tuple(
                    sorted(variable(u, v, color[u], color[v]) for u, v in matching)
                )
                row[monomial] += 1
            if target is not None and all(c == target for c in word):
                row[()] -= 1
            out.append(dict(row))
    for word in product(COLORS, repeat=6):
        row = defaultdict(int)
        for matching in MATCHINGS6:
            monomial = tuple(
                sorted(variable(u, v, word[u], word[v]) for u, v in matching)
            )
            row[monomial] += 1
        if all(c == 2 for c in word):
            row[()] -= 1
        out.append(dict(row))
    require(len(out) == 1053, len(out))
    return out


def quotient_if_divides(term: Monomial, monomial: Monomial) -> Monomial | None:
    i = 0
    quotient = []
    for x in monomial:
        if i < len(term) and term[i] == x:
            i += 1
        else:
            quotient.append(x)
    return tuple(quotient) if i == len(term) else None


def divisors(monomial: Monomial) -> set[Monomial]:
    return {
        tuple(monomial[i] for i in range(len(monomial)) if mask & (1 << i))
        for mask in range(1 << len(monomial))
    }


def constant_component(orbit: int, degree: int):
    generators = packet_generators(orbit)
    generator_degree = [max(map(len, g)) for g in generators]
    term_index: defaultdict[Monomial, list[int]] = defaultdict(list)
    for gi, generator in enumerate(generators):
        for term in generator:
            term_index[term].append(gi)

    columns: set[Monomial] = {()}
    queue = deque([()])
    rows: dict[tuple[int, Monomial], Polynomial] = {}
    while queue:
        column = queue.popleft()
        for term in divisors(column):
            multiplier = quotient_if_divides(term, column)
            require(multiplier is not None, (term, column))
            for gi in term_index.get(term, ()):
                if len(multiplier) > degree - generator_degree[gi]:
                    continue
                key = (gi, multiplier)
                if key in rows:
                    continue
                row = {
                    tuple(sorted(monomial + multiplier)): coefficient
                    for monomial, coefficient in generators[gi].items()
                }
                rows[key] = row
                for monomial in row:
                    if monomial not in columns:
                        columns.add(monomial)
                        queue.append(monomial)
    return columns, rows


def modular_row_space(rows: list[Polynomial], prime: int):
    """Sparse echelon basis, leading first by degree then lexicographically."""
    basis: dict[Monomial, Polynomial] = {}
    for source in rows:
        row = {m: a % prime for m, a in source.items() if a % prime}
        while row:
            pivot = max(row, key=lambda m: (len(m), m))
            old = basis.get(pivot)
            if old is None:
                inv = pow(row[pivot], -1, prime)
                basis[pivot] = {m: (a * inv) % prime for m, a in row.items()}
                break
            scale = row[pivot]
            for monomial, coefficient in old.items():
                value = (row.get(monomial, 0) - scale * coefficient) % prime
                if value:
                    row[monomial] = value
                else:
                    row.pop(monomial, None)
    unit = {(): 1}
    while unit:
        pivot = max(unit, key=lambda m: (len(m), m))
        old = basis.get(pivot)
        if old is None:
            break
        scale = unit[pivot]
        for monomial, coefficient in old.items():
            value = (unit.get(monomial, 0) - scale * coefficient) % prime
            if value:
                unit[monomial] = value
            else:
                unit.pop(monomial, None)
    return len(basis), not unit, len(unit)


def exact_rank(columns: set[Monomial], rows: list[Polynomial], add_unit=False) -> int:
    ordered_columns = sorted(columns, key=lambda m: (len(m), m))
    column_index = {monomial: i for i, monomial in enumerate(ordered_columns)}
    entries = {
        i: {column_index[m]: ZZ(a) for m, a in row.items()}
        for i, row in enumerate(rows)
    }
    row_count = len(rows)
    if add_unit:
        entries[row_count] = {column_index[()]: ZZ.one}
        row_count += 1
    matrix = DomainMatrix.from_dod(entries, (row_count, len(columns)), ZZ)
    return matrix.to_field().rank()


def orbit_isomorphism_check() -> None:
    """Swapping residual sites 2 and 4 takes sharp orbit 0 to orbit 1."""
    site_permutation = (0, 1, 4, 3, 2, 5)

    def permute_monomial(monomial: Monomial) -> Monomial:
        image = []
        for index in monomial:
            u, v, a, b = VARIABLE_DATA[index]
            image.append(variable(site_permutation[u], site_permutation[v], a, b))
        return tuple(sorted(image))

    def canonical(generators: list[Polynomial]):
        return sorted(
            tuple(sorted((monomial, coefficient) for monomial, coefficient in g.items()))
            for g in generators
        )

    image = [
        {permute_monomial(monomial): coefficient for monomial, coefficient in g.items()}
        for g in packet_generators(0)
    ]
    require(canonical(image) == canonical(packet_generators(1)), "orbit isomorphism")


EXPECTED = {
    3: (22, 7, ((0, 1), (2, 6), (3, 15)), 7, 8),
    4: (112, 65, ((0, 1), (2, 6), (3, 15), (4, 90)), 57, 58),
    5: (
        1320,
        1105,
        ((0, 1), (2, 6), (3, 15), (4, 90), (5, 1208)),
        921,
        922,
    ),
    6: (
        2160,
        2016,
        ((0, 1), (2, 6), (3, 15), (4, 90), (5, 1208), (6, 840)),
        1586,
        1587,
    ),
}
EXPECTED_D7_FRONTIER = (
    70398,
    110898,
    ((0, 1), (2, 6), (3, 15), (4, 90), (5, 1208), (6, 840), (7, 68238)),
)


def main() -> None:
    orbit_isomorphism_check()
    for degree, expected in EXPECTED.items():
        columns, row_map = constant_component(0, degree)
        rows = list(row_map.values())
        degree_counts = tuple(sorted(Counter(map(len, columns)).items()))
        rank = exact_rank(columns, rows)
        augmented_rank = exact_rank(columns, rows, add_unit=True)
        actual = (len(columns), len(rows), degree_counts, rank, augmented_rank)
        require(actual == expected, (degree, actual))
        print(
            f"D={degree} columns={len(columns)} rows={len(rows)} "
            f"rank_Q={rank} augmented_rank_Q={augmented_rank}"
        )

    columns, row_map = constant_component(0, 7)
    degree_counts = tuple(sorted(Counter(map(len, columns)).items()))
    frontier = (len(columns), len(row_map), degree_counts)
    require(frontier == EXPECTED_D7_FRONTIER, frontier)
    print(
        f"D=7 frontier columns={len(columns)} rows={len(row_map)} "
        "rank=NOT_COMPUTED"
    )
    print("two sharp orbit ideals are isomorphic by the site swap (2 4)")
    print("whole unrestricted 135-cell ideal; no support restriction or localization")


if __name__ == "__main__":
    main()
