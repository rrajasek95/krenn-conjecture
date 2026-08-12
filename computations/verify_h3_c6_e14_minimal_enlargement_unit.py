#!/usr/bin/env python3
"""The minimal response-silent E14 enlargement preserves a two-row unit.

Start with the rational silent-C6 q00 fibre and one selected pure-11 and
pure-22 tail as in 7320475.  Adjoin all decorated cells used by the E14 pair
Q3+Q6 at z=012111, giving arbitrary formal coefficients to cells not already
selected.  Allow all p1/s1 components on core sites 0,1,3,4.

For each of the three X1 tails, the complete pure target coefficient and a
literal mixed zero coefficient have identical endpoint polynomials.  The
identity holds coefficientwise in every new E14 cell parameter.  Hence the
minimal E14 enlargement is still an ordinary two-row unit.  Any full-source
survivor needs an asymmetric internal q tail or an endpoint outside the core.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B4_PATH = "computations/verify_h3_silent_c6_complete_response_mate_boundary.py"
PINS = {
    B4_PATH:
        "4f4a54d210b21da1183fe2fbfbb4441cec2388111b8c9e2d966a47e1d8fdcb7d",
    "notes/h3-silent-c6-complete-response-mate-boundary.md":
        "6c2dc1826d0e9be6b01081c2b84c535f30a5a427ae9a2225f490fdd2fc9bb22e",
    "computations/verify_h3_silent_c6_full_core_port_unit.py":
        "2b757f57d92722363f340b2a6105b82e091fc083726e1277569056e8a2ddf56a",
    "notes/h3-silent-c6-full-core-port-unit.md":
        "b16c29d16133e1c00cf58b8ee9305a9c53044fd127b3146b709728275157ff08",
    "computations/verify_h3_c6_degenerate_pair_transport_guard.py":
        "565b4622ca4b57904472ffa360f41e5ee330736501bdbd4990ad01985b38a080",
    "notes/h3-c6-degenerate-pair-transport-guard.md":
        "1b297d4fdaa244adb65e36dfce52d86d86b9553774586bb942a67632caaa46b6",
    "computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py":
        "59dd21c4664e8ccd88f771d0191d3db32e5fdb832e2c6de1f169cb197f9a3038",
    "notes/uniform-hall-k22-outside-endpoint-component-wedge.md":
        "cd3807d8f3f4f3d8ccda38e23c5ff291d3f0e3f1a33b69f3d2ef061b117d3347",
}
EXPECTED_LEDGER_SHA256 = (
    "a2d72f4ceadab5e0327c39f0f222c498fc8b54b3832eb7066d1caf796fd67f4a"
)
CORE = (0, 1, 3, 4)
ONE = ()
E14_CELLS = (
    ((0, 2), (0, 2), "u02_02"),
    ((3, 5), (1, 1), "u35_11"),
    ((0, 5), (0, 1), "u05_01"),
    ((2, 3), (2, 1), "u23_21"),
    ((1, 4), (1, 1), "u14_11"),
)
ZERO_WORD = {
    1: (1, 1, 1, 1, 0, 0),
    2: (1, 1, 1, 0, 1, 0),
    3: (1, 1, 0, 1, 1, 0),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def add(left, right):
    answer = defaultdict(Q, left)
    for monomial, coefficient in right.items():
        answer[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def multiply(left, right):
    answer = defaultdict(Q)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def variable(name):
    return {(name,): Q(1)}


def q_inventory(b4, first_index, second_index):
    q_cells = {
        physical: {(0, 0): {ONE: value}}
        for physical, value in b4.Q00_WEIGHTS.items()
    }
    for colour, tail in (
            (1, b4.BRIGHT_TAILS[1][first_index - 1]),
            (2, b4.BRIGHT_TAILS[2][second_index - 1])):
        for physical in tail:
            q_cells.setdefault(physical, {})[(colour, colour)] = {ONE: Q(1)}

    added = []
    already_selected = []
    for physical, decoration, parameter in E14_CELLS:
        cells = q_cells.setdefault(physical, {})
        if decoration in cells:
            already_selected.append((physical, decoration))
        else:
            cells[decoration] = variable(parameter)
            added.append((physical, decoration, parameter))
    return q_cells, tuple(added), tuple(already_selected)


def response_11(b4, q_cells):
    """Every complete G11 coefficient over arbitrary core endpoint entries."""
    output = defaultdict(lambda: defaultdict(dict))
    for p_site in CORE:
        for s_site in CORE:
            if p_site == s_site:
                continue
            remaining = tuple(site for site in range(6)
                              if site not in (p_site, s_site))
            for tail in b4.perfect_matchings(remaining):
                choices = [q_cells.get(physical, {}) for physical in tail]
                if any(not options for options in choices):
                    continue
                for decorations in product(*[tuple(options) for options
                                              in choices]):
                    q_coefficient = {ONE: Q(1)}
                    for physical, decoration in zip(
                            tail, decorations, strict=True):
                        q_coefficient = multiply(
                            q_coefficient, q_cells[physical][decoration]
                        )
                    for p_colour in range(3):
                        for s_colour in range(3):
                            word = [None] * 6
                            word[p_site] = p_colour
                            word[s_site] = s_colour
                            for physical, decoration in zip(
                                    tail, decorations, strict=True):
                                word[physical[0]], word[physical[1]] = decoration
                            endpoint_monomial = (
                                f"p1_{p_site}_{p_colour}",
                                f"s1_{s_site}_{s_colour}",
                            )
                            old = output[tuple(word)].get(
                                endpoint_monomial, {}
                            )
                            output[tuple(word)][endpoint_monomial] = add(
                                old, q_coefficient
                            )
    return {
        word: {endpoint: coefficient for endpoint, coefficient in row.items()
               if coefficient}
        for word, row in output.items() if any(row.values())
    }


def polynomial_json(polynomial):
    return [
        [list(endpoint), [
            [list(q_monomial), str(coefficient)]
            for q_monomial, coefficient in sorted(q_polynomial.items())
        ]]
        for endpoint, q_polynomial in sorted(polynomial.items())
    ]


def audit_chart(b4, first_index, second_index):
    q_cells, added, selected = q_inventory(b4, first_index, second_index)
    rows = response_11(b4, q_cells)
    target_word = (1,) * 6
    zero_word = ZERO_WORD[first_index]
    target = rows[target_word]
    zero = rows[zero_word]
    require(target == zero,
            f"chart {(first_index, second_index)} lost its E14-stable unit")

    # The common polynomial is nonzero.  In the third X1 chart q14:11 adds
    # the same hole-03 endpoint bracket to both rows.  It cannot produce the
    # desired hole-14 endpoint product in either coefficient.
    selected_bracket = {
        ("p1_0_1", "s1_1_1"),
        ("p1_1_1", "s1_0_1"),
    }
    require(selected_bracket <= set(target),
            "the selected hole-01 endpoint bracket changed")
    desired_hole14 = {
        ("p1_1_1", "s1_4_1"),
        ("p1_4_1", "s1_1_1"),
    }
    require(not (desired_hole14 & set(target)),
            "the response-silent E14 tail unexpectedly gained hole 14")
    if first_index == 3:
        q14_bracket = {
            ("p1_0_1", "s1_3_1"),
            ("p1_3_1", "s1_0_1"),
        }
        require(q14_bracket <= set(target),
                "q14:11 lost its parallel hole-03 contamination")
        require(all(target[endpoint] == variable("u14_11")
                    for endpoint in q14_bracket),
                "the q14 parallel coefficient changed")
    else:
        require("u14_11" not in {
            variable_name
            for q_polynomial in target.values()
            for q_monomial in q_polynomial
            for variable_name in q_monomial
        }, "q14 contaminated the wrong bright chart")

    return {
        "X1_tail_index": first_index,
        "X2_tail_index": second_index,
        "target_word": "111111",
        "zero_word": "".join(map(str, zero_word)),
        "formal_E14_cells_added": [
            [list(physical), list(decoration), parameter]
            for physical, decoration, parameter in added
        ],
        "E14_cells_already_selected": [
            [list(physical), list(decoration)]
            for physical, decoration in selected
        ],
        "identical_complete_endpoint_polynomial": polynomial_json(target),
        "desired_hole14_products_present": False,
        "ordinary_source_identity": "F_zero-F_target=1",
    }


def audit():
    pin_dependencies()
    b4 = load(B4_PATH, "silent_c6_e14_b4")
    records = [
        audit_chart(b4, first_index, second_index)
        for first_index in (1, 2, 3)
        for second_index in (1, 2, 3)
    ]
    require(len(records) == 9, "the nine E14 bright charts changed")
    require({record["zero_word"] for record in records}
            == {"111100", "111010", "110110"},
            "the three E14-stable zero words changed")

    ledger = {
        "pins": PINS,
        "core_sites": CORE,
        "formal_E14_cell_family": [
            [list(physical), list(decoration), parameter]
            for physical, decoration, parameter in E14_CELLS
        ],
        "records": records,
        "outside_core_endpoint_sites": [2, 5],
        "outside_endpoint_route": (
            "by the pinned complete-column theorem, a zero outside column "
            "is exactly deletable and a nonzero one is a free active arm"
        ),
        "theorem": (
            "on the complete minimal silent-C6 core endpoint envelope, "
            "adjoining all cells in the response-silent E14 pair with "
            "arbitrary formal coefficients preserves an ordinary two-row "
            "unit in all nine bright charts.  Therefore E14 alone cannot "
            "be a full source and does not force a hole-14 endpoint product"
        ),
        "sharp_survivor": (
            "a full source must add either an endpoint component outside "
            "the core, which routes by exact deletion/free activity, or an "
            "additional internal decorated q tail that enters the target "
            "and zero coefficients asymmetrically.  The latter is the "
            "smallest remaining source-exhaustivity guard; rank landing is "
            "separate"
        ),
        "scope": (
            "coefficientwise polynomial identity on 7320475's exact rational "
            "q00 fibre plus one selected X1/X2 tail and the minimal E14 "
            "decorated cell family, with every core p1/s1 component.  It "
            "does not include a second asymmetric internal q tail"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"minimal E14 unit ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 C6 minimal E14 enlargement unit: PASS (exact)")
    print("nine bright charts: target and mixed-zero polynomials identical")
    print("E14 q14:11 contamination is parallel, not hole-14 endpoint access")
    print("survivor requires outside endpoint or second asymmetric q tail")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
