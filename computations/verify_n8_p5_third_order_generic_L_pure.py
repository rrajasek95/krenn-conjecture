#!/usr/bin/env python3
"""Reduce the third-normal H1/H0 coefficients on the generic P5 L graph."""

import gc
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


THIRD = load_module(
    "n8_p5_third_order_for_generic_L",
    "verify_n8_p5_third_order_next_pure.py",
)
GENERIC = load_module(
    "n8_p5_generic_L_for_third_order_pure",
    "verify_n8_p5_generic_L_h0_degree9.py",
)
NEXT = THIRD.NEXT
P5 = THIRD.P5
PURE = THIRD.PURE
QQ = THIRD.QQ

EXPECTED_LEDGER_SHA256 = (
    "26f163baa17af989a52a32e6908fd6041cc64b8aa5d2580fdbeafa71d6090353"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def multiply(left, right):
    return THIRD.multiply(left, right)


def polynomial_digest(source):
    return THIRD.polynomial_digest(source)


def generic_relations(data):
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
            "generic-L first relation Q30 changed")
    require(order5[33] == multiply(multiply(common, v), first),
            "generic-L first relation Q33 changed")
    exceptional = []
    for equation in (30, 33):
        core = PURE.divide_by_monomial(order6[equation], (16, 16, 41))
        core = {
            monomial: 2 * coefficient
            for monomial, coefficient in GENERIC.COMPAT.divide_by_b(core).items()
        }
        exceptional.append(core)
    return first, exceptional


def localized_pure_flags(first, exceptional, h1, h0):
    names = [f"z{index}" for index in range(58)]
    ring_order = [names[GENERIC.SECOND_BEND],
                  names[GENERIC.FIRST_BEND], "w", "q", "p16", "p41"] \
        + names[:56]

    def encode(source):
        return GENERIC.COMPAT.AMBIENT.singular_polynomial(source, names)

    lines = [
        f"ring r=0,({','.join(ring_order)}),dp;",
        "poly ell=z9*z25-z11*z46;",
        f"poly first={encode(first)};",
        f"poly second30={encode(exceptional[0])};",
        f"poly second33={encode(exceptional[1])};",
        f"poly h1={encode(h1)};",
        f"poly h0={encode(h0)};",
        "poly loc11=z11*w-1;",
        "poly locb=(z44+z45)*q-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "poly second=q*(second30-second33);",
        "ideal i=ell,first,second,loc11,locb,loc16,loc41;",
        "ideal g=std(i);",
        '"UNIT",(reduce(1,g)==0);',
        '"SECOND30",(reduce(second30,g)==0);',
        '"SECOND33",(reduce(second33,g)==0);',
        '"H1",size(reduce(h1,g)),(reduce(h1,g)==0);',
        '"H0",size(reduce(h0,g)),(reduce(h0,g)==0);',
        '"H1FACTOR",factorize(reduce(h1,g));',
        '"H0FACTOR",factorize(reduce(h0,g));',
        "quit;",
    ]
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=180,
    )
    require(completed.returncode == 0,
            "Singular third-order generic-L reduction failed")
    print(completed.stdout)
    require("UNIT 0" in completed.stdout,
            "third-order generic-L ideal became unit")
    require("SECOND30 1" in completed.stdout
            and "SECOND33 1" in completed.stdout,
            "third-order generic-L bend graph changed")
    output = {}
    for label in ("H1", "H0"):
        line = next(item for item in completed.stdout.splitlines()
                    if item.startswith(label + " "))
        output[f"{label}_normal_form_terms"] = int(line.split()[1])
        output[f"{label}_zero"] = line.endswith(" 1")
    return output


def audit():
    mixed = GENERIC.symbolic_lift_data()
    corrections = mixed["corrections"][:3]
    first, exceptional = generic_relations(mixed)
    del mixed
    gc.collect()

    h1, h1_pure, _terms, _quotients = NEXT.h1_reducer()
    h1_third = THIRD.ThirdOrderProjector(h1)
    require(not THIRD.validate_normal_graph(h1_third),
            "H1 third normal graph regression returned")
    h1_strict = THIRD.ThirdStrictProjector(h1_third, corrections)
    h1 = THIRD.component_coefficient(h1_strict, h1, h1_pure, 9)
    h1_L = GENERIC.reduce_L(h1)
    del h1_strict, h1_third
    gc.collect()

    h0, h0_pure, _terms, _quotients, _remainder = NEXT.h0_reducer()
    h0_third = THIRD.ThirdOrderProjector(h0)
    require(not THIRD.validate_normal_graph(h0_third),
            "H0 third normal graph regression returned")
    h0_strict = THIRD.ThirdStrictProjector(h0_third, corrections)
    h0 = THIRD.component_coefficient(h0_strict, h0, h0_pure, 10)
    h0_L = GENERIC.reduce_L(h0)

    flags = localized_pure_flags(first, exceptional, h1_L, h0_L)
    ledger = {
        "branch": "P5",
        "chart": "z16*z41*z11*(z44+z45) != 0 on L=0",
        "first_bend_relation_terms": len(first),
        "first_bend_relation_sha256": polynomial_digest(first),
        "second_bend_relations": [
            [len(value), polynomial_digest(value)] for value in exceptional
        ],
        "H1_degree_nine_L_remainder_terms": len(h1_L),
        "H1_degree_nine_L_remainder_sha256": polynomial_digest(h1_L),
        "H0_degree_ten_L_remainder_terms": len(h0_L),
        "H0_degree_ten_L_remainder_sha256": polynomial_digest(h0_L),
        "localized_normal_forms": flags,
        "scope_guard": (
            "third-normal finite-order pure reduction on the twice-bent "
            "generic L graph before strict mixed order seven"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 third-order generic-L ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
