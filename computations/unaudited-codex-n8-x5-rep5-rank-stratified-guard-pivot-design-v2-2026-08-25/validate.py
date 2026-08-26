#!/usr/bin/env python3
"""Independent literal and algebra validation for the superseding v2 design."""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-2026-08-25"
REJECTION = HERE.parent / "unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-referee-2026-08-25"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def parse(path: Path):
    text = path.read_text()
    ring = next(line for line in text.splitlines() if line.startswith("ring r="))
    variables = ring.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    equations = []
    depth = start = 0
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


def C(value):
    return collections.Counter({(): value}) if value else collections.Counter()


def V(name):
    return collections.Counter({(name,): 1})


def add(*polys):
    out = collections.Counter()
    for poly in polys:
        out.update(poly)
    return collections.Counter({m: c for m, c in out.items() if c})


def neg(poly):
    return collections.Counter({m: -c for m, c in poly.items()})


def mul(*polys):
    out = C(1)
    for poly in polys:
        nxt = collections.Counter()
        for a, x in out.items():
            for b, y in poly.items():
                nxt[tuple(sorted(a + b))] += x * y
        out = collections.Counter({m: c for m, c in nxt.items() if c})
    return out


def dot(a, b):
    return add(*(mul(x, y) for x, y in zip(a, b)))


def cross(a, b):
    return [
        add(mul(a[1], b[2]), neg(mul(a[2], b[1]))),
        add(mul(a[2], b[0]), neg(mul(a[0], b[2]))),
        add(mul(a[0], b[1]), neg(mul(a[1], b[0]))),
    ]


result = json.loads((HERE / "results_design_v2.json").read_text())
assert result["schema"] == "KRENN_X5_REP5_RANK_STRATIFIED_GUARD_PIVOT_DESIGN_V2"
assert result["status"] == "PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES"
assert result["supersedes"]["rejection_manifest_sha256"] == "8a1c4e5faf9e73cffcfb5a8b52c697aa79fbb15e45aa9cae6d27911dd62ffea7"
assert sha(REJECTION / "FINAL_MANIFEST.sha256") == result["supersedes"]["rejection_manifest_sha256"]
assert result["repair"]["undeclared_removed_symbol_occurrences"] == 0

generator = (HERE / "generate_design_v2.py").read_text()
order = [
    generator.index("    def a37(i, j):"),
    generator.index("    def partner_entry(i, j):"),
    generator.index("    def a36(i, j):"),
    generator.index("    def a06(i, j):"),
    generator.index("    def a17(i, j):"),
    generator.index("    for word in itertools.product(m.COLORS, repeat=8):"),
]
assert order == sorted(order)

assert len(result["sources"]) == 9
seen = set()
for record in result["sources"]:
    path = HERE / record["path"]
    assert sha(path) == record["sha256"] and path.stat().st_size == record["bytes"]
    text, variables, equations = parse(path)
    assert text.startswith("// DESIGN INPUT ONLY: zero Singular or ideal runs authorized.\n") or record["rank_branch"] == "rank1_closed"
    assert len(variables) == len(set(variables)) == record["variables"]
    assert len(equations) == len(set(equations)) == record["generators"]
    tokens = set(re.findall(r"\b(?:a\d\d_\d\d|xn\d|yn\d|zn\d|abar|beta|t\d|sat)\b", "\n".join(equations)))
    assert tokens <= set(variables)
    for removed in record["removed_variables"]:
        assert not re.search(rf"\b{re.escape(removed)}\b", text), (path, removed)
    k = record["pivot_k"]
    if record["rank_branch"] == "rank2_open":
        m_index = record["t_open"]
        assert (len(variables), len(equations)) == (84, 6562)
        assert record["origin"] == "regenerated_from_raw_entries_v2"
        assert set(record["removed_variables"]) == {f"a17_{i}{k}" for i in range(3)} | {"a37_11", "a37_12", "a37_21", "a37_22"}
        expected_last = f"(abar*beta*a37_00*(a37_01-(xn1*a37_00)))*(a26_{k}0*a37_00+a26_{k}1*a37_01+a26_{k}2*a37_02)*t{m_index}*sat-1"
        assert equations[-1] == expected_last
        assert all(record["dependency_probe"].values())
    else:
        assert record["rank_branch"] == "rank1_closed" and record["t_open"] is None
        assert (len(variables), len(equations)) == (86, 6570)
        assert sha(OLD / record["path"]) == record["sha256"]
        assert record["origin"] == "byte_preserved_rejection_referee_literal_valid_complement"
    seen.add((k, record["rank_branch"], record["t_open"]))
assert seen == {(k, "rank2_open", m) for k in range(3) for m in (1, 2)} | {(k, "rank1_closed", None) for k in range(3)}

# Independent exact Cramer and localization replay.
w = [C(1), V("x1"), V("x2")]
v = [V("v0"), V("v1"), V("v2")]
d = add(v[1], neg(mul(w[1], v[0])))
t0, abar = V("t0"), V("abar")
reduced = add(abar, neg(mul(t0, w[2])))
u0 = [add(mul(reduced, v[1]), mul(w[1], t0, v[2])), neg(add(mul(t0, v[2]), mul(reduced, v[0]))), mul(d, t0)]
assert dot(u0, v) == C(0) and dot(u0, w) == mul(d, abar)
for m_index in (1, 2):
    tm = V(f"t{m_index}")
    um = [mul(tm, entry) for entry in cross(w, v)]
    assert dot(um, v) == C(0) and dot(um, w) == C(0)
    assert cross(u0, um) == [neg(mul(tm, d, abar, entry)) for entry in v]

N, P, b, tm, sat = [V(name) for name in ("N", "P", "b", "tm", "sat")]
saturation = add(mul(P, b, tm, sat), C(-1))
assert add(mul(b, mul(N, P, tm, sat)), neg(N)) == mul(N, saturation)
rho, vj, v0, inv = [V(name) for name in ("rho", "vj", "v0", "inv")]
assert add(mul(v0, mul(rho, vj, inv)), neg(mul(rho, vj))) == mul(rho, vj, add(mul(v0, inv), C(-1)))

cover = []
for k in range(3):
    for t1, t2 in itertools.product((False, True), repeat=2):
        branch = "D(t1)" if t1 else ("D(t2)" if t2 else "V(t1,t2)")
        cover.append((k, t1, t2, branch))
assert {branch for _, _, _, branch in cover} == {"D(t1)", "D(t2)", "V(t1,t2)"}
assert result["identity_replay"]["saturation_forward"] == "sat_new=sat_old/t_m"
assert result["identity_replay"]["saturation_reverse"] == "sat_old=t_m*sat_new"

assert result["scope"] == {
    "design_only": True,
    "singular_runs": 0,
    "ideal_runs": 0,
    "consumed_k0_reused": False,
    "mathematical_coverage": False,
    "rep5_closed": False,
    "performance_claim": False,
}
for forbidden in ("result.json", "ATTEMPT.json", "watchdog.json", "stdout.log", "stderr.log", "launch_clearance.json"):
    assert not (HERE / forbidden).exists()
assert not list(HERE.rglob("*.tmp"))

manifest = HERE / "MANIFEST.sha256"
if manifest.exists():
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        target = (manifest.parent / name.strip()).resolve()
        assert target.is_file() and sha(target) == expected, target

print(json.dumps({"status": "PASS", "literal_sources": 9, "open_sources": 6, "cover_strata": 9, "singular_runs": 0}, sort_keys=True))
