#!/usr/bin/env python3
"""Export the exact-Q triangle-pendant P26-open Cramer system.

The nine transported compatibility rows are source-derived polynomial
necessities only on the Cramer chart.  Accordingly the single Rabinowitsch
coefficient is the product of *all* six frozen open-chart factors

    F0, A3hat, P26, N4, N5, A2hat.

In particular it is not the unsound N5-only localization.  F0 is precisely
the two-term coefficient used by the earlier P26=0 boundary manifest.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE_DIR = (HERE.parent /
              "unaudited-codex-n8-orbit0-normalized-78-2026-08-20")
DISCOVERY = SOURCE_DIR / "discover_branch0_triangle_pendant_reduction.py"
CRAMER_AUDIT = SOURCE_DIR / "results_branch0_triangle_pendant_cramer_n5.json"
OLD_DIR = HERE.parent / "unaudited-codex-tp-p26-boundary-char0-2026-08-21"
OLD_EXPORT = OLD_DIR / "results_tp_p26_base_core_char0_export.json"
OLD_MANIFEST = OLD_DIR / "results_tp_p26_base_core_char0.manifest.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "tp_p26_interior_char0.msolve"
LABELS = HERE / "tp_p26_interior_char0_labels.json"
RESULT = HERE / "results_tp_p26_interior_char0_export.json"

SOURCE_LABELS = (8, 9, 10, 11, 13, 15, 17, 19, 21)
EXPECTED_TERMS = (80, 106, 61, 222, 262, 164, 122, 91, 101)
ACTIVE_NAMES = ("b0", "b1", "b3", "d4", "d5")
VARIABLE_NAMES = ("z", *ACTIVE_NAMES)
LIVE_LABELS = ("F0", "A3hat", "P26", "N4", "N5", "A2hat")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("tp_p26_interior_exact_source", DISCOVERY)
C = D.CHART
MSOLVE_IO = load("tp_p26_interior_msolve_io", TOOLKIT)
ACTIVE_INDICES = tuple(C.names.index(name) for name in ACTIVE_NAMES)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def primitive_integer(poly):
    require(bool(poly), "zero source polynomial")
    denominator = math.lcm(*(value.denominator for value in poly.values()))
    integers = [value.numerator * (denominator // value.denominator)
                for value in poly.values()]
    content = math.gcd(*map(abs, integers))
    require(content > 0, "zero polynomial content")
    value = C.scale(poly, Fraction(denominator, content))
    first = value[min(value)]
    if first < 0:
        value = C.scale(value, -1)
    require(all(coefficient.denominator == 1 for coefficient in value.values()),
            "primitive row is not integral")
    return value


def active_terms(poly):
    """Return a primitive exact five-variable integer dictionary."""
    answer = {}
    for exponent, coefficient in primitive_integer(poly).items():
        require(all(exponent[index] == 0 for index in range(C.n)
                    if index not in ACTIVE_INDICES),
                ("source row escaped active variables", exponent))
        key = tuple(exponent[index] for index in ACTIVE_INDICES)
        require(key not in answer, "projected monomial collision")
        answer[key] = int(coefficient)
    return answer


def encode_terms(poly, *, include_z=False, constant_minus_one=False):
    """Encode an integer dictionary coefficient-first and parenthesis-free."""
    pieces = []
    for position, exponent in enumerate(sorted(
            poly, key=lambda item: (sum(item), item), reverse=True)):
        coefficient = int(poly[exponent])
        require(coefficient != 0, "explicit zero coefficient")
        symbolic = ["z"] if include_z else []
        symbolic.extend(name + (f"^{power}" if power != 1 else "")
                        for name, power in zip(ACTIVE_NAMES, exponent,
                                               strict=True) if power)
        magnitude = abs(coefficient)
        factors = []
        if magnitude != 1 or not symbolic:
            factors.append(str(magnitude))
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+")
                       if position else ("-" if coefficient < 0 else ""))
                      + body)
    require(pieces, "empty encoded polynomial")
    if constant_minus_one:
        pieces.append("-1")
    encoded = "".join(pieces)
    require("(" not in encoded and ")" not in encoded and "**" not in encoded,
            "noncanonical msolve syntax escaped encoder")
    return encoded


def expected_f0():
    b0 = C.variable(C.names.index("b0"))
    b1 = C.variable(C.names.index("b1"))
    b3 = C.variable(C.names.index("b3"))
    d4 = C.variable(C.names.index("d4"))
    d5 = C.variable(C.names.index("d5"))
    return C.multiply(b0, b1, b3, d4, d5,
                      C.add(C.multiply(b1, d4), C.multiply(b0, d5)))


def profile(poly):
    return {"terms": len(poly), "degree": max(map(sum, poly))}


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    frozen = json.loads(CRAMER_AUDIT.read_text())
    require(tuple(frozen["transported_row_labels"]) == SOURCE_LABELS,
            "frozen transported labels changed")
    require(tuple(frozen["transported_row_term_counts"]) == EXPECTED_TERMS,
            "frozen transported term counts changed")

    data = D.cramer_branch_system(7, 12)
    source_rows = tuple(data["open_rows"])
    require(tuple(label for label, _ in source_rows) == SOURCE_LABELS,
            "source row order changed")
    require(tuple(len(poly) for _, poly in source_rows) == EXPECTED_TERMS,
            "source row profiles changed")
    live = tuple(data["open_live_factors"])
    require(len(live) == len(LIVE_LABELS), "open live-factor interface changed")
    require(C.add(live[0], C.scale(expected_f0(), -1)) == {},
            "F0 source factor changed")
    require(live[2] == data["determinant"], "P26 factor order changed")
    require(live[3] == data["numerator_a4"], "N4 factor order changed")
    require(live[4] == data["numerator_a5"], "N5 factor order changed")
    require(live[5] == data["live_a2_numerator"],
            "A2hat factor order changed")

    row_terms = tuple((label, active_terms(poly))
                      for label, poly in source_rows)
    live_terms = tuple((label, active_terms(poly))
                       for label, poly in zip(LIVE_LABELS, live, strict=True))
    localizer_source = C.multiply(*live)
    localizer_terms = active_terms(localizer_source)

    labelled = [(f"source_{label}", encode_terms(poly))
                for label, poly in row_terms]
    labelled.append(("RAB_F0_A3hat_P26_N4_N5_A2hat", encode_terms(
        localizer_terms, include_z=True, constant_minus_one=True)))
    INPUT.write_text(",".join(VARIABLE_NAMES) + "\n0\n" +
                     ",\n".join(poly for _, poly in labelled) + "\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "source_labels": list(SOURCE_LABELS),
        "localized_factors_in_product_order": list(LIVE_LABELS),
        "scope": "exact P26-open fully-live transported Cramer chart",
    }, indent=2, sort_keys=True) + "\n")

    parsed = MSOLVE_IO.read_msolve_input(
        INPUT, strict=True, allow_characteristic_zero=True)
    require(parsed.variables == VARIABLE_NAMES and parsed.characteristic == 0,
            "strict characteristic-zero parse changed")
    require(len(parsed.polynomials) == len(SOURCE_LABELS) + 1,
            "strict polynomial count changed")

    # Local mutation guards for a source coefficient and the P26 factor.
    first_terms = dict(row_terms[0][1])
    first_exponent = max(first_terms, key=lambda item: (sum(item), item))
    first_terms[first_exponent] *= -1
    require(MSOLVE_IO.polynomial_sha256(encode_terms(first_terms)) !=
            parsed.polynomial_sha256[0],
            "source coefficient mutation did not fire")
    p26_mutated = dict(live[2])
    p26_exponent = min(p26_mutated)
    p26_mutated[p26_exponent] *= -1
    mutated_localizer = active_terms(C.multiply(
        live[0], live[1], p26_mutated, live[3], live[4], live[5]))
    require(MSOLVE_IO.polynomial_sha256(encode_terms(
        mutated_localizer, include_z=True, constant_minus_one=True)) !=
        parsed.polynomial_sha256[-1],
        "P26 localizer mutation did not fire")

    old_export = json.loads(OLD_EXPORT.read_text())
    old_manifest = json.loads(OLD_MANIFEST.read_text())
    f0_expanded = encode_terms(live_terms[0][1])
    require(old_export["base_factor_expanded"] == f0_expanded,
            "old P26=0 manifest F0 coefficient changed")
    require(old_manifest["solution"] == {
        "degree": 0, "kind": "empty", "variable_count": 8},
        "old P26=0 manifest sentinel changed")

    result = {
        "status": "UNAUDITED exact source/export replay PASS",
        "characteristic": 0,
        "variables": list(VARIABLE_NAMES),
        "source_labels": list(SOURCE_LABELS),
        "source_profiles": [
            {"source_label": label, **profile(poly),
             "primitive_polynomial_sha256": digest}
            for (label, poly), digest in zip(
                row_terms, parsed.polynomial_sha256[:-1], strict=True)],
        "localized_factors": [
            {"label": label, **profile(poly),
             "expanded_sha256": MSOLVE_IO.polynomial_sha256(
                 encode_terms(poly))}
            for label, poly in live_terms],
        "rabinowitsch_product_order": list(LIVE_LABELS),
        "rabinowitsch_coefficient_terms": len(localizer_terms),
        "rabinowitsch_coefficient_degree": max(map(sum, localizer_terms)),
        "rabinowitsch_coefficient_sha256": MSOLVE_IO.polynomial_sha256(
            encode_terms(localizer_terms)),
        "rabinowitsch_row_sha256": parsed.polynomial_sha256[-1],
        "old_manifest_comparison": {
            "old_scope": "P26=0 with F0 nonzero",
            "old_logical_sha256": old_manifest["logical_sha256"],
            "old_input_file_sha256": old_export["input_file_sha256"],
            "old_z_coefficient": old_export["base_factor_expanded"],
            "old_z_coefficient_terms": old_export["base_factor_terms"],
            "exact_F0_match": True,
            "new_z_coefficient_exact_factor_extension":
                "F0*A3hat*P26*N4*N5*A2hat",
        },
        "source_path": str(DISCOVERY.relative_to(REPO)),
        "source_sha256": sha256(DISCOVERY.read_bytes()).hexdigest(),
        "frozen_cramer_audit_path": str(CRAMER_AUDIT.relative_to(REPO)),
        "frozen_cramer_audit_sha256": sha256(CRAMER_AUDIT.read_bytes()).hexdigest(),
        "input_path": INPUT.name,
        "input_bytes": INPUT.stat().st_size,
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "labels_path": LABELS.name,
        "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        "must_fire": [
            "strict parenthesis/**/coefficient-after-symbol rejection",
            "negating source row8 leading coefficient changes row8 digest",
            "negating a P26 coefficient changes Rabinowitsch digest",
            "old boundary F0 expansion matches exactly",
        ],
        "scope_guard": (
            "The nine transported rows are asserted only on P26 nonzero. "
            "The Rabinowitsch product includes P26 and every frozen open-live "
            "factor, including N5; hence a literal exact-Q [-1] closes the "
            "fully-live P26 interior.  No inference at P26=0 is made."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TP P26 interior exact-Q export: PASS")
    print("rows", [profile(poly) for _, poly in row_terms])
    print("live", [(label, profile(poly)) for label, poly in live_terms])
    print("rab", profile(localizer_terms), "bytes", INPUT.stat().st_size)
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
