"""Exact certificates for fixed-core design with two output requirements.

Discovery is optional and separate. Every accepted certificate contains an
actual complex vector and a rational positive-semidefinite dual slack.
"""
from itertools import product
from shared import C, Q, ZERO, core, gram, require


def problem(payload):
    data = core.matrices(core.read_source(payload['core']), payload['root'])
    vertices = [v for v in range(6) if v != payload['root']]
    rows, words = [], []
    for h in range(3):
        for word, row in zip(product(range(3), repeat=5), data['T']):
            full = [0]*6
            full[payload['root']] = h
            for p, color in zip(vertices, word):
                full[p] = color
            words.append(tuple(full))
            rows.append([ZERO]*(15*h)+row+[ZERO]*(15*(2-h)))
    index = {w: i for i, w in enumerate(words)}
    constraints, effects = [], []
    require(1 <= len(payload['qualities']) <= 2, 'At most two quality requirements')
    for quality in payload['qualities']:
        kind = quality['kind']
        if kind == 'target':
            target = [ZERO]*729
            seen = set()
            for entry in quality['entries']:
                word = tuple(entry['word'])
                require(word in index and word not in seen, 'Distinct valid target words')
                seen.add(word)
                target[index[word]] = core.decode(entry['value'])
            norm = core.dot(target, target).re
            require(norm > 0, 'Nonzero target')
            covector = [sum((core.conj(t)*row[j] for t, row in zip(target, rows)), ZERO)
                        for j in range(45)]
            effect = [[core.conj(x)*y/norm for y in covector] for x in covector]
        elif kind == 'events':
            selected = [tuple(w) for w in quality['words']]
            require(len(set(selected)) == len(selected) and all(w in index for w in selected),
                    'Distinct valid output events')
            effect = gram([rows[index[w]] for w in selected]) if selected else [[ZERO]*45 for _ in range(45)]
        else:
            raise ValueError('Unknown output quality')
        threshold = Q(quality['threshold'])
        require(0 <= threshold <= 1, 'Probability threshold')
        require(quality['sense'] in ('min', 'max'), 'Quality inequality direction')
        sign = 1 if quality['sense'] == 'min' else -1
        constraints.append([[sign*(effect[i][j]-threshold*data['K'][i][j])
                             for j in range(45)] for i in range(45)])
        effects.append(effect)
    return data, constraints, effects


def verify(payload):
    data, constraints, effects = problem(payload)
    multipliers = list(map(Q, payload['multipliers']))
    require(len(multipliers) == len(constraints) and all(x >= 0 for x in multipliers),
            'Nonnegative dual multipliers')
    upper = Q(payload['upper_eigenvalue'])
    slack = [[C(upper if i == j else 0)-data['K'][i][j]
              -sum((mu*matrix[i][j] for mu, matrix in zip(multipliers, constraints)), ZERO)
              for j in range(45)] for i in range(45)]
    pivots = core.psd(slack)
    vector = list(map(core.decode, payload['witness']))
    require(len(vector) == 45, '45 root coordinates')
    norm = core.dot(vector, vector).re
    strength = core.quadratic(data['K'], vector)
    require(norm > 0 and strength > 0, 'Nonzero output witness')
    margins = [core.quadratic(matrix, vector) for matrix in constraints]
    require(all(x >= 0 for x in margins), 'Witness meets every output requirement')
    factor = Q(4, 27)/data['energy']**2
    lo, hi = factor*strength/norm, factor*upper
    require(lo <= hi, 'Primal-dual order')
    return dict(rate_lower=str(lo), rate_upper=str(hi), relative_gap=str((hi-lo)/lo),
                quality_values=[str(core.quadratic(effect, vector)/strength) for effect in effects],
                margins=[str(x) for x in margins], psd=pivots)


def robust_upper(payload, radius, norm_lower, norm_upper, response_upper):
    """A dual upper bound on a whole ball of arbitrary complex five-site cores.

    The rational bounds must satisfy norm_lower <= ||Q|| <= norm_upper and
    ||L_Q|| <= response_upper. A six-site cofactor Lipschitz estimate supplies
    beta <= 4*(norm_upper*radius + radius**2/2), since sqrt(15) < 4.
    """
    data, constraints, _ = problem(payload)
    # Reuse complete certificate validation, including actual feasibility.
    verify(payload)
    rho, low, high, op = map(Q, (radius, norm_lower, norm_upper, response_upper))
    require(0 <= rho < low and low*low <= data['energy'] <= high*high and high >= low,
            'Valid core ball and norm bounds')
    require(op >= 0, 'Nonnegative response norm upper bound')
    core.psd([[C(op*op if i == j else 0)-data['K'][i][j]
               for j in range(45)] for i in range(45)])
    beta = 4*(high*rho+rho*rho/2)
    gram_error = 2*op*beta+beta*beta
    mu = list(map(Q, payload['multipliers']))
    # In output space B=I+sum mu*s*(P-threshold*I); ||P|| <= 1.
    signs = [1 if q['sense'] == 'min' else -1 for q in payload['qualities']]
    scalar = 1-sum(m*s*Q(q['threshold']) for m, s, q in zip(mu, signs, payload['qualities']))
    bnorm = abs(scalar)+sum(mu)
    value = Q(4, 27)*(Q(payload['upper_eigenvalue'])+bnorm*gram_error)/(low-rho)**4
    return dict(core_radius=str(rho), response_error_upper=str(beta),
                dual_output_operator_norm_upper=str(bnorm), rate_upper=str(value),
                scope='Every complex core in the Euclidean ball; every qualifying root vector')
