#!/usr/bin/env python3
"""Certify the first P5 Jacobi cascade and rule out its naive 3x3 intertwiner."""

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


UNIFORM = load_module(
    "n8_p5_uniform_for_jacobi_cascade",
    "verify_n8_p5_newest_bend_uniform_coefficient.py",
)
G = UNIFORM.G
F2 = UNIFORM.F2
WARD = UNIFORM.WARD

EXPECTED_LEDGER_SHA256 = (
    "3577137dd710dfd15274c435c52be7b1ac207028b4847cb246a65b06e68135c4"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        WARD.add(answer, {tuple(sorted(monomial)): QQ(coefficient)})
    return answer


def multiply(*sources):
    answer = {(): QQ(1)}
    for source in sources:
        answer = WARD.multiply(answer, source)
    return answer


def add(*sources):
    answer = {}
    for source in sources:
        WARD.add(answer, source)
    return answer


def negate(source):
    return {monomial: -coefficient for monomial, coefficient in source.items()}


def variable(index):
    return {(index,): QQ(1)}


def response(graph, marker, variable_index, absolute_order):
    return UNIFORM.derivative(
        graph["series"][variable_index][absolute_order], marker
    )


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(WARD.polynomial_digest(source).encode())
    return digest.hexdigest()


def audit():
    base = F2.audit(return_data=True)
    graph = G.source_graph(base, maximum_order=7, additional_bends=1)
    marker = graph["bend_variables"][1]
    layout = base["layout"]
    a = layout["a"]
    y_variables = layout["y"]

    x = variable(a[10])
    y = variable(a[37])
    z = variable(a[40])
    x_plus_y = add(x, y)
    h2_xy = add(multiply(x, x), multiply(x, y), multiply(y, y))

    two_channel = []
    for pivot, endpoint in ((110, 25), (113, 26), (116, 27)):
        amplitude = multiply(variable(a[16]), variable(a[endpoint]))
        expected = (
            amplitude,
            negate(multiply(amplitude, x_plus_y)),
            multiply(amplitude, h2_xy),
        )
        actual = tuple(
            response(graph, marker, y_variables[pivot], order)
            for order in (5, 6, 7)
        )
        require(actual == expected,
                f"two-channel cascade changed at y{pivot}")
        two_channel.extend(actual)

    one_channel_amplitudes = {
        155: negate(multiply(add(variable(a[33]), variable(a[39])), z)),
        158: negate(multiply(add(variable(a[34]), variable(a[39])), z)),
        161: negate(multiply(variable(a[35]), z)),
        191: multiply(add(negate(variable(a[39])), z), z),
        197: negate(multiply(z, variable(a[43]))),
    }
    one_channel = []
    for pivot, amplitude in one_channel_amplitudes.items():
        expected = (
            amplitude,
            multiply(amplitude, z),
            multiply(amplitude, z, z),
        )
        actual = tuple(
            response(graph, marker, y_variables[pivot], order)
            for order in (5, 6, 7)
        )
        require(actual == expected,
                f"one-channel cascade changed at y{pivot}")
        one_channel.extend(actual)

    # The evident 3-state block is the 2-state companion for roots
    # -z10,-z37 together with the geometric z40 channel.  The desired W
    # companion has roots -z0,-z30,-z52.  The Sylvester resultant is the
    # product of all pairwise root differences and is manifestly nonzero.
    desired = ((0, a[0]), (30, a[30]), (52, a[52]))
    raw_negative = ((10, a[10]), (37, a[37]))
    resultant = {(): QQ(1)}
    resultant_factors = []
    for raw_label, raw in raw_negative:
        for target_label, target in desired:
            factor = polynomial((((target,), 1), ((raw,), -1)))
            resultant = multiply(resultant, factor)
            resultant_factors.append(f"z{target_label}-z{raw_label}")
    for target_label, target in desired:
        factor = polynomial((((a[40],), 1), ((target,), 1)))
        resultant = multiply(resultant, factor)
        resultant_factors.append(f"z40+z{target_label}")
    require(resultant,
            "raw/desired companion resultant vanished identically")

    ledger = {
        "marker": "r4=z46^(4)",
        "relative_orders": [1, 2, 3],
        "two_channel_block": {
            "pivots": [110, 113, 116],
            "roots": ["-z10", "-z37"],
            "recurrence": (
                "v_(n+2)=-(z10+z37)*v_(n+1)-z10*z37*v_n"
            ),
            "response_sha256": family_digest(two_channel),
        },
        "one_channel_block": {
            "pivots": [155, 158, 161, 191, 197],
            "root": "z40",
            "recurrence": "v_(n+1)=z40*v_n",
            "response_sha256": family_digest(one_channel),
        },
        "naive_raw_3state_characteristic": (
            "(lambda+z10)*(lambda+z37)*(lambda-z40)"
        ),
        "desired_W_characteristic": (
            "(lambda+z0)*(lambda+z30)*(lambda+z52)"
        ),
        "sylvester_resultant_factors": resultant_factors,
        "sylvester_resultant_terms": len(resultant),
        "sylvester_resultant_sha256": WARD.polynomial_digest(resultant),
        "direct_intertwiner_verdict": (
            "over the P5 rational function field the two characteristic "
            "polynomials are coprime, so P*A=C*P has only P=0 for this "
            "naive three-state block"
        ),
        "next_required_state": (
            "include the new relative-order-three Schur variables and the "
            "localized center/output projection before seeking an intertwiner"
        ),
        "scope_guard": (
            "rules out only the evident 2+1 raw cascade as the desired "
            "three-state transfer; it does not rule out a larger-state "
            "intertwiner or the rational full-Rees identity"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "Jacobi cascade counterguard ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
