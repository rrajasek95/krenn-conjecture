#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
BINARY = ROOT / "audit_source/sparse_d12_dual"
with tempfile.TemporaryDirectory(prefix="round1061-hostile-") as temporary:
    temporary = Path(temporary)
    command = [
        str(BINARY), "--input", str(temporary / "absent.ms"),
        "--output", str(temporary / "result.json"),
        "--checkpoint", str(temporary / "checkpoint.bin"),
        "--vector-cache", str(temporary / "vectors.bin"),
        "--dual", str(temporary / "dual.tsv"),
        "--prime", "1073741827", "--wall-seconds", "1", "--rss-gib", "1",
        "--workers", "16", "--pivot", "rare", "--strategy", "repair",
        "--elimination", "hierarchical", "--incremental", "no",
        "--portfolio-period", "1", "--portfolio-parallel", "yes",
        "--support-cap", "100000", "--column-cap", "1000000", "--round-cap", "1061",
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    assert process.returncode != 0
    assert "hierarchical elimination requires explicit" in process.stderr
    assert not any(temporary.glob("result.json*"))

value = {
    "schema": "KRENN_AFF251_D12_ROUND1061_AUDIT_SIBLING_HOSTILE_V1",
    "status": "PASS",
    "hierarchical_non_cold_rejected": True,
    "result_absent": True,
    "production_source_mutated": False,
}
(ROOT / "hostile_results.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
print(json.dumps(value, sort_keys=True))
