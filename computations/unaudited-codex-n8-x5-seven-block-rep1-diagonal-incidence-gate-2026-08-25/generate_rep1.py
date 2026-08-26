#!/usr/bin/env python3
"""Generate the exact representative-1 diagonal-incidence ideals.

The sealed representative-3 generator is first reproduced byte-for-byte.  We
then independently replace the support, eliminated outside block, guard, and
carrier incidence for representative 1.
"""

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
CORE_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep3-diagonal-incidence-gate-2026-08-25"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/results_full_family_obligation.json"
PINS = {
    CORE_DIR / "MANIFEST.sha256": "43c6847a284f4745ffbb37f7d92ef74bfc80a3118ce7e5d0f8ca0b31b4df3ffd",
    CORE_DIR / "generate_gate.py": "592534f29786414f4ee741716d38a838f78cbae63590f66f23cd9f3695a322b0",
    PARENT: "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
}
REP1_ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 5), (2, 6), (4, 6), (4, 7)))
ELIMINATED = (4, 6)
OUTSIDE = (4, 7)
CHARTS = ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value)
    os.replace(temporary, path)


def load_core():
    specification = importlib.util.spec_from_file_location("sealed_rep3_incidence_core", CORE_DIR / "generate_gate.py")
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def star_terms(support, cap=(0, 3), center=4):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    answer = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pa in support and qb in support:
            answer.append((a, b, "direct", pa, qb))
        if pb in support and qa in support:
            answer.append((a, b, "switched", pb, qa))
    return tuple(answer)


def normalized_chart(i, p, q):
    candidates = []
    for permutation in itertools.permutations(range(3)):
        if permutation[i] == 0:
            candidates.append((permutation[p], permutation[q]))
    answer = min(candidates)
    assert answer in CHARTS
    return answer


def configure_rep1(core):
    core.ADDED = REP1_ADDED
    core.NONFIXED = tuple(sorted(core.VARIABLE | core.ADDED))
    core.ELIMINATED = ELIMINATED
    core.RETAINED = tuple(item for item in core.NONFIXED if item != core.ELIMINATED)
    core.SUPPORT = core.FIXED | set(core.NONFIXED)
    core.SUPPORTED = tuple(matching for matching in core.PM8 if set(matching) <= core.SUPPORT)
    assert len(core.SUPPORTED) == 12
    core.SOURCE = {
        (block, i, j): f"a{block[0]}{block[1]}_{i}{j}"
        for block in core.RETAINED for i, j in itertools.product(core.COLORS, repeat=2)
    }
    assert len(core.SOURCE) == 90

    def entry(edge, i, j):
        if edge in core.FIXED:
            return "1" if i == j else "0"
        if edge == ELIMINATED:
            # A46^T=-A26*A47^T, hence A46=-A47*A26^T.
            value = core.sum_string(
                core.atom_product(core.source(OUTSIDE, i, k), core.source((2, 6), j, k))
                for k in core.COLORS
            )
            return f"-({value})"
        return core.source(edge, i, j)

    core.entry = entry


def guard_equations(core):
    equations = []
    # A06*A47^T=0.
    for i, j in itertools.product(core.COLORS, repeat=2):
        equations.append(core.sum_string(
            core.atom_product(core.source((0, 6), i, k), core.source(OUTSIDE, j, k))
            for k in core.COLORS
        ))
    # (I-A17*A26)*A47^T=0.
    for i, j in itertools.product(core.COLORS, repeat=2):
        correction = core.sum_string(
            core.atom_product(
                core.source((1, 7), i, k),
                core.source((2, 6), k, ell),
                core.source(OUTSIDE, j, ell),
            )
            for k, ell in itertools.product(core.COLORS, repeat=2)
        )
        equations.append(f"{core.source(OUTSIDE, j, i)}-({correction})")
    return equations


def incidence_equations(core, coordinate=0):
    equations = []
    # e_coordinate in P=Col(A06).
    for i in core.COLORS:
        value = core.sum_string(core.atom_product(core.source((0, 6), i, j), core.X[j]) for j in core.COLORS)
        equations.append(f"({value})-{int(i == coordinate)}")
    # e_coordinate in Q=ColSpan(A13^T,A35).
    for i in core.COLORS:
        value = core.sum_string(
            [core.atom_product(core.source((1, 3), j, i), core.Y[j]) for j in core.COLORS]
            + [core.atom_product(core.source((3, 5), i, j), core.Z[j]) for j in core.COLORS]
        )
        equations.append(f"({value})-{int(i == coordinate)}")
    return equations


def build_program(core, ring, chart, algorithm="slimgb"):
    full = []
    for word in itertools.product(core.COLORS, repeat=8):
        value = core.amplitude(word)
        full.append(f"({value})-1" if len(set(word)) == 1 else value)
    equations = full + guard_equations(core) + incidence_equations(core, 0)
    equations.append(f"{core.source(OUTSIDE, chart[0], chart[1])}*{core.SAT}-1")
    variables = list(core.SOURCE.values()) + list(core.X) + list(core.Y) + list(core.Z) + [core.SAT]
    assert len(variables) == len(set(variables)) == 100
    assert len(equations) == 6586
    lines = [
        "option(noredefine);",
        f"ring r={ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        f"ideal G={algorithm}(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n"


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected
    core = load_core()
    rep3_metadata = json.loads((CORE_DIR / "gate_metadata.json").read_text())
    reproduction = {}
    for chart in core.CHARTS:
        chart_id = f"p{chart[0]}{chart[1]}"
        reproduction[chart_id] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            digest = sha256_text(core.build_program(ring, chart))
            assert digest == rep3_metadata["inputs"][chart_id][label]["sha256"]
            reproduction[chart_id][label] = digest

    configure_rep1(core)
    parent = json.loads(PARENT.read_text())["six_full_family_representatives"][1]
    assert parent["representative_id"] == 1
    assert parent["added"] == ["06", "13", "17", "25", "26", "46", "47"]
    digest, census = core.parent_digest_and_census()
    assert digest == parent["full_x5_6561_equation_sha256"] == "61640fb492640847a58cf9f5e2f1dbc3f381736d7909325f35b2dfffb211d5eb"
    assert {str(key): value for key, value in census.items()} == parent["full_x5_term_count_census"]
    assert parent["guard"]["fixed_identity_substitution"] == [
        "A06*A47^T=0", "A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0",
    ]
    terms = star_terms(core.SUPPORT)
    assert terms == (
        (1, 6, "switched", (0, 6), (1, 3)),
        (5, 6, "switched", (0, 6), (3, 5)),
    )
    carrier = next(
        item for item in parent["two_sandwich_stars"]
        if item["cap"] == "03" and item["star_center"] == 4 and item["common_block"] == "06"
    )
    assert carrier["factorization_up_to_output_permutation"] == "A06^T*K*[A13^T|A35]"
    assert carrier["P"] == "Row(A06^T)" and carrier["Q"] == "ColSpan(A13^T,A35)"

    cases = {
        f"i{i}_p{p}{q}": list(normalized_chart(i, p, q))
        for i, p, q in itertools.product(range(3), repeat=3)
    }
    assert len(cases) == 27 and set(map(tuple, cases.values())) == set(CHARTS)

    inputs = {}
    for chart in CHARTS:
        chart_id = f"p{chart[0]}{chart[1]}"
        inputs[chart_id] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            program = build_program(core, ring, chart)
            path = HERE / f"rep1_e0_{chart_id}_{label}.sing"
            atomic_write(path, program)
            inputs[chart_id][label] = {"path": path.name, "sha256": sha256_text(program)}

    metadata = {
        "schema": "KRENN_X5_REP1_DIAGONAL_INCIDENCE_GATE_V1",
        "status": "PASS_INPUT_GENERATION_AND_ORIENTATION_CENSUS",
        "representative_id": 1,
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable": ["04", "12", "35", "67"],
            "added": parent["added"],
            "supported_matchings": len(core.SUPPORTED),
            "star_terms": [list(item) for item in terms],
        },
        "source_orientation": {
            "elimination": "A46=-A47*A26^T",
            "guard": ["A06*A47^T=0", "(I-A17*A26)*A47^T=0"],
            "carrier": "A06^T*K*[A13^T|A35]",
            "P": "Col(A06)",
            "Q": "ColSpan(A13^T,A35)",
            "incidence": ["A06*x=e0", "A13^T*y+A35*z=e0"],
        },
        "s3_normalization": {
            "coordinate": 0,
            "residual_stabilizer": "swap colors 1 and 2",
            "outside_entry_orbits": [list(item) for item in CHARTS],
            "case_ledger": cases,
            "all_27_cases_covered": True,
        },
        "counts": {"variables": 100, "equations": 6586, "full_x5": 6561, "guard_after_elimination": 18, "incidence": 6, "saturation": 1},
        "parent_full_x5_digest": digest,
        "parent_term_census": census,
        "rep3_core_byte_reproduction": reproduction,
        "inputs": inputs,
        "scope": {"representative_1_only": True, "transport_claimed": False, "Q_requires_modular_unit": True, "first_run_only": "p00/p32003"},
    }
    atomic_write(HERE / "gate_metadata.json", json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": metadata["status"], "rep": 1, "charts": 5, "variables": 100, "equations": 6586}, sort_keys=True))


if __name__ == "__main__":
    main()
