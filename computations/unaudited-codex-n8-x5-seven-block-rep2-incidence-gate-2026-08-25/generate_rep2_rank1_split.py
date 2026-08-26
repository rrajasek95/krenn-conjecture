#!/usr/bin/env python3
"""Generate five smaller exact rank-one gauge/minor charts for representative 2."""

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
CHARTS = (
    {"id": "all_equal", "u_pivot": 0, "v_pivot": 0, "orbit": "i=r=s"},
    {"id": "incidence_eq_u", "u_pivot": 0, "v_pivot": 1, "orbit": "i=r!=s"},
    {"id": "incidence_eq_v", "u_pivot": 1, "v_pivot": 0, "orbit": "i=s!=r"},
    {"id": "minor_equal_not_incidence", "u_pivot": 1, "v_pivot": 1, "orbit": "r=s!=i"},
    {"id": "all_distinct", "u_pivot": 1, "v_pivot": 2, "orbit": "all distinct"},
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def load_core():
    assert sha256(CORE) == CORE_SHA256
    specification = importlib.util.spec_from_file_location("sealed_rank1_split_core", CORE)
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


def build_chart(module, ring, chart):
    original_u = tuple(f"u{i}" for i in module.COLORS)
    module.U = tuple("1" if i == chart["u_pivot"] else original_u[i] for i in module.COLORS)
    module.V = tuple(f"v{i}" for i in module.COLORS)
    module.DUAL = {name: tuple(f"{name}{i}" for i in module.COLORS) for name in "xyz"}
    module.RHO = tuple(f"rho{i}" for i in module.COLORS)
    module.SIGMA = tuple(f"sigma{i}" for i in module.COLORS)
    module.TAU = "tau"

    full_equations = []
    pure = mixed = 0
    for word in itertools.product(module.COLORS, repeat=8):
        value = module.amplitude(word)
        if len(set(word)) == 1:
            full_equations.append(f"({value})-1")
            pure += 1
        else:
            full_equations.append(value)
            mixed += 1
    guard = module.guard_equations()
    adjoint = module.adjoint_equations()
    incidence = module.incidence_equations()
    inverse = f"eta*{module.V[chart['v_pivot']]}-1"
    equations = full_equations + guard + adjoint + incidence + [inverse]
    variables = (
        list(module.SOURCE.values())
        + [name for name in module.U if name != "1"] + list(module.V)
        + [item for name in "xyz" for item in module.DUAL[name]]
        + list(module.RHO) + list(module.SIGMA) + [module.TAU, "eta"]
    )
    assert len(variables) == 103 and len(set(variables)) == 103
    assert len(equations) == 6583
    lines = [
        "option(noredefine);",
        f"ring r={ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n", {
        "variables": len(variables),
        "equations": len(equations),
        "full_x5_equations": len(full_equations),
        "pure_equations": pure,
        "mixed_equations": mixed,
        "guard_equations": len(guard),
        "adjoint_equations": len(adjoint),
        "incidence_equations": len(incidence),
        "inverse_equations": 1,
    }


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    module = load_core()
    inputs = {}
    counts = None
    for chart in CHARTS:
        inputs[chart["id"]] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            program, counts = build_chart(module, ring, chart)
            path = HERE / f"rep2_rank1split_{chart['id']}_{label}.sing"
            atomic_write(path, program)
            inputs[chart["id"]][label] = {"path": path.name, "sha256": sha256_text(program)}
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_RANK1_SPLIT_V1",
        "status": "READY_FIVE_EXACT_GAUGE_MINOR_CHARTS",
        "representative_id": 2,
        "support_added": ["06", "14", "17", "23", "26", "56", "57"],
        "prior_unsplit_failures": {
            "Q120_sha256": "c254b996535894c0948f1918e739aba8e362b9e6e0d3835a0c089423214cd90b",
            "Q300_sha256": "dd7fb62677a61dac320fb4c23febed3027e98c1943e27820104562c65dd159d0",
            "mathematical_coverage": False,
        },
        "zero_rank_branch": {
            "status": "CLOSED_STRUCTURALLY",
            "proof": (
                "A57=0 gives A56=0; hence L67=0. The full-family stratum has A67 nonzero, so its "
                "Frobenius functional is live on ker(L67)=Mat3 and cap67/triangle012 is active."
            ),
        },
        "rank_one_charts": {
            "normalization": "choose u_r!=0 and scale u_r=1; impose eta*v_s-1=0",
            "coverage": "all nonzero rank-one factors, modulo diagonal S3 on (failed colour i,r,s)",
            "failed_colour": 0,
            "charts": CHARTS,
            "counts": counts,
        },
        "inputs": inputs,
        "scope": {
            "new_ideals_not_wall_widening": True,
            "same_full_x5_provider": True,
            "same_guard_and_adjoint": True,
            "Q_coverage_before_runs": False,
        },
    }
    atomic_write(HERE / "rep2_rank1_split_metadata.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "charts": 5,
        "variables": counts["variables"],
        "equations": counts["equations"],
        "zero_rank": "closed_structurally",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
