#!/usr/bin/env python3
"""Audit the source-labelled linear-contraction closure of the 52-row S3 class."""

from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNELS = HERE / "direct_fh_transfer_kernels.txt"
PROVIDER = HERE / "direct_fh_unique_min_provider.txt"
PACKET = HERE / "s3_source_closure.txt"
RESULTS = HERE / "results_s3_source_closure.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parse_kernels():
    answer = defaultdict(dict)
    active = None
    for line in KERNELS.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[0] == "BEGIN":
            active = fields[1]
        elif fields[0] == "END":
            active = None
        elif fields[0] == "ROW" and active:
            answer[active][bytes.fromhex(fields[1])] = int(fields[2])
    return answer


def parse_provider():
    codes = {}
    quadratic = defaultdict(list)
    for line in PROVIDER.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[0] == "LINEAR":
            codes[int(fields[1])] = (int(fields[2]), fields[3])
        elif fields[0] == "L2":
            quadratic[int(fields[1])].append((bytes.fromhex(fields[2]), int(fields[3])))
    return codes, quadratic


def main():
    kernels = parse_kernels()
    codes, quadratic = parse_provider()
    h2, h3, s3 = map(kernels.__getitem__, ("H2", "H3", "S3"))
    literal_s3 = set(s3) & set(h3)
    residual52 = set(s3) - set(h3)
    require(len(literal_s3) == 14 and len(residual52) == 52, "14+52 partition changed")
    require(Counter(s3[row] for row in literal_s3) == Counter({-1: 13, 1: 1}),
            "literal S3 coefficient profile changed")
    require(Counter(s3[row] for row in residual52) == Counter({1: 52}),
            "52-row coefficient profile changed")

    occurrences = defaultdict(list)
    columns = []
    for h2_row in sorted(h2):
        cell = h2_row[0]
        multiplier = h2_row[1:]
        outputs = []
        for tail, coefficient in quadratic[cell]:
            require(coefficient == 1, "linear quadratic coefficient changed")
            output = bytes(sorted(multiplier + tail))
            occurrences[output].append((h2_row, cell, multiplier, tail))
            outputs.append(output)
        columns.append((h2_row, cell, multiplier, outputs))

    require(Counter(map(len, occurrences.values())) == Counter({1: 70, 2: 1}),
            "linear-tail collision profile changed")
    collision_row, collision_sources = next((row, sources) for row, sources in occurrences.items()
                                              if len(sources) == 2)
    require(collision_row.hex() == "05c0d5", "lex/source collision row changed")
    require(set(source[0].hex() for source in collision_sources) == {"30c0", "72d5"},
            "collision source labels changed")

    lines = [
        "KRENN_N8_DIRECT_FH_S3_SOURCE_CLOSURE_V1",
        "FORMULA S3=-h3+SUM_m2((m2/x(m2))*q2_x(m2)) SELECTOR smallest_byte",
        "PARTITION literal_compatible=14 residual_nonliteral=52",
    ]
    mixed_columns = 0
    closed_columns = 0
    category_occurrences = Counter()
    for h2_row, cell, multiplier, outputs in columns:
        categories = []
        for output in outputs:
            if output in residual52:
                category = "R52"
            elif output in literal_s3:
                category = "L14"
            elif output in h3:
                category = "H3_CANCELLED"
            else:
                raise RuntimeError("linear tail escaped S3/h3 union")
            categories.append(category)
            category_occurrences[category] += 1
        if all(category == "R52" for category in categories):
            closed_columns += 1
        else:
            mixed_columns += 1
        code, word = codes[cell]
        lines.append(
            f"COLUMN h2={h2_row.hex()} x={cell} multiplier={multiplier.hex()} "
            f"linear_code={code} linear_word={word} PROFILE="
            + ",".join(f"{category}:{output.hex()}" for category, output in zip(categories, outputs))
        )
    lines.append(
        "COLLISION row=05c0d5 sources="
        + ",".join(f"h2={source[0].hex()}/x={source[1]}/mult={source[2].hex()}/tail={source[3].hex()}"
                   for source in collision_sources)
    )
    for row in sorted(literal_s3):
        lines.append(f"LITERAL14 {row.hex()} {s3[row]}")
    for row in sorted(residual52):
        lines.append(f"RESIDUAL52 {row.hex()} {s3[row]}")
    PACKET.write_text("\n".join(lines) + "\n", encoding="ascii")

    require((closed_columns, mixed_columns) == (5, 7), "column closure census changed")
    require(category_occurrences == Counter({"R52": 52, "H3_CANCELLED": 18, "L14": 2}),
            "tail category occurrence census changed")
    result = {
        "format": "n8-direct-Fh-S3-source-closure-v1",
        "status": "EXACT_NOT_CLOSED",
        "partition": {
            "literal_compatible_rows": 14,
            "matching_endpoint_colour_incompatible_rows": 14,
            "nonmatching_collision_rows": 38,
            "nonliteral_residual_rows": 52,
        },
        "source_columns": 12,
        "columns_entirely_in_residual52": closed_columns,
        "columns_meeting_literal_h3_rows": mixed_columns,
        "linear_tail_occurrences": dict(sorted(category_occurrences.items())),
        "tail_support_multiplicity_histogram": dict(sorted(Counter(map(len, occurrences.values())).items())),
        "smallest_collision": {
            "row": collision_row.hex(),
            "source_h2_rows": sorted(source[0].hex() for source in collision_sources),
            "meaning": "two distinct source-labelled linear contractions meet at one literal h3 row",
        },
        "theorem": (
            "removing the 14 literal compatible S3 rows does not leave a class closed under "
            "the twelve relevant chart26 linear contractions: seven columns also output literal "
            "h3 rows; five columns stay wholly inside the 52 rows"
        ),
        "packet": str(PACKET.relative_to(ROOT)),
        "packet_sha256": sha256(PACKET.read_bytes()).hexdigest(),
        "kernel_packet_sha256": sha256(KERNELS.read_bytes()).hexdigest(),
        "provider_sha256": sha256(PROVIDER.read_bytes()).hexdigest(),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("S3 source closure audit: PASS (NOT_CLOSED)")
    print("closed/mixed columns:", closed_columns, mixed_columns)
    print("collision:", collision_row.hex(), sorted(source[0].hex() for source in collision_sources))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
