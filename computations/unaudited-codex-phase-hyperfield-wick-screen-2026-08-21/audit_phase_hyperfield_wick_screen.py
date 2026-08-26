#!/usr/bin/env python3
"""Exact bounded phase-hyperfield/Wick screen for signless hafnians."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_phase_hyperfield_wick_screen.json"
PINS = {
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "notes/delta-matroid-transversal.md":
        "ab3140e5777ebc52cac184fc60a9e1dbe215f7a1902a2ee45b47c9dd7a11fdc4",
    "computations/verify_global_cut_wick_invariant_boundary.py":
        "7aa7289cce09e86be8958263932e56a57c8cd7b565bb17ebfde6fdf9805925bd",
    "computations/verify_global_wick_top_invariant_counterguard.py":
        "192c03668e56262315e685f49c29fafeed071faf2a292dfdc94544fd7a5f4183",
    "computations/verify_dense_paired_eq_chart.py":
        "f9b4c9e9bc8046274511200d2e41e75381671af5840134c63495ec8b8b7288c0",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None, relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def phase_sign(value):
    value = Fraction(value)
    return 0 if value == 0 else (1 if value > 0 else -1)


def phase_hyperzero_real(values):
    """Whether 0 is in the phase-hyperfield sum of real phases."""
    phases = {phase_sign(value) for value in values} - {0}
    return not phases or phases == {-1, 1}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((min(first, second), max(first, second)),) + tail


def signless_hafnian(vertices, weights):
    @lru_cache(None)
    def recurse(items):
        if not items:
            return Fraction(1)
        first = items[0]
        answer = Fraction(0)
        for position in range(1, len(items)):
            second = items[position]
            value = weights.get((min(first, second), max(first, second)), 0)
            if not value:
                continue
            rest = items[1:position] + items[position + 1:]
            answer += value * recurse(rest)
        return answer

    return recurse(tuple(sorted(vertices)))


def pfaffian(vertices, weights):
    """Pfaffian in the supplied total order, with weights keyed by positions."""
    ordered = tuple(vertices)

    @lru_cache(None)
    def recurse(items):
        if not items:
            return Fraction(1)
        first = items[0]
        answer = Fraction(0)
        for position in range(1, len(items)):
            second = items[position]
            pair = (min(first, second), max(first, second))
            value = weights.get(pair, 0)
            if not value:
                continue
            rest = items[1:position] + items[position + 1:]
            answer += ((-1) ** (position + 1)) * value * recurse(rest)
        return answer

    return recurse(ordered)


def raw_four_point_wick(signless_p4, a, b, c):
    # p_empty*p_1234-p_12*p_34+p_13*p_24-p_14*p_23.
    return [signless_p4, -a, b, -c]


def counterguard():
    weights = {
        (0, 1): Fraction(1), (2, 3): Fraction(1),
        (0, 2): Fraction(-2), (1, 3): Fraction(1),
        (0, 3): Fraction(1), (1, 2): Fraction(1),
    }
    products = [weights[0, 1] * weights[2, 3],
                weights[0, 2] * weights[1, 3],
                weights[0, 3] * weights[1, 2]]
    h4 = signless_hafnian(range(4), weights)
    require(products == [1, -2, 1] and h4 == 0, (products, h4))
    require(phase_hyperzero_real(products),
            "ordinary signless cancellation lost its phase hyperzero")
    wick_terms = raw_four_point_wick(h4, *products)
    require([phase_sign(value) for value in wick_terms] == [0, -1, -1, -1],
            wick_terms)
    require(not phase_hyperzero_real(wick_terms),
            "counterguard unexpectedly became phase-Wick")

    signed_p4 = pfaffian(range(4), weights)
    signed_terms = raw_four_point_wick(signed_p4, *products)
    require(signed_p4 == 4 and sum(signed_terms) == 0,
            (signed_p4, signed_terms))
    require(phase_hyperzero_real(signed_terms),
            "the genuine Pfaffian field relation lost phase orthogonality")

    weights8 = dict(weights)
    weights8[4, 5] = Fraction(1)
    weights8[6, 7] = Fraction(1)
    live = []
    for matching in perfect_matchings(range(8)):
        term = Fraction(1)
        for pair in matching:
            term *= weights8.get(pair, 0)
        if term:
            live.append(term)
    require(len(tuple(perfect_matchings(range(8)))) == 105,
            "K8 matching count changed")
    require(live == [1, -2, 1] and sum(live) == 0, live)
    return {
        "four_port_products": [int(value) for value in products],
        "signless_hafnian": int(h4),
        "signless_term_phase_hyperzero": True,
        "literal_W4_terms": [int(value) for value in wick_terms],
        "literal_W4_phases": [phase_sign(value) for value in wick_terms],
        "literal_W4_phase_hyperzero": False,
        "genuine_signed_pfaffian": int(signed_p4),
        "genuine_pfaffian_W4_sum": int(sum(signed_terms)),
        "K8_fibre_terms_total": 105,
        "K8_fibre_live_terms": 3,
        "K8_live_products": [int(value) for value in live],
        "K8_signless_hafnian": int(sum(live)),
    }


def n4_ghz_control():
    # Port order is site-major: port=3*site+colour.
    physical_matchings = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    weights = {}
    edges = []
    for colour, matching in physical_matchings.items():
        for left, right in matching:
            pair = tuple(sorted((3 * left + colour, 3 * right + colour)))
            weights[pair] = Fraction(1)
            edges.append(pair)
    require(len(edges) == 6 and len({v for edge in edges for v in edge}) == 12,
            "n4 GHZ port graph stopped being a matching")

    raw = {}
    for colour in range(3):
        subset = sorted(3 * site + colour for site in range(4))
        products = [weights.get(tuple(sorted((subset[0], subset[1]))), 0)
                    * weights.get(tuple(sorted((subset[2], subset[3]))), 0),
                    weights.get(tuple(sorted((subset[0], subset[2]))), 0)
                    * weights.get(tuple(sorted((subset[1], subset[3]))), 0),
                    weights.get(tuple(sorted((subset[0], subset[3]))), 0)
                    * weights.get(tuple(sorted((subset[1], subset[2]))), 0)]
        h4 = sum(products)
        terms = raw_four_point_wick(h4, *products)
        raw[str(colour)] = {
            "ports": subset,
            "matching_products": [int(value) for value in products],
            "W4_phases": [phase_sign(value) for value in terms],
            "phase_hyperzero": phase_hyperzero_real(terms),
        }
    require([raw[str(c)]["phase_hyperzero"] for c in range(3)]
            == [True, False, True], raw)

    # Relabel the six disjoint source edges consecutively. Then the skew
    # matrix is block diagonal and every principal Pfaffian is the signless
    # principal hafnian. This is extra orientation/order data, not a
    # functorial property of the literal site-major signless coordinates.
    edge_order = sorted(edges)
    old_to_new = {}
    adjacent_weights = {}
    for index, edge in enumerate(edge_order):
        old_to_new[edge[0]] = 2 * index
        old_to_new[edge[1]] = 2 * index + 1
        adjacent_weights[2 * index, 2 * index + 1] = weights[edge]
    checked = 0
    for mask in range(1 << 12):
        subset = tuple(index for index in range(12) if mask >> index & 1)
        if len(subset) % 2:
            continue
        h = signless_hafnian(subset, adjacent_weights)
        p = pfaffian(subset, adjacent_weights)
        require(h == p, (subset, h, p))
        checked += 1
    require(checked == 2048, checked)
    return {
        "pure_output": {"0000": 1, "1111": 1, "2222": 1},
        "live_port_graph": "six disjoint edges",
        "literal_site_major_W4": raw,
        "literal_site_major_is_phase_Wick": False,
        "edge_adjacent_reorientation_is_field_Wick": True,
        "even_principal_coordinates_checked": checked,
        "interpretation": (
            "the sparse control admits a Pfaffian orientation, but the "
            "literal signless phase assignment is not canonical"
        ),
    }


def n8_laurent_control():
    module = load("phase_wick_laurent",
                  "computations/verify_global_wick_top_invariant_counterguard.py")
    vertices, edges = module.prism_seed()
    vertices, edges, shift = module.expand_vertex(vertices, edges, min(vertices))
    require(len(vertices) == 8 and len(edges) == 12, (vertices, edges))
    terms, determinant = module.audit_stage(vertices, edges)
    require(len(terms) == 5 and determinant == 1, (terms, determinant))
    histogram = {}
    for _word, exponent in terms:
        histogram[exponent] = histogram.get(exponent, 0) + 1
    require(histogram == {0: 3, 1: 2}, histogram)
    mates = module.port_pairing(vertices, edges)
    require(len(mates) == 24, len(mates))

    # In the port graph every port has a unique mate. Ordering these twelve
    # pairs consecutively gives an exact block-diagonal skew realization.
    unordered_pairs = sorted({tuple(sorted((port, mate)))
                              for port, (mate, _exponent) in mates.items()})
    require(len(unordered_pairs) == 12, unordered_pairs)
    exponents = {}
    for physical, (colour, exponent) in edges.items():
        left = (physical[0], colour)
        right = (physical[1], colour)
        exponents[tuple(sorted((left, right)))] = exponent
    adjacent_weights = {}
    for index, pair in enumerate(unordered_pairs):
        exponent = exponents[pair]
        adjacent_weights[2 * index, 2 * index + 1] = (
            Fraction(2 ** exponent) if exponent >= 0
            else Fraction(1, 2 ** (-exponent)))
    checked = 0
    for pair_mask in range(1 << 12):
        subset = tuple(position for index in range(12)
                       if pair_mask >> index & 1
                       for position in (2 * index, 2 * index + 1))
        h = signless_hafnian(subset, adjacent_weights)
        p = pfaffian(subset, adjacent_weights)
        require(h == p, (pair_mask, h, p))
        checked += 1
    require(checked == 4096, checked)
    return {
        "n": 8,
        "source_edges": len(edges),
        "port_graph": "twelve disjoint edges",
        "port_mates": len(mates),
        "top_terms": len(terms),
        "top_valuation_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "valuation_zero_terms": 3,
        "positive_valuation_mixed_terms": 2,
        "exact_covariance_determinant_at_t2": int(determinant),
        "field_Wick_union_coordinates_checked": checked,
        "phase_shadow_at_nonzero_t": (
            "all five top terms remain nonzero phase +; phase alone does "
            "not record that the two mixed coefficients tend to zero"
        ),
        "exact_GHZ_phase_point_at_nonzero_t": False,
    }


def n6_scope():
    # A Wick vector for 18 ports needs every even principal coordinate.
    all_even = 1 << 17
    one_hot = 3 ** 6
    require(all_even == 131072 and one_hot == 729, (all_even, one_hot))
    require(not phase_hyperzero_real([1, 1]),
            "phase hyperfield accidentally acquired characteristic two")
    return {
        "arbitrary_complex_six_site_theorem": True,
        "rank_graph_types": 19,
        "source_cells": 15 * 9,
        "one_hot_output_rows": one_hot,
        "even_principal_Wick_coordinates": all_even,
        "unseen_even_coordinates": all_even - one_hot,
        "char2_to_phase_hyperfield_morphism": False,
        "morphism_guard": "1+1=0 over F2, but 0 is not in 1 boxplus 1 in the phase hyperfield",
        "proof_transport": (
            "the complex n6 theorem uses ranks, minors, and shared Laurent "
            "magnitudes; the char2 theorem uses parity. Neither is a "
            "consequence of the phase-Wick support axioms"
        ),
    }


def main():
    pin_ledger = {}
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))
        pin_ledger[relative] = observed

    payload = {
        "status": "PASS exact negative phase-hyperfield/Wick screen",
        "tract_axiom": (
            "W2 alternates products of principal Wick coordinates; a "
            "signless hafnian zero only gives hyperzero for its own matching "
            "monomial phases"
        ),
        "four_port_and_105_term_counterguard": counterguard(),
        "n4_exact_GHZ_control": n4_ghz_control(),
        "n6_theorem_scope": n6_scope(),
        "n8_Laurent_boundary_control": n8_laurent_control(),
        "terminal_verdict": {
            "literal_signless_phases_form_Wick_vector_in_general": False,
            "signless_zero_implies_phase_hyperzero_of_same_terms": True,
            "signless_zero_implies_Wick_tract_orthogonality": False,
            "phase_Wick_axioms_force_active_clean_pair": False,
            "reason": (
                "the first implication fails on four ports; where a separate "
                "Pfaffian orientation exists, Wick structure forgets the "
                "shared magnitudes, valuations, and labelled cap-response "
                "incidence needed for cleanliness"
            ),
        },
        "scope": {
            "support_enumeration": False,
            "broad_polynomial_solve": False,
            "primary_reference": "Jin--Kim, Orthogonal matroids over tracts, Definition 3.1 (W2)",
            "primary_reference_url": "https://arxiv.org/html/2303.05353v2#S3.SS1",
            "dependency_sha256": pin_ledger,
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "four_port_signless_zero": 0,
        "literal_W4_phases": [0, -1, -1, -1],
        "K8_live_over_total": [3, 105],
        "n4_literal_phase_Wick": False,
        "n4_reoriented_field_Wick": True,
        "n8_Laurent_reoriented_field_Wick": True,
        "clean_pair_forced": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
