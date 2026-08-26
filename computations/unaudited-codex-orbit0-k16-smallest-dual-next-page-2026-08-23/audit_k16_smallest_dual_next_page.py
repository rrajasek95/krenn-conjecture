#!/usr/bin/env python3
"""One exact next attachment of the smallest K16 replacement dual."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIOUS_DIR = (ROOT / "computations"
                / "unaudited-codex-orbit0-k16-second-page-duals-2026-08-23")
PREVIOUS_SCRIPT = PREVIOUS_DIR / "audit_k16_second_page_duals.py"
PREVIOUS_RESULT = PREVIOUS_DIR / "results_k16_second_page_duals.json"
RESULT = HERE / "results_k16_smallest_dual_next_page.json"


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


PREVIOUS = load("orbit0_k16_smallest_next_previous", PREVIOUS_SCRIPT)
F = PREVIOUS.F
D24 = PREVIOUS.D24


def incident_columns(rows):
    answer = set()
    for row in rows:
        answer.update(D24.incident_degree24_columns(row))
    return answer


def factor_stabilizer():
    words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words)
    anchor_set = frozenset(anchors)
    answer = tuple(
        action for action in range(len(F.EXPORT.STABILIZER))
        if frozenset(F.move_row(term, action) for term in anchors) == anchor_set
    )
    require(len(answer) == 384, len(answer))
    return answer


def move_column(column, action):
    word, multiplier = column
    sites, colours = F.EXPORT.STABILIZER[action]
    moved_word = [None] * 8
    for old_site in range(8):
        moved_word[sites[old_site]] = colours[word[old_site]]
    transform = F.EXPORT.TRANSFORMS[action]
    moved_multiplier = bytes(sorted(transform[cell] for cell in multiplier))
    return tuple(moved_word), moved_multiplier


def canonical_column(column, actions):
    return min((move_column(column, action) for action in actions), key=repr)


def fraction_record(value):
    return [value.numerator, value.denominator]


def build(mutate=False):
    require(file_sha256(PREVIOUS_SCRIPT)
            == "0d308c757fed5200b188ebc971ad8b3277b259020696e4377bfa236bb871fc92",
            "previous checker drift")
    require(file_sha256(PREVIOUS_RESULT)
            == "4b59d6972448780699ef2a66a2ad85041f149cdde656914f6d3d5faea675aebf",
            "previous replacement-dual ledger drift")
    previous = json.loads(PREVIOUS_RESULT.read_text())
    require(previous["logical_sha256"]
            == "65ff0ce73034f302ad2022d983b2e366e4d1226c4f1f7b26a7773fe6f1280b66",
            "previous logical theorem drift")

    replacement = previous["smallest_replacement_extended_dual"]
    type_index = replacement["type_index"]
    require(type_index == 6 and len(replacement["support"]) == 4,
            "smallest replacement dual changed")
    q = bytes.fromhex(replacement["literal_factorized_q"])
    old_support = tuple(bytes.fromhex(record["row"])
                        for record in previous["types"][type_index]
                        ["literal_dual_support"])
    replacement_support = tuple(bytes.fromhex(record["row"])
                                for record in replacement["support"])
    replacement_values = {
        bytes.fromhex(record["row"]): Fraction(*record["coefficient"])
        for record in replacement["support"]
    }
    require(len(old_support) == 6 and len(replacement_support) == 4
            and replacement_values[q] == 1,
            "support interface changed")

    old_columns = incident_columns(old_support)
    attachment_columns = incident_columns(replacement_support)
    added_columns = attachment_columns - old_columns
    if mutate:
        added_columns.remove(min(added_columns, key=repr))
    all_columns = old_columns | attachment_columns
    if mutate:
        all_columns = old_columns | added_columns
    require(len(old_columns) == 327
            and len(attachment_columns) == 247
            and len(old_columns & attachment_columns) == 5
            and len(added_columns) == 242
            and len(all_columns) == 569,
            "hostile mutation/next attachment census changed")

    ordered_columns = tuple(sorted(all_columns, key=repr))
    complete_vectors = []
    rows = set()
    minimum_histogram = Counter()
    total_nnz = 0
    for column in ordered_columns:
        outputs = Counter(D24.degree24_column_rows(column))
        degrees = {row: D24.row_k_degree(row) for row in outputs}
        minimum_histogram[min(degrees.values())] += 1
        vector = {row: multiplicity for row, multiplicity in outputs.items()
                  if degrees[row] <= 16}
        complete_vectors.append(vector)
        rows.update(vector)
        total_nnz += len(vector)
    require(len(rows) == 19495 and total_nnz == 24843
            and minimum_histogram
            == Counter({10: 2, 11: 2, 12: 40, 13: 31,
                        14: 210, 15: 103, 16: 181}),
            "complete K<=16 attachment changed")

    rank, target_remainder, next_dual = PREVIOUS.sparse_row_span(
        tuple(complete_vectors), {q: Fraction(1)})
    target_member = not target_remainder
    require(rank == 436 and not target_member
            and len(target_remainder) == 11 and len(next_dual) == 23,
            (rank, len(target_remainder), len(next_dual)))
    degree_profile = Counter(D24.row_k_degree(row) for row in next_dual)
    coefficient_profile = Counter(str(value) for value in next_dual.values())
    require(degree_profile == Counter({10: 2, 11: 1, 12: 9,
                                       13: 3, 14: 5, 16: 3})
            and coefficient_profile == Counter({"-1": 16, "1": 7}),
            "next dual profile changed")

    # Audit the requested H-canonical interface without replacing the literal
    # rank calculation by an unsound signature quotient.
    actions = factor_stabilizer()
    orbit_ledgers = {}
    for label, columns in (
            ("old_page", old_columns),
            ("replacement_support_page", attachment_columns),
            ("new_columns", added_columns),
            ("adjoined_union", all_columns)):
        canonical = Counter(canonical_column(column, actions)
                            for column in columns)
        orbit_ledgers[label] = {
            "literal_columns": len(columns),
            "H_canonical_column_orbits": len(canonical),
            "intersection_multiplicity_histogram": {
                str(key): value for key, value
                in sorted(Counter(canonical.values()).items())
            },
        }
    require(all(record["literal_columns"]
                == record["H_canonical_column_orbits"]
                for record in orbit_ledgers.values()),
            "unexpected H compression in local attachment")

    next_support = [
        {
            "row": row.hex(),
            "coefficient": fraction_record(value),
            "K_degree": D24.row_k_degree(row),
        }
        for row, value in sorted(next_dual.items())
    ]
    next_digest = sha256(json.dumps(next_support, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()
    payload = {
        "format": "n8-orbit0-k16-smallest-dual-next-page-v1",
        "status": "FOUR_ROW_CLASS_STAYS_SPARSE_AFTER_ONE_EXACT_ATTACHMENT",
        "input": {
            "previous_type_index": type_index,
            "canonical_anchor_signature": replacement["canonical_anchor_signature"],
            "literal_q": q.hex(),
            "old_dual_support": len(old_support),
            "replacement_dual_support": len(replacement_support),
            "replacement_dual": replacement["support"],
        },
        "one_page_attachment": {
            "old_page_columns": len(old_columns),
            "replacement_support_incident_columns": len(attachment_columns),
            "overlap_columns": len(old_columns & attachment_columns),
            "new_columns": len(added_columns),
            "adjoined_columns": len(all_columns),
            "complete_K_le_16_rows": len(rows),
            "matrix_nnz": total_nnz,
            "minimum_K_degree_histogram": {
                str(key): value for key, value in sorted(minimum_histogram.items())
            },
            "column_rank_over_Q": rank,
            "target_augmented_rank_over_Q": rank + int(not target_member),
            "q_in_column_span": target_member,
            "target_remainder_support": len(target_remainder),
        },
        "H_canonical_census": orbit_ledgers,
        "next_dual": {
            "support_size": len(next_support),
            "K_degree_profile": {
                str(key): value for key, value in sorted(degree_profile.items())
            },
            "coefficient_profile": dict(sorted(coefficient_profile.items())),
            "support": next_support,
            "support_logical_sha256": next_digest,
            "normalization": "annihilates all 569 adjoined columns and pairs q to 1",
        },
        "classification": {
            "verdict": "STAYS_SPARSE_ON_THIS_PAGE",
            "reason": (
                "The four-row class does not fill: augmented rank is 437 versus "
                "column rank 436. Its exact replacement grows only to 23 rows "
                "with coefficients +/-1, so it remains a compact obstruction "
                "after this one attachment."
            ),
            "frontier_warning": (
                "The page already spans K10 through K16, has 19,495 rows, and "
                "all 569 literal columns remain distinct under H-canonicalization. "
                "This predicts a broad next frontier, but no incident column of "
                "the 23-row dual and no second page is enumerated."
            ),
        },
        "scope_guard": (
            "Exact for the union of the prior first-page columns and every "
            "literal source column incident to the exported four-row replacement "
            "dual, with complete outputs through K16. No second attachment, full "
            "component, 701m residual, localization, or other chart is tested."
        ),
        "pinned": {
            str(PREVIOUS_SCRIPT.relative_to(ROOT)): file_sha256(PREVIOUS_SCRIPT),
            str(PREVIOUS_RESULT.relative_to(ROOT)): file_sha256(PREVIOUS_RESULT),
        },
    }
    logical = sha256(json.dumps(payload, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    payload = build(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "logical_sha256": payload["logical_sha256"],
        "one_page_attachment": payload["one_page_attachment"],
        "next_dual": {
            key: value for key, value in payload["next_dual"].items()
            if key != "support"
        },
        "classification": payload["classification"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
