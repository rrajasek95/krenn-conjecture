#!/usr/bin/env python3
"""Exact projective-T0 and arc/integral-closure reduction audit."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_t0_arc_integral_closure.json"

PINS = (
    "computations/unaudited-codex-x5-torus-hm-audit-2026-08-21/audit_x5_torus_hm.py",
    "computations/unaudited-codex-x5-global-base-locus-2026-08-21/audit_x5_global_base_locus.py",
    "computations/unaudited-codex-ghz-rees-boundary-2026-08-21/audit_ghz_rees_boundary.py",
    "computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21/audit_tail_remote_hafnian_contraction.py",
    "computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21/results_tail_remote_hafnian_contraction.json",
    "computations/unaudited-codex-tail-connectedness-smalln-2026-08-21/audit_tail_connectedness_smalln.py",
    "computations/unaudited-codex-tail-connectedness-smalln-2026-08-21/results_tail_connectedness_smalln.json",
    "computations/unaudited-codex-tail-idempotent-remote-2026-08-21/audit_tail_idempotent_remote.py",
    "computations/unaudited-codex-tail-idempotent-remote-2026-08-21/results_tail_idempotent_remote.json",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True,
                     separators=(",", ":")).encode("ascii")
    return sha256(raw).hexdigest()


def cell_label(i, j, a, b):
    require(i < j, (i, j, a, b))
    return i, j, a, b


CELLS = tuple(cell_label(i, j, a, b)
              for i, j in combinations(range(8), 2)
              for a, b in product(range(3), repeat=2))


def projected_stub_weight(site, colour):
    """Restriction of e_(site,colour) to sum_i u_(i,colour)=0."""
    answer = [0] * 21
    start = 7 * colour
    if site < 7:
        answer[start + site] = 1
    else:
        for index in range(start, start + 7):
            answer[index] = -1
    return tuple(answer)


def vector_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def projected_cell_weights():
    weights = {}
    for variable in CELLS:
        i, j, a, b = variable
        weight = vector_add(projected_stub_weight(i, a),
                            projected_stub_weight(j, b))
        require(weight not in weights, (variable, weights.get(weight), weight))
        weights[weight] = variable
    require(len(weights) == 252, len(weights))
    return weights


def explicit_generic_cocharacter():
    values = {}
    for colour in range(3):
        first = [3 ** (7 * colour + site) for site in range(7)]
        first.append(-sum(first))
        for site, value in enumerate(first):
            values[site, colour] = value
        require(sum(values[site, colour] for site in range(8)) == 0,
                (colour, values))
    scalar_weights = {}
    for variable in CELLS:
        i, j, a, b = variable
        value = values[i, a] + values[j, b]
        require(value not in scalar_weights,
                (variable, scalar_weights.get(value), value))
        scalar_weights[value] = variable
    return {
        "formula": "u_(i,c)=3^(7c+i) for i<7; u_(7,c)=-sum_(i<7)u_(i,c)",
        "distinct_cell_weights": len(scalar_weights),
        "minimum": min(scalar_weights),
        "maximum": max(scalar_weights),
    }


@lru_cache(None)
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


MATCHINGS = perfect_matchings(tuple(range(8)))


def semi_invariance_audit():
    checked = 0
    for word in product(range(3), repeat=8):
        expected = Counter((site, word[site]) for site in range(8))
        for matching in MATCHINGS:
            observed = Counter()
            for i, j in matching:
                observed[i, word[i]] += 1
                observed[j, word[j]] += 1
            require(observed == expected, (word, matching, observed, expected))
            checked += 1
    require(checked == 6561 * 105, checked)
    return checked


LAURENT_CELLS = {
    ((0, 1), 0, 0): -1,
    ((0, 3), 1, 1): 0,
    ((0, 7), 2, 2): 0,
    ((1, 4), 2, 2): 0,
    ((1, 6), 1, 1): 0,
    ((2, 3), 2, 2): 0,
    ((2, 4), 1, 1): 0,
    ((2, 5), 0, 0): 1,
    ((3, 4), 0, 0): 0,
    ((5, 6), 2, 2): 0,
    ((5, 7), 1, 1): 0,
    ((6, 7), 0, 0): 0,
}


def laurent_output(valuations):
    choices_by_edge = defaultdict(list)
    for (pair, left, right), value in valuations.items():
        choices_by_edge[pair].append((left, right, value))
    output = defaultdict(Counter)
    for matching in MATCHINGS:
        edge_choices = [choices_by_edge[pair] for pair in matching]
        if any(not choices for choices in edge_choices):
            continue
        for chosen in product(*edge_choices):
            word = [None] * 8
            exponent = 0
            for (i, j), (left, right, value) in zip(
                    matching, chosen, strict=True):
                word[i], word[j] = left, right
                exponent += value
            output[tuple(word)][exponent] += 1
    return output


def expected_laurent_output():
    return {
        (0,) * 8: Counter({0: 1}),
        (1,) * 8: Counter({0: 1}),
        (2,) * 8: Counter({0: 1}),
        tuple(map(int, "12012000")): Counter({1: 1}),
        tuple(map(int, "21000012")): Counter({1: 1}),
    }


def known_t0_collapses():
    require(laurent_output(LAURENT_CELLS) == expected_laurent_output(),
            laurent_output(LAURENT_CELLS))
    # The one-, two-, and three-minimal-cell arcs differ only on the pure
    # colour-0 matching 01|25|34|67, by zero-sum edge shifts.  Such a shift is
    # exactly a T0 cocharacter: put the shift on one endpoint of each edge.
    edge_order = ((0, 1), (2, 5), (3, 4), (6, 7))
    variants = {
        1: (-1, 1, 0, 0),
        2: (-1, 2, -1, 0),
        3: (-1, 3, -1, -1),
    }
    lifts = {}
    for number in (2, 3):
        delta = tuple(right - left for left, right
                      in zip(variants[1], variants[number], strict=True))
        require(sum(delta) == 0, (number, delta))
        u = {(site, colour): 0 for site in range(8) for colour in range(3)}
        for pair, shift in zip(edge_order, delta, strict=True):
            u[pair[0], 0] = shift
        require(sum(u[site, 0] for site in range(8)) == 0, (number, u))
        observed = tuple(u[i, 0] + u[j, 0] for i, j in edge_order)
        require(observed == delta, (number, observed, delta))
        lifts[str(number)] = {
            "edge_shift_from_one_cell": list(delta),
            "nonzero_site_weights": {
                str(site): value for (site, colour), value in u.items()
                if colour == 0 and value
            },
        }

    # The earlier infinite redistribution is also a literal T0 direction on
    # the live colour-1 support.
    for parameter in range(2, 9):
        moved = dict(LAURENT_CELLS)
        moved[((2, 4), 1, 1)] += parameter
        moved[((5, 7), 1, 1)] -= parameter
        require(laurent_output(moved) == expected_laurent_output(), parameter)
    return {
        "one_two_three_cell_arc_lifts": lifts,
        "infinite_redistribution": (
            "u_(2,1)=N, u_(5,1)=-N, all other u=0; on the live support "
            "this adds +N to A_24[11] and -N to A_57[11]."
        ),
        "verdict": "all previously frozen valuation variations collapse modulo loop-T0",
    }


def live_same_colour_edges(valuations, colour):
    return {pair for (pair, left, right) in valuations
            if left == right == colour}


def even_cycle_invariants(valuations):
    invariants = []
    for colour in range(3):
        edges = live_same_colour_edges(valuations, colour)
        for sites in combinations(range(8), 4):
            a, b, c, d = sites
            pairings = (
                ((a, b), (c, d)),
                ((a, c), (b, d)),
                ((a, d), (b, c)),
            )
            for first, second in combinations(pairings, 2):
                if set(first + second) <= edges:
                    first_value = sum(valuations[(tuple(sorted(pair)), colour, colour)]
                                      for pair in first)
                    second_value = sum(valuations[(tuple(sorted(pair)), colour, colour)]
                                       for pair in second)
                    invariants.append(abs(first_value - second_value))
    return sorted(invariants)


def infinite_inequivalent_arc_family():
    records = []
    for parameter in range(2, 11):
        valuations = dict(LAURENT_CELLS)
        valuations[((2, 3), 0, 0)] = parameter
        valuations[((0, 2), 0, 0)] = parameter
        valuations[((1, 3), 0, 0)] = 3 * parameter
        output = laurent_output(valuations)
        pure = {word: polynomial for word, polynomial in output.items()
                if len(set(word)) == 1}
        mixed = {word: polynomial for word, polynomial in output.items()
                 if len(set(word)) > 1}
        require(pure == {(0,) * 8: Counter({0: 1}),
                         (1,) * 8: Counter({0: 1}),
                         (2,) * 8: Counter({0: 1})}, (parameter, pure))
        require(min(min(polynomial) for polynomial in mixed.values()) == 1,
                (parameter, mixed))
        invariants = even_cycle_invariants(valuations)
        require(invariants == [3 * parameter + 1],
                (parameter, invariants))
        records.append({
            "N": parameter,
            "added_valuations": {"A_23[00]": parameter,
                                  "A_02[00]": parameter,
                                  "A_13[00]": 3 * parameter},
            "unique_even_cycle_absolute_invariant": invariants[0],
            "affine_leading_output": "Delta+t*(two frozen mixed words)",
            "projective_leading_output": "t^4*Delta",
        })
    require(len({row["unique_even_cycle_absolute_invariant"] for row in records})
            == len(records), records)
    return {
        "family": records,
        "invariant_formula": (
            "|v(A_01[00])+v(A_23[00])-v(A_02[00])-v(A_13[00])|=3N+1"
        ),
        "invariance": (
            "Endpoint potentials from T0 cancel because every site occurs "
            "once with each sign; common projective shifts cancel 2-2. The "
            "finite site/colour group only permutes/signs the finite list of "
            "four-cycle invariants. This support has exactly one such cycle."
        ),
        "scope": (
            "These are infinitely many contact arcs over the same leading "
            "GHZ Rees direction. They are not asserted to be the finitely many "
            "divisorial Rees valuations of the ideal."
        ),
    }


def reduce_lambda_monomial(coefficient, exponent):
    quotient, remainder = divmod(exponent, 4)
    return coefficient * Fraction(1, 105) ** quotient, remainder


def remote_cell(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    if a == b:
        return Fraction(1), 1
    exceptional = {
        (0, 1, 0, 2): (Fraction(1), 0),
        (6, 7, 1, 2): (Fraction(1), 0),
        (0, 6, 0, 1): (Fraction(-1, 5), -1),
        (0, 1, 0, 1): (Fraction(1, 5), -1),
        (6, 7, 1, 0): (Fraction(1, 5), -1),
    }
    return exceptional.get((u, v, a, b), (Fraction(0), 0))


def remote_point_audit():
    nonzero_mixed = []
    profiles = Counter()
    for word in product(range(3), repeat=8):
        polynomial = Counter()
        for matching in MATCHINGS:
            coefficient = Fraction(1)
            exponent = 0
            for i, j in matching:
                local_coefficient, local_exponent = remote_cell(
                    i, j, word[i], word[j])
                coefficient *= local_coefficient
                exponent += local_exponent
                if not coefficient:
                    break
            if coefficient:
                coefficient, remainder = reduce_lambda_monomial(
                    coefficient, exponent)
                polynomial[remainder] += coefficient
        polynomial = {degree: value for degree, value in polynomial.items()
                      if value}
        if polynomial and len(set(word)) > 1:
            nonzero_mixed.append(word)
            profile = tuple(sorted(Counter(word).values(), reverse=True))
            profiles[profile] += 1
    require(len(nonzero_mixed) == 2390, len(nonzero_mixed))
    require(profiles[(6, 2)] == 168 and profiles[(4, 4)] == 210 and
            profiles[(4, 2, 2)] == 1260, profiles)

    profile620 = [word for word in nonzero_mixed
                  if tuple(sorted(Counter(word).values(), reverse=True)) == (6, 2)]
    incidence = Counter((site, colour)
                        for word in profile620
                        for site, colour in enumerate(word))
    require(len(profile620) == 168 and
            set(incidence.values()) == {56}, incidence)
    return {
        "nonzero_mixed_amplitudes": len(nonzero_mixed),
        "nonzero_profile_counts": {
            "620": profiles[(6, 2)],
            "440": profiles[(4, 4)],
            "422": profiles[(4, 2, 2)],
        },
        "profile620_character_sum": "56*(p0+p1+p2)=0 on T0",
        "consequence": (
            "All 168 profile-620 amplitudes are nonzero. They cannot all "
            "receive strictly positive T0 weight because their character sum "
            "is zero. The partial remote point is not on the normalized mixed "
            "scheme and cannot be turned into a GHZ-contact arc by T0."
        ),
    }


def rees_divisor_audit():
    """Separate contact arcs from divisorial valuations and profile blowups."""
    # Work in the projective chart in which the unique minimal cell
    # A_01[00] is one.  Each family member has fifteen nonzero homogeneous
    # cells, including the anchor, and hence 237 local coordinate functions
    # vanish identically along the arc.
    anchor = ((0, 1), 0, 0)
    require(anchor in LAURENT_CELLS and LAURENT_CELLS[anchor] == -1,
            LAURENT_CELLS.get(anchor))
    for parameter in range(2, 11):
        valuations = dict(LAURENT_CELLS)
        valuations[((2, 3), 0, 0)] = parameter
        valuations[((0, 2), 0, 0)] = parameter
        valuations[((1, 3), 0, 0)] = 3 * parameter
        require(len(valuations) == 15, (parameter, len(valuations)))
        local_nonzero = len(valuations) - 1
        require(local_nonzero == 14, (parameter, local_nonzero))
        require(251 - local_nonzero == 237, parameter)
        output = laurent_output(valuations)
        # Dehomogenizing the quartic map by an anchor of order -1 adds four
        # to every raw output order.  The pure rows have raw order zero.
        contact = min(exponent + 4 for polynomial in output.values()
                      for exponent in polynomial)
        require(contact == 4, (parameter, contact))

    # Exact local generator census at the one-cell point.  A row whose two
    # anchor endpoint colours are 00 has 15 matchings through the anchor and
    # therefore a cubic residual H_6 part.  Its other 90 matchings are
    # quartic.  All other rows have 105 quartic terms.
    residual_edges = len(tuple(combinations(range(2, 8), 2)))
    residual_variables = residual_edges * 9
    touching_variables = (28 - residual_edges) * 9 - 1
    cubic_rows = 3 ** 6
    quartic_rows = 3 ** 8 - cubic_rows
    cubic_terms = cubic_rows * len(perfect_matchings(tuple(range(2, 8))))
    quartic_terms = cubic_rows * (len(MATCHINGS) - 15) + quartic_rows * len(MATCHINGS)
    require((residual_variables, touching_variables) == (135, 116),
            (residual_variables, touching_variables))
    require(cubic_rows == 729 and quartic_rows == 5832,
            (cubic_rows, quartic_rows))
    require(cubic_terms == 10935 and quartic_terms == 677970,
            (cubic_terms, quartic_terms))
    require(cubic_terms + quartic_terms == 6561 * 105,
            cubic_terms + quartic_terms)

    return {
        "contact_arc_vs_divisor": {
            "projective_local_coordinates": 251,
            "family_nonzero_local_coordinates": 14,
            "family_identically_zero_local_coordinates": 237,
            "base_ideal_contact_order": 4,
            "conclusion": (
                "Each displayed N-arc induces only a curve semivaluation: "
                "its kernel contains 237 ambient coordinate functions. A "
                "divisorial valuation of the ambient function field has "
                "zero kernel. Thus the family is not an infinite family of "
                "Rees divisors, and no individual Rees divisor is canonically "
                "assigned without computing the normalized blowup."
            ),
        },
        "one_cell_local_base_ideal": {
            "ambient_regular_local_dimension": 251,
            "generators": 6561,
            "cubic_leading_rows": cubic_rows,
            "cubic_matching_monomials": cubic_terms,
            "cubic_variables": residual_variables,
            "quartic_leading_rows": quartic_rows,
            "quartic_matching_monomials": quartic_terms,
            "remaining_endpoint_variables": touching_variables,
            "exact_form": (
                "For endpoint colours 00, F_w=H_6(w|_{2..7})+Q_w "
                "after dehomogenizing A_01[00]=1, with degrees 3 and 4; "
                "the other rows are quartic Q_w."
            ),
            "obstruction": (
                "The known GHZ arc lies in the kernel of every cubic H_6 "
                "row and first appears in the quartic normal direction. "
                "Therefore the 729-row cubic initial ideal does not control "
                "the relevant normalized blowup; the full 6561-generator "
                "Rees algebra in 251 variables is required."
            ),
        },
        "remote_tail_ideal": {
            "ambient_tail_generators": 168,
            "ambient_blowup": (
                "In the smooth source chart this is the coordinate ideal of "
                "an irreducible codimension-168 linear subspace, so its "
                "ordinary normalized blowup has one exceptional divisor."
            ),
            "normalized_exact_source_ring": (
                "The frozen N8-DIAGONAL theorem gives A8/J8=0, hence the "
                "full tail ideal J8=A8. Its blowup on the normalized exact "
                "source scheme is the identity and has no Rees divisor."
            ),
            "selected_tail_guard": (
                "A selected 12-column tail ideal need not be the unit ideal, "
                "but it omits 156 literal tail variables and therefore is "
                "not a source-faithful replacement for J8."
            ),
        },
        "cap_target_guard": {
            "carriers": 728,
            "locally_closed": True,
            "reason": (
                "No-cap is a union of carrier-rank strata with chosen live "
                "pivot minors and blocker-membership minors. It is not the "
                "vanishing set of one canonical small invariant ideal. A "
                "blowup target must retain this branch/localizer data."
            ),
        },
        "terminal_conclusion": (
            "A fixed source ideal has finitely many Rees divisors abstractly, "
            "but neither the one-cell cubic truncation nor the remote tail "
            "ideal gives a finite computable blowup controlling cap failure. "
            "Beyond global normalization of the full base/cap Rees data, no "
            "smaller source-faithful divisor reduction is currently justified."
        ),
    }


def build_result():
    projected = projected_cell_weights()
    semi_terms = semi_invariance_audit()
    result = {
        "status": "PASS exact projective-T0 arc/integral-closure audit",
        "projected_weight_injectivity": {
            "projected_character_lattice": "Z^24/<p0,p1,p2>, rank 21",
            "distinct_literal_cell_characters": len(projected),
            "proof": (
                "If two two-stub weights differ by sum_c r_c p_c, an untouched "
                "site in each colour forces r_c=0. Equality of the remaining "
                "two-stub multisets is equality of the canonical literal cell."
            ),
            "explicit_global_generic_cocharacter": explicit_generic_cocharacter(),
        },
        "hypothetical_exact_source_one_cell_theorem": {
            "semi_invariant_matching_terms_checked": semi_terms,
            "unique_exposed_cell": True,
            "minimum_weight_strictly_negative": True,
            "negative_proof": (
                "Each normalized pure amplitude has a live perfect-matching "
                "term. Its four cell weights sum to p_c(u)=0. Generic "
                "distinctness rules out all four weights being zero, so one "
                "is negative and the global minimum m<0."
            ),
            "arc": "B(t)=t^(-m)*(lambda_u(t) acting on A)",
            "output": "H(B(t))=t^(-4m)*Delta_8,3 exactly",
            "mixed_terms": (
                "Every term of F_w has order chi_w(u)-4m, independent of its "
                "matching. Thus F_w(B)=t^(chi_w-4m)F_w(A)=0 for every mixed w."
            ),
            "verdict": (
                "The one-cell theorem is correct but tautological: it is a "
                "projectivized symmetry orbit of the hypothetical point. No "
                "matching term is selected inside a word and the initial "
                "cancellation equations are the original equations."
            ),
        },
        "known_arc_quotient": known_t0_collapses(),
        "infinite_inequivalent_contact_arcs": infinite_inequivalent_arc_family(),
        "remote_idempotent_control": remote_point_audit(),
        "rees_divisor_status": rees_divisor_audit(),
        "jet_support_integral_closure_scaffold": {
            "theorem": (
                "In a regular local ring, the intersection over all finite "
                "m-jet support closures of an ideal equals its integral "
                "closure (de Fernex-Ein-Ishii, Proposition 4.12). Equivalently, "
                "integral dependence is controlled by all arc valuations; the "
                "divisorial reduction is the finite set of Rees valuations."
            ),
            "exact_scope": (
                "Apply this in a smooth ambient affine/projective chart. The "
                "pure-normalized quotient need not itself be regular, and the "
                "projectively rescaled torus arcs are arcs of the all-amplitude "
                "base ideal/Rees graph, not arcs satisfying F_pure=1 at t=0."
            ),
            "primary_source": "https://arxiv.org/abs/1704.07494",
        },
        "terminal_verdict": {
            "fixed_ideal_has_finitely_many_rees_valuations": True,
            "symmetry_identifies_them_with_frozen_arc_types": False,
            "all_relevant_contact_arcs_finite_modulo_symmetry": False,
            "precise_no_go": (
                "Noetherianity gives finitely many unknown divisorial Rees "
                "valuations, but S8xS3 and loop-T0 do not reduce the contact "
                "arc space to the known one-/two-/three-cell or remote types. "
                "The explicit even-cycle family has infinitely many quotient "
                "classes with the same leading GHZ direction."
            ),
            "smallest_new_target": (
                "There is no smaller justified divisor target. One must either "
                "normalize the full one-cell Rees algebra together with a "
                "fixed carrier rank/pivot branch, or first derive a new exact "
                "source polynomial whose vanishing canonically encodes cap "
                "failure. Finite arc sampling cannot prove this."
            ),
        },
        "pinned_sources": {name: file_sha(ROOT / name) for name in PINS},
    }
    result["logical_sha256"] = logical_sha(result)
    return result


def main(write_results=False, print_result=False):
    result = build_result()
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(json.dumps({
        "status": result["status"],
        "projected_weights": result[
            "projected_weight_injectivity"]["distinct_literal_cell_characters"],
        "semi_invariant_terms": result[
            "hypothetical_exact_source_one_cell_theorem"
        ]["semi_invariant_matching_terms_checked"],
        "inequivalent_cycle_invariants": [row[
            "unique_even_cycle_absolute_invariant"] for row in result[
                "infinite_inequivalent_contact_arcs"]["family"]],
        "remote_nonzero_mixed": result[
            "remote_idempotent_control"]["nonzero_mixed_amplitudes"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--print-result", action="store_true")
    args = parser.parse_args()
    main(args.write_results, args.print_result)
