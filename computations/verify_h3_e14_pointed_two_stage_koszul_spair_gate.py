#!/usr/bin/env python3
"""Audit the first proper face of a pointed two-stage E14 comparison.

The raw assignment ``H0-u -> 1-v04`` cannot be both pointed and have a
nonzero private return.  Keep the degree-zero map pointed and try instead to
send the central product to the E14 return by a higher homotopy.

On the only silent localization branch v04=0, the complete mixed unary row
has the exact form

    v24*U_000101 = -g + sum_(j=1)^12 T_j.

Thus a source-valid cell with principal face ``g`` necessarily carries the
twelve nonprivate proper tails.  The 13 face blocks comprise 14 literal
monomials because the unspecialized private face is
``R=g-v04*g``.  The complete first-hit reduction of the twelve-tail packet
returns precisely ``R`` and has a primitive cokernel dual, so the current
inventory does not close the two-stage totalization.

There is a tempting centered occurrence compression
``c_g+1_90=90g``.  With the target row retained it is instead
``c_g+B=90g-u``.  Even granting the centered cell the primitive cap face
``(-Q,-ores)``, normalization of the principal occurrence divides every
augmented face by 90.  The old cap cycle ``T+rho`` cancels the resulting
target/residue discrepancy in the reduced cap quotient.  However that cap
cycle is not source-labelled in the pure target/E14 word of ``g``; the
committed centered occurrence class is in a third, mixed response word.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py":
        "5eef4dff45be6e8993808ef5bcb533d62143dd4bc833a16e2015b48e7bc408d8",
    "notes/h3-e14-keq-private-placement-pointedness-gate.md":
        "59111d6a2dda8a16785cab6c6d129c806ea7e01a2a6d54e092c8841f6521c6c0",
    "computations/verify_h3_e14_augp2_post_residue_master_local_reduction.py":
        "5924fbd6559514c1b9a46b5df658c0cc98dfe4dc33de1d5c78d940974012eccb",
    "notes/h3-e14-augp2-post-residue-master-local-reduction.md":
        "22d3e112f34f5c325ea7bc297609f20c392e92b8d07756c464adbd37ab2a051f",
    "computations/verify_h3_e14_private_return_localization_unit_fork.py":
        "8ed9667a4ac5e2fb362e67c1a2f37e90a32a389e46c4e694361a43ad1d370f86",
    "notes/h3-e14-private-return-localization-unit-fork.md":
        "fc3a0994626ef5308d73ffdbef9d846929295a4e83f5acc93e80f4927493f31c",
    "computations/verify_h3_e14_keq_private_factor_localization_provenance_gate.py":
        "b3b3114ba14d4e3d9c5e02390881c54c6b04f6a16f343c588344807289db0d24",
    "notes/h3-e14-keq-private-factor-localization-provenance-gate.md":
        "a2c0a1adf58bdf80c96e85cb61c894c0fa172b8c4f8668b4c66ce08dbe47a7d2",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py":
        "85be051fa9f27fb909c2a9844084f2c6ccb1feb243d3d6fae1e69cca945e39d3",
    "notes/h3-p2-mate-slack-centered-occurrence-reduction.md":
        "d9a6b2fd0648870acfb2a6cbec8ab4ec4e32a6b617e1c7079cf57f073504914b",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_reynolds_attach_coupled_obstruction.py":
        "c37ae0188febbde82196a297307b55d03833a2adee87a0e9f12733eef006110b",
    "notes/h3-reynolds-attach-coupled-obstruction.md":
        "d22645280f293482e6ad11074fee4b95044dc1e2714df8e4e370e4845982b39e",
}
EXPECTED_LEDGER_SHA256 = "bdaab7de4af63d8d043f19fcfd0e81234f0ceec1f7e671cd13ca987dd4d8455e"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    width = len(columns[0])
    require(all(len(column) == width for column in columns), "rank width")
    matrix = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, width)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[answer], matrix[pivot] = matrix[pivot], matrix[answer]
        value = matrix[answer][column]
        matrix[answer] = [entry / value for entry in matrix[answer]]
        for row in range(width):
            if row == answer or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def centered_occurrence_compression() -> dict[str, object]:
    n = 90
    zero = (Q(0),) * n
    ones = (Q(1),) * n
    e_g = (Q(1),) + (Q(0),) * (n - 1)
    c_g = add(scale(n, e_g), scale(-1, ones))
    require(add(c_g, ones) == scale(n, e_g)
            and sum(c_g, Q(0)) == 0,
            "c_g+1_90=90g changed")

    # Retain (occurrence coefficients, pure target, Q_cap, ores_cap).  The
    # complete physical pure-target response row is 1_90-u.  The following
    # grants the strongest optimistic possibility: a source-valid c_g cell
    # also carries the primitive cap face (-Q,-ores).  Then
    #
    #   c_g + (1_90-u) = (90g, -u, -Q, -ores).
    #
    # To obtain principal coefficient one we must divide by 90, so all three
    # augmented coefficients become -1/90.  K_Eq can cancel Q, but the target
    # and ores coefficients are still short by -89/90.  Thus the target
    # constant is cap-shaped only integrally; it is not the normalized z_cap
    # required by the E14 cell.
    centered_with_cap = c_g + (Q(0), Q(-1), Q(-1))
    complete_target_row = ones + (Q(-1), Q(0), Q(0))
    integral_compressed = add(centered_with_cap, complete_target_row)
    require(integral_compressed
                == scale(n, e_g) + (Q(-1), Q(-1), Q(-1)),
            "the integral augmented centered compression changed")
    normalized = scale(Q(1, n), integral_compressed)
    keq_q_correction = zero + (Q(0), Q(1, n), Q(0))
    after_keq = add(normalized, keq_q_correction)
    desired = e_g + (Q(-1), Q(0), Q(-1))
    residual = add(desired, scale(Q(-1), after_keq))
    require(after_keq == e_g + (Q(-1, n), Q(0), Q(-1, n))
            and residual
                == zero + (Q(-89, 90), Q(0), Q(-89, 90)),
            "the factor-90 target/cap residual changed")
    target_dual = zero + (Q(1), Q(0), Q(0))
    q_dual = zero + (Q(0), Q(1), Q(0))
    ores_dual = zero + (Q(0), Q(0), Q(1))
    require(dot(target_dual, residual) == Q(-89, 90)
            and dot(q_dual, residual) == 0
            and dot(ores_dual, residual) == Q(-89, 90)
            and rank((target_dual, q_dual, ores_dual)) == 3,
            "the normalized augmentation residual stopped separating")

    # In the reduced old cap complex at Y=1, coordinates are
    # (Yw,target,Q,ores).  T+rho is boundary-zero and has exactly the equal
    # target/residue direction.  Hence the factor-90 residual is not a new
    # coarse cokernel class.  With the present sign convention
    # desired-after_keq=(-89/90)(T+rho).
    reynolds = load(
        "computations/verify_h3_reynolds_attach_coupled_obstruction.py",
        "two_stage_reynolds",
    )
    old_cap = reynolds.derived_cap_and_attach_audit()
    require(old_cap["derived_differential"]
                == {"T": "-Y*w", "rho": "w"}
            and old_cap["derived_target"] == {"T": "1", "rho": "0"}
            and old_cap["derived_ordinary_residue"]
                == {"T": "0", "rho": "1"},
            ("the old cap signatures changed", old_cap))
    cap_T = (Q(-1), Q(1), Q(0), Q(0))
    cap_rho = (Q(1), Q(0), Q(0), Q(1))
    cap_cycle = add(cap_T, cap_rho)
    typed_residual = (Q(0), Q(-89, 90), Q(0), Q(-89, 90))
    cap_repair = scale(Q(-89, 90), cap_cycle)
    require(cap_cycle == (Q(0), Q(1), Q(0), Q(1))
            and cap_repair == typed_residual,
            "the formal T+rho normalization repair changed")

    cap = load(
        "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py",
        "two_stage_cap",
    )
    cap_ledger, cap_digest = cap.audit()
    require(cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "the centered primitive-cap ledger changed")
    cap_signature = cap_ledger["physical_cap_quotient"]
    require(cap_signature["row_order"].index("target") == 5
            and cap_signature["row_order"].index("ores") == 6
            and cap_signature["required_augmented_signature"][5] == 0
            and cap_signature["required_augmented_signature"][6] == -1,
            ("z_cap target/ores signature changed", cap_signature))

    mate = load(
        "computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py",
        "two_stage_mate",
    )
    mate_ledger, mate_digest = mate.audit()
    require(mate_digest == mate.EXPECTED_LEDGER_SHA256,
            "the centered mate ledger changed")
    literal = mate_ledger["literal_mate_class"]
    extension = mate_ledger["source_cell_and_terminal"]
    require(literal["response_head_word"] == "11:110000"
            and extension["smallest_source_extension"].startswith(
                "one same-grade centered occurrence cell")
            and not extension["raw_projector_source_valid"],
            ("the actual c_f source scope changed", mate_ledger))

    return {
        "coefficient_identity": "c_g+1_90=90g",
        "optimistic_integral_augmented_identity": (
            "c_g(with -Q,-ores)+(1_90-u)=90g-u-Q-ores"
        ),
        "normalized_after_KEq": [1, "-1/90", 0, "-1/90"],
        "desired_normalized_signature": [1, -1, 0, -1],
        "residual_target_Q_ores": ["-89/90", 0, "-89/90"],
        "normalization_index": 90,
        "z_cap_signature_target_ores": [0, -1],
        "old_cap_cycle_T_plus_rho": [0, 1, 0, 1],
        "old_cap_cycle_row_order": ["Yw", "target", "Q", "ores"],
        "coarse_cap_coefficient_for_desired_minus_current": "-89/90",
        "coarse_normalization_residual_in_old_cap_span": True,
        "target_constant_is_exactly_normalized_z_cap_without_cap_cycle": False,
        "cap_shape_can_be_granted_before_normalization": True,
        "actual_centered_block": "mixed response head/word 11:110000",
        "needed_centered_block": (
            "pure target G11[111111] at the marked occurrence g, followed "
            "by the E14 word-000101 unary comparison"
        ),
        "word_transport_constructed": False,
        "old_cap_cycle_same_word_fine_repeated_grade": False,
        "old_cap_cycle_full_anchor_q_terminal_silence_certified": False,
        "first_typing_obstruction": (
            "T+rho is only available in the selected old cap block; the "
            "committed primitive cap is word 01211222/repeated P3+K2, while "
            "g is tagged in pure target G11[111111] and its E14 unary "
            "comparison is word 000101"
        ),
        "physical_conclusion": (
            "the factor-90 mismatch is repairable in the reduced cap "
            "quotient by T+rho, but no committed source-labelled transport "
            "places that cycle in the pure-target/E14 grade; the existing "
            "mixed-word c_f cannot supply the transport"
        ),
    }


def literal_unary_spair_packet() -> dict[str, object]:
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "two_stage_first",
    )
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "the unary S-pair first-reduction ledger changed")
    rewrite = first.load(first.REWRITE_PATH, "two_stage_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "two_stage_top")
    two = top.load(top.TWO_CELL_PATH, "two_stage_two")
    e14 = two.load(two.E14_PATH, "two_stage_e14")
    b4 = e14.load(e14.B4_PATH, "two_stage_b4")
    _candidates, _names, _responses, unary = two.universal(e14, b4, 1, 1)

    word = (0, 0, 0, 1, 0, 1)
    pivot = ("u35_11",)
    multiplier = ("v2411",)
    factor, remainder = first.factor_unary(unary[word], pivot)
    require(factor == {(): Q(-1), ("v0400",): Q(1)}
            and len(remainder) == 12,
            ("the canonical U=pA+B split changed", factor, remainder))

    private_terms = {
        tuple(sorted(pivot + multiplier)): Q(-1),
        tuple(sorted(pivot + ("v0400",) + multiplier)): Q(1),
    }
    tail_terms = {
        tuple(sorted(monomial + multiplier)): coefficient
        for monomial, coefficient in remainder.items()
    }
    multiplied_complete_row = {
        tuple(sorted(monomial + multiplier)): coefficient
        for monomial, coefficient in unary[word].items()
    }
    require(set(private_terms).isdisjoint(tail_terms)
            and private_terms | tail_terms == multiplied_complete_row
            and len(multiplied_complete_row) == 14,
            "the complete unary-times-q packet changed")
    degree_profile = Counter(map(len, tail_terms))
    require(degree_profile == Counter({3: 10, 4: 2}),
            ("the 12-tail degree profile changed", degree_profile))

    canonical = first_ledger["canonical_first_reduction"]
    require(canonical["B_tail_count"] == 12
            and canonical["target_augmented_first_hit_column_count"] == 269
            and canonical["target_augmented_first_hit_rank_Q"] == 269
            and canonical["rational_dual_support"] == 22
            and canonical["rational_dual_pairing"] == "-1"
            and canonical["primitive_integral_dual_pairing"] == "-30",
            ("the first-hit module changed", canonical))
    reduced = canonical["reduced_target"]
    require(reduced == [
        [["p1_0_1", "s1_1_1"],
         ["u35_11", "v0400", "v2411"], "-1"],
        [["p1_0_1", "s1_1_1"], ["u35_11", "v2411"], "1"],
    ], ("the first-hit remainder stopped being R", reduced))

    return {
        "complete_row": "v24_11*U[000101]=-R_E14+T_12",
        "R_E14": "g-v04_00*g",
        "silent_branch_v04_zero": "v24_11*U[000101]=-g+T_12",
        "nonprivate_proper_tail_count": len(tail_terms),
        "proper_tail_degree_profile": {
            str(degree): count for degree, count in sorted(degree_profile.items())
        },
        "face_block_count": 1 + len(tail_terms),
        "literal_monomial_count": len(multiplied_complete_row),
        "face_count_explanation": (
            "one factorized private face R plus twelve nonprivate tails; "
            "R itself has two literal monomials before v04=0"
        ),
        "first_hit_module": {
            "columns": canonical["target_augmented_first_hit_column_count"],
            "rank_Q": canonical["target_augmented_first_hit_rank_Q"],
            "reduction_of_T12": "R_E14",
            "rational_dual_support": canonical["rational_dual_support"],
            "rational_dual_pairing": canonical["rational_dual_pairing"],
            "primitive_integral_pairing":
                canonical["primitive_integral_dual_pairing"],
        },
        "physical_first_proper_face": (
            "the full T_12 packet in the complete word/fine grade, not only "
            "its reduced-Eq or target-normal projection"
        ),
    }


def pointed_two_stage_gate(packet: dict[str, object]) -> dict[str, object]:
    pointed = load(
        "computations/verify_h3_e14_keq_private_placement_pointedness_gate.py",
        "two_stage_pointed",
    )
    pointed_ledger, pointed_digest = pointed.audit()
    require(pointed_digest == pointed.EXPECTED_LEDGER_SHA256,
            "the private-placement pointedness ledger changed")
    require(pointed_ledger["shortest_positive_target"].startswith(
                "one augmented P2 totalization with two distinct")
            and "P_f=[d(u_f-u)]" in pointed_ledger["verdict"],
            ("the pointed higher-cell target changed", pointed_ledger))

    localization = load(
        "computations/verify_h3_e14_private_return_localization_unit_fork.py",
        "two_stage_localization",
    )
    localization_ledger, localization_digest = localization.audit()
    require(localization_digest == localization.EXPECTED_LEDGER_SHA256,
            "the private-return localization fork changed")
    silent = localization_ledger["fork"]["D_1_minus_v04_and_V_v04"]
    require(silent.startswith("v04=0 and R_E14=g"),
            ("the silent primitive branch changed", silent))

    provenance = load(
        "computations/verify_h3_e14_keq_private_factor_localization_provenance_gate.py",
        "two_stage_provenance",
    )
    provenance_ledger, provenance_digest = provenance.audit()
    require(provenance_digest == provenance.EXPECTED_LEDGER_SHA256,
            "the private-factor provenance gate changed")
    require(not provenance_ledger["source_row_vs_selected_coefficient"]
                ["coefficient_extraction_is_algebra_map"],
            ("coefficient extraction became a source map", provenance_ledger))

    # Abstract Koszul product rule: d(P_f e_Eq)=F e_Eq-P_f d(e_Eq).
    # A pointed degree-zero map kills F only in the source ideal; the P_f
    # face remains separate.  On the physical E14 side, mapping the principal
    # product to R invokes the complete unary relation, whose aggregate row is
    # (-R,+T12).  Deleting T12 is not a chain boundary.
    koszul_product = (Q(1), Q(-1))
    unary_total = (Q(-1), Q(1))
    private_only = (Q(-1), Q(0))
    require(sum(koszul_product, Q(0)) == 0
            and sum(unary_total, Q(0)) == 0
            and sum(private_only, Q(0)) == -1,
            "the two-stage boundary augmentation changed")
    proper_tail_dual = (Q(0), Q(1))
    require(dot(proper_tail_dual, unary_total) == 1
            and dot(proper_tail_dual, private_only) == 0,
            "the proper-tail deletion guard changed")

    return {
        "degree_zero": (
            "keep the comparison pointed; do not set H0-u equal to 1-v04"
        ),
        "pointed_degree_one_face": "P_f with dP_f=u_f-u",
        "abstract_Koszul_product_boundary": (
            "d(P_f*e_Eq)=(u_f-u)e_Eq-P_f*d(e_Eq)"
        ),
        "higher_E14_principal_face": "(H0-u)e_Eq maps to R_E14",
        "literal_physical_chain_condition": packet["complete_row"],
        "first_forced_proper_face": "T_12 (twelve nonprivate unary tails)",
        "projected_Eq_shadow_is_complete_face": False,
        "current_inventory_closes_T12": False,
        "reason": (
            "the complete 269-column first-hit image reduces T_12 back to "
            "R_E14 and has a primitive nonzero dual"
        ),
        "smallest_new_cell": (
            "one source-labelled endpoint-word-change mapping-cone/Tate cell "
            "whose 13 face blocks are R_E14 and the twelve T_j, together "
            "with a next companion homotopy killing the T_12 first-hit class"
        ),
        "P_f_is_same_homogeneous_cell": False,
        "P_f_can_be_separate_face_of_same_totalization": True,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    packet = literal_unary_spair_packet()
    ledger = {
        "theorem": "pointed two-stage E14 Koszul/S-pair gate",
        "pins": PINS,
        "centered_occurrence_compression": centered_occurrence_compression(),
        "literal_unary_spair_packet": packet,
        "pointed_two_stage_totalization": pointed_two_stage_gate(packet),
        "verdict": (
            "A pointed degree-zero comparison can only carry the nonzero E14 "
            "return as a higher face.  The exact coefficient compression "
            "c_g+1_90=90g does not yet construct it physically.  The old "
            "cap cycle T+rho repairs its factor-90 target/ores discrepancy "
            "in the reduced quotient, but no committed map puts that cycle "
            "in g's pure-target word/fine/repeated grade or certifies its "
            "anchor/q/terminal silence; the known c_f lives in a different "
            "word block.  The first literal d^2/"
            "chain-map face of the higher E14 cell is the complete twelve-"
            "tail unary-times-q packet (thirteen face blocks with R), not "
            "only the reduced-Eq shadow.  Its current complete first-hit "
            "reduction returns R and is dual-detected, so one further "
            "endpoint-word-change companion homotopy is genuinely missing."
        ),
        "scope": (
            "canonical h=3 chart-(1,1), silent v04=0 E14 branch.  This gives "
            "the exact smallest proper-face interface and a no-go for the "
            "current two-stage inventory; it does not exclude a new full "
            "mapping-cone/Tate attachment or prove its terminal alternative"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("centered compression: c_g+1_90=90g (COEFFICIENT ONLY)")
    print("factor-90 residual: killed coarsely by T+rho; typed lift MISSING")
    print("pointed higher E14 cell first proper face: FULL T_12")
    print("13 face blocks / 14 literal monomials before v04=0")
    print("current first-hit reduction: T_12 -> R_E14, NOT ZERO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
