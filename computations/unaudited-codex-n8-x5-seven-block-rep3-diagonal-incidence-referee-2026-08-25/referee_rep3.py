#!/usr/bin/env python3
"""Independent small-file referee of the corrected rep3 incidence gate."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep3-diagonal-incidence-gate-2026-08-25"
EXPECTED_MANIFEST = "43c6847a284f4745ffbb37f7d92ef74bfc80a3118ce7e5d0f8ca0b31b4df3ffd"
CHARTS = ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


assert sha(SRC / "MANIFEST.sha256") == EXPECTED_MANIFEST
metadata = load(SRC / "gate_metadata.json")
producer = load(SRC / "results_rep3_incidence_audit.json")
assert metadata["counts"] == {
    "variables": 100, "equations": 6586, "full_x5": 6561,
    "guard_after_elimination": 18, "incidence": 6, "saturation": 1,
}
assert metadata["source_orientation"] == {
    "elimination": "A36=-A37*A26^T",
    "guard": ["A06*A37^T=0", "(I-A17*A26)*A37^T=0"],
    "P_incidence": "A06*x=e0",
    "Q_incidence": "A35*y+A37*z=e0",
}

# Independent orbit census: normalize diagonal coordinate i to 0, then quotient
# the ordered nonzero A37 entry (p,q) by the residual swap of colors 1 and 2.
def normalized(i, p, q):
    images = []
    for perm in itertools.permutations(range(3)):
        if perm[i] == 0:
            images.append((perm[p], perm[q]))
    return min(images)


cases = {(i, p, q): normalized(i, p, q) for i, p, q in itertools.product(range(3), repeat=3)}
assert len(cases) == 27 and set(cases.values()) == set(CHARTS)
assert tuple(tuple(x) for x in metadata["s3_normalization"]["outside_entry_orbits"]) == CHARTS

runs = []
for p, q in CHARTS:
    chart = f"p{p}{q}"
    mod_path = SRC / ("results_modular_p00.json" if chart == "p00" else f"results_p32003_{chart}.json")
    q_path = SRC / ("results_q_p00.json" if chart == "p00" else f"results_Q_{chart}.json")
    mod = load(mod_path)
    exact = load(q_path)
    assert mod["status"] == "UNIT_IDEAL_MODULAR" and mod["returncode"] == 0
    assert exact["status"] == "UNIT_IDEAL_EXACT_Q" and exact["returncode"] == 0
    assert "INPUT_GENERATORS=6586" in mod["stdout"] and "UNIT_REMAINDER=0" in mod["stdout"]
    assert "INPUT_GENERATORS=6586" in exact["stdout"] and "UNIT_REMAINDER=0" in exact["stdout"]
    assert mod["input_sha256"] == metadata["inputs"][chart]["p32003"]["sha256"]
    assert exact["input_sha256"] == metadata["inputs"][chart]["Q"]["sha256"]
    assert mod["observed_peak_rss_bytes"] < mod["rss_cap_bytes"]
    assert exact["observed_peak_rss_bytes"] < exact["rss_cap_bytes"]
    runs.append({
        "chart": chart,
        "modular_result_sha256": sha(mod_path),
        "exact_Q_result_sha256": sha(q_path),
    })

assert producer["status"] == "PASS_REP3_ALL_RANKS_EXACT_Q"
assert producer["census"]["exact_Q_units"] == 5
assert producer["s3_normalization"]["all_27_coordinate_entry_cases_covered"] is True
assert producer["scope"] == {
    "representative_3_only": True,
    "transport_to_other_representatives": False,
    "non_full_family": False,
    "broad_cegar": False,
}

result = {
    "schema": "KRENN_X5_REP3_DIAGONAL_INCIDENCE_INDEPENDENT_REFEREE_V1",
    "status": "ACCEPT_REP3_CORRECTED_DIAGONAL_INCIDENCE_CLOSURE",
    "pins": {
        "producer_manifest_sha256": EXPECTED_MANIFEST,
        "producer_audit_sha256": sha(SRC / "results_rep3_incidence_audit.json"),
        "metadata_sha256": sha(SRC / "gate_metadata.json"),
        "generator_sha256": sha(SRC / "generate_gate.py"),
    },
    "orientation_referee": {
        "derivation": "A26*A37^T+A36^T=0 gives A36=-A37*A26^T; substituting into A37^T+A17*A36^T=0 gives (I-A17*A26)A37^T=0.",
        "P": "Col(A06)",
        "Q": "ColSpan(A35,A37)",
        "diagonal_failure": "e_i in P intersection Q",
        "incidence_equations": ["A06*x=e_i", "A35*y+A37*z=e_i"],
    },
    "chart_referee": {
        "coordinate_entry_cases": 27,
        "S3_then_S2_orbits": [list(x) for x in CHARTS],
        "modular_units": 5,
        "exact_Q_units": 5,
        "runs": runs,
    },
    "nonzero_branch": "Every possible failed diagonal incidence plus a nonzero A37 entry is excluded by an exact-Q unit ideal. The guard makes Col(A06) proper, so the fixed-I cap functional is also live; all four activity functionals are live.",
    "zero_branch": "A37=0 forces A36=0, hence L67=0; on the claimed full-family stratum nonzero A67 makes the cap functional live and Mat3 supplies all diagonal functionals.",
    "scope": {
        "representative_3_only": True,
        "full_family_only": True,
        "no_guard_mate_transport_added_by_referee": True,
        "no_other_representative_transport": True,
        "D12_read": False,
    },
}

(HERE / "results_rep3_referee.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "Q_units": 5, "cases": 27}))
