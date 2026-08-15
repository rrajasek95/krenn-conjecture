#!/usr/bin/env python3
"""Audit the literal divided-root lift on marked collision deletion faces.

The six ordinary site roots map a perfect-matching coefficient from word
11110000 to word 01211222.  A collision branch is not a perfect matching:
one site is missing and another is doubled.  Its literal lift must therefore
use divided root order equal to the occurrence multiplicity at every changed
site.  This checker verifies that trigger-dependent lift on all 540 marked
branches and on their complete Boolean deletion cubes.

For the canonical branch 07|23|45|67, the two kept-factor deletions q23 and
q45 land termwise in the decorated cap P3+K2 faces underlying
0112/q23:21 and 0121/q45:12.  The same map commutes with the universal
first-principal-parts differential.  This constructs the marked-derived
coefficient/word/fine P2 restriction.  It does not construct the separate
physical occurrence-to-B1/B4 augmentation, identify the protected B and Eq
copies, or supply the hidden lower/ores correction.
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
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
}
EXPECTED_LEDGER_SHA256 = (
    "6c61945946ddf7e8935c4ee62cd90a32c212adcc4835e203b2a62a301b66d559"
)

SITES = tuple(range(8))
RESPONSE_WORD = tuple(map(int, "11110000"))
CAP_WORD = tuple(map(int, "01211222"))
CHANGED = tuple(site for site in SITES
                if RESPONSE_WORD[site] != CAP_WORD[site])
DIRECT_FREE_EDGE = (3, 6)
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


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def decorated(word: tuple[int, ...], edges):
    return tuple(sorted((left, right, word[left], word[right], False)
                        for left, right in edges))


def multiplicities(edges) -> tuple[int, ...]:
    counts = Counter(site for edge in edges for site in edge)
    return tuple(counts[site] for site in SITES)


def apply_divided_site(term, site: int, old: int, new: int, order: int):
    eligible = []
    for position, (left, right, left_colour, right_colour, is_d) in enumerate(term):
        if left == site and left_colour == old:
            eligible.append((position, "left"))
        elif right == site and right_colour == old:
            eligible.append((position, "right"))
    outputs = Counter()
    for chosen in combinations(eligible, order):
        output = list(term)
        for position, side in chosen:
            left, right, left_colour, right_colour, is_d = output[position]
            if side == "left":
                output[position] = (left, right, new, right_colour, is_d)
            else:
                output[position] = (left, right, left_colour, new, is_d)
        outputs[tuple(sorted(output))] += Q(1)
    return {key: value for key, value in outputs.items() if value}


def compose_operator(terms, site: int, old: int, new: int, order: int):
    output = Counter()
    for term, coefficient in terms.items():
        for image, value in apply_divided_site(
                term, site, old, new, order).items():
            output[image] += coefficient * value
    return {key: value for key, value in output.items() if value}


def divided_root_lift(term, edges):
    terms = {term: Q(1)}
    counts = multiplicities(edges)
    for site in CHANGED:
        terms = compose_operator(
            terms, site, RESPONSE_WORD[site], CAP_WORD[site], counts[site]
        )
    return terms


def ordinary_fixed_root_lift(term):
    """The tempting but incorrect order-one root product on a branch."""
    terms = {term: Q(1)}
    for site in CHANGED:
        terms = compose_operator(
            terms, site, RESPONSE_WORD[site], CAP_WORD[site], 1
        )
    return terms


def mark_d(term, edge):
    output = []
    for cell in term:
        left, right, left_colour, right_colour, _is_d = cell
        output.append((left, right, left_colour, right_colour,
                       (left, right) == edge))
    return tuple(sorted(output))


def exterior_derivative(term, edges):
    return {mark_d(term, edge): Q(1) for edge in edges}


def apply_lift_to_sum(forms, edges):
    answer = Counter()
    for form, coefficient in forms.items():
        for image, value in divided_root_lift(form, edges).items():
            answer[image] += coefficient * value
    return {key: value for key, value in answer.items() if value}


def branches():
    parents = tuple(matching for matching in perfect_matchings(SITES)
                    if DIRECT_FREE_EDGE not in matching)
    require(len(parents) == 90, len(parents))
    output = []
    for parent_index, parent in enumerate(parents):
        source_edge = next(edge for edge in parent if 0 in edge)
        missing = source_edge[1]
        for doubled in range(1, 8):
            if doubled == missing:
                continue
            branch = tuple(sorted(
                (set(parent) - {source_edge}) | {(0, doubled)}
            ))
            output.append((parent_index, parent, missing, doubled, branch))
    require(len(output) == 540 and len({entry[-1] for entry in output}) == 540,
            len(output))
    return tuple(output)


def replace_zero_edge(edges, old_edge, new_edge):
    require(old_edge in edges and new_edge not in edges,
            (edges, old_edge, new_edge))
    return tuple(sorted((set(edges) - {old_edge}) | {new_edge}))


def full_cube_audit() -> dict[str, object]:
    branch_rows = branches()
    subset_count = 0
    deletion_square_count = 0
    jet_count = 0
    missing_histogram = Counter()
    doubled_histogram = Counter()
    ordinary_outcomes = Counter()
    trigger_squares = 0
    for _parent_index, _parent, missing, doubled, branch in branch_rows:
        missing_histogram[missing] += 1
        doubled_histogram[doubled] += 1
        source_top = decorated(RESPONSE_WORD, branch)
        target_top = decorated(CAP_WORD, branch)
        ordinary = ordinary_fixed_root_lift(source_top)
        if ordinary == {target_top: Q(1)}:
            ordinary_outcomes["correct"] += 1
        elif not ordinary:
            ordinary_outcomes["zero"] += 1
        else:
            ordinary_outcomes["nonzero_wrong"] += 1

        # The parent-to-branch trigger square is literal.  Replacing the
        # site-0 edge before the multiplicity-order roots gives the same
        # fully cap-decorated branch as first changing the parent word and
        # then applying the corresponding cap trigger.
        old_edge = (0, missing)
        new_edge = (0, doubled)
        require(replace_zero_edge(_parent, old_edge, new_edge) == branch,
                (_parent, old_edge, new_edge, branch))
        source_parent = decorated(RESPONSE_WORD, _parent)
        target_parent = decorated(CAP_WORD, _parent)
        require(divided_root_lift(source_parent, _parent)
                == {target_parent: Q(1)}
                and divided_root_lift(source_top, branch)
                == {target_top: Q(1)},
                ("trigger square", _parent, branch))
        trigger_squares += 1
        for size in range(5):
            for retained in combinations(branch, size):
                retained = tuple(sorted(retained))
                source = decorated(RESPONSE_WORD, retained)
                target = decorated(CAP_WORD, retained)
                image = divided_root_lift(source, retained)
                require(image == {target: Q(1)},
                        ("divided lift", missing, doubled, retained, image,
                         target))
                subset_count += 1

                # The tensor/root lift commutes with the universal first PP
                # differential when the distinguished dx factor carries the
                # same endpoint colour action.
                source_d = exterior_derivative(source, retained)
                target_d = exterior_derivative(target, retained)
                require(apply_lift_to_sum(source_d, retained) == target_d,
                        ("jet naturality", missing, doubled, retained))
                jet_count += len(retained)

                for removed in retained:
                    lower = tuple(edge for edge in retained if edge != removed)
                    source_lower = decorated(RESPONSE_WORD, lower)
                    target_lower = decorated(CAP_WORD, lower)
                    require(divided_root_lift(source_lower, lower)
                            == {target_lower: Q(1)},
                            ("deletion square", retained, removed))
                    deletion_square_count += 1

    require(subset_count == 540 * 16
            and deletion_square_count == 540 * 32
            and jet_count == 540 * 32,
            (subset_count, deletion_square_count, jet_count))
    return {
        "marked_branches": len(branch_rows),
        "parent_to_branch_trigger_squares_checked": trigger_squares,
        "boolean_subsets_checked": subset_count,
        "deletion_squares_checked": deletion_square_count,
        "first_PP_terms_checked": jet_count,
        "missing_site_histogram": dict(sorted(missing_histogram.items())),
        "doubled_site_histogram": dict(sorted(doubled_histogram.items())),
        "ordinary_order_one_branch_outcomes": dict(ordinary_outcomes),
        "operator_at_changed_site": (
            "divided root E_site(old->new)^[occurrence multiplicity]"
        ),
        "coefficient_on_every_retained_face": "1",
        "complete_boolean_deletion_naturality": True,
        "parent_trigger_naturality": True,
        "first_principal_parts_naturality": True,
    }


def selected_p2_audit(bc, first_face, private) -> dict[str, object]:
    bc_ledger, bc_digest = bc.audit()
    require(bc_digest == bc.EXPECTED_LEDGER_SHA256
            and bc_ledger["finite_collision_groupoid"]
                ["marked_square_is_strictly_Cartesian"], bc_digest)
    first_ledger, first_digest = first_face.audit()
    require(first_digest == first_face.EXPECTED_LEDGER_SHA256, first_digest)
    face = first_ledger["explicit_M_N_q01_face"]
    require(face["required_physical_decorated_labels"] == [
        "0112/q23:21 -> B1", "0121/q45:12 -> B4"
    ] and face["common_V_supplies_top_and_undecorated_proper_faces"], face)

    selected = next(entry for entry in branches()
                    if entry[1] == SELECTED_PARENT
                    and entry[-1] == SELECTED_BRANCH)
    _parent_index, _parent, missing, doubled, branch = selected
    require((missing, doubled) == (1, 7), (missing, doubled))
    source_branch = decorated(RESPONSE_WORD, branch)
    target_branch = decorated(CAP_WORD, branch)
    require(divided_root_lift(source_branch, branch)
            == {target_branch: Q(1)}, target_branch)

    q23 = (2, 3)
    q45 = (4, 5)
    lower23 = tuple(edge for edge in branch if edge != q23)
    lower45 = tuple(edge for edge in branch if edge != q45)
    source23, target23 = (decorated(RESPONSE_WORD, lower23),
                          decorated(CAP_WORD, lower23))
    source45, target45 = (decorated(RESPONSE_WORD, lower45),
                          decorated(CAP_WORD, lower45))
    require(divided_root_lift(source23, lower23) == {target23: Q(1)}
            and divided_root_lift(source45, lower45) == {target45: Q(1)},
            (source23, target23, source45, target45))

    expected23 = tuple(sorted((
        (0, 7, 0, 2, False),
        (4, 5, 1, 2, False),
        (6, 7, 2, 2, False),
    )))
    expected45 = tuple(sorted((
        (0, 7, 0, 2, False),
        (2, 3, 2, 1, False),
        (6, 7, 2, 2, False),
    )))
    require(target23 == expected23 and target45 == expected45,
            (target23, target45))
    # The marked cap object is (cofactor, original missing site).  The mark
    # and the other two absent sites recover the deleted edge, so these are
    # literal objects of the strict marked BC square rather than an
    # unmarked cofactor identification.
    for lower, removed in ((lower23, q23), (lower45, q45)):
        occupied = {site for edge in lower for site in edge}
        absent = set(SITES) - occupied
        require(absent == {missing, *removed}
                and tuple(sorted(absent - {missing})) == removed,
                (lower, removed, absent))

    private_ledger, private_digest = private.audit()
    require(private_digest == private.EXPECTED_LEDGER_SHA256, private_digest)
    reinsertion = private_ledger["q23_reinsertion"]
    require(reinsertion["forced_repair_dq23_private_detector"] == "35/72"
            and reinsertion["ordinary_residue_aggregate"] == 0,
            reinsertion)
    return {
        "parent": "01|23|45|67",
        "branch": "07|23|45|67",
        "missing_site": missing,
        "doubled_site": doubled,
        "branch_root_orders_on_changed_sites": {
            str(site): multiplicities(branch)[site] for site in CHANGED
        },
        "delete_q23": {
            "source_decorated_face": [list(cell) for cell in source23],
            "target_decorated_face": [list(cell) for cell in target23],
            "marked_derived_face": "0112/q23:21",
            "required_augmented_label_not_yet_constructed": "B1",
            "coefficient": "1",
        },
        "delete_q45": {
            "source_decorated_face": [list(cell) for cell in source45],
            "target_decorated_face": [list(cell) for cell in target45],
            "marked_derived_face": "0121/q45:12",
            "required_augmented_label_not_yet_constructed": "B4",
            "coefficient": "1",
        },
        "marked_derived_word_fine_repeated_landing_rank": 2,
        "physical_B1_B4_augmentation_constructed": False,
        "strict_marked_BC_objects": True,
        "first_PP_transport": "d commutes with the divided endpoint action",
        "forced_dq23_detector_after_transport": "35/72",
        "forced_dq23_ordinary_residue": "0",
    }


def scope_audit() -> dict[str, object]:
    return {
        "constructed": (
            "the source-derived marked divided-root map on every collision "
            "branch, every deletion face, and the universal first PP face; "
            "in particular both decorated q23/q45 marked-derived P2 "
            "word/fine landings"
        ),
        "correction_to_ordinary_root_claim": (
            "ordinary order-one roots suffice only on perfect matchings; "
            "a missing site requires order zero and a doubled site order two"
        ),
        "not_constructed": [
            "an underived identification of the marked totalization N with r0",
            "the physical occurrence-to-B1/B4 augmentation",
            "the protected B-only versus tied B=Eq readout",
            "the hidden (lower,word-ores)=(-E,+E) correction",
            "an intrinsic Fredholm pairing of the reduced Eq class",
        ],
        "next_exact_boundary": (
            "augment the divided-root P2 map by the physical B1/B4, B/Eq "
            "and labelled ordinary-residue totalization; the coefficient "
            "dq face is present, but its protected cap readout is not"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    first_face = load(
        "computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py",
        "divroot_first_face",
    )
    private = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "divroot_private",
    )
    bc = load(
        "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py",
        "divroot_marked_bc",
    )
    ledger = {
        "theorem": (
            "trigger-dependent divided roots give a literal marked "
            "collision deletion/PP chain map and construct the two derived "
            "decorated marked-derived P2 landings; the physical B1/B4 and "
            "protected augmented readouts remain"
        ),
        "pins": PINS,
        "complete_marked_cube": full_cube_audit(),
        "selected_q23_q45_P2": selected_p2_audit(
            bc, first_face, private
        ),
        "scope": scope_audit(),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"ledger": ledger, "ledger_sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h=3 divided-root marked deletion/P2 naturality: PASS")
        print("ledger_sha256", digest)
        print("marked-derived P2 word/fine landing: CONSTRUCTED")
        print("physical B1/B4/B/Eq/ores landing: OPEN")


if __name__ == "__main__":
    main()
