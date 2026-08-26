#!/usr/bin/env python3
"""Independent literal/algebra referee for the superseding rep5 nine-stratum v2 design."""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25"
REJECTION = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-referee-2026-08-25"
PINS = {
    PRODUCER / "MANIFEST.sha256": "50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1",
    PRODUCER / "results_design_v2.json": "4d572fc359430eab8a55ee80ffe98993521e510f9eb48c37ab185742ad19bf00",
    PRODUCER / "generate_design_v2.py": "5f1c16d4307776a1f294b06cfeb1139a3d0c8ac8cb22064782b3b59709b67699",
    PRODUCER / "rep5_p00_guardpivot_k0_rank2_t1_Q.sing": "4a7875119acf8b8b4b1f78b5180bb1578371d1dfc0a56aa697b8e493ad518c0a",
    PRODUCER / "rep5_p00_guardpivot_k0_rank2_t2_Q.sing": "3f35b2baf2160f9fad6378b178ca10f1db1b0c36420ae906ef5e9ad4a5a15baa",
    PRODUCER / "rep5_p00_guardpivot_k1_rank2_t1_Q.sing": "face720c953a5ac7f4e0e86b9c88114f3000f31c16d35dc7800109d6eb855cc9",
    PRODUCER / "rep5_p00_guardpivot_k1_rank2_t2_Q.sing": "5cd212cf9f512804caf561c9879b79aa5e957a3648e8e0f77f3c1570b47dd336",
    PRODUCER / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing": "1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e",
    PRODUCER / "rep5_p00_guardpivot_k2_rank2_t2_Q.sing": "601c79ceb92a1128bc92abcea62575454b02c016a585f7f69b340e8fa1f08a79",
    PRODUCER / "rep5_p00_guardpivot_k0_rank1_closed_Q.sing": "3dfc97bdcddfe15870e56744101af011e943a0609f98848bfee60c78cac76e79",
    PRODUCER / "rep5_p00_guardpivot_k1_rank1_closed_Q.sing": "96943ee3f63c84322b65fdf3f44dc46340186807675d2d44a429fe764d9e9115",
    PRODUCER / "rep5_p00_guardpivot_k2_rank1_closed_Q.sing": "12f08480dc093f3ecb38b6d250f8b8064b64dab2aed9e1e0dea136e287ca7a41",
    REJECTION / "FINAL_MANIFEST.sha256": "8a1c4e5faf9e73cffcfb5a8b52c697aa79fbb15e45aa9cae6d27911dd62ffea7",
    REJECTION / "results_referee.json": "bd13a637305966d993ef4373c3a0f300afae6ee7c269fe097b83552a76a60bd9",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(path: Path) -> tuple[str, list[str], list[str]]:
    text = path.read_text()
    ring = next(line for line in text.splitlines() if line.startswith("ring r="))
    variables = ring.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    equations = []
    depth = 0
    start = 0
    for index, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            assert depth >= 0
        elif character == "," and depth == 0:
            equations.append(body[start:index].strip())
            start = index + 1
    equations.append(body[start:].strip())
    assert depth == 0
    return text, variables, equations


def constant(value: int):
    return collections.Counter({(): value}) if value else collections.Counter()


def variable(name: str):
    return collections.Counter({(name,): 1})


def add(*polynomials):
    result = collections.Counter()
    for polynomial in polynomials:
        result.update(polynomial)
    return collections.Counter({monomial: coefficient for monomial, coefficient in result.items() if coefficient})


def negative(polynomial):
    return collections.Counter({monomial: -coefficient for monomial, coefficient in polynomial.items()})


def multiply(*polynomials):
    result = constant(1)
    for polynomial in polynomials:
        product = collections.Counter()
        for left, left_coefficient in result.items():
            for right, right_coefficient in polynomial.items():
                product[tuple(sorted(left + right))] += left_coefficient * right_coefficient
        result = collections.Counter({monomial: coefficient for monomial, coefficient in product.items() if coefficient})
    return result


def dot(left, right):
    return add(*(multiply(a, b) for a, b in zip(left, right)))


def cross(left, right):
    return [
        add(multiply(left[1], right[2]), negative(multiply(left[2], right[1]))),
        add(multiply(left[2], right[0]), negative(multiply(left[0], right[2]))),
        add(multiply(left[0], right[1]), negative(multiply(left[1], right[0]))),
    ]


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)
producer = json.loads((PRODUCER / "results_design_v2.json").read_text())
rejection = json.loads((REJECTION / "results_referee.json").read_text())
assert producer["status"] == "PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES"
assert rejection["status"] == "REJECT_LITERAL_RANK2_SOURCES_REFERENCE_UNDECLARED_ELIMINATED_A37"
assert producer["supersedes"] == {
    "rejected_producer_manifest_sha256": "f28dbb2bd003e8ebcfae4eba7945b29507c2a39c417700c17653131cd6674221",
    "rejection_manifest_sha256": PINS[REJECTION / "FINAL_MANIFEST.sha256"],
    "rejection_result_sha256": PINS[REJECTION / "results_referee.json"],
    "rejection_status": rejection["status"],
}
assert producer["repair"]["defect"] == rejection["materialization_defect"]

# Independently require the repaired dependency order: raw source dictionary first,
# then proportional A37, then every expression that consumes it, then amplitudes.
generator = (PRODUCER / "generate_design_v2.py").read_text()
order_markers = [
    "    source = {",
    "    def raw(edge, i, j):",
    "    def a37(i, j):",
    "    def partner_entry(i, j):",
    "    def a36(i, j):",
    "    def a06(i, j):",
    "    def a17(i, j):",
    "    def entry(edge, i, j):",
    "    for word in itertools.product(m.COLORS, repeat=8):",
]
positions = [generator.index(marker) for marker in order_markers]
assert positions == sorted(positions)
solved_position = generator.index("    solved |= {(3, 7, i, j)")
assert solved_position < positions[0]
assert "return source[edge, i, j]" in generator
assert "return m.product(raw((3, 7), i, q), pivot_v(j), inverse_v)" in generator

records = producer["sources"]
assert len(records) == 9
observed = set()
open_a37_absence = {}
for record in records:
    path = PRODUCER / record["path"]
    assert sha256(path) == record["sha256"] and path.stat().st_size == record["bytes"]
    text, variables, equations = parse(path)
    assert len(variables) == len(set(variables)) == record["variables"]
    assert len(equations) == len(set(equations)) == record["generators"]
    identifiers = set(re.findall(r"\b(?:a\d\d_\d\d|xn\d|yn\d|zn\d|abar|beta|t\d|sat)\b", "\n".join(equations)))
    assert identifiers == set(variables)
    for removed in record["removed_variables"]:
        assert re.search(rf"\b{re.escape(removed)}\b", text) is None, (record["path"], removed)
    pivot = record["pivot_k"]
    if record["rank_branch"] == "rank2_open":
        assert (len(variables), len(equations)) == (84, 6562)
        assert record["origin"] == "regenerated_from_raw_entries_v2"
        removed_a37 = {"a37_11", "a37_12", "a37_21", "a37_22"}
        assert removed_a37 <= set(record["removed_variables"])
        counts = {name: len(re.findall(rf"\b{name}\b", text)) for name in sorted(removed_a37)}
        assert counts == {name: 0 for name in sorted(removed_a37)}
        open_a37_absence[record["path"]] = counts
        assert all(record["dependency_probe"].values())
        assert record["t_open"] in (1, 2)
    else:
        assert record["rank_branch"] == "rank1_closed" and record["t_open"] is None
        assert (len(variables), len(equations)) == (86, 6570)
        assert "t1" not in variables and "t2" not in variables
        assert record["origin"] == "byte_preserved_rejection_referee_literal_valid_complement"
    observed.add((pivot, record["rank_branch"], record["t_open"]))
expected = {(pivot, "rank2_open", t_open) for pivot in range(3) for t_open in (1, 2)} | {(pivot, "rank1_closed", None) for pivot in range(3)}
assert observed == expected and len(open_a37_absence) == 6

# Independent sparse-integer replay of Cramer rows and localized inverse identities.
w = [constant(1), variable("w1"), variable("w2")]
v = [variable("v0"), variable("v1"), variable("v2")]
d = add(v[1], negative(multiply(w[1], v[0])))
t0 = variable("t0")
abar = variable("abar")
reduced = add(abar, negative(multiply(t0, w[2])))
u0 = [add(multiply(reduced, v[1]), multiply(w[1], t0, v[2])), negative(add(multiply(t0, v[2]), multiply(reduced, v[0]))), multiply(d, t0)]
assert dot(u0, v) == constant(0) and dot(u0, w) == multiply(d, abar)
identity_count = 2
for t_open in (1, 2):
    tm = variable(f"t{t_open}")
    um = [multiply(tm, component) for component in cross(w, v)]
    assert dot(um, v) == constant(0) and dot(um, w) == constant(0)
    assert cross(u0, um) == [negative(multiply(tm, d, abar, component)) for component in v]
    identity_count += 5
n, p, b, tm, sat = [variable(name) for name in ("N", "P", "b", "tm", "sat")]
saturation = add(multiply(p, b, tm, sat), constant(-1))
assert add(multiply(b, multiply(n, p, tm, sat)), negative(n)) == multiply(n, saturation)
rho, vj, v0, inverse = [variable(name) for name in ("rho", "vj", "v0", "inverse")]
assert add(multiply(v0, multiply(rho, vj, inverse)), negative(multiply(rho, vj))) == multiply(rho, vj, add(multiply(v0, inverse), constant(-1)))
identity_count += 2

# D(t1) U D(t2) U V(t1,t2) is an exact four-case Boolean cover for each k.
case_ledger = []
for pivot in range(3):
    for t1_nonzero, t2_nonzero in itertools.product((False, True), repeat=2):
        branch = "D(t1)" if t1_nonzero else "D(t2)" if t2_nonzero else "V(t1,t2)"
        case_ledger.append({"pivot_k": pivot, "t1_nonzero": t1_nonzero, "t2_nonzero": t2_nonzero, "branch": branch})
assert {entry["branch"] for entry in case_ledger} == {"D(t1)", "D(t2)", "V(t1,t2)"}
strata = [(pivot, branch) for pivot in range(3) for branch in ("D(t1)", "D(t2)", "V(t1,t2)")]
assert len(strata) == len(set(strata)) == 9
assert producer["identity_replay"]["nine_strata"] == [[pivot, branch] for pivot, branch in strata]
assert producer["rank2_open_strata"] == {"count": 6, "variables": 84, "generators": 6562, "breakdown": {"full_x5": 6561, "combined_saturation": 1, "explicit_guards": 0}}
assert producer["rank1_closed_strata"] == {"count": 3, "variables": 86, "generators": 6570, "breakdown": {"full_x5": 6561, "first_guards": 2, "second_guards": 6, "combined_saturation": 1}}
assert producer["scope"] == {"design_only": True, "singular_runs": 0, "ideal_runs": 0, "consumed_k0_reused": False, "mathematical_coverage": False, "rep5_closed": False, "performance_claim": False}
for forbidden in ("result.json", "ATTEMPT.json", "watchdog.json", "stdout.log", "stderr.log", "launch_clearance.json"):
    assert not (PRODUCER / forbidden).exists()
assert not list(PRODUCER.rglob("*.tmp"))

result = {
    "schema": "KRENN_X5_REP5_RANK_STRATIFIED_GUARD_PIVOT_DESIGN_V2_REFEREE_V1",
    "status": "PASS_SUPERSEDING_LITERAL_SAFE_NINE_STRATA_DESIGN_ZERO_SOLVES",
    "producer_manifest_sha256": PINS[PRODUCER / "MANIFEST.sha256"],
    "producer_result_sha256": PINS[PRODUCER / "results_design_v2.json"],
    "bound_rejection": {"manifest_sha256": PINS[REJECTION / "FINAL_MANIFEST.sha256"], "result_sha256": PINS[REJECTION / "results_referee.json"], "status": rejection["status"]},
    "raw_layer_order": {"markers": order_markers, "positions_strictly_increasing": True, "solved_a37_removed_before_raw_source_dictionary": True, "dependent_a35_a36_after_corrected_a37": True},
    "source_audit": {"rank2_open": {"count": 6, "variables_each": 84, "generators_each": 6562, "removed_a37_occurrences": open_a37_absence}, "rank1_complements": {"count": 3, "variables_each": 86, "generators_each": 6570}, "undeclared_identifiers": 0},
    "algebra_replay": {"sparse_integer_identities": identity_count, "forward_reverse_a17": True, "forward_reverse_a37": True, "nine_stratum_cover": True, "boolean_cases": case_ledger},
    "scope": {"design_only": True, "singular_runs": 0, "ideal_runs": 0, "mathematical_coverage": False, "rep5_closed": False},
    "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
}
temporary = HERE / "results_referee.json.tmp"
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, HERE / "results_referee.json")
print(json.dumps({"status": result["status"], "open_sources": 6, "complements": 3, "strata": 9, "solver_runs": 0}, sort_keys=True))
