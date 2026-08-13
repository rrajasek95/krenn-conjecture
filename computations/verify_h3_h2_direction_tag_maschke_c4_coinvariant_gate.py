#!/usr/bin/env python3
"""Quotient the h=3 H2 direction-tag module by physical symmetries.

The 210 nonzero response direction pairs are partitioned into seventy
three-element fibres by their common complementary H2 tail.  Their centered
tag module K has dimension 70*(3-1)=140.  Site permutations and endpoint
transpose act on K.  This checker constructs the complete integral action
matrix on K and proves

    dim_Q K_G = 1.

The C2+ and P2/P2^T sectors have zero coinvariants; the C4 sector has one
coinvariant, represented in every C4 fibre by

    2 e_DQ - e_PS(1) - e_PS(2).

Thus a termwise equivariant characteristic-zero PP/action-bar schema would
contract every nontrivial tag character, but it cannot contract this C4
trivial line.  The already known P2 word-0102 private carrier is downstream
of K and remains a second, differently typed landing datum.  Once either
local dual is physically placed in the complete augmented grade, the pinned
o2 theorem gives the exact filler-or-terminal alternative.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h3_h2_second_hasse_k33_tagged_landing_gate.py":
        "b2e96e12b68a44d24dd984d20a627a900537efc7924a7c78521c3c14a42066c6",
    "notes/h3-h2-second-hasse-k33-tagged-landing-gate.md":
        "e18ef1b1b187c06e1a222caf1958b43acaf703c92faa2a697e0e0b55f69048be",
    "computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py":
        "1994697181c6034267d98a26a28ab4c69c3fcb979b657c8d7d06fc81b86650ed",
    "notes/h3-centered-occurrence-endpoint-matching-maschke-pointed-gate.md":
        "c56f3d4dd1f04f34e5a6c88f077820cf118eea5de31affc8f4196e4bd78fe75c",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "notes/uniform-physical-cartan-source-prism.md":
        "7d1da671c9203c7d6080d988fef662caba6024b65227881e111285ad35ba8067",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
}
EXPECTED_LEDGER_SHA256 = (
    "cdcbc5eb4b1fb8906e3abf399f12bba54bd174401c2f24cd098dac5c549de8a4"
)
PRIMES = (1_000_003, 1_000_033)


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def component_name(profile: tuple[tuple[str, int], ...]) -> str:
    names = {
        (("QQ-disjoint", 3),): "C2plus",
        (("DQ", 1), ("PS-distinct", 2)): "C4",
        (("PQ-disjoint", 3),): "P2",
        (("SQ-disjoint", 3),): "P2_reverse",
    }
    require(profile in names, ("unknown component profile", profile))
    return names[profile]


def rank_mod(rows: list[list[int]], prime: int) -> int:
    if not rows:
        return 0
    work = [[entry % prime for entry in row] for row in rows]
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged matrix")
    pivot = 0
    for column in range(width):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        inverse = pow(work[pivot][column], prime - 2, prime)
        work[pivot] = [(entry * inverse) % prime for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                (left - coefficient * right) % prime
                for left, right in zip(work[row], work[pivot], strict=True)
            ]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def apply_site(variable, permutation):
    kind = variable[0]
    if kind == "q":
        return ("q",) + tuple(sorted((permutation[variable[1]],
                                      permutation[variable[2]])))
    if kind in ("p", "s"):
        return (kind, permutation[variable[1]])
    require(kind == "d", variable)
    return variable


def apply_theta(variable):
    kind = variable[0]
    if kind == "p":
        return ("s", variable[1])
    if kind == "s":
        return ("p", variable[1])
    return variable


def act_pair(pair, generator):
    kind, payload = generator
    if kind == "site":
        return frozenset(apply_site(variable, payload) for variable in pair)
    require(kind == "theta", generator)
    return frozenset(apply_theta(variable) for variable in pair)


def orbit_partition(items, actions):
    unseen = set(items)
    answer = []
    while unseen:
        start = min(unseen)
        orbit = {start}
        queue = deque((start,))
        unseen.remove(start)
        while queue:
            item = queue.popleft()
            for action in actions:
                image = action(item)
                if image not in orbit:
                    require(image in set(items), ("action left inventory", image))
                    orbit.add(image)
                    unseen.discard(image)
                    queue.append(image)
        answer.append(tuple(sorted(orbit)))
    return tuple(answer)


def inventory(classification):
    _target, response = classification.source_monomials()
    index = classification.pair_index(response)
    pairs = tuple(sorted(
        (pair for pair, tails in index.items() if tails),
        key=lambda pair: repr(tuple(sorted(pair))),
    ))
    pair_position = {pair: position for position, pair in enumerate(pairs)}
    tails = tuple(sorted({tail for pair in pairs for tail in index[pair]},
                         key=repr))
    tail_position = {tail: position for position, tail in enumerate(tails)}

    adjacency = defaultdict(set)
    for pair_index, pair in enumerate(pairs):
        for tail in index[pair]:
            adjacency[("p", pair_index)].add(("t", tail_position[tail]))
            adjacency[("t", tail_position[tail])].add(("p", pair_index))

    components = []
    seen = set()
    for start in sorted(adjacency):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        component_pairs = []
        component_tails = []
        while stack:
            vertex = stack.pop()
            if vertex[0] == "p":
                component_pairs.append(vertex[1])
            else:
                component_tails.append(vertex[1])
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        require(len(component_pairs) == len(component_tails) == 3,
                (component_pairs, component_tails))
        components.append(tuple(sorted(component_pairs,
                                       key=lambda i: repr(tuple(sorted(pairs[i]))))))
    components = tuple(sorted(components,
                              key=lambda c: repr(tuple(pairs[i] for i in c))))
    component_position = {
        frozenset(component): position
        for position, component in enumerate(components)
    }
    pair_to_component = {
        pair_index: (component_index, local_index)
        for component_index, component in enumerate(components)
        for local_index, pair_index in enumerate(component)
    }
    profiles = []
    for component in components:
        profile = tuple(sorted(Counter(
            classification.pair_shape(pairs[value]) for value in component
        ).items()))
        profiles.append(component_name(profile))
    require(len(pairs) == 210 and len(components) == 70
            and Counter(profiles) == Counter({
                "C2plus": 15, "C4": 15,
                "P2": 20, "P2_reverse": 20,
            }), (len(pairs), len(components), Counter(profiles)))
    return (pairs, pair_position, components, component_position,
            pair_to_component, tuple(profiles))


def direction_tag_quotient(classification) -> dict[str, object]:
    (pairs, pair_position, components, component_position,
     pair_to_component, profiles) = inventory(classification)

    generators = []
    for selected in range(5):
        permutation = list(range(6))
        permutation[selected], permutation[selected + 1] = (
            permutation[selected + 1], permutation[selected]
        )
        generators.append(("site", tuple(permutation)))
    generators.append(("theta", None))

    pair_actions = []
    component_actions = []
    local_actions = []
    for generator in generators:
        action = tuple(pair_position[act_pair(pair, generator)]
                       for pair in pairs)
        pair_actions.append(action)
        component_image = []
        local_image = {}
        for component_index, component in enumerate(components):
            image_set = frozenset(action[value] for value in component)
            target_component = component_position[image_set]
            component_image.append(target_component)
            for local_index, pair_index in enumerate(component):
                mapped_component, mapped_local = pair_to_component[action[pair_index]]
                require(mapped_component == target_component,
                        (generator, component_index, local_index))
                local_image[(component_index, local_index)] = (
                    target_component, mapped_local
                )
        component_actions.append(tuple(component_image))
        local_actions.append(local_image)

    dimension = 2 * len(components)

    def difference(component_index, positive, negative):
        answer = [0] * dimension
        offset = 2 * component_index
        if positive == 1:
            answer[offset] += 1
        elif positive == 2:
            answer[offset + 1] += 1
        if negative == 1:
            answer[offset] -= 1
        elif negative == 2:
            answer[offset + 1] -= 1
        return answer

    relations = []
    for local_action in local_actions:
        for component_index in range(len(components)):
            for local_index in (1, 2):
                target_component, target_local = local_action[
                    (component_index, local_index)
                ]
                base_component, base_local = local_action[(component_index, 0)]
                require(target_component == base_component,
                        "one K3 direction difference split across components")
                row = difference(target_component, target_local, base_local)
                row[2 * component_index + local_index - 1] -= 1
                relations.append(row)

    ranks = {str(prime): rank_mod(relations, prime) for prime in PRIMES}
    require(set(ranks.values()) == {139}, ranks)

    sectors = {
        "C2plus": tuple(2 * i + j for i, name in enumerate(profiles)
                        if name == "C2plus" for j in (0, 1)),
        "C4": tuple(2 * i + j for i, name in enumerate(profiles)
                    if name == "C4" for j in (0, 1)),
        "P2_plus_reverse": tuple(
            2 * i + j for i, name in enumerate(profiles)
            if name in ("P2", "P2_reverse") for j in (0, 1)
        ),
    }
    sector_ranks = {}
    for name, columns in sectors.items():
        projected = [[row[column] for column in columns] for row in relations]
        sector_ranks[name] = {
            str(prime): rank_mod(projected, prime) for prime in PRIMES
        }
    require(sector_ranks == {
        "C2plus": {str(prime): 30 for prime in PRIMES},
        "C4": {str(prime): 29 for prime in PRIMES},
        "P2_plus_reverse": {str(prime): 80 for prime in PRIMES},
    }, sector_ranks)

    # The direct-DQ coefficient is an integral invariant functional on K.
    invariant = [0] * dimension
    survivor = [0] * dimension
    for component_index, (component, name) in enumerate(zip(components,
                                                            profiles,
                                                            strict=True)):
        if name != "C4":
            continue
        weights = [int(classification.pair_shape(pairs[value]) == "DQ")
                   for value in component]
        require(sum(weights) == 1, weights)
        invariant[2 * component_index] = weights[1] - weights[0]
        invariant[2 * component_index + 1] = weights[2] - weights[0]
        coefficients = [-1, -1, -1]
        coefficients[weights.index(1)] = 2
        require(sum(coefficients) == 0, coefficients)
        survivor[2 * component_index] = coefficients[1]
        survivor[2 * component_index + 1] = coefficients[2]

    require(any(invariant) and any(survivor), "C4 invariant disappeared")
    require(all(sum(left * right for left, right in zip(invariant, row,
                                                        strict=True)) == 0
                for row in relations), "C4 functional is not action-invariant")
    require(sum(left * right for left, right in zip(invariant, survivor,
                                                    strict=True)) == 30,
            "C4 survivor normalization changed")

    def act_vector(vector, local_action):
        answer = [0] * dimension
        for component_index in range(len(components)):
            for local_index in (1, 2):
                coefficient = vector[2 * component_index + local_index - 1]
                if not coefficient:
                    continue
                target_component, target_local = local_action[
                    (component_index, local_index)
                ]
                base_component, base_local = local_action[(component_index, 0)]
                require(target_component == base_component, "action vector split")
                image = difference(target_component, target_local, base_local)
                answer = [left + coefficient * right
                          for left, right in zip(answer, image, strict=True)]
        return answer

    require(all(act_vector(survivor, action) == survivor
                for action in local_actions),
            "the displayed aggregate C4 vector ceased to be invariant")

    pair_orbits = orbit_partition(
        tuple(range(len(pairs))),
        tuple(lambda value, action=action: action[value]
              for action in pair_actions),
    )
    component_orbits = orbit_partition(
        tuple(range(len(components))),
        tuple(lambda value, action=action: action[value]
              for action in component_actions),
    )
    pair_orbit_profiles = sorted(
        (len(orbit), sorted({classification.pair_shape(pairs[value])
                             for value in orbit}))
        for orbit in pair_orbits
    )
    component_orbit_profiles = sorted(
        (len(orbit), sorted({profiles[value] for value in orbit}))
        for orbit in component_orbits
    )
    require(pair_orbit_profiles == [
        (15, ["DQ"]),
        (30, ["PS-distinct"]),
        (45, ["QQ-disjoint"]),
        (120, ["PQ-disjoint", "SQ-disjoint"]),
    ], pair_orbit_profiles)
    require(component_orbit_profiles == [
        (15, ["C2plus"]),
        (15, ["C4"]),
        (40, ["P2", "P2_reverse"]),
    ], component_orbit_profiles)

    # Four pair orbits minus three component orbits is the trivial
    # multiplicity in Q[pairs]-Q[components].  The explicit rank and dual
    # prove that there is no hidden rational coinvariant.
    require(len(pair_orbits) - len(component_orbits) == 1,
            "orbit-difference formula changed")
    return {
        "direction_tag_dimension": dimension,
        "acting_generators": "five adjacent site transpositions plus p<->s",
        "pair_orbits": pair_orbit_profiles,
        "component_orbits": component_orbit_profiles,
        "trivial_multiplicity_by_orbits": 1,
        "action_relation_rows": len(relations),
        "action_relation_rank_mod_primes": ranks,
        "rational_coinvariant_dimension": 1,
        "sector_dimensions": {name: len(columns)
                              for name, columns in sectors.items()},
        "sector_action_ranks_mod_primes": sector_ranks,
        "surviving_irreducible": "one trivial representation in C4",
        "surviving_C4_vector": (
            "sum over the 15 C4 fibres of "
            "(2 e_DQ-e_PS(first orientation)-e_PS(second orientation))"
        ),
        "surviving_dual": "sum of the DQ coefficients on the C4 fibres",
        "survivor_dual_pairing": 30,
        "C4_theta_odd_line": (
            "e_PS(first)-e_PS(second); nontrivial and contracted by "
            "(1-theta)/2 in characteristic zero"
        ),
    }


def terminal_promotion_audit() -> dict[str, object]:
    terminal = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "h2_tag_terminal_promotion",
    )
    ledger, digest = terminal.audit()
    require(digest == terminal.EXPECTED_LEDGER_SHA256,
            "the augmented terminal theorem ledger changed")
    extension = ledger["explicit_local_dual_extension"]
    fork = ledger["post_placement_dichotomy"]
    require(fork["third_branch"] is False
            and fork["pure_local_filler_cases"]
            and fork["augmented_terminal_cases"],
            "the exact filler-or-terminal fork changed")
    return {
        "promotion_is_conditional_on_literal_same_grade_placement": True,
        "known_augmented_rows_crossed": "q/ainc/target/W/ores/ridge",
        "explicit_extension_audited": bool(extension),
        "post_placement_alternative": fork["exact_alternative"],
        "third_branch": fork["third_branch"],
        "application_to_C4_line": (
            "a nonzero physically placed C4 invariant dual extends to an "
            "accepted augmented terminal unless the protected-zero filler exists"
        ),
        "application_to_P2_line": (
            "the known word-0102 private dual has the same post-placement fork, "
            "but lies downstream of the 140-dimensional tag module"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    classification = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "h2_direction_tag_classification",
    )
    ledger = {
        "theorem": "h3 H2 direction-tag Maschke quotient and C4 invariant gate",
        "pins": PINS,
        "structural_quotient": direction_tag_quotient(classification),
        "termwise_equivariant_PP_consequence": {
            "conditional_positive": (
                "if the physical PP/Cartan/Hasse comparison is defined on each "
                "literal direction tag and is natural for site permutations and "
                "endpoint transpose, characteristic-zero action bars contract "
                "all nontrivial tag representations"
            ),
            "not_contracted": "the single trivial C4 direct-versus-PS-average line",
            "root_colour_scope": (
                "root-colour permutations transport fine-grade copies but do not "
                "change the uncoloured pair/component orbit difference"
            ),
            "P2_scope": (
                "the P2 and reversed-P2 tag sectors have zero coinvariants; the "
                "known P2 word-0102 occurrence-private carrier appears only after "
                "the tagged Hasse restriction and is not a class in this K"
            ),
        },
        "augmented_terminal_promotion": terminal_promotion_audit(),
        "shortest_remaining_schema": (
            "one termwise equivariant PP schema removes every nontrivial tag.  "
            "Its independent invariant faces are the C4 direct-DQ versus "
            "endpoint-pair average and, after restriction, the P2 word-0102 "
            "private landing.  Once either is placed with literal word/fine/"
            "direction grade, 4373ae6 gives filler or augmented terminal."
        ),
        "scope": (
            "exact uncoloured h=3 direction-tag representation over Q and an "
            "exact conditional terminal promotion.  No physical termwise PP "
            "landing or C4 invariant filler is constructed here."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    quotient = ledger["structural_quotient"]
    print("direction-tag module: dimension 140")
    print("pair/component orbits: 4/3; coinvariant dimension 1")
    print("sector ranks: C2plus 30/30, C4 29/30, P2+reverse 80/80")
    print("sole invariant: C4 (2 DQ - PS - PS)")
    print("P2 word-0102 carrier: downstream and independent")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
