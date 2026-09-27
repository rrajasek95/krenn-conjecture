"""Exact algebra and controls for the balanced response and cofactor criteria."""

from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "single-invertible-edge-ghz-2026-09-27"))
import edge_projection as EP
from edge_projection import Poly, T, E, ZERO, ONE, require


def adjoint(matrix):
    return [list(row) for row in zip(*[[z.conjugate() for z in row] for row in matrix])]


def apply(matrix, vector):
    return [sum((x*y for x, y in zip(row, vector)), ZERO) for row in matrix]


def inner(x, y):
    return sum((a.conjugate()*b for a, b in zip(x, y)), ZERO)


def norm2(x):
    return sum((z.abs2() for z in x), Q(0))


def response_matrix(xs, ys):
    p, q = len(xs[0]), len(ys[0])
    return [[y[b] if a == j else ZERO for j in range(p)]
            + [x[a] if b == j else ZERO for j in range(q)]
            for x, y in zip(xs, ys) for a, b in product(range(p), range(q))]


def symbolic_conjugate(poly):
    def conjugate_name(name):
        return name[4:] if name.startswith("bar_") else "bar_" + name
    return Poly({tuple(sorted(conjugate_name(v) for v in monomial)): coefficient
                 for monomial, coefficient in poly.terms.items()})


def determinant(matrix):
    n = len(matrix)
    result = Poly()
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = Poly((-1)**inversions)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        result += term
    return result


def check_formal_gram():
    counts = []
    for p, q, m in ((2, 2, 4), (2, 3, 4), (3, 4, 4)):
        xs = [[Poly.variable(f"x_{i}_{a}") for a in range(p)] for i in range(m)]
        ys = [[Poly.variable(f"y_{i}_{b}") for b in range(q)] for i in range(m)]
        matrix = [[y[b] if a == j else Poly() for j in range(p)]
                  + [x[a] if b == j else Poly() for j in range(q)]
                  for x, y in zip(xs, ys) for a, b in product(range(p), range(q))]
        xnorm = sum((symbolic_conjugate(x)*x for row in xs for x in row), Poly())
        ynorm = sum((symbolic_conjugate(y)*y for row in ys for y in row), Poly())
        k = [[sum((xs[i][a]*symbolic_conjugate(ys[i][b]) for i in range(m)), Poly())
              for b in range(q)] for a in range(p)]
        for i, j in product(range(p+q), repeat=2):
            actual = sum((symbolic_conjugate(row[i])*row[j] for row in matrix), Poly())
            if i < p and j < p:
                expected = ynorm if i == j else Poly()
            elif i >= p and j >= p:
                expected = xnorm if i == j else Poly()
            elif i < p:
                expected = k[i][j-p]
            else:
                expected = symbolic_conjugate(k[j][i-p])
            require(actual.terms == expected.terms, "Formal Hermitian response Gram entry")
        counts.append(dict(left_dimension=p, right_dimension=q, vector_pairs=m,
                           gram_entries=(p+q)**2))

    k = [[Poly.variable(f"k_{i}_{j}") for j in range(2)] for i in range(2)]
    z = Poly.variable("z")
    matrix = [[z if i == j else Poly() for j in range(4)] for i in range(4)]
    for i, j in product(range(2), repeat=2):
        matrix[i][2+j] = -k[i][j]
        matrix[2+j][i] = -symbolic_conjugate(k[i][j])
    frob = sum((symbolic_conjugate(v)*v for row in k for v in row), Poly())
    det = determinant(k)
    expected = z*z*z*z-frob*z*z+symbolic_conjugate(det)*det
    require(determinant(matrix).terms == expected.terms,
            "Centered binary Gram characteristic polynomial")
    return dict(rectangular_gram_identities=counts,
                total_gram_entries=sum(row["gram_entries"] for row in counts),
                binary_characteristic_polynomial=True)


def unitary_basis(n, phase):
    basis = [[ONE if i == j else ZERO for i in range(n)] for j in range(n)]
    if n >= 2:
        basis[0][:2] = [E(Q(3, 5)), Q(4, 5)*phase]
        basis[1][:2] = [-Q(4, 5)*phase.conjugate(), E(Q(3, 5))]
    else:
        basis[0][0] = phase
    for i, j in product(range(n), repeat=2):
        require(inner(basis[i], basis[j]) == (ONE if i == j else ZERO),
                "Exact complex orthonormal basis")
    return basis


def check_spectral_fixtures():
    records = []
    tests = ((2, 2, (Q(1), Q(0)), Q(0)),
             (2, 2, (Q(1), Q(1)), Q(0)),
             (2, 2, (Q(1), Q(1, 8)), Q(0)),
             (2, 3, (Q(1), Q(1, 3)), Q(1, 5)),
             (3, 4, (Q(1), Q(2, 3), Q(1, 4)), Q(0)),
             (1, 3, (Q(1),), Q(0)),
             (4, 4, (Q(1), Q(1), Q(1), Q(1)), Q(0)))
    sharp = False
    for p, q, weights, negative in tests:
        left = unitary_basis(p, T.OMEGA)
        right = unitary_basis(q, T.OMEGA*T.OMEGA)
        xs = [[w*z for z in left[i]] for i, w in enumerate(weights)]
        ys = [[w*z for z in right[i]] for i, w in enumerate(weights)]
        if negative:
            xs.append([negative*z for z in left[0]])
            ys.append([-negative*z for z in right[0]])
        a2 = sum((norm2(x) for x in xs), Q(0))
        require(a2 == sum((norm2(y) for y in ys), Q(0)), "Balanced row norms")
        singular = [w*w-(negative*negative if i == 0 else 0)
                    for i, w in enumerate(weights)]
        require(singular == sorted(singular, reverse=True) and min(singular) >= 0,
                "Known nonnegative singular values in descending order")
        require(sum(singular) <= a2, "Exact nuclear-norm budget")
        matrix = response_matrix(xs, ys)
        gram = EP.matmul(adjoint(matrix), matrix)
        eigenvectors = []
        eigenvalues = []
        for i, sigma in enumerate(singular):
            for sign in (-1, 1):
                vector = left[i]+[sign*z for z in right[i]]
                value = a2+sign*sigma
                require(apply(gram, vector) == [value*z for z in vector],
                        "Exact Gram eigenvector")
                eigenvectors.append(vector)
                eigenvalues.append(value)
        for i in range(len(singular), p):
            eigenvectors.append(left[i]+[ZERO]*q)
            eigenvalues.append(a2)
        for i in range(len(singular), q):
            eigenvectors.append([ZERO]*p+right[i])
            eigenvalues.append(a2)
        require(len(eigenvectors) == p+q, "Complete rectangular eigenbasis")
        for i, j in product(range(p+q), repeat=2):
            require(bool(inner(eigenvectors[i], eigenvectors[j])) == (i == j),
                    "Orthogonal eigenbasis")
        for vector, value in zip(eigenvectors, eigenvalues):
            require(apply(gram, vector) == [value*z for z in vector],
                    "Complete spectral certificate")
        sorted_values = sorted(eigenvalues)
        require(sorted_values[1] >= a2/2, "Only one potentially weak input direction")
        sharp = sharp or sorted_values[1] == a2/2
        hidden = left[0]+[-z for z in right[0]]
        require(norm2(hidden[:p]) == norm2(hidden[p:]) == 1,
                "Equal component sizes in the weak direction")
        for seed in (1, 2, 3):
            attachment = [E(seed+j, seed-2*j) for j in range(p+q)]
            coefficient = inner(hidden, attachment)/2
            error = [x-v*coefficient for x, v in zip(attachment, hidden)]
            require(not inner(hidden, error), "Orthogonal error decomposition")
            require(a2*norm2(error) <= 2*norm2(apply(matrix, attachment)),
                    "Response controls every perpendicular component")
        records.append(dict(dimensions=[p, q], balanced_squared_norm=str(a2),
                            gram_eigenvalues=[str(v) for v in sorted_values]))
    require(sharp, "Sharp one-half Gram gap attained")

    # K=0 permits any equal-component direction, with no weak singular value.
    xs = [[ONE, ZERO], [ONE, ZERO]]
    ys = [[ONE, ZERO], [E(-1), ZERO]]
    gram = EP.matmul(adjoint(response_matrix(xs, ys)), response_matrix(xs, ys))
    require(gram == [[E(2) if i == j else ZERO for j in range(4)] for i in range(4)],
            "Zero-cross-Gram case")

    # Omitting the balancing changes the norm in the claimed estimate.
    xs, ys = [[E(4), ZERO]], [[E(Q(1, 4)), ZERO]]
    vector = [ZERO, ONE, ZERO, ZERO]
    require(norm2(apply(response_matrix(xs, ys), vector)) == Q(1, 16) < Q(1, 2),
            "Unbalanced input norm invalidates the advertised gap")
    # Conjugation is necessary over complex fields.
    xs, ys = [[ONE, T.OMEGA]], [[T.OMEGA, ONE]]
    true_k = [[xs[0][i]*ys[0][j].conjugate() for j in range(2)] for i in range(2)]
    false_k = [[xs[0][i]*ys[0][j] for j in range(2)] for i in range(2)]
    require(true_k != false_k, "Missing conjugation negative control")
    xs = [[ONE, ZERO], [ONE, ZERO]]
    ys = [[ZERO, ONE], [ZERO, ONE]]
    hidden = [ONE, ZERO, ZERO, E(-1)]
    require(not norm2(apply(response_matrix(xs, ys), hidden))
            and EP.norm2(EP.scaled(EP.outer(hidden[:2], hidden[2:]), 2)) == 4,
            "Zero response can leave a nonzero rank-one product output")
    return dict(fixtures=records, sharp_gram_fraction="1/2",
                zero_cross_gram_checked=True, unbalanced_negative_control=True,
                missing_conjugation_negative_control=True,
                hidden_product_negative_control=True)


def check_product_and_scalar_identities():
    var = Poly.variable
    p, q = [var(f"p_{i}") for i in range(2)], [var(f"q_{i}") for i in range(2)]
    hidden = {j: [var(f"k_{j}_{a}") for a in range(2)] for j in (4, 5)}
    errors = {(root, j, a, b): var(f"e_{root}_{j}_{a}_{b}")
              for root, j, a, b in product(range(2), (4, 5), range(2), range(2))}
    # Use the unnormalised equal-component vector (p,q); the leading factor is 2.
    def component(root, j, a, b):
        return (p if root == 0 else q)[a]*hidden[j][b]+errors[root, j, a, b]
    count = 0
    for a, b, c, d in product(range(2), repeat=4):
        actual = (component(0, 4, a, c)*component(1, 5, b, d)
                  + component(0, 5, a, d)*component(1, 4, b, c))
        leading = 2*p[a]*q[b]*hidden[4][c]*hidden[5][d]
        remainder = (
            p[a]*hidden[4][c]*errors[1, 5, b, d]
            + errors[0, 4, a, c]*q[b]*hidden[5][d]
            + p[a]*hidden[5][d]*errors[1, 4, b, c]
            + errors[0, 5, a, d]*q[b]*hidden[4][c]
            + errors[0, 4, a, c]*errors[1, 5, b, d]
            + errors[0, 5, a, d]*errors[1, 4, b, c])
        require(actual.terms == (leading+remainder).terms, "Product plus controlled remainder")
        count += 1

    a, t, u, d, c = [var(name) for name in ("a", "t", "u", "d", "c")]
    certificates = []
    def record(name, left, right, assumptions):
        require(left.terms == right.terms, "Scalar certificate: " + name)
        certificates.append(dict(name=name, nonnegative_factors=assumptions))
    record("balanced norm dominates the outside edge",
           a*a-c*u*u, (a*a-c*t*u)+c*u*(t-u),
           ["a^2 >= c*t*u", "c,u >= 0", "u <= t"])
    record("response error fits the hidden-amplitude scale",
           a*a*d-c*t*d*u, d*(a*a-c*t*u),
           ["a^2 >= c*t*u", "d >= 0"])
    record("quadratic error after multiplying by the large outside edge",
           a*a*t*d*d-c*u*t*t*d*d, t*d*d*(a*a-c*t*u),
           ["a^2 >= c*t*u", "t >= 0"])
    record("linear error coefficient stays bounded",
           a*a-c*t*t*d*d,
           (a*a-c*t*u)+c*t*(u-d)+c*t*d*(1-t*d),
           ["a^2 >= c*t*u", "c,t,d >= 0", "u >= d", "t*d <= 1"])
    x, y, z, w = [var(name) for name in ("x", "y", "z", "w")]
    record("full column norm envelope",
           (x*x+y*y)*(z*z+w*w)-(x*w+y*z)*(x*w+y*z),
           (x*z-y*w)*(x*z-y*w), ["a square is nonnegative for real inputs"])
    # Every unit core vector removes at most one of the two units of GHZ norm.
    gap_checks = []
    for left in unitary_basis(2, T.OMEGA):
        for right in unitary_basis(2, T.OMEGA*T.OMEGA):
            core = EP.outer(left, right)
            retained = 2-core[0][0].abs2()-core[1][1].abs2()
            require(retained >= 1, "Rank-one core projection retains GHZ signal")
            gap_checks.append(str(retained))
    require(2-ONE.abs2() == 1, "Sharp one-line GHZ projection bound")
    return dict(product_coefficients=count, scalar_certificates=certificates,
                complex_projection_squared_gaps=gap_checks, sharp_projection_squared_gap="1")


def check_quartet_remainders():
    leading = remainder = words = 0
    for quartet in combinations(range(6), 4):
        complement = tuple(v for v in range(6) if v not in quartet)
        for colors in product((1, 2), repeat=4):
            word = dict(zip(quartet, colors))
            word.update({v: 0 for v in complement})
            lcount = rcount = 0
            for matching in T.matchings(tuple(range(6))):
                if complement in matching:
                    require(all(i in quartet and j in quartet
                                for i, j in matching if (i, j) != complement),
                            "Leading ground edge times a quartet matching")
                    lcount += 1
                else:
                    mixed = [(i, j) for i, j in matching if (word[i] == 0) != (word[j] == 0)]
                    binary = [(i, j) for i, j in matching if word[i] and word[j]]
                    require(len(mixed) == 2 and len(binary) == 1
                            and all(v in quartet for v in binary[0]),
                            "Remainder has two mixed edges and one internal binary edge")
                    rcount += 1
            require((lcount, rcount) == (3, 12), "Complete fifteen-matching split")
            leading += lcount
            remainder += rcount
            words += 1
    return dict(quartet_words=words, leading_matchings=leading,
                remainder_matchings=remainder, internal_binary_edge_property=True)


def check_ground_criteria():
    ground = T.original_ground()
    cof = {edge: T.hafnian(ground, tuple(v for v in range(6) if v not in edge))
           for edge in combinations(range(6), 2)}
    def anchored(i, j):
        return bool(cof[tuple(sorted((i, j)))])
    classes = dict(anchored=[], common_neighbor=[], outside_cycle=[], remaining=[])
    for i, j in cof:
        outside = [v for v in range(6) if v not in (i, j)]
        common = any(anchored(i, r) and anchored(j, r) for r in outside)
        cycle = any(all(anchored(r, s) for r in pair for s in outside if s not in pair)
                    for pair in combinations(outside, 2))
        name = ("anchored" if cof[i, j] else "common_neighbor" if common
                else "outside_cycle" if cycle else "remaining")
        classes[name].append([i, j])
    require([len(classes[key]) for key in classes] == [4, 2, 1, 8],
            "Ground-dependent pruning of the thirty single-cell directions")
    require(not T.hafnian(ground, tuple(range(6))) and all(ground.values()),
            "Full-support zero-hafnian ground fixture")
    return dict(cofactor_support=[list(e) for e, c in cof.items() if c],
                edge_classes=classes, remaining_projective_directions=16,
                scope="This exact ground fixture; not a universal count")


def check():
    return dict(formal_gram=check_formal_gram(),
                spectral_gap=check_spectral_fixtures(),
                product_and_scalar_bounds=check_product_and_scalar_identities(),
                quartet_remainders=check_quartet_remainders(),
                ground_criteria=check_ground_criteria(),
                inherited_matching_identities=EP.check_formal_identities())
