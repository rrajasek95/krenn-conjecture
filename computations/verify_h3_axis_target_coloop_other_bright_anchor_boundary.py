#!/usr/bin/env python3
"""Audit the mandatory other-bright anchor against the coloop carrier.

The pure anchors K,L,M have colours 0,1,2.  If an edge of the selected
colour-2 matching M is a target coloop, deleting it removes the only
mandatory colour-2 column at both endpoints; K and L supply only colours 0
and 1.  Thus L cannot by itself raise the selected-anchor deleted-star rank
above two or make the coloop arm four-good.

Likewise L does not force a decomposable pure-word witness for the crossed
response carrier.  A (1,2) crossed row shares p_1 with L but requires s_2,
whereas L uses s_1; the transpose has the analogous mismatch at P.  The
checker freezes a literal common-source support in which all three pure
matching monomials and the mixed M/N pair are present, yet the crossed
response tensor vanishes on the pure-one output coordinate because no s_2
tail-one cell exists.  This is an exact topology/label boundary, not a full
GHZ source point.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_common_covector_synchronization.py":
        "cb834de7584912dc8c4f650a0504326cf8badb7f4c4e9e823bad5068a53e7d31",
    "notes/h3-axis-target-coloop-common-covector-synchronization.md":
        "59d0b3778a1a86febdda55a428083e1e756131bf45e4e8a1c5883e30cc08d33c",
    "computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py":
        "6de8935cae41f03e71141850b63b9fd167418bb1cebe0575ce0f3de03e8386b3",
    "notes/h3-axis-target-coloop-common-covector-k22-scope.md":
        "d083a5d967175ac26f32b252d03b57ae22aff81a661889e012e5a1b781378a31",
    "computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py":
        "d42f7b266764f1c7d371a64f323fff1c5b50a9d73b30d343112603d1924435c8",
    "notes/h3-axis-target-coloop-even-cycle-e3-boundary.md":
        "52897d6063ff5ca46c714a5262c87fae4d243779ccdaee6caa4498c70dd8f2f9",
}
EXPECTED_LEDGER_SHA256 = (
    "26b700e22938d7f48a633636339b982e1c61a2b06e4c61f46da3b291e58287e6"
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


def decorated_cell(pair, word):
    left, right = pair
    return left, right, word[left], word[right]


def decorated_monomial(matching, word):
    return frozenset(decorated_cell(pair, word) for pair in matching)


def selected_anchor_rank(selected, deleted_pair, endpoint):
    # One coordinate row per colour survives exactly when its selected pure
    # matching avoids the deleted physical pair.  Different colours are
    # independent regardless of their physical neighbour.
    return sum(deleted_pair not in matching for _colour, matching in selected)


P, S = 6, 7


def audit_selected_anchor_rank():
    unary = tuple(sorted((edge(P, S), edge(0, 1), edge(2, 3), edge(4, 5))))
    other = tuple(sorted((edge(P, 4), edge(S, 5), edge(0, 1), edge(2, 3))))
    target = tuple(sorted((edge(P, 0), edge(S, 1), edge(2, 3), edge(4, 5))))
    selected = ((0, unary), (1, other), (2, target))
    audits = []
    for target_arm in (edge(P, 0), edge(S, 1)):
        ranks = tuple(selected_anchor_rank(selected, target_arm, endpoint)
                      for endpoint in target_arm)
        require(ranks == (2, 2),
                "the other-bright anchor repaired the selected-colour coloop")
        surviving_colours = tuple(
            colour for colour, matching in selected if target_arm not in matching
        )
        require(surviving_colours == (0, 1),
                "a selected-colour column survived deletion of its coloop arm")
        audits.append({
            "target_coloop_arm": target_arm,
            "selected_anchor_deleted_star_ranks": ranks,
            "surviving_colour_rows": surviving_colours,
        })
    return {
        "selected_pure_matchings": {
            "K_unary_colour0": unary,
            "L_other_bright_colour1": other,
            "M_target_coloop_colour2": target,
        },
        "target_arm_audits": audits,
        "uniform_reason": (
            "after deleting a selected-colour-t coloop arm, the mandatory "
            "unary and other-bright anchors supply only rows 0 and m; L "
            "cannot supply the missing row t"
        ),
    }


def audit_literal_label_boundary():
    # Canonical C6 target/outside pair and one unary/other-bright anchor.
    unary = tuple(sorted((edge(P, S), edge(0, 1), edge(2, 3), edge(4, 5))))
    other = tuple(sorted((edge(P, 4), edge(S, 5), edge(0, 1), edge(2, 3))))
    target = tuple(sorted((edge(P, 0), edge(S, 1), edge(2, 3), edge(4, 5))))
    outside = tuple(sorted((edge(P, 2), edge(S, 3), edge(0, 1), edge(4, 5))))
    require(cycle_lengths(target, outside) == (6,),
            "the canonical target/outside pair stopped being a C6")

    pure0, pure1, pure2 = ((colour,) * 8 for colour in range(3))
    # Site order 0,1,2,3,4,5,P,S.  Endpoint labels (1,2) select the crossed
    # row p1*s2.  Both target and outside skeletons are nonzero on this word.
    mixed = (2, 2, 1, 2, 2, 2, 1, 2)
    support = set()
    for matching, word in ((unary, pure0), (other, pure1),
                           (target, pure2), (target, mixed),
                           (outside, mixed)):
        support.update(decorated_monomial(matching, word))

    require(decorated_monomial(unary, pure0) <= support
            and decorated_monomial(other, pure1) <= support
            and decorated_monomial(target, pure2) <= support,
            "a mandatory pure anchor monomial left the literal support")
    require(decorated_monomial(target, mixed) <= support
            and decorated_monomial(outside, mixed) <= support,
            "the selected mixed companion pair left the support")

    # Every s2 component in the support has tail colour 2.  Therefore no
    # p1*s2 matching can evaluate on residual word 1^6, even though the
    # diagonal p1*s1 matching L is nonzero there.
    s2_cells = tuple(sorted(cell for cell in support
                            if S in cell[:2]
                            and cell[2 if cell[0] == S else 3] == 2))
    s2_tail_colours = tuple(
        cell[3] if cell[0] == S else cell[2] for cell in s2_cells
    )
    require(s2_cells and set(s2_tail_colours) == {2},
            "an s2 tail-one component entered the support guard")

    crossed_pure1 = []
    for matching in perfect_matchings(range(8)):
        p_pair = next(pair for pair in matching if P in pair)
        s_pair = next(pair for pair in matching if S in pair)
        p_cell = decorated_cell(p_pair, pure1)
        s_word = list(pure1)
        s_word[S] = 2
        s_word = tuple(s_word)
        # Full crossed output has endpoint heads (1,2) and residual word 1^6.
        crossed_word = (1,) * 6 + (1, 2)
        monomial = decorated_monomial(matching, crossed_word)
        if monomial <= support:
            crossed_pure1.append(matching)
    require(not crossed_pure1,
            "the other-bright pure word acquired a crossed response base")

    # Label audit in both orientations.  A pure-m diagonal base uses
    # (p_m,s_m); either crossed orientation changes exactly one outer head.
    orientation_audits = []
    for crossed in ((1, 2), (2, 1)):
        shared = sum(left == right
                     for left, right in zip((1, 1), crossed, strict=True))
        require(shared == 1,
                "a crossed row stopped differing from L at one endpoint")
        orientation_audits.append({
            "diagonal_L_endpoint_heads": [1, 1],
            "crossed_endpoint_heads": list(crossed),
            "shared_endpoint_rows": shared,
            "mismatched_endpoint_rows": 2 - shared,
        })

    return {
        "site_order": [0, 1, 2, 3, 4, 5, "P", "S"],
        "pure_anchor_words": ["0^8", "1^8", "2^8"],
        "mixed_crossed_word": "22122212",
        "target_M": target,
        "outside_N": outside,
        "other_bright_L": other,
        "unary_K": unary,
        "literal_scalar_cells": len(support),
        "s2_tail_colours": list(s2_tail_colours),
        "p1s2_terms_on_pure1_residual_word": 0,
        "orientation_audit": orientation_audits,
        "consequence": (
            "the mandatory L monomial is nonzero in its diagonal row but "
            "does not force either common-carrier column to be nonzero on "
            "the decomposable pure-one output covector"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "selected_anchor_rank": audit_selected_anchor_rank(),
        "literal_common_source_label_boundary": audit_literal_label_boundary(),
        "negative_theorem": (
            "the mandatory other-bright pure matching L cannot by itself "
            "upgrade a selected-colour target-coloop arm to deleted-star "
            "rank three: K and L supply only the two nonselected colour "
            "rows after deletion.  Nor does L force its decomposable pure "
            "output word to witness the crossed bistar columns, because a "
            "crossed row differs from L at exactly one endpoint head"
        ),
        "smallest_next_input": (
            "an alternate pure matching in the selected target colour, or "
            "a literal crossed response base carrying the mismatched outer "
            "head.  Either is extra physical provenance beyond the three "
            "mandatory pure anchors"
        ),
        "scope": (
            "uniform selected-anchor rank/endpoint-label theorem plus a "
            "literal common-source support realization.  The realization "
            "is a topology/label boundary, not a full exact GHZ source; "
            "additional scalar cells could create the missing crossed base"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"other-bright anchor boundary ledger changed: {digest}")
    print("h3 target-coloop other-bright anchor boundary: PASS")
    print("mandatory L leaves selected-colour coloop ranks (2,2)")
    print("pure-L coordinate need not see the crossed bistar columns")
    print("remaining input: selected-colour alternate or crossed response base")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
