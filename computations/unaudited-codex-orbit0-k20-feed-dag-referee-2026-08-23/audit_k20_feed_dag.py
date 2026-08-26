#!/usr/bin/env python3
"""Independent source-labelled K20 feed-DAG and sign referee.

No K20 residual or charge is computed.  The audit enumerates degree paths,
pins the frozen discarded K16 population, and gives one literal K14 head whose
discarded K16/K18 descendants prove that the hidden (2,4) and (2,2,2)
lineages are structurally live.
"""

from __future__ import annotations

import ast
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SIGN_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-sign-referee-2026-08-23"
               / "audit_filtered_k16_sign.py")
K16_LITERAL = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
               / "results_orbit0_k16_literal_residual.json")
K16_FILTERED = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
                / "results_filtered_k16_run.json")
CYCLE_RESULT = (ROOT / "computations/unaudited-codex-orbit0-filtered-k20-interface-audit-2026-08-23"
                / "results_filtered_k20_interface.json")
CYCLE_SUPERSESSION = (ROOT / "computations/unaudited-codex-orbit0-filtered-k20-interface-audit-2026-08-23"
                      / "REPORT_K14_DAG_SUPERSESSION.md")
ARITH_RESULT = (ROOT / "computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23"
                / "results_k19_k24_arithmetic.json")
OUT = HERE / "results_k20_feed_dag_referee.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


S = load("k20_dag_sign", SIGN_SOURCE)
F, D = S.F, S.D


def compositions(total, parts=(2, 3, 4)):
    if total == 0:
        return ((),)
    answer = []
    for part in parts:
        if part <= total:
            for tail in compositions(total - part, parts):
                answer.append((part,) + tail)
    return tuple(answer)


def direct_packets():
    counts = {2: 12, 3: 32, 4: 60}
    profiles = {}
    for a in counts:
        for b in counts:
            for c in counts:
                degree = 8 + a + b + c
                if 14 <= degree <= 20:
                    profile = tuple(sorted((a, b, c)))
                    profiles.setdefault(degree, Counter())[profile] += \
                        counts[a] * counts[b] * counts[c]
    # The loop counts labelled placements.  Identical degree triples appear
    # once per labelled order, exactly as in E0*E1*E2.
    return {
        degree: {"+".join(map(str, profile)): value
                 for profile, value in sorted(packet.items())}
        for degree, packet in sorted(profiles.items())
    }


def lex_hidden_lineage_sentinel():
    cover_raw = json.loads(S.COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in
                      cover_raw["single_pivot_cover"]
                      ["minimum_cover_orbit_representatives"])
    anchor_cells = D.CTX.anchor_cells

    def signature(row):
        counts = Counter(row)
        return tuple(counts[cell] for cell in anchor_cells)

    def valid_pivots(sig):
        answer = []
        for pivot in D.CTX.pivots(sig):
            base = tuple(left - right for left, right in
                         zip(sig, D.CTX.vectors[pivot], strict=True))
            survivors = set()
            for tail in D.CTX.tails[pivot][2]:
                counts = Counter(tail)
                child = tuple(left + counts[cell] for left, cell in
                              zip(base, anchor_cells, strict=True))
                if not D.CTX.pivots(child):
                    survivors.add(D.CTX.canonical_signature(child))
            if survivors <= cover:
                answer.append(pivot)
        require(answer, sig)
        return tuple(answer)

    words = tuple(F.word_from_pair_colours(row) for row in F.PAIR_COLOURS)
    anchors = tuple(F.BASE.term_ids(word, F.M0) for word in words)
    errors2 = tuple(Counter({term: 1 for term in F.BASE.word_terms(word)
                             if term != anchor and F.row_k_degree(term) == 2})
                    for word, anchor in zip(words, anchors, strict=True))
    packet = F.polynomial_product(F.polynomial_product(errors2[0], errors2[1]),
                                  errors2[2])
    head = min(bytes(sorted(r8 + packet_row))
               for r8, _orbit_size, _coefficient in D.r8_h_records()
               for packet_row in packet)
    first_pivots = valid_pivots(signature(head))
    require(first_pivots == (70,), first_pivots)
    first_pivot = first_pivots[0]
    quotient = Counter(head)
    quotient.subtract(D.CTX.anchors[first_pivot])
    multiplier = bytes(sorted(quotient.elements()))

    k16_histogram = Counter()
    pivotable_k16 = []
    for tail_index, tail in enumerate(D.CTX.tails[first_pivot][2]):
        child = bytes(sorted(multiplier + tail))
        pivots = D.CTX.pivots(signature(child))
        k16_histogram[len(pivots)] += 1
        if pivots:
            pivotable_k16.append((tail_index, tail, child, pivots))
    require(k16_histogram == {0: 10, 3: 2}, k16_histogram)

    k18_histogram = Counter()
    pivotable_k18 = []
    for k16_tail_index, _tail, child, pivots in pivotable_k16:
        for pivot in pivots:
            quotient = Counter(child)
            quotient.subtract(D.CTX.anchors[pivot])
            child_multiplier = bytes(sorted(quotient.elements()))
            for tail_index, tail in enumerate(D.CTX.tails[pivot][2]):
                grandchild = bytes(sorted(child_multiplier + tail))
                grandpivots = D.CTX.pivots(signature(grandchild))
                k18_histogram[len(grandpivots)] += 1
                if grandpivots:
                    pivotable_k18.append((k16_tail_index, pivot, tail_index,
                                          tail, grandchild, grandpivots))
    require(k18_histogram == {0: 64, 1: 8}, k18_histogram)
    first_k16 = pivotable_k16[0]
    first_k18 = pivotable_k18[0]
    return {
        "K14_head": head.hex(),
        "K14_valid_pivot": first_pivot,
        "K14_pivot_word": "".join(map(str, D.CTX.words[first_pivot])),
        "K14_pivot_anchor": D.CTX.anchors[first_pivot].hex(),
        "K16_K2_child_pivot_histogram": dict(sorted(k16_histogram.items())),
        "pivotable_K16_children": len(pivotable_k16),
        "first_pivotable_K16": {
            "tail_index": first_k16[0],
            "tail": first_k16[1].hex(),
            "row": first_k16[2].hex(),
            "all_pivots": list(first_k16[3]),
        },
        "K18_second_K2_child_pivot_histogram": dict(sorted(k18_histogram.items())),
        "pivotable_K18_provider_children": len(pivotable_k18),
        "first_pivotable_K18": {
            "K16_tail_index": first_k18[0],
            "K16_pivot": first_k18[1],
            "tail_index": first_k18[2],
            "tail": first_k18[3].hex(),
            "row": first_k18[4].hex(),
            "all_pivots": list(first_k18[5]),
        },
    }


def main():
    k16_literal = json.loads(K16_LITERAL.read_text())
    k16_filtered = json.loads(K16_FILTERED.read_text())
    cycle = json.loads(CYCLE_RESULT.read_text())
    arithmetic = json.loads(ARITH_RESULT.read_text())
    require(cycle["logical_sha256"] ==
            "8dc4eb6cce02ea7ca7d2830e7c34409e2aa17d87d66267e28ecbdda04f3159e5",
            "Cycle K20 interface changed")
    require(cycle["status"] == "RETRACTED_INCOMPLETE_K20_DAG_NO_PREFIX_RUN",
            cycle["status"])
    require(k16_literal["collection"]
            ["reducible_K16_tail_occurrences"] == 75691040,
            "discarded K14/K2 K16 population changed")
    require("Higher tails emitted by K15/K16 pivots are not constructed"
            in k16_filtered["scope"], k16_filtered["scope"])
    require(arithmetic["logical_sha256"] ==
            "f77bc67518a2bf8611e88a4eaa7995b1896c96a5882d29d55647f1a7e0605610",
            "arithmetic plan changed")
    require(arithmetic["hidden_higher_tail_guard"]
            ["K20_maximum_pivot_denominator_depth"] == 3,
            arithmetic["hidden_higher_tail_guard"])
    require(arithmetic["hidden_higher_tail_guard"]
            ["K20_depth3_product_lcm"] == 400591699200,
            arithmetic["hidden_higher_tail_guard"])

    packets = direct_packets()
    packet_totals = {degree: sum(packet.values())
                     for degree, packet in packets.items()}
    require(packet_totals == {
        14: 1728, 15: 13824, 16: 62784, 17: 171008,
        18: 313920, 19: 345600, 20: 216000,
    }, packet_totals)

    paths = []
    for source_degree in range(14, 21):
        for increments in compositions(20 - source_degree):
            transitions = len(increments)
            # Every direct source packet has sign -R8'.  Every cancellation
            # transition adds one further minus sign.
            sign = "positive" if transitions % 2 else "negative"
            paths.append({
                "source_degree": source_degree,
                "increments": list(increments),
                "denominator_depth": transitions,
                "sign_relative_to_R8prime": sign,
            })
    require(len(paths) == 11, len(paths))
    require(not any(row["source_degree"] == 19 for row in paths), paths)
    require(max(row["denominator_depth"] for row in paths) == 3, paths)

    sentinel = lex_hidden_lineage_sentinel()
    expected_hidden = {
        (14, (2, 4)): "negative",
        (14, (2, 2, 2)): "positive",
    }
    actual_hidden = {
        (row["source_degree"], tuple(row["increments"])):
            row["sign_relative_to_R8prime"]
        for row in paths
        if row["source_degree"] == 14
        and tuple(row["increments"]) in ((2, 4), (2, 2, 2))
    }
    require(actual_hidden == expected_hidden, actual_hidden)

    result = {
        "status": "REFEREE_FAIL_CYCLE_K20_INTERFACE_OMITS_HIDDEN_K14_CHAINS",
        "recurrence": (
            "B_d=D_d+sum_{j=2,3,4} T_j(Piv(B_{d-j})), where "
            "T_j(c row)=-c/|pivots(row)| times all K_j tails"
        ),
        "direct_packets_per_R8_H_slice": packets,
        "direct_packet_totals_per_R8_H_slice": packet_totals,
        "direct_packet_totals_all_485_slices": {
            degree: 485 * count for degree, count in packet_totals.items()},
        "complete_primitive_K20_paths": paths,
        "degree_guard": {
            "K17_feeds_K20": "yes, by one K3 transition",
            "K19_feeds_K20": "no, minimum transition is K2 and lands at K21",
            "odd_layer_guard": (
                "odd degree alone is not an exclusion: K15 and K17 feed; only "
                "the distance-one K19 layer cannot"
            ),
        },
        "cycle_interface_comparison": {
            "cycle_logical_sha256": cycle["logical_sha256"],
            "cycle_initial_declared_lineages": 10,
            "complete_primitive_paths": len(paths),
            "unsound_zero_lineage": "K14 --K2--> K16 --K4--> K20",
            "missing_lineage": "K14 --K2--> K16 --K2--> K18 --K2--> K20",
            "reason": (
                "the frozen K14/K2 artifact is already the nonpivotable K16 "
                "normal; it omits the higher tails of the reducible raw K16 "
                "children and cannot prove their outgoing lineages empty"
            ),
        },
        "discarded_population": {
            "reducible_K14_K2_K16_tail_occurrences": 75691040,
            "frozen_scope": k16_filtered["scope"],
        },
        "literal_live_counterexample": sentinel,
        "denominators": {
            "maximum_depth": 3,
            "K14_policy": "frozen 25-cover-valid pivot average",
            "later_policy": "average all literal dividing K0 pivots",
            "one_step_scale": 281801520,
            "certified_global_scale": arithmetic["recommended_single_integer_scale"],
            "K20_depth3_distinct_products": len(arithmetic["hidden_higher_tail_guard"]
                                                    ["K20_depth3_products"]),
            "guard": (
                "The independent arithmetic DP explicitly propagated the hidden "
                "depth-three path: all 142 products have LCM 400591699200. Thus "
                "the existing global U remains valid even though the feed DAG "
                "and active residual recurrence still omitted the lineage."
            ),
        },
        "missing_provenance": {
            "first": (
                "retain every reducible raw K14/K2 K16 child with its K14 head, "
                "valid-pivot denominator, literal pivot and coefficient"
            ),
            "second": (
                "for each such K16 child, emit both K4 tails directly to K20 "
                "and K2 tails to a collected K18 parent stream under all-pivot averaging"
            ),
            "third": (
                "for pivotable K18 descendants, emit K2 tails to K20 with the "
                "three-count denominator product and exact H-orbit mass"
            ),
            "existing_Cycle_K18_gap": (
                "The K18 charge run retained scalar charges/evaluation counts "
                "only; its outgoing parent profiles were not serialized."
            ),
        },
        "pinned": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in (SIGN_SOURCE, K16_LITERAL, K16_FILTERED, CYCLE_RESULT,
                         CYCLE_SUPERSESSION, ARITH_RESULT)
        },
        "scope": (
            "Exact DAG/sign/provenance referee and one literal live sentinel; "
            "no K20 row, charge, profile closure or coefficient cancellation solve."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
