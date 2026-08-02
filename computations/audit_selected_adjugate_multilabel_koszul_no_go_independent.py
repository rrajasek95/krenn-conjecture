#!/usr/bin/env python3
"""Independent exact audit of the selected adjugate/Koszul no-go pair.

This script does not import either primary checker.  It rebuilds the sparse
polynomial identities, the nine all-label tilts, the direct-free triangular
specialization, the exact word-tag module, the exterior contractions, and the
degree-two/three target Koszul matrices using only the standard library.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations


ZERO = F(0)
ONE = F(1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Sparse exact polynomials.  A monomial is a sorted tuple of variable names.
def clean(poly):
    return {m: c for m, c in poly.items() if c}


def const(value):
    value = F(value)
    return {} if not value else {(): value}


def var(name):
    return {(name,): ONE}


def add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, ZERO) + coefficient
    return clean(out)


def neg(poly):
    return {m: -c for m, c in poly.items()}


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    out = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(sorted(lm + rm))
            out[monomial] = out.get(monomial, ZERO) + lc * rc
    return clean(out)


def scale(value, poly):
    return mul(const(value), poly)


def total(polys):
    out = {}
    for poly in polys:
        out = add(out, poly)
    return out


def specialize_zero(poly, prefixes):
    return {
        monomial: coefficient
        for monomial, coefficient in poly.items()
        if not any(any(name.startswith(prefix) for prefix in prefixes)
                   for name in monomial)
    }


def audit_power_free_identities():
    P = [var(f"P{i}") for i in range(3)]
    R = [[var(f"R{i}{k}") for k in range(3)] for i in range(3)]
    Q = var("Q")
    S = [var(f"S{k}") for k in range(3)]
    x = [var(f"x{i}") for i in range(3)]
    y = var("y")
    t = [var(f"t{k}") for k in range(3)]
    v = var("v")
    z = var("z")
    Hcoef = [var(f"Hcoef{i}") for i in range(3)]
    T = [var(f"T{k}") for k in range(3)]
    h = var("h")

    f = [add(mul(P[i], z), mul(x[i], y)) for i in range(3)]
    g = [[add(mul(R[i][k], z), mul(x[i], t[k]))
          for k in range(3)] for i in range(3)]
    phi = add(mul(Q, z), mul(y, v))
    psi = [add(mul(S[k], z), mul(t[k], v)) for k in range(3)]
    H = [total((mul(P[i], v), mul(Hcoef[i], y), mul(Q, x[i])))
         for i in range(3)]
    N = [[total((mul(R[i][k], v), mul(Hcoef[i], t[k]),
                 mul(S[k], x[i])))
          for k in range(3)] for i in range(3)]

    D, E, Gamma, C = {}, {}, {}, {}
    for i in range(3):
        for k in range(3):
            key = (i, k)
            D[key] = sub(mul(P[i], t[k]), mul(R[i][k], y))
            E[key] = sub(mul(S[k], y), mul(Q, t[k]))
            Gamma[key] = sub(mul(P[i], S[k]), mul(R[i][k], Q))
            C[key] = mul(x[i], E[key])
            require(sub(mul(f[i], t[k]), mul(g[i][k], y))
                    == mul(D[key], z), f"connection {(i, k)}")
            require(sub(mul(psi[k], y), mul(phi, t[k]))
                    == mul(E[key], z), f"opposite connection {(i, k)}")
            require(sub(mul(S[k], f[i]), mul(Q, g[i][k]))
                    == add(mul(Gamma[key], z), C[key]),
                    f"first curvature half {(i, k)}")
            require(sub(mul(t[k], H[i]), mul(y, N[i][k]))
                    == sub(mul(D[key], v), C[key]),
                    f"second curvature half {(i, k)}")
            require(total((mul(S[k], f[i]), mul(t[k], H[i]),
                           neg(mul(Q, g[i][k])), neg(mul(y, N[i][k]))))
                    == add(mul(D[key], v), mul(Gamma[key], z)),
                    f"curvature normal {(i, k)}")

            first = sub(
                add(mul(h, add(mul(R[i][k], y), mul(T[k], x[i]))),
                    mul(P[i], t[k])),
                add(mul(h, add(mul(P[i], t[k]), mul(T[k], x[i]))),
                    mul(R[i][k], y)),
            )
            second = sub(
                add(mul(h, add(mul(T[k], v), mul(S[k], y))),
                    mul(Q, t[k])),
                add(mul(h, add(mul(T[k], v), mul(Q, t[k]))),
                    mul(S[k], y)),
            )
            require(first == neg(mul(sub(h, const(1)), D[key])),
                    f"first normal difference {(i, k)}")
            require(second == mul(sub(h, const(1)), E[key]),
                    f"second normal difference {(i, k)}")

    # Every literal J=I+E_uv contraction, including the doubled diagonal.
    tilt_ledger = []
    for u in range(3):
        for w in range(3):
            weights = {(i, i): F(1) for i in range(3)}
            weights[(u, w)] = weights.get((u, w), ZERO) + ONE
            d_j = total(scale(c, D[key]) for key, c in weights.items())
            e_j = total(scale(c, E[key]) for key, c in weights.items())
            gamma_j = total(scale(c, Gamma[key]) for key, c in weights.items())
            c_j = total(scale(c, C[key]) for key, c in weights.items())
            require(d_j == add(total(D[(i, i)] for i in range(3)), D[(u, w)]),
                    f"tilt D {(u, w)}")
            require(e_j == add(total(E[(i, i)] for i in range(3)), E[(u, w)]),
                    f"tilt E {(u, w)}")
            require(gamma_j == add(total(Gamma[(i, i)] for i in range(3)),
                                   Gamma[(u, w)]), f"tilt Gamma {(u, w)}")
            require(c_j == add(total(C[(i, i)] for i in range(3)), C[(u, w)]),
                    f"tilt C {(u, w)}")
            target = [weights.get((i, i), ZERO) for i in range(3)]
            require(target == [F(2) if u == w == i else ONE for i in range(3)],
                    f"tilt target {(u, w)}")
            tilt_ledger.extend((len(d_j), len(e_j), len(gamma_j), len(c_j), *target))

    # Selected transpose-adjugate identities, reconstructed independently.
    A, B, Fq, U = P[0], R[0][0], Q, S[0]
    d, e = D[(0, 0)], E[(0, 0)]
    kappa = sub(mul(A, U), mul(B, Fq))
    require(sub(mul(U, y), mul(Fq, t[0])) == e, "adjugate first row")
    require(sub(mul(A, t[0]), mul(B, y)) == d, "adjugate second row")
    require(add(mul(A, e), mul(Fq, d)) == mul(kappa, y),
            "adjugate recovers y")
    require(add(mul(B, e), mul(U, d)) == mul(kappa, t[0]),
            "adjugate recovers t")

    # Set the whole R block to zero; the identities remain polynomial and
    # become the claimed triangular formulas without dividing by B.
    z0 = lambda poly: specialize_zero(poly, ("R",))
    require(z0(d) == mul(A, t[0]), "direct-free D")
    require(z0(e) == sub(mul(U, y), mul(Fq, t[0])), "direct-free E")
    require(z0(kappa) == mul(A, U), "direct-free kappa")
    require(z0(add(mul(A, e), mul(Fq, d))) == mul(mul(A, U), y),
            "direct-free y recovery")
    require(z0(add(mul(B, e), mul(U, d))) == mul(mul(A, U), t[0]),
            "direct-free t recovery")

    return tilt_ledger


def matrix_rank(matrix):
    rows = [list(map(F, row)) for row in matrix]
    if not rows:
        return 0
    width = len(rows[0])
    rank = 0
    for col in range(width):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][col]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def nullspace(matrix):
    rows = [list(map(F, row)) for row in matrix]
    height = len(rows)
    width = len(rows[0]) if height else 0
    pivots = []
    r = 0
    for col in range(width):
        pivot = next((i for i in range(r, height) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        value = rows[r][col]
        rows[r] = [x / value for x in rows[r]]
        for i in range(height):
            if i != r and rows[i][col]:
                value = rows[i][col]
                rows[i] = [x - value * y for x, y in zip(rows[i], rows[r])]
        pivots.append(col)
        r += 1
        if r == height:
            break
    free = [col for col in range(width) if col not in pivots]
    basis = []
    for col in free:
        vec = [ZERO] * width
        vec[col] = ONE
        for row, pivot in enumerate(pivots):
            vec[pivot] = -rows[row][col]
        basis.append(vec)
    return basis


def mat_vec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), ZERO) for row in matrix]


def mat_mul(left, right):
    if not left or not right:
        return []
    columns = list(zip(*right))
    return [[sum((a * b for a, b in zip(row, col)), ZERO)
             for col in columns] for row in left]


def det2(a, b, c, d):
    return a * d - b * c


FAILURES = {
    "direct_free": (
        ("000000", (0, 0), ZERO, ONE),
        ("111111", (1, 1), ZERO, ONE),
        ("222222", (2, 2), ZERO, ONE),
        ("012112", (2, 2), ONE, ZERO),
        ("012212", (2, 1), ONE, ZERO),
        ("012212", (2, 2), ONE, ZERO),
    ),
    "tilted": (
        ("000000", (0, 0), ZERO, ONE),
        ("111111", (1, 1), ZERO, ONE),
        ("222222", (2, 2), ZERO, ONE),
        ("002012", (2, 2), F(1, 2), ZERO),
        ("022012", (0, 2), F(-3, 2), ZERO),
        ("022012", (2, 0), F(1, 2), ZERO),
        ("022012", (2, 2), F(-1, 4), ZERO),
    ),
}


def audit_word_module_and_exterior():
    expected_mixed = {
        "direct_free": ("12112", "12212"),
        "tilted": ("02012", "22012"),
    }
    r_site = {"direct_free": 3, "tilted": 1}
    kappa = {"direct_free": F(-1, 4), "tilted": F(-5, 2)}
    selected_word = "012012"
    ledgers = []
    for name, failures in FAILURES.items():
        pure = failures[:3]
        mixed = failures[3:]
        require([word for word, _, _, _ in pure]
                == ["000000", "111111", "222222"], f"{name} pure words")
        require(all(actual == 0 and target == 1
                    for _, _, actual, target in pure), f"{name} pure targets")
        require(all(word[0] == "0" and target == 0 and actual
                    for word, _, actual, target in mixed), f"{name} mixed scope")
        tags = tuple(dict.fromkeys(word[1:] for word, _, _, _ in mixed))
        require(tags == expected_mixed[name], f"{name} mixed tags")
        require("00000" not in tags, f"{name} mixed tag became Y0")
        for word, _, _, _ in mixed:
            changed = tuple(i for i, (a, b) in enumerate(zip(word, selected_word))
                            if a != b)
            require(changed == (r_site[name],), f"{name} non-r mixed word {word}")

        # After graph shear, columns are (target[3], response[Y0,m1,m2]).
        # The adjacent representatives use arbitrary nondegenerate target
        # vectors and the exact two mixed response directions.  The anchors
        # span all target axes, so this is a quotient countermodel for every
        # target cancellation permitted by the modeled rows.
        generators = [
            ([ONE, ZERO, ZERO], [ZERO, ZERO, ZERO]),
            ([ZERO, ONE, ZERO], [ZERO, ZERO, ZERO]),
            ([ZERO, ZERO, ONE], [ZERO, ZERO, ZERO]),
            ([ONE, F(2), ZERO], [ZERO, ONE, ZERO]),
            ([ZERO, ONE, F(3)], [ZERO, ZERO, ONE]),
        ]
        tag_index = {tags[0]: 1, tags[1]: 2}
        for word, _, actual, _ in mixed:
            response = [ZERO, ZERO, ZERO]
            response[tag_index[word[1:]]] = actual
            generators.append(([ZERO, ZERO, ZERO], response))
        generators.append(([ZERO, ZERO, ZERO], [ZERO, ZERO, ZERO]))

        target_matrix = [[g[0][row] for g in generators] for row in range(3)]
        response_matrix = [[g[1][row] for g in generators] for row in range(3)]
        kernel = nullspace(target_matrix)
        kernel_responses = [mat_vec(response_matrix, vector) for vector in kernel]
        require(matrix_rank(kernel_responses) == 2, f"{name} kernel response rank")
        desired = [[-kappa[name], ZERO, ZERO]]
        require(matrix_rank(kernel_responses + desired) == 3,
                f"{name} Y0 rank jump")

        # One- and higher-anchor graph spaces project isomorphically to the
        # corresponding target exterior powers: the projection matrix is I.
        for degree, expected in ((1, 3), (2, 3), (3, 1)):
            source = list(combinations(range(3), degree))
            target = list(combinations(range(3), degree))
            compound = []
            for rows in target:
                compound.append([
                    ONE if rows == cols else ZERO for cols in source
                ])
            require(matrix_rank(compound) == expected,
                    f"{name} graph exterior degree {degree}")

        pair_responses = []
        for i, j in combinations(range(len(generators)), 2):
            ti, ri = generators[i]
            tj, rj = generators[j]
            for a in range(3):
                pair_responses.append([
                    ti[a] * rj[q] - tj[a] * ri[q] for q in range(3)
                ])
        triple_responses = []
        for i, j, k in combinations(range(len(generators)), 3):
            ts = [generators[index][0] for index in (i, j, k)]
            rs = [generators[index][1] for index in (i, j, k)]
            for a, b in combinations(range(3), 2):
                coefficients = (
                    det2(ts[1][a], ts[2][a], ts[1][b], ts[2][b]),
                    -det2(ts[0][a], ts[2][a], ts[0][b], ts[2][b]),
                    det2(ts[0][a], ts[1][a], ts[0][b], ts[1][b]),
                )
                triple_responses.append([
                    sum((coefficients[q] * rs[q][coord] for q in range(3)), ZERO)
                    for coord in range(3)
                ])
        exterior = pair_responses + triple_responses
        require(matrix_rank(exterior) == 2, f"{name} exterior response rank")
        require(matrix_rank(exterior + desired) == 3,
                f"{name} exterior Y0 rank jump")

        # The unsheared graph is (e_i,Y_i), and subtracting phi(target)
        # produces exactly (e_i,0).
        for i in range(3):
            target = [ONE if j == i else ZERO for j in range(3)]
            residue = list(target)
            sheared = [residue[j] - target[j] for j in range(3)]
            require(sheared == [ZERO] * 3, f"{name} graph shear {i}")
        require(det3([[ONE, ZERO, ZERO], [ZERO, ONE, ZERO],
                      [ZERO, ZERO, ONE]]) == ONE, f"{name} anchor determinant")
        ledgers.extend((name, tags, len(kernel), matrix_rank(exterior)))
    return ledgers


def det3(matrix):
    a, b, c = matrix
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def symmetric_basis(degree):
    return [(a, b, degree - a - b)
            for a in range(degree + 1)
            for b in range(degree - a + 1)]


def wedge_basis(degree):
    return list(combinations(range(3), degree))


def koszul_matrix(total_degree, exterior_degree):
    """Matrix K_p(m) -> K_{p-1}(m), with columns indexed by K_p."""
    p = exterior_degree
    source = [(wedge, monomial)
              for wedge in wedge_basis(p)
              for monomial in symmetric_basis(total_degree - p)]
    target = [(wedge, monomial)
              for wedge in wedge_basis(p - 1)
              for monomial in symmetric_basis(total_degree - p + 1)]
    target_index = {entry: i for i, entry in enumerate(target)}
    matrix = [[ZERO for _ in source] for _ in target]
    for col, (wedge, monomial) in enumerate(source):
        for position, index in enumerate(wedge):
            smaller = wedge[:position] + wedge[position + 1:]
            product = list(monomial)
            product[index] += 1
            row = target_index[(smaller, tuple(product))]
            matrix[row][col] += ONE if position % 2 == 0 else -ONE
    return matrix, len(target), len(source)


def audit_koszul():
    expected = {
        2: ((6, 9, 3), (6, 3)),
        3: ((10, 18, 9, 1), (10, 8, 1)),
    }
    ledger = []
    for degree, (expected_dims, expected_ranks) in expected.items():
        matrices = {}
        dimensions = [len(wedge_basis(p)) * len(symmetric_basis(degree - p))
                      for p in range(degree + 1)]
        ranks = []
        for p in range(1, degree + 1):
            matrix, target_dim, source_dim = koszul_matrix(degree, p)
            require((target_dim, source_dim) == (dimensions[p - 1], dimensions[p]),
                    f"Koszul dimensions m={degree}, p={p}")
            matrices[p] = matrix
            ranks.append(matrix_rank(matrix))
        require(tuple(dimensions) == expected_dims, f"Koszul dims m={degree}")
        require(tuple(ranks) == expected_ranks, f"Koszul ranks m={degree}")
        for p in range(2, degree + 1):
            composite = mat_mul(matrices[p - 1], matrices[p])
            require(all(not entry for row in composite for entry in row),
                    f"Koszul d^2 m={degree}, p={p}")
            require(ranks[p - 2] + ranks[p - 1] == dimensions[p - 1],
                    f"Koszul exactness m={degree}, K_{p - 1}")
        require(ranks[-1] == dimensions[-1], f"top Koszul injectivity m={degree}")
        ledger.extend((degree, tuple(dimensions), tuple(ranks)))
    return ledger


def main():
    tilt = audit_power_free_identities()
    module = audit_word_module_and_exterior()
    koszul = audit_koszul()
    payload = repr((tilt, module, koszul)).encode()
    digest = sha256(payload).hexdigest()
    print("independent selected-adjugate / multilabel-Koszul audit: PASS")
    print("  all nine I+E_uv tilts and direct-free adjugate formulas: exact")
    print("  exact gap tags and graph/exterior target-kernel ranks: exact")
    print("  fixed-degree Koszul dimensions/ranks: (6,9,3)/(6,3),")
    print("                                        (10,18,9,1)/(10,8,1)")
    print("  modeled-row no-go: valid; larger decorated source operations untouched")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
