#!/usr/bin/env python3
"""Independent census, normalization, and exact-Q replay of all triple groups."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-boundary-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "52c4900fab9799096f4967dc04eaba223c36d640d787a87a5708652b2d187ee8",
    PARENT / "generate_sparse_pair01.py": "635049c3df63a3a078c1b03a0e99c20867e97acf3ce8c405d0641715242b42b9",
    PARENT / "single_relaxation_ledger.json": "0ccd1d583721d5a7fb9546acedff13e7405d2eacbb4117e65c0af8fe26c84fff",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_normalize(text, triple, base):
    # Independent implementation: canonicalize each bijection from the three
    # literal names to x,y,z, then take the byte minimum.
    tokens = ("x", "y", "z")
    expression = re.compile(r"\b(?:" + "|".join(re.escape(item) for item in triple) + r")\b")
    answers = []
    for image in itertools.permutations(tokens):
        mapping = dict(zip(triple, image))
        replaced = expression.sub(lambda match: mapping[match.group(0)], text)
        lines = replaced.splitlines()
        ring = f"ring r=0,({','.join(sorted(set(base) | set(tokens)))}),dp;"
        positions = [index for index, line in enumerate(lines) if line.startswith("ring r=0,")]
        assert len(positions) == 1
        lines[positions[0]] = ring
        answers.append("\n".join(lines) + "\n")
    canonical = min(answers)
    # Translate x,y,z to the production canonical token names before hashing.
    mapping = {"x": "extra0", "y": "extra1", "z": "extra2"}
    expression = re.compile(r"\b(?:x|y|z)\b")
    translated = expression.sub(lambda match: mapping[match.group(0)], canonical)
    lines = translated.splitlines()
    final_ring = f"ring r=0,({','.join(sorted(set(base) | set(mapping.values())))}),dp;"
    positions = [index for index, line in enumerate(lines) if line.startswith("ring r=0,")]
    assert len(positions) == 1
    lines[positions[0]] = final_ring
    return "\n".join(lines) + "\n"


def atomic_progress(stage, completed, total):
    path = HERE / "audit_progress.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps({
        "schema": "KRENN_X5_REP2_TRIPLE_AUDIT_PROGRESS_V1",
        "stage": stage,
        "completed": completed,
        "total": total,
    }, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    assert __debug__
    started = time.monotonic()
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    generator = load(PARENT / "generate_sparse_pair01.py")
    singles = json.loads((PARENT / "single_relaxation_ledger.json").read_text())
    zero = sorted(item["extra"] for item in singles["records"])
    expected = list(itertools.combinations(zero, 3))
    assert len(expected) == 54740

    ledger = json.loads((HERE / "triple_group_ledger.json").read_text())
    run = json.loads((HERE / "results_triple_groups.json").read_text())
    assert ledger["status"] == "PASS_ENUMERATION_ONLY_NO_IDEALS_RUN"
    assert ledger["raw_triple_count"] == 54740 and ledger["normalized_group_count"] == 3366
    assert run["status"] == "PASS_ALL_TRIPLE_GROUPS_UNIT"
    assert run["attempt_count"] == 3366 and run["attempted_raw_chart_coverage"] == 54740
    assert run["unit_count"] == 3366 and run["nonunit_count"] == run["failure_count"] == 0
    assert run["max_lane_wall_seconds"] < 2

    record_by_triple = {tuple(item["triple"]): item["normalized_sha256"] for item in ledger["triple_records"]}
    assert len(record_by_triple) == 54740 and set(record_by_triple) == set(expected)
    grouped = {
        tuple(triple): group["normalized_sha256"]
        for group in ledger["groups"] for triple in group["members"]
    }
    assert grouped == record_by_triple
    assert sum(len(group["members"]) for group in ledger["groups"]) == 54740
    group_by_digest = {group["normalized_sha256"]: group for group in ledger["groups"]}
    assert len(group_by_digest) == 3366
    for digest, group in group_by_digest.items():
        path = HERE / group["canonical_input"]
        assert sha256(path) == digest == group["canonical_input_sha256"]

    # Independent raw-chart regeneration and normalization hash replay.
    normalization_started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="rep2_triple_independent_") as temporary_directory:
        original_here = generator.HERE
        generator.HERE = Path(temporary_directory)
        try:
            for index, triple in enumerate(expected):
                generated = generator.build(generator.BASE_LIVE | set(triple), f"audit_{index}")
                raw = (generator.HERE / generated["path"]).read_text()
                canonical = independent_normalize(raw, triple, generator.BASE_LIVE)
                assert hashlib.sha256(canonical.encode()).hexdigest() == record_by_triple[triple]
                if (index + 1) % 1000 == 0:
                    atomic_progress("NORMALIZATION", index + 1, len(expected))
        finally:
            generator.HERE = original_here
    normalization_wall = time.monotonic() - normalization_started

    # Independent exact-Q replay of every canonical group.
    replay_started = time.monotonic()
    attempts = {item["normalized_sha256"]: item for item in run["attempts"]}
    assert len(attempts) == 3366 and set(attempts) == set(group_by_digest)
    replay_unit = 0
    for index, digest in enumerate(sorted(group_by_digest)):
        group = group_by_digest[digest]
        production = attempts[digest]
        assert production["status"] == "UNIT_IDEAL"
        assert production["member_count"] == len(group["members"])
        assert sha256(HERE / production["stdout"]) == production["stdout_sha256"]
        process = subprocess.run(
            ["gtimeout", "2", "Singular", str(HERE / group["canonical_input"])],
            capture_output=True, text=True, timeout=3,
        )
        stdout = process.stdout + process.stderr
        assert process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout
        assert "UNIT_REMAINDER=0" in stdout and "STATUS=NONUNIT" not in stdout
        replay_unit += 1
        if (index + 1) % 250 == 0:
            atomic_progress("SINGULAR_REPLAY", index + 1, len(group_by_digest))
    replay_wall = time.monotonic() - replay_started
    assert replay_unit == 3366

    result = {
        "schema": "KRENN_X5_REP2_SPARSE_TRIPLE_BOUNDARY_AUDIT_V1",
        "status": "PASS_EXACT_NO_FULL_PAIR01_POINT_WITH_AT_MOST_THREE_EXTRA_COORDINATES",
        "pins": {str(path): digest for path, digest in PINS.items()},
        "raw_triple_census": 54740,
        "normalized_group_census": 3366,
        "raw_normalization_hash_replays": 54740,
        "canonical_q_unit_replays": replay_unit,
        "production": {
            "unit": run["unit_count"],
            "nonunit": run["nonunit_count"],
            "failure": run["failure_count"],
            "raw_coverage": run["attempted_raw_chart_coverage"],
            "aggregate_wall_seconds": run["aggregate_wall_seconds"],
            "max_lane_wall_seconds": run["max_lane_wall_seconds"],
        },
        "audit_timing": {
            "normalization_wall_seconds": normalization_wall,
            "q_replay_wall_seconds": replay_wall,
            "total_wall_seconds": time.monotonic() - started,
        },
        "exact_minimum_extra_coordinate_lower_bound": 4,
        "scope": {
            "included": "base17 plus every zero-, one-, two-, or three-coordinate full pair01 amplitude chart over Q",
            "excluded": "guard, adjoint, incidence, rank nonzero, and charts with >=4 extra coordinates",
            "prior_388_triples": "not used; exhaustive 54740 census supersedes their diagnostic coverage",
        },
        "hostile_guards": [
            "triple set equality with C(70,3)",
            "group membership is a no-gap/no-duplicate partition",
            "independent six-permutation canonicalizer reproduces all54740 hashes",
            "all3366 Q ideals independently replay unit within2s",
            "no guard/adjoint/incidence conclusion inferred",
        ],
    }
    output = HERE / "results_triple_boundary_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    atomic_progress("COMPLETE", 1, 1)
    print(json.dumps({
        "status": result["status"],
        "raw": result["raw_triple_census"],
        "groups": result["normalized_group_census"],
        "unit_replays": replay_unit,
        "lower_bound": 4,
        "wall": result["audit_timing"]["total_wall_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
