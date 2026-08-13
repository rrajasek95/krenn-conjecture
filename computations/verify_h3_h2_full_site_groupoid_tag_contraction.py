#!/usr/bin/env python3
"""Contract the h=3 H2 direction tags under the full eight-site groupoid.

The fixed-response audit treats six residual sites and two distinguished
response endpoints P,S.  Encoding d,p,s,q uniformly as the edges of K8
shows that the complete 210-pair / 70-component inventory is S8-stable.
The residual-site subgroup leaves one C4 coinvariant.  One endpoint--
residual transposition kills it, so the full centered tag module has zero
coinvariants over characteristic zero.

This is a coefficient/groupoid theorem.  It says that a termwise
site-natural physical PP comparison has no additional invariant C4 tag; it
does not construct that comparison or the downstream word-0102 carrier.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py":
        "bee87b90c32720583f50d1c65dc2280dd337a46d197932d8c22aab802362d9ff",
    "notes/h3-h2-direction-tag-maschke-c4-coinvariant-gate.md":
        "f61147619b6758924c700fd3a4d99a1edb398ed9abc23f417fdf745209055d29",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
}
PRIMES = (1_000_003, 1_000_033)
EXPECTED_LEDGER_SHA256 = (
    "32598f0d35eb7b57b5885481d9d7590bb85a9f27a0f4de8078a9955b46c51ffe"
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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def variable_edge(variable) -> frozenset[int]:
    """Encode q_ij,p_i,s_i,d as edges ij,iP,iS,PS of K8."""
    kind = variable[0]
    if kind == "q":
        return frozenset((variable[1], variable[2]))
    if kind == "p":
        return frozenset((variable[1], 6))
    if kind == "s":
        return frozenset((variable[1], 7))
    require(kind == "d", variable)
    return frozenset((6, 7))


def edge_variable(edge: frozenset[int]):
    left, right = sorted(edge)
    if (left, right) == (6, 7):
        return ("d",)
    if right == 6:
        return ("p", left)
    if right == 7:
        return ("s", left)
    return ("q", left, right)


def act_pair(pair, permutation):
    return frozenset(
        edge_variable(frozenset(permutation[site]
                                for site in variable_edge(variable)))
        for variable in pair
    )


def action_relations(base, classification, adjacent_swaps):
    (pairs, pair_position, components, component_position,
     pair_to_component, _profiles) = base.inventory(classification)
    dimension = 2 * len(components)

    def difference(component_index, positive, negative):
        answer = [0] * dimension
        if positive == 1:
            answer[2 * component_index] += 1
        elif positive == 2:
            answer[2 * component_index + 1] += 1
        if negative == 1:
            answer[2 * component_index] -= 1
        elif negative == 2:
            answer[2 * component_index + 1] -= 1
        return answer

    relations = []
    for selected in adjacent_swaps:
        permutation = list(range(8))
        permutation[selected], permutation[selected + 1] = (
            permutation[selected + 1], permutation[selected]
        )
        action = tuple(pair_position[act_pair(pair, permutation)]
                       for pair in pairs)
        local_action = {}
        for component_index, component in enumerate(components):
            image = frozenset(action[pair_index]
                              for pair_index in component)
            target_component = component_position[image]
            for local_index, pair_index in enumerate(component):
                mapped_component, mapped_local = pair_to_component[
                    action[pair_index]
                ]
                require(mapped_component == target_component,
                        (selected, component_index, local_index))
                local_action[(component_index, local_index)] = (
                    target_component, mapped_local
                )
        for component_index in range(len(components)):
            for local_index in (1, 2):
                target_component, target_local = local_action[
                    (component_index, local_index)
                ]
                base_component, base_local = local_action[
                    (component_index, 0)
                ]
                require(target_component == base_component,
                        "one centered fibre split under the site action")
                row = difference(target_component, target_local, base_local)
                row[2 * component_index + local_index - 1] -= 1
                relations.append(row)
    return relations, len(pairs), len(components), dimension


def audit():
    pin_dependencies()
    base = load(
        "computations/verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py",
        "h2_tag_base",
    )
    classification = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "h2_classification",
    )

    residual_relations, pair_count, component_count, dimension = (
        action_relations(base, classification, range(5))
    )
    full_relations, pair_count_full, component_count_full, dimension_full = (
        action_relations(base, classification, range(7))
    )
    bridge_relations, *_ = action_relations(
        base, classification, tuple(range(6))
    )
    require((pair_count, component_count, dimension)
            == (pair_count_full, component_count_full, dimension_full)
            == (210, 70, 140),
            (pair_count, component_count, dimension))

    residual_ranks = {
        str(prime): base.rank_mod(residual_relations, prime)
        for prime in PRIMES
    }
    bridge_ranks = {
        str(prime): base.rank_mod(bridge_relations, prime)
        for prime in PRIMES
    }
    full_ranks = {
        str(prime): base.rank_mod(full_relations, prime)
        for prime in PRIMES
    }
    require(set(residual_ranks.values()) == {139}, residual_ranks)
    require(set(bridge_ranks.values()) == {140}, bridge_ranks)
    require(set(full_ranks.values()) == {140}, full_ranks)

    ledger = {
        "theorem": "full eight-site action-groupoid contracts every H2 direction tag",
        "pins": PINS,
        "edge_dictionary": {
            "q_ij": "edge ij among residual sites 0..5",
            "p_i": "edge iP with P=6",
            "s_i": "edge iS with S=7",
            "d": "edge PS",
        },
        "inventory": {
            "direction_pairs": pair_count,
            "K33_components": component_count,
            "centered_dimension": dimension,
        },
        "residual_S6_action_rank": residual_ranks,
        "after_one_endpoint_residual_swap_rank": bridge_ranks,
        "full_S8_action_rank": full_ranks,
        "coinvariant_dimensions": {
            "fixed_response_endpoints": 1,
            "full_eight_site_groupoid": 0,
        },
        "conclusion": (
            "the old invariant C4 line 2e_DQ-e_PS1-e_PS2 is not invariant "
            "after a physical site transposition exchanges one response "
            "endpoint with one residual site"
        ),
        "physical_scope": (
            "conditional on one termwise source-valid PP comparison natural "
            "under changes of the two selected response endpoints; coefficient "
            "S8 covariance alone does not construct that comparison, and the "
            "downstream P2 word-0102 private carrier remains"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("fixed response endpoints: tag action rank 139/140")
    print("one endpoint-residual site swap: tag action rank 140/140")
    print("full S8 H2 direction-tag coinvariants: ZERO")
    print("physical termwise PP naturality: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
