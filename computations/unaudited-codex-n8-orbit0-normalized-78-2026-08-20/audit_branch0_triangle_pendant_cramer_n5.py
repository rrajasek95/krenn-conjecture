#!/usr/bin/env python3
"""Exact Cramer reduction and modular N5-nilpotence for k4 TP.

This audit proves the symbolic reduction on the open P26 chart over Q.  It
then records, as discovery only, that the transported a5 numerator N5 has
nilpotence exponent exactly three modulo 1009 and 1013.  No characteristic-
zero membership or determinant-zero-branch claim is made.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
DISCOVERY = HERE / "discover_branch0_triangle_pendant_reduction.py"
OUT = HERE / "results_branch0_triangle_pendant_cramer_n5.json"
EXPECTED_ROWS = (8, 9, 10, 11, 13, 15, 17, 19, 21)
EXPECTED_TERMS = (80, 106, 61, 222, 262, 164, 122, 91, 101)


def load():
    spec = importlib.util.spec_from_file_location("n8_tp_discovery", DISCOVERY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D = load()
C = D.CHART


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def scaled_e_rows():
    rows, _, _, _ = D.solve_a0_a3_a2_a1()
    replacements = {index: C.variable(index) for index in range(C.n)}
    live_d3 = C.add(
        C.multiply(C.variable(7), C.variable(C.d_index[4])),
        C.multiply(C.variable(6), C.variable(C.d_index[5])))
    replacements[C.d_index[3]] = C.scale(live_d3, -1)
    replacements[4] = C.multiply(
        C.variable(4), D.inverse_monomial(C.d_index[4]))
    replacements[5] = C.multiply(
        C.variable(5),
        D.inverse_monomial(C.d_index[4], C.d_index[5]))
    transformed = {
        label: D.divide_common_monomial(C.clear_denominators(
            D.substitute_poly(poly, replacements)))
        for label, poly in rows if label != 100
    }
    return transformed, live_d3


def exact_ledger():
    data = D.cramer_branch_system(7, 12)
    rows, live_d3 = scaled_e_rows()
    linear = {label: D.split_linear(poly) for label, poly in rows.items()}
    lc, la, lb = linear[7]
    rc, ra, rb = linear[12]
    determinant_raw = C.add(C.multiply(la, rb),
                            C.scale(C.multiply(lb, ra), -1))
    numerator_4_raw = C.add(C.multiply(lb, rc),
                            C.scale(C.multiply(lc, rb), -1))
    numerator_5_raw = C.add(C.multiply(lc, ra),
                            C.scale(C.multiply(la, rc), -1))
    common = C.multiply(C.variable(C.d_index[4]), live_d3)
    require(determinant_raw == C.multiply(common, data["determinant"]),
            "Cramer determinant common factor changed")
    require(numerator_4_raw == C.multiply(common, data["numerator_a4"]),
            "Cramer a4 numerator common factor changed")
    require(numerator_5_raw == C.multiply(common, data["numerator_a5"]),
            "Cramer a5 numerator common factor changed")
    for label in (7, 12):
        constant, coefficient_4, coefficient_5 = linear[label]
        replay = C.add(
            C.multiply(constant, data["determinant"]),
            C.multiply(coefficient_4, data["numerator_a4"]),
            C.multiply(coefficient_5, data["numerator_a5"]))
        require(replay == {}, f"Cramer replay failed on row {label}")
    labels = tuple(label for label, _ in data["open_rows"])
    terms = tuple(len(poly) for _, poly in data["open_rows"])
    require(labels == EXPECTED_ROWS, "transported row labels changed")
    require(terms == EXPECTED_TERMS, "transported row term counts changed")
    require(len(data["determinant"]) == 26, "P26 term count changed")
    require(len(data["numerator_a4"]) == 18, "N4 term count changed")
    require(len(data["numerator_a5"]) == 46, "N5 term count changed")
    require(len(data["live_a2_numerator"]) == 31,
            "transported A2 numerator term count changed")
    return data


def modular_nilpotence(prime, data):
    rows = [C.singular(poly) for _, poly in data["open_rows"]]
    n5 = C.singular(data["numerator_a5"])
    command = (
        f"ring R={prime},(b0,b1,b3,d4,d5),dp;"
        f"ideal I={','.join(rows)};ideal G=slimgb(I);"
        f"poly f={n5};poly q=1;"
        'print("BEGIN");print(size(G));print(dim(G));'
        'for(int n=1;n<=3;n++){q=reduce(q*f,G);'
        'print(size(q));print(deg(q));}print("END");quit;')
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"Singular failed in characteristic {prime}")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    require(body == ["142", "3", "46", "8", "891", "16", "0", "-1"],
            f"nilpotence ledger changed in characteristic {prime}: {body}")
    return {
        "groebner_basis_size": 142,
        "ideal_dimension": 3,
        "N5_remainders_term_count_degree": [[46, 8], [891, 16], [0, -1]],
        "least_nilpotence_exponent": 3,
    }


def payload_digest(data):
    payload = {
        "determinant": C.singular(data["determinant"]),
        "numerator_a4": C.singular(data["numerator_a4"]),
        "numerator_a5": C.singular(data["numerator_a5"]),
        "live_a2_numerator": C.singular(data["live_a2_numerator"]),
        "rows": [[label, C.singular(poly)] for label, poly in data["open_rows"]],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(encoded.encode("ascii")).hexdigest()


def main():
    data = exact_ledger()
    modular = {str(prime): modular_nilpotence(prime, data)
               for prime in (1009, 1013)}
    result = {
        "status": "UNAUDITED exact Cramer reduction plus modular-only nilpotence",
        "branch_mask": 0,
        "defect_support_edge_indices": [2, 3, 4, 5],
        "proved_relation_used": "E=d3+b1*d4+b0*d5=0",
        "laurent_rescaling": ["x=d4*a4", "y=d4*d5*a5"],
        "cramer_pair_source_labels": [7, 12],
        "common_cancelled_factor": "d4*(b0*d5+b1*d4)=-d4*d3",
        "open_branch_divisor": "P26",
        "open_branch_divisor_terms_degree": [26, 7],
        "cramer_numerator_terms": {"N4": 18, "N5": 46},
        "transported_row_labels": list(EXPECTED_ROWS),
        "transported_row_term_counts": list(EXPECTED_TERMS),
        "transported_A2_numerator_terms": 31,
        "modular_nilpotence": modular,
        "modular_tracked_lift_p1009": {
            "multiplier_term_counts": [111017, 96896, 134577, 60204,
                                       60776, 96708, 0, 96119, 120440],
            "total_multiplier_terms": 776737,
            "maximum_product_degree": 36,
        },
        "exact_payload_sha256": payload_digest(data),
        "exact_Q_status": (
            "OPEN: N5^3 membership has only modular evidence; direct Q "
            "slimgb timed out at 180 seconds"
        ),
        "determinant_zero_branch_status": "OPEN",
        "logical_scope": (
            "The E substitution, Laurent rescaling, common-factor cancellation, "
            "and Cramer formulas are exact over Q.  The exponent-three result "
            "is a two-prime discovery target, not a characteristic-zero proof."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("triangle+pendant Cramer N5 audit: PASS")
    print("exact P26/N4/N5 terms:", 26, 18, 46)
    print("modular least nilpotence exponent:", 3)
    print("exact-Q membership claimed:", False)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
