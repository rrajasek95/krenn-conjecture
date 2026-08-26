#!/usr/bin/env python3
"""Strict zero-run self-audit for the exception1114 modular held package."""

import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPECTED = {
    "rank1_manifest": "aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46",
    "reduction_manifest": "785ec6cb6a5d790ece4fa3aed3801b48c3c51423e4378cd761ad8b50cd2d22b9",
    "q": "ed6a47ec38fca48e6b7396e36c61e3eca8004089bd2964476e1dcdd45b69de1f",
    "p": "4789b9cef4c3db41eb63819d66c7bd86f24f46a647a2665daf65c0b2b15beda3",
    "derivation": "7d2817c82cc0cfcbc6785fa8f47c2d122e84cc0523d72aea5c0240bd30baf34d",
    "runner": "545e9fb222bb3623ec8c3b5a09b45eec52a62489f79fcb91855e712463839c3c",
    "singular": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    "gtimeout": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def require(condition, detail="validation failure"):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def bytes_sha(value):
    return hashlib.sha256(value).hexdigest()


def validate_values(held, acceptance, clearance, exact_q, refusal, source, derivation, runner):
    require(held["schema"] == "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_HELD_V1")
    require(held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE")
    require(held["pins"] == {
        "rank1_refinement_manifest_sha256": EXPECTED["rank1_manifest"],
        "symbolic_reduction_manifest_sha256": EXPECTED["reduction_manifest"],
        "q_source_sha256": EXPECTED["q"], "modular_source_sha256": EXPECTED["p"],
        "source_derivation_sha256": EXPECTED["derivation"], "runner_sha256": EXPECTED["runner"],
        "singular_sha256": EXPECTED["singular"], "gtimeout_sha256": EXPECTED["gtimeout"],
    })
    require(held["source"] == {"path": "rep1114_rank1_z1_fulltorus_dedup_p32003.sing", "field": "F_32003", "variables": 58, "generators": 6533, "sha256": EXPECTED["p"]})
    execution = held["execution"]
    require(execution["maximum_lane_count"] == 1 and execution["native_wall_seconds"] == 300 and execution["wrapper_wall_seconds"] == 315)
    require(execution["rss_cap_bytes"] == 8 * 1024**3)
    require(all(execution[key] is True for key in ("direct_libproc_group_rss", "fresh_libproc_process_census", "atomic_result", "exclusive_attempt_marker", "strict_stop_after_any_outcome", "combined_sat_or_checker_overlap_forbidden")))
    require(held["authorization"] == {"independent_acceptance_present": False, "fresh_clearance_present": False, "exact_Q_authorized": False, "automatic_relaunch_authorized": False})
    require(held["scope"] == {"attempts": 0, "results": 0, "solver_runs": 0, "mathematical_coverage": False, "record1114_closed": False})

    require(acceptance["schema"] == "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_ACCEPTANCE_V1")
    require(acceptance["source_sha256"] == EXPECTED["p"] and acceptance["runner_sha256"] == EXPECTED["runner"])
    require(acceptance["prime"] == 32003 and acceptance["variables"] == 58 and acceptance["generators"] == 6533 and acceptance["maximum_lane_count"] == 1)
    require(acceptance["exact_Q_authorized"] is acceptance["automatic_relaunch_authorized"] is False)
    require(acceptance["held_manifest_sha256"].startswith("<"))

    require(clearance["schema"] == "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_CLEARANCE_V1")
    require(clearance["source_sha256"] == EXPECTED["p"] and clearance["runner_sha256"] == EXPECTED["runner"])
    require(clearance["maximum_lane_count"] == 1 and clearance["native_wall_seconds"] == 300 and clearance["wrapper_wall_seconds"] == 315 and clearance["rss_cap_bytes"] == 8 * 1024**3)
    require(clearance["expected_census_match_count"] == 0 and clearance["exact_Q_authorized"] is clearance["automatic_relaunch_authorized"] is False)
    require(clearance["held_manifest_sha256"].startswith("<") and clearance["nonce"].startswith("<"))

    require(exact_q["status"] == "HELD_DEPENDENCIES_ABSENT_NO_RUNNER_NO_LAUNCH")
    require(exact_q["q_source"]["sha256"] == EXPECTED["q"] and exact_q["q_source"]["variables"] == 58 and exact_q["q_source"]["generators"] == 6533)
    require(set(exact_q["required_future_dependencies"].values()) == {"UNIT_IDEAL_MODULAR_DIAGNOSTIC", None})
    require(exact_q["authorization"] == {"exact_Q_authorized": False, "runner_materialized": False, "launch_clearance_present": False, "automatic_followup": False})

    require(refusal["status"] == "REFUSE_UNTIL_ACCEPTANCE_AND_FRESH_CLEARANCE")
    require(refusal["missing_by_design"] == ["independent_referee_acceptance.json", "launch_clearance.json"])
    require(refusal["exact_Q_separately_conditional"] is True)
    require({"cadical", "drat-trim", "Singular", "gtimeout"} <= set(refusal["overlap_forbidden_executables"]))

    require(bytes_sha(source) == EXPECTED["p"])
    require(source.count(b"ring r=32003,(") == 1 and source.count(b"ideal G=slimgb(I);") == 1)
    require(source.count(b'print("INPUT_VARIABLES="+string(nvars(r)));') == 1)
    require(source.count(b'print("INPUT_GENERATORS="+string(size(I)));') == 1)
    for token in (b"option(redSB);", b"GROEBNER_SIZE=", b"UNIT_REMAINDER=", b"STATUS=UNIT_IDEAL", b"STATUS=NONUNIT_OR_UNRESOLVED"):
        require(source.count(token) == 1, token)
    ring_variables = source.split(b"ring r=32003,(", 1)[1].split(b"),dp;", 1)[0].split(b",")
    require(len(ring_variables) == 58 and len(set(ring_variables)) == 58)
    ideal = source.split(b"ideal I=", 1)[1].split(b";\nprint(\"INPUT_VARIABLES", 1)[0]
    require(ideal.count(b",\n") + 1 == 6533)

    require(derivation["status"] == "PASS_SOLE_Q_TO_P_RING_PLUS_STRONG_TRANSCRIPT_ZERO_RUN")
    require(derivation["input"]["sha256"] == EXPECTED["q"] and derivation["output"]["sha256"] == EXPECTED["p"])
    require(derivation["prime"]["value"] == 32003 and derivation["transformation"]["inverse_byte_replay"] is True)
    require(derivation["scope"] == {"solver_runs": 0, "attempts": 0, "launch_authorized": False, "exact_Q_authorized": False, "automatic_relaunch_authorized": False})

    require(bytes_sha(runner) == EXPECTED["runner"])
    for token in (b"NATIVE = 300", b"WRAPPER = 315", b"RSS_CAP = 8 * 1024**3", b"proc_listallpids", b"proc_listpgrppids", b"os.O_EXCL", b"start_new_session=True", b"ATTEMPT.json", b"automatic_relaunch", b"exact_Q_launched"):
        require(token in runner, token)
    for forbidden in (b'"cadical"', b'"drat-trim"', b'"Singular"', b'"gtimeout"'):
        require(forbidden in runner, forbidden)


def load_values():
    return (
        json.loads((HERE / "held_pilot.json").read_text()),
        json.loads((HERE / "independent_referee_acceptance.schema.json").read_text()),
        json.loads((HERE / "launch_clearance.schema.json").read_text()),
        json.loads((HERE / "exact_Q_followup_conditional.json").read_text()),
        json.loads((HERE / "refusal_contract.json").read_text()),
        (HERE / "rep1114_rank1_z1_fulltorus_dedup_p32003.sing").read_bytes(),
        json.loads((HERE / "source_derivation.json").read_text()),
        (HERE / "run_one_lane.py").read_bytes(),
    )


def main():
    require(sha(ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26/MANIFEST.sha256") == EXPECTED["rank1_manifest"])
    require(sha(ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26/MANIFEST.sha256") == EXPECTED["reduction_manifest"])
    q_path = ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26/rep1114_rank1_z1_fulltorus_dedup_Q.sing"
    require(sha(q_path) == EXPECTED["q"])
    require(sha(Path("/usr/local/bin/Singular")) == EXPECTED["singular"] and sha(Path("/usr/local/bin/gtimeout")) == EXPECTED["gtimeout"])
    require(sha(HERE / "source_derivation.json") == EXPECTED["derivation"] and sha(HERE / "run_one_lane.py") == EXPECTED["runner"])
    values = load_values()
    validate_values(*values)
    modular = values[5]
    q = q_path.read_bytes()
    strong = b'''option(redSB);
ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly unit_remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(unit_remainder));
if (unit_remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
'''
    require(modular.replace(b"ring r=32003,(", b"ring r=0,(", 1)[:-len(strong)] + b"quit;\n" == q)
    denominators = [int(value) for value in re.findall(rb"\(-?\d+/(\d+)\)", q)]
    require(all(value % 32003 for value in denominators))
    for name in ("independent_referee_acceptance.json", "launch_clearance.json", "RUN_EXCLUSIVE.lock", "ATTEMPT.json", "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json"):
        require(not (HERE / name).exists(), ("zero-run/stale refusal", name))
    require(not list(HERE.glob("*.tmp")))
    audit = json.loads((HERE / "results_self_audit.json").read_text())
    require(audit["status"] == "PASS_HELD_ZERO_RUN_SELF_AUDIT")
    require(audit["source"]["sha256"] == EXPECTED["p"] and audit["source"]["inverse_Q_byte_replay"] is True)
    require(audit["execution"]["solver_runs"] == audit["execution"]["attempts"] == audit["execution"]["results"] == 0)
    hostile = json.loads((HERE / "results_hostiles.json").read_text())
    require(hostile["status"] == "PASS_ALL_REJECTED" and hostile["count"] == 16 and hostile["solver_runs"] == 0)
    print("PASS held p32003 self-audit: exact 58/6533 source, hardened one lane, zero run")


if __name__ == "__main__":
    main()
