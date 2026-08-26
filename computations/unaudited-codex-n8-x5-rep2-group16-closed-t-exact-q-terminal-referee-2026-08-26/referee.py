#!/usr/bin/env python3
"""Independent terminal replay of the rep2 group16 closed-t exact-Q lane."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
C = ROOT / "computations"
RUN = C / "unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-conditional-held-2026-08-26"
HELD_REF = C / "unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-conditional-held-referee-2026-08-26"
MOD = C / "unaudited-codex-n8-x5-rep2-group16-closed-t-modular-held-2026-08-26"
MOD_REF = C / "unaudited-codex-n8-x5-rep2-group16-closed-t-modular-terminal-referee-2026-08-26"
BASE = C / "unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing"
RUNTIME = RUN / "rep2_group016_62_Vt0_Vt1_Vt2_Q_strong.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(manifest: Path) -> int:
    count = 0
    seen: set[Path] = set()
    for raw in manifest.read_text().splitlines():
        digest, name = raw.split(None, 1)
        target = Path(name.strip())
        target = target if target.is_absolute() else (manifest.parent / target).resolve()
        assert target.is_file() and target not in seen and sha(target) == digest
        seen.add(target)
        count += 1
    return count


assert sha(RUN / "MANIFEST.sha256") == "122fd1c6ef07f9955d2b4e8f908478d05e45aa8a9b5d8505f2b8e44ba89ae771"
assert replay(RUN / "MANIFEST.sha256") == 16
assert sha(RUNTIME) == "53fc0b26c52c5f55505c101c72ed0a7a73159092667edde4cdf1c573e4bd6795"
assert sha(RUN / "run_one_lane.py") == "0eeb4b6e56474a4ab451e6f5d006c00c1b0618e2cde14ab6bd152e7f3f8c5f92"
assert sha(RUN / "modular_unit_dependency.json") == "1366ccf2f49d0f8c149f590d79ccbf810933de8496a44bcd857b5f26f385141c"
assert sha(HELD_REF / "results_referee.json") == "19e391e6109cd3c9759e643d1b5406ef4d2b49d3e12bc8c7c76f563b46437d13"
assert sha(HELD_REF / "independent_referee_acceptance.json") == "1d4c6a58cf89118947d18370abe418b169e65a19a1a2ae7112e53ab3777ce302"
assert sha(HELD_REF / "FINAL_MANIFEST.sha256") == "e215dc4e29f9a74f88bb93de17647c1d43dd63e50e6c26274889103fa1a6152c"
assert replay(HELD_REF / "FINAL_MANIFEST.sha256") == 4
assert (RUN / "independent_referee_acceptance.json").read_bytes() == (HELD_REF / "independent_referee_acceptance.json").read_bytes()

assert sha(MOD / "result.json") == "7c7d9c890863548ae7efc079284cc418a9fab7dbc427ac234e16bd8e55c4f06e"
assert sha(MOD / "TERMINAL_MANIFEST.sha256") == "31d3c4290de2214fed4846909e0a1309a3adf103ea9415bea35a391e0a87999b"
assert sha(MOD_REF / "results_referee.json") == "07fabc04915cd909127774ae132eba470fa9917b9cf408ef220599b53a8448ff"
assert sha(MOD_REF / "FINAL_MANIFEST.sha256") == "2cfa80ecaa36de10f82a9dd1305683e7e50b3aa12c99a75cb75a20b536f34334"
replay(MOD / "TERMINAL_MANIFEST.sha256")
replay(MOD_REF / "FINAL_MANIFEST.sha256")

assert sha(RUN / "TERMINAL_MANIFEST.sha256") == "c38650a1008e3b29c5c927ecc72b151160416edb41748821c9e89320f87e001e"
assert replay(RUN / "TERMINAL_MANIFEST.sha256") == 6
assert [line.split(None, 1)[1].strip() for line in (RUN / "TERMINAL_MANIFEST.sha256").read_text().splitlines()] == [
    "MANIFEST.sha256", "independent_referee_acceptance.json", "launch_clearance.json",
    "ATTEMPT.json", "RUN_EXCLUSIVE.lock", "result.json",
]

old = b'print("INPUT_GENERATORS="+string(size(I)));\nquit;\n'
strong = (
    b'print("INPUT_GENERATORS="+string(size(I)));\nideal G=slimgb(I);\n'
    b'print("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\n'
    b'print("UNIT_REMAINDER="+string(remainder));\n'
    b'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'
)
assert sha(BASE) == "43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc"
assert RUNTIME.read_bytes().replace(strong, old, 1) == BASE.read_bytes()

acceptance = json.loads((RUN / "independent_referee_acceptance.json").read_text())
clearance = json.loads((RUN / "launch_clearance.json").read_text())
attempt = json.loads((RUN / "ATTEMPT.json").read_text())
lock = json.loads((RUN / "RUN_EXCLUSIVE.lock").read_text())
result = json.loads((RUN / "result.json").read_text())
assert sha(RUN / "result.json") == "4a8b6a51e66b06648789a62b8317fd73c381097d137e3ef61daf72c834c331c9"
assert sha(RUN / "launch_clearance.json") == "e11dfcf9cc2f6fddbc3e54373b26e8cfeff2ae67f2534887e38353d663faec07"
assert sha(RUN / "ATTEMPT.json") == "9a99b3df3440073f2458e7612e41fbef6c1e2008f5b8cecb7e8063f00fcba6de"
assert sha(RUN / "RUN_EXCLUSIVE.lock") == "5281377e47232e2edaeb67df45cbbc9c49d3f1b9e86d1f06e44d63e26dccb5dd"
assert acceptance["status"] == "PASS_APPROVE_ONE_CLOSED_T_EXACT_Q_ONLY"
assert acceptance["exact_Q_authorized"] is True and acceptance["other_chart_authorized"] is acceptance["automatic_relaunch_authorized"] is False
issued = datetime.fromisoformat(clearance["issued_at_utc"].replace("Z", "+00:00")).astimezone(timezone.utc)
expires = datetime.fromisoformat(clearance["expires_at_utc"].replace("Z", "+00:00")).astimezone(timezone.utc)
assert 0 < (expires - issued).total_seconds() <= 600
assert clearance["manager_clearance_confirmed"] is clearance["resource_clearance_confirmed"] is clearance["no_overlap_confirmed"] is True
assert clearance["expected_census_match_count"] == 0
assert (clearance["native_wall_seconds"], clearance["wrapper_wall_seconds"], clearance["rss_cap_bytes"]) == (480, 510, 8 * 1024**3)
assert clearance["nonce"] == attempt["nonce"] == lock["nonce"]
assert attempt["status"] == "ATTEMPT_CONSUMED" and attempt["relaunch_forbidden_even_if_no_result"] is True
assert attempt["prelaunch_census"]["match_count"] == 0 and attempt["prelaunch_census"]["matches"] == []
assert attempt["prelaunch_census"]["unobservable_pids"] == 0
assert attempt["prelaunch_census"]["policy_sha256"] == clearance["census_policy_sha256"]

required = {"INPUT_VARIABLES=62", "INPUT_GENERATORS=6568", "GROEBNER_SIZE=1", "UNIT_REMAINDER=0", "STATUS=UNIT_IDEAL"}
assert result["schema"] == "KRENN_X5_REP2_GROUP16_CLOSED_T_EXACT_Q_RESULT_V1"
assert result["status"] == "UNIT_IDEAL_EXACT_Q" and result["mathematical_coverage"] is True
assert result["field"] == "Q" and result["chart"] == "V(A67,A12,t0,t1,t2) intersect D(b0)"
assert (result["variables"], result["generators"]) == (62, 6568)
assert result["termination"] is None and result["returncode"] == 0 and result["stderr"] == ""
assert required <= set(result["stdout"].splitlines())
assert result["wall_seconds"] < 480 and result["peak_group_rss_bytes"] < 8 * 1024**3
assert result["strong_transcript_required"] is result["exact_Q_launched"] is True
assert result["other_chart_launched"] is result["prior_timeout_reused"] is result["automatic_relaunch"] is False
assert not list(RUN.glob("*.tmp")) and not (RUN / "result.json.tmp").exists()

chart_design = json.loads((MOD / "source_derivation.json").read_text())
assert chart_design["chart"]["single_chart_closes_group16"] is False

out = {
    "schema": "KRENN_X5_REP2_GROUP16_CLOSED_T_EXACT_Q_TERMINAL_REFEREE_V1",
    "status": "PASS_UNIT_IDEAL_EXACT_Q_CLOSED_T_CHART_ONLY",
    "field": "Q", "chart": result["chart"], "variables": 62, "generators": 6568,
    "groebner_basis_size": 1, "unit_remainder": 0,
    "wall_seconds": result["wall_seconds"], "peak_group_rss_bytes": result["peak_group_rss_bytes"],
    "result_sha256": sha(RUN / "result.json"), "terminal_manifest_sha256": sha(RUN / "TERMINAL_MANIFEST.sha256"),
    "held_manifest_sha256": sha(RUN / "MANIFEST.sha256"), "held_referee_manifest_sha256": sha(HELD_REF / "FINAL_MANIFEST.sha256"),
    "modular_terminal_manifest_sha256": sha(MOD / "TERMINAL_MANIFEST.sha256"),
    "modular_referee_manifest_sha256": sha(MOD_REF / "FINAL_MANIFEST.sha256"),
    "attempt_consumed": True, "resource_clear": True, "automatic_relaunch": False,
    "chart_exact_Q_coverage_promoted": True, "single_chart_closes_group16": False,
    "group16_closed": False, "rep2_closed_union": list(range(16)), "rep2_closed_count": 16,
    "rep2_closed": False, "seven_block_family_closed": False, "conjecture_closed": False,
    "remaining_scope": "other group16 charts and groups17..161",
}
(HERE / "results_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "audit_sha256": sha(HERE / "results_referee.json")}, sort_keys=True))
