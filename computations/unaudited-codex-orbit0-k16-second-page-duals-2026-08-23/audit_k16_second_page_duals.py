#!/usr/bin/env python3
"""Literal first-page referee for the 14 post-singleton K16 duals.

The archived 19/14 affine split first removes every K16 tail admitting a
second K0 singleton pivot.  For each of its 14 inconsistent anchor types this
checker extracts a deletion-minimal exact rational dual, lifts it to one
canonical literal factorized K14 head, and enumerates every degree-24 mixed
source column incident to the literal support.  It expands only that first
incident page and keeps every output of K-degree at most 16.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
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
SOURCE_PROVIDER = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
                   / "audit_orbit0_t2_pivot_setup.py")
RESULT = HERE / "results_k16_second_page_duals.json"


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


def solve_exact(matrix, rhs):
    """Return one exact solution with free variables zero, or None."""
    require(len(matrix) == len(rhs), "linear system height mismatch")
    variable_count = len(matrix[0]) if matrix else 0
    rows = [[Fraction(value) for value in row] + [Fraction(value_rhs)]
            for row, value_rhs in zip(matrix, rhs, strict=True)]
    pivot_columns = []
    pivot_row = 0
    for column in range(variable_count):
        selected = next((index for index in range(pivot_row, len(rows))
                         if rows[index][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            scale = rows[index][column]
            rows[index] = [left - scale * right
                           for left, right in zip(rows[index], rows[pivot_row],
                                                  strict=True)]
        pivot_columns.append(column)
        pivot_row += 1
    if any(not any(row[:variable_count]) and row[-1] for row in rows):
        return None
    solution = [Fraction(0) for _ in range(variable_count)]
    for index, column in enumerate(pivot_columns):
        solution[column] = rows[index][-1]
    return solution


def sparse_row_span(rows, target):
    """Exact sparse row reduction, target remainder, and a separating dual."""
    rows = tuple(rows)
    basis = {}
    pivot_order = []

    def reduce(vector, insert):
        vector = {key: Fraction(value) for key, value in vector.items() if value}
        # Clear every previously inserted pivot, not merely pivots preceding
        # the smallest currently live coordinate.  This keeps the basis
        # triangular in insertion order and makes the dual back-substitution
        # below exact even when byte/int key order and insertion order differ.
        for old_pivot in pivot_order:
            if old_pivot not in vector:
                continue
            scale = vector[old_pivot]
            for key, value in basis[old_pivot].items():
                updated = vector.get(key, Fraction(0)) - scale * value
                if updated:
                    vector[key] = updated
                else:
                    vector.pop(key, None)
        if vector and insert:
            pivot = min(vector)
            scale = vector[pivot]
            vector = {key: value / scale for key, value in vector.items()}
            basis[pivot] = vector
            pivot_order.append(pivot)
        return {}

    ordered = sorted(rows, key=lambda row: (len(row), tuple(sorted(row))))
    for row in ordered:
        reduce(row, True)
    remainder = {key: Fraction(value) for key, value in target.items() if value}
    # A target may begin with a free (nonpivot) coordinate while still carrying
    # later pivot coordinates.  Reduce pivots in insertion order rather than
    # stopping at that first free coordinate.
    for pivot in pivot_order:
        if pivot not in remainder:
            continue
        scale = remainder[pivot]
        for key, value in basis[pivot].items():
            updated = remainder.get(key, Fraction(0)) - scale * value
            if updated:
                remainder[key] = updated
            else:
                remainder.pop(key, None)
    dual = {}
    if remainder:
        free = min(remainder)
        dual[free] = Fraction(1, 1) / remainder[free]
        for pivot in reversed(pivot_order):
            value = -sum(coefficient * dual.get(key, Fraction(0))
                         for key, coefficient in basis[pivot].items()
                         if key != pivot)
            if value:
                dual[pivot] = value
        require(sum(value * dual.get(key, 0) for key, value in target.items()) == 1,
                "separating dual missed target")
        require(all(sum(value * dual.get(key, 0) for key, value in row.items()) == 0
                    for row in rows), "separating dual missed a source column")
    return len(basis), remainder, dual


K14 = load("orbit0_k16_second_page_k14", K14_SOURCE)
F = K14.FROZEN
D24 = load("orbit0_k16_second_page_d24", SOURCE_PROVIDER)


def fraction_record(value):
    return [value.numerator, value.denominator]


def mixed_pivots():
    cells = tuple(sorted(F.A))
    answer = []
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = F.word_from_pair_colours(colours)
        anchor = F.BASE.term_ids(word, F.M0)
        tails = tuple(term for term in F.BASE.word_terms(word)
                      if F.row_k_degree(term) == 2)
        require(len(tails) == 12, (colours, len(tails)))
        answer.append({
            "colours": colours,
            "word": word,
            "anchor": anchor,
            "anchor_vector": tuple(Counter(anchor)[cell] for cell in cells),
            "tails": tails,
            "tail_vectors": tuple(
                tuple(Counter(tail)[cell] for cell in cells) for tail in tails),
        })
    require(len(answer) == 78, len(answer))
    return tuple(answer)


def factor_data():
    words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words)
    errors = tuple(Counter({
        term: 1 for term in F.BASE.word_terms(word)
        if term != anchor and F.row_k_degree(term) == 2
    }) for word, anchor in zip(words, anchors, strict=True))
    packet = F.polynomial_product(F.polynomial_product(errors[0], errors[1]),
                                  errors[2])
    require(len(packet) == 1728 and set(packet.values()) == {1},
            "K6 packet changed")
    anchor_set = frozenset(anchors)
    stabilizer = tuple(
        action for action in range(len(F.EXPORT.STABILIZER))
        if frozenset(F.move_row(term, action) for term in anchors) == anchor_set
    )
    require(len(stabilizer) == 384, len(stabilizer))
    return anchors, tuple(sorted(packet)), stabilizer


def move_signature(signature, permutation):
    moved = [0] * len(signature)
    for old, new in enumerate(permutation):
        moved[new] = signature[old]
    return tuple(moved)


def canonical_literal_heads(target_signatures, packet, stabilizer):
    """Choose the lex literal factorized q in each requested signature orbit."""
    cells = tuple(sorted(F.A))
    position = {cell: index for index, cell in enumerate(cells)}
    actions = []
    for action in stabilizer:
        transform = F.EXPORT.TRANSFORMS[action]
        actions.append((action, tuple(position[transform[cell]] for cell in cells)))

    raw_to_target = {}
    for target in target_signatures:
        for _action, permutation in actions:
            raw_to_target[move_signature(target, permutation)] = target
    raw_to_action = {}
    for raw, target in raw_to_target.items():
        raw_to_action[raw] = next(
            action for action, permutation in actions
            if move_signature(raw, permutation) == target
        )

    residual_json = json.loads(F.R8P.read_text())
    residual = tuple(bytes.fromhex(row) for row, _numerator, _denominator
                     in residual_json["residual"])
    h_representatives = []
    for representative in residual:
        unseen = set(F.EXPORT.row_orbit(representative))
        while unseen:
            seed = min(unseen)
            orbit = F.orbit_under(seed, stabilizer)
            h_representatives.append(seed)
            unseen.difference_update(orbit)
    require(len(h_representatives) == 485, len(h_representatives))

    answer = {}
    heads_scanned = 0
    for residual_row in sorted(h_representatives):
        for packet_row in packet:
            heads_scanned += 1
            raw = bytes(sorted(residual_row + packet_row))
            raw_signature = tuple(Counter(raw)[cell] for cell in cells)
            target = raw_to_target.get(raw_signature)
            if target is None:
                continue
            moved = F.move_row(raw, raw_to_action[raw_signature])
            require(tuple(Counter(moved)[cell] for cell in cells) == target,
                    "literal-head transport failed")
            if target not in answer or moved < answer[target]:
                answer[target] = moved
    require(heads_scanned == 838080 and set(answer) == set(target_signatures),
            (heads_scanned, len(answer)))
    return answer, heads_scanned


def post_singleton_columns(signature, pivots):
    columns = []
    live_pivots = []
    for pivot in pivots:
        anchor = pivot["anchor_vector"]
        if not all(left >= right
                   for left, right in zip(signature, anchor, strict=True)):
            continue
        base = tuple(left - right
                     for left, right in zip(signature, anchor, strict=True))
        column = Counter()
        for tail in pivot["tail_vectors"]:
            row = tuple(left + right
                        for left, right in zip(base, tail, strict=True))
            reducible = any(all(left >= right
                                for left, right in zip(row,
                                                       other["anchor_vector"],
                                                       strict=True))
                            for other in pivots)
            if not reducible:
                column[row] += 1
        columns.append(column)
        live_pivots.append(pivot)
    require(columns, signature)
    return tuple(live_pivots), tuple(columns)


def deletion_minimal_dual(columns):
    coordinates = sorted(set().union(*(set(column) for column in columns)))
    active = list(coordinates)
    for coordinate in coordinates:
        trial = [row for row in active if row != coordinate]
        matrix = [[column.get(row, 0) for row in trial] for column in columns]
        if solve_exact(matrix, [1] * len(columns)) is not None:
            active = trial
    matrix = [[column.get(row, 0) for row in active] for column in columns]
    solution = solve_exact(matrix, [1] * len(columns))
    require(solution is not None, "dual extraction failed")
    support = {row: value for row, value in zip(active, solution, strict=True)
               if value}
    require(support, "empty affine dual")
    # Literal deletion-minimality: removing any retained coordinate destroys
    # B^T lambda = 1.
    for deleted in support:
        trial = [row for row in support if row != deleted]
        require(solve_exact([[column.get(row, 0) for row in trial]
                             for column in columns], [1] * len(columns)) is None,
                ("dual not deletion-minimal", deleted))
    require(all(sum(column.get(row, 0) * value
                    for row, value in support.items()) == 1
                for column in columns), "dual does not separate every pivot")
    return support, len(coordinates)


def quotient(row, divisor):
    result = Counter(row)
    result.subtract(divisor)
    require(all(value >= 0 for value in result.values()), "nondividing head")
    return bytes(sorted(cell for cell, value in result.items()
                        for _ in range(value)))


def literal_dual(signature, q, pivots, projected_dual):
    cells = tuple(sorted(F.A))
    columns = []
    literal = {}
    pivot_colours = []
    for pivot in pivots:
        anchor_vector = pivot["anchor_vector"]
        if not all(left >= right
                   for left, right in zip(signature, anchor_vector, strict=True)):
            continue
        base = quotient(q, pivot["anchor"])
        column = Counter()
        for tail, tail_vector in zip(pivot["tails"], pivot["tail_vectors"],
                                     strict=True):
            projected = tuple(left - middle + right
                              for left, middle, right
                              in zip(signature, anchor_vector, tail_vector,
                                     strict=True))
            reducible = any(all(left >= right
                                for left, right in zip(projected,
                                                       other["anchor_vector"],
                                                       strict=True))
                            for other in pivots)
            if reducible:
                continue
            raw = bytes(sorted(base + tail))
            column[raw] += 1
            value = projected_dual.get(projected, Fraction(0))
            if value:
                require(raw not in literal or literal[raw] == value,
                        "literal lift coefficient collision")
                literal[raw] = value
        columns.append(column)
        pivot_colours.append(pivot["colours"])
    require(all(sum(multiplicity * literal.get(row, 0)
                    for row, multiplicity in column.items()) == 1
                for column in columns), "literal dual lost pivot separation")
    require(all(tuple(Counter(row)[cell] for cell in cells) in projected_dual
                for row in literal), "literal support escaped projected dual")
    return tuple(columns), literal, tuple(pivot_colours)


def first_page(q, literal, mutate=False):
    support_rows = tuple(sorted(literal))
    incident_columns = set()
    for row in support_rows:
        incident_columns.update(D24.incident_degree24_columns(row))
    columns = tuple(sorted(incident_columns, key=repr))
    if mutate:
        columns = tuple(column for column in columns
                        if min(D24.row_k_degree(row)
                               for row in D24.degree24_column_rows(column)) < 16)

    minimum_histogram = Counter()
    crossing_histogram = Counter()
    lower_rows = defaultdict(Counter)
    k16_rows = set()
    complete_column_vectors = []
    direct = []
    lower_column_indices = []
    lower_crossing = {}
    for index, column in enumerate(columns):
        outputs = Counter(D24.degree24_column_rows(column))
        degrees = {row: D24.row_k_degree(row) for row in outputs}
        complete_column_vectors.append({
            row: multiplicity for row, multiplicity in outputs.items()
            if degrees[row] <= 16
        })
        minimum = min(degrees.values())
        minimum_histogram[minimum] += 1
        crossing = sum(multiplicity * literal.get(row, 0)
                       for row, multiplicity in outputs.items())
        crossing_histogram[crossing] += 1
        k16_rows.update(row for row, degree in degrees.items() if degree == 16)
        if minimum == 16 and crossing:
            direct.append((column, crossing, outputs))
        if minimum < 16:
            lower_index = len(lower_column_indices)
            lower_column_indices.append(index)
            lower_crossing[lower_index] = crossing
            for row, multiplicity in outputs.items():
                if degrees[row] < 16:
                    lower_rows[row][lower_index] += multiplicity

    # This is the actual first lower-kernel page: c annihilates ker(A) iff
    # c lies in the row span of the complete K<16 incidence matrix A.
    lower_rank, remainder, _lower_dual = sparse_row_span(
        tuple(dict(row) for row in lower_rows.values()), lower_crossing)
    lower_kernel_dimension = len(lower_column_indices) - lower_rank
    transferred_detection_rank = int(bool(remainder))

    # Distinguish killing the old dual from filling the local target.  This is
    # exact column-span membership on precisely the bounded incident page; a
    # nonzero target remainder is a new extended dual for this restricted
    # page, not a global nonmembership claim.
    page_column_rank, target_remainder, replacement_dual = sparse_row_span(
        tuple(complete_column_vectors), {q: Fraction(1)})
    target_is_member = not target_remainder

    require(direct, "hostile mutation removed every direct K16 killer")
    witness_column, witness_value, witness_outputs = min(direct, key=repr)
    witness_word, witness_multiplier = witness_column
    witness_hits = tuple(sorted(row for row in witness_outputs if row in literal))
    require(witness_value != 0
            and min(D24.row_k_degree(row) for row in witness_outputs) == 16
            and witness_hits, "invalid direct source witness")
    degree_profile = Counter(D24.row_k_degree(row) for row in replacement_dual)
    coefficient_profile = Counter(str(value) for value in replacement_dual.values())
    return {
        "literal_dual_rows": len(literal),
        "incident_source_columns": len(columns),
        "minimum_K_degree_histogram": {
            str(key): value for key, value in sorted(minimum_histogram.items())
        },
        "functional_crossing_histogram": {
            str(key): value for key, value in sorted(crossing_histogram.items())
        },
        "distinct_lower_rows": len(lower_rows),
        "distinct_K16_rows": len(k16_rows),
        "direct_min16_killers": len(direct),
        "first_direct_witness": {
            "word": "".join(map(str, witness_word)),
            "multiplier": witness_multiplier.hex(),
            "functional_pairing": fraction_record(witness_value),
            "literal_dual_rows_hit": [row.hex() for row in witness_hits],
            "K16_outputs": sum(D24.row_k_degree(row) == 16
                               for row in witness_outputs),
        },
        "lower_only_page": {
            "columns": len(lower_column_indices),
            "K_less_than_16_rows": len(lower_rows),
            "exact_row_rank_over_Q": lower_rank,
            "lower_kernel_dimension": lower_kernel_dimension,
            "dual_detects_lower_kernel": bool(remainder),
            "transferred_detection_rank": transferred_detection_rank,
            "remainder_support": len(remainder),
        },
        "restricted_full_page_target_test": {
            "column_rank_over_Q": page_column_rank,
            "target_augmented_rank_over_Q": page_column_rank
            + int(not target_is_member),
            "local_q_in_column_span": target_is_member,
            "target_remainder_support": len(target_remainder),
            "replacement_dual_support": len(replacement_dual),
            "replacement_dual_K_degree_profile": {
                str(key): value for key, value in sorted(degree_profile.items())
            },
            "replacement_dual_coefficient_profile": dict(sorted(
                coefficient_profile.items())),
            "guard": (
                "Exact only for columns incident to the chosen old dual "
                "support. Nonmembership means an extended dual survives this "
                "bounded page; it is not full-component nonmembership."
            ),
        },
        "old_dual_first_page_verdict": "DIES_BY_DIRECT_MIN16_SOURCE_COLUMN",
    }, replacement_dual


def build(mutate=False):
    require(file_sha256(K14_SOURCE)
            == "7a9891d5fc4d8964518147c0202e0f29b7393e7bed3a7651beb053eb4402c19a",
            "K14 source drift")
    require(file_sha256(COVER)
            == "5efffe78e3fd9c42ca91be2a6a10bb7d4d4cc0fa13d986ca411cc692c999dfdf",
            "19/14 cover drift")
    cover = json.loads(COVER.read_text())
    signatures = tuple(ast.literal_eval(row) for row in
                       cover["affine_signature_test"]["obstructed_representatives"])
    require(len(signatures) == 14 and len(set(signatures)) == 14,
            "affine-obstructed type list changed")
    pivots = mixed_pivots()
    _anchors, packet, stabilizer = factor_data()
    heads, heads_scanned = canonical_literal_heads(signatures, packet, stabilizer)

    records = []
    replacement_duals = []
    for index, signature in enumerate(signatures):
        live_pivots, projected_columns = post_singleton_columns(signature, pivots)
        projected_dual, projected_rows = deletion_minimal_dual(projected_columns)
        literal_columns, literal, pivot_colours = literal_dual(
            signature, heads[signature], pivots, projected_dual)
        require(len(literal_columns) == len(projected_columns)
                and len(pivot_colours) == len(projected_columns),
                "literal/projected pivot mismatch")
        page, replacement_dual = first_page(
            heads[signature], literal, mutate and index == 0)
        replacement_duals.append(replacement_dual)
        records.append({
            "canonical_anchor_signature": list(signature),
            "literal_factorized_q": heads[signature].hex(),
            "pivot_count": len(live_pivots),
            "irreducible_projected_tail_rows": projected_rows,
            "deletion_minimal_projected_dual": [
                {
                    "row": list(row),
                    "coefficient": fraction_record(value),
                }
                for row, value in sorted(projected_dual.items())
            ],
            "literal_dual_support": [
                {"row": row.hex(), "coefficient": fraction_record(value)}
                for row, value in sorted(literal.items())
            ],
            "page": page,
        })

    direct_counts = Counter(row["page"]["direct_min16_killers"]
                            for row in records)
    lower_detection = Counter(row["page"]["lower_only_page"]
                              ["dual_detects_lower_kernel"] for row in records)
    target_membership = Counter(row["page"]["restricted_full_page_target_test"]
                                ["local_q_in_column_span"] for row in records)
    require(all(row["page"]["old_dual_first_page_verdict"]
                == "DIES_BY_DIRECT_MIN16_SOURCE_COLUMN" for row in records),
            "an affine dual survived full first page")
    require(target_membership == Counter({False: 14}),
            "a restricted first page unexpectedly filled its local q")
    smallest_index = min(range(len(records)),
                         key=lambda index: (len(replacement_duals[index]), index))
    smallest_dual = replacement_duals[smallest_index]
    replacement_support_histogram = Counter(map(len, replacement_duals))
    payload = {
        "format": "n8-orbit0-k16-second-page-duals-v1",
        "status": (
            "OLD_14_DUALS_DIE_DIRECTLY_BUT_RESTRICTED_TARGETS_REMAIN_NONMEMBERS"
        ),
        "source": {
            "post_second_singleton_affine_inconsistent_types": 14,
            "literal_singleton_pivots": 78,
            "K2_tails_per_pivot": 12,
            "factorized_K14_heads_scanned": heads_scanned,
            "canonical_literal_representatives": len(heads),
        },
        "summary": {
            "deletion_minimal_dual_support_histogram": {
                str(key): value for key, value in sorted(Counter(
                    len(row["deletion_minimal_projected_dual"]) for row in records
                ).items())
            },
            "literal_dual_support_histogram": {
                str(key): value for key, value in sorted(Counter(
                    len(row["literal_dual_support"]) for row in records
                ).items())
            },
            "archived_duals_dying_by_direct_min16_source": len(records),
            "archived_duals_surviving_full_first_page": 0,
            "types_with_replacement_extended_dual_on_restricted_page": 14,
            "replacement_dual_support_histogram": {
                str(key): value for key, value
                in sorted(replacement_support_histogram.items())
            },
            "restricted_page_local_target_membership": {
                str(key).lower(): value for key, value in sorted(
                    target_membership.items(), key=lambda item: item[0])
            },
            "direct_killer_count_range": [min(direct_counts), max(direct_counts)],
            "lower_only_kernel_detection": {
                str(key).lower(): value for key, value in sorted(
                    lower_detection.items(), key=lambda item: item[0])
            },
            "interpretation": (
                "Every deletion-minimal post-singleton dual already pairs "
                "nontrivially with a literal source column of minimum K-degree "
                "16. Thus none reaches a stage where lower-filtration transfer "
                "is required to kill that old dual. This is not itself a "
                "filler: for all 14 representatives the restricted-page "
                "target-augmented rank is column rank plus one, so a "
                "replacement extended dual remains."
            ),
        },
        "smallest_replacement_extended_dual": {
            "type_index": smallest_index,
            "canonical_anchor_signature": records[smallest_index]
            ["canonical_anchor_signature"],
            "literal_factorized_q": records[smallest_index]["literal_factorized_q"],
            "support": [
                {"row": row.hex(), "coefficient": fraction_record(value),
                 "K_degree": D24.row_k_degree(row)}
                for row, value in sorted(smallest_dual.items())
            ],
            "normalization": "annihilates every restricted-page column and pairs q to 1",
        },
        "types": records,
        "scope_guard": (
            "For each of the 14 anchor-signature types this tests one canonical "
            "literal factorized representative q and its complete incident "
            "first source page through K16. Factor-stabilizer transport covers "
            "the exact H-orbit of that q, not every non-H-equivalent literal "
            "completion with the same anchor signature. No second incident "
            "page, 701m-row residual, localization, or other chart is tested."
        ),
        "pinned": {
            str(K14_SOURCE.relative_to(ROOT)): file_sha256(K14_SOURCE),
            str(COVER.relative_to(ROOT)): file_sha256(COVER),
            str(SOURCE_PROVIDER.relative_to(ROOT)): file_sha256(SOURCE_PROVIDER),
            str(F.R8P.relative_to(ROOT)): file_sha256(F.R8P),
        },
    }
    logical = sha256(json.dumps(payload, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate", action="store_true",
                        help="delete all direct min16 columns for the first type")
    args = parser.parse_args()
    payload = build(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "logical_sha256": payload["logical_sha256"],
        "summary": payload["summary"],
        "per_type": [
            {
                "signature": row["canonical_anchor_signature"],
                "pivots": row["pivot_count"],
                "projected_dual_rows": len(row["deletion_minimal_projected_dual"]),
                "literal_dual_rows": len(row["literal_dual_support"]),
                "direct_killers": row["page"]["direct_min16_killers"],
                "lower_only": row["page"]["lower_only_page"],
                "target_test": row["page"]["restricted_full_page_target_test"],
            }
            for row in payload["types"]
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
