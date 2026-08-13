#!/usr/bin/env python3
"""Separate Gate-II relabeling from its minimal pointed mapping cylinder.

The canonical physical Cartan boundary is the mixed character of the
root/endpoint V4 orbit.  The occurrence-asymmetric direction needed by the
trapped fan packet is the root-only character.  Physical site/colour
relabeling conjugates root operations to root operations and endpoint-site
transpositions to endpoint-site transpositions.  It therefore preserves the
ordered pair of character signs and cannot identify these two directions.
Multiplication by the common remote q tail is V4-trivial and does not change
the obstruction.

At the linear mapping-cylinder level one new occurrence direction and one
mixed-target companion are necessary and sufficient.  The root-only face
has target defect

    delta = m_(c|i) + m_(i|c) - p_i - p_c,

which is independent of the two normalized pure-target rows.  A paired
relative cylinder (root,delta)+(0,-delta) gives the missing target-zero root
line.  This is a finite exact interface, not a construction of its physical
source-labelled companion.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_extra_mate_deletion_or_gate_ii.py":
        "337e739a7392e207c37e9aa5fe0f0900d90c967bb764c981f3f71b2922f7036d",
    "notes/h3-active-coloop-extra-mate-deletion-or-gate-ii.md":
        "0a8d3767bc348c606beaf631c77a6f26e8c0bd0b0fd524eb9748372138b22af0",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "notes/h3-active-fan-coloop-complete-row-pivot.md":
        "2a68b7a9da9c61c67c4f63e666a6cbb1023344722943b9042f2ff15b2863e92e",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
    "notes/h3-gate-ii-cartan-full-q-pointed-character-gate.md":
        "3ffd0d0894dfbb81cb672f87548b3b7a2da28ac1b36a6466bbef6ad149cf0933",
    "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py":
        "86db5c89196a183c5ddc2b1c2198029fa45ea1cdff1f7d239a74870cd4957e94",
    "notes/h3-fan-coloop-packet-q-comparison-defect.md":
        "a66eff0a65488b3c4f824a2558cc093d57a0ba8f9ec6c2ffc3af57b630a9ea6d",
}
EXPECTED_LEDGER_SHA256 = (
    "2b6becf27bf6755c5580d9fad63d90271c3d4ee6a42a8057b73369941a601c15"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add(left, right):
    return tuple(Q(a) + Q(b)
                 for a, b in zip(left, right, strict=True))


def subtract(left, right):
    return tuple(Q(a) - Q(b)
                 for a, b in zip(left, right, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def audit_physical_orbit_invariant():
    # Corner order is 1,w,s,sw.  The sign pair is ordered as
    # (root-Weyl sign, endpoint-site-transposition sign).
    trivial = tuple(map(Q, (1, 1, 1, 1)))
    root_only = tuple(map(Q, (1, -1, 1, -1)))
    endpoint_only = tuple(map(Q, (1, 1, -1, -1)))
    mixed = tuple(map(Q, (1, -1, -1, 1)))
    characters = {
        (1, 1): trivial,
        (-1, 1): root_only,
        (1, -1): endpoint_only,
        (-1, -1): mixed,
    }
    require(rank(tuple(characters.values())) == 4,
            "the root/endpoint character decomposition changed")
    for signs, row in characters.items():
        root_sign, endpoint_sign = signs
        w_action = (row[1], row[0], row[3], row[2])
        s_action = (row[2], row[3], row[0], row[1])
        require(w_action == scale(root_sign, row)
                and s_action == scale(endpoint_sign, row),
                ("character sign changed", signs, row))

    # A physical relabeling may move the two root sites, the endpoint pair,
    # and the colours, but it does not exchange a local colour-root action
    # with a site transposition.  Conjugation preserves both eigenvalues.
    canonical_signs = (-1, -1)
    required_signs = (-1, 1)
    require(canonical_signs != required_signs
            and characters[canonical_signs] == mixed
            and characters[required_signs] == root_only,
            "the physical Cartan/pointed character distinction changed")

    # The common remote q tail is fixed by both actions, hence has trivial
    # character.  Tensoring with it leaves the sign pair unchanged.
    tail_signs = (1, 1)
    transported_canonical = tuple(left * right for left, right in
                                  zip(canonical_signs, tail_signs,
                                      strict=True))
    transported_required = tuple(left * right for left, right in
                                 zip(required_signs, tail_signs,
                                     strict=True))
    require(transported_canonical == canonical_signs
            and transported_required == required_signs,
            "common-tail normalization changed an orbit character")

    marked = (Q(1), Q(0), Q(0), Q(0))
    reconstruction = scale(Q(1, 4), tuple(sum(entries) for entries in
                                           zip(*characters.values(),
                                               strict=True)))
    require(reconstruction == marked,
            "the pointed occurrence decomposition changed")
    return {
        "corner_order": ["1", "w", "s", "sw"],
        "canonical_endpoint_odd_Cartan_character": {
            "name": "chi_ws", "sign_pair": list(canonical_signs),
            "row": list(map(int, mixed)),
        },
        "required_occurrence_asymmetric_character": {
            "name": "chi_w", "sign_pair": list(required_signs),
            "row": list(map(int, root_only)),
        },
        "physical_relabeling_preserves": [
            "root-operation kind", "endpoint-transposition kind",
            "the two ordered eigenvalues",
        ],
        "common_remote_q_tail_character": list(tail_signs),
        "orbit_identification_exists": False,
        "marked_occurrence":
            "P_f=(chi_1+chi_w+chi_s+chi_ws)/4",
    }


def transversal(family, edges):
    return frozenset(candidate for candidate in edges
                     if all(set(candidate) & set(member)
                            for member in family))


def audit_full_packet_support_guard():
    # This is a secondary invariant for the *complete supported packet*.
    # It is not used to deny that one literal occurrence can be relabeled.
    vertices = tuple(range(6))
    edges = tuple(combinations(vertices, 2))
    triangle = frozenset(((0, 1), (0, 2), (1, 2)))
    matching = frozenset(((0, 3), (1, 2)))
    path = frozenset(((0, 1), (0, 3), (1, 2)))
    adjacent = frozenset(((0, 1), (0, 2)))
    singleton = frozenset(((0, 1),))
    star = frozenset((tuple(sorted((0, site))) for site in range(1, 6)))
    representatives = (triangle, matching, path, adjacent, singleton, star)
    union_sizes = []
    degree_sequences = []
    for shore in representatives:
        mate = transversal(shore, edges)
        support = shore | mate
        degrees = tuple(sorted((sum(vertex in edge for edge in support)
                                for vertex in vertices), reverse=True))
        union_sizes.append(len(support))
        degree_sequences.append(degrees)
    require(union_sizes == [3, 6, 5, 6, 9, 5]
            and max(union_sizes) < len(edges),
            ("closed-shore union census changed", union_sizes))
    return {
        "canonical_complete_endpoint_holes": len(edges),
        "six_closed_shore_union_sizes": union_sizes,
        "six_closed_shore_union_degree_sequences":
            [list(values) for values in degree_sequences],
        "consequence": (
            "a wholly trapped nonzero full packet has a proper hole-support "
            "graph, so it is not a relabeling of the complete 15-hole "
            "endpoint-port packet; this does not obstruct relabeling one "
            "individual carrier occurrence"
        ),
    }


def audit_minimal_pointed_mapping_cylinder():
    # Occurrence orbit module, corner order 1,w,s,sw.
    trivial = tuple(map(Q, (1, 1, 1, 1)))
    root = tuple(map(Q, (1, -1, 1, -1)))
    endpoint = tuple(map(Q, (1, 1, -1, -1)))
    mixed = tuple(map(Q, (1, -1, -1, 1)))
    available = (trivial, endpoint, mixed)
    marked = (Q(1), Q(0), Q(0), Q(0))
    marked_without_root = scale(Q(1, 4), tuple(
        trivial[index] + endpoint[index] + mixed[index]
        for index in range(4)))
    require(rank(available) == 3
            and rank(available + (root,)) == 4
            and subtract(marked, marked_without_root) == scale(Q(1, 4), root),
            "the minimal pointed occurrence face changed")

    # Target word basis is m_(c|i),m_(i|c),p_i,p_c.
    pure_i = tuple(map(Q, (0, 0, 1, 0)))
    pure_c = tuple(map(Q, (0, 0, 0, 1)))
    delta = tuple(map(Q, (1, 1, -1, -1)))
    target_old = (pure_i, pure_c)
    require(rank(target_old) == 2
            and rank(target_old + (delta,)) == 3,
            "the mixed-target companion quotient changed")

    zero_occurrence = (Q(0),) * 4
    zero_target = (Q(0),) * 4
    root_face = (root, delta)
    principal_companion = (zero_occurrence, scale(-1, delta))
    closed = (add(root_face[0], principal_companion[0]),
              add(root_face[1], principal_companion[1]))
    require(closed == (root, zero_target),
            "the minimal root/target mapping cylinder stopped closing")

    # Neither half can be omitted.  The first supplies the unique missing
    # occurrence line; the second supplies the unique non-pure target class.
    require(rank(available + (root_face[0],)) == 4
            and rank(available + (principal_companion[0],)) == 3
            and rank(target_old + (root_face[1],)) == 3
            and rank(target_old + (closed[1],)) == 2,
            "the minimality ranks of the paired cylinder changed")
    return {
        "occurrence_quotient": {
            "available_rank": 3,
            "rank_with_root_face": 4,
            "pointed_residual": "P_f-P_available=chi_w/4",
        },
        "target_quotient": {
            "old_pure_target_rank": 2,
            "rank_with_delta": 3,
            "delta": [1, 1, -1, -1],
            "word_basis": ["m_(c|i)", "m_(i|c)", "p_i", "p_c"],
        },
        "formal_paired_cylinder": {
            "root_face": "(chi_w,delta)",
            "principal_companion": "(0,-delta)",
            "closed_sum": "(chi_w,0)",
        },
        "minimality": (
            "one root-only occurrence line and one mixed-target companion "
            "class are both forced; they may be faces of one relative PP/"
            "Spencer mapping-cylinder object, not two independent global "
            "theorems"
        ),
        "physical_status": (
            "formal finite cylinder only: the missing theorem must realize "
            "the principal companion by a source-labelled C2+/C4/P2 Hasse "
            "cell in the identical fan word/fine/repeated/common-tail grade"
        ),
    }


def audit_q_and_pointed_anchor_rows():
    root = tuple(map(Q, (1, -1, 1, -1)))

    # After all three available characters are quotiented out, matching and
    # anchor comparison defects are scalar multiples of the one root line.
    # The literal q identity is componentwise and supplies no implication in
    # either direction between matching transport and pointedness.
    records = []
    for matching_coefficient, anchor_coefficient in ((0, 0), (1, 0),
                                                       (0, 1), (1, 1)):
        matching_defect = scale(matching_coefficient, root)
        anchor_defect = scale(anchor_coefficient, root)
        q_defect = subtract(matching_defect, anchor_defect)
        require(q_defect == scale(
            matching_coefficient - anchor_coefficient, root),
            "q=M-a stopped holding in the root quotient")
        records.append({
            "delta_M": matching_coefficient,
            "delta_a": anchor_coefficient,
            "delta_q_root_coefficient":
                matching_coefficient - anchor_coefficient,
        })

    # The marked anchor has exactly one-quarter of the missing root row after
    # the existing three characters are removed.
    pointed_root_coefficient = Q(1, 4)
    require(scale(pointed_root_coefficient, root)
            == tuple(map(Q, (Q(1, 4), Q(-1, 4),
                             Q(1, 4), Q(-1, 4)))),
            "the H=P_f root coefficient changed")
    return {
        "root_quotient_defects": records,
        "literal_identity": "delta_q=delta_M-delta_a",
        "termwise_common_tail_matching_transport":
            "delta_M=0 implies delta_q=-delta_a",
        "pointed_anchor_requirement":
            "H=P_f has residual chi_w/4 after the three available lines",
        "independence": (
            "q transport alone does not construct H=P_f: delta_M=delta_a "
            "may cancel in q while both are nonzero.  Conversely pointed "
            "anchor transport without matching transport leaves a q defect"
        ),
        "post_comparison_alternative": (
            "once a physical Phi exists, a nonzero [delta_q] is consumed by "
            "the pinned physical-q witness alternative; a zero class is "
            "removed by a protected-row correction"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II physical-orbit obstruction and pointed cylinder",
        "pins": PINS,
        "physical_orbit_invariant": audit_physical_orbit_invariant(),
        "complete_packet_support_guard": audit_full_packet_support_guard(),
        "minimal_pointed_mapping_cylinder":
            audit_minimal_pointed_mapping_cylinder(),
        "physical_q_and_pointed_anchor": audit_q_and_pointed_anchor_rows(),
        "sharp_verdict": (
            "Common-tail normalization and physical relabeling do not turn "
            "the canonical endpoint-odd Cartan packet into the pointed "
            "trapped fan packet.  The ordered root/endpoint character is an "
            "exact orbit invariant: Cartan supplies chi_ws while pointedness "
            "needs chi_w.  The smallest formal repair is one paired relative "
            "cylinder with root face (chi_w,delta) and principal face "
            "(0,-delta).  Its sole unconstructed datum is a source-labelled "
            "mixed-target companion in the identical C2+/C4/P2 grade.  It "
            "must separately carry H=P_f and the literal q=M-a rows"
        ),
        "scope": (
            "exact h=3 orbit-character, full-hole-support, target-rank and "
            "augmented-row interface.  It constructs only the formal finite "
            "mapping cylinder, not its physical source-labelled Hasse/PP "
            "realization and not a complete trapped GHZ source"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Gate-II physical orbit ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("Gate II relabeling orbit: NO (chi_ws != chi_w)")
    print("common-tail multiplication: CHARACTER-TRIVIAL")
    print("minimal formal repair: ONE ROOT FACE + ONE MIXED-TARGET COMPANION")
    print("physical source-labelled companion: OPEN")
    print("H=P_f and q=M-a: SEPARATE AUGMENTED ROWS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
