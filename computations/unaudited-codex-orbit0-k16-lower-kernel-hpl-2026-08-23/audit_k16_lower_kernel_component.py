#!/usr/bin/env python3
"""Exact lex-component/HPL audit for the orbit-zero K16 boundary.

The full 701,717,184-row residual is deliberately not expanded.  This script
constructs the smallest literal same-head Schreyer star, then closes its raw
degree-24 source incidence through K-degree 16 until a fixed 100,000-row cap.
All outputs below K17 are retained, so the escape census is lower-kernel safe.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import product
import argparse
import ast
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_DIR = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
K14_SOURCE = K14_DIR / "audit_orbit0_k14_interface.py"
COVER = K14_DIR / "results_k16_anchor_cover.json"
LITERAL_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
LITERAL_RESULT = LITERAL_DIR / "results_orbit0_k16_literal_residual.json"
DEGREE24_SOURCE = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
                   / "audit_orbit0_t2_pivot_setup.py")
RESULT = HERE / "results_k16_lower_kernel_component.json"
ROW_CAP = 100_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


K14 = load("orbit0_k16_hpl_k14", K14_SOURCE)
F = K14.FROZEN
D24 = load("orbit0_k16_hpl_d24", DEGREE24_SOURCE)


def fractionless_packet():
    words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words)
    errors = []
    for word, anchor in zip(words, anchors, strict=True):
        errors.append(Counter({
            term: 1 for term in F.BASE.word_terms(word)
            if term != anchor and F.row_k_degree(term) == 2
        }))
    require(tuple(map(len, errors)) == (12, 12, 12), "K2 packet changed")
    packet = F.polynomial_product(F.polynomial_product(errors[0], errors[1]),
                                  errors[2])
    require(len(packet) == 1728 and set(packet.values()) == {1},
            "leading packet changed")
    return anchors, packet


def quotient(row, divisor):
    answer = Counter(row)
    answer.subtract(divisor)
    require(all(value >= 0 for value in answer.values()), "nondividing pivot")
    return bytes(sorted(cell for cell, value in answer.items()
                        for _ in range(value)))


def all_mixed_pivots():
    answer = []
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = F.word_from_pair_colours(colours)
        anchor = F.BASE.term_ids(word, F.M0)
        tails = tuple(term for term in F.BASE.word_terms(word)
                      if F.row_k_degree(term) == 2)
        require(len(tails) == 12, (colours, len(tails)))
        answer.append((colours, word, anchor, tails))
    require(len(answer) == 78, len(answer))
    return tuple(answer)


def factor_stabilizer(three_anchors):
    factor_set = frozenset(three_anchors)
    answer = tuple(
        action for action in range(len(F.EXPORT.STABILIZER))
        if frozenset(F.move_row(term, action) for term in three_anchors)
        == factor_set
    )
    require(len(answer) == 384, len(answer))
    return answer


def canonical_anchor_signature(row, actions):
    anchor_cells = tuple(sorted(F.A))
    position = {cell: index for index, cell in enumerate(anchor_cells)}
    raw = tuple(Counter(row)[cell] for cell in anchor_cells)
    images = []
    for action in actions:
        permutation = tuple(position[F.EXPORT.TRANSFORMS[action][cell]]
                            for cell in anchor_cells)
        moved = [0] * 12
        for old, new in enumerate(permutation):
            moved[new] = raw[old]
        images.append(tuple(moved))
    return raw, min(images)


def source_column_digest(columns):
    digest = sha256()
    for word, multiplier in sorted(columns, key=repr):
        digest.update(bytes(word))
        digest.update(multiplier)
    return digest.hexdigest()


def row_digest(rows):
    digest = sha256()
    for row in sorted(rows):
        digest.update(row)
    return digest.hexdigest()


def histogram(counter):
    return {str(key): counter[key] for key in sorted(counter)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true",
                        help="hostile mutation of the lex q label")
    args = parser.parse_args()

    cover = json.loads(COVER.read_text())
    require(cover["source"] == {
        "K14_factor_stabilizer_orbits": 33,
        "K14_signatures": 216,
        "exact_K2_tails_per_row": [12],
        "mixed_singleton_rows": 78,
    }, "25-signature source packet changed")
    minimum_cover = cover["single_pivot_cover"]["minimum_cover_orbit_representatives"]
    require(len(minimum_cover) == 25
            and len({ast.literal_eval(row) for row in minimum_cover}) == 25
            and cover["single_pivot_cover"]["exact_minimum_global_orbit_union"] == 25,
            "25-signature minimum cover changed")
    require(cover["affine_signature_test"]
            ["K14_orbits_with_complete_signature_level_K16_cancellation"] == 19
            and cover["affine_signature_test"]
            ["K14_orbits_with_signature_level_affine_obstruction"] == 14,
            "signature affine census changed")

    literal_sha = file_sha256(LITERAL_RESULT)
    require(literal_sha ==
            "28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189",
            "literal 701m-row no-go changed")

    three_anchors, packet = fractionless_packet()
    raw_r8 = json.loads(F.R8P.read_text())
    r8 = min(bytes.fromhex(record[0]) for record in raw_r8["residual"])
    packet_row = min(packet)
    q = bytes(sorted(r8 + packet_row))
    if args.mutate:
        q = q[:-1] + bytes([q[-1] - 1])
    require(q.hex() ==
            "000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3"
            and len(q) == 24 and F.row_k_degree(q) == 14,
            "lex q changed/hostile mutation fired")

    actions = factor_stabilizer(three_anchors)
    raw_signature, canonical_signature = canonical_anchor_signature(q, actions)
    require(raw_signature == (2, 1, 1, 2, 1, 1, 1, 0, 0, 1, 0, 0)
            and canonical_signature
            == (0, 0, 1, 0, 0, 1, 1, 1, 2, 1, 1, 2),
            "lex q signature changed")
    q_stabilizer = tuple(action for action in actions
                         if F.move_row(q, action) == q)
    require(q_stabilizer == (0,), "lex q unexpectedly acquired symmetry")

    pivots = []
    tail_columns = []
    for colours, word, anchor, tails in all_mixed_pivots():
        if not K14.divides(q, anchor):
            continue
        base = quotient(q, anchor)
        column = Counter(bytes(sorted(base + tail)) for tail in tails)
        require(sum(column.values()) == 12, "tail collision changed")
        pivots.append((colours, word, anchor, tails))
        tail_columns.append(column)
    pivot_colours = tuple(row[0] for row in pivots)
    require(pivot_colours == (
        (0, 1, 0, 0), (0, 2, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0),
        (1, 2, 0, 0), (2, 0, 0, 0), (2, 1, 0, 0), (2, 2, 0, 0),
    ), "lex q pivot packet changed")

    seed_rows = set().union(*(set(column) for column in tail_columns))
    owner_degree = Counter(sum(row in column for column in tail_columns)
                           for row in seed_rows)
    private_by_pivot = [tuple(sorted(row for row in column
                                     if sum(row in other
                                            for other in tail_columns) == 1))
                        for column in tail_columns]
    require(len(seed_rows) == 42
            and owner_degree == Counter({1: 16, 2: 8, 3: 16, 8: 2})
            and tuple(map(len, private_by_pivot)) == (2,) * 8,
            "8-pivot/42-row star changed")

    # Complete first incidence shell.  The provider enumerates every mixed
    # word/multiplier column containing a row by selecting a perfect-matching
    # divisor with multiplicity, and validates that the row occurs once.
    first_columns = set()
    for row in sorted(seed_rows):
        first_columns.update(D24.incident_degree24_columns(row))
    first_rows = set()
    first_column_minimum = Counter()
    first_column_profiles = Counter()
    for column in first_columns:
        outputs = D24.degree24_column_rows(column)
        degrees = tuple(D24.row_k_degree(row) for row in outputs)
        first_column_minimum[min(degrees)] += 1
        low = Counter(degree for degree in degrees if degree <= 16)
        first_column_profiles[tuple(sorted(low.items()))] += 1
        first_rows.update(row for row, degree in zip(outputs, degrees, strict=True)
                          if degree <= 16)
    first_row_degrees = Counter(D24.row_k_degree(row) for row in first_rows)
    require(len(first_columns) == 3625
            and len(first_rows) == 67315
            and first_column_minimum
            == Counter({12: 26, 13: 48, 14: 1055, 15: 564, 16: 1932})
            and first_row_degrees
            == Counter({12: 5, 13: 41, 14: 1035, 15: 9218, 16: 57016}),
            "complete first incidence shell changed")

    lex_exit = min(
        (column, row) for column in first_columns
        for row in D24.degree24_column_rows(column)
        if D24.row_k_degree(row) <= 16 and row not in seed_rows
    )

    # Exact whole-row BFS prefix.  Stop only after every incident column and
    # every <=K16 output of the current row has been included.
    closure_rows = set(seed_rows)
    closure_columns = set()
    queue = deque(sorted(seed_rows))
    processed = []
    while queue and len(closure_rows) < ROW_CAP:
        row = queue.popleft()
        processed.append(row)
        for column in D24.incident_degree24_columns(row):
            if column in closure_columns:
                continue
            closure_columns.add(column)
            for output in D24.degree24_column_rows(column):
                if D24.row_k_degree(output) <= 16 and output not in closure_rows:
                    closure_rows.add(output)
                    queue.append(output)

    closure_row_degrees = Counter(D24.row_k_degree(row) for row in closure_rows)
    closure_column_minimum = Counter(
        min(D24.row_k_degree(row) for row in D24.degree24_column_rows(column))
        for column in closure_columns
    )
    require(len(processed) == 73 and len(closure_rows) == 102110
            and len(closure_columns) == 5839 and len(queue) == 102037
            and closure_row_degrees
            == Counter({12: 23, 13: 201, 14: 2508, 15: 13992, 16: 85386})
            and closure_column_minimum
            == Counter({12: 69, 13: 101, 14: 1679, 15: 987, 16: 3003}),
            "whole-row closure prefix changed")

    payload = {
        "format": "n8-orbit0-k16-lower-kernel-hpl-v1",
        "status": "EXACT_LOCAL_HPL_OBSTRUCTION_LITERAL_COMPONENT_ESCAPES_100K",
        "authoritative_target": {
            "identity": "a*T belongs to I_mix + K^16",
            "scope": (
                "orbit-zero anchors-one chart; localized/powered filtered "
                "containment, not exponent-one target membership"
            ),
            "projected_packet": {
                "K14_signature_orbits": 33,
                "K16_signature_minimum_cover": 25,
                "signature_affine_zero_types": 19,
                "signature_affine_obstructed_types": 14,
            },
            "literal_expansion_no_go": {
                "nonzero_literal_H_orbits": 1848174,
                "labelled_rows": 701717184,
                "literal_result_sha256": literal_sha,
                "guard": (
                    "The 25 signatures forget nonanchor labels; the 701m rows "
                    "must not be materialized as the next certificate."
                ),
            },
        },
        "lex_factorized_head": {
            "r8": r8.hex(),
            "K6_packet_row": packet_row.hex(),
            "q_K14": q.hex(),
            "raw_anchor_signature": list(raw_signature),
            "canonical_anchor_signature": list(canonical_signature),
            "factor_stabilizer_order": len(actions),
            "q_stabilizer_order": len(q_stabilizer),
        },
        "same_head_schreyer_star": {
            "pivot_pair_colours": [list(row) for row in pivot_colours],
            "pivot_count": len(pivots),
            "K16_terms_per_pivot": 12,
            "distinct_K16_rows": len(seed_rows),
            "row_owner_degree_histogram": histogram(owner_degree),
            "private_rows_per_pivot": [len(rows) for rows in private_by_pivot],
            "tail_matrix_rank_over_Q": 8,
            "head_kernel_dimension": 7,
            "transferred_lower_kernel_rank_over_Q": 7,
            "affine_tail_cancellation": False,
            "exact_rank_proof": (
                "Each of the eight literal tail columns B_p has two rows absent "
                "from every other B_p. The resulting 8x8 identity minor makes "
                "B injective; its restriction to sum(alpha_p)=0 has rank 7, "
                "and B*alpha=0,sum(alpha)=1 is impossible."
            ),
            "tail_columns": [
                {
                    "pair_colours": list(colours),
                    "rows": [row.hex() for row in sorted(column)],
                    "private_rows": [row.hex() for row in private],
                }
                for colours, column, private
                in zip(pivot_colours, tail_columns, private_by_pivot, strict=True)
            ],
        },
        "complete_first_literal_shell": {
            "seed_rows": len(seed_rows),
            "incident_source_columns": len(first_columns),
            "all_output_rows_K_le_16": len(first_rows),
            "row_K_degree_histogram": histogram(first_row_degrees),
            "column_minimum_K_degree_histogram": histogram(first_column_minimum),
            "column_low_output_profile_histogram": {
                str(key): value for key, value in sorted(first_column_profiles.items())
            },
            "lex_first_exit": {
                "word": "".join(map(str, lex_exit[0][0])),
                "multiplier": lex_exit[0][1].hex(),
                "row": lex_exit[1].hex(),
                "row_K_degree": D24.row_k_degree(lex_exit[1]),
            },
            "lower_tail_soundness": (
                "Every output through K16 of every source column incident to "
                "the 42 seed rows is retained; K17+ is correctly zero in gr_K^16."
            ),
        },
        "whole_row_closure_prefix": {
            "row_cap": ROW_CAP,
            "processed_rows_complete": len(processed),
            "last_processed_row": processed[-1].hex(),
            "rows": len(closure_rows),
            "columns": len(closure_columns),
            "queued_rows": len(queue),
            "row_K_degree_histogram": histogram(closure_row_degrees),
            "column_minimum_K_degree_histogram": histogram(closure_column_minimum),
            "rows_sha256": row_digest(closure_rows),
            "columns_sha256": source_column_digest(closure_columns),
            "verdict": (
                "The literal connected component exceeds 100k rows after only "
                "73 complete row expansions. No peel/rank conclusion is made."
            ),
        },
        "provenance_preserving_H_quotient_spec": {
            "row_nodes": "H-orbits of labelled degree-24 monomials of K-degree <=16",
            "column_nodes": "H-orbits of literal mixed (word, degree-20 multiplier) columns",
            "matrix_entry": (
                "total coefficient mass from the complete H-orbit of a source "
                "column into the complete H-orbit of a row"
            ),
            "incidence_provider": (
                "for one row representative enumerate every perfect-matching "
                "divisor/source column, canonicalize the column under H, then "
                "expand its 105 literal terms through K16 and canonicalize rows"
            ),
            "soundness": (
                "The target and ideal are H-invariant and char0 averaging is exact, "
                "so a full solution can be averaged to the orbit-sum subspace. "
                "Unlike the 25-signature projection, orbit representatives retain "
                "every nonanchor label and stabilizer mass."
            ),
            "dfs_terminal": (
                "close the target-rooted bipartite component; singleton-peel only "
                "after all incident column orbits of a row orbit are exposed; then "
                "test exact-Q target augmentation on the finite residual"
            ),
        },
        "pinned": {
            str(K14_SOURCE.relative_to(ROOT)): file_sha256(K14_SOURCE),
            str(COVER.relative_to(ROOT)): file_sha256(COVER),
            str(LITERAL_RESULT.relative_to(ROOT)): literal_sha,
            str(DEGREE24_SOURCE.relative_to(ROOT)): file_sha256(DEGREE24_SOURCE),
            str(F.R8P.relative_to(ROOT)): file_sha256(F.R8P),
        },
        "scope_guard": (
            "The local Schreyer class is exact and the literal escape census is "
            "complete to its stated cap. This does not decide the whole K16 "
            "component, filtered membership, localization, or any other chart."
        ),
        "source_sha256": file_sha256(Path(__file__)),
    }
    logical = dict(payload)
    logical.pop("source_sha256")
    payload["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", payload["logical_sha256"])


if __name__ == "__main__":
    main()
