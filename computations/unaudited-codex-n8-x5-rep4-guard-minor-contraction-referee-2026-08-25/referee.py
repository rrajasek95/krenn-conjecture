#!/usr/bin/env python3
"""Independent referee for the rep4 guard-minor contraction design."""
import collections
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25"
OBL = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25"
OUT = HERE / "results_referee.json"
PLAN = HERE / "ONE_CHART_MODULAR_HELD_PLAN.json"

EXPECTED = {
    PROD / "MANIFEST.sha256": "7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02",
    PROD / "results_rep4_contraction_design.json": "7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c",
    PROD / "generate_design.py": "b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a",
    PROD / "chart_orbit_ledger.json": "dac85725f217b45cbaae7b9b434640309cc5ed6e0b40e846534c8a26409bd4d8",
    PROD / "rep4_guard_minor_tiny_y_Q.sing": "d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b",
    PROD / "rep4_guard_minor_tiny_z_Q.sing": "6e760563b048b7bfa27c5b3df60e22f30d73264747876e6a70c862d5cb3f8ddd",
    PARENT / "MANIFEST.sha256": "9a3cec1a39422d2c3d7a6b40f6acdec0b04b19b893c0a1fb657c69d3b50bb8fe",
    PARENT / "results_remaining_reps_low_rank_carrier.json": "359aa45545d85378dd9e945eb82be3adb98922648025fe853f930feac2b5f458",
    OBL / "MANIFEST.sha256": "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf",
    OBL / "results_full_family_obligation.json": "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_manifest(path):
    count = 0
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        assert sha(path.parent / rel.strip()) == digest, (path, rel)
        count += 1
    return count


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def orbit_representative(record):
    coordinate, p, q, r, kind, s, a, b = record
    candidates = []
    for permutation in itertools.permutations(range(3)):
        aa, bb = sorted((permutation[a], permutation[b]))
        candidates.append((
            permutation[coordinate], permutation[p], permutation[q], permutation[r],
            kind, permutation[s], aa, bb,
        ))
    return min(candidates)


def top_level_count(body):
    depth = 0
    count = 1 if body.strip() else 0
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            assert depth >= 0
        elif char == "," and depth == 0:
            count += 1
    assert depth == 0
    return count


def polynomial_identity_census():
    def var(name):
        return collections.Counter({(name,): 1})

    def add(*polys):
        out = collections.Counter()
        for poly in polys:
            out.update(poly)
        return collections.Counter({term: value for term, value in out.items() if value})

    def mul(*polys):
        out = collections.Counter({(): 1})
        for poly in polys:
            following = collections.Counter()
            for left, left_value in out.items():
                for right, right_value in poly.items():
                    following[tuple(sorted(left + right))] += left_value * right_value
            out = collections.Counter({term: value for term, value in following.items() if value})
        return out

    def neg(poly):
        return collections.Counter({term: -value for term, value in poly.items()})

    checks = 0
    for a, b in itertools.combinations(range(3), 2):
        c = next(value for value in range(3) if value not in (a, b))
        w = [var(f"w{j}") for j in range(3)]
        v = [var(f"v{j}") for j in range(3)]
        t, abar = var("t"), var("abar")
        determinant = add(mul(w[a], v[b]), neg(mul(w[b], v[a])))
        for active in (False, True):
            reduced = add(abar if active else collections.Counter(), neg(mul(t, w[c])))
            row = [None] * 3
            row[a] = add(mul(reduced, v[b]), mul(w[b], t, v[c]))
            row[b] = neg(add(mul(w[a], t, v[c]), mul(reduced, v[a])))
            row[c] = mul(determinant, t)
            guard = add(*(mul(row[j], v[j]) for j in range(3)))
            incidence = add(*(mul(row[j], w[j]) for j in range(3)))
            assert guard == collections.Counter()
            assert incidence == (mul(determinant, abar) if active else collections.Counter())
            checks += 2
    return checks


for path, digest in EXPECTED.items():
    assert sha(path) == digest, (path, sha(path), digest)
manifest_entries = replay_manifest(PROD / "MANIFEST.sha256")
result = json.loads((PROD / "results_rep4_contraction_design.json").read_text())

# Independent source-labelled support/guard/carrier replay.
fixed = {(0, 3), (1, 6), (2, 7), (4, 5)}
variable = {(0, 4), (1, 2), (3, 5), (6, 7)}
added = {(0, 6), (1, 5), (1, 7), (2, 3), (2, 6), (4, 6), (4, 7)}
support = fixed | variable | added
all_matchings = tuple(sorted(matchings(tuple(range(8)))))
supported = tuple(value for value in all_matchings if set(value) <= support)
assert len(all_matchings) == 105 and len(supported) == 12
assert ["|".join(f"{a}{b}" for a, b in value) for value in supported] == result["source_reconstruction"]["supported_matchings"]
assert result["source_reconstruction"]["added"] == ["06", "15", "17", "23", "26", "46", "47"]
assert result["source_reconstruction"]["guard"] == ["A06*A47^T=0", "(I-A17*A26)*A47^T=0"]
assert result["source_reconstruction"]["carrier"] == "A06^T*K*[A23^T|A35]"
assert result["source_reconstruction"]["incidence"] == ["A06*x=e_i", "A23^T*y+A35*z=e_i"]
parent = json.loads((PARENT / "results_remaining_reps_low_rank_carrier.json").read_text())
rep4 = next(item for item in parent["representatives"] if item["representative_id"] == 4)
assert rep4["support"]["added_nonzero"] == result["source_reconstruction"]["added"]
assert rep4["carrier"]["factorization_up_to_output_permutation"] == "A06^T*K*[A23^T|A35]"
obligation = json.loads((OBL / "results_full_family_obligation.json").read_text())["six_full_family_representatives"][4]
assert obligation["guard"]["derived"] == ["A46^T=-A26*A47^T", "(I-A17*A26)*A47^T=0", "A06*A47^T=0"]
assert obligation["full_x5_6561_equation_sha256"] == result["source_reconstruction"]["full_x5_digest"]

# Independent raw chart enumeration and common-colour S3 quotient.
raw = []
for coordinate, p, q, r, s in itertools.product(range(3), repeat=5):
    for kind in ("y", "z"):
        for other in range(3):
            if other != q:
                a, b = sorted((q, other))
                raw.append((coordinate, p, q, r, kind, s, a, b))
groups = collections.defaultdict(list)
for chart in raw:
    groups[orbit_representative(chart)].append(chart)
assert len(raw) == 972 and len(groups) == 162
assert set(map(len, groups.values())) == {6}
assert sum(key[4] == "y" for key in groups) == sum(key[4] == "z" for key in groups) == 81
ledger = json.loads((PROD / "chart_orbit_ledger.json").read_text())
assert ledger["raw"] == 972 and len(ledger["groups"]) == 162
for item in ledger["groups"]:
    key = tuple(item["representative"])
    assert key in groups and item["size"] == len(groups[key]) == 6
    assert {tuple(x) for x in item["members"]} == set(groups[key])

# Exact Cramer formulas: all three two-column minors and both delta branches.
assert polynomial_identity_census() == result["symbolic_replay"]["generic_cramer_polynomial_identities"] == 12
assert result["orientation_audit"] == {
    "outside_row": "v=row_p(A47); A06*v=0 is the row-p equation of A06*A47^T=0",
    "reduced_guard_entry": "A47[j,i]-sum_k,l A17[i,k]A26[k,l]A47[j,l]=0",
    "y_pivot": "y_s=1 solves row s of A23 because (A23^T*y)_i=sum_j A23[j,i]y_j",
    "z_pivot": "z_s=1 solves column s of A35 because (A35*z)_i=sum_j A35[i,j]z_j",
}
assert result["chart_cover"]["saturation"] == "abar*beta*A47[p,q]*d*sat-1"
assert result["substitution"]["tautologies_removed"] == ["six incidence equations", "three row-p A06*A47^T equations"]

assert result["counts"] == {
    "old_variables": 100, "old_generators": 6586,
    "new_variables": 91, "new_generators": 6577,
    "full_x5": 6561, "remaining_guard": 15, "combined_saturation": 1,
}
for kind, expected_sha in (("y", EXPECTED[PROD / "rep4_guard_minor_tiny_y_Q.sing"]), ("z", EXPECTED[PROD / "rep4_guard_minor_tiny_z_Q.sing"])):
    item = result["materialized_inputs"][kind]
    source = (PROD / item["path"]).read_text()
    assert sha(PROD / item["path"]) == expected_sha == item["sha256"]
    assert source.count("ring r=0,") == 1 and "ring r=32003," not in source
    ring_start = source.index("ring r=0,(") + len("ring r=0,(")
    ring_end = source.index("),dp;", ring_start)
    variables = [value.strip() for value in source[ring_start:ring_end].split(",")]
    assert len(variables) == len(set(variables)) == 91
    assert not any(name.startswith("a06_") for name in variables)
    if kind == "y":
        assert not any(name in variables for name in ("a23_00", "a23_01", "a23_02"))
    else:
        assert not any(name in variables for name in ("a35_00", "a35_10", "a35_20"))
    ideal_start = source.index("ideal I=") + len("ideal I=")
    ideal_end = source.index(";\nprint(\"INPUT_VARIABLES=", ideal_start)
    assert top_level_count(source[ideal_start:ideal_end]) == 6577
    assert "slimgb(" not in source and "reduce(" not in source
    assert source.count("quit;") == 1

assert result["scope"] == {"materialized_design_inputs": 2, "ideal_runs": 0, "rep4_closed": False, "transport_claimed": False}
assert all(result["hostile_tests"].values())
plan = json.loads(PLAN.read_text())
assert plan["status"] == "HELD_NOT_RUN_RESOURCE_BLOCKED"
assert plan["launch_authorized"] is False
assert plan["chart"] == [0, 0, 0, 0, "y", 0, 0, 1]
assert plan["diagnostic_Q_source_sha256"] == EXPECTED[PROD / "rep4_guard_minor_tiny_y_Q.sing"]
assert plan["p32003_solver_source_expected_sha256"] == "9471d6bbfb0af012c313cafa97e12f5b3cea380e6cefb0c8f355cb53def80524"
assert plan["maximum_lanes"] == 1 and plan["automatic_relaunch"] is False

audit = {
    "schema": "KRENN_X5_REP4_GUARD_MINOR_CONTRACTION_REFEREE_V1",
    "status": "PASS_STRICT_SMALLER_EXACT_DESIGN_NO_RUN_NO_CLOSURE",
    "producer_manifest_sha256": EXPECTED[PROD / "MANIFEST.sha256"],
    "producer_result_sha256": EXPECTED[PROD / "results_rep4_contraction_design.json"],
    "manifest_entries_replayed": manifest_entries,
    "support_guard_carrier_regenerated": True,
    "cramer_polynomial_identities": 12,
    "counts": result["counts"],
    "chart_census": result["chart_census"],
    "materialized_Q_sources": 2,
    "ideal_runs": 0,
    "rep4_closed": False,
    "one_chart_held_plan_sha256": sha(PLAN),
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": audit["status"], "result_sha256": sha(OUT)}, sort_keys=True))
