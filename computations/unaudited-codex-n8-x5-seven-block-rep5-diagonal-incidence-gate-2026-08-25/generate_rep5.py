#!/usr/bin/env python3
"""Generate rep5 incidence gates from a byte-reproduced sealed rep3 core."""

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
REP5_ADDED = frozenset(((0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 6), (3, 7)))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def load_core():
    specification = importlib.util.spec_from_file_location("sealed_rep3_incidence_core", CORE_DIR / "generate_gate.py")
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def reconfigure(module):
    module.ADDED = REP5_ADDED
    module.NONFIXED = tuple(sorted(module.VARIABLE | module.ADDED))
    module.RETAINED = tuple(item for item in module.NONFIXED if item != module.ELIMINATED)
    module.SUPPORT = module.FIXED | set(module.NONFIXED)
    module.SUPPORTED = tuple(matching for matching in module.PM8 if set(matching) <= module.SUPPORT)
    assert len(module.SUPPORTED) == 12
    module.SOURCE = {
        (block, i, j): f"a{block[0]}{block[1]}_{i}{j}"
        for block in module.RETAINED for i, j in itertools.product(module.COLORS, repeat=2)
    }
    assert len(module.SOURCE) == 90


def star_terms(support, cap=(0, 3), center=4):
    p, q = cap
    answer = []
    residual = tuple(site for site in range(8) if site not in cap)
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


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value)
    os.replace(temporary, path)


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected
    core = load_core()
    rep3_metadata = json.loads((CORE_DIR / "gate_metadata.json").read_text())
    reproduction = {}
    for chart in core.CHARTS:
        chart_id = f"p{chart[0]}{chart[1]}"
        reproduction[chart_id] = {}
        for label_ring, ring in (("p32003", "32003"), ("Q", "0")):
            program = core.build_program(ring, chart)
            digest = sha256_text(program)
            assert digest == rep3_metadata["inputs"][chart_id][label_ring]["sha256"]
            reproduction[chart_id][label_ring] = digest

    reconfigure(core)
    parent = json.loads(PARENT.read_text())["six_full_family_representatives"][5]
    assert parent["representative_id"] == 5
    assert parent["added"] == ["06", "15", "17", "24", "26", "36", "37"]
    digest, census = core.parent_digest_and_census()
    assert digest == parent["full_x5_6561_equation_sha256"] == "e8015349824f6851fba73d9ec57f4d8b59ea4ac686925415ff61c89b45df5f3a"
    assert {str(k): v for k, v in census.items()} == parent["full_x5_term_count_census"]
    assert parent["guard"]["fixed_identity_substitution"] == ["A06*A37^T=0", "A37^T+A17*A36^T=0", "A26*A37^T+A36^T=0"]
    terms = star_terms(core.SUPPORT)
    assert terms == (
        (5, 6, "switched", (0, 6), (3, 5)),
        (6, 7, "direct", (0, 6), (3, 7)),
    )
    carrier = next(item for item in parent["two_sandwich_stars"] if item["cap"] == "03" and item["star_center"] == 4 and item["common_block"] == "06")
    assert carrier["factorization_up_to_output_permutation"] == "A06^T*K*[A35|A37]"
    assert carrier["P"] == "Row(A06^T)" and carrier["Q"] == "ColSpan(A35,A37)"

    inputs = {}
    for chart in core.CHARTS:
        chart_id = f"p{chart[0]}{chart[1]}"
        inputs[chart_id] = {}
        for label_ring, ring in (("p32003", "32003"), ("Q", "0")):
            program = core.build_program(ring, chart)
            path = HERE / f"rep5_e0_{chart_id}_{label_ring}.sing"
            atomic_write(path, program)
            inputs[chart_id][label_ring] = {"path": path.name, "sha256": sha256_text(program)}
    metadata = {
        "schema": "KRENN_X5_REP5_DIAGONAL_INCIDENCE_GATE_V1",
        "status": "PASS_INPUT_GENERATION_AND_REP3_BYTE_REPRODUCTION",
        "representative_id": 5,
        "support": {"fixed": ["03", "16", "27", "45"], "variable": ["04", "12", "35", "67"], "added": parent["added"], "supported_matchings": 12},
        "source_orientation": {"elimination": "A36=-A37*A26^T", "guard": ["A06*A37^T=0", "(I-A17*A26)*A37^T=0"], "carrier": "A06^T*K*[A35|A37]", "P": "Col(A06)", "Q": "ColSpan(A35,A37)", "incidence": ["A06*x=e0", "A35*y+A37*z=e0"]},
        "s3_normalization": {"coordinate": 0, "residual_stabilizer": "swap 1 and 2", "outside_entry_orbits": [list(x) for x in core.CHARTS], "complete": True},
        "counts": {"variables": 100, "equations": 6586, "full_x5": 6561, "guard_after_elimination": 18, "incidence": 6, "saturation": 1},
        "parent_full_x5_digest": digest,
        "parent_term_census": census,
        "rep3_core_byte_reproduction": reproduction,
        "inputs": inputs,
        "scope": {"representative_5_only": True, "transport_claimed": False, "Q_requires_modular_unit": True},
    }
    atomic_write(HERE / "gate_metadata.json", json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": metadata["status"], "charts": 5, "rep": 5}, sort_keys=True))


if __name__ == "__main__":
    main()
