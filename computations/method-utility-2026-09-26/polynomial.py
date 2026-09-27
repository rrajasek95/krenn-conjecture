"""Sparse Gaussian-rational polynomials and integral-dependence certificates."""
from shared import C, Q, ZERO, ONE, core, require


def add(*polys):
    out = {}
    for poly in polys:
        for powers, value in poly.items():
            out[powers] = out.get(powers, ZERO)+value
    return {p: v for p, v in out.items() if v}


def scale(poly, coefficient):
    coefficient = C.cast(coefficient)
    return {p: coefficient*v for p, v in poly.items() if coefficient*v}


def mul(a, b):
    out = {}
    for p, x in a.items():
        for q, y in b.items():
            require(len(p) == len(q), 'Consistent polynomial variables')
            powers = tuple(i+j for i, j in zip(p, q))
            out[powers] = out.get(powers, ZERO)+x*y
    return {p: v for p, v in out.items() if v}


def power(poly, exponent, variables):
    require(isinstance(exponent, int) and exponent >= 0, 'Nonnegative integer exponent')
    out = {(0,)*variables: ONE}
    for _ in range(exponent):
        out = mul(out, poly)
    return out


def decode(entries, variables):
    out = {}
    for entry in entries:
        powers = tuple(entry['powers'])
        require(len(powers) == variables and all(isinstance(k, int) and k >= 0 for k in powers),
                'Valid monomial')
        require(powers not in out, 'Distinct polynomial monomials')
        out[powers] = core.decode(entry['coefficient'])
    return {p: v for p, v in out.items() if v}


def encode(poly):
    return [dict(powers=list(p), coefficient=core.encode(v)) for p, v in sorted(poly.items())]


def coefficient_bound(poly):
    # Valid on the complex Euclidean unit ball: |each coordinate| <= 1.
    return sum(abs(z.re)+abs(z.im) for z in poly.values())


def verify_integral(payload):
    n, degree = payload['variables'], payload['degree']
    require(isinstance(n, int) and n > 0 and isinstance(degree, int) and degree > 0,
            'Positive dimensions and monic degree')
    target = decode(payload['target'], n)
    require(bool(target), 'Nonzero certificate target polynomial')
    errors = [decode(e, n) for e in payload['errors']]
    require(bool(errors), 'At least one error generator')
    groups = payload['coefficients']
    require(len(groups) == degree, 'One coefficient in every ideal power')
    identity = power(target, degree, n)
    bounds = []
    for j, terms in enumerate(groups, start=1):
        coefficient, bound = {}, Q(0)
        for term in terms:
            indices = term['errors']
            require(len(indices) == j and all(isinstance(i, int) and 0 <= i < len(errors) for i in indices),
                    'Coefficient belongs to the required ideal power')
            multiplier = decode(term['multiplier'], n)
            product = multiplier
            for i in indices:
                product = mul(product, errors[i])
            coefficient = add(coefficient, product)
            bound += coefficient_bound(multiplier)
        bounds.append(bound)
        identity = add(identity, mul(coefficient, power(target, degree-j, n)))
    require(not identity, 'Exact monic integral-dependence identity')
    constant = Q(payload['norm_constant'])
    require(constant > 0 and sum(b/constant**j for j, b in enumerate(bounds, start=1)) <= 1,
            'Positive norm majorant')
    return dict(monic_degree=degree, coefficient_bounds=list(map(str, bounds)),
                norm_constant=str(constant),
                conclusion='|target| <= norm_constant * ||errors||_2 on the unit ball')


def arc_outputs(payload):
    """Expand an entire polynomial source path, never a truncated Taylor jet."""
    source = {}
    for entry in payload['source']:
        cell = tuple(entry['cell'])
        core.read_source([dict(cell=list(cell), value=['1', '0'])])
        require(cell not in source, 'Distinct source arc cells')
        source[cell] = decode(entry['polynomial'], 1)
    base_norm = sum(p.get((0,), ZERO).abs2() for p in source.values())
    require(base_norm > 0, 'Arc has a nonzero limiting source')
    outputs = {}
    # Enumerate active cells per edge, then all perfect matchings.
    edges = {}
    for (p, q, i, j), value in source.items():
        edges.setdefault((p, q), []).append((i, j, value))
    from itertools import product
    for matching in core.matchings(tuple(range(6))):
        for choices in product(*(edges.get(edge, []) for edge in matching)):
            word, term = [None]*6, {(0,): ONE}
            for (p, q), (i, j, value) in zip(matching, choices):
                word[p], word[q] = i, j
                term = mul(term, value)
            word = tuple(word)
            outputs[word] = add(outputs.get(word, {}), term)
    pure = [(h,)*6 for h in range(3)]
    target = scale(add(*(outputs.get(word, {}) for word in pure)), Q(1, 3))
    errors = dict(outputs)
    for word in pure:
        errors[word] = add(errors.get(word, {}), scale(target, -1))
    require(bool(target), 'Nonzero desired amplitude along the arc')
    require(any(errors.values()), 'Nonzero error; exact GHZ arc would contradict the exact theorem')
    r = min(p[0] for p in target)
    s = min(p[0] for poly in errors.values() for p in poly)
    require(r > 0 and s > r, 'Arc approaches GHZ at a zero-output boundary')
    return dict(target_order=r, error_order=s, error_to_target_order=str(Q(s, r)),
                achieved_rate_exponent=str(Q(r, s-r)),
                violates_square_root=(s > 3*r), source_base_norm_squared=str(base_norm),
                scope='Exact polynomial arc, all matching output coefficients expanded')
