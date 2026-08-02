#!/usr/bin/env python3
"""Independent audit of the h=3 selected-cap landing counterguard.

This checker does not import the primary checker.  It encodes the two
committed scalar block packets as single eight-site cell tables, enumerates
matchings independently, and reconstructs the cap, overlap, anchor, and
rank ledgers.  It also counts failures of the full pq tensor EqSystem so
that selected-word scope is executable rather than only documentary.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product


ZERO = F(0)
ONE = F(1)
COLORS = range(3)
INTERNAL = tuple(range(6))
P = 6
Q = 7
ALL_SITES = tuple(range(8))
LABELS = (0, 1, 2, 0, 1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def key(a, b, ca, cb):
    if a < b:
        return (a, b, ca, cb)
    return (b, a, cb, ca)


def cells_from_rows(rows):
    cells = {}
    for a, b, ca, cb, numerator, denominator in rows:
        k = key(a, b, ca, cb)
        value = F(numerator, denominator)
        require(value and k not in cells, f"bad explicit cell {k}")
        cells[k] = value
    return cells


DIRECT_FREE_ROWS = (
    (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, 1),
    (0, 3, 0, 1, 1, 1), (0, 4, 0, 1, 1, 1),
    (0, 5, 0, 2, 1, 1), (0, 6, 0, 0, 1, 1),
    (1, 2, 1, 2, 1, 1), (1, 3, 1, 2, 1, 1),
    (1, 4, 1, 1, 1, 1), (1, 6, 1, 1, 1, 1),
    (2, 3, 2, 0, 1, 1), (2, 6, 2, 2, 1, 1),
    (3, 4, 0, 1, 1, 1), (3, 5, 0, 2, 1, 1),
    (3, 7, 0, 0, 1, 1), (4, 7, 1, 1, 1, 1),
    (5, 7, 2, 2, 1, 1),
    (6, 7, 0, 1, -1, 4), (6, 7, 0, 2, -1, 2),
    (6, 7, 1, 1, -1, 2), (6, 7, 1, 2, -1, 2),
    (6, 7, 2, 0, -1, 4), (6, 7, 2, 1, -1, 4),
    (6, 7, 2, 2, -1, 4),
)


TILTED_ROWS = (
    (0, 1, 0, 1, 1, 1), (0, 2, 0, 2, 1, 1),
    (0, 4, 0, 1, 1, 1), (0, 5, 0, 2, 1, 1),
    (0, 6, 0, 0, 1, 1), (1, 2, 1, 2, 1, 1),
    (1, 3, 0, 0, 1, 1), (1, 4, 1, 1, 1, 1),
    (1, 5, 2, 2, 1, 1), (1, 6, 0, 2, -1, 4),
    (1, 6, 1, 0, 1, 1), (1, 6, 1, 1, 1, 1),
    (1, 6, 2, 0, 1, 4), (1, 6, 2, 1, 1, 2),
    (1, 6, 2, 2, 1, 8), (2, 3, 2, 0, 1, 1),
    (2, 6, 2, 2, 1, 1), (2, 7, 2, 1, 1, 1),
    (3, 4, 0, 1, 1, 1), (3, 5, 0, 2, 1, 1),
    (3, 7, 0, 0, 1, 1), (4, 7, 1, 1, 1, 1),
    (5, 7, 2, 2, 1, 1),
    (6, 7, 0, 1, -3, 2), (6, 7, 0, 2, -1, 1),
    (6, 7, 1, 1, -1, 1), (6, 7, 1, 2, -1, 2),
    (6, 7, 2, 0, -1, 4), (6, 7, 2, 1, -1, 4),
    (6, 7, 2, 2, -1, 4),
)


PACKETS = {
    "direct_free": {
        "cells": cells_from_rows(DIRECT_FREE_ROWS),
        "r": 3, "s": 2, "x": 0,
        "p_color": 2, "q_color": 0, "r_color": 0, "s_color": 2,
        "pq": (
            (F(0), F(-1, 4), F(-1, 2)),
            (F(0), F(-1, 2), F(-1, 2)),
            (F(-1, 4), F(-1, 4), F(-1, 4)),
        ),
        "pr": ((ZERO, ZERO, ZERO),) * 3,
        "full_failures": (
            ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
            ((0, 1, 2, 1, 1, 2), 2, 2, ONE, ZERO),
            ((0, 1, 2, 2, 1, 2), 2, 1, ONE, ZERO),
            ((0, 1, 2, 2, 1, 2), 2, 2, ONE, ZERO),
            ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
            ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
        ),
    },
    "tilted": {
        "cells": cells_from_rows(TILTED_ROWS),
        "r": 1, "s": 2, "x": 0,
        "p_color": 0, "q_color": 1, "r_color": 1, "s_color": 2,
        "pq": (
            (F(0), F(-3, 2), F(-1)),
            (F(0), F(-1), F(-1, 2)),
            (F(-1, 4), F(-1, 4), F(-1, 4)),
        ),
        "pr": (
            (F(0), F(1), F(1, 4)),
            (F(0), F(1), F(1, 2)),
            (F(-1, 4), F(0), F(1, 8)),
        ),
        "full_failures": (
            ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
            ((0, 0, 2, 0, 1, 2), 2, 2, F(1, 2), ZERO),
            ((0, 2, 2, 0, 1, 2), 0, 2, F(-3, 2), ZERO),
            ((0, 2, 2, 0, 1, 2), 2, 0, F(1, 2), ZERO),
            ((0, 2, 2, 0, 1, 2), 2, 2, F(-1, 4), ZERO),
            ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
            ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
        ),
    },
}


def get(cells, a, b, ca, cb):
    return cells.get(key(a, b, ca, cb), ZERO)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for vertices in (
        ALL_SITES,
        INTERNAL,
        (Q, 0, 1, 2, 4, 5),
        (Q, 0, 2, 3, 4, 5),
    )
}


def matching_value(cells, assignment, vertices):
    total = ZERO
    for matching in MATCHINGS.get(tuple(vertices), perfect_matchings(vertices)):
        value = ONE
        for a, b in matching:
            value *= get(cells, a, b, assignment[a], assignment[b])
            if not value:
                break
        total += value
    return total


def response_value(cells, left, right, left_color, right_color,
                   residual, residual_assignment):
    total = ZERO
    for a in residual:
        left_value = get(
            cells, left, a, left_color, residual_assignment[a]
        )
        if not left_value:
            continue
        for b in residual:
            if a == b:
                continue
            right_value = get(
                cells, right, b, right_color, residual_assignment[b]
            )
            if not right_value:
                continue
            complement = tuple(site for site in residual if site not in (a, b))
            total += left_value * right_value * matching_value(
                cells, residual_assignment, complement
            )
    return total


def matrix_rank(matrix):
    work = [list(row) for row in matrix]
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        rank += 1
    return rank


def block(cells, left, right):
    return tuple(
        tuple(get(cells, left, right, i, j) for j in COLORS)
        for i in COLORS
    )


def star_rank(cells, endpoint, residual):
    rows = []
    for endpoint_color in COLORS:
        rows.append([
            get(cells, endpoint, site, endpoint_color, site_color)
            for site in residual
            for site_color in COLORS
        ])
    return matrix_rank(rows)


def selected_assignment(packet, chart):
    if chart == "pq":
        residual = INTERNAL
        assignment = {site: LABELS[site] for site in residual}
        return (P, Q), residual, assignment
    r = packet["r"]
    residual = (Q,) + tuple(site for site in INTERNAL if site != r)
    assignment = {Q: packet["q_color"]}
    assignment.update({site: LABELS[site] for site in INTERNAL if site != r})
    return (P, r), residual, assignment


def audit_caps_and_scope(name, packet):
    cells = packet["cells"]
    ledger = []
    for chart, expected_block in (("pq", packet["pq"]), ("pr", packet["pr"])):
        endpoints, residual, assignment = selected_assignment(packet, chart)
        left, right = endpoints
        internal = matching_value(cells, assignment, residual)
        actual_block = block(cells, left, right)
        require(actual_block == expected_block, f"{name} {chart} block changed")
        for i in COLORS:
            for j in COLORS:
                response = response_value(
                    cells, left, right, i, j, residual, assignment
                )
                full = dict(assignment)
                full[left], full[right] = i, j
                global_value = matching_value(cells, full, ALL_SITES)
                require(
                    global_value == actual_block[i][j] * internal + response,
                    f"{name} {chart} cap decomposition {(i, j)} failed",
                )
                require(
                    global_value == ZERO,
                    f"{name} selected {chart} cap {(i, j)} survived",
                )
                ledger.extend((internal, response, global_value))

    endpoints, residual, pq_assignment = selected_assignment(packet, "pq")
    pq_word = tuple(pq_assignment[site] for site in residual)
    _, pr_residual, pr_assignment = selected_assignment(packet, "pr")
    pr_word = tuple(pr_assignment[site] for site in pr_residual)
    require(
        sorted(pq_word) == sorted(pr_word) == [0, 0, 1, 1, 2, 2],
        f"{name} selected words are not separating",
    )

    boundary = {
        P: packet["p_color"], Q: packet["q_color"],
        packet["r"]: packet["r_color"],
        packet["s"]: packet["s_color"],
    }
    complement = tuple(site for site in ALL_SITES if site not in boundary)
    crossed = []
    for word in product(COLORS, repeat=4):
        assignment = dict(boundary)
        assignment.update(dict(zip(complement, word)))
        crossed.append(matching_value(cells, assignment, ALL_SITES))
    require(crossed == [ZERO] * 81, f"{name} crossed slice is not zero")

    require(star_rank(cells, P, INTERNAL) == 3, f"{name} pq left star")
    require(star_rank(cells, Q, INTERNAL) == 3, f"{name} pq right star")
    pr_residual_sites = (Q,) + tuple(
        site for site in INTERNAL if site != packet["r"]
    )
    require(star_rank(cells, P, pr_residual_sites) == 3,
            f"{name} pr left star")
    require(star_rank(cells, packet["r"], pr_residual_sites) == 3,
            f"{name} pr right star")

    failures = []
    for word in product(COLORS, repeat=6):
        residual_assignment = dict(zip(INTERNAL, word))
        for i in COLORS:
            for j in COLORS:
                assignment = dict(residual_assignment)
                assignment[P], assignment[Q] = i, j
                value = matching_value(cells, assignment, ALL_SITES)
                target = ONE if i == j and all(c == i for c in word) else ZERO
                if value != target:
                    failures.append((word, i, j, value, target))
    require(
        tuple(failures) == packet["full_failures"],
        f"{name} full EqSystem failure locus changed",
    )
    require(failures, f"{name} unexpectedly became a full tensor solution")
    ledger.extend(crossed)
    ledger.extend(failures)
    return ledger, failures


def poly_add(*terms):
    result = {}
    for term in terms:
        for support, value in term.items():
            result[support] = result.get(support, ZERO) + value
            if not result[support]:
                del result[support]
    return result


def poly_scale(scale, term):
    return {
        support: scale * value
        for support, value in term.items()
        if scale * value
    }


def poly_mul(left, right):
    result = {}
    for a, av in left.items():
        for b, bv in right.items():
            if a & b:
                continue
            support = a | b
            result[support] = result.get(support, ZERO) + av * bv
            if not result[support]:
                del result[support]
    return result


def linear(cells, endpoint, endpoint_color, common):
    return {
        1 << site: value
        for site in common
        if (value := get(
            cells, endpoint, site, endpoint_color, LABELS[site]
        ))
    }


def quadratic(cells, common):
    result = {}
    for a, b in combinations(common, 2):
        value = get(cells, a, b, LABELS[a], LABELS[b])
        if value:
            result[(1 << a) | (1 << b)] = value
    return result


def top(term, common):
    return term.get(sum(1 << site for site in common), ZERO)


def audit_overlap(name, packet):
    cells = packet["cells"]
    r, s = packet["r"], packet["s"]
    i = packet["p_color"]
    j = packet["q_color"]
    k = packet["r_color"]
    ell = packet["s_color"]
    common = tuple(site for site in INTERNAL if site not in (r, s))

    a = get(cells, P, Q, i, j)
    b = get(cells, P, r, i, k)
    c = get(cells, Q, r, j, k)
    e = get(cells, P, s, i, ell)
    f = get(cells, Q, s, j, ell)
    u = get(cells, r, s, k, ell)
    kappa = a * u - b * f
    require(kappa, f"{name} curvature vanished")

    z = quadratic(cells, common)
    x = linear(cells, P, i, common)
    y = linear(cells, Q, j, common)
    t = linear(cells, r, k, common)
    v = linear(cells, s, ell, common)
    pq = poly_add(poly_scale(a, z), poly_mul(x, y))
    pr = poly_add(poly_scale(b, z), poly_mul(x, t))
    transition = poly_add(poly_scale(a, t), poly_scale(-b, y))

    require(
        poly_add(poly_mul(pq, t), poly_scale(-ONE, poly_mul(pr, y)))
        == poly_mul(transition, z),
        f"{name} connection sign failed",
    )

    l_pq_r = poly_add(
        poly_scale(3 * b, y), poly_scale(3 * c, x), poly_scale(a, t)
    )
    l_pr_q = poly_add(
        poly_scale(3 * a, t), poly_scale(3 * c, x), poly_scale(b, y)
    )
    require(
        poly_add(l_pq_r, poly_scale(-ONE, l_pr_q))
        == poly_scale(F(-2), transition),
        f"{name} normal sign failed",
    )

    h_pq_s = poly_add(
        poly_scale(a, v), poly_scale(e, y), poly_scale(f, x)
    )
    n_pr_s = poly_add(
        poly_scale(b, v), poly_scale(e, t), poly_scale(u, x)
    )
    curvature_left = poly_add(
        poly_scale(u, pq),
        poly_mul(t, h_pq_s),
        poly_scale(-f, pr),
        poly_scale(-ONE, poly_mul(y, n_pr_s)),
    )
    curvature_right = poly_add(
        poly_mul(transition, v), poly_scale(kappa, z)
    )
    require(curvature_left == curvature_right, f"{name} curvature sign")

    m_pq = 3 * (b * f + e * c) + a * u
    m_pr = 3 * (a * u + e * c) + b * f
    require(m_pq - m_pr == -2 * kappa, f"{name} direct-double sign")

    z_square = poly_mul(z, z)
    high_curvature = poly_scale(kappa, z_square)
    high_direct = poly_scale(-kappa, z_square)
    low_connection = poly_mul(poly_mul(transition, v), z)
    low_normal = poly_scale(-ONE, low_connection)
    require(
        poly_add(high_curvature, high_direct) == {}
        and poly_add(low_connection, low_normal) == {},
        f"{name} Euler cancellation failed",
    )

    assignment = {site: LABELS[site] for site in common}
    chi = matching_value(cells, assignment, common)
    values = tuple(
        top(term, common)
        for term in (high_curvature, high_direct, low_connection, low_normal)
    )
    require(
        values[0] == 2 * chi * kappa
        and values[1] == -2 * chi * kappa
        and values[2] == -values[3],
        f"{name} Euler top normalization failed",
    )

    if name == "direct_free":
        require(
            (a, b, c, e, f, u, kappa, chi, values)
            == (
                F(-1, 4), ZERO, ONE, ONE, ZERO, ONE,
                F(-1, 4), ONE,
                (F(-1, 2), F(1, 2), F(-3, 4), F(3, 4)),
            ),
            "direct-free overlap ledger changed",
        )
    else:
        require(
            (a, b, f, u, kappa, chi, values)
            == (
                F(-3, 2), ONE, ONE, ONE, F(-5, 2), F(2),
                (F(-10), F(10), F(-5), F(5)),
            ),
            "tilted overlap ledger changed",
        )
        require(
            b != ZERO and matrix_rank(packet["pr"]) == 3,
            "tilted second chart is not canonically active and full rank",
        )

    return {
        "A": a, "B": b, "C": c, "E": e, "F": f, "U": u,
        "kappa": kappa, "chi": chi, "tops": values,
    }


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                ZERO,
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matadd(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matscale(scale, matrix):
    return [[scale * value for value in row] for row in matrix]


def zero_matrix():
    return [[ZERO] * 3 for _ in range(3)]


def phi_from_deltas(deltas, direct):
    phi = zero_matrix()
    for i in COLORS:
        for j in COLORS:
            phi[i][j] = (
                -sum(
                    (deltas[c][i][c] * direct[c][j]
                     for c in COLORS if c != i),
                    ZERO,
                )
                -sum(
                    (direct[i][c] * deltas[c][c][j]
                     for c in COLORS if c != j),
                    ZERO,
                )
                -direct[i][j] * deltas[j][j][j]
            )
    return phi


def cycle(matrix, phi):
    return (
        matrix[1][2] * matrix[2][0] * phi[0][1]
        + matrix[2][0] * matrix[0][1] * phi[1][2]
        + matrix[0][1] * matrix[1][2] * phi[2][0]
    )


def audit_anchors_and_rank(packet, overlap):
    cells = packet["cells"]
    cross = []
    for i in COLORS:
        row = []
        for j in COLORS:
            assignment = {site: LABELS[site] for site in INTERNAL}
            complement = tuple(
                site for site in INTERNAL if site not in (i, 3 + j)
            )
            row.append(matching_value(cells, assignment, complement))
        cross.append(row)
    require(
        cross == [[ZERO, ONE, F(2)], [ZERO, F(2), F(2)], [ONE, ONE, ONE]],
        "cross cofactor matrix changed",
    )
    direct = matscale(F(-1, 4), cross)
    require(tuple(map(tuple, direct)) == packet["pq"], "anchor direct block")

    x = [[ONE, ONE, F(-2)] for _ in COLORS]
    y = [
        [F(5, 2), F(10), F(25, 2)],
        [ZERO, ZERO, ZERO],
        [F(-1, 2), F(-2), F(-5, 2)],
    ]
    require(
        matadd(matmul(transpose(x), cross), matmul(cross, y))
        == zero_matrix(),
        "cofactor connection failed",
    )
    leakage = matadd(matmul(transpose(x), direct), matmul(direct, y))
    require(leakage == zero_matrix(), "direct leakage failed")

    deltas = []
    for color in COLORS:
        target = zero_matrix()
        target[color][color] = ONE
        delta = matscale(
            -ONE,
            matadd(matmul(transpose(x), target), matmul(target, y)),
        )
        require(delta != zero_matrix(), f"anchor defect {color} vanished")
        deltas.append(delta)

    expected_deltas = [
        [[F(-7, 2), F(-10), F(-25, 2)], [F(-1), ZERO, ZERO],
         [F(2), ZERO, ZERO]],
        [[ZERO, F(-1), ZERO], [ZERO, F(-1), ZERO],
         [ZERO, F(2), ZERO]],
        [[ZERO, ZERO, F(-1)], [ZERO, ZERO, F(-1)],
         [F(1, 2), F(2), F(9, 2)]],
    ]
    require(deltas == expected_deltas, "explicit anchor defects changed")

    contributions = []
    for retained in COLORS:
        partial = [
            deltas[c] if c == retained else zero_matrix()
            for c in COLORS
        ]
        contributions.append(cycle(direct, phi_from_deltas(partial, direct)))
    require(
        contributions == [F(-9, 64), F(-3, 32), F(15, 64)]
        and all(contributions)
        and sum(contributions, ZERO) == ZERO,
        "anchor contributions changed",
    )
    theta = F(4) * cycle(direct, phi_from_deltas(deltas, direct))
    xi = cycle(direct, leakage)
    require(theta == xi == ZERO, "anchor total is not zero")

    chi = overlap["chi"]
    relations = [
        [ONE, -ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ZERO, -2 * chi, ONE, ZERO, ZERO, ZERO],
        [ZERO, ZERO, 2 * chi, ZERO, ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO, ZERO, ZERO, ONE, ONE],
    ]
    landing = [ONE, ZERO, -chi, ZERO, ZERO, ZERO, ZERO]
    require(
        matrix_rank(relations) == 5
        and matrix_rank(relations + [landing]) == 6,
        "rank jump changed",
    )
    witness = [theta, xi, overlap["kappa"], *overlap["tops"]]
    require(
        all(sum((a * b for a, b in zip(row, witness)), ZERO) == ZERO
            for row in relations),
        "rank witness misses a retained row",
    )
    residual = sum(
        (a * b for a, b in zip(landing, witness)), ZERO
    )
    require(residual == F(1, 4), "landing residual changed")
    return theta, xi, tuple(contributions), residual


def normalize(value):
    if isinstance(value, F):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return tuple((key, normalize(item)) for key, item in sorted(value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(normalize(item) for item in value)
    return value


EXPECTED_DIGEST = "360e70817a8fac2f64adae0db09b89f9a00163a7e63646df8e22c97a06ebf056"


def main():
    ledger = []
    failures = {}
    overlaps = {}
    for name, packet in PACKETS.items():
        cap_ledger, packet_failures = audit_caps_and_scope(name, packet)
        overlap = audit_overlap(name, packet)
        ledger.extend((name, cap_ledger, overlap))
        failures[name] = packet_failures
        overlaps[name] = overlap
    anchor = audit_anchors_and_rank(PACKETS["direct_free"], overlaps["direct_free"])
    ledger.append(anchor)
    digest = sha256(repr(normalize(ledger)).encode()).hexdigest()
    if EXPECTED_DIGEST:
        require(digest == EXPECTED_DIGEST, "independent ledger digest changed")

    print("independent selected-cap landing counterguard audit: PASS")
    print(f"  direct-free full EqSystem failures : {len(failures['direct_free'])}")
    print(f"  tilted full EqSystem failures      : {len(failures['tilted'])}")
    print(f"  direct-free landing residual       : {anchor[-1]}")
    print(f"  tilted canonical activity B        : {overlaps['tilted']['B']}")
    print(f"  aggregate SHA-256                  : {digest}")
    print("  tensor-valued EqSystem             : EXPLICITLY FAILS")


if __name__ == "__main__":
    main()
