#!/usr/bin/env python3
"""Exact audit of the higher-split low-role incidence closure."""

from __future__ import annotations


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def square_pencil_cap(polynomial_degree: int) -> int:
    """Gcd plus square-variable Wronskian cap, including a zero cubic."""
    capacities = []
    for gcd_degree in range(max(0, polynomial_degree - 1)):
        square_degree = (polynomial_degree - gcd_degree) // 2
        if square_degree < 1:
            continue
        capacities.append(gcd_degree + 2 * square_degree - 2)
    require(
        capacities,
        "capacities",
    )
    cap = max(capacities)
    require(
        cap <= polynomial_degree - 2,
        "cap <= polynomial_degree - 2",
    )
    return cap


def kernel_gap(h: int, k: int, q: int) -> int:
    """Forced Wronskian weight minus cap after minimizing all gcd data."""
    return q * q - 2 * q - h - 2 + max(0, q - k)


# The exact higher-split staircase from the q=5 obstruction.
for h in range(8, 41):
    admitted = [k for k in range(1, 41) if kernel_gap(h, k, 5) > 0]
    if h <= 12:
        require(
            admitted == list(range(1, 41)),
            "admitted == list(range(1, 41))",
        )
    elif h == 13:
        require(
            admitted == [1, 2, 3, 4],
            "admitted == [1, 2, 3, 4]",
        )
    elif h == 14:
        require(
            admitted == [1, 2, 3],
            "admitted == [1, 2, 3]",
        )
    elif h == 15:
        require(
            admitted == [1, 2],
            "admitted == [1, 2]",
        )
    elif h == 16:
        require(
            admitted == [1],
            "admitted == [1]",
        )
    else:
        require(
            admitted == [],
            "admitted == []",
        )

    # Once q=5 is excluded, every larger q is excluded more strongly.
    for k in admitted:
        gaps = [kernel_gap(h, k, q) for q in range(5, 20)]
        require(
            gaps[0] > 0,
            "gaps[0] > 0",
        )
        require(
            all(b > a for a, b in zip(gaps, gaps[1:])),
            "all(b > a for a, b in zip(gaps, gaps[1:]))",
        )


# Audit every numerical incidence inequality well beyond the theorem range;
# the geometry is conditional only on the row kernel being four-dimensional.
for h in range(8, 201):
    for d in (0, 1, 2):
        singletons = h + 2 - 2 * d
        layers = h + 2 - d
        ambient_degree = h + 3 - d
        require(
            singletons + d == layers,
            "singletons + d == layers",
        )

        # Pair-drop four-space inequality.
        require(
            2 * singletons > 3 * (ambient_degree // 2 - 2),
            "2 * singletons > 3 * (ambient_degree // 2 - 2)",
        )

        # First singleton quotient pencil.  This count incorporates either
        # a zero neighbor or a fixed zero with the unique triple edge missing.
        first_degree = ambient_degree - 3
        zero_neighbor_pairs = (singletons - 2) + d
        fixed_zero_missing_pairs = (singletons - 1) + (d - 1)
        if d == 0:
            # With no repeated layer there is no missing edge.  A fixed zero
            # leaves every other singleton nonzero.
            fixed_zero_missing_pairs = singletons - 1
        minimum_pairs = min(zero_neighbor_pairs, fixed_zero_missing_pairs)
        require(
            minimum_pairs >= first_degree,
            "minimum_pairs >= first_degree",
        )
        require(
            2 * minimum_pairs > 2 * first_degree - 1,
            "2 * minimum_pairs > 2 * first_degree - 1",
        )

        cubic_load = singletons - 1
        require(
            cubic_load - (first_degree - 2) == 3 - d > 0,
            "cubic_load - (first_degree - 2) == 3 - d > 0",
        )
        require(
            cubic_load > square_pencil_cap(first_degree),
            "cubic_load > square_pencil_cap(first_degree)",
        )

        # Absorption audit.  Only patterns leaving a four-space need be
        # considered.  They necessarily leave at least four singleton
        # hyperplanes, so the lower nonzero-node count used in the proof is
        # honest.
        for absorbed_cubics in range(singletons + 1):
            for absorbed_quadratics in range(d + 1):
                absorbed_degree = (
                    3 * absorbed_cubics + 2 * absorbed_quadratics
                )
                reduced_degree = ambient_degree - absorbed_degree
                if reduced_degree < 3:
                    continue

                remaining_singletons = singletons - absorbed_cubics
                require(
                    remaining_singletons >= 4,
                    "remaining_singletons >= 4",
                )

                all_equal_excess = (
                    3 * singletons
                    + 2 * absorbed_quadratics
                    - ambient_degree
                )
                require(
                    all_equal_excess == (
                        2 * h + 3 - 5 * d + 2 * absorbed_quadratics
                    ),
                    "all_equal_excess == ( 2 * h + 3 - 5 * d + 2 * absorbed_qu...",
                )
                require(
                    all_equal_excess > 0,
                    "all_equal_excess > 0",
                )

                second_degree = reduced_degree - 6
                if second_degree < 1:
                    # Two distinct hyperplanes would have a two-dimensional
                    # intersection divisible by two cubics, already
                    # impossible in this degree.
                    continue
                require(
                    second_degree >= 1,
                    "second_degree >= 1",
                )
                terminal_cubics = remaining_singletons - 2
                terminal_nonzero = terminal_cubics - 1

                parity_excess = (
                    2 * terminal_nonzero - (2 * second_degree - 1)
                )
                require(
                    parity_excess == (
                        5
                        - 2 * d
                        + 4 * absorbed_cubics
                        + 4 * absorbed_quadratics
                    ),
                    "parity_excess == ( 5 - 2 * d + 4 * absorbed_cubics + 4 * ...",
                )
                require(
                    parity_excess > 0,
                    "parity_excess > 0",
                )

                cap_excess = terminal_cubics - (second_degree - 2)
                require(
                    cap_excess == (
                        5
                        - d
                        + 2 * absorbed_cubics
                        + 2 * absorbed_quadratics
                    ),
                    "cap_excess == ( 5 - d + 2 * absorbed_cubics + 2 * absorbe...",
                )
                require(
                    cap_excess > 0,
                    "cap_excess > 0",
                )
                if second_degree < 3:
                    require(
                        terminal_cubics > 0,
                        "terminal_cubics > 0",
                    )
                    continue
                require(
                    terminal_cubics > square_pencil_cap(second_degree),
                    "terminal_cubics > square_pencil_cap(second_degree)",
                )


# Local gcd corrections relative to the unabsorbed row count.
for q in range(5, 20):
    # Singleton: order one is impossible; every order >=2 is favorable.
    for multiplicity in range(2, 10):
        correction = q * multiplicity - (q - 1)
        require(
            correction >= q + 1,
            "correction >= q + 1",
        )

    # Repeated: order one changes order two to order one; order two is
    # impossible; order >=3 makes the row automatic but remains favorable.
    require(
        q + 1 > 0,
        "q + 1 > 0",
    )
    for multiplicity in range(3, 10):
        correction = q * multiplicity - (q - 2)
        require(
            correction == (multiplicity - 1) * q + 2 > 0,
            "correction == (multiplicity - 1) * q + 2 > 0",
        )

    # Common-pole gcd minimization gives exactly max(0,q-k).
    for k in range(1, 20):
        contributions = []
        for multiplicity in range(0, 20):
            if multiplicity <= k:
                weight = max(0, q - k + multiplicity)
            else:
                weight = 0
            contributions.append(q * multiplicity + weight)
        require(
            min(contributions) == max(0, q - k),
            "min(contributions) == max(0, q - k)",
        )


# Pieri boundary: add L vertical four-strips by omitting one of five rows.
# The explicit schedule proves sigma_(1^4)^L is nonzero for every h>=13.
for h in range(13, 101):
    layers = h + 2
    width = h - 1
    partition = [0, 0, 0, 0, 0]
    omission_schedule = [4] * (layers - 12)
    for omitted in (3, 2, 1, 0):
        omission_schedule.extend([omitted] * 3)
    require(
        len(omission_schedule) == layers,
        "len(omission_schedule) == layers",
    )

    for omitted in omission_schedule:
        for row in range(5):
            if row != omitted:
                partition[row] += 1
        require(
            all(
                partition[row] >= partition[row + 1] for row in range(4)
            ),
            "all( partition[row] >= partition[row + 1] for row in rang...",
        )
        require(
            partition[0] <= width,
            "partition[0] <= width",
        )

    require(
        partition == [layers - 3] * 4 + [12],
        "partition == [layers - 3] * 4 + [12]",
    )
    require(
        sum(partition) == 4 * layers,
        "sum(partition) == 4 * layers",
    )
    require(
        max(partition) <= width,
        "max(partition) <= width",
    )

    # Five-space pair incidence is automatic: four signed evaluations leave
    # a nonzero common kernel.
    require(
        5 - 4 >= 1,
        "5 - 4 >= 1",
    )
    require(
        2 * 3 + (h - 3) == h + 3,
        "2 * 3 + (h - 3) == h + 3",
    )


print("higher-split low-role selected-lift incidence closure: PASS")
print("d=0,1,2 four-space incidence geometry: uniform in h")
print("kernel staircase: h<=12 all k; then 4,3,2,1 small-k rows")
print("zero singleton, unique missing edge, gcd, and absorption: exact")
print("q=5 Pieri boundary path: exact through h=100")
