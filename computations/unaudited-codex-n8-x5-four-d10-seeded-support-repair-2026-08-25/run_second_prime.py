#!/usr/bin/env python3
"""Run the conditionally authorized p=1000000007 seeded D10 repairs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PRIME = 1000000007
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_four_d10_seeded_repair"
WATCHDOG = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d9-resumable-single-branch-design-2026-08-25/watchdog8_180_resume.py"
PINS = {"source": "162fb54dfc1c28f93d1a6f0a7dbbb0827f18c57645a28ab0fb602cf1bd3e85b6", "binary": "48cce22f3f5c9cb897b98b65a7f3d1fb971f115fc696c404170cb2148f7c211a", "watchdog": "370c4c9e07ebbba03f459542e23cd68882aa10c455e309aee2a6dce1e2eb46d1"}
BRANCHES = {
    "direct": ("343383c57eed5de414052f8defeaa91784dd9ced0df5355338e328f346f8a3a1", 58, "1ba8170e8270a138c18a724b47d3f9e22794a530dedba2b59fd9a1108c6c0b58", "1f52d09bb9c06ec9bb6a8e5c034a7a3a7adaecd8ce1e439d47a9a02d0305f57d"),
    "triangle_endpoint_colour": ("1a58301d9a316c37fda825bf1112d38b5bae19479308f7de23fe5ef7b0d8ee16", 54, "77c28c29782512148a7898383634a62c2bbdcffe9fc253b1878703cb45baad90", "5b0b75493bcc80ba1fb4bb9ecdbb52ebe3983f4bed72fab1002389fb7d9b2ff1"),
    "third_colour": ("e761815e90f949bce7ab32598749610e36db54293b87693a7af522241acde1ec", 54, "bc53e3db9771589ba254c7a83473c40fa8775d5ff08f4a7742f9aeaae69a1bcd", "9962b1905f39e887f14d7fd6a2373f46c5714f4dfca6e3475843c94ddd5ea266"),
    "cap_endpoint_colour": ("08aaff0a26cb8d4b382e889ea956e48654baf856f80810162fc19d12c2eba744", 54, "45267e78fcccfd29ac5b039302e9943e1cd66148ade75f20ce61afb75a1e1697", "c6d70d02e57ef6eb440061a790f225f3e8e9e492daab02af29a0d587c7606caf"),
}

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    first = json.loads((HERE / "results_first_prime.json").read_text())
    assert first["status"] == "PASS_FOUR_GLOBAL_MODULAR_DUALS" and first["all_four_global_duals"] is True
    for path, expected in ((SOURCE, PINS["source"]), (BINARY, PINS["binary"]), (WATCHDOG, PINS["watchdog"])):
        assert sha(path) == expected
    records = []
    for branch, (provider_sha, seed_count, selected_sha, seed_sha) in BRANCHES.items():
        provider = HERE / f"provider_{branch}_p{PRIME}.ms"
        seed_dir = HERE / f"seed_{branch}_p{PRIME}"
        selected, seed_dual = seed_dir / "selected.tsv", seed_dir / "transported_d9_dual.tsv"
        for path, expected in ((provider, provider_sha), (selected, selected_sha), (seed_dual, seed_sha)):
            assert sha(path) == expected
        output = HERE / f"p{PRIME}_{branch}"
        assert not output.exists()
        output.mkdir()
        command = [str(BINARY), "--branch", branch, "--input", str(provider), "--resume-selected", str(selected),
                   "--resume-dual", str(seed_dual), "--resume-round-offset", "0", "--output", str(output / "result.json"),
                   "--selected", str(output / "selected.tsv"), "--dual", str(output / "dual.tsv"), "--prime", str(PRIME),
                   "--column-cap", "200000", "--wall-seconds", "175"]
        wrapper = [sys.executable, str(WATCHDOG), "--rss-gib", "8", "--wall-seconds", "180", "--poll-seconds", "0.25",
                   "--source", str(SOURCE), "--expected-source-sha256", PINS["source"], "--expected-binary-sha256", PINS["binary"],
                   "--telemetry", str(output / "watchdog.json"), "--stdout", str(output / "stdout.log"),
                   "--stderr", str(output / "stderr.log"), "--", *command]
        completed = subprocess.run(wrapper, cwd=REPO, check=False)
        assert (output / "result.json").exists()
        result, watch = json.loads((output / "result.json").read_text()), json.loads((output / "watchdog.json").read_text())
        assert completed.returncode == 0 and watch["status"] == "PASS_TERMINAL"
        assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D10_RESUMABLE_RESULT_V1"
        assert result["branch"] == branch and result["prime"] == PRIME and result["degree"] == 10
        assert result["resumed_columns"] == seed_count and result["transported_seed_loaded"] is True
        assert result["selected_columns"] <= 200000 and result["elapsed_seconds"] < 180
        assert result["status"] in {"COMPLETE_MODULAR_DUAL_DIAGNOSTIC", "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY"}
        record = {"branch": branch, "transported_violation_count": seed_count, "engine_status": result["status"],
                  "global_modular_dual": result["global_modular_dual"], "selected_columns": result["selected_columns"],
                  "dual_support": result["dual_support"], "rounds": len(result["rounds"]), "elapsed_seconds": result["elapsed_seconds"],
                  "peak_rss_kib": watch["peak_rss_kib"], "result_sha256": sha(output / "result.json"),
                  "selected_sha256": sha(output / "selected.tsv"),
                  "dual_sha256": sha(output / "dual.tsv") if (output / "dual.tsv").exists() else None,
                  "watchdog_sha256": sha(output / "watchdog.json")}
        atomic(output / "acceptance.json", record)
        record["acceptance_sha256"] = sha(output / "acceptance.json")
        records.append(record)
    all_closed = all(record["engine_status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC" for record in records)
    summary = {"schema": "KRENN_X5_FOUR_D10_SEEDED_SECOND_PRIME_RESULT_V1",
               "status": "PASS_FOUR_GLOBAL_MODULAR_DUALS" if all_closed else "FAIL_CLOSED_NO_EXACT_LIFT",
               "prime": PRIME, "records": records, "all_four_global_duals": all_closed,
               "second_prime_condition_from_first_prime": True, "degree_eleven_launched": False}
    atomic(HERE / "results_second_prime.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if not all_closed:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
