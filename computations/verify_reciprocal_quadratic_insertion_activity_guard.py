#!/usr/bin/env python3
"""N=8 guard: an active reciprocal quadratic insertion need not activate ports."""

from fractions import Fraction as F


P, R = 6, 7
RESIDUAL = tuple(range(6))
Q_EDGES = frozenset(((0, 1), (2, 3), (4, 5)))
P_PORTS = frozenset((0, 1))
R_PORTS = frozenset((2, 3))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def q_matching_count(vertices):
    return sum(
        all(tuple(sorted(edge)) in Q_EDGES for edge in matching)
        for matching in perfect_matchings(tuple(sorted(vertices)))
    )


def arm_cofactor_count(endpoint, port):
    """Count full-source matchings after deleting one endpoint-port arm."""

    other = R if endpoint == P else P
    remaining_residual = set(RESIDUAL) - {port}
    other_ports = R_PORTS if other == R else P_PORTS
    count = 0
    for other_port in other_ports & remaining_residual:
        after_other = remaining_residual - {other_port}
        count += q_matching_count(after_other)
    return count


def main():
    # The reciprocal direct pair is active: its deleted cofactor is q^[3].
    reciprocal_cofactor = q_matching_count(set(RESIDUAL))
    require(reciprocal_cofactor == 1, "reciprocal direct cofactor changed")

    # The permanent survivor uses artificial port insertions 02 and 13 (or
    # 03 and 12) and the remaining residual q-edge 45.
    insertion_pairings = (
        (((0, 2), (1, 3)), (4, 5)),
        (((0, 3), (1, 2)), (4, 5)),
    )
    for artificial_edges, cofactor_edge in insertion_pairings:
        require(set(sum((tuple(edge) for edge in artificial_edges), ())) == {0, 1, 2, 3},
                "artificial ports stopped covering four residual sites")
        require(tuple(sorted(cofactor_edge)) in Q_EDGES, "quadratic insertion cofactor died")

    candidate = (
        (F(1), F(1), F(1)),
        (F(-1), F(1), F(1)),
        (F(-1), F(-1), F(1)),
    )
    mixed_permanent = candidate[0][1] * candidate[1][2] + candidate[0][2] * candidate[1][1]
    require(mixed_permanent == 2, "reciprocal mixed permanent survivor changed")
    quadratic_insertion = mixed_permanent * q_matching_count({4, 5})
    require(quadratic_insertion == 2, "active quadratic insertion changed")

    # Nevertheless every original source arm supplying one of those four
    # port cells is dead.  After choosing it, the other endpoint can use one
    # port, but the four residual sites have only one q-edge rather than a
    # q^[2] perfect matching.
    arm_counts = {
        (P, port): arm_cofactor_count(P, port) for port in sorted(P_PORTS)
    } | {
        (R, port): arm_cofactor_count(R, port) for port in sorted(R_PORTS)
    }
    require(arm_counts == {(P, 0): 0, (P, 1): 0, (R, 2): 0, (R, 3): 0},
            "a quadratic port arm became active")

    # Original aggregate support graph: reciprocal PR, the four port arms,
    # and the three residual matching edges.  No residual endpoint is cubic.
    original_edges = set(Q_EDGES)
    original_edges.add((P, R))
    original_edges.update((P, port) for port in P_PORTS)
    original_edges.update((R, port) for port in R_PORTS)
    degrees = {
        vertex: sum(vertex in edge for edge in original_edges)
        for vertex in range(8)
    }
    require(degrees == {0: 2, 1: 2, 2: 2, 3: 2, 4: 1, 5: 1, 6: 3, 7: 3},
            "source support degree guard changed")
    require(not any(degrees[v] == 3 for v in RESIDUAL),
            "an internal adjacent-cubic candidate appeared")

    # A complementary diagonal-response skeleton shows that the permanent
    # no-go does not force *any* active quadratic survivor.  Give colour i a
    # p/s port pair equal to the endpoints of the i-th q edge.  Each diagonal
    # response then has an active q^[2] cofactor.  Principal quadratic minors
    # have an active q^[1] cofactor but vanish for `candidate`; every mixed
    # nonzero permanent leaves endpoints from two different q edges and its
    # q^[1] cofactor is zero.
    q_pairs = ((0, 1), (2, 3), (4, 5))
    p_site = {colour: q_pairs[colour][0] for colour in range(3)}
    r_site = {colour: q_pairs[colour][1] for colour in range(3)}
    diagonal_response = {
        colour: q_matching_count(
            set(RESIDUAL) - {p_site[colour], r_site[colour]}
        )
        for colour in range(3)
    }
    require(diagonal_response == {0: 1, 1: 1, 2: 1},
            "diagonal response skeleton lost activity")

    pairs = ((0, 1), (0, 2), (1, 2))
    quadratic_channels = {}
    total_quadratic = F(0)
    for rows in pairs:
        for columns in pairs:
            sites = (
                p_site[rows[0]], p_site[rows[1]],
                r_site[columns[0]], r_site[columns[1]],
            )
            cofactor = (
                0 if len(set(sites)) < 4
                else q_matching_count(set(RESIDUAL) - set(sites))
            )
            permanent = (
                candidate[rows[0]][columns[0]] * candidate[rows[1]][columns[1]]
                + candidate[rows[0]][columns[1]] * candidate[rows[1]][columns[0]]
            )
            quadratic_channels[(rows, columns)] = (permanent, cofactor)
            total_quadratic += permanent * cofactor
    require(
        all(
            (permanent == 0 and cofactor == 1) if rows == columns
            else (cofactor == 0)
            for (rows, columns), (permanent, cofactor) in quadratic_channels.items()
        ),
        "permanent/cofactor complementary support changed",
    )
    require(any(permanent for permanent, _cofactor in quadratic_channels.values()),
            "3x3 permanent obstruction disappeared")
    require(total_quadratic == 0, "source-specific cofactor annihilation failed")

    print("reciprocal quadratic-insertion activity guard: PASS")
    print(f"reciprocal q^[3] cofactor={reciprocal_cofactor}")
    print(f"surviving artificial pairings={insertion_pairings}; coefficient={quadratic_insertion}")
    print(f"original port-arm cofactors={arm_counts}")
    print(f"original support degrees={degrees}")
    print(f"diagonal response cofactors={diagonal_response}")
    print(f"permanent/cofactor channel ledger={quadratic_channels}; total={total_quadratic}")
    print("verdict=the permanent no-go need not yield an active channel; even an active channel need not activate original arms/cubic pair")


if __name__ == "__main__":
    main()
