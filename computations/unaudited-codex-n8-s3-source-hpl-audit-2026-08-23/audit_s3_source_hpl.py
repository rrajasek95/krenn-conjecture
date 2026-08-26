#!/usr/bin/env python3
"""Bounded source-labelled audit of the 66-term S3 transfer obstruction."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_DIR = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
KERNEL = SOURCE_DIR / "direct_fh_transfer_kernels.txt"
SKELETON_RESULT = SOURCE_DIR / "results_s3_physical_skeleton.json"
PM4_RESULT = ROOT / "computations/unaudited-codex-n8-s3-pm4-translate-2026-08-23/results_s3_pm4_translate.json"
LOW_SOURCE_RESULT = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/results_s3_source_component.json"
LOW_SOURCE_SCRIPT = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/audit_s3_source_component.py"
PROVIDER = SOURCE_DIR / "direct_fh_unique_min_provider.txt"
COMPLETE_PATH = ROOT / "computations/verify_n8_chart26_complete_degree5_buchberger.py"
COMPAT_PATH = ROOT / "computations/verify_n8_chart26_first_degree6_compatibility.py"
WEIGHT_PATH = ROOT / "computations/verify_n8_chart26_weighted_degree6_census.py"
BIANCHI_PATH = ROOT / "computations/verify_n8_chart26_cross_vertex_bianchi.py"
PURE_QUOTIENT_DIR = ROOT / "computations/unaudited-codex-triangle-pure-quotient-collapse-2026-08-22"
PURE_QUOTIENT_REPORT = PURE_QUOTIENT_DIR / "REPORT.md"
PURE_QUOTIENT_RESULT = PURE_QUOTIENT_DIR / "results.json"
PURE_QUOTIENT_CHECK = PURE_QUOTIENT_DIR / "check_results.py"
FIVE_SET_REPORT = ROOT / "computations/unaudited-codex-five-set-response-surjectivity-2026-08-22/REPORT.md"
CARRIER_RESTRICTION_DIR = ROOT / "computations/unaudited-codex-n8-s3-carrier-restriction-2026-08-23"
CARRIER_RESTRICTION_REPORT = CARRIER_RESTRICTION_DIR / "REPORT.md"
CARRIER_RESTRICTION_RESULT = CARRIER_RESTRICTION_DIR / "results_s3_carrier_restriction.json"
NEXT_ATTACHMENT_DIR = ROOT / "computations/unaudited-codex-n8-s3-dual-next-attachments-2026-08-23"
NEXT_ATTACHMENT_REPORT = NEXT_ATTACHMENT_DIR / "REPORT.md"
NEXT_ATTACHMENT_RESULT = NEXT_ATTACHMENT_DIR / "results_s3_dual_next_attachments.json"
RESULT = HERE / "results_s3_source_hpl.json"
EXPECTED = {
    KERNEL: "859f144440e45ca64c1534ae99506e31524d76cd3c47e83911b384c2fea49650",
    SKELETON_RESULT: "e7805b6eb1353816377b1c78543b025d6a7cd41c498bd618a4f46a9c19df1e38",
    PM4_RESULT: "36d242722508553b349d17bde620d9bb3576b92fa384c4204d36cde7488d60ff",
    LOW_SOURCE_RESULT: "7d27d9301ca81b4567db74fb872b324d068f1c90eae37caf5fe544adeb2b4b27",
    LOW_SOURCE_SCRIPT: "a4d22563904e8dde445067b9e8c466cd048ea471ffdaac566b66202eec1ae189",
    PROVIDER: "92aac535bd99d4ccacc17cf19f034505f7270bceeb4fa7a3d38f22fd3de37497",
    COMPLETE_PATH: "3d96ec2b26781b70e5cac1878d7090e525c135e285815f9fecb48fca88bd7e30",
    COMPAT_PATH: "a500003996151031ed8ff16ffa6ce27fb2eb1906a9a76effd7c69365cf2a60ef",
    WEIGHT_PATH: "27371803eecef4a0c4084aa11947116d3bf7161a145cc756bb487c45c17856a0",
    BIANCHI_PATH: "6697d96f951920ebcf15637f58a871accdf1e88398573899f2c284e32c2f655e",
    PURE_QUOTIENT_REPORT: "10537d9ba02cd05a18a7c9a0dad88ca2e2e452747bce7f95a066e3d82306d9f4",
    PURE_QUOTIENT_RESULT: "cf2ca70211cbacd9ddaa99afcca09f7c7cc2973a156de92bb118f3d9fb7a5db8",
    PURE_QUOTIENT_CHECK: "f16a7cd1903490c99435cc250124daaf502c08b4243574d17763fddb1eb9d32b",
    FIVE_SET_REPORT: "2db9a83c9bce5a549499edf76f8fd0f4d846ac17fb1424d8494467dd57073a99",
    CARRIER_RESTRICTION_REPORT: "a65719d8eff62b9e8c9857921f56ca60f9bbaa1337e0bce99d6f1163691eb7df",
    CARRIER_RESTRICTION_RESULT: "52f325e4d19769189a33ff4b04a0a9c8b6ebc1655ff58b460cedb2c4456d1948",
    NEXT_ATTACHMENT_REPORT: "069d3c87ea121f57375fa05896f83796e2249369da2ff8e936168adf8bce0bc7",
    NEXT_ATTACHMENT_RESULT: "3c402e74f4ff48c0fff57d031d36d4a6a8a41e9c92866b336ce3a89db2be07ca",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


COMPLETE = load("s3_complete", COMPLETE_PATH)
COMPAT = load("s3_compat", COMPAT_PATH)
WEIGHT = load("s3_weight", WEIGHT_PATH)
FIRST = COMPLETE.FIRST
D5 = COMPLETE.D5
QQ = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parse_s3():
    active = False
    answer = {}
    for line in KERNEL.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[:2] == ["BEGIN", "S3"]:
            active = True
        elif fields[:2] == ["END", "S3"]:
            active = False
        elif active and fields[0] == "ROW":
            answer[bytes.fromhex(fields[1])] = int(fields[2])
    require(len(answer) == 66 and Counter(answer.values()) == Counter({1: 53, -1: 13}),
            "S3 packet changed")
    return answer


def skeleton_type(row):
    degrees = sorted(Counter(
        vertex for value in row for vertex in D5.COORDINATES[value][:2]
    ).values(), reverse=True)
    return {
        (1, 1, 1, 1, 1, 1): "3P2",
        (2, 1, 1, 1, 1): "P3+P2",
        (2, 2, 1, 1): "P4",
    }[tuple(degrees)]


def add_value(target, row, value):
    output = target.get(row, QQ(0)) + value
    if output:
        target[row] = output
    else:
        target.pop(row, None)


def selected_weighted_remainders(originals, degree4, code_to_lead, degree5):
    """Replay only the four frozen d6 curvature representatives."""
    cache = {}
    by_pair = {tuple(sorted(value[:2])): lead for lead, value in degree5.items()}

    def basis_polynomial(kind, lead):
        key = kind, lead
        if key in cache:
            return cache[key]
        if kind == "4":
            polynomial = {row: QQ(value)
                          for row, value in originals[degree4[lead]].items()}
        else:
            first_code, second_code, _distance = degree5[lead]
            lcm = bytes(sorted(set(code_to_lead[first_code])
                               | set(code_to_lead[second_code])))
            polynomial = {row: QQ(value) for row, value in
                          COMPLETE.s_polynomial(lcm, first_code, second_code,
                                                originals, code_to_lead).items()}
        coefficient = polynomial[lead]
        polynomial = {row: value / coefficient for row, value in polynomial.items()}
        cache[key] = polynomial
        return polynomial

    def monomial_lcm(first, second):
        return bytes(sorted((Counter(first) | Counter(second)).elements()))

    def s_polynomial(first_kind, first, second_kind, second):
        lcm = monomial_lcm(first, second)
        answer = {}
        for row, value in basis_polynomial(first_kind, first).items():
            add_value(answer, FIRST.multiply(FIRST.quotient(lcm, first), row), value)
        for row, value in basis_polynomial(second_kind, second).items():
            add_value(answer, FIRST.multiply(FIRST.quotient(lcm, second), row), -value)
        return answer

    def order_key(row):
        return -len(row), -WEIGHT.WEIGHT.weight(row), row

    def reduce_polynomial(polynomial):
        work = dict(polynomial)
        remainder = {}
        steps = 0
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
                if output != row:
                    add_value(work, output, -factor * value)
            steps += 1
            require(steps <= 200000, "selected weighted reduction exceeded guard")
        return remainder, steps

    cases = (
        ("45_path_1", "4", code_to_lead[1], "5", by_pair[(1, 10)]),
        ("45_path_2", "4", code_to_lead[1], "5", by_pair[(1, 37)]),
        ("45_collision", "4", code_to_lead[730], "5", by_pair[(730, 2188)]),
        ("55_collision", "5", by_pair[(730, 1459)], "5", by_pair[(730, 3646)]),
    )
    output = []
    for label, first_kind, first, second_kind, second in cases:
        remainder, steps = reduce_polynomial(
            s_polynomial(first_kind, first, second_kind, second)
        )
        output.append((label, remainder, steps))
    return output


def value_at(coordinate, site):
    left, right, left_colour, right_colour = coordinate
    return left_colour if site == left else right_colour


def coordinate_id(left, right, left_colour, right_colour):
    if left < right:
        return D5.COORDINATE_ID[(left, right, left_colour, right_colour)]
    return D5.COORDINATE_ID[(right, left, right_colour, left_colour)]


def response_factorizations(row, s3, triangle={0, 1, 2}):
    if len(row) != 3:
        return []
    coordinates = [D5.COORDINATES[value] for value in row]
    answer = []
    for first_index, first in enumerate(coordinates):
        if 6 not in first[:2] or 7 in first[:2]:
            continue
        for second_index, second in enumerate(coordinates):
            if first_index == second_index or 7 not in second[:2] or 6 in second[:2]:
                continue
            residual_first = first[1] if first[0] == 6 else first[0]
            residual_second = second[1] if second[0] == 7 else second[0]
            if residual_first == residual_second:
                continue
            cap_colours = value_at(first, 6), value_at(second, 7)
            residual_colours = (value_at(first, residual_first),
                                value_at(second, residual_second))
            mate_first = coordinate_id(6, residual_second,
                                       cap_colours[0], residual_colours[1])
            mate_second = coordinate_id(7, residual_first,
                                        cap_colours[1], residual_colours[0])
            spectator = next(row[index] for index in range(3)
                             if index not in (first_index, second_index))
            spectator_coordinate = D5.COORDINATES[spectator]
            occupied = {6, 7, residual_first, residual_second}
            spectator_disjoint = not (set(spectator_coordinate[:2]) & occupied)
            remaining = sorted(set(range(6))
                               - {residual_first, residual_second}
                               - set(spectator_coordinate[:2]))
            implicit_support = []
            if spectator_disjoint and len(remaining) == 2:
                for left_colour in range(3):
                    for right_colour in range(3):
                        identifier = coordinate_id(remaining[0], remaining[1],
                                                   left_colour, right_colour)
                        if not D5.IS_OFF_SUPPORT[identifier]:
                            implicit_support.append(identifier)
            mate = bytes(sorted((mate_first, mate_second, spectator)))
            response_edge = tuple(sorted((residual_first, residual_second)))
            answer.append({
                "response_edge": list(response_edge),
                "inside_triangle": set(response_edge) <= triangle,
                "K_cell": list(cap_colours),
                "response_output_colours": list(residual_colours),
                "spectator": list(spectator_coordinate),
                "spectator_disjoint": spectator_disjoint,
                "implicit_support_cells": implicit_support,
                "valid_normalized_response": bool(implicit_support),
                "orientation_mate": mate.hex(),
                "orientation_mate_in_S3": mate in s3,
            })
    return answer


def primitive_three_dual(support_rows, columns, target):
    """The primitive integer dual on a three-row separating support."""
    equations = []
    for column in columns.values():
        equation = tuple(column.get(row, 0) for row in support_rows)
        if any(equation) and equation not in equations:
            equations.append(equation)
    vector = None
    for left in equations:
        for right in equations:
            candidate = (
                left[1] * right[2] - left[2] * right[1],
                left[2] * right[0] - left[0] * right[2],
                left[0] * right[1] - left[1] * right[0],
            )
            if (any(candidate)
                    and all(sum(a * b for a, b in zip(candidate, equation)) == 0
                            for equation in equations)):
                vector = candidate
                break
        if vector is not None:
            break
    require(vector is not None, "three-row separator did not have rank two")
    from math import gcd
    divisor = gcd(gcd(abs(vector[0]), abs(vector[1])), abs(vector[2]))
    vector = tuple(value // divisor for value in vector)
    pairing = sum(value * target.get(row, 0)
                  for row, value in zip(support_rows, vector))
    require(pairing != 0, "three-row nullvector stopped separating the target")
    if pairing < 0:
        vector = tuple(-value for value in vector)
    return dict(zip(support_rows, vector))


def internal_response_restrictions(dual, triangle={0, 1, 2}):
    """Complete two-orientation cap-67 packets seen by a sparse dual."""
    packets = {}
    for row in dual:
        for factor in response_factorizations(row, dual, triangle):
            if not factor["inside_triangle"] or not factor["valid_normalized_response"]:
                continue
            mate = bytes.fromhex(factor["orientation_mate"])
            key = tuple(sorted((row, mate)))
            if key in packets:
                continue
            pairing = dual.get(row, 0) + dual.get(mate, 0)
            if pairing:
                packets[key] = {
                    "rows": [item.hex() for item in key],
                    "K_cell": factor["K_cell"],
                    "response_edge": factor["response_edge"],
                    "response_output_colours": factor["response_output_colours"],
                    "pairing": pairing,
                }
    return packets


def provider_quadratics(originals, equivariant=False):
    """Return the frozen lex or exact stabilizer-equivariant linear section."""
    if not equivariant:
        linear_code = {}
        for line in PROVIDER.read_text(encoding="ascii").splitlines():
            fields = line.split()
            if fields and fields[0] == "LINEAR":
                linear_code[int(fields[1])] = int(fields[2])
        require(len(linear_code) == 240, "frozen linear provider changed")
    else:
        by_variable = defaultdict(list)
        for code, polynomial in originals.items():
            minimum = min(map(len, polynomial))
            layer = [row for row, value in polynomial.items()
                     if len(row) == minimum and value]
            if minimum == 1 and len(layer) == 1 and polynomial[layer[0]] == 1:
                by_variable[layer[0][0]].append(code)
        linear_code = {}
        seen = set()
        for variable in sorted(by_variable):
            if variable in seen:
                continue
            seen.update(transform[variable] for transform in D5.VARIABLE_TRANSFORMS)
            stabilizer = [index for index, transform in enumerate(D5.VARIABLE_TRANSFORMS)
                          if transform[variable] == variable]
            fixed = [code for code in by_variable[variable]
                     if all(D5.WORD_TRANSFORMS[index][code] == code
                            for index in stabilizer)]
            require(fixed, "equivariant provider orbit has no fixed source")
            base = min(fixed)
            for index, transform in enumerate(D5.VARIABLE_TRANSFORMS):
                moved_variable = transform[variable]
                moved_code = D5.WORD_TRANSFORMS[index][base]
                if moved_variable in linear_code:
                    require(linear_code[moved_variable] == moved_code,
                            "equivariant section is not well-defined")
                linear_code[moved_variable] = moved_code
        require(len(linear_code) == 240, "equivariant provider is incomplete")
    quadratic = {
        variable: Counter({row: value for row, value in originals[code].items()
                           if len(row) == 2})
        for variable, code in linear_code.items()
    }
    require(all(len(layer) == 6 for layer in quadratic.values()),
            "linear-provider quadratic tail changed")
    return linear_code, quadratic


def transferred_s3(code, originals, quadratic):
    polynomial = originals[code]
    layers = defaultdict(Counter)
    for row, value in polynomial.items():
        layers[len(row)][row] += value
    require(layers[0] == Counter({b"": 1})
            and {degree: len(layers[degree]) for degree in (2, 3, 4)}
                == {2: 12, 3: 32, 4: 60},
            "constant-provider profile changed")
    output = Counter({row: -value for row, value in layers[3].items()})
    for row, value in layers[2].items():
        selected = row[0]
        quotient = row[1:]
        for tail, coefficient in quadratic[selected].items():
            add_value(output, bytes(sorted(quotient + tail)), value * coefficient)
    require(all(len(row) == 3 for row in output), "transferred S3 left cubic degree")
    return output


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    s3 = parse_s3()
    profile = Counter(skeleton_type(row) for row in s3)
    require(profile == Counter({"3P2": 28, "P3+P2": 28, "P4": 10}),
            "physical skeleton profile changed")
    matching = {row: value for row, value in s3.items()
                if skeleton_type(row) == "3P2"}
    collision = {row: value for row, value in s3.items()
                 if skeleton_type(row) != "3P2"}

    originals, original_lead_to_code = FIRST.original_basis()
    code_to_lead = {code: lead for lead, code in original_lead_to_code.items()}

    # All literal cubic layers. Their supports are pairwise disjoint.
    cubic_occurrences = defaultdict(list)
    cubic_columns = {}
    for code, polynomial in originals.items():
        cubic = {row: value for row, value in polynomial.items() if len(row) == 3}
        if cubic:
            cubic_columns[code] = cubic
        for row, value in cubic.items():
            cubic_occurrences[row].append((code, value))
    require(sum(map(len, cubic_occurrences.values())) == len(cubic_occurrences) == 111826,
            "literal cubic outputs stopped being globally unique")
    literal_matching = {row: cubic_occurrences[row] for row in matching
                        if row in cubic_occurrences}
    require(len(literal_matching) == 14
            and {code for occurrences in literal_matching.values()
                 for code, _value in occurrences} == {3780}
            and Counter(matching[row] for row in literal_matching)
                == Counter({-1: 13, 1: 1}),
            "matching/cubic intersection changed")
    absent_matching = sorted(set(matching) - set(literal_matching))
    require(len(absent_matching) == 14 and absent_matching[0].hex() == "0491ae",
            "matching cubic separator changed")

    # The second constant provider and both frozen/equivariant linear sections.
    require(D5.decode_word(3780) == (1, 2, 0, 1, 2, 0, 0, 0)
            and D5.decode_word(5108) == (2, 1, 0, 0, 0, 0, 1, 2),
            "constant-provider word labels changed")
    provider_records = {}
    provider_differences = {}
    for section_name, equivariant in (("frozen_lex", False),
                                      ("equivariant", True)):
        _linear_code, quadratic = provider_quadratics(originals, equivariant)
        first_s3 = transferred_s3(3780, originals, quadratic)
        second_s3 = transferred_s3(5108, originals, quadratic)
        if not equivariant:
            require(dict(first_s3) == s3, "frozen provider did not reproduce S3")
        difference = Counter(second_s3)
        for row, value in first_s3.items():
            add_value(difference, row, -value)
        common = sorted(set(first_s3) & set(second_s3))
        require(common == [bytes.fromhex("0491ae"), bytes.fromhex("089bcc")]
                and all(first_s3[row] == second_s3[row] == 1 for row in common),
                "two-provider common support changed")
        provider_records[section_name] = {
            "code3780_support": len(first_s3),
            "code3780_coefficients": {str(value): count for value, count
                                       in sorted(Counter(first_s3.values()).items())},
            "code5108_support": len(second_s3),
            "code5108_coefficients": {str(value): count for value, count
                                       in sorted(Counter(second_s3.values()).items())},
            "support_intersection": len(common),
            "common_equal_rows": [row.hex() for row in common],
            "difference_support": len(difference),
            "difference_coefficients": {str(value): count for value, count
                                         in sorted(Counter(difference.values()).items())},
        }
        provider_differences[section_name] = difference
    require(provider_records["frozen_lex"] == {
        "code3780_support": 66,
        "code3780_coefficients": {"-1": 13, "1": 53},
        "code5108_support": 58,
        "code5108_coefficients": {"-1": 9, "1": 49},
        "support_intersection": 2,
        "common_equal_rows": ["0491ae", "089bcc"],
        "difference_support": 120,
        "difference_coefficients": {"-1": 60, "1": 60},
    }, "frozen two-provider transfer changed")
    require(provider_records["equivariant"]["code3780_support"] == 68
            and provider_records["equivariant"]["code5108_support"] == 60
            and provider_records["equivariant"]["difference_support"] == 124
            and provider_records["equivariant"]["difference_coefficients"]
                == {"-1": 62, "1": 62},
            "equivariant two-provider transfer changed")

    # Complete d5 associated-y3 cells and target-rooted incidence component.
    pairs, _cores, _histogram = COMPLETE.build_pairs(code_to_lead)
    degree5 = {}
    degree3_columns = []
    incidence = defaultdict(list)
    direct_collision_hits = defaultdict(list)
    for cell_index, (lcm, first_code, second_code) in enumerate(pairs):
        polynomial = COMPLETE.s_polynomial(
            lcm, first_code, second_code, originals, code_to_lead
        )
        lead = FIRST.leading_monomial(polynomial)
        degree5[lead] = (first_code, second_code,
                         sum(a != b for a, b in zip(D5.decode_word(first_code),
                                                    D5.decode_word(second_code))))
        layer = {row: value for row, value in polynomial.items() if len(row) == 3}
        if layer:
            column_index = len(degree3_columns)
            degree3_columns.append(("D5", cell_index, first_code, second_code, layer))
            for row in layer:
                incidence[row].append(column_index)
            for row in set(layer) & set(collision):
                direct_collision_hits[row].append(
                    [cell_index, first_code, second_code, layer[row]]
                )
    offset = len(degree3_columns)
    for code, layer in cubic_columns.items():
        column_index = len(degree3_columns)
        degree3_columns.append(("G", code, layer))
        for row in layer:
            incidence[row].append(column_index)
    require(len(pairs) == len(degree5) == 84005
            and len(direct_collision_hits) == 8
            and len({hit[0] for hits in direct_collision_hits.values() for hit in hits}) == 4,
            "complete d5 collision incidence changed")
    require(Counter(len(hits) for hits in direct_collision_hits.values()) == Counter({1: 8}),
            "one collision row gained multiple direct d5 cells")
    require(all(record[0] >= offset for record in degree3_columns[offset:]),
            "unreachable generator offset guard") if False else None

    def component(seed):
        rows = set(seed)
        columns = set()
        queue = deque(seed)
        while queue:
            row = queue.popleft()
            for column_index in incidence.get(row, ()):
                if column_index in columns:
                    continue
                columns.add(column_index)
                layer = degree3_columns[column_index][-1]
                for other in layer:
                    if other not in rows:
                        rows.add(other)
                        queue.append(other)
        return rows, columns

    component_rows, component_columns = component(s3)
    require(len(component_rows) == 187 and len(component_columns) == 10
            and Counter(degree3_columns[index][0] for index in component_columns)
                == Counter({"D5": 8, "G": 2}),
            "S3 target-rooted d5/cubic component changed")
    collision_rows, collision_columns = component(collision)
    require(len(collision_rows) == 73 and len(collision_columns) == 4,
            "collision target-rooted component changed")
    collision_absent = sorted(set(collision) - set(direct_collision_hits))
    require(len(collision_absent) == 30 and collision_absent[0].hex() == "0e4faa",
            "one-row collision separator changed")

    pm4 = json.loads(PM4_RESULT.read_text())
    require(pm4["S3_component"]["translated_cells"] == 0
            and pm4["exact"]["membership"] is False,
            "PM4 translated component changed")

    # Independent complete raw-degree5 low-source component and its smallest
    # exact dual. This is stronger than the Buchberger-cell incidence above.
    low_source = json.loads(LOW_SOURCE_RESULT.read_text())
    require(low_source["degree5_low_source_component"] == {
        **low_source["degree5_low_source_component"],
        "rows": 1311, "columns": 330, "Q_rank": 330,
        "residual52_membership": False,
    }, "low-source component census changed")
    tiny_dual = {bytes.fromhex(row): value
                 for row, value in low_source["minimal_exact_dual"]["support"]}
    require(tiny_dual == {bytes.fromhex("0c4fcc"): 1,
                          bytes.fromhex("1557a7"): 1,
                          bytes.fromhex("3072a7"): -1}
            and low_source["minimal_exact_dual"]["target_pairing"] == 1,
            "minimal exact low-source dual changed")
    residual52 = {row: value for row, value in s3.items()
                  if row not in literal_matching}
    require(len(residual52) == 52
            and sum(tiny_dual.get(row, 0) * value
                    for row, value in residual52.items()) == 1,
            "tiny dual lost residual52 pairing")
    difference_pairings = {
        section: int(sum(tiny_dual.get(row, 0) * value
                         for row, value in difference.items()))
        for section, difference in provider_differences.items()
    }
    require(difference_pairings == {"frozen_lex": 0, "equivariant": 0},
            "second-provider difference killed the tiny dual")

    # Three frozen first d6 cells.
    basis = COMPAT.initial_basis()
    schedule = COMPAT.degree6_schedule(basis)
    first_d6 = []
    for schedule_index, (_lcm, first_index, second_index) in enumerate(schedule[:3], 1):
        _computed_lcm, source = COMPAT.s_polynomial(basis[first_index], basis[second_index])
        remainder, _certificate = COMPAT.reduce_polynomial(source, basis)
        remainder, lead = COMPAT.normalize(remainder)
        hits = sorted(set(remainder) & set(collision))
        first_d6.append({
            "cell": schedule_index,
            "terms": len(remainder),
            "degree3_terms": sum(len(row) == 3 for row in remainder),
            "collision_hits": [row.hex() for row in hits],
        })
        if schedule_index < 3:
            basis.append({"kind": "degree6", "label": schedule_index,
                          "total_degree": 6, "polynomial": remainder, "lead": lead})
    require(not any(record["collision_hits"] for record in first_d6),
            "first d6 cells acquired an S3 collision")

    # Four source-labelled weighted frontier representatives singled out by
    # the frozen path/collision audit.
    selected = selected_weighted_remainders(
        originals, dict(original_lead_to_code), code_to_lead, degree5
    )
    selected_records = []
    for label, remainder, steps in selected:
        hits = sorted(set(remainder) & set(collision))
        selected_records.append({
            "label": label,
            "terms": len(remainder),
            "reduction_steps": steps,
            "degree_histogram": dict(sorted(Counter(map(len, remainder)).items())),
            "collision_hits": [row.hex() for row in hits],
        })
    require(not any(record["collision_hits"] for record in selected_records),
            "selected path/collision frontier acquired an S3 collision")

    # Canonical cap 67, residual triangle 012. A source-faithful response
    # coordinate requires both endpoint orientations with one common spectator.
    factor_records = {}
    factor_histogram = Counter()
    for row in collision:
        factors = response_factorizations(row, s3)
        factor_records[row.hex()] = factors
        factor_histogram[(len(factors),
                          sum(item["inside_triangle"] for item in factors),
                          sum(item["orientation_mate_in_S3"] for item in factors))] += 1
    require(factor_histogram == Counter({
        (0, 0, 0): 28,
        (1, 0, 0): 4,
        (1, 0, 1): 2,
        (2, 0, 0): 3,
        (2, 1, 0): 1,
    }), "canonical triangle response-factor histogram changed")
    full_packets = sorted(row for row, factors in factor_records.items()
                          if any(item["orientation_mate_in_S3"] for item in factors))
    require(full_packets == ["5893de", "589cd5"],
            "full response packet changed")
    inside = [(row, item) for row, factors in factor_records.items()
              for item in factors if item["inside_triangle"]]
    require(len(inside) == 1 and inside[0][0] == "316fb7"
            and inside[0][1]["orientation_mate"] == "3967b7"
            and not inside[0][1]["orientation_mate_in_S3"],
            "triangle-relevant half-response changed")
    valid_factors = [(row, item) for row, factors in factor_records.items()
                     for item in factors if item["valid_normalized_response"]]
    require(not valid_factors
            and not inside[0][1]["spectator_disjoint"]
            and not inside[0][1]["implicit_support_cells"],
            "a primal S3 collision became a valid normalized response")

    # Restrict the minimal three-row dual to the complete internal response
    # packet R_01[1,2] in the K_00 channel with spectator A_34[1,2].
    response_packet = (bytes.fromhex("3072a7"), bytes.fromhex("3969a7"))
    response_pairing = sum(tiny_dual.get(row, 0) for row in response_packet)
    require(response_pairing == -1, "tiny dual lost its internal response pairing")
    tiny_decoding = {
        row.hex(): [list(D5.COORDINATES[value]) for value in row]
        for row in tiny_dual
    }
    require(tiny_decoding == {
        "0c4fcc": [[0, 2, 1, 0], [1, 3, 2, 1], [4, 5, 2, 0]],
        "1557a7": [[0, 3, 1, 0], [1, 4, 2, 0], [3, 4, 1, 2]],
        "3072a7": [[0, 6, 1, 0], [1, 7, 2, 0], [3, 4, 1, 2]],
    }, "tiny dual source decoding changed")

    # Exhaust the deletion-minimal exact three-row duals from the complete
    # raw degree-five low-source component.  This is the precise nine-channel
    # test required by the direct blocker on the normalized orbit-26 chart.
    # A67[00] is the normalized support cell, so
    #   <K,A67> = K00 + sum_(a,b)!=(0,0) y67[a,b] K[a,b].
    # Consequently a first HPL lift of the K00 class needs the other eight
    # matrix-coordinate response channels on this same chart.
    LOW = load("s3_low_source_for_channel_audit", LOW_SOURCE_SCRIPT)
    low_polynomials = LOW.normalized_polynomials(D5)
    low_rows, low_columns = LOW.build_low_component(residual52, low_polynomials)
    low_census, low_separating, _low_row_index = LOW.stopping_set_census(
        low_rows, low_columns, residual52
    )
    require(low_census[-1]["separating_sets"] == len(low_separating) == 28,
            "minimal low-source separator family changed")
    minimal_duals = []
    packet_profile = Counter()
    channel_cells = set()
    response_bearing_duals = 0
    for support in sorted(low_separating, key=lambda item: tuple(sorted(item))):
        support_rows = tuple(low_rows[index] for index in sorted(support))
        dual = primitive_three_dual(support_rows, low_columns, residual52)
        packets = internal_response_restrictions(dual)
        if packets:
            response_bearing_duals += 1
        for packet in packets.values():
            channel_cells.add(tuple(packet["K_cell"]))
            packet_profile[(tuple(packet["response_edge"]),
                            tuple(packet["response_output_colours"]),
                            tuple(packet["K_cell"]))] += 1
        minimal_duals.append({
            "support": [[row.hex(), value] for row, value in sorted(dual.items())],
            "internal_response_packets": list(packets.values()),
        })
    require(channel_cells == {(0, 0)},
            "a fixed-chart minimal dual acquired a non-K00 response channel")
    require(response_bearing_duals > 0, "all minimal response restrictions vanished")
    fixed_chart_missing = [(a, b) for a in range(3) for b in range(3)
                           if (a, b) not in channel_cells]
    colour_orbit_cells = {(colour, colour) for colour in range(3)}
    orbitwise_missing = [(a, b) for a in range(3) for b in range(3)
                         if (a, b) not in colour_orbit_cells]
    require(len(fixed_chart_missing) == 8 and len(orbitwise_missing) == 6,
            "direct-blocker channel cokernel changed")

    # Source-labelled compatibility with the archived quotient-collapse
    # theorem.  The tiny packet is the xy=01, t=2 response coordinate for
    # cap 67, residual triangle 012 and O=345.  Its omitted fourth matching
    # edge is exactly the normalized support anchor A25[00]=1.
    anchor_67_00 = coordinate_id(6, 7, 0, 0)
    anchor_25_00 = coordinate_id(2, 5, 0, 0)
    require((anchor_67_00, anchor_25_00) == (243, 135)
            and not D5.IS_OFF_SUPPORT[anchor_67_00]
            and not D5.IS_OFF_SUPPORT[anchor_25_00],
            "orbit-26 cap/cofactor anchors changed")
    tiny_packet_factor = next(
        factor for factor in response_factorizations(response_packet[0], tiny_dual)
        if factor["inside_triangle"] and factor["valid_normalized_response"]
    )
    require(tiny_packet_factor["response_edge"] == [0, 1]
            and tiny_packet_factor["K_cell"] == [0, 0]
            and tiny_packet_factor["response_output_colours"] == [1, 2]
            and tiny_packet_factor["spectator"] == [3, 4, 1, 2]
            and tiny_packet_factor["implicit_support_cells"] == [anchor_25_00],
            "tiny dual no longer lies in the literal 01-response coordinate")
    pure_quotient = json.loads(PURE_QUOTIENT_RESULT.read_text())
    require(pure_quotient["primes"] == [1009, 1013]
            and pure_quotient["identity_checks_per_source_prime"] == 756
            and pure_quotient["triangle_groups_per_source_prime"] == 1680,
            "pure quotient-collapse ledger changed")
    carrier_restriction = json.loads(CARRIER_RESTRICTION_RESULT.read_text())
    next_attachment = json.loads(NEXT_ATTACHMENT_RESULT.read_text())
    require(carrier_restriction["logical_sha256"]
                == "24b3590e37a3ed115e9370904ed0f211c661d90e02ef7d738f4d47853d1ad8e9"
            and next_attachment["canonical_direct_blocker_test"]
                ["independent_provider_columns"] == 18
            and next_attachment["canonical_direct_blocker_test"]
                ["off_support_cap_corrections"] == 16
            and next_attachment["first_new_total_degree6_layer"]
                ["incident_columns"] == 14,
            "carrier restriction/next-attachment guard changed")
    quotient_bridge = {
        "cap_pair": [6, 7],
        "residual_triangle": [0, 1, 2],
        "tiny_response_edge_xy": [0, 1],
        "opposite_vertex_t": 2,
        "outside_sites_O": [3, 4, 5],
        "five_set_W": [0, 1, 3, 4, 5],
        "tiny_K_cell": [0, 0],
        "tiny_response_output_colours": [1, 2],
        "tiny_spectator": [3, 4, 1, 2],
        "implicit_normalized_support_cell": {
            "id": anchor_25_00,
            "coordinate": [2, 5, 0, 0],
            "value": 1,
        },
        "quotient_identities": [
            "[K00] = H0 [<K,A67>]",
            "[K11] = H1 [<K,A67>]",
            "[K22] = H2 [<K,A67>]",
        ],
        "open_hypotheses": (
            "for every c=0,1,2 and every cyclic t in triangle012, the "
            "five-set response increment is 9; and H0*H1*H2 is nonzero"
        ),
        "interior_consequence": (
            "all four evaluated blocker classes K00,K11,K22,<K,A67> are "
            "equivalent; hence the four-way membership disjunction collapses "
            "to the K00 response image"
        ),
        "remaining_obligations": {
            "chain_coherence_on_the_open": (
                "the inverse-system dual reads only one of the two independent "
                "degree6 response-orientation columns; quotient rowspace "
                "equivalence supplies no source syzygy joining the companion"
            ),
            "five_set_determinantal": (
                "at least one of the nine (c,t) response increments is <=8"
            ),
            "pure_cofactor": "H0*H1*H2=0",
        },
        "direct_HPL_scope": (
            "the exact identity supersedes nine-channel lifting only for the "
            "blocker-membership disjunction. It does not fill the source-complex "
            "class: the two K00 orientations are separate degree6 singleton "
            "columns, and the 16 direct corrections are separate degree7 columns"
        ),
        "chain_level_verdict": (
            "response-image attachment only, not annihilation of the S3 class; "
            "no injectivity theorem for response restriction is available"
        ),
        "replay": (
            "python3 computations/unaudited-codex-triangle-pure-quotient-"
            "collapse-2026-08-22/check_results.py"
        ),
    }

    if mutate:
        factor_histogram[(0, 0, 0)] += 1
    require(sum(factor_histogram.values()) == 38,
            "hostile factorization mutation survived")

    result = {
        "format": "n8-S3-source-HPL-audit-v1",
        "status": "EXACT SURVIVING COLLISION/TOR CLASS",
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
        "S3": {
            "rows": 66,
            "coefficient_histogram": dict(sorted(Counter(s3.values()).items())),
            "physical_skeletons": dict(sorted(profile.items())),
        },
        "literal_cubic_test": {
            "generators": len(originals),
            "distinct_cubic_outputs": len(cubic_occurrences),
            "global_cubic_monomial_multiplicity": 1,
            "matching_rows": len(matching),
            "literal_matching_rows": len(literal_matching),
            "literal_matching_source_code": 3780,
            "literal_matching_source_word": "12012000",
            "literal_target_signs": dict(sorted(Counter(
                matching[row] for row in literal_matching).items())),
            "absent_matching_rows": len(absent_matching),
            "lex_absent_matching_separator": absent_matching[0].hex(),
            "guard": (
                "the 14 present monomials cannot be cancelled separately: "
                "they belong to one 32-term cubic layer, with target signs 13-/1+"
            ),
        },
        "second_constant_provider": {
            "providers": [
                {"code": 3780, "word": "12012000", "constant": 1},
                {"code": 5108, "word": "21000012", "constant": 1},
            ],
            "sections": provider_records,
            "constant_canceling_cell": "S3(5108)-S3(3780)",
            "tiny_dual_pairing_with_difference": difference_pairings,
            "verdict": (
                "the provider difference does not kill residual52; the exact "
                "three-row low-source dual annihilates it for both sections"
            ),
        },
        "complete_degree5_y3_test": {
            "cells": len(pairs),
            "cells_with_y3": sum(record[0] == "D5" for record in degree3_columns),
            "collision_rows": len(collision),
            "directly_incident_collision_rows": len(direct_collision_hits),
            "directly_incident_cells": len({hit[0] for hits in direct_collision_hits.values()
                                             for hit in hits}),
            "direct_incidence": {row.hex(): hits for row, hits
                                  in sorted(direct_collision_hits.items())},
            "S3_component_rows": len(component_rows),
            "S3_component_columns": len(component_columns),
            "S3_component_column_types": dict(sorted(Counter(
                degree3_columns[index][0] for index in component_columns).items())),
            "collision_component_rows": len(collision_rows),
            "collision_component_columns": len(collision_columns),
            "collision_rows_absent_all_d5_cells": len(collision_absent),
            "lex_one_row_collision_separator": collision_absent[0].hex(),
            "canonical_Bianchi_guard": (
                "all four canonical star cells are in the complete d5 scan; "
                "all S3 incidences are Hamming-two direct-double cells"
            ),
        },
        "existing_higher_cell_test": {
            "PM4_degree_one_translated_cells_meeting_S3": 0,
            "first_three_degree6_cells": first_d6,
            "selected_weighted_path_collision_representatives": selected_records,
            "verdict": "no S3 collision row occurs in these frozen source-labelled cells",
        },
        "canonical_triangle_67_012": {
            "collision_rows_without_any_response_factorization": 28,
            "factor_histogram": [
                {"factorizations": key[0], "inside_triangle": key[1],
                 "mates_in_S3": key[2], "rows": value}
                for key, value in sorted(factor_histogram.items())
            ],
            "only_complete_orientation_packet": full_packets,
            "complete_packet_response_edge": [2, 4],
            "complete_packet_is_outside_triangle": True,
            "triangle_relevant_half_response": "316fb7",
            "missing_orientation_mate": "3967b7",
            "cokernel_verdict": (
                "the apparent complete outside packet and the apparent internal "
                "half-packet are physical collision factorizations: their third "
                "edge meets a response endpoint/cap, so neither is a normalized "
                "response coordinate. The primal S3 packet has no valid response."
            ),
            "blocker_verdict": (
                "the primal S3 packet has no complete internal response, but "
                "the minimal dual restricts nontrivially to exactly the K00 "
                "channel; only the K00 blocker kills this restriction"
            ),
            "minimal_dual": {
                "support": [[row.hex(), value] for row, value in sorted(tiny_dual.items())],
                "decoded_source_cells": tiny_decoding,
                "response_packet": [row.hex() for row in response_packet],
                "response_packet_pairing": response_pairing,
                "response_identification": (
                    "-K00 * R_01[1,2] * A_34[1,2] on the complete two-orientation packet"
                ),
                "cap_error_guard": (
                    "this is cubic in source cells, while N8 cap error terms "
                    "s*r^2*x and r^3 have source degree six"
                ),
                "Bockstein_guard": (
                    "support skeletons are simple 3P2, P4, 3P2; there is no C4 "
                    "and no parallel physical/decorated edge"
                ),
                "blocker_rank_test": {
                    "K00_in_rowspan": "restriction vanishes",
                    "K11_in_rowspan": (
                        "covered by the global colour transport on the corresponding "
                        "colour-permuted normalized chart"
                    ),
                    "K22_in_rowspan": (
                        "covered by the global colour transport on the corresponding "
                        "colour-permuted normalized chart"
                    ),
                    "direct_in_rowspan": (
                        "its leading form is K00 because A67[00]=1, but its first "
                        "correction requires the eight absent fixed-chart K_ab channels"
                    ),
                },
            },
            "direct_blocker_HPL_channel_test": {
                "normalized_anchor": "A67[00]=1",
                "direct_form": (
                    "<K,A67> = K00 + sum_{(a,b)!=(0,0)} y67[a,b] K_ab"
                ),
                "minimal_exact_duals": len(minimal_duals),
                "response_bearing_minimal_duals": response_bearing_duals,
                "minimal_dual_records": minimal_duals,
                "response_packet_profile": [
                    {"response_edge": list(key[0]),
                     "response_output_colours": list(key[1]),
                     "K_cell": list(key[2]), "dual_occurrences": value}
                    for key, value in sorted(packet_profile.items())
                ],
                "fixed_chart_channel_cells": [list(cell)
                                              for cell in sorted(channel_cells)],
                "fixed_chart_channel_rank": len(channel_cells),
                "fixed_chart_cokernel_cells": [list(cell)
                                                for cell in fixed_chart_missing],
                "colour_transport_channel_cells": [list(cell)
                                                    for cell in sorted(colour_orbit_cells)],
                "colour_transport_channel_rank": len(colour_orbit_cells),
                "colour_transport_cokernel_cells": [list(cell)
                                                     for cell in orbitwise_missing],
                "first_correction": (
                    "a direct lift must add y67[a,b]*lambda_ab for every nonanchor "
                    "cell; no deletion-minimal fixed-chart dual supplies any of "
                    "those eight lambda_ab directions"
                ),
                "verdict": (
                    "the three diagonal blocker branches are covered orbitwise by "
                    "global colour transport, but the direct branch is not closed "
                    "under first HPL perturbation; even after transport the six "
                    "off-diagonal Mat3 channels remain a literal cokernel. The exact "
                    "quotient-collapse identity collapses blocker memberships on the "
                    "common open but does not provide the missing source-complex chain"
                ),
            },
            "pure_quotient_collapse_attachment": quotient_bridge,
        },
        "smallest_survivor": {
            "lex_collision_row": "0e4faa",
            "coefficient": 1,
            "skeleton": "P3+P2",
            "physical_edges": [[0, 2], [1, 3], [3, 4]],
            "dual": "delta_0e4faa",
            "annihilates": (
                "all literal cubic layers, complete d5 y3 cells, PM4 degree-one "
                "translates, first three d6 cells, and four frozen weighted "
                "path/collision representatives"
            ),
            "triangle_scope": "cap-67 invisible (no 6/7 response-spoke pair)",
        },
        "scope_guard": (
            "This is an exact bounded associated-graded/source-cell audit. It "
            "does not enumerate the full degree6 frontier or prove nonmembership "
            "against all higher HPL cells. The surviving delta is a certificate "
            "only for the explicitly listed complete/bounded cell families."
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        canonical = json.loads(json.dumps(result, sort_keys=True))
        require(RESULT.exists() and json.loads(RESULT.read_text()) == canonical,
                "stored result changed")
    print(result["status"])
    print("S3/collision/d5-hit=", 66, 38,
          result["complete_degree5_y3_test"]["directly_incident_collision_rows"])
    print("survivor/triangle-half=", result["smallest_survivor"]["lex_collision_row"],
          result["canonical_triangle_67_012"]["triangle_relevant_half_response"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
