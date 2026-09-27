"""Small exact fixtures, with no numerical discovery dependency."""
from itertools import combinations
from shared import C, Q, ONE, core
import polynomial as p


def monomial(powers, value=1):
    return {tuple(powers): C.cast(value)}


def toy_integral():
    # xy is not in (x^2,y^2), but (xy)^2 - x^2*y^2 = 0.
    return dict(variables=2, degree=2, target=p.encode(monomial([1, 1])),
                errors=[p.encode(monomial([2, 0])), p.encode(monomial([0, 2]))],
                coefficients=[[], [dict(multiplier=p.encode(monomial([0, 0], -1)), errors=[0, 1])]],
                norm_constant='1')


def prism_integral():
    n = 9
    xs = [monomial([int(i == j) for i in range(n)]) for j in range(n)]
    # x_h, y_h, z_h in three successive triples.
    tau = [p.mul(p.mul(xs[h], xs[3+h]), xs[6+h]) for h in range(3)]
    lam = p.scale(p.add(*tau), Q(1, 3))
    errors = [p.add(t, p.scale(lam, -1)) for t in tau]
    mu, internal = {(0,)*n: ONE}, {(0,)*n: ONE}
    for x in xs[6:]:
        mu = p.mul(mu, x)
    for x in xs[:6]:
        internal = p.mul(internal, x)
    # lambda^3 - P*mu + lambda*sum_{i<j} e_i*e_j + e_a*e_b*e_c = 0.
    terms = [dict(multiplier=p.encode(p.scale(internal, -1)), errors=[3])]
    terms += [dict(multiplier=p.encode(p.mul(lam, errors[j])), errors=[i])
              for i, j in combinations(range(3), 2)]
    terms.append(dict(multiplier=p.encode(p.mul(errors[1], errors[2])), errors=[0]))
    return dict(variables=n, degree=1, target=p.encode(p.power(lam, 3, n)),
                errors=[p.encode(e) for e in errors+[mu]], coefficients=[terms], norm_constant='5')


def prism_arc(exponent=1, cancellation=False):
    constant, vertical = p.encode(monomial([0])), p.encode(monomial([exponent]))
    internal_cells = [(0, 1, 0, 0), (0, 2, 2, 2), (1, 2, 1, 1),
                      (3, 4, 0, 0), (3, 5, 2, 2), (4, 5, 1, 1)]
    vertical_cells = [(0, 3, 1, 1), (1, 4, 2, 2), (2, 5, 0, 0)]
    entries = [dict(cell=list(cell), polynomial=constant) for cell in internal_cells]
    entries += [dict(cell=list(cell), polynomial=vertical) for cell in vertical_cells]
    if cancellation:
        entries += [dict(cell=list(cell), polynomial=p.encode(monomial([degree], value)))
                    for cell, degree, value in [((2, 3, 1, 1), 8, 1),
                                                ((2, 4, 1, 1), 4, 1),
                                                ((3, 5, 1, 1), 4, -1)]]
    return dict(source=entries)


def w_core():
    return dict(root=5, core=[dict(cell=[i, j, 0, 0], value=['1', '0'])
                             for i, j in combinations(range(5), 2)],
                qualities=[dict(kind='target', sense='min', threshold='1',
                                entries=[dict(word=[int(j == i) for j in range(6)], value=['1', '0'])
                                         for i in range(6)])])


def verify_w():
    """Check actual W6 outputs, minimum root norm, and general-even formula."""
    import quality
    from itertools import product
    data, _, effects = quality.problem(w_core())
    # v is a minimum-norm preimage of the unnormalized six-term W vector.
    v = [core.ZERO]*45
    for j in range(5):
        v[3*j+1] = C(Q(1, 3))
        v[15+3*j] = C(Q(1, 15))
    # u on output space is chosen so that L*u = v; this certifies v perpendicular ker L.
    adjoint = [core.ZERO]*45
    output_norm, target_overlap, count = Q(0), C(0), 0
    for h in range(3):
        for word, row in zip(product(range(3), repeat=5), data['T']):
            full = word+(h,)
            is_w = full.count(1) == 1 and full.count(0) == 5
            output = core.dot([core.conj(z) for z in row], v[15*h:15*(h+1)])
            core.require(output == C(int(is_w)), 'Every W6 output coefficient')
            count += int(bool(output))
            output_norm += output.abs2()
            target_overlap += output if is_w else C(0)
            u = Q(1, 45) if is_w and h == 1 else Q(1, 9) if is_w else Q(0)
            for j, z in enumerate(row):
                adjoint[15*h+j] += core.conj(z)*u
    core.require(adjoint == v, 'Minimum norm preimage lies in the adjoint image')
    norm = core.dot(v, v).re
    core.require(count == 6 and norm == Q(26, 45), 'W target and minimum incident norm')
    rate = Q(4, 27)/data['energy']**2*output_norm/norm
    core.require(rate == Q(1, 65), 'Optimal exact W6 fixed-core rate')
    table = []
    for n in (4, 6, 8, 10, 12):
        N, m = n-1, n//2
        h = 1
        for k in range(1, n-2, 2):
            h *= k
        core.require(h == len(list(core.matchings(tuple(range(n-2))))), 'Cofactor matching count')
        energy = Q(N*(N-1), 2)
        gain = Q(n*h*h*N, N*N+1)
        scale = Q((m-1)**(m-1), m**m)/energy**(m-1)
        hafnian_bound = Q((N*h)**2, (n*N//2)**m)
        core.require(scale*gain == Q(n, N*N+1)*hafnian_bound,
                     'Attained rate equals the architecture-wide upper bound')
        table.append(dict(sites=n, cofactor=h, response_gain=str(gain), rate=str(scale*gain)))
    return dict(exact_W6_rate=str(rate), minimum_preimage_norm_squared=str(norm),
                output_coefficients_checked=729, even_size_rates=table)


def verify_weighted_w():
    """A different, genuinely complex core and a nonuniform complex W target."""
    from itertools import product
    source = {(i, j, 0, 0): C(1+(i+2*j) % 3, (i-j) % 2)
              for i, j in combinations(range(5), 2)}
    data = core.matrices(source, 5)
    h = [data['T'][0][3*i] for i in range(5)]
    core.require(all(h), 'Chosen complex core has all needed cofactors')
    T = sum(z.abs2() for z in h)
    amplitudes = [C(i+1, (-1)**i) for i in range(5)]+[C(2, 3)]
    v = [core.ZERO]*45
    for i in range(5):
        v[3*i+1] = amplitudes[i]/h[i]
        v[15+3*i] = amplitudes[5]*core.conj(h[i])/T
    adjoint = [core.ZERO]*45
    for root_color in range(3):
        for word, row in zip(product(range(3), repeat=5), data['T']):
            full = word+(root_color,)
            is_w = full.count(1) == 1 and full.count(0) == 5
            site = full.index(1) if is_w else None
            expected = amplitudes[site] if is_w else core.ZERO
            output = sum((z*x for z, x in zip(row, v[15*root_color:15*(root_color+1)])), core.ZERO)
            core.require(output == expected, 'Complex weighted W coefficient')
            u = (amplitudes[site]/(h[site].abs2() if site < 5 else T)) if is_w else core.ZERO
            for j, z in enumerate(row):
                adjoint[15*root_color+j] += core.conj(z)*u
    core.require(adjoint == v, 'Complex minimum norm witness is in adjoint image')
    D = sum(amplitudes[i].abs2()/h[i].abs2() for i in range(5))+amplitudes[5].abs2()/T
    core.require(core.dot(v, v).re == D, 'Weighted W norm formula')
    core.require(T <= Q(9, 20)*data['energy']**2, 'Sharp five-site cofactor bound on example')
    xs = [z.abs2() for z in h]
    defect = sum((x-y)**2/(x*y) for x, y in combinations(xs, 2))
    core.require(defect == T*sum(1/x for x in xs)-25, 'Exact cofactor balance identity')
    return dict(core_energy=str(data['energy']), cofactor_norm_squared=str(T),
                minimum_incident_norm_squared=str(D), cofactor_balance_defect=str(defect),
                output_coefficients_checked=729)
