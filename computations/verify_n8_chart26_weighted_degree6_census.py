#!/usr/bin/env python3
"""Count and sample the weighted chart-26 degree-six Buchberger frontier.

The certified weight preserves 6,558 squarefree degree-four leads and 84,005
squarefree degree-five leads.  For squarefree monomials, an LCM has degree
six precisely at intersection sizes 2, 3, and 4 for pairs of types 4-4,
4-5, and 5-5.  Shared-core incidence gives an exact count without expanding
the roughly three million S-polynomials.

The checker also classifies source/overlap signatures and exactly reduces
one representative of each of the resulting 7+15+21 structural classes.
Representative behavior is discovery data, not a proof that every pair in
the same coarse class has the same remainder.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
WEIGHT_PATH = HERE / "verify_n8_chart26_feasible_squarefree_weight.py"
SPEC = importlib.util.spec_from_file_location("n8_squarefree_weight", WEIGHT_PATH)
WEIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WEIGHT)
FIRST = WEIGHT.FIRST
COMPLETE = WEIGHT.COMPLETE
D5 = WEIGHT.D6.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "e8384cac6824cb6a46c2f93f4cab8fbca100f76bba510699b058256ffc4d7fea"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def hamming(first, second, words):
    return sum(a != b for a, b in zip(words[first], words[second]))


def graph_signature(row):
    edge_multiplicity = Counter()
    degree = Counter()
    for value in row:
        left, right, _left_colour, _right_colour = D5.COORDINATES[value]
        edge_multiplicity[(left, right)] += 1
        degree[left] += 1
        degree[right] += 1
    return (
        tuple(sorted(degree.values(), reverse=True)),
        tuple(sorted(edge_multiplicity.values(), reverse=True)),
    )


def skeleton_type(row):
    """Return the underlying uncoloured site-multigraph skeleton."""
    edge_multiplicity = Counter(
        D5.COORDINATES[value][:2] for value in row
    )
    adjacency = {vertex: set() for vertex in range(8)}
    for left, right in edge_multiplicity:
        adjacency[left].add(right)
        adjacency[right].add(left)

    unseen = set(adjacency)
    component_labels = []
    while unseen:
        seed = min(unseen)
        component = {seed}
        frontier = [seed]
        unseen.remove(seed)
        while frontier:
            vertex = frontier.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    frontier.append(neighbor)
        edge_count = sum(
            1 for left, right in edge_multiplicity
            if left in component and right in component
        )
        degrees = sorted(
            (len(adjacency[vertex]) for vertex in component), reverse=True
        )
        if len(component) == 1:
            label = "P1"
        elif edge_count == len(component) - 1 and max(degrees) <= 2:
            label = f"P{len(component)}"
        elif edge_count == len(component) and min(degrees) == max(degrees) == 2:
            label = f"C{len(component)}"
        else:
            label = (
                f"G{len(component)}e{edge_count}d"
                + "-".join(map(str, degrees))
            )
        component_labels.append(label)
    component_labels.sort(
        key=lambda label: (int(label[1:].split("e")[0].split("d")[0]), label),
        reverse=True,
    )
    base = "+".join(component_labels)
    multiplicities = sorted(edge_multiplicity.values(), reverse=True)
    if multiplicities and multiplicities[0] > 1:
        return "multi[" + ",".join(map(str, multiplicities)) + "]:" + base
    return base


def repeated_coordinates(row):
    return {
        f"{value:02x}": multiplicity
        for value, multiplicity in sorted(Counter(row).items())
        if multiplicity > 1
    }


def alternating_base_matching(row):
    """Unique perfect matching of an even-component simple path forest."""
    edges = {D5.COORDINATES[value][:2] for value in row}
    require(len(edges) == len(row),
            "alternating base requested for a nonsimple site graph")
    adjacency = {vertex: set() for vertex in range(8)}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    require(all(1 <= len(neighbors) <= 2 for neighbors in adjacency.values()),
            "alternating base requested for a nonspanning path forest")

    unseen = set(adjacency)
    matching = []
    while unseen:
        endpoints = sorted(
            vertex for vertex in unseen if len(adjacency[vertex]) == 1
        )
        require(endpoints, "alternating base requested for a cycle")
        path = []
        previous = None
        vertex = endpoints[0]
        while True:
            path.append(vertex)
            unseen.remove(vertex)
            following = [
                neighbor for neighbor in adjacency[vertex]
                if neighbor != previous and neighbor in unseen
            ]
            if not following:
                break
            require(len(following) == 1,
                    "alternating base requested for a branched forest")
            previous, vertex = vertex, following[0]
        require(len(path) % 2 == 0,
                "alternating base requested for an odd path component")
        matching.extend(
            tuple(sorted((path[index], path[index + 1])))
            for index in range(0, len(path), 2)
        )
    return tuple(sorted(matching))


def matching_label(matching):
    return ",".join(f"{left}{right}" for left, right in matching)


def overlap_signature(core, first, second):
    union = bytes(sorted(set(first) | set(second)))
    return graph_signature(core), graph_signature(union)


def canonical_same_type_pair(first, second):
    return min(
        b"".join(sorted((
            bytes(sorted(transform[value] for value in first)),
            bytes(sorted(transform[value] for value in second)),
        )))
        for transform in D5.VARIABLE_TRANSFORMS
    )


def canonical_mixed_type_pair(first, second):
    return min(
        bytes(sorted(transform[value] for value in first))
        + bytes(sorted(transform[value] for value in second))
        for transform in D5.VARIABLE_TRANSFORMS
    )


def build_leads():
    originals, original_lead_to_code = FIRST.original_basis()
    degree4 = dict(original_lead_to_code)
    code_to_lead = {code: lead for lead, code in degree4.items()}
    words = {code: D5.decode_word(code) for code in originals}
    degree5_pairs, _cores, _histogram = COMPLETE.build_pairs(code_to_lead)
    degree5 = {}
    for lcm, first_code, second_code in degree5_pairs:
        polynomial = COMPLETE.s_polynomial(
            lcm, first_code, second_code, originals, code_to_lead
        )
        lead = FIRST.leading_monomial(polynomial)
        degree5[lead] = (
            first_code,
            second_code,
            hamming(first_code, second_code, words),
        )
    require(len(degree4) == 6558 and len(degree5) == 84005,
            "weighted lower-layer lead census changed")
    return originals, degree4, code_to_lead, degree5, words


def classify_pairs(degree4, degree5, words):
    counts = Counter()
    representatives = {}
    orbit_counters = {kind: Counter() for kind in ("44", "45", "55")}
    lcm_skeleton_counters = {
        kind: Counter() for kind in ("44", "45", "55")
    }

    by_two = defaultdict(list)
    for monomial in degree4:
        for core in combinations(monomial, 2):
            by_two[bytes(core)].append(monomial)
    for core, monomials in by_two.items():
        for index, first in enumerate(monomials):
            for second in monomials[index + 1:]:
                if len(set(first) & set(second)) != 2:
                    continue
                distance = hamming(degree4[first], degree4[second], words)
                signature = (
                    "44", distance, overlap_signature(core, first, second)
                )
                counts[signature] += 1
                representatives.setdefault(signature, (first, second))
                lcm_skeleton_counters["44"][
                    skeleton_type(bytes(sorted(set(first) | set(second))))
                ] += 1
                orbit_counters["44"][
                    canonical_same_type_pair(first, second)
                ] += 1

    degree4_by_three = defaultdict(list)
    degree5_by_three = defaultdict(list)
    for monomial in degree4:
        for core in combinations(monomial, 3):
            degree4_by_three[bytes(core)].append(monomial)
    for monomial in degree5:
        for core in combinations(monomial, 3):
            degree5_by_three[bytes(core)].append(monomial)
    for core, degree4_monomials in degree4_by_three.items():
        for first in degree4_monomials:
            source_code = degree4[first]
            for second in degree5_by_three.get(core, ()):
                if len(set(first) & set(second)) != 3:
                    continue
                left, right, cell_distance = degree5[second]
                source_distances = tuple(sorted((
                    hamming(source_code, left, words),
                    hamming(source_code, right, words),
                )))
                source_signature = (cell_distance,) + source_distances
                signature = (
                    "45", source_signature,
                    overlap_signature(core, first, second),
                )
                counts[signature] += 1
                representatives.setdefault(signature, (first, second))
                lcm_skeleton_counters["45"][
                    skeleton_type(bytes(sorted(set(first) | set(second))))
                ] += 1
                orbit_counters["45"][
                    canonical_mixed_type_pair(first, second)
                ] += 1

    degree5_by_four = defaultdict(list)
    for monomial in degree5:
        for core in combinations(monomial, 4):
            degree5_by_four[bytes(core)].append(monomial)
    for core, monomials in degree5_by_four.items():
        for index, first in enumerate(monomials):
            first_left, first_right, first_distance = degree5[first]
            first_sources = {first_left, first_right}
            for second in monomials[index + 1:]:
                second_left, second_right, second_distance = degree5[second]
                second_sources = {second_left, second_right}
                cross_distances = tuple(sorted(
                    hamming(left, right, words)
                    for left in first_sources for right in second_sources
                ))
                source_signature = (
                    min(first_distance, second_distance),
                    max(first_distance, second_distance),
                    len(first_sources & second_sources),
                    cross_distances,
                )
                signature = (
                    "55", source_signature,
                    overlap_signature(core, first, second),
                )
                counts[signature] += 1
                representatives.setdefault(signature, (first, second))
                lcm_skeleton_counters["55"][
                    skeleton_type(bytes(sorted(set(first) | set(second))))
                ] += 1
                orbit_counters["55"][
                    canonical_same_type_pair(first, second)
                ] += 1
    return counts, representatives, orbit_counters, lcm_skeleton_counters


def add_value(polynomial, row, value):
    result = polynomial.get(row, QQ(0)) + value
    if result:
        polynomial[row] = result
    else:
        polynomial.pop(row, None)


def monomial_lcm(first, second):
    return bytes(sorted((Counter(first) | Counter(second)).elements()))


def representative_reductions(
        originals, degree4, code_to_lead, degree5, representatives, counts):
    cache = {}

    def basis_polynomial(kind, lead):
        key = kind, lead
        if key in cache:
            return cache[key]
        if kind == "4":
            polynomial = {
                row: QQ(value)
                for row, value in originals[degree4[lead]].items()
            }
        else:
            first_code, second_code, _distance = degree5[lead]
            lcm = bytes(sorted(
                set(code_to_lead[first_code])
                | set(code_to_lead[second_code])
            ))
            polynomial = {
                row: QQ(value) for row, value in COMPLETE.s_polynomial(
                    lcm,
                    first_code,
                    second_code,
                    originals,
                    code_to_lead,
                ).items()
            }
        lead_coefficient = polynomial[lead]
        polynomial = {
            row: value / lead_coefficient
            for row, value in polynomial.items()
        }
        cache[key] = polynomial
        return polynomial

    def s_polynomial(first_kind, first, second_kind, second):
        lcm = monomial_lcm(first, second)
        first_multiplier = FIRST.quotient(lcm, first)
        second_multiplier = FIRST.quotient(lcm, second)
        answer = {}
        for row, value in basis_polynomial(first_kind, first).items():
            add_value(answer, FIRST.multiply(first_multiplier, row), value)
        for row, value in basis_polynomial(second_kind, second).items():
            add_value(answer, FIRST.multiply(second_multiplier, row), -value)
        return answer

    def source_label(kind, lead):
        if kind == "4":
            code = degree4[lead]
            return {
                "kind": "degree4_generator",
                "code": code,
                "word": list(D5.decode_word(code)),
            }
        first_code, second_code, distance = degree5[lead]
        return {
            "kind": "degree5_transport_cell",
            "source_codes": [first_code, second_code],
            "source_words": [
                list(D5.decode_word(first_code)),
                list(D5.decode_word(second_code)),
            ],
            "source_hamming_distance": distance,
        }

    def skeleton_histogram(rows, degree=None):
        return dict(sorted(Counter(
            skeleton_type(row) for row in rows
            if degree is None or len(row) == degree
        ).items()))

    def input_source_matchings(first_kind, first, second_kind, second):
        by_matching = defaultdict(list)

        def add_sources(prefix, kind, lead):
            codes = ([degree4[lead]] if kind == "4"
                     else list(degree5[lead][:2]))
            for index, code in enumerate(codes):
                matching = tuple(sorted(
                    D5.COORDINATES[value][:2]
                    for value in code_to_lead[code]
                ))
                label = f"{prefix}:{kind}:code{code}"
                if kind == "5":
                    label += f":source{index + 1}"
                by_matching[matching].append(label)

        add_sources("first", first_kind, first)
        add_sources("second", second_kind, second)
        return by_matching

    def path_forest_base_audit(rows, source_matchings):
        by_type = {}
        combined = Counter()
        for forest_type in ("P6+P2", "P4+P4"):
            bases = Counter(
                matching_label(alternating_base_matching(row))
                for row in rows if len(row) == 6
                and skeleton_type(row) == forest_type
            )
            combined.update(bases)
            by_type[forest_type] = {
                "terms": sum(bases.values()),
                "distinct_base_matchings": len(bases),
                "all_terms_share_one_base_matching": len(bases) == 1,
                "base_matching_histogram": dict(sorted(bases.items())),
            }
        source_labels = {
            matching_label(matching): labels
            for matching, labels in sorted(source_matchings.items())
        }
        input_base_terms = sum(
            count for matching, count in combined.items()
            if matching in source_labels
        )
        return {
            "path_forest_terms": sum(combined.values()),
            "distinct_base_matchings": len(combined),
            "all_path_terms_share_one_base_matching": len(combined) == 1,
            "terms_with_an_input_source_base_matching": input_base_terms,
            "all_path_terms_have_an_input_source_base_matching": (
                bool(combined) and input_base_terms == sum(combined.values())
            ),
            "input_source_matchings": source_labels,
            "by_forest_type": by_type,
        }

    def order_key(row):
        return -len(row), -WEIGHT.weight(row), row

    def reduce_polynomial(polynomial):
        work = dict(polynomial)
        remainder = {}
        steps = 0
        maximum_work = len(work)
        while work:
            row = min(work, key=order_key)
            coefficient = work.pop(row)
            choice = None
            if len(row) >= 5:
                for divisor in FIRST.divisors(row, 5):
                    if divisor in degree5:
                        choice = "5", divisor
                        break
            if choice is None and len(row) >= 4:
                for divisor in FIRST.divisors(row, 4):
                    if divisor in degree4:
                        choice = "4", divisor
                        break
            if choice is None:
                remainder[row] = coefficient
                continue
            kind, lead = choice
            reducer = basis_polynomial(kind, lead)
            multiplier = FIRST.quotient(row, lead)
            factor = coefficient / reducer[lead]
            for term, value in reducer.items():
                output = FIRST.multiply(multiplier, term)
                if output == row:
                    continue
                require(order_key(output) > order_key(row),
                        "weighted representative reduction is not decreasing")
                add_value(work, output, -factor * value)
            steps += 1
            maximum_work = max(maximum_work, len(work))
            require(steps <= 200000,
                    "representative reduction exceeded its step guard")
        return remainder, steps, maximum_work

    records = []
    for signature, (first, second) in sorted(
            representatives.items(), key=lambda item: repr(item[0])):
        pair_kind = signature[0]
        first_kind = "5" if pair_kind == "55" else "4"
        second_kind = "4" if pair_kind == "44" else "5"
        source = s_polynomial(first_kind, first, second_kind, second)
        remainder, steps, maximum_work = reduce_polynomial(source)
        lead = min(remainder, key=order_key) if remainder else None
        degree6_remainder_skeletons = skeleton_histogram(remainder, degree=6)
        record = {
            "pair_kind": pair_kind,
            "signature": repr(signature[1:]),
            "class_pair_count": counts[signature],
            "first_lead": first.hex(),
            "second_lead": second.hex(),
            "first_source": source_label(first_kind, first),
            "second_source": source_label(second_kind, second),
            "lcm_skeleton": skeleton_type(monomial_lcm(first, second)),
            "source_terms": len(source),
            "source_degree6_skeletons": skeleton_histogram(source, degree=6),
            "remainder_terms": len(remainder),
            "remainder_degree_histogram": dict(sorted(
                Counter(map(len, remainder)).items()
            )),
            "remainder_lead": lead.hex() if lead is not None else None,
            "remainder_lead_skeleton": (
                skeleton_type(lead) if lead is not None else None
            ),
            "remainder_lead_repeated_coordinates": (
                repeated_coordinates(lead) if lead is not None else {}
            ),
            "remainder_degree6_skeletons": degree6_remainder_skeletons,
            "remainder_contains_P6_P2": "P6+P2" in degree6_remainder_skeletons,
            "remainder_contains_P4_P4": "P4+P4" in degree6_remainder_skeletons,
            "remainder_lead_squarefree": (
                len(lead) == len(set(lead)) if lead is not None else None
            ),
            "reduction_steps": steps,
            "maximum_work_terms": maximum_work,
        }
        if lead is not None and len(lead) != len(set(lead)):
            record["path_forest_base_matching_audit"] = (
                path_forest_base_audit(
                    remainder,
                    input_source_matchings(
                        first_kind, first, second_kind, second
                    ),
                )
            )
        records.append(record)
    return records


def audit():
    originals, degree4, code_to_lead, degree5, words = build_leads()
    counts, representatives, orbit_counters, lcm_skeleton_counters = classify_pairs(
        degree4, degree5, words
    )
    pair_totals = {
        kind: sum(value for signature, value in counts.items()
                  if signature[0] == kind)
        for kind in ("44", "45", "55")
    }
    require(pair_totals == {
        "44": 967750, "45": 792653, "55": 1165402
    }, "weighted degree-six pair census changed")
    structural_class_counts = Counter(
        signature[0] for signature in representatives
    )
    require(structural_class_counts
            == Counter({"44": 7, "45": 15, "55": 21}),
            "weighted degree-six structural class census changed")
    lower_skeletons = {
        "degree4": Counter(skeleton_type(row) for row in degree4),
        "degree5": Counter(skeleton_type(row) for row in degree5),
    }
    require(lower_skeletons == {
        "degree4": Counter({"P2+P2+P2+P2": 6558}),
        "degree5": Counter({"P4+P2+P2": 84005}),
    }, "weighted lower-layer path-forest skeleton changed")
    expected_lcm_skeletons = {
        "44": Counter({
            "multi[2,2,1,1]:P2+P2+P2+P2": 829100,
            "C4+P2+P2": 138650,
        }),
        "45": Counter({
            "C4+P2+P2": 671758,
            "multi[2,1,1,1,1]:P4+P2+P2": 120895,
        }),
        "55": Counter({
            "multi[2,1,1,1,1]:P4+P2+P2": 1089204,
            "C4+P2+P2": 76198,
        }),
    }
    require(lcm_skeleton_counters == expected_lcm_skeletons,
            "weighted degree-six LCM skeleton census changed")
    orbit_records = {}
    expected_orbits = {
        "44": (933326, Counter({1: 898902, 2: 34424})),
        "45": (790051, Counter({1: 787449, 2: 2602})),
        "55": (1160461, Counter({1: 1155520, 2: 4941})),
    }
    for kind, counter in orbit_counters.items():
        multiplicities = Counter(counter.values())
        require((len(counter), multiplicities) == expected_orbits[kind],
                f"{kind} stabilizer-type census changed")
        orbit_records[kind] = {
            "canonical_types": len(counter),
            "selected_pair_multiplicity_histogram": dict(sorted(
                multiplicities.items()
            )),
        }

    records = representative_reductions(
        originals, degree4, code_to_lead, degree5, representatives, counts
    )
    representative_summary = {}
    for kind in ("44", "45", "55"):
        selected = [record for record in records
                    if record["pair_kind"] == kind]
        representative_summary[kind] = {
            "classes": len(selected),
            "zero_remainders": sum(
                record["remainder_terms"] == 0 for record in selected
            ),
            "squarefree_nonzero_leads": sum(
                record["remainder_lead_squarefree"] is True
                for record in selected
            ),
            "nonsquarefree_nonzero_leads": sum(
                record["remainder_lead_squarefree"] is False
                for record in selected
            ),
        }
    require(representative_summary == {
        "44": {"classes": 7, "zero_remainders": 3,
               "squarefree_nonzero_leads": 4,
               "nonsquarefree_nonzero_leads": 0},
        "45": {"classes": 15, "zero_remainders": 0,
               "squarefree_nonzero_leads": 12,
               "nonsquarefree_nonzero_leads": 3},
        "55": {"classes": 21, "zero_remainders": 9,
               "squarefree_nonzero_leads": 11,
               "nonsquarefree_nonzero_leads": 1},
    }, "weighted representative summary changed")
    offending_records = [
        record for record in records
        if record["remainder_lead_squarefree"] is False
    ]
    require(len(offending_records) == 4,
            "weighted nonsquarefree representative census changed")
    offending_summary = [(
        record["pair_kind"],
        record["class_pair_count"],
        record["first_lead"],
        record["second_lead"],
        record["remainder_lead"],
        record["remainder_lead_repeated_coordinates"],
        record["remainder_degree6_skeletons"].get("P6+P2", 0),
        record["remainder_degree6_skeletons"].get("P4+P4", 0),
        record["path_forest_base_matching_audit"]["distinct_base_matchings"],
        record["path_forest_base_matching_audit"][
            "terms_with_an_input_source_base_matching"
        ],
    ) for record in offending_records]
    require(offending_summary == [
        ("45", 42754, "0948c6f4", "0948c6d9e4", "0951acc6f4f4",
         {"f4": 2}, 156, 82, 72, 0),
        ("45", 38702, "0948c6f4", "0948c6dce4", "0952acc6f4f4",
         {"f4": 2}, 164, 100, 82, 0),
        ("45", 8412, "0948c6f4", "010c48c6f4", "0309094bc6f4",
         {"09": 2}, 0, 0, 0, 0),
        ("55", 45776, "01094ec6f4", "010c4ec6f4", "0409094ec6f4",
         {"09": 2}, 0, 0, 0, 0),
    ], "weighted Bianchi-curvature representative records changed")

    endpoint_incident_45 = sum(
        value for signature, value in counts.items()
        if signature[0] == "45" and 0 in signature[1][1:]
    )
    shared_source_55 = sum(
        value for signature, value in counts.items()
        if signature[0] == "55" and signature[1][2] == 1
    )
    require(endpoint_incident_45 == 81456,
            "degree4-degree5 endpoint-incidence census changed")
    require(shared_source_55 == 329268,
            "degree5-degree5 shared-source census changed")

    class_records = [
        [signature[0], repr(signature[1:]), value]
        for signature, value in sorted(counts.items(), key=lambda item: repr(item[0]))
    ]
    ledger = {
        "certified_weight_sha256": (
            "a2728326ada93de8b5d3372335efa151708dc86cb72b7b01e807d59f355b1527"
        ),
        "degree4_leads": len(degree4),
        "degree5_leads": len(degree5),
        "lower_lead_skeletons": {
            kind: dict(sorted(counter.items()))
            for kind, counter in lower_skeletons.items()
        },
        "degree6_pair_counts": pair_totals,
        "total_degree6_pairs": sum(pair_totals.values()),
        "degree6_lcm_skeleton_counts": {
            kind: dict(sorted(counter.items()))
            for kind, counter in lcm_skeleton_counters.items()
        },
        "structural_class_counts": dict(sorted(
            structural_class_counts.items()
        )),
        "stabilizer_type_census": orbit_records,
        "degree45_endpoint_incident_pairs": endpoint_incident_45,
        "degree55_shared_source_pairs": shared_source_55,
        "structural_classes": class_records,
        "representative_reductions": records,
        "representative_summary": representative_summary,
        "nonsquarefree_representative_records": offending_records,
        "conclusion": (
            "the weighted degree6 frontier has 2925805 pairs but only 43 "
            "coarse source/overlap classes; four sampled Bianchi-curvature "
            "families retain nonsquarefree leads and require straightening"
        ),
        "scope_guard": (
            "one representative per coarse class does not certify uniform "
            "reduction behavior for every pair in that class"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen weighted degree-six census ledger changed")
    print(
        "n=8 chart26 weighted degree-six census: PASS; "
        "pairs=967750/792653/1165402, classes=7/15/21"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
