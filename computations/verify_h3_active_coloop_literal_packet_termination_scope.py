#!/usr/bin/env python3
"""Compose the literal active-coloop packet and freeze its entry boundary.

The complete-response theorem 2448528 eliminates the two sharp closed-shore
traps of 5ddaa7e.  This checker composes that result with the K6 Galois
closure and proves the strongest sound termination statement: a completed
special two-occurrence packet cannot remain in a closed Hall state.  In its
last 4736 response-completion cases its certified family has empty Galois
transversal, so no nonempty opposite Hall shore remains cross-intersecting.

This does not normalize an arbitrary active-fan coloop.  Relabeling and
nonzero torus scaling preserve the number of nonzero cofactor matching
monomials and response occurrences.  The special packet has a monomial
pure-zero cofactor; an explicit normalized coloop guard has three nonzero
cofactor terms.  The missing theorem is therefore a source-valid sparse
packet extraction (or, more weakly, privacy in the closed-shore quotient),
not another Hall termination argument.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py":
        "fe60edcc44c33e660b50f7e8d627b506c5bd81c1d97f15e66b9e8a35e9f3c4ad",
    "notes/h3-active-coloop-closed-shore-complete-row-response-gate.md":
        "1470ffc55dff20f0919b4be884ca8d54efe7a15e90117d1610aef067c82b44b2",
    "computations/verify_h3_active_coloop_forced_mate_recurrence_potential_boundary.py":
        "f08e9bc7e7a2a6d561426890c60120b96b37334fb54337d06845fe78d3ffe984",
    "notes/h3-active-coloop-forced-mate-recurrence-potential-boundary.md":
        "3a6823f8b5e8d555883ecbb188137a8d6ec54351d54292ccd06ede3035c4f3aa",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
    "notes/h3-active-fan-coloop-saturation-boundary.md":
        "4431948d139c45f8619928878b0dde0cba39ddc9a0942bd6a899bd9d53daa1d6",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "notes/h3-active-fan-coloop-complete-row-pivot.md":
        "2a68b7a9da9c61c67c4f63e666a6cbb1023344722943b9042f2ff15b2863e92e",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
}
EXPECTED_LEDGER_SHA256 = "aa8f091cda9fa8d7a90b338c65f68bc1595bbd19610d7f95f4939abccf93be88"


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


def audit_hall_exhaustivity(saturation):
    """No containing closed concept is exactly empty Galois transversal."""
    concepts = set()
    for mask in range(1, saturation.FULL_MASK + 1):
        mate = saturation.transversal(mask)
        if mate:
            concepts.add((saturation.transversal(mate), mate))
    require(len(concepts) == 446, "the K6 closed-concept census changed")

    empty_transversal = 0
    for mask in range(1, saturation.FULL_MASK + 1):
        empty = saturation.transversal(mask) == 0
        contained = any(mask & ~left == 0 for left, _right in concepts)
        require(empty == (not contained),
                ("Hall/closed-containment equivalence failed", mask,
                 saturation.mask_edges(mask)))
        empty_transversal += int(empty)
    require(empty_transversal == saturation.FULL_MASK - 5141,
            "the empty-transversal family count changed")
    return {
        "nonempty_edge_families_checked": saturation.FULL_MASK,
        "closed_ordered_concepts": len(concepts),
        "families_with_empty_transversal": empty_transversal,
        "equivalence": (
            "T(A)=empty iff no closed shore contains A; if T(A) is nonempty "
            "then cl(A)=T(T(A)) is one of the 446 closed shores containing A"
        ),
        "consequence_for_2448528": (
            "zero containing closed shores in all 4736 response completions "
            "means T(A)=empty.  Therefore no nonempty opposite effective-hole "
            "family B can satisfy B subset T(A): some a in A and b in B are "
            "disjoint, the pinned free-Hall/four-good alternative"
        ),
    }


def audit_special_packet_composition(response_gate, saturation):
    result = response_gate.audit()
    census = result["simultaneous_unary_mate_census"]
    exit_result = result["completed_response_seed_hall_exit"]
    require(census["simultaneous_mate_choices"] == 2744
            and census["pure_zero_coloop_escapes"] == 728
            and census["new_pure_one_target_response_occurrences"] == 288
            and census["trapped_closed_shore_packets"] == 148,
            ("the literal three-unary branch split changed", census))
    require(exit_result["total_completions_tested"] == 4736
            and exit_result["closed_shore_survivors"] == 0,
            ("the response completion exit changed", exit_result))

    saturation_result = saturation.audit_galois_saturation()
    require(saturation_result["closed_ordered_concepts"] == 446
            and "15-|cl(A)|" in saturation_result["potential"],
            ("the finite Hall saturation theorem changed", saturation_result))
    return {
        "literal_packet_processor": {
            "three_unary_mate_choices": 2744,
            "named_coloop_destroyed": 728,
            "new_selected_target_response_occurrence": 288,
            "all_offdiagonal_with_immediate_outside_growth": 1580,
            "initially_trapped_nine_edge_packets": 148,
            "response_completions_of_trapped_packets": 4736,
            "response_completions_still_cross_intersecting": 0,
        },
        "formal_local_termination": (
            "the special packet has no transition back to its original "
            "closed Hall state: it destroys the named coloop, enlarges the "
            "selected target packet, or makes the certified shore transversal "
            "empty and hence forces a disjoint cross-shore/free-Hall landing"
        ),
        "finite_saturation_role": (
            "outside-shore steps decrease 15-|cl(A)| and cannot cycle; in "
            "the final 4736 response cases the stronger T(A)=empty conclusion "
            "already gives a disjoint pair against the nonempty opposite fan "
            "shore without another iteration"
        ),
        "handoff_warning": (
            "if named-coloop destruction exposes another coloop, or a new "
            "target occurrence is reselected, the resulting packet is "
            "arbitrary; reapplying this special processor requires the "
            "separate sparse-entry theorem audited below"
        ),
    }


def q_label(left, right, left_colour=0, right_colour=0):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right, left_colour, right_colour)


def product_values(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def cofactor_terms(first, q_values, coloop=(0, 1), colour=0):
    remaining = tuple(site for site in first.SITES if site not in coloop)
    answer = []
    for matching in first.perfect_matchings(remaining):
        value = product_values(
            q_values.get(q_label(left, right, colour, colour), Q(0))
            for left, right in matching
        )
        if value:
            answer.append((matching, value))
    return tuple(answer)


def audit_symmetry_scaling_boundary(first):
    _p_values, _s_values, special_q = first.literal_guard_values()
    special_terms = cofactor_terms(first, special_q)
    require(special_terms == ((((2, 3), (4, 5)), Q(1)),),
            ("the special monomial cofactor changed", special_terms))

    # A normalized pure-zero coloop with three residual cofactor monomials.
    # Every nonzero pure-zero six-site matching still contains 01, while the
    # cofactor is 1+1-1=1.  Nonzero torus scaling and relabeling cannot turn
    # any of these three support terms off.
    general_q = {
        q_label(0, 1): Q(1),
        q_label(2, 3): Q(1), q_label(4, 5): Q(1),
        q_label(2, 4): Q(1), q_label(3, 5): Q(1),
        q_label(2, 5): Q(1), q_label(3, 4): Q(-1),
    }
    general_terms = cofactor_terms(first, general_q)
    require(len(general_terms) == 3
            and sum(value for _matching, value in general_terms) == 1,
            ("the three-tail cofactor guard changed", general_terms))
    pure_matchings = tuple(
        matching for matching in first.MATCHINGS6
        if product_values(general_q.get(q_label(left, right), Q(0))
                          for left, right in matching)
    )
    require(len(pure_matchings) == 3
            and all((0, 1) in matching for matching in pure_matchings),
            ("the three-tail packet lost literal coloopness", pure_matchings))

    # The support count is preserved because site/colour relabeling is a
    # bijection and multiplication by nonzero torus characters preserves
    # exactly which coordinates and monomial products vanish.
    require(len(special_terms) != len(general_terms),
            "the support-count obstruction disappeared")
    return {
        "special_packet_pure_c_cofactor_support": len(special_terms),
        "arbitrary_coloop_guard_cofactor_support": len(general_terms),
        "arbitrary_guard_terms": [
            {"matching": repr(matching), "value": str(value)}
            for matching, value in general_terms
        ],
        "arbitrary_guard_normalization": "q01[00]*C_0=1*(1+1-1)=1",
        "arbitrary_guard_literal_coloop": (
            "the three nonzero pure-zero perfect matchings all contain 01"
        ),
        "orbit_invariant": (
            "site/colour relabeling and nonzero diagonal scaling preserve "
            "the number of nonzero cofactor matching monomials"
        ),
        "conclusion": (
            "an arbitrary normalized literal coloop is not in the symmetry/"
            "scaling orbit of the monomial-cofactor two-occurrence guard"
        ),
        "scope": (
            "this is a source-support guard, not a new full GHZ solution; it "
            "refutes only a formal relabeling/scaling reduction"
        ),
    }


def audit():
    pin_dependencies()
    response_gate = load(
        "computations/verify_h3_active_coloop_closed_shore_complete_row_response_gate.py",
        "literal_termination_response_gate",
    )
    saturation = load(
        "computations/verify_h3_active_fan_coloop_saturation_boundary.py",
        "literal_termination_saturation",
    )
    first = load(
        "computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py",
        "literal_termination_first_gate",
    )
    ledger = {
        "theorem": "h3 active-coloop literal-packet termination and entry scope",
        "pins": PINS,
        "hall_exhaustivity": audit_hall_exhaustivity(saturation),
        "special_packet_termination":
            audit_special_packet_composition(response_gate, saturation),
        "relabel_scaling_boundary": audit_symmetry_scaling_boundary(first),
        "exact_missing_arbitrary_entry": {
            "name": "closed-shore-private sparse two-occurrence extraction",
            "input": (
                "an arbitrary source-provenant active fan, a literal pure-c "
                "coloop alpha with alpha*C_c=1, and the complete unary/four-"
                "response packet furnished by the uniform coloop pivot"
            ),
            "required_output": (
                "either an existing anchor-safe deletion, target-fibre point, "
                "typed outside-shore/four-good exit, or a choice of one "
                "nonzero residual cofactor tail and one endpoint pair for "
                "which the three mixed tail-square R rows are private modulo "
                "the current closed-shore span"
            ),
            "protected_data": (
                "word, fine/repeated grade, response head and orientation, "
                "common residual q tail, and every selected mutual anchor"
            ),
            "why_this_is_weakest": (
                "2448528 uses only privacy of those three mixed response "
                "rows; it does not require all unrelated source coordinates "
                "to vanish.  Exact support equality with the displayed "
                "literal guard would be a stronger sufficient theorem"
            ),
        },
        "final_scope": (
            "the closed-shore recurrence is terminated for the pinned special "
            "two-occurrence packet.  Arbitrary active-fan coloop normalization "
            "does not follow by relabeling/scaling and remains equivalent to "
            "the closed-shore-private sparse extraction above; Hall saturation "
            "and termination are no longer part of that missing statement"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("literal-packet termination ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    print("special active-coloop closed-shore packet: TERMINATES")
    print("4736/4736 response completions: EMPTY TRANSVERSAL / FREE HALL")
    print("arbitrary coloop by relabel/scaling: NO (cofactor support 1 vs 3)")
    print("ledger_sha256=" + digest)
    return ledger


if __name__ == "__main__":
    audit()
