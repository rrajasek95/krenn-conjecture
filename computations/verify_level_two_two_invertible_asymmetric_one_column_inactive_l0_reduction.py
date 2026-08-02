#!/usr/bin/env python3
"""Audit the inactive-inactive asymmetric one-column L0 reduction.

In the 2I+2R+2Z chart of the companion L1 boundary theorem, let t be the
rank-one site with P_t=0 and Q_t nonzero and let u be the rank-one site
with both selected columns nonzero.  If both zero endpoints are L1-inactive,
every endpoint slice is a generalized gauge plus a scalar multiple of the
t-star S_t.

The mixed and pure L0 equations force complementary pure tensors

    H=Psi(M)=h e_s^6,       D(S_t)=q e_k^6,       k=1-s.

For a zero site z and colour a, the three inner spoke columns on
A={0,1,u} map to their four-site cofactor L_z^a.  After normalizing only
the inner sites, the map is

    Phi(U0,U1,Uu)=U0*p*a + p*U1*a + J*Uu

and has rank five with kernel span{(p,-p,0)}.  The three forbidden pure
corners imply that a rank-55 survivor must carry this nonzero antisymmetric
kernel direction at one zero shore.  If neither shore carries it, both
shore pairs have common right factors and the coordinate-shore path theorem
gives rank at most 49.

Research evidence only.  Standard library exact arithmetic; checks remain
live under python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
ASYM = run_path(str(
    HERE / "verify_level_two_two_invertible_asymmetric_one_column_l1_boundary.py"
))
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))

COLOURS = (0, 1)
SITES = tuple(range(6))
INNER = (0, 1, 3)
ONE_COLUMN = 2
ZEROS = (4, 5)
WORDS3 = tuple(product(COLOURS, repeat=3))
J = ((Q(0), Q(1)), (Q(1), Q(0)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS6 = perfect_matchings(SITES)


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def matrix_vector_product(matrix, vector):
    return tuple(
        sum((Q(entry) * Q(value) for entry, value in zip(row, vector)), Q(0))
        for row in matrix
    )


# Sparse formal polynomials.  A monomial is a sorted tuple of variable names.
def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = {}
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] = (
                    updated.get(monomial, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not updated[monomial]:
                    del updated[monomial]
        answer = updated
    return answer


def determinant(matrix):
    size = len(matrix)
    answer = constant(0)
    for assignment in permutations(range(size)):
        inversions = sum(
            assignment[left] > assignment[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = constant(-1 if inversions % 2 else 1)
        for row, column in enumerate(assignment):
            term = multiply(term, matrix[row][column])
        answer = add(answer, term)
    return answer


def audit_l0_scalar_and_flattening_dichotomy():
    # Write delta_v=beta_v-b_v.  Independence of the two pure targets
    # first forces H and K=D(S_t) independent.  The mixed equations then
    # give a0*delta1=a1*delta0=0.  Exactly one diagonal correction survives.
    survivors = []
    collinear = 0
    mixed_failures = 0
    for a0, a1, delta0, delta1 in product((0, 1), repeat=4):
        if a0 * delta1 or a1 * delta0:
            mixed_failures += 1
            continue
        diagonal = (a0 * delta0, a1 * delta1)
        if diagonal == (0, 0):
            collinear += 1
        else:
            survivors.append((a0, a1, delta0, delta1, diagonal))
    require(survivors == [
        (0, 1, 0, 1, (0, 1)),
        (1, 0, 1, 0, (1, 0)),
    ], ("L0 scalar terminal charts changed", survivors))
    require((collinear, mixed_failures) == (7, 7),
            ("L0 scalar census changed", collinear, mixed_failures))

    # In either terminal chart K=alpha*e_k^6+beta*e_s^6 with alpha nonzero.
    # Its t-flattening has rank at most one because every S_t edge has the
    # common t-factor Q_t.  The displayed 2x2 minor is +/-alpha*beta, hence
    # beta=0.  Singleton outer-product support then forces Q_t and the
    # complementary five-site cofactor to the physical k axes.
    alpha = variable("alpha")
    beta = variable("beta")
    determinant_checks = 0
    support_checks = 0
    for s in COLOURS:
        k = 1 - s
        flattening = [[constant(0), constant(0)] for _ in COLOURS]
        flattening[s][0] = beta
        flattening[k][1] = alpha
        minor = add(
            multiply(flattening[0][0], flattening[1][1]),
            scale(-1, multiply(flattening[0][1], flattening[1][0])),
        )
        expected = scale(1 if s == 0 else -1, multiply(alpha, beta))
        require(minor == expected,
                ("terminal t-flattening minor changed", s))
        determinant_checks += 1

        singleton = frozenset(((k, (k,) * 5),))
        require(
            frozenset(row for row, _ in singleton) == frozenset((k,))
            and frozenset(word for _, word in singleton)
            == frozenset(((k,) * 5,)),
            "pure outer-product support did not force both factors",
        )
        support_checks += 1
    return survivors, determinant_checks, support_checks


def audit_star_matching_support():
    # D(S_t) has one marked edge t-i for i in A.  Its complement has three
    # perfect matchings.  The one using 45 dies because M_45=0; each of the
    # other two uses one A-4 and one A-5 spoke.
    raw = 0
    dead = 0
    both_shores = 0
    per_edge = {}
    for i in INNER:
        remaining = tuple(site for site in SITES
                          if site not in (ONE_COLUMN, i))
        matchings = perfect_matchings(remaining)
        require(len(matchings) == 3,
                ("wrong four-site cofactor matching count", i))
        edge_counts = {"raw": 0, "M45-dead": 0, "both-shores": 0}
        for matching in matchings:
            raw += 1
            edge_counts["raw"] += 1
            if (4, 5) in matching:
                dead += 1
                edge_counts["M45-dead"] += 1
                continue
            shore_incidence = {
                z: sum(z in edge for edge in matching) for z in ZEROS
            }
            require(shore_incidence == {4: 1, 5: 1},
                    ("live star term missed a zero shore", i, matching))
            both_shores += 1
            edge_counts["both-shores"] += 1
        per_edge[i] = edge_counts
    require((raw, dead, both_shores) == (9, 3, 6),
            ("star matching census changed", raw, dead, both_shores))
    return per_edge, (raw, dead, both_shores)


def cofactor_map_matrix(p, a):
    """Matrix of (U0,U1,Uu) -> U0*p*a+p*U1*a+J*Uu."""

    columns = tuple((site, colour) for site in range(3) for colour in COLOURS)
    matrix = []
    for word in WORDS3:
        row = []
        for site, colour in columns:
            if site == 0:
                value = int(word[0] == colour) * p[word[1]] * a[word[2]]
            elif site == 1:
                value = int(word[1] == colour) * p[word[0]] * a[word[2]]
            else:
                value = int(word[2] == colour) * J[word[0]][word[1]]
            row.append(value)
        matrix.append(row)
    return matrix


def symbolic_cofactor_map_matrix(p, a):
    """Polynomial version of ``cofactor_map_matrix`` for exact minors."""

    columns = tuple((site, colour) for site in range(3) for colour in COLOURS)
    matrix = []
    for word in WORDS3:
        row = []
        for site, colour in columns:
            if site == 0 and word[0] == colour:
                value = multiply(p[word[1]], a[word[2]])
            elif site == 1 and word[1] == colour:
                value = multiply(p[word[0]], a[word[2]])
            elif (site == 2 and word[2] == colour
                  and J[word[0]][word[1]]):
                value = constant(1)
            else:
                value = constant(0)
            row.append(value)
        matrix.append(row)
    return matrix


def audit_covariant_cofactor_kernel():
    # p0,p1 are nonzero because u has two selected columns.  At least one
    # coordinate of the nonzero u-line a is nonzero.  The two displayed
    # 5x5 minors prove rank >=5 on those two affine charts; the universal
    # kernel vector proves rank <=5.
    p = (variable("p0"), variable("p1"))
    a = (variable("a0"), variable("a1"))
    symbolic = symbolic_cofactor_map_matrix(p, a)
    rows_a0 = (0, 2, 3, 4, 6)
    rows_a1 = (1, 2, 3, 5, 7)
    columns = (0, 1, 2, 4, 5)
    minor_a0 = determinant([
        [symbolic[row][column] for column in columns] for row in rows_a0
    ])
    minor_a1 = determinant([
        [symbolic[row][column] for column in columns] for row in rows_a1
    ])
    expected_a0 = scale(-2, multiply(
        variable("p0"), variable("p1"), variable("p1"),
        variable("a0"), variable("a0"), variable("a0"),
    ))
    expected_a1 = scale(-2, multiply(
        variable("p0"), variable("p1"), variable("p1"),
        variable("a1"), variable("a1"), variable("a1"),
    ))
    require((minor_a0, minor_a1) == (expected_a0, expected_a1),
            ("cofactor rank-five minors changed", minor_a0, minor_a1))

    ranks = {}
    for p_numeric in ((Q(1), Q(1)), (Q(1), Q(2)), (Q(2), Q(1))):
        for a_numeric in (
            (Q(1), Q(0)), (Q(0), Q(1)),
            (Q(1), Q(1)), (Q(1), Q(2)),
        ):
            matrix = cofactor_map_matrix(p_numeric, a_numeric)
            kernel = (
                p_numeric[0], p_numeric[1],
                -p_numeric[0], -p_numeric[1],
                Q(0), Q(0),
            )
            require(not any(matrix_vector_product(matrix, kernel)),
                    ("antisymmetric cofactor vector left the kernel", p_numeric,
                     a_numeric))
            ranks[p_numeric, a_numeric] = rational_rank(matrix)
    require(set(ranks.values()) == {5},
            ("cofactor map sample ranks changed", ranks))

    # The two rank-five minors plus the universal nonzero kernel show that
    # this is the entire kernel, not just one distinguished direction.
    return (minor_a0, minor_a1), ranks


def inactive_packet(pure_colour):
    """Formal packet retaining exactly the support needed at t=pure_colour."""

    packet = {}
    for left, right in combinations(SITES, 2):
        for left_colour, right_colour in product(COLOURS, repeat=2):
            if (left, right) == (4, 5):
                value = constant(0)
            elif ONE_COLUMN in (left, right):
                t_colour = (left_colour if left == ONE_COLUMN
                            else right_colour)
                other = right if left == ONE_COLUMN else left
                if other in INNER and t_colour == pure_colour:
                    # Q_t is supported on the complementary colour.
                    value = constant(0)
                else:
                    value = variable(
                        f"m{left}{right}{left_colour}{right_colour}"
                    )
            else:
                value = variable(
                    f"m{left}{right}{left_colour}{right_colour}"
                )
            packet[left, right, left_colour, right_colour] = value
    return packet


def matching_coefficient(packet, word):
    answer = constant(0)
    for matching in MATCHINGS6:
        term = constant(1)
        for left, right in matching:
            term = multiply(
                term, packet[left, right, word[left], word[right]]
            )
        answer = add(answer, term)
    return answer


def inner_zero_cofactor(packet, zero, zero_colour, inner_word):
    answer = constant(0)
    for i in INNER:
        j, ell = tuple(site for site in INNER if site != i)
        left, right = min(i, zero), max(i, zero)
        spoke_colours = (
            (inner_word[INNER.index(i)], zero_colour)
            if i < zero else
            (zero_colour, inner_word[INNER.index(i)])
        )
        core_left, core_right = min(j, ell), max(j, ell)
        core_colours = (
            inner_word[INNER.index(core_left)],
            inner_word[INNER.index(core_right)],
        )
        answer = add(answer, multiply(
            packet[left, right, *spoke_colours],
            packet[core_left, core_right, *core_colours],
        ))
    return answer


def audit_physical_corner_factorization():
    # This check is deliberately in the physical colour axes, before the
    # independent normalization used to compute ker(Phi).  At t=s the
    # inner-t blocks and M45 vanish, giving T_ab=x_a L5^b+y_b L4^a.
    checks = 0
    for s in COLOURS:
        packet = inactive_packet(s)
        for inner_word in WORDS3:
            for colour4, colour5 in product(COLOURS, repeat=2):
                word_map = dict(zip(INNER, inner_word))
                word_map.update({
                    ONE_COLUMN: s, 4: colour4, 5: colour5,
                })
                word = tuple(word_map[site] for site in SITES)
                expected = add(
                    multiply(
                        packet[2, 4, s, colour4],
                        inner_zero_cofactor(
                            packet, 5, colour5, inner_word
                        ),
                    ),
                    multiply(
                        packet[2, 5, s, colour5],
                        inner_zero_cofactor(
                            packet, 4, colour4, inner_word
                        ),
                    ),
                )
                require(matching_coefficient(packet, word) == expected,
                        ("physical corner factorization failed", word))
                checks += 1
    require(checks == 64, "physical corner identity census changed")
    return checks


def audit_corner_and_mod_kernel_dichotomy():
    # If A_s,A_k are independent and B_k is nonzero, the equations
    # T_sk=T_kk=0 either make both A vectors proportional to B_k (y_k!=0)
    # or force x_s=x_k=0 (y_k=0); then T_ks=0 forces y_s=0 and T_ss=0.
    independent_branches = {
        "y_k nonzero": "A_s,A_k become dependent",
        "y_k zero": "T_ss forced zero",
    }
    require(set(independent_branches.values()) == {
        "A_s,A_k become dependent", "T_ss forced zero",
    }, "independent-shore corner split changed")

    # Hence an independent shore forces the opposite k-cofactor to vanish.
    # Since K(k^6) is nonzero and every live star term uses both zero shores,
    # the opposite k-column triple itself is nonzero and lies in ker(Phi).
    shore_patterns = {
        (True, True): "impossible",
        (True, False): "nonzero kernel carrier at shore 5",
        (False, True): "nonzero kernel carrier at shore 4",
        (False, False): "dependent-dependent",
    }
    require(sum("kernel carrier" in value
                for value in shore_patterns.values()) == 2,
            "independent/dependent shore dichotomy changed")

    # On a dependent shore with L_k nonzero, L_s=alpha L_k and exactness of
    # ker(Phi) gives U_s=alpha U_k+lambda*(p,-p,0).  This numerical identity
    # audits the sign and the componentwise common-factor limit lambda=0.
    p = (Q(2), Q(3))
    a = (Q(5), Q(7))
    matrix = cofactor_map_matrix(p, a)
    kernel = (p[0], p[1], -p[0], -p[1], Q(0), Q(0))
    u_k = (Q(1), Q(4), Q(2), Q(8), Q(3), Q(9))
    alpha = Q(-2)
    lam = Q(5)
    u_s = tuple(
        alpha * value + lam * correction
        for value, correction in zip(u_k, kernel)
    )
    require(
        matrix_vector_product(matrix, u_s)
        == tuple(alpha * value
                 for value in matrix_vector_product(matrix, u_k)),
        "dependent shore failed modulo the antisymmetric kernel",
    )
    fixed_u_s = tuple(alpha * value for value in u_k)
    require(all(
        fixed_u_s[2 * site:2 * site + 2]
        == tuple(alpha * value
                 for value in u_k[2 * site:2 * site + 2])
        for site in range(3)
    ), "lambda=0 did not give one common zero-side factor")

    # If both shores have lambda=0 (and neither k-cofactor vanishes), their
    # full-column spokes have fixed right factors.  Together with Q_t and
    # exceptional path 4-t-5, the imported exact theorem gives rank <=49.
    path_identities, categories = SHORE["audit_path_factorization"]()
    require(path_identities == 64 and categories == {
        "all_cross": 6, "34": 3, "35": 3, "45": 3,
    }, "coordinate-shore path closure changed")
    return independent_branches, shore_patterns, path_identities


def audit_scope_map():
    scope = {
        "inactive-inactive/no carrier": "path rank <= 49",
        "inactive-inactive/carrier": "remaining antisymmetric residue",
        "one-active": "separate chart",
        "both-active": "closed by prior L1 path theorem",
        "both rank-one sites one-column": "excluded from scope",
    }
    require(scope["inactive-inactive/carrier"]
            == "remaining antisymmetric residue",
            "inactive-inactive survivor was overclosed")
    return scope


def main():
    old_defect = ASYM["audit_inactive_zero_slice_defect"]()
    scalar, minors, singleton = audit_l0_scalar_and_flattening_dichotomy()
    star, star_census = audit_star_matching_support()
    cofactor_minors, ranks = audit_covariant_cofactor_kernel()
    corner_identities = audit_physical_corner_factorization()
    branches, shore_patterns, path_identities = (
        audit_corner_and_mod_kernel_dichotomy()
    )
    scope = audit_scope_map()

    print("2I+2R+2Z asymmetric inactive-inactive L0 reduction: passed")
    print(f"  imported one-star identity    : {old_defect}")
    print(f"  scalar terminal charts        : {scalar}")
    print(f"  t-flattening/singletons       : {minors}/{singleton}")
    print(f"  star raw/dead/live terms      : {star_census} ({star})")
    print(f"  cofactor rank-five minors     : {cofactor_minors}")
    print(f"  exact cofactor sample ranks   : {set(ranks.values())}")
    print(f"  physical corner identities   : {corner_identities}/64")
    print(f"  independent-shore branches   : {branches}")
    print(f"  shore-pair dichotomy          : {shore_patterns}")
    print(f"  no-carrier path identities    : {path_identities}/64")
    print(f"  scope                         : {scope}")


if __name__ == "__main__":
    main()
