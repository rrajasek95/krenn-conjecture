#!/usr/bin/env python3
"""Restrict the six-root marked word section to the two physical P2 cuts.

For a matching containing 23 (respectively 45), deletion commutes exactly
with the six-root word map after omitting the roots at the deleted endpoints.
The two lower maps land in the independent words 0112/q23:21 and
0121/q45:12.  Reinsertion satisfies the same transported square.

Tensoring these monic termwise maps with the marked parent section supplies
the pointed occurrence sections required by the already constructed h=2
Hasse/cobar square.  The q23 Leibniz rule then carries the exact private
coefficient with detector 35/72; the q45 face is its sigma mate.  The result
is derived/marked: the complete B/Eq hidden (-E,+E) landing remains open.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_six_root_marked_collision_word_section.py":
        "d0da0f1473fc1032416c3758ffc932531ac71698c2370ee67224baedd2e13f95",
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py":
        "2e7a8640482bcde91241bde7b067131e46c0188cbf276c1c1a43243177ef3b7f",
}
EXPECTED_LEDGER_SHA256 = "4b8fc421160619bdf23fe574b4e27473edaf077f79b6ebf7aee7473526a00ae3"

CUTS = ((2, 3), (4, 5))


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


def apply_root_subset(root, monomial, sites):
    terms = {tuple(monomial): Q(1)}
    for site in sites:
        old = root.RESPONSE_WORD[site]
        new = root.CAP_WORD[site]
        require(old != new, (site, old, new))
        following = Counter()
        for term, coefficient in terms.items():
            for output in root.apply_site_root(term, site, old, new):
                following[output] += coefficient
        terms = {term: coefficient for term, coefficient in following.items()
                 if coefficient}
    return terms


def cut_cell(word, cut):
    left, right = cut
    return left, right, word[left], word[right]


def remove_cell(monomial, cell):
    require(cell in monomial, ("cell absent", cell, monomial))
    output = list(monomial)
    output.remove(cell)
    return tuple(sorted(output))


def insert_cell(monomial, cell):
    require(cell not in monomial, ("cell already present", cell, monomial))
    return tuple(sorted(tuple(monomial) + (cell,)))


def target_value(word) -> int:
    return int(len(set(word)) == 1)


def multiplicities(edges):
    counts = Counter(site for edge in edges for site in edge)
    return tuple(counts[site] for site in range(8))


def apply_divided_site(monomial, site: int, old: int, new: int, order: int):
    eligible = []
    for position, (left, right, left_colour, right_colour) in enumerate(monomial):
        if left == site and left_colour == old:
            eligible.append((position, 2))
        elif right == site and right_colour == old:
            eligible.append((position, 3))
    outputs = Counter()
    for chosen in combinations(eligible, order):
        output = [list(cell) for cell in monomial]
        for position, colour_position in chosen:
            output[position][colour_position] = new
        outputs[tuple(sorted(tuple(cell) for cell in output))] += Q(1)
    return {term: coefficient for term, coefficient in outputs.items()
            if coefficient}


def divided_root_lift(root, monomial, edges):
    terms = {tuple(monomial): Q(1)}
    counts = multiplicities(edges)
    changed = tuple(site for site, values in enumerate(zip(
        root.RESPONSE_WORD, root.CAP_WORD, strict=True))
                    if values[0] != values[1])
    for site in changed:
        following = Counter()
        for term, coefficient in terms.items():
            for output, value in apply_divided_site(
                    term, site, root.RESPONSE_WORD[site],
                    root.CAP_WORD[site], counts[site]).items():
                following[output] += coefficient * value
        terms = {term: coefficient for term, coefficient in following.items()
                 if coefficient}
    return terms


def sparse_rank(columns) -> int:
    basis = {}
    for original in columns:
        vector = {row: Q(value) for row, value in original.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                coefficient = vector[pivot]
                basis[pivot] = {row: value / coefficient
                                for row, value in vector.items()}
                break
            coefficient = vector[pivot]
            for row, value in basis[pivot].items():
                residue = vector.get(row, Q(0)) - coefficient * value
                if residue:
                    vector[row] = residue
                else:
                    vector.pop(row, None)
    return len(basis)


def trigger_dependent_divided_naturality_audit(root) -> dict[str, object]:
    """Check the parent-to-branch square omitted by an objectwise audit."""
    parents = tuple(matching for matching in root.perfect_matchings(root.SITES)
                    if root.DIRECT_FREE_EDGE not in matching)
    require(len(parents) == 90, len(parents))
    trigger_squares = 0
    marked_p3k2_faces = 0
    total_order_histogram = Counter()
    missing_histogram = Counter()
    doubled_histogram = Counter()
    for parent in parents:
        source_edge = next(edge for edge in parent if 0 in edge)
        missing = source_edge[1]
        for doubled in range(1, 8):
            if doubled == missing:
                continue
            inserted = (0, doubled)
            branch = tuple(sorted(
                (set(parent) - {source_edge}) | {inserted}
            ))
            source_parent = root.decorated_monomial(root.RESPONSE_WORD, parent)
            target_parent = root.decorated_monomial(root.CAP_WORD, parent)
            source_branch = root.decorated_monomial(root.RESPONSE_WORD, branch)
            target_branch = root.decorated_monomial(root.CAP_WORD, branch)

            require(divided_root_lift(root, source_parent, parent)
                    == {target_parent: Q(1)}
                    and divided_root_lift(root, source_branch, branch)
                    == {target_branch: Q(1)},
                    (parent, missing, doubled, branch))

            source_removed = cut_cell(root.RESPONSE_WORD, source_edge)
            source_inserted = cut_cell(root.RESPONSE_WORD, inserted)
            target_removed = cut_cell(root.CAP_WORD, source_edge)
            target_inserted = cut_cell(root.CAP_WORD, inserted)
            require(insert_cell(remove_cell(source_parent, source_removed),
                                source_inserted) == source_branch
                    and insert_cell(remove_cell(target_parent, target_removed),
                                    target_inserted) == target_branch,
                    ("trigger replacement", parent, missing, doubled))
            trigger_squares += 1
            missing_histogram[missing] += 1
            doubled_histogram[doubled] += 1
            counts = multiplicities(branch)
            total_order_histogram[sum(
                counts[site] for site in range(8)
                if root.RESPONSE_WORD[site] != root.CAP_WORD[site]
            )] += 1

            for removed in branch:
                cofactor = tuple(edge for edge in branch if edge != removed)
                degree = Counter(site for edge in cofactor for site in edge)
                profile = tuple(sorted(degree.values(), reverse=True))
                if profile != (2, 1, 1, 1, 1):
                    continue
                source_cofactor = root.decorated_monomial(
                    root.RESPONSE_WORD, cofactor)
                target_cofactor = root.decorated_monomial(
                    root.CAP_WORD, cofactor)
                require(divided_root_lift(root, source_cofactor, cofactor)
                        == {target_cofactor: Q(1)},
                        ("marked P3K2 deletion", branch, removed))
                marked_p3k2_faces += 1

    require(trigger_squares == 540 and marked_p3k2_faces == 1080
            and sum(total_order_histogram.values()) == 540,
            (trigger_squares, marked_p3k2_faces, total_order_histogram))
    return {
        "parents": len(parents),
        "parent_to_collision_trigger_squares": trigger_squares,
        "marked_P3K2_deletion_faces": marked_p3k2_faces,
        "missing_site_histogram": dict(sorted(missing_histogram.items())),
        "doubled_site_histogram": dict(sorted(doubled_histogram.items())),
        "branch_total_divided_root_order_histogram":
            dict(sorted(total_order_histogram.items())),
        "branch_component": (
            "at each changed site use divided-root order equal to its "
            "occurrence multiplicity (zero if missing, two if doubled)"
        ),
        "literal_trigger_identity": (
            "Phi_branch I_(0j)^r D_(0i)^r = "
            "I_(0j)^c D_(0i)^c Phi_parent"
        ),
        "trigger_commutator_on_every_parent_branch": 0,
        "coefficient_on_every_branch_and_marked_face": 1,
        "why_this_is_stronger_than_objectwise_deletion": (
            "the variable divided order is compatible with the Delta5 "
            "parent-to-trigger differential, so the family is one natural "
            "transformation rather than unrelated recolourings"
        ),
    }


def restriction_reinsertion_audit(root) -> dict[str, object]:
    changed = tuple(site for site, values in enumerate(zip(
        root.RESPONSE_WORD, root.CAP_WORD, strict=True))
                    if values[0] != values[1])
    require(changed == (0, 2, 4, 5, 6, 7), changed)
    matchings = tuple(root.perfect_matchings(root.SITES))

    records = []
    word_columns = []
    for cut_index, cut in enumerate(CUTS):
        source_cell = cut_cell(root.RESPONSE_WORD, cut)
        target_cell = cut_cell(root.CAP_WORD, cut)
        lower_roots = tuple(site for site in changed if site not in cut)
        containing = tuple(matching for matching in matchings if cut in matching)
        direct_free = tuple(matching for matching in containing
                            if root.DIRECT_FREE_EDGE not in matching)
        require(len(containing) == 15, (cut, len(containing)))

        for matching in containing:
            source = root.decorated_monomial(root.RESPONSE_WORD, matching)
            target = root.decorated_monomial(root.CAP_WORD, matching)
            full = root.apply_root_product(source)
            require(full == {target: Q(1)}, (cut, matching, full))

            source_cofactor = remove_cell(source, source_cell)
            target_cofactor = remove_cell(target, target_cell)
            lower = apply_root_subset(root, source_cofactor, lower_roots)
            require(lower == {target_cofactor: Q(1)},
                    ("restriction/root commutator", cut, matching, lower,
                     target_cofactor))
            require(remove_cell(next(iter(full)), target_cell)
                    == next(iter(lower)),
                    ("restriction square", cut, matching))

            reinserted_source = insert_cell(source_cofactor, source_cell)
            require(reinserted_source == source, (cut, matching))
            reinserted_target = {
                insert_cell(term, target_cell): coefficient
                for term, coefficient in lower.items()
            }
            require(root.apply_root_product(reinserted_source)
                    == reinserted_target,
                    ("reinsertion/root commutator", cut, matching))

        remaining = tuple(site for site in root.SITES if site not in cut)
        lower_source = "".join(str(root.RESPONSE_WORD[site])
                               for site in remaining)
        lower_target = "".join(str(root.CAP_WORD[site])
                               for site in remaining)
        core = tuple(site for site in range(6) if site not in cut)
        core_target = "".join(str(root.CAP_WORD[site]) for site in core)
        spectator_target = "".join(str(root.CAP_WORD[site])
                                    for site in (6, 7))
        word_columns.append({cut_index: Q(1)})
        records.append({
            "cut": "".join(map(str, cut)),
            "source_q_colour": "".join(map(str, source_cell[2:])),
            "target_q_colour": "".join(map(str, target_cell[2:])),
            "roots_omitted": [site for site in changed if site in cut],
            "lower_root_order": len(lower_roots),
            "matching_terms_checked": len(containing),
            "direct_free_terms": len(direct_free),
            "lower_source_word_with_spectators": lower_source,
            "lower_target_word_with_spectators": lower_target,
            "physical_core_target_word": core_target,
            "spectator_target_word": spectator_target,
            "restriction_commutator": 0,
            "reinsertion_commutator": 0,
            "termwise_coefficient": 1,
        })

    require(records[0]["physical_core_target_word"] == "0112"
            and records[0]["target_q_colour"] == "21"
            and records[1]["physical_core_target_word"] == "0121"
            and records[1]["target_q_colour"] == "12"
            and sparse_rank(tuple(word_columns)) == 2,
            records)

    # Every vertex of the full or either lower root cube is mixed.  Hence
    # neither the top map nor its P2 restriction exports a GHZ target face.
    cube_records = []
    for name, removed in (("top", ()), ("q23", (2, 3)), ("q45", (4, 5))):
        active_sites = tuple(site for site in root.SITES if site not in removed)
        roots = tuple(site for site in changed if site not in removed)
        values = []
        for mask in range(1 << len(roots)):
            word = list(root.RESPONSE_WORD)
            for position, site in enumerate(roots):
                if (mask >> position) & 1:
                    word[site] = root.CAP_WORD[site]
            restricted = tuple(word[site] for site in active_sites)
            values.append(target_value(restricted))
        require(not any(values), (name, values))
        cube_records.append({
            "cube": name,
            "vertices": len(values),
            "nonzero_GHZ_targets": sum(values),
        })

    return {
        "full_changed_sites": list(changed),
        "cuts": records,
        "two_cut_word_image_rank": sparse_rank(tuple(word_columns)),
        "old_diagonal_N_word_image_rank": 0,
        "required_and_constructed_P2_word_rank": 2,
        "target_census": cube_records,
        "target_commutator": 0,
        "literal_identities": [
            "R_23^21 Phi_6 = Phi_(omit 2) R_23^11",
            "Phi_6 I_23^11 = I_23^21 Phi_(omit 2)",
            "R_45^12 Phi_6 = Phi_(omit 4,5) R_45^00",
            "Phi_6 I_45^00 = I_45^12 Phi_(omit 4,5)",
        ],
    }


def pointed_occurrence_and_dq_audit(root, labelled, private, parity,
                                    sigma, direct) -> dict[str, object]:
    root_ledger, root_digest = root.audit()
    require(root_digest == root.EXPECTED_LEDGER_SHA256, root_digest)
    section = root_ledger["marked_collision_chain_section"]
    require(section["chain_map"] and section["parent_augmentation_monic"]
            and section["root_parent_fine_labels_retained"], section)

    labelled_ledger, labelled_digest = labelled.audit()
    require(labelled_digest == labelled.EXPECTED_LEDGER_SHA256,
            labelled_digest)
    provenance = labelled_ledger["source_provenance"]
    require(provenance["ambient_complete_PP_square"]
            and not provenance["occurrence_local_section_constructed"],
            provenance)

    parity_ledger = parity.endpoint_data()
    _occurrence, values, _lookup, _swap, _b, _s = parity_ledger
    require(len(values) == len(set(values)) == 12, len(values))

    private_ledger, private_digest = private.audit()
    require(private_digest == private.EXPECTED_LEDGER_SHA256, private_digest)
    debt = private_ledger["second_even_Bminus4_debt"]
    reinsertion = private_ledger["q23_reinsertion"]
    z_private = tuple(map(Q, debt["preimage"]))
    forced = tuple(map(Q, reinsertion["forced_repair_dq23_coefficient"]))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(len(z_private)))
    require(z_private == forced and sum(z_private, Q(0)) == 0
            and sum(a * b for a, b in zip(detector, z_private, strict=True))
                == Q(35, 72),
            (z_private, forced))

    sigma_ledger, sigma_digest = sigma.audit()
    require(sigma_digest == sigma.EXPECTED_LEDGER_SHA256, sigma_digest)
    require(sigma_ledger["minimal_target_Eq_cone"]["cut_symmetry"]
            == "sigma=(2 5)(3 4)",
            sigma_ledger["minimal_target_Eq_cone"])

    direct_ledger, direct_digest = direct.audit()
    require(direct_digest == direct.EXPECTED_LEDGER_SHA256, direct_digest)
    protected = direct_ledger["direct_derived_N_in_PAComp"][
        "first_protected_use_of_cap_modulo_Eq"]
    require(protected["hidden_proper_faces"] == {
        "lower_private": "-E", "word_resolved_ores": "+E"
    }, protected)

    return {
        "old_conditional_interface": (
            "one pointed occurrence section, natural for the two root PP "
            "operators and q23 reinsertion, supplies the full h2 square"
        ),
        "new_input_supplying_that_section": (
            "the monic marked parent section followed by the exact omitted-"
            "root q23/q45 restriction; occurrence, fine and reinsertion "
            "labels are retained termwise"
        ),
        "ordered_occurrence_sections": len(values),
        "pointed_occurrence_section_in_marked_derived_category": True,
        "private_linear_combination": [str(value) for value in z_private],
        "private_augmentation": 0,
        "q23_product_rule": reinsertion["product_rule"],
        "dq23_coefficient": [str(value) for value in forced],
        "dq23_detector": reinsertion[
            "forced_repair_dq23_private_detector"],
        "dq23_ordinary_residue": reinsertion["ordinary_residue_aggregate"],
        "q45_sigma_mate": {
            "symmetry": "sigma=(2 5)(3 4)",
            "detector_value": "35/72",
        },
        "newly_constructed_scope": [
            "both independent lower P2 word sections",
            "the occurrence-pointed two-direction Hasse/cobar squares",
            "q23/dq23 reinsertion and its q45/dq45 sigma mate",
        ],
        "not_constructed": [
            "underived projection of the marked cap top to r0",
            "the hidden lower/private -E face",
            "the hidden word-resolved ores +E face",
            "the complete B-only versus tied B=Eq landing",
        ],
        "next_exact_boundary": {
            "hidden_faces": protected["hidden_proper_faces"],
            "B_Eq_residual": protected["residual"],
            "integral_covector_value_on_required_B_only": 3,
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    root = load(
        "computations/verify_h3_six_root_marked_collision_word_section.py",
        "six_root_p2_root",
    )
    labelled = load(
        "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py",
        "six_root_p2_labelled",
    )
    private = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "six_root_p2_private",
    )
    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "six_root_p2_parity",
    )
    sigma = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "six_root_p2_sigma",
    )
    direct = load(
        "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py",
        "six_root_p2_direct",
    )
    ledger = {
        "theorem": (
            "the six-root marked collision section is natural for both "
            "physical q cuts: omitting roots at the deleted endpoints gives "
            "the independent 0112/q23:21 and 0121/q45:12 P2 sections.  "
            "Marked occurrence functoriality then realizes the private "
            "q/dq reinsertion pair with detector 35/72.  The first remaining "
            "landing is the protected hidden (-E,+E) B/Eq pair"
        ),
        "pins": PINS,
        "trigger_dependent_divided_naturality":
            trigger_dependent_divided_naturality_audit(root),
        "root_restriction_reinsertion":
            restriction_reinsertion_audit(root),
        "pointed_occurrence_and_dq": pointed_occurrence_and_dq_audit(
            root, labelled, private, parity, sigma, direct),
        "scope": (
            "exact rational marked-derived comparison on the canonical h=3 "
            "word and both physical cuts; all matching monomials containing "
            "each cut, all 12 ordered lower occurrences, target, first PP "
            "reinsertion and sigma covariance.  No underived r0 or absolute "
            "Eq cell is assumed"
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
        print("h=3 six-root marked collision P2 restriction: PASS")
        print("mode", arguments.mode)
        print("ledger_sha256", digest)
        print("P2 word rank: 2")
        print("dq23/dq45 detector: 35/72")
        print("next boundary: hidden (-E,+E) protected landing")


if __name__ == "__main__":
    main()
