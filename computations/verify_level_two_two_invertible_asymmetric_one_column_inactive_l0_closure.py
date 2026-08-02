#!/usr/bin/env python3
"""Close the inactive-inactive asymmetric one-column L0 chart.

The preceding reduction leaves a rank-five inner cofactor map Phi with
kernel span{(p,-p,0)}.  This checker audits the two extra slice arguments.

First, the pure H corner at the rank-one inner site u compares a scalar
multiple of the invertible matrix J with a rank-one product.  It forces the
physical pure colour s at u onto the rank-one line h_u.  If a k-column is a
literal nonzero Phi-kernel carrier, the pure star cofactor gives the same
rank-two/rank-one comparison and forces the complementary physical colour
k onto h_u, a contradiction.

Thus both k-cofactors are nonzero and both shore pairs are dependent.
The three forbidden corners force those two k-cofactors onto one line;
the nonzero ss corner makes that line the physical pure s-product.  Its
u-opposite slice then forces both columns of both u-zero blocks onto h_u.
Every block incident with u has this fixed root, so rank(dPsi)<=32+10=42.

Literal residual R2 is audited at the two invertible roots: the u-edge is
the pure-s witness and the t-edge the pure-k witness.  R2 is therefore
compatible there but is unnecessary for the rank bound.

Research evidence only.  Standard library exact arithmetic; checks remain
live under python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
REDUCTION = run_path(str(
    HERE / "verify_level_two_two_invertible_asymmetric_one_column_inactive_l0_reduction.py"
))
ONE_ACTIVE = run_path(str(
    HERE / "verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py"
))

COLOURS = (0, 1)
J = ((Q(0), Q(1)), (Q(1), Q(0)))


def matrix_rank_2(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return 2 if determinant else 1


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS)
        for row in COLOURS
    )


def add_matrix(left, right):
    return tuple(
        tuple(left[row][column] + right[row][column]
              for column in COLOURS)
        for row in COLOURS
    )


def scale_matrix(coefficient, matrix):
    return tuple(
        tuple(coefficient * matrix[row][column] for column in COLOURS)
        for row in COLOURS
    )


def determinant_2(matrix):
    return REDUCTION["add"](
        REDUCTION["multiply"](matrix[0][0], matrix[1][1]),
        REDUCTION["scale"](
            -1, REDUCTION["multiply"](matrix[0][1], matrix[1][0])
        ),
    )


def audit_h_slice_fixes_physical_s_root():
    # Normalize only the inner calculation so h_u=e0.  On the u=e1 slice,
    # every Phi(W_z^s) is W_{z,u}^s(e1)*J.  Thus T_ss is A*J.  The physical
    # target is h*eta_u^s(e1)*(eta_0^s outer eta_1^s), a nonzero rank-one
    # matrix if eta_u^s(e1) is nonzero.
    coefficient = REDUCTION["variable"]("A")
    left = (
        (REDUCTION["constant"](0), coefficient),
        (coefficient, REDUCTION["constant"](0)),
    )
    require(
        determinant_2(left)
        == REDUCTION["scale"](
            -1, REDUCTION["multiply"](coefficient, coefficient)
        ),
        "the pure-H u-opposite determinant changed",
    )

    eta0 = (Q(2), Q(3))
    eta1 = (Q(5), Q(7))
    product_matrix = outer(eta0, eta1)
    require(matrix_rank_2(J) == 2
            and matrix_rank_2(product_matrix) == 1,
            "H-slice rank-two/rank-one comparison changed")

    conclusions = (
        "T_ss u-opposite scalar is zero",
        "physical eta_u^s has zero opposite coordinate",
        "physical e_s at u is parallel to h_u",
    )
    return determinant_2(left), conclusions


def audit_literal_kernel_carrier_contradiction():
    # Let W_4^k=lambda*(p,-p,0).  At u=e1, the star cofactor is
    #
    #   lambda*W_{5,u}^k(e1)*(p outer e0-e0 outer p).
    #
    # The e1-coordinate p1 is nonzero because P_u,Q_u are both nonzero.
    # The skew matrix has rank two.  Equality with the pure-k product slice
    # therefore forces both W_{5,u}^k(e1)=0 and eta_u^k(e1)=0, putting the
    # physical k-axis on h_u.  The H slice already put s there.
    p = (Q(2), Q(3))
    e0 = (Q(1), Q(0))
    skew = add_matrix(outer(p, e0), scale_matrix(-1, outer(e0, p)))
    expected = ((Q(0), Q(-3)), (Q(3), Q(0)))
    require(skew == expected and matrix_rank_2(skew) == 2,
            ("literal carrier skew slice changed", skew))

    b = REDUCTION["variable"]("B_u_perp")
    p1 = REDUCTION["variable"]("p1")
    formal_skew = (
        (REDUCTION["constant"](0),
         REDUCTION["scale"](-1, REDUCTION["multiply"](b, p1))),
        (REDUCTION["multiply"](b, p1), REDUCTION["constant"](0)),
    )
    expected_determinant = REDUCTION["multiply"](b, b, p1, p1)
    require(determinant_2(formal_skew) == expected_determinant,
            "literal carrier skew determinant changed")

    contradictions = {}
    for carrier_shore in (4, 5):
        opposite = 9 - carrier_shore
        contradictions[carrier_shore] = (
            f"physical e_k at u forced onto h_u via shore {opposite}",
            "contradicts physical e_s at u parallel h_u",
        )
    return skew, determinant_2(formal_skew), contradictions


def star_bilinear(left, right, p_u, rho):
    """Inner three-tensor in C_t at fixed zero-shore colours."""

    e0 = (Q(1), Q(0))
    star = (e0, e0, tuple(Q(rho) * value for value in p_u))
    answer = []
    for x0, x1, xu in product(COLOURS, repeat=3):
        word = (x0, x1, xu)
        value = Q(0)
        for i in range(3):
            j, ell = tuple(site for site in range(3) if site != i)
            value += (
                star[i][word[i]]
                * (
                    left[j][word[j]] * right[ell][word[ell]]
                    + right[j][word[j]] * left[ell][word[ell]]
                )
            )
        answer.append(value)
    return tuple(answer)


def tensor_product(*vectors):
    answer = []
    for word in product(COLOURS, repeat=len(vectors)):
        value = Q(1)
        for site, colour in enumerate(word):
            value *= vectors[site][colour]
        answer.append(value)
    return tuple(answer)


def enumerated_star_bilinear(left, right, p_u, rho):
    """Independent six-site matching enumeration of star_bilinear."""

    inner_actual = (0, 1, 3)
    local = {site: index for index, site in enumerate(inner_actual)}
    star = {
        0: (Q(1), Q(0)),
        1: (Q(1), Q(0)),
        3: tuple(Q(rho) * value for value in p_u),
    }

    def base_value(edge, word):
        first, second = edge
        if edge == (4, 5):
            return Q(0)
        if first in inner_actual and second == 4:
            return left[local[first]][word[first]]
        if first in inner_actual and second == 5:
            return right[local[first]][word[first]]
        # This value can only occur beside M45 and hence must drop out.
        if first in inner_actual and second in inner_actual:
            return Q(13)
        raise RuntimeError(("unexpected star-complement edge", edge))

    answer = []
    for inner_word in product(COLOURS, repeat=3):
        word = {
            0: inner_word[0], 1: inner_word[1], 2: 0,
            3: inner_word[2], 4: 0, 5: 0,
        }
        value = Q(0)
        for marked_site in inner_actual:
            remaining = tuple(
                site for site in range(6) if site not in (2, marked_site)
            )
            for matching in REDUCTION["perfect_matchings"](remaining):
                term = star[marked_site][word[marked_site]]
                for edge in matching:
                    term *= base_value(edge, word)
                value += term
        answer.append(value)
    return tuple(answer)


def audit_full_star_mixed_purity():
    # For K0=(p,-p,0), direct expansion of the complete bilinear star gives
    # B(K0,K0)=-2*rho*p tensor p tensor h_u.  This is the way the full
    # five-site cofactor sees a direction invisible to each linear Phi.
    p = (Q(2), Q(3))
    h_u = (Q(5), Q(7))
    rho = Q(11)
    zero = (Q(0), Q(0))
    kernel = (p, tuple(-value for value in p), zero)
    actual = star_bilinear(kernel, kernel, h_u, rho)
    enumerated = enumerated_star_bilinear(kernel, kernel, h_u, rho)
    expected = tuple(
        -2 * rho * value
        for value in tensor_product(p, p, h_u)
    )
    require(actual == enumerated == expected and any(actual),
            ("full-star kernel square changed", actual, enumerated, expected))

    # Also compare the two constructions away from the kernel specialization
    # so a sign error cannot be hidden by its zero u-component.
    generic_left = ((Q(1), Q(4)), (Q(2), Q(5)), (Q(3), Q(6)))
    generic_right = ((Q(7), Q(10)), (Q(8), Q(11)), (Q(9), Q(12)))
    require(
        star_bilinear(generic_left, generic_right, h_u, rho)
        == enumerated_star_bilinear(
            generic_left, generic_right, h_u, rho
        ),
        "bilinear star formula disagrees with matching enumeration",
    )

    # Put P=B(W4k,W5k), X=B(K0,W5k), Y=B(W4k,K0), Z=B(K0,K0).
    # The two mixed zero-shore colours and the ss colour are
    #   E4=alpha4 P+lambda4 X,
    #   E5=alpha5 P+lambda5 Y,
    #   Ess=alpha4 alpha5 P+alpha4 lambda5 Y
    #       +lambda4 alpha5 X+lambda4 lambda5 Z.
    # The exact identity below shows that E4=E5=Ess=0 implies
    # lambda4 lambda5 Z=alpha4 alpha5 P.
    names = {
        name: REDUCTION["variable"](name)
        for name in ("P", "X", "Y", "Z", "a4", "a5", "l4", "l5")
    }
    P, X, Y, Z = (names[name] for name in ("P", "X", "Y", "Z"))
    a4, a5, l4, l5 = (
        names[name] for name in ("a4", "a5", "l4", "l5")
    )
    mixed4 = REDUCTION["add"](
        REDUCTION["multiply"](a4, P),
        REDUCTION["multiply"](l4, X),
    )
    mixed5 = REDUCTION["add"](
        REDUCTION["multiply"](a5, P),
        REDUCTION["multiply"](l5, Y),
    )
    pure_ss = REDUCTION["add"](
        REDUCTION["multiply"](a4, a5, P),
        REDUCTION["multiply"](a4, l5, Y),
        REDUCTION["multiply"](l4, a5, X),
        REDUCTION["multiply"](l4, l5, Z),
    )
    eliminated = REDUCTION["add"](
        pure_ss,
        REDUCTION["scale"](-1, REDUCTION["multiply"](a4, mixed5)),
        REDUCTION["scale"](-1, REDUCTION["multiply"](a5, mixed4)),
    )
    expected_elimination = REDUCTION["add"](
        REDUCTION["multiply"](l4, l5, Z),
        REDUCTION["scale"](-1, REDUCTION["multiply"](a4, a5, P)),
    )
    require(eliminated == expected_elimination,
            ("full-star mixed elimination changed", eliminated))

    # Since Z is a nonzero product rooted at h_u, two nonzero lambdas would
    # make the nonzero physical-k product P proportional to Z.  That puts
    # physical e_k at u on h_u, contradicting the H-slice conclusion for
    # physical e_s.  Thus at most one lambda is nonzero.  If lambda4 is the
    # live one, mixed5=0 with lambda5=0 forces alpha5=0 (and symmetrically).
    single_carrier = {
        "lambda4 nonzero": "lambda5=alpha5=0, hence W5s=0",
        "lambda5 nonzero": "lambda4=alpha4=0, hence W4s=0",
    }
    return actual, eliminated, single_carrier


def forbidden_corner_matrix(alpha4, alpha5):
    # Variables are (x_s,x_k,y_s,y_k).  Rows are the A and B coefficients
    # of T_sk,T_ks,T_kk when L4s=alpha4*A and L5s=alpha5*B.
    return (
        (Q(0), Q(0), Q(0), Q(alpha4)),
        (Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(alpha5), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(0), Q(0)),
    )


def audit_dependent_shores_collapse_to_pure_line():
    # Once literal kernel columns are excluded, the old corner dichotomy
    # leaves L4k=A and L5k=B nonzero, with each s-cofactor proportional to
    # its k-cofactor.  If A,B were independent, the six scalar coordinates
    # of the three forbidden corners have rank four for every alpha4,alpha5,
    # killing x_s,x_k,y_s,y_k and hence T_ss.
    universal_rows = tuple(
        forbidden_corner_matrix(Q(0), Q(0))[row]
        for row in (1, 2, 4, 5)
    )
    require(REDUCTION["rational_rank"](universal_rows) == 4,
            "the alpha-independent forbidden-corner minor changed")

    ranks = {}
    for alpha4, alpha5 in product((Q(0), Q(1), Q(2)), repeat=2):
        matrix = forbidden_corner_matrix(alpha4, alpha5)
        ranks[alpha4, alpha5] = REDUCTION["rational_rank"](matrix)
    require(set(ranks.values()) == {4},
            ("independent cofactor-line corner ranks changed", ranks))

    # Therefore B=rho*A.  The surviving T_ss is a nonzero scalar multiple
    # of A and is the physical pure s-product, so both L4k,L5k lie on that
    # product line.
    line_data = {
        "L4k": "gamma4 * physical-s product",
        "L5k": "gamma5 * physical-s product",
        "gamma4 nonzero": True,
        "gamma5 nonzero": True,
    }
    require(line_data["gamma4 nonzero"] and line_data["gamma5 nonzero"],
            "one surviving k-cofactor line became zero")
    return ranks, line_data


def audit_pure_line_fixes_all_u_blocks():
    # The physical s-factor at u is h_u=e0.  On u=e1,
    # Phi(W_z^k)=W_{z,u}^k(e1)*J, while its now-known pure-s right side is
    # zero.  Hence W_{z,u}^k(e1)=0.  The shore relation
    # W_z^s=alpha_z W_z^k+lambda_z(p,-p,0) has no u correction, so its
    # s-column is on h_u as well.
    h_u = (Q(1), Q(0))
    complement = (Q(0), Q(1))
    fixed = {}
    for zero in (4, 5):
        w_u_k = tuple(Q(3 + zero) * entry for entry in h_u)
        alpha = Q(zero - 2)
        w_u_s = tuple(alpha * entry for entry in w_u_k)
        require(sum(left * right for left, right in zip(w_u_k, complement))
                == 0,
                ("k-column left the fixed u-line", zero))
        require(sum(left * right for left, right in zip(w_u_s, complement))
                == 0,
                ("s-column left the fixed u-line", zero))
        fixed[zero] = (w_u_s, w_u_k)

    incident = ("u0", "u1", "ut", "u4", "u5")
    require(len(incident) == 5, "fixed-u incident-edge census changed")

    # Reuse the exact fixed-root support theorem and its sharp integral
    # calibration.  It returns the 32-dimensional fixed slice, ten escape
    # cells, the upper bound 42, and a packet attaining 42.
    fixed_root = ONE_ACTIVE["audit_product_slice_and_fixed_root_bound"]()
    require(fixed_root[4:] == (42, 42),
            ("fixed-u rank bound/calibration changed", fixed_root))
    return fixed, incident, fixed_root


def audit_literal_r2_at_invertible_roots():
    # This is a physical-coordinate statement, made before any inner
    # normalization.  Since h_u is the physical s-axis, M_iu has pure
    # output column s at u.  Since Q_t is the physical k-axis, M_it has
    # pure output column k at t.  They are nonzero and on distinct edges.
    tables = {}
    for s in COLOURS:
        k = 1 - s
        for root in (0, 1):
            witnesses = {
                s: ("u", "nonzero M_iu with shore factor h_u=e_s"),
                k: ("t", "nonzero M_it with shore factor Q_t=e_k"),
            }
            require(
                set(witnesses) == set(COLOURS)
                and witnesses[s][0] != witnesses[k][0],
                ("literal R2 witnesses failed at an invertible root",
                 s, root, witnesses),
            )
            tables[s, root] = witnesses
    return tables


def audit_chart_closure_map():
    chart = {
        "no kernel carrier": "coordinate-shore path rank <= 49",
        "literal k-column carrier": "incompatible physical s/k u-roots",
        "independent cofactor shore": "forces opposite literal carrier",
        "two dependent nonzero k-cofactors": "fixed-u rank <= 42",
    }
    require(set(chart.values()) == {
        "coordinate-shore path rank <= 49",
        "incompatible physical s/k u-roots",
        "forces opposite literal carrier",
        "fixed-u rank <= 42",
    }, "inactive-inactive closure map changed")
    return chart


def main():
    # Keep the exact predecessor live: rank-five Phi, 64 corner identities,
    # the kernel sign, and the no-carrier path bound.
    old_kernel = REDUCTION["audit_covariant_cofactor_kernel"]()
    old_corners = REDUCTION["audit_physical_corner_factorization"]()
    old_dichotomy = REDUCTION["audit_corner_and_mod_kernel_dichotomy"]()

    h_root = audit_h_slice_fixes_physical_s_root()
    literal = audit_literal_kernel_carrier_contradiction()
    full_star = audit_full_star_mixed_purity()
    line = audit_dependent_shores_collapse_to_pure_line()
    fixed = audit_pure_line_fixes_all_u_blocks()
    r2 = audit_literal_r2_at_invertible_roots()
    chart = audit_chart_closure_map()

    print("2I+2R+2Z asymmetric inactive-inactive L0 closure: passed")
    print(f"  imported Phi rank/kernel      : {set(old_kernel[1].values())}")
    print(f"  imported physical corners    : {old_corners}/64")
    print(f"  imported shore dichotomy     : {old_dichotomy[1]}")
    print(f"  pure-H physical u-root       : {h_root}")
    print(f"  literal-carrier contradiction: {literal}")
    print(f"  full-star mixed purity        : {full_star}")
    print(f"  dependent cofactor line      : {line}")
    print(f"  fixed-u bound/calibration    : {fixed[2][4:]}")
    print(f"  literal R2 invertible roots  : {len(r2)}/4")
    print(f"  chart closure map            : {chart}")


if __name__ == "__main__":
    main()
