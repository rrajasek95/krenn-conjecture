#!/usr/bin/env python3
"""Independent post-run pin audit for the exact round1343 gate inputs."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
V4 = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25"
SOURCE = V4 / "sealed_v4_1/main.rs"
BINARY = V4 / "sealed_v4_1/sparse_d12_dual"
WATCHDOG = REPO / "computations/unaudited-codex-n8-affine251-d12-hierarchical-generic-2026-08-24/run_with_macos_rss_watchdog_v2.py"
PROVIDER = REPO / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p1073741827.ms"
EXPECTED = {
    "source_sha256": "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59",
    "binary_sha256": "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048",
    "watchdog_sha256": "53d95032600078655d5c656570eec04635516e5ff6b08acdb54744114d750e97",
    "provider_sha256": "daa427528bbbeece064b09396023b66f32b804ba6d304178d19ced13e9b38a4e",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


actual = {
    "source_sha256": sha256(SOURCE),
    "binary_sha256": sha256(BINARY),
    "watchdog_sha256": sha256(WATCHDOG),
    "provider_sha256": sha256(PROVIDER),
}
assert actual == EXPECTED
pins = json.loads((HERE / "LAUNCH_PINS.json").read_text())
audit = json.loads((HERE / "results_round1343_cap_audit.json").read_text())
assert pins["status"] == "PASS_FROZEN_SEALED_ROUND1342_INPUT"
assert audit["status"] == "PASS_EXACT_CAP1500_TO_CAP1750_EQUIVALENCE"
for label in ("cap1500_control", "cap1750_candidate"):
    result_path = HERE / label / "result.json"
    watch = json.loads((HERE / label / "watchdog.json").read_text())
    assert watch["binary_sha256"] == EXPECTED["binary_sha256"]
    assert watch["result_sha256"] == sha256(result_path)
    command = watch["command"]
    assert command[command.index("--input") + 1] == str(PROVIDER)
value = {
    "schema": "KRENN_AFFINE251_D12_ROUND1343_FINAL_PIN_AUDIT_V1",
    "status": "PASS_EXACT_SOURCE_BINARY_WATCHDOG_PROVIDER_AND_RESULT_PINS",
    **actual,
    "poincare_manifest_sha256": pins["poincare_manifest_sha256"],
    "poincare_result_sha256": pins["poincare_result_sha256"],
    "round1343_checkpoint_sha256": audit["checkpoint_sha256"],
    "round1343_vectors_sha256": audit["vectors_sha256"],
}
(HERE / "results_final_pin_audit.json").write_text(
    json.dumps(value, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(value, sort_keys=True))
