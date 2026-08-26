#!/usr/bin/env python3
"""Literal lower-kernel mutation from the two monic constant providers.

The normalized mixed source has exactly two generators with constant term 1,
codes 3780 and 5108.  Their difference begins in y degree two.  Multiply the
difference by a y6 monomial m (implicit t^2), cancel its y8 layer with the
frozen code-3780 constant provider and its y9 layer with the frozen monic
linear providers, and read the resulting y10 coefficient.  Any nonzero value
at the lex C10 row is a literal proof that the deterministic coefficient is
not invariant under lower contraction-kernel choices.
"""

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIRST_PATH = ROOT / "computations/verify_n8_chart26_first_homogeneous_spair.py"
PROVIDER = HERE / "direct_fh_unique_min_provider.txt"
RESULTS = HERE / "results_c10_constant_provider_kernel.json"
TARGET = bytes.fromhex("0111202020494f4f50f8")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("c10_constant_kernel", FIRST_PATH)
FIRST = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load normalized source")
spec.loader.exec_module(FIRST)


def add(polynomial, row, coefficient):
    value = polynomial[row] + coefficient
    if value:
        polynomial[row] = value
    else:
        del polynomial[row]


def multiply_monomial(polynomial, multiplier, scalar=1):
    answer = Counter()
    for row, coefficient in polynomial.items():
        add(answer, bytes(sorted(row + multiplier)), scalar * coefficient)
    return answer


def product(left, right):
    answer = Counter()
    for left_row, left_coefficient in left.items():
        for right_row, right_coefficient in right.items():
            add(answer, bytes(sorted(left_row + right_row)),
                left_coefficient * right_coefficient)
    return answer


def parse_linear_provider():
    linear_code = {}
    quadratic = defaultdict(Counter)
    for line in PROVIDER.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "LINEAR":
            linear_code[int(fields[1])] = int(fields[2])
        elif fields[0] == "L2":
            quadratic[int(fields[1])][bytes.fromhex(fields[2])] += int(fields[3])
    require(len(linear_code) == 240
            and all(len(quadratic[cell]) == 6 for cell in linear_code),
            "linear provider packet changed")
    return linear_code, quadratic


def unique_divisors(row, degree):
    return sorted({bytes(row[index] for index in positions)
                   for positions in combinations(range(len(row)), degree)})


def main():
    originals, _lead_to_code = FIRST.original_basis()
    constant_codes = sorted(code for code, polynomial in originals.items()
                            if polynomial.get(b"") == 1)
    require(constant_codes == [3780, 5108],
            "constant-provider word census changed")
    base = originals[3780]
    alternative = originals[5108]
    delta = Counter(alternative)
    delta.subtract(base)
    delta = Counter({row: coefficient for row, coefficient in delta.items()
                     if coefficient})
    require(b"" not in delta and not any(len(row) == 1 for row in delta),
            "constant-provider difference retained y0/y1")
    delta_by_degree = {
        degree: Counter({row: coefficient for row, coefficient in delta.items()
                         if len(row) == degree})
        for degree in (2, 3, 4)
    }
    require(all(delta_by_degree.values()),
            "constant-provider difference lost a transfer layer")
    h2 = Counter({row: coefficient for row, coefficient in base.items()
                  if len(row) == 2})
    linear_code, quadratic = parse_linear_provider()

    records = []
    witnesses = []
    for multiplier in unique_divisors(TARGET, 6):
        d8 = multiply_monomial(delta_by_degree[2], multiplier)
        d9 = multiply_monomial(delta_by_degree[3], multiplier)
        d10 = multiply_monomial(delta_by_degree[4], multiplier)

        terminal = Counter(d10)
        for row, coefficient in product(d8, h2).items():
            add(terminal, row, -coefficient)
        linear_columns = Counter()
        for row, coefficient in d9.items():
            cell = row[0]
            require(cell in linear_code, "d9 row selected a support cell")
            remainder = row[1:]
            linear_columns[(linear_code[cell], remainder)] -= coefficient
            for tail, tail_coefficient in quadratic[cell].items():
                add(terminal, bytes(sorted(remainder + tail)),
                    -coefficient * tail_coefficient)
        terminal = Counter({row: coefficient for row, coefficient in terminal.items()
                            if coefficient})
        target_coefficient = terminal.get(TARGET, 0)
        record = {
            "multiplier_y6": multiplier.hex(),
            "d8_rows": len(d8),
            "d9_rows": len(d9),
            "constant_correction_columns": len(d8),
            "linear_correction_columns": len(linear_columns),
            "terminal_y10_rows": len(terminal),
            "target_coefficient": target_coefficient,
        }
        records.append(record)
        if target_coefficient:
            # Verify the literal column combination directly through y10.
            columns = Counter({(5108, multiplier): 1, (3780, multiplier): -1})
            for row, coefficient in d8.items():
                columns[(3780, row)] -= coefficient
            columns.update(linear_columns)
            columns = Counter({column: coefficient for column, coefficient
                               in columns.items() if coefficient})
            image = Counter()
            for (code, source_multiplier), scalar in columns.items():
                for term, coefficient in originals[code].items():
                    output = bytes(sorted(source_multiplier + term))
                    if len(output) <= 10:
                        add(image, output, scalar * coefficient)
            lower = {row: coefficient for row, coefficient in image.items()
                     if len(row) <= 9 and coefficient}
            degree10 = Counter({row: coefficient for row, coefficient in image.items()
                                if len(row) == 10 and coefficient})
            require(not lower, "literal provider mutation is not a lower kernel")
            require(degree10 == terminal,
                    "straight-line transfer disagrees with literal column replay")
            require(degree10[TARGET] == target_coefficient,
                    "literal replay changed target coefficient")
            witnesses.append({
                **record,
                "source_columns": [
                    {
                        "code": code,
                        "word": list(FIRST.D5.decode_word(code)),
                        "multiplier_y": source_multiplier.hex(),
                        "multiplier_t_exponent": 8 - len(source_multiplier),
                        "coefficient": coefficient,
                    }
                    for (code, source_multiplier), coefficient
                    in sorted(columns.items())
                ],
                "source_column_count": len(columns),
                "literal_lower_rows_after_collection": 0,
                "literal_y10_support": len(degree10),
                "literal_y10_sha256": sha256(b"".join(
                    row + str(coefficient).encode("ascii") + b"\n"
                    for row, coefficient in sorted(degree10.items())
                )).hexdigest(),
            })

    require(witnesses, "constant-provider kernel did not change lex C10")
    witness = min(witnesses, key=lambda item: (
        item["source_column_count"], item["multiplier_y6"]
    ))
    result = {
        "format": "n8-orbit26-c10-constant-provider-kernel-v1",
        "status": "EXACT_LITERAL_LOWER_KERNEL_CHANGES_LEX_C10",
        "target_y10": TARGET.hex(),
        "constant_provider_codes": constant_codes,
        "constant_provider_words": [
            list(FIRST.D5.decode_word(code)) for code in constant_codes
        ],
        "delta_degree_histogram": dict(sorted(Counter(
            map(len, delta)).items()
        )),
        "tested_y6_divisors": len(records),
        "nonzero_target_witnesses": len(witnesses),
        "target_coefficient_histogram": dict(sorted(Counter(
            record["target_coefficient"] for record in records
        ).items())),
        "lex_smallest_minimal_column_witness": witness,
        "theorem": (
            "The displayed exact source-column combination has zero collected "
            "output in every encoded y degree at most nine and nonzero coefficient "
            "at the lex y10*t2 row. It is therefore a literal vector in the lower "
            "contraction kernel on which the relative C10 coordinate is nonzero. "
            "Consequently the deterministic coefficient -4 is not invariant under "
            "all lower-degree contraction choices."
        ),
        "scope": (
            "fixed normalized orbit26 chart and homogeneous total degree12; this "
            "falsifies coefficient invariance but does not show that one kernel "
            "choice cancels the entire y10 residual or proves ideal membership"
        ),
        "source_sha256": {
            str(FIRST_PATH.relative_to(ROOT)):
                sha256(FIRST_PATH.read_bytes()).hexdigest(),
            str(PROVIDER.relative_to(ROOT)):
                sha256(PROVIDER.read_bytes()).hexdigest(),
        },
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("C10 constant-provider lower-kernel mutation: PASS")
    print("tested/nonzero/minimal columns/target coefficient:", len(records),
          len(witnesses), witness["source_column_count"],
          witness["target_coefficient"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
