#!/usr/bin/env python3
"""Audit physical same-grade access to the centered occurrence class.

At intrinsic response order h there are 2h selected sites and

    N_h = 2h(2h-1)(2h-3)!!

literal response occurrences.  The scaled anchor bridge is therefore
N_h[du_f]=[du], conditional on physical descent of
c_{f,h}=N_h e_f-sum_M e_M.  The h=3 selected mixed response word 110000
has N_3=90 literal occurrences.  Its
word stabilizer has five occurrence orbits of sizes 6,24,24,12,24; the
marked occurrence lies in the six-element orbit.  Complete response rows,
target-compatible diagonal stabilizers, and word-preserving permutation
bars have only the total orbit-sum image in the selected head/word block.
Response-head differences live in direct-sum blocks and have the same
one-dimensional projection.

Uniformly, c_{f,h} has two independent debts already in the coarse word
module: a marked-within-six-orbit class and an orbit-marginal class.  The
six is 2(2h-3)!! at general h.  The raw relative occurrence projector has
nonzero scalar face N_h*f(x), so it
does not promote them to a source-valid cell.  Explicit centered covectors
detect both debts but are occurrence selectors, not physically typed
terminals.  Fixed-pair spectator extension does not carry c_{f,h}, even
modulo the complete row, to c_{f,h+1}.  Once a same-grade physical cell and
a uniform physical q readout are supplied, the existing
zero-indeterminacy/relative-generator theorem is exhaustive on the h=3
packet; its terminal promotion and simultaneous-face-zero routing remain
separate clauses of PAComp(h).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
N = 90
SITES = tuple(range(6))
WORD = (1, 1, 0, 0, 0, 0)
PINS = {
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py":
        "403819751753802f4bb01b07cca2540fc6abf0479b9be5569ee74f414ea667ad",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
    "computations/verify_h3_component_iv_face_zero_routing_boundary.py":
        "217d14b451a36b6e86caadf14bd5ce63aeda484f8e0917b7f2e1034b640a4fc0",
    "computations/verify_global_assembly_after_h3_master_comparison_scope.py":
        "90030edac855fe4fd85abd5db55354bee2121b3a4d8c6c023e4b0e639f5f0c93",
}
EXPECTED_LEDGER_SHA256 = "bea8d7cf46c393fe352dc553dcbb54f987dba8597290abb038135aaae3c08a73"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def odd_double_factorial(value: int) -> int:
    require(value >= -1 and value % 2 == 1,
            ("odd double factorial received a bad argument", value))
    answer = 1
    while value > 0:
        answer *= value
        value -= 2
    return answer


def uniform_occurrence_audit():
    records = []
    for h in range(3, 21):
        sites = 2 * h
        zeros = sites - 2
        residual_matchings = odd_double_factorial(sites - 3)
        occurrence_count = sites * (sites - 1) * residual_matchings
        marked_orbit = 2 * residual_matchings
        ratio = h * (2 * h - 1)

        # Five S_2 x S_(2h-2) orbit types: both distinguished endpoints;
        # distinguished/zero in either orientation; two zero endpoints with
        # the residual distinguished sites paired; and two zero endpoints
        # with the distinguished sites split.
        orbit_sizes = (
            marked_orbit,
            2 * zeros * residual_matchings,
            2 * zeros * residual_matchings,
            zeros * (zeros - 1) * odd_double_factorial(zeros - 3),
            zeros * (zeros - 1) * (zeros - 2)
            * odd_double_factorial(zeros - 3),
        )
        require(sum(orbit_sizes) == occurrence_count,
                ("uniform orbit census changed", h, orbit_sizes,
                 occurrence_count))
        require(occurrence_count == ratio * marked_orbit,
                ("uniform marked-orbit ratio changed", h))

        # c_h = r_h(s_h e_f-1_O)+((r_h-1)1_O-1_Oc).
        # It has two independent centered components for every h>=3.
        # Check on the three coefficient strata f, O\{f}, O^c rather
        # than allocating the enormous occurrence module at large h.
        full_profile = (occurrence_count - 1, -1, -1)
        local_profile = (marked_orbit - 1, -1, 0)
        marginal_profile = (ratio - 1, ratio - 1, -1)
        reconstructed = tuple(
            ratio * local_profile[index] + marginal_profile[index]
            for index in range(3)
        )
        require(reconstructed == full_profile,
                ("uniform centered decomposition changed", h))
        require((marked_orbit - 1) + (marked_orbit - 1) * (-1) == 0
                and marked_orbit * (ratio - 1)
                - (occurrence_count - marked_orbit) == 0,
                ("uniform centered augmentation changed", h))
        require(rank(((1, 1, 1), local_profile, marginal_profile)) == 3,
                ("uniform centered debts ceased to be independent", h))

        records.append({
            "h": h,
            "selected_sites": sites,
            "ambient_descent_order": sites + 2,
            "N_h": occurrence_count,
            "marked_orbit_size_s_h": marked_orbit,
            "ratio_r_h": ratio,
            "five_orbit_sizes": list(orbit_sizes),
            "scaled_anchor_law": f"{occurrence_count}[du_f]=[du]",
        })
    require(records[0]["N_h"] == N
            and records[0]["five_orbit_sizes"] == [6, 24, 24, 12, 24],
            "the uniform census lost its h=3 specialization")
    return {
        "formula": "N_h=2h(2h-1)(2h-3)!!",
        "selected_response_sites": "2h (ambient descent order 2h+2)",
        "marked_orbit": "s_h=2(2h-3)!!",
        "ratio": "r_h=N_h/s_h=h(2h-1)",
        "decomposition": (
            "c_f,h=r_h(s_h e_f-1_O)+((r_h-1)1_O-1_Oc)"
        ),
        "scaled_bridge_identity": (
            "N_h z_f-u=(N_h z_f-sum_M z_M)+(sum_M z_M-u)"
        ),
        "characteristic_zero_consequence": (
            "physical descent of c_f,h gives N_h[du_f]=[du], which is "
            "equivalent to anchor visibility because N_h is a unit"
        ),
        "orders_checked": records,
    }


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


def occurrences():
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in SITES
                         if site not in (p_site, s_site))
            for matching in perfect_matchings(rest):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == N,
            "the response occurrence inventory changed")
    return tuple(answer)


def word_stabilizer():
    answer = []
    for first in permutations((0, 1)):
        for second in permutations((2, 3, 4, 5)):
            image = dict(zip((0, 1), first, strict=True))
            image.update(dict(zip((2, 3, 4, 5), second, strict=True)))
            answer.append(tuple(image[site] for site in SITES))
    require(len(answer) == 48, "the word stabilizer order changed")
    return tuple(answer)


def act(occurrence, permutation):
    p_site, s_site, matching = occurrence
    return (
        permutation[p_site],
        permutation[s_site],
        tuple(sorted(edge(permutation[left], permutation[right])
                     for left, right in matching)),
    )


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(vectors):
    basis = {}
    for original in vectors:
        values = [Q(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                values = [left - coefficient * right for left, right in
                          zip(values, basis[pivot], strict=True)]
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def unit(index, size=N):
    answer = [Q(0)] * size
    answer[index] = Q(1)
    return tuple(answer)


def occurrence_orbit_audit():
    occ = occurrences()
    lookup = {value: index for index, value in enumerate(occ)}
    group = word_stabilizer()
    unseen = set(range(N))
    orbits = []
    while unseen:
        index = min(unseen)
        orbit = frozenset(lookup[act(occ[index], permutation)]
                          for permutation in group)
        orbits.append(tuple(sorted(orbit)))
        unseen.difference_update(orbit)
    sizes = sorted(len(orbit) for orbit in orbits)
    require(sizes == [6, 12, 24, 24, 24],
            ("the fixed-word occurrence orbits changed", sizes))

    marked_occurrence = (0, 1, ((2, 3), (4, 5)))
    marked_index = lookup[marked_occurrence]
    marked_orbit = next(orbit for orbit in orbits if marked_index in orbit)
    require(len(marked_orbit) == 6,
            "the marked both-one endpoint orbit changed")

    orbit_records = []
    for orbit in sorted(orbits, key=lambda values: (len(values), values)):
        representative = occ[orbit[0]]
        p_site, s_site, matching = representative
        orbit_records.append({
            "size": len(orbit),
            "endpoint_colours": [WORD[p_site], WORD[s_site]],
            "residual_matching": [list(pair) for pair in matching],
            "contains_marked": marked_index in orbit,
        })
    return occ, group, marked_index, marked_orbit, tuple(orbits), orbit_records


def complete_operation_image_audit(occ, group, orbits):
    ones = (Q(1),) * N
    lookup = {value: index for index, value in enumerate(occ)}

    # Every word-preserving permutation fixes the complete response sum.
    permuted_rows = []
    for permutation in group:
        row = [Q(0)] * N
        for occurrence in occ:
            row[lookup[act(occurrence, permutation)]] += 1
        row = tuple(row)
        require(row == ones, "a word permutation split the complete row")
        permuted_rows.append(row)

    # Every occurrence uses each output site exactly once with the word's
    # colour, so all target-compatible diagonal stabilizers have one common
    # character.  Record the common incidence profile directly.
    incidence_profiles = []
    for p_site, s_site, matching in occ:
        incidence = [0] * (6 * 3)
        incidence[3 * p_site + WORD[p_site]] += 1
        incidence[3 * s_site + WORD[s_site]] += 1
        for left, right in matching:
            incidence[3 * left + WORD[left]] += 1
            incidence[3 * right + WORD[right]] += 1
        incidence_profiles.append(tuple(incidence))
    require(len(set(incidence_profiles)) == 1,
            "the fixed-word occurrences acquired different torus characters")

    # Response-head rows are independent complete blocks.  Differences of
    # four heads project to multiples of ones in the selected head block.
    blocks = 4
    complete_heads = []
    for head in range(blocks):
        row = [Q(0)] * (blocks * N)
        row[head * N:(head + 1) * N] = ones
        complete_heads.append(tuple(row))
    head_differences = [add(complete_heads[head], scale(-1, complete_heads[0]))
                        for head in range(1, blocks)]
    selected_projections = [row[:N] for row in complete_heads + head_differences]
    require(rank(selected_projections) == 1,
            "response-head differences split the selected occurrence block")

    orbit_sums = []
    for orbit in orbits:
        row = [Q(0)] * N
        for index in orbit:
            row[index] = 1
        orbit_sums.append(tuple(row))
    require(rank(orbit_sums) == 5 and add(*orbit_sums) == ones,
            "the five orbit marginals changed")
    return {
        "complete_selected_head_row_rank": 1,
        "word_permutation_images_rank": rank(permuted_rows),
        "target_diagonal_character_profiles": len(set(incidence_profiles)),
        "response_head_blocks": blocks,
        "selected_projection_of_head_differences_rank": rank(selected_projections),
        "word_stabilizer_orbit_sum_rank": rank(orbit_sums),
        "physical_orbit_sums_individually_constructed": False,
        "coarse_to_fine_consequence": (
            "c_f is absent already after forgetting fine/repeated labels; "
            "therefore no combination of these operations can build it in "
            "the stricter literal fine grade"
        ),
    }


def centered_class_decomposition(marked, marked_orbit, orbits):
    ones = (Q(1),) * N
    e_marked = unit(marked)
    selected_sum = tuple(Q(index in marked_orbit) for index in range(N))
    other_sum = add(ones, scale(-1, selected_sum))
    c_full = add(scale(N, e_marked), scale(-1, ones))
    c_local = add(scale(len(marked_orbit), e_marked), scale(-1, selected_sum))
    c_marginal = add(scale(14, selected_sum), scale(-1, other_sum))
    require(add(scale(15, c_local), c_marginal) == c_full,
            "the local/marginal centered decomposition changed")
    require(sum(c_full, Q(0)) == sum(c_local, Q(0))
            == sum(c_marginal, Q(0)) == 0,
            "a centered class acquired augmentation")
    require(rank((ones, c_local, c_marginal)) == 3,
            "the two centered debts stopped being independent")

    local_dual = tuple(
        Q(5) if index == marked else
        Q(-1) if index in marked_orbit else Q(0)
        for index in range(N)
    )
    marginal_dual = tuple(Q(14) if index in marked_orbit else Q(-1)
                          for index in range(N))
    require(dot(local_dual, ones) == dot(marginal_dual, ones) == 0
            and dot(local_dual, c_full) == 450
            and dot(marginal_dual, c_full) == 1260,
            "the centered occurrence cokernel duals changed")
    return c_full, c_local, c_marginal, local_dual, marginal_dual, {
        "full_class": "c_f=90e_f-1_90",
        "decomposition": "c_f=15*(6e_f-1_O)+14*1_O-1_(O^c)",
        "marked_word_stabilizer_orbit_size": len(marked_orbit),
        "within_orbit_debt": "6e_f-1_O",
        "orbit_marginal_debt": "14*1_O-1_(O^c)",
        "debts_independent_mod_complete_row": True,
        "local_centered_dual_on_c_f": 450,
        "orbit_marginal_dual_on_c_f": 1260,
    }


def relative_projector_zero_face_audit(marked, c_full):
    # Normalize the active marked occurrence to one and cancel it with one
    # mate, so the complete mixed response value is zero.  The raw centered
    # operator 90*P_f-E_total returns 90, not zero.
    values = [Q(0)] * N
    values[marked] = 1
    cancellation = next(index for index in range(N) if index != marked)
    values[cancellation] = -1
    response_value = sum(values, Q(0))
    raw_marked_value = values[marked]
    centered_zero_face = N * raw_marked_value - response_value
    require(response_value == 0 and centered_zero_face == N,
            "the centered relative projector zero-face changed")
    require(dot(c_full, (Q(1),) * N) == 0,
            "the centered class stopped killing the complete coefficient row")
    return {
        "normalized_source_values": "f=1, one mate=-1, all others=0",
        "complete_response_value": 0,
        "raw_centered_projector_value": int(centered_zero_face),
        "first_unavoidable_face": "90*f(x)",
        "source_valid": False,
        "needed_correction": (
            "one same-grade physical scalar/target face cancelling 90*f(x), "
            "together with the occurrence boundary c_f"
        ),
    }


def spectator_stability_audit():
    # Embed the h=3 occurrence module into h=4 by adjoining two fixed
    # spectator sites paired to each other.  Work modulo the complete h=4
    # response row as well: lambda*i(c_3)+b*1=a*c_4 has only the zero
    # solution.  Outside the embedded support b=-a; on an embedded
    # nonmarked occurrence -lambda+b=-a forces lambda=0; the marked
    # coordinate then forces a=0.
    old_count = N
    h_new = 4
    new_count = 2 * h_new * (2 * h_new - 1) * odd_double_factorial(2 * h_new - 3)
    require(new_count == 840 and old_count < new_count,
            "the first spectator occurrence counts changed")

    embedded = [Q(0)] * new_count
    embedded[0] = old_count - 1
    for index in range(1, old_count):
        embedded[index] = -1
    new_centered = [Q(-1)] * new_count
    new_centered[0] += new_count
    complete = [Q(1)] * new_count
    require(rank((tuple(embedded), tuple(complete), tuple(new_centered))) == 3,
            "fixed-spectator extension unexpectedly carried the new center")

    return {
        "test": "h=3 to h=4 fixed-pair spectator extension",
        "embedded_support": old_count,
        "new_occurrence_count": new_count,
        "new_endpoint_or_matching_occurrences_outside_image": new_count-old_count,
        "c_hplus1_in_span_of_embedded_c_h_and_complete_row": False,
        "reason": (
            "outside the embedded support the new centered class is -1, "
            "while the embedded class is zero; comparing an embedded "
            "nonmarked coordinate and the marked coordinate rules out a "
            "repair by the complete row"
        ),
        "uniformity_verdict": (
            "centered descent is not local/spectator-stable under tensoring "
            "with one fixed matching edge; a uniform cell needs transfer "
            "over the new endpoint placements and residual matchings"
        ),
    }


def augmented_cokernel_terminal_audit(c_full, local_dual, marginal_dual):
    first_flat = (ROOT / (
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py"
    )).read_text()
    derived = (ROOT / (
        "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py"
    )).read_text()
    face_zero = (ROOT / (
        "computations/verify_h3_component_iv_face_zero_routing_boundary.py"
    )).read_text()
    global_scope = (ROOT / (
        "computations/verify_global_assembly_after_h3_master_comparison_scope.py"
    )).read_text()
    require('"physical_covector": "Lambda=sum_6 selected matching rows - ainc"'
            in first_flat
            and "arbitrary new relative generator" in first_flat,
            "the pinned physical six-term terminal scope changed")
    require("q kills ker J" in derived
            and "relative_generator" in derived
            and "physically typed terminal" in derived
            and "functional q" in derived,
            "the pinned zero-indeterminacy/generator alternative changed")
    require("physical V(h_1,...,h_5) -> all-inactive routing: NOT PROVED"
            in face_zero
            and '"simultaneous_face_zero_routing_constructed": False'
            in global_scope
            and '"q_alternative_alone_is_global_terminal": False'
            in global_scope,
            "the PAComp face-zero/terminal-promotion boundary changed")

    complete = (Q(1),) * N
    zero_terminal = (Q(0),) * N
    require(dot(local_dual, complete) == dot(marginal_dual, complete) == 0
            and dot(zero_terminal, c_full) == 0
            and dot(local_dual, c_full) and dot(marginal_dual, c_full),
            "the untyped-cokernel terminal guard changed")
    return {
        "first_coarse_cokernel_detectors": [
            "marked-within-six-orbit covector",
            "selected-orbit versus other-four-orbits marginal covector",
        ],
        "both_kill_complete_response_row": True,
        "physical_terminal_identification_constructed": False,
        "sharp_guard": (
            "the complete response row may have q/target/residue readout zero "
            "while both occurrence covectors detect c_f; abstract cokernel "
            "detection is not terminal typing"
        ),
        "existing_exhaustive_split_after_typing": (
            "for the complete augmented correction map J and physical "
            "Lambda=sum_6(m_i)-ainc: Lambda nonzero on ker J normalizes to "
            "the relative generator; Lambda killing ker J makes it descend "
            "as the Fredholm separator"
        ),
        "single_missing_terminal_clause": (
            "define Lambda on the new same-grade occurrence comparison and "
            "prove its difference from the centered marked readout is a "
            "complete protected-row coboundary"
        ),
        "uniform_PAComp_scope": {
            "h3_Lambda_dichotomy_after_physical_typing": True,
            "spectator_extension_promotes_Lambda_for_all_h": False,
            "simultaneous_deleted_face_zero_routing": False,
            "curvature_forces_a_face_open": False,
            "local_occurrence_dual_is_source_terminal": False,
            "required_clause": (
                "for every h, either construct the complete same-grade cell "
                "and identify its q/anchor dual with the source-provenant "
                "terminal quotient, or route its first nonlift there; "
                "separately cover the all-h_v-zero stratum"
            ),
        },
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    occ, group, marked, marked_orbit, orbits, orbit_records = occurrence_orbit_audit()
    operation_image = complete_operation_image_audit(occ, group, orbits)
    c_full, c_local, c_marginal, local_dual, marginal_dual, decomposition = (
        centered_class_decomposition(marked, marked_orbit, orbits)
    )
    ledger = {
        "theorem": "uniform centered occurrence same-grade physical gate",
        "pins": PINS,
        "uniform_occurrence_count": uniform_occurrence_audit(),
        "selected_response": {
            "head_word": "11:110000",
            "literal_occurrences": N,
            "word_stabilizer_order": len(group),
            "word_stabilizer_orbits": orbit_records,
        },
        "complete_operation_image": operation_image,
        "centered_class": decomposition,
        "relative_projector": relative_projector_zero_face_audit(marked, c_full),
        "spectator_stability": spectator_stability_audit(),
        "augmented_cokernel": augmented_cokernel_terminal_audit(
            c_full, local_dual, marginal_dual
        ),
        "exact_verdict": (
            "at every h the centered class uses N_h=2h(2h-1)(2h-3)!! "
            "occurrences and splits into a marked-orbit and orbit-marginal "
            "debt.  At h=3, stabilizer-induced rows, word-preserving "
            "permutation bars, and response-head differences do not build "
            "it even after forgetting fine grade.  The raw occurrence "
            "projector has scalar face N_h f(x), and fixed-pair spectator "
            "extension does not carry c_f,h modulo the complete row.  The "
            "natural occurrence duals are not yet physical terminals"
        ),
        "minimal_positive_theorem": (
            "for every h construct one source-valid same-word/fine/repeated-"
            "grade relative occurrence cell carrying c_f,h and its forced "
            "-N_h f scalar face, including transfer across all endpoint and "
            "matching orbits.  Identify its physical q/anchor readout with "
            "the source-provenant terminal quotient and cover the simultaneous "
            "deleted-face-zero stratum.  At h=3 the pinned Lambda-on-kernel "
            "dichotomy then gives either the relative generator or a descended "
            "Fredholm separator"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("centered occurrence physical-gate ledger changed", digest))
    return ledger, digest


def main():
    _, digest = audit()
    print("uniform centered occurrence same-grade physical gate: PASS")
    print("N_h=2h(2h-1)(2h-3)!!; scaled bridge N_h[du_f]=[du]")
    print("fixed-word occurrence orbits: 6,12,24,24,24")
    print("complete-row/stabilizer/head-difference image in selected block: rank 1")
    print("c_f debts: marked-within-six + orbit marginal")
    print("raw relative projector scalar face: 90*f(x)")
    print("fixed-pair spectator extension: NOT centered-class stable")
    print("uniform terminal promotion + simultaneous face-zero routing: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
