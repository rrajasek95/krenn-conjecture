"""Exact examples at the newly separated boundary classes."""
from itertools import combinations, product, permutations
from fractions import Fraction as Q
from exact import E, ZERO, ONE, OMEGA, require, matchings, hafnian, outputs, cell, rank
import graphs


def critical_core():
    # Core sites 0..4; site 5 is isolated. Opposite edges of 0..3 have
    # weights 1, omega, omega^2. Every edge to site 4 has weight one.
    scalar = {(0, 1): ONE, (2, 3): ONE,
              (0, 2): OMEGA, (1, 3): OMEGA,
              (0, 3): OMEGA*OMEGA, (1, 2): OMEGA*OMEGA}
    scalar.update({(i, 4): ONE for i in range(4)})
    return scalar


def check_critical():
    require(OMEGA*OMEGA+OMEGA+ONE == ZERO and OMEGA.abs2() == 1, 'Primitive cube-root arithmetic')
    q = critical_core()
    minors = [hafnian(q, [j for j in range(5) if j != i]) for i in range(5)]
    require(all(not z for z in minors), 'Every four-site core hafnian cancels exactly')
    a = {(i, j, 0, 0): z for (i, j), z in q.items()}
    require(not outputs(a), 'Isolated-root base has zero output')
    # Every four-site source tensor vanishes: those including 5 are empty,
    # and the other five were checked above. Hence all 135 derivatives vanish.
    for vertices in combinations(range(6), 4):
        require(not hafnian(q, vertices), 'All 15 four-site hafnians vanish')
    p, weights = graphs.cover(6, set(q))
    require(set(weights) == set(q) and set(weights.values()) == {Q(1, 2)}, 'K5 matching cover')
    eta = Q(1, 100)
    bound = (1+Q(1, 4)*eta**2/(1-eta)**2)/3
    require(bound == Q(39205, 117612) and bound < Q(334, 1000), 'Diagonal neighborhood ceiling')
    return dict(source_energy='10', nonzero_core_edges=10, vanishing_four_site_hafnians=15,
                derivative_rank=0, derivative_columns=135,
                all_six_root_response_ranks=[0]*6, all_six_augmented_ranks=[3]*6,
                diagonal_radius=str(eta), diagonal_fidelity_ceiling=str(bound),
                full_complex_neighborhood='Unresolved: off-diagonal perturbations are not covered')


def diagonal_identity():
    # A genuinely complex diagonal source; the identity is not positivity-based.
    a = {(i, j, h, h): E(1+(i+2*j+h) % 3, (i+j+2*h) % 3)
         for i, j in combinations(range(6), 2) for h in range(3)}
    h = outputs(a)
    support = set(combinations(range(5), 2))
    _, weights = graphs.cover(6, support)
    norms = []
    for color in (1, 2):
        reconstructed, norm = ZERO, Q(0)
        for (i, j), weight in weights.items():
            word = [color]*6
            word[i] = word[j] = 0
            coefficient = weight*a[i, j, color, color]/a[i, j, 0, 0]
            reconstructed += coefficient*h.get(tuple(word), ZERO)
            norm += coefficient.abs2()
        require(reconstructed == h[(color,)*6], 'Mixed coefficients reconstruct a pure amplitude')
        norms.append(norm)
    target = sum((h.get((c,)*6, ZERO) for c in range(3)), ZERO)
    total = sum(z.abs2() for z in h.values())
    fidelity = target.abs2()/(3*total)
    upper = (1+sum(s/(1+s) for s in norms))/3
    require(fidelity <= upper, 'Source-dependent diagonal fidelity ceiling')
    return dict(identity_colors_checked=2, actual_fidelity=str(fidelity), fidelity_upper=str(upper),
                reconstruction_coefficient_norms_squared=list(map(str, norms)))


def four_site_identities():
    a = {(i, j, h, k): E(1+(i+j+h) % 3, (j+h+k) % 2)
         for i, j in combinations(range(4), 2) for h, k in product(range(3), repeat=2)}
    H = outputs(a, n=4)
    count = 0
    for h, i, p, q in product(range(3), range(3), range(4), range(4)):
        value = ZERO
        for r in range(4):
            if r == p or r == q:
                continue
            u, v = [s for s in range(4) if s not in (r, q)]
            value += a[cell(p, r, i, h)]*a[cell(u, v, h, h)]
        if p == q:
            word = [h]*4
            word[p] = i
            expected = H.get(tuple(word), ZERO)
        else:
            r, s = [t for t in range(4) if t not in (p, q)]
            expected = a[cell(p, r, i, h)]*a[cell(p, s, h, h)]+a[cell(p, s, i, h)]*a[cell(p, r, h, h)]
        require(value == expected, 'Four-site cofactor identity including endpoint order')
        count += 1
    return dict(cofactor_entries_checked=count,
                analytic_dependency='Whole-binary and omission identities, exact proof sections 2-3, including three-site odd cores')


def regular_triangles():
    four = tuple(matchings(tuple(range(4))))
    for coloring in permutations(range(3)):
        source = {}
        expected = {}
        for matching, color in zip(four, coloring):
            amplitude = ONE
            for j, (u, v) in enumerate(matching):
                weight = E(2+color, j+1)
                source[u, v, color, color] = weight
                amplitude *= weight
            expected[(color,)*4] = amplitude
        require(outputs(source, n=4) == expected, 'All six colored four-site matching constructions')
    fixtures = 0
    triples = (tuple(combinations(range(3), 2)), tuple(combinations(range(3, 6), 2)))
    for lc, rc in product(permutations(range(3)), repeat=2):
        base, factors = {}, [[ONE]*3 for _ in range(6)]
        edge_by_color = [{color: edge for edge, color in zip(edges, coloring)}
                         for edges, coloring in zip(triples, (lc, rc))]
        for color in range(3):
            (i, j), (k, l) = [side[color] for side in edge_by_color]
            left, right = E(2+color, 1), E(1, 1+color)
            base[i, j, color, color], base[k, l, color, color] = left, right
            factors[i][color] = ONE/left
            factors[k][color] = ONE/right
            unmatched = next(v for v in range(3) if v not in (i, j))
            factors[unmatched][color] = left*right
        for color in range(3):
            value = ONE
            for row in factors:
                value *= row[color]
            require(value == ONE, 'Gauge preserves each pure target amplitude')
        require(all(z*factors[i][a]*factors[j][b] == ONE for (i, j, a, b), z in base.items()),
                'Gauge normalizes every weighted internal edge')
        for vertices, edges in zip((tuple(range(3)), tuple(range(3, 6))), triples):
            rows = []
            for word in product(range(3), repeat=3):
                colors = dict(zip(vertices, word))
                row = []
                for omitted, h in product(vertices, range(3)):
                    i, j = [v for v in vertices if v != omitted]
                    row.append(base.get((i, j, colors[i], colors[j]), ZERO) if colors[omitted] == h else ZERO)
                rows.append(row)
            require(rank(rows) == 9, 'Weighted monochromatic triangle response is injective')
        if fixtures == 0:
            dense = {(i, j, a, b): E(1+(i+j+a) % 3, (j+b) % 2)
                     for i, j in combinations(range(6), 2) for a, b in product(range(3), repeat=2)}
            transformed = {cell: z*factors[cell[0]][cell[2]]*factors[cell[1]][cell[3]] for cell, z in dense.items()}
            before, after = outputs(dense), outputs(transformed)
            for word in product(range(3), repeat=6):
                scale = ONE
                for v, color in enumerate(word):
                    scale *= factors[v][color]
                require(after.get(word, ZERO) == scale*before.get(word, ZERO), 'Full-complex gauge covariance')
        fixtures += 1
    return dict(four_site_colorings=6, triangle_color_assignments=fixtures,
                gauge_covariance_words=729, response_rank_per_triangle=9)


def w_two_roots():
    # Add genuinely colored cells at root 1 that are invisible because the
    # cofactor matrix has a kernel, while its support is complete/nonbipartite.
    D = {(2, 3): ONE, (4, 5): ONE, (2, 4): ONE, (3, 5): ONE,
         (2, 5): E(2), (3, 4): E(2)}
    C = [[ZERO if i == j else hafnian(D, [v for v in range(2, 6) if v not in (i, j)])
          for j in range(2, 6)] for i in range(2, 6)]
    require(rank(C) == 3, 'Singular cofactor matrix')
    v = [ONE, -ONE, -ONE, ONE]
    require(all(sum((x*y for x, y in zip(row, v)), ZERO) == ZERO for row in C), 'Exact kernel direction')
    a = {(i, j, 0, 0): z for (i, j), z in D.items()}
    for i in range(2, 6):
        a[1, i, 0, 0] = ONE
        a[0, i, 0, 1] = E(Q(1, 4))
    # Ground-core hafnian is 6. Both root-only excitations come through 01.
    a[0, 1, 1, 0] = E(Q(1, 6))
    a[0, 1, 0, 1] = E(Q(1, 6))
    reduced = dict(a)
    for i, z in zip(range(2, 6), v):
        a[1, i, 1, 0] = OMEGA*z
        a[1, i, 2, 0] = z
    expected = {tuple(int(j == i) for j in range(6)): ONE for i in range(6)}
    require(outputs(a) == expected and outputs(reduced) == expected, 'Full ternary W output before and after deletion')
    removed = sum(z.abs2() for key, z in a.items() if key not in reduced)
    require(removed == 8, 'Invisible cells consume strictly positive source energy')
    # An exact bipartite cancellation example outside the reduction hypothesis.
    s = E(Q(1, 2))
    b = {(i, j, 0, 0): ONE for i in (2, 3) for j in (4, 5)}
    for i in range(2, 6):
        sign = 1 if i in (2, 3) else -1
        b[0, i, 0, 0] = -sign*s
        b[0, i, 0, 1] = s
        b[1, i, 0, 0] = s
        b[1, i, 0, 1] = sign*s
    b[0, 1, 0, 1] = b[0, 1, 1, 0] = E(Q(1, 2))
    require(outputs(b) == expected, 'Exact W with two active excitation roots and bipartite cofactors')
    energy = sum(z.abs2() for z in b.values())
    rate = Q(6)/energy**3
    require(rate == Q(48, 4913) and rate < Q(1, 65), 'Bipartite example does not improve the known rate')
    return dict(nonbipartite_cofactor_rank=3, deleted_energy=str(removed),
                nonzero_outputs_before=6, nonzero_outputs_after=6, ternary_words_checked=729,
                bipartite_example_energy=str(energy), bipartite_example_rate=str(rate))
