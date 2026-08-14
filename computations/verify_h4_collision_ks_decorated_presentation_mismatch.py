#!/usr/bin/env python3
"""Find the first decorated mismatch in the h=4 collision/KS overlap.

The intrinsic Hasse structure map identifies three presentations of one
six-site tail T=e0 e1 e2.  This checker retains the physical h=3 cap word
on each two-edge window and asks whether those presentations lie in one
h=4 word/fine/repeated and protected augmented block.

The answer fails first at the word idempotent.  Every h=3 cap window has
tail-colour multiset {1,2,2,2}.  There is no six-site word whose restriction
to all three four-site windows has that multiset.  A canonical extension by
a 22 spectator gives presentation words

    0121221222, 0121122222, 0121122222,

so the first word idempotent has values (1,0,0), detected by both primitive
overlap differences.  Fine grades differ for the same reason; the coarse
P3+K2 topology agrees, but full removed/reinserted-edge labels do not.

The currently constructed relative collision packet has no physical
cross-grade bridge, hence no physical q/anchor/etc. values.  Its exact
zero-cap dual extension is zero on all protected coordinates.  Conditional
on three transported local B0 bridges with coefficients mu_i, the known
cap/Cartan equations force

    target=W=-mu, ores=ridge=mu, q=anchor=0.

These scalar values agree iff the mu_i agree, but that conditional equality
does not repair the earlier word/fine/repeated mismatch.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h4_collision_ks_one_edge_shuffle_overlap.py":
        "bf25a8c481ad8e42a14b22ff3f955f5d321289356d9dd11962ffc68d4e06671e",
    "notes/h4-collision-ks-one-edge-shuffle-overlap.md":
        "3b50f4a6e556f3cd760d335910b788b7b16d074d0a5382dc89bae381e2932972",
    "computations/verify_h3_collision_xi_augmented_dual_unsigned_root_shortcut_gate.py":
        "87c315287f77145be213a287a9e231620016d179a67a1344840f8637b83fc085",
    "notes/h3-collision-xi-augmented-dual-unsigned-root-shortcut-gate.md":
        "71b64df58291668ec717f414dc337251a70d6afe43d6c374a5b76255138a2a7a",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
}
EXPECTED_LEDGER_SHA256 = (
    "e8df4f9fed9abe69b4eb2a2cff826fe1a25718cfddb80f4cae1ddee01275efb4"
)

SITES = ("P", "S", "0", "1", "2", "3", "4", "5", "6", "7")
TAIL_EDGES = ((4, 5), (6, 7), (8, 9))
WINDOWS = tuple(
    tuple(edge for edge in TAIL_EDGES if edge != spectator)
    for spectator in TAIL_EDGES
)
FAMILIES = (
    {
        "name": "forward_01=-D*s1",
        "local_edges": ((0, 1), (1, 3)),
        "missing_doubled": ("0", "S"),
        "operation": "DSQ",
    },
    {
        "name": "reverse_01=+p0*q01",
        "local_edges": ((0, 2), (2, 3)),
        "missing_doubled": ("S", "0"),
        "operation": "PQQ",
    },
    {
        "name": "forward_02=-D*s0",
        "local_edges": ((0, 1), (1, 2)),
        "missing_doubled": ("1", "S"),
        "operation": "DSQ",
    },
    {
        "name": "reverse_02=+p1*q01",
        "local_edges": ((0, 3), (2, 3)),
        "missing_doubled": ("S", "1"),
        "operation": "PQQ",
    },
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def response_word() -> tuple[int, ...]:
    return tuple(map(int, "1111000000"))


def cap_presentation_word(spectator_index: int) -> tuple[int, ...]:
    """Canonical relabelled 01211222 window plus a remote 22 edge."""
    word = [0, 1, 2, 1] + [2] * 6
    window_vertices = sorted(
        site for edge in WINDOWS[spectator_index] for site in edge
    )
    require(len(window_vertices) == 4, "window vertices")
    # The canonical h3 tail letters are 1,2,2,2 in increasing local order.
    for site, colour in zip(window_vertices, (1, 2, 2, 2), strict=True):
        word[site] = colour
    return tuple(word)


def dot(left: tuple[int | Q, ...], right: tuple[int | Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


DIFF_01 = (Q(1), Q(-1), Q(0))
DIFF_02 = (Q(1), Q(0), Q(-1))


def word_obstruction_audit() -> dict[str, object]:
    # Exhaust the possible common six-site words, without making a choice of
    # which endpoint of a relabelled h3 window carries its unique tail 1.
    common = []
    for tail_word in product(range(3), repeat=6):
        valid = True
        for spectator in TAIL_EDGES:
            window_colours = [
                tail_word[site - 4] for site in range(4, 10)
                if site not in spectator
            ]
            if sorted(window_colours) != [1, 2, 2, 2]:
                valid = False
                break
        if valid:
            common.append(tail_word)
    require(not common, ("a common cap tail word appeared", common))

    words = tuple(cap_presentation_word(index) for index in range(3))
    require(tuple(map(word_text, words)) == (
        "0121221222", "0121122222", "0121122222"
    ), words)
    first_word_row = tuple(Q(word == words[0]) for word in words)
    second_word_row = tuple(Q(word == words[1]) for word in words)
    require(first_word_row == (1, 0, 0)
            and second_word_row == (0, 1, 1)
            and dot(DIFF_01, first_word_row) == 1
            and dot(DIFF_02, first_word_row) == 1,
            "word mismatch detector")

    # Counting proof: if x_i is the number of 1s on edge i and X=sum x_i,
    # every complement window would force X-x_i=1.  Thus x_i=X-1 and
    # X=3(X-1), i.e. 2X=3, impossible over the integers.
    return {
        "response_words": [word_text(response_word())] * 3,
        "response_word_values_equal": True,
        "cap_words_under_canonical_22_extension": list(map(word_text, words)),
        "cap_word_values_equal": False,
        "first_cap_word_idempotent_values": [1, 0, 0],
        "primitive_detector_values": {
            "(1,-1,0)": 1,
            "(1,0,-1)": 1,
        },
        "exhaustive_common_six_tail_words": len(common),
        "choice_free_counting_obstruction": (
            "X-x_i=1 for i=0,1,2 implies 2X=3"
        ),
        "first_nonzero_mismatch": "physical cap word idempotent",
    }


def fine_and_repeated_audit() -> dict[str, object]:
    records = []
    for family in FAMILIES:
        full_repeated = tuple(
            (
                "P3+K2",
                tuple((SITES[left], SITES[right])
                      for left, right in WINDOWS[index]),
                (SITES[TAIL_EDGES[index][0]],
                 SITES[TAIL_EDGES[index][1]]),
            )
            for index in range(3)
        )
        require(len(set(full_repeated)) == 3,
                ("full repeated labels coalesced", family["name"]))
        cap_fine = tuple(
            "t_{}{}*q_(v,{})".format(
                SITES[TAIL_EDGES[index][0]],
                SITES[TAIL_EDGES[index][1]],
                "|".join(
                    SITES[left] + SITES[right]
                    for left, right in WINDOWS[index]
                ),
            )
            for index in range(3)
        )
        require(len(set(cap_fine)) == 3,
                ("cap fine labels coalesced", family["name"], cap_fine))
        records.append({
            "family": family["name"],
            "operation_type": family["operation"],
            "response_fine_values_equal": True,
            "response_fine_value": (
                family["operation"] + " on intrinsic tail 23|45|67"
            ),
            "cap_fine_values_equal": False,
            "cap_fine_values": list(cap_fine),
            "coarse_missing_doubled_grade": list(
                family["missing_doubled"]
            ),
            "coarse_repeated_topology_values": ["P3+K2"] * 3,
            "coarse_repeated_topology_equal": True,
            "full_window_removed_reinserted_labels": [
                {
                    "window": [list(edge) for edge in label[1]],
                    "spectator_or_reinsertion_edge": list(label[2]),
                }
                for label in full_repeated
            ],
            "full_repeated_labels_equal": False,
        })
    return {
        "fixed_packet_families": len(FAMILIES),
        "presentations_per_family": 3,
        "fixed_presentation_faces": len(FAMILIES) * 3,
        "records": records,
        "fine_mismatch_reason": (
            "the physical cap fine degree is t*q_(v,N), and the PP bridge "
            "retains the presentation's distinct removed/reinsertion edge t "
            "and two-edge window N"
        ),
        "repeated_scope": (
            "coarse P3+K2 agrees; the physical removed-edge, window and "
            "reinsertion labels retained by the PP bridge are distinct"
        ),
    }


def protected_values(mu: tuple[Q, Q, Q]) -> dict[str, tuple[Q, Q, Q]]:
    zero = (Q(0), Q(0), Q(0))
    negative = tuple(-value for value in mu)
    return {
        "target": negative,
        "q": zero,
        "anchor_ainc": zero,
        "ores": mu,
        "W": negative,
        "ridge": mu,
    }


def serializable(values: tuple[Q, ...]) -> list[str]:
    return [str(value) for value in values]


def protected_row_audit() -> dict[str, object]:
    # Before any cross-grade bridge, the exact presentation-safe Xi dual has
    # zero values on all protected cap/Cartan coordinates.  These zeros are
    # an extension of a detector, not a physical assignment to the missing
    # collision/KS source generator.
    current = protected_values((Q(0), Q(0), Q(0)))
    require(all(not any(values) for values in current.values()),
            "current zero-cap extension")

    # If all three transported local bridges are granted with the same
    # normalized coefficient, the cap/Cartan values are scalar-natural.
    equal_mu = (Q(1, 30),) * 3
    transported = protected_values(equal_mu)
    require(all(dot(DIFF_01, values) == dot(DIFF_02, values) == 0
                for values in transported.values()),
            "equal bridge coefficients stopped descending")

    # One isolated local bridge is not overlap-natural and is detected in
    # exactly the target/ores/W/ridge rows forced by the cap equations.
    isolated_mu = (Q(1, 30), Q(0), Q(0))
    isolated = protected_values(isolated_mu)
    require(dot(DIFF_01, isolated["target"]) == Q(-1, 30)
            and dot(DIFF_01, isolated["ores"]) == Q(1, 30)
            and dot(DIFF_01, isolated["W"]) == Q(-1, 30)
            and dot(DIFF_01, isolated["ridge"]) == Q(1, 30)
            and dot(DIFF_01, isolated["q"]) == 0
            and dot(DIFF_01, isolated["anchor_ainc"]) == 0,
            "isolated bridge mismatch values")

    return {
        "current_literal_packet": {
            "physical_cross_grade_bridge_exists": False,
            "physical_presentation_values_defined": False,
            "presentation_safe_Xi_dual_zero_cap_extension": {
                name: serializable(values) for name, values in current.items()
            },
            "warning": (
                "these zeros are dual-extension coordinates and must not be "
                "called physical q/anchor/ridge values of the absent cell"
            ),
        },
        "conditional_three_transported_B0_bridges": {
            "mu": serializable(equal_mu),
            "forced_formula": (
                "target=W=-mu, ores=ridge=mu, q=anchor=0"
            ),
            "presentation_values": {
                name: serializable(values)
                for name, values in transported.items()
            },
            "all_scalar_mismatch_detectors_zero": True,
            "physical_grade_descent": False,
            "reason": "the three bridge copies still occupy the mismatched words",
        },
        "isolated_one_presentation_bridge_control": {
            "mu": serializable(isolated_mu),
            "detector_(1,-1,0)": {
                name: str(dot(DIFF_01, values))
                for name, values in isolated.items()
            },
        },
        "first_protected_row_conclusion": (
            "no unconditional physical values exist before the bridge; "
            "conditionally, equal local bridge coefficients make all six "
            "protected scalar rows equal, but cannot cross the word mismatch"
        ),
    }


def fixed_packet_records() -> dict[str, object]:
    cap_words = tuple(cap_presentation_word(index) for index in range(3))
    records = []
    for family in FAMILIES:
        for index in range(3):
            records.append({
                "family": family["name"],
                "presentation": index,
                "h3_window": [
                    [SITES[left], SITES[right]]
                    for left, right in WINDOWS[index]
                ],
                "spectator_edge": [
                    SITES[TAIL_EDGES[index][0]],
                    SITES[TAIL_EDGES[index][1]],
                ],
                "response_word": word_text(response_word()),
                "cap_word": word_text(cap_words[index]),
                "operation": family["operation"],
            })
    require(len(records) == 12, "fixed packet record count")
    return {"count": len(records), "records": records}


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h4 collision/KS decorated presentation mismatch",
        "pins": PINS,
        "fixed_twelve_face_packet": fixed_packet_records(),
        "word": word_obstruction_audit(),
        "fine_and_repeated": fine_and_repeated_audit(),
        "protected_rows": protected_row_audit(),
        "verdict": (
            "The intrinsic h4 Hasse shuffle does not descend to the existing "
            "physical collision/KS cap grade.  Response word/fine data are "
            "window-independent, but the three physical h3 cap windows "
            "cannot be restrictions of one six-site word.  A canonical 22 "
            "extension gives word-idempotent values (1,0,0), read nonzero "
            "by both primitive overlap differences.  Fine and full repeated "
            "labels also mismatch.  Protected physical values are not "
            "defined because the h3 cross-grade bridge is absent.  If three "
            "equal transported B0 bridges are conditionally granted, their "
            "target/q/anchor/ores/W/ridge scalars agree, but the earlier "
            "word/fine/repeated mismatch remains."
        ),
        "first_failure": {
            "row": "cap word idempotent",
            "presentation_values": [1, 0, 0],
            "detector_values": [1, 1],
            "detectors": ["(1,-1,0)", "(1,0,-1)"],
        },
        "minimum_extra_physical_datum": (
            "a word-changing h4 overlap/connection cell between the three "
            "window-labelled 01211222 copies, retaining fine, removed-edge "
            "and reinsertion labels; only after it exists do the equal-mu "
            "cap/Cartan formulas provide protected-row descent"
        ),
        "scope": (
            "Exact fixed tail 23|45|67 and all four collision families.  "
            "The no-common-word count is independent of the chosen tail "
            "labels and window orientations.  This does not assert a GHZ "
            "spectator tensor factor, construct the missing h3 physical "
            "bridge, or assign physical terminal values to a formal carrier."
        ),
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
    print("h4 decorated collision/KS overlap: FAILS AT CAP WORD")
    print("three cap words: 0121221222, 0121122222, 0121122222")
    print("first word-idempotent values: (1,0,0)")
    print("overlap detectors: (1,-1,0)=1, (1,0,-1)=1")
    print("fine/full repeated labels: MISMATCH")
    print("protected physical rows: UNDEFINED BEFORE MISSING h3 BRIDGE")
    print("conditional equal bridges: PROTECTED SCALARS EQUAL, GRADE STILL FAILS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
