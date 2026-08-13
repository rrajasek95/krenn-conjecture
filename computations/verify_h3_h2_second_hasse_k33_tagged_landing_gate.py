#!/usr/bin/env python3
"""Expose the common direction-tag obstruction in every h=3 H2 face.

The complete response H2 census has 210 nonzero direction pairs and 210
distinct complementary lower tails.  Join a pair to a tail when together
they form a literal response occurrence.  The resulting bipartite graph is
the disjoint union of seventy K3,3 components.  Consequently the untagged
pair-to-tail incidence has rank 70 and a 140-dimensional standard tag
kernel/cokernel.  Every C2+, C4, P2 and reversed-P2 face has this same
rank-one aggregate / rank-two direction-tag split.

Thus the ordinary Hasse restriction is one uniform coefficient map, but it
cannot be the required physical landing after the direction-pair tag is
forgotten.  A physical comparison must carry the centered tag module.  The
smallest already explicit instance is the P2 0102 endpoint-even private
coordinate, detected by -13/6; q23 reinsertion has the independent labelled
dq detector 35/72.  Existing P2, C2+ and C4 theorems construct source-side
coherence but not this carrier landing.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
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
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "notes/h2-p2-relative-occurrence-graph-resolution-gate.md":
        "101f1040df04e5f6a3ca7c5034c1a3a713903704936207619c5ec8e00d59df37",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "notes/h2-p2-0112-one-endpoint-hasse-placement-gate.md":
        "5b17afb39c796d79021e0c16fb9e9d0e65c33acc9c7d1b8b6185747bd1450ab5",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "notes/h2-p2-0102-private-parity-reinsertion-gate.md":
        "c8c19b6bcd63a5e5b2a0854eac685643d36791ede811924137df717f39b6f620",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "notes/h2-b4-cplus-shared-interface-gate.md":
        "4c89253c18f4475371849a78c990e27b7d6af79193522cd5a583af80cc929fb8",
    "computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py":
        "024eb1cbe7d5aca9795c7d2491bb6399c0e93324f898d031707c1c752d7ea14c",
    "notes/h3-loop-degeneracy-hasse-cross-term-scope-gate.md":
        "2906899b807451def78bf92e36e1c212c4242982a3ad8f86d2fe2ba274b6cd11",
}
EXPECTED_LEDGER_SHA256 = "4199398ce09747e2179e9b256cb14242a2aa92e451b86058b8a9f32a227f62a9"


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


def rank(vectors: tuple[tuple[Q, ...], ...]) -> int:
    work = [list(map(Q, vector)) for vector in vectors]
    if not work:
        return 0
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
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
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def component_name(profile: tuple[tuple[str, int], ...]) -> str:
    names = {
        (("QQ-disjoint", 3),): "C2plus",
        (("DQ", 1), ("PS-distinct", 2)): "C4",
        (("PQ-disjoint", 3),): "P2",
        (("SQ-disjoint", 3),): "P2_reverse",
    }
    require(profile in names, ("unknown component profile", profile))
    return names[profile]


def tagged_incidence_audit(classification) -> dict[str, object]:
    _target, response = classification.source_monomials()
    index = classification.pair_index(response)
    pairs = tuple(sorted(
        (pair for pair, tails in index.items() if tails),
        key=lambda pair: repr(tuple(sorted(pair))),
    ))
    tails = tuple(sorted({tail for pair in pairs for tail in index[pair]},
                         key=repr))
    tail_index = {tail: position for position, tail in enumerate(tails)}
    require(len(pairs) == len(tails) == 210
            and sum(len(index[pair]) for pair in pairs) == 630,
            (len(pairs), len(tails)))

    adjacency: dict[tuple[str, int], list[tuple[str, int]]] = {
        **{("pair", i): [] for i in range(len(pairs))},
        **{("tail", i): [] for i in range(len(tails))},
    }
    for pair_position, pair in enumerate(pairs):
        require(len(index[pair]) == 3,
                ("a nonzero H2 pair lost its three tails", pair))
        for tail in index[pair]:
            tail_position = tail_index[tail]
            adjacency[("pair", pair_position)].append(
                ("tail", tail_position)
            )
            adjacency[("tail", tail_position)].append(
                ("pair", pair_position)
            )

    components = []
    seen = set()
    for start in adjacency:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        components.append(tuple(component))

    profiles = Counter()
    representatives = {}
    for component in components:
        pair_positions = tuple(sorted(vertex[1] for vertex in component
                                      if vertex[0] == "pair"))
        tail_positions = tuple(sorted(vertex[1] for vertex in component
                                      if vertex[0] == "tail"))
        require(len(pair_positions) == len(tail_positions) == 3,
                ("a component stopped being 3+3", component))
        expected_tail_vertices = {("tail", value)
                                  for value in tail_positions}
        require(all(set(adjacency[("pair", value)]) == expected_tail_vertices
                    for value in pair_positions),
                ("a component stopped being K3,3", component))
        profile = tuple(sorted(Counter(
            classification.pair_shape(pairs[value])
            for value in pair_positions
        ).items()))
        name = component_name(profile)
        profiles[name] += 1
        representatives.setdefault(name, {
            "direction_pairs": [repr(tuple(sorted(pairs[value])))
                                for value in pair_positions],
            "complement_tails": [repr(tails[value])
                                 for value in tail_positions],
        })

        # The three incidence rows are all (1,1,1).  Their centered tag
        # module has basis 3e_i-one and rank two.
        incidence_rows = tuple((Q(1), Q(1), Q(1)) for _ in range(3))
        one = (Q(1), Q(1), Q(1))
        centered = tuple(tuple(Q(3 * (row == column)) - one[column]
                               for column in range(3)) for row in range(3))
        require(rank(incidence_rows) == 1 and rank(centered) == 2
                and tuple(sum(vector[column] for vector in centered)
                          for column in range(3)) == (Q(0), Q(0), Q(0)),
                "the K3,3 aggregate/standard split changed")

    require(len(components) == 70
            and profiles == Counter({
                "C2plus": 15, "C4": 15,
                "P2": 20, "P2_reverse": 20,
            }), (len(components), profiles))
    return {
        "tagged_direction_pairs": len(pairs),
        "distinct_complement_tails": len(tails),
        "literal_pair_tail_incidences": 630,
        "bipartite_components": len(components),
        "component_graph": "K3,3",
        "component_profile": dict(sorted(profiles.items())),
        "untagged_incidence_rank": len(components),
        "direction_tag_kernel_dimension": len(pairs) - len(components),
        "tail_cokernel_dimension": len(tails) - len(components),
        "per_component_split": "constant rank 1 plus standard rank 2",
        "canonical_representatives": representatives,
        "consequence": (
            "one ordinary Hasse restriction handles every coefficient "
            "aggregate, but any map factoring through the untagged lower "
            "polynomial kills the two-dimensional centered direction-tag "
            "module in each component"
        ),
    }


def strongest_h2_status_audit() -> dict[str, object]:
    p2_first = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "h2_k33_p2_first",
    )
    first_ledger, first_digest = p2_first.audit()
    require(first_digest == p2_first.EXPECTED_LEDGER_SHA256,
            "the first P2 placement ledger changed")
    p2_reinsert = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "h2_k33_p2_reinsert",
    )
    reinsert_ledger, reinsert_digest = p2_reinsert.audit()
    require(reinsert_digest == p2_reinsert.EXPECTED_LEDGER_SHA256,
            "the P2 reinsertion ledger changed")
    p2_graph = load(
        "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py",
        "h2_k33_p2_graph",
    )
    graph_ledger, graph_digest = p2_graph.audit()
    require(graph_digest == p2_graph.EXPECTED_LEDGER_SHA256,
            "the P2 relative graph ledger changed")
    c2plus = load(
        "computations/verify_h2_b4_cplus_shared_interface_gate.py",
        "h2_k33_c2plus",
    )
    c2_ledger, c2_digest = c2plus.audit()
    require(c2_digest == c2plus.EXPECTED_LEDGER_SHA256,
            "the C2plus shared-interface ledger changed")
    c4 = load(
        "computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py",
        "h2_k33_c4",
    )
    c4_ledger, c4_digest = c4.audit()
    require(c4_digest == c4.EXPECTED_LEDGER_SHA256,
            "the C4 Hasse comparison ledger changed")

    representative = first_ledger["one_endpoint_Hasse_faces"]
    private = reinsert_ledger["second_even_Bminus4_debt"]
    require(representative["representative_word"] == "0102"
            and first_ledger["representative_dual"]["value"] == "-13/6"
            and private["physical_lift_constructed"] is False
            and reinsert_ledger["representative_detector"]
                ["on_private_preimage"] == "35/72",
            "the minimal P2 private coordinate changed")
    carrier = graph_ledger["remaining_carrier_landing"]
    require(carrier["endpoint_even_private_carrier_rank"] == 5
            and graph_ledger["exact_P2_combination"]["boundary"]
                == "t_zprivate-z_private(u)",
            "the universal P2 carrier frontier changed")
    c2_status = c2_ledger["full_interface_and_typing"]
    require(c2_status["physical_restriction_reinsertion_map_constructed"]
            is False,
            "the C2plus restriction map appeared")
    c4_status = c4_ledger["inventory_verdict"]
    require(c4_status["formal_prolonged_Hasse_face_exists"]
            and not c4_status["old_literal_matching_Hasse_column_exists"],
            "the C4 formal/physical distinction changed")

    return {
        "uniform_source_side": {
            "ordinary_Hasse_restriction": "constructed for all types",
            "P2_relative_graph_and_labelled_PP": "constructed",
            "what_is_not_uniformly_landed": "centered direction-tag carrier",
        },
        "minimal_explicit_unfilled_instance": {
            "type": "P2",
            "base_word": "0112",
            "intermediate_word": "0102",
            "residual": "q45:12",
            "reinsertion": "q23:21",
            "top_word_grade": "01211222 / labelled P3+K2",
            "private_detector": "+e0+e3-e1-e6",
            "detector_on_private_face": "-13/6",
            "detector_on_dq23_preimage": "35/72",
            "ordinary_residue_on_dq23_preimage": 0,
            "physical_lift_constructed": False,
        },
        "P2_relative_carrier": {
            "boundary": "t_zprivate-z_private(u)",
            "endpoint_even_private_rank": 5,
            "presentation_safe_while_t_retained": True,
            "setting_t_zero_preserves_H0": False,
        },
        "C2plus_status": (
            "coefficient B-4/delta-plus match is exact; the target-bearing "
            "restriction/reinsertion map is not constructed"
        ),
        "C4_status": (
            "the formal divided-power Hasse face exists; the old literal "
            "site-squarefree source inventory has no labelled relative cell"
        ),
        "smallest_positive_schema": (
            "a centered direction-pair-tagged carrier family, natural for "
            "restriction, root PP and reinsertion.  Its P2 instance must land "
            "the displayed 0102 and dq23 coordinates; C2plus/C4 instances "
            "retain their distinct target and repeated-grade readouts.  This "
            "is one indexed schema, not one fixed untagged column"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    classification = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "h2_k33_classification",
    )
    ledger = {
        "theorem": "h3 H2 K3,3 tagged lower-landing obstruction",
        "pins": PINS,
        "complete_tagged_incidence": tagged_incidence_audit(classification),
        "strongest_h2_placement_status": strongest_h2_status_audit(),
        "answer": (
            "One natural Hasse/PP construction handles the source-side "
            "coefficient aggregates of C2plus, C4 and P2.  It does not give "
            "the physical landing because the untagged restriction has rank "
            "70 on 210 direction pairs and kills 140 centered tag directions. "
            "The minimal explicit unfilled instance is the P2 word-0102 "
            "endpoint-even private carrier (dual -13/6), followed after "
            "q23 reinsertion by the labelled dq coordinate 35/72."
        ),
        "interaction_with_terminal_theorem": (
            "Once the tagged carrier is landed in the complete augmented "
            "cap grade, 4373ae6 extends every local dual through q/ainc/"
            "target/W/ores/ridge and gives protected filler or terminal."
        ),
        "scope": (
            "exact uncoloured site/head incidence and the canonical h2 P2, "
            "C2plus and C4 placement interfaces.  Colouring preserves the "
            "component census but adds the literal fine grades; no physical "
            "tagged carrier is constructed here."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("H2 pair-tail incidence: 70 DISJOINT K3,3 COMPONENTS")
    print("untagged rank 70; direction-tag kernel/cokernel 140")
    print("one uniform source Hasse map: YES; physical tagged landing: NO")
    print("first explicit missing coordinate: P2 0102 (-13/6), dq23 35/72")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
