#!/usr/bin/env python3
"""Independent source-level referee of the rep5 guard-pivot quotient design."""
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DES = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
TERM = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-v2-terminal-referee-2026-08-25"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

pins = {
    DES / "MANIFEST.sha256": "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9",
    DES / "results_design.json": "e13e76529f19397cb88f100898ea5653908129e431cfe11c45aa94c59102953d",
    DES / "rep5_p00_guardpivot_k0_Q.sing": "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1",
    DES / "rep5_p00_guardpivot_k1_Q.sing": "cdf782ee92b0a019c2a77d6ccc980828c7d0279ebcc3592cced648306fd95e6c",
    DES / "rep5_p00_guardpivot_k2_Q.sing": "ef6fec2e4ba4baf44c07e9d90e0a1b7fb2624d99c838d901d388e3041bf6aa6d",
    BASE / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    BASE / "results_rep5_contraction_design.json": "b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b",
    TERM / "FINAL_MANIFEST.sha256": "69b6e61f2a493a5c0fb1edd589105d2d3b38d0bec3450314fa56a1411a80241a",
    TERM / "results_referee.json": "0cf977520416ab3de81748195b824913a9ad159d7660d059f5f3e03767199875",
}
for path, expected in pins.items(): assert sha(path) == expected, (path, sha(path), expected)

def replay(path, base):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        expected, raw = line.split(None, 1)
        target = Path(raw.strip())
        if not target.is_absolute():
            target = ROOT / target if raw.strip().startswith("computations/") else base / target
        assert target.is_file() and sha(target) == expected, target
        count += 1
    return count

design_manifest_entries = replay(DES / "MANIFEST.sha256", DES)
base_manifest_entries = replay(BASE / "MANIFEST.sha256", BASE)
terminal_manifest_entries = replay(TERM / "FINAL_MANIFEST.sha256", TERM)
result = json.loads((DES / "results_design.json").read_text())
base = json.loads((BASE / "results_rep5_contraction_design.json").read_text())
terminal = json.loads((TERM / "results_referee.json").read_text())
assert result["status"] == "PASS_STRICT_SMALLER_EXACT_THREE_CHART_DESIGN_ZERO_SOLVES"
assert base["counts"]["new_variables"] == 91 and base["counts"]["new_generators"] == 6577
assert terminal["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
assert terminal["termination"] == "NATIVE_WALL_CAP_180" and terminal["mathematical_coverage"] is False

def parse_source(path):
    text = path.read_text()
    ring_line = next(line for line in text.splitlines() if line.startswith("ring r="))
    variables = ring_line.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    depth = 0; start = 0; equations = []
    for index, char in enumerate(body):
        if char == "(": depth += 1
        elif char == ")": depth -= 1
        elif char == "," and depth == 0:
            equations.append(body[start:index].strip()); start = index + 1
    equations.append(body[start:].strip())
    assert depth == 0
    return text, variables, equations

P = "(abar*beta*a37_00*(a37_01-(xn1*a37_00)))"
source_census = []
for k, expected_sha in enumerate((pins[DES / "rep5_p00_guardpivot_k0_Q.sing"], pins[DES / "rep5_p00_guardpivot_k1_Q.sing"], pins[DES / "rep5_p00_guardpivot_k2_Q.sing"])):
    path = DES / f"rep5_p00_guardpivot_k{k}_Q.sing"
    text, variables, equations = parse_source(path)
    eliminated = [f"a17_{i}{k}" for i in range(3)]
    retained = [f"a17_{i}{j}" for i in range(3) for j in range(3) if j != k]
    assert text.count("ring r=0,") == 1 and len(variables) == len(set(variables)) == 88
    assert len(equations) == len(set(equations)) == 6574
    assert all(name not in variables and name not in text for name in eliminated)
    assert all(name in variables for name in retained)
    b_k = "(" + "+".join(f"a26_{k}{l}*a37_0{l}" for l in range(3)) + ")"
    assert equations[-1] == f"{P}*{b_k}*sat-1"
    assert all(eq not in ("0", "1", "-1") for eq in equations)
    source_census.append({"pivot_k": k, "sha256": expected_sha, "variables": 88, "generators": 6574, "eliminated": eliminated, "combined_saturation": equations[-1]})

# Independent algebra: after substituting A17[i,k]=N_i*P*sat, the removed
# guard is N_i-A17[i,k]*b_k = N_i*(1-P*b_k*sat), hence vanishes on the chart.
for N, P_value, b_value, sat in ((2,3,5,7),(-11,13,17,-19),(0,23,29,31)):
    assert N - (N * P_value * sat) * b_value == N * (1 - P_value * b_value * sat)
assert result["proof"]["removed_guard_identity"] == "A37[p,i]-sum_h A17[i,h]*b_h = N_i*(1-P*b_k*sat)"
assert result["proof"]["definitions"]["b_h"] == "sum_l A26[h,l]*A37[p,l]"
assert "at least one of b_0,b_1,b_2 is nonzero" in result["proof"]["cover"]
assert result["proof"]["forward"].startswith("on b_k!=0 set sat_new=sat_old/b_k")
assert result["proof"]["reverse"].startswith("set sat_old=b_k*sat_new")
assert result["proof"]["chart_union"] == "three k charts cover the full original p00 chart; no symmetry identification is assumed"
assert result["reduction"]["full_x5_equations"] == 6561
assert result["reduction"]["guards_removed"] == 3 and result["reduction"]["combined_saturation"] == 1
assert result["scope"] == {"design_inputs_materialized": 3, "solver_runs": 0, "parent_relaunched": False, "mathematical_coverage": False, "rep5_closed": False}
assert result["alternative_order"]["tested_by_solver"] is False
for forbidden in ("result.json", "watchdog.json", "stdout.log", "stderr.log", "ATTEMPT.json", "launch_clearance.json"):
    assert not (DES / forbidden).exists(), forbidden
assert not any(DES.glob("*.tmp"))

print(json.dumps({
    "status": "PASS_EXACT_GUARD_PIVOT_THREE_CHART_DESIGN_ZERO_SOLVES",
    "parent": {"variables": 91, "generators": 6577},
    "charts": source_census,
    "ledger_correction": "producer variables_removed display leaked final k=2; literal sources correctly eliminate A17[:,k] chartwise",
    "manifest_entries": {"design": design_manifest_entries, "base": base_manifest_entries, "terminal": terminal_manifest_entries},
    "scope": {"solver_runs": 0, "mathematical_coverage": False, "rep5_closed": False},
}, sort_keys=True))
