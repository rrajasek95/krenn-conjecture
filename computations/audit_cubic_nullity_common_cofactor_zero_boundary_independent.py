#!/usr/bin/env python3
"""Clean-room audit of the cubic common-cofactor-zero boundary.

This script does not import the primary verifier.  It expands perfect
matchings as products of endpoint-ordered edge entries, checks both gluing
identities, and reconstructs the dense cancellation family over Q.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from random import Random

import sympy as sp


COLOURS = range(3)
ZERO = tuple(tuple(Fraction(0) for _ in COLOURS) for _ in COLOURS)
E00 = ((Fraction(1), Fraction(0), Fraction(0)),
       (Fraction(0), Fraction(0), Fraction(0)),
       (Fraction(0), Fraction(0), Fraction(0)))
E01 = ((Fraction(0), Fraction(1), Fraction(0)),
       (Fraction(0), Fraction(0), Fraction(0)),
       (Fraction(0), Fraction(0), Fraction(0)))
ASYMMETRIC = ((Fraction(2), Fraction(-1), Fraction(3)),
              (Fraction(5), Fraction(0), Fraction(7)),
              (Fraction(-2), Fraction(11), Fraction(1)))


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLOURS) for i in COLOURS)


def scaled(matrix, scalar):
    return tuple(tuple(scalar * entry for entry in row) for row in matrix)


def store(blocks, u, v, matrix):
    """Store a matrix whose rows are at u and columns are at v."""
    assert u != v
    if u < v:
        blocks[u, v] = matrix
    else:
        blocks[v, u] = transpose(matrix)


def oriented(blocks, u, v):
    matrix = blocks.get((min(u, v), max(u, v)), ZERO)
    return matrix if u < v else transpose(matrix)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def nonzero_entries(matrix):
    return tuple(
        (i, j, matrix[i][j])
        for i in COLOURS
        for j in COLOURS
        if matrix[i][j]
    )


def matching_tensor(vertices, blocks):
    """Expand matchings first and edge entries second; words use physical order."""
    vertices = tuple(sorted(vertices))
    if not vertices:
        return {(): Fraction(1)}
    output = defaultdict(Fraction)
    for matching in perfect_matchings(vertices):
        choices = [nonzero_entries(oriented(blocks, u, v)) for u, v in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            assignment = {}
            coefficient = Fraction(1)
            for (u, v), (cu, cv, value) in zip(matching, selected, strict=True):
                assignment[u] = cu
                assignment[v] = cv
                coefficient *= value
            output[tuple(assignment[v] for v in vertices)] += coefficient
    return {word: value for word, value in output.items() if value}


def add_to(output, word, value):
    if value:
        output[word] += value
        if not output[word]:
            del output[word]


def insert_word(sites, fixed, rest_sites, rest_word):
    assignment = dict(zip(rest_sites, rest_word, strict=True))
    assignment.update(fixed)
    return tuple(assignment[v] for v in sites)


def cofactor_columns(sites, blocks):
    sites = tuple(sorted(sites))
    columns = []
    for center in sites:
        rest = tuple(v for v in sites if v != center)
        cofactor = matching_tensor(rest, blocks)
        for colour in COLOURS:
            column = defaultdict(Fraction)
            for word, value in cofactor.items():
                add_to(column, insert_word(sites, {center: colour}, rest, word), value)
            columns.append((center, colour, dict(column)))
    return columns


def apply_cofactor_map(sites, vector, blocks):
    output = defaultdict(Fraction)
    for center, colour, column in cofactor_columns(sites, blocks):
        multiplier = vector[center][colour]
        for word, value in column.items():
            add_to(output, word, multiplier * value)
    return dict(output)


def slice_tensor(tensor, sites, fixed):
    sites = tuple(sorted(sites))
    remaining = tuple(v for v in sites if v not in fixed)
    indices = {v: sites.index(v) for v in fixed}
    output = defaultdict(Fraction)
    for word, value in tensor.items():
        if all(word[indices[v]] == colour for v, colour in fixed.items()):
            add_to(output, tuple(word[sites.index(v)] for v in remaining), value)
    return remaining, dict(output)


def theta(local, first_rows, second_rows, blocks):
    local = tuple(sorted(local))
    output = defaultdict(Fraction)
    for v in local:
        for w in local:
            if v == w:
                continue
            rest = tuple(x for x in local if x not in (v, w))
            lower = matching_tensor(rest, blocks)
            for cv, cw in product(COLOURS, repeat=2):
                scalar = first_rows[v][cv] * second_rows[w][cw]
                if not scalar:
                    continue
                for word, value in lower.items():
                    full = insert_word(local, {v: cv, w: cw}, rest, word)
                    add_to(output, full, scalar * value)
    return dict(output)


def tensor_sum(*terms):
    output = defaultdict(Fraction)
    for tensor in terms:
        for word, value in tensor.items():
            add_to(output, word, value)
    return dict(output)


def tensor_scale(tensor, scalar):
    return {word: scalar * value for word, value in tensor.items() if scalar * value}


def random_matrix(rng):
    return tuple(
        tuple(Fraction(rng.randrange(-4, 5)) for _ in COLOURS)
        for _ in COLOURS
    )


def audit_gluing_and_endpoint_order():
    """Check (3), (7), (9), and (17) with interleaved physical labels."""
    rng = Random(914_2026)
    local = (1, 4, 6, 9)
    q, q_prime = 8, 2
    blocks = {}
    for u, v in combinations(local, 2):
        store(blocks, u, v, random_matrix(rng))
    for terminal in (q, q_prime):
        for v in local:
            store(blocks, terminal, v, random_matrix(rng))
    store(blocks, q, q_prime, ASYMMETRIC)

    common = matching_tensor(local, blocks)
    assert common
    k_sites = tuple(sorted(local + (q_prime,)))
    vector = {
        v: tuple(Fraction(rng.randrange(-3, 4)) for _ in COLOURS)
        for v in k_sites
    }
    image = apply_cofactor_map(k_sites, vector, blocks)

    # Equation (7), coefficient by coefficient.
    equation7_checks = 0
    for j in COLOURS:
        remaining, actual = slice_tensor(image, k_sites, {q_prime: j})
        assert remaining == tuple(sorted(local))
        first = tensor_scale(common, vector[q_prime][j])
        z_rows = {v: vector[v] for v in local}
        star_rows = {v: oriented(blocks, q_prime, v)[j] for v in local}
        expected = tensor_sum(first, theta(local, z_rows, star_rows, blocks))
        assert actual == expected
        equation7_checks += len(set(actual) | set(expected))

    # The exact local-port formula z -> z tensor P.  Since P is nonzero,
    # the three local basis images are independent, proving the claimed
    # zero intersection and injectivity of kernel restriction.
    local_images = []
    for j in COLOURS:
        basis_vector = {v: (Fraction(0),) * 3 for v in k_sites}
        basis_vector[q_prime] = tuple(Fraction(i == j) for i in COLOURS)
        basis_image = apply_cofactor_map(k_sites, basis_vector, blocks)
        expected = {
            insert_word(k_sites, {q_prime: j}, local, word): value
            for word, value in common.items()
        }
        assert basis_image == expected
        local_images.append(basis_image)
    assert sparse_column_rank(local_images) == 3

    # Equation (9) in both endpoint orientations.  This is checked as a
    # universal matching identity, before imposing a pure target value.
    full_sites = tuple(sorted(local + (q, q_prime)))
    whole = matching_tensor(full_sites, blocks)
    equation9_checks = 0
    direct_q = oriented(blocks, q, q_prime)
    direct_q_prime = oriented(blocks, q_prime, q)
    assert direct_q_prime == transpose(direct_q)
    for d, j in product(COLOURS, repeat=2):
        remaining, actual = slice_tensor(whole, full_sites, {q: d, q_prime: j})
        assert remaining == tuple(sorted(local))
        q_rows = {v: oriented(blocks, q, v)[d] for v in local}
        qp_rows = {v: oriented(blocks, q_prime, v)[j] for v in local}
        forward = tensor_sum(
            tensor_scale(common, direct_q[d][j]),
            theta(local, q_rows, qp_rows, blocks),
        )
        reverse = tensor_sum(
            tensor_scale(common, direct_q_prime[j][d]),
            theta(local, qp_rows, q_rows, blocks),
        )
        assert actual == forward == reverse
        equation9_checks += len(set(actual) | set(forward) | set(reverse))

    # Equation (17): changing only the direct block changes H by Delta A P.
    old_direct = direct_q
    new_direct = random_matrix(rng)
    changed = dict(blocks)
    store(changed, q, q_prime, new_direct)
    changed_whole = matching_tensor(full_sites, changed)
    delta = defaultdict(Fraction)
    for word in set(whole) | set(changed_whole):
        add_to(delta, word, changed_whole.get(word, 0) - whole.get(word, 0))
    expected_delta = defaultdict(Fraction)
    sites = tuple(sorted(full_sites))
    for rest_word, p_value in common.items():
        rest_assignment = dict(zip(sorted(local), rest_word, strict=True))
        for d, j in product(COLOURS, repeat=2):
            value = (new_direct[d][j] - old_direct[d][j]) * p_value
            assignment = dict(rest_assignment)
            assignment[q], assignment[q_prime] = d, j
            add_to(expected_delta, tuple(assignment[v] for v in sites), value)
    assert dict(delta) == dict(expected_delta)

    return equation7_checks, equation9_checks


def odd_double_factorial(n):
    assert n >= -1 and n % 2
    answer = 1
    for value in range(n, 0, -2):
        answer *= value
    return answer


def scalar_hafnian(vertices, weight):
    total = 0
    for matching in perfect_matchings(tuple(vertices)):
        term = 1
        for u, v in matching:
            term *= weight[min(u, v), max(u, v)]
        total += term
    return total


def expected_h(r, u, v):
    if {u, v} & {1, 2}:
        return odd_double_factorial(r - 3)
    return -2 * odd_double_factorial(r - 5)


def dense_blocks(r):
    local = tuple(range(1, r + 1))
    q, q_prime = 0, r + 1
    blocks = {}
    weights = {}
    for u, v in combinations(local, 2):
        value = -(r - 2) if (u, v) == (1, 2) else 1
        weights[u, v] = value
        store(blocks, u, v, scaled(E00, value))
    for terminal in (q, q_prime):
        for v in local:
            store(blocks, terminal, v, E01)
    store(blocks, q, q_prime, ASYMMETRIC)
    return local, q, q_prime, blocks, weights


def sparse_column_rank(columns):
    words = sorted({word for column in columns for word in column})
    matrix = [[Fraction(column.get(word, 0)) for column in columns] for word in words]
    if not matrix:
        return 0
    rows, cols = len(matrix), len(columns)
    pivot = 0
    for col in range(cols):
        hit = next((row for row in range(pivot, rows) if matrix[row][col]), None)
        if hit is None:
            continue
        matrix[pivot], matrix[hit] = matrix[hit], matrix[pivot]
        lead = matrix[pivot][col]
        matrix[pivot] = [entry / lead for entry in matrix[pivot]]
        for row in range(rows):
            if row == pivot or not matrix[row][col]:
                continue
            multiple = matrix[row][col]
            matrix[row] = [
                a - multiple * b
                for a, b in zip(matrix[row], matrix[pivot], strict=True)
            ]
        pivot += 1
        if pivot == rows:
            break
    return pivot


def rank_mod(rows, prime):
    matrix = [[entry % prime for entry in row] for row in rows]
    rank = 0
    width = len(matrix[0]) if matrix else 0
    for col in range(width):
        hit = next((row for row in range(rank, len(matrix)) if matrix[row][col]), None)
        if hit is None:
            continue
        matrix[rank], matrix[hit] = matrix[hit], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(inv * value) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][col]:
                scale = matrix[row][col]
                matrix[row] = [
                    (a - scale * b) % prime
                    for a, b in zip(matrix[row], matrix[rank], strict=True)
                ]
        rank += 1
    return rank


def expected_marker_column(sites, local, terminal, center, colour, r):
    if center == terminal:
        return {}
    output = defaultdict(Fraction)
    for marker in local:
        if marker == center:
            continue
        assignment = {v: 0 for v in sites}
        assignment[terminal] = 0
        assignment[center] = colour
        assignment[marker] = 1
        add_to(
            output,
            tuple(assignment[v] for v in sites),
            Fraction(expected_h(r, center, marker)),
        )
    return dict(output)


def audit_uniform_algebra():
    # An identity in symbolic t=r-2 and d=(r-5)!! audits the two-dimensional
    # constant-sector determinant, rather than extrapolating finite ranks.
    t, d = sp.symbols("t d", positive=True, integer=True)
    a = (t - 1) * d
    b = -2 * d
    constant_sector = sp.factor(a * b * (t - 1) - 2 * t * a**2)
    assert constant_sector == -2 * (t - 1) ** 2 * (t + 1) * d**2
    determinant = sp.factor((-a) * (2 * d) ** (t - 1) * constant_sector)
    assert sp.simplify(
        determinant - 2**t * (t - 1) ** 3 * (t + 1) * d ** (t + 2)
    ) == 0

    ledger = {}
    for r in range(4, 32, 2):
        # Partition by use of special edge 12.
        containing = -(r - 2) * odd_double_factorial(r - 3)
        avoiding = odd_double_factorial(r - 1) - odd_double_factorial(r - 3)
        assert containing + avoiding == 0
        closed_det = (
            2 ** (r - 2)
            * (r - 3) ** 3
            * (r - 1)
            * odd_double_factorial(r - 5) ** r
        )
        assert closed_det
        ledger[r + 4] = (closed_det, 3 * r)

        if r <= 12:
            local = tuple(range(1, r + 1))
            weight = {
                (u, v): (-(r - 2) if (u, v) == (1, 2) else 1)
                for u, v in combinations(local, 2)
            }
            assert scalar_hafnian(local, weight) == 0
            for u, v in combinations(local, 2):
                rest = tuple(x for x in local if x not in (u, v))
                assert scalar_hafnian(rest, weight) == expected_h(r, u, v)

            m = sp.Matrix(
                r,
                r,
                lambda i, j: 0 if i == j else expected_h(r, i + 1, j + 1),
            )
            assert int(m.det()) == closed_det

            # The colour-one sector is the weighted signless incidence
            # matrix.  It has rank r over Q, but only r-1 in characteristic
            # two; this records exactly where the complex-field hypothesis
            # is being used.
            incidence = []
            for u, v in combinations(range(r), 2):
                row = [0] * r
                row[u] = row[v] = expected_h(r, u + 1, v + 1)
                incidence.append(row)
            assert sp.Matrix(incidence).rank() == r
            assert rank_mod(incidence, 2) == r - 1

    assert ledger[8] == (12, 12)
    return ledger


def audit_dense_physical_family(r):
    local, q, q_prime, blocks, weights = dense_blocks(r)
    common = matching_tensor(local, blocks)
    assert common == {}

    double_count = 0
    for u, v in combinations(local, 2):
        rest = tuple(x for x in local if x not in (u, v))
        cofactor = matching_tensor(rest, blocks)
        assert cofactor == {(0,) * len(rest): Fraction(expected_h(r, u, v))}
        double_count += 1

    kernel_ports = {}
    for omitted, terminal in ((q, q_prime), (q_prime, q)):
        sites = tuple(sorted(local + (terminal,)))
        columns = cofactor_columns(sites, blocks)
        nonlocal_columns = []
        all_columns = []
        for center, colour, column in columns:
            expected = expected_marker_column(sites, local, terminal, center, colour, r)
            assert column == expected
            all_columns.append(column)
            if center == terminal:
                assert not column
            else:
                nonlocal_columns.append(column)
        assert sparse_column_rank(nonlocal_columns) == 3 * r
        assert sparse_column_rank(all_columns) == 3 * r
        assert len(all_columns) == 3 * (r + 1)
        # Hence the kernel has dimension three and is precisely V_terminal.
        kernel_ports[omitted] = terminal
    assert kernel_ports == {q: q_prime, q_prime: q}

    full_sites = tuple(sorted(local + (q, q_prime)))
    whole = matching_tensor(full_sites, blocks)
    assert whole
    expected = defaultdict(Fraction)
    for u, v in combinations(local, 2):
        assignment = {site: 0 for site in full_sites}
        assignment[u] = assignment[v] = 1
        add_to(
            expected,
            tuple(assignment[site] for site in full_sites),
            Fraction(2 * expected_h(r, u, v)),
        )
    assert whole == dict(expected)

    # The arbitrary nonsymmetric direct block is silent because P=0.
    no_direct = dict(blocks)
    store(no_direct, q, q_prime, ZERO)
    assert matching_tensor(full_sites, no_direct) == whole
    assert oriented(blocks, q_prime, q) == transpose(ASYMMETRIC)

    # It fails every nonzero pure-cofactor equation, including c=0: the
    # tensor is nonzero and every supported word has exactly two local 1s.
    for colour in COLOURS:
        pure_word = (colour,) * len(full_sites)
        assert pure_word not in whole
        assert whole != {pure_word: Fraction(1)}

    # Every physical pair carries a nonzero aggregate block.
    assert len(blocks) == len(full_sites) * (len(full_sites) - 1) // 2
    assert all(matrix != ZERO for matrix in blocks.values())

    return {
        "N": r + 4,
        "double_cofactors": double_count,
        "rank_each": 3 * r,
        "kernel_ports": (kernel_ports[q], kernel_ports[q_prime]),
        "mixed_terms": len(whole),
    }


def main():
    eq7, eq9 = audit_gluing_and_endpoint_order()
    ledger = audit_uniform_algebra()
    records = [audit_dense_physical_family(r) for r in (4, 6, 8)]
    print("equation (7) independent coefficients:", eq7)
    print("equation (9) forward/reverse coefficients:", eq9)
    print("uniform determinant/rank ledger N=8..34:", ledger)
    for record in records:
        print("dense zero-boundary family:", record)
    print("PASS: independent cubic common-cofactor-zero boundary audit")


if __name__ == "__main__":
    main()
