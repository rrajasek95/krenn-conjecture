#!/usr/bin/env python3
"""Exact source export for the k5 0:31:30 A-open/R25 branch.

Raw row 7 is ``A*a4+B``.  On A nonzero we substitute a4=-B/A,
clear one denominator from every (a4-linear) literal row, and remove only
the already localized associates of A and b4.  The initial gate localizes
the selected-base and a*d antecedents only; if it is unit, this is stronger
than restoring the additional c-product and H live factors.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
REPO = COMP.parent
BUILDER = (COMP / "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
           "build_recursive_face_charts.py")
ROUTING = (COMP / "unaudited-codex-k56-boundary-routing-2026-08-21" /
           "results_k56_recursive_boundary_routing.json")
STRUCTURAL = (COMP / "unaudited-codex-face03130-structural-2026-08-21" /
              "results_face03130_reverse_interface_standard.json")
TOOLKIT = COMP / "toolkit/groebner/msolve_io.py"
INPUT_Q = HERE / "face03130_aopen_base_char0.msolve"
INPUT_P = HERE / "face03130_aopen_base_p1073741827.msolve"
INPUT_FULL_Q = HERE / "face03130_aopen_full_char0.msolve"
INPUT_FULL_P = HERE / "face03130_aopen_full_p1073741827.msolve"
INPUT_SPLIT_Q = HERE / "face03130_aopen_split_live_char0.msolve"
INPUT_SPLIT_P = HERE / "face03130_aopen_split_live_p1073741827.msolve"
INPUT_CORE8_Q = HERE / "face03130_aopen_core8_split_live_char0.msolve"
INPUT_CORE8_P = HERE / "face03130_aopen_core8_split_live_p1073741827.msolve"
LABELS = HERE / "face03130_aopen_base_labels.json"
LABELS_FULL = HERE / "face03130_aopen_full_labels.json"
LABELS_SPLIT = HERE / "face03130_aopen_split_live_labels.json"
LABELS_CORE8 = HERE / "face03130_aopen_core8_split_live_labels.json"
RESULT = HERE / "results_face03130_aopen_export.json"
STATE = (0, 31, 30)
PIVOT_RAW = 7
R25_RAW = 16
PRIME = 1073741827
CORE8_RAW = (6, 8, 12, 14, 16, 18, 19, 20)
ACTIVE_NAMES = ("a0", "a1", "a2", "a3", "a5", "b3", "b4", "b5",
                "d2", "d3", "d4")
VARIABLE_NAMES = ("z", *ACTIVE_NAMES)
SPLIT_VARIABLE_NAMES = ("zbase", "zc", "zh", *ACTIVE_NAMES)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def primitive(poly, variables, sp):
    value = sp.Poly(sp.expand(poly), *variables, domain=sp.QQ)
    require(not value.is_zero, "zero reduced row")
    denominators = [int(coefficient.q) for _, coefficient in value.terms()]
    denominator = math.lcm(*denominators)
    integers = [int(coefficient * denominator)
                for _, coefficient in value.terms()]
    content = math.gcd(*map(abs, integers))
    value = sp.Poly(value.as_expr() * denominator / content,
                    *variables, domain=sp.QQ)
    require(all(coefficient.q == 1 for _, coefficient in value.terms()),
            "primitive row escaped Z")
    if value.LC() < 0:
        value = -value
    return value


def exact_remove(poly, factor, variables, sp):
    value = sp.Poly(poly, *variables, domain=sp.QQ)
    divisor = sp.Poly(factor, *variables, domain=sp.QQ)
    exponent = 0
    while True:
        quotient, remainder = sp.div(value, divisor)
        if not remainder.is_zero:
            return value, exponent
        value = quotient
        exponent += 1


def encode(poly):
    pieces = []
    for position, (exponent, coefficient) in enumerate(poly.terms()):
        require(coefficient.q == 1 and coefficient != 0,
                "encoder requires nonzero integer coefficients")
        coefficient = int(coefficient)
        symbolic = [name + (f"^{power}" if power != 1 else "")
                    for name, power in zip(ACTIVE_NAMES, exponent, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = []
        if magnitude != 1 or not symbolic:
            factors.append(str(magnitude))
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+") if position else
                       ("-" if coefficient < 0 else "")) + body)
    require(pieces, "empty encoder input")
    return "".join(pieces)


def encode_rab(poly, zname="z"):
    pieces = []
    for position, (exponent, coefficient) in enumerate(poly.terms()):
        require(coefficient.q == 1 and coefficient != 0,
                "Rabinowitsch encoder requires Z coefficients")
        coefficient = int(coefficient)
        symbolic = [zname]
        symbolic.extend(name + (f"^{power}" if power != 1 else "")
                        for name, power in zip(ACTIVE_NAMES, exponent,
                                               strict=True) if power)
        factors = ([str(abs(coefficient))] if abs(coefficient) != 1 else [])
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+") if position else
                       ("-" if coefficient < 0 else "")) + body)
    return "".join(pieces) + "-1"


def extract_localizer(value, symbols, sp):
    require("*(" in value and value.endswith(")-1"),
            "unexpected localizer syntax")
    body = value.split("*(", 1)[1][:-3]
    return sp.expand(sp.sympify(body.replace("^", "**"), locals=symbols))


def profile(poly):
    return {"terms": len(poly.terms()), "degree": poly.total_degree()}


def main():
    try:
        import sympy as sp
    except ImportError:
        candidate = REPO / ".venv/lib"
        sites = sorted(candidate.glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    HERE.mkdir(parents=True, exist_ok=True)
    BUILD = load("face03130_aopen_builder", BUILDER)
    MSOLVE_IO = load("face03130_aopen_msolve_io", TOOLKIT)
    record = BUILD.build_state(STATE)
    require(record["key"] == "0:31:30" and
            record["nonzero_gauged_source_row_count"] == 16,
            "literal face interface changed")
    structural = json.loads(STRUCTURAL.read_text())
    require(structural["logical_sha256"] ==
            "96052061416f3e47eb5d2b051ba92f3e6d2f34d7bdc2198778697ba7670418ba",
            "frozen structural audit changed")

    all_names = record["variable_names"]
    all_variables = sp.symbols(" ".join(all_names))
    by_name = dict(zip(all_names, all_variables, strict=True))
    variables = tuple(by_name[name] for name in ACTIVE_NAMES)
    a4 = by_name["a4"]

    def decode(terms):
        return sp.expand(sum(
            sp.Rational(*term["coefficient"]) * sp.prod(
                variable**power for variable, power in
                zip(all_variables, term["exponents"], strict=True))
            for term in terms))

    source = tuple((row["raw_index"], row["label"], decode(row["terms"]))
                   for row in record["rows"])
    source_map = {raw: poly for raw, _, poly in source}
    pivot = sp.Poly(source_map[PIVOT_RAW], a4)
    require(pivot.degree() == 1, "raw7 is no longer a4-linear")
    A, B = map(sp.expand, (pivot.nth(1), pivot.nth(0)))
    require(str(A) == "-a0*d2*d4 + b4*d2 + d4" and
            str(B) == structural["best_fraction_free_packet"]["pivot_residual"],
            "frozen A/B pivot changed")

    reduced = []
    for raw, label, poly in source:
        if raw == PIVOT_RAW:
            continue
        in_a4 = sp.Poly(poly, a4)
        require(in_a4.degree() <= 1, f"raw{raw} is nonlinear in a4")
        numerator = sp.expand(A * in_a4.nth(0) - B * in_a4.nth(1))
        value, removed_A = exact_remove(numerator, A, variables, sp)
        value, removed_b4 = exact_remove(value, by_name["b4"], variables, sp)
        value = primitive(value.as_expr(), variables, sp)
        reduced.append({
            "raw_index": raw, "label": label, "poly": value,
            "removed_localized_A_power": removed_A,
            "removed_localized_b4_power": removed_b4,
        })
    require(len(reduced) == 15 and len({tuple(row["poly"].terms())
                                       for row in reduced}) == 15,
            "reduced row count/deduplication changed")
    r25 = next(row for row in reduced if row["raw_index"] == R25_RAW)
    require(profile(r25["poly"]) == {"terms": 25, "degree": 6},
            "R25 reduced profile changed")
    frozen_r25 = sp.Poly(
        structural["best_fraction_free_packet"]["primitive"],
        *variables, domain=sp.QQ)
    require(r25["poly"] in (frozen_r25, -frozen_r25),
            "raw16 reduction differs from frozen R25")

    localizers = {key: extract_localizer(value, by_name, sp)
                  for key, value in record["localizers"].items()}
    selected = localizers["selected_base_terms"]
    ad = localizers["both_live_a_d"]
    require(sp.expand(selected - by_name["a5"]*by_name["b3"]*
                      by_name["b4"]) == 0,
            "selected-base localizer changed")
    ad_sub = sp.cancel(ad.subs(a4, -B/A))
    ad_num, ad_den = map(sp.expand, ad_sub.as_numer_denom())
    ad_expected = (-B * by_name["a1"]*by_name["a2"]*by_name["a3"] *
                   by_name["d2"]*by_name["d3"]*by_name["d4"])
    require(sp.cancel(ad_sub-ad_expected/A) == 0 and
            (sp.expand(ad_den-A) == 0 or sp.expand(ad_den+A) == 0),
            "transported a*d localizer changed")
    base = primitive(
        A * B * by_name["a1"]*by_name["a2"]*by_name["a3"]*by_name["a5"] *
        by_name["b3"]*by_name["b4"]*by_name["d2"]*by_name["d3"]*by_name["d4"],
        variables, sp)
    require(profile(base) == {"terms": 16, "degree": 17},
            "base-live Rabinowitsch profile changed")

    extra_localizers = []
    for key in ("both_live_c_numerators", "H"):
        transported = sp.cancel(localizers[key].subs(a4, -B/A))
        numerator, denominator = transported.as_numer_denom()
        numerator = primitive(numerator, variables, sp)
        core, removed_b4 = exact_remove(
            numerator.as_expr(), by_name["b4"], variables, sp)
        core = primitive(core.as_expr(), variables, sp)
        require(removed_b4 == 1,
                f"transported {key} lost its frozen b4 factor")
        extra_localizers.append({
            "label": key, "numerator": numerator, "core": core,
            "denominator": str(sp.factor(denominator)),
            **profile(numerator),
            "removed_already_live_b4_power": removed_b4,
            "core_profile": profile(core),
            "factor_profiles": [
                {"terms": len(sp.Poly(factor, *variables).terms()),
                 "degree": sp.Poly(factor, *variables).total_degree(),
                 "multiplicity": multiplicity,
                 "factor": str(factor)}
                for factor, multiplicity in sp.factor_list(
                    numerator.as_expr())[1]],
        })

    labelled = [(f"raw{row['raw_index']}_{row['label']}", encode(row["poly"]))
                for row in reduced]
    labelled.append(("RAB_Aopen_selected_ad", encode_rab(base)))
    for path, characteristic in ((INPUT_Q, 0), (INPUT_P, PRIME)):
        path.write_text(",".join(VARIABLE_NAMES) + f"\n{characteristic}\n" +
                        ",\n".join(poly for _, poly in labelled) + "\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "source_raw_indices": [row["raw_index"] for row in reduced],
        "pivot_raw_index": PIVOT_RAW,
        "R25_raw_index": R25_RAW,
        "localized_base_factors": ["A", "B", "a1", "a2", "a3", "a5",
                                   "b3", "b4", "d2", "d3", "d4"],
    }, indent=2, sort_keys=True) + "\n")

    full_product = primitive(
        base.as_expr() * sp.prod(row["core"].as_expr()
                                 for row in extra_localizers), variables, sp)
    require(profile(full_product) == {"terms": 25230, "degree": 37},
            "full-live Rabinowitsch profile changed")
    labelled_full = labelled[:-1] + [
        ("RAB_Aopen_all_original_live", encode_rab(full_product))]
    for path, characteristic in ((INPUT_FULL_Q, 0), (INPUT_FULL_P, PRIME)):
        path.write_text(",".join(VARIABLE_NAMES) + f"\n{characteristic}\n" +
                        ",\n".join(poly for _, poly in labelled_full) + "\n")
    LABELS_FULL.write_text(json.dumps({
        "labels": [label for label, _ in labelled_full],
        "source_raw_indices": [row["raw_index"] for row in reduced],
        "pivot_raw_index": PIVOT_RAW,
        "R25_raw_index": R25_RAW,
        "localized_factor_packets": [
            "A*B*a1*a2*a3*a5*b3*b4*d2*d3*d4",
            "transported both_live_c_numerators with redundant b4 removed",
            "transported H numerator with redundant b4 removed",
        ],
    }, indent=2, sort_keys=True) + "\n")

    labelled_split = labelled[:-1] + [
        ("RAB_Aopen_selected_ad", encode_rab(base, "zbase")),
        ("RAB_Aopen_c_product", encode_rab(extra_localizers[0]["core"], "zc")),
        ("RAB_Aopen_H", encode_rab(extra_localizers[1]["core"], "zh")),
    ]
    for path, characteristic in ((INPUT_SPLIT_Q, 0), (INPUT_SPLIT_P, PRIME)):
        path.write_text(",".join(SPLIT_VARIABLE_NAMES) +
                        f"\n{characteristic}\n" +
                        ",\n".join(poly for _, poly in labelled_split) + "\n")
    LABELS_SPLIT.write_text(json.dumps({
        "labels": [label for label, _ in labelled_split],
        "source_raw_indices": [row["raw_index"] for row in reduced],
        "scope": "three separate inverse variables for the exact full-live product",
    }, indent=2, sort_keys=True) + "\n")
    source_by_raw = {row["raw_index"]: (label, encoded)
                     for row, (label, encoded) in
                     zip(reduced, labelled[:-1], strict=True)}
    labelled_core8 = [source_by_raw[raw] for raw in CORE8_RAW]
    labelled_core8 += labelled_split[-3:]
    for path, characteristic in ((INPUT_CORE8_Q, 0), (INPUT_CORE8_P, PRIME)):
        path.write_text(",".join(SPLIT_VARIABLE_NAMES) +
                        f"\n{characteristic}\n" +
                        ",\n".join(poly for _, poly in labelled_core8) + "\n")
    LABELS_CORE8.write_text(json.dumps({
        "labels": [label for label, _ in labelled_core8],
        "source_raw_indices": list(CORE8_RAW),
        "selection_rule": "eight smallest reduced rows by (terms,degree,raw)",
    }, indent=2, sort_keys=True) + "\n")

    parsed_q = MSOLVE_IO.read_msolve_input(
        INPUT_Q, strict=True, allow_characteristic_zero=True)
    parsed_p = MSOLVE_IO.read_msolve_input(INPUT_P, strict=True)
    require(parsed_q.variables == parsed_p.variables == VARIABLE_NAMES and
            len(parsed_q.polynomials) == len(parsed_p.polynomials) == 16 and
            parsed_q.polynomials == parsed_p.polynomials,
            "Q/modular source inputs differ")
    require(parsed_q.polynomial_sha256 == parsed_p.polynomial_sha256,
            "Q/modular polynomial digests differ")
    parsed_full_q = MSOLVE_IO.read_msolve_input(
        INPUT_FULL_Q, strict=True, allow_characteristic_zero=True)
    parsed_full_p = MSOLVE_IO.read_msolve_input(INPUT_FULL_P, strict=True)
    require(parsed_full_q.variables == parsed_full_p.variables == VARIABLE_NAMES
            and parsed_full_q.polynomials == parsed_full_p.polynomials and
            parsed_full_q.polynomial_sha256 == parsed_full_p.polynomial_sha256
            and parsed_full_q.polynomials[:-1] == parsed_q.polynomials[:-1],
            "full-live Q/modular/source rows differ")
    parsed_split_q = MSOLVE_IO.read_msolve_input(
        INPUT_SPLIT_Q, strict=True, allow_characteristic_zero=True)
    parsed_split_p = MSOLVE_IO.read_msolve_input(INPUT_SPLIT_P, strict=True)
    require(parsed_split_q.variables == parsed_split_p.variables ==
            SPLIT_VARIABLE_NAMES and
            parsed_split_q.polynomials == parsed_split_p.polynomials and
            parsed_split_q.polynomial_sha256 == parsed_split_p.polynomial_sha256
            and parsed_split_q.polynomials[:-3] == parsed_q.polynomials[:-1],
            "split-live Q/modular/source rows differ")
    parsed_core8_q = MSOLVE_IO.read_msolve_input(
        INPUT_CORE8_Q, strict=True, allow_characteristic_zero=True)
    parsed_core8_p = MSOLVE_IO.read_msolve_input(INPUT_CORE8_P, strict=True)
    require(parsed_core8_q.variables == parsed_core8_p.variables ==
            SPLIT_VARIABLE_NAMES and
            parsed_core8_q.polynomials == parsed_core8_p.polynomials and
            parsed_core8_q.polynomial_sha256 == parsed_core8_p.polynomial_sha256
            and len(parsed_core8_q.polynomials) == 11,
            "core8 Q/modular interface differs")

    reduced_by_raw = {row["raw_index"]: row["poly"] for row in reduced}

    def secondary_pivot_profile(raw_index, variable_name):
        """Exact size audit for a proposed second fraction-field solve."""
        variable = by_name[variable_name]
        pivot_row = reduced_by_raw[raw_index]
        pivot_in_variable = sp.Poly(pivot_row.as_expr(), variable)
        require(pivot_in_variable.degree() == 1,
                f"raw{raw_index} is not linear in {variable_name}")
        coefficient = sp.expand(pivot_in_variable.nth(1))
        residual = sp.expand(pivot_in_variable.nth(0))
        target_variables = tuple(value for value in variables
                                 if value != variable)

        def transform(poly):
            value = sp.cancel(poly.as_expr().subs(
                variable, -residual/coefficient))
            numerator, denominator = value.as_numer_denom()
            numerator_poly, removed_coefficient = exact_remove(
                numerator, coefficient, target_variables, sp)
            numerator_poly, removed_b4 = exact_remove(
                numerator_poly.as_expr(), by_name["b4"],
                target_variables, sp)
            numerator_poly = primitive(
                numerator_poly.as_expr(), target_variables, sp)
            return {
                **profile(numerator_poly),
                "denominator": str(sp.factor(denominator)),
                "removed_new_pivot_power": removed_coefficient,
                "removed_already_live_b4_power": removed_b4,
            }

        row_profiles = [
            {"raw_index": row["raw_index"], **transform(row["poly"])}
            for row in reduced if row["raw_index"] != raw_index]
        live_profiles = [
            {"label": label, **transform(poly)}
            for label, poly in [
                ("base", base),
                ("c_core", extra_localizers[0]["core"]),
                ("H_core", extra_localizers[1]["core"]),
            ]]
        return {
            "pivot_raw_index": raw_index,
            "variable": variable_name,
            "coefficient": str(coefficient),
            "coefficient_profile": profile(primitive(
                coefficient, target_variables, sp)),
            "residual": str(residual),
            "residual_profile": profile(primitive(
                residual, target_variables, sp)),
            "transformed_row_profiles": row_profiles,
            "transformed_live_profiles": live_profiles,
            "maximum_row_terms": max(row["terms"] for row in row_profiles),
            "maximum_live_terms": max(row["terms"] for row in live_profiles),
        }

    secondary_profiles = [
        secondary_pivot_profile(16, "a2"),
        secondary_pivot_profile(20, "b3"),
    ]
    require([(row["maximum_row_terms"], row["maximum_live_terms"])
             for row in secondary_profiles] == [(262, 735), (425, 1103)],
            "secondary-pivot growth profile changed")

    result = {
        "status": "UNAUDITED exact A-open source reduction/export PASS",
        "state": "0:31:30", "pivot": "raw7=A*a4+B", "A": str(A),
        "B": str(B), "substitution": "a4=-B/A",
        "active_variables": list(ACTIVE_NAMES),
        "reduced_rows": [
            {key: value for key, value in row.items() if key != "poly"} |
            profile(row["poly"]) |
            {"polynomial_sha256": MSOLVE_IO.polynomial_sha256(
                encode(row["poly"]))}
            for row in reduced],
        "base_localizer": {
            "factor_order": ["A", "B", "a1", "a2", "a3", "a5", "b3",
                             "b4", "d2", "d3", "d4"],
            **profile(base),
            "coefficient_sha256": MSOLVE_IO.polynomial_sha256(encode(base)),
        },
        "extra_original_live_factor_profiles": [
            {key: value for key, value in row.items()
             if key not in ("numerator", "core")}
            for row in extra_localizers],
        "extra_live_factors_not_localized_in_initial_gate": [
            "both_live_c_numerators", "H"],
        "gate_strength_scope": (
            "If the base-localized gate is empty, this is stronger than the "
            "original interior and no c/H localization is needed. A nonunit "
            "result requires restoring those two transported numerators."),
        "input_Q_sha256": parsed_q.file_sha256,
        "input_Q_logical_sha256": parsed_q.logical_sha256,
        "input_modular_sha256": parsed_p.file_sha256,
        "input_modular_logical_sha256": parsed_p.logical_sha256,
        "full_live_localizer": {
            **profile(full_product),
            "factor_packets": ["base", "c_core", "H_core"],
            "coefficient_sha256": MSOLVE_IO.polynomial_sha256(
                encode(full_product)),
        },
        "input_full_Q_sha256": parsed_full_q.file_sha256,
        "input_full_Q_logical_sha256": parsed_full_q.logical_sha256,
        "input_full_modular_sha256": parsed_full_p.file_sha256,
        "input_full_modular_logical_sha256": parsed_full_p.logical_sha256,
        "input_split_Q_sha256": parsed_split_q.file_sha256,
        "input_split_Q_logical_sha256": parsed_split_q.logical_sha256,
        "input_split_modular_sha256": parsed_split_p.file_sha256,
        "input_split_modular_logical_sha256": parsed_split_p.logical_sha256,
        "split_live_equivalence": (
            "zbase*base=zc*c_core=zh*H_core=1 is equivalent to one inverse "
            "of base*c_core*H_core over every field."),
        "core8_raw_indices": list(CORE8_RAW),
        "input_core8_Q_sha256": parsed_core8_q.file_sha256,
        "input_core8_Q_logical_sha256": parsed_core8_q.logical_sha256,
        "input_core8_modular_sha256": parsed_core8_p.file_sha256,
        "input_core8_modular_logical_sha256": parsed_core8_p.logical_sha256,
        "secondary_pivot_growth": secondary_profiles,
        "secondary_pivot_conclusion": (
            "The natural raw16/a2 and raw20/b3 solves reduce dimension but "
            "destroy sparsity. Future work should use a component/slice or "
            "an alternate row combination, not either literal second pivot."),
        "polynomial_sha256": list(parsed_q.polynomial_sha256),
        "labels_sha256": file_sha(LABELS),
        "source_hashes": {"builder": file_sha(BUILDER),
                          "routing": file_sha(ROUTING),
                          "structural": file_sha(STRUCTURAL)},
        "mutation_guards": [
            "changing a raw7 pivot coefficient changes A/B and reduced rows",
            "changing raw16 changes the frozen R25 comparison",
            "dropping A or B changes the base-localizer digest",
        ],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03130 A-open source export: PASS")
    print("rows", [(row["raw_index"], profile(row["poly"]),
                    row["removed_localized_A_power"],
                    row["removed_localized_b4_power"]) for row in reduced])
    print("base", profile(base), "extra", [
        (row["label"], row["terms"], row["degree"])
        for row in extra_localizers])
    print("Q", parsed_q.file_sha256, "mod", parsed_p.file_sha256)
    print("full", profile(full_product), parsed_full_q.file_sha256,
          parsed_full_p.file_sha256)
    print("split", INPUT_SPLIT_Q.stat().st_size, parsed_split_q.file_sha256,
          parsed_split_p.file_sha256)
    print("core8", INPUT_CORE8_Q.stat().st_size, parsed_core8_q.file_sha256,
          parsed_core8_p.file_sha256)
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
