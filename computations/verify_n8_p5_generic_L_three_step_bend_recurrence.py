#!/usr/bin/env python3
"""Test the next P5 bend equation by exact triangular localization.

The generic-L centre is monic successively in z46,s,t,r3,r4 after
localizing z11 and b.  Direct substitution therefore computes the exact
localized normal form without materializing the large Groebner basis.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SPAIR = load_module(
    "n8_p5_spair_for_three_step_recurrence",
    "analyze_n8_p5_generic_L_r5_nakayama_s_pair.py",
)
G = SPAIR.G
F2 = SPAIR.F2
NAK = SPAIR.NAK
REES = SPAIR.REES
EXPECTED_LEDGER_SHA256 = (
    "6070cd95bdaa51bc6610df37a4f6748a8e98c63f21e20412152c0f7e4856b0ac"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def normalize_monomial(monomial, inverse_pairs):
    output = list(monomial)
    for variable, inverse in inverse_pairs:
        cancellations = min(output.count(variable), output.count(inverse))
        for _index in range(cancellations):
            output.remove(variable)
            output.remove(inverse)
    return tuple(sorted(output))


def add(target, source, inverse_pairs, scale=QQ(1)):
    for monomial, coefficient in source.items():
        output = normalize_monomial(monomial, inverse_pairs)
        value = target.get(output, QQ(0)) + scale * coefficient
        if value:
            target[output] = value
        else:
            target.pop(output, None)


def multiply(left, right, inverse_pairs):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            add(answer, {
                left_monomial + right_monomial:
                left_coefficient * right_coefficient
            }, inverse_pairs)
    return answer


def substitute(source, variable, replacement, inverse_pairs):
    maximum = max(
        (monomial.count(variable) for monomial in source), default=0
    )
    powers = [{(): QQ(1)}]
    for _degree in range(maximum):
        powers.append(multiply(powers[-1], replacement, inverse_pairs))
    answer = {}
    for monomial, coefficient in source.items():
        degree = monomial.count(variable)
        base = list(monomial)
        for _index in range(degree):
            base.remove(variable)
        term = multiply(
            {tuple(base): coefficient}, powers[degree], inverse_pairs
        )
        add(answer, term, inverse_pairs)
    return answer


def variable_coefficient(source, variable, inverse_pairs):
    answer = {}
    for monomial, coefficient in source.items():
        degree = monomial.count(variable)
        require(degree <= 1, "triangular centre stopped being affine")
        if not degree:
            continue
        output = list(monomial)
        output.remove(variable)
        add(answer, {tuple(output): coefficient}, inverse_pairs)
    return answer


def solve_affine(relation, variable, inverse_coefficient, inverse_pairs):
    coefficient = variable_coefficient(
        relation, variable, inverse_pairs
    )
    require(
        multiply(coefficient, inverse_coefficient, inverse_pairs)
        == {(): QQ(1)},
        "declared centre coefficient inverse changed",
    )
    constant = {
        monomial: value for monomial, value in relation.items()
        if variable not in monomial
    }
    replacement = multiply(
        constant, inverse_coefficient, inverse_pairs
    )
    return {monomial: -value for monomial, value in replacement.items()}


def polynomial(entries, inverse_pairs):
    answer = {}
    for monomial, coefficient in entries:
        add(answer, {tuple(monomial): QQ(coefficient)}, inverse_pairs)
    return answer


def triangular_replacements(base, graph, relations, inverse_z11):
    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    q = graph["inverse_b"]
    inverse_pairs = ((b, q), (a[11], inverse_z11))
    z46 = a[46]
    s = base["first_bend"]
    t = base["second_bend"]
    r3, r4, _r5 = graph["bend_variables"]
    variables = (z46, s, t, r3, r4)
    inverses = (
        {(inverse_z11,): QQ(-1)},
        {(inverse_z11,): QQ(1)},
        {tuple(sorted((inverse_z11, q))): QQ(1)},
        {(): QQ(-1)},
        {(): QQ(1)},
    )

    ell, first, second, grow = relations
    w4 = polynomial((
        ((s, a[0], a[30], a[52]), 1),
        ((t, a[0], a[30]), 1),
        ((t, a[0], a[52]), 1),
        ((t, a[30], a[52]), 1),
        ((r3, a[0]), 1),
        ((r3, a[30]), 1),
        ((r3, a[52]), 1),
        ((r4,), 1),
    ), inverse_pairs)
    source_relations = (ell, first, second, grow, w4)
    replacements = []
    term_profile = []
    for variable, relation, inverse in zip(
        variables, source_relations, inverses
    ):
        for old_variable, replacement in replacements:
            relation = substitute(
                relation, old_variable, replacement, inverse_pairs
            )
        replacement = solve_affine(
            relation, variable, inverse, inverse_pairs
        )
        replacements.append((variable, replacement))
        term_profile.append(len(replacement))
    return inverse_pairs, replacements, w4, term_profile


def reduce_triangular(source, replacements, inverse_pairs):
    profile = [len(source)]
    for variable, replacement in replacements:
        source = substitute(source, variable, replacement, inverse_pairs)
        profile.append(len(source))
    return source, profile


def audit():
    base = F2.audit(return_data=True)
    graph = G.source_graph(base, maximum_order=8, additional_bends=2)
    relations = NAK.center_relations(base, graph)
    inverse_z11 = graph["inverse_b"] + 1
    inverse_pairs, replacements, w4, replacement_terms = (
        triangular_replacements(base, graph, relations, inverse_z11)
    )

    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    r3, r4, r5 = graph["bend_variables"]
    t = base["second_bend"]
    w5 = polynomial((
        ((t, a[0], a[30], a[52]), 1),
        ((r3, a[0], a[30]), 1),
        ((r3, a[0], a[52]), 1),
        ((r3, a[30], a[52]), 1),
        ((r4, a[0]), 1),
        ((r4, a[30]), 1),
        ((r4, a[52]), 1),
        ((r5,), 1),
    ), inverse_pairs)
    common = polynomial((
        ((a[11], a[16], a[16], a[41]), QQ(1, 2)),
    ), inverse_pairs)
    u = polynomial((
        ((a[26],), 1), ((b,), 1), ((a[44],), -1),
    ), inverse_pairs)
    v = polynomial((
        ((a[26],), 1), ((a[44],), -1),
    ), inverse_pairs)

    expected30 = multiply(multiply(common, u, inverse_pairs), w5,
                          inverse_pairs)
    expected33 = multiply(multiply(common, v, inverse_pairs), w5,
                          inverse_pairs)
    q8 = graph["compatibility_orders"][7]
    differences = []
    profiles = []
    for row, expected in ((29, expected30), (32, expected33)):
        difference = dict(q8[row])
        add(difference, expected, inverse_pairs, QQ(-1))
        remainder, profile = reduce_triangular(
            difference, replacements, inverse_pairs
        )
        differences.append(remainder)
        profiles.append(profile)

    require(not differences[0] and not differences[1],
            "Q8 failed the three-step bend recurrence")
    ledger = {
        "chart": "post-207 localized generic L/F1/F2/G/W4",
        "triangular_variables": ["z46", "s", "t", "r3", "r4"],
        "inverse_pairs": ["b*q=1", "z11*w=1"],
        "replacement_term_counts": replacement_terms,
        "W4": "r4+e1*r3+e2*t+e3*s",
        "W5": "r5+e1*r4+e2*r3+e3*t",
        "elementary_variables": ["z0", "z30", "z52"],
        "Q8_factorization": {
            "M30": "(1/2)*z11*z16^2*z41*(z26+b-z44)*W5",
            "M33": "(1/2)*z11*z16^2*z41*(z26-z44)*W5",
        },
        "difference_term_profiles": {
            "M30": profiles[0],
            "M33": profiles[1],
        },
        "remainders_zero": [not source for source in differences],
        "Q8_total_terms": sum(map(len, q8)),
        "Q8_family_sha256": sha256("".join(
            REES.polynomial_digest(source) for source in q8
        ).encode()).hexdigest(),
        "scope_guard": (
            "exact Q8 recurrence in the localized triangular quotient; "
            "the generating-function/all-order recurrence remains to prove"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            "three-step bend recurrence ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
