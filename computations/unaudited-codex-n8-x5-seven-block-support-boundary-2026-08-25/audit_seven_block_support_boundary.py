#!/usr/bin/env python3
"""Exact seven-added-block closure and first structural carrier boundary."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "fcfc7f972dfb0ed6c7d9cffdc6e2ce552ebad68ae1bc0af121df1455029327b7"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/results_six_block_support_cap.json"
PARENT_RESULT_SHA256 = "fe1af0a5d935aa58a9727ba0b04c331e366b5c5c2b28979733188f175baa398d"
SIX_SOURCE = HERE.parent / "unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/audit_six_block_support_cap.py"
SIX_SOURCE_SHA256 = "8d45ee288a3ed3405946dae2f78467c7ff4b1fcaaa1e48ad646d86cd14793b87"
FIVE_SOURCE = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/audit_five_block_support_cap.py"
FIVE_SOURCE_SHA256 = "4a686fe5bbf80559283d993245166764d5b52d8b4bd33b144017f26f5f2c1f45"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(SIX_SOURCE) == SIX_SOURCE_SHA256
assert sha256(FIVE_SOURCE) == FIVE_SOURCE_SHA256
spec = importlib.util.spec_from_file_location("five_block", FIVE_SOURCE)
assert spec is not None and spec.loader is not None
five = importlib.util.module_from_spec(spec)
spec.loader.exec_module(five)


def permute_variables(variables):
    return frozenset(
        tuple(sorted((five.GUARD_PERMUTATION[a], five.GUARD_PERMUTATION[b])))
        for a, b in variables
    )


def nonidentity_certificates(support):
    certificates = []
    for cap in sorted(support - set(five.FIXED)):
        edges = five.response_edges(support, *cap)
        shape = five.carrier_shape(edges)
        if shape is not None:
            kind, defining_vertices = shape
            certificates.append({
                "cap": five.edge_string(cap),
                "carrier": kind,
                "defining_vertices": list(defining_vertices),
                "possible_response_edges": list(map(five.edge_string, edges)),
                "forbidden_response_rank": 0,
                "kernel_dimension": 9,
                "activity_hyperplanes": ["K00=0", "K11=0", "K22=0", f"<K,A{five.edge_string(cap)}>=0"],
                "active_by_hyperplane_avoidance": True,
            })
    return certificates


def replay_nonidentity(source, certificate, K):
    cap = tuple(map(int, certificate["cap"]))
    possible = {tuple(map(int, text)) for text in certificate["possible_response_edges"]}
    residual = tuple(site for site in range(8) if site not in cap)
    forbidden = tuple(edge for edge in itertools.combinations(residual, 2) if edge not in possible)
    assert all(five.core.response(source, *cap, *edge, K) == five.zero_matrix()
               for edge in forbidden)


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    assert parent["scope"]["all_zero_through_six_block_layers_closed"] is True

    additions = tuple(itertools.combinations(five.OFF_FAMILY, 7))
    assert len(additions) == 77520
    fixed_closed = []
    evaders = []
    for added in additions:
        certificate = five.fixed_cap_certificate(set(five.FAMILY) | set(added))
        if certificate is None:
            evaders.append(added)
        else:
            fixed_closed.append((added, certificate))
    assert len(fixed_closed) == 56240 and len(evaders) == 21280

    reduction_census = Counter()
    reduction_records = []
    stable = []
    for added in evaders:
        reduced, steps = five.guard_reduce(added)
        reduction_census[len(reduced)] += 1
        if len(reduced) == 7:
            assert not steps
            stable.append(added)
        else:
            assert len(reduced) <= 6 and steps
            reduction_records.append({
                "added": list(map(five.edge_string, added)),
                "steps": steps,
                "reduced": list(map(five.edge_string, reduced)),
                "inherited_layer": f"{len(reduced)}-block",
            })
    assert dict(sorted(reduction_census.items())) == {
        2: 54, 3: 1430, 4: 6454, 5: 8926, 6: 3926, 7: 490
    }
    assert len(reduction_records) == 20790 and len(stable) == 490

    stable_set = set(stable)
    seen = set()
    stable_orbits = []
    for representative in sorted(stable):
        if representative in seen:
            continue
        mate = five.permute_support(representative)
        assert mate in stable_set
        members = tuple(sorted({representative, mate}))
        seen.update(members)
        stable_orbits.append(members)
    assert len(stable_orbits) == 251
    assert Counter(map(len, stable_orbits)) == {2: 239, 1: 12}

    # Resolve all 16 exact zero/nonzero strata of the four variable family
    # blocks. Added blocks are nonzero by definition of the exact stratum.
    variable_order = tuple(sorted(five.VARIABLE))
    classification_records = []
    classifier_census = Counter()
    unresolved = []
    for added in stable:
        for mask in range(16):
            variables = frozenset(
                variable_order[index] for index in range(4) if mask & (1 << index)
            )
            support = set(five.FIXED) | set(variables) | set(added)
            fixed_certificate = five.fixed_cap_certificate(support)
            if fixed_certificate is not None:
                kind = "fixed_identity_cap"
                certificate = fixed_certificate
            else:
                certificates = nonidentity_certificates(support)
                if certificates:
                    kind = "nonidentity_cap_hyperplane_avoidance"
                    certificate = certificates[0]
                else:
                    kind = "unresolved_response_minor_locus"
                    certificate = None
            classifier_census[kind] += 1
            record = {
                "added": list(map(five.edge_string, added)),
                "nonzero_variable_blocks": list(map(five.edge_string, sorted(variables))),
                "classification": kind,
                "certificate": certificate,
            }
            classification_records.append(record)
            if kind == "unresolved_response_minor_locus":
                unresolved.append((added, variables))
    assert classifier_census == {
        "fixed_identity_cap": 6895,
        "nonidentity_cap_hyperplane_avoidance": 881,
        "unresolved_response_minor_locus": 64,
    }
    assert len(classification_records) == 7840 and len(unresolved) == 64

    unresolved_added = {added for added, _variables in unresolved}
    assert len(unresolved_added) == 20
    unresolved_variable_census = Counter(
        tuple(map(five.edge_string, sorted(variables)))
        for _added, variables in unresolved
    )
    assert unresolved_variable_census == {
        ("04", "35"): 20,
        ("04", "12", "35"): 20,
        ("04", "35", "67"): 12,
        ("04", "12", "35", "67"): 12,
    }

    unresolved_set = set(unresolved)
    unresolved_seen = set()
    unresolved_orbits = []
    for item in sorted(unresolved, key=lambda value: (value[0], sorted(value[1]))):
        if item in unresolved_seen:
            continue
        added, variables = item
        mate = (five.permute_support(added), permute_variables(variables))
        assert mate in unresolved_set
        members = tuple(sorted({item, mate}, key=lambda value: (value[0], sorted(value[1]))))
        unresolved_seen.update(members)
        unresolved_orbits.append(members)
    assert len(unresolved_orbits) == 32 and Counter(map(len, unresolved_orbits)) == {2: 32}

    unresolved_records = []
    for orbit_id, members in enumerate(unresolved_orbits):
        member_records = []
        for added, variables in members:
            support = set(five.FIXED) | set(variables) | set(added)
            assert five.fixed_cap_certificate(support) is None
            assert nonidentity_certificates(support) == []
            cap67_edges = five.response_edges(support, *five.CAP) if five.CAP in support else ()
            outside = tuple(sorted(set(added) & set(five.OUTSIDE_CAP_ADJACENT)))
            complete_rectangles = []
            for r in (3, 4, 5):
                rectangle = {(1, 7), (2, 6), tuple(sorted((r, 6))), tuple(sorted((r, 7)))}
                if rectangle <= support:
                    complete_rectangles.append(str(r))
            member_records.append({
                "added": list(map(five.edge_string, added)),
                "nonzero_variable_blocks": list(map(five.edge_string, sorted(variables))),
                "outside_cap67_added_edges": list(map(five.edge_string, outside)),
                "complete_outside_switched_rectangles": complete_rectangles,
                "cap67_response_edges": list(map(five.edge_string, cap67_edges)),
                "all_supported_carriers_fail_triangle_star": True,
                "next_exact_conditions": (
                    "rank(L_C)<=8 and each activity functional is nonzero on ker(L_C), "
                    "or formal-guard coefficient equations force a block zero"
                ),
            })
        unresolved_records.append({
            "orbit_id": orbit_id,
            "members": member_records,
        })

    # Full-family boundary: exactly twelve supports (six orbits) have all four
    # variable blocks nonzero and no structural carrier.
    full_variables = frozenset(five.VARIABLE)
    full_family_unresolved = tuple(added for added, variables in unresolved if variables == full_variables)
    assert len(full_family_unresolved) == 12

    # Exact literal replay of 257 distributed closed nonidentity strata.
    nonidentity_records = [
        record for record in classification_records
        if record["classification"] == "nonidentity_cap_hyperplane_avoidance"
    ]
    literal_records = []
    for sample in range(257):
        record = nonidentity_records[(sample * 347) % len(nonidentity_records)]
        added = tuple(tuple(map(int, edge)) for edge in record["added"])
        variables = frozenset(tuple(map(int, edge)) for edge in record["nonzero_variable_blocks"])
        source = {}
        for edge in five.FIXED:
            five.install_block(source, edge, five.identity_matrix())
        matrices = {
            edge: five.dense_matrix(41 + sample + 19 * index)
            for index, edge in enumerate(sorted(set(variables) | set(added)))
        }
        for edge, matrix in matrices.items():
            five.install_block(source, edge, matrix)
        certificate = record["certificate"]
        cap = tuple(map(int, certificate["cap"]))
        assert cap in matrices
        t, K, pairing = five.construct_active_K(matrices[cap])
        assert pairing != 0 and all(K[i][i] != 0 for i in five.core.COLORS)
        replay_nonidentity(source, certificate, K)
        literal_records.append({
            "sample": sample,
            "added": record["added"],
            "variables": record["nonzero_variable_blocks"],
            "cap": certificate["cap"],
            "carrier": certificate["carrier"],
            "t": t,
            "pairing": str(pairing),
        })

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_SUPPORT_BOUNDARY_V1",
        "status": "PASS_EXACT_SEVEN_BLOCK_CLASSIFICATION_WITH_64_FIRST_STRUCTURAL_EVADER_STRATA",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "five_source_sha256": FIVE_SOURCE_SHA256,
        "enumeration": {
            "seven_block_supports": len(additions),
            "fixed_identity_triangle_or_star_closed": len(fixed_closed),
            "fixed_identity_evaders": len(evaders),
            "guard_reduced_size_census": {str(k): v for k, v in sorted(reduction_census.items())},
            "guard_reduced_to_parent_at_most_six": len(reduction_records),
            "stable_seven_block_supports": len(stable),
            "stable_guard_symmetry_orbits": len(stable_orbits),
            "stable_orbit_size_census": {str(k): v for k, v in sorted(Counter(map(len, stable_orbits)).items())},
            "reduction_records_sha256": hashlib.sha256(
                json.dumps(reduction_records, sort_keys=True).encode()
            ).hexdigest(),
            "stable_supports_sha256": hashlib.sha256(
                json.dumps([list(map(five.edge_string, added)) for added in stable], sort_keys=True).encode()
            ).hexdigest(),
        },
        "exact_variable_stratum_classification": {
            "strata": len(classification_records),
            "census": dict(classifier_census),
            "classification_records_sha256": hashlib.sha256(
                json.dumps(classification_records, sort_keys=True).encode()
            ).hexdigest(),
            "closed_strata": 7776,
            "unresolved_structural_strata": len(unresolved),
            "unresolved_added_supports": len(unresolved_added),
            "unresolved_guard_symmetry_orbits": len(unresolved_orbits),
            "unresolved_orbit_records": unresolved_records,
            "unresolved_variable_subset_census": {
                ",".join(key): value for key, value in sorted(unresolved_variable_census.items())
            },
            "full_family_nonzero_unresolved_supports": len(full_family_unresolved),
            "full_family_nonzero_unresolved_orbits": 6,
        },
        "general_lemmas": {
            "no_outside_edge": (
                "absence of all edges from cap sites 6,7 to outside sites 3,4,5 "
                "forces every cap67 response outside triangle012 to vanish for all K"
            ),
            "switched_rectangle": (
                "a guard-stable nonzero outside pair A_r6,A_r7 requires both A17 and A26; "
                "otherwise a rank-nine injection forces one outside block to zero"
            ),
            "induction_verdict": (
                "the structural triangle/star induction closes through six blocks but stops "
                "at seven on 64 exact variable strata"
            ),
        },
        "literal_replay": {
            "samples": len(literal_records),
            "closed_nonidentity_strata_distributed": True,
            "active_K_constructed": True,
            "forbidden_responses_replayed": True,
            "records_sha256": hashlib.sha256(
                json.dumps(literal_records, sort_keys=True).encode()
            ).hexdigest(),
        },
        "scope": {
            "all_seven_block_supports_classified": True,
            "all_seven_block_strata_closed": False,
            "closed_seven_block_stable_strata": 7776,
            "unresolved_seven_block_structural_strata": 64,
            "first_full_family_structural_evader_supports": 12,
            "zero_through_six_layers_closed": True,
            "full_support_dichotomy": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_seven_block_support_boundary.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_seven_block_support_boundary.json")
    print(json.dumps({
        "status": result["status"],
        "supports": len(additions),
        "fixed_closed": len(fixed_closed),
        "guard_reduced": len(reduction_records),
        "stable": len(stable),
        "stratum_census": dict(classifier_census),
        "unresolved_orbits": len(unresolved_orbits),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
