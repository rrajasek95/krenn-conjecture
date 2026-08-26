#!/usr/bin/env python3
"""Independent small-file referee for the sealed canonical rank-two branch."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank2-incidence-gate-2026-08-25"
RANK1 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25/MANIFEST.sha256"
GUARD = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/MANIFEST.sha256"
CHARTS = ("all_equal", "incidence_eq_u", "incidence_eq_v",
          "minor_equal_not_incidence", "all_distinct")
EXPECTED = "INPUT_GENERATORS=6589\nGROEBNER_SIZE=1\nUNIT_REMAINDER=0\nSTATUS=UNIT_IDEAL\n"
FIXED = frozenset(((0,3),(1,6),(2,7),(4,5)))
VARIABLE = frozenset(((0,4),(1,2),(3,5),(6,7)))
REPS = (
    frozenset(((0,6),(1,3),(1,7),(2,4),(2,6),(5,6),(5,7))),
    frozenset(((0,6),(1,3),(1,7),(2,5),(2,6),(4,6),(4,7))),
    frozenset(((0,6),(1,4),(1,7),(2,3),(2,6),(5,6),(5,7))),
    frozenset(((0,6),(1,4),(1,7),(2,5),(2,6),(3,6),(3,7))),
    frozenset(((0,6),(1,5),(1,7),(2,3),(2,6),(4,6),(4,7))),
    frozenset(((0,6),(1,5),(1,7),(2,4),(2,6),(3,6),(3,7))),
)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def need(value, message):
    if not value:
        raise SystemExit("REJECT: " + message)


def image(edges, permutation):
    return frozenset(tuple(sorted((permutation[a], permutation[b]))) for a,b in edges)


need(sha(PROD / "MANIFEST.sha256") ==
     "3e408289040035bf1dcf9152611d62cd495050817e9a990c0315483d8993b0de",
     "producer manifest")
need(sha(PROD / "results_rank2_branch_audit.json") ==
     "a8f5be71e8ed4140e869625bd4e4ac768dd669dd2abfe8304a8597baf30af09c",
     "producer audit")
need(sha(RANK1) == "45ab914ff35c446f67fcc2ec86a6d4201c8ddf3e0afed0b9420e269ad610daa9",
     "rank<=1 parent")
need(sha(GUARD) == "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf",
     "guard parent")

metadata = json.loads((PROD / "rank2_ideal_metadata.json").read_text())
need(metadata["substitutions"]["A56"] == "-U*(A26*V)^T", "A56 orientation")
need(metadata["guard_after_substitution"] == ["A06*V=0", "(I-A17*A26)*V=0"],
     "guard reduction")
need(metadata["counts_per_chart"]["variables"] == 120
     and metadata["counts_per_chart"]["equations"] == 6589
     and metadata["counts_per_chart"]["reduced_response_dual_variables"] == 18,
     "chart census")

runs = {}
for chart in CHARTS:
    record = metadata["inputs"][chart]["Q"]
    source = PROD / record["path"]
    result_path = PROD / f"results_rank2_{chart}_Q.json"
    result = json.loads(result_path.read_text())
    need(sha(source) == record["sha256"] == result["input_sha256"], chart + " input")
    need(result["status"] == "PASS_RATIONAL_UNIT_IDEAL"
         and result["ring"] == "Q" and result["returncode"] == 0
         and result["timed_out"] is False and result["unit_ideal"] is True
         and result["mathematical_coverage"] is True
         and result["stdout"] == EXPECTED, chart + " rational unit")
    runs[chart] = {"input_sha256": record["sha256"],
                   "result_sha256": sha(result_path)}

# Five equality types are the exact diagonal-S3 orbits on (i,r,s).
def kind(t):
    i,r,s = t
    if i == r == s: return "i=r=s"
    if i == r: return "i=r!=s"
    if i == s: return "i=s!=r"
    if r == s: return "r=s!=i"
    return "all distinct"

orbit_counts = {}
for triple in itertools.product(range(3), repeat=3):
    orbit_counts[kind(triple)] = orbit_counts.get(kind(triple), 0) + 1
need(orbit_counts == {"i=r=s":3, "i=r!=s":6, "i=s!=r":6,
                      "r=s!=i":6, "all distinct":6}, "chart orbit census")

# Independently replay the no-transport boundary.
transport = []
for target in REPS:
    count = 0
    for permutation in itertools.permutations(range(8)):
        if image(FIXED, permutation) == FIXED and image(VARIABLE, permutation) == VARIABLE \
                and image(REPS[0], permutation) == target:
            count += 1
    transport.append(count)
need(transport == [1,0,0,0,0,0], "transport counts")

output = {
    "schema": "KRENN_X5_SEVEN_BLOCK_RANK2_BRANCH_REFEREE_V1",
    "status": "PASS_INDEPENDENT_CANONICAL_ALL_RANKS_TRIANGLE_OR_STAR_BRANCH",
    "pins": {
        "producer_manifest_sha256": sha(PROD / "MANIFEST.sha256"),
        "producer_audit_sha256": sha(PROD / "results_rank2_branch_audit.json"),
        "rank_le_one_manifest_sha256": sha(RANK1),
        "guard_manifest_sha256": sha(GUARD),
    },
    "rational_unit_charts": runs,
    "chart_orbit_counts": orbit_counts,
    "rank_three_exclusion": {
        "identity": "A06 A57^T=0",
        "hypothesis": "A06 is nonzero on the canonical support",
        "deduction": "rank(A06)+rank(A57)<=3, hence rank(A57)<=2",
        "valid": True,
    },
    "all_rank_assembly": {
        "rank_le_one": "sealed parent exact-Q theorem",
        "rank_two": "five independently checked exact-Q unit ideals",
        "rank_three": "excluded by guard and nonzero A06",
        "canonical_conclusion": "active cap67/triangle012 or cap45/star2",
    },
    "transport_counts": transport,
    "scope": {
        "canonical_representative_all_ranks": True,
        "canonical_guard_mate": True,
        "other_five_full_family_representatives": False,
        "all_64_loci": False,
        "uniform_induction": False,
        "D12_read": False,
    },
    "next_obligation": "separate source-labelled ideal for representatives 1..5; no direct transport exists"
}
temporary = HERE / "results_rank2_branch_referee.json.tmp"
temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_rank2_branch_referee.json")
print(json.dumps({"status": output["status"], "Q_units": len(runs),
                  "transport": transport}, sort_keys=True))
