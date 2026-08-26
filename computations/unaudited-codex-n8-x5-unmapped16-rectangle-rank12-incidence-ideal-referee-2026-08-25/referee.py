#!/usr/bin/env python3
"""Independent static referee for the rank-1/rank-2 incidence ideals."""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROD = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
PARENT_REF = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-referee-2026-08-25"
OUT = HERE / "results_referee.json"
PLAN = HERE / "STAGED_PILOT_HELD_PLAN.json"

EXPECTED = {
    PROD / "MANIFEST.sha256": "743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf",
    PROD / "results_rank12_incidence_design.json": "96b13ad342acd0fb02c37015b86303c9d6d7d880abe0e2a4e21f5e9e1aea5a28",
    PROD / "generate_design.py": "2e75fb413a7585fe149d407477360afcd0ede4e19965f5a43db257cd70a2d625",
    PARENT / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    PARENT / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
    PARENT_REF / "FINAL_MANIFEST.sha256": "e60df2b5c052c3955c33471717aadb7f4d44b2d15203cad26d8e8753ceb223a6",
    PARENT_REF / "results_referee.json": "f1e412c4320139fdd268088fa790adbeb071ff2689d5009aa241e6b937a90ef2",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_manifest(path):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        assert sha(path.parent / rel.strip()) == digest, (path, rel)
        count += 1
    return count


def top_level_count(body):
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            count += 1
    assert depth == 0
    return count


def orbit_census(rank):
    colors = range(3)
    permutations = tuple(itertools.permutations(colors))
    values = [
        (i, rows, columns)
        for i in colors
        for rows in itertools.combinations(colors, rank)
        for columns in itertools.combinations(colors, rank)
    ]

    def act(value, permutation):
        i, rows, columns = value
        return (
            permutation[i],
            tuple(sorted(permutation[x] for x in rows)),
            tuple(sorted(permutation[x] for x in columns)),
        )

    unseen = set(values)
    groups = []
    while unseen:
        seed = min(unseen)
        orbit = {act(seed, p) for p in permutations}
        assert orbit <= set(values)
        unseen -= orbit
        groups.append((min(orbit), len(orbit)))
    return groups


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(PROD / "MANIFEST.sha256")
result = json.loads((PROD / "results_rank12_incidence_design.json").read_text())
assert result["schema"] == "KRENN_X5_RECTANGLE_4647_RANK12_INCIDENCE_IDEAL_DESIGN_V1"
assert result["status"] == "PASS_EXACT_MATERIALIZATION_NO_SOLVE"
assert result["support"] == ["01", "15", "17", "23", "26", "46", "47"]
assert result["records"] == {"A12_absent": 0, "A12_present": 2}
assert result["guard_and_carrier"] == {
    "original_guard": ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"],
    "substitutions": ["A46=-A47*A26^T", "A47=U*V^T", "(I-A17*A26)*V=0"],
    "carrier": "cap27/star1: [A23^T|A26^T]*K*A47^T",
    "inactive_diagonal_incidence": ["V*z=e_i", "A23*u+A26*w=e_i"],
}

# Independent finite common-S3 orbit census.
groups1 = orbit_census(1)
groups2 = orbit_census(2)
assert len(groups1) == len(groups2) == 5
assert sum(size for _, size in groups1) == sum(size for _, size in groups2) == 27
assert [size for _, size in groups1] == [3, 6, 6, 6, 6]
assert [size for _, size in groups2] == [6, 6, 6, 6, 3]
assert result["chart_census"] == {"raw_per_rank": 27, "S3_orbits_per_rank": 5, "canonical_inputs": 10}

# U[I,:]=I_r fixes the GL_r gauge.  The selected saturation is exactly the
# remaining det(V[J,:]) != 0 chart condition; the forward/reverse formulas
# in the producer result are mutually inverse on that chart.
parameter = result["minimal_rank_parameterization"]
assert parameter["chart"].startswith("choose I,J with det(A47[I,J])!=0")
assert parameter["forward"].startswith("U=A47[:,J]*A47[I,J]^-1")
assert parameter["reverse"].startswith("U[I,:]=I_r and det(V[J,:])!=0")
assert parameter["saturation"] == "sat*det(V[J,:])-1"
assert parameter["gauge_removed"] == "r^2 variables removed from the parent U,V factorization; rank1 77->76, rank2 84->80 for the A12-free ideal"

expected_counts = {1: (76, 6571), 2: (80, 6574)}
canonical = result["canonical_inputs"]
assert len(canonical) == 10
seen = set()
for item in canonical:
    rank = item["rank"]
    variables_expected, generators_expected = expected_counts[rank]
    path = PROD / item["path"]
    assert path.name not in seen
    seen.add(path.name)
    assert sha(path) == item["sha256"]
    source = path.read_text()
    assert source.startswith("// DESIGN INPUT ONLY: do not run")
    assert source.count("ring r=0,") == 1 and "ring r=32003," not in source
    ring_start = source.index("ring r=0,(") + len("ring r=0,(")
    ring_end = source.index("),dp;", ring_start)
    variables = [x.strip() for x in source[ring_start:ring_end].split(",")]
    assert len(variables) == len(set(variables)) == variables_expected == item["variables"]
    assert all(not x.startswith("a12_") for x in variables)
    ideal_start = source.index("ideal I=(") + len("ideal I=")
    ideal_end = source.index(";\nprint(\"INPUT_VARIABLES=", ideal_start)
    generators = top_level_count(source[ideal_start:ideal_end])
    assert generators == generators_expected == item["generators"]
    assert "slimgb(" not in source and "std(" not in source and "reduce(" not in source
    assert source.count("quit;") == 1

assert result["counts"] == {
    "generator_breakdown": {
        "full_x5": 6561, "guard": {"rank1": 3, "rank2": 6},
        "V_incidence": 3, "partner_incidence": 3, "rank_saturation": 1,
    },
    "rank1": {"variables": 76, "generators": 6571, "canonical_inputs": 5},
    "rank2": {"variables": 80, "generators": 6574, "canonical_inputs": 5},
}
assert result["variants"]["same_ideal"] is True
assert result["variants"]["A12_absent_lift"] == "A12=0"
assert result["variants"]["A12_present_lift"] == "A12=I_3"
assert result["scope"] == {"inputs_materialized": 10, "solver_launches": 0, "records_closed": 0}
assert all(result["hostile_tests"].values())

plan = json.loads(PLAN.read_text())
assert plan["status"] == "HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE"
assert plan["launch_authorized"] is False
assert plan["chart"]["Q_source_sha256"] == canonical[0]["sha256"]
assert plan["chart"]["rank"] == 1 and plan["chart"]["orbit_index"] == 0
assert plan["stages"][0]["field"] == "F_32003"
assert plan["stages"][1]["field"] == "Q"
assert plan["stages"][1]["requires"] == "stage1 exact UNIT plus independent audit and fresh explicit clearance"

audit = {
    "schema": "KRENN_X5_RECTANGLE_RANK12_INCIDENCE_IDEAL_REFEREE_V1",
    "status": "PASS_EXACT_FINITE_DESIGN_NO_SOLVE_NO_CLOSURE",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_result_sha256": EXPECTED[PROD / "results_rank12_incidence_design.json"],
    "manifest_entries_replayed": manifest_entries,
    "gauge": "A47=U*V^T with U[I,:]=I_r and sat*det(V[J,:])-1",
    "counts": result["counts"],
    "orbit_census": {
        "rank1_raw": 27, "rank1_orbits": 5, "rank1_sizes": [size for _, size in groups1],
        "rank2_raw": 27, "rank2_orbits": 5, "rank2_sizes": [size for _, size in groups2],
        "canonical_Q_inputs": 10,
    },
    "A12_lifts_share_ideal": True,
    "solver_launches": 0,
    "records_closed": 0,
    "staged_pilot_held_plan_sha256": sha(PLAN),
    "scope": "design/materialization only; no incidence, unmapped16, or conjecture closure",
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
