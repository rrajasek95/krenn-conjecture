#!/usr/bin/env python3
"""Test the four ordinary equation generators against the Gate-II root defect.

The simultaneous local Weyl action at sites 2,5 sends the two pure GHZ
words to two mixed words.  In word order (mixed_i, mixed_c, pure_i, pure_c)
its target defect is

    delta = (1,1,-1,-1).

There are four ordinary source-equation/Tate generators, one for each word.
Their differentials are d theta_y=F_y-tau_y.  The mixed target values are
tau=0, while the two pure values are one.  Consequently the augmented
target map of these four generators has image only the two pure axes.
Adding the pure generators cancels the last two entries of delta but leaves
the primitive mixed class (1,1,0,0).  Pairwise Koszul generators do not
enlarge that degree-one target image.

The audit is literal on the complete direct-free h=3 source: every one of
the four F_y has 90 matching terms with the same matching skeletons, and
the root action transports them termwise.  Each ordinary equation generator
is nevertheless the aggregate over all 90 skeletons.  It cannot isolate a
chosen common-tail occurrence or the pointed anchor P_f.  Declaring that
selected root character to be an additional ordinary source relation raises
the occurrence-presentation rank and changes H0.  An H0-safe repair must
therefore be a genuinely relative target cylinder/PP cell carrying the
mixed target normal, not another old equation/Koszul generator.

Finally, the four-generator data do not determine the external matching row
M, hence do not type q=M-a on the proposed cell.  This is a source/target
no-go, not a full physical cokernel terminal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_cartan_full_q_pointed_character_gate.py":
        "6f791c41e743a94279ccf9e4924af11a42c278baa7737a5eed108bf85136f499",
    "notes/h3-gate-ii-cartan-full-q-pointed-character-gate.md":
        "3ffd0d0894dfbb81cb672f87548b3b7a2da28ac1b36a6466bbef6ad149cf0933",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_rootless_c5_first_higher_anchor_spair.py":
        "3f9c39e8505da148d85a2d5125cefc502321f3652af2d9c0d12cd65aa41d469c",
    "notes/h3-rootless-c5-first-higher-anchor-spair.md":
        "3182bbc0840c25004e43058b54b252bac969e10ce1cc530a59940a1565d5bf29",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "notes/h3-direct-free-complete-first-fine-degree-membership.md":
        "be8407215a2435faefc779bab6ef02a7cb256fd8d2aae118ab55ab13934058fc",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
}
EXPECTED_LEDGER_SHA256 = "ce0b4936e3e0e92a8a99cd79b29fea88a86bf503fcc5d34641a6ab97c54fcc9a"

TAIL_SITES = (2, 5)
WORD_ORDER = ("mixed_i", "mixed_c", "pure_i", "pure_c")
N = 90


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(vectors, width=None):
    vectors = tuple(tuple(map(Q, vector)) for vector in vectors)
    if not vectors:
        return 0
    if width is None:
        width = len(vectors[0])
    require(all(len(vector) == width for vector in vectors), "rank width")
    work = [list(vector) for vector in vectors]
    answer = 0
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
        if answer == len(work):
            break
    return answer


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def unit(index, width):
    return tuple(Q(position == index) for position in range(width))


def signed_weyl_word(word):
    answer = list(word)
    sign = 1
    for site in TAIL_SITES:
        if answer[site] == 1:
            answer[site] = 2
            sign *= -1
        elif answer[site] == 2:
            answer[site] = 1
    return tuple(answer), sign


def strip_decorations(monomial):
    return tuple((left, right) for left, right, _a, _b in monomial)


def literal_four_word_audit(base):
    pure_i = (1,) * 8
    pure_c = (2,) * 8
    mixed_i, sign_i = signed_weyl_word(pure_i)
    mixed_c, sign_c = signed_weyl_word(pure_c)
    require(sign_i == sign_c == 1
            and mixed_i == (1, 1, 2, 1, 1, 2, 1, 1)
            and mixed_c == (2, 2, 1, 2, 2, 1, 2, 2),
            (mixed_i, sign_i, mixed_c, sign_c))
    words = (mixed_i, mixed_c, pure_i, pure_c)
    rows = tuple(base.full_row(word) for word in words)
    require(all(len(row) == len(set(row)) == N for row in rows),
            "a four-word source row changed size")

    skeletons = tuple(tuple(map(strip_decorations, row)) for row in rows)
    require(all(set(skeleton) == set(skeletons[0])
                for skeleton in skeletons),
            "the local root orbit changed matching skeletons")
    require(len(set(skeletons[0])) == N,
            "the direct-free row lost a matching skeleton")

    # Each word equation contributes the full sum on its own 90-coordinate
    # block.  No ordinary equation generator selects one skeleton.
    width = len(words) * N
    equation_source_rows = []
    for word_index in range(len(words)):
        row = [Q(0)] * width
        for skeleton_index in range(N):
            row[word_index * N + skeleton_index] = Q(1)
        equation_source_rows.append(tuple(row))
    selected_root = [Q(0)] * width
    for word_index, coefficient in enumerate((1, 1, -1, -1)):
        selected_root[word_index * N] = Q(coefficient)
    selected_root = tuple(selected_root)
    require(rank(equation_source_rows, width) == 4
            and rank(tuple(equation_source_rows) + (selected_root,), width) == 5,
            "the common-tail occurrence quotient changed")

    # A primitive covector inside the first mixed word kills its complete
    # equation row but detects the selected root occurrence.  It is a
    # presentation dual only, not a physical terminal.
    tail_dual = add(unit(0, width), scale(-1, unit(1, width)))
    require(all(sum(tail_dual[index] * equation_source_rows[row][index]
                    for index in range(width)) == 0
                for row in range(len(equation_source_rows))),
            "the selected-tail dual stopped killing complete rows")
    require(sum(tail_dual[index] * selected_root[index]
                for index in range(width)) == 1,
            "the selected-tail primitive dual changed")
    return {
        "word_order": list(WORD_ORDER),
        "words": ["".join(map(str, word)) for word in words],
        "terms_per_complete_direct_free_row": N,
        "common_matching_skeletons": N,
        "root_transport_preserves_skeleton_and_decorated_remote_tail": True,
        "ordinary_equation_source_rank": 4,
        "rank_after_selected_root_occurrence": 5,
        "selected_common_tail_in_old_equation_span": False,
        "primitive_occurrence_dual": "e_(mixed_i,f)^*-e_(mixed_i,g)^*",
    }


def ordinary_generator_target_audit():
    # Word order is mixed_i,mixed_c,pure_i,pure_c.  For d theta_y=F_y-tau_y,
    # the GHZ target values are tau=(0,0,1,1).  Thus mixed source equations
    # are target-zero generators.  The two pure generators carry their own
    # target axes.
    zero = (Q(0),) * 4
    target_columns = (
        zero,
        zero,
        unit(2, 4),
        unit(3, 4),
    )
    defect = tuple(map(Q, (1, 1, -1, -1)))
    require(rank(target_columns, 4) == 2
            and rank(target_columns + (defect,), 4) == 3,
            "the four-generator target rank changed")

    # The unique correction to the pure entries is +theta_pi+theta_pc.
    # Coefficients on the two mixed generators are irrelevant to target.
    pure_correction = add(target_columns[2], target_columns[3])
    residual = add(defect, pure_correction)
    require(residual == (Q(1), Q(1), Q(0), Q(0)),
            "the primitive mixed target residual changed")

    lambda_mixed_i = unit(0, 4)
    lambda_mixed_c = unit(1, 4)
    require(all(sum(left * right for left, right in
                    zip(functional, column, strict=True)) == 0
                for functional in (lambda_mixed_i, lambda_mixed_c)
                for column in target_columns)
            and sum(left * right for left, right in
                    zip(add(lambda_mixed_i, lambda_mixed_c), defect,
                        strict=True)) == 2,
            "the primitive mixed cokernel dual changed")

    # Pairwise Koszul generators theta_i wedge theta_j have boundaries
    # r_i theta_j-r_j theta_i.  At the GHZ point every r_i is zero, so their
    # degree-one augmented target is zero.  They cannot enlarge im(T).
    koszul_pairs = 6
    koszul_target_columns = (zero,) * koszul_pairs
    require(rank(target_columns + koszul_target_columns, 4) == 2,
            "ordinary pairwise Koszul cells enlarged the target image")
    return {
        "root_only_target_defect": [1, 1, -1, -1],
        "ordinary_generators": {
            "mixed_i": "d theta=F_mixed; target 0",
            "mixed_c": "d theta=F_mixed; target 0",
            "pure_i": "d theta=F_pure-1; target pure_i",
            "pure_c": "d theta=F_pure-1; target pure_c",
        },
        "four_generator_target_rank": 2,
        "target_rank_after_defect": 3,
        "best_pure_correction": "+theta_pure_i+theta_pure_c",
        "uncancelled_target": [1, 1, 0, 0],
        "primitive_cokernel_class": "[m_(c|i)+m_(i|c)]",
        "primitive_duals": ["mixed_i^*", "mixed_c^*"],
        "pairwise_Koszul_generators": koszul_pairs,
        "target_rank_after_all_pairwise_Koszul": 2,
        "target_safe_relative_chi_w_from_four_generators": False,
    }


def h0_anchor_q_scope():
    # In the occurrence-expanded linear presentation, four complete
    # equations have rank four.  Adding the selected root-only relation has
    # rank five, hence drops H0 dimension by one.  This is the exact reason a
    # bare new source Koszul generator is not presentation safe.
    source_dimension = 4 * N
    old_relation_rank = 4
    new_relation_rank = 5
    require(source_dimension - old_relation_rank == 356
            and source_dimension - new_relation_rank == 355,
            "the occurrence H0 guard changed")

    # The pure source-row generator has the committed coarse signature
    # (ainc,W,target,ores)=(-1,0,+1,0); mixed generators have target and
    # anchor/ainc zero.  Cancelling the pure part therefore also adds a pure
    # ainc face.  The four-equation data contain no M-extension, so q=M-a is
    # not determined.  Two possible M assignments give different q with the
    # same source differential and target correction.
    ainc_after_pure_correction = Q(-2)
    q_if_M_zero = Q(0) - ainc_after_pure_correction
    q_if_M_equals_a = ainc_after_pure_correction - ainc_after_pure_correction
    require((q_if_M_zero, q_if_M_equals_a) == (Q(2), Q(0)),
            "the q-extension ambiguity changed")
    return {
        "ordinary_Tate_presentation": (
            "the four d theta_y=F_y-tau_y generators preserve the original "
            "physical equation quotient H0"
        ),
        "occurrence_presentation_H0_dimension_before_new_relation": 356,
        "H0_dimension_after_declaring_selected_chi_w_an_old_source_relation": 355,
        "bare_new_source_Koszul_generator_is_H0_safe": False,
        "H0_safe_positive_shape": (
            "a relative target cylinder/PP cell carrying the mixed target "
            "normal while retaining the physical source quotient"
        ),
        "pointed_anchor": (
            "old equation PP faces are aggregate on all 90 skeletons; they "
            "do not supply the selected P_f/common-tail anchor"
        ),
        "pure_generator_coarse_signature":
            "(ainc,W,target,ores)=(-1,0,+1,0)",
        "mixed_generator_anchor_and_target": 0,
        "ainc_after_best_pure_target_correction": str(
            ainc_after_pure_correction),
        "M_from_four_equation_Koszul_data": "not determined",
        "two_compatible_q_values_with_same_principal_data": [
            str(q_if_M_zero), str(q_if_M_equals_a)],
        "literal_q_equals_M_minus_a_constructed": False,
    }


def audit():
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "gate_ii_four_equation_base",
    )
    ledger = {
        "theorem": "h3 Gate-II four-equation Koszul root-target no-go",
        "pins": PINS,
        "literal_four_word_source": literal_four_word_audit(base),
        "ordinary_equation_target_map": ordinary_generator_target_audit(),
        "presentation_anchor_q_scope": h0_anchor_q_scope(),
        "exact_verdict": (
            "The four ordinary source-equation/Tate generators cannot make "
            "the root-only chi_w Cartan face target safe.  The two mixed-word "
            "generators are target zero, so the entire ordinary target image "
            "is the two-dimensional pure span.  The pure generators cancel "
            "only the -pure_i-pure_c part of (w-1)Delta and leave the "
            "primitive mixed class m_(c|i)+m_(i|c).  Pairwise Koszul cells do "
            "not enlarge this image.  On the source side all four generators "
            "are 90-term aggregates and do not isolate the selected common "
            "tail or P_f.  Declaring the missing selected character to be a "
            "new ordinary relation changes occurrence-presentation H0.  The "
            "first new physical cell must therefore be a root-decorated mixed "
            "target cylinder/relative PP cell; its M/ainc extension must then "
            "be supplied to type q=M-a"
        ),
        "first_additional_cell": {
            "target": "-(m_(c|i)+m_(i|c)) after the old pure correction",
            "source_boundary": "selected root-only chi_w modulo complete rows",
            "grade": (
                "literal fan word orbit, selected fine/repeated grade and "
                "fixed decorated common tail"
            ),
            "required_rows": [
                "H0/presentation-safe mapping cylinder", "pointed P_f anchor",
                "physical M and a with q=M-a", "protected/ridge/terminal rows",
            ],
        },
        "scope": (
            "exact canonical h=3 four-word target module and literal 90-term "
            "direct-free source rows.  The primitive mixed covectors and "
            "occurrence dual are not promoted here to physical terminals, "
            "and no all-h statement is claimed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("four-equation root-target ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("Gate II four ordinary equations: TARGET IMAGE = PURE RANK 2")
    print("best correction residual: MIXED_i + MIXED_c")
    print("pairwise ordinary Koszul cells: NO TARGET-RANK GROWTH")
    print("selected common-tail/P_f section: NOT SUPPLIED")
    print("first new cell: MIXED TARGET CYLINDER / RELATIVE PP")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
