#!/usr/bin/env python3
"""Exact homogenized source lifts for two lower recursive face units."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_recursive_face_charts.json"
OUT = HERE / "results_recursive_face_exact_units.json"
TARGETS = (("0:13:1", 6, True), ("0:15:3", 8, False))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def combined_base_c(record):
    factors = []
    for label in ("selected_base_terms", "both_live_c_numerators"):
        value = record["localizers"][label]
        require(value.endswith("-1") and "*(" in value,
                "unexpected localizer encoding")
        factors.append(value[value.index("*(") + 1:-2])
    return "s*" + "*".join(factors) + "-1"


def exact_lift(record, target_power, serialize_lift):
    labels = [row["label"] for row in record["rows"]] + ["SAT_base_c"]
    generators = [row["polynomial"] for row in record["rows"]]
    generators.append(combined_base_c(record))
    names = record["variable_names"] + ["s"]
    names = [name for name in names
             if any(re.search(rf"\b{re.escape(name)}\b", generator)
                    for generator in generators)]
    names.append("t")
    prints = "".join(
        f'print("BEGIN_COEFF_{index}");print(string(L[{index + 1},1]));'
        f'print("END_COEFF_{index}");'
        for index in range(len(generators))
    )
    lift_setup = (
        f"poly target=t^{target_power};matrix L=lift(J,ideal(target));"
        "matrix MJ[1][size(J)]=J;matrix C=MJ*L;"
        if serialize_lift else f"poly target=t^{target_power};"
    )
    product_check = ("print(string(C[1,1]-target));"
                     if serialize_lift else 'print("NOT_SERIALIZED");')
    command = (
        f"ring R=0,({','.join(names)}),dp;"
        f"ideal I={','.join(generators)};ideal J=homog(I,t);"
        "ideal G=slimgb(J);"
        f"{lift_setup}print(\"BEGIN_CHECK\");{product_check}"
        "print(string(reduce(target,G)));"
        f"print(string(reduce(t^{target_power - 1},G)));"
        "print(\"END_CHECK\");"
        f"{prints if serialize_lift else ''}quit;"
    )
    completed = subprocess.run(
        ["Singular", "-q", "-c", command], text=True,
        capture_output=True, timeout=(60 if serialize_lift else 30), check=False,
    )
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular exact lift failed: " + completed.stderr[-1000:])
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN_CHECK"), lines.index("END_CHECK")
    checks = lines[begin + 1:end]
    require(len(checks) == 3
            and checks[0] == ("0" if serialize_lift else "NOT_SERIALIZED")
            and checks[1] == "0" and checks[2] != "0",
            "homogeneous lift/minimality changed")
    coefficients = []
    if serialize_lift:
        for index, label in enumerate(labels):
            begin_marker, end_marker = (f"BEGIN_COEFF_{index}",
                                        f"END_COEFF_{index}")
            begin, end = lines.index(begin_marker), lines.index(end_marker)
            coefficient = "".join(lines[begin + 1:end])
            coefficients.append({"label": label,
                                 "coefficient": coefficient})
    nonzero = [row for row in coefficients if row["coefficient"] != "0"]
    source_nonzero = [row for row in nonzero if row["label"] != "SAT_base_c"]
    if serialize_lift:
        require(source_nonzero, "lift uses no literal source row")
    return {
        "key": record["key"],
        "target": f"t^{target_power}",
        "minimal_t_power": target_power,
        "ring_variables": names,
        "raw_source_row_count": len(record["rows"]),
        "generator_count": len(generators),
        "nonzero_coefficient_count": len(nonzero),
        "coefficient_character_count": sum(len(row["coefficient"])
                                             for row in coefficients),
        "coefficients": coefficients,
        "exact_matrix_product_replay": serialize_lift,
        "source_multiplier_ledger_status": (
            "SERIALIZED" if serialize_lift else "TIMEOUT at 300 seconds"
        ),
        "target_remainder": "0",
        "previous_t_power_remainder_nonzero": checks[2],
        "localized_H": False,
        "localized_both_live_a_d": False,
        "localized": ["selected_base_terms", "both_live_c_numerators"],
    }


def main():
    payload = json.loads(INPUT.read_text())
    by_key = {record["key"]: record for record in payload["states"]}
    records = [exact_lift(by_key[key], power, serialize)
               for key, power, serialize in TARGETS]
    result = {
        "status": "UNAUDITED exact homogenized recursive face units",
        "records": records,
        "conclusion": (
            "The recursive faces (0,13,1) and (0,15,3) are empty after "
            "localizing only their selected base terms and remaining c "
            "numerators.  This is stronger than their H-live both-term scope."
        ),
        "scope_guard": (
            "Each t^N identity is in the full homogenized source ideal; "
            "dehomogenizing t=1 is a literal affine unit certificate."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("two recursive face exact units: PASS")
    print([(record["key"], record["target"],
            record["nonzero_coefficient_count"],
            record["coefficient_character_count"])
           for record in records])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
