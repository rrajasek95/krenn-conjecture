#!/usr/bin/env python3
"""Generate rep2 rank<=1/rank2 gates from two byte-pinned parameterized cores."""

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
RANK1_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25"
RANK2_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank2-incidence-gate-2026-08-25"
PINS = {
    RANK1_DIR / "MANIFEST.sha256": "45ab914ff35c446f67fcc2ec86a6d4201c8ddf3e0afed0b9420e269ad610daa9",
    RANK1_DIR / "generate_rank1_gate.py": "1fc2a1a62e4092f75cbb330009bbb9649e83e559167f251217a26b7eb3bc7c14",
    RANK2_DIR / "MANIFEST.sha256": "3e408289040035bf1dcf9152611d62cd495050817e9a990c0315483d8993b0de",
    RANK2_DIR / "generate_rank2_gates.py": "c5f2b37e404727550cd06d748bec84f9007b757be205704f88584e513fe6a98d",
}
REP0_ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)))
REP2_ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
EXPECTED_REP0_RANK1 = {
    "p32003": "28ffb8ee4206baa434630605479b21680bf6bbf10e5d1d391209d085fdbf0db1",
    "Q": "1fde037823a9ccf5d6aae9ce1d73485306867d9e3bf6e88675088262d18f55ea",
}
EXPECTED_REP0_RANK2 = {
    "all_equal": {"p32003": "c110dccf307bc3fc9969565fe7e0bb781559c0e5d9e1e0f46966746f02881493", "Q": "08d43774b82f8653236d6241f8639694488c23e55478e22ffe4a09b83c07558d"},
    "incidence_eq_u": {"p32003": "4d3cb71c03b5b28a3da15558b5500f95f7fd19ee8bfdfa70cd721e372a79cefc", "Q": "69b7df463d7dd5214035a38b18b7c86858a7b4a72dcf0acd62d8901dbd85258c"},
    "incidence_eq_v": {"p32003": "4b2996f1f3facea30e4ee6b349967ca823457ed7d74b2b0a6204c377fa6b1d04", "Q": "1135e7a4b449f905c7344e5e70078a064cde3ed30a64820f6bd38c6929bda5d6"},
    "minor_equal_not_incidence": {"p32003": "9dc2f69e80c929f286db312402c08267fe499ff96824e704e0afda1996c072f7", "Q": "fc52aa9feb635d3f93fa3b8614f00ef5086413c1802fed9352c2564ae8b9979f"},
    "all_distinct": {"p32003": "010464409f939ce6e30b71936a6bbaf566880a42d17ce3c83ac21e241da77cef", "Q": "2e2a2c0b65ce2a40462309c23649a78af51802ac91d2f8214f0d1ca810224cf8"},
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def load_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def reconfigure(module, added):
    module.ADDED = frozenset(added)
    module.NONFIXED = tuple(sorted(module.ADDED | module.VARIABLE))
    module.RETAINED = tuple(edge for edge in module.NONFIXED if edge not in module.ELIMINATED)
    module.SUPPORT = module.FIXED | set(module.NONFIXED)
    module.SUPPORTED = tuple(matching for matching in module.PM8 if set(matching) <= module.SUPPORT)
    assert len(module.SUPPORTED) == 13
    module.SOURCE = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in module.RETAINED
        for i, j in itertools.product(module.COLORS, repeat=2)
    }
    assert len(module.SOURCE) == 81


def supported_star_terms(support, cap=(4, 5), center=1):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    terms = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        if pa in support and qb in support:
            terms.append((a, b, "direct", pa, qb))
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pb in support and qa in support:
            terms.append((a, b, "switched", pb, qa))
    return tuple(terms)


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    for path, digest in PINS.items():
        assert sha256(path) == digest
    rank1 = load_module("sealed_rank1_core", RANK1_DIR / "generate_rank1_gate.py")
    rank2 = load_module("sealed_rank2_core", RANK2_DIR / "generate_rank2_gates.py")

    # Refactor control: before changing support, the imported cores must reproduce
    # every proof-producing rep0 input byte-for-byte.
    rep0_reproduction = {"rank1": {}, "rank2": {}}
    for label, ring in (("p32003", "32003"), ("Q", "0")):
        program, _ = rank1.build_program(ring, "slimgb")
        digest = sha256_text(program)
        assert digest == EXPECTED_REP0_RANK1[label]
        rep0_reproduction["rank1"][label] = digest
    for chart in rank2.CHARTS:
        rep0_reproduction["rank2"][chart["id"]] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            program, _ = rank2.build_program(ring, chart)
            digest = sha256_text(program)
            assert digest == EXPECTED_REP0_RANK2[chart["id"]][label]
            rep0_reproduction["rank2"][chart["id"]][label] = digest

    reconfigure(rank1, REP2_ADDED)
    reconfigure(rank2, REP2_ADDED)
    support = rank1.FIXED | rank1.VARIABLE | REP2_ADDED
    star = supported_star_terms(support)
    expected_star = (
        (0, 3, "direct", (0, 4), (3, 5)),
        (0, 6, "direct", (0, 4), (5, 6)),
        (0, 7, "direct", (0, 4), (5, 7)),
    )
    assert star == expected_star

    inputs = {"rank_le_one": {}, "rank_two": {}}
    counts = {}
    for label, ring in (("p32003", "32003"), ("Q", "0")):
        program, count = rank1.build_program(ring, "slimgb")
        path = HERE / f"rep2_rank1_{label}.sing"
        atomic_write(path, program)
        inputs["rank_le_one"][label] = {"path": path.name, "sha256": sha256_text(program)}
        counts["rank_le_one"] = count
    for chart in rank2.CHARTS:
        chart_id = chart["id"]
        inputs["rank_two"][chart_id] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            program, count = rank2.build_program(ring, chart)
            path = HERE / f"rep2_rank2_{chart_id}_{label}.sing"
            atomic_write(path, program)
            inputs["rank_two"][chart_id][label] = {"path": path.name, "sha256": sha256_text(program)}
            counts["rank_two"] = count

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_PARAMETERIZED_GATES_V1",
        "representative_id": 2,
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable": ["04", "12", "35", "67"],
            "added": ["06", "14", "17", "23", "26", "56", "57"],
        },
        "selection": {
            "guard_outside_site": 5,
            "low_rank_factor": "A57",
            "same_guard_shape_as_rep0": True,
            "direct_transport_from_rep0": False,
            "reason": "same single outside factor and the same 103/120-variable ranks, but a distinct source support",
        },
        "stored_edge_guard": {
            "at_identity": [
                "A06*A57^T=0",
                "A57^T+A17*A56^T=0",
                "A26*A57^T+A56^T=0",
            ],
            "derived": [
                "A56^T=-A26*A57^T",
                "(I-A17*A26)*A57^T=0",
                "A06*A57^T=0",
            ],
        },
        "candidate_star": {
            "cap": "45",
            "center": 1,
            "supported_forbidden_terms": [
                {"response": "03", "left": "04", "right": "35"},
                {"response": "06", "left": "04", "right": "56"},
                {"response": "07", "left": "04", "right": "57"},
            ],
            "factorization": "A04*K*[A35^T|A56|A57]",
            "P": "Row(A04)",
            "Q": "ColSpan(A35^T,A56,A57)=ColSpan(A35^T,U)",
        },
        "parameterized_core": {
            "rank1_source_sha256": PINS[RANK1_DIR / "generate_rank1_gate.py"],
            "rank2_source_sha256": PINS[RANK2_DIR / "generate_rank2_gates.py"],
            "rep0_byte_reproduction": rep0_reproduction,
            "supported_representatives": [0, 2],
            "not_claimed_for_other_representatives": [1, 3, 4, 5],
        },
        "substitution": {
            "rank_le_one": ["A57=u*v^T", "A56=-u*(A26*v)^T"],
            "rank_two": ["A57=U*V^T", "A56=-U*(A26*V)^T"],
        },
        "counts": counts,
        "inputs": inputs,
    }
    output = HERE / "rep2_gate_metadata.json"
    atomic_write(output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS_PARAMETERIZED_CORE_REPRODUCES_REP0_AND_GENERATES_REP2",
        "rep": 2,
        "rank1_inputs": 2,
        "rank2_inputs": 10,
        "star": result["candidate_star"]["factorization"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
