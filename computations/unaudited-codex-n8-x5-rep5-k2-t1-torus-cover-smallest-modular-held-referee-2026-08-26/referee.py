#!/usr/bin/env python3
"""Independent zero-run referee for the rep5 smallest torus modular package."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELD = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-torus-cover-smallest-modular-held-2026-08-26"
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26"
DESIGN_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-referee-2026-08-26"
TIMEOUT_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_top(text: str) -> list[str]:
    out, depth, start = [], 0, 0
    for i, char in enumerate(text):
        if char == "(": depth += 1
        elif char == ")": depth -= 1
        elif char == "," and depth == 0:
            out.append(text[start:i]); start = i + 1
    out.append(text[start:])
    assert depth == 0
    return out


TOKEN = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*|[0-9]+|[-+*()])")


class TermCounter:
    """Count leaves after formal distribution without constructing expansion."""
    def __init__(self, source: str):
        self.tokens = TOKEN.findall(source)
        assert "".join(self.tokens) == re.sub(r"\s+", "", source)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def pop(self, expected=None):
        token = self.tokens[self.pos]; self.pos += 1
        if expected is not None: assert token == expected
        return token

    def parse(self):
        value = self.expression(); assert self.pos == len(self.tokens); return value

    def expression(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            self.pop(); value += self.term()
        return value

    def term(self):
        value = self.factor()
        while self.peek() == "*":
            self.pop(); value *= self.factor()
        return value

    def factor(self):
        if self.peek() in ("+", "-"):
            self.pop(); return self.factor()
        if self.peek() == "(":
            self.pop(); value = self.expression(); self.pop(")"); return value
        self.pop(); return 1


def source_census(path: Path) -> dict:
    text = path.read_text()
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    generators = split_top(text.split("ideal I=", 1)[1].split(";\n", 1)[0])
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path),
        "bytes": len(text.encode()),
        "variables": len(variables),
        "generators": len(generators),
        "expanded_syntax_term_count": sum(TermCounter(g).parse() for g in generators),
    }


def check_runner(text: str) -> None:
    ast.parse(text)
    required = (
        "NATIVE=240", "WRAPPER=255", "RSS_CAP=8*1024**3",
        "proc_listallpids", "proc_pidpath", "proc_listpgrppids", "proc_pid_rusage",
        "start_new_session=True", "grouprss(process.pid)", "os.killpg",
        "os.O_EXCL", "os.replace(t,path)", "assert not list(H.glob('*.tmp'))",
        "maximum_lane_count", "exact_Q_authorized", "other_chart_authorized",
        "automatic_relaunch_authorized", "relaunch_forbidden_even_if_no_result",
        "NATIVE_WALL_CAP_240", "RSS_CAP_8GIB",
    )
    assert all(literal in text for literal in required)
    forbidden = ("subprocess.run(['ps'", "subprocess.check_output(['ps'", "shell=True")
    assert not any(literal in text for literal in forbidden)


def main() -> None:
    assert sha256(HELD / "MANIFEST.sha256") == "21df0017be41a8ec9e4035b0902649cf9c8ed97d43c65c88a93d1db7f8bf6d72"
    assert sha256(DESIGN / "MANIFEST.sha256") == "2b220f91ffa21c28506f5112a3a3e7fe791c7e3c783c1e7a319186628743659e"
    assert sha256(DESIGN_REF / "MANIFEST.sha256") == "20f24c8de6e7edb0818c30c11df4716e983fd5f8bf5778ee36d6d3bccf27d0ff"
    assert sha256(TIMEOUT_REF / "FINAL_MANIFEST.sha256") == "0cb2ba3080ddda143ac01e4fd9f8714876c070ee86e7e574415c22cae4cac4ff"
    timeout = json.loads((TIMEOUT_REF / "results_referee.json").read_text())
    assert timeout["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
    assert timeout["mathematical_coverage"] is False and timeout["automatic_relaunch"] is False

    ledger = json.loads((HELD / "selection_ledger.json").read_text())
    paths = sorted(DESIGN / item["path"] for item in ledger["candidates"])
    assert len(paths) == 16 and len(set(paths)) == 16
    census = [source_census(path) for path in paths]
    assert all((x["variables"], x["generators"], x["bytes"], x["expanded_syntax_term_count"]) ==
               (73, 6561, 4416511, 5322351) for x in census)
    selected = min(census, key=lambda x: (x["bytes"], x["expanded_syntax_term_count"], x["sha256"]))
    assert selected["sha256"] == "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0"

    q = (ROOT / selected["path"]).read_bytes()
    modular_path = HELD / "rep5_k2_t1_gauge_yn11_yn21_t01_t20_p32003.sing"
    modular = modular_path.read_bytes()
    strong = (
        b'ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\n'
        b'poly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\n'
        b'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'
    )
    expected = q.replace(b"ring r=0,(", b"ring r=32003,(", 1)[:-len(b"quit;\n")] + strong
    assert modular == expected
    assert sha256(modular_path) == "c36bd3b77052487b43751b03f48849c76091ec121a04abc3305cb56ec6494a8b"
    assert modular.count(b"ring r=32003,(") == 1 and modular.count(b"slimgb(I)") == 1

    runner_path = HELD / "run_one_lane.py"
    runner_text = runner_path.read_text()
    assert sha256(runner_path) == "76ed54497a532b28bb69b4d5a1243220af19cb7bdb4a4dd4b19d9b8a5b99d17f"
    check_runner(runner_text)
    # Four independent hostile mutations must fail the static runner contract.
    hostiles = []
    for label, mutated in (
        ("native", runner_text.replace("NATIVE=240", "NATIVE=241", 1)),
        ("rss", runner_text.replace("RSS_CAP=8*1024**3", "RSS_CAP=9*1024**3", 1)),
        ("observer", runner_text.replace("grouprss(process.pid)", "(0,0)", 1)),
        ("atomic", runner_text.replace("os.replace(t,path)", "path.write_text(t.read_text())", 1)),
    ):
        rejected = False
        try: check_runner(mutated)
        except AssertionError: rejected = True
        assert rejected
        hostiles.append({"name": label, "rejected": True})

    held = json.loads((HELD / "held_pilot.json").read_text())
    assert held["status"] == "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE"
    assert held["scope"]["attempts"] == held["scope"]["solver_runs"] == held["scope"]["results"] == 0
    assert held["scope"]["prior_timeout_reused"] is False
    absent = [
        "independent_referee_acceptance.json", "launch_clearance.json", "ATTEMPT.json",
        "result.json", "result.json.tmp", "stdout.log", "stderr.log", "watchdog.json", "RUN_EXCLUSIVE.lock",
    ]
    assert all(not (HELD / name).exists() for name in absent)
    assert not list(HELD.glob("*.tmp")) and not list(HELD.rglob("__pycache__"))
    for schema_name in ("independent_referee_acceptance.schema.json", "launch_clearance.schema.json"):
        schema = json.loads((HELD / schema_name).read_text())
        assert schema["additionalProperties"] is False
        assert set(schema["required"]) == set(schema["properties"])

    result = {
        "schema": "KRENN_X5_REP5_K2_T1_TORUS_SMALLEST_MODULAR_HELD_REFEREE_V1",
        "status": "PASS_APPROVED_HELD_ZERO_RUN",
        "held_manifest_sha256": sha256(HELD / "MANIFEST.sha256"),
        "design_manifest_sha256": sha256(DESIGN / "MANIFEST.sha256"),
        "design_referee_manifest_sha256": sha256(DESIGN_REF / "MANIFEST.sha256"),
        "prior_timeout_referee_manifest_sha256": sha256(TIMEOUT_REF / "FINAL_MANIFEST.sha256"),
        "candidate_count": 16,
        "selection_rule": ["source_bytes", "expanded_syntax_term_count", "lexicographic_sha256"],
        "all_tied_before_sha": True,
        "selected_Q_sha256": selected["sha256"],
        "modular_source_sha256": sha256(modular_path),
        "variables": 73,
        "generators": 6561,
        "runner_sha256": sha256(runner_path),
        "native_wall_seconds": 240,
        "wrapper_wall_seconds": 255,
        "rss_cap_bytes": 8589934592,
        "direct_libproc_group_rss": True,
        "atomic_result": True,
        "hostiles": hostiles,
        "attempts": 0,
        "solver_runs": 0,
        "mathematical_coverage": False,
        "exact_Q_authorized": False,
        "other_chart_authorized": False,
        "automatic_relaunch_authorized": False,
        "approval_scope": "held one-lane F_32003 diagnostic only; still requires fresh independent acceptance and manager/resource clearance",
    }
    (HERE / "results_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
