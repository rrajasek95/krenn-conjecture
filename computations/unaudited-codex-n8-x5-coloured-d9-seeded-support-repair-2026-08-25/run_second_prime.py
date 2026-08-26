#!/usr/bin/env python3
"""Run the conditionally authorized p=1000000007 coloured D9 repairs."""
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
BINARY = HERE / "x5_coloured_d9_seeded_repair"
WATCHDOG = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d9-resumable-single-branch-design-2026-08-25/watchdog8_180_resume.py"
PINS = {
    "source": "f379f09f502ce24e4f177687ee95e7f0a68223c257c1aa285c5bd0298ace2a31",
    "binary": "a28be09b1d6bdd9a0e7a43c9be0487cbd6f44029be58b99e03f109b3689a0798",
    "watchdog": "370c4c9e07ebbba03f459542e23cd68882aa10c455e309aee2a6dce1e2eb46d1",
}
BRANCHES = {
    "triangle_endpoint_colour": ("1a58301d9a316c37fda825bf1112d38b5bae19479308f7de23fe5ef7b0d8ee16", "366271ef02e49831780ea8df18ddac590648f8f52ecb8388305beb7e5cf89a0d", "62deb9a0d50e30c2556d2abbfd522e6b3d19c8c3600e7df7083870f172f4ccb9"),
    "third_colour": ("e761815e90f949bce7ab32598749610e36db54293b87693a7af522241acde1ec", "a16549a93631c3e4c6f2c14eb190b4747bfd79bb93cbd7731b3d1bf1d045ce21", "3d0162d77b65c69c1062d9ff0c2aff3b456e1c19253f2a876a821108fcc3392c"),
    "cap_endpoint_colour": ("08aaff0a26cb8d4b382e889ea956e48654baf856f80810162fc19d12c2eba744", "9dec176f77a5435df5c4e77617d366ed7e42db17ac8f193991f38f5f79876bd0", "f4f7bf6bf6e94952dc96e276135946bc5a58e045dae5ac0990ff9bfdcf5ba275"),
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
    assert first["status"] == "PASS_THREE_GLOBAL_MODULAR_DUALS" and first["all_three_global_duals"] is True
    for path, expected in ((SOURCE, PINS["source"]), (BINARY, PINS["binary"]), (WATCHDOG, PINS["watchdog"])):
        assert sha(path) == expected
    records = []
    for branch, (provider_sha, selected_sha, seed_sha) in BRANCHES.items():
        provider = HERE / f"provider_{branch}_p{PRIME}.ms"
        seed_dir = HERE / f"seed_{branch}_p{PRIME}"
        selected = seed_dir / "selected.tsv"
        seed_dual = seed_dir / "transported_d8_dual.tsv"
        for path, expected in ((provider, provider_sha), (selected, selected_sha), (seed_dual, seed_sha)):
            assert sha(path) == expected
        output = HERE / f"p{PRIME}_{branch}"
        assert not output.exists()
        output.mkdir()
        command = [
            str(BINARY), "--branch", branch, "--input", str(provider),
            "--resume-selected", str(selected), "--resume-dual", str(seed_dual),
            "--resume-round-offset", "0", "--output", str(output / "result.json"),
            "--selected", str(output / "selected.tsv"), "--dual", str(output / "dual.tsv"),
            "--prime", str(PRIME), "--column-cap", "100000", "--wall-seconds", "175",
        ]
        wrapper = [
            sys.executable, str(WATCHDOG), "--rss-gib", "8", "--wall-seconds", "180",
            "--poll-seconds", "0.25", "--source", str(SOURCE),
            "--expected-source-sha256", PINS["source"],
            "--expected-binary-sha256", PINS["binary"],
            "--telemetry", str(output / "watchdog.json"),
            "--stdout", str(output / "stdout.log"), "--stderr", str(output / "stderr.log"),
            "--", *command,
        ]
        completed = subprocess.run(wrapper, cwd=REPO, check=False)
        result = json.loads((output / "result.json").read_text())
        watch = json.loads((output / "watchdog.json").read_text())
        assert completed.returncode == 0 and watch["status"] == "PASS_TERMINAL"
        assert result["schema"] == "KRENN_X5_FOUR_BLOCKER_D9_RESUMABLE_RESULT_V1"
        assert result["branch"] == branch and result["prime"] == PRIME and result["degree"] == 9
        assert result["resumed_columns"] == 18 and result["transported_seed_loaded"] is True
        assert result["selected_columns"] <= 100000 and result["elapsed_seconds"] < 180
        assert result["status"] in {"COMPLETE_MODULAR_DUAL_DIAGNOSTIC", "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY"}
        record = {
            "branch": branch,
            "engine_status": result["status"],
            "global_modular_dual": result["global_modular_dual"],
            "selected_columns": result["selected_columns"],
            "dual_support": result["dual_support"],
            "rounds": len(result["rounds"]),
            "elapsed_seconds": result["elapsed_seconds"],
            "peak_rss_kib": watch["peak_rss_kib"],
            "result_sha256": sha(output / "result.json"),
            "selected_sha256": sha(output / "selected.tsv"),
            "dual_sha256": sha(output / "dual.tsv") if (output / "dual.tsv").exists() else None,
            "watchdog_sha256": sha(output / "watchdog.json"),
        }
        atomic(output / "acceptance.json", record)
        record["acceptance_sha256"] = sha(output / "acceptance.json")
        records.append(record)
    all_closed = all(record["engine_status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC" for record in records)
    summary = {
        "schema": "KRENN_X5_COLOURED_D9_SEEDED_SECOND_PRIME_RESULT_V1",
        "status": "PASS_THREE_GLOBAL_MODULAR_DUALS" if all_closed else "FAIL_CLOSED_NO_SECOND_PRIME",
        "prime": PRIME,
        "records": records,
        "all_three_global_duals": all_closed,
        "second_prime_condition_from_first_prime": True,
        "degree_ten_launched": False,
    }
    atomic(HERE / "results_second_prime.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if not all_closed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
