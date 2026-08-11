#!/usr/bin/env python3
"""Exclude the E3-flat target-coloop plane in the physical one-bad chart.

The five literal full-H8 words are fixed explicitly.  Two response-base
matchings M,N avoid the selected direct pair P-S.  In the normalized
one-bad packet the colour-zero outer rows vanish, so both matching
evaluations are zero on the unary word 0^8.  The unary target value is one.
Consequently the E3 minor on (bright target, outside mixed, unary) is the
nonzero E2 target/outside minor, up to its harmless orientation sign.

This is a source-typing correction to an abstract five-row E3-flat module.
The resulting third base lies in the unary direct-anchor family; it opens
M union N but need not leave the selected three-anchor union.
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
    "computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py":
        "a280b40657f2ab02c9c9f6ecf50dd3326db12bcc20614cbbd12bddffac8a1b62",
    "notes/shared-reciprocal-two-bad-anchor-safe-retraction.md":
        "dda2e2e0b3e81bca41392f355ce3f678a38d8f09053646b2f22df3a86b24bee5",
    "computations/verify_n8_chart26_c4_exchange_3cell.py":
        "4398d15df3a5f0b34c2745fdb7087a289452ed03983d22431c4f20d116f019c6",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
}
EXPECTED_LEDGER_SHA256 = (
    "1e572c10454eaf99a0737d07a3a0efd6df1cb01c4d85c22359444f893de3f20e"
)


P, S = 6, 7
WORDS = (
    "22222222",  # selected bright target t
    "22122212",  # outside mixed word d: P=1, S=2
    "21222212",  # a second literal mixed word
    "00000000",  # unary target
    "11111111",  # the other bright target
)
TARGET_VALUES = (Q(1), Q(0), Q(0), Q(1), Q(1))
TARGET_INDEX, OUTSIDE_INDEX, UNARY_INDEX = 0, 1, 3


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


def det3(first, second, third, indices):
    i, j, k = indices
    return (
        first[i] * (second[j] * third[k] - second[k] * third[j])
        - first[j] * (second[i] * third[k] - second[k] * third[i])
        + first[k] * (second[i] * third[j] - second[j] * third[i])
    )


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


def audit_literal_words_and_outer_zero():
    require(len(WORDS) == 5 and TARGET_VALUES == (1, 0, 0, 1, 1),
            "the five literal word target pattern changed")
    require(WORDS[TARGET_INDEX] == "2" * 8
            and WORDS[UNARY_INDEX] == "0" * 8,
            "the bright/unary words changed")
    require(any(value != WORDS[OUTSIDE_INDEX][0]
                for value in WORDS[OUTSIDE_INDEX]),
            "the selected outside word stopped being mixed")

    target_base = tuple(sorted((edge(P, 0), edge(S, 1),
                                edge(2, 3), edge(4, 5))))
    outside_base = tuple(sorted((edge(P, 2), edge(S, 3),
                                 edge(0, 1), edge(4, 5))))
    require(edge(P, S) not in target_base
            and edge(P, S) not in outside_base,
            "a response base acquired the direct unary pair")

    # In word 0^8 either response skeleton would need one colour-zero cell
    # in each outer row.  The normalized one-bad packet has those complete
    # rows zero, so both monomials vanish before any tail cancellation.
    outer_zero_factors = {
        "target_base": [f"{P}-0:00", f"{S}-1:00"],
        "outside_base": [f"{P}-2:00", f"{S}-3:00"],
    }
    return {
        "literal_words": list(WORDS),
        "target_values": [str(value) for value in TARGET_VALUES],
        "target_base": target_base,
        "outside_base": outside_base,
        "unary_evaluation_zero_factors": outer_zero_factors,
        "normalized_rows": "p_0=s_0=0 away from the direct E_00 pair",
    }


def audit_unary_e3_minor():
    # Other word entries are deliberately arbitrary.  Only the physical
    # zeros a_unary=b_unary=0, the target-coloop zero b_target=0, and the
    # nonzero E2 pivot a_target*b_outside are used.
    a = (Q(2), Q(3), Q(-5), Q(0), Q(7))
    b = (Q(0), Q(-4), Q(6), Q(0), Q(9))
    require(a[TARGET_INDEX] and not b[TARGET_INDEX]
            and b[OUTSIDE_INDEX]
            and not a[UNARY_INDEX] and not b[UNARY_INDEX],
            "the physical target/outside/unary evaluations changed")
    delta = (a[TARGET_INDEX] * b[OUTSIDE_INDEX]
             - a[OUTSIDE_INDEX] * b[TARGET_INDEX])
    e3 = det3(a, b, TARGET_VALUES,
              (TARGET_INDEX, OUTSIDE_INDEX, UNARY_INDEX))
    require(delta == -8 and e3 == delta,
            f"the unary E3 minor stopped equalling E2: {delta}/{e3}")
    require(rank((a, b, TARGET_VALUES)) == 3,
            "the physical unary coordinate re-entered the E3-flat plane")

    # The claim is coefficient-independent.  Audit several signs and
    # arbitrary remaining entries while retaining the four load-bearing
    # physical coordinates.
    audits = 0
    for a_target in (Q(-3), Q(1), Q(5)):
        for b_outside in (Q(-2), Q(4)):
            first = (a_target, Q(11), Q(-7), Q(0), Q(13))
            second = (Q(0), b_outside, Q(17), Q(0), Q(-19))
            current_delta = a_target * b_outside
            current_e3 = det3(first, second, TARGET_VALUES,
                              (TARGET_INDEX, OUTSIDE_INDEX, UNARY_INDEX))
            require(current_e3 == current_delta != 0,
                    "an arbitrary physical unary E3 audit failed")
            audits += 1

    # The abstract flat sample previously proposed for h=(1,0,0,1,1)
    # violates both response-base unary zeros.
    old_flat_a = (Q(1), Q(1), Q(2), Q(3), Q(4))
    old_flat_b = (Q(0), Q(-1), Q(-2), Q(-2), Q(-3))
    require(old_flat_a[UNARY_INDEX] != 0
            and old_flat_b[UNARY_INDEX] != 0,
            "the abstract E3-flat guard unexpectedly became one-bad physical")
    return {
        "matching_M": [str(value) for value in a],
        "matching_N": [str(value) for value in b],
        "E2_target_outside_minor": str(delta),
        "E3_target_outside_unary_minor": str(e3),
        "identity": "det(M,N,h)_(target,outside,unary)=Delta_target,outside",
        "coefficient_independent_audits": audits,
        "abstract_flat_guard_unary_entries": [
            str(old_flat_a[UNARY_INDEX]), str(old_flat_b[UNARY_INDEX])],
    }


def audit_unary_third_base_route():
    # Every nonzero 0^8 full-source matching uses the direct P-S cell because
    # all colour-zero outer response cells vanish.  Its residual factor is
    # one of the fifteen six-site pure-zero matchings.
    residual = tuple(perfect_matchings(range(6)))
    require(len(residual) == 15,
            "the six-site unary matching count changed")
    unary_bases = tuple(tuple(sorted((edge(P, S),) + matching))
                        for matching in residual)
    require(all(edge(P, S) in matching for matching in unary_bases),
            "a normalized unary base avoided the direct anchor")

    representatives = {
        "C6": (
            ((0, 6), (1, 7), (2, 3), (4, 5)),
            ((0, 1), (2, 6), (3, 7), (4, 5)),
        ),
        "C8": (
            ((0, 6), (1, 7), (2, 3), (4, 5)),
            ((0, 4), (1, 5), (2, 6), (3, 7)),
        ),
    }
    audits = {}
    for name, (target, outside) in representatives.items():
        old_union = set(target) | set(outside)
        require(edge(P, S) not in old_union,
                f"the {name} response-base union acquired the direct anchor")
        new_edge_counts = [len(set(matching) - old_union)
                           for matching in unary_bases]
        require(min(new_edge_counts) >= 1,
                f"a unary {name} third base stayed in the two-base union")
        audits[name] = {
            "unary_bases": len(unary_bases),
            "all_use_direct_anchor": True,
            "minimum_edges_outside_M_union_N": min(new_edge_counts),
            "maximum_edges_outside_M_union_N": max(new_edge_counts),
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
        "literal_full_H8_typing": audit_literal_words_and_outer_zero(),
        "unary_E3_flat_exclusion": audit_unary_e3_minor(),
        "unary_third_base_route": audit_unary_third_base_route(),
        "positive_theorem": (
            "in the normalized h3 one-bad packet, choose the bright target "
            "word, one mixed outside word, and the unary word 0^8.  Both "
            "fixed response matching bases vanish on 0^8 because p0=s0=0, "
            "while its source target is one.  Therefore their E3 minor is "
            "exactly the nonzero E2 target/outside minor, so the E3-flat "
            "two-base plane is impossible"
        ),
        "third_base": (
            "the surviving E3 expansion is a unary full-source coefficient. "
            "Every literal third base uses the direct E00 anchor P-S and a "
            "pure-zero residual matching, hence leaves the old C6/C8 union"
        ),
        "sharp_residual": (
            "the direct P-S edge is already the selected unary anchor.  E3 "
            "therefore opens the two-base cycle source-validly but does not "
            "by itself expose an edge outside the full three-anchor union "
            "or restore the bright target-coloop deleted-star colour"
        ),
        "scope": (
            "exact normalized one-bad full-H8 words at h=3.  It corrects "
            "the scope of an abstract five-row flat evaluation module; it "
            "does not claim a free/four-good landing for the anchor-contained "
            "unary third base"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"unary E3-flat exclusion ledger changed: {digest}")
    print("h3 target-coloop physical unary E3-flat exclusion: PASS")
    print("literal words: bright target, mixed outside, mixed, unary, bright")
    print("response bases vanish on unary; E3(target,outside,unary)=E2")
    print("third base: unary direct anchor; anchor-contained route remains")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
