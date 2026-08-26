#!/usr/bin/env python3
"""Exact anchor-signature denominator census for the K14--K24 source recurrence."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from math import lcm
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
K17_AUX = (ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
           / "results_filtered_k17_aux_export.json")
OUT = HERE / "results_k19_k24_arithmetic.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def factor(n):
    answer = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            answer[divisor] = answer.get(divisor, 0) + 1
            n //= divisor
        divisor += 1
    if n > 1:
        answer[n] = 1
    return answer


def main(write=False, mutate=False):
    d = load("k19_k24_arithmetic_design", DESIGN)
    cover_raw = json.loads(COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in
                      cover_raw["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    require(len(cover) == 25, len(cover))

    tail_signatures = {}
    for pivot in range(78):
        for tail_degree in (2, 3, 4):
            signatures = set()
            for tail in d.CTX.tails[pivot][tail_degree]:
                counts = Counter(tail)
                signatures.add(tuple(counts[cell] for cell in d.CTX.anchor_cells))
            require(len(signatures) == {2: 6, 3: 4, 4: 1}[tail_degree],
                    (pivot, tail_degree, len(signatures)))
            tail_signatures[pivot, tail_degree] = signatures

    # Exact possible all-dividing-pivot counts at every parent K-degree.  A
    # balanced degree-24 row has each of the 12 disjoint anchor cells 0,1,2
    # times and sum(signature)=24-K.
    count_histograms = {}
    count_sets = {}
    signatures_by_degree = defaultdict(set)
    for signature in product(range(3), repeat=12):
        degree = 24 - sum(signature)
        if 14 <= degree <= 20:
            signatures_by_degree[degree].add(signature)
            choices = len(d.CTX.pivots(signature))
            if choices:
                count_histograms.setdefault(degree, Counter())[choices] += 1
    for degree in range(14, 21):
        count_sets[degree] = sorted(count_histograms[degree])
    require(count_sets[20] == [1], count_sets[20])

    # Exact direct source signature sets, avoiding row expansion: convolve the
    # 485 R8' signatures with the 6/4/1 unique tail signatures in each colour.
    factor_words = tuple(d.F.word_from_pair_colours(row) for row in d.F.PAIR_COLOURS)
    factor_pivots = tuple(d.CTX.anchor_to_pivot[d.F.BASE.term_ids(word, d.F.M0)]
                          for word in factor_words)
    direct = defaultdict(set)
    r8_signatures = {d.CTX.signature(row) for row, _size, _coefficient in d.r8_h_records()}
    for degrees in product((2, 3, 4), repeat=3):
        target_degree = 8 + sum(degrees)
        for r8 in r8_signatures:
            for additions in product(*(tail_signatures[factor_pivots[f], degrees[f]]
                                       for f in range(3))):
                child = tuple(r8[i] + sum(addition[i] for addition in additions)
                              for i in range(12))
                require(sum(child) == 24 - target_degree, (target_degree, child))
                require(all(0 <= value <= 2 for value in child), child)
                direct[target_degree].add(child)
    require(set(direct) == set(range(14, 21)), sorted(direct))

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

    # Source-lineage exact DP before coefficient collection/cancellation.
    # State values are the exact products of averaging pivot counts along a
    # path.  Direct terms inject product 1 at every K14..K20 bucket.
    states = defaultdict(lambda: defaultdict(set))
    depth_states = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
    for degree, signatures in direct.items():
        for signature in signatures:
            states[degree][signature].add(1)
            depth_states[degree][signature][0].add(1)
    k14_valid_counts = Counter()
    for degree in range(14, 21):
        for signature, old_products in list(states[degree].items()):
            pivots = k14_valid(signature) if degree == 14 else d.CTX.pivots(signature)
            if not pivots:
                continue
            choices = len(pivots)
            if degree == 14:
                k14_valid_counts[choices] += 1
            products_after_average = {value * choices for value in old_products}
            depth_products_after_average = {
                depth + 1: {value * choices for value in products}
                for depth, products in depth_states[degree][signature].items()
            }
            for tail_degree in (2, 3, 4):
                child_degree = degree + tail_degree
                if child_degree > 24:
                    continue
                for pivot in pivots:
                    base = tuple(signature[i] - d.CTX.vectors[pivot][i]
                                 for i in range(12))
                    for addition in tail_signatures[pivot, tail_degree]:
                        child = tuple(base[i] + addition[i] for i in range(12))
                        require(sum(child) == 24 - child_degree,
                                (degree, tail_degree, child))
                        require(all(0 <= value <= 2 for value in child), child)
                        states[child_degree][child].update(products_after_average)
                        for depth, products in depth_products_after_average.items():
                            depth_states[child_degree][child][depth].update(products)

    layer = {}
    global_products = set()
    for degree in range(19, 25):
        products_here = sorted({value for values in states[degree].values() for value in values})
        require(products_here, degree)
        global_products.update(products_here)
        by_depth = {}
        for depth in sorted({depth for values in depth_states[degree].values()
                             for depth in values}):
            products_at_depth = sorted({
                value
                for values in depth_states[degree].values()
                for value in values.get(depth, ())
            })
            by_depth[str(depth)] = {
                "products": products_at_depth,
                "distinct_products": len(products_at_depth),
                "maximum_product": max(products_at_depth),
                "product_lcm": lcm(*products_at_depth),
            }
        layer[str(degree)] = {
            "reachable_anchor_signatures_before_cancellation": len(states[degree]),
            "distinct_pivot_count_products": len(products_here),
            "products": products_here,
            "maximum_product": max(products_here),
            "product_lcm": lcm(*products_here),
            "products_by_pivot_depth": by_depth,
        }

    # Mandatory hidden-tail guard: the full recurrence must retain pivotable
    # K2 children instead of recording only their first irreducible page.
    # In particular K14 -> K16 -> K18 -> K20 has three averaging factors.
    k20_depth3 = layer["20"]["products_by_pivot_depth"].get("3")
    require(k20_depth3 is not None and k20_depth3["distinct_products"] > 0,
            k20_depth3)
    require(max(map(int, layer["20"]["products_by_pivot_depth"])) == 3,
            layer["20"]["products_by_pivot_depth"].keys())
    require(max(map(int, layer["24"]["products_by_pivot_depth"])) == 4,
            layer["24"]["products_by_pivot_depth"].keys())

    universal = lcm(*global_products)
    if mutate:
        universal += 1
    # Independent degree-wise safe scale calculation.  These are LCMs over all
    # feasible signatures; K14 uses the actual frozen valid-policy counts.
    policy_lcm = {degree: lcm(*count_sets[degree]) for degree in range(15, 21)}
    policy_lcm[14] = lcm(*k14_valid_counts)
    require(policy_lcm == {14: 3_612_840, 15: 21_677_040, 16: 55_440,
                           17: 840, 18: 12, 19: 2, 20: 1}, policy_lcm)
    path_safe_universal = 2_403_550_195_200
    require(universal <= path_safe_universal and path_safe_universal % universal == 0,
            (universal, path_safe_universal))
    require(universal == 400_591_699_200, universal)

    # Hostile L1 recurrence: averaging never increases the L1 contribution of
    # one tail degree, so a pivoted parent emits at most 12/32/60 times its L1
    # mass to K(d+2/3/4).  Assume every parent is pivotable and every term in a
    # bucket collides on one row.  This bounds both collection and coefficients.
    r8_l1_fraction = sum(orbit_size * abs(coefficient)
                          for _row, orbit_size, coefficient in d.r8_h_records())
    require(r8_l1_fraction.denominator == 1, r8_l1_fraction)
    r8_l1 = r8_l1_fraction.numerator
    direct_profile_counts = Counter()
    for degrees in product((2, 3, 4), repeat=3):
        count = 1
        for degree in degrees:
            count *= {2: 12, 3: 32, 4: 60}[degree]
        direct_profile_counts[8 + sum(degrees)] += count
    l1_bound = {}
    direct_l1 = {}
    for degree in range(14, 25):
        direct_l1[degree] = r8_l1 * direct_profile_counts[degree]
        l1_bound[degree] = direct_l1[degree] + sum(
            l1_bound.get(degree - increment, 0) * tails
            for increment, tails in ((2, 12), (3, 32), (4, 60)))
    max_scaled = max(l1_bound.values()) * universal
    max_transient_orbit_mass = max_scaled * len(d.H)
    i128_max = 2 ** 127 - 1
    require(max_transient_orbit_mass < i128_max,
            (max_transient_orbit_mass, i128_max))

    result = {
        "status": "PASS_EXACT_K19_K24_DENOMINATOR_PLAN",
        "arithmetic_model": {
            "total_monomial_degree": 24,
            "anchor_multiplicity_range": [0, 2],
            "anchor_sum_at_Kd": "24-d",
            "last_pivotable_degree": 20,
            "K20_pivot_count_is_always_one": True,
            "recurrence_increments": [2, 3, 4],
        },
        "all_pivot_count_histogram_by_parent_degree": {
            str(degree): {str(key): value for key, value in
                          sorted(count_histograms[degree].items())}
            for degree in range(14, 21)
        },
        "actual_K14_valid_policy_count_histogram_by_signature": {
            str(key): value for key, value in sorted(k14_valid_counts.items())
        },
        "policy_count_lcm_by_parent_degree": {
            str(key): value for key, value in sorted(policy_lcm.items())
        },
        "direct_signature_count_by_degree": {
            str(key): len(value) for key, value in sorted(direct.items())
        },
        "source_lineage_products_by_output_degree": layer,
        "hidden_higher_tail_guard": {
            "required_path": "K14 --K2--> K16 --K2--> K18 --K2--> K20",
            "K20_maximum_pivot_denominator_depth": 3,
            "K20_depth3_products": k20_depth3["products"],
            "K20_depth3_product_lcm": k20_depth3["product_lcm"],
            "K24_maximum_pivot_denominator_depth": 4,
            "verdict": (
                "The earlier source-signature DP already propagated every K2/K3/K4 "
                "child, including pivotable hidden tails; the explicit depth audit "
                "therefore leaves the recommended scale unchanged."
            ),
        },
        "minimal_lcm_for_enumerated_source_lineages": universal,
        "recommended_single_integer_scale": universal,
        "recommended_scale_factorization": {
            str(key): value for key, value in factor(universal).items()
        },
        "conservative_degree_lcm_product_scale": path_safe_universal,
        "conservative_over_exact_factor": path_safe_universal // universal,
        "global_one_page_scale_281801520_is_insufficient_for_nested_pages": True,
        "first_explicit_one_page_scale_counterexample": {
            "output_degree": 19,
            "reachable_pivot_count_product": 25,
            "reason": "281801520 has only one factor of 5, so it does not clear two successive five-pivot averages",
        },
        "bigint_required_for_denominators": False,
        "coefficient_growth_bound": {
            "R8prime_labelled_L1_mass": r8_l1,
            "direct_profile_count_by_degree": {
                str(key): value for key, value in sorted(direct_profile_counts.items())
            },
            "direct_L1_mass_by_degree": {
                str(key): value for key, value in sorted(direct_l1.items())
            },
            "hostile_all_parents_pivotable_L1_bound_by_degree": {
                str(key): value for key, value in sorted(l1_bound.items())
            },
            "maximum_at_K24": l1_bound[24],
            "maximum_scaled_labelled_numerator": max_scaled,
            "maximum_transient_scaled_H_orbit_mass_numerator": max_transient_orbit_mass,
            "H_order": len(d.H),
            "i128_max": i128_max,
            "i128_transient_safety_margin_floor": i128_max // max_transient_orbit_mass,
            "proof": "For one pivot average, summing over all chosen pivots cancels the 1/m factor in L1; the K2/K3/K4 pages multiply L1 by at most 12/32/60. The recurrence assumes every parent pivots and every contribution collides.",
        },
        "representation": {
            "record": "canonical H-row plus scaled coefficient per labelled row (not orbit mass)",
            "coefficient_type": "signed i128",
            "reduction": "expand one complete parent H-orbit, divide by pivot count exactly, canonicalize children, then exact-divide each child orbit mass by its orbit size before checkpointing",
            "checkpoint": "sorted binary/TSV runs per K-degree with numerator at the fixed scale, byte offset, record count, and per-run SHA256",
            "guards": [
                "assert scale % pivot_count == 0 at every head cancellation",
                "assert child scaled orbit mass % child_orbit_size == 0 before storing per-labelled coefficient",
                "drop signed zero only after exact addition",
                "store sign convention parent c emits -c/pivot_count",
                "merge all sorted runs exactly before reducing the next degree",
            ],
        },
        "scope": "Exact source-lineage anchor-signature arithmetic before row cancellation; no K19+ residual or charge run.",
        "pinned": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in (DESIGN, COVER, K17_AUX)
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "universal": universal,
                      "recommended": universal,
                      "products_per_layer": {key: value["distinct_pivot_count_products"]
                                             for key, value in layer.items()},
                      "logical_sha256": logical}, indent=2, sort_keys=True))


if __name__ == "__main__":
    import sys
    main("--write-results" in sys.argv, "--mutate" in sys.argv)
