#!/usr/bin/env python3
"""Export Q plus three literal consistency minors for guarded msolve.

The third minor uses normalized packet rows (1,2,3,4).  Together with the
two previously audited minors it removes the sole modular parameter-curve
component of either pair, leaving a zero-dimensional exceptional locus to
classify.  This export is modular discovery only.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"
TOOLKIT = HERE.parent / "toolkit" / "groebner"
INPUT = HERE / "branch0_cycle_delta_au_open_three_minor_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_delta_au_open_three_minor_labels.json"
RESULT = HERE / "results_branch0_cycle_delta_au_open_three_minor_export.json"
PRIME = 1073741827

if str(TOOLKIT) not in sys.path:
    sys.path.append(str(TOOLKIT))
from msolve_io import read_msolve_input  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("n8_cycle_delta_three_minor_audit", AUDIT_PATH)
sp = AUDIT.sp
SOURCE = AUDIT.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def third_minor(rows, derived):
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    normalized = AUDIT.INTERFACE.derive(rows)[6]
    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row])
               for entry in entries]
              for row, entries in enumerate(normalized)]
    return AUDIT.minor_core(
        matrix, (1, 2, 3, 4), d4, derived["d4_value"], derived["q"],
        b0, b1, x, d1)


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    derived = AUDIT.derive(rows)
    third = third_minor(rows, derived)
    b0, b1, _, d1, _, _ = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    d4_numerator = sp.cancel(derived["d4_value"]).as_numer_denom()[0]
    live = sp.expand(
        b0*b1*d1*x*(b1+d1)*(x-1)*derived["au"]
        * d4_numerator*derived["a"])
    polynomials = (derived["q"], derived["left"], derived["right"],
                   third, live)
    labels = ["Q", "minor_2345", "minor_0234", "minor_1234",
              "live_saturator"]
    INPUT.write_text(
        "b0,b1,d1,x\n" + str(PRIME) + "\n"
        + ",\n".join(encode(poly) for poly in polynomials) + "\n")
    LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")
    parsed = read_msolve_input(INPUT, strict=True)
    require(len(parsed.polynomials) == 5,
            "strict parser lost an exported row")

    # Hostile source mutation: t_013 is row 1.  It changes precisely the new
    # minor among the three selected row sets.
    mutated_raw = dict(raw["t_013"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["t_013"] = SOURCE.expression(mutated_raw)
    mutated_derived = AUDIT.derive(mutated_rows)
    mutated_third = third_minor(mutated_rows, mutated_derived)
    require(derived["q"] == mutated_derived["q"]
            and derived["left"] == mutated_derived["left"]
            and derived["right"] == mutated_derived["right"]
            and third != mutated_third,
            "the literal t_013 mutation did not fire only in the new minor")

    result = {
        "status": "UNAUDITED three-minor modular msolve export",
        "prime": PRIME,
        "variables": ["b0", "b1", "d1", "x"],
        "labels": labels,
        "row_terms": [len(sp.Poly(poly, b0, b1, d1, x).terms())
                      for poly in polynomials],
        "row_sha256": [sha256(encode(poly).encode("ascii")).hexdigest()
                       for poly in polynomials],
        "input_file": INPUT.name,
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "scope": (
            "Modular discovery for Delta=0,Bplus!=0,Au!=0,A!=0 only. "
            "The final row is the expanded chart-live saturator. Selected "
            "p_i+1 factors are absent after projection, so a negative "
            "modular result is nonterminal; exact full-packet replay is "
            "required."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au-open three-minor export: PASS")
    print("terms:", result["row_terms"])
    print("input sha256:", result["input_file_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
