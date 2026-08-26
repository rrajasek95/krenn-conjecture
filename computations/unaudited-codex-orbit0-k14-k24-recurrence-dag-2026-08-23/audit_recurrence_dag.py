#!/usr/bin/env python3
"""Complete source-lineage recurrence/provenance DAG for K14..K24.

This is a signature-level/source-provenance audit.  It never constructs a
residual row stream.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import product
from math import lcm
import argparse
import ast
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
COVER = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
         / "results_k16_anchor_cover.json")
ARITH = (ROOT / "computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23"
         / "results_k19_k24_arithmetic.json")
K16 = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
       / "results_filtered_k16_run.json")
K17 = K16.with_name("results_filtered_k17_run.json")
K18 = (ROOT / "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23"
       / "results_k18_charge.json")
K19 = (ROOT / "computations/unaudited-codex-orbit0-k19-charge-2026-08-23"
       / "results_k19_charge.json")
OUT = HERE / "results_recurrence_dag.json"
TEMPLATE = HERE / "interface_template_K20.json"

TAIL_COUNTS = {2: 12, 3: 32, 4: 60}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def node_id(triple, responses):
    direct = "".join(map(str, triple))
    tail = "direct" if not responses else "-".join(map(str, responses))
    return f"D{8 + sum(triple)}:{direct}|R:{tail}"


def disposition(triple, responses, degree, reachable):
    if not reachable:
        return {
            "state": "PROVEN_EMPTY_SIGNATURE_CLASS",
            "rows_retained": False,
            "downstream_coverage": "NOT_REQUIRED",
            "evidence": [],
        }

    direct_degree = 8 + sum(triple)
    discarded_prefix = direct_degree == 14 and responses[:1] == (2,)
    if discarded_prefix:
        if len(responses) == 1:
            return {
                "state": "PARTIAL_IRREDUCIBLE_ONLY_PIVOTABLE_DISCARDED",
                "rows_retained": "irreducible K16 normal only",
                "downstream_coverage": "INCOMPLETE",
                "evidence": [str(K16.relative_to(ROOT))],
            }
        return {
            "state": "MISSING_DISCARDED_K14_K2_PIVOTABLE_PARENT",
            "rows_retained": False,
            "downstream_coverage": "MISSING",
            "evidence": [],
        }

    if not responses:
        if degree == 14:
            state = "SOURCE_RECONSTRUCTIBLE_K14_HEADS_CANCELLED"
            evidence = [str(COVER.relative_to(ROOT))]
        elif degree == 15:
            state = "LITERAL_CHECKPOINT_THEN_FULLY_PIVOTED"
            evidence = [str(K16.relative_to(ROOT))]
        elif degree == 16:
            state = "LITERAL_DIRECT_CHECKPOINT_SPLIT_PIVOTABLE_NORMAL"
            evidence = [str(K16.relative_to(ROOT))]
        elif degree == 17:
            state = "EXACT_CHARGE_ONLY_NO_ROWS"
            evidence = [str(K17.relative_to(ROOT))]
        elif degree == 18:
            state = "EXACT_COMPONENT_CHARGE_ONLY_NO_ROWS"
            evidence = [str(K18.relative_to(ROOT))]
        elif degree == 19:
            state = "EXACT_COMPONENT_CHARGE_ONLY_NO_ROWS"
            evidence = [str(K19.relative_to(ROOT))]
        else:
            state = "NOT_RUN_SOURCE_RECONSTRUCTIBLE"
            evidence = []
        return {
            "state": state,
            "rows_retained": degree in (15, 16),
            "downstream_coverage": "PENDING" if degree >= 20 else "SOURCE_AVAILABLE",
            "evidence": evidence,
        }

    # Exact scalar pages that were computed from complete source
    # reconstructions, excluding the discarded K14/K2 subtree above.
    if degree == 17:
        return {
            "state": "EXACT_CHARGE_ONLY_NO_ROWS",
            "rows_retained": False,
            "downstream_coverage": "SOURCE_RECONSTRUCTION_REQUIRED",
            "evidence": [str(K17.relative_to(ROOT))],
        }
    if degree == 18:
        return {
            "state": "EXACT_COMPONENT_CHARGE_ONLY_NO_ROWS",
            "rows_retained": False,
            "downstream_coverage": "SOURCE_RECONSTRUCTION_REQUIRED",
            "evidence": [str(K18.relative_to(ROOT))],
        }
    if degree == 19:
        return {
            "state": "EXACT_COMPONENT_CHARGE_ONLY_NO_ROWS",
            "rows_retained": False,
            "downstream_coverage": "SOURCE_RECONSTRUCTION_REQUIRED",
            "evidence": [str(K19.relative_to(ROOT))],
        }
    if degree == 16:
        return {
            "state": "LITERAL_NORMAL_ONLY_PARENT_PIVOTABLE_STREAM_NOT_CHECKPOINTED",
            "rows_retained": "normal only",
            "downstream_coverage": "SOURCE_RECONSTRUCTION_REQUIRED",
            "evidence": [str(K16.relative_to(ROOT))],
        }
    return {
        "state": "NOT_RUN_SOURCE_RECONSTRUCTION_REQUIRED",
        "rows_retained": False,
        "downstream_coverage": "PENDING",
        "evidence": [],
    }


def build():
    d = load("recurrence_dag_design", DESIGN)
    cover_raw = json.loads(COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in
                      cover_raw["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    require(len(cover) == 25, len(cover))
    arithmetic = json.loads(ARITH.read_text())
    require(arithmetic["hidden_higher_tail_guard"]
            ["K20_maximum_pivot_denominator_depth"] == 3,
            arithmetic["hidden_higher_tail_guard"])
    require(arithmetic["hidden_higher_tail_guard"]
            ["K24_maximum_pivot_denominator_depth"] == 4,
            arithmetic["hidden_higher_tail_guard"])

    tail_signatures = {}
    for pivot in range(78):
        for shift in (2, 3, 4):
            signatures = set()
            for tail in d.CTX.tails[pivot][shift]:
                counts = Counter(tail)
                signatures.add(tuple(counts[cell] for cell in d.CTX.anchor_cells))
            require(len(signatures) == {2: 6, 3: 4, 4: 1}[shift],
                    (pivot, shift, len(signatures)))
            tail_signatures[pivot, shift] = signatures

    factor_words = tuple(d.F.word_from_pair_colours(row) for row in d.F.PAIR_COLOURS)
    factor_pivots = tuple(d.CTX.anchor_to_pivot[d.F.BASE.term_ids(word, d.F.M0)]
                          for word in factor_words)
    r8_signatures = {d.CTX.signature(row)
                     for row, _size, _coefficient in d.r8_h_records()}

    def direct_states(triple):
        answer = defaultdict(set)
        for r8 in r8_signatures:
            for additions in product(*(tail_signatures[factor_pivots[f], triple[f]]
                                       for f in range(3))):
                child = tuple(r8[i] + sum(addition[i] for addition in additions)
                              for i in range(12))
                require(sum(child) == 16 - sum(triple), (triple, child))
                answer[child].add(1)
        return answer

    def k14_valid(signature):
        answer = []
        for pivot in d.CTX.pivots(signature):
            base = tuple(left - right for left, right in
                         zip(signature, d.CTX.vectors[pivot], strict=True))
            survivors = set()
            for addition in tail_signatures[pivot, 2]:
                child = tuple(base[i] + addition[i] for i in range(12))
                if not d.CTX.pivots(child):
                    survivors.add(d.CTX.canonical_signature(child))
            if survivors <= cover:
                answer.append(pivot)
        require(answer, signature)
        return tuple(answer)

    def advance(states, parent_degree, shift):
        answer = defaultdict(set)
        for signature, products_here in states.items():
            pivots = (k14_valid(signature) if parent_degree == 14
                      else d.CTX.pivots(signature))
            if not pivots:
                continue
            count = len(pivots)
            for pivot in pivots:
                base = tuple(signature[i] - d.CTX.vectors[pivot][i]
                             for i in range(12))
                for addition in tail_signatures[pivot, shift]:
                    child = tuple(base[i] + addition[i] for i in range(12))
                    require(all(0 <= value <= 2 for value in child), child)
                    answer[child].update(value * count for value in products_here)
        return answer

    nodes = []
    edges = []
    states_by_id = {}
    for triple in product((2, 3, 4), repeat=3):
        start_degree = 8 + sum(triple)
        start_id = node_id(triple, ())
        states_by_id[start_id] = direct_states(triple)
        queue = deque([(triple, (), start_degree)])
        seen = set()
        while queue:
            triple_now, responses, degree = queue.popleft()
            current_id = node_id(triple_now, responses)
            if current_id in seen:
                continue
            seen.add(current_id)
            states = states_by_id[current_id]
            products_here = sorted({value for values in states.values() for value in values})
            current = disposition(triple_now, responses, degree, bool(states))
            product_class = None
            if products_here:
                product_class = {
                    "pivot_depth": len(responses),
                    "distinct_products": len(products_here),
                    "products": products_here,
                    "maximum_product": max(products_here),
                    "product_lcm": lcm(*products_here),
                    "global_scale_divides": 400_591_699_200 % lcm(*products_here) == 0,
                }
            nodes.append({
                "id": current_id,
                "direct_packet": {
                    "ordered_factor_shifts": list(triple_now),
                    "degree": 8 + sum(triple_now),
                    "tail_term_count": (TAIL_COUNTS[triple_now[0]]
                                        * TAIL_COUNTS[triple_now[1]]
                                        * TAIL_COUNTS[triple_now[2]]),
                    "initial_sign": -1,
                },
                "response_shifts": list(responses),
                "degree": degree,
                "sign_relative_to_unsigned_R8prime": -1 if len(responses) % 2 == 0 else 1,
                "reachable": bool(states),
                "reachable_anchor_signatures": len(states),
                "denominator_product_class": product_class,
                "current_provenance": current,
            })
            if degree <= 20 and states:
                for shift in (2, 3, 4):
                    child_degree = degree + shift
                    if child_degree > 24:
                        continue
                    child_responses = responses + (shift,)
                    child_id = node_id(triple_now, child_responses)
                    child_states = advance(states, degree, shift)
                    states_by_id[child_id] = child_states
                    edges.append({
                        "parent": current_id,
                        "child": child_id,
                        "shift": shift,
                        "tail_terms_per_pivot": TAIL_COUNTS[shift],
                        "pivot_policy": ("frozen_valid_K14" if degree == 14
                                         else "all_literal_dividing_pivots"),
                        "coefficient_rule": "child coefficient = -parent coefficient / pivot_count",
                        "child_reachable": bool(child_states),
                    })
                    queue.append((triple_now, child_responses, child_degree))

    nodes.sort(key=lambda item: item["id"])
    edges.sort(key=lambda item: (item["parent"], item["shift"]))
    reachable = [node for node in nodes if node["reachable"]]
    by_degree = defaultdict(list)
    for node in reachable:
        by_degree[node["degree"]].append(node["id"])

    missing = [node["id"] for node in reachable
               if node["current_provenance"]["downstream_coverage"]
               in ("MISSING", "PENDING")]
    missing18 = [node["id"] for node in reachable if node["degree"] == 18
                 and node["response_shifts"] == [2, 2]
                 and node["direct_packet"]["degree"] == 14]
    missing19 = [node["id"] for node in reachable if node["degree"] == 19
                 and node["response_shifts"] == [2, 3]
                 and node["direct_packet"]["degree"] == 14]
    require(len(missing18) == len(missing19) == 1, (missing18, missing19))

    result = {
        "status": "PASS_COMPLETE_SIGNATURE_RECURRENCE_DAG_WITH_KNOWN_PROVENANCE_GAPS",
        "model": {
            "degree_range": [14, 24],
            "ordered_direct_packets": 27,
            "response_shifts": [2, 3, 4],
            "tail_counts": {str(key): value for key, value in TAIL_COUNTS.items()},
            "direct_sign": -1,
            "response_sign_flip": True,
            "pivot_policies": {"K14": "frozen valid policy", "K15_K20": "all dividing pivots"},
            "last_pivotable_parent_degree": 20,
            "fixed_integer_scale": 400_591_699_200,
        },
        "counts": {
            "nodes_all": len(nodes),
            "nodes_reachable": len(reachable),
            "edges_all_reachable_parents": len(edges),
            "reachable_lineages_by_degree": {
                str(degree): len(ids) for degree, ids in sorted(by_degree.items())
            },
            "currently_missing_or_pending_reachable_lineages": len(missing),
        },
        "known_omissions": {
            "K18_missing_K14_K2_K2": missing18,
            "K19_missing_K14_K2_K3": missing19,
            "root_cause": (
                "the K14->K16 artifact retained only the irreducible K16 normal; "
                "its pivotable K2 children were discarded before emitting later tails"
            ),
        },
        "retracted_aggregate_claims": [
            {
                "artifact": str(K18.relative_to(ROOT)),
                "correction": "listed components remain exact; total K18 page omits K14 response path [2,2]",
            },
            {
                "artifact": str(K19.relative_to(ROOT)),
                "correction": "listed components remain exact; total K19 page omits K14 response path [2,3]",
            },
            {
                "artifact": "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k18-2026-08-23/results_charge_ledger_through_k18.json",
                "correction": "aggregate compensation invalid because K18 was incomplete",
            },
            {
                "artifact": "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k19-2026-08-23/results_charge_ledger_through_k19.json",
                "correction": "aggregate compensation invalid because K18 and K19 were incomplete",
            },
        ],
        "nodes": nodes,
        "edges": edges,
        "required_reachable_lineage_ids_by_degree": {
            str(degree): sorted(ids) for degree, ids in sorted(by_degree.items())
        },
        "future_interface_rule": (
            "A K20+ interface passes only if its covered_lineage_ids equal the complete "
            "reachable-lineage set at that degree and every entry supplies a 64-hex "
            "evidence digest plus a declared coverage kind."
        ),
        "pinned": {str(path.relative_to(ROOT)): digest(path)
                   for path in (DESIGN, COVER, ARITH, K16, K17, K18, K19)},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def verify_claim(result, claim):
    degree = claim.get("target_degree")
    require(isinstance(degree, int) and 20 <= degree <= 24,
            ("target_degree", degree))
    expected = set(result["required_reachable_lineage_ids_by_degree"][str(degree)])
    covered = claim.get("covered_lineages", {})
    require(isinstance(covered, dict), "covered_lineages must be an object")
    actual = set(covered)
    require(actual == expected, {
        "missing": sorted(expected - actual),
        "unexpected": sorted(actual - expected),
    })
    for lineage, provenance in covered.items():
        require(provenance.get("coverage_kind") in
                ("literal_rows", "exact_source_reconstruction", "exact_charge_only"),
                (lineage, provenance))
        evidence = provenance.get("evidence_sha256", "")
        require(len(evidence) == 64 and all(c in "0123456789abcdef" for c in evidence),
                (lineage, evidence))
    return {"status": "PASS_COMPLETE_INTERFACE_PATH_COVERAGE", "target_degree": degree,
            "covered_reachable_lineages": len(actual)}


def verify_interface(result, path):
    return verify_claim(result, json.loads(path.read_text()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--verify-interface", type=Path)
    parser.add_argument("--selftest-complete", action="store_true")
    parser.add_argument("--hostile", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        ids = result["required_reachable_lineage_ids_by_degree"]["20"]
        template = {
            "target_degree": 20,
            "covered_lineages": {
                lineage: {"coverage_kind": "FILL_ME",
                          "evidence_sha256": "FILL_ME"}
                for lineage in ids
            },
        }
        TEMPLATE.write_text(json.dumps(template, indent=2, sort_keys=True) + "\n")
    if args.verify_interface:
        verdict = verify_interface(result, args.verify_interface)
    elif args.selftest_complete:
        ids = result["required_reachable_lineage_ids_by_degree"]["20"]
        claim = {lineage: {"coverage_kind": "exact_source_reconstruction",
                           "evidence_sha256": "0" * 64}
                 for lineage in ids}
        verdict = verify_claim(result, {"target_degree": 20,
                                        "covered_lineages": claim})
    elif args.hostile:
        ids = result["required_reachable_lineage_ids_by_degree"]["20"]
        claim = {lineage: {"coverage_kind": "exact_charge_only",
                           "evidence_sha256": "0" * 64}
                 for lineage in ids[1:]}
        verdict = verify_claim(result, {"target_degree": 20,
                                        "covered_lineages": claim})
    else:
        verdict = {
            "status": result["status"],
            "counts": result["counts"],
            "known_omissions": result["known_omissions"],
            "logical_sha256": result["logical_sha256"],
        }
    print(json.dumps(verdict, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
