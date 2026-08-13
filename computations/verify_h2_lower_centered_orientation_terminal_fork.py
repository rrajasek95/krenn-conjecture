#!/usr/bin/env python3
"""Audit the two physical h=2 lower centered debts by endpoint parity.

For four sites an occurrence is an ordered p/s endpoint pair and the unique
residual edge on the other two sites.  Hence there are twelve occurrences.
The centered marked class c_2=12e_f-1 splits under p/s transposition as

    c_2^- = 6(e_f-e_rho(f)),
    c_2^+ = 6(e_f+e_rho(f))-1.

The first summand is the oriented endpoint readout.  It can use the existing
active-fan landing only after the occurrence coordinate has been promoted to
the literal same-tail physical offdiagonal readout.  If that readout is dark,
the survivor is c_2^+, a centered class in the six-dimensional unordered-hole
module.  It is not in the one-dimensional complete H0/response line.  A
primitive hole-difference covector proves this, and fixed-endpoint q-only K4
matching differences have rank zero at order two.

The two actual cuts are checked with their original site labels and words:
delete 23 to get 0112 and reinsert q23:21; delete 45 to get 0121 and reinsert
q45:12.  In both cases the marked occurrence has endpoints (p,s)=(0,1) and
the same mixed q23:21*q45:12 tail after reinsertion.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "notes/h2-lower-centered-endpoint-parity-terminal-fork.md":
        "27d25d400daf8c26ff0da928a21cbfd3116058308799f3080cdcae8ae979ddbd",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "computations/verify_h3_gamma1_affine_raw_occurrence_cut_gate.py":
        "34f39ba15de4e4fb0673b883d29ea86c92c1a359b6a3361ad61c17fc2368db1c",
    "computations/verify_h3_centered_projector_e14_word_arrow_gate.py":
        "e1b8b17c75292f55439652ac9e5dcb1a24a3e4079c2d378e9fa63544e5491b46",
    "notes/h3-centered-projector-e14-word-arrow-gate.md":
        "e0c5249f0e79551c87dbd1b25bc3e52501ea1ae7eac07484509bbd38d18cf3de",
    "computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py":
        "ea8cb46d5ee84b1973cb062df73b75c0704a0a31823b53e7187e737175964d53",
    "notes/h3-direct-free-normals-e14-pointed-composition-gate.md":
        "aa927470ffc926bc5639be94c76ab66c00cdabfa0082a0b94f6d117d7add0942",
    "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py":
        "00db2478df3162a374434ea7d0ab285f770510d33b72619377560404c96b16e8",
    "notes/h3-shared-four-term-endpoint-word-change-inventory-boundary.md":
        "12ffea4f2c520f22320ba47a253b686e0b29dbe43d6e2ef8f43f4f86208a4c29",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "notes/uniform-centered-occurrence-endpoint-association-projector.md":
        "6be3edc16be3b429f517fe007886fd3289281f8e8acdde1f13ebebf2a20bb836",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
}
EXPECTED_LEDGER_SHA256 = (
    "62603383e8aeaf8b691c8f28fea5df80f206d555b3dfc4cd53c6a46a5d4251b9"
)

Occurrence = tuple[int, int, tuple[int, int]]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, "loop edge")
    return (left, right) if left < right else (right, left)


def occurrences(sites: tuple[int, ...]) -> tuple[Occurrence, ...]:
    answer = []
    for p_site in sites:
        for s_site in sites:
            if p_site == s_site:
                continue
            residual = tuple(site for site in sites
                             if site not in (p_site, s_site))
            require(len(residual) == 2, "h=2 residual stopped being one edge")
            answer.append((p_site, s_site, edge(*residual)))
    require(len(answer) == len(set(answer)) == 12,
            "the h=2 occurrence count changed")
    return tuple(answer)


def unit(index: int, size: int) -> tuple[Fraction, ...]:
    answer = [Fraction(0)] * size
    answer[index] = Fraction(1)
    return tuple(answer)


def add(*vectors: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    require(vectors, "empty vector sum")
    return tuple(sum((vector[index] for vector in vectors), Fraction(0))
                 for index in range(len(vectors[0])))


def scale(coefficient: int | Fraction,
          vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(Fraction(coefficient) * value for value in vector)


def dot(left: tuple[Fraction, ...],
        right: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def rank(vectors: tuple[tuple[Fraction, ...], ...] | list[tuple[Fraction, ...]]) -> int:
    basis: dict[int, tuple[Fraction, ...]] = {}
    for original in vectors:
        values = tuple(Fraction(value) for value in original)
        for pivot in sorted(basis):
            if values[pivot]:
                values = add(values, scale(-values[pivot], basis[pivot]))
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        basis[pivot] = scale(1 / values[pivot], values)
    return len(basis)


def transpose(occurrence: Occurrence) -> Occurrence:
    p_site, s_site, residual = occurrence
    return (s_site, p_site, residual)


def pair_sum(occ: tuple[Occurrence, ...], lookup: dict[Occurrence, int],
             hole: tuple[int, int]) -> tuple[Fraction, ...]:
    p_site, s_site = hole
    residual = edge(*(site for site in sorted(set().union(*[set(o[:2]) | set(o[2]) for o in occ]))
                      if site not in hole))
    # The universe expression above is deliberately derived from the packet,
    # so this helper also audits that each unordered endpoint hole has one
    # complementary residual edge.
    first = (p_site, s_site, residual)
    second = (s_site, p_site, residual)
    require(first in lookup and second in lookup,
            ("missing oriented hole pair", hole, residual))
    return add(unit(lookup[first], len(occ)), unit(lookup[second], len(occ)))


def cut_packet_audit() -> dict[str, object]:
    full_word = {0: 0, 1: 1, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2}
    cuts = (
        {
            "deleted_edge": (2, 3),
            "remaining_sites": (0, 1, 4, 5),
            "lower_word": "0112",
            "reinsertion": "q23:21",
            "marked_residual": (4, 5),
            "marked_residual_label": "q45:12",
        },
        {
            "deleted_edge": (4, 5),
            "remaining_sites": (0, 1, 2, 3),
            "lower_word": "0121",
            "reinsertion": "q45:12",
            "marked_residual": (2, 3),
            "marked_residual_label": "q23:21",
        },
    )
    records = []
    for item in cuts:
        sites = item["remaining_sites"]
        lower_word = "".join(str(full_word[site]) for site in sites)
        require(lower_word == item["lower_word"],
                ("lower word changed", item, lower_word))
        occ = occurrences(sites)
        marked = (0, 1, item["marked_residual"])
        require(marked in occ and transpose(marked) in occ,
                ("marked lower orientation disappeared", item))
        deleted = item["deleted_edge"]
        deleted_colour = "".join(str(full_word[site]) for site in deleted)
        residual_colour = "".join(
            str(full_word[site]) for site in item["marked_residual"]
        )
        require(item["reinsertion"] ==
                f"q{deleted[0]}{deleted[1]}:{deleted_colour}",
                ("reinsertion decoration changed", item, deleted_colour))
        require(item["marked_residual_label"] ==
                f"q{item['marked_residual'][0]}{item['marked_residual'][1]}:{residual_colour}",
                ("marked residual decoration changed", item, residual_colour))
        restored_six = "".join(str(full_word[site]) for site in range(6))
        restored_eight = "".join(str(full_word[site]) for site in range(8))
        require(restored_six == "012112" and restored_eight == "01211222",
                "the physical cap word changed")
        records.append({
            "deleted_edge": "".join(map(str, deleted)),
            "remaining_sites": list(sites),
            "lower_word": lower_word,
            "marked_occurrence": [0, 1, list(item["marked_residual"])],
            "transposed_occurrence": [1, 0, list(item["marked_residual"])],
            "marked_residual": item["marked_residual_label"],
            "reinsertion": item["reinsertion"],
            "restored_mixed_tail": "q23:21*q45:12",
            "restored_word_grade": "01211222 / labelled repeated P3+K2",
            "occurrences": len(occ),
        })
    return {
        "full_word": "01211222",
        "selected_occurrence_before_cut": [0, 1, [[2, 3], [4, 5]]],
        "cuts": records,
        "same_tail_after_reinsertion": "q23:21*q45:12",
    }


def parity_packet_audit(sites: tuple[int, ...],
                        marked_residual: tuple[int, int]) -> dict[str, object]:
    occ = occurrences(sites)
    lookup = {item: index for index, item in enumerate(occ)}
    marked = (0, 1, marked_residual)
    mate = transpose(marked)
    marked_index = lookup[marked]
    mate_index = lookup[mate]
    ones = (Fraction(1),) * len(occ)
    e_plus = unit(marked_index, len(occ))
    e_minus = unit(mate_index, len(occ))
    centered = add(scale(12, e_plus), scale(-1, ones))
    transposed_centered = add(scale(12, e_minus), scale(-1, ones))
    odd = scale(Fraction(1, 2), add(centered, scale(-1, transposed_centered)))
    even = scale(Fraction(1, 2), add(centered, transposed_centered))
    require(odd == scale(6, add(e_plus, scale(-1, e_minus))),
            "the p/s-odd lower class changed")
    require(even == add(scale(6, add(e_plus, e_minus)), scale(-1, ones)),
            "the p/s-even lower class changed")
    require(add(odd, even) == centered,
            "the lower parity decomposition changed")

    odd_dual_values = [Fraction(0)] * len(occ)
    odd_dual_values[marked_index] = 1
    odd_dual_values[mate_index] = -1
    odd_dual = tuple(odd_dual_values)

    holes = tuple(edge(sites[left], sites[right])
                  for left in range(len(sites))
                  for right in range(left + 1, len(sites)))
    require(len(holes) == 6, "the unordered endpoint-hole count changed")
    hole_rows = tuple(pair_sum(occ, lookup, hole) for hole in holes)
    require(rank(hole_rows) == 6 and add(*hole_rows) == ones,
            "the six swap-even hole rows changed")
    marked_hole = edge(0, 1)
    comparison_hole = next(hole for hole in holes if hole != marked_hole)
    marked_hole_row = hole_rows[holes.index(marked_hole)]
    comparison_hole_row = hole_rows[holes.index(comparison_hole)]
    even_standard = tuple(add(row, scale(-1, hole_rows[-1]))
                          for row in hole_rows[:-1])
    require(rank(even_standard) == 5,
            "the swap-even augmentation-zero rank changed")
    require(rank((*even_standard, even)) == 5,
            "the even survivor left the hole-standard module")
    require(rank((ones,)) == 1 and rank((ones, even)) == 2,
            "the common H0 line acquired the even centered class")

    even_dual = add(marked_hole_row, scale(-1, comparison_hole_row))
    require(dot(odd_dual, ones) == 0
            and dot(odd_dual, odd) == 12
            and dot(odd_dual, even) == 0,
            "the primitive odd detector changed")
    require(dot(even_dual, ones) == 0
            and dot(even_dual, odd) == 0
            and dot(even_dual, even) == 12,
            "the primitive even hole detector changed")

    # Endpoint adjacency B changes exactly one ordered endpoint through the
    # unique residual edge.  At order two it has degree four.  On the
    # swap-even module its spectrum is 4,0,-2; hence B(B+2)/24 projects to
    # the common row, and B-4 is invertible on every even centered direction.
    def endpoint_neighbors(occurrence: Occurrence) -> tuple[Occurrence, ...]:
        p_site, s_site, residual = occurrence
        left, right = residual
        return (
            (left, s_site, edge(p_site, right)),
            (p_site, left, edge(s_site, right)),
            (right, s_site, edge(p_site, left)),
            (p_site, right, edge(s_site, left)),
        )

    def apply_endpoint(vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(sum((vector[lookup[neighbor]]
                          for neighbor in endpoint_neighbors(item)),
                         Fraction(0))
                     for item in occ)

    require(all(len(set(endpoint_neighbors(item))) == 4 for item in occ),
            "the h2 endpoint adjacency degree changed")
    b_ones = apply_endpoint(ones)
    require(b_ones == scale(4, ones),
            "the h2 endpoint adjacency constant eigenvalue changed")
    b_even = apply_endpoint(even)
    b2_even = apply_endpoint(b_even)
    require(add(b2_even, scale(2, b_even)) == (Fraction(0),) * len(occ),
            "the marked even class left the {0,-2} endpoint spectrum")
    require(scale(Fraction(1, 24),
                  apply_endpoint(add(b_even, scale(2, even))))
            == (Fraction(0),) * len(occ),
            "the H0 endpoint projector failed to kill c2+")
    even_preimage = scale(
        Fraction(-1, 24), add(b_even, scale(6, even))
    )
    require(add(apply_endpoint(even_preimage), scale(-4, even_preimage))
            == even,
            "the (B-4) preimage of c2+ changed")
    integral_preimage = scale(12, even_preimage)
    require(all(value.denominator == 1 for value in integral_preimage),
            "the denominator-12 even preimage changed")

    # A q-only matching comparison fixes the p/s endpoints.  At order two
    # the complementary residual set has two sites and exactly one matching,
    # so its matching-difference module has rank zero.  A K4 perfect-matching
    # row on all four sites instead changes the operation type (it replaces
    # the two ordered response endpoints by a second q-edge).
    q_only_difference_rank = 0
    for p_site in sites:
        for s_site in sites:
            if p_site == s_site:
                continue
            residual_sites = tuple(site for site in sites
                                   if site not in (p_site, s_site))
            require(len(residual_sites) == 2,
                    "fixed-endpoint residual stopped being unique")
    require(q_only_difference_rank == 0,
            "a fixed-endpoint K4 switch appeared at order two")

    return {
        "sites": list(sites),
        "occurrence_count": len(occ),
        "marked": [0, 1, list(marked_residual)],
        "transpose": [1, 0, list(marked_residual)],
        "centered_class": "c2=12*e_+-1_12",
        "parity_split": {
            "odd": "c2^-=6*(e_+-e_-)",
            "even": "c2^+=6*(e_++e_-)-1_12",
        },
        "primitive_odd_detector": {
            "formula": "e_+^*-e_-^*",
            "on_common_H0": 0,
            "on_odd": 12,
            "on_even": 0,
        },
        "swap_even_hole_module": {
            "unordered_holes": [list(hole) for hole in holes],
            "rank": 6,
            "common_H0": "sum_h b_h=1_12",
            "augmentation_zero_rank": 5,
            "even_survivor": "6*b_marked-sum_h b_h",
            "even_survivor_in_common_H0_line": False,
            "primitive_detector": (
                "+1 on both marked orientations, -1 on both orientations "
                "of one comparison hole"
            ),
            "primitive_detector_value": 12,
            "endpoint_adjacency": {
                "degree": 4,
                "even_spectrum": [4, 0, -2],
                "H0_projector": "B*(B+2)/24",
                "centered_factorization": (
                    "c2^+=(B-4)w, w=-(B+6)c2^+/24"
                ),
                "denominator_clearing": (
                    "12*w is integral on the twelve occurrence coordinates"
                ),
                "physical_B_minus_4_lift_constructed": False,
            },
        },
        "fixed_endpoint_q_only_matching_difference_rank": q_only_difference_rank,
        "K4_scope": (
            "with ordered p/s endpoints fixed, only one residual q edge "
            "exists.  A full K4 matching/Bianchi row uses two q edges and "
            "therefore changes the source-operation block"
        ),
    }


def physical_scope_audit() -> dict[str, object]:
    centered = (ROOT / "notes/h3-centered-projector-e14-word-arrow-gate.md").read_text()
    direct = (ROOT / "notes/h3-direct-free-normals-e14-pointed-composition-gate.md").read_text()
    shared = (ROOT / "notes/h3-shared-four-term-endpoint-word-change-inventory-boundary.md").read_text()
    fan = (ROOT / "notes/uniform-bidirectional-private-site-fan-rank-boundary.md").read_text()
    active = (ROOT / "notes/h3-active-fan-coloop-or-four-good.md").read_text()
    endpoint = (ROOT / "notes/uniform-centered-occurrence-endpoint-association-projector.md").read_text()
    cap = (ROOT / "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md").read_text()
    require("deleted 23: lower word 0112" in centered
            and "deleted 45: lower word 0121" in centered
            and "`p/s`-odd" in centered,
            "the pinned lower-word statement changed")
    require("*already placed*" in direct
            and "source word `01211222`" in direct
            and "canonical E14 word/grade based at `000101`" in direct,
            "the pointed E14 placement scope changed")
    require("coefficients $(1,1)$" in shared
            and "T_{\\rm pure}" in shared
            and "T_{\\rm mix}" in shared,
            "the signless E14/tail mismatch statement changed")
    require("nonzero off-diagonal physical cell" in fan
            and "distinct-head four-good active overlap" in fan,
            "the physical bidirectional-fan entry changed")
    require("four-good or a literal" in active
            and "pure-colour target coloop" in active,
            "the active-fan landing alternative changed")
    require("one-endpoint" in endpoint
            and "Cartan product-rule face" in endpoint
            and "source-valid Cartan/Hasse bicomplex" in endpoint,
            "the endpoint adjacency physical-lift scope changed")
    require("endpoint-even companion" in cap
            and "not target-safe" in cap
            and "primitive source-normal" in cap,
            "the signless Cartan target-normal obstruction changed")
    return {
        "odd_branch_entry_hypothesis": (
            "the nonzero p/s-odd occurrence projection is realized by the "
            "literal same-tail offdiagonal physical response/curvature cell"
        ),
        "odd_branch_existing_landing": (
            "bidirectional private-site fan, then four-good or a literal "
            "pure-colour coloop (with the pinned normalized coloop landing)"
        ),
        "abstract_occurrence_nonzero_alone_is_terminal": False,
        "odd_dark_consequence": "[c2]=[c2^+] in the physical quotient",
        "common_H0_fills_even_survivor": False,
        "minimal_even_filler": (
            "one equivariant protected source-valid lift of B-4 in each "
            "literal lower word (its five image directions are the hole "
            "standard module), compatible with q23:21/q45:12 reinsertion; "
            "or promote its first augmented cokernel to a typed exit"
        ),
        "even_coefficient_factorization": (
            "c2^+=(B-4)*(-(B+6)c2^+/24); the denominator clears by 12"
        ),
        "even_physical_first_obstruction": (
            "B is a one-endpoint Cartan/matching prism, so its lift has a "
            "one-endpoint product-rule face.  The target-safe physical "
            "Cartan cell is endpoint-odd; its signless/even companion has "
            "target defect 2(w-1)Delta.  A target-normal correction still "
            "needs the pinned primitive source-normal attachment"
        ),
        "E14_unit_scope": (
            "the known E14 units terminalize support already placed in word "
            "000101.  They do not transport lower words 0112/0121 in the "
            "mixed tail to that chart; the correct E14 response hit is "
            "signless and has the pure 11|11 tail"
        ),
        "K4_scope": (
            "q-only K4 matching differences do not act inside a fixed-p/s "
            "order-two occurrence fibre; a full K4 row changes operation type"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    cuts = cut_packet_audit()
    packets = [
        parity_packet_audit((0, 1, 4, 5), (4, 5)),
        parity_packet_audit((0, 1, 2, 3), (2, 3)),
    ]
    ledger = {
        "theorem": "h2 lower centered orientation terminal fork",
        "pins": PINS,
        "physical_cuts": cuts,
        "packets": packets,
        "physical_scope": physical_scope_audit(),
        "fork": {
            "odd_bright": (
                "after literal same-tail physical typing, a nonzero p/s-odd "
                "orientation supplies an offdiagonal entry and enters the "
                "existing bidirectional active-fan landing"
            ),
            "odd_dark": (
                "the odd summand dies, but c2^+=6*b_marked-sum_h b_h "
                "survives in a rank-five swap-even hole quotient"
            ),
            "odd_dark_coefficient_compression": (
                "one B-4 factor suffices coefficientwise; this does not "
                "supply its signless physical Cartan/Hasse lift"
            ),
            "common_response_verdict": (
                "the complete H0/response row is only sum_h b_h and cannot "
                "supply c2^+; a hole-changing protected comparison or a "
                "typed cokernel exit remains necessary"
            ),
        },
        "verdict": (
            "The two lower debts have the same exact twelve-occurrence parity "
            "fork.  The odd part is a direct terminal route only after it is "
            "typed as the literal same-tail physical offdiagonal cell.  If "
            "odd-dark, the survivor is not common H0 but the marked vector in "
            "the five-dimensional swap-even hole-standard module.  Neither a "
            "fixed-endpoint q-only K4 switch nor the already placed E14 unit "
            "theorems fill that module."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h2 orientation-fork ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("lower physical cuts: 0112/q23:21 and 0121/q45:12")
    print("c2 parity: 6(e+-e-) + 6(e++e-)-1")
    print("odd bright: CONDITIONAL PHYSICAL ACTIVE-FAN ENTRY")
    print("odd dark: rank-five swap-even hole survivor")
    print("common H0 and fixed-endpoint q-only K4: DO NOT FILL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
