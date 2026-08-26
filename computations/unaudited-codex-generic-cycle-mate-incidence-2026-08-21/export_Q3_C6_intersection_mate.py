#!/usr/bin/env python3
"""Export the fixed-left mate ideal for the Q3=C6 intersection signature."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_left_slices_export_mate.py"
SIGNATURE_PATH = HERE / "results_localizer_face_signatures.json"
OUT = HERE / "results_Q3_C6_intersection_mate_export.json"
PRIMES = (1073741827, 1073741789)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("generic_cycle_Q3_C6_mate_audit", AUDIT_PATH)


def main():
    signature = json.loads(SIGNATURE_PATH.read_text())
    records = signature["Q3_C6_intersections"]
    fields = ("entry_support", "cofactor_support", "Q_support")
    for field in fields:
        if len({tuple(record[field]) for record in records}) != 1:
            raise RuntimeError(f"intersection {field} signatures ceased to agree")
    if not all(record["H_nonzero"] for record in records):
        raise RuntimeError("intersection ceased to be H-live")
    record = records[0]
    zero_cells = frozenset(record["cofactor_support"])
    remaining = tuple(index for index in range(24) if index not in zero_cells)
    variable_names = tuple(f"x{index}" for index in remaining)
    old_to_new = {old: new for new, old in enumerate(remaining)}

    def renumber(poly):
        specialized = AUDIT.specialize(poly, zero_cells)
        answer = Counter()
        for monomial, coefficient in specialized.items():
            answer[tuple(old_to_new[index] for index in monomial)] += coefficient
        return AUDIT.clean(answer)

    hafnian = AUDIT.CORE.pure_hafnian()
    rows = []
    rows.extend(("mate_e_"+"".join(map(str, edge)),
                 renumber(AUDIT.CORE.e_pair(*edge)))
                for edge in AUDIT.CORE.SUPER_EDGES)
    rows.extend(("mate_t_"+"".join(map(str, triple)),
                 renumber(AUDIT.CORE.t_triple(*triple)))
                for triple in combinations(range(4), 3))
    rows.extend((f"mate_cofactor_{index}",
                 renumber(AUDIT.PROBE.derivative(hafnian, index)))
                for index in record["entry_support"])
    rows.extend((f"mate_Q_{15-index}", renumber(
        AUDIT.CORE.q_orientation(tuple(
            ((15-index) >> (3-site)) & 1 for site in range(4)))))
        for index in record["Q_support"])
    unique = []
    aliases = []
    seen = {}
    for label, poly in rows:
        key_poly = tuple(sorted(poly.items()))
        if not poly:
            continue
        if key_poly in seen:
            aliases[seen[key_poly]].append(label)
        else:
            seen[key_poly] = len(unique)
            unique.append((label, poly))
            aliases.append([label])
    mate_h = renumber(hafnian)
    if not mate_h:
        raise RuntimeError("intersection mate H vanished structurally")
    outputs = []
    for prime in PRIMES:
        path = HERE / f"Q3_C6_intersection_mate_p{prime}.msolve"
        ordinary_text = [AUDIT.encode(poly, variable_names)
                         for _, poly in unique]
        h_text = AUDIT.encode(mate_h, variable_names)
        path.write_text(
            ",".join(variable_names)+f"\n{prime}\n"
            + ",\n".join(ordinary_text)+",\n"+h_text+"\n")
        # msolve 0.10.1 can segfault in native -S mode on this 17-variable
        # signature.  Freeze the algebraically equivalent explicit
        # Rabinowitsch input as the portable fallback.
        h_terms = h_text.split("+")
        rabinowitsch = "-1+"+"+".join(
            "u" if term == "1" else "u*"+term for term in h_terms)
        explicit_path = HERE / f"Q3_C6_intersection_mate_explicit_p{prime}.msolve"
        explicit_path.write_text(
            ",".join((*variable_names, "u"))+f"\n{prime}\n"
            + ",\n".join((*ordinary_text, rabinowitsch))+"\n")
        body = path.read_text().split("\n", 2)[2]
        if "(" in body or "**" in body:
            raise RuntimeError("msolve syntax regression")
        outputs.append({
            "prime": prime,
            "path": path.name,
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "explicit_rabinowitsch_path": explicit_path.name,
            "explicit_rabinowitsch_sha256": sha256(
                explicit_path.read_bytes()).hexdigest(),
            "ordinary_rows_after_dedupe": len(unique),
            "total_rows": len(unique)+1,
        })
    result = {
        "status": "UNAUDITED exact-signature Q3=C6 fixed-left mate export PASS",
        "signature_sha256": sha256(SIGNATURE_PATH.read_bytes()).hexdigest(),
        "intersection_point_count": len(records),
        "entry_support": record["entry_support"],
        "cofactor_support": record["cofactor_support"],
        "left_Q_support": record["Q_support"],
        "remaining_mate_variables": list(variable_names),
        "generator_aliases": aliases,
        "outputs": outputs,
        "final_saturator": "mate_H",
        "scope": (
            "Common exact H-live signature of the two Q3=C6 component "
            "intersection points. Mate e/t, both directional "
            "entry*cofactor consequences, complement-Q rows, and mate H "
            "only; no left H equation or generic C6 localizer is imposed."
        ),
        "source_hashes": {
            "audit": sha256(AUDIT_PATH.read_bytes()).hexdigest(),
            "signature": sha256(SIGNATURE_PATH.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q3=C6 fixed-left mate export PASS")
    print("rows", len(unique), "+ H; variables", len(variable_names))
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
