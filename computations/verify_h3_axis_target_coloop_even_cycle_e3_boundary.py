#!/usr/bin/env python3
"""E3/E4 boundary of the h=3 single-even-cycle target-coloop exchange.

For coloop/outside matching bases M,N, let a,b be their complete five-word
evaluation vectors and h the exact source target vector.  The E3 matching-
exchange coefficients are the 3x3 minors det(a,b,h).  If one is nonzero,
perfect-matching expansion selects a third literal base K distinct from M,N.
Because M triangle N is one C6 or C8, every such K uses an edge outside the
two-base union.  It is therefore either off the selected three-anchor union
or explicitly carried by the third anchor/strict-Hall web.

If every E3 coefficient vanishes, a,b are independent by E2 and h lies in
their two-plane.  The checker freezes an exact five-row rational example of
this E3-flat holonomy.  E4 is the Laplace coherence among E3 minors and adds
no equation on the flat stratum.  This is a source-typed boundary, not a
physical full one-bad point.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_four_hole_exchange.py":
        "5283fae67a31ea3c9794fc8bbf351f7da5bc8251490dbdffbef04bde1f2a987f",
    "notes/h3-axis-target-coloop-four-hole-exchange.md":
        "9aa3a6e9315cc52769f0124188a17e69b6165fd45c04b21aa7203a4d70d5e341",
    "computations/verify_n8_chart26_c4_exchange_3cell.py":
        "4398d15df3a5f0b34c2745fdb7087a289452ed03983d22431c4f20d116f019c6",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "e96a469ff1e52b4bbe9fd60ec934552d131541c0e16dd2f279438e782a6b37de"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def rank(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def det3(first, second, third, indices):
    i, j, k = indices
    return (
        first[i] * (second[j] * third[k] - second[k] * third[j])
        - first[j] * (second[i] * third[k] - second[k] * third[i])
        + first[k] * (second[i] * third[j] - second[j] * third[i])
    )


def all_e3(first, second, third):
    return {indices: det3(first, second, third, indices)
            for indices in combinations(range(len(first)), 3)}


def audit_e3_rank_dichotomy():
    # Five exact source-word values: unary and the two diagonals are one;
    # the two crossed responses are zero.  The chosen coloop target is c=0.
    target = (Q(1), Q(0), Q(0), Q(1), Q(1))

    # E3-flat boundary.  The outside vector has zero target entry but is
    # nonzero on a crossed word.  E2 is active, while h=a+b makes every E3
    # determinant zero.
    a_flat = (Q(1), Q(1), Q(2), Q(3), Q(4))
    b_flat = tuple(target[index] - a_flat[index]
                   for index in range(5))
    require(b_flat[0] == 0 and b_flat[1] != 0,
            "the flat coloop/outside evaluations changed")
    delta_flat = a_flat[0] * b_flat[1] - a_flat[1] * b_flat[0]
    require(delta_flat == -1,
            "the flat boundary lost its nonzero E2 exchange")
    flat_e3 = all_e3(a_flat, b_flat, target)
    require(not any(flat_e3.values())
            and rank((a_flat, b_flat, target)) == 2,
            "the exact E3-flat word plane changed")

    # Rank-three branch: one perturbation makes a literal E3 coefficient
    # nonzero.  The determinant is the coefficient with which a third
    # matching base can survive after M,N cancel separately.
    a_curved = a_flat
    b_curved = list(b_flat)
    b_curved[2] += 1
    b_curved = tuple(b_curved)
    curved_e3 = all_e3(a_curved, b_curved, target)
    nonzero = {indices: value for indices, value in curved_e3.items()
               if value}
    require(rank((a_curved, b_curved, target)) == 3 and nonzero,
            "the curved word plane lost its E3 detector")

    # If a,b are independent (guaranteed by the nonzero target/outside E2
    # minor), all E3 vanish iff h lies in span(a,b).
    require(rank((a_flat, b_flat)) == 2,
            "the E2-flat matching pair became dependent")
    require((not any(flat_e3.values()))
            == (rank((a_flat, b_flat, target)) == 2),
            "E3 vanishing stopped detecting the two-base target plane")
    require((not any(curved_e3.values()))
            == (rank((a_curved, b_curved, target)) == 2),
            "E3 rank detection failed on the curved sample")

    # E4 is the row-Laplace identity among the four 3x3 minors.  Verify it
    # for every four-state subset and both matching rows, in both strata.
    e4_checks = 0
    for first, second, e3 in (
            (a_flat, b_flat, flat_e3),
            (a_curved, b_curved, curved_e3)):
        for indices in combinations(range(5), 4):
            c, d, e, f = indices
            # C_cde is det(a,b,h) on those indices.  The standard maximal-
            # minor signs are (-,+,-,+) after deleting c,d,e,f.
            for row in (first, second):
                value = (
                    row[c] * e3[(d, e, f)]
                    - row[d] * e3[(c, e, f)]
                    + row[e] * e3[(c, d, f)]
                    - row[f] * e3[(c, d, e)]
                )
                require(value == 0, "the E4 Laplace coherence changed")
                e4_checks += 1

    return {
        "source_target_vector": [str(value) for value in target],
        "flat_matching_M": [str(value) for value in a_flat],
        "flat_matching_N": [str(value) for value in b_flat],
        "flat_E2_minor": str(delta_flat),
        "flat_E3_nonzero_count": 0,
        "flat_three_row_rank": 2,
        "flat_relation": "H=M+N",
        "curved_E3_nonzero": {
            str(indices): str(value) for indices, value in nonzero.items()
        },
        "curved_three_row_rank": 3,
        "E4_checks": e4_checks,
        "E4_effect_on_flat_stratum": "identically zero",
    }


def cycle_lengths(first, second):
    common = set(first) & set(second)
    symmetric = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    lengths = []
    unseen = set(adjacency)
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            following = next(site for site in adjacency[current]
                             if site != previous)
            length += 1
            previous, current = current, following
            unseen.discard(previous)
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def audit_third_base_must_leave_cycle():
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "the K8 matching count changed")
    representatives = {
        "C8": (
            ((0, 6), (1, 7), (2, 3), (4, 5)),
            ((0, 4), (1, 5), (2, 6), (3, 7)),
        ),
        "C6": (
            ((0, 6), (1, 7), (2, 3), (4, 5)),
            ((0, 1), (2, 6), (3, 7), (4, 5)),
        ),
    }
    audits = {}
    for name, (first, second) in representatives.items():
        first, second = tuple(sorted(first)), tuple(sorted(second))
        expected_cycles = (8,) if name == "C8" else (6,)
        require(cycle_lengths(first, second) == expected_cycles,
                f"the {name} representative changed")
        union = set(first) | set(second)
        contained = tuple(matching for matching in matchings
                          if set(matching) <= union)
        require(set(contained) == {first, second},
                f"a third perfect matching stayed inside the {name} union")
        outside_counts = [len(set(matching) - union)
                          for matching in matchings if matching not in contained]
        require(outside_counts and min(outside_counts) == 1,
                f"the first third-base escape changed on {name}")
        audits[name] = {
            "base_union_edges": len(union),
            "perfect_matchings_contained_in_union": len(contained),
            "third_bases_audited": len(outside_counts),
            "minimum_new_physical_edges": min(outside_counts),
            "consequence": (
                "every E3-selected third matching has an edge outside M union N"
            ),
        }
    return audits


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "five_word_E3_E4": audit_e3_rank_dichotomy(),
        "single_cycle_third_base": audit_third_base_must_leave_cycle(),
        "positive_routing": (
            "if some E3 determinant is nonzero, its perfect-matching "
            "expansion cancels M,N separately and selects a third literal "
            "base K.  On a single C6/C8, K has a physical edge outside "
            "M union N.  If that edge is outside the three selected target "
            "matchings it enters the nonanchor four-good route; otherwise "
            "its exact provenance is carried by the third selected anchor "
            "and enters the anchor-contained strict-Hall exchange web"
        ),
        "sharp_boundary": (
            "all E3 determinants may vanish despite a nonzero E2 exchange. "
            "Then the exact five-row target vector lies in the evaluation "
            "plane of M,N.  E4 is only Laplace coherence and vanishes on "
            "this stratum.  Excluding it needs the multiplicative/common-q "
            "realizability of the two matching evaluation vectors, not "
            "another determinantal source face"
        ),
        "scope": (
            "literal E3 support theorem plus exact five-word rank boundary. "
            "The flat rational evaluation packet is not asserted to be a "
            "physical full one-bad source; its role is to identify the next "
            "source augmentation precisely"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"h3 even-cycle E3 boundary ledger changed: {digest}")
    print("h3 target-coloop single-cycle E3 boundary: PASS")
    print("E3 nonzero -> third physical matching with a new edge")
    print("E3 flat -> exact two-base five-word target plane")
    print("E4: coherence only; no new equation on the flat stratum")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
