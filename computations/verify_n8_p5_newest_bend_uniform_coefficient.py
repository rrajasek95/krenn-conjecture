#!/usr/bin/env python3
"""Certify the all-order newest-bend coefficient on the P5 Schur graph."""

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


R4 = load_module(
    "n8_p5_r4_for_uniform_bend",
    "verify_n8_p5_generic_L_koszul_ward_r4.py",
)
WARD = R4.WARD
G = R4.G
F2 = R4.F2

EXPECTED_LEDGER_SHA256 = (
    "7419aaf1492fa46d6a2af344333ce34e163c30bbf3824999808245ab47af6cf2"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def derivative(source, variable):
    answer = {}
    for monomial, coefficient in source.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        output = list(monomial)
        output.remove(variable)
        output = tuple(output)
        answer[output] = (
            answer.get(output, QQ(0)) + coefficient * multiplicity
        )
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        WARD.add(answer, {tuple(sorted(monomial)): QQ(coefficient)})
    return answer


def maximum_variable_degree(source, variable):
    return max((monomial.count(variable) for monomial in source), default=0)


def family_digest(sources):
    digest = sha256()
    for source in sources:
        digest.update(WARD.polynomial_digest(source).encode())
    return digest.hexdigest()


def audit():
    base = F2.audit(return_data=True)
    graph = G.source_graph(base, maximum_order=7, additional_bends=1)
    require(len(graph["bend_variables"]) == 2,
            "uniform-bend graph lost r3/r4")
    r4 = graph["bend_variables"][1]
    layout = base["layout"]
    a = layout["a"]
    z46 = a[46]
    b = graph["b_variable"]

    source_affinity = {}
    for label, sources in (
        ("normal", base["normal"]),
        ("transverse", base["transverse"]),
        ("obstruction", base["obstruction"]),
    ):
        degrees = [maximum_variable_degree(source, z46) for source in sources]
        require(max(degrees, default=0) <= 1,
                f"{label} strict rows stopped being affine in z46")
        source_affinity[label] = {
            "rows": len(sources),
            "z46_degree_zero": degrees.count(0),
            "z46_degree_one": degrees.count(1),
            "maximum_z46_degree": max(degrees, default=0),
        }

    # The r4 derivative is a time-shifted Jacobi field.  Record its first
    # four relative coefficients.  The first entry is the prescribed z46
    # perturbation; later entries are the unique 207-row implicit response.
    response_records = []
    for relative_order in range(4):
        absolute_order = 4 + relative_order
        derivatives = {
            variable: derivative(series[absolute_order], r4)
            for variable, series in graph["series"].items()
            if derivative(series[absolute_order], r4)
        }
        response_records.append({
            "relative_order": relative_order,
            "nonzero_variables": len(derivatives),
            "terms": sum(map(len, derivatives.values())),
            "maximum_terms": max(map(len, derivatives.values()), default=0),
            "sha256": family_digest(
                source for _variable, source in sorted(derivatives.items())
            ),
        })
    require(
        [(item["nonzero_variables"], item["terms"], item["maximum_terms"])
         for item in response_records]
        == [(1, 1, 1), (11, 16, 3), (11, 23, 5), (22, 41, 7)],
        "newest-bend Jacobi response profile changed",
    )

    require(all(
        not derivative(source, r4)
        for sources in graph["transverse_residual_orders"][3:7]
        for source in sources
    ), "newest-bend Jacobi field left a transverse residual")

    compatibility_derivatives = []
    for relative_order in range(4):
        sources = graph["compatibility_orders"][3 + relative_order]
        values = [derivative(source, r4) for source in sources]
        compatibility_derivatives.append(values)
    require(not any(
        source
        for values in compatibility_derivatives[:3]
        for source in values
    ), "newest bend reached compatibility before relative order three")

    terminal = compatibility_derivatives[3]
    nonzero_rows = [row + 1 for row, source in enumerate(terminal) if source]
    require(nonzero_rows == [30, 33],
            "newest-bend terminal response rows changed")
    common = polynomial((((a[11], a[16], a[16], a[41]), QQ(1, 2)),))
    unit30 = polynomial((
        ((a[26],), 1), ((b,), 1), ((a[44],), -1)
    ))
    factor33 = polynomial((((a[26],), 1), ((a[44],), -1)))
    expected30 = WARD.multiply(common, unit30)
    expected33 = WARD.multiply(common, factor33)
    require(terminal[29] == expected30,
            "uniform M30 newest-bend coefficient changed")
    require(terminal[32] == expected33,
            "uniform M33 newest-bend coefficient changed")

    # Up through the first compatibility response no r4 square can occur.
    # This is also the valuation inequality 2k>k+3 for every future k>=4.
    audited_series = [
        source
        for series in graph["series"].values()
        for source in series[:8]
    ]
    audited_compatibility = [
        source
        for values in graph["compatibility_orders"][:7]
        for source in values
    ]
    require(max(
        maximum_variable_degree(source, r4)
        for source in audited_series + audited_compatibility
    ) <= 1, "r4 acquired a square before its first compatibility response")

    ledger = {
        "formal_system": {
            "implicit_rows": 207,
            "normal_rows": 196,
            "transverse_rows": 11,
            "localized_transverse_jacobian": "b*I_11",
            "coefficient_ring": "generic-L localized characteristic zero",
        },
        "strict_source_affinity": source_affinity,
        "jacobi_response": response_records,
        "first_compatibility_relative_order": 3,
        "earlier_compatibility_derivatives_zero": True,
        "terminal_nonzero_rows": nonzero_rows,
        "uniform_coefficients": {
            "M30": "1/2*z11*z16^2*z41*(z26+b-z44)",
            "M33": "1/2*z11*z16^2*z41*(z26-z44)",
            "M30_is_localized_unit": True,
        },
        "all_order_statement": (
            "for every new z46 coefficient r_k at order k>=4, the unique "
            "207-row Jacobi response is tau^k times the same series V; "
            "therefore the coefficient of r_k in M30 at order k+3 is the "
            "displayed localized unit, while only M33 has another direct "
            "compatibility response at that relative order"
        ),
        "linearity_guard": (
            "higher powers of r_k have valuation at least 2k>k+3 for k>=4"
        ),
        "remaining_uniform_datum": (
            "prove a source-level/Schur syzygy making the full corrected "
            "M33 and other 26 germs follow M30 at every order"
        ),
        "scope_guard": (
            "all-order newest-bend coefficient theorem for the formal 207-row "
            "P5 graph; not yet all-order principalization or pure membership"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "uniform newest-bend coefficient ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
