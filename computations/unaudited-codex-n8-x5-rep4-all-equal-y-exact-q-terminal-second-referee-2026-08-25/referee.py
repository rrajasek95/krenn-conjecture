#!/usr/bin/env python3
"""Independent terminal audit of the sole rep4 all-equal-y exact-Q chart."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-2026-08-25"
FIRST = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-referee-2026-08-25"
HELD_REF = ROOT / "computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-referee-2026-08-25"

PINS = {
    RUN / "MANIFEST.sha256": "7b93ce7bee8ac3d8bad0384490ee511a819e9c4b1d800b776dc8016897a30d20",
    RUN / "TERMINAL_MANIFEST.sha256": "ff3178d7b546d4afadeeb8659001685d7d5bd3bb78c73b06b33ed539184e6d5d",
    RUN / "HELD_EXACT_Q_PLAN.json": "ed0a6b95a9cf6e228e22eb588c41de9f6b8140560e4eed853489375526dd31a0",
    RUN / "HELD_LAUNCH_RECORD.json": "8bc79fecd19e85c8e86703d1bcc6e83cda4c1cf18f1661b5a9e9287e9d9ce48b",
    RUN / "rep4_all_equal_y_exact_Q.sing": "c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019",
    RUN / "run_exact_q.py": "1892065935daf8ad47530fee138f48ed4a5d6a772320018f6e9d94cfddab894a",
    RUN / "independent_referee_acceptance.json": "e5e3a7ce1d048d126418f478bde7672cebc4436f7b3ac77161a0a67c4113f52a",
    RUN / "launch_clearance.json": "b4ae5caf5fb900cbc2335793f991cca3329417723004823d6ec9d116c2e537f1",
    RUN / "ATTEMPT.json": "cb893de39383977d31d675294ca39682bf827696289c8e763ce698bee569d7fe",
    RUN / "result.json": "e7c85aeb41733abedde2aa0fda09d127d56690097ff83a57269a52c18ea46a9c",
    HELD_REF / "FINAL_MANIFEST.sha256": "a3c78897012074016ae2fd105d4a06d33d605a531aa65c7c52dc494b1988a947",
    FIRST / "results_referee.json": "ccc22fe2ec3d5db1d3ed3d175e5196819efa3e412cf632ef8c862ae70f3b72d3",
    FIRST / "FINAL_MANIFEST.sha256": "a8280c98344eb62f6df89ffec125e6cdba33a7dae63f47061c71114f7aabe805",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def replay(manifest: Path) -> None:
    for line in manifest.read_text().splitlines():
        expected, name = line.split(None, 1)
        path = Path(name.strip())
        if not path.is_absolute():
            path = (manifest.parent / path).resolve()
        assert sha256(path) == expected, (path, sha256(path), expected)


def top_level_items(body: str) -> list[str]:
    """Split a Singular expression list without trusting printed size(I)."""
    items: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(body):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            items.append(body[start:index].strip())
            start = index + 1
    assert depth == 0
    items.append(body[start:].strip())
    assert all(items)
    return items


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
for manifest in (
    RUN / "MANIFEST.sha256",
    RUN / "TERMINAL_MANIFEST.sha256",
    HELD_REF / "FINAL_MANIFEST.sha256",
    FIRST / "FINAL_MANIFEST.sha256",
):
    replay(manifest)

# Independent literal source census: the Q ring and ideal really contain 91/6577.
source = (RUN / "rep4_all_equal_y_exact_Q.sing").read_text()
ring_match = re.search(r"^ring r=0,\(([^\n]+)\),dp;$", source, re.MULTILINE)
assert ring_match
variables = [name.strip() for name in ring_match.group(1).split(",")]
assert len(variables) == 91 and len(set(variables)) == 91
ideal_match = re.search(r"^ideal I=(.*?);\nprint\(\"INPUT_VARIABLES", source, re.MULTILINE | re.DOTALL)
assert ideal_match
generators = top_level_items(ideal_match.group(1))
assert len(generators) == 6577
assert "ideal G=slimgb(I);" in source
assert "poly remainder=reduce(1,G);" in source
assert source.count("STATUS=UNIT_IDEAL") == 1

# Independently parse the raw result and require the strong transcript, not status alone.
result = json.loads((RUN / "result.json").read_text())
assert result["schema"] == "KRENN_X5_REP4_ALL_EQUAL_Y_EXACT_Q_ONE_LANE_RESULT_V1"
assert result["status"] == "UNIT_IDEAL_EXACT_Q_SAME_CHART"
assert result["field"] == "Q" and result["variables"] == len(variables)
assert result["generators"] == len(generators)
assert result["termination"] is None and result["wrapper_returncode"] == 0
assert result["stderr"] == "" and result["mathematical_coverage"] is True
strong_transcript = [
    "INPUT_VARIABLES=91",
    "INPUT_GENERATORS=6577",
    "GROEBNER_SIZE=1",
    "UNIT_REMAINDER=0",
    "STATUS=UNIT_IDEAL",
    "Auf Wiedersehen.",
]
stdout_lines = result["stdout"].splitlines()
assert stdout_lines[-6:] == strong_transcript
assert all(result["stdout"].count(marker) == 1 for marker in strong_transcript)
assert result["wall_seconds"] == 8.554205416003242
assert result["observed_peak_group_rss_bytes"] == 284_598_272
assert result["observed_peak_group_members"] == 2
assert result["wall_seconds"] < result["native_wall_cap_seconds"] == 480
assert result["observed_peak_group_rss_bytes"] < result["rss_cap_bytes"] == 8 * 1024**3
assert result["internal_wrapper_enforced_seconds"] == 510
assert result["prelaunch_census"]["match_count"] == 0
assert result["prelaunch_census"]["unobservable_pids"] == 0

# Pinned authorization, atomic publication, and exactly-one-lane terminality.
attempt = json.loads((RUN / "ATTEMPT.json").read_text())
clearance = json.loads((RUN / "launch_clearance.json").read_text())
assert attempt["status"] == "ATTEMPT_CONSUMED"
assert attempt["relaunch_forbidden_even_if_no_result"] is True
assert attempt["nonce"] == result["nonce"] == clearance["nonce"]
assert result["held_manifest_sha256"] == PINS[RUN / "MANIFEST.sha256"]
assert result["source_sha256"] == PINS[RUN / "rep4_all_equal_y_exact_Q.sing"]
assert result["runner_sha256"] == PINS[RUN / "run_exact_q.py"]
assert result["independent_referee_acceptance_sha256"] == PINS[RUN / "independent_referee_acceptance.json"]
assert result["launch_clearance_sha256"] == PINS[RUN / "launch_clearance.json"]
assert clearance["maximum_lane_count"] == 1
assert clearance["exact_Q_authorized"] is True
assert clearance["second_lane_authorized"] is False
assert clearance["automatic_relaunch_authorized"] is False
assert result["exact_Q_launched"] is True
assert result["second_lane_launched"] is False
assert result["automatic_relaunch"] is False
assert result["rep2_equivalence_used"] is False

runner = (RUN / "run_exact_q.py").read_text()
assert runner.count("subprocess.Popen(") == 1
assert "os.replace(temporary, path)" in runner
assert "exclusive_json(HERE / \"ATTEMPT.json\", attempt)" in runner
assert "atomic_json(HERE / \"result.json\", result)" in runner
assert len(list(RUN.glob("result.json"))) == 1
assert len(list(RUN.glob("ATTEMPT.json"))) == 1
assert not list(RUN.rglob("*.tmp"))
assert not list(RUN.glob("stdout.log")) and not list(RUN.glob("stderr.log"))

first = json.loads((FIRST / "results_referee.json").read_text())
assert first["status"] == "PASS_EXACT_Q_UNIT_IDEAL_REP4_ALL_EQUAL_Y_SAME_CHART"
assert first["result_sha256"] == PINS[RUN / "result.json"]
assert first["terminal_manifest_sha256"] == PINS[RUN / "TERMINAL_MANIFEST.sha256"]

out = {
    "schema": "KRENN_X5_REP4_ALL_EQUAL_Y_EXACT_Q_TERMINAL_SECOND_REFEREE_V1",
    "status": "PASS_EXACT_Q_STRONG_UNIT_IDEAL_ONE_REP4_CHART_ONLY",
    "field": "Q",
    "variables_independently_counted": len(variables),
    "generators_independently_counted": len(generators),
    "groebner_basis_size_from_transcript": 1,
    "unit_remainder_from_transcript": 0,
    "strong_unit_transcript_exact": True,
    "source_sha256": PINS[RUN / "rep4_all_equal_y_exact_Q.sing"],
    "result_sha256": PINS[RUN / "result.json"],
    "producer_terminal_manifest_sha256": PINS[RUN / "TERMINAL_MANIFEST.sha256"],
    "first_referee_result_sha256": PINS[FIRST / "results_referee.json"],
    "first_referee_manifest_sha256": PINS[FIRST / "FINAL_MANIFEST.sha256"],
    "wall_seconds": result["wall_seconds"],
    "peak_group_rss_bytes": result["observed_peak_group_rss_bytes"],
    "atomic_result": True,
    "single_lane_only": True,
    "second_lane_launched": False,
    "automatic_relaunch": False,
    "scope": {
        "one_rep4_all_equal_y_chart_closed": True,
        "rep4_representative_closed": False,
        "cross_representative_claim": False,
        "full_family_closed": False,
        "conjecture_closed": False,
    },
}
(HERE / "results_second_referee.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": out["status"], "result_sha256": sha256(HERE / "results_second_referee.json")}, sort_keys=True))
