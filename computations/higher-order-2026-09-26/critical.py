"""Full-color polynomial identities at the completely singular core."""
from itertools import combinations, product
from shared import *


def clean(poly):
    return {m: z for m, z in poly.items() if z}


def add(poly, monomial, value):
    poly[monomial] = poly.get(monomial, ZERO)+value


def coefficient(source, word, degree):
    out = {}
    for matching in matchings(tuple(range(6))):
        term = {(0, ()): ONE}
        for i, j in matching:
            new = {}
            for (d, m), z in term.items():
                for (e, n), w in source[i, j, word[i], word[j]].items():
                    if d+e <= degree:
                        add(new, (d+e, tuple(sorted(m+n))), z*w)
            term = clean(new)
        for (d, m), z in term.items():
            if d == degree:
                add(out, m, z)
    return clean(out)


def verify():
    cells = tuple((i, j, a, b) for i, j in combinations(range(6), 2)
                  for a, b in product(range(3), repeat=2))
    indexes = {c: i for i, c in enumerate(cells)}
    q = critical_core()
    source = {c: {(d, (135*(d-1)+i,)): ONE for d in (1, 2, 3, 4)}
              for i, c in enumerate(cells)}
    first_source = {c: {(1, (i,)): ONE} for i, c in enumerate(cells)}
    for (i, j), z in q.items():
        source[i, j, 0, 0][0, ()] = z
    first = {w: coefficient(source, w, 1) for w in product(range(3), repeat=6)}
    require(not any(first.values()), 'All 135 first jets cancel in all 729 outputs')
    identities = 0
    for h in (1, 2):
        rhs = {}
        for (i, j), z in q.items():
            word = [h]*6
            word[i] = word[j] = 0
            second = coefficient(source, tuple(word), 2)
            remaining = tuple(v for v in range(6) if v not in (i, j))
            expected = {}
            for matching in matchings(remaining):
                monomial = tuple(sorted(indexes[u, v, h, h] for u, v in matching))
                add(expected, monomial, z)
            require(second == clean(expected), 'Quadratic receiving word has only the designated base edge')
            for monomial, value in second.items():
                add(rhs, tuple(sorted((indexes[i, j, h, h],)+monomial)), value/(2*z))
        third = coefficient(source, (h,)*6, 3)
        require(clean(rhs) == third, 'Pure cubic amplitude is in the quadratic error ideal')
        require(all(max(m) < 135 for m in third), 'Second and third source jets cannot change this pure coefficient')
        require(len(third) == 15, 'All fifteen pure matching monomials retained')
        # Delete one cover term: the resulting alleged identity must fail.
        bad = dict(rhs)
        i, j = next(iter(q))
        word = [h]*6
        word[i] = word[j] = 0
        for monomial, value in coefficient(source, tuple(word), 2).items():
            add(bad, tuple(sorted((indexes[i, j, h, h],)+monomial)), -value/(2*q[i, j]))
        require(clean(bad) != third, 'Missing matching-cover term is detected')
        fourth_rhs = {}
        for (i, j), z in q.items():
            word = [h]*6
            word[i] = word[j] = 0
            word = tuple(word)
            first_var = indexes[i, j, h, h]
            second_var = 135+first_var
            for monomial, value in coefficient(source, word, 3).items():
                add(fourth_rhs, tuple(sorted((first_var,)+monomial)), value/(2*z))
            for monomial, value in coefficient(source, word, 2).items():
                add(fourth_rhs, tuple(sorted((second_var,)+monomial)), value/(2*z))
            for monomial, value in coefficient(first_source, word, 3).items():
                add(fourth_rhs, tuple(sorted((first_var,)+monomial)), -value/(2*z))
        fourth = coefficient(source, (h,)*6, 4)
        require(clean(fourth_rhs) == fourth, 'Fourth pure coefficient modulo the preceding output constraints')
        require(all(max(m) < 270 for m in fourth), 'Third and fourth source jets cannot change the fourth pure coefficient')
        identities += 1
    # The finite-increment identity retains every endpoint-color entry.
    x = {c: E(Q(1+(i % 5), 20), Q((i % 3)-1, 30)) for i, c in enumerate(cells)}
    a = dict(x)
    for (i, j), z in q.items():
        a[i, j, 0, 0] += z
    ha, hx = outputs(a), outputs(x)
    for h in (1, 2):
        total = ZERO
        for (i, j), z in q.items():
            word = [h]*6
            word[i] = word[j] = 0
            total += x[i, j, h, h]/(2*z)*(ha.get(tuple(word), ZERO)-hx.get(tuple(word), ZERO))
        require(total == ha[(h,)*6], 'Finite-increment reconstruction with full-complex quartic remainder')
    return dict(formal_variables=540, arbitrary_cells_per_jet=135,
                first_order_words=729, pure_cubic_identities=identities,
                pure_quartic_identities=identities,
                finite_increment_colors=2, negative_control='Missing cover term REJECTED',
                consequence='If error is little-o(signal), signal is O(distance^4); no nonzero GHZ leading term through order three',
                unresolved='Order four and higher; the unrestricted square-root bound is not established')
