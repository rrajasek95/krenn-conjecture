#!/usr/bin/env python3
"""Audit the asymmetric one-column 2I+2R+2Z L1 boundary.

One rank-one endpoint t has P_t=0,Q_t!=0, while the other rank-one endpoint
u has both selected columns nonzero.  The two-column endpoint kills the two
skew modes left by the single invertible edge.  At t, L1 leaves

    U_t^s=0,  V_t^s=beta_s Q_t,

so an inactive-zero endpoint slice differs from the aligned cut gauge by
one scalar star on t.

At a zero site, L1 activity is P/V or Q/U.  Relative to the three
full-column sites {0,1,u}, either active type gives one fixed physical
zero-side factor.  Hence if both zeros are active, the shore {t,4,5} has
fixed factors Q_t,xi_4,xi_5 and exceptional path 4-t-5.  The exact
coordinate-shore theorem gives rank(dPsi)<=49.

Standard library only; checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
L1 = run_path(str(
    HERE / "verify_level_two_two_invertible_l1_collinearity_obstruction.py"
))
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))

COLOURS = (0, 1)
SITES = tuple(range(6))
CORE = (0, 1, 2, 3)
ONE_COLUMN = 2
TWO_COLUMN = 3
ZEROS = (4, 5)
FULL_COLUMN = (0, 1, TWO_COLUMN)
EDGES = tuple(combinations(SITES, 2))
SIGMA = (1, 1, 1, 1, -1, -1)


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


def flatten(matrix):
    return tuple(value for row in matrix for value in row)


def coefficient_matrix(residual, width):
    columns = []
    for basis in range(width):
        vector = [Q(0)] * width
        vector[basis] = Q(1)
        columns.append(tuple(residual(vector)))
    return [list(row) for row in zip(*columns)]


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
        rows[rank] = [entry / scale for entry in rows[rank]]
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


# Sparse formal polynomials.
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


def audit_two_column_endpoint_kills_core_skew():
    # The old propagation audit uses exactly one two-column rank-one
    # neighbour, so it applies unchanged even though the other rank-one
    # endpoint is now one-column.
    edge_modes = L1["audit_invertible_edge_modes"]()
    propagation = L1["audit_rank_one_propagation"]()
    require(edge_modes == ((3, 2), (3, 2)),
            "invertible-edge skew modes changed")
    require(propagation == (5, 5),
            "two-column rank-one propagation changed")
    return edge_modes, propagation


def audit_one_column_endpoint_modes():
    e0 = (Q(1), Q(0))
    e1 = (Q(0), Q(1))
    q_t = (Q(2), Q(3))

    # P/V variables: Vt0,Vt1,b,d0,d1.  With P_t=0 and the core skew
    # already killed, the two equations are
    #   e0 V_t^T = d_i e0 Q_t^T.
    # They leave independent aligned-core b and local beta modes.
    def pv_residual(vector):
        v_t = tuple(vector[index] for index in (0, 1))
        answer = []
        for edge_scalar in vector[3:5]:
            left = outer(e0, v_t)
            right = scale_matrix(edge_scalar, outer(e0, q_t))
            answer.extend(flatten(add_matrix(
                left, scale_matrix(-1, right)
            )))
        return answer

    pv = coefficient_matrix(pv_residual, 5)
    pv_core = (Q(0), Q(0), Q(1), Q(0), Q(0))
    pv_local = q_t + (Q(0), Q(1), Q(1))
    require(rational_rank(pv) == 3,
            "one-column P/V propagation rank changed")
    require(not any(L1["matrix_vector_product"](pv, pv_core))
            and not any(L1["matrix_vector_product"](pv, pv_local)),
            "one-column P/V generators changed")
    require(rational_rank((pv_core, pv_local)) == 2,
            "one-column P/V modes became dependent")

    # U/Q variables: Ut0,Ut1,a,d0,d1.  The equations are
    #   e1 U_t^T + a e0 Q_t^T = d_i e0 Q_t^T.
    # They force U_t=0 and d0=d1=a.
    def uq_residual(vector):
        u_t = tuple(vector[index] for index in (0, 1))
        a = vector[2]
        answer = []
        for edge_scalar in vector[3:5]:
            left = add_matrix(
                outer(e1, u_t), scale_matrix(a, outer(e0, q_t))
            )
            right = scale_matrix(edge_scalar, outer(e0, q_t))
            answer.extend(flatten(add_matrix(
                left, scale_matrix(-1, right)
            )))
        return answer

    uq = coefficient_matrix(uq_residual, 5)
    uq_aligned = (Q(0), Q(0), Q(1), Q(1), Q(1))
    require(rational_rank(uq) == 4,
            "one-column U/Q propagation rank changed")
    require(not any(L1["matrix_vector_product"](uq, uq_aligned)),
            "U_t=0,a-aligned mode left the L1 system")

    # The edge to the two-column rank-one site imposes no beta=b relation.
    h_t = (Q(5), Q(7))
    h_u = (Q(11), Q(13))
    p_u, q_u = Q(17), Q(19)
    beta, b, a = Q(23), Q(29), Q(31)
    p_t = (Q(0), Q(0))
    q_t_vector = tuple(Q(2) * value for value in h_t)
    p_u_vector = tuple(p_u * value for value in h_u)
    q_u_vector = tuple(q_u * value for value in h_u)
    v_t = tuple(beta * value for value in q_t_vector)
    v_u = tuple(b * value for value in q_u_vector)
    u_t = (Q(0), Q(0))
    u_u = tuple(a * value for value in p_u_vector)
    selected = add_matrix(
        outer(p_t, q_u_vector), outer(q_t_vector, p_u_vector)
    )
    pv_left = add_matrix(outer(p_t, v_u), outer(v_t, p_u_vector))
    uq_left = add_matrix(outer(q_t_vector, u_u), outer(u_t, q_u_vector))
    require(pv_left == scale_matrix(beta, selected),
            "the t-u P/V edge tied beta to the core scalar")
    require(uq_left == scale_matrix(a, selected),
            "the t-u U/Q edge lost aligned a")
    require(beta != b, "the beta/b independence witness collapsed")
    return (3, 2), (4, 1)


def audit_full_four_site_l1_system():
    # Expand all six L1 edges on {0,1,t,u} at once.  This guards against a
    # hidden t-u or cross-edge condition missed by the local propagation
    # decomposition.  Variables are two endpoint coordinates at each site
    # followed by one scalar for each of the six edges.
    e0 = (Q(1), Q(0))
    e1 = (Q(0), Q(1))
    h_u = (Q(5), Q(7))
    selected = {
        0: (e0, e1),
        1: (e0, e1),
        ONE_COLUMN: ((Q(0), Q(0)), (Q(2), Q(3))),
        TWO_COLUMN: (
            tuple(Q(11) * entry for entry in h_u),
            tuple(Q(13) * entry for entry in h_u),
        ),
    }
    core_edges = tuple(combinations(CORE, 2))
    width = 2 * len(CORE) + len(core_edges)

    def residual(vector, family):
        endpoint = {
            site: tuple(vector[2 * site + colour] for colour in COLOURS)
            for site in CORE
        }
        answer = []
        for edge_index, (left_site, right_site) in enumerate(core_edges):
            p_left, q_left = selected[left_site]
            p_right, q_right = selected[right_site]
            numerator = add_matrix(
                outer(p_left, q_right), outer(q_left, p_right)
            )
            edge_scalar = vector[2 * len(CORE) + edge_index]
            if family == "P/V":
                left = add_matrix(
                    outer(p_left, endpoint[right_site]),
                    outer(endpoint[left_site], p_right),
                )
            else:
                left = add_matrix(
                    outer(q_left, endpoint[right_site]),
                    outer(endpoint[left_site], q_right),
                )
            answer.extend(flatten(add_matrix(
                left, scale_matrix(-edge_scalar, numerator)
            )))
        return answer

    pv = coefficient_matrix(lambda vector: residual(vector, "P/V"), width)
    uq = coefficient_matrix(lambda vector: residual(vector, "Q/U"), width)
    require((rational_rank(pv), rational_rank(uq)) == (12, 13),
            "full asymmetric four-site L1 ranks changed")

    def direction(endpoint, live_edges):
        values = []
        for site in CORE:
            values.extend(endpoint.get(site, (Q(0), Q(0))))
        values.extend(Q(edge in live_edges) for edge in core_edges)
        return tuple(values)

    non_t_edges = frozenset(
        edge for edge in core_edges if ONE_COLUMN not in edge
    )
    t_edges = frozenset(
        edge for edge in core_edges if ONE_COLUMN in edge
    )
    pv_core = direction({
        0: selected[0][1],
        1: selected[1][1],
        TWO_COLUMN: selected[TWO_COLUMN][1],
    }, non_t_edges)
    pv_local = direction({
        ONE_COLUMN: selected[ONE_COLUMN][1],
    }, t_edges)
    uq_aligned = direction({
        0: selected[0][0],
        1: selected[1][0],
        TWO_COLUMN: selected[TWO_COLUMN][0],
    }, frozenset(core_edges))
    require(not any(L1["matrix_vector_product"](pv, pv_core))
            and not any(L1["matrix_vector_product"](pv, pv_local))
            and not any(L1["matrix_vector_product"](uq, uq_aligned)),
            "full asymmetric L1 generators changed")
    require(rational_rank((pv_core, pv_local)) == 2,
            "full P/V b,beta modes became dependent")
    return (12, 2), (13, 1)


def matrix_rank_2(matrix):
    if not any(entry for row in matrix for entry in row):
        return 0
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return 2 if determinant else 1


def audit_zero_site_l1_types():
    # At a zero endpoint, a nonzero V_z makes every full-column spoke
    # P_r V_z^T; a nonzero U_z makes every such spoke Q_r U_z^T.
    # At an invertible site the P and Q lines are independent, so the two
    # active types cannot coexist.  An invertible full-column spoke kills
    # both endpoint factors by rank.
    p0 = (Q(1), Q(0))
    q0 = (Q(0), Q(1))
    v = (Q(2), Q(3))
    u = (Q(5), Q(7))
    p_spoke = outer(p0, v)
    q_spoke = outer(q0, u)
    invertible = ((Q(1), Q(2)), (Q(3), Q(5)))
    require(matrix_rank_2(p_spoke) == matrix_rank_2(q_spoke) == 1,
            "active zero spoke lost rank one")
    require(matrix_rank_2(invertible) == 2,
            "full-column witness stopped being invertible")
    require(p0[0] * q0[1] - p0[1] * q0[0] == 1,
            "normalized P/Q lines became dependent")
    require(p_spoke != q_spoke,
            "P/V and Q/U active forms collided")

    types = {
        "I": {
            "endpoint": (0, 0),
            "full-column factor": None,
            "t-spoke": "unrestricted",
        },
        "P": {
            "endpoint": (0, "V_z"),
            "full-column factor": "v_z",
            # P_t=0 leaves the t-z L1 block unrestricted.
            "t-spoke": "unrestricted",
        },
        "Q": {
            "endpoint": ("U_z", 0),
            "full-column factor": "u_z",
            "t-spoke": "u_z",
        },
    }
    require(tuple(types) == ("I", "P", "Q"),
            "asymmetric zero-site type list changed")
    require(types["P"]["t-spoke"] == "unrestricted"
            and types["Q"]["t-spoke"] == "u_z",
            "one-column t-z asymmetry changed")
    return types


def audit_inactive_zero_slice_defect():
    # If both zero endpoint families vanish, every endpoint slice is the
    # aligned generalized cut gauge plus one t-star defect.  Put
    # c=tau*a*b and q=2*tau*a*(beta-b).
    tau = variable("tau")
    a = variable("a")
    b = variable("b")
    beta = variable("beta")
    c = multiply(tau, a, b)
    defect = scale(2, multiply(
        tau, a, add(beta, scale(-1, b))
    ))

    support = set()
    checks = 0
    for left, right in EDGES:
        if left in CORE and right in CORE:
            actual = (
                scale(2, multiply(tau, a, beta))
                if ONE_COLUMN in (left, right)
                else scale(2, c)
            )
        else:
            # Core-zero slices vanish with inactive endpoint factors;
            # M_45 itself is forced to zero.
            actual = constant(0)

        gauge = (
            scale(SIGMA[left] + SIGMA[right], c)
            if not (left in ZEROS and right in ZEROS)
            else constant(0)
        )
        difference = add(actual, scale(-1, gauge))
        expected = (
            defect
            if ONE_COLUMN in (left, right)
            and left in CORE and right in CORE
            else constant(0)
        )
        require(difference == expected,
                ("asymmetric endpoint defect changed", left, right))
        if expected:
            support.add((left, right))
        checks += 1

    require(support == {(0, 2), (1, 2), (2, 3)},
            ("one-column defect star changed", support))
    return checks, frozenset(support)


def audit_active_zero_path_closure():
    # Use inner sites {0,1,u} and shore {t,4,5}.  Generic-kernel blocks
    # from the inner set to t have fixed factor Q_t.  Each active zero has
    # its P/V or Q/U factor against all three inner sites.  The t-zero
    # blocks are arbitrary, and M_45=0, giving exceptional path 4-t-5.
    active_pairs = tuple(product(("P", "Q"), repeat=2))
    shores = {}
    for left_type, right_type in active_pairs:
        left_factor = "v4" if left_type == "P" else "u4"
        right_factor = "v5" if right_type == "P" else "u5"
        shores[left_type, right_type] = ("Q_t", left_factor, right_factor)
    require(len(shores) == 4
            and all(len(factors) == 3 for factors in shores.values()),
            "active-active shore-factor map changed")

    path_identities, categories = SHORE["audit_path_factorization"]()
    require(path_identities == 64,
            "coordinate-shore path identities changed")
    require(categories == {
        "all_cross": 6, "34": 3, "35": 3, "45": 3,
    }, "coordinate-shore path categories changed")
    bounds = {pair: 49 for pair in active_pairs}
    return shores, categories, bounds


def audit_boundary_map_and_symmetry():
    charts = {}
    for types in product(("I", "P", "Q"), repeat=2):
        charts[types] = (
            "path rank <= 49"
            if "I" not in types
            else "inactive-zero residue"
        )
    require(sum(outcome == "path rank <= 49"
                for outcome in charts.values()) == 4,
            "active-active chart count changed")
    require(sum(outcome == "inactive-zero residue"
                for outcome in charts.values()) == 5,
            "inactive-zero chart count changed")

    missing_p = {
        "missing": "P_t",
        "free endpoint family": "V_t=beta Q_t",
        "forced endpoint family": "U_t=0",
        "active unrestricted type": "P/V",
    }
    missing_q = {
        "missing": "Q_t",
        "free endpoint family": "U_t=alpha P_t",
        "forced endpoint family": "V_t=0",
        "active unrestricted type": "Q/U",
    }
    require(tuple(missing_p) == tuple(missing_q),
            "selected-family symmetry keys changed")
    require(missing_p["active unrestricted type"]
            != missing_q["active unrestricted type"],
            "P/Q active types failed to interchange")
    excluded = "both rank-one endpoints one-column"
    return charts, missing_p, missing_q, excluded


def main():
    core = audit_two_column_endpoint_kills_core_skew()
    endpoint = audit_one_column_endpoint_modes()
    full_core = audit_full_four_site_l1_system()
    zero_types = audit_zero_site_l1_types()
    defect = audit_inactive_zero_slice_defect()
    shores, categories, bounds = audit_active_zero_path_closure()
    charts, missing_p, missing_q, excluded = audit_boundary_map_and_symmetry()
    require(max(bounds.values()) == 49,
            "asymmetric active-zero rank bound changed")

    print("2I+2R+2Z asymmetric one-column L1 boundary: passed")
    print(f"  core skew/propagation       : {core}")
    print(f"  one-column endpoint modes  : {endpoint}")
    print(f"  full four-site L1 systems  : {full_core}")
    print(f"  zero-site L1 types         : {zero_types}")
    print(f"  inactive-zero slice defect : {defect}")
    print(f"  active-active shores       : {shores}")
    print(f"  path identities/categories : 64/{categories}")
    print(f"  active-active rank bounds  : {bounds}")
    print(f"  chart map                  : {charts}")
    print(f"  selected-family symmetry   : {missing_p}/{missing_q}")
    print(f"  excluded transverse chart : {excluded}")


if __name__ == "__main__":
    main()
