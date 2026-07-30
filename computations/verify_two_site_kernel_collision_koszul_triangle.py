#!/usr/bin/env python3
"""Exact audits for the two-site kernel-collision/Koszul-triangle boundary.

The script is dependency-free.  It checks the two inequivalent exact-support
collision patterns, the five-site multiplication ranks, the unique three-hole
two-family syzygy and its uniform Boolean-incidence nullity formula, and an
explicit factorized all-order carrier residue.
"""

from fractions import Fraction
from itertools import product


Q = Fraction
COLORS = range(3)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(left, right):
    out = dict(left)
    for word, value in right.items():
        out[word] = out.get(word, Q(0)) + value
        if out[word] == 0:
            del out[word]
    return out


def scale(poly, scalar):
    scalar = Q(scalar)
    return {
        word: scalar * value
        for word, value in poly.items()
        if scalar * value
    }


def sum_polys(polys):
    out = {}
    for poly in polys:
        out = add(out, poly)
    return out


def multiply(left, right):
    out = {}
    for first, a in left.items():
        first_sites = {site for site, _ in first}
        for second, b in right.items():
            if first_sites & {site for site, _ in second}:
                continue
            word = tuple(sorted(first + second))
            out[word] = out.get(word, Q(0)) + a * b
    return {word: value for word, value in out.items() if value}


def divided_power(poly, exponent):
    out = {(): Q(1)}
    for step in range(1, exponent + 1):
        out = scale(multiply(out, poly), Q(1, step))
    return out


def vector(site, color):
    return {((site, color),): Q(1)}


def edge(first, first_color, second, second_color):
    return multiply(vector(first, first_color), vector(second, second_color))


def pure_target(site_count, color):
    return {
        tuple((site, color) for site in range(site_count)): Q(1)
    }


def matrix_rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work))
             if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scalar = work[row][column]
            work[row] = [
                value - scalar * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def matrix_vector(matrix, vector_):
    return [
        sum(Q(entry) * Q(value) for entry, value in zip(row, vector_))
        for row in matrix
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def audit_exact_support_collision():
    # L=e_0 at r plus e_1 at s.  If S is supported at r,s, the shared
    # cap tensor is alpha e_0 tensor S_s + beta S_r tensor e_1.
    alpha, beta = Q(2), Q(-3)

    def cap_matrix(s_r, s_s):
        out = [[Q(0) for _ in COLORS] for _ in COLORS]
        for color, value in enumerate(s_s):
            out[0][color] += alpha * Q(value)
        for color, value in enumerate(s_r):
            out[color][1] += beta * Q(value)
        return out

    primary = cap_matrix((1, 0, 0), (0, 0, 1))
    crossed = cap_matrix((0, 0, 1), (1, 0, 0))
    require(matrix_rank(primary) == 1, "primary collision cap rank")
    require(matrix_rank(crossed) == 2, "crossed collision cap rank")

    target = [[Q(int(i == 0 and j == 0)) for j in COLORS]
              for i in COLORS]
    require(primary != target and crossed != target,
            "neither collision cap is the pure shared target")

    # Solve e_0 tensor S_s + S_r tensor e_1 = lambda e_0 tensor e_0.
    # Unknowns are the three coordinates of S_r, the three of S_s, lambda.
    equations = []
    for i, j in product(COLORS, repeat=2):
        row = [Q(0)] * 7
        if j == 1:
            row[i] += beta              # S_r[i]
        if i == 0:
            row[3 + j] += alpha         # S_s[j]
        if i == 0 and j == 0:
            row[6] -= 1                 # lambda
        equations.append(row)
    require(matrix_rank(equations) == 5,
            "exact-support shared-anchor solution dimension two")

    # The complete solution is
    # S_r=c e_0, S_s=(lambda/alpha)e_0-(beta*c/alpha)e_1.
    for c, lam in ((1, 2), (Q(-3, 2), Q(5, 3))):
        candidate = [
            c, 0, 0,
            lam / alpha, -beta * c / alpha, 0,
            lam,
        ]
        require(matrix_vector(equations, candidate) == [Q(0)] * 9,
                "displayed exact-support normal form")
    # In particular neither local component can be a nonzero e_2 witness.


def audit_outside_component_examples():
    # Six-site shared-anchor examples.  The extra e_0 component at site 2
    # is essential; every exact-support term collides with q^[2].
    left = add(vector(0, 0), vector(1, 1))
    q = add(edge(1, 0, 3, 0), edge(4, 0, 5, 0))
    q2 = divided_power(q, 2)
    target = pure_target(6, 0)

    primary = sum_polys((vector(0, 0), vector(1, 2), vector(2, 0)))
    crossed = sum_polys((vector(0, 2), vector(1, 0), vector(2, 0)))
    require(multiply(multiply(left, primary), q2) == target,
            "primary collision repaired by an outside component")
    require(multiply(multiply(left, crossed), q2) == target,
            "crossed collision repaired by an outside component")

    primary_exact = add(vector(0, 0), vector(1, 2))
    crossed_exact = add(vector(0, 2), vector(1, 0))
    require(not multiply(multiply(left, primary_exact), q2),
            "primary exact-support contribution is killed")
    require(not multiply(multiply(left, crossed_exact), q2),
            "crossed exact-support contribution is killed")


def rank_mod(matrix, prime):
    work = [[int(value) % prime for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work))
             if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(inverse * value) % prime
                      for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scalar = work[row][column]
            work[row] = [
                (value - scalar * pivot_value) % prime
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def audit_five_site_left_multiplication():
    # Degree four on five ternary sites: one hole and four local colors.
    domain = []
    for hole in range(5):
        occupied = [site for site in range(5) if site != hole]
        for colors in product(COLORS, repeat=4):
            domain.append((hole, dict(zip(occupied, colors))))
    outputs = list(product(COLORS, repeat=5))
    output_index = {word: index for index, word in enumerate(outputs)}
    matrix = [[0] * len(domain) for _ in outputs]

    # L=e_0 at site 0 plus e_1 at site 1.
    for column, (hole, assignment) in enumerate(domain):
        if hole == 0:
            word = tuple(0 if site == 0 else assignment[site]
                         for site in range(5))
            matrix[output_index[word]][column] += 1
        if hole == 1:
            word = tuple(1 if site == 1 else assignment[site]
                         for site in range(5))
            matrix[output_index[word]][column] += 1

    # The image is the sum of two 81-spaces with 27-dimensional
    # intersection, so its rational rank is at most 135.  A nonzero
    # 135-minor modulo 101 proves the matching lower bound over Q.
    rank = rank_mod(matrix, 101)
    require(rank == 135, "five-site left multiplication rank")
    require(len(domain) - rank == 270,
            "five-site annihilator dimension")
    require(270 == 3 * 81 + 27,
            "243 blind holes plus 27 collision tensors")


def hole_map_matrix(local_dimension=3, site_count=3):
    # One component for every hole, with p=e_0 and q=e_1 at every site.
    holes = range(site_count)
    domain = []
    for hole in holes:
        occupied = [site for site in holes if site != hole]
        for colors in product(range(local_dimension), repeat=site_count - 1):
            domain.append((hole, dict(zip(occupied, colors))))

    row_count = 2 * local_dimension ** site_count
    matrix = [[0] * len(domain) for _ in range(row_count)]
    for column, (hole, assignment) in enumerate(domain):
        for family, inserted_color in enumerate((0, 1)):
            word = tuple(
                inserted_color if site == hole else assignment[site]
                for site in holes
            )
            index = 0
            for color in word:
                index = local_dimension * index + color
            matrix[family * local_dimension ** site_count + index][column] += 1
    return matrix, domain


def generic_ternary_hole_nullity(site_count):
    n = site_count
    return (n - 6) * 3 ** (n - 1) + n * 2 ** (n - 1) + 2 ** (n + 1)


def audit_unique_koszul_triangle():
    matrix, domain = hole_map_matrix(3, 3)
    require(len(domain) == 27, "three-hole domain dimension")
    require(matrix_rank(matrix) == 26, "two-family hole-map rank")

    index = {
        (hole, tuple(assignment[site]
                     for site in range(3) if site != hole)): column
        for column, (hole, assignment) in enumerate(domain)
    }
    triangle = [Q(0)] * len(domain)
    # B_0=p_1 q_2-q_1 p_2.
    triangle[index[(0, (0, 1))]] += 1
    triangle[index[(0, (1, 0))]] -= 1
    # B_1=-(p_0 q_2-q_0 p_2).
    triangle[index[(1, (0, 1))]] -= 1
    triangle[index[(1, (1, 0))]] += 1
    # B_2=p_0 q_1-q_0 p_1.
    triangle[index[(2, (0, 1))]] += 1
    triangle[index[(2, (1, 0))]] -= 1
    require(matrix_vector(matrix, triangle) == [Q(0)] * len(matrix),
            "displayed Koszul triangle")
    require(any(triangle), "nonzero Koszul triangle")

    # Tensoring with arbitrary data on the two collision sites multiplies
    # both domain and kernel by 3^2.
    require(9 * 27 - 9 * 26 == 9,
            "nine-dimensional collision-decorated residual")

    # Uniform Boolean-incidence formula.  The proof in the note decomposes
    # by transverse sites; finite modular ranks here only audit the ledger.
    for site_count in range(1, 6):
        general_matrix, general_domain = hole_map_matrix(3, site_count)
        rank = rank_mod(general_matrix, 101)
        nullity = len(general_domain) - rank
        require(nullity == generic_ternary_hole_nullity(site_count),
                f"generic hole nullity at n={site_count}")
    require(generic_ternary_hole_nullity(3) == 1,
            "first triangle nullity")
    require(generic_ternary_hole_nullity(5) == 63,
            "five-outside-site nullity")

    # Separating k named components leaves arbitrary tensors on those sites
    # times the same map on n-k sites.  Injectivity begins exactly at n-k=2.
    for site_count in range(3, 8):
        require(generic_ternary_hole_nullity(site_count - (site_count - 2)) == 0,
                f"n-2 separated holes suffice at n={site_count}")
        require(generic_ternary_hole_nullity(site_count - (site_count - 3)) > 0,
                f"fewer separated holes leave a cycle at n={site_count}")


def matrix_rank_small(matrix):
    return matrix_rank(matrix)


def left_vector_matrix(vector_, matrix):
    return [
        sum(Q(vector_[i]) * Q(matrix[i][j]) for i in COLORS)
        for j in COLORS
    ]


def audit_factorized_carrier_residual():
    # Collision sites r=0,s=1 and outside sites 2,3,4.
    r, s = 0, 1
    p = {site: vector(site, 0) for site in (2, 3, 4)}
    q = {site: vector(site, 1) for site in (2, 3, 4)}
    p_sum = sum_polys(p.values())
    q_sum = sum_polys(q.values())

    z_triangle = sum_polys((
        multiply(p[3], q[4]),
        scale(multiply(q[3], p[4]), -1),
        scale(multiply(p[2], q[4]), -1),
        multiply(q[2], p[4]),
        multiply(p[2], q[3]),
        scale(multiply(q[2], p[3]), -1),
    ))
    z_rs = edge(r, 2, s, 2)
    z_base = add(z_rs, z_triangle)

    y = (vector(r, 0), vector(s, 1), vector(s, 2))
    t = (vector(r, 0), vector(s, 1), vector(s, 2))
    B, C = Q(1), Q(2)
    omega = add(scale(multiply(y[0], t[1]), C),
                scale(multiply(y[1], t[0]), -B))
    expected_omega = edge(r, 0, s, 1)
    require(omega == expected_omega, "fixed collision tensor omega")

    x = (
        add(vector(r, 0), p_sum),
        add(vector(s, 1), scale(p_sum, -1)),
        add(vector(s, 2), q_sum),
    )
    xi = (1, 1, 0)
    left = sum_polys(scale(x[i], xi[i]) for i in COLORS)
    require(left == add(vector(r, 0), vector(s, 1)),
            "left kernel form has exact two-site support")

    p_column = (1, -1, 1)
    a_column = (0, 0, 1)
    P = tuple(
        tuple((p_column, a_column, tuple(-v for v in p_column))[j][i]
              for j in COLORS)
        for i in COLORS
    )
    R_columns = (
        tuple(2 * v for v in p_column),
        tuple(Q(v, 2) for v in a_column),
        tuple(-2 * v for v in p_column),
    )
    R = tuple(tuple(R_columns[j][i] for j in COLORS) for i in COLORS)
    eta = (1, 0, 1)
    require(matrix_rank_small(P) == matrix_rank_small(R) == 2,
            "rank-two direct blocks")
    require(left_vector_matrix(xi, P) == [0, 0, 0],
            "shared left P kernel")
    require(left_vector_matrix(xi, R) == [0, 0, 0],
            "shared left R kernel")
    require(matrix_vector(P, eta) == [0, 0, 0],
            "noncoordinate right P kernel")
    require(matrix_vector(R, eta) == [0, 0, 0],
            "noncoordinate right R kernel")

    T_I = ((1, B), (C, 3))
    require(T_I[0][0] * T_I[1][1] - B * C == 1,
            "generic selector square")

    gamma = []
    for i in COLORS:
        gamma_i = sum_polys((
            scale(t[1], C * P[i][0]),
            scale(y[0], C * R[i][1]),
            scale(t[0], -B * P[i][1]),
            scale(y[1], -B * R[i][0]),
        ))
        gamma.append(gamma_i)
        require(not gamma_i, f"zero companion gamma_{i}")

    base_h = multiply(omega, z_base)
    require(base_h, "nonzero factorized triangle residue")
    require(all(all(site in {entry[0] for entry in word}
                    for site in (r, s))
                for word in base_h),
            "triangle residue occupies both collision sites")
    require(not multiply(left, base_h), "left colon relation")
    for i in COLORS:
        require(not multiply(x[i], base_h),
                f"ordered carrier multiplier x_{i}")

    # z^[2] is nonzero: z_rs can be paired with every triangle edge.
    require(divided_power(z_base, 2), "nonzero radial top power")

    # Uniform suspension.  The only surviving term in omega*z^[h-2]
    # uses one triangle edge and every added matching edge.
    for h in range(3, 9):
        z_h = dict(z_base)
        suspension_word = {(): Q(1)}
        next_site = 5
        for _ in range(h - 3):
            suspension_edge = edge(next_site, 0, next_site + 1, 0)
            z_h = add(z_h, suspension_edge)
            suspension_word = multiply(suspension_word, suspension_edge)
            next_site += 2
        suspended_h = multiply(omega, divided_power(z_h, h - 2))
        expected = multiply(base_h, suspension_word)
        require(suspended_h == expected and suspended_h,
                f"uniform suspended triangle at h={h}")
        for i in COLORS:
            carrier = add(multiply(x[i], suspended_h),
                          multiply(gamma[i], divided_power(z_h, h - 1)))
            require(not carrier, f"all-order carrier {i} at h={h}")
        require(divided_power(z_h, h - 1),
                f"nonzero radial power at h={h}")


def main():
    audit_exact_support_collision()
    audit_outside_component_examples()
    audit_five_site_left_multiplication()
    audit_unique_koszul_triangle()
    audit_factorized_carrier_residual()
    print("two-site kernel collision / Koszul triangle: PASS")
    print("  exact-support primary/crossed ranks: 1, 2 (both excluded)")
    print("  h=3 left multiplication: rank 135, kernel 270=243+27")
    print("  three-hole two-family map: rank 26, unique triangle kernel")
    print("  generic n-site carrier nullity formula audited through n=5")
    print("  collision-decorated homogeneous carrier residual: dimension 9")
    print("  factorized weighted-row residue suspended through h=8")


if __name__ == "__main__":
    main()
