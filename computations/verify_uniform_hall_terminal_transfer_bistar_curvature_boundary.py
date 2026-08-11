#!/usr/bin/env python3
"""Source-unit promotion for the terminal two-shared Hall recurrence.

The strict M3 endpoint exchange of f2c02cf legitimately returns to the
two-shared label migration.  It does not, by itself, turn the resulting
closed transfer graph into one same-star linear switch space.  In the first
returned mixed word the avoiding anchor term contains both endpoint arms:

    q01_22 * (q24_00*q35_00 + q23_00*q45_00)
      + q02_20*q13_20*q45_00.

The two crossing variables q02_20 and q13_20 lie on different physical
stars.  Simultaneously varying them has a nonzero mixed second difference.
Thus a weighted graph kernel across both endpoints is only a tangent kernel.
The full strict packet nevertheless closes: the colour-one companion rows
cancel the two colour-two alternate aggregates and leave localized monomial
source units.  Each individual endpoint exchange remains exactly linear,
as used in f2c02cf.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py":
        "1971623c20b0b337793d342b5bf698b69412a53f2f47aa4830300fa06f5a2456",
    "notes/uniform-hall-m3-unequal-tail-cycle-boundary.md":
        "f81b60615fabe540020a226838258c6b28ddfacffe17c4ae7489a4a07402c2f6",
    "computations/verify_uniform_two_shared_anchor_unary_label_migration.py":
        "78ab24f1c39d79ea38a80fd80bf43e43624e57dada0345c2c98b30559f528dc6",
    "notes/uniform-two-shared-anchor-unary-label-migration.md":
        "2e794feae556d582dc1623e698e2e331cae44e0de36e9d59125740a908d3b1c9",
    "computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py":
        "34bf365f2a9e154a10feab8fa7cc83b0aba519f4124b8e28ed959f280a51e721",
    "notes/uniform-hall-five-lock-signless-incidence-boundary.md":
        "4da56337a9cc6b8434a06b6cf1e4c9118334ebf695f4679e8183232f4733cb1b",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_multisite_hall_k22_source_reduction.py":
        "6f75623da9a371303fad5a7986fa3dba464e8c0fb593c97dc23df04a0e84b9f4",
    "notes/uniform-multisite-hall-k22-source-reduction.md":
        "ed05ae4c38b048932fcb9b50c452c074d96b555f4f00a17b18b25045cac197c9",
    "computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py":
        "59dd21c4664e8ccd88f771d0191d3db32e5fdb832e2c6de1f169cb197f9a3038",
    "notes/uniform-hall-k22-outside-endpoint-component-wedge.md":
        "cd3807d8f3f4f3d8ccda38e23c5ff291d3f0e3f1a33b69f3d2ef061b117d3347",
}
EXPECTED_LEDGER_SHA256 = "9e2ecc8cd8554340ab94fa77539f51b1cb8e881b4062283d5e000a282e23a792"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def cell_name(pair, word):
    left, right = pair
    return f"q{left}{right}_{word[left]}{word[right]}"


def monomial(matching, word):
    return tuple(sorted(cell_name(pair, word) for pair in matching))


def clean(polynomial):
    return Counter({term: coefficient for term, coefficient
                    in polynomial.items() if coefficient})


def variable(name):
    return Counter({(name,): Q(1)})


def add(*signed_polynomials):
    answer = Counter()
    for polynomial, coefficient in signed_polynomials:
        for term, value in polynomial.items():
            answer[term] += coefficient * value
    return clean(answer)


def multiply(*polynomials):
    answer = Counter({(): Q(1)})
    for polynomial in polynomials:
        updated = Counter()
        for left, left_value in answer.items():
            for right, right_value in polynomial.items():
                updated[tuple(sorted(left + right))] += left_value * right_value
        answer = clean(updated)
    return answer


def translate(polynomial, substitutions):
    answer = Counter()
    for term, coefficient in polynomial.items():
        expanded = Counter({(): coefficient})
        for name in term:
            expanded = multiply(expanded,
                                substitutions.get(name, variable(name)))
        answer.update(expanded)
    return clean(answer)


def audit_literal_return_row():
    # Canonical strict-K2,2 chart from f2c02cf.  The pivot e is shared by
    # Q0 and Q1; Q2 avoids it through arms g and h.
    e, g, h, tail = edge(0, 1), edge(0, 2), edge(1, 3), edge(4, 5)
    q0 = tuple(sorted((e, edge(2, 4), edge(3, 5))))
    q1 = tuple(sorted((e, edge(2, 3), tail)))
    q2 = tuple(sorted((g, h, tail)))
    anchor_union = set(q0) | set(q1) | set(q2)
    contained = tuple(matching for matching in perfect_matchings(range(6))
                      if set(matching) <= anchor_union)
    require(set(contained) == {q0, q1, q2},
            f"the canonical anchor union gained a matching: {contained}")

    # This is the first terminal/background row highlighted in the strict
    # provenance audit.
    # It is genuinely mixed.  The two e-containing terms form the complete
    # through aggregate; the sole avoiding term uses both third-anchor arms.
    word = (2, 2, 0, 0, 0, 0)
    terms = {matching: monomial(matching, word) for matching in contained}
    expected = {
        q0: ("q01_22", "q24_00", "q35_00"),
        q1: ("q01_22", "q23_00", "q45_00"),
        q2: ("q02_20", "q13_20", "q45_00"),
    }
    require(terms == expected, f"the literal returned row changed: {terms}")
    through = tuple(terms[matching] for matching in contained if e in matching)
    avoiding = tuple(terms[matching] for matching in contained if e not in matching)
    require(len(through) == 2 and avoiding == (expected[q2],),
            "the through/avoiding return partition changed")
    require(not set(g) & set(h) and set(g) | set(h) | set(tail) == set(range(6)),
            "the two endpoint arms stopped forming a physical matching")
    return {
        "selected_anchors": {"Q0": q0, "Q1": q1, "Q2": q2},
        "shared_pivot": e,
        "third_anchor_arms": [g, h],
        "full_word": "220000",
        "anchor_contained_terms": [terms[matching] for matching in contained],
        "exact_factorization": (
            "q01_22*(q24_00*q35_00+q23_00*q45_00)"
            "+q02_20*q13_20*q45_00"
        ),
        "source_typing": (
            "the avoiding transfer column is the product of one cell on "
            "the site-0 star and one cell on the site-1 star"
        ),
    }


def audit_mixed_second_difference():
    e = variable("e")
    a = variable("a")
    b = variable("b")
    g = variable("g")
    h = variable("h")
    tail = variable("t")
    dg = variable("dg")
    dh = variable("dh")
    row = add((multiply(e, a), 1), (multiply(e, b), 1),
              (multiply(g, h, tail), 1))
    shift_g = {"g": add((g, 1), (dg, 1))}
    shift_h = {"h": add((h, 1), (dh, 1))}
    shift_both = dict(shift_g)
    shift_both.update(shift_h)
    mixed = add(
        (translate(row, shift_both), 1),
        (translate(row, shift_g), -1),
        (translate(row, shift_h), -1),
        (row, 1),
    )
    expected = multiply(dg, dh, tail)
    require(mixed == expected,
            f"the bistar mixed second difference changed: {mixed}")

    # Each one-star restriction is genuinely affine-linear, so this does
    # not challenge the endpoint exchange used by f2c02cf.
    second_g = add(
        (translate(translate(row, shift_g), shift_g), 1),
        (translate(row, shift_g), -2), (row, 1))
    second_h = add(
        (translate(translate(row, shift_h), shift_h), 1),
        (translate(row, shift_h), -2), (row, 1))
    require(not second_g and not second_h,
            "an individual same-star exchange acquired curvature")

    # A concrete tangent cancellation across the two stars is not a finite
    # source switch.  At e=-1,g=h=t=1,a=1,b=0, take dg=1,dh=-1,de=0.
    # The first variation vanishes, while the translated row is -s^2.
    for parameter in (Q(1), Q(2), Q(-3), Q(1, 2)):
        base = Q(-1) + Q(1) * Q(1)
        moved = Q(-1) + (Q(1) + parameter) * (Q(1) - parameter)
        require(base == 0 and moved == -(parameter ** 2),
                "the tangent-but-not-finite bistar guard changed")
    return {
        "individual_site0_second_difference": 0,
        "individual_site1_second_difference": 0,
        "mixed_bistar_second_difference": "dg*dh*t",
        "physical_reason": (
            "q02_10 and q14_20 use disjoint physical edges; their product "
            "with q35_00 is a legal perfect-matching monomial"
        ),
        "tangent_guard": {
            "normalized_row": "F=e+g*h",
            "base_point": {"e": -1, "g": 1, "h": 1},
            "direction": {"de": 0, "dg": 1, "dh": -1},
            "first_variation": 0,
            "finite_residual": "-s^2",
        },
    }


def typed_response_terms(anchor_union, word, colour, p_sites, s_sites):
    """Literal response terms for one colour and two endpoint stars."""
    terms = []
    for p_site in p_sites:
        for s_site in s_sites:
            if word[p_site] != colour or word[s_site] != colour:
                continue
            complement = tuple(site for site in range(6)
                               if site not in (p_site, s_site))
            for matching in perfect_matchings(complement):
                if set(matching) <= anchor_union:
                    names = [f"p{colour}_{p_site}",
                             f"s{colour}_{s_site}"]
                    names.extend(cell_name(pair, word) for pair in matching)
                    terms.append(tuple(sorted(names)))
    return tuple(sorted(terms))


def response_terms(anchor_union, word):
    """Axis-purified colour-two response terms in the strict shore chart."""
    return typed_response_terms(anchor_union, word, 2, (1, 2), (0, 3))


def polynomial_from_terms(terms):
    answer = Counter()
    for term in terms:
        answer[term] += Q(1)
    return clean(answer)


def matrix_rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def source_cell(left, right, left_colour, right_colour, name):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return left, right, left_colour, right_colour, name


def deleted_star_rank(cells, site, deleted_edge):
    entries = []
    for left, right, left_colour, right_colour, _name in cells:
        if (left, right) == deleted_edge:
            continue
        if left == site:
            entries.append((left_colour, right, right_colour))
        elif right == site:
            entries.append((right_colour, left, left_colour))
    columns = sorted({(neighbour, tail) for _head, neighbour, tail in entries})
    matrix = [[Q(0) for _column in columns] for _head in range(3)]
    for head, neighbour, tail in entries:
        matrix[head][columns.index((neighbour, tail))] += 1
    return matrix_rank(matrix)


def audit_diagonal_response_exposure():
    # The strict opposite-shore axis support is
    #   p2 at sites 1,2; s2 at sites 0,3.
    # The two mixed diagonal rows obtained by deleting one crossing arm
    # expose q13_20*q45_00 and q02_20*q45_00 separately.
    e, g, h, tail = edge(0, 1), edge(0, 2), edge(1, 3), edge(4, 5)
    q0 = tuple(sorted((e, edge(2, 4), edge(3, 5))))
    q1 = tuple(sorted((e, edge(2, 3), tail)))
    q2 = tuple(sorted((g, h, tail)))
    anchor_union = set(q0) | set(q1) | set(q2)
    row_h = response_terms(anchor_union, (2, 2, 2, 0, 0, 0))
    row_g = response_terms(anchor_union, (2, 2, 0, 2, 0, 0))
    expected_h = tuple(sorted((
        tuple(sorted(("p2_2", "s2_0", "q13_20", "q45_00"))),
        tuple(sorted(("p2_1", "s2_0", "q23_20", "q45_00"))),
        tuple(sorted(("p2_1", "s2_0", "q24_20", "q35_00"))),
    )))
    expected_g = tuple(sorted((
        tuple(sorted(("p2_1", "s2_3", "q02_20", "q45_00"))),
        tuple(sorted(("p2_1", "s2_0", "q23_02", "q45_00"))),
        tuple(sorted(("p2_1", "s2_0", "q24_00", "q35_20"))),
    )))
    require(row_h == expected_h and row_g == expected_g,
            f"the two diagonal companion rows changed: {row_h}, {row_g}")

    # Because the displayed crossing terms and all four selected star
    # factors are nonzero, exactness forces one literal term from each
    # alternate pair (or the row is already a localized unit).
    alternatives = {
        "A": source_cell(2, 3, 2, 0, "q23_20"),
        "B": source_cell(2, 4, 2, 0, "q24_20"),
        "C": source_cell(2, 3, 0, 2, "q23_02"),
        "D": source_cell(3, 5, 2, 0, "q35_20"),
    }
    base = []
    for colour, matching in enumerate((q0, q1, q2)):
        for left, right in matching:
            base.append(source_cell(left, right, colour, colour,
                                    f"Q{colour}_{left}{right}"))
    base.extend((
        source_cell(0, 1, 2, 2, "terminal_q01_22"),
        source_cell(0, 2, 2, 0, "cross_q02_20"),
        source_cell(1, 3, 2, 0, "cross_q13_20"),
    ))

    active_names = {"cross_q02_20", "cross_q13_20", "A", "B", "C", "D"}
    rank_audit = []
    for left_choice in ("A", "B"):
        for right_choice in ("C", "D"):
            cells = base + [alternatives[left_choice], alternatives[right_choice]]
            active = [cell for cell in cells
                      if cell[4] in active_names
                      or cell[4] in (alternatives[left_choice][4],
                                     alternatives[right_choice][4])]
            candidates = []
            for index, first in enumerate(active):
                for second in active[index + 1:]:
                    first_edge, second_edge = first[:2], second[:2]
                    common = set(first_edge) & set(second_edge)
                    if not common or first_edge == second_edge:
                        continue
                    shared_site = next(iter(common))
                    first_head = first[2] if shared_site == first[0] else first[3]
                    second_head = second[2] if shared_site == second[0] else second[3]
                    ranks = tuple(
                        deleted_star_rank(cells, site, deleted)
                        for deleted in (first_edge, second_edge)
                        for site in deleted
                    )
                    candidates.append({
                        "cells": [first[4], second[4]],
                        "deleted_star_ranks": ranks,
                        "shared_heads": [first_head, second_head],
                        "distinct_head_four_good": (
                            ranks == (3, 3, 3, 3)
                            and first_head != second_head
                        ),
                    })
            require(candidates and not any(
                candidate["distinct_head_four_good"]
                for candidate in candidates
            ), f"a first companion pair unexpectedly closed {left_choice}{right_choice}")
            rank_audit.append({
                "forced_literal_choice": left_choice + right_choice,
                "adjacent_active_pairs": candidates,
            })
    return {
        "colour2_axis_support": {
            "p2_sites": [1, 2], "s2_sites": [0, 3]},
        "row_222000": row_h,
        "row_220200": row_g,
        "forced_alternate_sets": [
            ["q23_20*q45_00", "q24_20*q35_00"],
            ["q23_02*q45_00", "q24_00*q35_20"],
        ],
        "rank_audit": rank_audit,
        "exact_consequence": (
            "the other diagonal response rows expose each crossing arm, "
            "but replace it by one of four new decorated-anchor literal "
            "products.  On the strict envelope no one of the four 2x2 "
            "choices is already a distinct-head four-good pair"
        ),
    }


def audit_cross_colour_companion_units():
    """Close the strict bistar chart by its colour-one companion rows."""
    e, g, h, tail = edge(0, 1), edge(0, 2), edge(1, 3), edge(4, 5)
    q0 = tuple(sorted((e, edge(2, 4), edge(3, 5))))
    q1 = tuple(sorted((e, edge(2, 3), tail)))
    q2 = tuple(sorted((g, h, tail)))
    anchor_union = set(q0) | set(q1) | set(q2)

    row_112000 = typed_response_terms(
        anchor_union, (1, 1, 2, 0, 0, 0), 1, (0, 3), (1, 2))
    row_110200 = typed_response_terms(
        anchor_union, (1, 1, 0, 2, 0, 0), 1, (0, 3), (1, 2))
    expected_112000 = tuple(sorted((
        tuple(sorted(("p1_0", "s1_1", "q23_20", "q45_00"))),
        tuple(sorted(("p1_0", "s1_1", "q24_20", "q35_00"))),
    )))
    expected_110200 = tuple(sorted((
        tuple(sorted(("p1_0", "s1_1", "q23_02", "q45_00"))),
        tuple(sorted(("p1_0", "s1_1", "q24_00", "q35_20"))),
    )))
    require(row_112000 == expected_112000
            and row_110200 == expected_110200,
            "the colour-one diagonal companion rows changed")

    row_222000 = polynomial_from_terms(response_terms(
        anchor_union, (2, 2, 2, 0, 0, 0)))
    row_220200 = polynomial_from_terms(response_terms(
        anchor_union, (2, 2, 0, 2, 0, 0)))
    companion_112000 = polynomial_from_terms(row_112000)
    companion_110200 = polynomial_from_terms(row_110200)
    colour1_factor = multiply(variable("p1_0"), variable("s1_1"))
    shared_colour2_factor = multiply(variable("p2_1"), variable("s2_0"))

    certificate_h = add(
        (multiply(colour1_factor, row_222000), 1),
        (multiply(shared_colour2_factor, companion_112000), -1),
    )
    expected_h = multiply(
        colour1_factor, variable("p2_2"), variable("s2_0"),
        variable("q13_20"), variable("q45_00"))
    require(certificate_h == expected_h,
            f"the 222000/112000 source identity changed: {certificate_h}")

    certificate_g = add(
        (multiply(colour1_factor, row_220200), 1),
        (multiply(shared_colour2_factor, companion_110200), -1),
    )
    expected_g = multiply(
        colour1_factor, variable("p2_1"), variable("s2_3"),
        variable("q02_20"), variable("q45_00"))
    require(certificate_g == expected_g,
            f"the 220200/110200 source identity changed: {certificate_g}")

    return {
        "colour1_axis_support": {"p1_sites": [0, 3],
                                 "s1_sites": [1, 2]},
        "row_112000": row_112000,
        "row_110200": row_110200,
        "ordinary_source_identities": [
            (
                "(p1_0*s1_1)G222000-(p2_1*s2_0)G112000="
                "p1_0*s1_1*p2_2*s2_0*q13_20*q45_00"
            ),
            (
                "(p1_0*s1_1)G220200-(p2_1*s2_0)G110200="
                "p1_0*s1_1*p2_1*s2_3*q02_20*q45_00"
            ),
        ],
        "localized_factors": [
            "p1_0", "s1_1", "p2_1", "p2_2", "s2_0", "s2_3",
            "q02_20", "q13_20", "q45_00",
        ],
        "strict_chart_verdict": (
            "both identities have localized monomial right sides, so the "
            "endpoint-support-complete strict K2,2 chart is empty before "
            "any decorated-anchor exchange branch is chosen"
        ),
        "outside_port_scope": (
            "7114577 routes every additional outside endpoint component "
            "to an active distinct-head wedge, so it is not a survivor of "
            "this strict endpoint-support-complete chart"
        ),
    }


def audit_nonlinear_pivot_correction():
    # C=A+B is a unit in the localized residual because
    # e*C+g*h*T=0 and e,g,h,T are units.  The exact implicit correction
    # preserves that unary row for arbitrary finite dg,dh.
    samples = []
    for dg, dh in ((Q(1, 2), Q(1, 3)), (Q(-2), Q(3, 5)),
                   (Q(4, 7), Q(-5, 9))):
        e, g, h, tail, aggregate = Q(1), Q(1), Q(1), Q(1), Q(-1)
        require(e * aggregate + g * h * tail == 0,
                "the normalized terminal row stopped vanishing")
        corrected_e = e - tail * (g * dh + h * dg + dg * dh) / aggregate
        corrected_row = (corrected_e * aggregate
                         + (g + dg) * (h + dh) * tail)
        require(corrected_row == 0,
                "the exact nonlinear pivot correction changed")

        # Normalize the two displayed response rows with all selected star
        # factors and T equal to one, U=V=-1.  The pivot e is absent from
        # both rows, so its nonlinear correction cannot remove their first
        # defects: they are exactly dh and dg.
        p21 = p22 = s20 = s23 = Q(1)
        u_aggregate = v_aggregate = Q(-1)
        row_h_before = (p22 * s20 * h * tail
                        + p21 * s20 * u_aggregate)
        row_g_before = (p21 * s23 * g * tail
                        + p21 * s20 * v_aggregate)
        row_h_after = (p22 * s20 * (h + dh) * tail
                       + p21 * s20 * u_aggregate)
        row_g_after = (p21 * s23 * (g + dg) * tail
                       + p21 * s20 * v_aggregate)
        require((row_h_before, row_g_before) == (0, 0)
                and row_h_after == dh and row_g_after == dg,
                "the first response defects changed")

        # Reciprocal star rescaling can hide those two defects, but changes
        # the two selected diagonal target contributions.  This is exactly
        # the upstream affine target-line/joint-kernel issue, not a free
        # source modification.
        corrected_p22 = p22 * h / (h + dh)
        corrected_s23 = s23 * g / (g + dg)
        require(corrected_p22 * (h + dh) == p22 * h
                and corrected_s23 * (g + dg) == s23 * g,
                "the reciprocal response correction changed")
        target_before = p22 + s23
        target_after = corrected_p22 + corrected_s23
        require(target_after != target_before,
                "the sample reciprocal correction accidentally preserved target")
        samples.append({
            "dg": str(dg), "dh": str(dh),
            "corrected_e": str(corrected_e),
            "unary_residual": str(corrected_row),
            "response_defects": [str(row_h_after), str(row_g_after)],
            "target_before_after_reciprocal_star_fix": [
                str(target_before), str(target_after)],
        })
    return {
        "localized_unit": "C=A+B=-g*h*T/e",
        "exact_unary_correction": (
            "de=-T*(g*dh+h*dg+dg*dh)/C"
        ),
        "first_uncancelled_rows": {
            "222000": "p2_2*s2_0*T*dh",
            "220200": "p2_1*s2_3*T*dg",
        },
        "pivot_visibility": (
            "q01_22 is absent from both response coefficients, so the exact "
            "unary pivot correction cannot cancel either defect"
        ),
        "reciprocal_star_fix_boundary": (
            "rescaling p2_2 and s2_3 can keep the selected mixed products "
            "fixed, but changes the diagonal target contributions unless a "
            "joint-kernel/affine-fibre correction is supplied"
        ),
        "samples": samples,
    }


def audit_switch_spaces():
    e, g, h = edge(0, 1), edge(0, 2), edge(1, 3)
    star0 = {e, g}
    star1 = {e, h}
    require(set.intersection(*map(set, star0)) == {0}
            and set.intersection(*map(set, star1)) == {1},
            "an endpoint switch space stopped being one-star")
    require(not set(g) & set(h),
            "the two crossing arms unexpectedly acquired a common site")
    return {
        "site0_linear_switch_edges": sorted(star0),
        "site1_linear_switch_edges": sorted(star1),
        "shared_coordinate": e,
        "crossing_arms_are_disjoint": True,
        "coefficient_dependence": {
            "site0_transfer_coefficient": "q13_20*q45_00",
            "site1_transfer_coefficient": "q02_20*q45_00",
        },
        "failure_of_one_global_coefficient_ring": (
            "freezing the site-0 star leaves q14_20 fixed, and freezing the "
            "site-1 star leaves q02_10 fixed; a recurrence using both stars "
            "cannot freeze both coefficients while varying both arms"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "literal_return_row": audit_literal_return_row(),
        "bistar_curvature": audit_mixed_second_difference(),
        "diagonal_response_exposure": audit_diagonal_response_exposure(),
        "cross_colour_companion_units": audit_cross_colour_companion_units(),
        "nonlinear_pivot_correction": audit_nonlinear_pivot_correction(),
        "switch_space_typing": audit_switch_spaces(),
        "exact_verdict": (
            "the proposed weighted same-star SCC remains invalid, but the "
            "full strict response packet closes earlier: the colour-one "
            "companion rows cancel the two alternate aggregates and leave "
            "localized monomial source units"
        ),
        "valid_existing_scope": (
            "each endpoint exchange separately is affine-linear and remains "
            "valid.  The obstruction concerns only combining the two endpoint "
            "switch spaces into one exact finite holonomy kernel"
        ),
        "fulfilled_companion_promotion": (
            "the formerly missing rows 112000 and 110200 contain exactly "
            "the A+B and C+D aggregates with common factor p1_0*s1_1.  "
            "Combining them with 222000 and 220200 yields two ordinary "
            "localized monomial identities"
        ),
        "scope": (
            "source-labelled endpoint-support-complete strict K2,2 chart.  "
            "The SCC no-go remains a method guard; the strict chart itself "
            "is empty.  Additional outside endpoint ports are covered by "
            "the pinned 7114577 wedge theorem"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"terminal bistar-curvature ledger changed: {digest}")
    print("uniform Hall terminal-transfer bistar curvature promotion: PASS")
    print("individual endpoint exchanges: exact same-star linear")
    print("combined recurrence: mixed second difference dg*dh*q45_00")
    print("exact unary e-correction leaves response defects dh,dg")
    print("weighted SCC kernel is tangent-only without a quadratic correction")
    print("cross-colour companion rows give two ordinary localized units")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
