#!/usr/bin/env python3
"""Specialize the occurrence projector and isolate its first physical face.

At intrinsic response order three the matching and endpoint projectors are

    Pi_match=(A+I)/3,
    Pi_end=(B+2I)(B-2I)(B-4I)/240.

Their composition sends a marked occurrence to the constant vector 1/90,
so the marked delta outside the averaging operators gives c_f/90.

The first literal principal-parts face is already visible in A+I.  On the
marked residual matching 23|45 it is the six-term derivative of

    q23*q45+q24*q35+q25*q34.

It is target zero, but it belongs to the pointed fixed-endpoint response
fibre and has central-Eq incidence zero.  The later endpoint moves are the
actual site-transposition/two-root-Weyl Cartan paths.  Their marked target
normal is computed explicitly; after a moving-target correction, their
one-endpoint product-rule faces still have central-Eq incidence zero.

Thus the coefficient projector can have the correct c_f and P_f shadows,
but endpoint/matching totalization alone cannot produce the source-labelled
central placement Phi_orb((H0-u)e_Eq)=R_E14.  The latter raises rank by one
in the exact forgetful quotient.  This is a scoped source-domain obstruction,
not yet a physical Fredholm terminal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(6))
WORD = (1, 1, 0, 0, 0, 0)
N = 90
PINS = {
    "computations/verify_uniform_centered_occurrence_endpoint_association_projector.py":
        "0ef88312cead100120e4600ea3a2d0616262a96bf27726d07817610d11b43f59",
    "notes/uniform-centered-occurrence-endpoint-association-projector.md":
        "6be3edc16be3b429f517fe007886fd3289281f8e8acdde1f13ebebf2a20bb836",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_e14_t12_orbit_unary_companion_cycle_gate.py":
        "28a0baf3e6930e9336ceb5632e0abb8509a21ddaa1446eb7e93482831c35bc42",
    "notes/h3-e14-t12-orbit-unary-companion-cycle-gate.md":
        "9d04e359afb3a47b4e547797a00c29f7559a060aa51a69fdda984c0e988f2765",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "notes/h3-scaled-occurrence-anchor-bridge-alternative.md":
        "d89d40b3ff69e0d7dc8105b1aa1eea40dceabc84007c1b9759d1a2932ecba572",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
}
EXPECTED_LEDGER_SHA256 = (
    "6c5c70dab6c3213e8e4c02680b55c4eb1a0180b6c6f85980bb313828466ddff0"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, ("loop", left, right))
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index, right in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def occurrences() -> tuple[tuple[object, ...], ...]:
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == N,
            "the h3 occurrence inventory changed")
    return tuple(answer)


def matching_neighbors(matching: tuple[tuple[int, int], ...]):
    require(len(matching) == 2, ("not h3 residual matching", matching))
    (a, b), (c, d) = matching
    return (
        tuple(sorted((edge(a, c), edge(b, d)))),
        tuple(sorted((edge(a, d), edge(b, c)))),
    )


def endpoint_neighbors(occurrence: tuple[object, ...]):
    p_site, s_site, matching = occurrence
    answer = []
    for selected in SITES:
        if selected in (p_site, s_site):
            continue
        mate = next(other for pair in matching if selected in pair
                    for other in pair if other != selected)
        remainder = tuple(pair for pair in matching if selected not in pair)
        answer.append((selected, s_site,
                       tuple(sorted(remainder + (edge(p_site, mate),)))))
        answer.append((p_site, selected,
                       tuple(sorted(remainder + (edge(s_site, mate),)))))
    require(len(answer) == len(set(answer)) == 8,
            ("endpoint degree changed", occurrence))
    return tuple(answer)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * value for value in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
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


def unit(index: int, size: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(size))


def apply_matching(vector, values, lookup):
    return tuple(sum(vector[lookup[(item[0], item[1], neighbor)]]
                     for neighbor in matching_neighbors(item[2]))
                 for item in values)


def apply_endpoint(vector, values, lookup):
    return tuple(sum(vector[lookup[neighbor]]
                     for neighbor in endpoint_neighbors(item))
                 for item in values)


def coefficient_projector_audit() -> dict[str, object]:
    values = occurrences()
    lookup = {value: index for index, value in enumerate(values)}
    marked = (0, 1, ((2, 3), (4, 5)))
    marked_index = lookup[marked]
    delta = unit(marked_index, N)
    ones = (Q(1),) * N

    matching_numerator = add(apply_matching(delta, values, lookup), delta)
    expected_hole = tuple(Q(
        item[0] == 0 and item[1] == 1
    ) for item in values)
    require(matching_numerator == expected_hole
            and sum(matching_numerator, Q(0)) == 3,
            "(A+I)e_f stopped being the fixed-endpoint matching fibre")

    # A and B commute on all ninety basis vectors, not only the marked one.
    for index in range(N):
        basis = unit(index, N)
        require(apply_endpoint(apply_matching(basis, values, lookup),
                               values, lookup)
                == apply_matching(apply_endpoint(basis, values, lookup),
                                  values, lookup),
                ("A and B stopped commuting", index))

    endpoint_numerator = matching_numerator
    factor_records = []
    for root in (-2, 2, 4):
        endpoint_numerator = add(
            apply_endpoint(endpoint_numerator, values, lookup),
            scale(-root, endpoint_numerator),
        )
        factor_records.append({
            "root": root,
            "support": sum(bool(value) for value in endpoint_numerator),
            "mass": str(sum(endpoint_numerator, Q(0))),
        })
    require(endpoint_numerator == scale(8, ones),
            "the specialized endpoint numerator changed")
    combined_denominator = 3 * 240
    projected = scale(Q(1, combined_denominator), endpoint_numerator)
    centered = add(delta, scale(-1, projected))
    require(projected == scale(Q(1, N), ones)
            and scale(N, centered)
                == add(scale(N, delta), scale(-1, ones)),
            "Pi_end Pi_match stopped producing c_f/90")
    return {
        "intrinsic_response_order": 3,
        "occurrences": N,
        "marked_occurrence": [0, 1, [[2, 3], [4, 5]]],
        "matching_adjacency_degree": 2,
        "endpoint_adjacency_degree": 8,
        "Pi_match": "(A+I)/3",
        "Pi_end": "(B+2I)(B-2I)(B-4I)/240",
        "combined_denominator": combined_denominator,
        "matching_first_top": "b_01=sum_R e_(0,1;R)",
        "endpoint_factor_records": factor_records,
        "combined_numerator_on_e_f": "8*1_90",
        "combined_projector_on_e_f": "1_90/90",
        "centered_output": "e_f-1_90/90=c_f/90",
        "A_B_commute_on_all_basis_occurrences": True,
    }


def derivative_of_matching_fibre_audit() -> dict[str, object]:
    # The fixed-endpoint fibre has coefficient polynomial
    # p_0 s_1 (q23 q45+q24 q35+q25 q34).  Its ordinary first PP face has
    # the six displayed terms.  Keep dq as a literal labelled generator.
    monomials = (
        ("q23:00", "q45:00"),
        ("q24:00", "q35:00"),
        ("q25:00", "q34:00"),
    )
    derivative_terms = []
    for left, right in monomials:
        derivative_terms.append(("d" + left, right))
        derivative_terms.append((left, "d" + right))
    require(len(derivative_terms) == len(set(derivative_terms)) == 6,
            "the fixed-hole first Hasse face changed")

    # Every residual site has output colour zero, so the two matching
    # switches are literal zero-colour site permutations and have no GHZ
    # target normal.  They also live entirely in the response summand.
    marked = (0, 1, ((2, 3), (4, 5)))
    neighbors = tuple((0, 1, value)
                      for value in matching_neighbors(marked[2]))
    require(neighbors == (
        (0, 1, ((2, 4), (3, 5))),
        (0, 1, ((2, 5), (3, 4))),
    ), "the marked matching switches changed")
    return {
        "response_head_word": "11:110000",
        "endpoint_factor": "p1_0_1*s1_1_1",
        "matching_polynomial": (
            "q23:00*q45:00+q24:00*q35:00+q25:00*q34:00"
        ),
        "first_PP_face_terms": [list(term) for term in derivative_terms],
        "first_PP_face_count": len(derivative_terms),
        "marked_matching_neighbors": [repr(value) for value in neighbors],
        "target_readout": 0,
        "central_Eq_input_incidence": 0,
        "cap_scalar_ores": 0,
        "anchor_status": (
            "a fixed-endpoint occurrence-conormal face, not yet the global "
            "scaled anchor law"
        ),
        "physical_six_term_q_status": (
            "literal dq-labelled PP face; not the six-term generator "
            "readout or its terminal alternative"
        ),
        "source_validity_obstruction": (
            "the complete response row is the sum over all 30 ordered "
            "endpoint fibres.  Selecting b_01 is precisely pointed "
            "occurrence localization, not an old complete source row"
        ),
    }


def target_unit(word: tuple[int, ...], basis):
    return unit(basis.index(word), len(basis))


def two_root_target_defect(left_site: int, right_site: int, basis):
    left_colour = WORD[left_site]
    right_colour = WORD[right_site]
    if left_colour == right_colour:
        return (Q(0),) * len(basis)
    images = []
    for colour in range(3):
        value = [colour] * 6
        for site in (left_site, right_site):
            if value[site] == left_colour:
                value[site] = right_colour
            elif value[site] == right_colour:
                value[site] = left_colour
        images.append(target_unit(tuple(value), basis))
    delta = add(*(target_unit((colour,) * 6, basis)
                  for colour in range(3)))
    return add(*images, scale(-1, delta))


def endpoint_first_face_audit() -> dict[str, object]:
    basis = tuple(product(range(3), repeat=6))
    marked = (0, 1, ((2, 3), (4, 5)))
    moves = []
    total_normal = (Q(0),) * len(basis)
    for endpoint in (0, 1):
        for selected in (2, 3, 4, 5):
            mate = next(other for pair in marked[2] if selected in pair
                        for other in pair if other != selected)
            remainder = tuple(pair for pair in marked[2]
                              if selected not in pair)
            if endpoint == 0:
                neighbor = (selected, 1,
                            tuple(sorted(remainder + (edge(0, mate),))))
            else:
                neighbor = (0, selected,
                            tuple(sorted(remainder + (edge(1, mate),))))
            defect = two_root_target_defect(endpoint, selected, basis)
            require(any(defect), "a marked endpoint move became target safe")
            total_normal = add(total_normal, defect)
            moves.append({
                "endpoint_move": f"{endpoint}->{selected}",
                "site_transposition": f"({endpoint} {selected})",
                "two_root_Weyl_colours": [1, 0],
                "neighbor": repr(neighbor),
                "first_product_face": (
                    f"d z_f tensor H_({endpoint},{selected})"
                ),
                "central_Eq_input_incidence": 0,
            })

    expected = (Q(0),) * len(basis)
    expected = list(expected)
    for endpoint in (0, 1):
        for selected in (2, 3, 4, 5):
            one_pair = [0] * 6
            one_pair[endpoint] = one_pair[selected] = 1
            zero_pair = [1] * 6
            zero_pair[endpoint] = zero_pair[selected] = 0
            expected[basis.index(tuple(one_pair))] += 1
            expected[basis.index(tuple(zero_pair))] += 1
    expected[basis.index((0,) * 6)] -= 8
    expected[basis.index((1,) * 6)] -= 8
    expected = tuple(expected)
    require(total_normal == expected
            and sum(bool(value) for value in total_normal) == 18,
            "the marked h3 endpoint target normal changed")
    mixed_dual = target_unit((1, 0, 1, 0, 0, 0), basis)
    delta = add(*(target_unit((colour,) * 6, basis)
                  for colour in range(3)))
    require(dot(mixed_dual, delta) == 0
            and dot(mixed_dual, total_normal) == 1,
            "the h3 mixed target-normal detector changed")
    sparse = {
        "".join(map(str, word)): str(value)
        for word, value in zip(basis, total_normal, strict=True) if value
    }
    return {
        "marked_endpoint_move_count": len(moves),
        "moves": moves,
        "marked_endpoint_target_normal": sparse,
        "target_normal_formula": (
            "sum_(x in {0,1},t in {2,3,4,5}) "
            "(X_(ones at x,t)+X_(zeros at x,t))-8X_000000-8X_111111"
        ),
        "target_normal_support": len(sparse),
        "primitive_mixed_target_detector": "X_101000^*",
        "detector_on_Delta": 0,
        "detector_on_normal": 1,
        "moving_target_cone_can_absorb_normal": True,
        "after_target_correction_first_face": (
            "the eight path-labelled d z_f tensor H_(x,t) terms"
        ),
        "first_face_central_Eq_input_incidence": 0,
    }


def central_eq_incidence_audit() -> dict[str, object]:
    # Rows are (pointed P_f, primitive cap p, private occurrence R,
    # central Eq-input incidence, shifted ridge).  Give the endpoint/matching
    # totalization every benefit and retain its optimistic P_f shadow.
    projector_face = (Q(1), Q(0), Q(0), Q(0), Q(0))
    primitive_cap = (Q(0), Q(1), Q(0), Q(0), Q(0))
    orbit_D4_top = (Q(0), Q(0), Q(1), Q(0), Q(0))
    horizontal_cap_graph = (Q(0),) * 5
    required_placement = (Q(0), Q(0), Q(1), Q(1), Q(0))
    central_eq_dual = (Q(0), Q(0), Q(0), Q(1), Q(0))
    old = (projector_face, primitive_cap, orbit_D4_top,
           horizontal_cap_graph)
    require(rank(old) == 3 and rank(old + (required_placement,)) == 4
            and all(dot(central_eq_dual, column) == 0 for column in old)
            and dot(central_eq_dual, required_placement) == 1,
            "the projector/central-Eq quotient changed")

    # P_f and p are independent homogeneous faces.  Neither an endpoint nor
    # a residual-matching move changes the source-row label to the central Eq
    # generator; all their PP/Hasse faces therefore have Eq incidence zero.
    require(rank((projector_face, primitive_cap)) == 2,
            "P_f and p stopped being independent")
    return {
        "forgetful_rows": [
            "pointed conormal P_f", "primitive cap p",
            "private occurrence R_E14", "central Eq-input E",
            "shifted ridge gamma",
        ],
        "optimistic_full_projector_first_face": [1, 0, 0, 0, 0],
        "primitive_cap": [0, 1, 0, 0, 0],
        "orbit_D4_top": [0, 0, 1, 0, 0],
        "required_Phi_orb_E_to_R": [0, 0, 1, 1, 0],
        "rank_before_after_required_placement": [3, 4],
        "primitive_missing_dual": [0, 0, 0, 1, 0],
        "endpoint_matching_moves_supply_central_Eq_incidence": False,
        "reason": (
            "actual site Cartan, matching-switch, and their Hasse faces "
            "remain in the response/bar source summand; coefficient or "
            "target transport does not change the source-row label to e_Eq"
        ),
        "exact_missing_comparison": (
            "Phi_orb((H0-u)e_Eq)=R_E14 with full source labels"
        ),
        "T12_after_comparison": "closed by the old unary row (C=U, Z=0)",
        "cap_scope": (
            "p/z_cap remains a distinct homogeneous face unless the same "
            "augmented comparison schema explicitly carries its cap residue"
        ),
    }


def typing_and_terminal_audit() -> dict[str, object]:
    return {
        "bottom_response_grade": {
            "head_word": "11:110000",
            "marked_term": (
                "(p1_0_1*s1_1_1)q23:00*q45:00"
            ),
            "first_matching_PP_order": 1,
        },
        "primitive_cap_grade": {
            "word": "01211222",
            "fine": "t*q_(v,N)",
            "repeated": "P3+K2",
            "central_Eq_incidence": 0,
        },
        "D4_grade": {
            "word_arrow": "110000 -> 111111",
            "top_occurrence": "R_E14=g on v04=0",
            "central_Eq_incidence": 0,
        },
        "required_central_grade": {
            "domain": "E=(H0-u)e_Eq",
            "codomain": "R_E14 in the canonical E14 placement grade",
            "central_Eq_incidence": 1,
        },
        "target": (
            "matching first face is target zero; endpoint Cartan normal is "
            "the explicit 18-word packet and requires the moving-target cone"
        ),
        "anchor": (
            "a physical c_f/P_f face gives the sufficient scaled law "
            "90[du_f]=[du], but does not identify the central Eq source row"
        ),
        "physical_q": (
            "the first face is dq-labelled; the complete physical six-term "
            "q generator/separator alternative still requires the augmented "
            "source-labelled comparison"
        ),
        "terminal_extension_test": {
            "local_dual": "central Eq-input incidence",
            "kills_endpoint_matching_and_orbit_D4": True,
            "reads_required_placement": 1,
            "already_a_physical_Fredholm_terminal": False,
            "why_not": (
                "it is a source-domain incidence covector, not an accepted "
                "output/anchor/q/ridge readout.  It must extend across the "
                "complete word/fine/target/anchor/q/W/eta/sigma matrix"
            ),
            "exact_complete_alternative": (
                "in the complete augmented matrix J, either the E->R column "
                "is in im(J), or a full left covector annihilates J and "
                "reads that column nonzero"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": (
            "h3 centered endpoint/matching projector literal first-Hasse / "
            "central-Eq incidence gate"
        ),
        "pins": PINS,
        "specialized_coefficient_projector": coefficient_projector_audit(),
        "first_matching_Hasse_face": derivative_of_matching_fibre_audit(),
        "endpoint_Cartan_first_face": endpoint_first_face_audit(),
        "central_Eq_incidence": central_eq_incidence_audit(),
        "physical_typing_and_terminal": typing_and_terminal_audit(),
        "verdict": (
            "At h=3, Pi_end Pi_match is exactly (B+2)(B-2)(B-4)(A+I)/720 "
            "and sends e_f to 1/90, so its coefficient shadow gives c_f. "
            "The first literal PP face is the six-term derivative of the "
            "fixed-endpoint K4 matching fibre.  Endpoint stages add the "
            "explicit 18-word target normal and path-labelled one-endpoint "
            "faces.  Even granting target correction and an optimistic P_f "
            "collapse, every endpoint/matching face has central-Eq incidence "
            "zero.  The required source-labelled E->R placement raises the "
            "forgetful rank by one.  Hence the projector does not yet give a "
            "source-valid centered comparison; its sharp first cross-summand "
            "obstruction is central Eq incidence, not T12"
        ),
        "shortest_positive_theorem": (
            "construct one augmented source-labelled totalization whose "
            "bottom is the fixed-endpoint six-term Hasse face, whose endpoint "
            "Cartan target normal is absorbed by the moving target, and whose "
            "mixed comparison face has Phi_orb((H0-u)e_Eq)=R_E14.  Then the "
            "old unary row closes T12; cap/ridge/q close only to the extent "
            "that the same augmented schema carries their separately typed "
            "faces"
        ),
        "scope": (
            "exact rational coefficient and first-principal-parts audit for "
            "the canonical h=3 marked 11:110000 packet.  It does not promote "
            "the central-Eq incidence dual to a terminal, construct the full "
            "mixed comparison, or claim that coefficient correspondences "
            "are source maps"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("first-Hasse/Eq-incidence ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 Pi_end Pi_match: e_f -> 1_90/90 (EXACT)")
    print("first literal PP face: fixed-endpoint six-term K4 derivative")
    print("marked endpoint target normal: 18-word packet")
    print("endpoint/matching central Eq incidence: ZERO")
    print("required E->R central Eq incidence: ONE (OPEN)")
    print("T12 after E->R: CLOSED BY OLD UNARY")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
