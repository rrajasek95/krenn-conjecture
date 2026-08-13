#!/usr/bin/env python3
"""Audit the endpoint-role groupoid bar and compare the even C_plus family.

Retaining the two endpoint-role objects makes the tau bar honest:

    d b_i = (T,tau i) - (+,i).

Canonical transport of the T object back to + applies tau^{-1}, so the bar
boundary becomes zero.  Forgetting the object tag without transporting its
endpoint label instead gives e_{tau i}-e_i, but that fold is not a chain map
to the fixed physical complex unless the desired W column is already there.

At a pointed source its first obstruction is the scalar
f_tau(x)-f(x).  The complete response target is endpoint-even and reads zero
on the odd difference, so it cannot absorb this scalar.  Even if the scalar
vanishes, adjoining the odd boundary changes H_0 and is not a resolution of
the original fixed-label source.  One new odd occurrence-graph coordinate
is the minimal rank-preserving pointed extension.

The order-two even B-4 family and the inactive C_plus family share the same
signless-Cartan target-defect architecture, but they are not presently the
same literal source family.  Their words, involutions, module ranks, and
defined augmented signatures differ; identifying them requires exactly the
missing word/fine/Rees/Eq/residue comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "computations/verify_h3_order2_promoted_occurrence_orientation_gate.py":
        "c0a34736979eb8a5d059dce30224b3d22f3930e9afaf07916dbbf51b3539c15d",
    "notes/h3-order2-promoted-occurrence-orientation-gate.md":
        "5a4f015c519421d4df2cff2c267f4cee00b6f8e35435ad97323f453831305edb",
    "computations/verify_h2_lower_centered_orientation_terminal_fork.py":
        "6758c86ec151834d121e5b41b1dae677592cc4224c3aaad95d6f8321b826d3b2",
    "notes/h2-lower-centered-orientation-terminal-fork.md":
        "daa6d20d510be6472d9b1946a4854d6fd3322b61288f3fb77a8103b8a8b7d051",
    "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py":
        "b30000bfe8383e1f254fb8fee4724cbd99d8f70a5e8447cffb1c9086a179aec0",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py":
        "9679c047e440f48899f1385682bcf64b725e049da01a42b8134b40c3fda73177",
    "notes/h3-signless-cartan-adjacent-power-shared-cell-gate.md":
        "6f1b0e239ecc13e3577ed7f0cee051ab0e092ebfed5eb25240476ec613a271a1",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
    "computations/verify_h3_trace_cartan_lower_rees_typing_gate.py":
        "0190a8fa16dddf9cecf2de676d4f3ff87d184f031e523d87e1f80937ff55be94",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
}
EXPECTED_LEDGER_SHA256 = (
    "8ecf499ff8f9be532a7bbd8b72970bd04899c64efe46be581c6603a98058651c"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot load", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(columns: list[tuple[Q, ...]] | tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def unit(index: int, width: int):
    return tuple(Q(position == index) for position in range(width))


def add(left, right, scale=Q(1)):
    return tuple(Q(a) + Q(scale) * Q(b) for a, b in
                 zip(left, right, strict=True))


def occurrence_packet():
    occurrence = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "endpoint_role_bar_occurrences",
    )
    values = occurrence.occurrences(tuple(range(4)))
    lookup = {item: index for index, item in enumerate(values)}
    tau = tuple(lookup[(item[1], item[0], item[2])] for item in values)
    require(len(values) == 12
            and all(tau[tau[index]] == index and tau[index] != index
                    for index in range(len(values))),
            "the order-two endpoint-role involution changed")
    return values, tau


def two_object_bar_audit() -> dict[str, object]:
    values, tau = occurrence_packet()
    size = len(values)

    # C0=V_+ direct-sum V_T.  The T endpoint of b_i is labelled tau(i).
    bars = []
    for index in range(size):
        column = [Q(0)] * (2 * size)
        column[index] = -1
        column[size + tau[index]] = 1
        bars.append(tuple(column))
    require(rank(bars) == size,
            "the two-object groupoid bar stopped identifying its objects")

    # Canonical descent transports the T-labelled endpoint back by tau^-1.
    # It is a quasi-isomorphism from H0 of the two-object totalization to V,
    # and every bar boundary maps to zero.
    canonical_images = []
    raw_images = []
    for column in bars:
        canonical = [Q(0)] * size
        raw = [Q(0)] * size
        for index in range(size):
            canonical[index] += column[index]
            raw[index] += column[index]
            canonical[tau[index]] += column[size + index]
            raw[index] += column[size + index]
        canonical_images.append(tuple(canonical))
        raw_images.append(tuple(raw))
    require(all(not any(image) for image in canonical_images),
            "canonical groupoid transport acquired an odd boundary")
    expected_raw = tuple(add(unit(tau[index], size), unit(index, size), -1)
                         for index in range(size))
    require(tuple(raw_images) == expected_raw and rank(raw_images) == 6,
            "the nontransported fold stopped producing endpoint differences")

    # The groupoid totalization has H0 dimension 24-12=12, as it should for
    # one retained object.  Adjoining one raw odd boundary directly to V
    # instead lowers H0 from 12 to 11: it changes the source rather than
    # resolving it.
    require(2 * size - rank(bars) == size,
            "the two-object groupoid H0 dimension changed")
    selected_odd = raw_images[0]
    require(size - rank([selected_odd]) == size - 1,
            "the raw selected bar stopped changing fixed-object H0")

    return {
        "objects": ["fixed endpoint labels +", "transposed labels T"],
        "C0_dimension": 2 * size,
        "bar_generators": len(bars),
        "bar_rank": rank(bars),
        "groupoid_H0_dimension": 2 * size - rank(bars),
        "bar_boundary": "d b_i=(T,tau i)-(+,i)",
        "canonical_transport_fold": "(T,tau i) maps to (+,i)",
        "canonical_fold_boundary_rank": rank(canonical_images),
        "raw_label_forgetting_fold": "(T,tau i) maps to (+,tau i)",
        "raw_fold_boundary": "e_tau(i)-e_i",
        "raw_fold_odd_rank": rank(raw_images),
        "raw_selected_bar_H0_dimension": size - rank([selected_odd]),
        "conclusion": (
            "the honest groupoid bar only identifies the two labelled "
            "objects and has zero boundary after canonical transport.  The "
            "raw fold has the desired odd boundary but is a chain map only "
            "after supplying the missing physical W column"
        ),
    }


def pointed_basepoint_and_target_audit() -> dict[str, object]:
    values, tau = occurrence_packet()
    size = len(values)
    marked = values.index((0, 1, ((2, 3),)))
    mate = tau[marked]
    odd = add(unit(mate, size), unit(marked, size), -1)
    complete_target = tuple(Q(1) for _ in values)
    require(dot(complete_target, odd) == 0,
            "the endpoint-odd occurrence acquired a complete target")

    # Exact response-compatible counterexample: the aggregate complete row
    # evaluates to zero while the odd selected boundary does not.
    evaluation = [Q(0)] * size
    evaluation[marked] = 1
    evaluation[mate] = -1
    evaluation = tuple(evaluation)
    complete_value = dot(complete_target, evaluation)
    odd_value = dot(odd, evaluation)
    require(complete_value == 0 and odd_value == -2,
            "the pointed basepoint counterexample changed")

    # The complete physical target span is even.  It has no vector which can
    # serve as an occurrence-odd graph coordinate.  One new u^- coordinate
    # makes d b=o-u^- a rank-one relation in a 13-dimensional C0, preserving
    # H0 rank 12; without u^- the raw relation leaves H0 rank 11.
    old_target_rank = rank([complete_target])
    target_plus_odd_rank = rank([complete_target, odd])
    require(old_target_rank == 1 and target_plus_odd_rank == 2,
            "the odd target coordinate entered the complete response line")
    extended_boundary = odd + (Q(-1),)
    require((size + 1) - rank([extended_boundary]) == size,
            "one odd graph coordinate stopped preserving H0 rank")

    return {
        "marked": repr(values[marked]),
        "mate": repr(values[mate]),
        "odd_polynomial": "f_tau-f",
        "complete_response_target_on_odd": 0,
        "complete_response_quotient_counterguard": {
            "f": 1,
            "f_tau": -1,
            "complete_response_sum": str(complete_value),
            "pointed_bar_defect_f_tau_minus_f": str(odd_value),
            "scope": (
                "a quotient of the literal complete response row proving "
                "that the aggregate target equation alone does not force "
                "the odd equality; not an asserted full unary-compatible "
                "physical source point"
            ),
        },
        "pointed_DGA_condition": "epsilon_x(d b)=0",
        "condition_for_raw_bar": "f_tau(x)-f(x)=0",
        "condition_forced_by_complete_response": False,
        "complete_target_rank": old_target_rank,
        "rank_after_odd_occurrence_target": target_plus_odd_rank,
        "minimal_pointed_extension": (
            "one endpoint-odd occurrence graph coordinate u^- with "
            "d b=(f_tau-f)-u^-; it must carry value f_tau(x)-f(x) and the "
            "full word/fine/physical readouts"
        ),
        "minimal_extension_H0_dimension": size,
        "warning": (
            "a scalar zero-face correction alone is not in the mixed "
            "word/fine target grade; killing u^- afterward would again "
            "assume the physical occurrence comparison"
        ),
    }


def terminal_alternative_audit() -> dict[str, object]:
    lower = load(
        "computations/verify_h2_lower_centered_orientation_terminal_fork.py",
        "endpoint_role_terminal_fork",
    )
    ledger, digest = lower.audit()
    require(digest == lower.EXPECTED_LEDGER_SHA256,
            "the physical lower orientation fork changed")
    scope = ledger["physical_scope"]
    require(not scope["abstract_occurrence_nonzero_alone_is_terminal"]
            and "bidirectional private-site fan" in
            scope["odd_branch_existing_landing"],
            "the typed odd terminal alternative changed")
    return {
        "scalar_odd_bright": (
            "if f_tau(x)-f(x) is nonzero and the retained-label occurrence "
            "is identified with the literal same-tail offdiagonal cell, "
            "the bidirectional private-site fan gives four-good or a "
            "pure-colour coloop"
        ),
        "scalar_odd_dark": (
            "the pointed scalar obstruction vanishes, but the groupoid bar "
            "still does not define a fixed-object physical boundary"
        ),
        "full_augmented_alternative": (
            "the desired odd column is either in the complete physical "
            "image, or a full augmented cokernel covector detects it.  A "
            "nonzero physical-q kernel value normalizes to the relative "
            "generator; zero kernel value gives the Fredholm separator"
        ),
        "coefficient_odd_dual_is_terminal": False,
        "no_third_linear_branch": True,
    }


def word_histogram(word: str):
    return tuple(word.count(str(colour)) for colour in range(3))


def even_family_comparison_audit() -> dict[str, object]:
    lower = load(
        "computations/verify_h2_lower_centered_orientation_terminal_fork.py",
        "endpoint_even_lower_family",
    )
    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256,
            "the B-4 lower family changed")
    signless = load(
        "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py",
        "endpoint_even_Cplus",
    )
    signless_ledger, signless_digest = signless.audit()
    require(signless_digest == signless.EXPECTED_LEDGER_SHA256,
            "the signless C_plus gate changed")
    full = load(
        "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py",
        "endpoint_even_Cplus_full",
    )
    full_ledger, full_digest = full.audit()
    require(full_digest == full.EXPECTED_LEDGER_SHA256,
            "the C_plus full-interface gate changed")

    cuts = lower_ledger["physical_cuts"]["cuts"]
    require([cut["lower_word"] for cut in cuts] == ["0112", "0121"]
            and lower_ledger["physical_cuts"]["full_word"] == "01211222",
            "the literal B-4 words changed")
    cplus_word = signless_ledger["cut_and_target"]["selected_word"]
    require(cplus_word == "001122"
            and word_histogram(cplus_word) == (2, 2, 2)
            and {word_histogram(cut["lower_word"]) for cut in cuts}
                == {(1, 2, 1)},
            "the B-4/C_plus word signatures changed")
    forced = full_ledger["forced_full_interface_type"]
    descent = full_ledger["physical_descent_gate"]
    require(forced["formal_generator_rank"] == 1
            and forced["normalized_mixed_target"] == "-2 D tensor v"
            and forced["reduced_Eq_face"]
                == "+2 D (H0-u)Eq tensor v"
            and forced["labelled_ordinary_residue"] == "v"
            and not descent["source_valid"],
            "the forced C_plus augmented signature changed")
    b_minus_four = lower_ledger["packets"][0][
        "swap_even_hole_module"]["endpoint_adjacency"]
    require(not b_minus_four["physical_B_minus_4_lift_constructed"]
            and lower_ledger["packets"][0][
                "swap_even_hole_module"]["augmentation_zero_rank"] == 5,
            "the B-4 physical gate changed")

    return {
        "shared_structure": {
            "parity": "even",
            "Cartan_shape": "signless/endpoint-even Cartan product rule",
            "first_target_defect": "2*(w-1)*Delta",
            "interpretation": (
                "B-4 is a plausible new lower occurrence face of the same "
                "target-corrected construction theorem as C_plus"
            ),
        },
        "literal_B_minus_4": {
            "lower_words": [cut["lower_word"] for cut in cuts],
            "lower_word_histogram": [1, 2, 1],
            "reinsertion_grade": "01211222 / labelled repeated P3+K2",
            "involution": "endpoint-role tau at fixed sites",
            "coefficient_module": "rank-5 even centered hole quotient",
            "known_boundary": "c2^+=(B-4)*(-(B+6)c2^+/24)",
            "target_Rees_Eq_residue_signature": "not physically defined",
        },
        "literal_C_plus_iota": {
            "selected_word": cplus_word,
            "word_histogram": list(word_histogram(cplus_word)),
            "involution": "rho=(1 4) plus two-local 0<->2 Weyl",
            "source_module": "one rho-even omitted-label orbit",
            "generic_beta_only": True,
            "mixed_target": forced["normalized_mixed_target"],
            "same_grade_lower": "delta_plus",
            "reduced_Eq": forced["reduced_Eq_face"],
            "labelled_residue": forced["labelled_ordinary_residue"],
            "formal_tail_ainc_W_target_ores":
                descent["formal_tail_signature_ainc_W_target_ores"],
            "source_valid": descent["source_valid"],
        },
        "identical_literal_family": False,
        "first_nonidentity": (
            "the fixed endpoint-role groupoid and the rho/root collision "
            "groupoid are different labelled source categories; their "
            "source words and coefficient-module dimensions already differ"
        ),
        "missing_comparison": (
            "a source-labelled word/fine map carrying the B-4 lower faces "
            "to the one C_plus orbit, with the forced mixed target, "
            "delta_plus, reduced-Eq, labelled residue, Rees/beta, ridge, "
            "and W rows.  This is exactly the unconstructed iota/physical "
            "descent, not an equality of the existing columns"
        ),
        "unified_extension_possible": True,
        "unified_extension_constructed": False,
        "beta_zero": "remains the independent selected D0 Bockstein branch",
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "h2 endpoint-role groupoid pointed-bar gate",
        "pins": PINS,
        "two_object_groupoid": two_object_bar_audit(),
        "pointed_basepoint_and_target": pointed_basepoint_and_target_audit(),
        "physical_terminal_alternative": terminal_alternative_audit(),
        "B_minus_4_vs_C_plus": even_family_comparison_audit(),
        "verdict": (
            "Retaining endpoint labels makes the tau groupoid honest, but "
            "its canonical bar descends with zero boundary.  The fold that "
            "produces e_tau_f-e_f is the missing W comparison itself.  Its "
            "first pointed obstruction is f_tau(x)-f(x), which the even "
            "complete response target does not control; after that one "
            "still needs an odd occurrence-graph coordinate or a fully "
            "typed terminal.  The even B-4 and C_plus lanes share the same "
            "signless target-defect architecture, but are not the same "
            "literal family without the missing iota/augmented descent."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("endpoint-role pointed-bar ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("tau two-object groupoid bar: EXISTS")
    print("canonical fixed-label descent boundary: ZERO")
    print("raw odd fold: DESIRED CLASS BUT NOT A PHYSICAL CHAIN MAP")
    print("first pointed defect: f_tau(x)-f(x); complete target reads zero")
    print("minimal repair: one endpoint-odd occurrence graph coordinate")
    print("B-4 vs C_plus: SHARED ARCHITECTURE, NOT LITERAL IDENTIFICATION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
