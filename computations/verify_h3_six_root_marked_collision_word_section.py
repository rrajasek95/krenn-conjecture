#!/usr/bin/env python3
"""Construct the derived response-to-cap word section at h=3.

The response word 11110000 and the cap word 01211222 differ at six sites.
The product of the six corresponding local endpoint root operators sends
each perfect-matching monomial of the response coefficient to the monomial
with the same matching in the cap coefficient, with coefficient one.  Both
words are mixed, so the operator is target-safe.

Tensor this literal word map with the endpoint-even section of the marked
collision Beck--Chevalley resolution.  The result is an explicit chain map

    Delta^5(response word) -> Delta^5 x Delta^1(cap word)

over all 90 direct-free parent matchings.  This constructs the previously
missing *derived* operation/word section.  It does not yet construct the
underived P2 restriction of the cap q-faces; that is the next exact defect.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py":
        "a1e81eef9343bd2dda01b106acc202698cc12e93e7db3b55d45f5c6268779c33",
    "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py":
        "2e7a8640482bcde91241bde7b067131e46c0188cbf276c1c1a43243177ef3b7f",
}
EXPECTED_LEDGER_SHA256 = (
    "1c12231daa14798ede88268372b26cb03deafd9ae08dc492ea2e28cd92472d9f"
)

SITES = tuple(range(8))
RESPONSE_WORD = tuple(map(int, "11110000"))
CAP_WORD = tuple(map(int, "01211222"))
DIRECT_FREE_EDGE = (3, 6)
SELECTED_MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))


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


def decorated_monomial(word: tuple[int, ...], matching):
    return tuple(sorted(
        (left, right, word[left], word[right])
        for left, right in matching
    ))


def apply_site_root(monomial, site: int, old: int, new: int):
    """Apply one local endpoint matrix unit to a perfect-matching monomial."""
    outputs = []
    for position, cell in enumerate(monomial):
        left, right, left_colour, right_colour = cell
        changed = None
        if left == site and left_colour == old:
            changed = (left, right, new, right_colour)
        elif right == site and right_colour == old:
            changed = (left, right, left_colour, new)
        if changed is None:
            continue
        output = list(monomial)
        output[position] = changed
        outputs.append(tuple(sorted(output)))
    return tuple(outputs)


def apply_root_product(monomial):
    terms = {tuple(monomial): Q(1)}
    for site, (old, new) in enumerate(zip(RESPONSE_WORD, CAP_WORD, strict=True)):
        if old == new:
            continue
        following = {}
        for term, coefficient in terms.items():
            for output in apply_site_root(term, site, old, new):
                following[output] = following.get(output, Q(0)) + coefficient
        terms = {term: coefficient for term, coefficient in following.items()
                 if coefficient}
    return terms


def sparse_compose(left, right):
    columns = []
    for column in right:
        output = {}
        for middle, coefficient in column.items():
            for row, value in left[middle].items():
                output[row] = output.get(row, Q(0)) + coefficient * value
                if not output[row]:
                    output.pop(row)
        columns.append(output)
    return tuple(columns)


def word_operator_audit() -> dict[str, object]:
    matchings = tuple(perfect_matchings(SITES))
    require(len(matchings) == len(set(matchings)) == 105, len(matchings))
    changed_sites = tuple(
        site for site, values in enumerate(zip(RESPONSE_WORD, CAP_WORD,
                                                strict=True))
        if values[0] != values[1]
    )
    require(changed_sites == (0, 2, 4, 5, 6, 7), changed_sites)

    image = {}
    for matching in matchings:
        source = decorated_monomial(RESPONSE_WORD, matching)
        target = decorated_monomial(CAP_WORD, matching)
        expansion = apply_root_product(source)
        require(expansion == {target: Q(1)},
                ("root product is not termwise", matching, expansion, target))
        require(target not in image, ("word map not injective", target))
        image[target] = source
    require(len(image) == 105, len(image))

    direct_free = tuple(
        matching for matching in matchings if DIRECT_FREE_EDGE not in matching
    )
    require(len(direct_free) == 90, len(direct_free))
    selected_source = decorated_monomial(RESPONSE_WORD, SELECTED_MATCHING)
    selected_target = decorated_monomial(CAP_WORD, SELECTED_MATCHING)
    require(apply_root_product(selected_source) == {selected_target: Q(1)},
            (selected_source, selected_target))
    require(selected_source == (
        (0, 1, 1, 1), (2, 3, 1, 1),
        (4, 5, 0, 0), (6, 7, 0, 0),
    ) and selected_target == (
        (0, 1, 0, 1), (2, 3, 2, 1),
        (4, 5, 1, 2), (6, 7, 2, 2),
    ), (selected_source, selected_target))

    # The tensor target has nonzero entries only on constant words.  The
    # input letters required by the six roots contain both 0 and 1, so no
    # constant target word is in their domain.  Equivalently the source and
    # destination coefficient rows are both mixed target-zero rows.
    changed_input = {RESPONSE_WORD[site] for site in changed_sites}
    require(changed_input == {0, 1}
            and len(set(RESPONSE_WORD)) > 1
            and len(set(CAP_WORD)) > 1,
            changed_input)

    return {
        "response_word": "".join(map(str, RESPONSE_WORD)),
        "cap_word": "".join(map(str, CAP_WORD)),
        "changed_sites": list(changed_sites),
        "operator": [
            f"E_site{site}({RESPONSE_WORD[site]}->{CAP_WORD[site]})"
            for site in changed_sites
        ],
        "perfect_matching_terms_checked": len(matchings),
        "direct_free_parent_terms": len(direct_free),
        "same_matching_index_bijection": True,
        "coefficient_on_every_term": "1",
        "selected_source_occurrence": [list(cell) for cell in selected_source],
        "selected_cap_occurrence": [list(cell) for cell in selected_target],
        "centered_90_parent_vector_is_preserved": True,
        "target_safe": True,
        "target_reason": (
            "the six root input letters contain both 0 and 1, and both "
            "endpoint coefficient words are mixed GHZ-zero rows"
        ),
    }


def marked_chain_section_audit(bc) -> dict[str, object]:
    bases, cap_boundaries = bc.product_simplex_complex(6, 2)
    response_bases = tuple(bc.simplex_basis(6, degree)
                           for degree in range(6))
    response_boundaries = tuple(bc.simplex_boundary(6, degree)
                                for degree in range(1, 6))
    sections = []
    for degree in range(6):
        target_index = {cell: index for index, cell in enumerate(bases[degree])}
        columns = []
        for face in response_bases[degree]:
            columns.append({
                target_index[(degree, face, 0, (0,))]: Q(1, 2),
                target_index[(degree, face, 0, (1,))]: Q(1, 2),
            })
        sections.append(tuple(columns))

    for degree in range(1, 6):
        left = sparse_compose(cap_boundaries[degree - 1], sections[degree])
        right = sparse_compose(sections[degree - 1],
                               response_boundaries[degree - 1])
        require(left == right, ("marked section is not a chain map", degree,
                                left, right))

    # Both endpoint-labelled vertices augment to the same parent.  The
    # Reynolds half-sum is therefore monic on H0.
    for column in sections[0]:
        require(sum(column.values(), Q(0)) == 1, column)

    return {
        "response_fibre": "Delta5",
        "marked_cap_fibre": "Delta5 x Delta1",
        "section": "id_Delta5 tensor (endpoint_0+endpoint_1)/2",
        "degrees_checked": list(range(6)),
        "chain_map": True,
        "parent_augmentation_monic": True,
        "root_parent_fine_labels_retained": True,
        "word_map_tensor_section_constructed": True,
        "global_parent_copies": 90,
    }


def downstream_scope_audit(direct) -> dict[str, object]:
    ledger, digest = direct.audit()
    require(digest == direct.EXPECTED_LEDGER_SHA256, digest)
    direct_N = ledger["direct_derived_N_in_PAComp"]
    failure = direct_N["first_downstream_map_using_more_than_parent_augmentation"]
    require(failure["required_word_quotient_rank"] == 2
            and failure["old_derived_N_word_hit_rank"] == 0,
            failure)
    dq = direct_N["first_product_rule_after_granting_that_map"]
    require(dq["detector_value"] == "35/72", dq)
    return {
        "what_is_new": (
            "the six-root word operator tensored with the marked collision "
            "section supplies the derived response-to-cap Hom/word edge"
        ),
        "what_is_not_claimed": (
            "an underived AugP2/P2 restriction or an absolute Eq filler"
        ),
        "next_map": failure["map"],
        "old_rank": failure["old_derived_N_word_hit_rank"],
        "required_rank": failure["required_word_quotient_rank"],
        "next_forced_dq_detector": dq["detector_value"],
        "hidden_faces": direct_N["first_protected_use_of_cap_modulo_Eq"]
            ["hidden_proper_faces"],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    bc = load(
        "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py",
        "six_root_marked_bc",
    )
    direct = load(
        "computations/verify_h3_derived_marked_cap_direct_pacomp_schreyer_eq_gate.py",
        "six_root_direct_N",
    )
    bc_ledger, bc_digest = bc.audit()
    require(bc_digest == bc.EXPECTED_LEDGER_SHA256
            and bc_ledger["finite_collision_groupoid"]
                ["marked_square_is_strictly_Cartesian"],
            bc_digest)
    ledger = {
        "theorem": (
            "the six-site root product gives a target-safe termwise word "
            "bijection on the 90 parent matchings; tensoring it with the "
            "endpoint-even marked collision section constructs the missing "
            "derived response-to-cap operation/word section.  The next "
            "unconstructed map is the occurrence-local P2 restriction of "
            "the q23/q45 faces"
        ),
        "pins": PINS,
        "six_root_word_operator": word_operator_audit(),
        "marked_collision_chain_section": marked_chain_section_audit(bc),
        "downstream_scope": downstream_scope_audit(direct),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "word", "chain", "scope"),
                        default="all")
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
        print("h=3 six-root marked collision word section: PASS")
        print("mode", arguments.mode)
        print("ledger_sha256", digest)
        print("derived operation/word section: CONSTRUCTED")
        print("next physical map: q23/q45 P2 restriction, rank 0 -> 2")


if __name__ == "__main__":
    main()
