#!/usr/bin/env python3
"""Independent finite referee for the refined-91 cross-representative census.

This performs no Singular/Groebner/closure computation.  It rebuilds the
coloured support obstruction, colour-equivariant grading maps, and S3 chart
quotient directly from the sealed source records.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions are load-bearing")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMP = ROOT / "computations"
PRODUCER = COMP / "unaudited-codex-n8-x5-refined91-cross-representative-isomorphism-census-2026-08-25"
R1Q = COMP / "unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25"
R1G = COMP / "unaudited-codex-n8-x5-seven-block-rep1-diagonal-incidence-gate-2026-08-25"
R2 = COMP / "unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25"
R4 = COMP / "unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25"
R5 = COMP / "unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


PINS = {
    PRODUCER / "MANIFEST.sha256": "67dd1446276a21321a550dc12c74e60ed4d78e1122848cb2b96b2c2f13f3b134",
    PRODUCER / "results_isomorphism_census.json": "79d73aee9fdae65338557b3ba74032eb3395b113d46d5b29b6d289c6e6036cd6",
    PRODUCER / "equivalence_class_ledger.json": "ba6b0cc98309c860c1b91d024eb5effe050790ceae60ec1995385b8d7be73cd7",
    R1Q / "MANIFEST.sha256": "4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1",
    R1Q / "minor_quotient_metadata.json": "1a8c5bb3c105d8d87b2eab58a52934a44d7768c537cc33a1542d7d06402d317c",
    R1Q / "generate_minor_quotient.py": "63a4a58344c4bfdce0406d243f881216ca53eaa71264926a28364a823f560ac8",
    R1Q / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing": "edd174ccbc75a563fd67e0515b6dde2c54e5469b742629953080290fe7d1fb49",
    R1G / "MANIFEST.sha256": "36e39752896a052d8bfe75af29c39c4d8c09c090afb8a9692e818a63c9a811bf",
    R1G / "gate_metadata.json": "97342352d9162253c0c27aefdeba81f25b1265751e4c29daf706f828f4c9572e",
    R2 / "MANIFEST.sha256": "ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2",
    R2 / "results_rep2_corrected_contraction_design.json": "ed37c2e0da8088e08fb6891e60768d98fbbbf031935f752b4e4af280dfe27b26",
    R2 / "generate_design.py": "ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc",
    R2 / "rep2_corrected_guard_minor_tiny_y_Q.sing": "0285c34fcae56db7dc60830197d645799f5f1c90d84467868436ee453916aedf",
    R2 / "rep2_corrected_guard_minor_tiny_z_Q.sing": "3cc285cf29b2416b674f325c7afb891570c5bd4b92e0da458d8926c0f958fae4",
    R4 / "MANIFEST.sha256": "7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02",
    R4 / "results_rep4_contraction_design.json": "7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c",
    R4 / "generate_design.py": "b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a",
    R4 / "rep4_guard_minor_tiny_y_Q.sing": "d46cdf77b9edafbc17a92ec851badba2db63640ec7324e024a83e29da04e121b",
    R4 / "rep4_guard_minor_tiny_z_Q.sing": "6e760563b048b7bfa27c5b3df60e22f30d73264747876e6a70c862d5cb3f8ddd",
    R5 / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    R5 / "results_rep5_contraction_design.json": "b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b",
    R5 / "generate_design.py": "3844eadf4a9e21c2feb012cbd684c22ca7611f4d22f87659e19952d0381614f4",
    R5 / "rep5_guard_minor_tiny_y_p32003.sing": "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97",
    R5 / "rep5_guard_minor_tiny_z_p32003.sing": "cf9d4eafc3b25a59f848a3f3be942cd92c1e1758682cd83d3163a9e757ba3ce7",
}

REPS = (1, 2, 4, 5)
COLOURS = (0, 1, 2)
S3 = tuple(itertools.permutations(COLOURS))
SITES = tuple(range(8))
SITE_PERMS = tuple(itertools.permutations(SITES))
F_EXPECTED = frozenset({(0, 3), (1, 6), (2, 7), (4, 5)})
V_EXPECTED = frozenset({(0, 4), (1, 2), (3, 5), (6, 7)})
A_EXPECTED = {
    1: frozenset({(0, 6), (1, 3), (1, 7), (2, 5), (2, 6), (4, 6), (4, 7)}),
    2: frozenset({(0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)}),
    4: frozenset({(0, 6), (1, 5), (1, 7), (2, 3), (2, 6), (4, 6), (4, 7)}),
    5: frozenset({(0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 6), (3, 7)}),
}
ELIMINATED = {1: (4, 6), 2: (5, 6), 4: (4, 6), 5: (3, 6)}
PARTNER = {
    1: {"y": ((1, 3), "row"), "z": ((3, 5), "column")},
    2: {"y": ((2, 3), "row"), "z": ((3, 5), "column")},
    4: {"y": ((2, 3), "row"), "z": ((3, 5), "column")},
    5: {"y": ((3, 5), "column"), "z": ((3, 7), "column")},
}


def parse_edges(values):
    return frozenset(tuple(map(int, value)) for value in values)


def load_sources():
    rep1_gate = json.loads((R1G / "gate_metadata.json").read_text())
    rep1_quotient = json.loads((R1Q / "minor_quotient_metadata.json").read_text())
    rep2 = json.loads((R2 / "results_rep2_corrected_contraction_design.json").read_text())
    rep4 = json.loads((R4 / "results_rep4_contraction_design.json").read_text())
    rep5 = json.loads((R5 / "results_rep5_contraction_design.json").read_text())
    source_sections = {
        1: rep1_gate["support"],
        2: rep2["independent_source_reconstruction"],
        4: rep4["source_reconstruction"],
        5: rep5["source_reconstruction"],
    }
    design_sections = {1: rep1_quotient, 2: rep2, 4: rep4, 5: rep5}
    supports = {}
    for rep in REPS:
        section = source_sections[rep]
        fset, vset, aset = (parse_edges(section[key]) for key in ("fixed", "variable", "added"))
        assert fset == F_EXPECTED and vset == V_EXPECTED and aset == A_EXPECTED[rep]
        assert not (fset & vset or fset & aset or vset & aset)
        assert len(fset | vset | aset) == 15
        supports[rep] = {"F": fset, "V": vset, "A": aset, "all": fset | vset | aset}
        counts = design_sections[rep]["counts"]
        if rep == 1:
            assert counts["minor_quotient_variables"] == 91
            assert counts["minor_quotient_generators"] == 6577
            chart = design_sections[rep]["chart_census"]
            assert chart["raw_refined_charts"] == 972 and chart["s3_orbits"] == 162
            assert chart["orbits_by_partner_kind"] == {"y": 81, "z": 81}
        else:
            assert counts["new_variables"] == 91 and counts["new_generators"] == 6577
            assert counts["full_x5"] == 6561 and counts["remaining_guard"] == 15
            chart = design_sections[rep]["chart_census"]
            assert chart == {"raw": 972, "S3_orbits": 162, "orbit_size": 6, "y_orbits": 81, "z_orbits": 81}
    return supports


def move_edges(edges, permutation):
    return frozenset(tuple(sorted((permutation[a], permutation[b]))) for a, b in edges)


def support_graph_referee(supports, producer):
    counts = {str(left): {} for left in REPS}
    canonical = {}
    tested = 0
    pairs = tuple(itertools.combinations(SITES, 2))
    for left in REPS:
        codes = []
        for permutation in SITE_PERMS:
            moved = {name: move_edges(supports[left][name], permutation) for name in ("F", "V", "A")}
            codes.append("".join("F" if edge in moved["F"] else "V" if edge in moved["V"] else "A" if edge in moved["A"] else "." for edge in pairs))
        identity = codes[0]
        best = min(codes)
        canonical[str(left)] = {
            "automorphisms": sum(code == identity for code in codes),
            "canonicalizers": sum(code == best for code in codes),
            "canonical_code": best,
            "canonical_sha256": hashlib.sha256(best.encode()).hexdigest(),
        }
        for right in REPS:
            count = 0
            for permutation in SITE_PERMS:
                tested += 1
                if (move_edges(supports[left]["F"], permutation) == supports[right]["F"] and
                    move_edges(supports[left]["V"], permutation) == supports[right]["V"] and
                    move_edges(supports[left]["A"], permutation) == supports[right]["A"]):
                    count += 1
            counts[str(left)][str(right)] = count
    expected = {str(left): {str(right): int(left == right) for right in REPS} for left in REPS}
    assert counts == expected
    assert canonical == producer["support_graphs"]
    assert counts == producer["site_permutation_isomorphism_counts"]
    assert tested == len(REPS) ** 2 * 40320 == 645120
    return canonical, counts, tested


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    head = vertices[0]
    for index in range(1, len(vertices)):
        for rest in perfect_matchings(vertices[1:index] + vertices[index + 1:]):
            yield tuple(sorted(((head, vertices[index]),) + rest))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))
assert len(MATCHINGS) == 105


def polynomial_signature(support, word):
    monomials = []
    for matching in MATCHINGS:
        if not set(matching) <= support["all"]:
            continue
        variables = []
        for edge in matching:
            i, j = word[edge[0]], word[edge[1]]
            if edge in support["F"]:
                if i != j:
                    break
            else:
                variables.append((edge, i, j))
        else:
            monomials.append((matching, tuple(variables)))
    return tuple(monomials)


def full_word_covariance(supports):
    checks = 0
    for rep in REPS:
        for permutation in S3:
            for word in itertools.product(COLOURS, repeat=8):
                target_word = tuple(permutation[c] for c in word)
                mapped = tuple(
                    (matching, tuple((edge, permutation[i], permutation[j]) for edge, i, j in variables))
                    for matching, variables in polynomial_signature(supports[rep], word)
                )
                assert mapped == polynomial_signature(supports[rep], target_word)
                checks += 1
    assert checks == 4 * 6 * (3 ** 8) == 157464
    return checks


def chart_action(chart, permutation):
    coordinate, outside_row, outside_col, x_pivot, kind, partner_pivot, a, b = chart
    aa, bb = sorted((permutation[a], permutation[b]))
    return (permutation[coordinate], permutation[outside_row], permutation[outside_col],
            permutation[x_pivot], kind, permutation[partner_pivot], aa, bb)


def independent_charts():
    raw = []
    for coordinate, outside_row, outside_col, x_pivot, partner_pivot in itertools.product(COLOURS, repeat=5):
        for kind in ("y", "z"):
            for other in COLOURS:
                if other != outside_col:
                    a, b = sorted((outside_col, other))
                    raw.append((coordinate, outside_row, outside_col, x_pivot, kind, partner_pivot, a, b))
    assert len(raw) == 972 and len(set(raw)) == 972
    orbits = defaultdict(set)
    for chart in raw:
        orbit = {chart_action(chart, permutation) for permutation in S3}
        orbits[min(orbit)].update(orbit)
    assert len(orbits) == 162
    assert Counter(len(members) for members in orbits.values()) == {6: 162}
    assert Counter(key[4] for key in orbits) == {"y": 81, "z": 81}
    return raw, dict(orbits)


def matrix_variables(rep, chart):
    kind, pivot = chart[4], chart[5]
    retained = sorted((V_EXPECTED | A_EXPECTED[rep]) - {ELIMINATED[rep]})
    solved = {((0, 6), i, j) for i in COLOURS for j in COLOURS}
    partner, orientation = PARTNER[rep][kind]
    if orientation == "row":
        solved.update((partner, pivot, j) for j in COLOURS)
    else:
        solved.update((partner, i, pivot) for i in COLOURS)
    values = {(edge, i, j) for edge in retained for i in COLOURS for j in COLOURS}
    values -= solved
    assert len(values) == 78
    return values


def witness_variables(chart):
    x_pivot, kind, partner_pivot = chart[3], chart[4], chart[5]
    values = {("x", i) for i in COLOURS if i != x_pivot}
    values |= {("y", i) for i in COLOURS if kind != "y" or i != partner_pivot}
    values |= {("z", i) for i in COLOURS if kind != "z" or i != partner_pivot}
    values |= {("t", i) for i in COLOURS}
    values |= {("scalar", name) for name in ("abar", "beta", "sat")}
    assert len(values) == 13
    return values


def map_matrix(values, permutation):
    return {(edge, permutation[i], permutation[j]) for edge, i, j in values}


def map_witness(values, permutation):
    answer = set()
    for family, index in values:
        if family in ("x", "y", "z", "t"):
            answer.add((family, permutation[index]))
        else:
            answer.add((family, index))
    return answer


def expected_ring_names(rep, chart):
    matrix = {f"a{edge[0]}{edge[1]}_{i}{j}" for edge, i, j in matrix_variables(rep, chart)}
    witness = set()
    for family, index in witness_variables(chart):
        witness.add(f"{family}n{index}" if family in ("x", "y", "z") else f"t{index}" if family == "t" else index)
    return matrix | witness


def parse_singular(path):
    source = path.read_text()
    match = re.search(r"^ring r=([^,]+),\(([^\n]+)\),dp;$", source, re.MULTILINE)
    assert match
    variables = match.group(2).split(",")
    assert len(variables) == len(set(variables)) == 91
    body = source.split("ideal I=", 1)[1].split(";", 1)[0]
    generators = body.count(",\n") + 1
    assert generators == 6577
    return match.group(1), set(variables), generators


MATERIALIZED = {
    1: {"y": (R1Q / "rep1_minor_i0_p00_x0_y0_d01_p32003.sing", "32003")},
    2: {"y": (R2 / "rep2_corrected_guard_minor_tiny_y_Q.sing", "0"), "z": (R2 / "rep2_corrected_guard_minor_tiny_z_Q.sing", "0")},
    4: {"y": (R4 / "rep4_guard_minor_tiny_y_Q.sing", "0"), "z": (R4 / "rep4_guard_minor_tiny_z_Q.sing", "0")},
    5: {"y": (R5 / "rep5_guard_minor_tiny_y_p32003.sing", "32003"), "z": (R5 / "rep5_guard_minor_tiny_z_p32003.sing", "32003")},
}


def materialized_grading_referee():
    records = []
    for rep, lanes in MATERIALIZED.items():
        for kind, (path, expected_field) in lanes.items():
            chart = (0, 0, 0, 0, kind, 0, 0, 1)
            field, variables, generators = parse_singular(path)
            assert field == expected_field
            assert variables == expected_ring_names(rep, chart)
            records.append({"representative": rep, "partner_kind": kind, "field": field,
                            "variables": len(variables), "generators": generators,
                            "source_sha256": sha256(path)})
    assert len(records) == 7
    return records


def chart_ledger_referee(orbits, producer_ledger):
    classes = producer_ledger["classes"]
    assert len(classes) == 648
    class_ids = set()
    chart_maps = 0
    generator_family_maps = 0
    signs = Counter()
    per_rep = Counter()
    for record in classes:
        rep = record["representative"]
        assert rep in REPS
        per_rep[rep] += 1
        assert record["class_id"] not in class_ids
        class_ids.add(record["class_id"])
        canonical = tuple(record["canonical_chart"])
        assert canonical in orbits
        expected_members = orbits[canonical]
        actual_members = {tuple(member["chart"]) for member in record["raw_members"]}
        assert actual_members == expected_members
        assert record["raw_member_count"] == len(record["raw_members"]) == 6
        assert record["cross_representative_members"] == []
        assert record["class_id"] == f"rep{rep}_orbit{sorted(orbits).index(canonical):03d}"
        for member in record["raw_members"]:
            target = tuple(member["chart"])
            candidates = [permutation for permutation in S3 if chart_action(canonical, permutation) == target]
            assert len(candidates) == 1
            permutation = candidates[0]
            assert tuple(member["colour_permutation"]) == permutation
            assert map_matrix(matrix_variables(rep, canonical), permutation) == matrix_variables(rep, target)
            assert map_witness(witness_variables(canonical), permutation) == witness_variables(target)
            a, b = canonical[6:8]
            aa, bb = target[6:8]
            sign = 1 if (permutation[a], permutation[b]) == (aa, bb) else -1
            assert (permutation[a], permutation[b]) in ((aa, bb), (bb, aa))
            assert member["minor_sign"] == sign
            signs[sign] += 1
            chart_maps += 1
            generator_family_maps += 6561 + 6 + 9 + 1
    assert per_rep == {rep: 162 for rep in REPS}
    assert chart_maps == 3888
    assert generator_family_maps == 25_571_376
    assert signs == {-1: 1944, 1: 1944}
    return {
        "classes_per_representative": {str(rep): per_rep[rep] for rep in REPS},
        "raw_chart_maps": chart_maps,
        "generator_family_maps": generator_family_maps,
        "minor_sign_census": {str(sign): signs[sign] for sign in (-1, 1)},
    }


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    for path, expected in PINS.items():
        actual = sha256(path)
        assert actual == expected, (path, expected, actual)
    producer = json.loads((PRODUCER / "results_isomorphism_census.json").read_text())
    producer_ledger = json.loads((PRODUCER / "equivalence_class_ledger.json").read_text())
    assert producer["status"] == "PASS_NO_CROSS_REPRESENTATIVE_ISOMORPHISMS"
    assert producer["scope"] == {"solver_runs": 0, "generator_claims_beyond_verified_bijections": 0, "mathematical_closure": False}
    supports = load_sources()
    canonical, cross_counts, site_maps = support_graph_referee(supports, producer)
    word_checks = full_word_covariance(supports)
    raw, orbits = independent_charts()
    grading_sources = materialized_grading_referee()
    ledger = chart_ledger_referee(orbits, producer_ledger)
    assert producer["census"] == {"representatives": 4, "raw_charts": 3888,
        "within_representative_S3_classes": 648, "cross_representative_equivalences": 0,
        "final_equivalence_classes": 648}
    positive = producer["positive_bijection_audit"]
    assert positive["full_word_generator_maps_checked"] == word_checks
    assert positive["chart_maps"]["explicit_chart_bijections"] == ledger["raw_chart_maps"]
    assert positive["chart_maps"]["generator_family_bijections"] == ledger["generator_family_maps"]
    assert positive["chart_maps"]["minor_sign_census"] == ledger["minor_sign_census"]
    result = {
        "schema": "KRENN_X5_REFINED91_CROSS_REPRESENTATIVE_ISOMORPHISM_CENSUS_REFEREE_V1",
        "status": "PASS_INDEPENDENT_NO_CROSS_REPRESENTATIVE_ISOMORPHISMS",
        "producer_pins": {"manifest_sha256": PINS[PRODUCER / "MANIFEST.sha256"],
                          "result_sha256": PINS[PRODUCER / "results_isomorphism_census.json"],
                          "ledger_sha256": PINS[PRODUCER / "equivalence_class_ledger.json"]},
        "support_referee": {"representatives": list(REPS), "coloured_edges_per_representative": 15,
                            "site_maps_tested": site_maps, "site_permutations_per_ordered_pair": 40320,
                            "ordered_pairs": 16, "isomorphism_counts": cross_counts,
                            "canonical_supports": canonical},
        "grading_referee": {"materialized_sources_checked": grading_sources,
                            "matrix_variables_per_chart": 78, "witness_scalar_variables_per_chart": 13,
                            "variables_per_chart": 91, "generators_per_chart": 6577,
                            "full_word_covariance_checks": word_checks},
        "chart_referee": {"raw_per_representative": len(raw), "S3_classes_per_representative": len(orbits),
                          "members_per_class": 6, "total_raw": len(raw) * 4,
                          "total_classes": len(orbits) * 4, **ledger},
        "theorem_scope": {
            "statement": "Under the frozen typed source-label/full-X5 bijection contract, every generator-level isomorphism induces a colour-preserving F/V/A site-support isomorphism; exhaustive zero cross-support counts therefore rule out every cross-representative generator-level isomorphism in that contract.",
            "cross_generator_isomorphisms": 0,
            "solver_runs": 0,
            "ideal_or_closure_claim": False,
            "design_census_only": True,
        },
        "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    atomic_json(HERE / "results_referee.json", result)
    print(json.dumps({"status": result["status"], "site_maps": site_maps,
                      "word_checks": word_checks, "raw_charts": 3888,
                      "classes": 648, "cross_isomorphisms": 0,
                      "solver_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
