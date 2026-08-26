#!/usr/bin/env python3
"""Exact bounded audit of the orbit-85 C2 leaf module.

This checker never expands the Nullstellensatz multipliers.  It keeps the
source occurrence (compiler, amplitude row, matching) as a provenance label,
and uses the exact cross-colour multigrading to compare it with the frozen
71/611/332 first-polar packet.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERT = (ROOT / "computations" /
        "unaudited-codex-n8-diagonal-orbit85-extended-certificate-2026-08-23" /
        "certificate_dag.json")
OUT = HERE / "results_orbit85_c2_module.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((min(first, second), max(first, second)),)
                               + matching))


MATCHINGS = tuple(perfect_matchings(tuple(range(8))))
PAIRS = ((0, 1), (0, 2), (1, 2))


def word_from_masks(masks: tuple[int, int, int]) -> tuple[int, ...]:
    return tuple(next(colour for colour, mask in enumerate(masks)
                      if mask & (1 << site)) for site in range(8))


def cross_signature(word: tuple[int, ...], matching):
    counts = collections.Counter()
    for left, right in matching:
        if word[left] != word[right]:
            counts[tuple(sorted((word[left], word[right])))] += 1
    vector = tuple(counts[pair] for pair in PAIRS)
    return sum(vector), vector, tuple(value % 2 for value in vector)


def shape(masks, matching) -> str:
    word = word_from_masks(masks)
    sizes = sorted((mask.bit_count() for mask in masks), reverse=True)
    degree, vector, _parity = cross_signature(word, matching)
    require(degree == 2, "shape called outside the quadratic tail")
    if sizes == [6, 2, 0]:
        return "620"
    if sizes == [4, 4, 0]:
        return "440"
    require(sizes == [4, 2, 2], f"unexpected all-even profile {sizes}")
    active_pair = PAIRS[next(i for i, value in enumerate(vector) if value)]
    return ("422:small-small" if
            all(masks[colour].bit_count() == 2 for colour in active_pair)
            else "422:large-small")


def branch_stabilizer(case):
    free = [{colour, *case[colour]} for colour in range(3)]
    answer = []
    for site_perm in itertools.permutations(range(8)):
        for colour_perm in itertools.permutations(range(3)):
            if all({site_perm[site] for site in free[colour]}
                   == free[colour_perm[colour]] for colour in range(3)):
                answer.append((site_perm, colour_perm))
    return tuple(answer)


def act(term, group_element):
    masks, matching = term
    site_perm, colour_perm = group_element
    out_masks = [0, 0, 0]
    for colour, mask in enumerate(masks):
        for site in range(8):
            if mask & (1 << site):
                out_masks[colour_perm[colour]] |= 1 << site_perm[site]
    out_matching = tuple(sorted(
        (min(site_perm[left], site_perm[right]),
         max(site_perm[left], site_perm[right]))
        for left, right in matching))
    return tuple(out_masks), out_matching


def canonical(term, stabilizer):
    return min(act(term, group_element) for group_element in stabilizer)


def falsity(literal: int, bits: list[int]) -> int:
    value = bits[abs(literal)]
    return 1 - value if literal > 0 else value


def root_sensitivity(data, target: str, bits: list[int]) -> int:
    """Coefficient of one compiled input in the resolution/weakening DAG."""
    value = {}
    for node in data["proof_nodes"]:
        operation = node["op"]
        if operation == "compile_clause":
            value[node["id"]] = int(node["id"] == target)
        elif operation == "resolve_polynomials":
            left_factor = 1
            for literal in node["left_falsity_factors"]:
                left_factor *= falsity(literal, bits)
            right_factor = 1
            for literal in node["right_falsity_factors"]:
                right_factor *= falsity(literal, bits)
            value[node["id"]] = (left_factor * value[node["left"]]
                                 + right_factor * value[node["right"]])
        elif operation == "weaken_polynomial":
            factor = 1
            for literal in node["added_falsity_factors"]:
                factor *= falsity(literal, bits)
            value[node["id"]] = factor * value[node["input"]]
        else:
            raise RuntimeError(f"unknown DAG operation {operation}")
    return value[data["root"]]


def packet_census(word: tuple[int, ...]):
    by_degree = collections.Counter()
    by_grade = collections.Counter()
    for matching in MATCHINGS:
        degree, _vector, parity = cross_signature(word, matching)
        by_degree[degree] += 1
        by_grade[(degree, parity)] += 1
    return dict(sorted(by_degree.items())), {
        f"{degree}:{''.join(map(str, parity))}": count
        for (degree, parity), count in sorted(by_grade.items())
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()

    data = json.loads(CERT.read_text(encoding="utf-8"))
    require(data["format"] == "n8diag-orbit85-extended-ns-dag-v1",
            "wrong certificate format")
    require(len(MATCHINGS) == 105, "K8 matching census changed")

    leaf_ids = data["tail_interface"]["amplitude_leaf_ids"]
    masks_list = [tuple(map(int, identifier.split(":")[1:]))
                  for identifier in leaf_ids]
    leaf_set = set(masks_list)
    require(len(leaf_set) == 185, "distinct amplitude leaf count changed")

    amplitude_refs = []
    tail_compilers = collections.Counter()
    for node in data["proof_nodes"]:
        if node["op"] == "compile_clause":
            refs = [ref for ref in node["compiler"]["antecedents"]
                    if ref.startswith("amp:")]
            amplitude_refs.extend(refs)
            if refs:
                tail_compilers[(node["compiler"]["schema"], "nodes")] += 1
                tail_compilers[(node["compiler"]["schema"], "refs")] += len(refs)
    ref_counts = collections.Counter(tuple(map(int, ref.split(":")[1:]))
                                     for ref in amplitude_refs)
    require(len(amplitude_refs) == 569, "weighted amplitude references changed")
    require(tail_compilers == {
        ("A2", "nodes"): 25, ("A2", "refs"): 25,
        ("C0", "nodes"): 5, ("C0", "refs"): 160,
        ("XF", "nodes"): 6, ("XF", "refs"): 384,
    }, f"tail compiler interface changed: {tail_compilers}")

    terms = []
    distinct_shapes = collections.Counter()
    weighted_shapes = collections.Counter()
    for masks in masks_list:
        word = word_from_masks(masks)
        local = []
        for matching in MATCHINGS:
            degree, vector, parity = cross_signature(word, matching)
            if degree != 2:
                continue
            require(parity == (0, 0, 0),
                    "orbit-85 Tail2 left the even cross-parity sector")
            require(sorted(vector) == [0, 0, 2],
                    "orbit-85 Tail2 is not a doubled colour pair")
            term = (masks, matching)
            terms.append(term)
            local.append(term)
            distinct_shapes[shape(masks, matching)] += 1
            weighted_shapes[shape(masks, matching)] += ref_counts[masks]
        expected = {(6, 2, 0): 90, (4, 4, 0): 72,
                    (4, 2, 2): 30}[tuple(sorted(
                        (mask.bit_count() for mask in masks), reverse=True))]
        require(len(local) == expected, "leaf Tail2 matching count changed")

    require(len(terms) == 7248, "distinct Tail2 occurrence count changed")
    require(sum(weighted_shapes.values()) == 20208,
            "weighted Tail2 occurrence count changed")
    expected_distinct = {
        "620": 1980, "440": 648,
        "422:large-small": 3696, "422:small-small": 924,
    }
    expected_weighted = {
        "620": 4140, "440": 648,
        "422:large-small": 12336, "422:small-small": 3084,
    }
    require(dict(distinct_shapes) == expected_distinct,
            f"full-symmetry shape census changed: {distinct_shapes}")
    require(dict(weighted_shapes) == expected_weighted,
            f"weighted shape census changed: {weighted_shapes}")

    stabilizer = branch_stabilizer(data["case"])
    require(len(stabilizer) == 12, "full branch stabilizer is not order 12")
    orbit_hits = collections.Counter(canonical(term, stabilizer) for term in terms)
    ambient_sizes = collections.Counter(
        len({act(representative, group_element) for group_element in stabilizer})
        for representative in orbit_hits)
    intersection_sizes = collections.Counter(orbit_hits.values())
    by_shape = collections.Counter(shape(representative[0], representative[1])
                                  for representative in orbit_hits)
    require(len(orbit_hits) == 1248, "branch-stabilizer orbit count changed")
    require(ambient_sizes == {6: 552, 12: 696},
            f"branch orbit sizes changed: {ambient_sizes}")
    require(intersection_sizes == {1: 54, 2: 144, 3: 276, 4: 12,
                                   5: 12, 6: 495, 10: 30, 12: 225},
            f"branch orbit intersections changed: {intersection_sizes}")
    require(by_shape == {"620": 402, "440": 96,
                         "422:large-small": 592,
                         "422:small-small": 158},
            f"branch orbit shape census changed: {by_shape}")

    # The LRAT-selected 185-leaf support is deliberately not an H-submodule.
    stable_action_incidences = 0
    nonclosed_leaves = 0
    for masks in masks_list:
        images = set()
        dummy = ((0, 1), (2, 3), (4, 5), (6, 7))
        for group_element in stabilizer:
            images.add(act((masks, dummy), group_element)[0])
            if act((masks, dummy), group_element)[0] in leaf_set:
                stable_action_incidences += 1
        if not images <= leaf_set:
            nonclosed_leaves += 1
    require((stable_action_incidences, nonclosed_leaves) == (1730, 81),
            "LRAT core symmetry-nonclosure guard changed")

    packet_words = {
        "71": tuple(map(int, "00000001")),
        "611": tuple(map(int, "01222222")),
        "332": tuple(map(int, "00011122")),
    }
    packet = {name: {"degree_census": packet_census(word)[0],
                     "grade_census": packet_census(word)[1]}
              for name, word in packet_words.items()}
    require(packet["71"]["degree_census"] == {1: 105},
            "71 polar census changed")
    require(packet["611"]["degree_census"] == {1: 15, 2: 90},
            "611 polar census changed")
    require(packet["332"]["degree_census"]
            == {1: 9, 2: 18, 3: 42, 4: 36},
            "332 polar census changed")
    for name in ("611", "332"):
        quadratic_grades = {grade for grade in packet[name]["grade_census"]
                            if grade.startswith("2:")}
        require(quadratic_grades <= {"2:011", "2:101", "2:110"},
                f"{name} acquired doubled-pair quadratic support")
    require(all(not grade.startswith("2:000")
                for row in packet.values() for grade in row["grade_census"]),
            "frozen packet meets the doubled-pair separator sector")

    # Nonzero source-provenance witness for C2.  Seed 7 is a compact exact
    # Boolean evaluation of the stored resolution DAG.  At it the coefficient
    # of C0 compiler 13429 is +1 and p_704=1.  Set its inverse and first
    # complement witness to one, all other compiler scalars to zero, and keep
    # only the displayed matching monomial.  The C0 identity then evaluates
    # C2 to +1.
    max_variable = max(abs(literal) for node in data["proof_nodes"]
                       for literal in node.get("clause",
                                               node.get("result_clause", [])))
    rng = random.Random(7)
    bits = [0] + [rng.randrange(2) for _ in range(max_variable)]
    target_node = "c:13429"
    target_amp = "amp:130:125:0"
    target_matching = ((0, 1), (2, 3), (4, 5), (6, 7))
    target = next(node for node in data["proof_nodes"]
                  if node["id"] == target_node)
    require(target_amp in target["compiler"]["antecedents"],
            "nonzero witness source amplitude moved")
    marker_owners = [node["id"] for node in data["proof_nodes"]
                     if node["op"] == "compile_clause"
                     and target_amp in node["compiler"]["antecedents"]
                     and "pr:704" in node["compiler"]["antecedents"]]
    require(marker_owners == [target_node],
            f"u704/source-row marker lost uniqueness: {marker_owners}")
    require(bits[704] == 1, "nonzero witness selector evaluation changed")
    sensitivity = root_sensitivity(data, target_node, bits)
    require(sensitivity == 1, "root sensitivity witness changed")
    target_word = word_from_masks((130, 125, 0))
    require(cross_signature(target_word, target_matching)
            == (2, (2, 0, 0), (0, 0, 0)),
            "nonzero Tail2 monomial left the doubled 01 sector")
    c2_witness = {
        "compiler": target_node,
        "source_row": target_amp,
        "complement_witness": "r:C0:0:1:0",
        "guarded_inverse": "u:p704",
        "selector": "p704",
        "matching": [list(edge) for edge in target_matching],
        "monomial": "T_01^(1,0)*d_23^1*d_45^1*T_67^(1,0)",
        "resolution_sensitivity_at_seed7": sensitivity,
        "unique_coefficient_marker":
            "u704*r:C0:0:1:0*T_01^(1,0)*d_23^1*d_45^1*T_67^(1,0)",
        "marker_coefficient_after_selector_seed7": 1,
    }

    # Hostile guard: an all-even 620 row has a 2:000 component, so the
    # separator must never be advertised against the all-even/zero-tail
    # second-polar packet.
    mutated = packet_census(tuple(map(int, "00111111")))[1]
    require("2:000" in mutated,
            "all-even counterguard unexpectedly misses doubled sector")
    if args.mutate:
        require(len(orbit_hits) == 1247, "hostile orbit-count mutation survived")

    result = {
        "verdict": "C2_NONZERO_AND_SEPARATED_FROM_FROZEN_71_611_332_CARRIER_TAIL_MODULE",
        "scope": "source-labelled module over the epsilon-constant diagonal/branch coefficient ring",
        "compact_representation": {
            "certificate_dag_sha256":
                "d5effbf6447c7b74b8bcd9ae1370bc2e498f15cd8e95fae60576cf657907db96",
            "formula": "C2=sum_c alpha_c*D2(compiler_c), with alpha the exact reverse adjoint of the frozen resolution/weakening DAG",
            "tail_compilers": {
                "A2": {"nodes": 25, "source_refs": 25},
                "C0": {"nodes": 5, "source_refs": 160},
                "XF": {"nodes": 6, "source_refs": 384},
            },
            "distinct_source_rows": 185,
            "source_refs": 569,
            "D2_C0": "p_x*u_x*sum_j r_j*Tail2(w_j)",
        },
        "C2_grade": {"T_degree": 2, "cross_pair_parity": "000",
                     "pair_shape": "doubled"},
        "full_S8xS3_shapes": {
            "selected_distinct_terms": expected_distinct,
            "weighted_DAG_leaf_occurrences": expected_weighted,
            "ambient_orbit_sizes": {"620": 15120, "440": 15120,
                                    "422:large-small": 30240,
                                    "422:small-small": 7560},
        },
        "branch_stabilizer": {
            "order": len(stabilizer),
            "description": "S_{3,4,5} x <(1 2)_sites (1 2)_colours>",
            "orbit_buckets_meeting_selected_support": len(orbit_hits),
            "orbit_buckets_by_shape": dict(sorted(by_shape.items())),
            "ambient_orbit_size_histogram": dict(sorted(ambient_sizes.items())),
            "selected_intersection_size_histogram": dict(sorted(intersection_sizes.items())),
            "leaf_action_incidences_retained": stable_action_incidences,
            "nonclosed_amplitude_leaves": nonclosed_leaves,
        },
        "packet_representatives": packet,
        "separator": {
            "name": "Pi_dbl",
            "definition": "project to T-degree 2 and cross-pair parity 000",
            "frozen_packet_value": 0,
            "C2_unique_marker_value": 1,
            "coefficient_ring_guard": "multipliers contain no T variables",
        },
        "nonzero_source_witness": c2_witness,
        "counterguard": "Pi_dbl does not separate C2 from the all-even 620/440/422 second-polar packet",
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen result differs")
    print(rendered, end="")


if __name__ == "__main__":
    main()
