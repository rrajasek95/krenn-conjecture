#!/usr/bin/env python3
"""Resolve the generic-L P5 bends and the component-local H0 degree nine."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NEXT = load_module(
    "n8_p5_component_next_pure_for_generic_L",
    "verify_n8_p5_component_local_next_pure.py",
)
COMPONENT = NEXT.COMPONENT
DEG8 = COMPONENT.DEG8
COMPAT = COMPONENT.COMPAT
PURE = NEXT.PURE
P5 = NEXT.P5
CUBIC = NEXT.CUBIC
QQ = Fraction

FIRST_BEND = 56
SECOND_BEND = 57
EXPECTED_LEDGER_SHA256 = (
    "736ee026e09a4ae5497d27d3affe757f77fa96ff810b9fb7d7e3a89ab08e63c1"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def polynomial_digest(source):
    encoded = [
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(source.items())
    ]
    return sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def constant(value):
    return {(): QQ(value)} if value else {}


def negate(source):
    return {monomial: -coefficient for monomial, coefficient in source.items()}


def transverse_solution(residual, jacobian, detail):
    correction = {}
    for coordinate, row in zip(P5.P5_NORMAL_VARIABLES, P5.B_PIVOT_ROWS):
        incoming = residual[row]
        if incoming:
            correction[coordinate] = negate(COMPAT.divide_by_b(incoming))
    compatibility = COMPONENT.normalized_compatibility(residual, jacobian)
    image = P5.jacobian_times(jacobian, correction)
    check = [dict(value) for value in residual]
    for equation in range(39):
        add(check[equation], image[equation])
        require(check[equation] == compatibility[equation],
                f"{detail}: transverse reconstruction failed at Q{equation + 1}")
    return correction, compatibility


def compatibility_numerators(residual, jacobian):
    b = P5.polynomial((((44,), 1), ((45,), 1)))
    pivots = [residual[row] for row in P5.B_PIVOT_ROWS]
    answer = []
    for equation, row in enumerate(jacobian):
        value = multiply(b, residual[equation])
        for column in range(11):
            if row[column] and pivots[column]:
                add(value, multiply(row[column], pivots[column]), -1)
        answer.append(value)
    return answer


def reduce_L(source):
    quotient, remainder = PURE.divide_by_ell_with_remainder(source)
    reconstruction = multiply(quotient, PURE.ELL)
    add(reconstruction, remainder)
    require(reconstruction == source, "L reduction failed to reconstruct")
    return remainder


def nonzero_L_remainders(sources):
    return [
        (index + 1, reduce_L(source))
        for index, source in enumerate(sources)
        if reduce_L(source)
    ]


def singular_membership(
    order5, order6, first_relation, second_relations, h0_prior, h0_next
):
    names = [f"z{index}" for index in range(58)]
    ring_order = [names[SECOND_BEND], names[FIRST_BEND], "w", "q"] + names[:56]
    lines = [f"ring r=0,({','.join(ring_order)}),dp;"]
    for order, values in ((5, order5), (6, order6)):
        for equation, source in values:
            encoded = COMPAT.AMBIENT.singular_polynomial(source, names)
            lines.append(f"poly e{order}_{equation}={encoded};")
    encoded_first = COMPAT.AMBIENT.singular_polynomial(first_relation, names)
    encoded_r30 = COMPAT.AMBIENT.singular_polynomial(
        second_relations[0], names
    )
    encoded_r33 = COMPAT.AMBIENT.singular_polynomial(
        second_relations[1], names
    )
    encoded_prior = COMPAT.AMBIENT.singular_polynomial(h0_prior, names)
    encoded_next = COMPAT.AMBIENT.singular_polynomial(h0_next, names)
    lines.extend((
        "poly ell=z9*z25-z11*z46;",
        f"poly first={encoded_first};",
        f"poly second30={encoded_r30};",
        f"poly second33={encoded_r33};",
        f"poly h0prior={encoded_prior};",
        f"poly h0next={encoded_next};",
        "poly loc11=z11*w-1;",
        "poly locb=(z44+z45)*q-1;",
        "poly second=q*(second30-second33);",
        "ideal i=ell,first,second,loc11,locb;",
        "ideal g=std(i);",
        '"UNIT",(reduce(1,g)==0);',
        '"SECOND30",(reduce(second30,g)==0);',
        '"SECOND33",(reduce(second33,g)==0);',
        '"H0PRIOR",size(reduce(h0prior,g)),(reduce(h0prior,g)==0);',
        '"H0NEXT",size(reduce(h0next,g)),(reduce(h0next,g)==0);',
    ))
    for order, values in ((5, order5), (6, order6)):
        for equation, _source in values:
            lines.append(
                f'"COMPAT",{order},{equation},(reduce(e{order}_{equation},g)==0);'
            )
    lines.append("quit;")
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=180,
    )
    require(completed.returncode == 0, "Singular generic-L membership failed")
    print(completed.stdout)
    require("UNIT 0" in completed.stdout,
            "localized generic-L ideal became the unit ideal")
    require("SECOND30 1" in completed.stdout
            and "SECOND33 1" in completed.stdout,
            "second-bend pair did not collapse to one localized relation")
    require("H0PRIOR 0 1" in completed.stdout,
            "H0 degree-eight did not reduce to zero")
    require("H0NEXT 0 1" in completed.stdout,
            "H0 degree-nine did not reduce to zero")
    require(" 0" not in "\n".join(
        line for line in completed.stdout.splitlines()
        if line.startswith("COMPAT ")
    ), "a compatibility generator escaped the localized ideal")
    return completed.stdout


def scaled(source, coefficient):
    return {
        monomial: coefficient * value
        for monomial, value in source.items()
        if coefficient * value
    }


def divided_monomial(source, divisor):
    return PURE.divide_by_monomial(source, divisor)


def symbolic_lift_data():
    degree8 = DEG8.degree_eight_tail_data()
    compatibility = COMPAT.compatibility_tail_data(
        False, degree8["degree_seven_data"]
    )
    parts = compatibility["parts"]
    jacobian = compatibility["jacobian"]

    c1 = {
        coordinate: dict(value)
        for coordinate, value in compatibility["corrections"][0].items()
    }
    c1[46] = P5.monomial(FIRST_BEND)
    corrections = [c1]

    residual2 = P5.strict_residual(parts, corrections, 2)
    c2, compatibility2 = transverse_solution(residual2, jacobian, "order two")
    require(not any(compatibility2), "order-two compatibility returned")
    c2[46] = P5.monomial(SECOND_BEND)
    corrections.append(c2)

    residual3 = P5.strict_residual(parts, corrections, 3)
    c3, compatibility3 = transverse_solution(residual3, jacobian, "order three")
    require(not any(compatibility3), "order-three compatibility returned")
    corrections.append(c3)

    residual4 = P5.strict_residual(parts, corrections, 4)
    for equation in range(39):
        add(
            residual4[equation],
            degree8["degree_seven_data"]["degree_six"][equation],
        )
    c4, compatibility4 = transverse_solution(residual4, jacobian, "order four")
    compatibility4_L = nonzero_L_remainders(compatibility4)
    require(not compatibility4_L, "order-four compatibility survived L")
    corrections.append(c4)

    strict = COMPONENT.StrictJetProjector(
        degree8["second_projector"], corrections[:2]
    )
    higher_five = []
    higher_six = []
    series = degree8["degree_seven_data"]["series"]
    for number in range(1, 40):
        five, six = strict.higher_strict_orders(series._state(number))
        higher_five.append(five)
        higher_six.append(six)

    residual5 = P5.strict_residual(parts, corrections, 5)
    for equation in range(39):
        add(residual5[equation], higher_five[equation])
    c5, compatibility5 = transverse_solution(residual5, jacobian, "order five")
    compatibility5_L = nonzero_L_remainders(compatibility5)
    corrections.append(c5)

    residual6 = P5.strict_residual(parts, corrections, 6)
    for equation in range(39):
        add(residual6[equation], higher_six[equation])
    compatibility6 = compatibility_numerators(residual6, jacobian)
    compatibility6_L = nonzero_L_remainders(compatibility6)

    return {
        "degree8": degree8,
        "compatibility": compatibility,
        "corrections": corrections,
        "strict": strict,
        "compatibility4_L": compatibility4_L,
        "compatibility5_L": compatibility5_L,
        "compatibility6_L": compatibility6_L,
    }


def audit():
    data = symbolic_lift_data()
    for order in (5, 6):
        values = data[f"compatibility{order}_L"]
        print(f"ORDER {order} L REMAINDERS", [
            (index, len(value), polynomial_digest(value))
            for index, value in values
        ])
    order5 = dict(data["compatibility5_L"])
    order6 = dict(data["compatibility6_L"])
    first_relation = P5.polynomial((
        ((9, 29, 44), -1),
        ((0, 11, 46), 1),
        ((11, 24, 46), -1),
        ((11, 26, 54), 1),
        ((FIRST_BEND, 11), 1),
    ))
    u = P5.polynomial((((26,), 1), ((45,), 1)))
    v = P5.polynomial((((26,), 1), ((44,), -1)))
    common5 = P5.monomial(16, 16, 41, coefficient=QQ(1, 2))
    require(order5[30] == multiply(multiply(common5, u), first_relation),
            "Q30 first-bend factorization changed")
    require(order5[33] == multiply(multiply(common5, v), first_relation),
            "Q33 first-bend factorization changed")

    # Each exceptional numerator contains b, represented by exact division
    # below after first removing the common monomial z16^2*z41.
    exceptional = []
    for equation in (30, 33):
        core = divided_monomial(order6[equation], (16, 16, 41))
        core = scaled(COMPAT.divide_by_b(core), 2)
        exceptional.append(core)

    h0, h0_pure, _terms, _quotients, _remainder = NEXT.h0_reducer()
    h0_strict = COMPONENT.StrictJetProjector(
        DEG8.SecondOrderProjector(
            DEG8.TAILS.FactorizedP5Projector(h0)
        ),
        data["corrections"][:2],
    )
    h0_prior, h0_next = NEXT.h0_next_coefficient(
        h0_strict, h0, h0_pure
    )
    h0_prior_L = reduce_L(h0_prior)
    h0_next_L = reduce_L(h0_next)
    _singular_output = singular_membership(
        data["compatibility5_L"], data["compatibility6_L"],
        first_relation, exceptional, h0_prior_L, h0_next_L,
    )

    ledger = {
        "branch": "P5",
        "chart": "b=z44+z45 != 0",
        "first_bend_variable": "s=z46^(1)",
        "second_bend_variable": "t=z46^(2)",
        "order_five_L_remainders": [
            [index, len(value), polynomial_digest(value)]
            for index, value in data["compatibility5_L"]
        ],
        "order_six_L_remainders": [
            [index, len(value), polynomial_digest(value)]
            for index, value in data["compatibility6_L"]
        ],
        "first_bend_relation_terms": len(first_relation),
        "first_bend_relation_sha256": polynomial_digest(first_relation),
        "second_bend_relations": [
            [len(value), polynomial_digest(value)] for value in exceptional
        ],
        "H0_degree_eight_L_remainder_terms": len(h0_prior_L),
        "H0_degree_eight_L_remainder_sha256": polynomial_digest(h0_prior_L),
        "H0_degree_nine_L_remainder_terms": len(h0_next_L),
        "H0_degree_nine_L_remainder_sha256": polynomial_digest(h0_next_L),
        "localized_ideal_membership": {
            "localizers": ["z16", "z41", "z11", "b=z44+z45"],
            "compatibility_generators_reduce_to_zero": True,
            "second_bend_pair_reduces_to_one_relation": True,
            "ideal_is_nonunit": True,
            "H0_degree_eight_reduces_to_zero": True,
            "H0_degree_nine_reduces_to_zero": True,
        },
        "verdict": (
            "the generic L lift has no H0 survivor through degree nine"
        ),
        "scope_guard": (
            "finite-order formal-local result on the dense L chart with "
            "z16*z41*z11*(z44+z45) nonzero; not an all-orders membership proof"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L H0 ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
