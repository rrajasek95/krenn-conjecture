#!/usr/bin/env python3
"""Exhaust the four-site response/target closure around U_C4.

The four balanced operation corners are

    DQ[a|b], DQ[b|a], PS[P0,S1], PS[P1,S0]

with character delta=(1,1,-1,-1).  At the fixed residual window 2345
there are three C4 matching occurrences.  This checker retains separate
private B and reduced-Eq copies of every top occurrence, every one of the
18 literal direction-factor PP flags, and every one of the 24 tail-edge PP
flags.  It then grants a projection-complete local supermap:

* all matching-difference rows in B and Eq;
* the four physical response/cap diagonals B=Eq;
* all four signless K2,2 shore-crossing companions;
* every literal PP/reinsertion coordinate comparison; and
* the entire target/q/anchor/W/residue/ridge/eta/sigma space.

The resulting map has rank 126 in dimension 127.  Its unique left kernel is
the literal extension of delta.(B-Eq), constant through restriction and
reinsertion.  It detects the balanced private U_C4 face, while every h=2
physical response row and every derivative of it is tied B=Eq.  Thus the
normalized four-site response H-1 does not construct an absolute same-grade
primitive.  The normalized dual is, however, exhaustive on this local base
category.  A global filler must introduce an operation-labelled column with
nonzero delta-weighted private/Eq mismatch.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json


BASE_COMMITS = {
    "balanced_private_minus_Eq": "f753b5d",
    "original_H2_terminal_typing": "2dab781",
    "same_grade_dual_chain": "4aa11b9",
    "fixed_face_relative_C4": "20ecb75",
}
BASE_BLOBS = {
    "f753b5d:verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "2dab781:verify_h3_gate_ii_h2_local_duality_terminal_typing_shortcut_gate.py":
        "68447eeda523bf05f38dbcfbb9073cbc30e676ff20e52664995de75012ef6153",
    "4aa11b9:verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "20ecb75:verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py":
        "48bb5568b6d3360dd592011ed09aca364cfdbd24770d2e2419c1f99464825878",
}
EXPECTED_LEDGER_SHA256 = (
    "b52e14ea6deb394ea22eb79362f6ac0877f46c992382160f2dd206fff650f78e"
)


CORNERS = (
    "DQ[a|b]",
    "DQ[b|a]",
    "PS[P0,S1]",
    "PS[P1,S0]",
)
DELTA = tuple(map(Q, (1, 1, -1, -1)))
MATCHINGS = ("23|45", "24|35", "25|34")
DIRECTIONS = (
    "(dD)*q01",
    "D*(dq01)",
    "(dp0)*s1",
    "p0*(ds1)",
    "(dp1)*s0",
    "p1*(ds0)",
)
DIRECTION_CORNERS = (0, 1, 2, 2, 3, 3)
PRIMITIVE_DIRECTION_PROFILE = tuple(map(Q, (2, 2, -1, -1, -1, -1)))
TAIL_SLOTS = ("delete first tail edge", "delete second tail edge")
ALPHA = tuple(map(Q, (-1, 1, 1, -1)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def build_labels() -> tuple[str, ...]:
    labels: list[str] = []
    for block in ("B", "Eq"):
        for corner in range(4):
            for matching in range(3):
                labels.append(f"top:{block}:{corner}:{matching}")
    for block in ("B", "Eq"):
        for direction in range(6):
            for matching in range(3):
                labels.append(f"direction:{block}:{direction}:{matching}")
    for block in ("B", "Eq"):
        for corner in range(4):
            for matching in range(3):
                for slot in range(2):
                    labels.append(f"tail:{block}:{corner}:{matching}:{slot}")
    labels.extend(f"target:{corner}" for corner in range(4))
    labels.extend(f"W:{corner}" for corner in range(4))
    labels.extend(f"ores:{corner}" for corner in range(4))
    labels.extend(("M", "ainc", "q", "P_f", "ridge", "eta", "sigma"))
    require(len(labels) == len(set(labels)) == 127,
            ("local output dimension changed", len(labels)))
    return tuple(labels)


LABELS = build_labels()
INDEX = {label: index for index, label in enumerate(LABELS)}


def vector(**entries: int | Q) -> tuple[Q, ...]:
    unknown = set(entries) - set(LABELS)
    require(not unknown, ("unknown rows", sorted(unknown)))
    return tuple(Q(entries.get(label, 0)) for label in LABELS)


def sparse(entries: dict[str, int | Q]) -> tuple[Q, ...]:
    return vector(**entries)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(value) for value in vectors}) == 1,
            "add width")
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(coefficient: int | Q,
          value: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in value)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def top_label(block: str, corner: int, matching: int) -> str:
    return f"top:{block}:{corner}:{matching}"


def direction_label(block: str, direction: int, matching: int) -> str:
    return f"direction:{block}:{direction}:{matching}"


def tail_label(block: str, corner: int, matching: int, slot: int) -> str:
    return f"tail:{block}:{corner}:{matching}:{slot}"


def balanced_top(block: str) -> tuple[Q, ...]:
    return sparse({
        top_label(block, corner, matching): DELTA[corner]
        for corner in range(4) for matching in range(3)
    })


def tied_balanced_top() -> tuple[Q, ...]:
    return add(balanced_top("B"), balanced_top("Eq"))


def primitive_direction_face(block: str) -> tuple[Q, ...]:
    return sparse({
        direction_label(block, direction, matching):
            PRIMITIVE_DIRECTION_PROFILE[direction]
        for direction in range(6) for matching in range(3)
    })


def balanced_tail_face(block: str) -> tuple[Q, ...]:
    return sparse({
        tail_label(block, corner, matching, slot): DELTA[corner]
        for corner in range(4) for matching in range(3) for slot in range(2)
    })


def integral_terminal_dual() -> tuple[Q, ...]:
    entries: dict[str, Q] = {}
    for corner in range(4):
        for matching in range(3):
            entries[top_label("B", corner, matching)] = DELTA[corner]
            entries[top_label("Eq", corner, matching)] = -DELTA[corner]
    for direction, corner in enumerate(DIRECTION_CORNERS):
        for matching in range(3):
            entries[direction_label("B", direction, matching)] = DELTA[corner]
            entries[direction_label("Eq", direction, matching)] = -DELTA[corner]
    for corner in range(4):
        for matching in range(3):
            for slot in range(2):
                entries[tail_label("B", corner, matching, slot)] = DELTA[corner]
                entries[tail_label("Eq", corner, matching, slot)] = -DELTA[corner]
    return sparse(entries)


def top_projection_columns() -> tuple[tuple[str, tuple[Q, ...]], ...]:
    columns: list[tuple[str, tuple[Q, ...]]] = []

    # Each matching augmentation-zero plane is granted independently in B
    # and Eq.  This is stronger than retaining only the physical C4 bars.
    for block in ("B", "Eq"):
        for corner in range(4):
            for left, right in ((0, 1), (1, 2)):
                columns.append((
                    f"matching-difference:{block}:{corner}:{left}->{right}",
                    sparse({top_label(block, corner, left): -1,
                            top_label(block, corner, right): 1}),
                ))

    # The physical h=2 response/cap row has identical private and reduced-Eq
    # incidence.  Its normalized target value is an outside row.
    for corner in range(4):
        entries = {
            **{top_label("B", corner, matching): 1 for matching in range(3)},
            **{top_label("Eq", corner, matching): 1 for matching in range(3)},
            f"target:{corner}": 1,
        }
        columns.append((f"normalized-response:r0:{corner}", sparse(entries)))

    # The four physical signless K2,2 companions join opposite shores only
    # in the private block.  Their delta augmentation is zero.
    for direct in (0, 1):
        for endpoint in (2, 3):
            columns.append((
                f"K22-companion:{direct}:{endpoint}",
                sparse({
                    **{top_label("B", direct, matching): 1
                       for matching in range(3)},
                    **{top_label("B", endpoint, matching): 1
                       for matching in range(3)},
                }),
            ))
    return tuple(columns)


def lower_face_and_reinsertion_columns() \
        -> tuple[tuple[str, tuple[Q, ...]], ...]:
    columns: list[tuple[str, tuple[Q, ...]]] = []

    # Grant every literal restriction/reinsertion comparison separately in
    # B and Eq.  The direction maps retain DQ/PS operation type.
    for block in ("B", "Eq"):
        for direction, corner in enumerate(DIRECTION_CORNERS):
            for matching in range(3):
                columns.append((
                    f"direction-reinsert:{block}:{direction}:{matching}",
                    sparse({
                        direction_label(block, direction, matching): 1,
                        top_label(block, corner, matching): -1,
                    }),
                ))
        for corner in range(4):
            for matching in range(3):
                for slot in range(2):
                    columns.append((
                        f"tail-reinsert:{block}:{corner}:{matching}:{slot}",
                        sparse({
                            tail_label(block, corner, matching, slot): 1,
                            top_label(block, corner, matching): -1,
                        }),
                    ))
    require(len(columns) == 36 + 48,
            ("PP/reinsertion column count changed", len(columns)))
    return tuple(columns)


def external_augmented_columns() -> tuple[tuple[str, tuple[Q, ...]], ...]:
    # Grant the entire outside augmentation space.  Since the local terminal
    # has zero coefficient there, this is stronger than checking named rows.
    external = tuple(label for label in LABELS
                     if label.startswith(("target:", "W:", "ores:"))
                     or label in ("M", "ainc", "q", "P_f",
                                  "ridge", "eta", "sigma"))
    require(len(external) == 19, ("external row count changed", len(external)))
    columns = [(f"external-basis:{label}", sparse({label: 1}))
               for label in external]

    # Retain the literal named combinations as sign checks, even though the
    # full external span above already contains them.
    named: list[tuple[str, tuple[Q, ...]]] = []
    for corner in range(4):
        named.extend((
            (f"T:{corner}", sparse({f"W:{corner}": -1,
                                     f"target:{corner}": 1})),
            (f"rho:{corner}", sparse({f"W:{corner}": 1,
                                       f"ores:{corner}": 1})),
        ))
    named.extend((
        ("Cartan-K", sparse({
            **{f"ores:{corner}": ALPHA[corner] for corner in range(4)},
            "ridge": 1, "eta": 1, "sigma": -1,
        })),
        ("q=M-ainc", sparse({"M": 1, "ainc": -1, "q": -1})),
        ("pointed-anchor", sparse({"P_f": 1})),
    ))
    return tuple(columns + named)


def exhaustive_local_supermap_audit() -> dict[str, object]:
    top_columns = top_projection_columns()
    lower_columns = lower_face_and_reinsertion_columns()
    external_columns = external_augmented_columns()
    named = top_columns + lower_columns + external_columns
    values = tuple(value for _name, value in named)
    dual = integral_terminal_dual()

    require(len(top_columns) == 24
            and all(dot(dual, value) == 0 for value in values),
            "the local private-minus-Eq dual failed on the exhaustive supermap")
    observed_rank = rank(values)
    require(observed_rank == len(LABELS) - 1,
            ("local supermap stopped having corank one", observed_rank))

    candidate = balanced_top("B")
    eq_only = balanced_top("Eq")
    tied = tied_balanced_top()
    require(dot(dual, candidate) == 12
            and dot(dual, eq_only) == -12
            and dot(dual, tied) == 0,
            "the raw occurrence normalization changed")
    require(rank(values + (candidate,)) == len(LABELS)
            and rank(values + (eq_only,)) == len(LABELS)
            and rank(values + (tied,)) == observed_rank,
            "the private/Eq positive and tied controls changed")

    direction_private = primitive_direction_face("B")
    direction_tied = add(direction_private, primitive_direction_face("Eq"))
    tail_private = balanced_tail_face("B")
    tail_tied = add(tail_private, balanced_tail_face("Eq"))
    require(dot(dual, direction_private) == 24
            and dot(dual, direction_tied) == 0
            and dot(dual, tail_private) == 24
            and dot(dual, tail_tied) == 0,
            "the PP private/Eq test changed")

    return {
        "output_dimension": len(LABELS),
        "top_private_Eq_coordinates": 24,
        "direction_private_Eq_coordinates": 36,
        "tail_PP_private_Eq_coordinates": 48,
        "external_augmented_coordinates": 19,
        "top_projection_columns": len(top_columns),
        "literal_PP_reinsertion_columns": len(lower_columns),
        "rank": observed_rank,
        "cokernel_dimension": len(LABELS) - observed_rank,
        "unique_integral_left_kernel": (
            "delta.(B-Eq), extended with the same corner value through "
            "every direction and tail reinsertion flag"
        ),
        "normalized_terminal": "Psi_loc/12",
        "normalized_value_on_balanced_private_top": "1",
        "value_on_Eq_only_positive_control": "-1",
        "value_on_tied_B_Eq_control": "0",
        "primitive_direction_profile": [2, 2, -1, -1, -1, -1],
        "raw_value_on_private_direction_face": "24",
        "raw_value_on_tied_direction_face": "0",
        "raw_value_on_private_tail_PP_face": "24",
        "raw_value_on_tied_tail_PP_face": "0",
        "all_target_q_anchor_W_residue_ridge_eta_sigma_rows_granted": True,
        "consequence": (
            "the local terminal is not an inventory artifact: it kills a "
            "projection-complete supermap with every literal lower "
            "coordinate reinserted and the full outside augmentation space"
        ),
    }


def four_site_response_and_target_audit() -> dict[str, object]:
    words = tuple(product(range(3), repeat=4))
    pure = tuple(word for word in words if len(set(word)) == 1)
    mixed = tuple(word for word in words if len(set(word)) > 1)
    require(len(words) == 81 and len(pure) == 3 and len(mixed) == 78,
            "the four-site word/target census changed")

    # The selected parent word is 11:110000, so the residual 2345 word is
    # pure 0000.  Its normalized h=2 response is H_0000-1.  In the lifted
    # private/Eq projection the H incidence is diagonal.  Target is outside
    # the projection and cannot change delta.(B-Eq).
    dual = integral_terminal_dual()
    tied = tied_balanced_top()
    arbitrary_external = sparse({
        "target:0": 7, "target:1": -3, "W:2": 5, "ores:3": 11,
        "M": -2, "ainc": 13, "q": -15, "P_f": 17,
        "ridge": 19, "eta": -23, "sigma": 29,
    })
    proposed = add(tied, arbitrary_external)
    require(dot(dual, proposed) == 0,
            "external augmentation changed the tied response projection")

    # Every coefficient Hasse/PP derivative applies the same incidence map
    # to B and Eq.  Check the two literal first-face packets explicitly.
    tied_direction = add(primitive_direction_face("B"),
                         primitive_direction_face("Eq"))
    tied_tail = add(balanced_tail_face("B"),
                    balanced_tail_face("Eq"))
    require(dot(dual, tied_direction) == dot(dual, tied_tail) == 0,
            "a derivative of a tied response became private/Eq-unequal")

    return {
        "four_site_words": len(words),
        "normalized_pure_target_words": ["0000", "1111", "2222"],
        "mixed_target_zero_words": len(mixed),
        "selected_parent_head": "11:110000",
        "selected_residual_word_2345": "0000",
        "selected_h2_response_equation": (
            "H_0000-1=0, H_0000=q23q45+q24q35+q25q34"
        ),
        "same_grade_lift_projection": "B=Eq on every matching occurrence",
        "normalized_target_projection_on_B_minus_Eq": 0,
        "all_external_augmentation_rows_projection_on_B_minus_Eq": 0,
        "PP_product_rule": (
            "the 18 DQ/PS direction flags and 24 tail deletion flags carry "
            "identical private and reduced-Eq incidence"
        ),
        "absolute_U_C4_constructed": False,
        "reason": (
            "the h=2 row supplies at most the tied class (B,Eq)=(delta,delta); "
            "the required balanced private face is (delta,0)"
        ),
        "rank_test": (
            "the tied class leaves rank 126, while either private-only or "
            "Eq-only delta raises the local rank to 127"
        ),
    }


def typing_and_scope_audit() -> dict[str, object]:
    return {
        "literal_operation_corners": list(CORNERS),
        "corner_character_delta": [1, 1, -1, -1],
        "matching_occurrences": list(MATCHINGS),
        "direction_flags": [
            {"label": DIRECTIONS[index],
             "corner": CORNERS[DIRECTION_CORNERS[index]],
             "primitive_coefficient": int(PRIMITIVE_DIRECTION_PROFILE[index])}
            for index in range(6)
        ],
        "direction_flag_count_with_three_tails": 18,
        "tail_PP_flag_count": 24,
        "tag_preserving_actions": (
            "matching permutations, the two direct-corner swap, the two "
            "endpoint-PS swap, and literal restriction/reinsertion"
        ),
        "forbidden_as_internal_action": (
            "an oriented DQ-to-PS shore difference; it has nonzero "
            "delta.(B-Eq) and is exactly the missing profile-changing cell"
        ),
        "local_terminal_signature": {
            "private_B": "delta/12 per matching occurrence",
            "reduced_Eq": "-delta/12 per matching occurrence",
            "direction_and_tail_flags": (
                "same B/Eq values transported by literal reinsertion"
            ),
            "target": 0,
            "q": 0,
            "anchor_ainc_Pf": 0,
            "W": 0,
            "ordinary_residue": 0,
            "ridge_eta_sigma": 0,
        },
        "local_exhaustiveness": (
            "proved for the complete four-site response/target, C4 matching, "
            "signless companion, PP/reinsertion and named augmentation closure"
        ),
        "global_scope_guard": (
            "a new h=3 same-word/fine/repeated cross-profile column may break "
            "the local law; the local theorem identifies its necessary and "
            "sufficient first projection delta.(B-Eq)!=0"
        ),
        "first_global_positive_datum": (
            "one source-labelled DQ/PS relative-C4 column with unequal "
            "private and reduced-Eq projection, followed by repair of its "
            "word-0102/q/anchor/W/ridge faces"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    ledger = {
        "theorem": "h3 U_C4 four-site response private-minus-Eq local terminal gate",
        "base_commits": BASE_COMMITS,
        "base_blob_sha256": BASE_BLOBS,
        "exhaustive_local_supermap": exhaustive_local_supermap_audit(),
        "h2_four_site_response_and_normalized_target":
            four_site_response_and_target_audit(),
        "operation_PP_reinsertion_and_augmented_scope":
            typing_and_scope_audit(),
        "verdict": (
            "The physical h=2 four-site response and normalized target rows "
            "do not construct an absolute U_C4 in the original DQ/PS Hasse "
            "grade.  Their private and reduced-Eq incidence is tied, and "
            "every literal PP/reinsertion derivative preserves that tie.  "
            "After granting all matching differences, all signless K2,2 "
            "companions, every lower-coordinate reinsertion, and the full "
            "target/q/anchor/W/residue/ridge/eta/sigma space, the local map "
            "has rank 126 in dimension 127.  Its unique normalized terminal "
            "is Psi_loc/12=delta.(B-Eq)/12, transported through the lower "
            "flags.  Thus the local four-site branch is exhausted: a global "
            "filler must contain a genuinely new source-labelled column with "
            "delta-weighted private/Eq mismatch."
        ),
        "nonclaims": [
            "the h=2 Hasse[0] response row is not silently retagged as a DQ/PS Hasse[2] generator",
            "perfect target/W/ridge decoration is not called a fill when B=Eq",
            "the local terminal is not called a global terminal before all h3 cross-profile columns are classified",
            "an oriented DQ-to-PS difference is not called a tag-preserving action bar",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("h2 four-site response: B=Eq; ABSOLUTE U_C4 NOT CONSTRUCTED")
    print("local augmented supermap: rank 126 / 127")
    print("unique local terminal: delta.(B-Eq)/12")
    print("18 direction + 24 tail PP flags: EXHAUSTED BY REINSERTION")
    print("target/q/anchor/W/ridge: ZERO IN TERMINAL; CANNOT REPAIR TIED B=Eq")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
