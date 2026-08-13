#!/usr/bin/env python3
"""Construct the Cartan placement at a marked offdiagonal occurrence.

The ambient physical Cartan prism is already uniform.  This audit proves the
remaining elementary placement lemma: root at the endpoints of a marked
offdiagonal matching edge and transpose vertices from two distinct
complementary matching edges.  The four principal-boundary occurrences are
then distinct, so the critical projection is nonzero.  It also pins the
sharp boundary: augmented grade typing is inherited from the ambient prism,
while a dark component potential still needs the saturated complete-lift
promotion theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "notes/uniform-physical-cartan-source-prism.md":
        "7d1da671c9203c7d6080d988fef662caba6024b65227881e111285ad35ba8067",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_oo_zero_holonomy_schur_interference_reduction.py":
        "1e96bf98e997e55d2b050de6c56e7f597cd507737aefa6386296c44adab03631",
    "computations/verify_oo_dark_potential_source_promotion_counterguard.py":
        "76bdd6c8ce19cc466995b235bade9114d7d2779b74bfcd25eea703c2d1de3db2",
}
EXPECTED_LEDGER_SHA256 = (
    "0fd0ad4578c04ad3a6c68e96c47136efda46ca72ffa6aecaa71e06d1400cfffd"
)

COLOURS = (0, 1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def matching_edge_at(matching, site):
    found = tuple(pair for pair in matching if site in pair)
    require(len(found) == 1, ("matching lost unique incidence", site))
    return found[0]


def choose_transposition(matching, marked, forbidden=None):
    """Choose p,q on distinct complementary matching edges.

    If a direct-free edge is present, the transposition fixes it setwise.
    The proof has only the incidence alternatives encoded below; it does not
    inspect a critical-component support graph.
    """
    marked = edge(*marked)
    require(marked in matching, "the marked pair is not a matching edge")
    complement = tuple(pair for pair in matching if pair != marked)
    require(len(complement) >= 2, "placement needs order at least six")

    if forbidden is None:
        selected = (complement[0][0], complement[1][0])
    else:
        forbidden = edge(*forbidden)
        require(forbidden not in matching,
                "a direct-free matching used the forbidden edge")
        intersection = set(forbidden) & set(marked)
        require(len(intersection) <= 1,
                "a nonmatching forbidden pair cannot equal the marked edge")
        if not intersection:
            # The endpoints of a nonmatching pair lie on distinct matching
            # edges.  Swapping them fixes the forbidden pair setwise.
            selected = forbidden
        else:
            # Avoid the forbidden pair pointwise.  The outside forbidden
            # endpoint r has a mate p; take q on another complementary edge.
            root = next(iter(intersection))
            outside = next(site for site in forbidden if site != root)
            outside_edge = matching_edge_at(matching, outside)
            require(outside_edge in complement,
                    "the outside forbidden endpoint left the complement")
            first = next(site for site in outside_edge if site != outside)
            other_edge = next(pair for pair in complement
                              if pair != outside_edge)
            second = other_edge[0]
            selected = (first, second)

    first, second = selected
    require(first not in marked and second not in marked,
            "endpoint transposition met a root site")
    require(matching_edge_at(matching, first)
            != matching_edge_at(matching, second),
            "endpoint transposition used one matching edge")
    if forbidden is not None:
        image = edge(*(second if site == first else
                       first if site == second else site
                       for site in forbidden))
        require(image == forbidden,
                "endpoint transposition did not preserve the direct-free edge")
    return edge(first, second)


def transpose_site(site, transposition):
    first, second = transposition
    if site == first:
        return second
    if site == second:
        return first
    return site


def transpose_matching(matching, transposition):
    return tuple(sorted(edge(transpose_site(left, transposition),
                             transpose_site(right, transposition))
                        for left, right in matching))


def transpose_word(word, transposition):
    answer = list(word)
    first, second = transposition
    answer[first], answer[second] = answer[second], answer[first]
    return tuple(answer)


def weyl_word(word, roots, plane):
    """Signed Weyl a -> -b, b -> a on the selected colour plane."""
    first_colour, second_colour = plane
    answer = list(word)
    sign = 1
    for site in roots:
        if answer[site] == first_colour:
            answer[site] = second_colour
            sign *= -1
        elif answer[site] == second_colour:
            answer[site] = first_colour
        else:
            raise RuntimeError("a marked root site left its colour plane")
    return tuple(answer), sign


def principal_boundary(matching, word, roots, transposition, plane):
    """Return the labelled boundary (1-s)(w-1) at one occurrence."""
    changed_word, weyl_sign = weyl_word(word, roots, plane)
    swapped_matching = transpose_matching(matching, transposition)
    swapped_word = transpose_word(word, transposition)
    swapped_changed_word = transpose_word(changed_word, transposition)
    answer = Counter({
        (matching, changed_word): weyl_sign,
        (matching, word): -1,
        (swapped_matching, swapped_changed_word): -weyl_sign,
        (swapped_matching, swapped_word): 1,
    })
    answer = Counter({label: value for label, value in answer.items() if value})
    require(len(answer) == 4 and all(abs(value) == 1
                                     for value in answer.values()),
            "the four Cartan corners collided")
    require(answer[(matching, word)] == -1,
            "the marked critical coordinate disappeared")
    return answer


def audit_placement(matching, marked, forbidden, plane):
    roots = edge(*marked)
    word = [COLOURS[2]] * (2 * len(matching))
    word[roots[0]], word[roots[1]] = plane
    word = tuple(word)
    transposition = choose_transposition(matching, marked, forbidden)
    swapped = transpose_matching(matching, transposition)
    require(swapped != matching,
            "the cross-edge transposition fixed the marked matching")
    boundary = principal_boundary(
        matching, word, roots, transposition, plane)
    if forbidden is not None:
        forbidden = edge(*forbidden)
        require(forbidden not in swapped,
                "the placed Cartan corner left the direct-free chart")
    return {
        "roots": list(roots),
        "transposition": list(transposition),
        "corners": len(boundary),
        "marked_coefficient": boundary[(matching, word)],
    }


def audit_constructive_placement():
    records = []
    for size in (6, 8):
        matchings = tuple(perfect_matchings(range(size)))
        complete_placements = 0
        direct_free_placements = 0
        colour_planes = 0
        for matching in matchings:
            nonedges = tuple(pair for pair in combinations(range(size), 2)
                             if edge(*pair) not in matching)
            for marked in matching:
                for first_colour in COLOURS:
                    for second_colour in COLOURS:
                        if first_colour == second_colour:
                            continue
                        plane = (first_colour, second_colour)
                        audit_placement(matching, marked, None, plane)
                        complete_placements += 1
                        colour_planes += 1
                        for forbidden in nonedges:
                            audit_placement(matching, marked, forbidden, plane)
                            direct_free_placements += 1
        records.append({
            "order": size,
            "matchings": len(matchings),
            "ordered_offdiagonal_colour_planes": 6,
            "complete_placements": complete_placements,
            "direct_free_placements": direct_free_placements,
            "four_corners_distinct_in_every_placement": True,
            "marked_critical_coefficient": -1,
        })
    return {
        "finite_audits": records,
        "uniform_proof": (
            "root at the marked offdiagonal matching edge.  Since order is "
            "at least six, choose p,q on two distinct complementary matching "
            "edges.  Then s(mu)!=mu, while the Weyl word differs at the two "
            "roots, so the four (s,w)-corners are pairwise distinct"
        ),
        "direct_free_choice": (
            "if the forbidden edge is disjoint from the marked edge, swap "
            "its endpoints; otherwise avoid it pointwise by taking the mate "
            "of its outside endpoint and a vertex on another complement edge"
        ),
        "component_consequence": (
            "every critical occurrence containing a marked offdiagonal edge "
            "has a uniform physical Cartan prism whose critical projection "
            "is nonzero in that exact fine label"
        ),
    }


def audit_saturated_exit_interface():
    matching = ((0, 1), (2, 3), (4, 5))
    marked = (0, 1)
    plane = (0, 1)
    word = (0, 1, 2, 2, 2, 2)
    transposition = choose_transposition(matching, marked)
    boundary = principal_boundary(
        matching, word, marked, transposition, plane)
    marked_label = (matching, word)
    require(boundary[marked_label] == -1,
            "the saturated projection lost its marked label")
    remaining_labels = set(boundary) - {marked_label}
    require(len(remaining_labels) == 3,
            "the literal complement label count changed")
    return {
        "critical_projection_nonzero": True,
        "fine_label": {
            "word": list(word),
            "matching": [list(pair) for pair in matching],
            "coefficient": -1,
        },
        "saturation_alternative": (
            "retain every current word/tail/orientation/fine-grade label in "
            "pi_M.  A Cartan corner retained by pi_M is part of the critical "
            "connector; a nonzero corner outside that saturated label set is "
            "a literal word-changing or transposition exchange exit"
        ),
        "why_no_partial_source_is_needed": (
            "the physical chain is the complete ambient prism G; only its "
            "response vector g=pi_M G enters the Schur block, so projection "
            "need not itself be a source generator"
        ),
    }


def audit_dark_boundary(dark):
    type_split = dark.audit_smallest_type_split_counterguard()
    unsaturated = dark.audit_unsaturated_projection_counterguard()
    require(not type_split["same_row_kernel_available"]
            and not type_split["literal_outside_contaminant"],
            "the dark type-split counterguard changed")
    require(not unsaturated["projection_component_saturated"]
            and not unsaturated["typed_exit_valid"],
            "the unsaturated projection guard changed")
    return {
        "nonzero_charge_branch": (
            "ell^T(pi_M G)!=0 gives the Schur/Fitting unit"
        ),
        "dark_branch_identity": (
            "if ell^T(pi_M G)=0, solve My=pi_M G and form R=G-Cy; "
            "then pi_M R=0"
        ),
        "typed_exit_hypothesis": (
            "pi_M retains every current fine label and every nonzero "
            "complementary coordinate of R is a literal adjacency/exchange label"
        ),
        "zero_residual_hypothesis": (
            "R=0 still requires an occupied same-row scalar kernel or another "
            "independently anchor-safe move"
        ),
        "smallest_exact_obstruction": type_split["verdict"],
        "unsaturated_obstruction": unsaturated["verdict"],
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ambient = load(
        "computations/verify_uniform_physical_cartan_source_prism.py",
        "uniform_cartan_placement_ambient",
    )
    dark = load(
        "computations/verify_oo_dark_potential_source_promotion_counterguard.py",
        "uniform_cartan_placement_dark",
    )
    ambient_six = ambient.audit_order(6)
    require(ambient_six["endpoint_odd_target_defect"] == 0,
            "the uniform ambient target gate changed")
    ledger = {
        "theorem": "uniform marked-offdiagonal Cartan placement gate",
        "ambient_dependency": {
            "commit": "346d76a",
            "uniform_source_prism": True,
            "endpoint_odd_target_defect": 0,
            "augmented_typing_rule": (
                "placement retains every readout already defined on G; the "
                "canonical h=3 residue/ridge packet is inherited, while a "
                "new component grade still needs its augmented comparison map"
            ),
        },
        "constructive_placement": audit_constructive_placement(),
        "saturated_exit_interface": audit_saturated_exit_interface(),
        "dark_promotion_boundary": audit_dark_boundary(dark),
        "minimal_hypotheses": [
            "even order at least six",
            "a marked matching occurrence with distinct endpoint colours",
            "complete presentation, or one direct-free edge preserved by s",
            "fine-label-saturated component projection",
            "an augmented residue/ridge comparison in the chosen component grade",
        ],
        "frontier": (
            "root/transposition choice and nonzero critical incidence are "
            "closed.  The first remaining exact obstruction is augmented "
            "grade typing; after it, only the dark complete-lift residual "
            "R=G-Cy needs promotion to a typed exit or anchor-safe kernel move"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform Cartan placement ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("uniform marked-offdiagonal Cartan placement: CONSTRUCTED")
    print("critical projection: NONZERO in the exact fine label")
    print("ambient target/readouts: INHERITED, not reprojected")
    print("remaining dark promotion: R=G-Cy typed exit/kernel move")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
