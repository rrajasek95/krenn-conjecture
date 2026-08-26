#!/usr/bin/env python3
"""Exact ideal classification of the recursive face (B,T,D)=(0,30,12).

The check starts from all sixteen frozen, literal source rows.  It compares
their fully localized ideal with a small nine-relation presentation (plus the
unchanged localization equation) in both directions over Q.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_recursive_face_charts.json"
OUTPUT = HERE / "results_face_03012_component_classification.json"
KEY = "0:30:12"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def combined_localizer(record):
    factors = []
    for label in ("H", "selected_base_terms", "both_live_a_d",
                  "both_live_c_numerators"):
        value = record["localizers"][label]
        require(value.endswith("-1") and "*(" in value,
                f"unexpected {label} localizer encoding")
        factors.append(value[value.index("*(") + 1:-2])
    return "s*" + "*".join(factors) + "-1"


def singular_classification(record, mutate=False):
    source = [row["polynomial"] for row in record["rows"]]
    sat = combined_localizer(record)
    source.append(sat)
    relations = [
        "b0", "b5", "a1", "a4", "a3+b4+1", "b4*d3-1",
        ("a0*d3-a5" if mutate else "a0*d3+a5"),
        "a2+d3+1", "a5^2+a2-2*a5", sat,
    ]
    names = record["variable_names"] + ["s"]
    names = [name for name in names if any(
        re.search(rf"\b{re.escape(name)}\b", polynomial)
        for polynomial in source + relations)]
    command = (
        f"ring R=0,({','.join(names)}),dp;"
        f"ideal I={','.join(source)};ideal J={','.join(relations)};"
        "ideal GI=slimgb(I);ideal GJ=slimgb(J);"
        "ideal RIJ=reduce(GI,GJ);ideal RJI=reduce(GJ,GI);"
        'print("BEGIN");print(string(dim(GI)));print(string(dim(GJ)));'
        'print(string(size(GI)));print(string(size(GJ)));'
        'print("RIJ");print(RIJ);print("RJI");print(RJI);'
        'print("MUTREL");print(string(reduce(a0*d3+a5,GI)));'
        'print("END");quit;'
    )
    completed = subprocess.run(
        ["Singular", "-q", "-c", command], text=True,
        capture_output=True, timeout=30, check=False,
    )
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "exact Singular classification failed: " + completed.stderr)
    lines = completed.stdout.splitlines()
    begin, end = lines.index("BEGIN"), lines.index("END")
    body = lines[begin + 1:end]
    rij, rji, mutrel = (body.index("RIJ"), body.index("RJI"),
                        body.index("MUTREL"))
    header = body[:rij]
    require(len(header) == 4, f"unexpected header: {header}")
    return {
        "dimension_source_ideal": int(header[0]),
        "dimension_presentation_ideal": int(header[1]),
        "source_basis_size": int(header[2]),
        "presentation_basis_size": int(header[3]),
        "source_mod_presentation": "\n".join(body[rij + 1:rji]),
        "presentation_mod_source": "\n".join(body[rji + 1:mutrel]),
        "canonical_relation_mod_source": "\n".join(body[mutrel + 1:]),
        "active_ring_variables": names,
        "source_generator_count_including_localizer": len(source),
        "presentation_generator_count": len(relations),
    }


def main():
    payload = json.loads(INPUT.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    exact = singular_classification(record)
    require(exact["dimension_source_ideal"] == 1
            and exact["dimension_presentation_ideal"] == 1,
            "component dimension changed")
    require(set(exact["source_mod_presentation"].replace(" ", "").split(",\n"))
            <= {"0", "_[1]=0"},
            "source ideal is not contained in the presentation")
    require(set(exact["presentation_mod_source"].replace(" ", "").split(",\n"))
            <= {"0", "_[1]=0"},
            "presentation is not contained in source ideal")
    require(exact["canonical_relation_mod_source"] == "0",
            "canonical relation does not reduce to zero")
    mutation = singular_classification(record, mutate=True)
    require(mutation["presentation_mod_source"] != exact["presentation_mod_source"],
            "sign mutation failed to fire")

    result = {
        "status": "UNAUDITED exact recursive-face component classification",
        "key": KEY,
        "literal_source_raw_indices": [row["raw_index"]
                                       for row in record["rows"]],
        "localized_factors": ["H", "selected_base_terms",
                              "both_live_a_d", "both_live_c_numerators"],
        "exact_ideal_equality_over_Q": True,
        "presentation_relations": [
            "b0", "b5", "a1", "a4", "a3+b4+1", "b4*d3-1",
            "a0*d3+a5", "a2+d3+1", "a5^2+a2-2*a5",
            "the unchanged combined localization equation",
        ],
        "exact_singular_checks": exact,
        "parameterization": {
            "parameter": "r=a5",
            "q": "r^2-2*r-1=d3",
            "a0": "-r/q", "a1": "0", "a2": "r*(2-r)",
            "a3": "r*(2-r)/q", "a4": "0", "a5": "r",
            "b0": "0", "b1": "1", "b2": "1", "b3": "1",
            "b4": "1/q", "b5": "0", "d0": "q/r", "d1": "0",
            "d2": "1", "d3": "q", "d4": "0", "d5": "-1/r",
            "open_conditions": ["r!=0", "r!=2", "q!=0"],
            "pure_H": "4*r*(r-2)",
        },
        "mutation_control": "a0*d3+a5 changed to a0*d3-a5 and fired",
        "scope_guard": (
            "The equality is for the fully localized canonical face only. "
            "Boundary factors are separate nodes of the recursive face graph."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("(0,30,12) exact component classification: PASS")
    print("basis sizes/dimension:", exact["source_basis_size"],
          exact["presentation_basis_size"], exact["dimension_source_ideal"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
