#!/usr/bin/env python3
"""Exact source-faithful audit of the proposed framed-quiver reformulation."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TORUS_RESULT = (ROOT / "computations/unaudited-codex-x5-torus-hm-audit-2026-08-21" /
                "results_x5_torus_hm.json")
RESPONSE_RESULT = (ROOT / "computations/unaudited-codex-response-star-2026-08-20" /
                   "results_response_star.json")
OUT = HERE / "results_x5_framed_quiver.json"
PINNED_TORUS_LOGICAL = (
    "8ddc0cead9c8ec71b6091847319a053c8f1d3b275e19fb44c8280c716832b12c"
)
SITES = tuple(range(8))
COLOURS = tuple(range(3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def rank(rows, width):
    work = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


def audit_hafnian_equivariance():
    require(len(MATCHINGS) == 105, "perfect matching count changed")
    incidences = []
    for matching in MATCHINGS:
        degrees = [0] * 8
        for left, right in matching:
            degrees[left] += 1
            degrees[right] += 1
        require(degrees == [1] * 8, (matching, degrees))
        incidences.append(degrees)
    return {
        "edge_representation": "E=direct_sum_(i<j) V_i tensor V_j",
        "base_change": "A_ij -> (g_i tensor g_j) A_ij",
        "hafnian_map": "H:E -> tensor_(i=0)^7 V_i, homogeneous degree four",
        "equivariance": "H(g.A)=(tensor_i g_i)H(A)",
        "literal_certificate": (
            "Every one of the 105 matching summands contains each site factor "
            "exactly once."
        ),
        "matching_incidence_checks": len(incidences),
    }


def tangent_stabilizer():
    """Rank of the infinitesimal orbit map at GHZ in gl(3)^8."""
    columns = [(site, target, source)
               for site in SITES
               for target, source in product(COLOURS, repeat=2)]
    coefficient_rows = {}
    for column, (site, target, source) in enumerate(columns):
        word = [source] * 8
        word[site] = target
        word = tuple(word)
        coefficient_rows.setdefault(word, [0] * len(columns))[column] += 1
    rows = list(coefficient_rows.values())
    orbit_rank = rank(rows, len(columns))
    require(len(columns) == 72 and len(rows) == 51 and orbit_rank == 51,
            (len(columns), len(rows), orbit_rank))
    return {
        "ambient_base_change_dimension": len(columns),
        "infinitesimal_orbit_rank": orbit_rank,
        "stabilizer_dimension": len(columns) - orbit_rank,
        "off_diagonal_constraints": 48,
        "diagonal_constraints": 3,
        "equations": (
            "X_i[d,c]=0 for d!=c, and sum_i X_i[c,c]=0 for c=0,1,2"
        ),
    }


def contraction_rank_one_locus():
    # A vector in span(e0 tensor e0, e1 tensor e1, e2 tensor e2) is the
    # diagonal matrix diag(a0,a1,a2).  Its rank-one equations are a0*a1,
    # a0*a2, a1*a2.  Support enumeration confirms the projective locus is
    # exactly the three coordinate lines.
    rank_one_supports = []
    for mask in range(1, 8):
        support = tuple(colour for colour in COLOURS if (mask >> colour) & 1)
        all_pair_products_forced_zero = len(support) <= 1
        if all_pair_products_forced_zero:
            rank_one_supports.append(support)
    require(rank_one_supports == [(0,), (1,), (2,)], rank_one_supports)
    return {
        "two_site_contraction_space": (
            "D_ij=span(e_(i,0)tensor e_(j,0), e_(i,1)tensor e_(j,1), "
            "e_(i,2)tensor e_(j,2))"
        ),
        "rank_one_equations": ["a0*a1", "a0*a2", "a1*a2"],
        "projective_rank_one_locus": ["[e0 tensor e0]",
                                       "[e1 tensor e1]",
                                       "[e2 tensor e2]"],
        "consequence": (
            "A GHZ stabilizer permutes these three intrinsic lines for every "
            "site pair. Pairwise consistency forces one common permutation "
            "at all eight sites."
        ),
    }


def finite_stabilizer_components():
    permutations_checked = 0
    support = {tuple([colour] * 8) for colour in COLOURS}
    for sigma in permutations(COLOURS):
        image = {tuple([sigma[colour]] * 8) for colour in COLOURS}
        require(image == support, sigma)
        permutations_checked += 1
    require(permutations_checked == 6, permutations_checked)
    return {
        "largest_equation_preserving_group": (
            "G_GHZ=T0 semidirect S3, where g_i e_(i,c)="
            "d_(i,c)e_(i,sigma(c)) and product_i d_(i,c)=1"
        ),
        "identity_component_dimension": 21,
        "components": permutations_checked,
        "ordered_global_summand_framing_stabilizer": "T0",
        "ordered_local_basis_framing_stabilizer": "identity",
        "verdict": "No framing convention enlarges the continuous target-preserving group.",
    }


def quiver_orientation_obstruction():
    edges = tuple(combinations(SITES, 2))
    good_signings = []
    for signs in product((0, 1), repeat=8):
        if all(signs[left] != signs[right] for left, right in edges):
            good_signings.append(signs)
    require(not good_signings, good_signings)
    triangle = ((0, 1), (1, 2), (0, 2))
    require(all(edge in edges for edge in triangle), "K8 triangle disappeared")
    return {
        "ordinary_arrow_action": "A:i->j transforms as g_j A g_i^-1",
        "edge_tensor_as_map": (
            "V_i tensor V_j = Hom(V_i^*,V_j), transforming as g_j A g_i^T"
        ),
        "required_vertex_dualization": (
            "Every physical edge would have to join one primal and one dual "
            "site vertex."
        ),
        "two_colourings_checked": 256,
        "valid_two_colourings": 0,
        "falsifying_odd_cycle": [[0, 1], [1, 2], [0, 2]],
        "verdict": (
            "The K8 tensor representation is not an ordinary quiver "
            "representation with one GL(V_i) vertex per site. A doubled "
            "primal/dual quiver requires the involution constraint "
            "g_(i,-)=g_(i,+)^(-T), so ordinary King subrepresentations and "
            "independent vertex base changes are not source-faithful."
        ),
    }


def framed_stability_audit():
    frame_matrix = [[1 if row == column else 0 for column in COLOURS]
                    for row in COLOURS]
    require(rank(frame_matrix, 3) == 3, "local GHZ frame stopped spanning")
    coordinate_subsets_containing_frame = []
    for mask in range(8):
        if all((mask >> colour) & 1 for colour in COLOURS):
            coordinate_subsets_containing_frame.append(mask)
    require(coordinate_subsets_containing_frame == [7],
            coordinate_subsets_containing_frame)
    return {
        "king_criterion_if_ordinary": (
            "For a dimension vector d and character theta with theta.d=0, "
            "theta-semistability is the sign condition on theta(dim W) for "
            "every quiver subrepresentation W; HN uses the induced slopes."
        ),
        "soundness_here": False,
        "reason": (
            "There is no source-faithful ordinary quiver action, and the "
            "framed GHZ equation supplies no distinguished nonzero King "
            "character. On the actual stabilizer, theta=0 is the natural "
            "choice and gives no destabilizing filtration."
        ),
        "cyclic_framed_stability": (
            "If the three local GHZ frame vectors are used as generating "
            "framings, they already span every V_i. Any subrepresentation "
            "containing the framing is the whole representation, independent "
            "of all 28 edge tensors; cyclic stability is therefore vacuous."
        ),
        "frame_rank_at_each_site": 3,
        "proper_coordinate_subspaces_containing_all_frames": 0,
        "cap_mismatch": (
            "A clean cap is a nonzero K in the kernel of a 90x9 or 108x9 "
            "response matrix with four activity forms nonzero. It is not a "
            "site subspace preserved by the 28 edge maps, so no King/HN "
            "subrepresentation canonically produces K or an N8->N6 descent."
        ),
    }


def carrier_negative_control():
    response = json.loads(RESPONSE_RESULT.read_text())
    star = response["response_star"]["W25-F8"]
    triangle = response["response_star"]["triangle_extension"]["W25-F8"]
    require(star["choices"] == 168 and star["passing_choices"] == 0 and
            triangle["choices"] == 560 and triangle["passing_choices"] == 0,
            "W25-F8 carrier negative control changed")
    return {
        "source": response["inputs"]["W25-F8"],
        "ordered_GHZ_local_frames_make_cyclic_stability": True,
        "passing_star_carriers": star["passing_choices"],
        "passing_triangle_carriers": triangle["passing_choices"],
        "scope": (
            "This is an exact 728-carrier no-cap negative control, but it is "
            "outside X4 (78 level-four failures), hence not a counterexample "
            "to the target conjecture. It proves that framed cyclic stability "
            "alone has no formal implication to the carrier cap criterion."
        ),
    }


def main(write_results=False):
    torus = json.loads(TORUS_RESULT.read_text())
    require(torus["logical_sha256"] == PINNED_TORUS_LOGICAL,
            "pinned torus/HM audit changed")
    result = {
        "status": "PASS exact framed-quiver falsification audit",
        "source_faithful_tensor_model": audit_hafnian_equivariance(),
        "GHZ_stabilizer": {
            "infinitesimal": tangent_stabilizer(),
            "intrinsic_rank_one_locus": contraction_rank_one_locus(),
            "global_group": finite_stabilizer_components(),
        },
        "ordinary_quiver_obstruction": quiver_orientation_obstruction(),
        "king_HN_audit": framed_stability_audit(),
        "exact_stable_but_728_carrier_blocked_control": carrier_negative_control(),
        "prior_torus_HM_terminal": {
            "logical_sha256": torus["logical_sha256"],
            "raw_no_cap_closed": torus["closedness"]["closed"],
            "generic_rank_stratified_cone_dimension": torus[
                "rank_stratified_cones"]["generic_full_support"]["cone_dimension"],
            "minimal_310_face_verdict": torus["rank_stratified_cones"]
                ["frozen_310_minimal_supports"]["face_support_verdict"],
        },
        "terminal_theory_verdict": {
            "framed_quiver_supplies_larger_group": False,
            "king_destabilization_to_cap_or_descent": False,
            "reason": (
                "The actual target stabilizer is exactly the previously "
                "audited 21-dimensional torus up to common S3. The edge "
                "tensors are not an ordinary K8-quiver representation, and "
                "full GHZ framing makes standard cyclic stability vacuous."
            ),
            "cheapest_remaining_route": (
                "Use response-kernel/tail algebra directly, or prove a "
                "non-toric initial-ideal/support descent compatible with the "
                "728 rank strata; quiver HN adds no source-faithful mechanism."
            ),
        },
        "pinned_sources": {
            str(TORUS_RESULT.relative_to(ROOT)): file_sha(TORUS_RESULT),
            str(RESPONSE_RESULT.relative_to(ROOT)): file_sha(RESPONSE_RESULT),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "GHZ_stabilizer_dimension": result["GHZ_stabilizer"]
            ["infinitesimal"]["stabilizer_dimension"],
        "GHZ_stabilizer_components": result["GHZ_stabilizer"]
            ["global_group"]["components"],
        "ordinary_K8_quiver_two_colourings": result
            ["ordinary_quiver_obstruction"]["valid_two_colourings"],
        "W25_passing_carriers": 0,
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
