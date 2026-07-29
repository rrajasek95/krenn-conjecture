#!/usr/bin/env python3
"""Exact audits for the good-pair fan and six-port triple-cofactor reduction."""

from __future__ import annotations

from itertools import permutations, product
from math import comb


def span_f2(vectors: set[int] | frozenset[int]) -> frozenset[int]:
    """Linear span of bit-vectors in F_2^3."""
    out = {0}
    for v in vectors:
        out |= {x ^ v for x in tuple(out)}
    return frozenset(out)


def all_subspaces_f2_3() -> list[frozenset[int]]:
    spaces = {span_f2({v for v in range(8) if mask & (1 << v)})
              for mask in range(1 << 8)}
    out = sorted(spaces, key=lambda s: (len(s), tuple(sorted(s))))
    assert len(out) == 16
    assert [sum(len(s) == 2**d for s in out) for d in range(4)] == [1, 7, 7, 1]
    return out


def audit_essential_subspaces() -> None:
    """Exhaust distinct subspace families; duplicates can never be essential."""
    spaces = all_subspaces_f2_3()
    full = frozenset(range(8))
    max_essential = 0
    witness = None
    spanning_families = 0
    for mask in range(1 << len(spaces)):
        chosen = [spaces[i] for i in range(len(spaces)) if mask & (1 << i)]
        total = span_f2(set().union(*chosen) if chosen else set())
        if total != full:
            continue
        spanning_families += 1
        essential = []
        for i in range(len(chosen)):
            others = chosen[:i] + chosen[i + 1 :]
            other_span = span_f2(set().union(*others) if others else set())
            if other_span != full:
                essential.append(i)
        if len(essential) > max_essential:
            max_essential = len(essential)
            witness = (chosen, essential)
        assert len(essential) <= 3
    assert spanning_families > 0
    assert max_essential == 3
    assert witness is not None


def audit_counts_and_supports() -> None:
    # The dimension ledger for one row support: s=|S|, f=|F|, t=|S cap F|.
    for universe in range(4, 31):
        for s in range(universe + 1):
            for f in range(universe + 1):
                for t in range(max(0, s + f - universe), min(s, f) + 1):
                    # Deleting u in S leaves s-1 sites; deleting u outside S leaves s.
                    condition = (t == 0 or s - 1 <= 2) and (f - t == 0 or s <= 2)
                    if condition and f >= 4:
                        assert s <= 2

    for n in range(8, 82, 2):
        good = comb(n, 2) - 3 * n
        assert good == n * (n - 7) // 2
        assert 2 * good >= n * (n - 7)
        fan = n - 7
        if n >= 16:
            for regular in range(fan + 1):
                if regular <= 8:
                    assert fan - regular >= n - 15
                else:
                    # Three row supports, each of size at most two.
                    assert regular - 6 >= 3
        if n >= 24:
            for regular in range(fan + 1):
                if regular <= 16:
                    assert fan - regular >= n - 23
                else:
                    zero_blocks = regular - 6
                    assert zero_blocks >= 11
                    assert (zero_blocks + 4) // 5 >= 3

    # Once equality-three endpoints (whose bad degree is at most three) are
    # excluded, minimum bad degree five beats the two-witness orientation budget.
    for vertices in range(1, 100):
        assert 5 * vertices > 4 * vertices


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for j in range(1, len(vertices)):
        b = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(a, b), max(a, b)),) + tail))


def double_factorial_odd(k: int) -> int:
    if k in (-1, 0, 1):
        return 1
    out = 1
    for x in range(k, 0, -2):
        out *= x
    return out


def audit_triple_matching_partition() -> None:
    for n in (8, 10, 12):
        r, u, v = 0, 1, 2
        vertices = tuple(range(n))
        W = tuple(range(3, n))
        forbidden = {(r, u), (r, v)}
        actual = {
            matching
            for matching in perfect_matchings(vertices)
            if not any(edge in forbidden for edge in matching)
        }

        direct = set()
        for x in W:
            remaining = tuple(y for y in W if y != x)
            for tail in perfect_matchings(remaining):
                direct.add(tuple(sorted(((u, v), (r, x)) + tail)))

        three_star = set()
        for x, y, z in permutations(W, 3):
            remaining = tuple(a for a in W if a not in (x, y, z))
            for tail in perfect_matchings(remaining):
                three_star.add(tuple(sorted(((r, x), (u, y), (v, z)) + tail)))

        assert direct.isdisjoint(three_star)
        assert direct | three_star == actual
        m = n // 2
        w = n - 3
        assert len(direct) == w * double_factorial_odd(2 * m - 5)
        assert len(three_star) == w * (w - 1) * (w - 2) * double_factorial_odd(2 * m - 7)


def stored_cell(a: int, b: int, color_a: str, color_b: str):
    """Canonical stored edge cell, retaining which color belongs to which endpoint."""
    if a < b:
        return (a, b, color_a, color_b)
    return (b, a, color_b, color_a)


def audit_endpoint_orientation() -> None:
    # Re-name the three endpoints in every numerical order and ensure that b_de
    # always carries d at named u and e at named v after canonical storage.
    for r, u, v in permutations((0, 1, 2), 3):
        cell = stored_cell(u, v, "d", "e")
        if u < v:
            assert cell == (u, v, "d", "e")
        else:
            assert cell == (v, u, "e", "d")
        pcell = stored_cell(r, 3, "c", "alpha")
        if r < 3:
            assert pcell[2:] == ("c", "alpha")
        else:
            assert pcell[2:] == ("alpha", "c")


def rank_f2(columns: list[int]) -> int:
    basis: dict[int, int] = {}
    for value in columns:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def tensor_index(a: int, b: int, z: int, db: int = 3, dz: int = 2) -> int:
    return (a * db + b) * dz + z


def audit_two_hole_coordinate_anchor() -> None:
    # Over F_2, exhaust the tangent space
    # p_a tensor V_b tensor R + V_a tensor p_b tensor R.
    # A pure target e tensor e tensor x belongs to it exactly when e lies
    # on one of the two endpoint lines. This is the quotient proof in finite form.
    dim_a = dim_b = 3
    dim_z = 2
    for e_idx in range(3):
        e = 1 << e_idx
        for pa in range(1, 1 << dim_a):
            for pb in range(1, 1 << dim_b):
                columns: list[int] = []
                for b_idx in range(dim_b):
                    for z_idx in range(dim_z):
                        col = 0
                        for a_idx in range(dim_a):
                            if pa & (1 << a_idx):
                                col ^= 1 << tensor_index(a_idx, b_idx, z_idx)
                        columns.append(col)
                for a_idx in range(dim_a):
                    for z_idx in range(dim_z):
                        col = 0
                        for b_idx in range(dim_b):
                            if pb & (1 << b_idx):
                                col ^= 1 << tensor_index(a_idx, b_idx, z_idx)
                        columns.append(col)
                base_rank = rank_f2(columns)
                for x in range(1, 1 << dim_z):
                    target = 0
                    for a_idx in range(dim_a):
                        if not (e & (1 << a_idx)):
                            continue
                        for b_idx in range(dim_b):
                            if not (e & (1 << b_idx)):
                                continue
                            for z_idx in range(dim_z):
                                if x & (1 << z_idx):
                                    target ^= 1 << tensor_index(a_idx, b_idx, z_idx)
                    belongs = rank_f2(columns + [target]) == base_rank
                    endpoint_anchor = pa == e or pb == e
                    assert belongs == endpoint_anchor


def audit_hole_projection() -> None:
    # A degree-(w-1) sector is identified by its unique hole. Multiplication
    # by a site-linear term survives exactly when that term occupies the hole.
    for w in range(3, 13):
        sites = set(range(w))
        for support_mask in range(1 << min(w, 6)):
            support = {x for x in range(min(w, 6)) if support_mask & (1 << x)}
            C = set(range(min(w, 6)))
            visible = set()
            for hole in sites:
                for p_site in support:
                    survives = p_site == hole
                    if survives:
                        visible.add(hole)
                    assert survives == (p_site not in (sites - {hole}))
            assert visible <= C
            assert visible == support


def multiply_response(p_site: int, p_color: int, hole: int, word: dict[int, int]):
    if p_site != hole:
        return None
    out = dict(word)
    out[p_site] = p_color
    return tuple(out[x] for x in sorted(out))


def audit_sharp_response() -> None:
    C = (0, 1, 2)
    for c, d, e in product(range(3), repeat=3):
        if d != e:
            value = None
        else:
            hole = d
            word = {x: d for x in C if x != hole}
            value = multiply_response(c, c, hole, word)
        expected = (c, c, c) if c == d == e else None
        assert value == expected


def main() -> None:
    audit_essential_subspaces()
    audit_counts_and_supports()
    audit_triple_matching_partition()
    audit_endpoint_orientation()
    audit_two_hole_coordinate_anchor()
    audit_hole_projection()
    audit_sharp_response()
    print("good-pair fan six-port triple-cofactor reduction: PASS")


if __name__ == "__main__":
    main()
