#!/usr/bin/env python3
"""Exact source correction for the chart-26 terminal spoke ambiguity.

Restrict the aggregate coordinate ring to the twelve chart coordinates, the
seven coordinates of terminal row 04237475b8cfea, and x_02^{00}.  The chart
coordinates are then normalized to one.  On this face the single mixed
hafnian H_01000111 is exactly x_02^{00}, and the four clean-cap errors are
monomial multiples of that source equation.  Thus one source-labelled scalar
is both necessary and sufficient to correct this one-spoke terminal lift.

This is a face-local source-ideal calculation.  It does not construct the
uniform path-forest contraction or control simultaneous off-face spokes.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = (
    "1c651d1c5b004ec28fa6d158fd12de21ae3b1c4213131617a545cc8e30b9b490"
)
BOUNDARY_WORD = (0, 1, 0, 0, 0, 1, 1, 1)
ERROR_WORDS = (
    (0, 2, 0, 2, 2, 0),
    (0, 2, 0, 2, 2, 1),
    (0, 2, 2, 2, 2, 0),
    (0, 2, 2, 2, 2, 1),
)


def load_module(name, filename):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TERMINAL = load_module(
    "n8_chart26_augmented_terminal_base",
    "verify_n8_chart26_terminal_hamilton_readout.py",
)
D5 = TERMINAL.D5


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(polynomial, monomial, coefficient):
    value = polynomial.get(monomial, 0) + coefficient
    if value:
        polynomial[monomial] = value
    else:
        polynomial.pop(monomial, None)


def add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        add_value(answer, monomial, coefficient)
    return answer


def scale(polynomial, scalar):
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def multiply(left, right):
    answer = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            add_value(
                answer,
                bytes(sorted(first + second)),
                first_coefficient * second_coefficient,
            )
    return answer


def product_polynomials(polynomials):
    answer = {b"": 1}
    for polynomial in polynomials:
        answer = multiply(answer, polynomial)
    return answer


def variable(variable_id):
    return {bytes((variable_id,)): 1}


def normalize_support(polynomial):
    """Set every frozen chart-support coordinate equal to one."""
    answer = {}
    for monomial, coefficient in polynomial.items():
        normalized = bytes(
            variable_id for variable_id in monomial
            if variable_id not in D5.SUPPORT_IDS
        )
        add_value(answer, normalized, coefficient)
    return answer


def restricted_coordinates():
    active_ids = set(D5.SUPPORT_IDS)
    active_ids.update(TERMINAL.SELECTED_ROW)
    spoke_id = D5.COORDINATE_ID[TERMINAL.PERTURBING_SPOKE]
    active_ids.add(spoke_id)
    return {
        D5.COORDINATES[variable_id]: variable(variable_id)
        for variable_id in active_ids
    }


def restricted_hafnian(word, coordinates):
    polynomial = {}
    for term in D5.iter_word_terms(D5.word_code(word)):
        factors = []
        for variable_id in term:
            coordinate = D5.COORDINATES[variable_id]
            if coordinate not in coordinates:
                break
            factors.append(coordinates[coordinate])
        else:
            for monomial, coefficient in product_polynomials(factors).items():
                add_value(polynomial, monomial, coefficient)
    return polynomial


def polynomial_cap_error(coordinates):
    """Expand s r^[2] q + r^[3] in the restricted coordinate ring."""
    blocks = {edge: {} for edge in combinations(range(8), 2)}
    for coordinate, polynomial in coordinates.items():
        left, right, left_colour, right_colour = coordinate
        blocks[left, right][left_colour, right_colour] = polynomial

    def matrix(left, right):
        if left < right:
            return blocks[left, right]
        return {
            (right_colour, left_colour): polynomial
            for (left_colour, right_colour), polynomial
            in blocks[right, left].items()
        }

    cap = TERMINAL.SELECTED_CAP
    p, q = TERMINAL.SELECTED_ENDPOINTS
    residual = tuple(vertex for vertex in range(8) if vertex not in (p, q))

    scalar = {}
    for (left_colour, right_colour), polynomial in matrix(p, q).items():
        scalar = add(
            scalar,
            scale(polynomial, cap[left_colour][right_colour]),
        )

    direct = {}
    response = {}
    for position, left in enumerate(residual):
        for right in residual[position + 1:]:
            direct[left, right] = matrix(left, right)
            output = {}
            for (p_colour, left_colour), first in matrix(p, left).items():
                for (q_colour, right_colour), second in matrix(q, right).items():
                    key = (left_colour, right_colour)
                    output[key] = add(
                        output.get(key, {}),
                        scale(multiply(first, second), cap[p_colour][q_colour]),
                    )
            for (p_colour, right_colour), first in matrix(p, right).items():
                for (q_colour, left_colour), second in matrix(q, left).items():
                    key = (left_colour, right_colour)
                    output[key] = add(
                        output.get(key, {}),
                        scale(multiply(first, second), cap[p_colour][q_colour]),
                    )
            response[left, right] = output

    zero = {}
    errors = {}
    for word in product(range(3), repeat=6):
        colour = dict(zip(residual, word))
        coefficient = {}
        for matching in TERMINAL.perfect_matchings(residual):
            coefficient = add(coefficient, product_polynomials(
                response[edge].get(
                    (colour[edge[0]], colour[edge[1]]), zero
                )
                for edge in matching
            ))
            for direct_edge in matching:
                left, right = direct_edge
                coefficient = add(coefficient, product_polynomials((
                    scalar,
                    direct[direct_edge].get(
                        (colour[left], colour[right]), zero
                    ),
                    *(response[edge].get(
                        (colour[edge[0]], colour[edge[1]]), zero
                    ) for edge in matching if edge != direct_edge),
                )))
        if coefficient:
            errors[word] = coefficient
    return scalar, errors


def monomial_text(monomial):
    return [list(D5.COORDINATES[variable_id]) for variable_id in monomial]


def polynomial_text(polynomial):
    return [
        [monomial_text(monomial), coefficient]
        for monomial, coefficient in sorted(polynomial.items())
    ]


def laurent_quotient(numerator, denominator):
    """Return coefficient and positive/negative monomial parts for one term."""
    require(len(numerator) == len(denominator) == 1,
            "Laurent quotient requested outside a monomial packet")
    numerator_monomial, numerator_coefficient = next(iter(numerator.items()))
    denominator_monomial, denominator_coefficient = next(
        iter(denominator.items())
    )
    numerator_counts = Counter(numerator_monomial)
    denominator_counts = Counter(denominator_monomial)
    common = numerator_counts & denominator_counts
    numerator_counts -= common
    denominator_counts -= common
    return (
        numerator_coefficient,
        denominator_coefficient,
        bytes(sorted(numerator_counts.elements())),
        bytes(sorted(denominator_counts.elements())),
    )


def audit():
    coordinates = restricted_coordinates()
    spoke_id = D5.COORDINATE_ID[TERMINAL.PERTURBING_SPOKE]
    terminal_ids = tuple(TERMINAL.SELECTED_ROW)
    terminal_monomial = bytes(sorted(terminal_ids))
    require(spoke_id == 9, "perturbing-spoke variable id changed")
    require(spoke_id not in terminal_monomial,
            "terminal monomial started recording the off-path spoke")

    # Find every mixed source equation which sees the one-spoke direction.
    spoke_visible = {}
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        normalized = normalize_support(restricted_hafnian(word, coordinates))
        if any(spoke_id in monomial for monomial in normalized):
            spoke_visible[word] = normalized
    expected_visible = {
        (0, 1, 0, 0, 0, 0, 1, 0): {bytes((9, 234)): 1},
        BOUNDARY_WORD: {bytes((9,)): 1},
        (0, 2, 0, 0, 0, 2, 2, 2): {bytes((9, 116)): 1},
        (0, 2, 0, 1, 2, 0, 1, 0): {bytes((9, 184, 234)): 1},
        (0, 2, 0, 1, 2, 1, 1, 1): {bytes((9, 184)): 1},
    }
    require(spoke_visible == expected_visible,
            "the source equations seeing x_02^{00} changed")
    full_boundary = restricted_hafnian(BOUNDARY_WORD, coordinates)
    boundary = spoke_visible[BOUNDARY_WORD]
    require(boundary == variable(spoke_id),
            "H_01000111 stopped being the exposed-spoke coordinate")
    require(full_boundary == {
        bytes((9, 103, 162, 238)): 1
    }, "the unnormalized source-boundary monomial changed")

    scalar, full_errors = polynomial_cap_error(coordinates)
    normalized_scalar = normalize_support(scalar)
    normalized_errors = {
        word: normalize_support(polynomial)
        for word, polynomial in full_errors.items()
        if normalize_support(polynomial)
    }
    expected_errors = {
        ERROR_WORDS[0]: {bytes((9, 117, 234)): 2},
        ERROR_WORDS[1]: {bytes((9, 117)): 2},
        ERROR_WORDS[2]: {bytes((9, 234)): 2},
        ERROR_WORDS[3]: {bytes((9,)): 2},
    }
    require(normalized_scalar == {b"": -1},
            "selected direct cap scalar changed")
    require(normalized_errors == expected_errors,
            "the symbolic one-spoke cap-error packet changed")
    require(set(full_errors) == set(ERROR_WORDS),
            "an extra unnormalized error entered the coordinate face")

    # Before normalizing the chart support, each error is a Laurent monomial
    # multiple of the actual mixed source generator.  Every denominator is a
    # chart-support coordinate, so this is source-ideal membership on the
    # localized chart, not a numerical identity at one point.
    laurent_multipliers = {
        word: laurent_quotient(full_errors[word], full_boundary)
        for word in ERROR_WORDS
    }
    require(all(
        numerator_coefficient == 2
        and denominator_coefficient == 1
        and set(denominator_monomial).issubset(D5.SUPPORT_IDS)
        for (numerator_coefficient, denominator_coefficient,
             _numerator_monomial, denominator_monomial)
        in laurent_multipliers.values()
    ), "the correction stopped being a chart-Laurent source boundary")

    # This is the literal first augmented correction on the face.  It has
    # one source-labelled input and four physical target outputs.
    correction_multipliers = {
        ERROR_WORDS[0]: {bytes((117, 234)): 2},
        ERROR_WORDS[1]: {bytes((117,)): 2},
        ERROR_WORDS[2]: {bytes((234,)): 2},
        ERROR_WORDS[3]: {b"": 2},
    }
    corrections = {
        word: multiply(multiplier, boundary)
        for word, multiplier in correction_multipliers.items()
    }
    require(corrections == normalized_errors,
            "one mixed source boundary no longer cancels the cap error")

    # Literal rank-one realization of the first HPL readout correction.
    # In the free module with d0(u)=v, delta(x)=boundary*v and h(v)=u,
    # I(x)=x-boundary*u is a cycle.  Give x the naive physical error and u
    # the four-output multiplier packet.  Then aI=0 coefficientwise.
    hpl_naive = normalized_errors
    hpl_first_correction = corrections
    hpl_corrected = {
        word: add(hpl_naive.get(word, {}),
                  scale(hpl_first_correction.get(word, {}), -1))
        for word in set(hpl_naive) | set(hpl_first_correction)
    }
    hpl_corrected = {
        word: polynomial for word, polynomial in hpl_corrected.items()
        if polynomial
    }
    require(not hpl_corrected,
            "the local -a h delta i correction did not kill the readout")
    require(multiply(boundary, {b"": 1})
            == multiply({b"": 1}, boundary),
            "local HPL module lost commutativity")

    # Zero source scalars cannot suffice: specialize the seven terminal
    # variables to one.  The terminal monomial and cap activity are unchanged
    # between t=0 and t=1, while all four physical errors change 0 -> 2.
    def specialize(polynomial, spoke_value):
        value = 0
        for monomial, coefficient in polynomial.items():
            value += coefficient * (spoke_value ** monomial.count(spoke_id))
        return value

    error_at_zero = {
        "".join(map(str, word)): specialize(polynomial, 0)
        for word, polynomial in normalized_errors.items()
    }
    error_at_one = {
        "".join(map(str, word)): specialize(polynomial, 1)
        for word, polynomial in normalized_errors.items()
    }
    require(set(error_at_zero.values()) == {0}
            and set(error_at_one.values()) == {2},
            "minimality specialization changed")

    ledger = {
        "terminal_row": TERMINAL.SELECTED_ROW.hex(),
        "terminal_endpoints": list(TERMINAL.SELECTED_ENDPOINTS),
        "perturbing_spoke": list(TERMINAL.PERTURBING_SPOKE),
        "perturbing_spoke_id": spoke_id,
        "source_equations_seeing_spoke": {
            "".join(map(str, word)): polynomial_text(polynomial)
            for word, polynomial in sorted(spoke_visible.items())
        },
        "minimal_boundary_word": "".join(map(str, BOUNDARY_WORD)),
        "minimal_boundary": polynomial_text(boundary),
        "unnormalized_boundary": polynomial_text(full_boundary),
        "normalized_cap_scalar": polynomial_text(normalized_scalar),
        "normalized_error_packet": {
            "".join(map(str, word)): polynomial_text(polynomial)
            for word, polynomial in sorted(normalized_errors.items())
        },
        "correction_multipliers": {
            "".join(map(str, word)): polynomial_text(polynomial)
            for word, polynomial in sorted(correction_multipliers.items())
        },
        "unnormalized_laurent_multipliers": {
            "".join(map(str, word)): {
                "numerator_coefficient": data[0],
                "denominator_coefficient": data[1],
                "numerator_monomial": monomial_text(data[2]),
                "denominator_support_monomial": monomial_text(data[3]),
            }
            for word, data in sorted(laurent_multipliers.items())
        },
        "local_hpl_realization": {
            "d0": "u->v",
            "delta": "x->H_01000111*v",
            "homotopy": "v->u",
            "perturbed_inclusion": "I(x)=x-H_01000111*u",
            "naive_error_outputs": len(hpl_naive),
            "corrected_error_outputs": len(hpl_corrected),
        },
        "source_scalars_needed": 1,
        "zero_scalar_no_go": {
            "error_at_spoke_0": error_at_zero,
            "error_at_spoke_1": error_at_one,
        },
        "conclusion": (
            "on the selected coordinate face, the first augmented HPL "
            "correction is the four-output monomial map applied to the "
            "single mixed source boundary H_01000111=x_02^{00}"
        ),
        "scope_guard": (
            "exact only in the quotient by off-face coordinates and after "
            "chart-support normalization; no uniform hafnian contraction "
            "or simultaneous-spoke theorem is asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":"), default=str
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen augmented-terminal ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print(
        "n=8 chart26 augmented terminal chain: PASS; "
        "one source scalar cancels four errors"
    )
    print(json.dumps(ledger, sort_keys=True, default=str))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
