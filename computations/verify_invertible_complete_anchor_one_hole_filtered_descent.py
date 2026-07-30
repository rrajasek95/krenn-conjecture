#!/usr/bin/env python3
"""Exact lightweight audit of the common-site filtered one-hole packet."""

if not __debug__:
    raise RuntimeError("run without -O: this checker uses fail-closed assertions")

from fractions import Fraction as F
from itertools import combinations, product


def add(*polys):
    out = {}
    for poly in polys:
        for monomial, value in poly.items():
            out[monomial] = out.get(monomial, F(0)) + value
    return {monomial: value for monomial, value in out.items() if value}


def scale(poly, scalar):
    return {monomial: scalar * value for monomial, value in poly.items()
            if scalar * value}


def multiply(left, right):
    out = {}
    for left_monomial, left_value in left.items():
        left_sites = set(left_monomial)
        for right_monomial, right_value in right.items():
            if left_sites.intersection(right_monomial):
                continue
            monomial = tuple(sorted(left_sites.union(right_monomial)))
            out[monomial] = out.get(monomial, F(0)) + left_value * right_value
    return {monomial: value for monomial, value in out.items() if value}


def divided_power(poly, exponent):
    if exponent == 0:
        return {(): F(1)}
    out = {}
    for chosen in combinations(tuple(poly.items()), exponent):
        term = {(): F(1)}
        for monomial, value in chosen:
            term = multiply(term, {monomial: value})
        out = add(out, term)
    return out


def linear(values):
    return {(site,): F(value) for site, value in enumerate(values) if value}


def quadratic(site_count, offset=0):
    return {
        (left, right): F(1 + ((3 * left + 5 * right + offset) % 7))
        for left, right in combinations(range(site_count), 2)
    }


def coefficient_at_site(poly, site):
    out = {}
    for monomial, value in poly.items():
        if site not in monomial:
            continue
        reduced = tuple(vertex for vertex in monomial if vertex != site)
        out[reduced] = out.get(reduced, F(0)) + value
    return {monomial: value for monomial, value in out.items() if value}


def restrict_off_site(poly, site):
    return {monomial: value for monomial, value in poly.items()
            if site not in monomial}


def local_value(form, site):
    return form.get((site,), F(0))


def incident_form(quad, site):
    out = {}
    for monomial, value in quad.items():
        if site not in monomial:
            continue
        other = monomial[0] if monomial[1] == site else monomial[1]
        out[(other,)] = out.get((other,), F(0)) + value
    return out


def matrix_entry(matrix, row, column):
    return F(matrix[row][column])


def triple_row(direct_pq, direct_pr, direct_qr, x_rows, y_rows,
               t_rows, internal, i, j, k):
    linear_part = add(
        scale(t_rows[k], matrix_entry(direct_pq, i, j)),
        scale(y_rows[j], matrix_entry(direct_pr, i, k)),
        scale(x_rows[i], matrix_entry(direct_qr, j, k)),
    )
    return add(
        multiply(linear_part, divided_power(internal, 2)),
        multiply(multiply(multiply(x_rows[i], y_rows[j]), t_rows[k]), internal),
    )


def audit_physical_channel_formula():
    site_count = 5
    witness = 0
    internal = quadratic(site_count, offset=2)
    direct_pq = ((2, -1, 3), (1, 2, 0), (4, 1, 1))
    direct_pr = ((1, 2, -1), (0, 3, 2), (2, 1, 2))
    direct_qr = ((3, 0, 1), (-2, 1, 4), (1, 2, 1))

    # The first entries vanish: this is the missing physical c-channel at w.
    x_rows = [linear((0, 1 + i, 2 - i, 3, -1)) for i in range(3)]
    y_rows = [linear((0, 2, -1 - i, 1 + i, 4)) for i in range(3)]
    t_rows = [linear((2 + i, -1, 3, i + 1, 2 - i)) for i in range(3)]

    z0 = restrict_off_site(internal, witness)
    spoke = incident_form(internal, witness)
    x0 = [restrict_off_site(row, witness) for row in x_rows]
    y0 = [restrict_off_site(row, witness) for row in y_rows]
    t0 = [restrict_off_site(row, witness) for row in t_rows]

    for i, j, k in product(range(3), repeat=3):
        a_ij = add(
            scale(divided_power(z0, 2), matrix_entry(direct_pq, i, j)),
            multiply(multiply(x0[i], y0[j]), z0),
        )
        b_ijk = add(
            multiply(
                add(
                    scale(t0[k], matrix_entry(direct_pq, i, j)),
                    scale(y0[j], matrix_entry(direct_pr, i, k)),
                    scale(x0[i], matrix_entry(direct_qr, j, k)),
                ),
                z0,
            ),
            multiply(multiply(x0[i], y0[j]), t0[k]),
        )
        predicted = add(
            scale(a_ij, local_value(t_rows[k], witness)),
            multiply(spoke, b_ijk),
        )
        actual = coefficient_at_site(
            triple_row(direct_pq, direct_pr, direct_qr, x_rows, y_rows,
                       t_rows, internal, i, j, k),
            witness,
        )
        assert actual == predicted, (i, j, k, actual, predicted)

    # Exposing r in the pq pair chart reproduces the literal triple row.
    r_site = 5
    internal_pq = dict(internal)
    for k, row in enumerate(t_rows):
        if k != 0:
            continue
        for monomial, value in row.items():
            internal_pq[tuple(sorted((r_site, monomial[0])))] = value
    p_rows = []
    q_rows = []
    for i in range(3):
        p_rows.append(add(x_rows[i], {(r_site,): F(direct_pr[i][0])}))
        q_rows.append(add(y_rows[i], {(r_site,): F(direct_qr[i][0])}))
    for i, j in product(range(3), repeat=2):
        pair_row = add(
            scale(divided_power(internal_pq, 3), F(direct_pq[i][j])),
            multiply(multiply(p_rows[i], q_rows[j]),
                     divided_power(internal_pq, 2)),
        )
        exposed = coefficient_at_site(pair_row, r_site)
        expected = triple_row(
            direct_pq, direct_pr, direct_qr, x_rows, y_rows, t_rows,
            internal, i, j, 0,
        )
        assert exposed == expected, (i, j, exposed, expected)

    # If this witness is the selected fourth site in the selected colour,
    # its missing q-channel kills F and curvature routes to the nonzero
    # r-star scalar g_k.  This audits the label bookkeeping in (15a)-(15b).
    selected_i, selected_j, selected_k = 0, 1, 0
    selected_a = F(direct_pq[selected_i][selected_j])
    selected_b = F(direct_pr[selected_i][selected_k])
    selected_f = local_value(y_rows[selected_j], witness)
    selected_u = local_value(t_rows[selected_k], witness)
    curvature = selected_a * selected_u - selected_b * selected_f
    assert selected_f == 0
    assert curvature == selected_a * selected_u != 0


def dot(left, matrix, right, modulus=None):
    value = sum(left[i] * matrix[i][j] * right[j]
                for i in range(3) for j in range(3))
    return value if modulus is None else value % modulus


def contract_rows(rows, vector):
    return add(*(scale(rows[index], F(value))
                 for index, value in enumerate(vector)))


def audit_contracted_formula():
    site_count = 5
    witness = 0
    internal = quadratic(site_count, offset=4)
    direct_pq = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    direct_pr = ((2, 1, 0), (-1, 1, 2), (3, 0, 1))
    direct_qr = ((1, 2, -1), (0, 3, 1), (2, -2, 1))
    xi = (1, 1, 0)
    eta = (1, -1, 1)
    assert dot(xi, direct_pq, eta) == 0
    assert any(xi[i] * eta[j] for i in range(3) for j in range(3) if i != j)

    x_rows = [linear((1, 2 + i, -1, i + 1, 3)) for i in range(3)]
    y_rows = [linear((2, 1 - i, 3, -2, i + 1)) for i in range(3)]
    # Force the contracted local coefficients at w to vanish.
    x_rows[1] = add(x_rows[1], {(witness,): F(-2)})
    y_rows[2] = add(y_rows[2], {(witness,): F(-2)})
    t_rows = [linear((i + 1, 2, -1, 3 - i, 1)) for i in range(3)]
    x_cap = contract_rows(x_rows, xi)
    y_cap = contract_rows(y_rows, eta)
    assert local_value(x_cap, witness) == 0
    assert local_value(y_cap, witness) == 0

    z0 = restrict_off_site(internal, witness)
    spoke = incident_form(internal, witness)
    x0 = restrict_off_site(x_cap, witness)
    y0 = restrict_off_site(y_cap, witness)
    a_term = multiply(multiply(x0, y0), z0)

    for k in range(3):
        contracted = {}
        for i, j in product(range(3), repeat=2):
            contracted = add(
                contracted,
                scale(
                    triple_row(direct_pq, direct_pr, direct_qr,
                               x_rows, y_rows, t_rows, internal, i, j, k),
                    F(xi[i] * eta[j]),
                ),
            )
        alpha = sum(F(xi[i] * direct_pr[i][k]) for i in range(3))
        beta = sum(F(eta[j] * direct_qr[j][k]) for j in range(3))
        contracted_directly = add(
            multiply(add(scale(y_cap, alpha), scale(x_cap, beta)),
                     divided_power(internal, 2)),
            multiply(multiply(multiply(x_cap, y_cap), t_rows[k]), internal),
        )
        assert contracted == contracted_directly

        t0 = restrict_off_site(t_rows[k], witness)
        b_term = add(
            multiply(add(scale(y0, alpha), scale(x0, beta)), z0),
            multiply(multiply(x0, y0), t0),
        )
        predicted = add(
            scale(a_term, local_value(t_rows[k], witness)),
            multiply(spoke, b_term),
        )
        assert coefficient_at_site(contracted, witness) == predicted


def vectors(modulus=2):
    return [tuple(values) for values in product(range(modulus), repeat=3)]


def span(generators, modulus=2):
    if not generators:
        return frozenset({(0, 0, 0)})
    answer = set()
    for coefficients in product(range(modulus), repeat=len(generators)):
        answer.add(tuple(
            sum(coefficients[index] * generators[index][coordinate]
                for index in range(len(generators))) % modulus
            for coordinate in range(3)
        ))
    return frozenset(answer)


def all_subspaces(modulus=2):
    nonzero = vectors(modulus)[1:]
    spaces = {span(())}
    for count in range(1, 4):
        for generators in combinations(nonzero, count):
            spaces.add(span(generators, modulus))
    return sorted(spaces, key=lambda space: (len(space), tuple(sorted(space))))


def dimension(space, modulus=2):
    size = len(space)
    result = 0
    while size > 1:
        assert size % modulus == 0
        size //= modulus
        result += 1
    return result


def determinant_rows(left, right, target, modulus=2):
    matrix = (left, right, target)
    value = (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )
    return value % modulus


def cross(left, right, modulus=2):
    return (
        (left[1] * right[2] - left[2] * right[1]) % modulus,
        (left[2] * right[0] - left[0] * right[2]) % modulus,
        (left[0] * right[1] - left[1] * right[0]) % modulus,
    )


def audit_local_geometry():
    spaces = all_subspaces(2)
    axes = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    checked = 0
    for first, second in product(spaces, repeat=2):
        aligned = [
            target_index
            for target_index, target in enumerate(axes)
            if all(determinant_rows(left, right, target) == 0
                   for left in first for right in second)
        ]
        if len(aligned) < 2:
            continue
        e, f = aligned[:2]
        missing = ({0, 1, 2} - {e, f}).pop()
        crosses = {cross(left, right) for left in first for right in second}
        if crosses != {(0, 0, 0)}:
            assert all(vector[missing] == 0 for vector in first)
            assert all(vector[missing] == 0 for vector in second)
        checked += 1
    assert checked
    return checked


def matrix_rank_mod2(matrix):
    rows = [list(row) for row in matrix]
    rank = 0
    for column in range(3):
        pivot = next((row for row in range(rank, 3) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(3):
            if row != rank and rows[row][column]:
                rows[row] = [left ^ right for left, right in zip(rows[row], rows[rank])]
        rank += 1
    return rank


def outer_has_off_diagonal(left, right):
    return any(left[i] * right[j] for i in range(3) for j in range(3) if i != j)


def audit_selector_lemma():
    spaces = all_subspaces(2)
    nonzero_vectors = vectors(2)[1:]
    invertible = [matrix for entries in product(range(2), repeat=9)
                  for matrix in [[entries[0:3], entries[3:6], entries[6:9]]]
                  if matrix_rank_mod2(matrix) == 3]
    checked = 0
    # Common-line total-wedge sites have both kernel dimensions at least two.
    for first_kernel, second_kernel, direct in product(spaces, spaces, invertible):
        if dimension(first_kernel) < 2 or dimension(second_kernel) < 2:
            continue
        witnesses = [
            (left, right)
            for left in first_kernel if left != (0, 0, 0)
            for right in second_kernel if right != (0, 0, 0)
            if dot(left, direct, right, 2) == 0
            and outer_has_off_diagonal(left, right)
        ]
        assert witnesses, (first_kernel, second_kernel, direct)
        checked += 1

    # If one image is zero and the other map is singular, use its kernel.
    for first_kernel, direct in product(spaces, invertible):
        if dimension(first_kernel) < 1:
            continue
        witnesses = [
            (left, right)
            for left in first_kernel if left != (0, 0, 0)
            for right in nonzero_vectors
            if dot(left, direct, right, 2) == 0
            and outer_has_off_diagonal(left, right)
        ]
        assert witnesses
        checked += 1

    # In the full-rank/zero case, any chosen preimage of a coordinate axis
    # has a two-dimensional isotropic set containing an off-diagonal choice.
    for left, direct in product(nonzero_vectors, invertible):
        witnesses = [right for right in nonzero_vectors
                     if dot(left, direct, right, 2) == 0
                     and outer_has_off_diagonal(left, right)]
        assert witnesses
        checked += 1
    return checked


def audit_incidence_count():
    checked = 0
    for low_rank_count in range(7):
        for coordinate_plane_count in range(7 - low_rank_count):
            if 2 * low_rank_count + coordinate_plane_count < 3:
                continue
            assert low_rank_count + coordinate_plane_count >= 2
            # Only the single cross site can be outside the five-site overlap.
            assert low_rank_count + coordinate_plane_count - 1 >= 1
            checked += 1
    return checked


def audit_nonzero_colon_example():
    # A concrete nonzero member of Ann_3(lambda) on four square-zero sites.
    spoke = linear((1, 1, 0, 0))
    colon = {(0, 1, 2): F(1)}
    assert colon
    assert not multiply(spoke, colon)


def main():
    audit_physical_channel_formula()
    audit_contracted_formula()
    geometry_cases = audit_local_geometry()
    selector_cases = audit_selector_lemma()
    incidence_counts = audit_incidence_count()
    audit_nonzero_colon_example()
    print("invertible complete-anchor one-hole filtered descent: PASS")
    print(f"  local subspace pairs audited: {geometry_cases}")
    print(f"  isotropic selector cases audited: {selector_cases}")
    print(f"  incidence count pairs audited: {incidence_counts}")
    print("  pure-sandwich refinement and contracted overlap: PASS")
    print("  coincident selected-curvature routing: PASS")
    print("  explicit nonzero four-site colon representative: PASS")


if __name__ == "__main__":
    main()
