#!/usr/bin/env python3
"""Exact guard for the fixed-dark-plane scalar one-site jet.

The complement-plane scalar provenance class is already closed.  This
checker audits the remaining blocker incidence and gives a rational packet
on the fixed dark plane which satisfies

* the rank-(1,1) scalar-shore factorization and injective endpoint stars;
* one literal coordinate plane on the dark shore;
* a rank-three diagonal map on the four-dimensional clean cap plane;
* the full nine one-site rows after one genuine two-site contraction; and
* the consecutive-power identities E=i_y i_z q^[2], F=i_y i_z q^[3].

Nevertheless the unique target-free cap has nonzero physical response.
Thus one-site compatibility cannot close this branch; a simultaneous
two-site/full-overlap statement is genuinely necessary.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product


Q = Fraction
EMPTY = -1
N_SITES = 6
B = (0, 1, 2)
X, Y, Z = (3, 4, 5)
EXPECTED_DIGEST = "44ce6b13ef9cd36a95aeb963bf812bb183996c5125436d98ba8779bbd7243e24"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(*elements):
    out = {}
    for element in elements:
        for word, coefficient in element.items():
            out[word] = out.get(word, Q(0)) + coefficient
            if not out[word]:
                del out[word]
    return out


def scale(coefficient, element):
    return {word: coefficient * value for word, value in element.items()
            if coefficient * value}


def multiply(left, right):
    out = {}
    for u, a in left.items():
        for v, b in right.items():
            if any(u[site] != EMPTY and v[site] != EMPTY
                   for site in range(N_SITES)):
                continue
            word = tuple(u[site] if u[site] != EMPTY else v[site]
                         for site in range(N_SITES))
            out[word] = out.get(word, Q(0)) + a * b
            if not out[word]:
                del out[word]
    return out


def power(element, exponent):
    out = {tuple([EMPTY] * N_SITES): Q(1)}
    for _ in range(exponent):
        out = multiply(out, element)
    return out


def factorial(n):
    out = 1
    for value in range(2, n + 1):
        out *= value
    return out


def divided_power(element, exponent):
    return scale(Q(1, factorial(exponent)), power(element, exponent))


def atom(site, colour, coefficient=Q(1)):
    word = [EMPTY] * N_SITES
    word[site] = colour
    return {tuple(word): Q(coefficient)}


def linear(terms):
    return add(*(atom(site, colour, coefficient)
                 for site, colour, coefficient in terms))


def pure(sites, colour):
    out = {tuple([EMPTY] * N_SITES): Q(1)}
    for site in sites:
        out = multiply(out, atom(site, colour))
    return out


def contract(element, assignments):
    out = {}
    for word, coefficient in element.items():
        if any(word[site] != colour for site, colour in assignments.items()):
            continue
        reduced = list(word)
        for site in assignments:
            reduced[site] = EMPTY
        reduced = tuple(reduced)
        out[reduced] = out.get(reduced, Q(0)) + coefficient
    return {word: coefficient for word, coefficient in out.items()
            if coefficient}


def vector(element, words):
    return [element.get(word, Q(0)) for word in words]


def rank(vectors):
    if not vectors:
        return 0
    matrix = [list(row) for row in vectors]
    rows = len(matrix)
    columns = len(matrix[0])
    pivot = 0
    for column in range(columns):
        chosen = next((row for row in range(pivot, rows)
                       if matrix[row][column]), None)
        if chosen is None:
            continue
        matrix[pivot], matrix[chosen] = matrix[chosen], matrix[pivot]
        value = matrix[pivot][column]
        matrix[pivot] = [entry / value for entry in matrix[pivot]]
        for row in range(rows):
            if row == pivot or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * base
                           for entry, base in zip(matrix[row], matrix[pivot])]
        pivot += 1
        if pivot == rows:
            break
    return pivot


def element_rank(elements):
    words = sorted(set().union(*(element.keys() for element in elements)))
    return rank([vector(element, words) for element in elements])


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Q(0))


def outer(left, right):
    return tuple(tuple(a * b for b in right) for a in left)


def matrix_add(terms):
    return tuple(tuple(sum((coefficient * matrix[i][j]
                            for coefficient, matrix in terms), Q(0))
                       for j in range(3)) for i in range(3))


def matrix_pair(left, right):
    return sum((left[i][j] * right[i][j]
                for i in range(3) for j in range(3)), Q(0))


def permute_mask(mask, permutation):
    return sum(1 << permutation[site] for site in range(3)
               if mask & (1 << site))


def blocker_canonical(blockers):
    perms = tuple(permutations(range(3)))
    return min(tuple(permute_mask(blockers[colour_permutation[colour]],
                                  site_permutation)
                     for colour in range(3))
               for site_permutation in perms
               for colour_permutation in perms)


def blocker_audit():
    """Classify the fixed-plane ledgers left by the complement closure."""
    counts = Counter()
    for blockers in product(range(8), repeat=3):
        local_degrees = [sum(bool(mask & (1 << site)) for mask in blockers)
                         for site in range(3)]
        # Some dark site is a coordinate plane, no site contains all axes.
        if max(local_degrees) != 2:
            continue
        # The complement-plane theorem closed every release with two live
        # labels.  A label is live after releasing x exactly when Z_c is
        # empty or the singleton {x}.
        if any(sum(mask in (0, 1 << site) for mask in blockers) > 1
               for site in range(3)):
            continue
        counts[blocker_canonical(blockers)] += 1

    expected = {
        (0, 3, 3): 9,
        (0, 3, 5): 18,
        (0, 3, 7): 18,
        (0, 7, 7): 3,
        (1, 2, 3): 18,
        (1, 2, 5): 36,
        (1, 2, 7): 18,
        (1, 3, 6): 36,
        (1, 6, 6): 9,
        (1, 6, 7): 18,
        (3, 5, 6): 6,
    }
    require(dict(counts) == expected, ("blocker orbit census changed", counts))
    require(sum(counts.values()) == 189, "wrong labelled blocker count")
    return tuple(sorted(counts.items()))


def guard_audit():
    # Dark-shore coefficient vectors and local fields.  At X the two fields
    # span Pi_0=<e_1,e_2>; at Y and Z they are the single blocker lines.
    lam = (Q(1), Q(1), Q(-1))
    mu = (Q(1), Q(-1), Q(-1))
    u_shore = add(atom(X, 1), atom(Y, 1), atom(Z, 2))
    v_shore = add(atom(X, 2), atom(Y, 1), atom(Z, 2))

    # The induced blocker orbit is (empty,{X,Y},{X,Z}), canonical (0,3,5).
    local_spans = {
        X: ({1, 2}),
        Y: ({1}),
        Z: ({2}),
    }
    blockers = tuple(sum(1 << (site - X) for site in (X, Y, Z)
                             if colour in local_spans[site])
                     for colour in range(3))
    require(blockers == (0, 3, 5), ("wrong guard blocker orbit", blockers))

    # Two two-dimensional annihilator bases.  Their coordinate restrictions
    # are a0=(1,0),a1=(0,1),a2=(1,1) and
    # b0=(1,1),b1=(1,0),b2=(0,1).
    h = ((Q(1), Q(0), Q(1)), (Q(0), Q(1), Q(1)))
    g = ((Q(1), Q(1), Q(0)), (Q(1), Q(0), Q(1)))
    require(all(dot(lam, value) == 0 for value in h), "bad left annihilator")
    require(all(dot(mu, value) == 0 for value in g), "bad right annihilator")

    # Exact rational one-site response guard on B.
    l0 = linear(((0, 0, 1), (1, 2, 1), (2, 1, 1)))
    l1 = linear(((1, 2, 1), (2, 0, 1)))
    m0 = linear(((1, 1, 1), (1, 2, 1), (2, 0, 1)))
    m1 = atom(1, 0)
    t = linear(((1, 0, 1), (1, 1, -1), (1, 2, -1), (2, 0, 1)))
    p_b = (l0, l1, {})
    s_b = ({}, m0, m1)

    # Full endpoint maps are injective.  On the annihilator bases they give
    # precisely L0,L1 and M0,M1.
    p = tuple(add(p_b[i], scale(lam[i], u_shore)) for i in range(3))
    s = tuple(add(s_b[i], scale(mu[i], v_shore)) for i in range(3))
    require(element_rank(p) == 3 and element_rank(s) == 3,
            "endpoint star lost injectivity")
    require(add(*(scale(h[0][i], p_b[i]) for i in range(3))) == l0,
            "left basis-0 response mismatch")
    require(add(*(scale(h[1][i], p_b[i]) for i in range(3))) == l1,
            "left basis-1 response mismatch")
    require(add(*(scale(g[0][i], s_b[i]) for i in range(3))) == m0,
            "right basis-0 response mismatch")
    require(add(*(scale(g[1][i], s_b[i]) for i in range(3))) == m1,
            "right basis-1 response mismatch")

    responses = tuple(multiply(left, right)
                      for left in (l0, l1) for right in (m0, m1))
    require(element_rank(responses) == 4, "response family is not four-dimensional")
    target_b = pure(B, 0)
    images = tuple(multiply(response, t) for response in responses)
    require(images == (target_b, target_b, {}, {}),
            ("one-site response image changed", images))

    # Direct matrix a=e_0 mu^T annihilates the clean cap plane.
    direct = ((Q(1), Q(-1), Q(-1)),
              (Q(0), Q(0), Q(0)),
              (Q(0), Q(0), Q(0)))
    cap_basis = tuple(outer(left, right) for left in h for right in g)
    require(all(matrix_pair(direct, cap) == 0 for cap in cap_basis),
            "direct scalar does not vanish on the cap plane")
    diagonals = tuple(tuple(cap[i][i] for i in range(3))
                      for cap in cap_basis)
    require(rank([list(column) for column in zip(*diagonals)]) == 3,
            "diagonal map is not rank three")

    # The unique diagonal-zero cap has a nonzero response but its one-site
    # image vanishes.
    kernel_coefficients = (Q(-1), Q(1), Q(0), Q(-1))
    k_star = matrix_add(tuple(zip(kernel_coefficients, cap_basis)))
    require(tuple(k_star[i][i] for i in range(3)) == (0, 0, 0),
            "target-free cap has a diagonal residue")
    r_star = add(*(scale(coefficient, response)
                   for coefficient, response in zip(kernel_coefficients, responses)))
    require(r_star, "target-free physical response vanished")
    require(multiply(r_star, t) == {},
            "target-free response is visible in the one-site jet")

    # Build one actual six-site q.  Contracting Y,Z in q^[2],q^[3] gives
    # E=e_0^X t and F=e_0^X X_0^B exactly.
    q_c = multiply(l0, m1)
    q = add(q_c, multiply(atom(Y, 0), atom(X, 0)),
            multiply(atom(Z, 0), t))
    e_x = contract(divided_power(q, 2), {Y: 0, Z: 0})
    f_x = contract(divided_power(q, 3), {Y: 0, Z: 0})
    expected_e = multiply(atom(X, 0), t)
    expected_f = multiply(atom(X, 0), target_b)
    require(e_x == expected_e, ("second cofactor mismatch", e_x))
    require(f_x == expected_f, ("third cofactor mismatch", f_x))

    # The complete nine one-site rows.  Since E uses X, the local shore
    # pieces collide and the response is the B-part used above.
    p_c = tuple(add(p_b[i], scale(lam[i], atom(X, 1))) for i in range(3))
    s_c = tuple(add(s_b[i], scale(mu[i], atom(X, 2))) for i in range(3))
    target_c = pure(B + (X,), 0)
    row_count = 0
    for i in range(3):
        for j in range(3):
            lhs = add(scale(direct[i][j], f_x),
                      multiply(multiply(p_c[i], s_c[j]), e_x))
            rhs = target_c if i == j == 0 else {}
            require(lhs == rhs, ("one-site row failed", i, j, lhs, rhs))
            row_count += 1

    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    full_targets = tuple(pure(tuple(range(N_SITES)), colour)
                         for colour in range(3))

    def contracted_residuals(assignments):
        residuals = []
        for i in range(3):
            for j in range(3):
                source = add(scale(direct[i][j], q3),
                             multiply(multiply(p[i], s[j]), q2))
                lhs = contract(source, assignments)
                rhs = contract(full_targets[i], assignments) if i == j else {}
                residual = add(lhs, scale(Q(-1), rhs))
                if residual:
                    residuals.append((i, j, residual))
        return residuals

    # A second, distinct complete one-site contraction also passes.  The
    # third does not, and the first joint five-site contraction (leave X,Y
    # visible, contract only Z) detects all nine rows.  This is the exact
    # boundary between separate one-site data and simultaneous two-site
    # compatibility.
    release_x = contracted_residuals({Y: 0, Z: 0})
    release_y = contracted_residuals({X: 0, Z: 0})
    release_z = contracted_residuals({X: 0, Y: 0})
    joint_xy = contracted_residuals({Z: 0})
    require(not release_x and not release_y,
            ("a certified one-site release failed", release_x, release_y))
    require(tuple((i, j, len(residual)) for i, j, residual in release_z) ==
            ((0, 0, 1), (0, 1, 2), (0, 2, 1),
             (1, 0, 1), (1, 2, 1), (2, 1, 1)),
            ("third-release boundary changed", release_z))
    require(len(joint_xy) == 9 and
            all(len(residual) == 2 for _, _, residual in joint_xy),
            ("joint two-site boundary changed", joint_xy))

    # The joint failure is one scalar-shore normal class.  Its response-label
    # matrix is exactly lambda mu^T, so every cap in Q annihilates it.  The
    # target-free cap also satisfies the joint cap-contracted equation
    # R_* E_xy=0.  Only the individually labelled rows see this obstruction.
    normal_word = multiply(
        target_b,
        add(multiply(atom(X, 1), atom(Y, 1)),
            multiply(atom(X, 2), atom(Y, 1))),
    )
    for i, j, residual in joint_xy:
        require(residual == scale(lam[i] * mu[j], normal_word),
                ("joint residual lost lambda-mu factorization", i, j, residual))
    cap_weighted_joint = add(*(scale(k_star[i][j], residual)
                               for i, j, residual in joint_xy))
    require(cap_weighted_joint == {},
            ("target-free cap sees the labelled joint residual",
             cap_weighted_joint))
    e_xy = contract(q2, {Z: 0})
    require(multiply(r_star, e_xy) == {},
            "target-free response fails the joint cap equation")

    # The complete fully-dark cofactor map on this blocker orbit has domain
    # K_X tensor K_Y tensor K_Z of dimension 1*2*2=4.  It attains the sharp
    # rank-one factorization boundary: E_A and beta_A have the same kernel.
    # Thus the carrier identities below do not already manufacture the
    # kernel/target separation required by the dark-shore theorem.
    dark_thetas = tuple((0, y_colour, z_colour)
                        for y_colour in (0, 2)
                        for z_colour in (0, 1))
    dark_e = tuple(contract(q2, {X: theta[0], Y: theta[1], Z: theta[2]})
                   for theta in dark_thetas)
    dark_f = tuple(contract(q3, {X: theta[0], Y: theta[1], Z: theta[2]})
                   for theta in dark_thetas)
    dark_beta = tuple((Q(1), Q(0), Q(0)) if theta == (0, 0, 0)
                      else (Q(0), Q(0), Q(0))
                      for theta in dark_thetas)
    require((element_rank(dark_e), element_rank(dark_f), rank(dark_beta)) ==
            (1, 1, 1), "the fully-dark rank boundary changed")
    require(tuple(bool(value) for value in dark_e) ==
            tuple(any(value) for value in dark_beta) ==
            (True, False, False, False),
            "E_A and beta_A stopped having the same kernel")

    # Audit the full contracted source-row residual on Q.  This is linear
    # in K and must not be confused with the canonical N=8 clean error,
    # which is cubic in the effective response when the direct scalar is
    # zero.
    full_cap_responses = []
    full_cap_errors = []
    for cap in cap_basis:
        response = add(*(scale(cap[i][j], multiply(p[i], s[j]))
                         for i in range(3) for j in range(3)))
        error = multiply(response, q2)
        for i in range(3):
            error = add(error, scale(-cap[i][i], full_targets[i]))
        full_cap_responses.append(response)
        full_cap_errors.append(error)
    require(element_rank(full_cap_errors) == 2,
            "the full cap-row residual kernel changed dimension")
    require(full_cap_errors[0] == {},
            "the unary cap-row residual stopped vanishing")
    require(add(full_cap_errors[1], scale(-1, full_cap_errors[3])) == {},
            "the target-free cap-row residual stopped vanishing")
    unary_cap = cap_basis[0]
    require(tuple(unary_cap[i][i] for i in range(3)) == (1, 0, 0),
            "the unary cap diagonal changed")
    require(all(matrix_pair(direct, cap) == 0 for cap in cap_basis),
            "the cap plane acquired a direct scalar")

    # The actual homogeneous clean error at h=3 is
    # s R^[2] q + R^[3].  Here s=0 on Q, so it is R^[3].
    full_clean_cubics = [divided_power(response, 3)
                         for response in full_cap_responses]
    unary_clean_error = full_clean_cubics[0]
    k_star_response = add(
        scale(-1, full_cap_responses[0]),
        full_cap_responses[1],
        scale(-1, full_cap_responses[3]),
    )
    k_star_clean_error = divided_power(k_star_response, 3)
    clean_cubic_polarizations = []
    clean_cubic_support = []
    for indices in combinations_with_replacement(range(len(cap_basis)), 3):
        value = multiply(
            multiply(full_cap_responses[indices[0]],
                     full_cap_responses[indices[1]]),
            full_cap_responses[indices[2]],
        )
        clean_cubic_polarizations.append(value)
        if value:
            clean_cubic_support.append(indices)
    unary_square_k_star = multiply(
        multiply(full_cap_responses[0], full_cap_responses[0]),
        k_star_response,
    )
    unary_k_star_square = multiply(
        full_cap_responses[0],
        multiply(k_star_response, k_star_response),
    )
    require(element_rank(clean_cubic_polarizations) == 0,
            "the cap plane stopped being canonically clean")
    require(not clean_cubic_support,
            "a polarized cubic clean error appeared on the cap plane")

    return {
        "blockers": blockers,
        "endpoint_ranks": (element_rank(p), element_rank(s)),
        "response_rank": element_rank(responses),
        "diagonal_rank": 3,
        "one_site_image_rank": element_rank(images),
        "target_free_response_terms": len(r_star),
        "q_terms": len(q),
        "E_terms": len(e_x),
        "F_terms": len(f_x),
        "rows": row_count,
        "separate_one_site_rows": 18,
        "third_release_failures": len(release_z),
        "joint_two_site_failures": len(joint_xy),
        "joint_normal_terms": len(normal_word),
        "joint_cap_residual_terms": len(cap_weighted_joint),
        "dark_domain_dimension": len(dark_thetas),
        "dark_E_rank": element_rank(dark_e),
        "dark_beta_rank": rank(dark_beta),
        "dark_kernel_dimension": len(dark_thetas) - element_rank(dark_e),
        "cap_row_residual_rank": element_rank(full_cap_errors),
        "cap_row_residual_kernel_dimension": len(cap_basis) -
        element_rank(full_cap_errors),
        "unary_clean_error_terms": len(unary_clean_error),
        "target_free_clean_error_terms": len(k_star_clean_error),
        "basis_clean_cubic_rank": element_rank(full_clean_cubics),
        "polarized_clean_cubic_rank": element_rank(clean_cubic_polarizations),
        "polarized_clean_cubic_nonzero": len(clean_cubic_support),
        "clean_pencil_mixed_terms": (
            len(unary_square_k_star), len(unary_k_star_square)),
        "canonical_clean_plane_vector_dimension": len(cap_basis),
        "canonical_clean_plane_projective_dimension": len(cap_basis) - 1,
    }


def main():
    blocker_records = blocker_audit()
    guard = guard_audit()
    ledger = (blocker_records, tuple(sorted(guard.items())))
    digest = sha256(repr(ledger).encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest))
    print("N=8 rank-(1,1) scalar fixed-dark-plane one-site guard: passed")
    print(f"  labelled/orbit blocker ledgers : 189 / {len(blocker_records)}")
    print(f"  blocker orbit sizes            : {[count for _, count in blocker_records]}")
    print(f"  response/diagonal/image ranks  : {guard['response_rank']} / "
          f"{guard['diagonal_rank']} / {guard['one_site_image_rank']}")
    print(f"  genuine q/E/F terms            : {guard['q_terms']} / "
          f"{guard['E_terms']} / {guard['F_terms']}")
    print(f"  full one-site rows             : {guard['rows']} / 9")
    print(f"  two separate one-site rows     : {guard['separate_one_site_rows']} / 18")
    print(f"  third/joint residual rows      : {guard['third_release_failures']} / "
          f"{guard['joint_two_site_failures']}")
    print(f"  joint normal/cap residual terms: {guard['joint_normal_terms']} / "
          f"{guard['joint_cap_residual_terms']}")
    print(f"  dark domain/E/beta/kernel dims  : "
          f"{guard['dark_domain_dimension']} / {guard['dark_E_rank']} / "
          f"{guard['dark_beta_rank']} / {guard['dark_kernel_dimension']}")
    print(f"  cap-row residual rank/kernel    : "
          f"{guard['cap_row_residual_rank']} / "
          f"{guard['cap_row_residual_kernel_dimension']}")
    print(f"  clean cubic unary/K*/basis rank : "
          f"{guard['unary_clean_error_terms']} / "
          f"{guard['target_free_clean_error_terms']} / "
          f"{guard['basis_clean_cubic_rank']}")
    print(f"  polarized rank/nonzero/pencil   : "
          f"{guard['polarized_clean_cubic_rank']} / "
          f"{guard['polarized_clean_cubic_nonzero']} / "
          f"{guard['clean_pencil_mixed_terms']}")
    print(f"  inactive clean plane vector/P   : "
          f"{guard['canonical_clean_plane_vector_dimension']} / "
          f"{guard['canonical_clean_plane_projective_dimension']}")
    print(f"  target-free response terms     : {guard['target_free_response_terms']}")
    print(f"  ledger sha256                  : {digest}")


if __name__ == "__main__":
    main()
