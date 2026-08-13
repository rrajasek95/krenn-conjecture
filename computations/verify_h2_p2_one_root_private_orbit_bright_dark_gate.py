#!/usr/bin/env python3
"""Classify all eight P2 one-root private faces and their bright/dark gate.

The literal lower packet has word 0112 on sites (0,1,4,5), marked ordered
endpoints 01, and residual edge 45.  Its eight one-root faces are the eight
single-site recolourings of 0112.  The full site/colour stabilizer of the
unmarked word is V4.  It has three orbits on these faces, of sizes 4,2,2.
The stabilizer of the marked endpoint/residual cut is trivial; endpoint
reversal is an additional occurrence involution, and every private face is
even under it.  Thus one fixed representative plus physical covariance does
not fill the eight faces of the marked packet.

Evaluation does not repair the typing gap.  A private occurrence value is a
linear combination of matching monomials, not a literal optical source
coordinate.  Exact support-minimal occurrence-fibre examples show both that
a bright private value need not be a coordinate unit and that a dark lower
face can retain a bright dq23 reinsertion conormal.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h2-p2-0112-one-endpoint-hasse-placement-gate.md":
        "5b17afb39c796d79021e0c16fb9e9d0e65c33acc9c7d1b8b6185747bd1450ab5",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "notes/h2-p2-0102-private-parity-reinsertion-gate.md":
        "c8c19b6bcd63a5e5b2a0854eac685643d36791ede811924137df717f39b6f620",
    "computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py":
        "1735de099eeaec04a2197c613350fba4bd52d8955873c8a032894d8653087a0a",
    "notes/h3-trapped-carrier-actual-endpoint-map-boundary.md":
        "e3c3096592a42452e42703ed0e5c1e68e62182a7ab36a9c8277ea89b925bcab1",
}
EXPECTED_LEDGER_SHA256 = (
    "32bf7af4dbc4d5151c7c08a110a0af33e0eef18ebc98ccf9370c5f7c7bd10d6d"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def add(*vectors):
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


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


def word_text(word):
    return "".join(map(str, word))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    first = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "p2_private_orbit_first",
    )
    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "p2_private_orbit_parity",
    )
    reinsertion = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "p2_private_orbit_reinsertion",
    )
    first_ledger, first_digest = first.audit()
    reinsertion_ledger, reinsertion_digest = reinsertion.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256
            and reinsertion_digest == reinsertion.EXPECTED_LEDGER_SHA256,
            "a P2 dependency ledger changed")

    occurrence, abstract_values, lookup, swap, b_matrix, s_matrix = (
        parity.endpoint_data()
    )
    size = len(abstract_values)
    one = (Q(1),) * size
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
    ) for p_site, s_site, matching in abstract_values)
    physical_lookup = {value: index
                       for index, value in enumerate(physical_values)}
    colours = {0: 0, 1: 1, 4: 1, 5: 2}
    base_word = tuple(colours[site] for site in physical_sites)
    require(word_text(base_word) == "0112" and size == 12,
            "the literal P2 packet changed")

    def abstract_value(value):
        p_site, s_site, matching = value
        return (
            abstract_from_physical[p_site],
            abstract_from_physical[s_site],
            tuple(occurrence.edge(abstract_from_physical[left],
                                  abstract_from_physical[right])
                  for left, right in matching),
        )

    def faces_for_marked(marked_physical):
        marked = abstract_value(marked_physical)
        c_plus = tuple(Q(6 if value in (marked, swap(marked)) else 0) - 1
                       for value in abstract_values)
        identity = parity.identity(size)
        z = scale(Q(-1, 24), parity.matvec(
            parity.matrix_add(b_matrix, parity.matrix_scale(6, identity)),
            c_plus,
        ))
        faces: dict[tuple[int, ...], list[Q]] = {}
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
                        word = tuple(word)
                        faces.setdefault(word, [Q(0)] * size)[index] += z[index]
        return {word: tuple(vector) for word, vector in faces.items()}

    marked = (0, 1, ((4, 5),))
    marked_mate = (1, 0, ((4, 5),))
    face_vectors = faces_for_marked(marked)
    words = tuple(sorted(face_vectors))
    require(tuple(map(word_text, words)) == (
        "0012", "0102", "0110", "0111",
        "0122", "0212", "1112", "2112",
    ), "the eight one-root words changed")

    # Every one-root private class is endpoint-even, not merely 0102.
    private_vectors = {}
    for word, vector in face_vectors.items():
        constant = scale(sum(vector, Q(0)) / size, one)
        private = add(vector, scale(-1, constant))
        require(parity.matvec(s_matrix, vector) == vector
                and parity.matvec(s_matrix, private) == private
                and sum(private, Q(0)) == 0
                and private != (Q(0),) * size,
                ("one-root parity/private class changed", word))
        private_vectors[word] = private

    # Site/colour relabellings preserving the unmarked word 0112 form V4.
    site_permutations = []
    for image_tuple in permutations(physical_sites):
        site_map = dict(zip(physical_sites, image_tuple, strict=True))
        for colour_tuple in permutations((0, 1, 2)):
            colour_map = dict(zip((0, 1, 2), colour_tuple, strict=True))
            if all(colour_map[colours[site]] == colours[site_map[site]]
                   for site in physical_sites):
                site_permutations.append((site_map, colour_map))
    require(len(site_permutations) == 4,
            ("0112 word stabilizer changed", site_permutations))

    def transform_word(word, group_element):
        site_map, colour_map = group_element
        transformed = [None] * len(physical_sites)
        for old_index, old_site in enumerate(physical_sites):
            new_site = site_map[old_site]
            transformed[physical_sites.index(new_site)] = colour_map[word[old_index]]
        return tuple(transformed)

    def transform_occurrence(value, group_element):
        site_map, _colour_map = group_element
        p_site, s_site, matching = value
        return (
            site_map[p_site], site_map[s_site],
            tuple(tuple(sorted((site_map[left], site_map[right])))
                  for left, right in matching),
        )

    def transform_vector(vector, group_element):
        answer = [Q(0)] * size
        for index, value in enumerate(physical_values):
            answer[physical_lookup[transform_occurrence(value, group_element)]] = (
                vector[index]
            )
        return tuple(answer)

    def orbit(seed):
        return frozenset(transform_word(seed, element)
                         for element in site_permutations)

    word_orbits = []
    unseen = set(words)
    while unseen:
        current = orbit(min(unseen))
        require(current <= set(words), ("word orbit escaped", current))
        word_orbits.append(current)
        unseen -= current
    word_orbits.sort(key=lambda values: (len(values), sorted(values)))
    expected_orbits = {
        frozenset(tuple(map(int, text)) for text in
                  ("0012", "0102", "0122", "0212")),
        frozenset(tuple(map(int, text)) for text in ("0111", "1112")),
        frozenset(tuple(map(int, text)) for text in ("0110", "2112")),
    }
    require(set(word_orbits) == expected_orbits,
            ("root/site word types changed", word_orbits))

    # The permutation character on the eight word classes is (8,4,0,0).
    identity_element = next(
        element for element in site_permutations
        if all(element[0][site] == site for site in physical_sites)
        and all(element[1][colour] == colour for colour in (0, 1, 2))
    )
    middle_swap = next(
        element for element in site_permutations
        if element[0][1] == 4 and element[0][4] == 1
        and element[0][0] == 0 and element[0][5] == 5
    )
    flank_reflection = next(
        element for element in site_permutations
        if element[0][0] == 5 and element[0][5] == 0
        and element[0][1] == 1 and element[0][4] == 4
    )
    product = next(element for element in site_permutations
                   if element not in
                   (identity_element, middle_swap, flank_reflection))
    ordered_group = (identity_element, middle_swap, flank_reflection, product)
    character = tuple(sum(transform_word(word, element) == word
                          for word in words)
                      for element in ordered_group)
    require(character == (8, 4, 0, 0),
            ("eight-word permutation character changed", character))
    multiplicities = {}
    for middle_sign in (1, -1):
        for flank_sign in (1, -1):
            value = (character[0]
                     + middle_sign * character[1]
                     + flank_sign * character[2]
                     + middle_sign * flank_sign * character[3]) // 4
            multiplicities[(middle_sign, flank_sign)] = value
    require(sorted(multiplicities.values()) == [1, 1, 3, 3]
            and sum(multiplicities.values()) == 8,
            ("V4 character multiplicities changed", multiplicities))

    # Naturality holds only after transporting the marked occurrence too.
    for element in site_permutations:
        transported_marked = transform_occurrence(marked, element)
        transported_faces = faces_for_marked(transported_marked)
        for word, vector in face_vectors.items():
            require(transform_vector(vector, element)
                    == transported_faces[transform_word(word, element)],
                    ("transported packet lost covariance", element, word))

    fixed_marked_stabilizer = tuple(
        element for element in site_permutations
        if transform_occurrence(marked, element) in (marked, marked_mate)
    )
    require(fixed_marked_stabilizer == (identity_element,),
            ("marked cut acquired a site/root symmetry",
             fixed_marked_stabilizer))

    # Because the eight word blocks are disjoint, their private classes are
    # independent even after quotienting each complete response line.
    direct_private = []
    for block, word in enumerate(words):
        vector = [Q(0)] * (len(words) * size)
        start = block * size
        vector[start:start + size] = private_vectors[word]
        direct_private.append(tuple(vector))
    require(rank(direct_private) == 8,
            "the eight wordwise private classes lost independence")

    # Exact evaluation counterguards in the 0102 occurrence fibre.
    representative_word = tuple(map(int, "0102"))
    representative = face_vectors[representative_word]
    representative_private = private_vectors[representative_word]
    expected = tuple(map(Q, first_ledger["one_endpoint_Hasse_faces"]
                         ["representative_occurrence_vector"]))
    require(representative == expected,
            "the representative occurrence vector changed")
    private_preimage = tuple(map(
        Q, reinsertion_ledger["second_even_Bminus4_debt"]["preimage"]
    ))

    bright_evaluation = (Q(1), Q(-1)) + (Q(0),) * 10
    require(dot(one, bright_evaluation) == 0
            and dot(representative_private, bright_evaluation) == Q(-13, 12),
            "the support-two bright occurrence counterguard changed")
    require(rank([tuple(one[index] for index in (0, 1))]) == 1,
            "the support-two response circuit changed")

    dark_evaluation = (Q(-2), Q(15), Q(-13)) + (Q(0),) * 9
    require(dot(one, dark_evaluation) == 0
            and dot(representative_private, dark_evaluation) == 0
            and dot(private_preimage, dark_evaluation) == Q(-1, 8),
            "the dark-lower/bright-conormal counterguard changed")
    restricted_one = tuple(one[index] for index in (0, 1, 2))
    restricted_private = tuple(representative_private[index]
                               for index in (0, 1, 2))
    require(rank([restricted_one, restricted_private]) == 2
            and all(rank([
                tuple(restricted_one[index] for index in pair),
                tuple(restricted_private[index] for index in pair),
            ]) == 2 for pair in ((0, 1), (0, 2), (1, 2))),
            "the support-three dark circuit stopped being minimal")

    ledger = {
        "theorem": "h2 P2 eight one-root private orbit and bright-dark gate",
        "pins": PINS,
        "literal_packet": {
            "word": "0112",
            "sites": list(physical_sites),
            "marked_endpoints": "01",
            "residual": "q45:12",
            "reinsertion": "q23:21",
            "one_root_words": [word_text(word) for word in words],
            "private_rank_mod_complete_rows": rank(direct_private),
            "all_endpoint_even": True,
            "endpoint_odd_active_clean_projection_rank": 0,
        },
        "unmarked_word_root_site_symmetry": {
            "group": "V4",
            "word_orbits": [sorted(word_text(word) for word in values)
                            for values in word_orbits],
            "orbit_sizes": sorted(len(values) for values in word_orbits),
            "permutation_character_id_middle_flank_product": list(character),
            "character_multiplicities": {
                f"middle={middle:+d},flank={flank:+d}": value
                for (middle, flank), value in multiplicities.items()
            },
            "minimum_covariant_word_types": 3,
        },
        "marked_packet_covariance": {
            "site_root_stabilizer_size": len(fixed_marked_stabilizer),
            "site_root_stabilizer": "identity only",
            "endpoint_reversal": "acts internally and fixes every face class",
            "transported_packet_covariance": True,
            "one_seed_spans_fixed_packet": False,
            "reason": (
                "nontrivial V4 elements transport the marked occurrence as "
                "well as the face; they do not generate the other seven "
                "word blocks of the original marked packet"
            ),
        },
        "evaluation_bright_dark": {
            "bright_minimal_occurrence_fibre": {
                "values": [str(value) for value in bright_evaluation],
                "complete_response": "0",
                "private_value": "-13/12",
                "support": 2,
                "literal_optical_coordinate_unit": False,
            },
            "dark_lower_bright_conormal_fibre": {
                "values": [str(value) for value in dark_evaluation],
                "complete_response": "0",
                "private_lower_value": "0",
                "dq23_preimage_value": "-1/8",
                "support": 3,
                "minimal_for_complete_plus_lower_constraints": True,
            },
            "conclusion": (
                "private brightness is an occurrence-monomial readout, not "
                "a domain-coordinate column, so the fixed-q minimum-support "
                "column theorem does not imply deletion or a unit.  Lower "
                "darkness alone also does not land P2 because the independent "
                "dq23 conormal can remain bright"
            ),
        },
        "sharp_fork": {
            "bright": (
                "requires an occurrence-to-physical-source comparison; only "
                "then can a nonzero class enter a typed rank/deletion/terminal "
                "alternative"
            ),
            "dark": (
                "P2 lands at an evaluated source only if both all eight lower "
                "private readouts and their forced dq reinsertion readouts are "
                "dark; coefficient darkness does not construct a uniform chain"
            ),
            "remaining_source_theorem": (
                "three ambient root/site word types (or eight fixed-grade "
                "labelled sections), each as an endpoint-even occurrence-local "
                "one-endpoint PP cell including its dq23 face and full augmented "
                "physical readouts"
            ),
        },
        "scope": (
            "exact occurrence coefficient module and its first-PP reinsertion. "
            "The support-two/support-three evaluations are sharp linear "
            "occurrence-fibre counterguards, not asserted realizable optical "
            "sources; precisely that realization/comparison is the open gate."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("P2 private orbit ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("eight one-root private classes: ALL ENDPOINT-EVEN")
    print("unmarked 0112 V4 word orbits: 4 + 2 + 2")
    print("marked packet site/root stabilizer: IDENTITY")
    print("one covariant representative spans all eight: NO")
    print("lower-dark implies reinsertion-dark: NO (-1/8 guard)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
