#!/usr/bin/env python3
"""Exact audits for the arbitrary-common-annihilator contraction.

The script has two purposes.

* It tests the no-, one-, and two-hole matching decompositions when the
  annihilators are allowed to vary in a two-plane (rather than being fixed
  to the cross product).
* It checks the six-site equality consequences for an invertible deleted
  edge.  In particular it rejects the K8 witness-incidence model and
  verifies a sharp local countermodel to the three same-color pure-cofactor
  equations.

All calculations are over Q or exact polynomial rings over Q.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

from verify_witness_incidence_k8_countermodel import (
    K,
    LABEL,
    PAIRS,
    oriented as incidence_block,
    perfect_matchings,
)


E = tuple(sp.eye(3)[:, r] for r in range(3))
ZERO = sp.zeros(3, 3)


def scalar_hafnian(vertices, covectors, block):
    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        for u, v in matching:
            term *= (covectors[u].T * block(u, v) * covectors[v])[0]
        total += term
    return sp.expand(total)


def one_site_partial(vertices, hole, covectors, block):
    out = sp.zeros(3, 1)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        vector = None
        for u, v in matching:
            matrix = block(u, v)
            if u == hole:
                vector = matrix * covectors[v]
            elif v == hole:
                vector = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        out += term * vector
    return out.applyfunc(sp.expand)


def two_site_partial(vertices, w, z, covectors, block):
    out = sp.zeros(3, 3)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        vector_w = None
        vector_z = None
        direct = None
        for u, v in matching:
            matrix = block(u, v)
            if {u, v} == {w, z}:
                direct = matrix if (u, v) == (w, z) else matrix.T
            elif u == w:
                vector_w = matrix * covectors[v]
            elif v == w:
                vector_w = matrix.T * covectors[u]
            elif u == z:
                vector_z = matrix * covectors[v]
            elif v == z:
                vector_z = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        out += term * (direct if direct is not None else vector_w * vector_z.T)
    return out.applyfunc(sp.expand)


def matching_tensor(vertices, block):
    """Return the exact coefficient dictionary of a small matching tensor."""

    vertices = tuple(sorted(vertices))
    out = {}
    for colors in product(range(3), repeat=len(vertices)):
        color = dict(zip(vertices, colors))
        coefficient = sp.Integer(0)
        for matching in perfect_matchings(vertices):
            term = sp.Integer(1)
            for u, v in matching:
                term *= block(u, v)[color[u], color[v]]
            coefficient += term
        coefficient = sp.simplify(coefficient)
        if coefficient != 0:
            out[colors] = coefficient
    return out


def proportional(left, right):
    ratio = None
    for x, y in zip(left, right):
        if y == 0:
            if x != 0:
                return False
            continue
        candidate = sp.simplify(x / y)
        if ratio is None:
            ratio = candidate
        elif sp.simplify(candidate - ratio) != 0:
            return False
    return ratio is not None


def restricted_four_cofactor(block, vertices, labels):
    """Restrict H_vertices to the coordinate planes e_label^perp."""

    vertices = tuple(sorted(vertices))
    tensor = matching_tensor(vertices, block)
    return {
        colors: coefficient
        for colors, coefficient in tensor.items()
        if all(colors[i] != labels[vertex] for i, vertex in enumerate(vertices))
    }


def audit_incidence_k8():
    """The old K8 model passes cross tests but fails the plane tests."""

    projected_zero = 0
    projected_impure = 0
    projected_pure = 0
    full_equality_failures = 0

    for p, q in PAIRS:
        labels = LABEL[p // 2]
        outside = [u for u in range(8) if u not in (p, q)]

        # Every site is a triple zero-cross witness, and its two blocks have
        # the coordinate common row line prescribed by LABEL.
        for u in outside:
            r = labels[u]
            P = incidence_block(p, u)
            Q = incidence_block(q, u)
            assert all(P * K[c] * Q.T == ZERO for c in range(3))
            assert P[:, [c for c in range(3) if c != r]] == sp.zeros(3, 2)
            assert Q[:, [c for c in range(3) if c != r]] == sp.zeros(3, 2)
            assert P != ZERO or Q != ZERO

        groups = {r: [u for u in outside if labels[u] == r] for r in range(3)}
        assert all(len(groups[r]) == 2 for r in range(3))

        for r in range(3):
            remaining = [u for u in outside if u not in groups[r]]
            restricted = restricted_four_cofactor(
                incidence_block, remaining, labels
            )
            target_key = tuple(r for _ in sorted(remaining))
            if not restricted:
                projected_zero += 1
                full_equality_failures += 1
                continue
            if set(restricted) != {target_key}:
                projected_impure += 1
                full_equality_failures += 1
                continue

            projected_pure += 1
            kappa = restricted[target_key]
            w, z = groups[r]
            a_w = incidence_block(p, w)[:, r]
            a_z = incidence_block(p, z)[:, r]
            b_w = incidence_block(q, w)[:, r]
            b_z = incidence_block(q, z)[:, r]
            star_matrix = a_w * b_z.T + a_z * b_w.T
            compatibility = E[r] * E[r].T - kappa * star_matrix
            if not proportional(compatibility, incidence_block(p, q)):
                full_equality_failures += 1

    assert (projected_zero, projected_impure, projected_pure) == (7, 4, 1)
    assert full_equality_failures == 12
    return projected_zero, projected_impure, projected_pure


P_VERTEX = 6
Q_VERTEX = 7
OUTSIDE_PAIRS = {0: (0, 1), 1: (2, 3), 2: (4, 5)}
OUTSIDE_LABEL = {
    vertex: color for color, pair in OUTSIDE_PAIRS.items() for vertex in pair
}
OUTSIDE_INDEX = {
    vertex: index
    for pair in OUTSIDE_PAIRS.values()
    for index, vertex in enumerate(pair)
}


def make_local_blocks():
    """A rational local model satisfying all three pure-cofactor equations."""

    blocks = {}

    def put(u, v, value):
        if u < v:
            blocks[u, v] = value
        else:
            blocks[v, u] = value.T

    put(P_VERTEX, Q_VERTEX, sp.eye(3))
    for u in range(6):
        r = OUTSIDE_LABEL[u]
        projector = E[r] * E[r].T
        put(P_VERTEX, u, projector)
        put(Q_VERTEX, u, sp.Rational(1, 2) * projector)

    # For each two label classes use the same-index perfect matching, in
    # the third color.  The support is two disjoint triangles, so H_R=0.
    for c, d in combinations(range(3), 2):
        r = 3 - c - d
        for index in range(2):
            u = OUTSIDE_PAIRS[c][index]
            v = OUTSIDE_PAIRS[d][index]
            put(u, v, E[r] * E[r].T)

    def block(u, v):
        if u < v:
            return blocks.get((u, v), ZERO)
        return blocks.get((v, u), ZERO).T

    return block


def symbolic_plane_covectors():
    covectors = {}
    for u in range(6):
        r = OUTSIDE_LABEL[u]
        coordinates = []
        for c in range(3):
            coordinates.append(
                sp.Integer(0) if c == r else sp.Symbol(f"z{u}_{c}")
            )
        covectors[u] = sp.Matrix(coordinates)
    return covectors


def audit_local_model():
    block = make_local_blocks()
    outside = tuple(range(6))

    # Triple-zero stars with a fixed coordinate common row line.
    for u in outside:
        r = OUTSIDE_LABEL[u]
        P = block(P_VERTEX, u)
        Q = block(Q_VERTEX, u)
        assert all(P * K[c] * Q.T == ZERO for c in range(3))
        assert P[:, [c for c in range(3) if c != r]] == sp.zeros(3, 2)
        assert Q[:, [c for c in range(3) if c != r]] == sp.zeros(3, 2)

    # The outside six-site matching tensor is identically zero.
    assert matching_tensor(outside, block) == {}

    # All three overlapping projected four-site cofactors are pure, with
    # kappa=1, and their star bilinear forms are exactly E_rr.
    for r in range(3):
        remaining = [u for u in outside if u not in OUTSIDE_PAIRS[r]]
        restricted = restricted_four_cofactor(block, remaining, OUTSIDE_LABEL)
        assert restricted == {tuple(r for _ in sorted(remaining)): sp.Integer(1)}
        w, z = OUTSIDE_PAIRS[r]
        a_w = block(P_VERTEX, w)[:, r]
        a_z = block(P_VERTEX, z)[:, r]
        b_w = block(Q_VERTEX, w)[:, r]
        b_z = block(Q_VERTEX, z)[:, r]
        assert a_w * b_z.T + a_z * b_w.T == E[r] * E[r].T

    alpha = sp.Matrix(sp.symbols("a0:3"))
    beta = sp.Matrix(sp.symbols("b0:3"))
    zeta = symbolic_plane_covectors()
    g = (alpha.T * block(P_VERTEX, Q_VERTEX) * beta)[0]

    # Directly audit the matching decompositions.  This uses genuinely
    # arbitrary vectors in each annihilator plane, not their zero cross
    # products.
    all_covectors = dict(zeta)
    all_covectors[P_VERTEX] = alpha
    all_covectors[Q_VERTEX] = beta
    target_no_hole = sp.expand(
        sum(
            alpha[r] * beta[r] * sp.prod(zeta[u][r] for u in outside)
            for r in range(3)
        )
    )
    assert target_no_hole == 0
    assert scalar_hafnian(range(8), all_covectors, block) == sp.expand(
        g * scalar_hafnian(outside, zeta, block)
    )

    for w in outside:
        target_one_hole = sp.Matrix(
            [
                alpha[r]
                * beta[r]
                * sp.prod(zeta[u][r] for u in outside if u != w)
                for r in range(3)
            ]
        ).applyfunc(sp.expand)
        assert target_one_hole == sp.zeros(3, 1)
        direct = one_site_partial(
            range(8), w, {u: v for u, v in all_covectors.items() if u != w}, block
        )
        quotient = one_site_partial(
            outside, w, {u: zeta[u] for u in outside if u != w}, block
        )
        assert direct == (g * quotient).applyfunc(sp.expand)

    zero_two_hole = 0
    nonzero_two_hole = 0
    representative = None
    for w, z in combinations(outside, 2):
        contracted = [u for u in outside if u not in (w, z)]
        covectors = {u: zeta[u] for u in contracted}
        direct = two_site_partial(
            range(8),
            w,
            z,
            {
                **covectors,
                P_VERTEX: alpha,
                Q_VERTEX: beta,
            },
            block,
        )
        quotient = two_site_partial(outside, w, z, covectors, block)
        assert quotient == ZERO
        h = scalar_hafnian(contracted, covectors, block)
        x_w = block(P_VERTEX, w).T * alpha
        x_z = block(P_VERTEX, z).T * alpha
        y_w = block(Q_VERTEX, w).T * beta
        y_z = block(Q_VERTEX, z).T * beta
        correction = h * (x_w * y_z.T + y_w * x_z.T)
        assert direct == (g * quotient + correction).applyfunc(sp.expand)

        target = sp.diag(
            *[
                alpha[r]
                * beta[r]
                * sp.prod(zeta[u][r] for u in contracted)
                for r in range(3)
            ]
        )
        residual_on_incidence = (target - correction).applyfunc(sp.expand)

        # Same-label holes satisfy the required pure equations.  Cross-label
        # holes of the same index also vanish; opposite-index holes expose
        # exactly the next missing mixed-hole condition.
        if residual_on_incidence == ZERO:
            zero_two_hole += 1
        else:
            nonzero_two_hole += 1
            representative = representative or (w, z, residual_on_incidence)

    assert (zero_two_hole, nonzero_two_hole) == (9, 6)

    # A small exact incidence-point witness for one mixed-hole failure.
    w, z = 0, 3
    contracted = [u for u in outside if u not in (w, z)]
    chosen = {
        1: E[1],  # label 0
        2: E[0],  # label 1
        4: E[0],  # label 2
        5: E[1],  # label 2
    }
    assert scalar_hafnian(contracted, chosen, block) == 1
    alpha0, beta0 = E[0], E[1]
    assert (alpha0.T * beta0)[0] == 0
    x_w = block(P_VERTEX, w).T * alpha0
    x_z = block(P_VERTEX, z).T * alpha0
    y_w = block(Q_VERTEX, w).T * beta0
    y_z = block(Q_VERTEX, z).T * beta0
    assert x_w * y_z.T + y_w * x_z.T == sp.Rational(1, 2) * E[0] * E[1].T

    return zero_two_hole, nonzero_two_hole, representative


def audit_zero_correction_graph():
    """Audit the C6 graph behind the local model's six mixed failures."""

    vertices = [(color, index) for color in range(3) for index in range(2)]
    edges = {
        frozenset(((c, i), (d, j)))
        for c, d in combinations(range(3), 2)
        for i in range(2)
        for j in range(2)
        if i != j
    }
    assert len(edges) == 6
    assert all(
        sum(vertex in edge for edge in edges) == 2 for vertex in vertices
    )

    reached = {vertices[0]}
    while True:
        larger = reached | {
            vertex
            for edge in edges
            if edge & reached
            for vertex in edge
        }
        if larger == reached:
            break
        reached = larger
    assert reached == set(vertices)


def audit_pure_extension_annihilators():
    """Verify the four support cases in the extension-annihilator lemma.

    Work in the squarefree site algebra on four two-dimensional spaces.
    The degree-two element q has one 2-by-2 matrix on every edge.  After
    normalizing the nonzero components of ell to e_0, q*ell=0 is a linear
    system in the 24 edge coefficients.
    """

    sites = tuple(range(4))
    bits = tuple(range(2))
    edges = tuple(combinations(sites, 2))
    q_symbols = {
        (i, j, a, b): sp.Symbol(f"q{i}{j}{a}{b}")
        for i, j in edges
        for a, b in product(bits, repeat=2)
    }
    variables = list(q_symbols.values())

    def q_coefficient(i, j, a, b, entries=q_symbols):
        if i < j:
            return entries[i, j, a, b]
        return entries[j, i, b, a]

    def four_tensor(entries):
        out = {}
        for colors in product(bits, repeat=4):
            value = (
                q_coefficient(0, 1, colors[0], colors[1], entries)
                * q_coefficient(2, 3, colors[2], colors[3], entries)
                + q_coefficient(0, 2, colors[0], colors[2], entries)
                * q_coefficient(1, 3, colors[1], colors[3], entries)
                + q_coefficient(0, 3, colors[0], colors[3], entries)
                * q_coefficient(1, 2, colors[1], colors[2], entries)
            )
            out[colors] = sp.factor(value)
        return out

    nullities = []
    for support_size in range(1, 5):
        equations = []
        for triple in combinations(sites, 3):
            for colors in product(bits, repeat=3):
                color = dict(zip(triple, colors))
                value = sp.Integer(0)
                for i in triple:
                    if i < support_size and color[i] == 0:
                        j, k = (u for u in triple if u != i)
                        value += q_coefficient(j, k, color[j], color[k])
                equations.append(value)

        multiplication = sp.linear_eq_to_matrix(equations, variables)[0]
        basis = multiplication.nullspace()
        nullities.append(len(basis))
        parameters = sp.symbols(f"t{support_size}_0:{len(basis)}")
        generic_solution = [
            sum(parameters[j] * basis[j][i] for j in range(len(basis)))
            for i in range(len(variables))
        ]
        entries = {
            key: sp.expand(generic_solution[i])
            for i, key in enumerate(q_symbols)
        }
        tensor = four_tensor(entries)

        if support_size in (1, 3):
            assert all(value == 0 for value in tensor.values())
        elif support_size == 2:
            # Both supported-site factors are e_0.  The remaining 2-by-2
            # coefficient matrix has rank one, so the other two factors
            # are also pure whenever the tensor is nonzero.
            assert all(
                value == 0
                for colors, value in tensor.items()
                if colors[0] != 0 or colors[1] != 0
            )
            remaining = sp.Matrix(
                2,
                2,
                lambda a, b: tensor[0, 0, a, b],
            )
            assert remaining != sp.zeros(2, 2)
            assert sp.factor(remaining.det()) == 0

            def edge_matrix(i, j):
                return sp.Matrix(
                    2,
                    2,
                    lambda a, b: entries[i, j, a, b],
                )

            # In the support-two normal form the complementary edge is
            # zero and all four edges across support | complement have
            # rank at most one.  These are the facts used by the apex
            # corollary.
            assert edge_matrix(2, 3) == sp.zeros(2, 2)
            assert all(
                sp.factor(edge_matrix(i, j).det()) == 0
                for i in (0, 1)
                for j in (2, 3)
            )
        else:
            assert tensor[0, 0, 0, 0] != 0
            assert all(
                value == 0
                for colors, value in tensor.items()
                if colors != (0, 0, 0, 0)
            )

    assert nullities == [12, 8, 5, 2]

    # If no apex existed in a pure K4, each of the four target-transverse
    # contractions would have support two.  Its unique nonsupport edge is
    # identically zero, so those missing-neighbor choices must be symmetric
    # and form one of the three perfect matchings.  Every other edge would
    # be transverse at both endpoints (rank two), contradicting the
    # support-two rank-one assertion above.
    neighbor_sets = {
        i: tuple(j for j in sites if j != i) for i in sites
    }
    symmetric_missing_patterns = []
    for missing in product(*[neighbor_sets[i] for i in sites]):
        if all(missing[missing[i]] == i for i in sites):
            symmetric_missing_patterns.append(missing)
    assert len(set(symmetric_missing_patterns)) == 3
    for missing in symmetric_missing_patterns:
        for i, j in edges:
            if missing[i] == j:
                assert missing[j] == i
            else:
                assert missing[j] != i

    # Sharpness: a pure matching tensor can have two independent linear
    # annihilators.  This prevents replacing the componentwise conclusion
    # of the lemma by a false one-dimensional-kernel statement.
    zero2 = sp.zeros(2, 2)
    e00 = sp.Matrix([[1, 0], [0, 0]])
    sharp_matrices = {
        (0, 1): zero2,
        (0, 2): -e00,
        (1, 2): e00,
        (0, 3): -e00,
        (1, 3): e00,
        (2, 3): zero2,
    }
    sharp_entries = {
        (i, j, a, b): sharp_matrices[i, j][a, b]
        for i, j in edges
        for a, b in product(bits, repeat=2)
    }
    sharp_tensor = four_tensor(sharp_entries)
    assert sharp_tensor[0, 0, 0, 0] == -2
    assert all(
        value == 0
        for colors, value in sharp_tensor.items()
        if colors != (0, 0, 0, 0)
    )

    linear_columns = tuple(product(sites, bits))
    triple_rows = tuple(
        (triple, colors)
        for triple in combinations(sites, 3)
        for colors in product(bits, repeat=3)
    )
    sharp_map = sp.zeros(len(triple_rows), len(linear_columns))
    for row, (triple, colors) in enumerate(triple_rows):
        color = dict(zip(triple, colors))
        for column, (i, a) in enumerate(linear_columns):
            if i not in triple or color[i] != a:
                continue
            j, k = (u for u in triple if u != i)
            sharp_map[row, column] = q_coefficient(
                j, k, color[j], color[k], sharp_entries
            )
    assert len(sharp_map.nullspace()) == 2

    return tuple(nullities)


def audit_two_plus_four_star_obstruction():
    """Check the two diagonal entries used against a 2+4 graph split."""

    c, d, e = 0, 1, 2
    x_d = sp.Matrix(sp.symbols("xd0:3"))
    y_d = sp.Matrix(sp.symbols("yd0:3"))
    x_e = sp.Matrix(sp.symbols("xe0:3"))
    y_e = sp.Matrix(sp.symbols("ye0:3"))
    kappa_d, kappa_e = sp.symbols("kappa_d kappa_e", nonzero=True)

    # Connectivity of the four-component and its full color-c pair force
    # the star vectors on that component onto C e_c.  Hence the remaining
    # two same-color matrices have support only in row or column c.
    n_d = E[c] * x_d.T + y_d * E[c].T
    n_e = E[c] * x_e.T + y_e * E[c].T
    m_d = E[d] * E[d].T - kappa_d * n_d
    m_e = E[e] * E[e].T - kappa_e * n_e
    assert (m_d[d, d], m_d[e, e]) == (1, 0)
    assert (m_e[d, d], m_e[e, e]) == (0, 1)

    # If m_d=lambda_d*A and m_e=lambda_e*A for the same invertible A,
    # both lambdas are nonzero and these two coordinate pairs would be
    # proportional.  Their exact 2-by-2 determinant is instead one.
    diagonal_minor = sp.Matrix(
        [[m_d[d, d], m_d[e, e]], [m_e[d, d], m_e[e, e]]]
    ).det()
    assert diagonal_minor == 1


def audit_disconnected_apex_propagation():
    """Exhaust target-apex choices for the remaining disconnected cuts.

    A state records zero edges and endpoint lines forced by pure-K4
    apices.  On a zero K4, if two edges at one vertex have the same forced
    endpoint line L, quotienting that vertex by L leaves a pure tensor
    product.  Hence either the third edge has endpoint line L or the
    opposite edge is zero.  Branching on this exact disjunction closes all
    apex placements.
    """

    vertices = tuple(range(6))
    labels = {u: u // 2 for u in vertices}
    pairs = {r: (2 * r, 2 * r + 1) for r in range(3)}
    left = {0, 2, 4}
    right = {1, 3, 5}
    pure_sets = {
        r: tuple(sorted(set(vertices) - set(pairs[r]))) for r in range(3)
    }
    transversal_zero_sets = tuple(
        tuple(sorted(set(vertices) - {u, v}))
        for u in sorted(left)
        for v in sorted(right)
        if labels[u] != labels[v]
    )
    assert transversal_zero_sets == (
        (1, 2, 4, 5),
        (1, 2, 3, 4),
        (0, 3, 4, 5),
        (0, 1, 3, 4),
        (0, 2, 3, 5),
        (0, 1, 2, 5),
    )

    def edge(u, v):
        return tuple(sorted((u, v)))

    def four_matchings(four_set):
        a, b, c, d = four_set
        return (
            ((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        )

    # state = (frozenset(zero edges), sorted tuple of
    #          (((edge), endpoint), forced global color))
    empty_state = (frozenset(), tuple())

    def force_zero(state, chosen_edge):
        zeros, factors_tuple = state
        chosen_edge = edge(*chosen_edge)
        zeros = set(zeros)
        zeros.add(chosen_edge)
        factors = {
            key: value
            for key, value in dict(factors_tuple).items()
            if key[0] != chosen_edge
        }
        return frozenset(zeros), tuple(sorted(factors.items()))

    def force_factor(state, chosen_edge, endpoint, color):
        zeros, factors_tuple = state
        chosen_edge = edge(*chosen_edge)
        if chosen_edge in zeros:
            return state
        factors = dict(factors_tuple)
        key = (chosen_edge, endpoint)
        if key in factors and factors[key] != color:
            return force_zero(state, chosen_edge)
        factors[key] = color
        return zeros, tuple(sorted(factors.items()))

    def has_factor(state, chosen_edge, endpoint, color):
        zeros, factors_tuple = state
        chosen_edge = edge(*chosen_edge)
        return chosen_edge in zeros or dict(factors_tuple).get(
            (chosen_edge, endpoint)
        ) == color

    def impossible_pure_colors(state):
        zeros, factors_tuple = state
        factors = dict(factors_tuple)
        impossible = []
        for color, four_set in pure_sets.items():
            matching_survives = False
            for matching in four_matchings(four_set):
                survives = True
                for endpoints in matching:
                    chosen_edge = edge(*endpoints)
                    if chosen_edge in zeros:
                        survives = False
                        break
                    for endpoint in chosen_edge:
                        forced = factors.get((chosen_edge, endpoint))
                        if forced is not None and forced != color:
                            survives = False
                            break
                if survives:
                    matching_survives = True
                    break
            if not matching_survives:
                impossible.append(color)
        return tuple(impossible)

    def next_quotient_clause(state, zero_sets):
        for four_set in zero_sets:
            for endpoint in four_set:
                others = [u for u in four_set if u != endpoint]
                for color in range(3):
                    if color == labels[endpoint]:
                        continue
                    factored = [
                        u
                        for u in others
                        if has_factor(state, (endpoint, u), endpoint, color)
                    ]
                    for pair in combinations(factored, 2):
                        remaining = [u for u in others if u not in pair]
                        if len(remaining) != 1:
                            continue
                        third = remaining[0]
                        opposite = edge(*pair)
                        if (
                            not has_factor(
                                state, (endpoint, third), endpoint, color
                            )
                            and opposite not in state[0]
                        ):
                            return (
                                edge(endpoint, third),
                                endpoint,
                                color,
                                opposite,
                            )
        return None

    def initial_state(apices):
        state = empty_state
        for color, apex in enumerate(apices):
            for neighbor in pure_sets[color]:
                if neighbor != apex:
                    state = force_factor(
                        state, (apex, neighbor), apex, color
                    )
        return state

    def closes(state, zero_sets, memo):
        if impossible_pure_colors(state):
            return True
        if state in memo:
            return memo[state]
        clause = next_quotient_clause(state, zero_sets)
        if clause is None:
            memo[state] = False
            return False
        chosen_edge, endpoint, color, opposite = clause
        left_branch = force_factor(state, chosen_edge, endpoint, color)
        right_branch = force_zero(state, opposite)
        answer = closes(left_branch, zero_sets, memo) and closes(
            right_branch, zero_sets, memo
        )
        memo[state] = answer
        return answer

    apex_assignments = tuple(product(*(pure_sets[r] for r in range(3))))
    assert len(apex_assignments) == 64
    assert all(
        closes(initial_state(apices), transversal_zero_sets, {})
        for apices in apex_assignments
    )

    # The 64 placements have six orbits under class permutations and the
    # global swap of the two transversal components.  Record their small
    # representatives as an independently checkable coverage certificate.
    encoded_assignments = tuple(
        tuple((labels[u], u % 2) for u in apices)
        for apices in apex_assignments
    )

    def transform(encoded, permutation, flip):
        transformed = [None] * 3
        for color, (apex_class, index) in enumerate(encoded):
            transformed[permutation[color]] = (
                permutation[apex_class],
                index ^ flip,
            )
        return tuple(transformed)

    unseen = set(encoded_assignments)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform(representative, permutation, flip)
            for permutation in permutations(range(3))
            for flip in range(2)
        } & set(encoded_assignments)
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    assert [len(orbit) for orbit in orbits] == [12, 12, 12, 12, 4, 12]
    assert [orbit[0] for orbit in orbits] == [
        ((1, 0), (0, 0), (0, 0)),
        ((1, 0), (0, 0), (0, 1)),
        ((1, 0), (0, 1), (0, 0)),
        ((1, 0), (0, 1), (0, 1)),
        ((1, 0), (2, 0), (0, 0)),
        ((1, 0), (2, 0), (0, 1)),
    ]

    def proof_tree_size(state, zero_sets, depth=0):
        if impossible_pure_colors(state):
            return 1, depth
        clause = next_quotient_clause(state, zero_sets)
        assert clause is not None
        chosen_edge, endpoint, color, opposite = clause
        left_leaves, left_depth = proof_tree_size(
            force_factor(state, chosen_edge, endpoint, color),
            zero_sets,
            depth + 1,
        )
        right_leaves, right_depth = proof_tree_size(
            force_zero(state, opposite), zero_sets, depth + 1
        )
        return left_leaves + right_leaves, max(left_depth, right_depth)

    representative_vertices = [
        tuple(2 * apex_class + index for apex_class, index in orbit[0])
        for orbit in orbits
    ]
    proof_sizes = tuple(
        proof_tree_size(initial_state(apices), transversal_zero_sets)
        for apices in representative_vertices
    )
    assert proof_sizes == (
        (38, 11),
        (127, 15),
        (31, 12),
        (27, 10),
        (29, 10),
        (59, 12),
    )

    mixed_edges = {
        edge(u, v)
        for u, v in combinations(vertices, 2)
        if labels[u] != labels[v]
    }

    # The other 3+3 orbit has a full class in each component.  With
    # components {0,1,2} and {3,4,5}, the eight cross-component mixed
    # pairs have zero cofactors.
    nontransversal_component_edges = {
        edge(0, 2),
        edge(1, 2),
        edge(3, 4),
        edge(3, 5),
    }
    nontransversal_zero_sets = tuple(
        tuple(sorted(set(vertices) - set(chosen_edge)))
        for chosen_edge in sorted(mixed_edges - nontransversal_component_edges)
    )
    assert nontransversal_zero_sets == (
        (1, 2, 4, 5),
        (1, 2, 3, 5),
        (1, 2, 3, 4),
        (0, 2, 4, 5),
        (0, 2, 3, 5),
        (0, 2, 3, 4),
        (0, 1, 3, 5),
        (0, 1, 3, 4),
    )
    assert all(
        closes(initial_state(apices), nontransversal_zero_sets, {})
        for apices in apex_assignments
    )

    # Three two-vertex components must contain one edge of each class-pair.
    # Up to the pair symmetries take them to be 02,14,35; the other nine
    # mixed pairs cross components and have zero cofactors.
    matching_component_edges = {edge(0, 2), edge(1, 4), edge(3, 5)}
    matching_zero_sets = tuple(
        tuple(sorted(set(vertices) - set(chosen_edge)))
        for chosen_edge in sorted(mixed_edges - matching_component_edges)
    )
    assert matching_zero_sets == (
        (1, 2, 4, 5),
        (1, 2, 3, 5),
        (1, 2, 3, 4),
        (0, 3, 4, 5),
        (0, 2, 4, 5),
        (0, 2, 3, 4),
        (0, 1, 3, 5),
        (0, 1, 3, 4),
        (0, 1, 2, 5),
    )
    assert all(
        closes(initial_state(apices), matching_zero_sets, {})
        for apices in apex_assignments
    )

    return (
        len(apex_assignments),
        tuple(len(orbit) for orbit in orbits),
        proof_sizes,
        len(nontransversal_zero_sets),
        len(matching_zero_sets),
    )


def audit_dense_projected_cut_obstruction():
    """Exact toric audit behind the full-rank projected-edge theorem.

    A disconnected nonzero-cofactor graph supplies zero K4 hafnians across
    a vertex cut.  When all projected edge forms are nondegenerate, the
    shared Pluecker lemma puts them in one bracket chart.  Each zero K4 then
    gives two signed binomial relations among the fifteen edge scalars.
    This routine checks the five cut orbits and their exact certificates.
    """

    vertices = set(range(6))
    labels = {u: u // 2 for u in range(6)}
    edges = list(combinations(range(6), 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}

    def relation_rows(four_set):
        a, b, c, d = sorted(four_set)
        matchings = (
            ((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        )
        rows = []
        for other in (1, 2):
            row = [0] * len(edges)
            for edge in matchings[0]:
                row[edge_index[tuple(sorted(edge))]] += 1
            for edge in matchings[other]:
                row[edge_index[tuple(sorted(edge))]] -= 1
            rows.append(row)
        return rows

    representatives = {
        # The certificate y obeys y*A=0, while the sum of its coefficients
        # on the first signed relation of each K4 is odd.  Multiplying the
        # corresponding binomials therefore gives 1=-1.
        (0, 0, 1): ({0}, [0, 0, 1, 0, -1, 0, 1, 0]),
        (0, 0, 2): (
            {0, 1},
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0, 1, 0],
        ),
        (0, 1, 1): ({0, 2}, [0, -1, 0, 1, 1, -1, 0, 0, 0, 0, 0, 0]),
        (0, 1, 2): (
            {0, 1, 2},
            [0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 1, 0, -1, 1, 0, -1],
        ),
    }

    pure_sets = (
        vertices - {0, 1},
        vertices - {2, 3},
        vertices - {4, 5},
    )

    def zero_four_sets(cut):
        complement = vertices - cut
        return sorted(
            {
                tuple(sorted(vertices - {u, v}))
                for u in cut
                for v in complement
                if labels[u] != labels[v]
            }
        )

    # There are exactly five cut orbits under pair permutations, within-pair
    # swaps, and taking complements.
    signatures = set()
    for mask in range(1, 32):
        cut = {u for u in range(6) if (mask >> u) & 1}
        counts = [sum(u in cut for u in pair) for pair in OUTSIDE_PAIRS.values()]
        signature = min(
            tuple(sorted(counts)), tuple(sorted(2 - count for count in counts))
        )
        signatures.add(signature)
    assert signatures == {
        (0, 0, 1),
        (0, 0, 2),
        (0, 1, 1),
        (0, 1, 2),
        (1, 1, 1),
    }

    for _, (cut, certificate) in representatives.items():
        four_sets = zero_four_sets(cut)
        rows = [row for four_set in four_sets for row in relation_rows(four_set)]
        assert len(certificate) == len(rows)
        combined = [
            sum(certificate[i] * rows[i][column] for i in range(len(rows)))
            for column in range(len(edges))
        ]
        assert combined == [0] * len(edges)
        assert sum(certificate[::2]) % 2 == 1

    # In the remaining transversal-cut orbit the binomials are consistent,
    # but they force both ratios of the first pure K4 to be -1.  The resulting
    # cofactor is a nonzero product of two nondegenerate brackets, hence has
    # local mode rank two rather than one.
    cut = {0, 2, 4}
    four_sets = zero_four_sets(cut)
    rows = [row for four_set in four_sets for row in relation_rows(four_set)]
    ratio_certificates = (
        [-1, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0],
    )
    target_rows = relation_rows(pure_sets[0])
    for certificate, target in zip(ratio_certificates, target_rows):
        combined = [
            sum(certificate[i] * rows[i][column] for i in range(len(rows)))
            for column in range(len(edges))
        ]
        assert combined == target
        assert sum(certificate[::2]) % 2 == 1

    # Every cut's zero-K4 family is connected through three-vertex overlaps;
    # this is the exact condition needed to glue the local bracket charts.
    for mask in range(1, 32):
        cut = {u for u in range(6) if (mask >> u) & 1}
        four_sets = [set(four_set) for four_set in zero_four_sets(cut)]
        assert four_sets
        reached = {0}
        while True:
            larger = reached | {
                j
                for i in reached
                for j in range(len(four_sets))
                if len(four_sets[i] & four_sets[j]) >= 3
            }
            if larger == reached:
                break
            reached = larger
        assert reached == set(range(len(four_sets)))


def main():
    k8_counts = audit_incidence_k8()
    local_passes, local_failures, _ = audit_local_model()
    audit_zero_correction_graph()
    extension_nullities = audit_pure_extension_annihilators()
    audit_two_plus_four_star_obstruction()
    disconnected_audit = audit_disconnected_apex_propagation()
    audit_dense_projected_cut_obstruction()
    print("verified arbitrary common-annihilator matching decompositions")
    print(
        "rejected all 12 identity-pair/color equality branches of the K8 model",
        f"(projected zero/impure/pure = {k8_counts})",
    )
    print("verified three simultaneous pure four-site cofactors and star identities")
    print(
        "local two-hole audit:",
        local_passes,
        "passing and",
        local_failures,
        "mixed-hole failures",
    )
    print(
        "verified pure-extension annihilator support cases",
        extension_nullities,
    )
    print("verified the 2+4 cofactor-component star obstruction")
    print(
        "closed all remaining disconnected apex placements",
        disconnected_audit,
    )
    print("verified the full-rank projected-edge cut obstruction")


if __name__ == "__main__":
    main()
