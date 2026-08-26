#!/usr/bin/env python3
"""Export the weakest chart-forced mate incidence on the exact A=B component."""

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_left_slices_export_mate.py"
FACE_PATH = HERE / "derive_AB_component_localizer_faces.py"
LEDGER_PATH = HERE / "results_AB_component_localizer_faces.json"
MSOLVE_IO_PATH = HERE.parent / "toolkit/groebner/msolve_io.py"
OUT = HERE / "results_AB_component_weak_mate_export.json"
PRIMES = (1073741827, 1073741789)
ZERO_CELLS = frozenset((1, 2, 21, 22))
ENTRY_SUPPORT = (1, 2, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 19, 21, 22)
Q_SUPPORT = (0, 5, 6, 9, 10, 15)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("AB_component_weak_mate_audit", AUDIT_PATH)
FACE = load("AB_component_weak_face_audit", FACE_PATH)
MSOLVE_IO = load("AB_component_weak_msolve_io", MSOLVE_IO_PATH)


def main():
    ledger = json.loads(LEDGER_PATH.read_text())
    if not ledger["component_parametrization"]["all_source_rows_replay"]:
        raise RuntimeError("exact component source replay changed")
    r, s, t = sp.symbols("r s t")
    parameters, entries = AUDIT.raw_left_expressions()
    b0, b1, b3, d1, d3, d4 = parameters
    substitution = {
        b0: s, d1: r, d3: s, d4: -r*s, b3: t,
        b1: t*s*(r+2)-r-s-2,
    }
    chart_units = {factor
                   for factors in ledger["chart_factorization"].values()
                   for factor, _ in factors}

    def audit_unit(expression):
        value = FACE.reduce_r(expression.subs(substitution), r, s, t)
        factors = FACE.irreducible_factors(value, r, s, t)
        if any(factor not in chart_units for factor, _ in factors):
            raise RuntimeError(f"claimed component unit gained factor: {value}")
        return {"expression": str(sp.factor(value)),
                "numerator_factors": [factor for factor, _ in factors],
                "all_factors_are_chart_units": True}

    remaining = tuple(i for i in range(24) if i not in ZERO_CELLS)
    names = tuple(f"x{i}" for i in remaining)
    old_to_new = {old: new for new, old in enumerate(remaining)}

    def renumber(poly):
        specialized = AUDIT.specialize(poly, ZERO_CELLS)
        answer = Counter()
        for monomial, coefficient in specialized.items():
            answer[tuple(old_to_new[i] for i in monomial)] += coefficient
        return AUDIT.clean(answer)

    hafnian = AUDIT.CORE.pure_hafnian()
    raw_cofactors = tuple(AUDIT.PROBE.derivative(hafnian, i)
                          for i in range(24))
    raw_q = tuple(AUDIT.CORE.q_orientation(tuple(
        (i >> (3-site)) & 1 for site in range(4))) for i in range(16))
    cofactor_audit = {
        str(i): audit_unit(FACE.raw_to_sympy(raw_cofactors[i], entries))
        for i in sorted(ZERO_CELLS)
    }
    entry_audit = {str(i): audit_unit(entries[i]) for i in ENTRY_SUPPORT}
    q_audit = {
        str(i): audit_unit(FACE.raw_to_sympy(raw_q[i], entries))
        for i in Q_SUPPORT
    }
    rows = []
    rows += [("mate_e_"+"".join(map(str, edge)),
              renumber(AUDIT.CORE.e_pair(*edge)))
             for edge in AUDIT.CORE.SUPER_EDGES]
    rows += [("mate_t_"+"".join(map(str, triple)),
              renumber(AUDIT.CORE.t_triple(*triple)))
             for triple in combinations(range(4), 3)]
    rows += [(f"mate_cofactor_{i}",
              renumber(AUDIT.PROBE.derivative(hafnian, i)))
             for i in ENTRY_SUPPORT]
    rows += [(f"mate_Q_{15-i}", renumber(AUDIT.CORE.q_orientation(tuple(
        ((15-i) >> (3-site)) & 1 for site in range(4)))))
             for i in Q_SUPPORT]
    unique, aliases, seen = [], [], {}
    for label, poly in rows:
        key = tuple(sorted(poly.items()))
        if not poly:
            continue
        if key in seen:
            aliases[seen[key]].append(label)
        else:
            seen[key] = len(unique)
            unique.append((label, poly))
            aliases.append([label])
    h_text = AUDIT.encode(renumber(hafnian), names)
    h_terms = h_text.split("+")
    rab = "-1+"+"+".join("u" if x == "1" else "u*"+x for x in h_terms)
    outputs = []
    for prime in PRIMES:
        raw_path = HERE / f"AB_component_weak_mate_p{prime}.msolve"
        raw_path.write_text(",".join(names)+f"\n{prime}\n"+
                            ",\n".join([AUDIT.encode(poly, names)
                                      for _, poly in unique]+[h_text])+"\n")
        path = HERE / f"AB_component_weak_mate_explicit_p{prime}.msolve"
        path.write_text(",".join((*names, "u"))+f"\n{prime}\n"+
                        ",\n".join([AUDIT.encode(poly, names)
                                      for _, poly in unique]+[rab])+"\n")
        outputs.append({"prime": prime, "path": path.name,
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                        "native_saturation_path": raw_path.name,
                        "native_saturation_sha256": sha256(
                            raw_path.read_bytes()).hexdigest()})
    exact_path = HERE / "AB_component_weak_mate_exact.msolve"
    exact_path.write_text(",".join((*names, "u"))+"\n0\n"+
                          ",\n".join([AUDIT.encode(poly, names)
                                      for _, poly in unique]+[rab])+"\n")
    exact_input = MSOLVE_IO.read_msolve_input(
        exact_path, strict=True, allow_characteristic_zero=True)
    for record in outputs:
        modular = MSOLVE_IO.read_msolve_input(HERE / record["path"], strict=True)
        if (modular.variables != exact_input.variables or
                modular.polynomials != exact_input.polynomials):
            raise RuntimeError("exact/modular weak mate rows ceased to agree")
    result = {
        "status": "UNAUDITED exact-component weakest forced mate export PASS",
        "zero_cells": sorted(ZERO_CELLS),
        "entry_support": list(ENTRY_SUPPORT),
        "left_Q_support": list(Q_SUPPORT),
        "generator_aliases": aliases,
        "ordinary_row_count": len(unique),
        "localizer_audit": {
            "source_component_rows_replay": True,
            "chart_factors_preserved": True,
            "left_H_not_inferred": True,
            "cofactor_units_for_mate_entry_zeros": cofactor_audit,
            "entry_units_for_mate_cofactor_rows": entry_audit,
            "Q_units_for_complement_mate_Q_rows": q_audit,
        },
        "exact_output": {
            "path": exact_path.name,
            "sha256": sha256(exact_path.read_bytes()).hexdigest(),
            "logical_sha256": exact_input.logical_sha256,
            "variables": list(exact_input.variables),
            "ordinary_row_labels": aliases,
            "ordinary_row_sha256": list(exact_input.polynomial_sha256[:-1]),
            "mate_H_rabinowitsch_sha256": exact_input.polynomial_sha256[-1],
            "strict_coefficient_first_parse": True,
            "literal_modular_row_replay": True,
        },
        "outputs": outputs,
        "scope": (
            "Only chart-forced nonvanishing data on the exact A=B component; "
            "all original source rows replay under the frozen parametrization, "
            "no left H is inferred, and mate H is localized literally."
        ),
        "source_hashes": {
            "audit": sha256(AUDIT_PATH.read_bytes()).hexdigest(),
            "face": sha256(FACE_PATH.read_bytes()).hexdigest(),
            "ledger": sha256(LEDGER_PATH.read_bytes()).hexdigest(),
            "msolve_io": sha256(MSOLVE_IO_PATH.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("weak mate export PASS", len(names), len(unique), result["result_sha256"])


if __name__ == "__main__":
    main()
