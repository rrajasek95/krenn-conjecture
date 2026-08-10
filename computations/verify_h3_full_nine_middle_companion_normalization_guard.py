#!/usr/bin/env python3
"""Exact module/target audit for the genuine full-nine midpoint row.

This checker distinguishes the internal midpoint defect D from the
response companion M.  It verifies that D=0 is neither a literal full-row
consequence nor sufficient to kill the terminal class, whereas the
companion-corrected row alpha*D+M=0 is sufficient together with the
literal midpoint sum.  Pure diagonal target augmentations are retained as
separate normalized source rows.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json


SITES = tuple(range(6))
THREE_SETS = tuple(combinations(SITES, 3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rank(rows):
    if not rows:
        return 0
    work = [list(map(F, row)) for row in rows]
    answer = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(answer, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                left - value * right
                for left, right in zip(work[row], work[answer], strict=True)
            ]
        answer += 1
    return answer


def dot(left, right):
    return sum(
        (F(x) * F(y) for x, y in zip(left, right, strict=True)),
        F(0),
    )


def target(endpoint_left, endpoint_right, word):
    return int(
        endpoint_left == endpoint_right
        and all(label == endpoint_left for label in word)
    )


def direct_sum(left, right):
    left_width = len(left[0]) if left else 0
    right_width = len(right[0]) if right else 0
    return (
        [list(row) + [F(0)] * right_width for row in left]
        + [[F(0)] * left_width + list(row) for row in right]
    )


def audit_targets():
    cut_words = []
    for marked in THREE_SETS:
        marked = frozenset(marked)
        word = tuple(int(site in marked) for site in SITES)
        cut_words.append(word)
        require(target(0, 1, word) == 0, ("selected cut target", word))
        for diagonal in (0, 1, 2):
            require(
                target(diagonal, diagonal, word) == 0,
                ("diagonal cut target", diagonal, word),
            )
    require(len(cut_words) == 20 and len(set(cut_words)) == 20,
            "binary midpoint word ledger changed")
    for diagonal in (0, 1, 2):
        word = (diagonal,) * len(SITES)
        require(target(diagonal, diagonal, word) == 1,
                ("pure anchor target", diagonal))
    return tuple(cut_words)


def audit_relative_module(alpha):
    alpha = F(alpha)
    require(alpha, "selected direct scalar must be localized")

    # Dynamic coordinates are (C,D,M,Q3), where
    #   C=8*chi, D=sum of internal landing defects,
    #   M=sum of literal response companions.
    # The genuine selected midpoint sum and H2 terminal relation are
    # respectively alpha(C+D)+M=0 and C+16 Q3=0.
    literal_middle = [alpha, alpha, F(1), F(0)]
    h2_terminal = [F(1), F(0), F(0), F(16)]
    honest = [literal_middle, h2_terminal]
    require(rank(honest) == 2, ("honest dynamic rank", alpha))

    defect_zero = [F(0), F(1), F(0), F(0)]
    relative_attach = [F(0), alpha, F(1), F(0)]
    clean = [F(1), F(0), F(0), F(0)]
    terminal = [F(0), F(0), F(0), F(1)]

    # D=0 is new, but it does not imply C=0 or Q3=0: M can absorb C.
    with_defect = honest + [defect_zero]
    require(rank(with_defect) == 3, ("D row rank", alpha))
    require(rank(with_defect + [clean]) == 4,
            ("D row accidentally killed clean class", alpha))
    require(rank(with_defect + [terminal]) == 4,
            ("D row accidentally killed terminal class", alpha))
    defect_separator = [F(1), F(0), -alpha, F(-1, 16)]
    require(all(dot(row, defect_separator) == 0 for row in with_defect),
            ("D=0 separator left the row kernel", alpha))
    require(dot(clean, defect_separator) == 1,
            "D=0 separator stopped detecting C")
    require(dot(terminal, defect_separator) == F(-1, 16),
            "D=0 separator stopped detecting Q3")

    # The companion-corrected attaching row K=alpha*D+M is the missing
    # source-relative relation.  Subtracting it from the literal middle
    # row gives alpha*C, and H2 then gives Q3=0.
    with_attach = honest + [relative_attach]
    require(rank(with_attach) == 3, ("relative attaching rank", alpha))
    require(rank(with_attach + [clean]) == 3,
            ("relative attach did not contain clean row", alpha))
    require(rank(with_attach + [terminal]) == 3,
            ("relative attach did not contain terminal row", alpha))

    # Before adjoining either candidate, the genuine full-row presentation
    # has a separator with D and K both nonzero.
    honest_separator = [F(1), F(1), -2 * alpha, F(-1, 16)]
    require(all(dot(row, honest_separator) == 0 for row in honest),
            ("honest separator left the kernel", alpha))
    require(dot(defect_zero, honest_separator) == 1,
            "honest separator stopped detecting D")
    require(dot(relative_attach, honest_separator) == -alpha,
            "honest separator stopped detecting K")

    return {
        "alpha": str(alpha),
        "honest_rank": rank(honest),
        "rank_with_D": rank(with_defect),
        "rank_with_D_and_clean": rank(with_defect + [clean]),
        "rank_with_K": rank(with_attach),
        "rank_with_K_and_clean": rank(with_attach + [clean]),
        "D_separator": [str(value) for value in defect_separator],
        "honest_separator": [str(value) for value in honest_separator],
    }


def audit_anchor_direct_sum(alpha):
    alpha = F(alpha)
    # Static block from the certified two-chart presentation.
    static = [
        [F(1), F(0), F(1), F(0)],
        [F(0), F(0), F(1), F(1)],
        [F(0), F(0), F(1), F(-2)],
        [F(0), F(1), F(2), F(0)],
    ]
    require(rank(static) == 4, "static block lost rank")

    # Each pure diagonal anchor is the normalized source row d_i H_i+M_i-1=0.
    # Coordinates are (H0,M0,H1,M1,H2,M2,one).
    anchor_direct = (F(2), F(-3), F(5))
    anchors = []
    for index, direct in enumerate(anchor_direct):
        row = [F(0)] * 7
        row[2 * index] = direct
        row[2 * index + 1] = F(1)
        row[-1] = F(-1)
        anchors.append(row)
    require(rank(anchors) == 3, "anchor target block lost rank")
    anchor_point = [F(0), F(1), F(0), F(1), F(0), F(1), F(1)]
    require(all(dot(row, anchor_point) == 0 for row in anchors),
            "normalized anchor target point moved")

    dynamic = [
        [alpha, alpha, F(1), F(0)],
        [F(1), F(0), F(0), F(16)],
    ]
    base = direct_sum(static, direct_sum(anchors, dynamic))
    width = len(base[0])
    require(rank(base) == 9, "static/anchor/dynamic direct-sum rank moved")

    # In the combined presentation D remains independent, and after D=0
    # the clean row remains independent.  Thus retaining all three target
    # augmentations does not turn D=0 into the terminal relation.
    dynamic_offset = 4 + 7
    defect = [F(0)] * width
    defect[dynamic_offset + 1] = F(1)
    clean = [F(0)] * width
    clean[dynamic_offset] = F(1)
    require(rank(base + [defect]) == 10,
            "anchors unexpectedly supplied D=0")
    require(rank(base + [defect, clean]) == 11,
            "anchors plus D=0 unexpectedly supplied cleanliness")

    relative = [F(0)] * width
    relative[dynamic_offset + 1] = alpha
    relative[dynamic_offset + 2] = F(1)
    require(rank(base + [relative]) == 10,
            "relative attaching row failed to enter combined block")
    require(rank(base + [relative, clean]) == 10,
            "relative attaching row failed to imply cleanliness")

    return {
        "static_rank": rank(static),
        "anchor_rank": rank(anchors),
        "combined_rank": rank(base),
        "combined_plus_D": rank(base + [defect]),
        "combined_plus_D_clean": rank(base + [defect, clean]),
        "combined_plus_K": rank(base + [relative]),
        "combined_plus_K_clean": rank(base + [relative, clean]),
    }


def main():
    cut_words = audit_targets()
    records = [audit_relative_module(alpha) for alpha in (1, 2, F(-3, 2))]
    combined = audit_anchor_direct_sum(F(2))
    ledger = {
        "scope": "genuine full-nine selected midpoint aggregate with response companion",
        "cut_words": ["".join(map(str, word)) for word in cut_words],
        "literal_row": "alpha*(C+D)+M=0",
        "h2_terminal_row": "C+16*Q3=0",
        "insufficient_candidate": "D=0",
        "missing_relative_row": "K=alpha*D+M=0",
        "records": records,
        "target_block": combined,
        "verdict": "internal_defect_normalization_is_not_the_full_nine_attaching_relation",
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    expected = "bd7dcd9eb75a4bf7e3060f290e08a9ebe9dd4ca6d1cbd78ed10213b120618d5d"
    require(digest == expected, ("ledger digest", digest))
    print("h=3 genuine full-nine midpoint companion guard: PASS")
    print("literal aggregate: alpha*(C+D)+M=0; H2: C+16*Q3=0")
    print("D=0 remains insufficient; missing relative row is K=alpha*D+M=0")
    print("all 20 cut targets are zero; all three pure anchors retain -1")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
