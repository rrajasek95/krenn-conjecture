#!/usr/bin/env python3
"""Close the free-edge boundary of the binary 2I+3R+1Z stratum.

Let sites 0,1 be invertible, site 2 be zero, and sites 3,4,5 be
nonzero rank one.  At least one edge from 2 to the rank-one shore has
zero multiplier sum and is therefore arbitrary.  The checker verifies:

* the nine possible free-star/exceptional-shore potential patterns;
* the exact zero-cofactor columns when the two invertible-zero blocks vanish;
* the 46 and 54 shore-slice bounds when such a block can instead be free;
* the one-dimensional composite fiber closing the sole away-edge case;
* the 29-dimensional three-free-edge matching-tensor factorization; and
* the two explicit cancellation kernels in the zero-potential triangle.

Together these give rank(dPsi) <= 54 throughout the free-edge boundary.
Standard library only; checks remain live under python -O and python -I -S.
"""

from collections import Counter
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


COLOURS = (0, 1)
SITES = tuple(range(6))
INVERTIBLE = (0, 1)
ZERO = 2
SHORE = (3, 4, 5)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)


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


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}


# Canonical support types, up to relabeling sites 3,4,5.  The free set is
# F={r: nu_2+nu_r=0}; exceptional edges have nu_r+nu_s=0.
CASES = {
    "F1_empty": (frozenset((3,)), frozenset()),
    "F1_incident": (frozenset((3,)), frozenset(((3, 4),))),
    "F1_away": (frozenset((3,)), frozenset(((4, 5),))),
    "F1_path": (frozenset((3,)), frozenset(((3, 4), (3, 5)))),
    "F2_empty": (frozenset((3, 4)), frozenset()),
    "F2_mutual": (frozenset((3, 4)), frozenset(((3, 4),))),
    "F2_fan": (frozenset((3, 4)), frozenset(((3, 5), (4, 5)))),
    "F3_empty": (frozenset(SHORE), frozenset()),
    "F3_triangle": (
        frozenset(SHORE), frozenset(combinations(SHORE, 2))
    ),
}


def classify_potentials(values):
    zeta, *rank_one = values
    free_local = frozenset(
        index for index, value in enumerate(rank_one)
        if value == -zeta
    )
    require(free_local, ("not on the free boundary", values))
    exceptional_local = frozenset(
        edge for edge in combinations(range(3), 2)
        if rank_one[edge[0]] + rank_one[edge[1]] == 0
    )
    free_count = len(free_local)
    if free_count == 1:
        free_vertex = next(iter(free_local))
        if not exceptional_local:
            return "F1_empty"
        if len(exceptional_local) == 1:
            edge = next(iter(exceptional_local))
            return "F1_incident" if free_vertex in edge else "F1_away"
        require(
            len(exceptional_local) == 2
            and all(free_vertex in edge for edge in exceptional_local),
            ("bad one-free pattern", values, exceptional_local),
        )
        return "F1_path"
    if free_count == 2:
        mutual = tuple(sorted(free_local))
        if not exceptional_local:
            return "F2_empty"
        if exceptional_local == frozenset((mutual,)):
            return "F2_mutual"
        nonfree = next(index for index in range(3) if index not in free_local)
        fan = frozenset(
            tuple(sorted((vertex, nonfree))) for vertex in free_local
        )
        require(exceptional_local == fan,
                ("bad two-free pattern", values, exceptional_local))
        return "F2_fan"
    require(free_count == 3, ("bad free count", values))
    if not exceptional_local:
        return "F3_empty"
    require(
        exceptional_local == frozenset(combinations(range(3), 2)),
        ("bad three-free pattern", values, exceptional_local),
    )
    return "F3_triangle"


def audit_potential_classification():
    seen = set()
    compatible_seen = set()
    examples = {}
    for values in product(range(-3, 4), repeat=4):
        zeta, *rank_one = values
        if all(value != -zeta for value in rank_one):
            continue
        name = classify_potentials(values)
        seen.add(name)
        examples.setdefault(name, values)
        if zeta not in rank_one:
            compatible_seen.add(name)
    require(seen == set(CASES), ("potential patterns changed", seen))

    # If M_{i2} is free, nu_i=-zeta.  The invertible-rank-one numerator
    # is nonzero, so no rank-one potential may then equal zeta.
    allowed_with_free_i2 = compatible_seen
    require(
        allowed_with_free_i2
        == {"F1_empty", "F1_away", "F2_empty", "F3_empty"},
        ("free invertible-zero compatibility changed", allowed_with_free_i2),
    )
    return examples, allowed_with_free_i2


def support_value(case, edge, colours, zero_i2=False):
    free, exceptional = CASES[case]
    u, v = edge
    a, b = colours
    if v <= ZERO:
        if zero_i2 and v == ZERO and u in INVERTIBLE:
            return False
        return True
    if u in INVERTIBLE and v in SHORE:
        return b == 0
    if u == ZERO and v in SHORE:
        return v in free
    if edge in exceptional:
        return True
    return a == 0 and b == 0


def cofactor_may_live(edge, word, live):
    complement = tuple(site for site in SITES if site not in edge)
    return any(
        all(live(pair, (word[pair[0]], word[pair[1]]))
            for pair in matching)
        for matching in MATCHINGS[complement]
    )


def zero_differential_cells(case, zero_i2):
    def live(edge, colours):
        return support_value(case, edge, colours, zero_i2=zero_i2)

    answer = []
    for cell in CELLS:
        u, v, a, b = cell
        if not any(
            (word[u], word[v]) == (a, b)
            and cofactor_may_live((u, v), word, live)
            for word in product(COLOURS, repeat=6)
        ):
            answer.append(cell)
    return tuple(answer)


def graph_connected(vertices, edges):
    vertices = set(vertices)
    seen = {next(iter(vertices))}
    while True:
        expanded = seen | {
            v for u, v in edges if u in seen
        } | {
            u for u, v in edges if v in seen
        }
        expanded &= vertices
        if expanded == seen:
            return seen == vertices
        seen = expanded


def graph_nonbipartite(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colours = {}
    for root in vertices:
        if root in colours:
            continue
        colours[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in colours:
                    colours[v] = 1 - colours[u]
                    stack.append(v)
                elif colours[v] == colours[u]:
                    return True
    return False


def audit_zero_i2_bounds():
    one_free_counts = {}
    for case in ("F1_empty", "F1_incident", "F1_away", "F1_path"):
        zero = zero_differential_cells(case, zero_i2=True)
        require(len(zero) == 16, ("wrong one-free zero columns", case, zero))
        one_free_counts[case] = len(zero)

    two_free_counts = {}
    for case in ("F2_empty", "F2_mutual", "F2_fan"):
        zero = zero_differential_cells(case, zero_i2=True)
        expected = tuple(
            (3, 4, a, b) for a, b in product(COLOURS, repeat=2)
        )
        require(zero == expected, ("wrong two-free zero columns", case, zero))
        two_free_counts[case] = len(zero)

        # After deleting the free-free edge, the generic live graph remains
        # connected and contains the 0-1-3 triangle.  Hence its five
        # sum-zero vertex gauges are independent of the four zero columns.
        live_edges = {
            edge for edge in EDGES
            if edge != (3, 4)
            and any(support_value(case, edge, colours, zero_i2=True)
                    for colours in product(COLOURS, repeat=2))
        }
        require(graph_connected(SITES, live_edges),
                ("two-free deletion disconnected", case))
        require(graph_nonbipartite(SITES, live_edges),
                ("two-free deletion became bipartite", case))

    require(60 - 16 == 44, "one-free zero-column bound changed")
    require(60 - (4 + 5) == 51, "two-free gauge bound changed")
    return one_free_counts, two_free_counts


def shore_slice_bounds(case):
    def live(edge, colours):
        return support_value(case, edge, colours, zero_i2=False)

    bounds = {}
    for shore_word in product(COLOURS, repeat=3):
        active = set()
        for inner_word in product(COLOURS, repeat=3):
            word = inner_word + shore_word
            for cell in CELLS:
                u, v, a, b = cell
                if (word[u], word[v]) != (a, b):
                    continue
                if cofactor_may_live((u, v), word, live):
                    active.add(cell)
        bounds[shore_word] = min(8, len(active))
    return bounds


def audit_free_i2_slice_bounds():
    expected = {
        "F1_empty": {
            (0, 0, 0): 8, (0, 0, 1): 8,
            (0, 1, 0): 8, (0, 1, 1): 1,
            (1, 0, 0): 8, (1, 0, 1): 6,
            (1, 1, 0): 6, (1, 1, 1): 1,
        },
        "F2_empty": {
            (0, 0, 0): 8, (0, 0, 1): 8,
            (0, 1, 0): 8, (0, 1, 1): 6,
            (1, 0, 0): 8, (1, 0, 1): 6,
            (1, 1, 0): 8, (1, 1, 1): 2,
        },
    }
    for case, wanted in expected.items():
        actual = shore_slice_bounds(case)
        require(actual == wanted, ("shore slice bounds changed", case, actual))
    require(sum(expected["F1_empty"].values()) == 46,
            "one-free slice bound changed")
    require(sum(expected["F2_empty"].values()) == 54,
            "two-free slice bound changed")
    return {case: sum(bounds.values()) for case, bounds in expected.items()}


# Sparse formal polynomial arithmetic.
def variable(name):
    return Counter({(name,): 1})


def polynomial_add(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return Counter({key: value for key, value in answer.items() if value})


def polynomial_scale(scalar, value):
    return Counter({key: scalar * coefficient
                    for key, coefficient in value.items()
                    if scalar * coefficient})


def polynomial_subtract(left, right):
    return polynomial_add(left, polynomial_scale(-1, right))


def polynomial_multiply(*values):
    answer = Counter({(): 1})
    for value in values:
        updated = Counter()
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in value.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] += left_coefficient * right_coefficient
        answer = Counter({key: value for key, value in updated.items() if value})
    return answer


def build_formal_packet(case, zero_i2=False, constant_triangle=False):
    packet = {}
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            if constant_triangle and u in INVERTIBLE and v in SHORE:
                name = f"C_{u}_{a}" if b == 0 else None
            elif support_value(case, (u, v), (a, b), zero_i2=zero_i2):
                name = f"M_{u}_{v}_{a}_{b}"
            else:
                name = None
            packet[u, v, a, b] = variable(name) if name else Counter()
    return packet


def formal_hafnian(packet, vertices, word):
    total = Counter()
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        term = Counter({(): 1})
        for u, v in matching:
            term = polynomial_multiply(term, packet[u, v, word[u], word[v]])
        total = polynomial_add(total, term)
    return total


def formal_matching_tensor(packet, word):
    return formal_hafnian(packet, SITES, word)


def audit_away_composite_fiber():
    packet = build_formal_packet("F1_away")
    selected_edges = frozenset(((0, 4), (0, 5), (1, 4), (1, 5)))
    baseline = dict(packet)
    for u, v in selected_edges:
        for a, b in product(COLOURS, repeat=2):
            baseline[u, v, a, b] = Counter()

    identities = 0
    for word in product(COLOURS, repeat=6):
        A = packet[0, 4, word[0], word[4]]
        C = packet[0, 5, word[0], word[5]]
        B = packet[1, 4, word[1], word[4]]
        D = packet[1, 5, word[1], word[5]]
        p = packet[3, 4, word[3], word[4]]
        q = packet[3, 5, word[3], word[5]]
        zr = packet[2, 3, word[2], word[3]]
        k_0z = packet[0, 2, word[0], word[2]]
        k_1z = packet[1, 2, word[1], word[2]]
        expected = polynomial_add(
            polynomial_multiply(zr, polynomial_add(
                polynomial_multiply(A, D),
                polynomial_multiply(C, B),
            )),
            polynomial_multiply(p, polynomial_add(
                polynomial_multiply(C, k_1z),
                polynomial_multiply(D, k_0z),
            )),
            polynomial_multiply(q, polynomial_add(
                polynomial_multiply(A, k_1z),
                polynomial_multiply(B, k_0z),
            )),
        )
        selected_part = polynomial_subtract(
            formal_matching_tensor(packet, word),
            formal_matching_tensor(baseline, word),
        )
        require(selected_part == expected,
                ("away-edge factorization failed", word))
        identities += 1

    # The selected spokes enter only through
    # F=A tensor D+C tensor B, E=qA+pC, G=qB+pD.
    # Put S=pC-qA and R=pD-qB.  The displayed tangent kills F,E,G.
    p, q = variable("p"), variable("q")
    A = tuple(variable(f"A{i}") for i in COLOURS)
    B = tuple(variable(f"B{i}") for i in COLOURS)
    C = tuple(variable(f"C{i}") for i in COLOURS)
    D = tuple(variable(f"D{i}") for i in COLOURS)
    S = tuple(polynomial_subtract(
        polynomial_multiply(p, C[i]), polynomial_multiply(q, A[i])
    ) for i in COLOURS)
    R = tuple(polynomial_subtract(
        polynomial_multiply(p, D[i]), polynomial_multiply(q, B[i])
    ) for i in COLOURS)
    dA = tuple(polynomial_multiply(p, value) for value in S)
    dC = tuple(polynomial_scale(-1, polynomial_multiply(q, value))
               for value in S)
    dB = tuple(polynomial_scale(-1, polynomial_multiply(p, value))
               for value in R)
    dD = tuple(polynomial_multiply(q, value) for value in R)

    for i in COLOURS:
        require(not polynomial_add(
            polynomial_multiply(q, dA[i]),
            polynomial_multiply(p, dC[i]),
        ), "away composite E tangent did not vanish")
        require(not polynomial_add(
            polynomial_multiply(q, dB[i]),
            polynomial_multiply(p, dD[i]),
        ), "away composite G tangent did not vanish")
    for i, j in product(COLOURS, repeat=2):
        dF = polynomial_add(
            polynomial_multiply(dA[i], D[j]),
            polynomial_multiply(A[i], dD[j]),
            polynomial_multiply(dC[i], B[j]),
            polynomial_multiply(C[i], dB[j]),
        )
        require(not dF, ("away composite F tangent did not vanish", i, j))

    support_parameters = sum(
        support_value("F1_away", (u, v), (a, b))
        for u, v, a, b in CELLS
    )
    require(support_parameters == 34, "away support count changed")

    # On the dense open set p*q*S*R != 0, this tangent is nonzero.  It is
    # independent of the five vertex gauges because deleting its four spoke
    # edges leaves a connected nonbipartite generic live graph.  Polynomiality
    # extends restricted rank <=34-6 from that dense open set to the closure.
    remaining_edges = {
        edge for edge in EDGES
        if edge not in selected_edges
        and any(support_value("F1_away", edge, colours)
                for colours in product(COLOURS, repeat=2))
    }
    require(graph_connected(SITES, remaining_edges),
            "away-fiber gauge-complement graph disconnected")
    require(graph_nonbipartite(SITES, remaining_edges),
            "away-fiber gauge-complement graph became bipartite")
    restricted_bound = support_parameters - 6
    transverse = 60 - support_parameters
    require((restricted_bound, transverse, restricted_bound + transverse)
            == (28, 26, 54), "away composite dimension bound changed")
    return identities, 54


def audit_three_free_empty_factorization():
    packet = build_formal_packet("F3_empty")
    identities = 0
    for word in product(COLOURS, repeat=6):
        # Matchings not using a z-shore edge are confined to shore word 000.
        base = Counter()
        for matching in MATCHINGS[SITES]:
            if any(ZERO in edge and next(v for v in edge if v != ZERO) in SHORE
                   for edge in matching):
                continue
            term = Counter({(): 1})
            for u, v in matching:
                term = polynomial_multiply(
                    term, packet[u, v, word[u], word[v]]
                )
            base = polynomial_add(base, term)

        expected = base
        for t in SHORE:
            u, v = tuple(site for site in SHORE if site != t)
            if word[u] or word[v]:
                continue
            h_t = polynomial_add(
                polynomial_multiply(
                    packet[0, 1, word[0], word[1]],
                    packet[min(u, v), max(u, v), 0, 0],
                ),
                polynomial_multiply(
                    packet[0, u, word[0], 0],
                    packet[1, v, word[1], 0],
                ),
                polynomial_multiply(
                    packet[0, v, word[0], 0],
                    packet[1, u, word[1], 0],
                ),
            )
            expected = polynomial_add(expected, polynomial_multiply(
                packet[ZERO, t, word[ZERO], word[t]], h_t
            ))
        require(formal_matching_tensor(packet, word) == expected,
                ("three-free empty factorization failed", word))
        identities += 1

    # Enlarge the shore-000 tensor F to an arbitrary 3-qubit tensor (8),
    # and each B_t tensor H_t product to a 4-by-4 Segre cone (dimension 7).
    restricted_bound = 8 + 3 * (4 + 4 - 1)
    support_parameters = sum(
        support_value("F3_empty", (u, v), (a, b))
        for u, v, a, b in CELLS
    )
    transverse = 60 - support_parameters
    require((support_parameters, transverse, restricted_bound)
            == (39, 21, 29), "three-free dimension count changed")
    require(restricted_bound + transverse == 50,
            "three-free empty bound changed")
    return identities, 50


def audit_triangle_cancellation():
    packet = build_formal_packet(
        "F3_triangle", zero_i2=True, constant_triangle=True
    )
    identities = 0
    for z_colour in COLOURS:
        tangent = {cell: Counter() for cell in CELLS}
        for i in INVERTIBLE:
            sign = 1 if i == 0 else -1
            for i_colour in COLOURS:
                cell = (i, ZERO, i_colour, z_colour)
                tangent[cell] = polynomial_scale(
                    sign, packet[i, 3, i_colour, 0]
                )

        for word in product(COLOURS, repeat=6):
            total = Counter()
            for cell, variation in tangent.items():
                if not variation:
                    continue
                u, v, a, b = cell
                if (word[u], word[v]) != (a, b):
                    continue
                complement = tuple(site for site in SITES if site not in (u, v))
                total = polynomial_add(total, polynomial_multiply(
                    variation, formal_hafnian(packet, complement, word)
                ))
            require(not total, ("triangle cancellation failed", z_colour, word))
            identities += 1

    # The two tangents have disjoint z colours and are supported on the two
    # zero base edges 02,12, whereas all vertex gauges vanish on those edges.
    # The generic live graph is connected and nonbipartite, so five gauges
    # plus these two directions give kernel dimension at least seven.
    live_edges = {
        edge for edge in EDGES
        if any(
            (packet[edge[0], edge[1], a, b])
            for a, b in product(COLOURS, repeat=2)
        )
    }
    require(graph_connected(SITES, live_edges),
            "triangle live graph disconnected")
    require(graph_nonbipartite(SITES, live_edges),
            "triangle live graph became bipartite")
    require(60 - (5 + 2) == 53, "triangle cancellation bound changed")
    return identities, 53


def build_numeric_packet(case, zero_i2=False, constant_triangle=False):
    packet = {}
    constants = {
        (i, a): 2 + 7 * i + 5 * a
        for i in INVERTIBLE for a in COLOURS
    }
    for edge_index, (u, v) in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            if constant_triangle and u in INVERTIBLE and v in SHORE:
                value = constants[u, a] if b == 0 else 0
            elif support_value(case, (u, v), (a, b), zero_i2=zero_i2):
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            else:
                value = 0
            packet[u, v, a, b] = value
    return packet


def audit_calibration_ranks():
    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    specifications = (
        ("F1_empty", False, False, 35),
        ("F2_empty", False, False, 41),
        ("F1_away", False, False, 48),
        ("F3_empty", False, False, 44),
        ("F3_triangle", True, True, 47),
    )
    ranks = {}
    for case, zero_i2, constant, expected in specifications:
        derivative = core["differential"](
            build_numeric_packet(case, zero_i2, constant)
        )
        actual = tuple(
            core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        )
        require(actual == (expected, expected),
                ("calibration rank changed", case, actual))
        ranks[case + ("_constant" if constant else "")] = actual
    return ranks


def main():
    examples, free_i2_cases = audit_potential_classification()
    previous = run_path(str(Path(__file__).with_name(
        "verify_level_two_two_invertible_three_rank_one_one_zero_closure.py"
    )))
    isotropic_branches = previous["audit_triangle_common_isotropic_line"]()
    one_free, two_free = audit_zero_i2_bounds()
    slice_bounds = audit_free_i2_slice_bounds()
    away_identities, away_bound = audit_away_composite_fiber()
    three_identities, three_bound = audit_three_free_empty_factorization()
    triangle_identities, triangle_bound = audit_triangle_cancellation()
    calibrations = audit_calibration_ranks()
    bounds = {
        "zero_i2_F1": 44,
        "zero_i2_F2": 51,
        "free_i2_F1_empty": slice_bounds["F1_empty"],
        "free_i2_F1_away": away_bound,
        "free_i2_F2_empty": slice_bounds["F2_empty"],
        "F3_empty": three_bound,
        "F3_triangle": triangle_bound,
    }
    require(max(bounds.values()) == 54,
            ("free-edge maximum bound changed", bounds))
    print("2I+3R+1Z free-edge closure: all checks passed")
    print(f"  potential patterns          : {tuple(sorted(examples))}")
    print(f"  free i-z compatible cases  : {tuple(sorted(free_i2_cases))}")
    print(f"  zero-i-z columns F1/F2     : {one_free}, {two_free}")
    print(f"  formal identities away/F3 : {away_identities}/{three_identities}")
    print(f"  triangle cancellations     : {triangle_identities}")
    print(f"  triangle isotropic branches: {isotropic_branches}")
    print(f"  exact modular calibrations : {calibrations}")
    print(f"  covariant rank bounds      : {bounds}")
    print(f"  maximum differential rank : {max(bounds.values())}")


if __name__ == "__main__":
    main()
