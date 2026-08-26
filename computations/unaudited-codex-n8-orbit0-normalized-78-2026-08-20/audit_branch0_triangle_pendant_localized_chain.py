#!/usr/bin/env python3
"""Exact localized reduction and modular unit for k4 triangle+pendant.

This audit separates two statements deliberately:

* exact over Q: four literal localized eliminations reduce the chart to eight
  geometric variables and twelve distinct residual source rows;
* discovery only: that residual is the unit ideal modulo 1009 and 1013.

No rational unit certificate is claimed here.  Direct Q Groebner runs timed
out; a modular unit is not a proof of characteristic-zero emptiness.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
DISCOVERY_PATH = HERE / "discover_branch0_triangle_pendant_reduction.py"
OUT = HERE / "results_branch0_triangle_pendant_localized_chain.json"
EXPECTED_LABELS = (7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 21, 100)


def load():
    spec = importlib.util.spec_from_file_location("n8_triangle_pendant",
                                                  DISCOVERY_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D = load()
C = D.CHART


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def e_relation():
    return C.add(
        C.variable(C.d_index[3]),
        C.multiply(C.variable(7), C.variable(C.d_index[4])),
        C.multiply(C.variable(6), C.variable(C.d_index[5])))


def exact_ledger():
    raw_rows, _ = D.gauged_rows()
    raw_map = dict(raw_rows)
    reduced, _, first_replacements = D.solve_a0_a3()
    reduced_map = dict(reduced)

    # R20 and R14 are literal source rows and vanish after their displayed
    # localized substitutions for a0 and a3.
    require(D.substitute_poly(raw_map[20], first_replacements) == {},
            "R20 did not solve a0 exactly")
    require(D.substitute_poly(raw_map[14], first_replacements) == {},
            "R14 did not solve a3 exactly")

    e = e_relation()
    lhs = C.add(reduced_map[6], reduced_map[18])
    rhs = C.scale(C.multiply(C.variable(9),
                             C.variable(C.d_index[5]), e), -2)
    require(lhs == rhs,
            "R6/R18 exact E-relation ledger changed")

    a2_rows, a2_h, live_replacements, prior = D.solve_a0_a3_a2()
    a2_map = dict(a2_rows)
    require(100 in a2_map and a2_map[100] == e,
            "synthetic exact E row changed")
    final_before_drop, final_h, a1_value = D.solve_row_variable(
        a2_rows, a2_h, 6, 1)
    final_before_map = dict(final_before_drop)
    require(final_before_map[18] == rhs,
            "reduced R18 is no longer -2*b3*d5*E")

    final_rows, final_h_again, final_live, all_values = (
        D.solve_a0_a3_a2_a1())
    require(tuple(label for label, _ in final_rows) == EXPECTED_LABELS,
            "final localized source-row labels changed")
    require(final_h_again == final_h,
            "final Hafnian substitution changed")
    require(final_live == live_replacements,
            "final live-factor numerators changed")
    require(all_values[-1] == a1_value,
            "final a1 substitution changed")

    return final_rows, final_live, all_values


def polynomial_digest(rows, live_replacements):
    payload = {
        "rows": [[label, C.singular(poly)] for label, poly in rows],
        "live_replacements": {
            str(index): C.singular(live_replacements[index])
            for index in (2, 3, 6)
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(encoded.encode("ascii")).hexdigest()


def modular_status(prime, rows, live_replacements, include_rows=True):
    live_b = C.multiply(live_replacements[6], live_replacements[7],
                        live_replacements[9])
    live_a = C.one
    live_d = C.one
    for edge in (2, 3, 4, 5):
        live_a = C.multiply(live_a, live_replacements[edge])
        if edge != 2:
            live_d = C.multiply(live_d,
                                live_replacements[C.d_index[edge]])
    names = ("z", "w", "a4", "a5", "b0", "b1", "b3",
             "d3", "d4", "d5")
    generators = ([C.singular(poly) for _, poly in rows]
                  if include_rows else [])
    generators += [f"z*({C.singular(live_b)})-1",
                   f"w*({C.singular(C.multiply(live_a, live_d))})-1"]
    command = (
        f"ring R={prime},({','.join(names)}),Dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;')
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"Singular failed in characteristic {prime}")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    require(len(body) == 3,
            f"unexpected characteristic-{prime} status output")
    return tuple(body)


def main():
    rows, live_replacements, all_values = exact_ledger()
    modular = {prime: modular_status(prime, rows, live_replacements)
               for prime in (1009, 1013)}
    require(all(status == ("0", "1", "-1")
                for status in modular.values()),
            "two-prime modular unit control changed")
    no_source = modular_status(1009, rows, live_replacements,
                               include_rows=False)
    require(no_source[0] != "0",
            "source-deletion must-fire did not fire")

    result = {
        "status": "UNAUDITED exact reduction plus modular-only unit",
        "branch_mask": 0,
        "defect_support_edge_indices": [2, 3, 4, 5],
        "defect_support_shape": "triangle 12,13,23 plus pendant 03",
        "lossless_gauge": "b2=b4=b5=d2=1 over the algebraic closure",
        "exact_localized_chain": [
            "literal R20 solves a0 with denominator b0*d3",
            "literal R14 solves a3 with denominator b1*d3*d5",
            "R6red+R18red=-2*b3*d5*(d3+b1*d4+b0*d5)",
            "E=d3+b1*d4+b0*d5 is therefore zero",
            "R16+a2*E solves a2 with live monomial denominator",
            "reduced R6 solves a1 with live monomial denominator",
            "reduced R18=-2*b3*d5*E and is redundant",
        ],
        "remaining_geometric_variables": [
            "a4", "a5", "b0", "b1", "b3", "d3", "d4", "d5"
        ],
        "remaining_source_row_labels": list(EXPECTED_LABELS),
        "remaining_source_row_count": len(rows),
        "localized_products": [
            "b0*b1*b3",
            "(cleared numerator a2)*(cleared numerator a3)*a4*a5*d3*d4*d5",
        ],
        "pure_H_localized": False,
        "c_entry_product_localized": False,
        "modular_status_remainder_basis_size_dimension": {
            str(prime): list(status) for prime, status in modular.items()
        },
        "must_fire_without_source_rows_p1009": list(no_source),
        "exact_chain_digest": polynomial_digest(rows, live_replacements),
        "direct_Q_attempts": [
            "raw localized dp timed out at 240 seconds",
            "raw localized Dp/localizers-first timed out at 300 seconds",
            "reduced eight-variable Dp/localizers-first timed out at 240 seconds",
            "homogeneous reduced p1009 probe timed out at 150 seconds",
        ],
        "logical_scope": (
            "the exact localized reduction is proved; the residual unit is "
            "only a two-prime discovery until an exact-Q multiplier or dual "
            "is replayed; no k4-cycle or chart-closure claim"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-zero triangle+pendant localized chain: PASS")
    print("exact rows / geometric variables:", len(rows), 8)
    print("modular controls:", modular)
    print("exact unit claimed:", False)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
