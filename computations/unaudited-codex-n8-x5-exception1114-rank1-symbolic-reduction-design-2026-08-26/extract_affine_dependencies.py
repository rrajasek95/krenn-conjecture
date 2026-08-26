#!/usr/bin/env python3
"""Extract modular affine consequences of nonlinear-row dependencies."""

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26"
spec = importlib.util.spec_from_file_location("sealed_refinement", PARENT / "build_refinement.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
E = b.all_equations()
P = 1000003


def cm(value):
    return value.numerator * pow(value.denominator, P - 2, P) % P


basis = {}
provenance = {}
dependencies = []
for source_index, equation in enumerate(E):
    row = {m: cm(c) for m, c in equation.items() if len(m) >= 2}
    row = {m: c for m, c in row.items() if c}
    proof = {source_index: 1}
    while row:
        pivot = max(row, key=lambda m: (len(m), m))
        if pivot not in basis:
            inverse = pow(row[pivot], P - 2, P)
            basis[pivot] = {m: c * inverse % P for m, c in row.items()}
            provenance[pivot] = {i: c * inverse % P for i, c in proof.items()}
            break
        factor = row[pivot]
        old = basis[pivot]
        for monomial, coefficient in old.items():
            row[monomial] = (row.get(monomial, 0) - factor * coefficient) % P
            if not row[monomial]:
                del row[monomial]
        old_proof = provenance[pivot]
        for i, coefficient in old_proof.items():
            proof[i] = (proof.get(i, 0) - factor * coefficient) % P
            if not proof[i]:
                del proof[i]
    if not row:
        dependencies.append(proof)

affine = []
exact_relations = []
for proof in dependencies:
    consequence = {}
    for source_index, multiplier in proof.items():
        for monomial, coefficient in E[source_index].items():
            if len(monomial) <= 1:
                consequence[monomial] = (consequence.get(monomial, 0) + multiplier * cm(coefficient)) % P
                if not consequence[monomial]:
                    del consequence[monomial]
    affine.append({
        "dependency_terms": len(proof),
        "source_equations": {str(i): c for i, c in sorted(proof.items())},
        "affine_consequence": {"*".join(m) if m else "1": c for m, c in sorted(consequence.items())},
    })
    signed = {i: (-1 if c == P - 1 else c) for i, c in proof.items()}
    if set(signed.values()) - {-1, 1}:
        raise RuntimeError(("dependency did not lift as a signed identity", signed))
    exact = b.add(*(b.scale(E[i], coefficient) for i, coefficient in signed.items()))
    if exact:
        raise RuntimeError(("signed dependency failed exact Q replay", signed, len(exact)))
    exact_relations.append({"coefficients": {str(i): c for i, c in sorted(signed.items())}, "removed_equation": max(signed)})

removed = [row["removed_equation"] for row in exact_relations]
if len(set(removed)) != len(removed):
    raise RuntimeError("relations lack independent last coordinates")
if any(row["coefficients"][str(row["removed_equation"])] == 0 for row in exact_relations):
    raise RuntimeError("bad relation pivot")
if any(row["affine_consequence"] for row in affine):
    raise RuntimeError("unexpected affine remainder")

result = {
    "prime": P,
    "nonlinear_rank": len(basis),
    "dependencies": len(dependencies),
    "affine": affine,
    "exact_signed_relations": exact_relations,
    "exact_Q_nonlinear_rank": len(E) - len(exact_relations),
    "exact_Q_full_generator_rank": len(E) - len(exact_relations),
    "proof": "mod-p nonlinear rank is a Q lower bound; 20 independent exact signed full-polynomial identities are a matching upper bound and have zero affine remainder",
}
(HERE / "affine_dependencies_mod1000003.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({
    "rank": len(basis),
    "dependencies": len(dependencies),
    "dependency_sizes": [len(proof) for proof in dependencies],
    "affine_supports": [row["affine_consequence"] for row in affine],
}, indent=2, sort_keys=True))
