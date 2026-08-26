#!/usr/bin/env python3
"""Exact finite replay of the lazy all-generator CEGAR membership theorem."""

from hashlib import sha256
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINE = ROOT / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
if str(FINE) not in sys.path:
    sys.path.insert(0, str(FINE))

from audit_closure22_joint_cegar import insert, projected_word, separating_dual
from audit_colour_holonomy_quotients import (
    PM8, key_add, matching_term, reduce_row, row_add, semigroup_key,
)
from audit_physical_graph_quotient import P, holonomy


RUST = FINE / "results_closure22_plus_full_profile71_joint_cegar_rust_p32003.json"
DUAL = FINE / "results_closure22_plus_full_profile71_rational_dual.json"
OUT = HERE / "results_lazy_full_generator_cegar.json"


def dot(row, functional):
    return sum(
        coefficient * functional.get(column, 0)
        for column, coefficient in row.items()
    ) % P


def restricted_eager_universe():
    rust = json.loads(RUST.read_text())
    exact_dual_record = json.loads(DUAL.read_text())
    support = {tuple(item["column"]) for item in exact_dual_record["dual"]}
    rows = {}
    quotient_candidates = 0
    for label in rust["source_words"]:
        generator = projected_word(tuple(map(int, label)))
        quotients = set()
        for column in support:
            for term in generator:
                quotient = tuple(a - b for a, b in zip(column, term))
                if min(quotient) >= 0:
                    quotients.add(quotient)
        quotient_candidates += len(quotients)
        for quotient in quotients:
            row = {}
            for term in generator:
                column = key_add(quotient, term)
                if column in support:
                    row_add(row, column, 1)
            if row:
                rows[tuple(sorted(row.items()))] = row

    cone = semigroup_key(matching_term((0,) * 8, PM8[0]))
    target = {}
    for term, coefficient in holonomy().items():
        column = key_add(cone, semigroup_key(term))
        if column in support:
            row_add(target, column, coefficient)
    stored_dual = {
        tuple(item["column"]): item["coefficient"] % P
        for item in exact_dual_record["dual"]
    }
    assert set(stored_dual) == support
    assert len(support) == 196
    assert len(rows) == 387
    assert len(target) == 3
    assert all(dot(row, stored_dual) == 0 for row in rows.values())
    assert dot(target, stored_dual) == exact_dual_record["target_pairing"] % P == 2
    return rust, exact_dual_record, support, list(rows.values()), target, quotient_candidates, stored_dual


def eager_reduce(rows, target):
    basis = {}
    for row in rows:
        insert(dict(row), basis)
    remainder = reduce_row(dict(target), basis)
    return basis, remainder


def lazy_reduce(rows, target):
    basis = {}
    rounds = []
    while True:
        remainder = reduce_row(dict(target), basis)
        if not remainder:
            return basis, remainder, rounds, "target reduced to zero", {}
        functional = separating_dual(basis, remainder)
        crossing = [row for row in rows if dot(row, functional)]
        rank_before = len(basis)
        for row in crossing:
            insert(dict(row), basis)
        rounds.append({
            "round": len(rounds) + 1,
            "crossing_rows": len(crossing),
            "independent_rows_added": len(basis) - rank_before,
            "rank_after": len(basis),
        })
        if len(basis) == rank_before:
            assert not crossing
            return basis, remainder, rounds, "global separator stall", functional


def proportional(left, right, columns):
    pivot = next(column for column in columns if right.get(column, 0))
    scale = left.get(pivot, 0) * pow(right[pivot], P - 2, P) % P
    return scale and all(
        left.get(column, 0) == scale * right.get(column, 0) % P
        for column in columns
    )


def audit():
    (
        rust, exact_dual_record, support, rows, target,
        quotient_candidates, stored_dual,
    ) = restricted_eager_universe()
    eager_basis, eager_remainder = eager_reduce(rows, target)
    assert len(eager_basis) == 195
    assert len(eager_remainder) == 1

    lazy_basis, lazy_remainder, rounds, terminal, lazy_dual = lazy_reduce(rows, target)
    assert terminal == "global separator stall"
    assert len(rounds) == 13
    assert len(lazy_basis) == len(eager_basis) == 195
    assert len(lazy_remainder) == len(eager_remainder) == 1
    assert not rounds[-1]["crossing_rows"]
    assert all(dot(row, lazy_dual) == 0 for row in rows)
    assert dot(target, lazy_dual) != 0
    assert proportional(lazy_dual, stored_dual, support)

    # Positive direction on the same row universe: manufacture a target in
    # the eager span.  Starting again from V_0=0 must reach remainder zero.
    member_target = dict(rows[0])
    for column, coefficient in rows[1].items():
        row_add(member_target, column, 2 * coefficient)
    member_basis, member_remainder, member_rounds, member_terminal, _ = lazy_reduce(
        rows, member_target
    )
    assert not member_remainder
    assert member_terminal == "target reduced to zero"

    result = {
        "status": "PASS lazy full-generator CEGAR theorem and full71 replay",
        "theorem": {
            "ambient": "finite-dimensional vector space E over a field k",
            "full_row_pool": "finite R, with W=span_k(R)",
            "initialization": "any V_0 subseteq W; V_0=0 is allowed",
            "separator": "lambda(V_i)=0 and lambda(t)!=0 whenever t notin V_i",
            "update": "V_(i+1)=span(V_i union {r in R: lambda(r)!=0})",
            "stall_equivalence": (
                "At a nonmember iteration, no crossing row iff lambda(R)=0; "
                "equivalently lambda annihilates W and separates t from W."
            ),
            "termination_bound": "at most dim(W)-dim(V_0) nonstall rounds",
            "terminal_dichotomy": (
                "remainder zero iff t is in W; separator stall iff t is not in W"
            ),
            "target_touching_seed_required": False,
        },
        "proof_guards": {
            "V0_must_lie_in_W": (
                "Otherwise target reduction may use extraneous rows and proves "
                "membership only in W+V0."
            ),
            "scanner_must_cover_all_R": (
                "A stall certifies only the span of the rows actually scanned."
            ),
            "field_scope": (
                "The theorem is field-by-field. Modular membership needs Q replay; "
                "modular nonmembership needs an exact lifted dual to certify char0."
            ),
            "row_addition": (
                "Every crossing row is outside V_i because lambda annihilates V_i, "
                "so a nonstall round strictly raises dimension."
            ),
        },
        "full71_support_replay": {
            "source_words": len(rust["source_words"]),
            "exact_dual_support_columns": len(support),
            "translation_quotient_candidates_touching_support": quotient_candidates,
            "distinct_restricted_eager_rows": len(rows),
            "restricted_target_columns": len(target),
            "eager_rank": len(eager_basis),
            "eager_remainder_terms": len(eager_remainder),
            "lazy_initial_rank": 0,
            "lazy_rounds_including_terminal_scan": len(rounds),
            "lazy_rank": len(lazy_basis),
            "lazy_remainder_terms": len(lazy_remainder),
            "lazy_terminal": terminal,
            "lazy_terminal_dual_matches_stored_exact_dual_up_to_scalar": True,
            "stored_exact_target_pairing": exact_dual_record["target_pairing"],
            "rounds": rounds,
        },
        "positive_control": {
            "target": "row_0 + 2 row_1 in the same 387-row eager universe",
            "initial_rank": 0,
            "terminal": member_terminal,
            "rounds": len(member_rounds),
            "final_rank": len(member_basis),
            "remainder_terms": len(member_remainder),
        },
        "initialization_verdict": (
            "No target-touching initialization is needed for correctness. It is "
            "only a performance heuristic; the exact replay starts from V_0=0."
        ),
        "target_definition_reconciliation": {
            "unconed_literal_holonomy": (
                "stabilizer S2({3,4}) x S3({5,6,7}), order 12, trivial character"
            ),
            "coned_holonomy_with_fixed_01_23_45_67_pure_matching": (
                "stabilizer {id,(6 7)}, order 2, trivial character"
            ),
            "cegar_dependency": "none; the correctness proof uses only linear spans",
        },
        "source_digests": {
            "rust_full71": sha256(RUST.read_bytes()).hexdigest(),
            "exact_dual": sha256(DUAL.read_bytes()).hexdigest(),
        },
        "scope": (
            "The 196-column replay is the coordinate restriction supported by "
            "the known exact full-profile71 dual. It exhausts every restricted "
            "translation of the stored 62-word pool and compares lazy closure "
            "with eager span exactly over F_32003."
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(canonical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_results:
        if not OUT.exists() or OUT.read_text() != rendered:
            print("frozen result mismatch", file=sys.stderr)
            return 1
        print(result["status"], result["logical_sha256"])
        return 0
    OUT.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
