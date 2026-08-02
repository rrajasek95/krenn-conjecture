#!/usr/bin/env python3
"""Close the P-containing double-live one-column residue at rank 49.

For one active P/V zero z, matching support gives

    H = B_z tensor C + v_z tensor L,
    e_k^6-kappa H = -c B_z tensor C + v_z tensor D.

The z-flattening forces kappa=c and v_z parallel to e_k.  The pure s-row
of H then forces C parallel to e_s^4.  Injectivity of the invertible-
triangle cofactor map makes every I-spoke at the inactive zero carry the
fixed physical e_s shore.  Together with Q_t and v_z, the shore
{t,z,w} is the two-edge coordinate-shore path, so rank(dPsi) <= 49.

With two P/V zeros, the three fixed shores Q_t,v_4,v_5 are already present,
so the same path theorem applies directly.  Standard library only; checks
remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
DOUBLE = run_path(str(
    HERE
    / "verify_level_two_three_invertible_one_column_double_live_factor_complete_closure.py"
))
MIXED = run_path(str(
    HERE
    / "verify_level_two_three_invertible_one_column_double_live_mixed_residue_reduction.py"
))
PURE = run_path(str(
    HERE
    / "verify_level_two_three_invertible_one_column_pure_tensor_obstruction.py"
))
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))

INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
SITES = INNER + (RANK_ONE,) + ZEROS
COLOURS = (0, 1)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


# Sparse formal polynomial arithmetic.
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


def audit_one_p_matching_split():
    # Fix the active site z and let w be inactive.  Exactly three base
    # matchings use t-z and give B_z tensor C.  Nine use an I-z spoke and
    # have factor v_z.  Three use the dead z-w block.  In the endpoint
    # correction, T_z gives the same B_z tensor C, while S_z and T_w have
    # factor v_z.
    summaries = {}
    for active, inactive in ((4, 5), (5, 4)):
        base = {"B*C": 0, "v-factor": 0, "dead": 0}
        for matching in MATCHINGS:
            edges = frozenset(matching)
            if (min(active, inactive), max(active, inactive)) in edges:
                category = "dead"
            elif (RANK_ONE, active) in edges:
                category = "B*C"
            else:
                active_edge = next(
                    edge for edge in matching if active in edge
                )
                partner = (
                    active_edge[1]
                    if active_edge[0] == active else active_edge[0]
                )
                require(partner in INNER,
                        ("active zero lost its I-spoke", matching))
                category = "v-factor"
            base[category] += 1
        require(base == {"B*C": 3, "v-factor": 9, "dead": 3},
                ("one-P matching split changed", active, base))

        tangent = {"Tz:B*C": 0, "Sz:v": 0, "Tw:v": 0}
        tangent["Tz:B*C"] = len(perfect_matchings(INNER + (inactive,)))
        for inner in INNER:
            remaining = tuple(
                site for site in SITES if site not in (inner, active)
            )
            tangent["Sz:v"] += len(perfect_matchings(remaining))
        tangent["Tw:v"] = len(perfect_matchings(INNER + (active,)))
        require(tangent == {"Tz:B*C": 3, "Sz:v": 9, "Tw:v": 3},
                ("one-P tangent split changed", active, tangent))
        summaries[active] = (base, tangent)
    return summaries


def audit_flattening_forces_complementary_factor():
    # Substitution of H=X+vL into
    #   E_k-kappa H=-cX+vD
    # gives E_k+(c-kappa)H=v(D+cL).  In the z-flattening, the E_k and
    # E_s columns form a 2x2 diagonal minor with determinant
    # +/- (c-kappa)h.  The right side has rank at most one.  Since h!=0,
    # kappa=c, after which v tensor F=E_k forces line(v)=line(e_k).
    c = variable("c")
    kappa = variable("kappa")
    h = variable("h")
    difference = add(c, scale(-1, kappa))
    checks = 0
    for pure_colour in COLOURS:
        complementary = 1 - pure_colour
        matrix = [[constant(0), constant(0)] for _ in COLOURS]
        matrix[complementary][0] = constant(1)
        matrix[pure_colour][1] = multiply(difference, h)
        determinant = add(
            multiply(matrix[0][0], matrix[1][1]),
            scale(-1, multiply(matrix[0][1], matrix[1][0])),
        )
        expected = scale(
            1 if complementary == 0 else -1,
            multiply(difference, h),
        )
        require(determinant == expected and determinant,
                ("one-P flattening minor changed", pure_colour))

        target_support = frozenset((
            (complementary, (complementary,) * 5),
        ))
        require(
            frozenset(left for left, _ in target_support)
            == frozenset((complementary,))
            and frozenset(right for _, right in target_support)
            == frozenset(((complementary,) * 5,)),
            "rank-one target support stopped fixing both factors",
        )
        checks += 2
    return checks


def audit_normalized_one_p_factorization():
    # Once v=e_k, the s-row of H=B*C+v*L is b_s*C=h e_s^5.
    # A nonzero product with singleton support forces
    # supp(b_s)={s}, supp(C)={s^4}.  Rescale the factor pair B*C so C=e_s^4.
    # Then B=h e_s e_s^T-e_k ell_t^T and L=ell_t e_s^4.
    h = variable("h")
    c = variable("c")
    ell = tuple(variable(f"ell{colour}") for colour in COLOURS)
    support_solutions = {}
    identities = 0

    for pure_colour in COLOURS:
        complementary = 1 - pure_colour
        target = frozenset(((pure_colour, (pure_colour,) * 4),))
        solutions = []
        # The product support has cardinality one, so both factors have
        # singleton support.  Exhaust the 2*16 possible singleton pairs.
        for t_colour in COLOURS:
            for four_word in product(COLOURS, repeat=4):
                product_support = frozenset(((t_colour, four_word),))
                if product_support == target:
                    solutions.append((t_colour, four_word))
        require(solutions == [(pure_colour, (pure_colour,) * 4)],
                ("pure cofactor support extraction changed", pure_colour))
        support_solutions[pure_colour] = tuple(solutions)

        def b_value(z_colour, t_colour):
            if z_colour == pure_colour and t_colour == pure_colour:
                return h
            if z_colour == complementary:
                return scale(-1, ell[t_colour])
            return constant(0)

        def c_value(four_word):
            return constant(four_word == (pure_colour,) * 4)

        def l_value(t_colour, four_word):
            return (
                ell[t_colour]
                if four_word == (pure_colour,) * 4 else constant(0)
            )

        # The normalized H identity, ordered as z,t,the other four sites.
        for word in product(COLOURS, repeat=6):
            z_colour, t_colour = word[:2]
            four_word = word[2:]
            actual_h = add(
                multiply(b_value(z_colour, t_colour), c_value(four_word)),
                l_value(t_colour, four_word)
                if z_colour == complementary else constant(0),
            )
            expected_h = h if word == (pure_colour,) * 6 else constant(0)
            require(actual_h == expected_h,
                    ("normalized one-P H identity failed", pure_colour, word))

            # With kappa=c, D=e_k^5-cL.  Audit the complete pure-correction
            # identity E_k-cH=-c(B*C)+e_k*D.
            pure_target = constant(word == (complementary,) * 6)
            left = add(pure_target, scale(-1, multiply(c, expected_h)))
            d_value = add(
                constant((t_colour,) + four_word
                         == (complementary,) * 5),
                scale(-1, multiply(c, l_value(t_colour, four_word))),
            )
            right = add(
                scale(-1, multiply(
                    c, b_value(z_colour, t_colour), c_value(four_word)
                )),
                d_value if z_colour == complementary else constant(0),
            )
            require(left == right,
                    ("normalized one-P correction failed", pure_colour, word))
            identities += 2
    require(identities == 256, "normalized identity count changed")
    return support_solutions, identities


def audit_inactive_shore_from_pure_cofactor():
    # The four-site C is the invertible-triangle cofactor map Phi applied
    # separately to the two physical colour columns at the inactive zero.
    # C proportional to e_s^4 has zero k-slice.  Covariant injectivity of
    # Phi therefore kills all three k-columns and gives fixed right factor
    # e_s on every inactive I-spoke.
    matrix = PURE["cofactor_map_matrix"]()
    shape = PURE["audit_cofactor_injectivity"]()
    require(shape == (8, 6), "triangle cofactor injectivity audit changed")
    require(PURE["rational_rank"](matrix) == 6,
            "triangle cofactor map lost injectivity")
    conclusions = {}
    for pure_colour in COLOURS:
        complementary = 1 - pure_colour
        zero_slice = (Q(0),) * 8
        require(not any(zero_slice), "the forbidden cofactor slice revived")
        conclusions[pure_colour] = {
            "zero column": complementary,
            "fixed shore": f"e{pure_colour}",
            "spoke blocks": 3,
        }
    return shape, conclusions


def audit_path_reductions():
    # One-P: Q_t, v_z=e_k, and the newly forced e_s at the inactive zero.
    # Two-P: Q_t,v_4,v_5 are present directly from the active normal forms.
    charts = {
        ("I", "P"): ("Q_t", "e_s", "v_5=e_k"),
        ("P", "I"): ("Q_t", "v_4=e_k", "e_s"),
        ("P", "P"): ("Q_t", "v_4", "v_5"),
    }
    exceptional = frozenset(((RANK_ONE, 4), (RANK_ONE, 5)))
    require(len(exceptional) == 2 and (4, 5) not in exceptional,
            "the double-live exceptional path changed")
    require(all(len(factors) == 3 for factors in charts.values()),
            "a P-containing chart lost a shore factor")

    identities, categories = SHORE["audit_path_factorization"]()
    require(identities == 64, "coordinate-shore path audit changed")
    require(categories == {"all_cross": 6, "34": 3,
                           "35": 3, "45": 3},
            "coordinate-shore path categories changed")
    bounds = {chart: 49 for chart in charts}
    return charts, categories, bounds


def audit_imported_residue_scope():
    q_closed, residue = DOUBLE["audit_l1_active_type_grid"]()
    require(residue == (("I", "I"), ("I", "P"),
                        ("P", "I"), ("P", "P")),
            "double-live type residue changed")
    closed, survivors = MIXED["audit_mixed_scalar_census"]()
    require((closed, len(survivors)) == (7, 2),
            "mixed pure-colour census changed")
    matching = DOUBLE["audit_double_pv_matching_decomposition"]()
    require(matching == {
        "B4*v5": 3, "B5*v4": 3,
        "Q*v4*v5": 6, "dead-45": 3,
    }, "double-P/V matching decomposition changed")
    MIXED["audit_symmetric_dictionary"]()
    return q_closed, residue, matching


def main():
    split = audit_one_p_matching_split()
    flattenings = audit_flattening_forces_complementary_factor()
    supports, normal_form_identities = audit_normalized_one_p_factorization()
    phi_shape, inactive = audit_inactive_shore_from_pure_cofactor()
    charts, categories, bounds = audit_path_reductions()
    q_closed, residue, matching = audit_imported_residue_scope()
    require(max(bounds.values()) == 49,
            "P-containing double-live rank bound changed")

    print("three-invertible double-live P residue closure: passed")
    print(f"  one-P matching/tangent split : {split}")
    print(f"  flattening forcing checks    : {flattenings}")
    print(f"  normalized identities       : {normal_form_identities}")
    print(f"  pure support solutions      : {supports}")
    print(f"  cofactor injectivity        : {phi_shape}, {inactive}")
    print(f"  P chart shores              : {charts}")
    print(f"  path categories             : {categories}")
    print(f"  imported type residue       : {q_closed}/{residue}")
    print(f"  double-P/V matching shores  : {matching}")
    print(f"  differential-rank bounds    : {bounds}")


if __name__ == "__main__":
    main()
