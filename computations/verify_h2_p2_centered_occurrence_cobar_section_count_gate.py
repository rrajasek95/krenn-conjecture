#!/usr/bin/env python3
"""Count the pointed occurrence sections needed by the labelled P2 cobar.

There are three different counts which must not be conflated.

* The eight first one-root word classes have three V4 word orbits, but
  transporting the marked occurrence as well as the word means that three
  seeds do not span the fixed coefficient packet.  Exact covariance-span
  calculation gives seven ambient seeds; the strict marked grade needs all
  eight word labels.
* The exact second B-4 preimage z_private has four coefficient levels with
  multiplicities 2,4,4,2.  Modulo the complete response row it therefore
  needs at least eight literal occurrence selectors, and eight suffice.
* A universal pointed-section theorem is one theorem schema, but it must be
  instantiated at those eight tags.  Fermat's labelled square then supplies
  the finite root/q cobar for every instantiated tag.

The order-two centered classes c_i=12e_i-1 give exactly these pointed
selectors modulo the complete row.  Thus the missing P2 cap is the lower
centered occurrence descent with root/q functoriality.  The h=3 primitive p
is only its aggregate projected cap and cannot replace the eight sections.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_one_root_private_orbit_bright_dark_gate.py":
        "406c4be1a72a71c6c80fdf1c1929e64dce128847d5b20a02bb95e4a8582772d0",
    "notes/h2-p2-one-root-private-orbit-bright-dark-gate.md":
        "f07de0c9e1cc6b7558bf6efa08692d9fe8960af1b6fb13c437230f90c0dfc9b0",
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "notes/h2-labelled-two-direction-occurrence-hasse-cobar-square-gate.md":
        "37b4da7bddd358d4b8d89bc80f252da9e0742d7ae8fc5eab7daedfd97c1eed7a",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "notes/uniform-centered-occurrence-restriction-insertion-gate.md":
        "c3161b740606a19d1fb238921986a6ab3b9c2f9cec9d7bc9a9410059f8c213da",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py":
        "24c5504111da4f284d9d01a535de544a44ea1bae75430d98761e093cc6ca8482",
    "notes/h2-endpoint-role-groupoid-pointed-bar-gate.md":
        "2476b8ca7974f3b5fba02905d0430565d22e9f5c863337748ae8f5eb757a8de2",
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "notes/h3-pointed-occurrence-primitive-cap-p2-propagation-gate.md":
        "c1cac29cabc30d13b4b2a30d882e1b8e01268423be7b29d7748744ebecaf60ff",
}
EXPECTED_LEDGER_SHA256 = (
    "17ff7b657efbe8796ef78858731c27979b0b1bdd46fc19f5d513e360b941e2e2"
)


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


def add(*vectors):
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(len(rows)):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def unit(size, index):
    return tuple(Q(row == index) for row in range(size))


def word_text(word):
    return "".join(map(str, word))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    first = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "p2_section_count_first",
    )
    private_gate = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "p2_section_count_private",
    )
    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "p2_section_count_parity",
    )
    square = load(
        "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py",
        "p2_section_count_square",
    )
    centered = load(
        "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py",
        "p2_section_count_centered",
    )
    restriction = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "p2_section_count_restriction",
    )
    cap = load(
        "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py",
        "p2_section_count_cap",
    )
    first_ledger, first_digest = first.audit()
    private_ledger, private_digest = private_gate.audit()
    square_ledger, square_digest = square.audit()
    centered_ledger, centered_digest = centered.audit()
    restriction_ledger, restriction_digest = restriction.audit()
    cap_ledger, cap_digest = cap.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256
            and private_digest == private_gate.EXPECTED_LEDGER_SHA256
            and square_digest == square.EXPECTED_LEDGER_SHA256
            and centered_digest == centered.EXPECTED_LEDGER_SHA256
            and restriction_digest == restriction.EXPECTED_LEDGER_SHA256
            and cap_digest == cap.EXPECTED_LEDGER_SHA256,
            "a pinned dependency ledger changed")
    require(square_ledger["source_provenance"]
            ["occurrence_local_section_constructed"] is False
            and square_ledger["ordered_bar_realization"]["d_squared"] == 0,
            "the labelled square provenance changed")

    occurrence, values, lookup, swap, b_matrix, s_matrix = parity.endpoint_data()
    size = len(values)
    require(size == 12, "the order-two occurrence count changed")
    one = (Q(1),) * size

    # The private preimage which must be promoted to pointed occurrence
    # sections before Fermat's labelled square becomes physical.
    z_private = tuple(map(
        Q, private_ledger["second_even_Bminus4_debt"]["preimage"]
    ))
    histogram = Counter(z_private)
    require(histogram == Counter({
        Q(101, 432): 2,
        Q(-1, 108): 4,
        Q(-1, 27): 4,
        Q(-61, 432): 2,
    }) and sum(z_private, Q(0)) == 0,
            ("the private preimage levels changed", histogram))

    # If z=b*1+sum_(i in S)a_i e_i, every coordinate outside S equals b.
    # The largest equal-coordinate fibre has size four, so |S|>=8.  Exhaust
    # all smaller supports and exhibit a support-eight representation.
    units = tuple(unit(size, index) for index in range(size))
    for support_size in range(8):
        require(all(rank([one] + [units[index] for index in support]
                         + [z_private])
                    > rank([one] + [units[index] for index in support])
                    for support in combinations(range(size), support_size)),
                ("a sub-eight occurrence support acquired z_private",
                 support_size))
    base_value = Q(-1, 108)
    selected_indices = tuple(index for index, value in enumerate(z_private)
                             if value != base_value)
    selected_coefficients = tuple(z_private[index] - base_value
                                  for index in selected_indices)
    selector_expression = add(
        scale(base_value, one),
        *(scale(coefficient, units[index])
          for index, coefficient in
          zip(selected_indices, selected_coefficients, strict=True)),
    )
    require(len(selected_indices) == 8 and selector_expression == z_private,
            "the support-eight pointed selector formula changed")

    # The centered occurrence class c_i=12e_i-1 is the pointed/global
    # conormal.  The same eight indices give z_private exactly.
    centered_classes = tuple(add(scale(size, vector), scale(-1, one))
                             for vector in units)
    centered_coefficients = tuple(coefficient / size
                                  for coefficient in selected_coefficients)
    centered_expression = add(*(
        scale(coefficient, centered_classes[index])
        for index, coefficient in
        zip(selected_indices, centered_coefficients, strict=True)
    ))
    require(centered_expression == z_private,
            "the lower centered occurrence formula changed")
    expected_centered_coefficients = (
        Q(35, 1728), Q(-1, 432), Q(35, 1728), Q(-1, 432),
        Q(-1, 432), Q(-19, 1728), Q(-1, 432), Q(-19, 1728),
    )
    require(selected_indices == (0, 2, 3, 4, 7, 8, 9, 11)
            and centered_coefficients == expected_centered_coefficients,
            ("the explicit centered section formula changed",
             selected_indices, centered_coefficients))

    # If endpoint-even pair selectors existed physically, four would suffice
    # modulo the complete row.  The pinned endpoint-role groupoid explicitly
    # withholds that fixed-fibre fold, so this is conditional only.
    pair_indices = []
    seen = set()
    for index, value in enumerate(values):
        if index in seen:
            continue
        mate = lookup[swap(value)]
        seen.update((index, mate))
        pair_indices.append((index, mate))
        require(z_private[index] == z_private[mate],
                "z_private stopped being endpoint-even")
    pair_levels = Counter(z_private[left] for left, _right in pair_indices)
    require(len(pair_indices) == 6 and max(pair_levels.values()) == 2,
            ("the endpoint-pair section count changed", pair_levels))
    conditional_pair_selector_minimum = len(pair_indices) - max(
        pair_levels.values()
    )
    require(conditional_pair_selector_minimum == 4,
            "the conditional endpoint-pair minimum changed")

    # Rebuild the eight first one-root private face vectors and the ambient
    # unmarked-word V4.  This separately counts covariance seeds for those
    # output word blocks.  It is not the pointed-selector count above.
    physical_sites = (0, 1, 4, 5)
    physical_from_abstract = {0: 0, 1: 1, 2: 4, 3: 5}
    abstract_from_physical = {value: key
                              for key, value in physical_from_abstract.items()}
    physical_values = tuple((
        physical_from_abstract[p_site],
        physical_from_abstract[s_site],
        tuple(tuple(sorted((physical_from_abstract[left],
                            physical_from_abstract[right])))
              for left, right in matching),
    ) for p_site, s_site, matching in values)
    physical_lookup = {value: index
                       for index, value in enumerate(physical_values)}
    colours = {0: 0, 1: 1, 4: 1, 5: 2}
    base_word = tuple(colours[site] for site in physical_sites)
    identity = parity.identity(size)
    marked = (0, 1, (occurrence.edge(2, 3),))
    c_plus = tuple(Q(6 if value in (marked, swap(marked)) else 0) - 1
                   for value in values)
    z_first = scale(Q(-1, 24), parity.matvec(
        parity.matrix_add(b_matrix, parity.matrix_scale(6, identity)),
        c_plus,
    ))
    faces = defaultdict(lambda: [Q(0)] * size)
    for index, (p_site, s_site, matching) in enumerate(physical_values):
        residual = matching[0]
        for endpoint in (p_site, s_site):
            for selected in residual:
                if colours[endpoint] == colours[selected]:
                    continue
                for changed in (endpoint, selected):
                    word = list(base_word)
                    word[physical_sites.index(changed)] = (
                        colours[selected] if changed == endpoint
                        else colours[endpoint]
                    )
                    faces[tuple(word)][index] += z_first[index]
    face_private = {}
    for word, vector in faces.items():
        vector = tuple(vector)
        face_private[word] = add(
            vector, scale(-sum(vector, Q(0)) / size, one)
        )
    words = tuple(sorted(face_private))
    require(len(words) == 8
            and tuple(map(word_text, words)) == tuple(
                record["word"] for record in
                first_ledger["one_endpoint_Hasse_faces"]
                ["intermediate_words"]
            ), "the first private word packet changed")

    group = []
    for image_tuple in permutations(physical_sites):
        site_map = dict(zip(physical_sites, image_tuple, strict=True))
        for colour_tuple in permutations((0, 1, 2)):
            colour_map = dict(zip((0, 1, 2), colour_tuple, strict=True))
            if all(colour_map[colours[site]] == colours[site_map[site]]
                   for site in physical_sites):
                group.append((site_map, colour_map))
    require(len(group) == 4, "the unmarked-word V4 changed")

    def transform_word(word, element):
        site_map, colour_map = element
        answer = [None] * len(physical_sites)
        for old_index, old_site in enumerate(physical_sites):
            answer[physical_sites.index(site_map[old_site])] = (
                colour_map[word[old_index]]
            )
        return tuple(answer)

    def transform_occurrence(value, element):
        site_map, _colour_map = element
        p_site, s_site, matching = value
        return (
            site_map[p_site], site_map[s_site],
            tuple(tuple(sorted((site_map[left], site_map[right])))
                  for left, right in matching),
        )

    def transform_vector(vector, element):
        answer = [Q(0)] * size
        for index, value in enumerate(physical_values):
            answer[physical_lookup[transform_occurrence(value, element)]] = (
                vector[index]
            )
        return tuple(answer)

    def columns_from_seeds(seeds, target):
        return [
            transform_vector(face_private[seed], element)
            for seed in seeds for element in group
            if transform_word(seed, element) == target
        ]

    def seeds_span_targets(seeds, targets):
        return all(
            rank(columns_from_seeds(seeds, target)
                 + [face_private[target]])
            == rank(columns_from_seeds(seeds, target))
            for target in targets
        )

    word_orbits = []
    unseen = set(words)
    while unseen:
        seed = min(unseen)
        orbit = frozenset(transform_word(seed, element)
                          for element in group)
        word_orbits.append(orbit)
        unseen -= orbit
    word_orbits.sort(key=lambda orbit: (-len(orbit), sorted(orbit)))
    orbit_minima = []
    orbit_minimal_sets = []
    for orbit in word_orbits:
        ordered = tuple(sorted(orbit))
        solutions = []
        for count in range(1, len(ordered) + 1):
            solutions = [seeds for seeds in combinations(ordered, count)
                         if seeds_span_targets(seeds, ordered)]
            if solutions:
                break
        orbit_minima.append(count)
        orbit_minimal_sets.append(solutions)
    require(orbit_minima == [3, 2, 2],
            ("the per-orbit covariance minima changed", orbit_minima))

    all_solutions = []
    for count in range(1, len(words) + 1):
        all_solutions = [seeds for seeds in combinations(words, count)
                         if seeds_span_targets(seeds, words)]
        if all_solutions:
            break
    require(count == 7 and len(all_solutions) == 2,
            ("the global covariance minimum changed", count, all_solutions))
    expected_seed_sets = {
        frozenset(("0012", "0102", "0110", "0111",
                   "0212", "1112", "2112")),
        frozenset(("0102", "0110", "0111", "0122",
                   "0212", "1112", "2112")),
    }
    require({frozenset(map(word_text, seeds)) for seeds in all_solutions}
            == expected_seed_sets,
            ("the minimal seven seed sets changed", all_solutions))

    # Pin the relation to the h=3 centered projector and primitive cap.
    require(centered_ledger["relative_projector"]
            ["raw_centered_projector_value"] == 90
            and centered_ledger["augmented_cokernel"]
            ["physical_terminal_identification_constructed"] is False,
            "the centered occurrence source/terminal scope changed")
    h3_restriction = next(record for record in
                          restriction_ledger["components"]
                          if record["order"] == 3)
    require(h3_restriction["marked_residual_cuts"][0]
            ["lower_centered_coefficient"] == "15/2"
            and h3_restriction["marked_residual_cuts"][0]
            ["constant_coefficient"] == "13/2",
            "the h3-to-h2 centered restriction changed")
    cap_packet = cap_ledger["physical_cap_quotient"]
    cap_interface = cap_ledger["physical_cubic_interface"]
    require(cap_packet["required_augmented_signature"]
            == [0, -1, 0, 0, 0, 0, -1, 0, 0, 0]
            and "conditional only" in
            cap_interface["association_projector_is_a_Hasse_lift_of_p"],
            "the primitive cap projection scope changed")

    ledger = {
        "theorem": "h2 P2 centered occurrence cobar section count gate",
        "pins": PINS,
        "labelled_square": {
            "explicit_square_commit": "711f051",
            "source_side_d_squared": 0,
            "natural_parameters": (
                "one fixed structural occurrence tag and two commuting "
                "distinct-factor site-root directions"
            ),
            "pointed_occurrence_section_constructed": False,
            "q_reinsertion_face": "dq23 times the pointed section",
        },
        "private_preimage_pointed_sections": {
            "coefficient_histogram": {
                str(value): multiplicity
                for value, multiplicity in sorted(histogram.items())
            },
            "maximum_equal_coordinate_multiplicity": max(histogram.values()),
            "minimum_literal_occurrence_selectors_mod_complete_row": 8,
            "chosen_complete_row_coefficient": str(base_value),
            "chosen_selector_indices": list(selected_indices),
            "chosen_selector_coefficients": [str(value)
                                               for value in
                                               selected_coefficients],
            "conditional_endpoint_pair_selector_minimum": 4,
            "endpoint_pair_reduction_physical": False,
            "reason_pair_reduction_is_open": (
                "the endpoint-role groupoid transports the pointed label; "
                "its nontransported fold is the missing physical W column"
            ),
        },
        "centered_occurrence_identification": {
            "lower_class": "c_i=12e_i-1",
            "identity": "z_private=sum_i a_i*c_i on eight displayed tags",
            "indices": list(selected_indices),
            "coefficients_a_i": [str(value)
                                   for value in centered_coefficients],
            "same_degree_zero_source_type": True,
            "extra_P2_requirement": (
                "the c_i family must be source-valid and functorial under "
                "the labelled root PP square and q23 multiplication"
            ),
            "h3_restriction_shadow": (
                "D_e c_(f,3)=(15/2)c_(f/e,2)+(13/2)1 on each marked cut"
            ),
            "h3_centered_cell_constructed": False,
        },
        "word_face_covariance": {
            "V4_orbits": [sorted(map(word_text, orbit))
                           for orbit in word_orbits],
            "orbit_sizes": [len(orbit) for orbit in word_orbits],
            "minimum_seeds_per_orbit": orbit_minima,
            "minimum_ambient_covariance_seeds": count,
            "minimal_seed_sets": [sorted(map(word_text, seeds))
                                  for seeds in all_solutions],
            "three_orbit_representatives_suffice": False,
            "strict_marked_word_sections": 8,
            "reason": (
                "nontrivial V4 transport moves the marked occurrence; the "
                "transported face vector is generally not the fixed-packet "
                "face vector in the target word"
            ),
        },
        "primitive_cap_comparison": {
            "h3_projected_signature_row_order": cap_packet["row_order"],
            "h3_projected_signature": cap_packet[
                "required_augmented_signature"
            ],
            "p_is_projected_aggregate_cap": True,
            "p_constructed_as_augmented_Hasse_lift": False,
            "p_plus_coefficient_centered_identity_supplies_P2": False,
            "reason": (
                "p retains only the primitive cap quotient and carries no "
                "twelve-tag occurrence section, labelled root square, or "
                "dq23 conormal"
            ),
        },
        "nonfill_terminal_alternative": {
            "exact_linear_alternative": (
                "the full pointed private packet lies in the projected image "
                "of the complete augmented physical source map, or a "
                "projected cokernel covector detects it"
            ),
            "conormal_darkness_closes_pointwise_value": True,
            "conormal_darkness_constructs_source_chain": False,
            "existing_terminal_alternative_closes_arbitrary_occurrence_dual":
                False,
            "missing_typing": (
                "extend the first nonzero lower/dq private cokernel covector "
                "over all protected, anchor, target, Eq, residue, W, eta/sigma "
                "and physical-q columns as an accepted source terminal"
            ),
            "conditional_closure": (
                "if that terminal-promotion clause is appended, nonfill is a "
                "physical generator/separator; if the full lower and dq "
                "packet is dark at a source, the associated-graded value "
                "lands there, but no neighbourhood-level homotopy follows"
            ),
        },
        "shortest_positive_theorem": (
            "construct one universal order-two centered occurrence section "
            "C_i for every marked occurrence tag, with boundary 12e_i-1, "
            "functorial for commuting labelled roots and q reinsertion.  The "
            "eight-tag formula above then supplies z_private and Fermat's "
            "square supplies the finite cobar.  Alternatively promote the "
            "first full augmented nonfill covector to an accepted terminal."
        ),
        "scope": (
            "exact rational occurrence module, V4 covariance, centered "
            "restriction shadow, and first-PP labelled square.  No physical "
            "centered section or arbitrary occurrence-terminal promotion is "
            "claimed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("P2 centered cobar section-count ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("labelled occurrence square: FINITE, POINTED CAP OPEN")
    print("literal pointed selectors modulo complete row: 8")
    print("V4 face covariance seeds: 7, NOT 3")
    print("strict marked word sections: 8")
    print("centered c_i supplies cap type only with root/q functoriality")
    print("conormal dark: POINTWISE LANDING, NOT SOURCE HOMOTOPY")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
