#!/usr/bin/env python3
"""Build exact b0-free determinants between Cof(1,3) and all minors.

For ``G=g1*b0+g0`` and every all-minor row ``f=f1*b0+f0``, any common
zero satisfies the fraction-free identity ``g1*f0-g0*f1=0``.  This file
uses the strict expanded integer ledger and FLINT only; it never divides
by either leading coefficient.  Integer/monomial content is recorded and
the remaining primitive is factored exactly over Z.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "build_cofactor13_b0_resultants_flint.py"
LABELS_PATH = (HERE.parent /
    "unaudited-codex-k4-cycle-char0-rur-referee-2026-08-21" /
    "cofactor13_all_minors_labels.json")
OUT = HERE / "results_cofactor13_b0_minor_determinants_flint.json"
FACTORS_OUT = HERE / "cofactor13_b0_minor_large_factors.jsonl"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("cofactor13_flint_base", BASE_PATH)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def factor_record(poly):
    unit, factors = poly.factor()
    require(int(unit) in (-1, 1), "primitive factor unit changed")
    return [{"multiplicity": int(multiplicity), **BASE.profile(factor)}
            for factor, multiplicity in factors]


def main():
    ledgers = [BASE.read_rows(path) for path in BASE.INPUTS]
    require(ledgers[0][1] == ledgers[1][1],
            "two-prime integer ledgers diverged")
    rows = ledgers[0][1]
    labels = json.loads(LABELS_PATH.read_text())["labels"]
    require(len(labels) == len(rows) == 18 and labels[0] == "Q"
            and labels[16] == "cofactor_1_3_cramer_homogenized",
            "label ledger changed")
    g = BASE.parse_b0_coefficients(rows[16])
    require(set(g) == {0, 1}, "G stopped being affine-linear in b0")
    g1, g0 = g[1], g[0]
    records = []
    factor_lines = []
    for index in range(1, 16):
        f = BASE.parse_b0_coefficients(rows[index])
        require(set(f).issubset({0, 1}),
                f"{labels[index]} stopped being affine-linear in b0")
        f1 = f.get(1, BASE.CTX.constant(0))
        f0 = f.get(0, BASE.CTX.constant(0))
        determinant = g1*f0-g0*f1
        primitive, scalar, monomial = BASE.normalized(determinant)
        b1, d1, x = BASE.CTX.gens()
        removed = b1**monomial[0]*d1**monomial[1]*x**monomial[2]
        require(determinant == scalar*removed*primitive,
                f"{labels[index]} normalization failed")
        factors = primitive.factor()[1]
        large_factor, large_multiplicity = max(
            factors, key=lambda value: len(value[0]))
        require(int(large_multiplicity) == 1,
                f"{labels[index]} large factor multiplicity changed")
        large_encoded = str(large_factor).replace("**", "^")
        factor_lines.append(json.dumps({"source_label": labels[index],
                                        "polynomial": large_encoded},
                                       separators=(",", ":")))
        records.append({
            "source_index": index,
            "source_label": labels[index],
            "source_b0_degrees": sorted(f),
            "raw_profile": BASE.profile(determinant),
            "removed_integer_content_signed": scalar,
            "removed_chart_live_monomial_b1_d1_x": list(monomial),
            "primitive_profile": BASE.profile(primitive),
            "factor_profiles": factor_record(primitive),
            "large_factor_profile": BASE.profile(large_factor),
        })

    # Hostile swap changes the first determinant.
    require(records[0]["primitive_profile"]["sha256"] !=
            records[1]["primitive_profile"]["sha256"],
            "minor-label mutation did not fire")
    FACTORS_OUT.write_text("\n".join(factor_lines) + "\n")
    result = {
        "status": "UNAUDITED exact FLINT b0-minor determinants PASS",
        "identity": "E_f=g1*f0-g0*f1 for G=g1*b0+g0, f=f1*b0+f0",
        "cofactor_source_label": labels[16],
        "records": records,
        "input_file_sha256": [sha256(path.read_bytes()).hexdigest()
                              for path in BASE.INPUTS],
        "large_factors_path": FACTORS_OUT.name,
        "large_factors_file_sha256": sha256(
            FACTORS_OUT.read_bytes()).hexdigest(),
        "scope": (
            "Every primitive is a necessary exact condition for the "
            "corresponding minor together with Cof(1,3). Factors are "
            "reported without declaring any nonmonomial factor live."
        ),
        "must_fire": "the first two differently labelled minors differ",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Cof(1,3) b0-minor determinants: PASS")
    for record in records:
        print(record["source_label"], record["primitive_profile"],
              "factors", [(value["terms"], value["total_degree"],
                           value["multiplicity"])
                          for value in record["factor_profiles"]])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
