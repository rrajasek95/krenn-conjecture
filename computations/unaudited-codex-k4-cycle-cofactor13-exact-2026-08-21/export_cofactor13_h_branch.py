#!/usr/bin/env python3
"""Export the exact ``h=d1^2*x-1`` branch in two variables.

The frozen F4SAT saturator proves the factors listed in ``LIVE`` are
nonzero.  On ``h=0`` the exact Q row factors as

  -(d1^2+1)(d1^2+2*d1-1)(b0-d1)(b0+d1).

All but ``b0-d1`` are live, so Q forces ``b0=d1``.  We substitute these
two exact relations in every all-minor row and the cleared Cof(1,3) row,
clear only a Laurent power of live d1, then divide exact live factors.
The resulting two-variable rows are equivalent in the localized chart.
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
ROWS_OUT = HERE / "cofactor13_h_branch_rows.jsonl"
SINGULAR_OUT = HERE / "cofactor13_h_branch_exact.sing"
LIFT_OUT = HERE / "cofactor13_h_branch_lift.sing"
RESULT = HERE / "results_cofactor13_h_branch_export.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = load("cofactor13_h_branch_base", BASE_PATH)
from flint import fmpz_mpoly_ctx  # noqa: E402

CTX = fmpz_mpoly_ctx.get(("b1", "d1"))
b1, d1 = CTX.gens()
LIVE = (
    b1, d1, b1+d1, d1-1, d1+1,
    d1**2+1, d1**2+2*d1-1,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def poly_sha(poly):
    logical = [[[int(value) for value in exponent], int(coefficient)]
               for exponent, coefficient in sorted(poly.to_dict().items())]
    return sha256(json.dumps(logical, separators=(",", ":")).encode()).hexdigest()


def profile(poly):
    return {"terms": len(poly), "total_degree": int(poly.total_degree()),
            "degrees_b1_d1": [int(value) for value in poly.degrees()],
            "sha256": poly_sha(poly)}


def substitute_h_b0_d1(coefficients):
    """Substitute b0=d1, x=d1^-2 and clear a minimal d1 power."""
    terms = []
    minimum_d1 = 0
    for b0_power, coefficient_poly in coefficients.items():
        for (b1_power, d1_power, x_power), coefficient in \
                coefficient_poly.to_dict().items():
            new_d1 = int(d1_power)-2*int(x_power)+int(b0_power)
            minimum_d1 = min(minimum_d1, new_d1)
            terms.append((int(b1_power), new_d1, int(coefficient)))
    shift = -minimum_d1
    values = {}
    for b1_power, d1_power, coefficient in terms:
        exponent = (b1_power, d1_power+shift)
        values[exponent] = values.get(exponent, 0)+coefficient
    return CTX.from_dict({key: value for key, value in values.items() if value}), shift


def strip_live(poly):
    unit, factors = poly.factor()
    kept = CTX.constant(int(unit))
    removed = []
    for factor, multiplicity in factors:
        match = next((index for index, live in enumerate(LIVE)
                      if factor == live or factor == -live), None)
        if match is None:
            kept *= factor**int(multiplicity)
        else:
            removed.append({"live_factor_index": match,
                            "live_factor": str(LIVE[match]),
                            "multiplicity": int(multiplicity)})
    # Normalize the retained scalar sign/content and no monomial division:
    # all monomial live factors were already explicit in the factorization.
    values = kept.to_dict()
    require(values, "retained row unexpectedly zero")
    lead = values[max(values)]
    if lead < 0:
        kept = -kept
    return kept, removed


def main():
    ledgers = [BASE.read_rows(path) for path in BASE.INPUTS]
    require(ledgers[0][1] == ledgers[1][1],
            "two-prime exact ledgers diverged")
    rows = ledgers[0][1]
    labels = json.loads(LABELS_PATH.read_text())["labels"]
    require(labels[16] == "cofactor_1_3_cramer_homogenized",
            "Cof label changed")

    q_branch, q_shift = substitute_h_b0_d1(
        BASE.parse_b0_coefficients(rows[0]))
    require(not q_branch, "Q did not vanish after its forced h-branch root")
    records = []
    retained_rows = []
    for index in range(1, 17):
        branch, shift = substitute_h_b0_d1(
            BASE.parse_b0_coefficients(rows[index]))
        require(branch, f"{labels[index]} vanished identically")
        retained, removed = strip_live(branch)
        records.append({"source_index": index,
                        "source_label": labels[index],
                        "cleared_laurent_d1_power": shift,
                        "cleared_profile": profile(branch),
                        "removed_live_factors": removed,
                        "retained_profile": profile(retained)})
        retained_rows.append((labels[index], retained))

    ROWS_OUT.write_text("\n".join(json.dumps(
        {"source_label": label,
         "polynomial": str(poly).replace("**", "^")},
        separators=(",", ":")) for label, poly in retained_rows) + "\n")
    encoded = [str(poly).replace("**", "^") for _, poly in retained_rows]
    singular = (
        "option(redSB);\nring r=0,(b1,d1),dp;\n"
        "ideal I=" + ",\n".join(encoded) + ";\n"
        "ideal G=slimgb(I);\nprint(size(G));\nprint(G);\n"
    )
    SINGULAR_OUT.write_text(singular)
    lifted_rows = encoded + ["z*(b1+d1)-1"]
    lift_code = (
        "option(redSB);\nring r=0,(z,b1,d1),dp;\n"
        "ideal I=" + ",\n".join(lifted_rows) + ";\n"
        "matrix L=lift(I,ideal(1));\n"
        "ideal C=matrix(I)*L;\n"
        'print("CHECK"); print(C[1]-1); print("LIFT"); print(L);\n'
    )
    LIFT_OUT.write_text(lift_code)
    result = {
        "status": "UNAUDITED exact h-branch source export PASS",
        "branch_relations": ["d1^2*x-1=0", "b0-d1=0"],
        "Q_factorization_before_forcing_b0": (
            "-(d1^2+1)*(d1^2+2*d1-1)*(b0-d1)*(b0+d1)"
        ),
        "Q_laurent_clear_power": 6,
        "declared_live_factors_b1_d1": [str(value) for value in LIVE],
        "records": records,
        "rows_path": ROWS_OUT.name,
        "rows_file_sha256": sha256(ROWS_OUT.read_bytes()).hexdigest(),
        "singular_path": SINGULAR_OUT.name,
        "singular_file_sha256": sha256(SINGULAR_OUT.read_bytes()).hexdigest(),
        "lift_singular_path": LIFT_OUT.name,
        "lift_singular_file_sha256": sha256(
            LIFT_OUT.read_bytes()).hexdigest(),
        "input_file_sha256": [sha256(path.read_bytes()).hexdigest()
                              for path in BASE.INPUTS],
        "scope": (
            "The two-variable rows are exact localized consequences on "
            "the h=0 branch. A UNIT Groebner basis would be an exact "
            "branch closure; a nonunit result would not classify all "
            "components without further work."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Cof(1,3) h branch exact export: PASS")
    print("retained profiles:", [(label, profile(poly))
                                 for label, poly in retained_rows])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
