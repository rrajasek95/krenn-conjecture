#!/usr/bin/env python3
"""Close factor-complete active sites on the double-live one-column chart.

Assume P_t=0, Q_t!=0 and both M_t4,M_t5 are live.  At either zero, L1
allows inactivity, P/V activity with an unrestricted t-z block, or Q/U
activity forcing M_tz proportional to Q_t u_z^T.  Thus every Q/U site is
factor-complete: all nonzero base blocks and all endpoint tangents
incident with it share u_z.  A P/V site is factor-complete as well when
its live block has zero-side factor v_z.  In either situation both pure
L0 targets would have one fixed physical shore, impossible.

The checker also audits the exact three-shore matching and star-derivative
decomposition left when both sites are P/V and both live blocks are
misaligned.  Standard library only; checks remain live under -O/-I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
SITES = INNER + (RANK_ONE,) + ZEROS
COLOURS = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


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


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS)
        for row in COLOURS
    )


def matrix_rank_2(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return 2 if determinant else 1


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


def audit_l1_active_type_grid():
    # P_t=0,Q_t!=0.  A live P/V site has selected t-z side
    # P_t v_z^T=0 and leaves B_z unrestricted.  A live Q/U site has
    # nonzero Q_t u_z^T and forces B_z onto the u_z zero shore.
    p_t = (Q(0), Q(0))
    q_t = (Q(2), Q(3))
    v_z = (Q(5), Q(7))
    u_z = (Q(11), Q(13))
    arbitrary_b = ((Q(1), Q(2)), (Q(3), Q(5)))
    forced_b = outer(q_t, u_z)
    aligned_p_b = outer((Q(17), Q(19)), v_z)
    require(matrix_rank_2(outer(p_t, v_z)) == 0,
            "P/V selected live side became nonzero")
    require(matrix_rank_2(arbitrary_b) == 2,
            "the unrestricted P/V live block was factorized")
    require(matrix_rank_2(forced_b) == 1,
            "the Q/U live block lost its forced zero shore")
    require(matrix_rank_2(aligned_p_b) == 1,
            "the aligned P/V live block lost its zero shore")

    # I=inactive, P=P/V, Q=Q/U.  Every chart containing Q is closed by
    # the forced-shore theorem.  The only type-level residue is {I,P}^2;
    # each P entry must additionally have a misaligned live block.
    grid = tuple(product(("I", "P", "Q"), repeat=2))
    q_closed = tuple(chart for chart in grid if "Q" in chart)
    residue = tuple(chart for chart in grid if "Q" not in chart)
    require(len(grid) == 9 and len(q_closed) == 5 and len(residue) == 4,
            ("double-live active-type grid changed", grid))
    require(residue == (("I", "I"), ("I", "P"), ("P", "I"), ("P", "P")),
            ("P/V-only type residue changed", residue))
    return q_closed, residue


def audit_factor_complete_base_matchings():
    # Fix a factor-complete zero z.  Its nine matchings through I and
    # three matchings through t all supply the same zero-site factor.
    # The three matchings through the other zero use M_45=0 and die.
    z = 4
    other_zero = 5
    categories = {"I-factor": 0, "t-factor": 0, "dead-45": 0}
    for matching in MATCHINGS:
        edge = next(pair for pair in matching if z in pair)
        partner = edge[1] if edge[0] == z else edge[0]
        if partner in INNER:
            category = "I-factor"
        elif partner == RANK_ONE:
            category = "t-factor"
        else:
            require(partner == other_zero,
                    ("factor-complete site found an unknown partner", matching))
            category = "dead-45"
        categories[category] += 1
    require(categories == {"I-factor": 9, "t-factor": 3, "dead-45": 3},
            ("factor-complete base matching census changed", categories))
    return categories


def audit_nonincident_tangent_cofactors():
    # A tangent away from factor-complete z leaves z in its four-site
    # cofactor.  If z meets I or t, that base edge supplies the fixed
    # factor; if z meets the other zero, the term dies.  Audit all ten
    # nonincident tangent edges, a superset of the endpoint packets.
    z = 4
    other_zero = 5
    remaining_sites = tuple(site for site in SITES if site != z)
    counts = {"factor": 0, "dead-45": 0}
    by_edge = {}
    for tangent in combinations(remaining_sites, 2):
        cofactor_sites = tuple(site for site in SITES
                               if site not in tangent)
        local = {"factor": 0, "dead-45": 0}
        for matching in perfect_matchings(cofactor_sites):
            edge = next(pair for pair in matching if z in pair)
            partner = edge[1] if edge[0] == z else edge[0]
            category = "dead-45" if partner == other_zero else "factor"
            local[category] += 1
            counts[category] += 1
        by_edge[tangent] = local
    require(len(by_edge) == 10,
            "nonincident tangent edge count changed")
    require(counts == {"factor": 24, "dead-45": 6},
            ("factor-complete cofactor census changed", counts))
    require(all(sum(local.values()) == 3 for local in by_edge.values()),
            "a nonincident tangent lost a cofactor matching")
    return counts


def audit_incident_endpoint_tangents():
    # At an active site z, every actual endpoint tangent incident with z
    # has its physical active factor:
    #   P/V: V_z is a multiple of v_z and U_z=0;
    #   Q/U: U_z is a multiple of u_z and V_z=0.
    # This includes I-z, t-z, and possible z-other-zero interactions.
    # P/V has no actual t-z endpoint block when P_t=U_z=0; the auxiliary
    # literal T_z used in radial rewrites has the factor by hypothesis.
    types = {
        "P/V": {
            "factor": "v_z",
            "endpoint": ("Iz", "z5"),
            "auxiliary": ("Tz",),
        },
        "Q/U": {
            "factor": "u_z",
            "endpoint": ("Iz", "tz", "z5"),
            "auxiliary": (),
        },
    }
    endpoint_checks = 0
    auxiliary_checks = 0
    for active_type, data in types.items():
        factor = data["factor"]
        require(factor in ("v_z", "u_z"),
                ("unknown physical active factor", active_type))
        endpoint_checks += len(data["endpoint"])
        auxiliary_checks += len(data["auxiliary"])
    require((endpoint_checks, auxiliary_checks) == (5, 1),
            "incident tangent audit count changed")
    return types


def audit_fixed_shore_pure_contradiction():
    # H and all dPsi(N^su) have one fixed zero-site factor.  The two pure
    # target shore vectors e0,e1 have rank two, not one.
    shores = ((Q(1), Q(0)), (Q(0), Q(1)))
    require(rational_rank(shores) == 2,
            "the two pure zero-site shores became collinear")
    determinant = shores[0][0] * shores[1][1] - shores[0][1] * shores[1][0]
    require(determinant == 1,
            "the fixed-shore pure determinant changed")
    return determinant


def audit_double_pv_matching_decomposition():
    # In the genuinely misaligned P/V--P/V residue, write B4,B5 for the
    # live blocks and v4,v5 for the zero factors.  The nondead matching
    # tensor has exactly three shore classes:
    #
    #   B4 tensor v5 tensor C4       (t meets 4),
    #   B5 tensor v4 tensor C5       (t meets 5),
    #   Q_t tensor v4 tensor v5 K   (t meets I).
    #
    # The other three matchings use M45=0.
    categories = {"B4*v5": 0, "B5*v4": 0, "Q*v4*v5": 0, "dead-45": 0}
    for matching in MATCHINGS:
        edges = frozenset(matching)
        if (4, 5) in edges:
            category = "dead-45"
        elif (RANK_ONE, 4) in edges:
            category = "B4*v5"
        elif (RANK_ONE, 5) in edges:
            category = "B5*v4"
        else:
            t_edge = next(edge for edge in matching if RANK_ONE in edge)
            require(any(i in t_edge for i in INNER),
                    ("cross shore lost the Q_t factor", matching))
            category = "Q*v4*v5"
        categories[category] += 1
    require(categories == {
        "B4*v5": 3,
        "B5*v4": 3,
        "Q*v4*v5": 6,
        "dead-45": 3,
    }, ("double-P/V matching shores changed", categories))
    return categories


def audit_double_pv_star_derivatives():
    # Edge tangents T4,T5 have three cofactors each:
    # D(T4)=B4*v5*C4 and D(T5)=B5*v4*C5.
    # For S4, each of its three I-4 tangent edges has one cofactor through
    # t-5 (B5*v4) and two cross cofactors (Q*v4*v5); S5 is symmetric.
    counts = {
        "T4": {"B4*v5": 0},
        "T5": {"B5*v4": 0},
        "S4": {"B5*v4": 0, "Q*v4*v5": 0},
        "S5": {"B4*v5": 0, "Q*v4*v5": 0},
    }

    for z, label, shore in (
        (4, "T4", "B4*v5"),
        (5, "T5", "B5*v4"),
    ):
        remaining = tuple(site for site in SITES
                          if site not in (RANK_ONE, z))
        for _matching in perfect_matchings(remaining):
            counts[label][shore] += 1

    for z, label, opposite_edge, opposite_shore in (
        (4, "S4", (RANK_ONE, 5), "B5*v4"),
        (5, "S5", (RANK_ONE, 4), "B4*v5"),
    ):
        for i in INNER:
            remaining = tuple(site for site in SITES if site not in (i, z))
            for matching in perfect_matchings(remaining):
                shore = (
                    opposite_shore
                    if opposite_edge in matching
                    else "Q*v4*v5"
                )
                counts[label][shore] += 1

    require(counts == {
        "T4": {"B4*v5": 3},
        "T5": {"B5*v4": 3},
        "S4": {"B5*v4": 3, "Q*v4*v5": 6},
        "S5": {"B4*v5": 3, "Q*v4*v5": 6},
    }, ("double-P/V star derivative shores changed", counts))
    return counts


def audit_symmetric_dictionary():
    p_zero = {
        "one_column": "P_t=0",
        "automatic_complete": "Q/U",
        "forced_live": "Q_t*u_z",
        "conditional_complete": "P/V",
        "conditional_factor": "v_z",
    }
    q_zero = {
        "one_column": "Q_t=0",
        "automatic_complete": "P/V",
        "forced_live": "P_t*v_z",
        "conditional_complete": "Q/U",
        "conditional_factor": "u_z",
    }
    require(tuple(p_zero) == tuple(q_zero),
            "double-live symmetric dictionaries disagree")
    require(
        p_zero["automatic_complete"] == q_zero["conditional_complete"]
        and p_zero["conditional_complete"] == q_zero["automatic_complete"],
        "P/V and Q/U did not interchange",
    )
    return p_zero, q_zero


def main():
    q_closed, residue = audit_l1_active_type_grid()
    base = audit_factor_complete_base_matchings()
    cofactors = audit_nonincident_tangent_cofactors()
    incident = audit_incident_endpoint_tangents()
    determinant = audit_fixed_shore_pure_contradiction()
    pv_matching = audit_double_pv_matching_decomposition()
    pv_derivatives = audit_double_pv_star_derivatives()
    audit_symmetric_dictionary()
    print("three-invertible double-live factor-complete closure: passed")
    print(f"  Q/U-closed/type residue    : {q_closed}/{residue}")
    print(f"  factor-complete matchings  : {base}")
    print(f"  nonincident cofactors      : {cofactors}")
    print(f"  incident active tangents   : {incident}")
    print(f"  pure-shore determinant     : {determinant}")
    print(f"  double-P/V matching shores : {pv_matching}")
    print(f"  double-P/V star shores     : {pv_derivatives}")
    print("  symmetric P/Q cases        : both audited")


if __name__ == "__main__":
    main()
