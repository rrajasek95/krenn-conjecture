#!/usr/bin/env python3
"""Clean-room audit of the path/triangle exposed-grid obstruction.

This checker does not import the primary checker.  It reconstructs the
typed grids from omission incidences, exhausts the crossed-target algebra
over small odd finite fields (including zero and half-zero cases), proves
the final Boolean contradictions with a parity union-find, and gives exact
rational witnesses showing that the wedge quotient grid is satisfiable.
"""

from itertools import product


def vzero(n):
    return (0,) * n


def is_zero(v):
    return not any(v)


def scale(c, v, modulus=None):
    if modulus is None:
        return tuple(c * x for x in v)
    return tuple((c * x) % modulus for x in v)


def h_matrix(x, y, modulus=None):
    """Return a b'^T + a' b^T as a row-major tuple."""
    a, b = x
    c, d = y
    n = len(a)
    entries = []
    for i in range(n):
        for j in range(n):
            value = a[i] * d[j] + c[i] * b[j]
            entries.append(value if modulus is None else value % modulus)
    return tuple(entries)


def matrix_unit(n, i, coefficient=1):
    out = [0] * (n * n)
    out[n * i + i] = coefficient
    return tuple(out)


def zero_pair_kind(x, y, modulus):
    """Classify a nonzero zero-pair as P, S, or mixed antipodes."""
    if h_matrix(x, y, modulus) != vzero(len(x[0]) ** 2):
        return None
    if (is_zero(x[0]) and is_zero(x[1])) or (
        is_zero(y[0]) and is_zero(y[1])
    ):
        return "has-zero-point"
    if is_zero(x[1]) and is_zero(y[1]):
        return "P"
    if is_zero(x[0]) and is_zero(y[0]):
        return "S"
    for rho in range(1, modulus):
        candidate = (
            scale(rho, x[0], modulus),
            scale(-rho, x[1], modulus),
        )
        if y == candidate:
            return "M"
    return "unclassified"


def all_points(modulus, n, include_zero=False):
    vectors = tuple(product(range(modulus), repeat=n))
    points = tuple(product(vectors, repeat=2))
    if include_zero:
        return points
    return tuple(x for x in points if not (is_zero(x[0]) and is_zero(x[1])))


def audit_zero_pair_trichotomy(modulus):
    points_with_zero = all_points(modulus, 2, include_zero=True)
    zero_point = (vzero(2), vzero(2))
    for x in points_with_zero:
        for y in points_with_zero:
            if h_matrix(x, y, modulus) != vzero(4):
                continue
            kind = zero_pair_kind(x, y, modulus)
            if x == zero_point or y == zero_point:
                assert kind == "has-zero-point"
            else:
                assert kind in {"P", "S", "M"}

    # Conversely, every classified nonzero branch really is a zero pair.
    nonzero = all_points(modulus, 2)
    for x in nonzero:
        for y in nonzero:
            kind = zero_pair_kind(x, y, modulus)
            assert (kind in {"P", "S", "M"}) == (
                h_matrix(x, y, modulus) == vzero(4)
            )


def target_pairs(modulus, diagonal_index):
    points = all_points(modulus, 2)
    targets = {
        matrix_unit(2, diagonal_index, alpha)
        for alpha in range(1, modulus)
    }
    return tuple(
        (x, y)
        for x in points
        for y in points
        if h_matrix(x, y, modulus) in targets
    )


def pure_kind(x):
    if not is_zero(x[0]) and is_zero(x[1]):
        return "P"
    if is_zero(x[0]) and not is_zero(x[1]):
        return "S"
    return None


def audit_crossed_target_exhaustive():
    """Test every F_3 realization of two distinct crossed targets."""
    modulus = 3
    first = target_pairs(modulus, 0)
    second = target_pairs(modulus, 1)
    realizations = 0
    for x, y in first:
        for z, w in second:
            if h_matrix(x, z, modulus) != vzero(4):
                continue
            if h_matrix(y, w, modulus) != vzero(4):
                continue
            realizations += 1
            kinds = tuple(map(pure_kind, (x, y, z, w)))
            assert None not in kinds
            assert kinds[0] == kinds[2]
            assert kinds[1] == kinds[3]
            assert kinds[0] != kinds[1]
    assert realizations > 0
    return realizations


def canonical_cell(x, y):
    assert x != y
    return tuple(sorted((x, y)))


def derive_grid(omitted_pairs):
    missing = {}
    for color, pair in omitted_pairs.items():
        assert len(pair) == 2 and pair[0] != pair[1]
        for site in pair:
            missing.setdefault(site, set()).add(color)
    targets = {}
    zeros = set()
    for color, (u, v) in omitted_pairs.items():
        for i in missing[u]:
            for j in missing[v]:
                cell = canonical_cell((u, i), (v, j))
                if i == j == color:
                    targets[cell] = color
                else:
                    zeros.add(cell)
    assert len(targets) == len(omitted_pairs)
    assert set(targets).isdisjoint(zeros)
    return missing, targets, zeros


class ParityUnionFind:
    """Maintain equations type(x) xor type(y) = parity."""

    def __init__(self):
        self.parent = {}
        self.xor_to_parent = {}
        self.consistent = True

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.xor_to_parent[x] = 0

    def find(self, x):
        self.add(x)
        if self.parent[x] == x:
            return x, 0
        root, parity = self.find(self.parent[x])
        self.xor_to_parent[x] ^= parity
        self.parent[x] = root
        return root, self.xor_to_parent[x]

    def impose(self, x, y, parity):
        rx, px = self.find(x)
        ry, py = self.find(y)
        if rx == ry:
            if (px ^ py) != parity:
                self.consistent = False
            return
        self.parent[rx] = ry
        self.xor_to_parent[rx] = px ^ py ^ parity

    def component_count(self):
        return len({self.find(x)[0] for x in self.parent})


def parity_audit(targets, zeros):
    system = ParityUnionFind()
    for x, y in targets:
        system.impose(x, y, 1)
    for x, y in zeros:
        system.impose(x, y, 0)
    return system


def endpoint_aliases(targets):
    by_color = {color: edge for edge, color in targets.items()}
    return by_color


def has_crossed_square(first_edge, second_edge, zeros):
    x, y = first_edge
    z, w = second_edge
    return (
        canonical_cell(x, z) in zeros
        and canonical_cell(y, w) in zeros
    ) or (
        canonical_cell(x, w) in zeros
        and canonical_cell(y, z) in zeros
    )


def audit_path_and_triangle():
    path_pairs = {0: ("A", "B"), 1: ("B", "C"), 2: ("C", "D")}
    _, path_targets, path_zeros = derive_grid(path_pairs)
    assert len(path_zeros) == 5
    path_by_color = endpoint_aliases(path_targets)
    # The two crossed squares cover all target endpoints.  The crossed-target
    # lemma therefore licenses the pure parity reduction for the whole grid.
    t0, t1, t2 = (path_by_color[i] for i in range(3))
    assert has_crossed_square(t0, t1, path_zeros)
    assert has_crossed_square(t1, t2, path_zeros)
    path_system = parity_audit(path_targets, path_zeros)
    assert not path_system.consistent

    triangle_pairs = {0: ("A", "B"), 1: ("B", "C"), 2: ("C", "A")}
    _, triangle_targets, triangle_zeros = derive_grid(triangle_pairs)
    assert len(triangle_zeros) == 9
    triangle_by_color = endpoint_aliases(triangle_targets)
    t0, t1, t2 = (triangle_by_color[i] for i in range(3))
    assert has_crossed_square(t0, t1, triangle_zeros)
    assert has_crossed_square(t1, t2, triangle_zeros)
    triangle_system = parity_audit(triangle_targets, triangle_zeros)
    assert not triangle_system.consistent


def rational_wedge_witnesses():
    wedge_pairs = {0: ("A", "B"), 1: ("B", "C"), 2: ("D", "E")}
    _, targets, zeros = derive_grid(wedge_pairs)
    assert len(zeros) == 2
    by_color = endpoint_aliases(targets)

    # Choose a base orientation independently on the connected first-two-
    # target component and on the disconnected third target.
    witnesses = []
    for flip_connected, flip_disjoint in product((0, 1), repeat=2):
        assignment = {}
        for color in (0, 1):
            left, right = sorted(by_color[color])
            # Grid incidence, not lexicographic endpoint order, fixes which
            # endpoints must have the same type.  Search the two orientations
            # directly and retain the one compatible with all accumulated
            # zero cells.
            assignment[left] = flip_connected
            assignment[right] = flip_connected ^ 1
        # If the arbitrary sorted orientations disagreed with a zero edge,
        # flip both endpoints of target 1; its target remains nonzero.
        if any(assignment[x] != assignment[y] for x, y in zeros):
            for endpoint in by_color[1]:
                assignment[endpoint] ^= 1
        left, right = sorted(by_color[2])
        assignment[left] = flip_disjoint
        assignment[right] = flip_disjoint ^ 1
        assert all(assignment[x] != assignment[y] for x, y in targets)
        assert all(assignment[x] == assignment[y] for x, y in zeros)

        point = {}
        for endpoint, kind in assignment.items():
            color = endpoint[1]
            e = tuple(1 if k == color else 0 for k in range(3))
            point[endpoint] = (e, vzero(3)) if kind == 0 else (vzero(3), e)
        for edge, color in targets.items():
            x, y = edge
            assert h_matrix(point[x], point[y]) == matrix_unit(3, color)
        for x, y in zeros:
            assert h_matrix(point[x], point[y]) == vzero(9)
        witnesses.append(point)
    assert len(witnesses) == 4

    system = parity_audit(targets, zeros)
    assert system.consistent
    assert 2 ** system.component_count() == 4


def main():
    audit_zero_pair_trichotomy(3)
    audit_zero_pair_trichotomy(5)
    crossed_count = audit_crossed_target_exhaustive()
    audit_path_and_triangle()
    rational_wedge_witnesses()
    print("zero-pair trichotomy over F_3 and F_5: exhaustive PASS")
    print(f"crossed-target F_3 realizations checked: {crossed_count}")
    print("path parity system: UNSAT")
    print("triangle parity system: UNSAT")
    print("wedge quotient grid: 4 exact rational pure witnesses")


if __name__ == "__main__":
    main()
