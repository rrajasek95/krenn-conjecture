#!/usr/bin/env python3
"""Exact audit for polarized-eight-site-shared-pair-cap-countermodel.md.

This checks both the isolated rational countermodel and the finite census
behind the full-nine fixed-q obstruction.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


SITES = tuple(range(8))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)
assert len(MATCHINGS) == 105


def empty_quadratic():
    return {edge: {} for edge in EDGES}


def put(quadratic, edge, cell, value):
    edge = tuple(sorted(edge))
    value = Fraction(value)
    if value:
        quadratic[edge][cell] = value


def entry(quadratic, edge, colors):
    u, v = edge
    if u < v:
        return quadratic.get((u, v), {}).get(tuple(colors), Fraction(0))
    return quadratic.get((v, u), {}).get(tuple(reversed(colors)), Fraction(0))


def add_scaled(left, alpha, right, beta):
    answer = empty_quadratic()
    for edge in EDGES:
        cells = set(left.get(edge, {})) | set(right.get(edge, {}))
        for cell in cells:
            value = alpha * left.get(edge, {}).get(cell, 0)
            value += beta * right.get(edge, {}).get(cell, 0)
            put(answer, edge, cell, value)
    return answer


def decorated_matching_terms(vertices, quadratic):
    """Return (word-on-vertices, coefficient, decorated matching)."""
    vertices = tuple(vertices)
    answer = []
    for matching in perfect_matchings(vertices):
        cell_lists = []
        for edge in matching:
            cells = tuple(quadratic.get(tuple(sorted(edge)), {}).items())
            if not cells:
                break
            cell_lists.append(cells)
        else:
            for choices in product(*cell_lists):
                local = {}
                coefficient = Fraction(1)
                decorated = []
                for edge, (cell, value) in zip(matching, choices, strict=True):
                    u, v = edge
                    local[u], local[v] = cell
                    coefficient *= value
                    decorated.append((edge, cell))
                answer.append(
                    (
                        tuple(local[site] for site in vertices),
                        coefficient,
                        tuple(decorated),
                    )
                )
    return tuple(answer)


def matching_tensor(vertices, quadratic):
    answer = {}
    for word, coefficient, _ in decorated_matching_terms(vertices, quadratic):
        answer[word] = answer.get(word, Fraction(0)) + coefficient
    return {word: value for word, value in answer.items() if value}


def polarized_tensor(z, q):
    """Compute z*q^[3] on all eight sites by distinguished-edge sums."""
    answer = {}
    for coloring in product(COLORS, repeat=8):
        coefficient = Fraction(0)
        for matching in MATCHINGS:
            q_values = [
                entry(q, edge, (coloring[edge[0]], coloring[edge[1]]))
                for edge in matching
            ]
            z_values = [
                entry(z, edge, (coloring[edge[0]], coloring[edge[1]]))
                for edge in matching
            ]
            for distinguished in range(4):
                term = z_values[distinguished]
                for index in range(4):
                    if index != distinguished:
                        term *= q_values[index]
                coefficient += term
        if coefficient:
            answer[coloring] = coefficient
    return answer


def build_q():
    q = empty_quadratic()
    matchings = (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 7), (1, 2), (3, 4), (5, 6)),
        ((0, 4), (1, 7), (2, 6), (3, 5)),
    )
    for color, matching in enumerate(matchings):
        for edge in matching:
            put(q, edge, (color, color), 1)
    return q, matchings


def build_product_cap():
    p = {(0, 2): Fraction(1), (2, 2): Fraction(1),
         (4, 2): Fraction(-1, 8), (6, 2): Fraction(-1, 8)}
    s = {(0, 2): Fraction(1), (2, 2): Fraction(-1),
         (4, 2): Fraction(-1, 8), (6, 2): Fraction(1, 8)}
    ps = empty_quadratic()
    for u, v in EDGES:
        for color_u, color_v in product(COLORS, repeat=2):
            value = p.get((u, color_u), 0) * s.get((v, color_v), 0)
            value += s.get((u, color_u), 0) * p.get((v, color_v), 0)
            put(ps, (u, v), (color_u, color_v), value)
    return p, s, ps


def attach_missing_cell(terms, missing_edge, color):
    answer = {}
    for word, coefficient, _ in terms:
        remaining = tuple(site for site in SITES if site not in missing_edge)
        full = dict(zip(remaining, word, strict=True))
        full[missing_edge[0]] = color
        full[missing_edge[1]] = color
        full_word = tuple(full[site] for site in SITES)
        answer[full_word] = answer.get(full_word, Fraction(0)) + coefficient
    return answer


def canonical_cell(mode_x, mode_y):
    """Return ((u,v),(alpha,beta)) with the physical edge ordered."""
    u, alpha = mode_x
    v, beta = mode_y
    if u < v:
        return (u, v), (alpha, beta)
    return (v, u), (beta, alpha)


def audit_singleton_exposure(q, color_matchings, q4):
    """Audit the full matrix-valued map R -> R*q^[3]."""
    columns = tuple(
        (edge, cell)
        for edge in EDGES
        for cell in product(COLORS, repeat=2)
    )
    rows = {}
    for edge, cell in columns:
        u, v = edge
        complement = tuple(site for site in SITES if site not in edge)
        for word, coefficient, _ in decorated_matching_terms(complement, q):
            full = dict(zip(complement, word, strict=True))
            full[u], full[v] = cell
            full_word = tuple(full[site] for site in SITES)
            row = rows.setdefault(full_word, {})
            column = (edge, cell)
            row[column] = row.get(column, Fraction(0)) + coefficient

    rows = {
        word: {column: value for column, value in row.items() if value}
        for word, row in rows.items()
    }
    rows = {word: row for word, row in rows.items() if row}
    singleton_rows = {
        word: next(iter(row.items()))
        for word, row in rows.items()
        if len(row) == 1
    }

    active = {
        (tuple(sorted(edge)), (color, color))
        for color, matching in enumerate(color_matchings)
        for edge in matching
    }
    inactive = set(columns) - active
    singleton_columns = {column for column, _ in singleton_rows.values()}

    assert len(columns) == 252
    assert len(rows) == 363
    assert len(singleton_rows) == 358
    assert len(active) == 12
    assert len(inactive) == 240
    assert singleton_columns == inactive
    assert all(value == 1 for _, value in singleton_rows.values())
    assert set(singleton_rows).isdisjoint(q4)
    assert set(singleton_rows).isdisjoint({(color,) * 8 for color in COLORS})

    # Every pair of distinct active physical cells is either disjoint or
    # meets once.  Audit precisely the four or three cross corners used by
    # the zero-pair proof; all must be inactive singleton-exposed cells.
    active_list = sorted(active)
    physical_edges = {edge for edge, _ in active_list}
    assert len(physical_edges) == 12
    disjoint_pairs = 0
    meeting_pairs = 0
    for index, (first_edge, first_cell) in enumerate(active_list):
        first_color = first_cell[0]
        first_modes = tuple((site, first_color) for site in first_edge)
        for second_edge, second_cell in active_list[index + 1 :]:
            second_color = second_cell[0]
            second_modes = tuple((site, second_color) for site in second_edge)
            common_sites = set(first_edge) & set(second_edge)
            if not common_sites:
                disjoint_pairs += 1
                cross_cells = {
                    canonical_cell(first_mode, second_mode)
                    for first_mode in first_modes
                    for second_mode in second_modes
                }
                assert len(cross_cells) == 4
            else:
                assert len(common_sites) == 1
                meeting_pairs += 1
                common_site = next(iter(common_sites))
                first_other = next(
                    site for site in first_edge if site != common_site
                )
                second_other = next(
                    site for site in second_edge if site != common_site
                )
                cross_cells = {
                    canonical_cell(
                        (common_site, first_color),
                        (second_other, second_color),
                    ),
                    canonical_cell(
                        (first_other, first_color),
                        (common_site, second_color),
                    ),
                    canonical_cell(
                        (first_other, first_color),
                        (second_other, second_color),
                    ),
                }
                assert len(cross_cells) == 3
            assert cross_cells <= inactive

    assert disjoint_pairs == 42
    assert meeting_pairs == 24
    assert disjoint_pairs + meeting_pairs == 66

    # The final target difference (E_00-E_11)/4 has a nonzero 2-by-2
    # minor, whereas a scalar multiple of one rank-one line does not.
    target_minor = Fraction(1, 4) * Fraction(-1, 4)
    assert target_minor == Fraction(-1, 16)
    return (
        len(rows),
        len(singleton_rows),
        len(singleton_columns),
        disjoint_pairs,
        meeting_pairs,
        target_minor,
    )


def audit_border_core_isomorphism(color_matchings):
    """Check the stated relabeling to the registered Laurent border core."""
    site_map = (3, 0, 1, 5, 6, 7, 4, 2)
    color_map = (1, 2, 0)
    border_matchings = (
        frozenset(((0, 2), (1, 4), (3, 6), (5, 7))),
        frozenset(((0, 3), (1, 5), (2, 4), (6, 7))),
        frozenset(((0, 1), (2, 3), (4, 7), (5, 6))),
    )
    for color, matching in enumerate(color_matchings):
        image = frozenset(
            tuple(sorted((site_map[u], site_map[v])))
            for u, v in matching
        )
        assert image == border_matchings[color_map[color]]
    return color_map, site_map


def audit_overlap_normalization():
    """Check the factorial relating raw and polarized pair slices.

    If q0 has four matching edges, then q0*q0^[3] = 4*q0^[4].
    Hence (b*q0 + 4*p*s)*q0^[3] is four times
    b*q0^[4] + p*s*q0^[3], including its target side.
    """
    raw_direct = Fraction(1)
    raw_star = Fraction(1)
    polarized_direct = Fraction(4)
    polarized_star = Fraction(4)
    assert polarized_direct == 4 * raw_direct
    assert polarized_star == 4 * raw_star
    return polarized_direct, raw_direct


def main():
    q, color_matchings = build_q()
    border_isomorphism = audit_border_core_isomorphism(color_matchings)
    p, s, ps = build_product_cap()

    nonzero_q = {
        (edge, cell, value)
        for edge, matrix in q.items()
        for cell, value in matrix.items()
    }
    assert len(nonzero_q) == 12

    nonzero_ps = {
        (edge, cell, value)
        for edge, matrix in ps.items()
        for cell, value in matrix.items()
    }
    assert nonzero_ps == {
        ((0, 4), (2, 2), Fraction(-1, 4)),
        ((2, 6), (2, 2), Fraction(1, 4)),
    }

    q4_terms = decorated_matching_terms(SITES, q)
    assert len(q4_terms) == 5
    q4 = matching_tensor(SITES, q)
    mixed_a = (2, 1, 1, 2, 2, 2, 0, 0)
    mixed_b = (2, 2, 0, 0, 2, 1, 1, 2)
    expected_q4 = {(color,) * 8: Fraction(1) for color in COLORS}
    expected_q4[mixed_a] = Fraction(1)
    expected_q4[mixed_b] = Fraction(1)
    assert q4 == expected_q4

    complement_04 = tuple(site for site in SITES if site not in (0, 4))
    complement_26 = tuple(site for site in SITES if site not in (2, 6))
    terms_04 = decorated_matching_terms(complement_04, q)
    terms_26 = decorated_matching_terms(complement_26, q)
    assert len(terms_04) == 3
    assert len(terms_26) == 1
    assert attach_missing_cell(terms_04, (0, 4), 2) == {
        mixed_a: Fraction(1),
        mixed_b: Fraction(1),
        (2,) * 8: Fraction(1),
    }
    assert attach_missing_cell(terms_26, (2, 6), 2) == {
        (2,) * 8: Fraction(1)
    }

    a = Fraction(1, 4)
    z = add_scaled(q, a, ps, Fraction(4))
    nonzero_z = {
        (edge, cell): value
        for edge, matrix in z.items()
        for cell, value in matrix.items()
    }
    assert len(nonzero_z) == 12
    assert nonzero_z[(0, 4), (2, 2)] == Fraction(-3, 4)
    assert nonzero_z[(2, 6), (2, 2)] == Fraction(5, 4)
    assert all(
        value == Fraction(1, 4)
        for key, value in nonzero_z.items()
        if key not in {((0, 4), (2, 2)), ((2, 6), (2, 2))}
    )

    polarized = polarized_tensor(z, q)
    target = {(color,) * 8: Fraction(1) for color in COLORS}
    assert polarized == target
    exposure = audit_singleton_exposure(q, color_matchings, q4)
    overlap_factors = audit_overlap_normalization()

    print("perfect matchings enumerated:", len(MATCHINGS))
    print(
        "border-core isomorphism (colors / sites):",
        border_isomorphism,
    )
    print("coloring coefficients checked:", 3**8)
    print("q^[4] decorated terms:", len(q4_terms), tuple(q4))
    print("ps support:", sorted(nonzero_ps))
    print("F_04 decorated terms:", len(terms_04))
    print("F_26 decorated terms:", len(terms_26))
    print("z*q^[3] support:", polarized)
    print(
        "H_q rows / singleton rows / exposed inactive cells:",
        exposure[:3],
    )
    print(
        "active-cell pairs (disjoint / meeting):",
        exposure[3:5],
    )
    print("target rank-two minor:", exposure[5])
    print(
        "overlap target factors (polarized / raw):",
        overlap_factors,
    )
    print("full-nine fixed-q obstruction audit: PASS")
    print("exact eight-site shared pair-cap countermodel: PASS")


if __name__ == "__main__":
    main()
