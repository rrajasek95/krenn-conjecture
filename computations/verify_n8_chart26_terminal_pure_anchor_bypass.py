#!/usr/bin/env python3
"""Five-row pure-anchor bypass for the chart-26 terminal 102-face.

The 96-coordinate off-path terminal face was exposed in
verify_n8_chart26_terminal_triangular_exposure.py.  Adjoining the six first
path-edge error directions creates a quadratic matching-cycle system.  This
checker proves that no contraction of that system is needed for the selected
terminal carrier: five literal mixed hafnians have a Laurent polynomial
combination equal to the carrier itself.

Both the normalized identity and its support-cleared lift are verified over
the integers.  Thus this is characteristic-zero localized ideal membership,
not a numerical or modular rank certificate.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = (
    "e8fb7275325ed2e28b11bd9314a4d43c5dfa346563ccfb2923b3752c6f5263b1"
)


def load_module(name, filename):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXPOSURE = load_module(
    "n8_chart26_terminal_pure_anchor_base",
    "verify_n8_chart26_terminal_triangular_exposure.py",
)
AUGMENTED = EXPOSURE.AUGMENTED
TERMINAL = EXPOSURE.TERMINAL
D5 = EXPOSURE.D5

SIX_PATH_DIRECTIONS = frozenset((120, 121, 122, 240, 241, 242))
SOURCE_WORDS = (
    (0, 0, 1, 1, 1, 1, 1, 1),
    (1, 2, 0, 1, 2, 1, 2, 0),
    (1, 2, 1, 1, 1, 1, 2, 2),
    (1, 2, 1, 1, 2, 2, 2, 1),
    (2, 1, 0, 0, 2, 0, 1, 0),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def monomial(*variable_ids):
    return {bytes(sorted(variable_ids)): 1}


def monomial_product(*packets):
    return AUGMENTED.product_polynomials(packets)


def polynomial_text(polynomial):
    return [
        {
            "coefficient": coefficient,
            "coordinates": [
                list(D5.COORDINATES[variable_id])
                for variable_id in monomial_value
            ],
        }
        for monomial_value, coefficient in sorted(polynomial.items())
    ]


def word_text(word):
    return "".join(map(str, word))


def restricted_full_hafnian(word, active_ids):
    coordinates = {
        D5.COORDINATES[variable_id]: AUGMENTED.variable(variable_id)
        for variable_id in active_ids
    }
    return AUGMENTED.restricted_hafnian(word, coordinates)


def laurent_parts(numerator, denominator):
    numerator_counts = Counter(numerator)
    denominator_counts = Counter(denominator)
    common = numerator_counts & denominator_counts
    numerator_counts -= common
    denominator_counts -= common
    return (
        bytes(sorted(numerator_counts.elements())),
        bytes(sorted(denominator_counts.elements())),
    )


def audit():
    off_path = EXPOSURE.off_path_endpoint_coordinates()
    candidates = off_path | SIX_PATH_DIRECTIONS
    require(len(off_path) == 96 and len(candidates) == 102,
            "terminal 96+6 coordinate census changed")
    active = EXPOSURE.SUPPORT | EXPOSURE.TERMINAL_ROW | candidates

    # Seven terminal-row variables.
    x01 = D5.COORDINATE_ID[(0, 1, 1, 1)]
    x04 = D5.COORDINATE_ID[(0, 4, 2, 2)]
    x17 = D5.COORDINATE_ID[(1, 7, 2, 2)]
    x23 = D5.COORDINATE_ID[(2, 3, 0, 0)]
    x36 = D5.COORDINATE_ID[(3, 6, 1, 1)]
    x46 = D5.COORDINATE_ID[(4, 6, 0, 0)]
    x57 = D5.COORDINATE_ID[(5, 7, 0, 0)]

    # Coordinates in the five-row cancellation packet.
    x26 = D5.COORDINATE_ID[(2, 6, 1, 2)]
    x27_00 = D5.COORDINATE_ID[(2, 7, 0, 0)]
    x27_11 = D5.COORDINATE_ID[(2, 7, 1, 1)]
    x35 = D5.COORDINATE_ID[(3, 5, 0, 0)]
    x45 = D5.COORDINATE_ID[(4, 5, 1, 1)]
    x56 = D5.COORDINATE_ID[(5, 6, 1, 2)]
    path_x57 = D5.COORDINATE_ID[(5, 7, 2, 1)]

    # The support units used by the unnormalized lift.
    s01 = D5.COORDINATE_ID[(0, 1, 0, 0)]
    s03 = D5.COORDINATE_ID[(0, 3, 1, 1)]
    s14 = D5.COORDINATE_ID[(1, 4, 2, 2)]
    s16 = D5.COORDINATE_ID[(1, 6, 1, 1)]
    s23 = D5.COORDINATE_ID[(2, 3, 2, 2)]
    s24 = D5.COORDINATE_ID[(2, 4, 1, 1)]
    s56 = D5.COORDINATE_ID[(5, 6, 2, 2)]
    s57 = D5.COORDINATE_ID[(5, 7, 1, 1)]
    require({s01, s03, s14, s16, s23, s24, s56, s57}
            <= EXPOSURE.SUPPORT,
            "a pure-anchor lift coordinate left chart support")

    full_generators = tuple(
        restricted_full_hafnian(word, active) for word in SOURCE_WORDS
    )
    expected_full_generators = (
        {
            bytes(sorted((s01, s24, x36, s57))): 1,
            bytes(sorted((s01, x27_11, x36, x45))): 1,
        },
        {bytes(sorted((s03, s14, x27_00, x56))): 1},
        {
            bytes(sorted((s03, x17, s24, x56))): 1,
            bytes(sorted((s03, x17, x26, x45))): 1,
        },
        {
            bytes(sorted((s03, s14, x26, path_x57))): 1,
            bytes(sorted((s03, s14, x27_11, s56))): 1,
        },
        {
            bytes(sorted((x04, s16, x23, x57))): 1,
            bytes(sorted((x04, s16, x27_00, x35))): 1,
        },
    )
    require(full_generators == expected_full_generators,
            "one of the five literal mixed source rows changed")
    require(all(len(set(word)) > 1 for word in SOURCE_WORDS),
            "a pure source word entered the anchor certificate")

    # Polynomial multipliers for the support-cleared identity.  Signs are
    # (+,+,+,-,-).  All five products have physical degree twelve.
    multipliers = (
        monomial(x04, x17, x23, x57, s03, s14, s56, s16),
        monomial(x04, x17, s16, s24, s01, x36, path_x57, x35),
        monomial(x04, x23, x57, s14, s16, s01, x36, path_x57),
        monomial(x04, x17, x23, x57, s16, s01, x36, x45),
        monomial(x17, s03, s14, s24, s01, x36, path_x57, x56),
    )
    signs = (1, 1, 1, -1, -1)
    certificate = {}
    for sign, multiplier, generator in zip(
        signs, multipliers, full_generators
    ):
        certificate = AUGMENTED.add(
            certificate,
            AUGMENTED.scale(AUGMENTED.multiply(multiplier, generator), sign),
        )

    support_factor = bytes(sorted((
        s01, s03, s14, s16, s24, s56, s57,
    )))
    scalar_factor = bytes(sorted((x04, x17, x23, x36, x57)))
    cleared_anchor = {
        bytes(sorted(support_factor + scalar_factor)): 1
    }
    require(certificate == cleared_anchor,
            "the five-row support-cleared anchor identity changed")

    # Normalizing support deletes the seven support factors and gives the
    # compact identity B*C*D*p*q in the mixed ideal.
    normalized_generators = tuple(
        AUGMENTED.normalize_support(generator)
        for generator in full_generators
    )
    normalized_multipliers = tuple(
        AUGMENTED.normalize_support(multiplier)
        for multiplier in multipliers
    )
    normalized_certificate = {}
    for sign, multiplier, generator in zip(
        signs, normalized_multipliers, normalized_generators
    ):
        normalized_certificate = AUGMENTED.add(
            normalized_certificate,
            AUGMENTED.scale(AUGMENTED.multiply(multiplier, generator), sign),
        )
    require(normalized_certificate == monomial(
        x04, x17, x23, x36, x57
    ), "the normalized five-row identity changed")

    # Recover the unique full physical target lift of the selected Hamilton
    # row and prove its support-cleared source certificate directly.
    target = TERMINAL.pure_target_audit()
    selected_factor = target["selected_factor"]
    full_target_monomial = bytes(sorted(
        variable_id
        for pure_matching in selected_factor
        for variable_id in pure_matching
    ))
    expected_target = bytes(sorted((
        s01, x23, x46, x57,
        x01, s24, x36, s57,
        x04, x17, s23, s56,
    )))
    require(full_target_monomial == expected_target,
            "the selected physical target lift changed")
    require(AUGMENTED.normalize_support({full_target_monomial: 1})
            == {TERMINAL.SELECTED_ROW: 1},
            "the physical target stopped normalizing to the Hamilton row")

    # T / cleared_anchor = (x01*x46*s23)/(s03*s14*s16).  Clearing the
    # support-only denominator gives a literal polynomial source identity.
    target_numerator = bytes(sorted((x01, x46, s23)))
    target_denominator = bytes(sorted((s03, s14, s16)))
    quotient_numerator, quotient_denominator = laurent_parts(
        full_target_monomial,
        next(iter(cleared_anchor)),
    )
    require((quotient_numerator, quotient_denominator)
            == (target_numerator, target_denominator),
            "the terminal target Laurent quotient changed")
    require(set(target_denominator) <= EXPOSURE.SUPPORT,
            "the terminal target quotient gained a non-support denominator")

    cleared_target_left = monomial_product(
        {full_target_monomial: 1}, {target_denominator: 1}
    )
    cleared_target_right = {}
    numerator_polynomial = {target_numerator: 1}
    target_multipliers = []
    for sign, multiplier, generator in zip(
        signs, multipliers, full_generators
    ):
        target_multiplier = AUGMENTED.multiply(
            numerator_polynomial, multiplier
        )
        target_multipliers.append(target_multiplier)
        cleared_target_right = AUGMENTED.add(
            cleared_target_right,
            AUGMENTED.scale(
                AUGMENTED.multiply(target_multiplier, generator), sign
            ),
        )
    require(cleared_target_right == cleared_target_left,
            "the support-cleared terminal target certificate changed")

    ledger = {
        "terminal_row": TERMINAL.SELECTED_ROW.hex(),
        "terminal_endpoints": list(TERMINAL.SELECTED_ENDPOINTS),
        "face_coordinates": {
            "off_path": len(off_path),
            "path_edge": len(SIX_PATH_DIRECTIONS),
            "total": len(candidates),
        },
        "source_words": [word_text(word) for word in SOURCE_WORDS],
        "full_source_rows": [
            polynomial_text(generator) for generator in full_generators
        ],
        "full_multipliers": [
            polynomial_text(multiplier) for multiplier in multipliers
        ],
        "multiplier_signs": list(signs),
        "cleared_anchor": polynomial_text(cleared_anchor),
        "normalized_anchor": polynomial_text(normalized_certificate),
        "selected_unique_pure_matching_triple": [
            pure_matching.hex() for pure_matching in selected_factor
        ],
        "full_target_monomial": [
            list(D5.COORDINATES[variable_id])
            for variable_id in full_target_monomial
        ],
        "target_laurent_numerator": [
            list(D5.COORDINATES[variable_id])
            for variable_id in target_numerator
        ],
        "target_laurent_denominator_support": [
            list(D5.COORDINATES[variable_id])
            for variable_id in target_denominator
        ],
        "support_cleared_target_identity": {
            "left_terms": len(cleared_target_left),
            "right_terms_after_cancellation": len(cleared_target_right),
            "source_rows": len(full_generators),
        },
        "conclusion": (
            "on the selected simultaneous 102-coordinate face, the unique "
            "physical terminal Hamilton carrier belongs to the mixed source "
            "ideal after localization only at chart-support coordinates"
        ),
        "scope_guard": (
            "this is a pure-anchor bypass for the selected terminal carrier; "
            "it does not contract the whole 102-coordinate ideal and does "
            "not assert the identity after arbitrary additional off-face "
            "coordinates are restored"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen terminal pure-anchor ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print(
        "n=8 chart26 terminal pure-anchor bypass: PASS; "
        "five mixed rows kill the 102-face Hamilton carrier"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
