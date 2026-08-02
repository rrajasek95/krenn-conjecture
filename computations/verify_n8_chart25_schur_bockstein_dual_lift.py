#!/usr/bin/env python3
"""Exact Schur--Bockstein lift of the chart-25 four-row dual.

The frozen degree-four functional has three lower-filtration coordinates and
one leading coordinate.  This checker splits it as ``(-mu, lambda)`` for the
literal filtered source matrix

        [ A  0 ]
        [ T  B ]

and verifies ``lambda B = 0`` and ``lambda T = mu A`` on every source column
which can meet its support, both in the invariant quotient and on individually
labelled rows.  It also distinguishes the raw Schur target pairing from the
older hybrid display which paired the lower target with an already reduced
degree-four residual.

On the five-row common-factor fibre the same construction proves that the
relative ``4D`` vector is exactly the reduced Schur residual, with pairing one.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "086bc864911aef6b62d020c2a16ed82203e6ad3ca87005444e942162fd2a7ed4"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DUAL = load(
    "n8_chart25_schur_dual_base",
    "verify_n8_chart25_degree4_exact_dual.py",
)
RELATIVE = load(
    "n8_chart25_schur_relative_base",
    "verify_n8_chart25_relative_4d_obstruction.py",
)
BASE = DUAL.BASE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encode_fraction(value):
    value = QQ(value)
    return [value.numerator, value.denominator]


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vector(target, source, scalar=QQ(1)):
    for key, value in source.items():
        add_value(target, key, scalar * value)
    return target


def pairing(vector, cochain):
    return sum(
        (QQ(value) * cochain.get(key, QQ(0))
         for key, value in vector.items()),
        QQ(0),
    )


def invariant_column_pairing(column, cochain, degrees):
    """Pair one canonical source orbit with canonical invariant rows."""
    answer = QQ(0)
    for actual_column in BASE.column_orbit(column):
        for row in BASE.column_rows(actual_column):
            if (BASE.row_degree(row) in degrees
                    and row == BASE.canonical_row(row)):
                answer += cochain.get(row, QQ(0))
    return answer


def actual_column_pairing(column, cochain, degrees):
    """Pair one individually labelled source column with actual rows."""
    return sum(
        (cochain.get(row, QQ(0)) for row in BASE.column_rows(column)
         if BASE.row_degree(row) in degrees),
        QQ(0),
    )


def local_vector(rows, coefficients):
    return {
        row: QQ(coefficient)
        for row, coefficient in zip(rows, coefficients) if coefficient
    }


def tuple_dot(left, right):
    require(len(left) == len(right), "dot-product dimensions differ")
    return sum(
        (QQ(left[index]) * QQ(right[index]) for index in range(len(left))),
        QQ(0),
    )


def audit():
    lower_rows = tuple(
        row for row in DUAL.FUNCTIONAL if BASE.row_degree(row) < 4
    )
    leading_row, = (
        row for row in DUAL.FUNCTIONAL if BASE.row_degree(row) == 4
    )
    require(tuple(DUAL.FUNCTIONAL[row] for row in lower_rows) == (-2, -1, -1),
            "lower functional coordinates changed")
    require(DUAL.FUNCTIONAL[leading_row] == 1,
            "leading functional coordinate changed")

    # The lifted left cochain is ell=(-mu,lambda).
    mu = {row: QQ(-DUAL.FUNCTIONAL[row]) for row in lower_rows}
    lam = {leading_row: QQ(DUAL.FUNCTIONAL[leading_row])}
    lifted = {row: -value for row, value in mu.items()}
    lifted.update(lam)
    require(lifted == {row: QQ(value)
                       for row, value in DUAL.FUNCTIONAL.items()},
            "(-mu,lambda) does not recover the exact dual")

    # Support-local exhaustiveness was proved by the imported exact checker:
    # a column outside these incident families pairs to zero term by term.
    incident = DUAL.incident_source_columns()
    require({degree: len(columns) for degree, columns in incident.items()}
            == {2: 9, 3: 0, 4: 0},
            "canonical incident-source census changed")
    quotient_transfer_values = Counter()
    quotient_failures = []
    for degree, columns in incident.items():
        for column in columns:
            mu_a = invariant_column_pairing(column, mu, {2, 3})
            if degree < 4:
                lambda_t = invariant_column_pairing(column, lam, {4})
                quotient_transfer_values[(mu_a, lambda_t)] += 1
                if lambda_t != mu_a:
                    quotient_failures.append((repr(column), mu_a, lambda_t))
            else:
                lambda_b = invariant_column_pairing(column, lam, {4})
                if lambda_b:
                    quotient_failures.append((repr(column), "lambdaB", lambda_b))
    require(not quotient_failures,
            "quotient lambda*T=mu*A or lambda*B=0 failed")
    require(quotient_transfer_values == {
        (QQ(1), QQ(1)): 4,
        (QQ(2), QQ(2)): 5,
    }, "quotient transfer-value histogram changed")

    expanded, orbit_sizes = DUAL.expanded_functional()
    actual_mu = {
        row: -value for row, value in expanded.items()
        if BASE.row_degree(row) < 4
    }
    actual_lam = {
        row: value for row, value in expanded.items()
        if BASE.row_degree(row) == 4
    }
    actual_incident = DUAL.actual_incident_source_columns(expanded)
    require({degree: len(columns) for degree, columns in actual_incident.items()}
            == {2: 56, 3: 0, 4: 0},
            "actual incident-source census changed")
    actual_transfer_values = Counter()
    actual_failures = []
    for degree, columns in actual_incident.items():
        for column in columns:
            mu_a = actual_column_pairing(column, actual_mu, {2, 3})
            if degree < 4:
                lambda_t = actual_column_pairing(column, actual_lam, {4})
                actual_transfer_values[(mu_a, lambda_t)] += 1
                if lambda_t != mu_a:
                    actual_failures.append((repr(column), mu_a, lambda_t))
            else:
                lambda_b = actual_column_pairing(column, actual_lam, {4})
                if lambda_b:
                    actual_failures.append((repr(column), "lambdaB", lambda_b))
    require(not actual_failures,
            "actual-row lambda*T=mu*A or lambda*B=0 failed")
    require(actual_transfer_values == {(QQ(1, 4), QQ(1, 4)): 56},
            "actual transfer-value histogram changed")
    require(orbit_sizes == Counter({4: 3, 8: 1}),
            "dual-support orbit sizes changed")

    # Replay the chosen lower certificate only through the two cochains.  It
    # solves A*x0=-b and has the same value through T by the lift equation.
    certificate, _, _ = DUAL.VERIFY3.decode_certificate()
    mu_a_x0 = QQ(0)
    lambda_t_x0 = QQ(0)
    for word_text, multiplier, numerator, denominator in certificate:
        column = (tuple(map(int, word_text)), bytes(multiplier))
        scalar = QQ(numerator, denominator)
        mu_a_x0 += scalar * invariant_column_pairing(
            column, mu, {2, 3}
        )
        lambda_t_x0 += scalar * invariant_column_pairing(
            column, lam, {4}
        )
    require(mu_a_x0 == lambda_t_x0 == 2,
            "chosen certificate stopped satisfying the dual tail equation")

    # Here b,c are the raw residual coordinates in the convention
    # b+A*x=0, c+T*x+B*y=0.  Hence the Schur value is lambda*c-mu*b.
    raw_b = {
        row: DUAL.raw_target_coefficient(row) for row in lower_rows
    }
    raw_c = {leading_row: DUAL.raw_target_coefficient(leading_row)}
    mu_b = pairing(raw_b, mu)
    lambda_c = pairing(raw_c, lam)
    secondary_pairing = lambda_c - mu_b
    reduced_leading_pairing = lambda_c + lambda_t_x0
    raw_lifted_pairing = pairing(raw_b, lifted) + pairing(raw_c, lifted)
    require(tuple(raw_b.values()) == (QQ(-1), QQ(0), QQ(0))
            and tuple(raw_c.values()) == (QQ(-1),),
            "raw target coordinates changed")
    require(mu_b == -2 and lambda_c == -1,
            "raw target contractions changed")
    require(secondary_pairing == reduced_leading_pairing
            == raw_lifted_pairing == 1,
            "Schur target pairings no longer agree")
    require(mu_a_x0 == -mu_b,
            "lower certificate no longer solves the target under mu")

    actual_raw_b = {
        row: DUAL.raw_target_coefficient(row) for row in actual_mu
    }
    actual_raw_c = {
        row: DUAL.raw_target_coefficient(row) for row in actual_lam
    }
    actual_mu_b = pairing(actual_raw_b, actual_mu)
    actual_lambda_c = pairing(actual_raw_c, actual_lam)
    actual_lifted_pairing = (
        -actual_mu_b + actual_lambda_c
    )
    require(actual_mu_b == mu_b and actual_lambda_c == lambda_c
            and actual_lifted_pairing == raw_lifted_pairing,
            "actual-row and invariant raw target pairings disagree")

    # The older display used the lower part of the lifted cochain on b and
    # lambda on the already reduced degree-four residual.  It is a useful
    # nonzero diagnostic, but it double-counts the transferred tail and is
    # not the Schur pairing of one raw target vector.
    hybrid_pairing = pairing(raw_b, lifted) + reduced_leading_pairing
    require(hybrid_pairing == 3,
            "frozen hybrid display pairing changed")
    require(hybrid_pairing - secondary_pairing == lambda_t_x0,
            "hybrid/Schur discrepancy is not the transferred tail")

    # Five-row common-factor fibre.  Its literal cochain has -1/4 on four
    # lower AB leaves and +1/4 on the leading B^2 centre.
    local_rows = RELATIVE.frozen_rows()
    ab_rows = local_rows[:4]
    d_row = local_rows[4]
    require(tuple(BASE.row_degree(row) for row in local_rows)
            == (2, 2, 2, 2, 4),
            "local fibre filtration changed")
    local_mu = {row: QQ(1, 4) for row in ab_rows}
    local_lam = {d_row: QQ(1, 4)}
    local_boundaries = tuple(
        {ab_row: QQ(1), d_row: QQ(1)} for ab_row in ab_rows
    )
    require(all(pairing(boundary, local_mu) == pairing(boundary, local_lam)
                == QQ(1, 4) for boundary in local_boundaries),
            "local source-labelled lift equation failed")

    # q is the quotient packet.  Solving its lower part with the first three
    # labelled edges adds 3D, so its reduced leading residual is exactly 4D.
    local_b = local_vector(local_rows, (-1, -1, -1, 0, 0))
    local_c = {d_row: QQ(1)}
    correction = {}
    for boundary in local_boundaries[:3]:
        add_vector(correction, boundary)
    require({row: local_b.get(row, QQ(0))
             + correction.get(row, QQ(0)) for row in ab_rows}
            == {row: QQ(0) for row in ab_rows},
            "local lower correction did not solve b+A*x0=0")
    reduced_local = dict(local_c)
    add_value(reduced_local, d_row, correction.get(d_row, QQ(0)))
    four_d = {d_row: QQ(4)}
    require(reduced_local == four_d,
            "local reduced leading residual is not 4D")
    local_secondary = pairing(local_c, local_lam) - pairing(local_b, local_mu)
    require(local_secondary == pairing(four_d, local_lam) == 1,
            "local 4D class is not the Schur secondary pairing")

    quotient_packet = dict(local_b)
    add_vector(quotient_packet, local_c)
    literal_packet = local_vector(local_rows, (-1, -1, -1, 0, -3))
    packet_difference = dict(quotient_packet)
    add_vector(packet_difference, literal_packet, QQ(-1))
    local_lifted = {row: -value for row, value in local_mu.items()}
    local_lifted.update(local_lam)
    require(packet_difference == four_d,
            "quotient/literal packet difference changed")
    require(pairing(quotient_packet, local_lifted) == 1
            and pairing(literal_packet, local_lifted) == 0,
            "local packet pairings changed")

    # Exact target-side interface with the selected full-nine split-cap
    # quotient.  This proves the scalar factorization expected of a
    # comparison; it deliberately does not assert the missing source map.
    full_nine_samples = (
        (QQ(2), QQ(3), QQ(5), QQ(11), QQ(7, 5)),
        (QQ(3), QQ(0), QQ(2), QQ(5), QQ(-4, 9)),
        (QQ(-2), QQ(7), QQ(3), QQ(-5), QQ(13, 6)),
        (QQ(5, 3), QQ(-7, 4), QQ(11, 5), QQ(2, 9), QQ(-8, 7)),
    )
    full_nine_records = []
    for a, b_value, f, u, y_value in full_nine_samples:
        kappa = a * u - b_value * f
        require(kappa and y_value, "full-nine interface sample is inactive")
        connection = (a, f)
        curvature_column = (b_value, u)
        adjugate = (-f, a)
        require(tuple_dot(adjugate, connection) == 0,
                "adjugate stopped killing the connection column")
        require(tuple_dot(adjugate, curvature_column) == kappa,
                "adjugate stopped reading the curvature minor")

        # Coordinates are (cap boundary, physical target, ordinary residue).
        target_column = (-y_value, QQ(1), QQ(0))
        residue_column = (QQ(1), QQ(0), QQ(1))
        cap_cochain = (QQ(1), y_value, QQ(-1))
        split_cap = (kappa * y_value, QQ(0), QQ(0))
        require(tuple_dot(cap_cochain, target_column) == 0
                and tuple_dot(cap_cochain, residue_column) == 0,
                "split-cap cochain stopped annihilating existing columns")
        cap_pairing = tuple_dot(cap_cochain, split_cap)
        factorized_pairing = (
            local_secondary
            * tuple_dot(adjugate, curvature_column)
            * y_value
        )
        require(cap_pairing == factorized_pairing == kappa * y_value,
                "chart25/curvature/adjacent-power factorization failed")
        full_nine_records.append({
            "kappa": encode_fraction(kappa),
            "adjacent_power": encode_fraction(y_value),
            "cap_pairing": encode_fraction(cap_pairing),
        })

    ledger = {
        "quotient_functional_split": {
            "minus_mu": [encode_fraction(-mu[row]) for row in lower_rows],
            "lambda": encode_fraction(lam[leading_row]),
        },
        "canonical_incident_columns": {
            str(degree): len(columns) for degree, columns in incident.items()
        },
        "quotient_transfer_value_histogram": sorted(
            (encode_fraction(left), encode_fraction(right), count)
            for (left, right), count in quotient_transfer_values.items()
        ),
        "actual_incident_columns": {
            str(degree): len(columns)
            for degree, columns in actual_incident.items()
        },
        "actual_transfer_value_histogram": sorted(
            (encode_fraction(left), encode_fraction(right), count)
            for (left, right), count in actual_transfer_values.items()
        ),
        "certificate_mu_A_x0": encode_fraction(mu_a_x0),
        "certificate_lambda_T_x0": encode_fraction(lambda_t_x0),
        "mu_b": encode_fraction(mu_b),
        "lambda_c": encode_fraction(lambda_c),
        "raw_lifted_target_pairing": encode_fraction(raw_lifted_pairing),
        "actual_raw_lifted_target_pairing": encode_fraction(
            actual_lifted_pairing
        ),
        "reduced_leading_target_pairing": encode_fraction(
            reduced_leading_pairing
        ),
        "schur_secondary_pairing": encode_fraction(secondary_pairing),
        "old_hybrid_display_pairing": encode_fraction(hybrid_pairing),
        "local_rows": [row.hex() for row in local_rows],
        "local_source_rank": 4,
        "local_reduced_residual": "4D",
        "local_4D_pairing": encode_fraction(pairing(four_d, local_lam)),
        "local_quotient_packet_pairing": encode_fraction(
            pairing(quotient_packet, local_lifted)
        ),
        "local_literal_packet_pairing": encode_fraction(
            pairing(literal_packet, local_lifted)
        ),
        "full_nine_target_side_factorization": {
            "chart25_4D_pairing": encode_fraction(local_secondary),
            "cap_left_kernel": "(1,Y,-1)",
            "samples": full_nine_records,
            "literal_source_comparison_constructed": False,
        },
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart25 Schur--Bockstein ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 exact Schur--Bockstein dual lift: PASS")
    print("lambda*T = mu*A on canonical/actual incident columns:",
          sum(ledger["canonical_incident_columns"].values()),
          sum(ledger["actual_incident_columns"].values()))
    print("raw / reduced / Schur target pairings:",
          ledger["raw_lifted_target_pairing"],
          ledger["reduced_leading_target_pairing"],
          ledger["schur_secondary_pairing"])
    print("old hybrid display pairing:",
          ledger["old_hybrid_display_pairing"])
    print("local reduced residual / pairing:",
          ledger["local_reduced_residual"], ledger["local_4D_pairing"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
