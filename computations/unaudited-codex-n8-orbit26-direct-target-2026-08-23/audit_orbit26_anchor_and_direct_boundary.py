#!/usr/bin/env python3
"""Exact orbit-26 anchor lift and first direct F^h boundary.

This checker has two deliberately bounded jobs.

1. Keep nine selected support cells equal to one and retain the three pure
   matching invariants u0,u1,u2.  Replay the frozen six-column normalized
   contraction before specializing the u's.
2. Normalize all twelve support cells, replay the frozen exact degree-five
   full-source certificate, and extract only the first possible residual
   layer of the direct target F^h=H_0^h H_1^h H_2^h, namely y-degree six.

No Groebner basis, saturation, or unbounded closure is performed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NORMALIZED_PATH = ROOT / "computations" / "verify_n8_normalized_critical_contraction.py"
TARGET_EXPORTER_PATH = (
    ROOT
    / "computations"
    / "unaudited-codex-31-chart-full-fibre-gate-2026-08-22"
    / "export_normalized_chart_full_fibre.py"
)
RESULTS = HERE / "results_orbit26_anchor_and_direct_boundary.json"
RESIDUAL_PACKET = HERE / "direct_fh_y6_residual.txt"
PROVIDER_PACKET = HERE / "direct_fh_unique_min_provider.txt"
QQ = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


NORM = load_module("n8_normalized_critical", NORMALIZED_PATH)
D5 = NORM.D5
EXPORTER = load_module("n8_target_chart_exporter", TARGET_EXPORTER_PATH)


def xname(coordinate):
    u, v, a, b = coordinate
    return f"x{u}{v}_{a}{b}"


def fraction_pair(value):
    return [value.numerator, value.denominator]


def histogram_pairs(histogram):
    return [
        {"value": fraction_pair(value), "count": count}
        for value, count in sorted(histogram.items())
    ]


def normalized_row(row):
    return bytes(sorted(value for value in row if D5.IS_OFF_SUPPORT[value]))


def normalized_generator(code):
    return Counter(normalized_row(term) for term in D5.iter_word_terms(code))


def quotient(divisor, monomial):
    answer = list(monomial)
    for value in divisor:
        answer.remove(value)
    return bytes(answer)


def divides(divisor, monomial):
    return Counter(divisor) <= Counter(monomial)


def support_data():
    by_colour = {colour: [] for colour in range(3)}
    for variable in D5.SUPPORT_IDS:
        coordinate = D5.COORDINATES[variable]
        require(coordinate[2] == coordinate[3], "support cell is not pure")
        by_colour[coordinate[2]].append(variable)
    for colour in by_colour:
        by_colour[colour].sort(key=lambda variable: xname(D5.COORDINATES[variable]))
        require(len(by_colour[colour]) == 4, "pure support is not a matching")
    anchors = tuple(by_colour[colour][-1] for colour in range(3))
    normalized = frozenset(D5.SUPPORT_IDS - frozenset(anchors))
    require(len(normalized) == 9, "nine-cell normalization changed")

    mate = [-1] * 24
    for variable in D5.SUPPORT_IDS:
        u, v, a, b = D5.COORDINATES[variable]
        first, second = 3 * u + a, 3 * v + b
        mate[first] = second
        mate[second] = first
    source = EXPORTER.CHARTS.SOURCE
    rows = tuple(sorted(source.target_orbit_rows()))
    orbit = rows.index(source.canonical_key(tuple(mate))) + 1
    require(orbit == 26, "the actual t7 import chain is not current orbit 26")
    return by_colour, normalized, anchors, orbit


def residual_weight_function():
    """Character on the residual torus fixing all twelve support cells.

    The twelve support edges are a perfect matching of the 24 site-colour
    ports.  On the residual torus the two endpoint characters on each such
    edge are negatives.  Orient the smaller port positively; this gives a
    concrete Z^12 character coordinate system.
    """
    port_coordinate = {}
    for position, variable in enumerate(sorted(D5.SUPPORT_IDS)):
        u, v, a, b = D5.COORDINATES[variable]
        first, second = 3 * u + a, 3 * v + b
        if first > second:
            first, second = second, first
        port_coordinate[first] = position, 1
        port_coordinate[second] = position, -1
    require(len(port_coordinate) == 24, "support does not pair all ports")

    def weight(row):
        answer = [0] * 12
        for variable in row:
            u, v, a, b = D5.COORDINATES[variable]
            for port in (3 * u + a, 3 * v + b):
                position, sign = port_coordinate[port]
                answer[position] += sign
        return tuple(answer)

    return weight


def anchor_bridge(normalized_support, anchors, weight):
    anchor_position = {variable: index for index, variable in enumerate(anchors)}

    def anchor_key(row):
        off = []
        exponent = [0, 0, 0]
        for variable in row:
            if variable in normalized_support:
                continue
            if variable in anchor_position:
                exponent[anchor_position[variable]] += 1
            else:
                require(D5.IS_OFF_SUPPORT[variable], "unclassified source variable")
                off.append(variable)
        return bytes(sorted(off)), tuple(exponent)

    image = defaultdict(QQ)
    actual_columns = set()
    for scalar, code, multiplier in NORM.CONTRACTION:
        for actual_column in NORM.column_orbit((code, multiplier)):
            actual_columns.add(actual_column)
            for term in D5.iter_word_terms(actual_column[0]):
                image[anchor_key(actual_column[1] + term)] += scalar
    image = {key: value for key, value in image.items() if value}
    core = {
        exponent: coefficient
        for (off, exponent), coefficient in image.items()
        if not off
    }
    tail = {
        (off, exponent): coefficient
        for (off, exponent), coefficient in image.items()
        if off
    }
    require(core == {(0, 0, 0): QQ(1, 2), (1, 0, 0): QQ(1, 2)},
            "anchor-parametric core changed")

    specialized = defaultdict(QQ)
    for (off, _exponent), coefficient in image.items():
        specialized[off] += coefficient
    specialized = {row: value for row, value in specialized.items() if value}
    require(specialized.pop(b"") == 1 and len(specialized) == 2240,
            "u=1 did not recover the frozen all-twelve contraction")
    require(all(weight(off) == (0,) * 12 for off, _exponent in tail),
            "anchor tail escaped residual T0 weight zero")

    logical_lines = []
    for (off, exponent), coefficient in sorted(image.items()):
        logical_lines.append(
            f"{off.hex()}:{','.join(map(str, exponent))}:"
            f"{coefficient.numerator}/{coefficient.denominator}"
        )
    return {
        "six_column_orbit_representatives": len(NORM.CONTRACTION),
        "expanded_literal_columns": len(actual_columns),
        "anchor_core": "(1+u0)/2",
        "anchor_core_terms": [
            {"u_exponent": list(exponent), "coefficient": fraction_pair(coefficient)}
            for exponent, coefficient in sorted(core.items())
        ],
        "anchor_refined_tail_terms": len(tail),
        "tail_off_degree_histogram": dict(sorted(Counter(
            len(off) for off, _exponent in tail
        ).items())),
        "tail_anchor_exponent_histogram": {
            ",".join(map(str, exponent)): count
            for exponent, count in sorted(Counter(
                exponent for _off, exponent in tail
            ).items())
        },
        "tail_coefficient_histogram": histogram_pairs(Counter(tail.values())),
        "residual_T0_character_count": len({weight(off) for off, _ in tail}),
        "residual_T0_character": [0] * 12,
        "specialization_u_equal_one_tail_terms": len(specialized),
        "anchor_polynomial_sha256": sha256(
            ("\n".join(logical_lines) + "\n").encode("ascii")
        ).hexdigest(),
        "interpretation": (
            "the six-column contraction lifts over Q[u0,u1,u2,(u0u1u2)^-1], "
            "but its target is (1+u0)/2 rather than a Laurent unit"
        ),
    }


def truncated_product(polynomials, maximum_degree):
    answer = Counter({b"": 1})
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                row = bytes(sorted(left + right))
                if len(row) <= maximum_degree:
                    updated[row] += left_coefficient * right_coefficient
        answer = updated
    return answer


def direct_boundary(weight):
    maximum_degree = 6
    generator_cache = {}

    def generator(code):
        if code not in generator_cache:
            generator_cache[code] = normalized_generator(code)
        return generator_cache[code]

    pure = tuple(generator(D5.word_code((colour,) * 8)) for colour in range(3))
    target = truncated_product(pure, maximum_degree)

    certificate = json.loads(D5.CERTIFICATE_PATH.read_text())
    require(len(certificate["solution"]) == 7861,
            "frozen degree-five solution support changed")
    image = {}
    actual_columns = 0
    for item in certificate["solution"]:
        code = D5.word_code(tuple(item["word"]))
        multiplier = bytes(
            D5.COORDINATE_ID[tuple(variable)] for variable in item["multiplier"]
        )
        scalar = QQ(item["numerator"], item["denominator"])
        for actual_code, actual_multiplier in D5.column_orbit((code, multiplier)):
            actual_columns += 1
            normalized_multiplier = normalized_row(actual_multiplier)
            if len(normalized_multiplier) > maximum_degree:
                continue
            for term, coefficient in generator(actual_code).items():
                row = bytes(sorted(normalized_multiplier + term))
                if len(row) > maximum_degree:
                    continue
                value = image.get(row, QQ(0)) + scalar * coefficient
                if value:
                    image[row] = value
                else:
                    image.pop(row, None)

    residual = {}
    for row in set(target) | set(image):
        value = QQ(target.get(row, 0)) - image.get(row, QQ(0))
        if value:
            residual[row] = value
    require(residual and set(map(len, residual)) == {6},
            "degree-five certificate did not cancel every lower normalized layer")
    require(len(residual) == 224319, "direct degree-six boundary census changed")
    require(all(weight(row) == (0,) * 12 for row in residual),
            "direct boundary escaped residual T0 weight zero")

    residual_lines = [
        f"{row.hex()}:{coefficient.numerator}/{coefficient.denominator}"
        for row, coefficient in sorted(residual.items())
    ]
    lex_row = min(residual)
    require(lex_row.hex() == "01030876ccf8" and residual[lex_row] == 1,
            "lex-first direct boundary row changed")

    # Exact first incidence shell at the lexicographically first residual row.
    literal_columns = {}
    minimum_degree_histogram = Counter()
    minimum_layer_histogram = Counter()
    unique_minimum_terms = defaultdict(list)
    for code in range(3 ** 8):
        if len(set(D5.decode_word(code))) == 1:
            continue
        polynomial = generator(code)
        minimum_degree = min(map(len, polynomial))
        minimum_layer = {
            term: coefficient
            for term, coefficient in polynomial.items()
            if len(term) == minimum_degree
        }
        minimum_degree_histogram[minimum_degree] += 1
        minimum_layer_histogram[minimum_degree, len(minimum_layer)] += 1
        if len(minimum_layer) == 1:
            term, coefficient = next(iter(minimum_layer.items()))
            require(coefficient == 1, "unique normalized minimum is not monic")
            unique_minimum_terms[term].append(code)
        for term, coefficient in polynomial.items():
            if divides(term, lex_row):
                column = (code, quotient(term, lex_row))
                literal_columns[column] = term, coefficient

    require(minimum_degree_histogram
            == Counter({0: 2, 1: 358, 2: 2298, 3: 3058, 4: 842}),
            "normalized leading-degree word census changed")
    require(minimum_layer_histogram == Counter({
        (0, 1): 2,
        (1, 1): 358,
        (2, 3): 2298,
        (3, 15): 3058,
        (4, 105): 842,
    }), "normalized leading-layer support census changed")
    require(set(unique_minimum_terms) == (
        {b""} | {bytes([variable]) for variable in range(252)
                  if D5.IS_OFF_SUPPORT[variable]}
    ), "constant/linear unique minima do not cover all normalized variables")
    require(len(literal_columns) == 29, "lex boundary incident census changed")

    degree_six_support_histogram = Counter()
    exchange_distance_histogram = Counter()
    diagonal_coefficient_histogram = Counter()
    output_profile_histogram = Counter()
    private_columns = []
    lex_counter = Counter(lex_row)
    for column, (incident_term, incident_coefficient) in literal_columns.items():
        outputs = Counter()
        for term, coefficient in generator(column[0]).items():
            outputs[bytes(sorted(column[1] + term))] += coefficient
        degree_six = {row: value for row, value in outputs.items() if len(row) == 6}
        degree_six_support_histogram[len(degree_six)] += 1
        diagonal_coefficient_histogram[degree_six[lex_row]] += 1
        output_profile = tuple(sorted(Counter(map(len, outputs)).items()))
        output_profile_histogram[output_profile] += 1
        if len(degree_six) == 1:
            private_columns.append((column, incident_term, output_profile))
            exchange_distance_histogram[0] += 1
        else:
            distance = min(
                6 - sum((Counter(row) & lex_counter).values())
                for row in degree_six if row != lex_row
            )
            exchange_distance_histogram[distance] += 1

    require(degree_six_support_histogram
            == Counter({1: 10, 3: 4, 6: 5, 15: 1, 24: 3,
                        30: 3, 68: 1, 78: 2}),
            "lex boundary support histogram changed")
    require(exchange_distance_histogram == Counter({0: 10, 2: 19}),
            "lex boundary exchange-distance histogram changed")
    require(diagonal_coefficient_histogram == Counter({1: 29}),
            "lex boundary diagonal coefficients changed")

    private_columns.sort(key=lambda item: item[0])
    chosen_column, chosen_term, chosen_profile = private_columns[0]
    chosen_word = "".join(map(str, D5.decode_word(chosen_column[0])))
    require(
        chosen_word == "00000012"
        and chosen_column[1].hex() == "01030876cc"
        and chosen_term.hex() == "f8"
        and chosen_profile == ((6, 1), (7, 6), (8, 30), (9, 68)),
        "chosen private boundary pivot changed",
    )

    # Freeze the exact scaled residual and the tiny source provider needed by
    # the deterministic transfer to degree ten.  The factor four clears every
    # denominator in this boundary, so the Rust continuation can use integers.
    residual_packet_lines = [
        f"KRENN_N8_DIRECT_FH_Y6_V1 SCALE 4 COUNT {len(residual)}"
    ]
    for row, coefficient in sorted(residual.items()):
        scaled = 4 * coefficient
        require(scaled.denominator == 1, "boundary denominator does not divide four")
        residual_packet_lines.append(f"ROW {row.hex()} {scaled.numerator}")
    residual_packet_text = "\n".join(residual_packet_lines) + "\n"
    RESIDUAL_PACKET.write_text(residual_packet_text, encoding="ascii")

    constant_codes = sorted(unique_minimum_terms[b""])
    require(len(constant_codes) == 2, "constant-word census changed")
    provider_lines = ["KRENN_N8_UNIQUE_MIN_PROVIDER_V1"]
    constant_code = constant_codes[0]
    provider_lines.append(
        f"CONSTANT {constant_code} {''.join(map(str, D5.decode_word(constant_code)))}"
    )
    for term, coefficient in sorted(generator(constant_code).items()):
        require(coefficient == 1, "constant provider is not monic")
        provider_lines.append(
            f"CTERM {len(term)} {term.hex() or '-'} {coefficient}"
        )
    for variable in range(252):
        if not D5.IS_OFF_SUPPORT[variable]:
            continue
        codes = sorted(unique_minimum_terms[bytes([variable])])
        require(codes, "normalized variable lost its linear provider")
        code = codes[0]
        provider_lines.append(
            f"LINEAR {variable} {code} {''.join(map(str, D5.decode_word(code)))}"
        )
        degree_two = {
            term: coefficient
            for term, coefficient in generator(code).items()
            if len(term) == 2
        }
        require(len(degree_two) == 6 and all(value == 1 for value in degree_two.values()),
                "linear provider lost its six quadratic tails")
        for term, coefficient in sorted(degree_two.items()):
            provider_lines.append(f"L2 {variable} {term.hex()} {coefficient}")
    provider_packet_text = "\n".join(provider_lines) + "\n"
    PROVIDER_PACKET.write_text(provider_packet_text, encoding="ascii")

    return {
        "homogenized_target": "F^h=H_0^h*H_1^h*H_2^h, total degree 12",
        "normalized_variables": 240,
        "homogenizing_variables": 1,
        "frozen_degree5_certificate_orbit_columns": len(certificate["solution"]),
        "expanded_literal_certificate_columns": actual_columns,
        "target_terms_through_y_degree6": len(target),
        "certificate_image_terms_through_y_degree6": len(image),
        "first_residual_y_degree": 6,
        "first_residual_t_degree": 6,
        "first_residual_terms": len(residual),
        "first_residual_coefficient_histogram": histogram_pairs(Counter(residual.values())),
        "first_residual_sha256": sha256(
            ("\n".join(residual_lines) + "\n").encode("ascii")
        ).hexdigest(),
        "scaled_residual_packet": str(RESIDUAL_PACKET.relative_to(ROOT)),
        "scaled_residual_packet_sha256": sha256(
            residual_packet_text.encode("ascii")
        ).hexdigest(),
        "unique_minimum_provider_packet": str(PROVIDER_PACKET.relative_to(ROOT)),
        "unique_minimum_provider_packet_sha256": sha256(
            provider_packet_text.encode("ascii")
        ).hexdigest(),
        "residual_T0_character_count": 1,
        "residual_T0_character": [0] * 12,
        "leading_word_minimum_degree_histogram": dict(sorted(minimum_degree_histogram.items())),
        "leading_word_minimum_layer_histogram": {
            f"degree{degree}_support{support}": count
            for (degree, support), count in sorted(minimum_layer_histogram.items())
        },
        "unique_minimum_terms": len(unique_minimum_terms),
        "unique_linear_minimum_terms": sum(len(term) == 1 for term in unique_minimum_terms),
        "unique_linear_terms_cover_all_y_variables": True,
        "acyclic_contraction_range": (
            "every positive y-degree row through degree 9 has a distinct monic "
            "source column whose unique lowest output is that row; all other "
            "outputs have strictly larger y-degree"
        ),
        "first_coupled_degree": 10,
        "first_coupled_rule": (
            "degree-10 rows require a degree-2 generator term because the "
            "multiplier has total degree 8; every degree-2 minimum layer has "
            "exactly three monic terms"
        ),
        "lex_first_residual": {
            "row": lex_row.hex(),
            "coefficient": fraction_pair(residual[lex_row]),
            "literal_incident_columns": len(literal_columns),
            "support_stabilizer_column_orbits": len({
                NORM.canonical_column(column) for column in literal_columns
            }),
            "degree6_support_histogram": dict(sorted(degree_six_support_histogram.items())),
            "exchange_distance_histogram": dict(sorted(exchange_distance_histogram.items())),
            "private_degree6_columns": len(private_columns),
            "chosen_private_pivot": {
                "word": chosen_word,
                "word_code": chosen_column[0],
                "normalized_multiplier": chosen_column[1].hex(),
                "incident_generator_term": chosen_term.hex(),
                "multiplier_t_exponent": 8 - len(chosen_column[1]),
                "output_y_degree_histogram": dict(chosen_profile),
                "effect": (
                    "cancels the selected y^6*t^6 row and creates only "
                    "6 y^7*t^5, 30 y^8*t^4, and 68 y^9*t^3 rows"
                ),
            },
        },
        "scope": (
            "exact first-boundary extraction and contraction theorem only; "
            "the coupled degree-10/11/12 exchange complex is not solved"
        ),
    }


def audit():
    by_colour, normalized_support, anchors, orbit = support_data()
    weight = residual_weight_function()
    anchor = anchor_bridge(normalized_support, anchors, weight)
    boundary = direct_boundary(weight)
    source_variables = 252 - len(normalized_support)
    require(source_variables == 243, "source variable count changed")
    result = {
        "format": "n8-orbit26-anchor-and-direct-boundary-v1",
        "status": "EXACT_BOUNDED_PASS",
        "arithmetic": "Q",
        "current_target_chart_orbit": orbit,
        "nomenclature_guard": (
            "the t7/t8 import chain uses verify_n8_full_source_pure_product_"
            "degree5_lift.py and is current target-chart orbit 26; the separate "
            "dangerous-chart array index 26 is a different legacy orbit-29 lane"
        ),
        "literal_support_by_colour": {
            str(colour): [xname(D5.COORDINATES[value]) for value in by_colour[colour]]
            for colour in range(3)
        },
        "nine_cells_set_to_one": [
            xname(D5.COORDINATES[value]) for value in sorted(normalized_support)
        ],
        "live_invariant_anchors": [
            {"symbol": f"u{index}", "source_cell": xname(D5.COORDINATES[value])}
            for index, value in enumerate(anchors)
        ],
        "anchor_chart_interface": {
            "source_variables_after_nine_normalizations": source_variables,
            "product_inverse_variables": 1,
            "total_variables_with_product_inverse": source_variables + 1,
            "full_fibre_amplitude_equations": 6561,
            "product_inverse_equations": 1,
            "total_full_fibre_equations": 6562,
            "mixed_localized_equations": 6558 + 1,
            "inverse_equation": "zP*u0*u1*u2-1",
        },
        "anchor_bridge": anchor,
        "direct_Fh_boundary": boundary,
        "source_files": {
            str(NORMALIZED_PATH.relative_to(ROOT)): sha256(NORMALIZED_PATH.read_bytes()).hexdigest(),
            str(D5.CERTIFICATE_PATH.relative_to(ROOT)): sha256(D5.CERTIFICATE_PATH.read_bytes()).hexdigest(),
            str(TARGET_EXPORTER_PATH.relative_to(ROOT)): sha256(TARGET_EXPORTER_PATH.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return result


def main():
    result = audit()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("n8 orbit26 anchor/direct boundary: PASS")
    print("anchor core:", result["anchor_bridge"]["anchor_core"])
    print("direct boundary:", result["direct_Fh_boundary"]["first_residual_terms"])
    print("first coupled degree:", result["direct_Fh_boundary"]["first_coupled_degree"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
