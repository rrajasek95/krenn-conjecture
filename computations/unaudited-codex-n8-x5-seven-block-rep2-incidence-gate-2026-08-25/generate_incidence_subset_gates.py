#!/usr/bin/env python3
"""Generate bounded two-colour full-X5 subset diagnostics for two rep2 stars."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25/generate_rank1_gate.py"
CORE_SHA256 = "1fc2a1a62e4092f75cbb330009bbb9649e83e559167f251217a26b7eb3bc7c14"
REP2_ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
VARIANTS = ("cap45_star1_three_term", "cap03_star6_two_sandwich")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load_core():
    assert sha256(CORE) == CORE_SHA256
    specification = importlib.util.spec_from_file_location("sealed_rank1_subset_core", CORE)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    module.ADDED = REP2_ADDED
    module.NONFIXED = tuple(sorted(module.ADDED | module.VARIABLE))
    module.RETAINED = tuple(edge for edge in module.NONFIXED if edge not in module.ELIMINATED)
    module.SUPPORT = module.FIXED | set(module.NONFIXED)
    module.SUPPORTED = tuple(matching for matching in module.PM8 if set(matching) <= module.SUPPORT)
    module.SOURCE = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in module.RETAINED
        for i, j in itertools.product(module.COLORS, repeat=2)
    }
    assert len(module.SUPPORTED) == 13 and len(module.SOURCE) == 81
    return module


def alternate_incidence(module):
    rho = tuple(f"arho{i}" for i in module.COLORS)
    sigma = tuple(f"asigma{i}" for i in module.COLORS)
    tau = tuple(f"atau{i}" for i in module.COLORS)
    equations = []
    # cap03/star6: P=Row(A04^T), so A04*rho=e0.
    for i in module.COLORS:
        value = module.sum_string(
            module.atom_product(module.retained_entry((0, 4), i, j), rho[j]) for j in module.COLORS
        )
        equations.append(f"({value})-{int(i == 0)}")
    # Q=ColSpan(A23^T,A35): A23^T*sigma+A35*tau=e0.
    for i in module.COLORS:
        value = module.sum_string(
            [module.atom_product(module.retained_entry((2, 3), j, i), sigma[j]) for j in module.COLORS]
            + [module.atom_product(module.retained_entry((3, 5), i, j), tau[j]) for j in module.COLORS]
        )
        equations.append(f"({value})-{int(i == 0)}")
    return equations, list(rho) + list(sigma) + list(tau)


def build_program(module, ring, variant):
    selected_words = tuple(word for word in itertools.product(module.COLORS, repeat=8) if len(set(word)) <= 2)
    assert len(selected_words) == 765
    full_equations = []
    word_records = []
    for word in selected_words:
        value = module.amplitude(word)
        target = 1 if len(set(word)) == 1 else 0
        full_equations.append(f"({value})-1" if target else value)
        word_records.append({"word": "".join(map(str, word)), "target": target})
    guard = module.guard_equations()
    adjoint = module.adjoint_equations()
    if variant == "cap45_star1_three_term":
        incidence = module.incidence_equations()
        incidence_variables = list(module.RHO) + list(module.SIGMA) + [module.TAU]
    else:
        incidence, incidence_variables = alternate_incidence(module)
    equations = full_equations + guard + adjoint + incidence
    variables = (
        list(module.SOURCE.values()) + list(module.U) + list(module.V)
        + [item for name in "xyz" for item in module.DUAL[name]]
        + incidence_variables
    )
    expected_variables = 103 if variant == "cap45_star1_three_term" else 105
    assert len(variables) == expected_variables and len(set(variables)) == expected_variables
    assert len(equations) == 786
    lines = [
        "option(noredefine);",
        f"ring r={ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_SUBSET"); }',
        "quit;",
    ]
    ledger_sha = hashlib.sha256(json.dumps(word_records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return "\n".join(lines) + "\n", {
        "variables": len(variables), "equations": len(equations),
        "selected_full_x5_equations": len(full_equations),
        "guard_equations": len(guard), "adjoint_equations": len(adjoint),
        "incidence_equations": len(incidence), "selected_word_ledger_sha256": ledger_sha,
    }


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    module = load_core()
    inputs = {}
    counts = {}
    for variant in VARIANTS:
        inputs[variant] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            program, count = build_program(module, ring, variant)
            path = HERE / f"rep2_subset_{variant}_{label}.sing"
            atomic_write(path, program)
            inputs[variant][label] = {"path": path.name, "sha256": hashlib.sha256(program.encode()).hexdigest()}
            counts[variant] = count
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_INCIDENCE_SUBSET_V1",
        "status": "READY_BOUNDED_MODULAR_DIAGNOSTICS",
        "representative_id": 2,
        "equation_subset": "all and only 3 pure plus 762 mixed words using at most two colours",
        "subset_logic": "a unit ideal for a subset is an exact unit certificate for the full ideal; nonunit is diagnostic only",
        "variants": {
            "cap45_star1_three_term": {
                "factorization": "A04*K*[A35^T|A56|A57]",
                "counts": counts["cap45_star1_three_term"],
            },
            "cap03_star6_two_sandwich": {
                "factorization": "A04^T*K*[A23^T|A35]",
                "incidence": ["A04*rho=e0", "A23^T*sigma+A35*tau=e0"],
                "counts": counts["cap03_star6_two_sandwich"],
            },
        },
        "inputs": inputs,
        "run_policy": "modular only first; Q only after a terminal modular unit; <=120s sequential",
    }
    atomic_write(HERE / "rep2_incidence_subset_metadata.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "variants": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
