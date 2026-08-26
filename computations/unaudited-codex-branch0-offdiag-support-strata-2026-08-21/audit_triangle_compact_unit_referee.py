#!/usr/bin/env python3
"""Exact compact-basis referee for the branch0 triangle defect stratum.

All rows are rebuilt from the literal 22-row packet.  The anchor-preserving
site torus gauges three b entries and one selected d entry.  Three raw
cofactor rows then eliminate two variables.  Ten raw source rows plus only
the all-b localizer have exact unit Groebner basis over Q.

The result is intentionally labelled a basis certificate: Singular has not
serialized polynomial multipliers back to the ten raw source rows.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
INTERFACE_PATH = HERE / "build_support_strata_interface.py"
OUT = HERE / "results_triangle_compact_unit_referee.json"
SUPPORT = (0, 1, 3)
COMPACT_ROWS = (6, 7, 8, 9, 10, 11, 12, 13, 15, 19)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_triangle_compact_raw", INTERFACE_PATH)
CTX = SOURCE.Context(SUPPORT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def power(poly, exponent):
    answer = CTX.one
    for _ in range(exponent):
        answer = CTX.multiply(answer, poly)
    return answer


def substitute(poly, replacements):
    answer = {}
    for exponent, coefficient in poly.items():
        term = CTX.scale(CTX.one, coefficient)
        for index, multiplicity in enumerate(exponent):
            if multiplicity:
                term = CTX.multiply(term,
                                    power(replacements[index], multiplicity))
        answer = CTX.add(answer, term)
    return answer


def raw_rows():
    equations, _ = SOURCE.PROBE.equations((0,) * 6)
    require(len(equations) == 22, "raw packet row count changed")
    rows = []
    for index, raw in enumerate(equations):
        specialized = CTX.substitute(raw)
        if not specialized:
            rows.append({})
            continue
        cleared, _ = CTX.clear_denominators(specialized)
        rows.append(cleared)
    return tuple(rows)


def reduced_rows():
    rows = raw_rows()
    one = CTX.one
    gauge = {index: CTX.variable(index) for index in range(CTX.n)}
    for index in (8, 10, 11):  # b03=b13=b23=1.
        gauge[index] = one
    gauge[CTX.d_index[0]] = one  # d01=1.
    gauged = tuple(substitute(row, gauge) for row in rows)

    d1 = CTX.variable(CTX.d_index[1])
    d3 = CTX.variable(CTX.d_index[3])
    b0, b1 = CTX.variable(6), CTX.variable(7)
    relation_one = CTX.add(
        gauged[12], CTX.scale(gauged[20], -1),
        CTX.multiply(b0, gauged[16]),
        CTX.scale(CTX.multiply(b0, CTX.add(one, d1, d3)), 2),
    )
    require(not relation_one,
            "literal R12-R20+b0*R16 cofactor identity changed")
    expected_r16 = CTX.add(
        CTX.multiply(CTX.add(b1, CTX.scale(one, -1)), one),
        CTX.multiply(CTX.add(b0, CTX.scale(one, -1)), d1),
    )
    require(gauged[16] == expected_r16,
            "literal R16 cofactor identity changed")

    eliminate = {index: CTX.variable(index) for index in range(CTX.n)}
    eliminate[CTX.d_index[3]] = CTX.add(CTX.scale(one, -1),
                                                CTX.scale(d1, -1))
    eliminate[7] = CTX.add(one, d1,
                           CTX.scale(CTX.multiply(b0, d1), -1))
    reduced = tuple(substitute(row, eliminate) for row in gauged)
    compact = tuple((index, reduced[index]) for index in COMPACT_ROWS)
    require(all(poly for _, poly in compact), "a compact source row vanished")
    b_live = CTX.multiply(b0, eliminate[7], CTX.variable(9))
    return compact, b_live


def singular_status(characteristic, omit_index=None):
    compact, b_live = reduced_rows()
    generators = [CTX.singular(poly) for index, poly in compact
                  if index != omit_index]
    generators.append(f"z*({CTX.singular(b_live)})-1")
    names = ",".join(CTX.variable_names + ("z",))
    command = (
        f"ring R={characteristic},({names}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    completed = subprocess.run(
        ["Singular", "-q", "-c", command],
        text=True, capture_output=True, timeout=30, check=False,
    )
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"Singular characteristic {characteristic} failed")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    require(len(body) == 3, "Singular status output changed")
    return tuple(body)


def main():
    compact, b_live = reduced_rows()
    exact = singular_status(0)
    modular = {str(prime): singular_status(prime)
               for prime in (1009, 1013)}
    require(exact == ("0", "1", "-1"), "exact unit status failed")
    require(all(status == exact for status in modular.values()),
            "modular unit status failed")
    mutation = singular_status(1009, omit_index=COMPACT_ROWS[0])
    require(mutation[0] != "0", "raw-row deletion mutation did not fire")

    result = {
        "status": "UNAUDITED exact compact triangle unit referee",
        "branch_mask": 0,
        "defect_support_edge_indices": list(SUPPORT),
        "raw_source_row_indices": list(COMPACT_ROWS),
        "raw_source_row_count": len(compact),
        "torus_action": (
            "diag(t_i,t_i^-1): a_ij->t_i*t_j*a_ij, "
            "b_ij->t_i/t_j*b_ij, c_ij->t_j/t_i*c_ij, "
            "d_ij->d_ij/(t_i*t_j)"
        ),
        "gauge": ["b03=b13=b23=1", "d01=1 over the algebraic closure"],
        "gauge_losslessness": (
            "The first gauge uses the three star b entries.  Their common "
            "residual scale sets d01=1 because selected d01 and every b are "
            "localized.  Packet zero sets and all nonvanishing conditions "
            "are preserved by the torus weights."
        ),
        "literal_cofactor_ledger": [
            "R12-R20+b0*R16=-2*b0*(d0+d1+d3)",
            "R16=(b1-1)*d0+(b0-1)*d1",
            "after d0=1: d3=-1-d1, b1=1+d1-b0*d1",
        ],
        "localized_polynomial": CTX.singular(b_live),
        "localized_H": False,
        "localized_selected_a_d": False,
        "localized_selected_c": False,
        "exact_remainder_basis_size_dimension": list(exact),
        "modular_statuses": {prime: list(status)
                             for prime, status in modular.items()},
        "must_fire_delete_raw_row": {
            "row_index": COMPACT_ROWS[0],
            "status_mod1009": list(mutation),
        },
        "conclusion": (
            "The whole branch0 triangle defect stratum is empty after only "
            "the mandatory all-b localization; this includes every H and "
            "c boundary."
        ),
        "scope_guard": (
            "The exact Groebner basis is a source-labelled basis certificate. "
            "Polynomial multipliers expressing 1 have not been serialized."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch0 triangle compact unit referee: PASS")
    print("rows / exact / mutation:", len(compact), exact, mutation)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
