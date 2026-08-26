#!/usr/bin/env python3
"""Exact local audit of a provenance-preserving K14 -> K16 provider.

This deliberately audits only Tail's lexicographically first K14 monomial.
It does not expand the 701,717,184-row collected residual.  The point is to
pin the literal provider interface, its H-action, and a restartable local
peel before a streaming implementation is scaled to the full factor packet.
"""

from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_PATH = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
            / "audit_orbit0_k14_interface.py")
COVER_PATH = K14_PATH.parent / "results_k16_anchor_cover.json"
LITERAL_PATH = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
                / "results_orbit0_k16_literal_residual.json")
OUT = HERE / "results_k16_streaming_prefix.json"
PACKET_OUT = HERE / "packet_k16_lex_q.json"
CHECKPOINT = HERE / "checkpoint_k16_local_peel.json"

Q = bytes.fromhex("000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3")
R8 = bytes.fromhex("000d1955627597c4c6e0e6f3")
PACKET = bytes.fromhex("00040875797dcfd3d7eaeef2")
EXPECTED_PIVOTS = {
    (0, 1, 0, 0), (0, 2, 0, 0),
    (1, 0, 0, 0), (1, 1, 0, 0), (1, 2, 0, 0),
    (2, 0, 0, 0), (2, 1, 0, 0), (2, 2, 0, 0),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


SPEC = importlib.util.spec_from_file_location("k14_interface", K14_PATH)
K14 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(K14)
F = K14.FROZEN


def divides(row: bytes, divisor: bytes) -> bool:
    left = Counter(row)
    return all(left[cell] >= count for cell, count in Counter(divisor).items())


def quotient(row: bytes, divisor: bytes) -> bytes:
    counts = Counter(row)
    counts.subtract(divisor)
    require(all(value >= 0 for value in counts.values()),
            (row.hex(), divisor.hex(), "nondividing quotient"))
    return bytes(sorted(cell for cell, count in counts.items()
                        for _ in range(count)))


def exact_rank(columns, rows):
    """Small exact rational rank, with columns given as row->coefficient maps."""
    matrix = [[Fraction(column.get(row, 0)) for column in columns]
              for row in rows]
    rank = 0
    width = len(columns)
    for col in range(width):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][col]:
                continue
            scale = matrix[i][col]
            matrix[i] = [left - scale * right
                         for left, right in zip(matrix[i], matrix[rank], strict=True)]
        rank += 1
    return rank


def literal_metadata_prefix():
    """Read only the small JSON prefix before the 1.8m literal-orbit array."""
    with LITERAL_PATH.open("rb") as handle:
        prefix = handle.read(1 << 20)
    def field(name):
        match = re.search(rb'"' + name.encode() + rb'"\s*:\s*([0-9]+)', prefix)
        require(match is not None, (name, "missing from prefix"))
        return int(match.group(1))
    return {
        "labelled_support_after_collection": field("labelled_support_after_collection"),
        "irreducible_K16_tail_occurrences_before_collection": field(
            "irreducible_K16_tail_occurrences_before_collection"),
        "nonzero_literal_H_orbits_after_collection": field(
            "nonzero_literal_H_orbits_after_collection"),
        "nonzero_anchor_signature_orbits_after_collection": field(
            "nonzero_anchor_signature_orbits_after_collection"),
    }


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def peel(columns, stop_after=None, state=None):
    """Deterministic leaf peel, serializable after every pivot."""
    if state is None:
        active = set(range(len(columns)))
        ledger = []
    else:
        active = set(state["active_columns"])
        ledger = list(state["ledger"])
    while active and (stop_after is None or len(ledger) < stop_after):
        owners = {}
        for index in active:
            for row in columns[index]:
                owners.setdefault(row, []).append(index)
        leaves = sorted((row, incident[0]) for row, incident in owners.items()
                        if len(incident) == 1)
        if not leaves:
            break
        row, index = leaves[0]
        ledger.append({"column": index, "pivot_row": row.hex(),
                       "coefficient": columns[index][row]})
        active.remove(index)
        atomic_json(CHECKPOINT, {
            "schema": "k16-local-peel-v1",
            "active_columns": sorted(active),
            "ledger": ledger,
        })
    return {"active_columns": sorted(active), "ledger": ledger}


def build():
    require(Q == bytes(sorted(R8 + PACKET)), "q factor split failed")
    require(len(Q) == 24 and F.row_k_degree(Q) == 14,
            (len(Q), F.row_k_degree(Q)))

    mixed = []
    for pair_colours in product(range(3), repeat=4):
        if len(set(pair_colours)) == 1:
            continue
        word = F.word_from_pair_colours(pair_colours)
        anchor = F.BASE.term_ids(word, F.M0)
        terms = F.BASE.word_terms(word)
        profile = Counter(F.row_k_degree(term) for term in terms)
        require(profile == {0: 1, 2: 12, 3: 32, 4: 60},
                (pair_colours, profile))
        mixed.append((pair_colours, word, anchor, terms))
    require(len(mixed) == 78, len(mixed))

    pivots = [record for record in mixed if divides(Q, record[2])]
    require({record[0] for record in pivots} == EXPECTED_PIVOTS,
            [record[0] for record in pivots])

    # A generator column is streamed from (q, anchor, source word): no product
    # packet is materialized.  Each yielded row retains its matching index and
    # physical matching, which is enough to replay it against word_terms.
    column_records = []
    B_columns = []
    all_rows = Counter()
    for pair_colours, word, anchor, terms in pivots:
        multiplier = quotient(Q, anchor)
        emitted = []
        degree_profile = Counter()
        B = Counter()
        for matching_index, (matching, term) in enumerate(
                zip(F.BASE.PM8, terms, strict=True)):
            row = bytes(sorted(multiplier + term))
            degree = F.row_k_degree(row)
            degree_profile[degree] += 1
            if degree == 16:
                B[row] += 1
                all_rows[row] += 1
                emitted.append({
                    "row": row.hex(),
                    "coefficient": 1,
                    "matching_index": matching_index,
                    "physical_matching": [list(edge) for edge in matching],
                    "generator_term": term.hex(),
                })
        require(degree_profile == {14: 1, 16: 12, 17: 32, 18: 60},
                (pair_colours, degree_profile))
        require(len(B) == 12, (pair_colours, len(B)))
        B_columns.append(B)
        column_records.append({
            "pair_colours": "".join(map(str, pair_colours)),
            "word": "".join(map(str, word)),
            "anchor": anchor.hex(),
            "multiplier": multiplier.hex(),
            "head": Q.hex(),
            "degree_profile": {str(k): v for k, v in sorted(degree_profile.items())},
            "k16_terms": emitted,
        })

    rows = tuple(sorted(all_rows))
    require(len(rows) == 42, len(rows))
    require(Counter(all_rows.values()) == {1: 16, 2: 8, 3: 16, 8: 2},
            Counter(all_rows.values()))
    private_per_column = [sum(all_rows[row] == 1 for row in column)
                          for column in B_columns]
    require(private_per_column == [2] * 8, private_per_column)
    B_rank = exact_rank(B_columns, rows)
    require(B_rank == 8, B_rank)

    # The common K14 head has rank one.  Use differences from column zero as
    # an explicit basis of its seven-dimensional kernel and transfer it to B.
    transfer = []
    for index in range(1, 8):
        difference = Counter(B_columns[index])
        difference.subtract(B_columns[0])
        transfer.append(Counter({row: value for row, value in difference.items()
                                 if value}))
    transfer_rank = exact_rank(transfer, rows)
    require(transfer_rank == 7, transfer_rank)

    all_anchors = tuple(record[2] for record in mixed)
    immediately_reducible = {
        row for row in rows if any(divides(row, anchor) for anchor in all_anchors)
    }
    require(len(immediately_reducible) == 16, len(immediately_reducible))
    require(all(all_rows[row] == 1 for row in immediately_reducible),
            "a reducible local row was not private")

    factor_anchors = tuple(F.BASE.term_ids(
        F.word_from_pair_colours(pair_colours), F.M0)
        for pair_colours in F.PAIR_COLOURS)
    factor_stabilizer = tuple(
        action for action in range(len(F.EXPORT.STABILIZER))
        if frozenset(F.move_row(term, action) for term in factor_anchors)
        == frozenset(factor_anchors)
    )
    require(len(factor_stabilizer) == 384, len(factor_stabilizer))
    q_stabilizer = tuple(action for action in factor_stabilizer
                         if F.move_row(Q, action) == Q)
    require(len(q_stabilizer) == 1, len(q_stabilizer))

    anchor_order = tuple(sorted(F.A))
    anchor_position = {cell: index for index, cell in enumerate(anchor_order)}
    signature_permutations = []
    for action in factor_stabilizer:
        transform = F.EXPORT.TRANSFORMS[action]
        signature_permutations.append(tuple(anchor_position[transform[cell]]
                                            for cell in anchor_order))

    def signature(row):
        counts = Counter(row)
        return tuple(counts[cell] for cell in anchor_order)

    def canonical_signature(value):
        images = []
        for permutation in signature_permutations:
            moved = [0] * 12
            for old, new in enumerate(permutation):
                moved[new] = value[old]
            images.append(tuple(moved))
        return min(images)

    signature_counts = Counter(signature(row) for row in rows)
    canonical_signature_counts = Counter(canonical_signature(signature(row))
                                         for row in rows)
    cover_json = json.loads(COVER_PATH.read_text())
    cover = {ast.literal_eval(item) for item in
             cover_json["single_pivot_cover"]["minimum_cover_orbit_representatives"]}
    local_cover_overlap = sorted(set(canonical_signature_counts) & cover)

    # Validate restart plumbing: interrupt after four leaves, reload the
    # checkpoint, and demand the same terminal ledger as an uninterrupted run.
    if CHECKPOINT.exists():
        CHECKPOINT.unlink()
    partial = peel(B_columns, stop_after=4)
    require(len(partial["ledger"]) == 4, partial)
    resumed = peel(B_columns, state=json.loads(CHECKPOINT.read_text()))
    require(not resumed["active_columns"] and len(resumed["ledger"]) == 8,
            resumed)
    uninterrupted = peel(B_columns)
    require(resumed["ledger"] == uninterrupted["ledger"],
            "resumed leaf ledger differs from uninterrupted ledger")

    literal_metadata = literal_metadata_prefix()
    require(literal_metadata == {
        "labelled_support_after_collection": 701717184,
        "irreducible_K16_tail_occurrences_before_collection": 3740320,
        "nonzero_literal_H_orbits_after_collection": 1848174,
        "nonzero_anchor_signature_orbits_after_collection": 25,
    }, literal_metadata)

    packet = {
        "schema": "orbit0-k16-lex-q-provider-v1",
        "q": Q.hex(),
        "factor_r8": R8.hex(),
        "factor_packet": PACKET.hex(),
        "columns": column_records,
        "row_owner_counts": {row.hex(): all_rows[row] for row in rows},
        "immediately_reducible_rows": sorted(row.hex()
                                               for row in immediately_reducible),
    }
    packet_logical = sha256(json.dumps(packet, sort_keys=True,
                                       separators=(",", ":")).encode()).hexdigest()
    packet["logical_sha256"] = packet_logical
    atomic_json(PACKET_OUT, packet)

    column_digest = sha256("\n".join(
        f"{record['pair_colours']}:{record['anchor']}:{record['multiplier']}:" +
        ",".join(term["row"] for term in record["k16_terms"])
        for record in column_records
    ).encode()).hexdigest()
    row_digest = sha256("\n".join(row.hex() for row in rows).encode()).hexdigest()

    result = {
        "status": "PASS exact local K16 streaming-provider and restart audit",
        "scope": {
            "theorem": (
                "For Tail's fixed lex K14 row q, exactly eight normalized mixed "
                "source columns divide q. Their literal provider emits 12 K16 "
                "tails apiece, 42 distinct rows, and preserves word/matching/"
                "multiplier provenance without materializing a product packet."
            ),
            "guard": (
                "This validates one literal component, not the complete K<=16 "
                "closure and not K16 ideal membership. The 25 signatures are a "
                "lossy anchor projection. Since Stab_H(q) is trivial, H quotient "
                "transport must carry q and its source column together."
            ),
        },
        "source": {
            "q": Q.hex(),
            "r8_factor": R8.hex(),
            "packet_factor": PACKET.hex(),
            "mixed_generators": 78,
            "dividing_pivots": [record["pair_colours"] for record in column_records],
            "columns": 8,
            "terms_streamed_per_full_column": 105,
            "terms_retained_per_K_le_16_column": 13,
            "K16_tails_per_column": 12,
        },
        "local_K16_matrix": {
            "raw_tail_occurrences": 96,
            "distinct_rows": len(rows),
            "row_owner_histogram": {str(k): v for k, v in
                                    sorted(Counter(all_rows.values()).items())},
            "private_rows_per_column": private_per_column,
            "rank_B_over_Q": B_rank,
            "common_K14_head_rank": 1,
            "head_kernel_dimension": 7,
            "rank_of_B_on_explicit_head_kernel": transfer_rank,
            "immediately_K0_reducible_rows": len(immediately_reducible),
            "irreducible_rows_at_this_shell": len(rows) - len(immediately_reducible),
            "lower_kernel_coupling": (
                "The raw private-row proof makes B injective, but all 16 private "
                "rows are themselves K0-pivotable. Eliminating them creates the "
                "next filtration tails. Thus a full closure must retain the seven "
                "head-kernel transfer directions; the 42x8 shell cannot be "
                "terminally peeled in isolation."
            ),
        },
        "symmetry_projection": {
            "factor_stabilizer_order": len(factor_stabilizer),
            "q_stabilizer_order_inside_H": len(q_stabilizer),
            "literal_local_H_row_orbits": len({
                min(F.move_row(row, action) for action in factor_stabilizer)
                for row in rows
            }),
            "literal_anchor_signatures": len(signature_counts),
            "canonical_anchor_signature_orbits": len(canonical_signature_counts),
            "canonical_signature_multiplicity_histogram": {
                str(k): v for k, v in
                sorted(Counter(canonical_signature_counts.values()).items())
            },
            "overlap_with_frozen_25_projected_cover": len(local_cover_overlap),
            "guard": (
                "The local shell contains reducible as well as irreducible tails; "
                "only two of its nine canonical signature types are members of "
                "the selected global 25-orbit irreducible cover."
            ),
        },
        "restartable_peel": {
            "checkpoint_schema": "k16-local-peel-v1",
            "interrupted_after": 4,
            "terminal_pivots": len(resumed["ledger"]),
            "terminal_active_columns": resumed["active_columns"],
            "restart_equals_uninterrupted": True,
            "ledger": resumed["ledger"],
        },
        "global_streaming_assessment": {
            **literal_metadata,
            "operator": (
                "Input (literal K14 q, scalar, pivot word, anchor, factor "
                "provenance); emit sorted((q-anchor)+tail) for the twelve K2 "
                "terms, with source word, matching index, multiplier and scalar."
            ),
            "working_memory_per_occurrence": "O(12 rows) plus an external keyed reducer",
            "positive_engineering_result": (
                "The 701,717,184 labelled rows admit lazy H-orbit expansion and "
                "the source operator itself is streaming. Exact coefficient "
                "collection requires an external sort/hash reducer; retaining "
                "only the 25 signatures is not provenance-safe."
            ),
            "frozen_closure_crosscheck": {
                "tail_complete_shell_seed_rows": 42,
                "tail_complete_shell_source_columns": 3625,
                "tail_complete_shell_K_le_16_rows": 67315,
                "tail_partial_BFS_rows_after_73_processed": 102110,
                "tail_partial_BFS_columns_after_73_processed": 5839,
                "tail_row_digest": "9a600ae283a0c18bbd9f69e63a0ff796380aade630c110aa9a60756ad520abbb",
                "tail_column_digest": "568baf144f2aede0c594806d358ac4a7eaafd0e5b7a4d2be224f2b4267aae912",
                "scope": "Tail-provided independent closure counts; not recomputed here.",
            },
        },
        "digests": {
            "packet_logical_sha256": packet_logical,
            "local_column_digest": column_digest,
            "local_row_digest": row_digest,
        },
        "pinned": {
            str(K14_PATH.relative_to(ROOT)): sha256(K14_PATH.read_bytes()).hexdigest(),
            str(COVER_PATH.relative_to(ROOT)): sha256(COVER_PATH.read_bytes()).hexdigest(),
            str(LITERAL_PATH.relative_to(ROOT)): sha256(LITERAL_PATH.read_bytes()).hexdigest(),
        },
    }
    return result


def main():
    result = build()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    atomic_json(OUT, result)
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        "packet_logical_sha256": result["digests"]["packet_logical_sha256"],
        "rows": result["local_K16_matrix"]["distinct_rows"],
        "columns": result["source"]["columns"],
        "rank_B": result["local_K16_matrix"]["rank_B_over_Q"],
        "transfer_rank": result["local_K16_matrix"]["rank_of_B_on_explicit_head_kernel"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
