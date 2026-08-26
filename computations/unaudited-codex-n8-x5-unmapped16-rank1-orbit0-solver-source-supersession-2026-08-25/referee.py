#!/usr/bin/env python3
"""Referee the solver epilogue and superseding held staged plan; never solve."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
OLD_REF = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25"
AMEND = ROOT / "computations/unaudited-codex-n8-x5-rectangle-rank1-orbit0-p32003-pilot-2026-08-25"
Q_DIAGNOSTIC = DESIGN / "rank1_orbit0_i0_I0_J0_Q.sing"
P_EXECUTE = AMEND / "rank1_orbit0_p32003_execute.sing"
OUT = HERE / "results_referee.json"
PLAN = HERE / "SUPERSEDING_STAGED_HELD_PLAN.json"

EXPECTED = {
    DESIGN / "MANIFEST.sha256": "743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf",
    Q_DIAGNOSTIC: "1d9875cab81417094d51193862f40097b1c03e4816aedd8ceaf07a917eeb248b",
    OLD_REF / "FINAL_MANIFEST.sha256": "e3e7974ae201f5915e7eeec95f7b01e3db37f0ddfe69619d00a4c1a84a92838f",
    OLD_REF / "STAGED_PILOT_HELD_PLAN.json": "95120b83be0d16fb16b7814556c676caa7a01c1436e85ed884db98a210571c34",
    AMEND / "EXECUTION_SOURCE_AMENDMENT.json": "dbe489cc5e63e2793917aaa83f7f8e76e4d6427a42809da8d32ea014616fb154",
    AMEND / "prepare_execution_source.py": "7172e551e2d83f3f1ed4e7b6f23324f4bbf542603ee51a04131d318a2b4be187",
    P_EXECUTE: "7c34d1efbf74220f01a6ea150ede232b9f51f9168f15dd997ed2b204e8aacf9c",
}

OLD_TAIL = '''print("INPUT_VARIABLES="+string(nvars(r)));
print("INPUT_GENERATORS="+string(size(I)));
quit;
'''
SOLVER_TAIL = '''print("INPUT_VARIABLES="+string(nvars(r)));
print("INPUT_GENERATORS="+string(size(I)));
ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def validate_pair(q_diagnostic, p_execute):
    assert q_diagnostic.count("ring r=0,") == 1
    assert "ring r=32003," not in q_diagnostic
    assert q_diagnostic.endswith(OLD_TAIL)
    assert "slimgb(" not in q_diagnostic and "reduce(" not in q_diagnostic
    p_diagnostic = q_diagnostic.replace("ring r=0,", "ring r=32003,", 1)
    assert sha_bytes(p_diagnostic.encode()) == "b70098251cfe8aceb845c1a3c2af92a5ae944e9bfcb1c611d21adada8edd44cb"
    expected_execute = p_diagnostic[:-len(OLD_TAIL)] + SOLVER_TAIL
    assert p_execute == expected_execute
    assert p_execute.count("ring r=32003,") == 1 and "ring r=0," not in p_execute
    assert p_execute.count("ideal G=slimgb(I);") == 1
    assert p_execute.count("poly remainder=reduce(1,G);") == 1
    assert p_execute.count("STATUS=UNIT_IDEAL") == 1
    assert p_execute.count("STATUS=NONUNIT_OR_UNRESOLVED") == 1
    assert p_execute.count("quit;") == 1
    q_execute = p_execute.replace("ring r=32003,", "ring r=0,", 1)
    assert sha_bytes(q_execute.encode()) == "c062396aa8835e9c31d0e845a997d89f3b1d151f6494d36d5ba990cdadf9c44f"
    # The complete ring+ideal prefix is byte-identical: only field and tail differ.
    q_prefix = q_diagnostic[:-len(OLD_TAIL)]
    p_prefix = p_execute[:-len(SOLVER_TAIL)].replace("ring r=32003,", "ring r=0,", 1)
    assert q_prefix == p_prefix
    return p_diagnostic, q_execute


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
q_diagnostic = Q_DIAGNOSTIC.read_text()
p_execute = P_EXECUTE.read_text()
p_diagnostic, q_execute = validate_pair(q_diagnostic, p_execute)
amendment = json.loads((AMEND / "EXECUTION_SOURCE_AMENDMENT.json").read_text())
assert amendment["status"] == "PREPARED_NOT_RUN_REQUIRES_SUPERSEDING_CLEARANCE"
assert amendment["held_plan_sha256"] == EXPECTED[OLD_REF / "STAGED_PILOT_HELD_PLAN.json"]
assert amendment["Q_source_sha256"] == EXPECTED[Q_DIAGNOSTIC]
assert amendment["held_p32003_no_solve_sha256"] == sha_bytes(p_diagnostic.encode())
assert amendment["execution_source_sha256"] == EXPECTED[P_EXECUTE]
assert amendment["execution_source_bytes"] == len(p_execute.encode()) == 519401
assert amendment["solver_launches"] == 0

# Fail-closed hostile mutations exercise both the unchanged-ideal and unique-
# epilogue contracts.
hostiles = {}
mutations = {
    "ideal_prefix_mutation": q_diagnostic.replace("a01_00", "a01_01", 1),
    "missing_reduce": p_execute.replace("poly remainder=reduce(1,G);", "poly remainder=0;", 1),
    "extra_slimgb": p_execute.replace("ideal G=slimgb(I);", "ideal H=slimgb(I);\nideal G=slimgb(I);", 1),
    "wrong_field": p_execute.replace("ring r=32003,", "ring r=32009,", 1),
    "missing_nonunit_status": p_execute.replace("STATUS=NONUNIT_OR_UNRESOLVED", "STATUS=UNIT_IDEAL", 1),
}
for name, mutation in mutations.items():
    try:
        if name == "ideal_prefix_mutation":
            validate_pair(mutation, p_execute)
        else:
            validate_pair(q_diagnostic, mutation)
    except AssertionError:
        hostiles[name] = True
    else:
        hostiles[name] = False
assert all(hostiles.values())

plan = json.loads(PLAN.read_text())
assert plan["status"] == "APPROVE_HELD_NOT_RUN_REQUIRES_EXPLICIT_CLEARANCE"
assert plan["launch_authorized"] is False
assert plan["supersedes_plan_sha256"] == EXPECTED[OLD_REF / "STAGED_PILOT_HELD_PLAN.json"]
assert plan["superseded_plan_defect"] == "both frozen field sources ended after count prints and quit, so their stated unit acceptance tokens were unreachable"
assert plan["stages"][0]["source_sha256"] == EXPECTED[P_EXECUTE]
assert plan["stages"][1]["derived_Q_solver_source_sha256"] == sha_bytes(q_execute.encode())
assert plan["automatic_relaunch"] is False and plan["second_chart_authorized"] is False

audit = {
    "schema": "KRENN_X5_RANK1_ORBIT0_SOLVER_SOURCE_SUPERSESSION_REFEREE_V1",
    "status": "PASS_SOLVER_EPILOGUE_EXACT_HELD_NOT_RUN",
    "old_plan_sha256": EXPECTED[OLD_REF / "STAGED_PILOT_HELD_PLAN.json"],
    "old_plan_disposition": "REJECT_SUPERSEDED_UNLAUNCHED",
    "Q_diagnostic_source_sha256": EXPECTED[Q_DIAGNOSTIC],
    "p32003_diagnostic_source_sha256": sha_bytes(p_diagnostic.encode()),
    "p32003_execution_source_sha256": EXPECTED[P_EXECUTE],
    "Q_execution_source_expected_sha256": sha_bytes(q_execute.encode()),
    "variables": 76,
    "generators": 6571,
    "unchanged_ring_ideal_prefix": True,
    "sole_solver_epilogue": True,
    "hostile_tests": hostiles,
    "solver_launches": 0,
    "superseding_held_plan_sha256": sha(PLAN),
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
