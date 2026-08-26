#!/usr/bin/env python3
"""Exact guard collapse of the 24 first four-block structural evaders."""

from __future__ import annotations

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
PARENT = HERE.parent / "unaudited-codex-n8-x5-three-block-support-cap-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "34511eaf230805dec2c75a7babc3d6a3ff4c42b63e178adec298417a3e8f998e"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-three-block-support-cap-2026-08-25/results_three_block_support_cap.json"
PARENT_RESULT_SHA256 = "1eefe005739b12321e1d5871c5c11c2fa16b21b6555e426e71b031e04734b193"
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
TRIANGLE = frozenset((0, 1, 2))
OUTSIDE_CAP_ADJACENT = frozenset(((3, 6), (3, 7), (4, 6), (4, 7), (5, 6), (5, 7)))
VARIABLE_NAMES = {(0, 4): "X", (3, 5): "Y", (1, 2): "U", (6, 7): "V"}
RESIDUAL_SITE_COLOUR = ("a", "b", "b", "a", "a", "a", "b", "b")


def edge_string(edge):
    return "".join(map(str, edge))


def parse_edge(text):
    return tuple(map(int, text))


def identity_matrix():
    return [[int(row == column) for column in core.COLORS] for row in core.COLORS]


def zero_matrix():
    return [[0 for _ in core.COLORS] for _ in core.COLORS]


def dense_matrix(seed):
    return [
        [Fraction(seed + 1 + 3 * row + 5 * column, 23 + seed + row + column)
         for column in core.COLORS]
        for row in core.COLORS
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def install_block(source, edge, matrix):
    for left, right in itertools.product(core.COLORS, repeat=2):
        core.put(source, *edge, left, right, matrix[left][right])


def neighbours(support, vertex):
    return {
        other for edge in support if vertex in edge
        for other in edge if other != vertex
    }


def response_edges(support, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    answer = []
    for a, b in itertools.combinations(residual, 2):
        direct = tuple(sorted((p, a))) in support and tuple(sorted((q, b))) in support
        switched = tuple(sorted((p, b))) in support and tuple(sorted((q, a))) in support
        if direct or switched:
            answer.append((a, b))
    return tuple(answer)


def fixed_cap_certificate(support):
    for p, q in sorted(FIXED):
        residual = tuple(site for site in range(8) if site not in (p, q))
        edges = response_edges(support, p, q)
        vertices = {site for edge in edges for site in edge}
        if len(vertices) <= 3:
            triangle = list(sorted(vertices))
            triangle.extend(site for site in residual if site not in vertices and len(triangle) < 3)
            return {
                "cap": edge_string((p, q)),
                "triangle": "".join(map(str, triangle)),
                "possible_response_edges": list(map(edge_string, edges)),
                "forbidden_response_rank": 0,
                "kernel_dimension": 9,
                "K": "I3",
                "kappa": [1, 1, 1],
                "s_pairing": 3,
            }
    raise AssertionError("reduced support missing inherited fixed cap")


def forced_response_edge(edge):
    r = next(site for site in edge if site not in (6, 7))
    if 6 in edge:
        return tuple(sorted((2, r)))
    assert 7 in edge
    return tuple(sorted((1, r)))


def injection_guard(source_support, edge):
    r = next(site for site in edge if site not in (6, 7))
    response_edge = forced_response_edge(edge)
    assert not set(response_edge) <= TRIANGLE
    if 6 in edge:
        # R_{2r}: the switched term would require A26 and A7r.
        absent_partner_edges = ((2, 6), tuple(sorted((7, r))))
    else:
        # R_{1r}: the switched term would require A6r and A17.
        absent_partner_edges = (tuple(sorted((6, r))), (1, 7))
    assert any(partner not in source_support for partner in absent_partner_edges)

    # Literal basis map is a coordinate permutation Z -> Z^T, hence has a
    # unit 9x9 minor and rank nine.
    mapping = []
    for left, right in itertools.product(core.COLORS, repeat=2):
        source = {}
        for fixed in FIXED:
            install_block(source, fixed, identity_matrix())
        basis = zero_matrix()
        basis[left][right] = 1
        install_block(source, edge, basis)
        response = core.response(source, 6, 7, *response_edge, identity_matrix())
        assert response == transpose(basis)
        output = next((i, j) for i, j in itertools.product(core.COLORS, repeat=2)
                      if response[i][j] == 1)
        assert sum(abs(response[i][j]) for i, j in itertools.product(core.COLORS, repeat=2)) == 1
        mapping.append({"input": [left, right], "output": list(output), "coefficient": 1})
    assert len({tuple(item["output"]) for item in mapping}) == 9
    return {
        "block": edge_string(edge),
        "forbidden_response": edge_string(response_edge),
        "identity": f"R_{edge_string(response_edge)}^67(I)=A{edge_string(edge)}^T",
        "coordinate_map_rank": 9,
        "unit_minor_determinant_abs": 1,
        "zero_locus": f"A{edge_string(edge)}=0",
        "basis_mapping": mapping,
    }


def term_string(matching, names):
    factors = []
    for edge in matching:
        left_colour = RESIDUAL_SITE_COLOUR[edge[0]]
        right_colour = RESIDUAL_SITE_COLOUR[edge[1]]
        if edge in FIXED:
            assert left_colour == right_colour
            continue
        name = VARIABLE_NAMES.get(edge, names.get(edge))
        assert name is not None
        factors.append(f"{name}[{left_colour},{right_colour}]")
    return "1" if not factors else "*".join(factors)


def residual_formula(added):
    support = set(FAMILY) | set(added)
    names = {edge: f"Z{index}" for index, edge in enumerate(sorted(added))}
    new_matchings = tuple(
        matching for matching in core.PM8
        if set(matching) <= support and not set(matching) <= set(FAMILY)
    )
    terms = [term_string(matching, names) for matching in new_matchings]
    return {
        "formula": "P_a*Q_b" + (" + " + " + ".join(terms) if terms else ""),
        "new_matchings": [core.matching_string(matching) for matching in new_matchings],
        "block_names": {edge_string(edge): name for edge, name in names.items()},
    }


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    parent_orbits = parent["sharp_four_block_boundary_diagnostic"]["orbit_records"]
    assert len(parent_orbits) == 12
    supports = {
        tuple(sorted(parse_edge(edge) for edge in member))
        for orbit in parent_orbits for member in orbit["members"]
    }
    assert len(supports) == 24

    orbit_records = []
    support_records = []
    reduced_size_census = {}
    for orbit in parent_orbits:
        representative = tuple(sorted(parse_edge(edge) for edge in orbit["representative"]))
        forced = tuple(sorted(set(representative) & set(OUTSIDE_CAP_ADJACENT)))
        assert len(forced) in (1, 2)
        injections = [injection_guard(set(FAMILY) | set(representative), edge) for edge in forced]
        reduced = tuple(edge for edge in representative if edge not in forced)
        assert len(reduced) in (2, 3)
        reduced_certificate = fixed_cap_certificate(set(FAMILY) | set(reduced))
        before_formula = residual_formula(representative)
        after_formula = residual_formula(reduced)
        assert all(any(edge in matching for edge in forced)
                   for matching in core.PM8
                   if set(matching) <= set(FAMILY) | set(representative)
                   and not set(matching) <= set(FAMILY) | set(reduced))
        reduced_size_census[str(len(reduced))] = reduced_size_census.get(str(len(reduced)), 0) + 1
        orbit_records.append({
            "orbit_id": orbit["orbit_id"],
            "representative": list(map(edge_string, representative)),
            "members": orbit["members"],
            "forced_zero_blocks": list(map(edge_string, forced)),
            "guard_injections": injections,
            "residual_before_guard": before_formula,
            "reduced_support": list(map(edge_string, reduced)),
            "residual_after_guard": after_formula,
            "inherited_active_cap": reduced_certificate,
            "inherited_layer": f"{len(reduced)}-block theorem",
            "formal_guard_stratum_nonempty_with_all_four_blocks_nonzero": False,
        })

        for member_text in orbit["members"]:
            member = tuple(sorted(parse_edge(edge) for edge in member_text))
            member_forced = tuple(sorted(set(member) & set(OUTSIDE_CAP_ADJACENT)))
            member_reduced = tuple(edge for edge in member if edge not in member_forced)
            member_injections = [injection_guard(set(FAMILY) | set(member), edge) for edge in member_forced]
            support_records.append({
                "added": list(map(edge_string, member)),
                "forced_zero_blocks": list(map(edge_string, member_forced)),
                "guard_injections": member_injections,
                "reduced_support": list(map(edge_string, member_reduced)),
                "reduced_size": len(member_reduced),
                "inherited_active_cap": fixed_cap_certificate(set(FAMILY) | set(member_reduced)),
            })
    assert len(orbit_records) == 12 and len(support_records) == 24
    assert reduced_size_census == {"2": 6, "3": 6}
    assert sum(record["reduced_size"] == 2 for record in support_records) == 12
    assert sum(record["reduced_size"] == 3 for record in support_records) == 12

    # Exact distributed rational replay of both the injection before imposing
    # the guard and the inherited active cap after its forced zero blocks.
    replay_records = []
    ordered_supports = sorted(supports)
    outside_pairs = tuple(
        edge for edge in itertools.combinations(range(6), 2)
        if not set(edge) <= TRIANGLE
    )
    for sample in range(257):
        added = ordered_supports[(sample * 11) % len(ordered_supports)]
        forced = tuple(sorted(set(added) & set(OUTSIDE_CAP_ADJACENT)))
        matrices = {
            edge: dense_matrix(17 + sample + 13 * index)
            for index, edge in enumerate(sorted(VARIABLE | set(added)))
        }
        source = {}
        for edge in FIXED:
            install_block(source, edge, identity_matrix())
        for edge, matrix in matrices.items():
            install_block(source, edge, matrix)
        for edge in forced:
            response = core.response(source, 6, 7, *forced_response_edge(edge), identity_matrix())
            assert response == transpose(matrices[edge])

        for edge in forced:
            install_block(source, edge, zero_matrix())
        assert all(core.response(source, 6, 7, *edge, identity_matrix()) == zero_matrix()
                   for edge in outside_pairs)
        reduced = tuple(edge for edge in added if edge not in forced)
        certificate = fixed_cap_certificate(set(FAMILY) | set(reduced))
        p, q = parse_edge(certificate["cap"])
        triangle = frozenset(map(int, certificate["triangle"]))
        residual = tuple(site for site in range(8) if site not in (p, q))
        forbidden = tuple(
            edge for edge in itertools.combinations(residual, 2)
            if not set(edge) <= triangle
        )
        assert all(core.response(source, p, q, *edge, identity_matrix()) == zero_matrix()
                   for edge in forbidden)
        assert sum(identity_matrix()[i][j] * core.get(source, p, q, i, j)
                   for i, j in itertools.product(core.COLORS, repeat=2)) == 3
        replay_records.append({
            "sample": sample,
            "added": list(map(edge_string, added)),
            "forced": list(map(edge_string, forced)),
            "reduced": list(map(edge_string, reduced)),
            "cap": certificate["cap"],
            "triangle": certificate["triangle"],
        })

    result = {
        "schema": "KRENN_X5_FOUR_BLOCK_GUARD_COLLAPSE_V1",
        "status": "PASS_ALL_24_STRUCTURAL_EVADERS_FORCED_TO_CLOSED_LOWER_SUPPORT",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "core_sha256": CORE_SHA256,
        "formal_guard": {
            "cap": "67",
            "triangle": "012",
            "K": "I3",
            "forbidden_pairs": list(map(edge_string, outside_pairs)),
        },
        "guard_injection_lemma": {
            "outside_cap_adjacent_blocks": list(map(edge_string, sorted(OUTSIDE_CAP_ADJACENT))),
            "identity": (
                "for A_r6, R_2r^67(I)=A_r6^T when the switched partners are absent; "
                "for A_r7, R_1r^67(I)=A_r7^T"
            ),
            "coordinate_rank": 9,
            "unit_minor_determinant_abs": 1,
            "consequence": "formal guard forces the displayed block to zero",
        },
        "orbit_classification": {
            "orbits": len(orbit_records),
            "supports": len(support_records),
            "records": orbit_records,
            "support_records": support_records,
            "representative_reduced_size_census": reduced_size_census,
            "four_block_nonzero_guard_strata": 0,
        },
        "theorem": {
            "hypotheses_used": "formal cap67/triangle012 guard with K=I3",
            "pure_rows_used": False,
            "six_residual_common_zero_used": False,
            "source_equations_used": False,
            "conclusion": (
                "every one of the 24 supports loses one or two added blocks and "
                "reduces to the coefficient-independent active-cap two/three-block theorem"
            ),
            "inactive_parameter_locus": "empty on every exact four-block nonzero support stratum",
        },
        "literal_replay": {
            "samples": len(replay_records),
            "all_24_supports_distributed": True,
            "injection_before_guard": True,
            "all_outside_cap67_responses_zero_after_guard": True,
            "inherited_active_caps_replayed": True,
            "records_sha256": hashlib.sha256(json.dumps(replay_records, sort_keys=True).encode()).hexdigest(),
        },
        "scope": {
            "all_24_first_four_block_structural_evaders": True,
            "all_12_exact_guard_orbits": True,
            "all_other_four_block_supports": "already have fixed identity star/triangle certificate in parent",
            "all_four_block_supports_closed": True,
            "five_or_more_added_blocks": False,
            "full_support_dichotomy": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_four_block_guard_collapse.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_four_block_guard_collapse.json")
    print(json.dumps({
        "status": result["status"],
        "orbits": len(orbit_records),
        "supports": len(support_records),
        "representative_reductions": reduced_size_census,
        "nonzero_guard_strata": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
