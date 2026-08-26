#!/usr/bin/env python3
"""Structural descent audit for chart 1 with A_02[0,0]=0."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORT = (ROOT / "computations/unaudited-codex-n8-chart1-boundary-a0200-2026-08-23"
          / "results_chart1_boundary_export.json")
ROOT_D12 = (ROOT / "computations/unaudited-codex-n8-chart1-boundary-a0200-2026-08-23"
            / "results_d12_root_interface.json")
D12_CHECKPOINT = (ROOT / "computations/unaudited-codex-n8-chart1-boundary-a0200-2026-08-23"
                  / "checkpoint_d12_lazy_cegar.json")
SPK6 = (ROOT / "computations/unaudited-codex-n8-orbit26-minlayer-spk6-audit-2026-08-23"
        / "REPORT.md")
HOLE = ROOT / "notes/matching-hole-zero-cross-pfaffian-obstruction.md"
RESPONSE = (ROOT / "computations/unaudited-codex-response-star-2026-08-20"
            / "response_star_core.py")
EXPECTED = {
    EXPORT: "63a581a7277b21124c12c0cdb920772f934299eb901de39474fda3df586bdd0b",
    ROOT_D12: "66d6ef2bddc1185850a3ccd075cc218f6b4758edc4c14acf06826975f8adb602",
    D12_CHECKPOINT: "1ddd96e2cad9cf132336db0b68d208292554b96d4acb2df1879dd6f0e7db366f",
    SPK6: "03710d76e799e25e58107d9aa702b3848de32a65b4d6bb7b479b9a424ecdd884",
    HOLE: "4bd77fe4861202483c9028e045738d22696770ffc3cb7ba95202972507bf105e",
    RESPONSE: "89aa79a15fd9a98b16529cf69f8158b348d68902729cde0ea24b363fce5f2c59",
}
RESULT = HERE / "results_chart1_boundary_structural_descent.json"
PRIMES = (1009, 1013)
ANCHOR_MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))
BOUNDARY_EDGE = (0, 2)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(tuple(sorted(matching))
                  for matching in perfect_matchings(range(8)))
require(len(MATCHINGS) == 105, "K8 matching count")


def survives(word, matching):
    return not (BOUNDARY_EDGE in matching and word[0] == word[2] == 0)


def row_census(mutate=False):
    histogram = Counter()
    constant_rows = 0
    affected = 0
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        count = sum(survives(word, matching) for matching in MATCHINGS)
        histogram[count] += 1
        affected += count == 90
        if all(word[u] == word[v] for u, v in ANCHOR_MATCHING):
            constant_rows += 1
    if mutate:
        histogram[90] -= 1
    require(histogram == {90: 728, 105: 5830}, histogram)
    require((affected, constant_rows) == (728, 78),
            (affected, constant_rows))
    return histogram, constant_rows


def tail_decomposition():
    tail = (6, 7)
    record = Counter()
    per_colour = {}
    for colour in range(3):
        local = Counter()
        for residual_word in product(range(3), repeat=6):
            word = residual_word + (colour, colour)
            common = sum(tail in matching and survives(word, matching)
                         for matching in MATCHINGS)
            crossing = sum(tail not in matching and survives(word, matching)
                           for matching in MATCHINGS)
            is_pure = all(value == colour for value in residual_word)
            key = ("pure" if is_pure else "mixed", common, crossing)
            local[key] += 1
            record[key] += 1
        per_colour[str(colour)] = {
            f"{kind}:{common}+{crossing}": count
            for (kind, common, crossing), count in sorted(local.items())
        }
    require(record == {
        ("mixed", 12, 78): 242,
        ("mixed", 15, 90): 1942,
        ("pure", 12, 78): 1,
        ("pure", 15, 90): 2,
    }, record)

    word = (0, 0, 0, 0, 0, 0, 1, 1)
    common = [matching for matching in MATCHINGS
              if (6, 7) in matching and survives(word, matching)]
    crossing = [matching for matching in MATCHINGS
                if (6, 7) not in matching and survives(word, matching)]
    explicit = tuple(sorted(((0, 6), (1, 7), (2, 3), (4, 5))))
    require((len(common), len(crossing), explicit in crossing) == (12, 78, True),
            (len(common), len(crossing), explicit in crossing))
    deleted_common = sum((6, 7) in matching and BOUNDARY_EDGE in matching
                         for matching in MATCHINGS)
    deleted_crossing = sum((6, 7) not in matching and BOUNDARY_EDGE in matching
                           for matching in MATCHINGS)
    require((deleted_common, deleted_crossing) == (3, 12),
            (deleted_common, deleted_crossing))
    return {
        "all_lifted_rows": {
            f"{kind}:{common}+{crossing}": count
            for (kind, common, crossing), count in sorted(record.items())
        },
        "per_endpoint_colour": per_colour,
        "boundary_deletes": {
            "common_tail_terms": deleted_common,
            "crossing_tail_terms": deleted_crossing,
        },
        "explicit_word": "00000011",
        "explicit_common_tail_terms": len(common),
        "explicit_crossing_tail_terms": len(crossing),
        "surviving_crossing_matching": [list(edge) for edge in explicit],
        "surviving_crossing_monomial": (
            "A_06[0,1] A_17[0,1] A_23[0,0] A_45[0,0] "
            "= A_06[0,1] A_17[0,1] on chart 1"
        ),
    }


def source_value(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    if (u, v) in ANCHOR_MATCHING and a == b:
        return 1
    if (u, v, a, b) == (0, 2, 0, 0):
        return 0
    return 1 + ((37 * u + 53 * v + 7 * a + 11 * b
                 + 13 * u * v + 5 * a * b) % 29)


def determinant3(matrix):
    positive = {(0, 1, 2), (1, 2, 0), (2, 0, 1)}
    return sum((1 if sigma in positive else -1)
               * matrix[0][sigma[0]] * matrix[1][sigma[1]]
               * matrix[2][sigma[2]] for sigma in permutations(range(3)))


def sparse_rank(rows, prime):
    basis = {}
    for raw in rows:
        row = [value % prime for value in raw]
        while any(row):
            pivot = next(index for index, value in enumerate(row) if value)
            if pivot not in basis:
                inverse = pow(row[pivot], prime - 2, prime)
                basis[pivot] = [value * inverse % prime for value in row]
                break
            factor = row[pivot]
            row = [(left - factor * right) % prime
                   for left, right in zip(row, basis[pivot])]
        if len(basis) == 9:
            return 9
    return len(basis)


def response_row(p, q, a, b, alpha, beta):
    return [
        source_value(p, a, i, alpha) * source_value(q, b, j, beta)
        + source_value(p, b, i, beta) * source_value(q, a, j, alpha)
        for i in range(3) for j in range(3)
    ]


def dense_boundary_guard():
    edges = tuple(combinations(range(8), 2))
    determinants = {}
    for u, v in edges:
        matrix = [[source_value(u, v, a, b) for b in range(3)]
                  for a in range(3)]
        determinant = determinant3(matrix)
        require(determinant != 0, (u, v, matrix))
        determinants[f"{u}{v}"] = determinant
    rank_profiles = {}
    for prime in PRIMES:
        profile = Counter()
        for p, q in edges:
            residual = tuple(site for site in range(8) if site not in (p, q))
            for triangle in combinations(residual, 3):
                allowed = set(combinations(triangle, 2))
                rows = [response_row(p, q, a, b, alpha, beta)
                        for a, b in combinations(residual, 2)
                        if (a, b) not in allowed
                        for alpha in range(3) for beta in range(3)]
                require(len(rows) == 108, len(rows))
                profile[sparse_rank(rows, prime)] += 1
        require(profile == {9: 560}, (prime, profile))
        rank_profiles[str(prime)] = {str(rank): count
                                     for rank, count in sorted(profile.items())}
    nonzero_cells = sum(source_value(u, v, a, b) != 0
                        for u, v in edges
                        for a in range(3) for b in range(3))
    require(nonzero_cells == 251, nonzero_cells)
    return {
        "description": (
            "all chart anchors 1, A_02[0,0]=0, every other cell the displayed "
            "positive deterministic integer"
        ),
        "nonzero_cells": nonzero_cells,
        "zero_cells": ["A_02[0,0]"],
        "physical_block_determinants_nonzero": len(determinants),
        "physical_block_determinant_minmax": [
            min(determinants.values()), max(determinants.values())
        ],
        "triangle_response_rank_profiles": rank_profiles,
        "characteristic_zero_consequence": (
            "Each modular rank-nine witness is a nonzero 9x9 integer minor, "
            "so every one of the 560 literal triangle response matrices has "
            "rank nine over Q. Every 3x3 physical block is also exactly full rank."
        ),
    }


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift {path}")
    export = json.loads(EXPORT.read_text())
    root = json.loads(ROOT_D12.read_text())
    checkpoint = json.loads(D12_CHECKPOINT.read_text())
    histogram, constants = row_census(mutate)
    require(export["source"]["mixed_term_count_histogram"] ==
            {str(key): value for key, value in histogram.items()}, "export census")
    require(export["source"]["constant_mixed_generators"] == constants,
            "constant row census")
    require(root["status"] == "FINITE_ROOT_DUAL_KILLED_BY_NEXT_CELLS"
            and root["root_interface_rank"] == root["root_interface_columns"] == 18
            and root["finite_dual"]["new_violating_column_orbits"] == 130,
            "D12 root status changed")
    require(checkpoint["last_dual"] == [["0d55b8ee", 1, 1]]
            and checkpoint["ledger"][-1]["round"] == 6
            and checkpoint["ledger"][-1]["dual_support"] == 1
            and checkpoint["ledger"][-1]["new_violating_column_orbits"] == 42,
            "D12 round-six checkpoint changed")

    result = {
        "format": "n8-chart1-a0200-structural-descent-audit-v1",
        "status": "EXACT_NATURAL_DESCENTS_NOT_FORCED_BRANCH_REMAINS_OPEN",
        "branch": {
            "chart": 1,
            "anchors": "A_01[c,c]=A_23[c,c]=A_45[c,c]=A_67[c,c]=1",
            "boundary": "A_02[0,0]=0",
            "literal_mixed_rows": 6558,
            "term_count_histogram": {
                str(key): value for key, value in sorted(histogram.items())
            },
            "constant_mixed_rows": constants,
        },
        "exact_tail_cut": tail_decomposition(),
        "six_site_consequence": {
            "identity": (
                "For every u in {0,1,2}^6 and c, "
                "F_(u,c,c)=H6_boundary(u)+C_67(u,c), since A_67[c,c]=1."
            ),
            "on_X5": (
                "For the 728 mixed lifts in each endpoint colour, X5 gives "
                "H6_boundary(u)=-C_67(u,c), not H6_boundary(u)=0. The one "
                "omitted lift u=c^6 is a pure eight-site equation, and it too "
                "contains the crossing correction."
            ),
            "SPK6_failure": (
                "SP-K6 requires one common literal six-site array with all 729 "
                "coefficients equal to Delta_(6,3). The surviving 78/90-term "
                "crossing packets prevent that landing; the single boundary "
                "cell supplies no cancellation identity for them."
            ),
        },
        "dense_boundary_counterguard": dense_boundary_guard(),
        "mechanism_audit": {
            "clean_triangle_carrier": (
                "Not forced: the exact dense boundary guard has all 560 L_T "
                "of rank nine, so every blocker form is in each row span. This "
                "refutes boundary=>active triangle carrier; it does not classify "
                "wider cancellation-clean caps."
            ),
            "matching_hole_or_block": (
                "Not forced: the guard has only one zero among 252 cells and all "
                "28 physical 3x3 blocks full rank. The matching-hole theorem "
                "requires a full hole matching and a zero-cross mask, neither "
                "of which follows from A_02[0,0]=0."
            ),
            "six_site_descent": (
                "Not forced: the exact Laplace cut leaves 78 or 90 crossing "
                "terms. The displayed A_06[0,1]A_17[0,1] monomial is a literal "
                "survivor already in F_00000011."
            ),
        },
        "full_X5_interface_guard": {
            "D12_root_rows_columns_rank": [
                root["root_interface_rows"], root["root_interface_columns"],
                root["root_interface_rank"],
            ],
            "root_dual_support": root["finite_dual"]["support"],
            "root_dual_killers": root["finite_dual"]["new_violating_column_orbits"],
            "consequence": (
                "The first exact homogeneous constant-row projection does not "
                "close the branch: its five-row dual is killed by 130 literal "
                "next-column orbits. This is consistent with the crossing-tail "
                "obstruction and supplies no member/nonmember conclusion."
            ),
            "round6_checkpoint": {
                "dual_row": "0d55b8ee",
                "decoded_row": (
                    "A_02[1,1] A_14[1,1] A_36[1,1] A_57[1,1]"
                ),
                "dual_support": 1,
                "literal_next_column_killers": 42,
                "structural_consequence": (
                    "This row uses the live colour-one cell A_02[1,1], not the "
                    "vanishing A_02[0,0]. Factoring edge 02 from an eight-site "
                    "hafnian separates 15 containing-edge terms from 90 avoiding-"
                    "edge terms; multiplication by the displayed pure matching is "
                    "a cone, not a projection that erases the avoiding-edge sector."
                ),
            },
        },
        "remaining_exact_target": (
            "A source-labelled identity combining the full X5 rows so that, for "
            "one physical pair and all three endpoint colours, every crossing "
            "correction C_pq(u,c) cancels or becomes the response of one active "
            "clean cap. Without that same-source cancellation, neither SP-K6 nor "
            "the matching-hole theorem applies."
        ),
        "scope": (
            "The dense guard is not X5 and is used only to refute implications "
            "from the chart/boundary antecedent to rank/support descent. The row "
            "decomposition is an exact identity on all 6,558 source equations. "
            "No nonemptiness, ideal nonmembership, or conjecture claim is made."
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result drift")
    print(result["status"])
    print(result["dense_boundary_counterguard"]["triangle_response_rank_profiles"])
    print(result["logical_sha256"])


if __name__ == "__main__":
    main()
