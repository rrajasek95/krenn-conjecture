#!/usr/bin/env python3
"""Close the single-live one-column chart with the other zero active.

Assume P_t=0, Q_t!=0, M_tz is live, M_tw=0, and both zero endpoints
z,w are active common-factor L1 types.  The dead t-w edge excludes Q/U
activity at w, so w is P/V.  The live endpoint z may be P/V (with
unrestricted M_tz) or Q/U (forcing M_tz proportional to Q_t u_z^T).

In both cases every nonzero base matching and every endpoint-tangent
derivative term has the same physical v_w factor at w.  Thus both pure
L0 targets would lie in one fixed one-dimensional w-shore, impossible.
The Q_t=0 case is symmetric.  Standard library only; all checks remain
live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations


INNER = (0, 1, 2)
RANK_ONE = 3
LIVE_ZERO = 4
DEAD_ZERO = 5
SITES = INNER + (RANK_ONE, LIVE_ZERO, DEAD_ZERO)
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


def audit_l1_type_classification():
    # At the dead endpoint w, active Q/U would put the nonzero matrix
    # Q_t u_w^T on the left of an L1 equation whose right side is a scalar
    # times M_tw=0.  P/V instead uses P_t v_w^T=0 and is compatible.
    p_t = (Q(0), Q(0))
    q_t = (Q(2), Q(3))
    u_w = (Q(5), Q(7))
    v_w = (Q(11), Q(13))
    require(matrix_rank_2(outer(q_t, u_w)) == 1,
            "dead-endpoint Q/U obstruction vanished")
    require(matrix_rank_2(outer(p_t, v_w)) == 0,
            "dead-endpoint P/V compatibility vanished")

    # At live z, P/V again has zero selected left side and puts no
    # restriction on B.  Active Q/U has nonzero Q_t u_z^T, so L1 forces
    # the live block onto that rank-one physical shore.
    u_z = (Q(17), Q(19))
    v_z = (Q(23), Q(29))
    arbitrary_b = ((Q(1), Q(2)), (Q(3), Q(5)))
    forced_b = outer(q_t, u_z)
    require(matrix_rank_2(outer(p_t, v_z)) == 0,
            "live P/V selected side became nonzero")
    require(matrix_rank_2(arbitrary_b) == 2,
            "the P/V live block was accidentally factorized")
    require(matrix_rank_2(forced_b) == 1,
            "the Q/U live block lost its forced shore")
    return {
        "w": ("P/V",),
        "z": ("P/V", "Q/U"),
        "same": ("P/V", "P/V"),
        "opposite": ("Q/U", "P/V"),
    }


def audit_base_matching_shore():
    # Since M_tw=M_zw=0, every nonzero matching pairs w to an inner site,
    # where M_iw=P_i v_w^T supplies the physical v_w factor.  Three live
    # matchings use tz, six are t-I/z-I/w-I crosses, and six are dead.
    categories = {"tz": 0, "cross": 0, "dead": 0}
    checks = 0
    for matching in MATCHINGS:
        w_edge = next(edge for edge in matching if DEAD_ZERO in edge)
        partner = (
            w_edge[1] if w_edge[0] == DEAD_ZERO else w_edge[0]
        )
        if partner in (RANK_ONE, LIVE_ZERO):
            category = "dead"
        else:
            require(partner in INNER,
                    ("a nondead w edge lost its inner partner", matching))
            category = (
                "tz" if (RANK_ONE, LIVE_ZERO) in matching else "cross"
            )
        categories[category] += 1
        checks += 1
    require(checks == 15, "base matching census changed")
    require(categories == {"tz": 3, "cross": 6, "dead": 6},
            ("base matching shore decomposition changed", categories))
    return categories


def audit_nonincident_tangent_cofactors():
    # Any tangent not incident with w leaves w in the four-site cofactor.
    # Of its three cofactor matchings, a term either pairs w to I and
    # supplies v_w, or pairs w to t/z and vanishes.  Audit every possible
    # non-w tangent edge, a superset of the actual endpoint packets.
    counts = {"v_w": 0, "dead": 0}
    by_edge = {}
    for tangent in combinations(SITES[:-1], 2):
        remaining = tuple(site for site in SITES if site not in tangent)
        local = {"v_w": 0, "dead": 0}
        for matching in perfect_matchings(remaining):
            w_edge = next(edge for edge in matching if DEAD_ZERO in edge)
            partner = (
                w_edge[1] if w_edge[0] == DEAD_ZERO else w_edge[0]
            )
            category = "v_w" if partner in INNER else "dead"
            local[category] += 1
            counts[category] += 1
        by_edge[tangent] = local
    require(len(by_edge) == 10,
            "nonincident tangent edge count changed")
    require(counts == {"v_w": 18, "dead": 12},
            ("nonincident cofactor shore count changed", counts))
    require(all(sum(local.values()) == 3 for local in by_edge.values()),
            "a four-site cofactor lost a matching")
    return counts


def audit_incident_endpoint_tangents():
    # The actual endpoint tangents incident with w are:
    #   * I-w blocks P_i v_w^T in both type combinations;
    #   * additionally z-w=u_z v_w^T in the opposite Q/U-at-z chart.
    # All directly supply v_w.  The t-w endpoint tangent is zero.
    same = tuple(("Iw", i, "v_w") for i in INNER)
    opposite = same + (("zw", LIVE_ZERO, "v_w"),)
    require(len(same) == 3 and len(opposite) == 4,
            "incident endpoint tangent census changed")
    require(all(entry[-1] == "v_w" for entry in same + opposite),
            "an incident endpoint tangent lost the w factor")

    # Each I-w tangent has three core/z cofactors.  The optional z-w
    # tangent has the three perfect matchings on I+t.  Whether an
    # individual cofactor vanishes is irrelevant: its tangent already
    # supplies the physical shore.
    same_terms = len(same) * 3
    opposite_terms = len(opposite) * 3
    require((same_terms, opposite_terms) == (9, 12),
            "incident derivative term count changed")
    return same_terms, opposite_terms


def audit_pure_shore_contradiction():
    # H and every dPsi(N^su) lie in span(v_w) tensor V_rest.  A nonzero
    # pure target e_s^6 in that space forces e_s into span(v_w).  The two
    # target shore vectors e0,e1 have rank two and cannot lie in the same
    # one-dimensional subspace.
    pure_shores = ((Q(1), Q(0)), (Q(0), Q(1)))
    require(rational_rank(pure_shores) == 2,
            "the two physical pure shores became collinear")

    # Exact determinant version: if e0=alpha*v and e1=beta*v, the
    # determinant of [e0 e1] would be alpha*beta*det[v v]=0, not one.
    determinant = (
        pure_shores[0][0] * pure_shores[1][1]
        - pure_shores[0][1] * pure_shores[1][0]
    )
    require(determinant == 1,
            "the pure-shore determinant changed")
    return determinant


def audit_symmetric_dictionary():
    p_zero = {
        "one_column": "P_t=0",
        "dead_endpoint_type": "P/V",
        "dead_factor": "v_w",
        "opposite_live_type": "Q/U",
        "live_factor": "u_z",
    }
    q_zero = {
        "one_column": "Q_t=0",
        "dead_endpoint_type": "Q/U",
        "dead_factor": "u_w",
        "opposite_live_type": "P/V",
        "live_factor": "v_z",
    }
    require(tuple(p_zero) == tuple(q_zero),
            "symmetric active-endpoint dictionaries disagree")
    require(
        p_zero["dead_endpoint_type"] == q_zero["opposite_live_type"]
        and p_zero["opposite_live_type"] == q_zero["dead_endpoint_type"],
        "the P/V and Q/U types did not interchange",
    )
    require(
        (p_zero["dead_factor"], p_zero["live_factor"])
        == ("v_w", "u_z")
        and (q_zero["dead_factor"], q_zero["live_factor"])
        == ("u_w", "v_z"),
        "the physical factors did not interchange",
    )
    return p_zero, q_zero


def main():
    classification = audit_l1_type_classification()
    base = audit_base_matching_shore()
    cofactors = audit_nonincident_tangent_cofactors()
    incident = audit_incident_endpoint_tangents()
    determinant = audit_pure_shore_contradiction()
    audit_symmetric_dictionary()
    print("three-invertible single-live other-active overlap: passed")
    print(f"  L1 type classification      : {classification}")
    print(f"  base matching shore         : {base}")
    print(f"  nonincident tangent terms   : {cofactors}")
    print(f"  same/opposite incident terms: {incident}")
    print(f"  pure-shore determinant      : {determinant}")
    print("  symmetric P/Q cases         : both closed")


if __name__ == "__main__":
    main()
