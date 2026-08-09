#!/usr/bin/env python3
"""Reduce H0 degree ten by symbolic generic-L strict-order-seven compatibility."""

from fractions import Fraction
from hashlib import sha256
import gc
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


POINT = load_module(
    "n8_p5_strict7_point_for_symbolic",
    "verify_n8_p5_generic_L_strict7_point.py",
)
GENERIC = POINT.GENERIC
THIRD = POINT.THIRD
P5 = POINT.P5
CUBIC = POINT.CUBIC
COMPAT = POINT.COMPAT
PURE = THIRD.PURE
QQ = Fraction

THIRD_BEND = POINT.THIRD_BEND
INVERSE_B = 59
EXPECTED_LEDGER_SHA256 = (
    "81d5dd346fe93b5b70f9db5bf1bfab4c499f8356c86efb5ab65eba30463adac0"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def polynomial_digest(source):
    return POINT.polynomial_digest(source)


def negate(source):
    return {monomial: -coefficient for monomial, coefficient in source.items()}


def restrict_zero(source, variable):
    return {
        monomial: coefficient
        for monomial, coefficient in source.items()
        if variable not in monomial
    }


def restrict_correction(correction, variable):
    return {
        coordinate: restricted
        for coordinate, source in correction.items()
        if (restricted := restrict_zero(source, variable))
    }


def strict_residual_row(parts, corrections, strict_order, equation):
    value = {}
    for degree in range(2, min(5, strict_order + 2) + 1):
        arc_order = strict_order - degree + 2
        add(value, P5.coefficient_on_p5_arc(
            parts[degree][equation], corrections, arc_order
        ))
    return value


def transverse_from_pivots(residuals, detail):
    correction = {}
    for coordinate, row in zip(P5.P5_NORMAL_VARIABLES, P5.B_PIVOT_ROWS):
        incoming = residuals[row]
        if incoming:
            correction[coordinate] = negate(COMPAT.divide_by_b(incoming))
    image = P5.jacobian_times(residuals["jacobian"], correction)
    for row in P5.B_PIVOT_ROWS:
        check = dict(residuals[row])
        add(check, image[row])
        require(not check, f"{detail}: pivot Q{row + 1} did not cancel")
    return correction


def transverse_localized_from_pivots(residuals, detail):
    inverse = P5.monomial(INVERSE_B)
    b = P5.polynomial((((44,), 1), ((45,), 1)))
    one_minus_inverse = P5.polynomial((((), 1),))
    add(one_minus_inverse, multiply(b, inverse), -1)
    correction = {}
    for coordinate, row in zip(P5.P5_NORMAL_VARIABLES, P5.B_PIVOT_ROWS):
        incoming = residuals[row]
        if incoming:
            correction[coordinate] = negate(multiply(incoming, inverse))
    image = P5.jacobian_times(residuals["jacobian"], correction)
    for row in P5.B_PIVOT_ROWS:
        check = dict(residuals[row])
        add(check, image[row])
        expected = multiply(residuals[row], one_minus_inverse)
        require(check == expected,
                f"{detail}: localized pivot Q{row + 1} did not cancel")
    return correction


def compatibility_row(residual, correction, jacobian_row):
    answer = dict(residual)
    for column, coordinate in enumerate(P5.P5_NORMAL_VARIABLES):
        if jacobian_row[column] and correction.get(coordinate):
            add(answer, multiply(
                jacobian_row[column], correction[coordinate]
            ))
    return answer


def old_relations(data):
    order5 = dict(data["compatibility5_L"])
    order6 = dict(data["compatibility6_L"])
    first = P5.polynomial((
        ((9, 29, 44), -1),
        ((0, 11, 46), 1),
        ((11, 24, 46), -1),
        ((11, 26, 54), 1),
        ((GENERIC.FIRST_BEND, 11), 1),
    ))
    u = P5.polynomial((((26,), 1), ((45,), 1)))
    v = P5.polynomial((((26,), 1), ((44,), -1)))
    common = P5.monomial(16, 16, 41, coefficient=QQ(1, 2))
    require(order5[30] == multiply(multiply(common, u), first),
            "generic-L Q30 first relation changed")
    require(order5[33] == multiply(multiply(common, v), first),
            "generic-L Q33 first relation changed")
    exceptional = []
    for equation in (30, 33):
        core = PURE.divide_by_monomial(order6[equation], (16, 16, 41))
        core = {
            monomial: 2 * coefficient
            for monomial, coefficient in COMPAT.divide_by_b(core).items()
        }
        exceptional.append(core)
    return first, exceptional


def strict7_common_factor():
    return P5.polynomial((
        ((0, 26, 30, 54), 1),
        ((26, 30, 30, 54), -1),
        ((0, 7, 46, 54), 1),
        ((7, 24, 46, 54), -1),
        ((7, 30, 46, 54), -1),
        ((0, 26, 52, 54), -1),
        ((26, 30, 52, 54), 1),
        ((7, 46, 52, 54), 1),
        ((7, 26, 54, 54), 1),
        ((GENERIC.FIRST_BEND, 0, 52), -1),
        ((GENERIC.FIRST_BEND, 7, 54), 1),
        ((GENERIC.SECOND_BEND, 0), -1),
        ((GENERIC.SECOND_BEND, 52), -1),
        ((THIRD_BEND,), -1),
    ))


def singular_reduction(first, exceptional, q30, q33, h0, common_factor):
    names = [f"z{index}" for index in range(60)]
    ring_order = [
        names[THIRD_BEND], names[GENERIC.SECOND_BEND],
        names[GENERIC.FIRST_BEND], names[INVERSE_B],
        "w", "p16", "p41",
    ] + names[:56]

    def encode(source):
        return COMPAT.AMBIENT.singular_polynomial(source, names)

    common_monomial = P5.monomial(11, 16, 16, 41)
    u = P5.polynomial((((26,), 1), ((45,), 1)))
    minus_v = P5.polynomial((((44,), 1), ((26,), -1)))
    b = P5.polynomial((((44,), 1), ((45,), 1)))
    delta = P5.polynomial((((53,), 1), ((51,), -1)))
    expected_q30 = multiply(multiply(common_monomial, u), common_factor)
    expected_q30 = {
        monomial: QQ(-1, 2) * coefficient
        for monomial, coefficient in expected_q30.items()
    }
    expected_q33 = multiply(
        multiply(common_monomial, minus_v), common_factor
    )
    expected_q33 = {
        monomial: QQ(1, 2) * coefficient
        for monomial, coefficient in expected_q33.items()
    }
    expected_h0 = multiply(
        multiply(multiply(common_monomial, b), delta), common_factor
    )

    lines = [
        f"ring r=0,({','.join(ring_order)}),dp;",
        "poly ell=z9*z25-z11*z46;",
        f"poly first={encode(first)};",
        f"poly second30={encode(exceptional[0])};",
        f"poly second33={encode(exceptional[1])};",
        f"poly q30={encode(q30)};",
        f"poly q33={encode(q33)};",
        f"poly h0={encode(h0)};",
        f"poly expectedq30={encode(expected_q30)};",
        f"poly expectedq33={encode(expected_q33)};",
        f"poly expectedh0={encode(expected_h0)};",
        "poly loc11=z11*w-1;",
        "poly locb=(z44+z45)*z59-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "poly second=z59*(second30-second33);",
        "ideal old=ell,first,second,loc11,locb,loc16,loc41;",
        "ideal gold=std(old);",
        "poly q30old=reduce(q30,gold);",
        "poly q33old=reduce(q33,gold);",
        "poly h0old=reduce(h0,gold);",
        '"OLDUNIT",(reduce(1,gold)==0);',
        '"Q30OLD",size(q30old),(q30old==0);',
        '"Q33OLD",size(q33old),(q33old==0);',
        '"H0OLD",size(h0old),(h0old==0);',
        '"Q30FORM",(q30old==expectedq30);',
        '"Q33FORM",(q33old==expectedq33);',
        '"H0FORM",(h0old==expectedh0);',
        '"Q30FACTOR",factorize(q30old);',
        '"Q33FACTOR",factorize(q33old);',
        '"H0FACTOR",factorize(h0old);',
        "ideal lifted=old,q30,q33;",
        "ideal glifted=std(lifted);",
        '"NEWUNIT",(reduce(1,glifted)==0);',
        '"H0NEW",size(reduce(h0,glifted)),(reduce(h0,glifted)==0);',
        "quit;",
    ]
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=600,
    )
    require(completed.returncode == 0,
            "Singular symbolic strict7 reduction failed")
    print(completed.stdout)
    require("OLDUNIT 0" in completed.stdout,
            "old generic-L ideal became unit")
    require("NEWUNIT 0" in completed.stdout,
            "strict7 generic-L ideal became unit")
    require("H0NEW 0 1" in completed.stdout,
            "H0 degree ten survived symbolic strict7 compatibility")
    require("Q30FORM 1" in completed.stdout
            and "Q33FORM 1" in completed.stdout
            and "H0FORM 1" in completed.stdout,
            "symbolic strict7 common-factor identities changed")
    output = {}
    for label in ("Q30OLD", "Q33OLD", "H0OLD", "H0NEW"):
        line = next(value for value in completed.stdout.splitlines()
                    if value.startswith(label + " "))
        output[label] = {
            "terms": int(line.split()[1]),
            "zero": line.endswith(" 1"),
        }
    require(not output["H0OLD"]["zero"],
            "H0 degree ten already vanished before strict7")
    require(not output["Q30OLD"]["zero"]
            and not output["Q33OLD"]["zero"],
            "strict7 exceptional pair vanished in old ideal")
    output["common_factor_identities"] = True
    return output


def audit():
    data = GENERIC.symbolic_lift_data()
    degree8 = data["degree8"]
    compatibility = data["compatibility"]
    parts = compatibility["parts"]
    jacobian = compatibility["jacobian"]
    first, exceptional = old_relations(data)

    c1 = {coordinate: dict(value)
          for coordinate, value in data["corrections"][0].items()}
    c2 = {coordinate: dict(value)
          for coordinate, value in data["corrections"][1].items()}
    c3 = {coordinate: dict(value)
          for coordinate, value in data["corrections"][2].items()}
    c3[46] = P5.monomial(THIRD_BEND)
    corrections = [c1, c2, c3]

    rows = set(P5.B_PIVOT_ROWS)
    series = degree8["degree_seven_data"]["series"]
    old_higher = {}
    for row in rows:
        old_higher[row] = data["strict"].higher_strict_orders(
            series._state(row + 1)
        )

    residual4 = {"jacobian": jacobian}
    for row in rows:
        value = strict_residual_row(parts, corrections, 4, row)
        add(value, degree8["degree_seven_data"]["degree_six"][row])
        residual4[row] = value
    c4 = transverse_from_pivots(residual4, "strict order four")
    require(restrict_correction(c4, THIRD_BEND) == data["corrections"][3],
            "third-bend c4 failed its zero-bend regression")
    corrections.append(c4)

    residual5 = {"jacobian": jacobian}
    for row in rows:
        value = strict_residual_row(parts, corrections, 5, row)
        add(value, old_higher[row][0])
        residual5[row] = value
    c5 = transverse_from_pivots(residual5, "strict order five")
    require(restrict_correction(c5, THIRD_BEND) == data["corrections"][4],
            "third-bend c5 failed its zero-bend regression")
    corrections.append(c5)

    residual6 = {"jacobian": jacobian}
    for row in rows:
        value = strict_residual_row(parts, corrections, 6, row)
        add(value, old_higher[row][1])
        residual6[row] = value
    c6 = transverse_localized_from_pivots(residual6, "strict order six")
    corrections.append(c6)
    del old_higher, residual4, residual5, residual6
    gc.collect()

    target_rows = sorted(rows | {29, 32})
    third = POINT.third_from_second(
        series.reducer, degree8["second_projector"]
    )
    require(not THIRD.validate_normal_graph(third),
            "symbolic strict7 third normal graph regression returned")
    strict = THIRD.ThirdStrictProjector(third, corrections[:3])
    higher7 = {}
    for row in target_rows:
        state = series._state(row + 1)
        value = POINT.higher_mixed_coefficients(strict, state, (9,))[9]
        higher7[row] = value
        POINT.clear_state_caches(strict)
        print("Q", row + 1, "degree-nine terms", len(value), flush=True)

    residual7 = {}
    for row in target_rows:
        value = strict_residual_row(parts, corrections, 7, row)
        add(value, higher7[row])
        residual7[row] = value
    localized7 = {"jacobian": jacobian}
    localized7.update({row: residual7[row] for row in P5.B_PIVOT_ROWS})
    c7 = transverse_localized_from_pivots(
        localized7, "strict order seven"
    )
    q30 = compatibility_row(residual7[29], c7, jacobian[29])
    q33 = compatibility_row(residual7[32], c7, jacobian[32])
    print("STRICT7", [(30, len(q30), polynomial_digest(q30)),
                      (33, len(q33), polynomial_digest(q33))], flush=True)
    del strict, third, higher7, residual7, localized7, c7
    gc.collect()

    h0, h0_pure, _terms, _quotients, _remainder = THIRD.NEXT.h0_reducer()
    h0_third = THIRD.ThirdOrderProjector(h0)
    require(not THIRD.validate_normal_graph(h0_third),
            "H0 symbolic strict7 normal graph regression returned")
    h0_strict = THIRD.ThirdStrictProjector(h0_third, corrections[:3])
    h0_degree10 = THIRD.component_coefficient(
        h0_strict, h0, h0_pure, 10
    )
    h0_L = GENERIC.reduce_L(h0_degree10)
    print("H0", len(h0_L), polynomial_digest(h0_L), flush=True)

    common_factor = strict7_common_factor()
    reduction = singular_reduction(
        first, exceptional, q30, q33, h0_L, common_factor
    )
    ledger = {
        "branch": "P5",
        "chart": "z16*z41*z11*(z44+z45) != 0 on L=0",
        "third_bend": "r=z46^(3)",
        "streamed_strict7_rows": target_rows,
        "strict7_Q30": [len(q30), polynomial_digest(q30)],
        "strict7_Q33": [len(q33), polynomial_digest(q33)],
        "H0_degree_ten_L_remainder": [
            len(h0_L), polynomial_digest(h0_L)
        ],
        "strict7_common_factor": [
            len(common_factor), polynomial_digest(common_factor)
        ],
        "localized_normal_forms": reduction,
        "scope_guard": (
            "symbolic localized strict-order-seven membership on the dense "
            "generic L chart; not an all-orders formal lifting theorem"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 symbolic generic-L strict7 ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
