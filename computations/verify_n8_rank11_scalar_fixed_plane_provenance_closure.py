#!/usr/bin/env python3
"""Exact regression audit for the fixed-plane scalar-shore closure.

The uniform proof is in
``notes/n8-rank11-scalar-fixed-plane-provenance-closure.md``.  Its inputs
are the maximal rank-(1,1) scalar cap plane

    Q = {K : lambda^T K = 0, K mu = 0}

and one fixed complement site/colour (s,k) satisfying

    p_i,s(k) = c lambda_i,   t_j,s(k) = d mu_j.

The fixed cells make every Q-response coefficient incident with (s,k)
zero.  When the diagonal map Q -> F^3 has rank three, quotienting at that
coordinate makes the opposite response edge proportional to K_kk.  The
only target-free cap is consequently confined to the two-edge star at s.
If it were nonzero, equality of the two star completions would be rank one
across two crossing bipartitions; the elementary reshuffle-rank identity
then gives one common three-site factor.  The other two pure target rows
would force that factor onto two distinct coordinate lines, a contradiction.

This checker exhausts the finite Q-plane incidence over F_5, audits the
fixed-cell response cancellation, the one-dimensional target-free kernel,
the crossing-flattening rank identity over F_2, and the final pure-line
intersection.  It is a regression check, not a finite-field substitute for
the characteristic-zero proof and not a proof of SP-CLEAN-BRIDGE.
"""

from hashlib import sha256
from itertools import product
from pathlib import Path


P = 5
HERE = Path(__file__).resolve().parent
DEPENDENCIES = {
    "verify_rank_one_rank_one_scalar_gate_provenance_quotient.py":
        "e83c447a751b144cb050cd5686fbcc2d46b4e76be2127d2779ad84c0df44210a",
    "verify_n8_rank11_scalar_released_site_three_target_closure.py":
        "5b740f49dc7ee3d3ff1459ce970e2113523a84562214721ebfa21da7ab988d68",
}
EXPECTED_LEDGER_DIGEST = (
    "abe9d063b972c98571207ca0d9e33daed9db0a06cb2ca3f8ceb8689a1fac45e4"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inv(value, prime=P):
    value %= prime
    require(value, "division by zero")
    return pow(value, prime - 2, prime)


def rref(rows, width, prime=P):
    rows = [[entry % prime for entry in row] for row in rows]
    pivot_row = 0
    pivots = []
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inv(rows[pivot_row][column], prime)
        rows[pivot_row] = [(scale * entry) % prime
                           for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [(left - scale * right) % prime
                         for left, right in zip(rows[row], rows[pivot_row])]
        pivots.append(column)
        pivot_row += 1
    return tuple(tuple(row) for row in rows), tuple(pivots)


def rank(rows, width, prime=P):
    return len(rref(rows, width, prime)[1])


def nullspace(rows, width, prime=P):
    reduced, pivots = rref(rows, width, prime)
    free = [column for column in range(width) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [0] * width
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % prime
        answer.append(tuple(vector))
    return tuple(answer)


def projective_vectors(prime=P):
    answer = []
    for vector in product(range(prime), repeat=3):
        if not any(vector):
            continue
        pivot = next(entry for entry in vector if entry)
        normalized = tuple(entry * inv(pivot, prime) % prime
                           for entry in vector)
        if normalized == vector:
            answer.append(vector)
    return tuple(answer)


def hyperplane_basis(vector):
    return nullspace((vector,), 3)


def outer(left, right):
    return tuple(left[i] * right[j] % P
                 for i in range(3) for j in range(3))


def dependency_guard():
    for name, expected in DEPENDENCIES.items():
        actual = sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, ("dependency changed", name, actual))


def endpoint_value(kind, label, site, colour, fixed_colour, vector):
    if site == 0 and colour == fixed_colour:
        return vector[label]
    offset = 1 if kind == "p" else 3
    return (offset + 2 * label + 3 * site + colour) % P


def response_cell(cap, edge, colours, fixed_colour, left, right):
    a, b = edge
    ca, cb = colours
    total = 0
    for i in range(3):
        for j in range(3):
            kij = cap[3 * i + j]
            total += kij * (
                endpoint_value("p", i, a, ca, fixed_colour, left)
                * endpoint_value("s", j, b, cb, fixed_colour, right)
                + endpoint_value("p", i, b, cb, fixed_colour, left)
                * endpoint_value("s", j, a, ca, fixed_colour, right)
            )
    return total % P


def audit_cap_planes():
    vectors = tuple(vector for vector in projective_vectors()
                    if sum(entry != 0 for entry in vector) >= 2)
    records = []
    for left in vectors:
        for right in vectors:
            left_basis = hyperplane_basis(left)
            right_basis = hyperplane_basis(right)
            q_basis = tuple(outer(x, y)
                            for x in left_basis for y in right_basis)
            require(rank(q_basis, 9) == 4, (left, right, "Q rank"))
            delta = tuple(tuple(cap[3 * colour + colour]
                                for cap in q_basis)
                          for colour in range(3))
            delta_rank = rank(delta, 4)
            if delta_rank != 3:
                continue
            kernel_coefficients = nullspace(delta, 4)
            require(len(kernel_coefficients) == 1,
                    (left, right, "target-free dimension"))
            kernel_cap = tuple(sum(kernel_coefficients[0][column]
                                   * q_basis[column][entry]
                                   for column in range(4)) % P
                               for entry in range(9))
            require(any(kernel_cap), (left, right, "zero kernel cap"))
            require(all(kernel_cap[3 * colour + colour] == 0
                        for colour in range(3)),
                    (left, right, "nonzero target on kernel cap"))

            for fixed_colour in range(3):
                # The response on either edge through fixed site 0 has
                # zero fixed_colour row for every cap in Q.
                for cap in q_basis:
                    for other in (1, 2):
                        for other_colour in range(3):
                            value = response_cell(
                                cap, (0, other),
                                (fixed_colour, other_colour), fixed_colour,
                                left, right)
                            require(value == 0,
                                    (left, right, fixed_colour, other,
                                     other_colour, value))

                # Rank three means every diagonal coordinate is live and
                # the target-free cap is unique.
                require(any(cap[3 * fixed_colour + fixed_colour]
                            for cap in q_basis),
                        (left, right, fixed_colour, "dead diagonal"))
                records.append((left, right, fixed_colour,
                                tuple(kernel_cap)))
    require(len(records) == 736 * 3,
            ("wrong rank-three fixed-plane count", len(records)))
    return tuple(records)


def matrix_vectors(size, prime):
    return tuple(vector for vector in product(range(prime), repeat=size * size)
                 if any(vector))


def audit_crossing_flattening():
    # For T_suve=X_su Y_ve, the SV|UE flattening is X tensor Y and
    # therefore has rank rank(X)rank(Y).  Exhaust the 2x2 F_2 instance.
    matrices = matrix_vectors(2, 2)
    records = []
    for x in matrices:
        for y in matrices:
            crossing = []
            for s in range(2):
                for v in range(2):
                    crossing.append(tuple(
                        x[2 * s + u] * y[2 * v + e] % 2
                        for u in range(2) for e in range(2)))
            x_rank = rank(tuple(tuple(x[2 * i + j] for j in range(2))
                                for i in range(2)), 2, 2)
            y_rank = rank(tuple(tuple(y[2 * i + j] for j in range(2))
                                for i in range(2)), 2, 2)
            crossing_rank = rank(crossing, 4, 2)
            require(crossing_rank == x_rank * y_rank,
                    (x, y, x_rank, y_rank, crossing_rank))
            if crossing_rank == 1:
                require(x_rank == y_rank == 1,
                        ("crossing rank-one did not fully factor", x, y))
            records.append((x_rank, y_rank, crossing_rank))
    require(len(records) == 225, len(records))
    return tuple(records)


def audit_pure_line_intersection():
    pure = []
    for colour in range(3):
        word = tuple(1 if all(entry == colour for entry in colouring) else 0
                     for colouring in product(range(3), repeat=3))
        pure.append(word)
    require(rank(pure, 27) == 3, "pure three-site tensors dependent")
    for left in range(3):
        for right in range(left + 1, 3):
            require(rank((pure[left], pure[right]), 27) == 2,
                    ("distinct pure lines met", left, right))
    return tuple(pure)


def main():
    dependency_guard()
    planes = audit_cap_planes()
    crossing = audit_crossing_flattening()
    pure = audit_pure_line_intersection()
    ledger = (planes, crossing, pure)
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("ledger changed", digest))
    print("N=8 scalar fixed-plane provenance closure: PASS")
    print(f"  rank-three fixed planes : {len(planes)} = 736 x 3")
    print("  incident response rows  : all fixed-coordinate cells zero")
    print("  target-free cap kernel  : dimension 1")
    print(f"  crossing rank audits    : {len(crossing)}")
    print("  distinct pure A-lines   : pairwise disjoint")
    print(f"  ledger sha256           : {digest}")


if __name__ == "__main__":
    main()
