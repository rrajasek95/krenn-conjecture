#!/usr/bin/env python3
"""Audit q23/q45 restriction of the six-root marked word section.

On squarefree perfect matchings, deleting a cap edge commutes with the
six-root word operator only after the roots at the deleted endpoints are
omitted.  On a collision branch this has to be upgraded further: the root
at a site must be taken in divided order equal to the incidence
multiplicity of that site.  The resulting Hasse/substitution operator
commutes with every q23/q45 deletion and with the first PP differential.

For the selected branch 07|23|45|67 this constructs the two literal
marked-derived coefficient/word/fine faces with lower words 0112 and 0121.
It does not by itself change their marked-derived operation idempotent into
the underived physical B1/B4 (P2) idempotents.  The pinned augmented system
therefore still needs the source-labelled operation landing and its
(-E,+E) lower/ordinary-residue faces.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_six_root_marked_collision_word_section.py":
        "d0da0f1473fc1032416c3758ffc932531ac71698c2370ee67224baedd2e13f95",
    "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py":
        "a1e81eef9343bd2dda01b106acc202698cc12e93e7db3b55d45f5c6268779c33",
    "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py":
        "346f3885bae10462c11f8046240ad4bc5970f0950a25b163235445592be0e9ab",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
}
EXPECTED_LEDGER_SHA256 = (
    "e476c8a59693a496fa0ba81a4954b8e9d7ac973d3c2be3dca9c6a901e615945b"
)

SITES = tuple(range(8))
RESPONSE_WORD = tuple(map(int, "11110000"))
CAP_WORD = tuple(map(int, "01211222"))
CHANGED = tuple(site for site in SITES
                if RESPONSE_WORD[site] != CAP_WORD[site])
DIRECT_FREE_EDGE = (3, 6)
Q23 = (2, 3)
Q45 = (4, 5)
SELECTED_PARENT = ((0, 1), (2, 3), (4, 5), (6, 7))
SELECTED_BRANCH = ((0, 7), (2, 3), (4, 5), (6, 7))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def decorated(word, edges, marked=None):
    return tuple(sorted(
        (left, right, word[left], word[right], edge == marked)
        for edge in edges for left, right in (edge,)
    ))


def delete_cell(term, edge):
    answer = tuple(cell for cell in term if cell[:2] != edge)
    return answer if len(answer) + 1 == len(term) else None


def apply_divided_site(term, site, old, new, order):
    eligible = []
    for position, cell in enumerate(term):
        left, right, left_colour, right_colour, _marked = cell
        if left == site and left_colour == old:
            eligible.append((position, 2))
        elif right == site and right_colour == old:
            eligible.append((position, 3))
    output = Counter()
    for chosen in combinations(eligible, order):
        image = list(term)
        for position, colour_position in chosen:
            cell = list(image[position])
            cell[colour_position] = new
            image[position] = tuple(cell)
        output[tuple(sorted(image))] += Q(1)
    return {term: coefficient for term, coefficient in output.items()
            if coefficient}


def apply_root_orders(term, orders):
    terms = {term: Q(1)}
    for site in CHANGED:
        following = Counter()
        for source, coefficient in terms.items():
            for target, value in apply_divided_site(
                    source, site, RESPONSE_WORD[site], CAP_WORD[site],
                    orders[site]).items():
                following[target] += coefficient * value
        terms = {target: value for target, value in following.items() if value}
    return terms


def multiplicities(edges):
    count = Counter(site for edge in edges for site in edge)
    return tuple(count[site] for site in SITES)


def divided_root(term, edges):
    return apply_root_orders(term, multiplicities(edges))


def ordinary_root(term):
    return apply_root_orders(term, tuple(
        1 if site in CHANGED else 0 for site in SITES
    ))


def perfect_matching_restriction_audit(word_section) -> dict[str, object]:
    matchings = tuple(word_section.perfect_matchings(SITES))
    require(len(matchings) == 105, len(matchings))
    records = []
    for cut in (Q23, Q45):
        cap_cell = tuple((*cut, CAP_WORD[cut[0]], CAP_WORD[cut[1]], False))
        source_cell = tuple((
            *cut, RESPONSE_WORD[cut[0]], RESPONSE_WORD[cut[1]], False
        ))
        hit_rows = set()
        direct_free_rows = set()
        naive_nonzero = 0
        corrected_nonzero = 0
        active_orders = tuple(
            int(site in CHANGED and site not in cut) for site in SITES
        )
        for matching in matchings:
            source = decorated(RESPONSE_WORD, matching)
            target = decorated(CAP_WORD, matching)
            full_image = ordinary_root(source)
            require(full_image == {target: Q(1)},
                    ("ordinary perfect-matching root changed", matching))
            left = Counter()
            for image, coefficient in full_image.items():
                face = delete_cell(image, cut)
                if face is not None:
                    left[face] += coefficient
            source_face = delete_cell(source, cut)
            naive = {} if source_face is None else ordinary_root(source_face)
            corrected = ({} if source_face is None else
                         apply_root_orders(source_face, active_orders))
            if source_face is None:
                require(not left and not naive and not corrected,
                        (cut, matching, left, naive, corrected))
                continue
            require(source_cell in source and cap_cell in target,
                    (cut, source, target))
            require(not naive and corrected == dict(left),
                    ("root/deletion BC", cut, matching, left, naive,
                     corrected))
            naive_nonzero += bool(left)
            corrected_nonzero += bool(corrected)
            hit_rows.update(left)
            if DIRECT_FREE_EDGE not in matching:
                direct_free_rows.update(left)
        active_inputs = {
            RESPONSE_WORD[site] for site in CHANGED if site not in cut
        }
        remaining = tuple(site for site in SITES if site not in cut)
        expected_direct_free_rank = 15 if cut == Q23 else 12
        require(len(hit_rows) == naive_nonzero == corrected_nonzero == 15
                and len(direct_free_rows) == expected_direct_free_rank
                and active_inputs == {0, 1},
                (cut, len(hit_rows), naive_nonzero, corrected_nonzero,
                 len(direct_free_rows), active_inputs))
        records.append({
            "cut": "q23:21" if cut == Q23 else "q45:12",
            "source_cell": list(source_cell),
            "cap_cell": list(cap_cell),
            "remaining_source_word": "".join(
                str(RESPONSE_WORD[site]) for site in remaining),
            "remaining_cap_word": "".join(
                str(CAP_WORD[site]) for site in remaining),
            "full_matching_face_rank": len(hit_rows),
            "direct_free_face_rank": len(direct_free_rows),
            "naive_same_six_roots_after_deletion_rank": 0,
            "naive_BC_commutator_rank_direct_free": len(direct_free_rows),
            "endpoint_omitted_root_BC_commutator_rank": 0,
            "target_safe_on_six_site_face": True,
        })
    return {
        "operator": "ordinary order-one roots on squarefree matchings",
        "perfect_matchings_checked": len(matchings),
        "changed_sites": list(CHANGED),
        "restriction_records": records,
        "exact_rule": (
            "D_e R_S = R_(S minus changed endpoints(e)) D_e"
        ),
        "why_naive_restriction_fails": (
            "a root at an absent deleted endpoint annihilates the cofactor"
        ),
    }


def branch_rows(bc):
    parents = tuple(matching for matching in bc.perfect_matchings(bc.SITES)
                    if bc.DIRECT_FREE_EDGE not in matching)
    output = []
    for parent_index, parent_set in enumerate(parents):
        parent = tuple(sorted(parent_set))
        source_edge = next(edge for edge in parent if 0 in edge)
        missing = source_edge[1]
        for doubled in range(1, 8):
            if doubled == missing:
                continue
            branch = tuple(sorted(
                (set(parent) - {source_edge}) | {(0, doubled)}
            ))
            output.append((parent_index, parent, missing, doubled, branch))
    require(len(output) == 540, len(output))
    return tuple(output)


def first_pp_naturality(edges):
    source_sum = Counter()
    target_sum = Counter()
    for edge in edges:
        source_sum[decorated(RESPONSE_WORD, edges, edge)] += Q(1)
        target_sum[decorated(CAP_WORD, edges, edge)] += Q(1)
    image = Counter()
    for source, coefficient in source_sum.items():
        for target, value in divided_root(source, edges).items():
            image[target] += coefficient * value
    return ({term: value for term, value in image.items() if value}
            == dict(target_sum))


def divided_branch_restriction_audit(bc) -> dict[str, object]:
    rows = branch_rows(bc)
    deletion_counts = Counter()
    p3_counts = Counter()
    for _parent_index, _parent, _missing, _doubled, branch in rows:
        source = decorated(RESPONSE_WORD, branch)
        target = decorated(CAP_WORD, branch)
        require(divided_root(source, branch) == {target: Q(1)},
                ("branch root", branch))
        for cut in (Q23, Q45):
            if cut not in branch:
                continue
            deletion_counts[cut] += 1
            lower = tuple(edge for edge in branch if edge != cut)
            target_face = delete_cell(target, cut)
            require(target_face is not None
                    and divided_root(decorated(RESPONSE_WORD, lower), lower)
                        == {target_face: Q(1)},
                    ("divided deletion BC", branch, cut, target_face))
            if bc.site_profile(frozenset(lower)) == (2, 1, 1, 1, 1):
                p3_counts[cut] += 1
    require(deletion_counts == {Q23: 90, Q45: 72}
            and p3_counts == {Q23: 60, Q45: 48},
            (deletion_counts, p3_counts))

    selected = next(row for row in rows
                    if row[1] == SELECTED_PARENT
                    and row[-1] == SELECTED_BRANCH)
    _parent_index, _parent, missing, doubled, branch = selected
    source = decorated(RESPONSE_WORD, branch)
    target = decorated(CAP_WORD, branch)
    ordinary = ordinary_root(source)
    require(len(ordinary) == 2 and target not in ordinary
            and divided_root(source, branch) == {target: Q(1)},
            (ordinary, target))

    selected_faces = []
    for cut, physical_word, required_label in (
            (Q23, "0112", "0112/q23:21 -> B1"),
            (Q45, "0121", "0121/q45:12 -> B4")):
        lower = tuple(edge for edge in branch if edge != cut)
        source_face = decorated(RESPONSE_WORD, lower)
        target_face = decorated(CAP_WORD, lower)
        full_orders = multiplicities(branch)
        require(not apply_root_orders(source_face, full_orders)
                and divided_root(source_face, lower)
                    == {target_face: Q(1)}
                and delete_cell(target, cut) == target_face
                and first_pp_naturality(lower),
                (cut, full_orders, source_face, target_face))
        selected_faces.append({
            "deleted_edge": list(cut),
            "face_root_orders": {
                str(site): multiplicities(lower)[site] for site in CHANGED
            },
            "target_decorated_face": [list(cell) for cell in target_face],
            "missing_site_fine_mark": missing,
            "doubled_site": doubled,
            "repeated_type": "P3+K2",
            "compressed_lower_word": physical_word,
            "required_physical_label": required_label,
            "marked_derived_coefficient": "1",
            "first_PP_commutator": 0,
        })
    return {
        "marked_parents": 90,
        "marked_branches": len(rows),
        "q23_q45_branch_deletions": {
            "q23": deletion_counts[Q23], "q45": deletion_counts[Q45]
        },
        "P3K2_deletions": {
            "q23": p3_counts[Q23], "q45": p3_counts[Q45]
        },
        "literal_operator": (
            "product over sites of E_site(old->new)^[incidence_at_site]"
        ),
        "source_realization": (
            "the corresponding coefficient of the endpoint Hasse/substitution "
            "coaction; orders are 0,1,2 in the retained multiplicity grade"
        ),
        "ordinary_order_one_extension_to_selected_branch": {
            "output_terms": len(ordinary),
            "desired_fully_recoloured_term_occurs": False,
            "reason": "site 7 is doubled and needs divided order two",
        },
        "selected_branch": {
            "parent": "01|23|45|67",
            "branch": "07|23|45|67",
            "missing": missing,
            "doubled": doubled,
            "branch_orders": {
                str(site): multiplicities(branch)[site] for site in CHANGED
            },
            "faces": selected_faces,
        },
        "divided_root_BC_commutator_rank": 0,
        "first_PP_naturality": True,
        "parent_matching_and_missing_doubled_labels_preserved": True,
    }


def protected_operation_gate(word_section, first_face, sigma) -> dict[str, object]:
    word_ledger, word_digest = word_section.audit()
    require(word_digest == word_section.EXPECTED_LEDGER_SHA256, word_digest)
    require(word_ledger["marked_collision_chain_section"]
            ["word_map_tensor_section_constructed"], word_ledger)

    first_ledger, first_digest = first_face.audit()
    require(first_digest == first_face.EXPECTED_LEDGER_SHA256, first_digest)
    explicit = first_ledger["explicit_M_N_q01_face"]
    simultaneous = first_ledger[
        "simultaneous_D4_P2_K_Eq_d_even_composition"]
    require(explicit["coefficient_label_match"] == [
        "q23 response face -> B1", "q45 response face -> B4"
    ] and explicit["required_physical_decorated_labels"] == [
        "0112/q23:21 -> B1", "0121/q45:12 -> B4"
    ] and not explicit["common_V_supplies_word_fine_operation_transport"]
            and simultaneous["full_row_order"]
                == ["private R", "root lower", "root Eq", "root ores"]
            and simultaneous["common_V_contribution"] == [1, 0, 0, 0]
            and simultaneous["exact_remaining_proper_face_debt"]
                == [0, -1, 0, 1],
            (explicit, simultaneous))

    sigma_ledger, sigma_digest = sigma.audit()
    require(sigma_digest == sigma.EXPECTED_LEDGER_SHA256, sigma_digest)
    residual = sigma_ledger["actual_augmented_residual"]
    dressing = sigma_ledger["root_word_physical_dressing"]
    require(residual["target_residual"] == 0
            and residual["root_reduced_Eq_residual"] == 0
            and residual["labelled_ordinary_residue_residual"]
                ["forced_class_mod_old_diagonal_Cartan_span"]
                    == "v=(B1+B4)/2"
            and dressing["required_hidden_faces_on_raw_Cplus"]
                == {"lower_private": "-E", "word_resolved_ores": "+E"},
            (residual, dressing))

    # The divided root acts on coefficient/form labels.  It preserves the
    # marked-derived operation summand.  The two physical P2 operation rows
    # are independent target summands until a source operation comparison is
    # supplied.
    marked23 = (Q(1), Q(0), Q(0), Q(0))
    marked45 = (Q(0), Q(1), Q(0), Q(0))
    physical23 = (Q(0), Q(0), Q(1), Q(0))
    physical45 = (Q(0), Q(0), Q(0), Q(1))
    p2_duals = ((Q(0), Q(0), Q(1), Q(0)),
                (Q(0), Q(0), Q(0), Q(1)))
    dot = lambda left, right: sum((a * b for a, b in
                                   zip(left, right, strict=True)), Q(0))
    require(all(dot(dual, column) == 0 for dual in p2_duals
                for column in (marked23, marked45))
            and dot(p2_duals[0], physical23) == 1
            and dot(p2_duals[1], physical45) == 1,
            "physical P2 operation quotient changed")
    return {
        "constructed_rank_two": (
            "the two marked-derived decorated coefficient/word/fine faces"
        ),
        "coefficient_B_labels_already_source_provenant": ["B1", "B4"],
        "not_yet_constructed_rank_two": (
            "the underived physical P2/B1,B4 operation landing"
        ),
        "operation_quotient_coordinates": [
            "marked_Dq23", "marked_Dq45", "physical_P2_B1",
            "physical_P2_B4"
        ],
        "operation_residual_rank": 2,
        "normalized_operation_duals": [list(map(int, value))
                                         for value in p2_duals],
        "protected_readout_table": {
            "parent_matching": "preserved termwise; augmentation one",
            "fine_repeated": (
                "missing=1, doubled=7, deleted q edge and P3+K2 retained"
            ),
            "q": "q23:21 and q45:12 marked proper faces present",
            "target": "zero on the six-site restrictions",
            "root_reduced_Eq": "formal target/Eq cone residual zero",
            "complete_Eq": "not supplied by the divided-root map",
            "ordinary_residue": (
                "aggregate dq residue zero, but labelled v=(B1+B4)/2 and "
                "word-resolved +E face are not evaluated"
            ),
            "anchor": (
                "parent augmentation is monic; rooted physical anchor needs "
                "the operation landing"
            ),
            "W": "zero in the nearest pinned physical dressing",
            "ridge": "no divided-root P2 ridge value is constructed",
        },
        "required_full_pointed_section_boundary": {
            "row_order": simultaneous["full_row_order"],
            "value": [1, -1, 0, 1],
        },
        "unverified_faces_after_coefficient_BC": {
            "root_lower": "-E", "root_Eq": "0",
            "root_word_resolved_ores": "+E"
        },
        "simultaneous_augmented_system_closes_after_that_section":
            simultaneous["simultaneous_system_closes_if_label_map_is_supplied"],
        "physical_underived_P2_map_constructed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    word_section = load(
        "computations/verify_h3_six_root_marked_collision_word_section.py",
        "qface_word_section",
    )
    bc = load(
        "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py",
        "qface_bc",
    )
    first_face = load(
        "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py",
        "qface_first_face",
    )
    sigma = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "qface_sigma",
    )
    ledger = {
        "theorem": (
            "q23/q45 deletion commutes with the six-root word action after "
            "endpoint omission, and on collision branches after the unique "
            "multiplicity-adapted divided-Hasse correction. This constructs "
            "both marked-derived decorated lower word/fine faces, but not "
            "their underived physical P2 operation landing or protected "
            "(-E,+E) completion"
        ),
        "pins": PINS,
        "squarefree_root_deletion_commutators":
            perfect_matching_restriction_audit(word_section),
        "marked_branch_divided_Hasse_BC":
            divided_branch_restriction_audit(bc),
        "physical_operation_and_protected_gate":
            protected_operation_gate(word_section, first_face, sigma),
        "verdict": (
            "Positive at the derived coefficient level: the naive root "
            "restriction has rank-12 commutator on each direct-free q face, "
            "while omitting deleted endpoint roots makes it strict. The "
            "selected repeated branch additionally forces divided order two "
            "at site 7; the multiplicity-adapted Hasse operator then commutes "
            "on every q23/q45 branch deletion and first PP face, giving the "
            "0112 and 0121 marked-derived word/fine rows. Negative at the "
            "underived physical interface: endpoint roots preserve the "
            "marked-derived operation idempotent, and the existing B1/B4 "
            "coefficient labels do not by themselves define the P2 operation "
            "map. The exact remaining pointed boundary is "
            "(private R,root lower,root Eq,root ores)=(1,-1,0,1); target and "
            "root-Eq close formally, but complete Eq, labelled ores and ridge "
            "are not values of the divided-root map."
        ),
        "scope": (
            "exact rational h=3 calculation on all 105 squarefree matching "
            "terms, all 90 direct-free parents, all 540 marked collision "
            "branches, all q23/q45 deletions and the selected first PP faces; "
            "literal parent/missing/doubled/word/colour labels and pinned "
            "target/Eq/ores/q/anchor/W/ridge scope. This is not an underived "
            "AugP2 comparison and not an absolute Eq filler."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("six-root q-face ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "squarefree", "branch", "protected"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 six-root q-face restriction commutator:",
              arguments.mode, "PASS")
        print("ordinary direct-free q-face commutator ranks: 15, 12")
        print("divided-Hasse marked BC commutator rank: 0")
        print("marked-derived 0112/0121 word-fine rows: CONSTRUCTED")
        print("underived physical P2 operation rows: OPEN (rank 2)")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
