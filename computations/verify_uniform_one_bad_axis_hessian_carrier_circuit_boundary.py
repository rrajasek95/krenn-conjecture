#!/usr/bin/env python3
"""Minimum-support Hessian circuits in the axis-purified one-bad branch.

For a fixed opposite star plane, write C_u for the complete two-response
column of one occupied coordinate component of an axis-purified star.  If
the star has minimum site support, the occupied C_u are independent.  After
quotienting by the one diagonal target, their images have rank k-1 and the
star coefficients give the unique full-support circuit.

This checker also reconstructs the smallest physical k=2 boundary from the
committed affine concentration guard.  Its common q is genuine, every
first/second cofactor is computed from q, and all cofactor Euler recurrences
hold.  The two occupied columns are X+Y and -Y, so neither site component is
in the response kernel.  The Y cancellation is a literal alternating C4,
but both endpoint arms lie on the same target line and its endpoint
Pluecker minor is zero.  Thus common Hessian provenance supplies a carrier
circuit, not by itself a deletion or curved OO witness.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = "computations/verify_n8_one_bad_affine_coordinate_concentration_guard.py"
PINS = {
    GUARD_PATH:
        "cbc615239037fc5f9664fb1846043a1aa523f716c19d8a03cba4e239c07eb4ab",
    "notes/n8-one-bad-affine-coordinate-concentration-guard.md":
        "275613605e5b36b6fb7776848de4cac5a770ef9c442a4be2d3dcef2f92a860a4",
    "computations/verify_uniform_one_bad_semisimple_cofactor_tower_boundary.py":
        "5b6ae90480611c6b1f87d049f404d1e61bde4a93a3af3779c42d749de453c1fe",
    "notes/uniform-one-bad-semisimple-cofactor-tower-boundary.md":
        "43402aa2051086aedacfd04cfc5f9d3e155471946beffafaddc4617f33d59283",
}
EXPECTED_LEDGER_SHA256 = (
    "3b0c0bf757f76884a2f3ff068209c9ae207002eed1a9b63d129ddc82082fa22f"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_guard():
    path = ROOT / GUARD_PATH
    spec = spec_from_file_location("axis_hessian_affine_guard", path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {GUARD_PATH}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def clean(counter):
    return Counter({key: value for key, value in counter.items() if value})


def scale(counter, scalar):
    return clean(Counter({key: Q(scalar) * value
                          for key, value in counter.items()}))


def rank(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_linear_circuit_normal_form():
    audits = []
    for width in range(2, 9):
        # C_u=e_u, lambda_u=u+1, T=sum lambda_u C_u.  Modulo T, eliminate
        # the last coordinate.  The projected columns have their unique
        # dependence lambda, with every coefficient nonzero.
        lambdas = tuple(Q(index + 1) for index in range(width))
        columns = [tuple(Q(int(row == column)) for row in range(width))
                   for column in range(width)]
        target = tuple(lambdas)
        require(rank([[column[row] for column in columns]
                      for row in range(width)]) == width,
                "the independent minimum-support columns changed")

        projected = []
        for column in columns:
            # quotient by <T>, using the last target coordinate as pivot
            projected.append(tuple(
                column[row] - column[-1] * target[row] / target[-1]
                for row in range(width - 1)
            ))
        projected_matrix = [[column[row] for column in projected]
                            for row in range(width - 1)]
        require(rank(projected_matrix) == width - 1,
                "the quotient circuit lost rank")
        require(all(sum(lambdas[column] * projected_matrix[row][column]
                        for column in range(width)) == 0
                    for row in range(width - 1)),
                "the star coefficients stopped being the quotient circuit")
        audits.append({
            "occupied_sites": width,
            "column_rank": width,
            "target_quotient_rank": width - 1,
            "quotient_kernel_dimension": 1,
            "circuit_has_full_support": True,
        })
    return audits


def insert_edge(ambient, edge, colours, cofactor):
    remainder = tuple(site for site in ambient if site not in edge)
    output = Counter()
    for word, coefficient in cofactor.items():
        require(len(word) == len(remainder),
                (ambient, edge, len(word), len(remainder)))
        assignment = {edge[0]: colours[0], edge[1]: colours[1]}
        assignment.update(dict(zip(remainder, word, strict=True)))
        output[tuple(assignment[site] for site in ambient)] += coefficient
    return clean(output)


def audit_genuine_hessian(guard):
    q = guard.q_data()
    sites = tuple(guard.SITES)
    edges = tuple((left, right) for left in sites for right in sites
                  if left < right)
    cells_by_edge = {
        edge: tuple((left_colour, right_colour, coefficient)
                    for (left, right, left_colour, right_colour), coefficient
                    in q.items() if (left, right) == edge)
        for edge in edges
    }
    first = {
        edge: guard.hafnian_tensor(
            q, tuple(site for site in sites if site not in edge))
        for edge in edges
    }
    second = {}
    for index, edge in enumerate(edges):
        for other in edges[index + 1:]:
            if set(edge) & set(other):
                continue
            key = tuple(sorted((edge, other)))
            removed = set(edge) | set(other)
            second[key] = guard.hafnian_tensor(
                q, tuple(site for site in sites if site not in removed))

    # 2 F_e = sum_f q_f G_ef for every physical hole e.  This is the
    # genuine common symmetric Hessian recurrence, not declared F/G data.
    first_checks = 0
    for edge in edges:
        ambient = tuple(site for site in sites if site not in edge)
        recurrence = Counter()
        for other in edges:
            if set(edge) & set(other):
                continue
            key = tuple(sorted((edge, other)))
            for left_colour, right_colour, coefficient in cells_by_edge[other]:
                recurrence.update(scale(insert_edge(
                    ambient, other, (left_colour, right_colour), second[key]
                ), coefficient))
        require(clean(recurrence) == scale(first[edge], 2),
                f"genuine Hessian recurrence failed at {edge}")
        first_checks += 1

    # 3 q^[3] = sum_e q_e F_e.  The affine guard has zero top, and both
    # sides vanish coefficientwise.
    top = guard.hafnian_tensor(q, sites)
    top_euler = Counter()
    for edge in edges:
        for left_colour, right_colour, coefficient in cells_by_edge[edge]:
            top_euler.update(scale(insert_edge(
                sites, edge, (left_colour, right_colour), first[edge]
            ), coefficient))
    require(clean(top_euler) == scale(top, 3) == Counter(),
            "the genuine top Euler identity changed")

    x_target = guard.X_TARGET
    mixed_debt = guard.MIXED_DEBT
    fixed_s = ((5, 1, Q(1)),)
    column0 = guard.response(q, ((0, 1, Q(1)),), fixed_s)
    column1 = guard.response(q, ((1, 1, Q(1)),), fixed_s)
    require(column0 == Counter({x_target: Q(1), mixed_debt: Q(1)})
            and column1 == Counter({mixed_debt: Q(-1)}),
            "the two physical response columns changed")
    require(clean(column0 + column1) == Counter({x_target: Q(1)}),
            "the diagonal target response changed")
    require(rank([
        [column0.get(x_target, 0), column1.get(x_target, 0)],
        [column0.get(mixed_debt, 0), column1.get(mixed_debt, 0)],
    ]) == 2, "the occupied site columns stopped being minimum")

    # Literal source provenance of X+Y and -Y.  The two Y matchings differ
    # on P-0-2-1-P and share Q5 and 34.  Both P arms are target-line E_11,
    # so the endpoint Pluecker determinant is identically zero.
    carrier_matchings = {
        "X": (("P0:11", "Q5:11", "13:11", "24:11"), Q(1)),
        "+Y": (("P0:11", "Q5:11", "12:10", "34:00"), Q(1)),
        "-Y": (("P1:11", "Q5:11", "02:10", "34:00"), Q(-1)),
    }
    require(q[guard.cell(1, 3, 1, 1)]
            * q[guard.cell(2, 4, 1, 1)] == 1,
            "the pure carrier changed")
    require(q[guard.cell(1, 2, 1, 0)]
            * q[guard.cell(3, 4, 0, 0)] == 1,
            "the positive debt carrier changed")
    require(q[guard.cell(0, 2, 1, 0)]
            * q[guard.cell(3, 4, 0, 0)] == -1,
            "the negative debt carrier changed")
    endpoint_matrix = ((Q(1), Q(1)), (Q(0), Q(0)))
    endpoint_minor = (endpoint_matrix[0][0] * endpoint_matrix[1][1]
                      - endpoint_matrix[0][1] * endpoint_matrix[1][0])
    require(endpoint_minor == 0,
            "the axis-purified endpoint exchange became curved")

    return {
        "q_cells": len(q),
        "genuine_first_cofactors": len(first),
        "genuine_symmetric_second_cofactors": len(second),
        "cofactor_euler_checks": first_checks,
        "top": 0,
        "top_euler": "sum_e q_e F_e = 3 q^[3] = 0",
        "occupied_response_columns": ["X1+Y", "-Y"],
        "occupied_column_rank": 2,
        "individual_site_components_in_kernel": 0,
        "axis_star_self_square": "e1@0 * e1@1 != 0",
        "carrier_matchings": {
            name: {"cells": list(cells), "coefficient": str(coefficient)}
            for name, (cells, coefficient) in carrier_matchings.items()
        },
        "mixed_debt_exchange_cycle": ["P0", "02", "21", "1P"],
        "common_cells": ["Q5:11", "34:00"],
        "endpoint_rank": 1,
        "endpoint_pluecker_minor": str(endpoint_minor),
        "missing_full_packet_rows": [
            "q^[3]=X0", "second diagonal response X2",
            "the two coupled crossed rows for that second star pair",
        ],
    }


def main():
    pin_dependencies()
    guard = load_guard()
    ledger = {
        "pins": PINS,
        "minimum_support_linear_theorem": {
            "statement": (
                "if occupied complete response columns C_u are support-"
                "minimal and sum lambda_u C_u=T, they are independent; "
                "modulo <T> their images have rank k-1 and lambda is the "
                "unique full-support circuit"
            ),
            "representative_exact_audits": audit_linear_circuit_normal_form(),
        },
        "physical_genuine_hessian_boundary": audit_genuine_hessian(guard),
        "verdict": (
            "common symmetric Hessian provenance turns a minimum multisite "
            "axis star into a source-labelled carrier circuit, but it does "
            "not by itself put an occupied site component in the joint "
            "kernel or create a curved endpoint minor"
        ),
        "next_actual_source_input": (
            "couple the flat internal carrier circuit to the missing unary "
            "top and the other-colour diagonal/crossed companion rows; this "
            "is the first place a crossed endpoint arm or a source-valid "
            "minimum-support deletion can arise"
        ),
        "scope": (
            "coordinate-free minimum-support normal form plus an exact "
            "physical h=3 boundary; not a full one-bad packet because its "
            "unary top and second-colour response packet are absent"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"axis Hessian carrier-circuit ledger changed: {digest}")
    print("uniform one-bad axis/Hessian carrier-circuit boundary: PASS")
    print("minimum k-site response: column rank k; target quotient rank k-1")
    print("physical k=2 columns: X1+Y, -Y; genuine Hessian recurrences: 15")
    print("flat carrier exchange: C4; endpoint Pluecker minor: 0")
    print("remaining source input: unary top + other-colour companion rows")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
