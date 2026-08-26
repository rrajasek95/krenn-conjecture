#!/usr/bin/env python3
"""Export the exact factor-preserving transfer kernels at y-degree ten.

This is a straight-line representation of the correction of the *complete*
original residual through y-degree ten.  In scale-four convention it is

  C10 = R10 - R8*h2 + R7*S3 + R6*S4 + L(R9),

where the monic constant provider is 1+h2+h3+h4, the monic linear provider
at cell x is x+q2_x, and

  S3 = -h3 + sum_{m2 in h2} (m2/x(m2))*q2_x(m2),
  S4 = -h4 + h2^2 + sum_{m3 in h3} (m3/x(m3))*q2_x(m3).

The selector x(m) is the smallest cell of m.  No division by a coefficient
or source variable occurs.  The script also exports the literal N4
three-term leading blocks of all minimum-y-degree-two mixed generators.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations" / "verify_n8_normalized_critical_contraction.py"
PROVIDER = HERE / "direct_fh_unique_min_provider.txt"
KERNEL_PACKET = HERE / "direct_fh_transfer_kernels.txt"
BLOCK_PACKET = HERE / "quadratic_pm4_blocks.txt"
RESULTS = HERE / "results_factored_y10_transfer.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("n8_normalized", SOURCE)
NORM = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load normalized source")
spec.loader.exec_module(NORM)
D5 = NORM.D5


def add(vector, row, coefficient):
    value = vector[row] + coefficient
    if value:
        vector[row] = value
    else:
        del vector[row]


def product(left, right):
    answer = Counter()
    for lrow, lcoefficient in left.items():
        for rrow, rcoefficient in right.items():
            add(answer, bytes(sorted(lrow + rrow)), lcoefficient * rcoefficient)
    return answer


def divide_cell(row, cell):
    values = list(row)
    values.remove(cell)
    return bytes(values)


def parse_provider():
    constant = defaultdict(Counter)
    linear_code = {}
    quadratic = defaultdict(Counter)
    constant_code = None
    for line_number, line in enumerate(PROVIDER.read_text(encoding="ascii").splitlines(), 1):
        fields = line.split()
        if line_number == 1:
            require(fields == ["KRENN_N8_UNIQUE_MIN_PROVIDER_V1"], "provider magic changed")
        elif fields[0] == "CONSTANT":
            constant_code = int(fields[1])
        elif fields[0] == "CTERM":
            degree = int(fields[1])
            row = b"" if fields[2] == "-" else bytes.fromhex(fields[2])
            constant[degree][row] += int(fields[3])
        elif fields[0] == "LINEAR":
            linear_code[int(fields[1])] = int(fields[2])
        elif fields[0] == "L2":
            quadratic[int(fields[1])][bytes.fromhex(fields[2])] += int(fields[3])
        else:
            raise RuntimeError(f"bad provider line {line_number}")
    require(constant_code == 3780, "constant provider changed")
    require({degree: len(rows) for degree, rows in constant.items()}
            == {0: 1, 2: 12, 3: 32, 4: 60}, "constant profile changed")
    require(len(linear_code) == 240 and all(len(quadratic[x]) == 6 for x in linear_code),
            "linear provider profile changed")
    return constant_code, constant, linear_code, quadratic


def build_kernels(constant, quadratic):
    h2, h3, h4 = constant[2], constant[3], constant[4]
    s3 = Counter({row: -coefficient for row, coefficient in h3.items()})
    for row, coefficient in h2.items():
        cell = row[0]
        quotient = divide_cell(row, cell)
        for tail, tail_coefficient in quadratic[cell].items():
            add(s3, bytes(sorted(quotient + tail)), coefficient * tail_coefficient)

    s4 = Counter({row: -coefficient for row, coefficient in h4.items()})
    for row, coefficient in product(h2, h2).items():
        add(s4, row, coefficient)
    for row, coefficient in h3.items():
        cell = row[0]
        quotient = divide_cell(row, cell)
        for tail, tail_coefficient in quadratic[cell].items():
            add(s4, bytes(sorted(quotient + tail)), coefficient * tail_coefficient)
    require(all(len(row) == 3 for row in s3), "S3 is not cubic")
    require(all(len(row) == 4 for row in s4), "S4 is not quartic")
    return s3, s4


def matching_edges(sites):
    if not sites:
        return ((),)
    first = sites[0]
    answer = []
    for position in range(1, len(sites)):
        second = sites[position]
        remainder = sites[1:position] + sites[position + 1:]
        for matching in matching_edges(remainder):
            answer.append(tuple(sorted(((first, second),) + matching)))
    return tuple(sorted(answer))


def word_label(code):
    return "".join(map(str, D5.decode_word(code)))


def coordinate_label(identifier):
    i, j, a, b = D5.COORDINATES[identifier]
    return f"x{i}{j}_{a}{b}"


def quadratic_blocks():
    by_terms = defaultdict(list)
    for code in range(3 ** 8):
        terms = []
        for literal in D5.iter_word_terms(code):
            row = bytes(sorted(x for x in literal if D5.IS_OFF_SUPPORT[x]))
            terms.append((row, literal))
        minimum = min(map(lambda item: len(item[0]), terms))
        if minimum != 2 or len(set(D5.decode_word(code))) == 1:
            continue
        minimum_terms = sorted((row, literal) for row, literal in terms if len(row) == 2)
        require(len(minimum_terms) == 3, "minimum-degree-two word lost its N4 triple")
        key = tuple(row for row, _ in minimum_terms)
        support_ids = sorted(set(sum((tuple(literal) for _, literal in minimum_terms), ()))
                         & D5.SUPPORT_IDS)
        # The common two support edges E occur in all three literal matchings.
        common = set(minimum_terms[0][1])
        for _, literal in minimum_terms[1:]:
            common &= set(literal)
        common &= D5.SUPPORT_IDS
        require(len(common) == 2, "minimum-degree-two word has no common two-edge support matching")
        endpoints = set()
        for identifier in common:
            endpoints.update(D5.COORDINATES[identifier][:2])
        outside = tuple(sorted(set(range(8)) - endpoints))
        require(len(outside) == 4, "quadratic word does not leave four sites")
        expected_edge_sets = set(matching_edges(outside))
        actual_edge_sets = set()
        for row, _ in minimum_terms:
            actual_edge_sets.add(tuple(sorted(D5.COORDINATES[x][:2] for x in row)))
        require(actual_edge_sets == expected_edge_sets, "leading triple is not the literal N4 hafnian")
        by_terms[key].append((code, tuple(sorted(common)), outside, tuple(support_ids)))
    require(len(by_terms) == 2206, "quadratic block count changed")
    require(sum(map(len, by_terms.values())) == 2298, "quadratic word count changed")
    require(Counter(map(len, by_terms.values())) == Counter({1: 2114, 2: 92}),
            "quadratic source multiplicity profile changed")
    return by_terms


def packet_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    constant_code, constant, linear_code, quadratic = parse_provider()
    s3, s4 = build_kernels(constant, quadratic)

    kernel_lines = [
        "KRENN_N8_DIRECT_FH_TRANSFER_KERNELS_V1",
        "COORDINATE_ENCODING byte=id in lex (edge i<j, ordered colours a,b); monomial=sorted bytes hex",
        "CONVENTION source generators H_w; y=off-orbit26-support degree; t=on-support degree; total=12",
        "PROVIDER constant_word=12012000 equation=1+h2+h3+h4 linear_equation=x+q2_x",
        "SELECTOR x(m)=smallest_byte_of_m",
        "FORMULA SCALE4 C10=R10-R8*h2+R7*S3+R6*S4+L(R9)",
        "FORMULA S3=-h3+SUM_m2((m2/x(m2))*q2_x(m2))",
        "FORMULA S4=-h4+h2^2+SUM_m3((m3/x(m3))*q2_x(m3))",
        "FORMULA L(c*m)=-c*(m/x(m))*q2_x(m), x(m)=smallest_byte_of_m",
    ]
    for label, polynomial in (("H2", constant[2]), ("H3", constant[3]),
                              ("H4", constant[4]), ("S3", s3), ("S4", s4)):
        kernel_lines.append(f"BEGIN {label} COUNT {len(polynomial)}")
        kernel_lines.extend(f"ROW {row.hex()} {coefficient}"
                            for row, coefficient in sorted(polynomial.items()))
        kernel_lines.append(f"END {label}")
    KERNEL_PACKET.write_text("\n".join(kernel_lines) + "\n", encoding="ascii")

    blocks = quadratic_blocks()
    block_lines = [
        "KRENN_N8_QUADRATIC_PM4_BLOCKS_V1",
        "COORDINATE_ENCODING byte=id in lex (edge i<j, ordered colours a,b); monomial=sorted bytes hex",
        "SCOPE minimum-y-degree-two mixed generators on orbit26 normalized chart",
        f"COUNTS blocks={len(blocks)} words={sum(map(len, blocks.values()))} terms={3*len(blocks)}",
    ]
    for index, (terms, sources) in enumerate(sorted(blocks.items())):
        outside = sources[0][2]
        require(all(source[2] == outside for source in sources), "same triple acquired different outside sites")
        block_lines.append(
            f"BLOCK {index} U={''.join(map(str, outside))} TERMS={','.join(row.hex() for row in terms)} SOURCES={len(sources)}"
        )
        for code, common, _, _ in sources:
            block_lines.append(
                f"SOURCE code={code} word={word_label(code)} E={','.join(map(str, common))} Elabels={','.join(coordinate_label(x) for x in common)}"
            )
    BLOCK_PACKET.write_text("\n".join(block_lines) + "\n", encoding="ascii")

    residual_result = json.loads((HERE / "results_full_direct_residual_through10.json").read_text())
    result = {
        "format": "n8-direct-Fh-factored-y10-transfer-v1",
        "status": "EXACT_FACTORED_CIRCUIT_AND_PM4_CENSUS",
        "constant_provider_code": constant_code,
        "kernel_counts": {"h2": len(constant[2]), "h3": len(constant[3]),
                          "h4": len(constant[4]), "S3": len(s3), "S4": len(s4)},
        "kernel_coefficient_histograms": {
            "S3": dict(sorted(Counter(s3.values()).items())),
            "S4": dict(sorted(Counter(s4.values()).items())),
        },
        "kernel_packet": str(KERNEL_PACKET.relative_to(ROOT)),
        "kernel_packet_sha256": packet_hash(KERNEL_PACKET),
        "quadratic_packet": str(BLOCK_PACKET.relative_to(ROOT)),
        "quadratic_packet_sha256": packet_hash(BLOCK_PACKET),
        "quadratic_census": {
            "source_words": 2298,
            "distinct_three_term_blocks": 2206,
            "distinct_quadratic_rows": 6618,
            "source_multiplicity_histogram": {"1": 2114, "2": 92},
            "block_components": 2206,
        },
        "circuit": "C10=R10-R8*h2+R7*S3+R6*S4+L(R9)",
        "circuit_input_row_counts": {
            f"R{degree}": residual_result["packets"][str(degree)]["rows"]
            for degree in range(6, 11)
        },
        "scale": 4,
        "degree_intersection_guard": {
            "S3_degree": 3,
            "unrelated_attachment_degree": 8,
            "literal_intersection": 0,
            "claim": "the two 66-row counts are not a literal identity",
        },
        "superseded_control": {
            "path": str((HERE / "r6_lex_correction_y10_tail.txt").relative_to(ROOT)),
            "scope": "isolated R6 lex correction tail only; not the full post-correction residual",
        },
        "scope": (
            "exact straight-line representation of the full through-y10 transfer and exact "
            "minimum-degree-two source census; the combined C10 support is not expanded here"
        ),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "provider_sha256": packet_hash(PROVIDER),
        "full_residual_logical_sha256": residual_result["logical_sha256"],
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("factored y10 transfer and PM4 census: PASS")
    print("S3/S4:", len(s3), len(s4))
    print("quadratic blocks/words:", len(blocks), sum(map(len, blocks.values())))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
