#!/usr/bin/env python3
"""Export the canonical characteristic-zero TP P26=0 base-localized core.

The eight exact rows are the frozen greedy core

    7,8,9,10,12,15,19,101,

where 101 is the reduced determinant P26.  The only localization is

    F0=b0*b1*b3*d4*d5*(b1*d4+b0*d5).

The Rabinowitsch row is expanded termwise with every integer coefficient
printed before every symbolic factor.  This deliberately does not reuse the
old exporter whose ``z*2*monomial`` terms exposed an msolve parser ambiguity.
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
ROW_CORE = SOURCE_DIR / "results_branch0_triangle_pendant_p26_base_row_core.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
INPUT = HERE / "tp_p26_base_core_char0.msolve"
LABELS = HERE / "tp_p26_base_core_char0_labels.json"
RESULT = HERE / "results_tp_p26_base_core_char0_export.json"
CORE_LABELS = (7, 8, 9, 10, 12, 15, 19, 101)
ACTIVE_NAMES = ("a4", "a5", "b0", "b1", "b3", "d4", "d5")
VARIABLE_NAMES = ("z", *ACTIVE_NAMES)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("tp_p26_char0_exact_source", DISCOVERY)
C = D.CHART
MSOLVE_IO = load("tp_p26_char0_msolve_io", TOOLKIT)
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
    """Return an exact seven-variable integer dictionary."""
    answer = {}
    for exponent, coefficient in primitive_integer(poly).items():
        require(all(exponent[index] == 0 for index in range(C.n)
                    if index not in ACTIVE_INDICES),
                ("source row escaped active variables", exponent))
        key = tuple(exponent[index] for index in ACTIVE_INDICES)
        require(key not in answer, "projected monomial collision")
        answer[key] = int(coefficient)
    return answer


def encode_terms(poly, include_z=False, constant_minus_one=False):
    """Encode an integer dictionary coefficient-first and parenthesis-free."""
    pieces = []
    names = ACTIVE_NAMES
    for position, exponent in enumerate(sorted(
            poly, key=lambda item: (sum(item), item), reverse=True)):
        coefficient = int(poly[exponent])
        require(coefficient != 0, "explicit zero coefficient")
        symbolic = []
        if include_z:
            symbolic.append("z")
        symbolic.extend(name + (f"^{power}" if power != 1 else "")
                        for name, power in zip(names, exponent, strict=True)
                        if power)
        magnitude = abs(coefficient)
        factors = []
        if magnitude != 1 or not symbolic:
            factors.append(str(magnitude))
        factors.extend(symbolic)
        body = "*".join(factors)
        if position == 0:
            pieces.append(("-" if coefficient < 0 else "") + body)
        else:
            pieces.append(("-" if coefficient < 0 else "+") + body)
    require(pieces, "empty encoded polynomial")
    if constant_minus_one:
        pieces.append("-1")
    encoded = "".join(pieces)
    require("(" not in encoded and ")" not in encoded and "**" not in encoded,
            "noncanonical msolve syntax escaped encoder")
    # The critical hostile parser form is a number after a symbolic factor.
    require(not any(part and part[0].isalpha() and "*" in part and
                    part.split("*", 1)[1].split("*", 1)[0].isdigit()
                    for part in encoded.replace("-", "+").split("+")),
            "coefficient-after-symbol encoding")
    return encoded


def expected_base():
    b0 = C.variable(C.names.index("b0"))
    b1 = C.variable(C.names.index("b1"))
    b3 = C.variable(C.names.index("b3"))
    d4 = C.variable(C.names.index("d4"))
    d5 = C.variable(C.names.index("d5"))
    return C.multiply(b0, b1, b3, d4, d5,
                      C.add(C.multiply(b1, d4), C.multiply(b0, d5)))


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    frozen_core = json.loads(ROW_CORE.read_text())
    require(tuple(frozen_core["final_labels"]) == CORE_LABELS,
            "frozen two-prime core labels changed")
    data = D.cramer_branch_system(7, 12)
    all_rows = {label: poly for label, poly in data["closed_rows"]}
    require(tuple(all_rows) == (7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 21,
                                101),
            "exact P26 boundary row interface changed")
    base = data["closed_live_factors"][0]
    require(C.add(base, C.scale(expected_base(), -1)) == {},
            "base F0 factor changed")

    row_terms = [(label, active_terms(all_rows[label]))
                 for label in CORE_LABELS]
    base_terms = active_terms(base)
    labelled = [(f"source_{label}", encode_terms(poly))
                for label, poly in row_terms]
    labelled.append(("RAB_F0", encode_terms(
        base_terms, include_z=True, constant_minus_one=True)))
    INPUT.write_text(",".join(VARIABLE_NAMES) + "\n0\n" +
                     ",\n".join(poly for _, poly in labelled) + "\n")
    LABELS.write_text(json.dumps({
        "labels": [label for label, _ in labelled],
        "source_labels": list(CORE_LABELS),
        "localized_factor": "b0*b1*b3*d4*d5*(b1*d4+b0*d5)",
    }, indent=2, sort_keys=True) + "\n")

    parsed = MSOLVE_IO.read_msolve_input(
        INPUT, strict=True, allow_characteristic_zero=True)
    require(parsed.variables == VARIABLE_NAMES and parsed.characteristic == 0
            and len(parsed.polynomials) == 9,
            "strict characteristic-zero parse changed")
    # Mutation guard: flip the first source coefficient.  Exactly one
    # polynomial digest must change.
    first_terms = dict(row_terms[0][1])
    first_exponent = max(first_terms,
                         key=lambda item: (sum(item), item))
    first_terms[first_exponent] *= -1
    mutated = encode_terms(first_terms)
    require(MSOLVE_IO.polynomial_sha256(mutated) !=
            parsed.polynomial_sha256[0],
            "hostile source coefficient mutation did not fire")
    require(tuple(parsed.polynomial_sha256[1:]) == tuple(
        MSOLVE_IO.polynomial_sha256(poly) for _, poly in labelled[1:]),
        "mutation locality guard changed")

    profiles = []
    for (label, poly), (_, encoded), digest in zip(
            row_terms, labelled, parsed.polynomial_sha256, strict=False):
        profiles.append({
            "source_label": label,
            "terms": len(poly),
            "degree": max(map(sum, poly)),
            "primitive_polynomial_sha256": digest,
        })
    result = {
        "status": "UNAUDITED exact source/export replay PASS",
        "characteristic": 0,
        "variables": list(VARIABLE_NAMES),
        "source_labels": list(CORE_LABELS),
        "source_profiles": profiles,
        "base_factor_expanded": encode_terms(base_terms),
        "base_factor_terms": len(base_terms),
        "rabinowitsch_expanded": labelled[-1][1],
        "rabinowitsch_terms": len(base_terms) + 1,
        "localized_factors": ["b0", "b1", "b3", "d4", "d5",
                              "b1*d4+b0*d5"],
        "not_localized": ["P26", "a4", "a5", "H", "Cprod"],
        "source_path": str(DISCOVERY.relative_to(REPO)),
        "source_sha256": sha256(DISCOVERY.read_bytes()).hexdigest(),
        "frozen_core_path": str(ROW_CORE.relative_to(REPO)),
        "frozen_core_sha256": sha256(ROW_CORE.read_bytes()).hexdigest(),
        "input_path": INPUT.name,
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "input_polynomial_sha256": list(parsed.polynomial_sha256),
        "labels_path": LABELS.name,
        "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        "must_fire": [
            "strict parenthesis/**/coefficient-after-symbol rejection",
            "negating source row7 leading coefficient changes only row7",
        ],
        "scope_guard": (
            "A literal characteristic-zero [-1] plus independent source "
            "replay closes only the triangle-plus-pendant P26=0 boundary "
            "on F0 nonzero; it says nothing about P26!=0 or N5^3."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TP P26=0 base-core char0 export: PASS")
    print("terms", [profile["terms"] for profile in profiles],
          "rab", result["rabinowitsch_terms"])
    print("input", result["input_file_sha256"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
