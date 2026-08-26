#!/usr/bin/env python3
"""Export Q and all fifteen literal consistency minors for modular F4SAT.

Every solution of the six-row affine-linear packet makes the augmented
6-by-4 matrix have rank at most three, hence kills all fifteen maximal
minors.  Emptiness of this necessary determinantal locus on the displayed
chart-live open set would therefore close the packet branch.  A nonunit or
a modular unit alone is not a characteristic-zero theorem.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_branch0_cycle_delta_au_open_generic.py"
TOOLKIT = HERE.parent / "toolkit" / "groebner"
INPUT = HERE / "branch0_cycle_delta_au_open_all_minors_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_delta_au_open_all_minors_labels.json"
RESULT = HERE / "results_branch0_cycle_delta_au_open_all_minors_export.json"
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


AUDIT = load("n8_cycle_delta_all_minor_export_audit", AUDIT_PATH)
sp = AUDIT.sp
SOURCE = AUDIT.SOURCE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encode(poly):
    return str(sp.expand(poly)).replace("**", "^")


def open_core(matrix, selected, derived, b0, b1, d1, d4, x):
    value = sp.cancel(AUDIT.determinant4(matrix, selected).subs(
        d4, derived["d4_value"])).as_numer_denom()[0]
    value = sp.rem(sp.Poly(value, b0, domain="QQ(b1,d1,x)"),
                   sp.Poly(derived["q"], b0,
                           domain="QQ(b1,d1,x)")).as_expr()
    value = sp.cancel(value).as_numer_denom()[0]
    poly = sp.Poly(value, b0, b1, d1, x)
    content = tuple(min(monomial[index] for monomial, _ in poly.terms())
                    for index in range(4))
    monomial = b0**content[0]*b1**content[1]*d1**content[2]*x**content[3]
    core = poly.exquo(sp.Poly(monomial, b0, b1, d1, x)).as_expr()
    return core, content


def derive_minors(rows, derived):
    b0, b1, _, d1, _, d4 = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    normalized = AUDIT.INTERFACE.derive(rows)[6]
    live_row_factors = (b1**2*d1**2*x, 1, 1,
                        d4**2*x, b1*x, d1*d4)
    matrix = [[sp.cancel(entry/live_row_factors[row])
               for entry in entries]
              for row, entries in enumerate(normalized)]
    minors = []
    contents = []
    selections = list(itertools.combinations(range(6), 4))
    for selected in selections:
        core, content = open_core(
            matrix, selected, derived, b0, b1, d1, d4, x)
        minors.append(core)
        contents.append(content)
    return selections, minors, contents


def main():
    raw_rows, _ = SOURCE.SOURCE.data()
    raw = {label: poly for label, poly, _ in raw_rows}
    rows = {label: SOURCE.expression(poly) for label, poly, _ in raw_rows}
    derived = AUDIT.derive(rows)
    selections, minors, contents = derive_minors(rows, derived)
    b0, b1, _, d1, _, _ = SOURCE.PARAMETERS
    x = sp.Symbol("x")
    d4_numerator = sp.cancel(derived["d4_value"]).as_numer_denom()[0]
    live = sp.expand(
        b0*b1*d1*x*(b1+d1)*(x-1)*derived["au"]
        * d4_numerator*derived["a"])
    polynomials = [derived["q"], *minors, live]
    labels = ["Q", *("minor_" + "".join(map(str, selected))
                         for selected in selections), "live_saturator"]
    INPUT.write_text(
        "b0,b1,d1,x\n" + str(PRIME) + "\n"
        + ",\n".join(encode(poly) for poly in polynomials) + "\n")
    LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")
    parsed = read_msolve_input(INPUT, strict=True)
    require(len(parsed.polynomials) == 17,
            "strict parser lost an all-minor row")

    # A literal t_013 mutation changes exactly the minors containing row 1;
    # Q and every minor avoiding row 1 remain byte-identical.
    mutated_raw = dict(raw["t_013"])
    key = sorted(mutated_raw)[0]
    mutated_raw[key] = -mutated_raw[key]
    mutated_rows = dict(rows)
    mutated_rows["t_013"] = SOURCE.expression(mutated_raw)
    mutated_derived = AUDIT.derive(mutated_rows)
    _, mutated_minors, _ = derive_minors(mutated_rows, mutated_derived)
    require(derived["q"] == mutated_derived["q"],
            "the packet-row mutation changed Q")
    for selected, original, mutated in zip(
            selections, minors, mutated_minors):
        require((original != mutated) == (1 in selected),
                f"the t_013 mutation had wrong support at {selected}")

    result = {
        "status": "UNAUDITED all-minor modular F4SAT export",
        "prime": PRIME,
        "variables": ["b0", "b1", "d1", "x"],
        "labels": labels,
        "minor_rows": [list(selected) for selected in selections],
        "removed_live_monomials": [list(content) for content in contents],
        "row_terms": [len(sp.Poly(poly, b0, b1, d1, x).terms())
                      for poly in polynomials],
        "row_sha256": [sha256(encode(poly).encode("ascii")).hexdigest()
                       for poly in polynomials],
        "input_file": INPUT.name,
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "scope": (
            "Necessary determinantal obstruction on the exact localized "
            "Delta=0,Bplus!=0,Au!=0,A!=0 chart. A unit after exact-Q "
            "replay would close the full packet branch. A modular unit is "
            "only discovery; a nonunit may contain rank-deficient false "
            "positives and is not a packet counterexample."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta/Au-open all-minor export: PASS")
    print("minor term range:", min(result["row_terms"][1:-1]),
          max(result["row_terms"][1:-1]))
    print("input sha256:", result["input_file_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
