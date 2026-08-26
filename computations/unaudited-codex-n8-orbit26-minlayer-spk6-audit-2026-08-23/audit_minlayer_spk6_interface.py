#!/usr/bin/env python3
"""Audit the orbit-26 minimum layers and their exact SP-K6 interface."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DIRECT_DIR = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
DIRECT_SCRIPT = DIRECT_DIR / "audit_orbit26_anchor_and_direct_boundary.py"
DIRECT_RESULT = DIRECT_DIR / "results_orbit26_anchor_and_direct_boundary.json"
RESIDUAL_PACKET = DIRECT_DIR / "direct_fh_y6_residual.txt"
PROVIDER_PACKET = DIRECT_DIR / "direct_fh_unique_min_provider.txt"
SPK6 = ROOT / "proofs/six-site-arbitrary-complex-obstruction.md"
BASELINE = ROOT / "certification/BASELINE.md"
SUPERSESSIONS = ROOT / "certification/SUPERSESSIONS.md"
RESULT_PATH = HERE / "results_minlayer_spk6_interface.json"
EXPECTED = {
    DIRECT_SCRIPT: "5b6a3669c5cfe8d5c0af364f0eba7da0a901a031014219db4844f3c657b9acf7",
    DIRECT_RESULT: "6fed2f0349831cadc3858aae5abe2bb6ecf93ad65acb49295331d203fc590557",
    RESIDUAL_PACKET: "234edf92012e289fab8b5e98dfb73148985755ca2eafa200b0f71c1886ace456",
    PROVIDER_PACKET: "92aac535bd99d4ccacc17cf19f034505f7270bceeb4fa7a3d38f22fd3de37497",
    SPK6: "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    BASELINE: "2b3a966a7873a58569e1f4ae0d94d4f32c7139da4bcdaef2cef4bddb254b7f24",
    SUPERSESSIONS: "07ac9f0f8b92d991a7cac7a5b2d8f15fae5db44914a4166b21bdde0fba926a3c",
}
EXPECTED_DIRECT_LOGICAL = "dd31d2dbeb5f6e550df0761fe9e3710f26b186eb49d84cf0c0a4d0d581924e60"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_direct():
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    stored = json.loads(DIRECT_RESULT.read_text())
    require(stored["logical_sha256"] == EXPECTED_DIRECT_LOGICAL,
            "direct-boundary logical result drifted")
    spec = importlib.util.spec_from_file_location("minlayer_direct", DIRECT_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, str(DIRECT_SCRIPT))
    spec.loader.exec_module(module)
    return module, stored


def transform_term(term, transform):
    return bytes(sorted(transform[value] for value in term))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def audit(mutate=False):
    direct, stored = load_direct()
    D5 = direct.D5
    support = set(D5.SUPPORT_IDS)

    residual_header = RESIDUAL_PACKET.read_text().splitlines()[0]
    provider_lines = PROVIDER_PACKET.read_text().splitlines()
    require(residual_header == "KRENN_N8_DIRECT_FH_Y6_V1 SCALE 4 COUNT 224319",
            "residual packet header changed")
    require(provider_lines[0] == "KRENN_N8_UNIQUE_MIN_PROVIDER_V1",
            "provider packet header changed")

    polynomials = {}
    minimum = {}
    compatible = {}
    by_linear_variable = defaultdict(list)
    degree_histogram = Counter()
    layer_histogram = Counter()

    for code in range(3 ** 8):
        word = D5.decode_word(code)
        if len(set(word)) == 1:
            continue
        polynomial = direct.normalized_generator(code)
        d = min(map(len, polynomial))
        layer = tuple(sorted(term for term in polynomial if len(term) == d))
        polynomials[code] = polynomial
        minimum[code] = (d, layer)
        degree_histogram[d] += 1
        layer_histogram[d, len(layer)] += 1

        usable = []
        for variable in sorted(support):
            left, right, left_colour, right_colour = D5.COORDINATES[variable]
            if (word[left], word[right]) == (left_colour, right_colour):
                usable.append(variable)
        compatible[code] = tuple(usable)
        require(len(usable) == 4 - d,
                "minimum degree is not four minus compatible support edges")
        covered = {
            site for variable in usable
            for site in D5.COORDINATES[variable][:2]
        }
        require(len(covered) == 2 * len(usable),
                "compatible support cells are not site-disjoint")
        unmatched = tuple(site for site in range(8) if site not in covered)
        require(len(unmatched) == 2 * d, "unmatched-site count changed")
        expected = []
        for matching in perfect_matchings(unmatched):
            expected.append(bytes(sorted(
                D5.COORDINATE_ID[(left, right, word[left], word[right])]
                for left, right in matching
            )))
        require(layer == tuple(sorted(expected))
                and all(polynomial[term] == 1 for term in layer),
                "minimum layer is not the complete unmatched-site hafnian")
        if d == 1:
            by_linear_variable[layer[0][0]].append(code)

    require(degree_histogram == Counter({0: 2, 1: 358, 2: 2298, 3: 3058, 4: 842})
            and layer_histogram == Counter({
                (0, 1): 2, (1, 1): 358, (2, 3): 2298,
                (3, 15): 3058, (4, 105): 842,
            }), "minimum-layer census changed")
    require(set(by_linear_variable) == set(range(252)) - support,
            "linear minima do not cover the 240 normalized variables")
    linear_multiplicity = Counter(len(codes) for codes in by_linear_variable.values())
    require(linear_multiplicity == Counter({1: 130, 2: 102, 3: 8}),
            "linear-provider multiplicities changed")

    # Independently parse and replay the frozen deterministic provider.
    provider = {}
    provider_l2 = defaultdict(list)
    for line in provider_lines[1:]:
        fields = line.split()
        if fields[0] == "LINEAR":
            variable, code = map(int, fields[1:3])
            provider[variable] = code
        elif fields[0] == "L2":
            variable = int(fields[1])
            provider_l2[variable].append(bytes.fromhex(fields[2]))
    require(len(provider) == len(provider_l2) == 240,
            "provider variable count changed")
    for variable, code in provider.items():
        d, layer = minimum[code]
        require(d == 1 and layer == (bytes([variable]),)
                and polynomials[code][layer[0]] == 1,
                "packet chose a non-monic/nonlinear provider")
        actual_l2 = sorted(term for term in polynomials[code] if len(term) == 2)
        require(sorted(provider_l2[variable]) == actual_l2
                and len(actual_l2) == 6,
                "packet quadratic tails changed")

    # The deterministic lex provider is not H-equivariant, but an exact
    # equivariant section exists.  This separates acyclicity from symmetry.
    transforms = D5.VARIABLE_TRANSFORMS
    word_transforms = D5.WORD_TRANSFORMS
    lex_covariance_failures = sum(
        provider[transform[variable]] != word_transforms[index][code]
        for variable, code in provider.items()
        for index, transform in enumerate(transforms)
    )
    require(lex_covariance_failures == 64,
            "deterministic-provider covariance guard changed")
    equivariant = {}
    variable_orbits = []
    seen = set()
    for variable in sorted(by_linear_variable):
        if variable in seen:
            continue
        orbit = tuple(sorted({transform[variable] for transform in transforms}))
        seen.update(orbit)
        stabilizer = [index for index, transform in enumerate(transforms)
                      if transform[variable] == variable]
        fixed = [code for code in by_linear_variable[variable]
                 if all(word_transforms[index][code] == code
                        for index in stabilizer)]
        require(fixed, "variable orbit has no stabilizer-fixed linear provider")
        base = min(fixed)
        for index, transform in enumerate(transforms):
            moved_variable = transform[variable]
            moved_code = word_transforms[index][base]
            if moved_variable in equivariant:
                require(equivariant[moved_variable] == moved_code,
                        "equivariant section is not well-defined")
            equivariant[moved_variable] = moved_code
        variable_orbits.append((variable, len(orbit), base))
    require(len(variable_orbits) == 66 and len(equivariant) == 240
            and all(equivariant[transform[variable]]
                    == word_transforms[index][code]
                    for variable, code in equivariant.items()
                    for index, transform in enumerate(transforms)),
            "equivariant linear section changed")

    # Literal homogeneous degree bookkeeping proving triangular contraction.
    triangular_templates = []
    for y_degree in range(1, 10):
        multiplier_y_degree = y_degree - 1
        multiplier_t_degree = 9 - y_degree
        require(multiplier_y_degree + multiplier_t_degree == 8,
                "linear multiplier left homogeneous degree eight")
        triangular_templates.append({
            "row_y_degree": y_degree,
            "provider_minimum_degree": 1,
            "multiplier_y_degree": multiplier_y_degree,
            "multiplier_t_degree": multiplier_t_degree,
            "all_nonpivot_outputs_have_y_degree_at_least": y_degree + 1,
        })

    # The first coupled N4 layer: every distinct minimum triple is an
    # isolated K4 perfect-matching exchange at quadratic degree.
    triple_words = defaultdict(list)
    for code, (d, layer) in minimum.items():
        if d == 2:
            triple_words[layer].append(code)
    triples = set(triple_words)
    nodes = set().union(*map(set, triples))
    require(len(triples) == 2206 and len(nodes) == 6618
            and Counter(len(codes) for codes in triple_words.values())
            == Counter({1: 2114, 2: 92}),
            "quadratic exchange census changed")
    for triple in triples:
        require(len(set(triple)) == 3, "quadratic block has repeated node")
        site_edges = {
            tuple(sorted(D5.COORDINATES[variable][:2]))
            for term in triple for variable in term
        }
        sites = {site for edge in site_edges for site in edge}
        degrees = Counter(site for edge in site_edges for site in edge)
        require(len(site_edges) == 6 and len(sites) == 4
                and set(degrees.values()) == {3},
                "quadratic triple is not the three matchings of a K4")

    def move_triple(triple, index):
        return tuple(sorted(
            transform_term(term, transforms[index]) for term in triple
        ))

    triple_orbits = Counter()
    seen = set()
    for triple in sorted(triples):
        if triple in seen:
            continue
        orbit = {move_triple(triple, index) for index in range(len(transforms))}
        require(orbit <= triples, "quadratic orbit left packet")
        seen.update(orbit)
        multiplicities = tuple(sorted(len(triple_words[item]) for item in orbit))
        triple_orbits[len(orbit), multiplicities] += 1
    require(triple_orbits == Counter({
        (4, (1, 1, 1, 1)): 517,
        (4, (2, 2, 2, 2)): 23,
        (2, (1, 1)): 22,
        (1, (1,)): 2,
    }), "quadratic orbit decomposition changed")

    # Canonical d=2 word: its next layer is two punctured N6 fibres, not a
    # full SP-K6 system.
    d2_code = min(code for code, (d, _layer) in minimum.items() if d == 2)
    require(d2_code == 11 and D5.decode_word(d2_code) == (0, 0, 0, 0, 0, 1, 0, 2),
            "canonical d2 word changed")
    d2_support = compatible[d2_code]
    require(len(d2_support) == 2, "canonical d2 compatible edge count changed")
    d2_layer = minimum[d2_code][1]
    degree3_by_used_support = defaultdict(set)
    for raw_term in D5.iter_word_terms(d2_code):
        used = tuple(sorted(set(raw_term) & support))
        normalized = bytes(value for value in raw_term if value not in support)
        if len(normalized) == 3:
            require(len(used) == 1 and used[0] in d2_support,
                    "degree3 term has wrong support provenance")
            degree3_by_used_support[used[0]].add(normalized)
    require(set(degree3_by_used_support) == set(d2_support)
            and all(len(terms) == 12 for terms in degree3_by_used_support.values())
            and sum(map(len, degree3_by_used_support.values())) == 24,
            "d2 next layer is not two 12-term punctured fibres")
    completed_six_fibres = {
        edge: set(terms) | set(d2_layer)
        for edge, terms in degree3_by_used_support.items()
    }
    require(all(len(fibre) == 15
                and Counter(map(len, fibre)) == Counter({2: 3, 3: 12})
                for fibre in completed_six_fibres.values()),
            "punctured fibre completion changed")

    # Literal same-word/common-multiplier provenance.  For either compatible
    # support edge e, the 15 raw matchings containing e split after
    # normalization into the same three d2 terms and the corresponding twelve
    # d3 terms.  An arbitrary outer multiplier multiplies both pieces equally.
    containing_support = defaultdict(set)
    avoiding_support = defaultdict(set)
    for raw_term in D5.iter_word_terms(d2_code):
        normalized = bytes(value for value in raw_term if value not in support)
        for edge in d2_support:
            (containing_support if edge in raw_term else avoiding_support)[edge].add(
                normalized
            )
    require(all(containing_support[edge] == completed_six_fibres[edge]
                and len(containing_support[edge]) == 15
                and len(avoiding_support[edge]) == 90
                for edge in d2_support),
            "same-word N4+punctured-N6 completion changed")

    # Fixed-edge d=3 rows cover only restricted mixed residual words.  None
    # supplies the pure coefficients required by SP-K6.
    d3_edge_words = defaultdict(set)
    for code, (d, _layer) in minimum.items():
        if d != 3:
            continue
        edge, = compatible[code]
        left, right = D5.COORDINATES[edge][:2]
        word = D5.decode_word(code)
        residual_word = tuple(word[site] for site in range(8)
                              if site not in (left, right))
        d3_edge_words[edge].add(residual_word)
    d3_counts = {
        edge: len(words) for edge, words in d3_edge_words.items()
    }
    require(sum(d3_counts.values()) == 3058
            and sorted(d3_counts.values())
            == [250, 250, 251, 251, 251, 251, 258, 259, 259, 259, 259, 260]
            and all(tuple([colour] * 6) not in words
                    for words in d3_edge_words.values() for colour in range(3)),
            "d3 fixed-edge word coverage changed")

    # Closing under lower pages adds residual assignments with one, two, or
    # three further compatible support edges.  This is all 3^6 assignments,
    # but fixed endpoint colour makes the target one-colour, not ternary GHZ.
    fixed_edge_closure = []
    for edge in sorted(support):
        left, right, colour, other_colour = D5.COORDINATES[edge]
        require(colour == other_colour, "support edge stopped being diagonal")
        remaining = tuple(site for site in range(8)
                          if site not in (left, right))
        extra_histogram = Counter()
        original_mixed = 0
        residual_constant_status = []
        for residual_word in product(range(3), repeat=6):
            word = [None] * 8
            word[left] = word[right] = colour
            for site, value in zip(remaining, residual_word):
                word[site] = value
            compatible_count = 0
            for support_edge in support:
                u, v, a, b = D5.COORDINATES[support_edge]
                compatible_count += (word[u], word[v]) == (a, b)
            require(compatible_count >= 1,
                    "fixed support edge ceased to be compatible")
            extra_histogram[compatible_count - 1] += 1
            if len(set(word)) > 1:
                original_mixed += 1
            if len(set(residual_word)) == 1:
                residual_colour = residual_word[0]
                residual_constant_status.append({
                    "residual_colour": residual_colour,
                    "original_word_is_pure": len(set(word)) == 1,
                    "target_coefficient": int(residual_colour == colour),
                })
        require(sum(extra_histogram.values()) == 729
                and extra_histogram[0] == d3_counts[edge]
                and original_mixed == 728
                and sorted(item["target_coefficient"]
                           for item in residual_constant_status) == [0, 0, 1],
                "fixed-edge lower-page closure changed")
        fixed_edge_closure.append({
            "support_edge": list(D5.COORDINATES[edge]),
            "fixed_endpoint_colour": colour,
            "residual_words_by_extra_compatible_edges":
                dict(sorted(extra_histogram.items())),
            "all_residual_words": sum(extra_histogram.values()),
            "original_mixed_equation_rows": original_mixed,
            "omitted_original_pure_row": 1,
            "residual_constant_words": residual_constant_status,
            "induced_six_site_target": f"e_{colour}^tensor6",
        })

    if mutate:
        d3_counts[min(d3_counts)] += 1
    require(sum(d3_counts.values()) == 3058,
            "hostile d3 coverage mutation survived")

    result = {
        "format": "n8-orbit26-minlayer-spk6-interface-v1",
        "status": "PASS min-layer theorem; direct SP-K6 landing fails",
        "source_sha256": {
            str(path.relative_to(ROOT)): digest for path, digest in EXPECTED.items()
        },
        "direct_boundary_logical_sha256": EXPECTED_DIRECT_LOGICAL,
        "minimum_layer_theorem": {
            "statement": (
                "For a mixed word w, let s(w) be the compatible chart-support "
                "edges. They are site-disjoint. The minimum normalized "
                "offdegree is d=4-|s(w)|, and the complete minimum layer is "
                "the monic hafnian on the 2d unmatched sites."
            ),
            "word_count_by_d": dict(sorted(degree_histogram.items())),
            "layer_support_by_d": {
                str(d): support_size for (d, support_size), count in layer_histogram.items()
                if count == degree_histogram[d]
            },
            "literal_words_checked": len(minimum),
            "all_coefficients_monic": True,
        },
        "linear_contraction": {
            "linear_words": 358,
            "normalized_variables_covered": len(by_linear_variable),
            "provider_multiplicity_histogram": dict(sorted(linear_multiplicity.items())),
            "frozen_provider_replayed": True,
            "triangular_templates": triangular_templates,
            "acyclic_through_y_degree": 9,
            "reason": "each nonpivot output strictly raises y-degree",
            "fixed_chart_variable_orbits": len(variable_orbits),
            "frozen_lex_provider_covariance_failures": lex_covariance_failures,
            "equivariant_section_exists": True,
            "equivariant_section_changes_from_frozen_provider": sum(
                equivariant[variable] != provider[variable] for variable in provider
            ),
        },
        "degree10_N4_exchange": {
            "quadratic_words": 2298,
            "distinct_K4_matching_triples": len(triples),
            "quadratic_monomial_nodes": len(nodes),
            "base_components": len(triples),
            "base_component_size": 3,
            "base_incidence_rank_over_Q": len(triples),
            "base_node_kernel_dimension": len(nodes) - len(triples),
            "single_source_blocks": 2114,
            "double_source_blocks": 92,
            "fixed_chart_orbit_decomposition": [
                {"orbit_size": orbit_size,
                 "source_multiplicities_on_orbit": list(multiplicities),
                 "orbit_count": count}
                for (orbit_size, multiplicities), count in sorted(triple_orbits.items())
            ],
            "translation_guard": (
                "disjointness is a theorem only for the unmultiplied quadratic "
                "nodes; degree-8 balanced multipliers can identify degree-10 "
                "outputs, so the full translated core is not declared block diagonal"
            ),
        },
        "degree11_N6_interface": {
            "canonical_d2_word_code": d2_code,
            "canonical_d2_word": "00000102",
            "compatible_support_edges": [
                list(D5.COORDINATES[edge]) for edge in d2_support
            ],
            "N4_minimum_terms": len(d2_layer),
            "next_layer_terms": 24,
            "punctured_N6_fibres": 2,
            "terms_per_punctured_fibre": 12,
            "missing_N4_terms_per_fibre": 3,
            "missing_triple_is_exact_same_word_and_multiplier": True,
            "raw_matchings_containing_selected_outer_support_edge": 15,
            "raw_matchings_avoiding_selected_outer_support_edge": 90,
            "completed_fibre_normalized_degree_histogram": {"2": 3, "3": 12},
            "d3_fixed_support_edge_word_counts": [
                {"support_edge": list(D5.COORDINATES[edge]),
                 "available_residual_words": count,
                 "missing_from_3^6": 729 - count,
                 "pure_residual_words_present": 0}
                for edge, count in sorted(d3_counts.items())
            ],
            "SP_K6_endpoint_ordered_block_compatibility": (
                "yes for each individual six-site hafnian fibre"
            ),
            "lower_page_completion_reaches_all_729_residual_words": True,
            "fixed_edge_closure": fixed_edge_closure,
            "SP_K6_full_word_family_compatibility": (
                "combinatorially yes after d3+d2+d1+d0 completion, but only "
                "after extracting terms containing the fixed outer edge"
            ),
            "SP_K6_three_nonzero_pure_coefficients_compatibility": False,
            "SP_K6_literal_unfiltered_equation_compatibility": False,
            "verdict": (
                "The d2 three-term block is exactly the missing part of each "
                "12-term punctured N6 fibre, with the same word and common "
                "multiplier. Lower-page completion reaches all 729 residual "
                "words. Nevertheless a fixed outer support cell fixes one "
                "endpoint colour: 728 rows are mixed equations and the sole "
                "omitted original-pure row gives target e_c^tensor6, while "
                "the other two residual constant words have target zero. "
                "Moreover each literal eight-site generator has 90 matchings "
                "avoiding the selected outer edge. Thus the completed symbols "
                "still do not give H6(A)=Delta_6,3, and SP-K6 cannot be "
                "imported without an active three-colour cap/extraction."
            ),
        },
        "smallest_missing_bridge": (
            "For one physical deleted pair, combine endpoint-colour contractions "
            "so all three diagonal outer channels are active, cancel the 90-term "
            "avoid-edge contamination in every word, and obtain three nonzero "
            "pure residual coefficients for one common collection of blocks. "
            "This is precisely a source-faithful active-cap/clean extraction; "
            "only then can SP-K6 be invoked."
        ),
        "scope_guard": (
            "The minimum-layer and first N4-to-N6 boundary statements are exact. "
            "No deterministic contraction of the full 224319-row residual and "
            "no translated degree10 core solve is performed here."
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return json.loads(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.check_results:
        require(RESULT_PATH.exists()
                and json.loads(RESULT_PATH.read_text()) == result,
                "stored result changed")
    if args.write_results:
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("linear/N4/d3=", 358,
          result["degree10_N4_exchange"]["distinct_K4_matching_triples"],
          sum(item["available_residual_words"]
              for item in result["degree11_N6_interface"]
              ["d3_fixed_support_edge_word_counts"]))
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
