#!/usr/bin/env python3
"""Exact fixed-cap/guard/nonidentity-cap closure of six added blocks."""

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
PARENT = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "119ec632645202f973c89c3381e85113a902c4066e627ba7c6d051fa729d49fb"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/results_five_block_support_cap.json"
PARENT_RESULT_SHA256 = "3d4882eb2d7f0687125ec5a22ec95ca9325cf31df9d3d572760c3e23b2c4fe57"
PARENT_SOURCE = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/audit_five_block_support_cap.py"
PARENT_SOURCE_SHA256 = "4a686fe5bbf80559283d993245166764d5b52d8b4bd33b144017f26f5f2c1f45"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(PARENT_SOURCE) == PARENT_SOURCE_SHA256
spec = importlib.util.spec_from_file_location("five_block", PARENT_SOURCE)
assert spec is not None and spec.loader is not None
five = importlib.util.module_from_spec(spec)
spec.loader.exec_module(five)


def active_cap_replay(source, cap, certificate, K):
    possible = {tuple(map(int, text)) for text in certificate["possible_response_edges"]}
    residual = tuple(site for site in range(8) if site not in cap)
    forbidden = tuple(edge for edge in itertools.combinations(residual, 2) if edge not in possible)
    assert all(five.core.response(source, *cap, *edge, K) == five.zero_matrix()
               for edge in forbidden)


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    assert parent["scope"]["all_zero_through_five_block_layers_closed"] is True

    additions = tuple(itertools.combinations(five.OFF_FAMILY, 6))
    assert len(additions) == 38760
    fixed_closed = []
    evaders = []
    for added in additions:
        certificate = five.fixed_cap_certificate(set(five.FAMILY) | set(added))
        if certificate is None:
            evaders.append(added)
        else:
            fixed_closed.append((added, certificate))
    assert len(fixed_closed) == 34124 and len(evaders) == 4636

    reduction_census = Counter()
    reduction_records = []
    stable = []
    for added in evaders:
        reduced, steps = five.guard_reduce(added)
        reduction_census[len(reduced)] += 1
        if len(reduced) == 6:
            assert not steps
            stable.append(added)
        else:
            assert len(reduced) <= 5 and steps
            reduction_records.append({
                "added": list(map(five.edge_string, added)),
                "steps": steps,
                "reduced": list(map(five.edge_string, reduced)),
                "inherited_layer": f"{len(reduced)}-block",
            })
    assert dict(sorted(reduction_census.items())) == {2: 96, 3: 1080, 4: 2244, 5: 1104, 6: 112}
    assert len(reduction_records) == 4524 and len(stable) == 112

    # General support lemma: any response of cap67 outside triangle012 uses
    # at least one edge joining {6,7} to {3,4,5}.  The finite m=6 boundary
    # classification shows no stable fixed-cap evader contains such an edge.
    assert all(not (set(added) & set(five.OUTSIDE_CAP_ADJACENT)) for added in stable)
    for added in stable:
        assert set(five.response_edges(set(five.FAMILY) | set(added), *five.CAP)) <= {
            (0, 1), (0, 2), (1, 2)
        }

    stable_set = set(stable)
    seen = set()
    orbits = []
    for representative in sorted(stable):
        if representative in seen:
            continue
        mate = five.permute_support(representative)
        assert mate in stable_set
        members = tuple(sorted({representative, mate}))
        seen.update(members)
        orbits.append(members)
    assert len(orbits) == 57
    assert Counter(map(len, orbits)) == {2: 55, 1: 2}

    orbit_records = []
    zero_cap_census = Counter()
    for orbit_id, members in enumerate(orbits):
        representative = members[0]
        support = set(five.FAMILY) | set(representative)
        cap_edges = five.response_edges(support, *five.CAP)
        assert set(cap_edges) <= {(0, 1), (0, 2), (1, 2)}
        zero_strata = []
        for member in members:
            member_support = set(five.FAMILY) | set(member)
            member_cap_edges = five.response_edges(member_support, *five.CAP)
            assert set(member_cap_edges) <= {(0, 1), (0, 2), (1, 2)}
            zero_certificate = five.fixed_cap_certificate(member_support - {five.CAP})
            assert zero_certificate is not None
            zero_cap_census[(zero_certificate["cap"], zero_certificate["carrier"])] += 1
            zero_strata.append({
                "member": list(map(five.edge_string, member)),
                "certificate": zero_certificate,
            })
        orbit_records.append({
            "orbit_id": orbit_id,
            "representative": list(map(five.edge_string, representative)),
            "members": [list(map(five.edge_string, member)) for member in members],
            "outside_cap67_added_edges": [],
            "cap67_response_edges": list(map(five.edge_string, cap_edges)),
            "cap67_nonzero_stratum": {
                "forbidden_response_rank": 0,
                "kernel_dimension": 9,
                "activity_hyperplanes": ["K00=0", "K11=0", "K22=0", "<K,A67>=0"],
                "constructive_K": "K(t)_ij=t^(3i+j), some t in {1,...,9}",
                "active_clean_cap": True,
            },
            "cap67_zero_strata": zero_strata,
        })
    assert zero_cap_census == {("16", "star"): 60, ("16", "triangle"): 48, ("27", "star"): 4}

    outside_cap_pairs = tuple(
        edge for edge in itertools.combinations(range(6), 2)
        if not set(edge) <= five.TRIANGLE
    )
    literal_records = []
    for sample in range(257):
        added = stable[(sample * 43) % len(stable)]
        source = {}
        for edge in five.FIXED:
            five.install_block(source, edge, five.identity_matrix())
        matrices = {
            edge: five.dense_matrix(31 + sample + 17 * index)
            for index, edge in enumerate(sorted(five.VARIABLE | set(added)))
        }
        for edge, matrix in matrices.items():
            five.install_block(source, edge, matrix)

        t, K, pairing = five.construct_active_K(matrices[five.CAP])
        assert pairing != 0 and all(K[i][i] != 0 for i in five.core.COLORS)
        assert all(five.core.response(source, *five.CAP, *edge, K) == five.zero_matrix()
                   for edge in outside_cap_pairs)

        five.install_block(source, five.CAP, five.zero_matrix())
        certificate = five.fixed_cap_certificate((set(five.FAMILY) | set(added)) - {five.CAP})
        assert certificate is not None
        cap = tuple(map(int, certificate["cap"]))
        active_cap_replay(source, cap, certificate, five.identity_matrix())
        assert sum(five.identity_matrix()[i][j] * five.core.get(source, *cap, i, j)
                   for i, j in itertools.product(five.core.COLORS, repeat=2)) == 3
        literal_records.append({
            "sample": sample,
            "added": list(map(five.edge_string, added)),
            "nonzero_A67_t": t,
            "nonzero_A67_pairing": str(pairing),
            "zero_A67_cap": certificate["cap"],
            "zero_A67_carrier": certificate["carrier"],
        })
    assert {tuple(record["added"]) for record in literal_records} == {
        tuple(map(five.edge_string, added)) for added in stable
    }

    result = {
        "schema": "KRENN_X5_SIX_BLOCK_SUPPORT_CAP_V1",
        "status": "PASS_ALL_38760_SIX_BLOCK_SUPPORTS_CLOSED_UNDER_FORMAL_GUARD",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "parent_source_sha256": PARENT_SOURCE_SHA256,
        "enumeration": {
            "six_block_supports": len(additions),
            "fixed_identity_triangle_or_star_closed": len(fixed_closed),
            "fixed_identity_evaders": len(evaders),
            "guard_reduced_size_census": {str(k): v for k, v in sorted(reduction_census.items())},
            "guard_reduced_to_parent_at_most_five": len(reduction_records),
            "stable_six_block_supports": len(stable),
            "stable_guard_symmetry_orbits": len(orbits),
            "orbit_size_census": {str(k): v for k, v in sorted(Counter(map(len, orbits)).items())},
            "zero_A67_fixed_cap_census": {
                f"{cap}_{carrier}": count
                for (cap, carrier), count in sorted(zero_cap_census.items())
            },
            "stable_orbit_records": orbit_records,
            "reduction_records_sha256": hashlib.sha256(
                json.dumps(reduction_records, sort_keys=True).encode()
            ).hexdigest(),
        },
        "general_no_outside_edge_criterion": {
            "statement": (
                "if no supported edge joins cap site 6 or 7 to an outside site 3,4,5, "
                "then every cap67 response outside triangle012 is identically zero for all K"
            ),
            "proof": (
                "each cap67 response monomial on residual pair ab uses one 6-edge and one "
                "7-edge; if ab is not contained in 012, at least one is outside-cap-adjacent"
            ),
            "valid_for_any_number_of_added_blocks": True,
            "all_112_stable_six_block_evaders_satisfy": True,
        },
        "six_load_theorem": {
            "statement": (
                "every six-added-block support has a fixed identity triangle/star cap, "
                "guard-reduces to a closed <=5 support, or satisfies the general no-outside-edge criterion"
            ),
            "A67_nonzero": "cap67 active by avoidance of four proper hyperplanes in its 9-dimensional kernel",
            "A67_zero": "a fixed identity cap16 or cap27 triangle/star certificate is active",
            "coefficient_dependent_minors_required": False,
            "pure_rows_used": False,
            "six_residual_common_zero_used": False,
            "source_equations_used": False,
        },
        "literal_replay": {
            "samples": len(literal_records),
            "all_112_stable_supports_distributed": True,
            "nonzero_A67_active_K_constructed": True,
            "zero_A67_fixed_caps_replayed": True,
            "records_sha256": hashlib.sha256(
                json.dumps(literal_records, sort_keys=True).encode()
            ).hexdigest(),
        },
        "scope": {
            "all_six_block_supports": True,
            "all_zero_through_six_block_layers_closed": True,
            "seven_or_more_added_blocks": False,
            "full_support_dichotomy": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_six_block_support_cap.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_six_block_support_cap.json")
    print(json.dumps({
        "status": result["status"],
        "supports": len(additions),
        "fixed_closed": len(fixed_closed),
        "evaders": len(evaders),
        "reduction_census": dict(sorted(reduction_census.items())),
        "stable_orbits": len(orbits),
        "zero_cap_census": {
            f"{cap}_{carrier}": count
            for (cap, carrier), count in sorted(zero_cap_census.items())
        },
    }, sort_keys=True))


if __name__ == "__main__":
    main()
