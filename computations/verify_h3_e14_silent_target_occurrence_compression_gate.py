#!/usr/bin/env python3
"""Audit centered-occurrence compression on the silent E14 target fibre.

On ``v04=0`` the private return

    g=(p1_0_1*s1_1_1)u35_11*v24_11

is one of the ninety tagged occurrences of the complete ``G11[111111]``
target row.  In the tagged occurrence module put

    c_g=90 e_g-1_90,       T=1_90-tau.

The unique rational combination of ``c_g,T`` whose occurrence part is
exactly ``e_g`` is ``(c_g+T)/90``.  Consequently it carries target face
``-tau/90``.  Even under the optimistic grant that the response AugP2
section transports to this target occurrence with primitive cap
``p=(-Q,-ores)``, its cap face is only ``p/90``; after the physical K_Eq
lift cancels Q this is ``z_cap/90``.  It is not the normalized mixed cell
with occurrence, target, and scalar-cap coefficients all one.

There is a formal word-changing route: the fourth Hasse coefficient of the
global root ``0 -> 1`` sends the mixed occurrence and complete response row
to their pure-target mates.  It also sends the zero target coefficient to
the affine target row plus the unit.  The complete principal-parts
resolution totalizes its proper faces, but the pinned fourth-Hasse descent
audit proves that its coordinate top is not a physical fixed-fibre map.
Thus the target occurrence section is still unconstructed, before the
factor-90 augmented mismatch is considered.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_private_return_localization_unit_fork.py":
        "8ed9667a4ac5e2fb362e67c1a2f37e90a32a389e46c4e694361a43ad1d370f86",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py":
        "4dabdae7b9060bdb92c0ed32b0016e7e2694750dc176e1857cc9a54cb8176587",
    "computations/verify_h3_c6_e14_minimal_enlargement_unit.py":
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py":
        "754038f33ae07329e0fc6a8825df9f1695664a40df91afbb77e52dedb1e1aae1",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
    "computations/verify_h3_source_valid_tower_first_obstruction.py":
        "ba37c966c2ef2cca2f8909a91e8ff8a8567282e68a847ac4eef75d3bb78a56ac",
}
EXPECTED_LEDGER_SHA256 = (
    "030d56344cfef4698fe070e175a207a8227fd9d885380a97e8fb975b7696cc8e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, ("loop", left, right))
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def occurrences() -> tuple[tuple[int, int, tuple[tuple[int, int], ...]], ...]:
    sites = tuple(range(6))
    answer = []
    for p_site in sites:
        for s_site in sites:
            if p_site == s_site:
                continue
            residual = tuple(site for site in sites
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == 90,
            "the six-site response occurrence census changed")
    return tuple(answer)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    rows = [list(map(Q, row)) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
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


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(value: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(value * entry for entry in vector)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def tagged_occurrence_audit() -> dict[str, object]:
    inventory = occurrences()
    # The two q factors in g are q35:11 and q24:11; with endpoint colours
    # p1@0:1 and s1@1:1, every output site has colour 1.
    marked = (0, 1, ((2, 4), (3, 5)))
    require(marked in inventory, "the private return lost its occurrence tag")
    marked_index = inventory.index(marked)
    target_word = (1, 1, 1, 1, 1, 1)
    response_word = (1, 1, 0, 0, 0, 0)
    require(sorted(target_word) != sorted(response_word),
            "the pure and mixed words unexpectedly entered one site orbit")
    colour_multiplicities = lambda word: tuple(word.count(colour)
                                                for colour in range(3))
    target_mult = colour_multiplicities(target_word)
    response_mult = colour_multiplicities(response_word)
    require(target_mult == (0, 6, 0)
            and response_mult == (4, 2, 0)
            and sorted(target_mult) != sorted(response_mult),
            "a site/global-colour transport obstruction changed")
    return {
        "complete_G11_target_occurrences": len(inventory),
        "marked_private_return_index": marked_index,
        "marked_tag": {
            "p_site_colour": "0:1",
            "s_site_colour": "1:1",
            "residual_matching": ["24:11", "35:11"],
        },
        "marked_monomial": "(p1_0_1*s1_1_1)u35_11*v24_11",
        "target_word": "111111",
        "response_centered_word": "110000",
        "colour_multiplicities": {
            "target": list(target_mult),
            "response": list(response_mult),
        },
        "site_or_global_colour_transport_exists": False,
    }


def four_root_hasse_audit() -> dict[str, object]:
    # Use the response occurrence with the *same* endpoint/matching tag as g
    # and change the four residual site colours 0 -> 1.  Under the global
    # unipotent 0 -> 0+t*1, a word with four zero sites has coefficients
    # C(4,k) at Hasse levels k.  The top coefficient is one and preserves
    # the occurrence tag.
    binomial_profile = (1, 4, 6, 4, 1)
    require(sum(binomial_profile) == 16
            and binomial_profile[-1] == 1,
            "the four-root Boolean Hasse profile changed")

    # Write G_m for the complete mixed coefficient (target value zero), G_t
    # for the pure coefficient, and F_t=G_t-1 for its affine source row.
    # The top Hasse coefficient is D4(G_m)=G_t=F_t+1.  Applying it to the
    # centered expression gives
    #
    #   D4(90 P_f-G_m)=90 P_g-G_t,
    #
    # whose value modulo F_t is 90g-1.  This is the exact target-constant
    # conversion suggested by the localization fork.
    # Coordinates here are (P_g,G_t,F_t,unit).
    d4_mixed_row = tuple(map(Q, (0, 1, -1, -1)))
    require(d4_mixed_row == tuple(map(Q, (0, 1, -1, -1))),
            "D4(G_m)=F_t+1 encoding changed")
    centered_top = tuple(map(Q, (90, -1, 0, 0)))
    target_substitution = tuple(map(Q, (0, 1, -1, -1)))
    modulo_target = add(centered_top, target_substitution)
    require(modulo_target == tuple(map(Q, (90, 0, -1, -1))),
            "the 90g-1 target conversion changed")

    return {
        "global_root": "0 -> 1 on the four zero output sites",
        "source_word": "110000",
        "top_word": "111111",
        "same_occurrence_tag": "p@0,s@1, residual 24|35",
        "Boolean_face_profile": list(binomial_profile),
        "top_occurrence_coefficient": 1,
        "complete_row_identity": "D4(G11[110000])=G11[111111]=F_target+1",
        "centered_identity": (
            "D4(90 P_f-G_m)=90 P_g-G_t; modulo F_target this is 90g-1"
        ),
        "formal_complete_PP_totalization_exists": True,
        "physical_fixed_fibre_descent_exists": False,
        "descent_obstruction": (
            "the coordinate fourth operator sends the selected source "
            "equation to a unit; the prolonged cone has a nonzero "
            "underived (H0-u)e0 projection defect"
        ),
    }


def augmented_compression_audit() -> dict[str, object]:
    # Coordinates:
    #   marked occurrence, one common unmarked occurrence coefficient,
    #   affine target normal, cap Q, cap ordinary residue.
    # The two occurrence coordinates suffice because c_g and T are constant
    # on all 89 unmarked tags.
    #
    # Strong optimistic grant: a target-word lift of c_g has the same
    # primitive cap p=(-Q,-ores) as the response AugP2 lift.  No committed
    # theorem supplies this cross-word lift; granting it makes the no-go
    # stronger.
    centered = tuple(map(Q, (89, -1, 0, -1, -1)))
    target_row = tuple(map(Q, (1, 1, -1, 0, 0)))
    isolated = scale(Q(1, 90), add(centered, target_row))
    require(isolated == tuple(map(Q, (
        1, 0, Q(-1, 90), Q(-1, 90), Q(-1, 90)
    ))), "the unique centered/target compression changed")

    # Solving a*c_g+b*T=e_g on occurrence coordinates gives b=a and
    # 90a=1.  The occurrence projection of the two columns is invertible,
    # so no combination supported on these two columns can alter the forced
    # augmented faces while leaving e_g fixed.
    require(rank((centered, target_row)) == 2,
            "the centered and target rows stopped being independent")
    occurrence_matrix_determinant = 89 * 1 - 1 * (-1)
    require(occurrence_matrix_determinant == 90,
            "the occurrence isolation index changed")

    # The physical invisible K_Eq lift n=(+Q,0) cancels the Q component.
    invisible_keq = tuple(map(Q, (0, 0, 0, Q(1, 90), 0)))
    after_keq = add(isolated, invisible_keq)
    require(after_keq == tuple(map(Q, (
        1, 0, Q(-1, 90), 0, Q(-1, 90)
    ))), "the post-K_Eq scalar residue changed")

    # The normalized mixed target/cap cell would have coefficient one on g,
    # target -1, Q zero, and scalar cap residue -1.  It is not in the span of
    # the two occurrence columns (even allowing the prescribed K_Eq Q reset).
    desired_after_keq = tuple(map(Q, (1, 0, -1, 0, -1)))
    require(rank((centered, target_row, desired_after_keq)) == 3,
            "the normalized target/cap cell entered the two-column span")
    residual = add(desired_after_keq, scale(-1, after_keq))
    require(residual == tuple(map(Q, (
        0, 0, Q(-89, 90), 0, Q(-89, 90)
    ))), "the affine target/cap normalization residual changed")

    # A primitive integral formulation avoids division: c_g+T has principal
    # coefficient 90 while target and cap coefficients remain primitive.
    integral = add(centered, target_row)
    require(integral == tuple(map(Q, (90, 0, -1, -1, -1))),
            "the integral compression signature changed")

    return {
        "row_order": [
            "marked occurrence", "common unmarked occurrence",
            "affine target normal", "cap Q", "cap scalar ores",
        ],
        "optimistic_granted_c_g_lift": list(map(str, centered)),
        "complete_target_row": list(map(str, target_row)),
        "unique_occurrence_isolation_coefficients": {
            "c_g": "1/90", "target_row": "1/90",
        },
        "isolated_signature_before_K_Eq": list(map(str, isolated)),
        "isolated_signature_after_K_Eq": list(map(str, after_keq)),
        "normalized_desired_signature_after_K_Eq":
            list(map(str, desired_after_keq)),
        "remaining_target_and_cap_residual": list(map(str, residual)),
        "integral_signature_c_g_plus_target": list(map(str, integral)),
        "occurrence_isolation_index": occurrence_matrix_determinant,
        "verdict": (
            "c_g plus the target row isolates g only with target and cap "
            "normalization 1/90; primitive target/cap normalization would "
            "require a new occurrence-zero augmented correction"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "silent E14 target-occurrence compression gate",
        "pins": PINS,
        "tagged_occurrence": tagged_occurrence_audit(),
        "four_root_Hasse_route": four_root_hasse_audit(),
        "augmented_compression": augmented_compression_audit(),
        "physical_typing": {
            "existing_AugP2_naturality": (
                "marked lower response occurrence/root/reinsertion grades"
            ),
            "desired_new_domain": "pure target G11[111111] occurrence g",
            "transport_constructed": False,
            "first_typing_failure": (
                "site/global-colour permutations do not connect the word "
                "idempotents; the formal fourth-Hasse root route does, but "
                "its top does not descend to the physical fixed-fibre map"
            ),
            "stronger_conditional_failure": (
                "even granting the cross-word c_g lift with primitive cap, "
                "the unique isolated g has target and z_cap faces 1/90 of "
                "the normalized E14 mixed-cell faces"
            ),
        },
        "shortest_positive_addition": (
            "a physical comparison from the complete four-root PP "
            "totalization to an affine target-normalized AugP2 occurrence "
            "section on the pure G11 word, whose occurrence-zero correction changes target "
            "and scalar cap residue by -89/90 while preserving the marked "
            "principal coefficient; equivalently an integral section with "
            "principal/target/cap signature (1,-1,-1), not (90,-1,-1)"
        ),
        "scope": (
            "canonical h=3 chart-(1,1), silent v04=0 private return.  The "
            "90-occurrence and augmented rank statements are exact over Q. "
            "The cap signature is an optimistic grant of the still-open "
            "cross-word AugP2 transport, not a claimed physical source cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("silent target-occurrence ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("silent E14 target occurrence: 90 tags; g is literal: PASS")
    print("unique isolation: (c_g+target)/90")
    print("formal D4 route: 90f -> 90g-1; physical descent OPEN")
    print("forced target/z_cap normalization: -1/90, -1/90")
    print("normalized E14 target/z_cap cell: OUTSIDE TWO-COLUMN SPAN")
    print("cross-word AugP2 transport: NOT CONSTRUCTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
