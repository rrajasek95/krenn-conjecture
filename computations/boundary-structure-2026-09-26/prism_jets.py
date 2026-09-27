"""A symbolic third-order obstruction with every higher jet left free.

Coefficients are sparse polynomials in formal first/second/third source jets.
This verifies polynomial identities, not samples of proposed perturbations.
"""
from collections import defaultdict
from itertools import combinations, product
from exact import require, matchings


def multiply(left, right, cutoff):
    out = defaultdict(int)
    for (a, u), x in left.items():
        for (b, v), y in right.items():
            if a+b <= cutoff:
                out[a+b, tuple(sorted(u+v))] += x*y
    return {k: v for k, v in out.items() if v}


def coefficient(source, word, degree):
    out = defaultdict(int)
    for matching in matchings(tuple(range(6))):
        term = {(0, ()): 1}
        for i, j in matching:
            term = multiply(term, source.get((i, j, word[i], word[j]), {}), degree)
        for (power, monomial), value in term.items():
            if power == degree:
                out[monomial] += value
    return {k: v for k, v in out.items() if v}


def verify():
    cells = tuple((i, j, a, b) for i, j in combinations(range(6), 2)
                  for a, b in product(range(3), repeat=2))
    base = {(0, 1, 0, 0), (0, 2, 2, 2), (1, 2, 1, 1),
            (3, 4, 0, 0), (3, 5, 2, 2), (4, 5, 1, 1)}
    vertical = {(0, 3, 1, 1), (1, 4, 2, 2), (2, 5, 0, 0)}
    source = {cell: {} for cell in cells}
    internal_variables = {}
    variable = 1  # variable zero is the arbitrary first-order target amplitude l.
    for cell in cells:
        if cell in base:
            source[cell][0, ()] = 1
        if (cell[0] < 3) == (cell[1] < 3):
            internal_variables[cell] = variable
            source[cell][1, (variable,)] = 1
            variable += 1
        elif cell in vertical:
            source[cell][1, (0,)] = 1
    require(len(internal_variables) == 54, 'Every internal first-jet coordinate is free')
    for degree in (2, 3):
        for cell in cells:
            source[cell][degree, (variable,)] = 1
            variable += 1
    require(variable == 325, 'One amplitude, 54 internal jets, and 270 higher-jet variables')
    for word in product(range(3), repeat=6):
        expected = {(0,): 1} if len(set(word)) == 1 else {}
        require(coefficient(source, word, 1) == expected, 'Complete first-order target equation')
    q = (1, 2, 0)
    left, right = [], []
    for color, omitted in ((0, 2), (1, 0), (2, 1)):
        i, j = [v for v in range(3) if v != omitted]
        li = internal_variables[i, j, q[i], q[j]]
        ri = internal_variables[i+3, j+3, q[i], q[j]]
        left.append(li)
        right.append(ri)
        require(coefficient(source, q+(color,)*3, 2) == {tuple(sorted((0, li))): 1},
                'Second-order left constraint is l times a left defect')
        require(coefficient(source, (color,)*3+q, 2) == {tuple(sorted((0, ri))): 1},
                'Second-order right constraint is l times a right defect')
    expected = {(0, 0, 0): 1}
    expected.update({tuple(sorted((0, l, r))): 1 for l, r in zip(left, right)})
    third = coefficient(source, q+q, 3)
    require(third == expected, 'Protected third-order coefficient is l^3+l sum L_h R_h')
    # The polynomial identity l*E3 - sum E2_left*E2_right = l^4.
    identity = defaultdict(int)
    for monomial, value in third.items():
        identity[tuple(sorted((0,)+monomial))] += value
    for l, r in zip(left, right):
        identity[tuple(sorted((0, 0, l, r)))] -= 1
    identity = {k: v for k, v in identity.items() if v}
    require(identity == {(0, 0, 0, 0): 1}, 'Exact elimination identity for the third-order obstruction')
    return dict(formal_variables=variable, full_first_order_coefficients=729,
                arbitrary_second_jet_cells=135, arbitrary_third_jet_cells=135,
                second_order_constraints=6, protected_word=list(q+q),
                identity='l * E3_protected - sum_h E2_left_h * E2_right_h = l^4',
                consequence='With l nonzero and second-order error zero, third-order error cannot vanish')
