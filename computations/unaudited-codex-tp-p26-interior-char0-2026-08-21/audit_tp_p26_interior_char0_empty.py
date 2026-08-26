#!/usr/bin/env python3
"""Independent exact replay of the TP P26-open characteristic-zero gate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE_DIR = (HERE.parent /
              "unaudited-codex-n8-orbit0-normalized-78-2026-08-20")
DISCOVERY = SOURCE_DIR / "discover_branch0_triangle_pendant_reduction.py"
CRAMER_AUDIT_SOURCE = SOURCE_DIR / "audit_branch0_triangle_pendant_cramer_n5.py"
CRAMER_RESULT = SOURCE_DIR / "results_branch0_triangle_pendant_cramer_n5.json"
BOUNDARY_DIR = HERE.parent / "unaudited-codex-tp-p26-boundary-char0-2026-08-21"
BOUNDARY_EXPORT = BOUNDARY_DIR / "results_tp_p26_base_core_char0_export.json"
BOUNDARY_MANIFEST = BOUNDARY_DIR / "results_tp_p26_base_core_char0.manifest.json"
INPUT = HERE / "tp_p26_interior_char0.msolve"
OUTPUT = HERE / "results_tp_p26_interior_char0.param.out"
MANIFEST = HERE / "results_tp_p26_interior_char0.manifest.json"
LABELS = HERE / "tp_p26_interior_char0_labels.json"
EXPORT_RESULT = HERE / "results_tp_p26_interior_char0_export.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
PARAM_RUNNER = REPO / "computations/toolkit/groebner/run_msolve_parametrize.py"
RESULT_PREFIX = HERE / "results_tp_p26_interior_char0_replay"

SOURCE_LABELS = (8, 9, 10, 11, 13, 15, 17, 19, 21)
EXPECTED_TERMS = (80, 106, 61, 222, 262, 164, 122, 91, 101)
LIVE_LABELS = ("F0", "A3hat", "P26", "N4", "N5", "A2hat")
ACTIVE_NAMES = ("b0", "b1", "b3", "d4", "d5")
VARIABLE_NAMES = ("z", *ACTIVE_NAMES)
INPUT_SHA = "6c8d379f399465c73e475c09314bee3a315f8f89ca40e941fcff845f561fbd73"
OUTPUT_SHA = "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
MANIFEST_LOGICAL = "2ca019ebd396746cd525d4eca2ac5a4cc4afbd59e27d55ad43d698ca3fa35466"
BOUNDARY_LOGICAL = "62019cf3279c50d713b276bd28bcf0abbcb4b6658f342dfae1f8a8316602a2aa"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("tp_p26_interior_replay_source", DISCOVERY)
C = D.CHART
CRAMER = load("tp_p26_interior_cramer_audit", CRAMER_AUDIT_SOURCE)
MSOLVE_IO = load("tp_p26_interior_replay_msolve_io", TOOLKIT)
sys.path.insert(0, str(TOOLKIT.parent))
PARAM = load("tp_p26_interior_replay_param_runner", PARAM_RUNNER)
ACTIVE_INDICES = tuple(C.names.index(name) for name in ACTIVE_NAMES)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path: Path):
    return sha256(path.read_bytes()).hexdigest()


def primitive_project(poly, reverse=False):
    """Clear rational content and project independently to five variables."""
    require(poly, "zero source row")
    denominator = math.lcm(*(value.denominator for value in poly.values()))
    integers = [value.numerator * (denominator // value.denominator)
                for value in poly.values()]
    content = math.gcd(*map(abs, integers))
    sign = -1 if poly[min(poly)] < 0 else 1
    items = list(poly.items())
    if reverse:
        items.reverse()
    answer = {}
    for exponent, value in items:
        require(all(exponent[index] == 0 for index in range(C.n)
                    if index not in ACTIVE_INDICES),
                ("source row escaped active variables", exponent))
        key = tuple(exponent[index] for index in ACTIVE_INDICES)
        coefficient = sign * value.numerator * (
            denominator // value.denominator) // content
        require(key not in answer and coefficient != 0,
                "projected collision/zero")
        answer[key] = coefficient
    return answer


def parse_encoded(value, names):
    """Parse the deliberately tiny coefficient-first msolve grammar."""
    value = "".join(value.split())
    if not value.startswith(("+", "-")):
        value = "+" + value
    pieces = re.findall(r"([+-])([^+-]+)", value)
    require("".join(sign + body for sign, body in pieces) == value,
            "unsupported msolve source syntax")
    answer = {}
    positions = {name: index for index, name in enumerate(names)}
    for sign, body in pieces:
        factors = body.split("*")
        coefficient = -1 if sign == "-" else 1
        if re.fullmatch(r"\d+", factors[0]):
            coefficient *= int(factors.pop(0))
        exponent = [0] * len(names)
        for factor in factors:
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?",
                                 factor)
            require(match is not None and match.group(1) in positions,
                    ("unsupported factor", factor))
            exponent[positions[match.group(1)]] += int(match.group(2) or 1)
        key = tuple(exponent)
        require(key not in answer, ("unexpanded/duplicate term", key))
        answer[key] = coefficient
    return answer


def dictionary_sha(value):
    return sha256(json.dumps(
        sorted((list(key), coefficient) for key, coefficient in value.items()),
        separators=(",", ":")).encode()).hexdigest()


def expected_f0():
    b0 = C.variable(C.names.index("b0"))
    b1 = C.variable(C.names.index("b1"))
    b3 = C.variable(C.names.index("b3"))
    d4 = C.variable(C.names.index("d4"))
    d5 = C.variable(C.names.index("d5"))
    return C.multiply(b0, b1, b3, d4, d5,
                      C.add(C.multiply(b1, d4), C.multiply(b0, d5)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()

    require(file_sha(INPUT) == INPUT_SHA and file_sha(OUTPUT) == OUTPUT_SHA,
            "frozen char0 input/output digest changed")
    parsed = MSOLVE_IO.read_msolve_input(
        INPUT, strict=True, allow_characteristic_zero=True)
    require(parsed.variables == VARIABLE_NAMES and parsed.characteristic == 0
            and len(parsed.polynomials) == 10,
            "strict input interface changed")
    labels = json.loads(LABELS.read_text())
    require(tuple(labels["source_labels"]) == SOURCE_LABELS and
            tuple(labels["localized_factors_in_product_order"]) == LIVE_LABELS,
            "labels/live-factor order changed")

    # Re-run the exact (non-modular) Cramer ledger.  This proves that the nine
    # transported rows and all six factors have the literal source meaning.
    exact_ledger = CRAMER.exact_ledger()
    data = D.cramer_branch_system(7, 12)
    require(exact_ledger["open_rows"] == data["open_rows"] and
            exact_ledger["open_live_factors"] == data["open_live_factors"],
            "independent Cramer reconstruction changed")
    rows = tuple(data["open_rows"])
    live = tuple(data["open_live_factors"])
    require(tuple(label for label, _ in rows) == SOURCE_LABELS and
            tuple(len(poly) for _, poly in rows) == EXPECTED_TERMS,
            "transported source row interface changed")
    require(len(live) == 6 and live[0] == expected_f0() and
            live[2] == data["determinant"] and
            live[3] == data["numerator_a4"] and
            live[4] == data["numerator_a5"] and
            live[5] == data["live_a2_numerator"],
            "open-live source interface changed")

    input_polys = tuple(parse_encoded(value, VARIABLE_NAMES)
                        for value in parsed.polynomials)
    order = list(range(len(rows)))
    if args.mode == "-O":
        order.reverse()
    row_checks = []
    for position in order:
        label, source = rows[position]
        expected = primitive_project(
            source, reverse=args.mode in ("-O", "-I-S"))
        actual_full = input_polys[position]
        require(all(exponent[0] == 0 for exponent in actual_full),
                f"source {label} acquired z")
        actual = {exponent[1:]: coefficient
                  for exponent, coefficient in actual_full.items()}
        require(actual == expected,
                f"literal monomial/coefficient replay failed for {label}")
        row_checks.append({"label": label, "terms": len(expected),
                           "degree": max(map(sum, expected)),
                           "dictionary_sha256": dictionary_sha(expected)})

    localizer_source = C.multiply(*live)
    expected_localizer = primitive_project(
        localizer_source, reverse=args.mode in ("-O", "-I-S"))
    expected_rab = {(1, *exponent): coefficient
                    for exponent, coefficient in expected_localizer.items()}
    expected_rab[(0, 0, 0, 0, 0, 0)] = -1
    require(input_polys[-1] == expected_rab,
            "full expanded Rabinowitsch product replay failed")
    require(len(expected_localizer) == 8506 and
            max(map(sum, expected_localizer)) == 40,
            "full Rabinowitsch profile changed")

    # Byte-level sentinel/runner checks.
    manifest = json.loads(MANIFEST.read_text())
    require(OUTPUT.read_text() == "[-1]:\n" and
            PARAM.parse_parametrization(OUTPUT, 0, 6) ==
            {"kind": "empty", "degree": 0, "variable_count": 6},
            "literal characteristic-zero empty sentinel changed")
    require(manifest["status"] ==
            "completed_characteristic_zero_parametrization" and
            manifest["solution"] ==
            {"kind": "empty", "degree": 0, "variable_count": 6} and
            manifest["logical_sha256"] == MANIFEST_LOGICAL and
            manifest["input"]["sha256"] == INPUT_SHA and
            manifest["timeout_seconds"] == 300 and
            manifest["characteristic_zero_explicit_opt_in"] is True and
            manifest["command"][-2:] == ["-P", "1"],
            "guarded exact-Q runner manifest changed")

    # Reconcile exactly with the complementary P26=0 closure.
    boundary_export = json.loads(BOUNDARY_EXPORT.read_text())
    boundary_manifest = json.loads(BOUNDARY_MANIFEST.read_text())
    f0 = primitive_project(live[0])
    require(boundary_manifest["logical_sha256"] == BOUNDARY_LOGICAL and
            boundary_manifest["solution"] ==
            {"kind": "empty", "degree": 0, "variable_count": 8} and
            boundary_export["base_factor_expanded"] ==
            "b0^2*b1*b3*d4*d5^2+b0*b1^2*b3*d4^2*d5" and
            set(f0) == {(2, 1, 1, 1, 2), (1, 2, 1, 2, 1)} and
            set(f0.values()) == {1},
            "old P26=0 F0 closure comparison changed")

    # Must-fire mutations: one transported coefficient, one factor inside
    # the localizer, and the two nonempty/malformed characteristic-zero
    # sentinels.
    mutated_row = dict(primitive_project(rows[0][1]))
    mutated_row[max(mutated_row, key=lambda item: (sum(item), item))] *= -1
    require(mutated_row != {exponent[1:]: coefficient for exponent, coefficient
                            in input_polys[0].items()},
            "source mutation did not fire")
    mutated_p26 = dict(live[2])
    mutated_p26[min(mutated_p26)] *= -1
    mutated_product = primitive_project(C.multiply(
        live[0], live[1], mutated_p26, live[3], live[4], live[5]))
    require(mutated_product != expected_localizer,
            "P26 localizer mutation did not fire")
    hostile_positive = HERE / ".hostile_positive_dimension.tmp"
    hostile_one = HERE / ".hostile_one.tmp"
    try:
        hostile_positive.write_text("[1,6,-1,[]]:\n")
        hostile_one.write_text("[1]:\n")
        require(PARAM.parse_parametrization(hostile_positive, 0, 6)["kind"] ==
                "positive_dimensional", "positive dimension accepted as empty")
        rejected_one = False
        try:
            PARAM.parse_parametrization(hostile_one, 0, 6)
        except ValueError:
            rejected_one = True
        require(rejected_one, "historical char0 [1] accepted")
    finally:
        hostile_positive.unlink(missing_ok=True)
        hostile_one.unlink(missing_ok=True)

    export_result = json.loads(EXPORT_RESULT.read_text())
    require(export_result["input_file_sha256"] == INPUT_SHA and
            export_result["rabinowitsch_coefficient_terms"] == 8506 and
            export_result["rabinowitsch_product_order"] == list(LIVE_LABELS),
            "export result ledger changed")
    result = {
        "status": "UNAUDITED exact char0 empty source replay PASS",
        "mode": args.mode,
        "branch": "triangle-plus-pendant P26!=0 fully-live interior",
        "theorem": (
            "V_Qbar(R8,R9,R10,R11,R13,R15,R17,R19,R21) intersect "
            "D(F0*A3hat*P26*N4*N5*A2hat) is empty."),
        "source_labels": list(SOURCE_LABELS),
        "row_checks": row_checks,
        "rabinowitsch_product_order": list(LIVE_LABELS),
        "rabinowitsch_coefficient_terms_degree": [8506, 40],
        "rabinowitsch_dictionary_sha256": dictionary_sha(expected_localizer),
        "empty_sentinel_exact": "[-1]:",
        "input_sha256": INPUT_SHA,
        "output_sha256": OUTPUT_SHA,
        "manifest_logical_sha256": MANIFEST_LOGICAL,
        "boundary_manifest_logical_sha256": BOUNDARY_LOGICAL,
        "coverage": (
            "The exact F0-open P26=0 gate and this fully-live P26-open gate "
            "cover the TP stratum by P26=0 or P26!=0."),
        "divisor_scope": (
            "A3hat=0, N4=0, N5=0, or A2hat=0 inside P26!=0 is outside this "
            "gate, but each violates a frozen TP live/support antecedent; no "
            "such divisor is an unresolved subchart of the TP stratum."),
        "must_fire": [
            "transported row8 coefficient mutation",
            "P26 factor mutation inside full Rab product",
            "positive-dimensional sentinel rejection",
            "historical characteristic-zero [1] rejection",
        ],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    output = Path(str(RESULT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
