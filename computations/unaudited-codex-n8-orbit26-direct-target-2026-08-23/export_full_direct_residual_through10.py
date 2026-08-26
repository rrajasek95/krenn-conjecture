#!/usr/bin/env python3
"""Replay the frozen degree-five certificate through normalized y-degree 10.

The earlier boundary checker intentionally stopped at degree six.  This
exporter retains the pre-existing degree-seven through degree-ten residuals,
which are required before a positive triangular continuation can be claimed.
All coefficients are multiplied by four, the exact common denominator of the
frozen certificate.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations" / "verify_n8_normalized_critical_contraction.py"
RESULTS = HERE / "results_full_direct_residual_through10.json"
PACKETS = {
    degree: HERE / f"direct_fh_original_y{degree}_residual.txt"
    for degree in range(6, 11)
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("n8_normalized", SOURCE)
NORM = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load normalized source")
spec.loader.exec_module(NORM)
D5 = NORM.D5


def normalized_row(row):
    return bytes(sorted(value for value in row if D5.IS_OFF_SUPPORT[value]))


def normalized_generator(code):
    return Counter(normalized_row(term) for term in D5.iter_word_terms(code))


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


def main():
    maximum_degree = 10
    cache = {}

    def generator(code):
        if code not in cache:
            cache[code] = normalized_generator(code)
        return cache[code]

    pure = tuple(generator(D5.word_code((colour,) * 8)) for colour in range(3))
    target = truncated_product(pure, maximum_degree)
    certificate = json.loads(D5.CERTIFICATE_PATH.read_text())
    image = {}
    literal_columns = 0
    literal_outputs = 0
    for item in certificate["solution"]:
        code = D5.word_code(tuple(item["word"]))
        multiplier = bytes(
            D5.COORDINATE_ID[tuple(variable)] for variable in item["multiplier"]
        )
        scalar = Fraction(item["numerator"], item["denominator"])
        for actual_code, actual_multiplier in D5.column_orbit((code, multiplier)):
            literal_columns += 1
            normalized_multiplier = normalized_row(actual_multiplier)
            for term, coefficient in generator(actual_code).items():
                row = bytes(sorted(normalized_multiplier + term))
                if len(row) > maximum_degree:
                    continue
                literal_outputs += 1
                value = image.get(row, Fraction()) + scalar * coefficient
                if value:
                    image[row] = value
                else:
                    image.pop(row, None)

    residual = {}
    for row in set(target) | set(image):
        value = Fraction(target.get(row, 0)) - image.get(row, Fraction())
        if value:
            residual[row] = value
    require(not any(len(row) <= 5 for row in residual),
            "frozen certificate left a residual below degree six")

    packet_records = {}
    for degree, path in PACKETS.items():
        part = sorted(
            (row, coefficient) for row, coefficient in residual.items()
            if len(row) == degree
        )
        magic = (
            "KRENN_N8_DIRECT_FH_Y6_V1" if degree == 6
            else f"KRENN_N8_DIRECT_FH_ORIGINAL_Y{degree}_V1"
        )
        lines = [f"{magic} SCALE 4 COUNT {len(part)}"]
        coefficient_histogram = Counter()
        for row, coefficient in part:
            scaled = 4 * coefficient
            require(scaled.denominator == 1,
                    "certificate denominator does not divide four")
            coefficient_histogram[scaled.numerator] += 1
            lines.append(f"ROW {row.hex()} {scaled.numerator}")
        text = "\n".join(lines) + "\n"
        path.write_text(text, encoding="ascii")
        packet_records[str(degree)] = {
            "rows": len(part),
            "scaled_coefficient_histogram": dict(sorted(coefficient_histogram.items())),
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(text.encode("ascii")).hexdigest(),
        }

    require(packet_records["6"]["sha256"]
            == sha256((HERE / "direct_fh_y6_residual.txt").read_bytes()).hexdigest(),
            "independent through-10 replay does not reproduce the y6 packet")
    result = {
        "format": "n8-direct-Fh-original-residual-through10-v1",
        "status": "EXACT_Q_REPLAY",
        "target": "F^h=H_0^h*H_1^h*H_2^h",
        "total_homogeneous_degree": 12,
        "certificate_orbit_columns": len(certificate["solution"]),
        "expanded_literal_columns": literal_columns,
        "streamed_literal_outputs_through_y10": literal_outputs,
        "target_terms_through_y10": len(target),
        "image_terms_through_y10": len(image),
        "residual_terms_through_y10": len(residual),
        "packets": packet_records,
        "scope": (
            "complete original residual through y-degree10; no correction "
            "columns have yet been applied in this artifact"
        ),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "certificate_sha256": sha256(D5.CERTIFICATE_PATH.read_bytes()).hexdigest(),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("full normalized direct residual through y10: PASS")
    print("degree counts:", {degree: item["rows"] for degree, item in packet_records.items()})
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
