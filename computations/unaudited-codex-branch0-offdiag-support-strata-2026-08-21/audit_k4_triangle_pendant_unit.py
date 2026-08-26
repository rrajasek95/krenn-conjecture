#!/usr/bin/env python3
"""Two-prime broad-unit lead for branch0 k4 triangle-plus-pendant support.

The support is {01,02,03,12}.  The site torus gauges b03=b13=b23=1 and
then d01=1.  All sixteen surviving literal packet rows and only the remaining
all-b localizer have unit Groebner basis modulo 1009 and 1013.  The direct
exact-Q computation timed out, so this file intentionally proves no
characteristic-zero theorem.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
INTERFACE_PATH = HERE / "build_support_strata_interface.py"
OUT = HERE / "results_k4_triangle_pendant_modular_lead.json"
SUPPORT = (0, 1, 2, 3)
EXPECTED_ROWS = tuple(range(6, 22))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("n8_k4_triangle_pendant_raw", INTERFACE_PATH)
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


def gauged_rows():
    equations, _ = SOURCE.PROBE.equations((0,) * 6)
    rows = []
    for raw in equations:
        specialized = CTX.substitute(raw)
        if specialized:
            specialized, _ = CTX.clear_denominators(specialized)
        rows.append(specialized)
    require(len(rows) == 22 and not any(rows[:6]),
            "raw permanent substitution changed")

    gauge = {index: CTX.variable(index) for index in range(CTX.n)}
    for index in (8, 10, 11):  # b03=b13=b23=1.
        gauge[index] = CTX.one
    gauge[CTX.d_index[0]] = CTX.one  # d01=1.
    gauged = tuple(substitute(row, gauge) for row in rows)
    live = tuple(index for index, row in enumerate(gauged) if row)
    require(live == EXPECTED_ROWS, "gauged source-row support changed")
    b_live = CTX.multiply(CTX.variable(6), CTX.variable(7),
                          CTX.variable(9))
    return gauged, b_live


def singular_status(characteristic, include_rows=True):
    rows, b_live = gauged_rows()
    generators = ([CTX.singular(rows[index]) for index in EXPECTED_ROWS]
                  if include_rows else [])
    generators.append(f"z*({CTX.singular(b_live)})-1")
    active_names = [name for name in CTX.variable_names + ("z",)
                    if any(re.search(rf"\b{re.escape(name)}\b", generator)
                           for generator in generators)]
    command = (
        f"ring R={characteristic},({','.join(active_names)}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(string(reduce(1,G)));print(size(G));'
        'print(dim(G));print("END");quit;'
    )
    started = time.monotonic()
    completed = subprocess.run(
        ["Singular", "-q", "-c", command], text=True,
        capture_output=True, timeout=120, check=False,
    )
    elapsed = time.monotonic() - started
    require(completed.returncode == 0 and not completed.stderr.strip(),
            f"Singular characteristic {characteristic} failed")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN") + 1:lines.index("END")]
    require(len(body) == 3, "Singular status output changed")
    return tuple(body), round(elapsed, 6), active_names


def main():
    rows, b_live = gauged_rows()
    modular = {}
    active_names = None
    for prime in (1009, 1013):
        status, elapsed, names = singular_status(prime)
        if active_names is None:
            active_names = names
        require(names == active_names, "active variable list changed by prime")
        modular[str(prime)] = {"status": list(status)}
    unit_status = ["0", "1", "-1"]
    require(all(record["status"] == unit_status
                for record in modular.values()),
            "modular unit status failed")
    mutation, mutation_seconds, _ = singular_status(1009,
                                                     include_rows=False)
    require(mutation[0] != "0", "source-row deletion did not fire")

    result = {
        "status": "UNAUDITED k4 triangle-plus-pendant modular lead",
        "branch_mask": 0,
        "support_edge_indices": list(SUPPORT),
        "support_edges": [list(SOURCE.EDGES[index]) for index in SUPPORT],
        "raw_source_row_indices": list(EXPECTED_ROWS),
        "raw_source_row_labels": [SOURCE.raw_labels()[index]
                                  for index in EXPECTED_ROWS],
        "raw_source_row_count": len(EXPECTED_ROWS),
        "torus_gauge": ["b03=b13=b23=1", "d01=1"],
        "torus_gauge_losslessness": (
            "The three star b values and selected d01 are nonzero on the "
            "chart.  The anchor-preserving site torus sets them to one over "
            "the algebraic closure and preserves every packet zero and "
            "nonvanishing condition."
        ),
        "active_ring_variables": active_names,
        "localized_polynomial": CTX.singular(b_live),
        "localized_H": False,
        "localized_selected_a_d": False,
        "localized_selected_c": False,
        "exact_Q_status": "TIMEOUT in a separate 300-second dp probe",
        "modular": modular,
        "must_fire_without_source_rows": {
            "status_mod1009": list(mutation),
        },
        "conclusion": (
            "The displayed broad ideal is the unit ideal over F_1009 and "
            "F_1013.  This is a characteristic-zero discovery lead only."
        ),
        "scope_guard": (
            "No characteristic-zero conclusion is inferred from the two "
            "prime units or from the exact-Q timeout."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch0 k4 triangle-plus-pendant modular lead: PASS")
    print("primes / mutation:",
          {prime: record["status"] for prime, record in modular.items()},
          mutation)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
