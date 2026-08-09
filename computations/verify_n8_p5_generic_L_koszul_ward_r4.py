#!/usr/bin/env python3
"""Correct the P5 Ward connection by the next monic z46 bend."""

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


WARD = load_module(
    "n8_p5_koszul_ward_for_r4",
    "analyze_n8_p5_generic_L_koszul_ward_prefix.py",
)
NAK = WARD.NAK
G = WARD.G
F2 = WARD.F2
REES = WARD.REES

EXPECTED_LEDGER_SHA256 = (
    "b9f736bd9a978547b4ffce15ac503bd5cc0b6425eb8756cb904abd95e424a4ca"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        WARD.add(answer, {tuple(sorted(monomial)): QQ(coefficient)})
    return answer


def audit():
    base = F2.audit(return_data=True)
    depth = 2
    graph = G.source_graph(
        base, maximum_order=5 + depth, additional_bends=1
    )
    require(len(graph["bend_variables"]) == 2,
            "r4 graph did not expose two retained bends")
    r4 = graph["bend_variables"][1]
    epsilon = graph["inverse_b"] + 1
    inverse_z11 = epsilon + 1
    inverse_z16 = epsilon + 2
    inverse_z41 = epsilon + 3
    inverse_u = epsilon + 4
    inverse_z9 = epsilon + 5

    relations = NAK.center_relations(base, graph)
    rows = NAK.truncated_rows(graph, epsilon, depth)
    _pure_coefficients, pure_windows = NAK.pure_prefixes(
        base, graph, epsilon
    )
    images, center_images = WARD.corrected_field(
        base, graph, relations, inverse_z11, inverse_z9
    )

    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    order7_m30 = graph["compatibility_orders"][6][29]
    r4_coefficient = WARD.derivation(
        order7_m30, {r4: {(): QQ(1)}}
    )
    common = polynomial((((a[11], a[16], a[16], a[41]), QQ(1, 2)),))
    unit_factor = polynomial((
        ((a[26],), 1), ((b,), 1), ((a[44],), -1)
    ))
    expected_coefficient = WARD.multiply(common, unit_factor)
    require(r4_coefficient == expected_coefficient,
            "M30 next-bend coefficient changed")

    before_r4 = WARD.derivation(order7_m30, images)
    inverse_coefficient = polynomial(((
        (inverse_z11, inverse_z16, inverse_z16, inverse_z41, inverse_u),
        2,
    ),))
    images[r4] = {
        monomial: -coefficient
        for monomial, coefficient in WARD.multiply(
            before_r4, inverse_coefficient
        ).items()
    }

    result = WARD.singular_test(
        base, graph, relations, rows, pure_windows, epsilon, depth,
        images, center_images, inverse_z11, inverse_z16, inverse_z41,
        inverse_u, inverse_z9,
    )
    require(set(result["centers"]) == {"L", "F1", "F2", "G"},
            "r4 Ward center output incomplete")
    require(all(zero for _size, zero in result["centers"].values()),
            "r4 Ward field left a center derivative")
    failures = [
        row for row, zero in result["row_flags"].items() if not zero
    ]
    pure_failures = [
        key for key, zero in result["pure_flags"].items() if not zero
    ]
    require(not failures,
            "r4-corrected Ward field left a mixed derivative")
    require(not pure_failures,
            "r4-corrected Ward field left a pure prefix derivative")
    require(result["row_flags"].get(30)
            and result["row_flags"].get(33),
            "r4 correction did not close the M30/M33 pair")

    ledger = {
        "chart": "generic L/F1/F2/G with z9 and M30 coefficient inverted",
        "prefix": f"tau-saturated mixed germs modulo epsilon^{depth}",
        "next_bend": "r4=z46^(4)",
        "M30_r4_coefficient": (
            "1/2*z11*z16^2*z41*(z26+b-z44)"
        ),
        "M30_r4_coefficient_is_localized_unit": True,
        "theta_r4_terms": len(images[r4]),
        "center_derivatives_zero": all(
            zero for _size, zero in result["centers"].values()
        ),
        "mixed_derivative_failures_after_r4": failures,
        "mixed_derivative_remainder_sizes": {
            str(row): result["row_sizes"][row] for row in failures
        },
        "M30_derivative_zero_after_r4": result["row_flags"].get(30),
        "M33_derivative_zero_after_r4": result["row_flags"].get(33),
        "pure_derivative_failures_after_r4": [
            list(key) for key in pure_failures
        ],
        "pure_derivative_remainder_sizes": {
            f"H{colour}_{start}": result["pure_sizes"][colour, start]
            for colour, start in pure_failures
        },
        "mixed_derivative_term_counts": result["row_image_terms"],
        "pure_derivative_term_counts": result["pure_image_terms"],
        "singular_output_sha256": result["stdout_sha256"],
        "scope_guard": (
            "exact one-next-bend connection on the dual-number graph prefix; "
            "an all-order induction still requires a uniform monic/principal "
            "recurrence theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L Koszul-Ward r4 ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
