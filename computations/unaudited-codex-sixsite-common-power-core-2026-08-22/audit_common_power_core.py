#!/usr/bin/env python3
"""Exact audit of the isolated h=3 common-power core.

This replays the literal six-site scalar-zero packet and proves that the
unique response product cancelling q^[3] is a diagonal channel.  Hence the
two displayed common-power equations, even with one shared rank-three
endpoint factorization, do not retain the fixed-label off-diagonal incidence
of a normalized full-nine row.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py"
SOURCE_SHA256 = "20ec8fabda17ab915e9b071df00a06d72e985943a3672a5f0a9e02edff80badf"
EXPECTED_LEDGER_SHA256 = "a45ce1b648f7792848b1232dbcda425e878ac7629c2bba6b5e84f1242b61f90f"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    actual = sha256(SOURCE.read_bytes()).hexdigest()
    require(actual == SOURCE_SHA256,
            ("pinned source changed", actual, SOURCE_SHA256))
    spec = importlib.util.spec_from_file_location("scalar_packet", SOURCE)
    require(spec is not None and spec.loader is not None, "cannot load source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def product_table(module, left, right):
    output = defaultdict(lambda: module.ZERO)
    for (left_site, left_colour), left_value in left.items():
        for (right_site, right_colour), right_value in right.items():
            if left_site == right_site:
                continue
            if left_site < right_site:
                key = ((left_site, right_site), left_colour, right_colour)
            else:
                key = ((right_site, left_site), right_colour, left_colour)
            output[key] = module.gadd(
                output[key], module.gmul(left_value, right_value))
    return {key: value for key, value in output.items()
            if value != module.ZERO}


def gaussian_tangent(module, distinguished, common):
    """Return distinguished*common^[2] with Gaussian-rational entries."""
    output = {}
    for word in module.WORDS:
        coefficient = module.ZERO
        for matching in module.MATCHINGS:
            for chosen, endpoints in enumerate(matching):
                term = distinguished.get(
                    (endpoints, word[endpoints[0]], word[endpoints[1]]),
                    module.ZERO,
                )
                for index, other in enumerate(matching):
                    if index == chosen:
                        continue
                    q_value = common.get(
                        (other, word[other[0]], word[other[1]]), Q(0))
                    term = module.gmul(term, (q_value, Q(0)))
                coefficient = module.gadd(coefficient, term)
        if coefficient != module.ZERO:
            output[word] = coefficient
    return output


def add_gaussian_tables(module, *tables):
    output = defaultdict(lambda: module.ZERO)
    for table in tables:
        for key, value in table.items():
            output[key] = module.gadd(output[key], value)
    return {key: value for key, value in output.items()
            if value != module.ZERO}


def scale_gaussian_table(module, scalar, table):
    return {key: module.gscale(scalar, value) for key, value in table.items()
            if module.gscale(scalar, value) != module.ZERO}


def rref(matrix, coefficient_columns):
    matrix = [list(row) for row in matrix]
    pivot_row = 0
    pivots = []
    for column in range(coefficient_columns):
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
        pivots.append(column)
        pivot_row += 1
    return matrix, tuple(pivots)


def word_name(word):
    return "".join(map(str, word))


def serialize_gaussian(table):
    return tuple(
        (word_name(word), str(value[0]), str(value[1]))
        for word, value in sorted(table.items())
    )


def build_ledger():
    module = load_source()
    p, s, diagonal_channels = module.response_factorization()
    channel_products = tuple(
        product_table(module, p[i], s[j])
        for i in range(3) for j in range(3)
    )
    images = tuple(
        gaussian_tangent(module, product, module.COMMON)
        for product in channel_products
    )

    q3_rational = module.cube_coefficients(module.COMMON)
    q3 = {word: (value, Q(0)) for word, value in q3_rational.items()}
    require(q3 == {tuple(map(int, "020200")): (Q(1), Q(0))}, q3)

    # The 22 product is the exact adjacent-power canceller:
    # q*q^[2]=3q^[3], hence (q+3z)q^[2]=0 iff zq^[2]=-q^[3].
    z_image = images[8]
    require(z_image == scale_gaussian_table(module, Q(-1), q3), z_image)
    q_times_q2 = scale_gaussian_table(module, Q(3), q3)
    corrected_row = add_gaussian_tables(
        module, q_times_q2, scale_gaussian_table(module, Q(3), z_image))
    require(corrected_row == {}, corrected_row)

    # r=-sum_i p_i s_i.  Reconstruct the source response R first, then
    # negate its common-power image and cube.
    response = {}
    for key in set().union(*(set(channel) for channel in diagonal_channels)):
        value = module.ZERO
        for channel in diagonal_channels:
            value = module.gadd(value, channel.get(key, module.ZERO))
        if value != module.ZERO:
            response[key] = value
    expected_response = {
        key: (value, Q(0)) for key, value in module.R.items()
    }
    require(response == expected_response, (response, expected_response))
    response_real = {key: value[0] for key, value in response.items()}
    response_q2 = module.tangent_coefficients(response_real, module.COMMON)
    response3 = module.cube_coefficients(response_real)
    delta = {(colour,) * 6: Q(1) for colour in range(3)}
    require(response_q2 == delta, response_q2)
    require(response3 == {(0,) * 6: Q(-1)}, response3)
    r_q2 = {word: -value for word, value in response_q2.items()}
    r3 = {word: -value for word, value in response3.items()}
    require(r_q2 == {word: -value for word, value in delta.items()}, r_q2)
    require(r3 == {(0,) * 6: Q(1)}, r3)

    # Solve Psi_q(sum x_ij p_i s_j)=-q^[3] over C exactly.  Split every
    # Gaussian equation into rational real/imaginary rows.  The 18 unknowns
    # are Re(x_00),...,Re(x_22),Im(x_00),...,Im(x_22).
    words = sorted(set(q3).union(*(set(image) for image in images)))
    equations = []
    for word in words:
        coefficients = tuple(image.get(word, module.ZERO) for image in images)
        target = module.gscale(Q(-1), q3.get(word, module.ZERO))
        equations.append(
            [value[0] for value in coefficients]
            + [-value[1] for value in coefficients]
            + [target[0]]
        )
        equations.append(
            [value[1] for value in coefficients]
            + [value[0] for value in coefficients]
            + [target[1]]
        )
    reduced, pivots = rref(equations, 18)
    require(pivots == tuple(range(18)), pivots)
    solution = [Q(0)] * 18
    for row, column in enumerate(pivots):
        solution[column] = reduced[row][-1]
    expected_solution = [Q(0)] * 18
    expected_solution[8] = Q(1)
    require(solution == expected_solution, solution)

    # A trace-preserving change of endpoint channel bases has
    # P'=PG, S'=S G^{-T}.  Its (a,b) product has channel coefficients
    # x=u v^T with u^T v=delta_ab.  The unique solution x=E_22 has
    # trace pairing one, so it cannot occupy an off-diagonal cell.
    coefficient_matrix = tuple(solution[:9])
    trace_pairing = coefficient_matrix[0] + coefficient_matrix[4] + coefficient_matrix[8]
    require(trace_pairing == Q(1), trace_pairing)

    return {
        "theorem": "corrected h3 adjacent/common-power scalar core guard",
        "pinned_source": {str(SOURCE.relative_to(ROOT)): SOURCE_SHA256},
        "normalization": {
            "divided_power": "q*q^[2]=3q^[3]",
            "selected_row": "(q+3z)q^[2]=0",
            "uncorrected_q_plus_z_is_not_used": True,
        },
        "literal_packet": {
            "q^[3]": serialize_gaussian(q3),
            "z": "p_2*s_2",
            "z*q^[2]": serialize_gaussian(z_image),
            "r": "-sum_i p_i*s_i",
            "r*q^[2]": tuple((word_name(word), str(value))
                              for word, value in sorted(r_q2.items())),
            "r^[3]": tuple((word_name(word), str(value))
                            for word, value in sorted(r3.items())),
            "endpoint_triples_injective": True,
            "channel_pairing": "identity",
        },
        "unique_canceller": {
            "word_rows": len(words),
            "rational_equations": len(equations),
            "unknowns_over_Q": 18,
            "rank": len(pivots),
            "solution": "x_22=1, all other complex x_ij=0",
            "trace_pairing": str(trace_pairing),
            "offdiagonal_trace_pairing_required": "0",
        },
        "scope": {
            "what_is_refuted": (
                "any deduction from the two scalar common-power equations, "
                "nonnilpotence, and an unlabeled shared rank-three endpoint "
                "factorization"
            ),
            "what_is_not_refuted": (
                "the literal fixed-label full-nine packet with a!=b, six "
                "offdiagonal annihilator cells, and three separately labelled "
                "diagonal target rows"
            ),
            "first_missing_datum": (
                "the selected canceller must be offdiagonal relative to the "
                "same trace pairing used in r=-sum B_ii"
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("six-site corrected common-power core: PASS")
    print("(q+3z)q2=0; r q2=-Delta; r3=X0")
    print("unique canceller x=E22 has trace pairing 1, hence is not offdiagonal")
    print("mode", arguments.mode)
    print("sha256:", digest)


if __name__ == "__main__":
    main()
