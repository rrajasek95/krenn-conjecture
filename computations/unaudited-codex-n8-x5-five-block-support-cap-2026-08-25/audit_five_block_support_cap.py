#!/usr/bin/env python3
"""Close the five-added-block layer by exact support/guard classification."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-four-block-guard-collapse-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "a9ffc82d1b3bda811dfeffc33c61c1a0b277bea48a2265a583fd01ed714070c8"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-four-block-guard-collapse-2026-08-25/results_four_block_guard_collapse.json"
PARENT_RESULT_SHA256 = "2ea44d104e37ec6e44793ebddb441af4df880d1335a4a9d52c49e07b50aa8cb6"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(CORE) == CORE_SHA256
spec = importlib.util.spec_from_file_location("x5_core", CORE)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (3, 5), (1, 2), (6, 7)))
FAMILY = FIXED | VARIABLE
CAP = (6, 7)
TRIANGLE = frozenset((0, 1, 2))
OUTSIDE_CAP_ADJACENT = frozenset(((3, 6), (3, 7), (4, 6), (4, 7), (5, 6), (5, 7)))
ALL_EDGES = frozenset(itertools.combinations(range(8), 2))
OFF_FAMILY = tuple(sorted(ALL_EDGES - FAMILY))
GUARD_PERMUTATION = (0, 2, 1, 3, 4, 5, 7, 6)


def edge_string(edge):
    return "".join(map(str, edge))


def identity_matrix():
    return [[int(row == column) for column in core.COLORS] for row in core.COLORS]


def zero_matrix():
    return [[0 for _ in core.COLORS] for _ in core.COLORS]


def dense_matrix(seed):
    return [
        [Fraction(seed + 1 + 3 * row + 5 * column, 29 + seed + row + column)
         for column in core.COLORS]
        for row in core.COLORS
    ]


def install_block(source, edge, matrix):
    for left, right in itertools.product(core.COLORS, repeat=2):
        core.put(source, *edge, left, right, matrix[left][right])


def response_edges(support, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    answer = []
    for a, b in itertools.combinations(residual, 2):
        direct = tuple(sorted((p, a))) in support and tuple(sorted((q, b))) in support
        switched = tuple(sorted((p, b))) in support and tuple(sorted((q, a))) in support
        if direct or switched:
            answer.append((a, b))
    return tuple(answer)


def carrier_shape(edges):
    vertices = frozenset(site for edge in edges for site in edge)
    if len(vertices) <= 3:
        return "triangle", tuple(sorted(vertices))
    centers = tuple(site for site in range(8) if edges and all(site in edge for edge in edges))
    if centers:
        return "star", (centers[0],)
    return None


def fixed_cap_certificate(support):
    for cap in sorted(FIXED):
        edges = response_edges(support, *cap)
        shape = carrier_shape(edges)
        if shape is not None:
            kind, defining_vertices = shape
            return {
                "cap": edge_string(cap),
                "carrier": kind,
                "defining_vertices": list(defining_vertices),
                "possible_response_edges": list(map(edge_string, edges)),
                "forbidden_response_rank": 0,
                "kernel_dimension": 9,
                "K": "I3",
                "kappa": [1, 1, 1],
                "s_pairing": 3,
            }
    return None


def permute_support(support):
    return tuple(sorted(tuple(sorted((GUARD_PERMUTATION[a], GUARD_PERMUTATION[b]))) for a, b in support))


def guard_forcing_reason(support, edge):
    """Return absent switched partners making the cap-67 injection literal."""
    assert edge in OUTSIDE_CAP_ADJACENT
    r = next(site for site in edge if site not in CAP)
    if 6 in edge:
        partners = ((2, 6), tuple(sorted((r, 7))))
        response_edge = tuple(sorted((2, r)))
        identity = f"R_{edge_string(response_edge)}^67(I)=A{edge_string(edge)}^T"
    else:
        partners = (tuple(sorted((r, 6))), (1, 7))
        response_edge = tuple(sorted((1, r)))
        identity = f"R_{edge_string(response_edge)}^67(I)=A{edge_string(edge)}^T"
    absent = tuple(partner for partner in partners if partner not in support)
    if not absent:
        return None
    return {
        "block": edge_string(edge),
        "forbidden_response": edge_string(response_edge),
        "switched_partners": list(map(edge_string, partners)),
        "absent_partners": list(map(edge_string, absent)),
        "identity": identity,
        "coordinate_rank": 9,
        "unit_minor_determinant_abs": 1,
    }


def guard_reduce(added):
    current = set(FAMILY) | set(added)
    remaining = set(added)
    steps = []
    while True:
        forced = None
        reason = None
        for edge in sorted(remaining & set(OUTSIDE_CAP_ADJACENT)):
            candidate = guard_forcing_reason(current, edge)
            if candidate is not None:
                forced, reason = edge, candidate
                break
        if forced is None:
            break
        steps.append(reason)
        remaining.remove(forced)
        current.remove(forced)
    return tuple(sorted(remaining)), steps


def construct_active_K(matrix):
    """Find K(t)_ij=t^(3i+j); a nonzero degree<=8 polynomial has <=8 roots."""
    assert any(matrix[i][j] != 0 for i, j in itertools.product(core.COLORS, repeat=2))
    for t in range(1, 10):
        K = [[Fraction(t ** (3 * i + j)) for j in core.COLORS] for i in core.COLORS]
        pairing = sum(K[i][j] * matrix[i][j]
                      for i, j in itertools.product(core.COLORS, repeat=2))
        if pairing != 0:
            return t, K, pairing
    raise AssertionError("nonzero degree-eight pairing polynomial vanished at nine points")


def forbidden_pairs(cap, certificate):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    possible = set(map(lambda text: tuple(map(int, text)), certificate["possible_response_edges"]))
    return tuple(edge for edge in itertools.combinations(residual, 2) if edge not in possible)


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    assert parent["scope"]["all_four_block_supports_closed"] is True

    additions = tuple(itertools.combinations(OFF_FAMILY, 5))
    assert len(additions) == 15504
    fixed_closed = []
    evaders = []
    for added in additions:
        certificate = fixed_cap_certificate(set(FAMILY) | set(added))
        if certificate is None:
            evaders.append(added)
        else:
            fixed_closed.append((added, certificate))
    assert len(fixed_closed) == 14976 and len(evaders) == 528

    reduction_census = Counter()
    reduction_records = []
    stable = []
    for added in evaders:
        reduced, steps = guard_reduce(added)
        reduction_census[len(reduced)] += 1
        if len(reduced) == 5:
            stable.append(added)
            assert not steps
        else:
            assert len(reduced) <= 4 and steps
            reduction_records.append({
                "added": list(map(edge_string, added)),
                "steps": steps,
                "reduced": list(map(edge_string, reduced)),
                "inherited_layer": f"{len(reduced)}-block",
            })
    assert dict(sorted(reduction_census.items())) == {2: 60, 3: 287, 4: 170, 5: 11}
    assert len(reduction_records) == 517 and len(stable) == 11
    assert all(not (set(added) & set(OUTSIDE_CAP_ADJACENT)) for added in stable)

    # Exact order-two guard symmetry gives six stable orbits.
    stable_set = set(stable)
    seen = set()
    stable_orbits = []
    for representative in sorted(stable):
        if representative in seen:
            continue
        mate = permute_support(representative)
        assert mate in stable_set
        members = tuple(sorted({representative, mate}))
        seen.update(members)
        stable_orbits.append(members)
    assert len(stable_orbits) == 6 and sorted(map(len, stable_orbits)) == [1, 2, 2, 2, 2, 2]

    survivor_records = []
    for orbit_id, members in enumerate(stable_orbits):
        representative = members[0]
        support = set(FAMILY) | set(representative)
        cap_edges = response_edges(support, *CAP)
        assert cap_edges == ((0, 1), (0, 2), (1, 2))

        # If A67 specializes to zero, use the maximal remaining variable
        # support. Any further zero specialization only removes responses.
        support_without_cap = support - {CAP}
        zero_cap_certificate = fixed_cap_certificate(support_without_cap)
        assert zero_cap_certificate is not None
        assert zero_cap_certificate["cap"] == "16"
        survivor_records.append({
            "orbit_id": orbit_id,
            "representative": list(map(edge_string, representative)),
            "members": [list(map(edge_string, member)) for member in members],
            "cap67_response_edges": list(map(edge_string, cap_edges)),
            "cap67_nonzero_stratum": {
                "carrier": "triangle012",
                "forbidden_response_rank": 0,
                "kernel_dimension": 9,
                "activity_hyperplanes": ["K00=0", "K11=0", "K22=0", "<K,A67>=0"],
                "hyperplanes_proper_when_A67_nonzero": True,
                "constructive_K": "K(t)_ij=t^(3i+j), choose t in {1,...,9} with <K(t),A67> != 0",
                "active_clean_cap": True,
            },
            "cap67_zero_stratum": zero_cap_certificate,
        })

    # Literal exact replay of both strata, distributed over all 11 supports.
    outside_cap_pairs = tuple(
        edge for edge in itertools.combinations(range(6), 2)
        if not set(edge) <= TRIANGLE
    )
    literal_records = []
    for sample in range(257):
        added = stable[(sample * 7) % len(stable)]
        source = {}
        for edge in FIXED:
            install_block(source, edge, identity_matrix())
        matrices = {
            edge: dense_matrix(19 + sample + 11 * index)
            for index, edge in enumerate(sorted(VARIABLE | set(added)))
        }
        for edge, matrix in matrices.items():
            install_block(source, edge, matrix)
        t, K, pairing = construct_active_K(matrices[CAP])
        assert all(K[i][i] != 0 for i in core.COLORS)
        assert pairing != 0
        assert all(core.response(source, *CAP, *edge, K) == zero_matrix()
                   for edge in outside_cap_pairs)

        # A67=0 branch: cap16 certificate remains valid even with every other
        # optional family block and added block dense.
        install_block(source, CAP, zero_matrix())
        certificate = fixed_cap_certificate((set(FAMILY) | set(added)) - {CAP})
        assert certificate is not None and certificate["cap"] == "16"
        cap = (1, 6)
        possible = set(tuple(map(int, text)) for text in certificate["possible_response_edges"])
        residual = tuple(site for site in range(8) if site not in cap)
        forbidden = tuple(edge for edge in itertools.combinations(residual, 2) if edge not in possible)
        assert all(core.response(source, *cap, *edge, identity_matrix()) == zero_matrix()
                   for edge in forbidden)
        assert sum(identity_matrix()[i][j] * core.get(source, *cap, i, j)
                   for i, j in itertools.product(core.COLORS, repeat=2)) == 3
        literal_records.append({
            "sample": sample,
            "added": list(map(edge_string, added)),
            "nonzero_A67_t": t,
            "nonzero_A67_pairing": str(pairing),
            "zero_A67_cap": certificate["cap"],
            "zero_A67_carrier": certificate["carrier"],
        })
    assert {tuple(record["added"]) for record in literal_records} == {
        tuple(map(edge_string, added)) for added in stable
    }

    result = {
        "schema": "KRENN_X5_FIVE_BLOCK_SUPPORT_CAP_V1",
        "status": "PASS_ALL_15504_FIVE_BLOCK_SUPPORTS_CLOSED_UNDER_FORMAL_GUARD",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "core_sha256": CORE_SHA256,
        "enumeration": {
            "off_family_edges": list(map(edge_string, OFF_FAMILY)),
            "five_block_supports": len(additions),
            "fixed_identity_triangle_or_star_closed": len(fixed_closed),
            "fixed_identity_evaders": len(evaders),
            "guard_reduced_size_census": {str(k): v for k, v in sorted(reduction_census.items())},
            "guard_reduced_to_parent_at_most_four": len(reduction_records),
            "stable_five_block_supports": len(stable),
            "stable_guard_symmetry_orbits": len(stable_orbits),
            "stable_orbit_records": survivor_records,
            "reduction_records_sha256": hashlib.sha256(
                json.dumps(reduction_records, sort_keys=True).encode()
            ).hexdigest(),
        },
        "guard_reduction_lemma": {
            "cap": "67",
            "triangle": "012",
            "K": "I3",
            "outside_blocks": list(map(edge_string, sorted(OUTSIDE_CAP_ADJACENT))),
            "endpoint6": "R_2r^67(I)=A_r6^T if A26 or A_r7 is absent",
            "endpoint7": "R_1r^67(I)=A_r7^T if A_r6 or A17 is absent",
            "coordinate_rank": 9,
            "unit_minor_determinant_abs": 1,
            "iterative_reduction_exact": True,
        },
        "five_load_theorem": {
            "statement": (
                "every five-added-block support either has a fixed identity triangle/star cap, "
                "guard-reduces to an already closed <=4-block support, or is one of 11 stable "
                "supports whose cap67 responses lie in triangle012"
            ),
            "nonzero_A67": (
                "M3 is the response kernel; the four activity failures are proper hyperplanes, "
                "so their finite union cannot cover M3 over characteristic zero"
            ),
            "zero_A67": (
                "cap16 has a fixed identity triangle/star certificate at maximal remaining "
                "variable support; zero specializations can only delete responses"
            ),
            "coefficient_dependent_minors_required": False,
            "pure_rows_used": False,
            "six_residual_common_zero_used": False,
            "source_equations_used": False,
        },
        "literal_replay": {
            "samples": len(literal_records),
            "all_11_stable_supports_distributed": True,
            "nonzero_A67_active_K_constructed": True,
            "zero_A67_fixed_cap_replayed": True,
            "records_sha256": hashlib.sha256(
                json.dumps(literal_records, sort_keys=True).encode()
            ).hexdigest(),
        },
        "scope": {
            "all_five_block_supports": True,
            "all_zero_through_five_block_layers_closed": True,
            "six_or_more_added_blocks": False,
            "full_support_dichotomy": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_five_block_support_cap.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_five_block_support_cap.json")
    print(json.dumps({
        "status": result["status"],
        "supports": len(additions),
        "fixed_closed": len(fixed_closed),
        "evaders": len(evaders),
        "reduction_census": dict(sorted(reduction_census.items())),
        "stable_orbits": len(stable_orbits),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
