#!/usr/bin/env python3
"""Exact bounded referee for the six seven-block X5 rank/activity strata."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOUNDARY_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/MANIFEST.sha256"
BOUNDARY_RESULT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/results_seven_block_support_boundary.json"
REFEREE_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-support-induction-boundary-referee-2026-08-25/FINAL_MANIFEST.sha256"
WITNESS_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-inactive-guard-witness-2026-08-25/MANIFEST.sha256"
WITNESS_RESULT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-inactive-guard-witness-2026-08-25/results_inactive_guard_witness.json"
SANDWICH_MANIFEST = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25/MANIFEST.sha256"
SANDWICH_RESULT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25/results_two_sandwich_reduction.json"

PINS = {
    BOUNDARY_MANIFEST: "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85",
    BOUNDARY_RESULT: "b3951e07149e4b831a5d3d3548284afb27f04154d805585468ba69bdb09b2f19",
    REFEREE_MANIFEST: "583bea191a1be0adb8d197270c22f9dd7b7ba0494b9d1f95b963213a19f23f61",
    WITNESS_MANIFEST: "34cc54e65d60ceec6da0ed203ff26d457f32455238f8e6f1ea6552267bdbbab7",
    WITNESS_RESULT: "bc17646368cfd53b5d534a9331ddb008926c626878cb4c2f503848312eb8f815",
    SANDWICH_MANIFEST: "056d73cd56818a18e2976707815f902cc433839ce69b192a88b118b7a9a5d707",
    SANDWICH_RESULT: "1d94711066e002f9f827ce4ce392526d0cb46c5b5c0f5eaba584af571561d19c",
}

COLORS = range(3)
SITES = tuple(range(8))
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
CAP = (6, 7)
TRIANGLE = frozenset((0, 1, 2))
REPS = (
    ((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)),
    ((0, 6), (1, 3), (1, 7), (2, 5), (2, 6), (4, 6), (4, 7)),
    ((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)),
    ((0, 6), (1, 4), (1, 7), (2, 5), (2, 6), (3, 6), (3, 7)),
    ((0, 6), (1, 5), (1, 7), (2, 3), (2, 6), (4, 6), (4, 7)),
    ((0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 6), (3, 7)),
)
M0 = tuple(sorted(FIXED))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def edge_text(edge):
    return "".join(map(str, edge))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(set(matchings(SITES))))
assert len(PM8) == 105 and M0 in PM8


def oriented_key(u, v, i, j):
    if u > v:
        return v, u, j, i
    return u, v, i, j


def symbolic_entry(support, u, v, i, j):
    edge = tuple(sorted((u, v)))
    if edge not in support:
        return None
    if edge in FIXED:
        return "1" if i == j else None
    a, b, x, y = oriented_key(u, v, i, j)
    return f"A{a}{b}_{x}{y}"


def monomial(*factors):
    if any(factor is None for factor in factors):
        return None
    return "*".join(sorted(factor for factor in factors if factor != "1")) or "1"


def response_row_polynomials(support, cap, pair, alpha, beta):
    p, q = cap
    a, b = pair
    answer = []
    for i, j in itertools.product(COLORS, repeat=2):
        terms = []
        direct = monomial(symbolic_entry(support, p, a, i, alpha),
                          symbolic_entry(support, q, b, j, beta))
        switched = monomial(symbolic_entry(support, p, b, i, beta),
                            symbolic_entry(support, q, a, j, alpha))
        if direct is not None:
            terms.append(direct)
        if switched is not None:
            terms.append(switched)
        answer.append(tuple(sorted(terms)))
    return tuple(answer)


def symbolic_map(support, cap, internal):
    residual = tuple(site for site in SITES if site not in cap)
    forbidden = tuple(edge for edge in itertools.combinations(residual, 2) if edge not in internal)
    rows = []
    for pair in forbidden:
        for alpha, beta in itertools.product(COLORS, repeat=2):
            rows.append(response_row_polynomials(support, cap, pair, alpha, beta))
    return forbidden, tuple(rows)


def structural_shape(edges):
    vertices = {v for edge in edges for v in edge}
    if len(vertices) <= 3:
        return "triangle"
    if edges and any(all(center in edge for edge in edges) for center in SITES):
        return "star"
    return None


def response_support_edges(support, cap):
    p, q = cap
    residual = tuple(site for site in SITES if site not in cap)
    result = []
    for a, b in itertools.combinations(residual, 2):
        if ((tuple(sorted((p, a))) in support and tuple(sorted((q, b))) in support)
                or (tuple(sorted((p, b))) in support and tuple(sorted((q, a))) in support)):
            result.append((a, b))
    return tuple(result)


def two_term_factorized_star_candidates(support):
    """Stars whose forbidden response has two terms sharing one source block."""
    candidates = []
    for cap in sorted(support):
        p, q = cap
        residual = tuple(site for site in SITES if site not in cap)
        for center in residual:
            terms = []
            for a, b in itertools.combinations(residual, 2):
                if center in (a, b):
                    continue
                direct = (tuple(sorted((p, a))), tuple(sorted((q, b))))
                switched = (tuple(sorted((p, b))), tuple(sorted((q, a))))
                if all(edge in support for edge in direct):
                    terms.append(frozenset(direct))
                if all(edge in support for edge in switched):
                    terms.append(frozenset(switched))
            if len(terms) != 2:
                continue
            common = terms[0] & terms[1]
            if len(common) == 1:
                candidates.append((edge_text(cap), center, edge_text(next(iter(common)))))
    return tuple(sorted(candidates))


def matrix_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows if any(row)]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [entry / value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def put(source, edge, row, column, value):
    source[(edge[0], edge[1], row, column)] = value


def get(source, u, v, i, j):
    a, b, x, y = oriented_key(u, v, i, j)
    return source.get((a, b, x, y), 0)


def identity_source():
    source = {}
    for edge in FIXED:
        for c in COLORS:
            put(source, edge, c, c, 1)
    return source


def response(source, cap, pair, K):
    p, q = cap
    a, b = pair
    out = [[0] * 3 for _ in COLORS]
    for alpha, beta in itertools.product(COLORS, repeat=2):
        out[alpha][beta] = sum(
            K[i][j] * (
                get(source, p, a, i, alpha) * get(source, q, b, j, beta)
                + get(source, p, b, i, beta) * get(source, q, a, j, alpha)
            )
            for i, j in itertools.product(COLORS, repeat=2)
        )
    return out


def basis(i, j):
    return [[int((r, c) == (i, j)) for c in COLORS] for r in COLORS]


def numeric_carrier(source, cap, internal):
    residual = tuple(site for site in SITES if site not in cap)
    forbidden = tuple(edge for edge in itertools.combinations(residual, 2) if edge not in internal)
    columns = []
    for i, j in itertools.product(COLORS, repeat=2):
        vector = []
        for pair in forbidden:
            R = response(source, cap, pair, basis(i, j))
            vector.extend(R[a][b] for a, b in itertools.product(COLORS, repeat=2))
        columns.append(vector)
    rows = [list(row) for row in zip(*columns)] if columns and columns[0] else []
    rank = matrix_rank(rows)
    activities = [
        [int((i, j) == (c, c)) for i, j in itertools.product(COLORS, repeat=2)]
        for c in COLORS
    ]
    p, q = cap
    activities.append([get(source, p, q, i, j) for i, j in itertools.product(COLORS, repeat=2)])
    live = [matrix_rank(rows + [activity]) == rank + 1 for activity in activities]
    return rank, live, rank < 9 and all(live)


def amplitude(source, word):
    total = 0
    for matching in PM8:
        value = 1
        for u, v in matching:
            value *= get(source, u, v, word[u], word[v])
            if not value:
                break
        total += value
    return total


def build_witness(record):
    source = identity_source()
    for text, item in record["source"]["matrix_units"].items():
        edge = tuple(map(int, text))
        put(source, edge, item["row"], item["column"], item["coefficient"])
    return source


def main():
    for path, digest in PINS.items():
        assert sha256(path) == digest
    boundary = json.loads(BOUNDARY_RESULT.read_text())
    witness_record = json.loads(WITNESS_RESULT.read_text())
    sandwich_record = json.loads(SANDWICH_RESULT.read_text())
    assert boundary["scope"]["first_full_family_structural_evader_supports"] == 12
    assert witness_record["status"] == "PASS_TRIANGLE_INACTIVE_GUARD_WITNESS_STAR_ROUTE_SURVIVES_AND_FULL_X5_FAILS"

    unresolved_records = [
        member
        for orbit in boundary["exact_variable_stratum_classification"]["unresolved_orbit_records"]
        for member in orbit["members"]
    ]
    assert len(unresolved_records) == 64
    factorized_star_choices = []
    candidate_count_census = Counter()
    for member in unresolved_records:
        support = set(FIXED)
        support.update(tuple(map(int, text)) for text in member["added"])
        support.update(tuple(map(int, text)) for text in member["nonzero_variable_blocks"])
        candidates = two_term_factorized_star_candidates(support)
        assert candidates
        candidate_count_census[len(candidates)] += 1
        factorized_star_choices.append(candidates[0])
    factorized_star_census = Counter(factorized_star_choices)
    independent_pattern_census = [
        {"cap": cap, "center": center, "common_block": common, "count": count}
        for (cap, center, common), count in sorted(factorized_star_census.items())
    ]
    assert independent_pattern_census == sandwich_record["census"]["pattern_census"]

    symbolic_records = []
    symbolic_digest_records = []
    for rep_id, rep in enumerate(REPS):
        support = FIXED | VARIABLE | set(rep)
        cap_edges = response_support_edges(support, CAP)
        outside = next(r for r in (3, 4, 5) if (r, 6) in support and (r, 7) in support)
        expected = tuple(itertools.combinations(sorted((0, 1, 2, outside)), 2))
        assert cap_edges == expected
        assert all(structural_shape(response_support_edges(support, cap)) is None
                   for cap in support)

        internal_triangle = set(itertools.combinations(sorted(TRIANGLE), 2))
        forbidden, rows = symbolic_map(support, CAP, internal_triangle)
        # The formal guard is exactly L_67 vec(I)=0. The three diagonal
        # activity rows are therefore live on the same kernel vector.
        guard_polynomials = []
        for row in rows:
            terms = []
            for index in (0, 4, 8):
                terms.extend(row[index])
            guard_polynomials.append(tuple(sorted(terms)))
        assert any(guard_polynomials)

        all_maps = []
        map_count = 0
        for cap in sorted(support):
            residual = tuple(site for site in SITES if site not in cap)
            for triangle in itertools.combinations(residual, 3):
                internal = set(itertools.combinations(triangle, 2))
                f, symbolic_rows = symbolic_map(support, cap, internal)
                all_maps.append((edge_text(cap), "triangle", triangle, f, symbolic_rows))
                map_count += 1
            for center in residual:
                internal = {tuple(sorted((center, other))) for other in residual if other != center}
                f, symbolic_rows = symbolic_map(support, cap, internal)
                all_maps.append((edge_text(cap), "star", (center,), f, symbolic_rows))
                map_count += 1
        assert map_count == len(support) * 26 == 390
        maps_sha = hashlib.sha256(json.dumps(all_maps, sort_keys=True).encode()).hexdigest()
        symbolic_digest_records.append(all_maps)

        graph_matchings = [matching for matching in PM8 if set(matching) <= support]
        alternative_occurrence_bound = sum(
            3 ** len(set(matching) & FIXED) for matching in graph_matchings if matching != M0
        )
        assert alternative_occurrence_bound < 78
        symbolic_records.append({
            "representative": list(map(edge_text, rep)),
            "outside_site": outside,
            "cap67_response_graph": list(map(edge_text, cap_edges)),
            "cap67_symbolic_rows": len(rows),
            "cap67_nonzero_symbolic_rows": sum(any(entry for entry in row) for row in rows),
            "formal_guard_polynomial_rows": sum(bool(row) for row in guard_polynomials),
            "symbolic_triangle_and_star_maps": map_count,
            "symbolic_maps_sha256": maps_sha,
            "graph_perfect_matchings": len(graph_matchings),
            "matrix_unit_alternative_word_occurrence_bound": alternative_occurrence_bound,
            "matrix_unit_full_X5_impossible": True,
        })

    # Canonical cap45/star(center=2) factorization.  The only structurally
    # nonzero forbidden pairs are 03,06,07, giving the concatenated map
    # A04*K*[A35^T | A56 | A57].  Its row space is P tensor Q.
    canonical_support = FIXED | VARIABLE | set(REPS[0])
    residual45 = tuple(site for site in SITES if site not in (4, 5))
    internal_star2 = {tuple(sorted((2, other))) for other in residual45 if other != 2}
    forbidden45, rows45 = symbolic_map(canonical_support, (4, 5), internal_star2)
    nonzero_forbidden45 = []
    for pair in forbidden45:
        pair_rows = rows45[9 * forbidden45.index(pair):9 * (forbidden45.index(pair) + 1)]
        if any(any(entry for entry in row) for row in pair_rows):
            nonzero_forbidden45.append(pair)
    assert nonzero_forbidden45 == [(0, 3), (0, 6), (0, 7)]

    # Independent literal replay of the sealed negative control.
    source = build_witness(witness_record)
    outside_pairs = tuple(
        pair for pair in itertools.combinations(range(6), 2) if not set(pair) <= TRIANGLE
    )
    I = basis(0, 0)
    for c in (1, 2):
        I[c][c] = 1
    assert all(response(source, CAP, pair, I) == [[0] * 3 for _ in COLORS]
               for pair in outside_pairs)

    triangles = []
    stars = []
    for cap in itertools.combinations(SITES, 2):
        residual = tuple(site for site in SITES if site not in cap)
        for triangle in itertools.combinations(residual, 3):
            internal = set(itertools.combinations(triangle, 2))
            triangles.append((cap, triangle, numeric_carrier(source, cap, internal)))
        for center in residual:
            internal = {tuple(sorted((center, other))) for other in residual if other != center}
            stars.append((cap, center, numeric_carrier(source, cap, internal)))
    active_triangles = [(cap, carrier) for cap, carrier, (_rank, _live, active) in triangles if active]
    active_stars = [(cap, carrier) for cap, carrier, (_rank, _live, active) in stars if active]
    assert active_triangles == []
    assert active_stars == [((1, 6), 2), ((4, 5), 2)]

    pure = [amplitude(source, (c,) * 8) for c in COLORS]
    residuals = [
        amplitude(source, (a, b, b, a, a, a, b, b))
        for a, b in itertools.permutations(COLORS, 2)
    ]
    mixed = [
        (word, amplitude(source, word))
        for word in itertools.product(COLORS, repeat=8)
        if len(set(word)) > 1 and amplitude(source, word) != 0
    ]
    assert pure == [1, 1, 1]
    assert residuals == [1, 1, 1, 1, 1, 2]
    assert len(mixed) == 114

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK_ACTIVITY_REFEREE_V1",
        "status": "PASS_EXACT_RANK_REDUCTION_AND_MATRIX_UNIT_SUBCLASS_CLOSED_GENERAL_LEMMA_OPEN",
        "dependencies": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "six_representatives": symbolic_records,
        "symbolic_all_maps_sha256": hashlib.sha256(
            json.dumps(symbolic_digest_records, sort_keys=True).encode()
        ).hexdigest(),
        "determinantal_reduction": {
            "formal_guard_identity": "L_67 vec(I3)=0",
            "rank_consequence": "rank(L_67)<=8",
            "diagonal_activity_consequence": "K00,K11,K22 are each nonzero on ker(L_67), witnessed simultaneously by I3",
            "only_remaining_cap67_activity_condition": "rank(stack(L_67,vec(A67)))=rank(L_67)+1",
            "equivalent_failure": "vec(A67) lies in rowspace(L_67); formal guard then also forces trace(A67)=0",
            "general_triangle_or_star_determinantal_test": "rank(L_C)<9 and rank(stack(L_C,a_i))=rank(L_C)+1 for each of K00,K11,K22,<K,A_C>",
        },
        "canonical_cap45_star2_factorization": {
            "forbidden_pairs_with_nonzero_symbolic_response": list(map(edge_text, nonzero_forbidden45)),
            "map": "K maps exactly to A04*K*[A35^T|A56|A57] in the pinned stored-edge convention",
            "P": "Row(A04)",
            "Q": "column span of A35^T,A56,A57",
            "response_row_space": "P tensor Q",
            "response_rank": "dim(P)*dim(Q)",
            "diagonal_activity_i_live": "not (e_i in P and e_i in Q)",
            "cap45_pairing_live": "trace is outside P tensor Q unless P=Q=Q^3",
            "active_star_criterion": "P and Q are not both full, and no coordinate vector e_i belongs to both P and Q",
            "inactive_or_rank9_locus": "P=Q=Q^3, or some e_i belongs to P intersect Q",
        },
        "canonical_formal_guard_reduction": {
            "R05": "A06*A57^T=0",
            "R15": "A17*A56^T+A57^T=0",
            "R25": "A26*A57^T+A56^T=0",
            "derived": [
                "A56^T=-A26*A57^T",
                "(I-A17*A26)*A57^T=0",
                "Col(A56) is contained in Col(A57)",
                "nonzero A06 forces rank(A57)<=2"
            ],
            "factorized_star_Q_simplification": "Q=Col(A35^T)+Col(A57)",
        },
        "all_64_factorized_star_reduction": {
            "unresolved_strata": len(unresolved_records),
            "each_has_two_forbidden_terms_with_common_source_block": True,
            "deterministic_choice": "lexicographically first (cap,center,common-block) candidate",
            "candidate_count_per_stratum_census": {str(k): v for k, v in sorted(candidate_count_census.items())},
            "choice_census": independent_pattern_census,
            "sealed_reduction_result_exactly_matched": True,
            "row_space_form": "P tensor Q for the row/column spaces induced by the common block and the two partner blocks",
            "activity_test": "the four activity augmentations reduce to finite subspace-incidence tests; this removes arbitrary minor expansion but does not by itself prove the full-X5 contradiction",
        },
        "matrix_unit_subclass_theorem": {
            "hypothesis": "each of the eleven nonidentity blocks is an arbitrary nonzero scalar multiple of one matrix unit",
            "fixed_matching_mixed_words_requiring_cancellation": 78,
            "alternative_occurrence_bounds": [record["matrix_unit_alternative_word_occurrence_bound"] for record in symbolic_records],
            "conclusion": "full X5 is impossible for every one of the six representatives because the total alternative word-occurrence capacity is strictly below 78",
        },
        "negative_control_replay": {
            "formal_guard": True,
            "pure_amplitudes": pure,
            "active_triangles": len(active_triangles),
            "active_stars": [{"cap": edge_text(cap), "center": center} for cap, center in active_stars],
            "six_residuals": residuals,
            "nonzero_mixed_amplitudes": len(mixed),
            "full_X5": False,
            "verdict": "refutes triangle-only guard+pure lemma; does not refute triangle-or-star-or-full-X5-contradiction",
        },
        "general_dense_stratum": {
            "verdict": "OPEN",
            "first_unproved_subclaim": "on the locus where vec(A67) is in rowspace(L67) and every triangle/star carrier fails an activity augmentation, the full mixed-amplitude ideal contains 1 or forces one of the fifteen named blocks to zero",
            "why_current_work_does_not_prove_it": "the matrix-unit occurrence bound is not valid for dense blocks, and no pinned identity eliminates the remaining determinantal locus",
            "no_countermodel_found_or_claimed": True,
        },
        "scope": {
            "representatives": 6,
            "exact_integer_rational_algebra": True,
            "symbolic_response_maps": True,
            "independent_negative_control_replay": True,
            "D12_read": False,
            "broad_solve": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_seven_block_rank_activity_referee.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_seven_block_rank_activity_referee.json")
    print(json.dumps({
        "status": result["status"],
        "occurrence_bounds": result["matrix_unit_subclass_theorem"]["alternative_occurrence_bounds"],
        "active_triangles": len(active_triangles),
        "active_stars": len(active_stars),
        "mixed": len(mixed),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
