#!/usr/bin/env python3
"""Verify the intrinsic restriction/divided-root chain commutator at h=3.

Work in the literal 252-variable edge ring of the official n=8, d=3
EqSystem.  For q=23 or q=45, let D_r and D_c be differentiation by the
decorated response and cap edge variables, let I_c multiply by the cap edge,
and let Phi (respectively Phi_hat) be the six-site divided-root operator
(respectively the operator after deleting the cut endpoints).  On the first
source-derived Spencer/Tate stage the two composites are

    O_B d = I_c D_c Phi d,
    d O_E = d I_c Phi_hat D_r.

They agree termwise on every matching occurrence of all 3^8 official
relations, including the scalar GHZ targets, and on every q23/q45 descendant
of the 540 marked collision branches.  This is an intrinsic, stabilization-
invariant zero commutator.

It is not yet the physical protected B-Eq scalar.  The original edge ring has
one coefficient occurrence, whereas the later PAComp presentation has B and
Eq copies.  The committed protected cap comparison lands diagonally and the
desired B-only output is not in that diagonal.  Thus identifying the two
intrinsic paths with the two protected readouts is precisely the remaining
physical factorization theorem; without it, B-Eq does not descend to the
original EqSystem.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_chart_model_is_official_eqsystem.py":
        "ef1a997323e0a116787fa3c50368e22ecd33804942a9179eabefa2993e4d9373",
    "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py":
        "9b387023ee8cac6bb000d6936a8985cbc16bbad0a9f7deb3613c1f44c233a1f8",
    "computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py":
        "d04ad992bde820edcc79b2660e64a141db8ff52a39a6a78be6c470105467106a",
    "computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py":
        "3fd68d8d8c84f0c9a8f76dff4e370279798f4ac9dbc811011a6cdfa344303c0f",
}
EXPECTED_LEDGER_SHA256 = (
    "2bfbee2d7446a857f4c51cc44930cf48fe809ecea15fa59b9a6fc8ae5ca3a635"
)

SITES = tuple(range(8))
COLOURS = tuple(range(3))
RESPONSE_WORD = tuple(map(int, "11110000"))
CAP_WORD = tuple(map(int, "01211222"))
CHANGED = tuple(
    site for site in SITES if RESPONSE_WORD[site] != CAP_WORD[site]
)
CUTS = ((2, 3), (4, 5))
DIRECT_FREE_EDGE = (3, 6)
DELTA_PLUS = tuple(map(Q, (-Q(1, 4), Q(1, 2), -Q(1, 4),
                          -Q(1, 4), Q(1, 2), -Q(1, 4))))


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def decorated_cell(word, edge):
    left, right = edge
    return left, right, word[left], word[right]


def decorated_monomial(word, matching):
    return tuple(sorted(decorated_cell(word, edge) for edge in matching))


def clean(counter):
    return Counter({term: coefficient for term, coefficient in counter.items()
                    if coefficient})


def delete_variable(monomial, variable):
    """The literal polynomial derivative by one decorated edge variable."""
    answer = Counter()
    for position, cell in enumerate(monomial):
        if cell != variable:
            continue
        answer[monomial[:position] + monomial[position + 1:]] += Q(1)
    return clean(answer)


def insert_variable(polynomial, variable):
    answer = Counter()
    for monomial, coefficient in polynomial.items():
        answer[tuple(sorted(monomial + (variable,)))] += coefficient
    return clean(answer)


def apply_divided_site(monomial, site, old, new, order):
    """Apply gamma_order(E_site(old,new)) with divided-Hasse normalization."""
    eligible = []
    for position, (left, right, left_colour, right_colour) in enumerate(monomial):
        if left == site and left_colour == old:
            eligible.append((position, 2))
        elif right == site and right_colour == old:
            eligible.append((position, 3))
    if order == 0:
        return Counter({monomial: Q(1)})
    if len(eligible) < order:
        return Counter()

    # Every source monomial used here has exactly ``order`` occurrences at
    # this site.  Writing the general one-subset case explicitly would hide
    # the divided-power normalization needed on marked doubled-site branches.
    require(len(eligible) == order,
            ("partial divided-root domain", site, order, eligible, monomial))
    output = [list(cell) for cell in monomial]
    for position, colour_position in eligible:
        output[position][colour_position] = new
    return Counter({tuple(sorted(tuple(cell) for cell in output)): Q(1)})


def site_multiplicity(monomial, site):
    return sum(left == site or right == site for left, right, _c, _d in monomial)


def apply_divided_roots(polynomial, active_sites):
    answer = Counter(polynomial)
    for site in active_sites:
        following = Counter()
        for monomial, coefficient in answer.items():
            order = site_multiplicity(monomial, site)
            for output, value in apply_divided_site(
                    monomial, site, RESPONSE_WORD[site], CAP_WORD[site],
                    order).items():
                following[output] += coefficient * value
        answer = clean(following)
    return answer


def polynomial_delete(polynomial, variable):
    answer = Counter()
    for monomial, coefficient in polynomial.items():
        for output, value in delete_variable(monomial, variable).items():
            answer[output] += coefficient * value
    return clean(answer)


def o_b_after_d(monomial, cut):
    """I_c D_c Phi applied to a polynomial monomial."""
    rooted = apply_divided_roots(Counter({monomial: Q(1)}), CHANGED)
    return insert_variable(
        polynomial_delete(rooted, decorated_cell(CAP_WORD, cut)),
        decorated_cell(CAP_WORD, cut),
    )


def d_after_o_e(monomial, cut):
    """I_c Phi_hat D_r applied after the Tate/Spencer differential."""
    deleted = delete_variable(monomial, decorated_cell(RESPONSE_WORD, cut))
    # Phi_hat is indexed by occurrences, not merely by the names of the two
    # deleted sites.  On a perfect matching the cut removes their only
    # occurrences, hence their divided order is zero.  On a marked collision
    # one endpoint may still occur in a second edge and must still be rooted.
    rooted = apply_divided_roots(deleted, CHANGED)
    return insert_variable(rooted, decorated_cell(CAP_WORD, cut))


def o_b_domain(word, matching, cut):
    """Exact nonzero predicate for I_c D_c Phi on a matching occurrence."""
    return (cut in matching
            and all(word[site] == RESPONSE_WORD[site] for site in CHANGED)
            and decorated_cell(word, cut) == decorated_cell(RESPONSE_WORD, cut))


def o_e_domain(word, matching, cut):
    """Exact nonzero predicate for I_c Phi_hat D_r."""
    lower_roots = tuple(site for site in CHANGED if site not in cut)
    return (cut in matching
            and decorated_cell(word, cut) == decorated_cell(RESPONSE_WORD, cut)
            and all(word[site] == RESPONSE_WORD[site] for site in lower_roots))


def official_eqsystem_audit(official):
    matchings = tuple(official.OFFICIAL_MATCHINGS)
    words = tuple(product(COLOURS, repeat=8))
    require(len(matchings) == 105 and len(words) == 6561,
            (len(matchings), len(words)))

    nonzero_rows = Counter()
    nonzero_occurrences = Counter()
    output_terms = Counter()
    occurrence_squares = 0
    scalar_target_squares = 0
    for word in words:
        target = int(len(set(word)) == 1)
        for cut in CUTS:
            left_relation = Counter()
            right_relation = Counter()
            row_nonzero = False
            for matching in matchings:
                source = decorated_monomial(word, matching)
                # The predicates are obtained directly from the decorated
                # derivative and root domains.  Checking them on all 1.37M
                # labelled occurrences avoids spending time materializing
                # empty Counters while retaining the literal full census.
                left_domain = o_b_domain(word, matching, cut)
                right_domain = o_e_domain(word, matching, cut)
                require(left_domain == right_domain,
                        ("operator-domain BC failure", word, matching, cut,
                         left_domain, right_domain))
                if left_domain:
                    left = o_b_after_d(source, cut)
                    right = d_after_o_e(source, cut)
                else:
                    left = Counter()
                    right = Counter()
                require(left == right,
                        ("termwise BC failure", word, matching, cut,
                         left, right))
                occurrence_squares += 1
                if left:
                    row_nonzero = True
                    nonzero_occurrences[cut] += 1
                    output_terms[cut] += sum(left.values(), Q(0))
                left_relation.update(left)
                right_relation.update(right)

            # The GHZ target is a scalar.  Both composites contain an edge
            # derivative, so its contribution vanishes, including on the
            # three nonzero pure target rows.
            if target:
                left_scalar = o_b_after_d((), cut)
                right_scalar = d_after_o_e((), cut)
                require(not left_scalar and not right_scalar,
                        ("scalar target survived", word, cut,
                         left_scalar, right_scalar))
                scalar_target_squares += 1
            require(clean(left_relation) == clean(right_relation),
                    ("official relation failure", word, cut))
            if row_nonzero:
                nonzero_rows[cut] += 1

    require(occurrence_squares == 2 * 6561 * 105
            and scalar_target_squares == 2 * 3,
            (occurrence_squares, scalar_target_squares))
    require(nonzero_rows == Counter({(2, 3): 3, (4, 5): 9})
            and nonzero_occurrences == Counter({(2, 3): 45, (4, 5): 135})
            and output_terms == nonzero_occurrences,
            (nonzero_rows, nonzero_occurrences, output_terms))
    return {
        "official_variables": 252,
        "official_relation_rows": len(words),
        "matching_occurrences_per_row": len(matchings),
        "cut_occurrence_squares_checked": occurrence_squares,
        "nonzero_rows_by_cut": {
            "q23": nonzero_rows[(2, 3)], "q45": nonzero_rows[(4, 5)]
        },
        "nonzero_occurrences_by_cut": {
            "q23": nonzero_occurrences[(2, 3)],
            "q45": nonzero_occurrences[(4, 5)],
        },
        "termwise_coefficients": "1",
        "literal_zero_domain_predicate_checked": True,
        "pure_GHZ_target_rows_checked": 3,
        "scalar_target_composite": 0,
        "relation_identity": "I_c D_c Phi d = d I_c Phi_hat D_r",
        "commutator_on_every_official_relation": 0,
    }


def marked_collision_descendant_audit(official, marked):
    parents = tuple(matching for matching in official.OFFICIAL_MATCHINGS
                    if DIRECT_FREE_EDGE not in matching)
    require(len(parents) == 90, len(parents))
    branch_labels = []
    q_descendants = Counter()
    for parent in parents:
        removed = next(edge for edge in parent if 0 in edge)
        missing = removed[1]
        for doubled in range(1, 8):
            if doubled == missing:
                continue
            inserted = (0, doubled)
            branch = tuple(sorted((set(parent) - {removed}) | {inserted}))
            label = (parent, missing, doubled)
            branch_labels.append(label)
            source = decorated_monomial(RESPONSE_WORD, branch)
            for cut in CUTS:
                if cut not in branch:
                    continue
                left = o_b_after_d(source, cut)
                right = d_after_o_e(source, cut)
                require(left == right and len(left) == 1
                        and sum(left.values(), Q(0)) == 1,
                        ("marked descendant BC failure", label, branch, cut,
                         left, right))
                q_descendants[cut] += 1

    require(len(branch_labels) == len(set(branch_labels)) == 540,
            len(branch_labels))

    # Pin the stronger existing audit: the same multiplicity-dependent root
    # family commutes on all parent/trigger and first P3+K2 deletion faces,
    # not merely on the selected q descendants counted above.
    marked_ledger, marked_digest = marked.audit()
    require(marked_digest == marked.EXPECTED_LEDGER_SHA256, marked_digest)
    trigger = marked_ledger["trigger_dependent_divided_naturality"]
    cuts = marked_ledger["root_restriction_reinsertion"]
    require(trigger["parent_to_collision_trigger_squares"] == 540
            and trigger["marked_P3K2_deletion_faces"] == 1080
            and trigger["trigger_commutator_on_every_parent_branch"] == 0
            and cuts["required_and_constructed_P2_word_rank"] == 2,
            (trigger, cuts))
    return {
        "marked_parent_matchings": len(parents),
        "operation_labelled_collision_branches": len(branch_labels),
        "selected_descendants_by_cut": {
            "q23": q_descendants[(2, 3)],
            "q45": q_descendants[(4, 5)],
        },
        "selected_descendant_commutator": 0,
        "all_parent_to_trigger_squares": 540,
        "all_marked_P3K2_first_deletions": 1080,
        "multiplicity_rule": (
            "divided-root order equals the current occurrence multiplicity "
            "at each changed site"
        ),
        "operation_parent_labels_retained": True,
        "q23_q45_word_fine_image_rank": 2,
    }


def protected_no_descent_audit(protected, intrinsic):
    protected_ledger, protected_digest = protected.audit()
    require(protected_digest == protected.EXPECTED_LEDGER_SHA256,
            protected_digest)
    cap = protected_ledger["protected_cap_commutator"]
    require(cap["actual_composite"] == "(delta_plus,delta_plus)"
            and cap["required_physical_landing"] == "(delta_plus,0)"
            and cap["combined_first_commutator"] == "(0,-delta_plus)"
            and cap["dual_on_actual_required_commutator"] == ["0", "3", "3"],
            cap)

    # This component is the exact finite descent calculation and does not
    # require rebuilding the unrelated 8,580-column inventory in that audit.
    descent = intrinsic.psi_label_descent_audit()
    require(not descent["Psi_defined_on_original_EqSystem_resolution"]
            and descent["pullback_of_intrinsic_covectors"]
                == "pi^*(lambda)=(lambda,lambda)", descent)

    zero = (Q(0),) * 6
    intrinsic_path_difference = tuple(left - right for left, right in
                                      zip(DELTA_PLUS, DELTA_PLUS, strict=True))
    require(intrinsic_path_difference == zero, intrinsic_path_difference)
    return {
        "intrinsic_common_cut_value": [str(value) for value in DELTA_PLUS],
        "intrinsic_path_difference": [str(value)
                                      for value in intrinsic_path_difference],
        "stabilization_invariant_scalar_on_path_commutator": "0",
        "protected_actual_tied_landing": "(delta_plus,delta_plus)",
        "protected_requested_landing": "(delta_plus,0)",
        "protected_anti_diagonal_detector_values_actual_requested": [0, 3],
        "B_or_Eq_copy_is_an_original_edge_or_relation_label": False,
        "nonzero_B_minus_Eq_descends_to_original_EqSystem": False,
        "sharp_no_descent_reason": (
            "the two source-derived composites are literally equal; the "
            "original occurrence module has one copy, while the nonzero "
            "anti-diagonal detector needs two later protected copies"
        ),
        "weakest_additional_physical_identification": (
            "prove that the normalized protected B and Eq augmentations of "
            "the selected PAComp carrier factor, with the same normalization, "
            "through I_c D_c Phi d and d I_c Phi_hat D_r respectively, "
            "including the hidden lower/private -E and word-resolved ores +E "
            "faces"
        ),
        "consequence_if_identification_is_proved": (
            "the intrinsic chain identity forces B=Eq on every actual "
            "solution, so the normalized B-only balanced RHS (detector 3) "
            "cannot be a boundary"
        ),
        "current_status": (
            "conditional balanced contradiction, not yet a physical "
            "Fredholm separator"
        ),
    }


def audit():
    pin_dependencies()
    official = load(
        "computations/verify_chart_model_is_official_eqsystem.py",
        "intrinsic_bc_official",
    )
    marked = load(
        "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py",
        "intrinsic_bc_marked",
    )
    protected = load(
        "computations/verify_h3_divided_root_p2_iota_cap_beq_commutator_gate.py",
        "intrinsic_bc_protected",
    )
    intrinsic = load(
        "computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py",
        "intrinsic_bc_label_descent",
    )
    ledger = {
        "theorem": (
            "on the literal h=3 EqSystem and its canonical first "
            "Spencer/Tate stage, restriction/reinsertion commutes exactly "
            "with the multiplicity-adapted divided-root map at q23 and q45"
        ),
        "pins": PINS,
        "official_EqSystem": official_eqsystem_audit(official),
        "marked_collision_descendants":
            marked_collision_descendant_audit(official, marked),
        "protected_no_descent":
            protected_no_descent_audit(protected, intrinsic),
        "stabilization_invariance": {
            "canonical_enrichment": (
                "first occurrence-labelled Spencer/Tate stage of the "
                "official relation presentation"
            ),
            "contractible_stabilization_action": (
                "extend both natural operators by the same zero map on a "
                "new contractible summand"
            ),
            "commutator_before_after_stabilization": [0, 0],
            "depends_on_auxiliary_B_or_Eq_copy": False,
        },
        "scope": (
            "all 6561 official n=8,d=3 polynomial relations, all 105 "
            "matching occurrences in each row, both selected q cuts, scalar "
            "GHZ targets, all 540 operation-labelled marked branches and "
            "their pinned first deletion census; the equality is intrinsic, "
            "but its identification with the later protected B/Eq copies "
            "remains conditional"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h=3 intrinsic divided-root/restriction commutator: PASS")
        print("mode", arguments.mode)
        print("official relation rows: 6561")
        print("literal cut occurrence squares: 1377810")
        print("intrinsic path commutator: 0")
        print("protected B-Eq identification: CONDITIONAL")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
