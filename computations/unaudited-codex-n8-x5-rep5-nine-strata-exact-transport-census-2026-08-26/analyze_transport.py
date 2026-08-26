#!/usr/bin/env python3
"""Exact source-labelled transport census for the nine corrected rep5 strata."""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import os
import re
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V2 = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25"
V2_MANIFEST_SHA = "50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1"
V2_RESULT_SHA = "4d572fc359430eab8a55ee80ffe98993521e510f9eb48c37ab185742ad19bf00"
SUPPORT = frozenset({(2,4),(1,2),(0,4),(2,7),(1,5),(3,7),(0,3),(0,6),(6,7),(4,5),(1,7),(2,6),(3,6),(1,6),(3,5)})
FIXED = frozenset({(1,6),(4,5),(0,3),(2,7)})
ELIMINATED = (3,6)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_program(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text()
    ring = next(line for line in text.splitlines() if line.startswith("ring r="))
    variables = ring.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    equations, depth, start = [], 0, 0
    for position, character in enumerate(body):
        if character == "(": depth += 1
        elif character == ")": depth -= 1
        elif character == "," and depth == 0:
            equations.append(body[start:position].strip()); start = position + 1
        assert depth >= 0
    equations.append(body[start:].strip()); assert depth == 0
    return variables, equations


def occurrence_rows(variables: list[str], equations: list[str]) -> dict[str, array]:
    positions = {name: index for index, name in enumerate(variables)}
    rows = {name: array("I", [0]) * 6561 for name in variables}
    token = re.compile(r"\b(?:" + "|".join(map(re.escape, sorted(variables, key=len, reverse=True))) + r")\b")
    for equation_index, equation in enumerate(equations[:6561]):
        for name, count in collections.Counter(token.findall(equation)).items():
            assert name in positions and count > 0
            rows[name][equation_index] = count
    return rows


def word(index: int) -> tuple[int, ...]:
    digits = [0] * 8
    for position in range(7, -1, -1): digits[position], index = index % 3, index // 3
    return tuple(digits)


def word_index(digits: tuple[int, ...]) -> int:
    out = 0
    for digit in digits: out = 3 * out + digit
    return out


def signature(row: array, mapping: list[int]) -> bytes:
    return array("I", (row[index] for index in mapping)).tobytes()


def multiset(rows: dict[str, array], mapping: list[int]) -> collections.Counter[bytes]:
    return collections.Counter(signature(row, mapping) for row in rows.values())


def signature_witness(source_rows: dict[str, array], target_rows: dict[str, array], mapping: list[int]) -> dict:
    source_by_signature: dict[bytes, list[str]] = collections.defaultdict(list)
    target_by_signature: dict[bytes, list[str]] = collections.defaultdict(list)
    identity = list(range(6561))
    for name, row in source_rows.items(): source_by_signature[signature(row, identity)].append(name)
    for name, row in target_rows.items(): target_by_signature[signature(row, mapping)].append(name)
    for packed in sorted(source_by_signature):
        if len(source_by_signature[packed]) > len(target_by_signature.get(packed, [])):
            counts = array("I"); counts.frombytes(packed)
            nonzero = [(index, value) for index, value in enumerate(counts) if value]
            return {
                "signature_sha256": hashlib.sha256(packed).hexdigest(),
                "source_variables": sorted(source_by_signature[packed]),
                "source_multiplicity": len(source_by_signature[packed]),
                "target_multiplicity": len(target_by_signature.get(packed, [])),
                "nonzero_generator_count": len(nonzero),
                "first_nonzero_occurrences": nonzero[:8],
            }
    raise AssertionError("no mismatch witness despite unequal multisets")


assert sha256(V2 / "MANIFEST.sha256") == V2_MANIFEST_SHA
assert sha256(V2 / "results_design_v2.json") == V2_RESULT_SHA
design = json.loads((V2 / "results_design_v2.json").read_text())
assert design["status"] == "PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES"
source_records = design["sources"]; assert len(source_records) == 9
parsed = {}
for record in source_records:
    path = V2 / record["path"]
    assert sha256(path) == record["sha256"]
    variables, equations = parse_program(path)
    assert len(variables) == record["variables"]
    assert len(equations) == record["generators"]
    assert len(equations[:6561]) == 6561
    parsed[record["path"]] = {"record": record, "variables": variables, "equations": equations, "rows": occurrence_rows(variables, equations)}

# Exact site automorphisms preserve support, fixed identity blocks, and the
# eliminated response edge.  The first two conditions already force identity;
# retaining the third makes the source-label contract explicit.
site_automorphisms = []
for permutation in itertools.permutations(range(8)):
    image_support = {tuple(sorted((permutation[i], permutation[j]))) for i, j in SUPPORT}
    image_fixed = {tuple(sorted((permutation[i], permutation[j]))) for i, j in FIXED}
    image_eliminated = tuple(sorted((permutation[ELIMINATED[0]], permutation[ELIMINATED[1]])))
    if image_support == SUPPORT and image_fixed == FIXED and image_eliminated == ELIMINATED:
        site_automorphisms.append(permutation)
assert site_automorphisms == [tuple(range(8))]

color_permutations = list(itertools.permutations(range(3)))
words = [word(index) for index in range(6561)]
generator_maps = {
    "".join(map(str, permutation)): [word_index(tuple(permutation[value] for value in tensor_word)) for tensor_word in words]
    for permutation in color_permutations
}
identity_map = list(range(6561))
identity_multisets = {name: multiset(data["rows"], identity_map) for name, data in parsed.items()}
pair_ledger = []
classes = []
names = [record["path"] for record in source_records]
positive_edges = set()
for source_name in names:
    source = parsed[source_name]
    for target_name in names:
        target = parsed[target_name]
        same_shape = (len(source["variables"]), len(source["equations"])) == (len(target["variables"]), len(target["equations"]))
        matches = []
        first_witness = None
        if same_shape:
            for permutation in color_permutations:
                key = "".join(map(str, permutation)); mapping = generator_maps[key]
                if identity_multisets[source_name] == multiset(target["rows"], mapping):
                    matches.append(key)
                elif first_witness is None:
                    first_witness = {"color_permutation": key, **signature_witness(source["rows"], target["rows"], mapping)}
        if matches:
            # The exhaustive necessary filter leaves only literal self/identity.
            assert source_name == target_name and matches == ["012"]
            assert source["variables"] == target["variables"] and source["equations"] == target["equations"]
            positive_edges.add((source_name, target_name))
        pair_ledger.append({
            "source": source_name, "target": target_name, "same_ring_and_generator_counts": same_shape,
            "color_permutations_tested": 6 if same_shape else 0,
            "exact_occurrence_multiset_matches": matches,
            "first_exact_mismatch_witness": first_witness,
            "full_generator_mapping_verified": bool(matches),
        })
assert positive_edges == {(name, name) for name in names}
classes = [[name] for name in names]
self_replays = []
for name in names:
    data = parsed[name]
    aggregate = hashlib.sha256("\0".join(data["equations"]).encode()).hexdigest()
    self_replays.append({"path": name, "generator_count": len(data["equations"]), "variable_count": len(data["variables"]), "generator_sequence_sha256": aggregate, "variable_bijection": "identity", "generator_bijection": "identity", "all_generators_exact": True})

selected = "rep5_p00_guardpivot_k2_rank2_t1_Q.sing"
out = {
    "allowed_action": {
        "site_permutations_enumerated": 40320, "source_label_preserving_site_automorphisms": [list(item) for item in site_automorphisms],
        "color_permutations_enumerated": [list(item) for item in color_permutations],
        "ring_variable_bijection_filter": "arbitrary bijection; exact per-amplitude-generator occurrence vectors compared as byte strings",
        "why_fail_closed": "any ring-variable bijection carrying all generators must carry the exact occurrence-vector multiset; a mismatch proves nonisomorphism before coefficients or monomials are weakened",
    },
    "branch_invariant": {"open84": {"variables": 84, "generators": 6562, "count": 6}, "complement86": {"variables": 86, "generators": 6570, "count": 3}, "cross_branch_transport": False},
    "exact_transport_classes": classes,
    "full_generator_self_replays": self_replays,
    "pair_ledger": pair_ledger,
    "pins": {"v2_manifest_sha256": V2_MANIFEST_SHA, "v2_result_sha256": V2_RESULT_SHA, "source_sha256": {record["path"]: record["sha256"] for record in source_records}},
    "required_representative_count": 9,
    "required_open84_representatives": 6,
    "required_complement86_representatives": 3,
    "schema": "KRENN_X5_REP5_NINE_STRATA_EXACT_TRANSPORT_CENSUS_V1",
    "selected_k2_t1_transport": {"source": selected, "covers": [selected], "does_not_cover": [name for name in names if name != selected]},
    "scope": {"design_only": True, "singular_runs": 0, "ideal_runs": 0, "mathematical_coverage": False, "rep5_closed": False},
    "status": "PASS_EXACT_PARTITION_NINE_SINGLETONS_NO_CROSS_STRATUM_TRANSPORT",
}
temporary = HERE / "results_transport_partition.json.tmp"
temporary.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n"); os.replace(temporary, HERE / "results_transport_partition.json")
print(json.dumps({"status": out["status"], "classes": len(classes), "required": 9, "selected_covers": 1}, sort_keys=True))
