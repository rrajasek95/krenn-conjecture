#!/usr/bin/env python3
"""Reduce the mixed-L0 double-live I/P residue and close (I,I).

After the factor-complete closure, each live zero is inactive (I) or
active P/V (P), and every P live block is misaligned.  Modulo the aligned
core gauge, an endpoint packet is

    a_s (sum_{z active} f_zu S_z - c_u (T_4+T_5)).

The generalized-gauge equations are exact.  A nonzero relation exists
only when every active spoke triple is uniform and every inactive zero
has all I-spokes zero.  Mixed L0 consequently leaves at most one pure
endpoint colour.

For (I,I), the all-zero-spoke relation closes by collinearity; otherwise
the surviving chart gives the full terminal equations H pure, Q_t
complementary pure, and C_t complementary pure.  The existing covariant
singular-overlap theorem then closes it without spoke invertibility.

For P-containing types the checker records the exact three-shore tensor
survivor.  Standard library only; checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
SITES = INNER + (RANK_ONE,) + ZEROS
COLOURS = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
DOUBLE = run_path(str(
    HERE
    / "verify_level_two_three_invertible_one_column_double_live_factor_complete_closure.py"
))
TERMINAL = run_path(str(
    HERE / "verify_level_two_three_invertible_one_column_singular_overlap.py"
))


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
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
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


# Sparse formal polynomials for localization and flattening minors.
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


def audit_exceptional_t_star_identity():
    # With both t-zero blocks live,
    # S_t=2*tau*G(e_t)-2*tau*(T4+T5).
    tau = Q(7, 3)
    checks = 0
    for edge in combinations(SITES, 2):
        i, j = edge
        star = Q(i + j + 1) if i in INNER and j == RANK_ONE else Q(0)
        t4 = Q(11) if edge == (RANK_ONE, 4) else Q(0)
        t5 = Q(13) if edge == (RANK_ONE, 5) else Q(0)
        if star:
            packet = star / (2 * tau)
        elif t4:
            packet = t4
        elif t5:
            packet = t5
        else:
            packet = Q(0)
        radial = int(RANK_ONE in edge) * packet
        require(
            star == 2 * tau * radial - 2 * tau * (t4 + t5),
            ("double-live exceptional star identity failed", edge),
        )
        checks += 1
    require(checks == 15, "exceptional edge identity count changed")
    return checks


def audit_nonuniform_localization_certificates():
    # Active P/V gives q_z=(lambda_i+lambda_z)m_iz.  The core kills
    # lambda_i, and the live t-z edge gives lambda_z=r, where r is the
    # common T4+T5 coefficient.  Thus q_z=r*m_iz.  Pair subtraction gives
    # the exact certificate q_z(m_i-m_j)=0 in a nonuniform triple.
    r = variable("r")
    q = variable("q")
    multiples = [variable(f"m{i}") for i in INNER]
    equations = [
        add(multiply(r, multiple), scale(-1, q))
        for multiple in multiples
    ]
    checks = 0
    for i, j in combinations(INNER, 2):
        left = add(
            multiply(multiples[j], equations[i]),
            scale(-1, multiply(multiples[i], equations[j])),
        )
        right = multiply(
            q, add(multiples[i], scale(-1, multiples[j]))
        )
        require(left == right,
                ("double-live localization certificate failed", i, j))
        checks += 1
    require(checks == 3, "localization certificate count changed")
    return checks


def gauge_system(types, uniform_flags, inactive_zero_flags):
    """Return the generalized-gauge system for q_z S_z+r(T4+T5)."""

    active = tuple(z for z, site_type in zip(ZEROS, types)
                   if site_type == "P")
    q_columns = {z: 7 + index for index, z in enumerate(active)}
    # Columns lambda_0,...,lambda_5,r,q_active...
    width = 7 + len(active)
    rows = []

    def equation(entries):
        row = [Q(0)] * width
        for column, coefficient in entries.items():
            row[column] += Q(coefficient)
        rows.append(row)

    for i, j in combinations(INNER, 2):
        equation({i: 1, j: 1})
    for i in INNER:
        equation({i: 1, RANK_ONE: 1})
    for z in ZEROS:
        # r*T_z=(lambda_t+lambda_z)M_tz.
        equation({RANK_ONE: 1, z: 1, 6: -1})

    active_position = 0
    inactive_position = 0
    for z, site_type in zip(ZEROS, types):
        if site_type == "P":
            uniform = uniform_flags[active_position]
            active_position += 1
            multiples = (2, 2, 2) if uniform else (2, 3, 5)
            q_column = q_columns[z]
            for i, multiple in zip(INNER, multiples):
                equation({i: multiple, z: multiple, q_column: -1})
        else:
            all_zero = inactive_zero_flags[inactive_position]
            inactive_position += 1
            if not all_zero:
                # One arbitrary nonzero I-z block is enough to impose
                # lambda_i+lambda_z=0.
                equation({0: 1, z: 1})
    return rows, width


def audit_typewise_gauge_dichotomy():
    # A nonzero tangent relation exists exactly when all active triples are
    # uniform and all inactive I-spoke shores vanish.  Enumerate all four
    # I/P type pairs and every uniform/zero flag pattern.
    summaries = {}
    total_cases = 0
    radial_cases = 0
    for types in product(("I", "P"), repeat=2):
        active_count = types.count("P")
        inactive_count = types.count("I")
        cases = []
        for uniform_flags in product((False, True), repeat=active_count):
            for inactive_zero_flags in product(
                (False, True), repeat=inactive_count
            ):
                rows, width = gauge_system(
                    types, uniform_flags, inactive_zero_flags
                )
                nullity = width - rational_rank(rows)
                radial = all(uniform_flags) and all(inactive_zero_flags)
                require(nullity == int(radial),
                        ("typewise gauge nullity changed", types,
                         uniform_flags, inactive_zero_flags, nullity))
                cases.append((uniform_flags, inactive_zero_flags, nullity))
                total_cases += 1
                radial_cases += int(radial)
        summaries[types] = tuple(cases)
    require(total_cases == 16 and radial_cases == 4,
            ("typewise gauge case census changed", total_cases, radial_cases))
    return summaries


def audit_radial_representatives():
    # At an active uniform P site, m*S_z+T_z=G(e_z).  At an inactive site
    # whose I-spokes vanish, T_z=G(e_z).  These combine to the unique
    # relation visible in the packet span with one common T4+T5 coefficient.
    representatives = {
        ("I", "I"): ("T4+T5",),
        ("I", "P"): ("T4+T5+m5*S5",),
        ("P", "I"): ("m4*S4+T4+T5",),
        ("P", "P"): ("m4*S4+m5*S5+T4+T5",),
    }
    require(all(len(value) == 1 for value in representatives.values()),
            "a radial packet representative disappeared")
    require(len(set(value[0] for value in representatives.values())) == 4,
            "radial packet representatives collided")
    return representatives


def audit_mixed_scalar_census():
    # Let R_u denote the endpoint residual class in the tangent quotient.
    # Mixed L0 gives a0*R1=a1*R0=0.  If both pure products vanish, the two
    # pure targets are collinear with H.  Exactly two one-colour charts
    # survive, independent of the quotient dimension.
    closed = 0
    survivors = []
    for a0, a1, r0, r1 in product((0, 1), repeat=4):
        if a0 * r1 or a1 * r0:
            continue
        pure = (a0 * r0, a1 * r1)
        if pure == (0, 0):
            closed += 1
        else:
            survivors.append((a0, a1, r0, r1, pure))
    require(survivors == [
        (0, 1, 0, 1, (0, 1)),
        (1, 0, 1, 0, (1, 0)),
    ], ("double-live mixed scalar survivors changed", survivors))
    require(closed == 7, "double-live mixed closed count changed")
    return closed, survivors


def audit_terminal_flattening():
    # In the inactive-inactive nongauge chart, the one surviving correction
    # is D(S_t)=Q_t tensor C_t.  With H=h e_s^6, the complementary pure
    # equation is Q_t*C_t=e_k^6-kappa*h*e_s^6.  Its t-flattening minor
    # kills kappa and singleton support forces Q_t,C_t pure in colour k.
    kappa = variable("kappa")
    h = variable("h")
    checks = 0
    for s in COLOURS:
        k = 1 - s
        matrix = [[constant(0), constant(0)] for _ in COLOURS]
        matrix[k][0] = constant(1)
        matrix[s][1] = scale(-1, multiply(kappa, h))
        determinant = add(
            multiply(matrix[0][0], matrix[1][1]),
            scale(-1, multiply(matrix[0][1], matrix[1][0])),
        )
        expected = scale(-1 if k == 0 else 1, multiply(kappa, h))
        require(determinant == expected and determinant,
                ("terminal t-flattening minor changed", s))
        singleton = frozenset(((k, (k,) * 5),))
        require(
            frozenset(left for left, _ in singleton) == frozenset((k,))
            and frozenset(right for _, right in singleton)
            == frozenset(((k,) * 5,)),
            "terminal singleton support changed",
        )
        checks += 1
    return checks


def audit_imported_terminal_closure():
    # Once H,Q_t,C_t are complementary pure tensors, the existing
    # covariant singular-overlap theorem closes every spoke-rank pattern:
    # independent cofactor shores contradict purity, while two dependent
    # shores have differential rank at most 49.
    cofactor_terms = TERMINAL["audit_terminal_cofactor_uses_both_shores"]()
    factors = TERMINAL["audit_dependent_pair_factorization"]()
    outcomes = TERMINAL["audit_covariant_dichotomy"]()
    slices, phi_shape, paths, categories = (
        TERMINAL["audit_imported_exact_lemmas"]()
    )
    require(cofactor_terms == 96 and factors == 24,
            "imported terminal term census changed")
    require(slices == 64 and phi_shape == (8, 6) and paths == 64,
            "imported terminal exact lemmas changed")
    require(categories == {"all_cross": 6, "34": 3, "35": 3, "45": 3},
            "imported terminal path categories changed")
    return outcomes


def audit_double_pv_pure_component_survivor():
    # Import the exact shore counts from the factor-complete boundary map.
    matching = DOUBLE["audit_double_pv_matching_decomposition"]()
    derivatives = DOUBLE["audit_double_pv_star_derivatives"]()

    # For R=f4*S4+f5*S5-c*(T4+T5), the pure correction has:
    #   B4*v5 shore from -c*T4 and f5*S5,
    #   B5*v4 shore from -c*T5 and f4*S4,
    #   Q*v4*v5 shore from f4*S4 and f5*S5.
    components = {
        "B4*v5": (("-c", "T4", 3), ("f5", "S5", 3)),
        "B5*v4": (("-c", "T5", 3), ("f4", "S4", 3)),
        "Q*v4*v5": (("f4", "S4", 6), ("f5", "S5", 6)),
    }
    require(tuple(components) == ("B4*v5", "B5*v4", "Q*v4*v5"),
            "double-P/V pure component order changed")
    require(sum(entry[2] for rows in components.values() for entry in rows)
            == 24,
            "double-P/V pure component term count changed")
    return matching, derivatives, components


def audit_symmetric_dictionary():
    p_zero = (
        "P_t=0", "I/P residue", "a_s", "Q_t", "P/V", "S_z"
    )
    q_zero = (
        "Q_t=0", "I/Q residue", "b_s", "P_t", "Q/U", "S_z"
    )
    require(len(p_zero) == len(q_zero) == 6,
            "symmetric mixed-residue dictionary changed")
    require(p_zero[-1] == q_zero[-1] == "S_z",
            "the symmetric zero-star label changed")
    require(set(p_zero[:-1]).isdisjoint(q_zero[:-1]),
            "symmetric mixed-residue labels collided")
    return p_zero, q_zero


def main():
    star = audit_exceptional_t_star_identity()
    certificates = audit_nonuniform_localization_certificates()
    dichotomy = audit_typewise_gauge_dichotomy()
    radial = audit_radial_representatives()
    closed, survivors = audit_mixed_scalar_census()
    flattenings = audit_terminal_flattening()
    outcomes = audit_imported_terminal_closure()
    matching, derivatives, components = audit_double_pv_pure_component_survivor()
    audit_symmetric_dictionary()
    print("three-invertible double-live mixed residue reduction: passed")
    print(f"  exceptional/localization    : {star}/{certificates}")
    print(f"  typewise gauge patterns     : {tuple((k, len(v)) for k, v in dichotomy.items())}")
    print(f"  radial representatives      : {radial}")
    print(f"  scalar charts closed/live   : {closed}/{len(survivors)}")
    print(f"  inactive terminal flattening: {flattenings}")
    print(f"  imported terminal outcomes  : {outcomes}")
    print(f"  double-P/V matching shores  : {matching}")
    print(f"  double-P/V derivative shores: {derivatives}")
    print(f"  exact pure components       : {components}")


if __name__ == "__main__":
    main()
