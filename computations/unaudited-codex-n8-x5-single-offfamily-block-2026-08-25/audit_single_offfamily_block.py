#!/usr/bin/env python3
"""Exact first-layer support classification beyond the four-cycle X5 family."""

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
PARENT = HERE.parent / "unaudited-codex-n8-x5-cycle-polynomial-ideal-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "8ab337cde3b98f68909c642b655ceeb386abed3a81d692d53bec294547ecd107"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(CORE) == CORE_SHA256
spec = importlib.util.spec_from_file_location("x5_core", CORE)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

FAMILY = frozenset({
    (0, 3), (3, 5), (4, 5), (0, 4),
    (1, 6), (6, 7), (2, 7), (1, 2),
})
SQUARES = (frozenset((0, 3, 5, 4)), frozenset((1, 6, 7, 2)))
TRIANGLE = frozenset((0, 1, 2))
ALL_EDGES = frozenset(itertools.combinations(range(8), 2))
OFF_FAMILY = tuple(sorted(ALL_EDGES - FAMILY))


def zero_matrix():
    return [[0 for _ in core.COLORS] for _ in core.COLORS]


def identity_matrix():
    return [[int(i == j) for j in core.COLORS] for i in core.COLORS]


def basis_matrix(row, column):
    answer = zero_matrix()
    answer[row][column] = 1
    return answer


def install_stored_block(source, edge, matrix):
    u, v = edge
    assert u < v
    for left, right in itertools.product(core.COLORS, repeat=2):
        core.put(source, u, v, left, right, matrix[left][right])


def subtract_matrix(left, right):
    return [[left[i][j] - right[i][j] for j in core.COLORS] for i in core.COLORS]


def response_vector(source, covector, response_edges):
    vector = []
    for a, b in response_edges:
        matrix = core.response(source, 6, 7, a, b, covector)
        vector.extend(matrix[i][j] for i in core.COLORS for j in core.COLORS)
    return vector


def matrix_rank(columns):
    if not columns:
        return 0
    rows = [list(map(Fraction, row)) for row in zip(*columns)]
    height, width = len(rows), len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, height) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in zip(rows[row], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def source_block_to_response_rank(edge, response_edges):
    base = core.base_source()
    baseline = response_vector(base, identity_matrix(), response_edges)
    columns = []
    for left, right in itertools.product(core.COLORS, repeat=2):
        source = core.base_source()
        install_stored_block(source, edge, basis_matrix(left, right))
        value = response_vector(source, identity_matrix(), response_edges)
        columns.append([entry - old for entry, old in zip(value, baseline)])
    return matrix_rank(columns)


def covector_to_response_rank(edge, block_rank, response_edges):
    source = core.base_source()
    block = zero_matrix()
    for index in range(block_rank):
        block[index][index] = index + 1
    install_stored_block(source, edge, block)
    base = core.base_source()
    columns = []
    for left, right in itertools.product(core.COLORS, repeat=2):
        covector = basis_matrix(left, right)
        value = response_vector(source, covector, response_edges)
        old = response_vector(base, covector, response_edges)
        columns.append([entry - prior for entry, prior in zip(value, old)])
    return matrix_rank(columns)


def edge_string(edge):
    return "".join(map(str, edge))


def clean_cap_census(source):
    """Exact star/triangle carrier criterion over Q for this small source."""
    active = []
    for p, q in itertools.combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in (p, q))
        for triangle in itertools.combinations(residual, 3):
            forbidden = tuple(
                edge for edge in itertools.combinations(residual, 2)
                if not set(edge) <= set(triangle)
            )
            columns = []
            for left, right in itertools.product(core.COLORS, repeat=2):
                vector = []
                covector = basis_matrix(left, right)
                for a, b in forbidden:
                    matrix = core.response(source, p, q, a, b, covector)
                    vector.extend(matrix[i][j] for i in core.COLORS for j in core.COLORS)
                columns.append(vector)
            response_rank = matrix_rank(columns)
            if response_rank == 9:
                continue
            response_rows = [list(row) for row in zip(*columns)]
            activities = []
            for colour in core.COLORS:
                activities.append([
                    int((left, right) == (colour, colour))
                    for left, right in itertools.product(core.COLORS, repeat=2)
                ])
            activities.append([
                core.get(source, p, q, left, right)
                for left, right in itertools.product(core.COLORS, repeat=2)
            ])
            activity_live = [matrix_rank(response_rows + [row]) == response_rank + 1 for row in activities]
            if all(activity_live):
                active.append({
                    "cap": edge_string((p, q)),
                    "triangle": "".join(map(str, triangle)),
                    "response_rank": response_rank,
                    "kernel_dimension": 9 - response_rank,
                })
    return active


def main():
    assert len(FAMILY) == 8 and len(OFF_FAMILY) == 20
    family_matchings = tuple(matching for matching in core.PM8 if set(matching) <= FAMILY)
    assert tuple(map(core.matching_string, family_matchings)) == (
        "03|12|45|67", "03|16|27|45", "04|12|35|67", "04|16|27|35"
    )

    # The site-support graph is C4 disjoint union C4.  An added chord leaves
    # two opposite vertices, and an added bridge leaves odd vertex counts in
    # both components.  Therefore no perfect matching can use one new edge.
    one_block_records = []
    for edge in OFF_FAMILY:
        matching_uses_edge = [
            matching for matching in core.PM8
            if edge in matching and set(matching) <= FAMILY | {edge}
        ]
        assert not matching_uses_edge
        component_hits = [index for index, square in enumerate(SQUARES) if set(edge) <= square]
        support_type = "square_chord" if component_hits else "cross_square_bridge"
        one_block_records.append({
            "edge": edge_string(edge),
            "support_type": support_type,
            "perfect_matchings_using_new_block": 0,
            "all_amplitude_polynomials_unchanged": True,
        })
    assert sum(item["support_type"] == "square_chord" for item in one_block_records) == 4
    assert sum(item["support_type"] == "cross_square_bridge" for item in one_block_records) == 16

    residual_edges = tuple(itertools.combinations(range(6), 2))
    outside_edges = tuple(edge for edge in residual_edges if not set(edge) <= TRIANGLE)
    inside_edges = tuple(edge for edge in residual_edges if set(edge) <= TRIANGLE)
    assert len(outside_edges) == 12 and len(inside_edges) == 3

    # Exact cap-67 response classification.  For an outside cap-adjacent
    # block Z, fixed A72=I or A61=I makes one forbidden response equal Z up to
    # transpose.  Thus the fixed-K map Z -> forbidden responses has rank 9.
    cap_records = []
    for edge in OFF_FAMILY:
        if 6 not in edge and 7 not in edge:
            continue
        other = edge[0] if edge[1] in (6, 7) else edge[1]
        fixed_k_outside_rank = source_block_to_response_rank(edge, outside_edges)
        fixed_k_inside_rank = source_block_to_response_rank(edge, inside_edges)
        covector_outside_profile = [
            covector_to_response_rank(edge, rank, outside_edges) for rank in range(4)
        ]
        covector_all_profile = [
            covector_to_response_rank(edge, rank, residual_edges) for rank in range(4)
        ]
        if other not in TRIANGLE:
            assert fixed_k_outside_rank == 9 and fixed_k_inside_rank == 0
            assert covector_outside_profile == [0, 3, 6, 9]
            assert covector_all_profile == [0, 3, 6, 9]
            guard_verdict = "forced_zero_by_named_K=I_triangle_guard"
        else:
            assert fixed_k_outside_rank == 0
            assert covector_outside_profile == [0, 0, 0, 0]
            # A06 and A07 create an allowed response; A26 and A17 share the
            # sole old neighbour and create no response on distinct pairs.
            expected_inside = 9 if edge in ((0, 6), (0, 7)) else 0
            assert fixed_k_inside_rank == expected_inside
            expected_profile = [0, 3, 6, 9] if expected_inside else [0, 0, 0, 0]
            assert covector_all_profile == expected_profile
            guard_verdict = "allowed_but_matching_null"
        cap_records.append({
            "edge": edge_string(edge),
            "other_site": other,
            "fixed_K_I_block_to_forbidden_response_rank": fixed_k_outside_rank,
            "fixed_K_I_block_to_internal_response_rank": fixed_k_inside_rank,
            "cap_covector_to_forbidden_response_rank_for_block_ranks_0_1_2_3": covector_outside_profile,
            "cap_covector_to_all_response_rank_for_block_ranks_0_1_2_3": covector_all_profile,
            "guard_verdict": guard_verdict,
        })
    assert len(cap_records) == 10
    assert sum(item["guard_verdict"].startswith("forced_zero") for item in cap_records) == 6
    assert sum(item["guard_verdict"].startswith("allowed") for item in cap_records) == 4

    # Two new site blocks are necessary and sometimes sufficient.  Enumerate
    # the exact first support-changing layer to make the remaining boundary
    # explicit, without solving its coefficient/guard equations.
    first_open_pairs = []
    for left, right in itertools.combinations(OFF_FAMILY, 2):
        new_matchings = [
            matching for matching in core.PM8
            if set(matching) <= FAMILY | {left, right}
            and not set(matching) <= FAMILY
        ]
        if not new_matchings:
            continue
        if any(set(left) <= square and set(right) <= square for square in SQUARES):
            pattern = "two_complementary_chords_in_one_square"
        else:
            pattern = "two_cross_square_bridges_adjacent_at_each_square"
        assert all(left in matching and right in matching for matching in new_matchings)
        first_open_pairs.append({
            "edges": [edge_string(left), edge_string(right)],
            "pattern": pattern,
            "new_matchings": [core.matching_string(matching) for matching in new_matchings],
        })
    assert len(first_open_pairs) == 34
    assert sum(item["pattern"].startswith("two_complementary") for item in first_open_pairs) == 2
    assert sum(item["pattern"].startswith("two_cross") for item in first_open_pairs) == 32
    assert sum(len(item["new_matchings"]) for item in first_open_pairs) == 36

    # An explicit smallest support-changing boundary is the complementary
    # chord pair A05,A34.  It preserves the named cap-67 guard.  Choosing
    # trace(A67)=0 makes K=I inactive at that named cap, so the pair layer
    # cannot be dismissed merely by reusing that one activity form.  We also
    # audit all 560 carriers for this particular integer witness; any global
    # no-cap statement beyond it remains outside the claim.
    boundary = {}
    for edge in ((0, 3), (1, 6), (2, 7), (4, 5)):
        install_stored_block(boundary, edge, identity_matrix())
    install_stored_block(boundary, (6, 7), [[1, 0, 0], [0, -1, 0], [0, 0, 0]])
    core.put(boundary, 0, 5, 0, 1, 1)
    core.put(boundary, 3, 4, 0, 1, 1)
    assert [core.amplitude(boundary, (colour,) * 8) for colour in core.COLORS] == [1, 1, 1]
    assert all(core.response(boundary, 6, 7, *edge, identity_matrix()) == zero_matrix()
               for edge in outside_edges)
    assert sum(boundary.get(core.key(6, 7, colour, colour), 0) for colour in core.COLORS) == 0
    changed_word = (0, 0, 0, 0, 1, 1, 0, 0)
    changed_terms = core.amplitude_terms(boundary, changed_word)
    assert changed_terms == [
        (((0, 3), (1, 6), (2, 7), (4, 5)), 1),
        (((0, 5), (1, 6), (2, 7), (3, 4)), 1),
    ]
    active_boundary_caps = clean_cap_census(boundary)

    # The direct two-bridge pair A01,A23 is the smallest guard-preserving
    # family that can actually defeat the six residuals.  This exact rational
    # point keeps B,C off-diagonal, chooses trace(V)=0, and cancels every
    # ordered cross residual.  It is diagnostic rather than an X5 point.
    direct_boundary = {}
    for edge in ((0, 3), (1, 6), (2, 7), (4, 5)):
        install_stored_block(direct_boundary, edge, identity_matrix())
    v_diagonal = (Fraction(1), Fraction(1), Fraction(-2))
    install_stored_block(direct_boundary, (6, 7), [
        [v_diagonal[row] if row == column else 0 for column in core.COLORS]
        for row in core.COLORS
    ])
    for a, b in itertools.permutations(core.COLORS, 2):
        core.put(direct_boundary, 0, 1, a, b, 1)
        # C[b,a] is the coefficient used with B[a,b] in R_ab.
        core.put(direct_boundary, 2, 3, b, a, -1 / v_diagonal[b])
    assert [core.amplitude(direct_boundary, (colour,) * 8) for colour in core.COLORS] == [1, 1, 1]
    direct_residuals = {}
    for a, b in itertools.permutations(core.COLORS, 2):
        word = (a, b, b, a, a, a, b, b)
        terms = core.amplitude_terms(direct_boundary, word)
        assert terms == [
            (((0, 1), (2, 3), (4, 5), (6, 7)), -1),
            (((0, 3), (1, 6), (2, 7), (4, 5)), 1),
        ]
        assert core.amplitude(direct_boundary, word) == 0
        direct_residuals[f"R{a}{b}"] = 0
    assert all(core.response(direct_boundary, 6, 7, *edge, identity_matrix()) == zero_matrix()
               for edge in outside_edges)
    assert sum(v_diagonal) == 0
    direct_violations = [
        (core.word_string(word), core.amplitude(direct_boundary, word))
        for word in itertools.product(core.COLORS, repeat=8)
        if len(set(word)) > 1 and core.amplitude(direct_boundary, word)
    ]
    assert direct_violations
    active_direct_caps = clean_cap_census(direct_boundary)
    assert active_direct_caps[0] == {
        "cap": "01", "triangle": "236", "response_rank": 0, "kernel_dimension": 9
    }
    direct_K = [[1 for _ in core.COLORS] for _ in core.COLORS]
    direct_residual_sites = (2, 3, 4, 5, 6, 7)
    direct_triangle = frozenset((2, 3, 6))
    direct_forbidden = tuple(
        edge for edge in itertools.combinations(direct_residual_sites, 2)
        if not set(edge) <= direct_triangle
    )
    assert all(core.response(direct_boundary, 0, 1, *edge, direct_K) == zero_matrix()
               for edge in direct_forbidden)
    assert [direct_K[colour][colour] for colour in core.COLORS] == [1, 1, 1]
    direct_s = sum(
        direct_K[left][right] * core.get(direct_boundary, 0, 1, left, right)
        for left, right in itertools.product(core.COLORS, repeat=2)
    )
    assert direct_s == 6

    # Distributed literal guards with arbitrary rational 3x3 coefficients.
    # The residual six remain the unique physical matching term because the
    # additional site edge is absent from every supported perfect matching.
    replay_records = []
    for sample in range(257):
        edge = OFF_FAMILY[sample % len(OFF_FAMILY)]
        source = core.base_source()
        for u, v, sign in ((0, 4, 1), (1, 2, 1), (3, 5, -1), (6, 7, -1)):
            for a, b in itertools.permutations(core.COLORS, 2):
                core.put(source, u, v, a, b, Fraction(sign * (sample + 1 + a), 17 + b))
        arbitrary = [
            [Fraction((sample + 2) * (1 + row + 3 * column), 31 + row + column)
             for column in core.COLORS]
            for row in core.COLORS
        ]
        install_stored_block(source, edge, arbitrary)
        residuals = []
        for a, b in itertools.permutations(core.COLORS, 2):
            word = (a, b, b, a, a, a, b, b)
            assert core.amplitude_terms(source, word) == [(core.M0, 1)]
            residuals.append(core.word_string(word))
        assert [core.amplitude(source, (colour,) * 8) for colour in core.COLORS] == [1, 1, 1]
        replay_records.append({"sample": sample, "edge": edge_string(edge), "residuals": residuals})

    result = {
        "schema": "KRENN_X5_SINGLE_OFFFAMILY_BLOCK_CLASSIFICATION_V1",
        "status": "PASS_ALL_SINGLE_BLOCK_ESCAPES_SOURCE_EQUIVALENT_OR_GUARD_ZERO",
        "parent_manifest_sha256": PARENT_SHA256,
        "core_sha256": CORE_SHA256,
        "support_graph": {
            "family_edges": list(map(edge_string, sorted(FAMILY))),
            "components": ["03-35-54-40", "16-67-72-21"],
            "off_family_edges": len(OFF_FAMILY),
            "single_block_records": one_block_records,
            "theorem": (
                "every single additional site block is matching-null, so deletion is "
                "source-polynomial-equivalent for every word and arbitrary block coefficients"
            ),
        },
        "cap_67_response_classification": {
            "named_covector": "K=I3",
            "forbidden_response_pairs": [edge_string(edge) for edge in outside_edges],
            "records": cap_records,
            "outside_cap_adjacent_blocks_forced_zero": 6,
            "inside_cap_adjacent_blocks_allowed_but_matching_null": 4,
            "rank_formula": (
                "for an outside block Z of matrix rank rho, the new cap-covector "
                "response operator is left/right multiplication by Z and has rank 3*rho; "
                "at K=I the forbidden response is Z up to transpose"
            ),
        },
        "first_support_changing_layer": {
            "minimum_additional_site_blocks": 2,
            "support_pairs": len(first_open_pairs),
            "two_chord_pairs": 2,
            "two_bridge_pairs": 32,
            "records": first_open_pairs,
            "guard_and_coefficient_equations_classified": False,
            "smallest_explicit_boundary": {
                "new_blocks": ["A05", "A34"],
                "named_cap_67_guard_preserved": True,
                "named_K_I_activity_s_trace_A67": 0,
                "pure_rows": [1, 1, 1],
                "changed_amplitude": "Phi(00001100)=2 from M0 plus 05|16|27|34",
                "global_active_clean_cap_census_for_this_integer_witness": len(active_boundary_caps),
                "first_global_active_clean_cap": active_boundary_caps[0] if active_boundary_caps else None,
                "interpretation": (
                    "smallest source-support change and named-cap inactivity witness only; "
                    "it is not asserted to be globally no-cap"
                ),
            },
            "smallest_residual_common_zero_boundary": {
                "new_blocks": ["B=A01", "C=A23"],
                "new_matching": "01|23|45|67",
                "base_sector_extra_term": "B[a,b]*C[c,a]*V[b,c]",
                "residual_formula": "R_ab=P_a*Q_b+B[a,b]*C[b,a]*V[b,b]",
                "specialization": (
                    "X=Y=U=0, Vdiag=(1,1,-2), B[a,b]=1 and "
                    "C[b,a]=-1/V[b,b] for a!=b; B,C diagonal zero"
                ),
                "pure_rows": [1, 1, 1],
                "six_residuals": direct_residuals,
                "named_cap_67_guard_preserved": True,
                "named_K_I_activity_s_trace_A67": 0,
                "mixed_violations": len(direct_violations),
                "first_mixed_violation": {
                    "word": direct_violations[0][0],
                    "amplitude": str(direct_violations[0][1]),
                },
                "global_active_clean_cap_census_for_this_rational_witness": len(active_direct_caps),
                "first_global_active_clean_cap": active_direct_caps[0] if active_direct_caps else None,
                "explicit_active_clean_cap": {
                    "cap": "01",
                    "triangle": "236",
                    "K": "all-ones 3x3 matrix",
                    "forbidden_responses": 0,
                    "kappa": [1, 1, 1],
                    "s_pairing_with_A01": direct_s,
                },
                "interpretation": (
                    "exact smallest failure of the six-residual unit-ideal extension; "
                    "the point is not X5, and this sampled coefficient point is routed "
                    "to an active cap if the displayed global census is nonempty"
                ),
            },
        },
        "literal_replay": {
            "samples": len(replay_records),
            "all_twenty_edges_distributed": True,
            "arbitrary_rational_3x3_added_blocks": True,
            "pure_rows": [1, 1, 1],
            "six_residuals_unique_M0": True,
            "records_sha256": hashlib.sha256(json.dumps(replay_records, sort_keys=True).encode()).hexdigest(),
        },
        "same_source_reciprocity": "preserved automatically; response ranks use the literal same source",
        "scope": {
            "all_single_additional_site_blocks_classified": True,
            "two_block_coefficient_families_classified": False,
            "active_clean_cap_needed_in_single_block_layer": False,
            "full_guard_support_classification": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_single_offfamily_block.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_single_offfamily_block.json")
    print(json.dumps({
        "status": result["status"],
        "single_edges": len(one_block_records),
        "forced_zero": 6,
        "matching_null_guard_survivors": 14,
        "first_open_pairs": len(first_open_pairs),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
