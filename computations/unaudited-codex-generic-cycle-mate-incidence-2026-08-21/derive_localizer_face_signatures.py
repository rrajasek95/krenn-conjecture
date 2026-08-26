#!/usr/bin/env python3
"""Exact generic signatures on Q3 and C6 faces and their intersection."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from itertools import permutations, product

import sympy as sp


HERE = Path(__file__).resolve().parent
FACE_PATH = HERE / "derive_AB_component_localizer_faces.py"
LEDGER_PATH = HERE / "results_AB_component_localizer_faces.json"
SUPPORT6_PATH = (HERE.parent /
    "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
    "results_weight0_support6_char0_component.json")
OUT = HERE / "results_localizer_face_signatures.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FACE = load("generic_cycle_face_signature_core", FACE_PATH)
AUDIT = FACE.AUDIT
CORE = FACE.CORE


def signature_on(substitution, entries, raw_cofactors, raw_q, raw_h):
    def value(expression):
        return sp.cancel(expression.subs(substitution))
    entry_values = tuple(value(expression) for expression in entries)
    def evaluate_raw(poly):
        answer = sp.Integer(0)
        for monomial, coefficient in poly.items():
            term = sp.Rational(coefficient)
            for index in monomial:
                term *= entry_values[index]
            answer += term
        return sp.cancel(answer)
    cofactor_values = tuple(evaluate_raw(poly) for poly in raw_cofactors)
    q_values = tuple(evaluate_raw(poly) for poly in raw_q)
    h_value = evaluate_raw(raw_h)
    entry_support = frozenset(i for i, item in enumerate(entry_values) if item != 0)
    cofactor_support = frozenset(i for i, item in enumerate(cofactor_values)
                                 if item != 0)
    q_support = frozenset(i for i, item in enumerate(q_values) if item != 0)
    structural = frozenset(i for i, poly in enumerate(raw_q)
                           if not AUDIT.specialize(poly, cofactor_support))
    directional = frozenset(15-i for i in q_support)
    uncovered = tuple((i, 15-i) for i in range(8)
                      if not ({i, 15-i} & (structural | directional)))
    return {
        "entry_support": sorted(entry_support),
        "cofactor_support": sorted(cofactor_support),
        "Q_support": sorted(q_support),
        "H_nonzero": h_value != 0,
        "structural_mate_Q_zeros": sorted(structural),
        "directional_mate_Q_zeros": sorted(directional),
        "uncovered_complementary_Q_pairs": [list(pair) for pair in uncovered],
        "compact_c3_antecedents": {
            "eight_cofactors": set((1, 2, 6, 10, 14, 18, 21, 22))
                                  <= cofactor_support,
            "four_Q": set((15, 3, 10, 9)) <= q_support,
        },
    }


def transform_signature(signature, permutation, flips):
    return (
        frozenset(FACE.cell_action(i, permutation, flips)
                  for i in signature["entry_support"]),
        frozenset(FACE.cell_action(i, permutation, flips)
                  for i in signature["cofactor_support"]),
        frozenset(FACE.q_action(i, permutation, flips)
                  for i in signature["Q_support"]),
    )


def main():
    ledger = json.loads(LEDGER_PATH.read_text())
    faces = {record["localizers"][0]: record["factor"]
             for record in ledger["minimal_face_antichain"]}
    root2 = sp.sqrt(2)
    r, s, t = sp.symbols("r s t")
    root = -1+root2
    parameters, entries = AUDIT.raw_left_expressions()
    b0, b1, b3, d1, d3, d4 = parameters
    component = {
        b0: s, d1: root, d3: s, d4: -root*s, b3: t,
        b1: t*s*(root+2)-root-s-2,
    }
    raw_h = CORE.pure_hafnian()
    raw_cofactors = tuple(AUDIT.PROBE.derivative(raw_h, i) for i in range(24))
    raw_q = tuple(CORE.q_orientation(tuple(
        (i >> (3-site)) & 1 for site in range(4))) for i in range(16))
    signatures = {}
    face_solutions = {}
    for label in ("Q3", "C6"):
        equation = sp.sympify(faces[label],
                              locals={"s": s, "t": t, "sqrt": sp.sqrt})
        solutions = sp.solve(equation, t)
        if len(solutions) != 1:
            raise RuntimeError(f"{label} face ceased to be linear in t")
        t_value = sp.factor(solutions[0], extension=root2)
        face_solutions[label] = t_value
        face_component = {key: sp.cancel(value.subs(t, t_value))
                          for key, value in component.items()}
        signatures[label] = signature_on(
            face_component, entries, raw_cofactors, raw_q, raw_h)

    # Exact intersection in the quadratic component field.
    q3_equation = sp.sympify(faces["Q3"],
                             locals={"s": s, "t": t, "sqrt": sp.sqrt})
    c6_equation = sp.sympify(faces["C6"],
                             locals={"s": s, "t": t, "sqrt": sp.sqrt})
    resultant = sp.factor(sp.resultant(q3_equation, c6_equation, t),
                          extension=root2)
    intersection_s = sp.solve(resultant, s)
    intersections = []
    for s_value in intersection_s:
        t_value = sp.factor(face_solutions["Q3"].subs(s, s_value),
                            extension=root2)
        point_sub = {key: sp.cancel(value.subs({s: s_value, t: t_value}))
                     for key, value in component.items()}
        sig = signature_on(point_sub, entries, raw_cofactors, raw_q, raw_h)
        sig["s"] = str(s_value)
        sig["t"] = str(t_value)
        intersections.append(sig)

    # Full B4 joint-signature comparison with the frozen support-six theorem.
    support6 = json.loads(SUPPORT6_PATH.read_text())
    support6_signature = (
        frozenset(support6["entry_nonzero_indices"]),
        frozenset(support6["cofactor_nonzero_indices"]),
        frozenset(support6["Q_support"]),
    )
    b4_matches = {}
    for label, signature in signatures.items():
        witnesses = []
        for permutation in permutations(range(4)):
            for flips in product((0, 1), repeat=4):
                if transform_signature(signature, permutation, flips) == support6_signature:
                    witnesses.append({"permutation": list(permutation),
                                      "flips": list(flips)})
        b4_matches[label] = witnesses

    result = {
        "status": "UNAUDITED exact generic face/intersection signatures PASS",
        "component_field": "Q(sqrt(2))(s), r=-1+sqrt(2)",
        "face_parametrizations": {label: str(value)
                                  for label, value in face_solutions.items()},
        "generic_signatures": signatures,
        "Q3_C6_intersection_resultant": str(resultant),
        "Q3_C6_intersections": intersections,
        "support6_B4_witnesses": b4_matches,
        "conclusion": (
            "C6 is the representative of the four-face stabilizer orbit. "
            "The compact-unit antecedent and support-six B4 fields state "
            "whether its generic stratum is already covered. The explicit "
            "Q3=C6 points are the sole recursive intersections up to that "
            "stabilizer."
        ),
        "scope": (
            "Exact symbolic signatures over one embedding of the irreducible "
            "quadratic component; vanishing statements are preserved by the "
            "conjugate embedding. B4 matching compares full entry/cofactor/Q "
            "supports, not Q support alone."
        ),
        "source_hashes": {
            "face": sha256(FACE_PATH.read_bytes()).hexdigest(),
            "ledger": sha256(LEDGER_PATH.read_bytes()).hexdigest(),
            "support6": sha256(SUPPORT6_PATH.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("localizer face signatures PASS")
    for label, signature in signatures.items():
        print(label, len(signature["entry_support"]),
              len(signature["cofactor_support"]), len(signature["Q_support"]),
              signature["compact_c3_antecedents"],
              signature["uncovered_complementary_Q_pairs"],
              "support6_witnesses", len(b4_matches[label]))
    print("intersection", resultant, len(intersections),
          [(point["H_nonzero"], point["uncovered_complementary_Q_pairs"])
           for point in intersections])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
