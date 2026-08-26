#!/usr/bin/env python3
"""Referee the full D12 dual against the 90-column lower-kernel witness.

The older witness changes the coefficient of the selected y10*t2 row by
+1.  It is nevertheless a literal homogeneous degree-12 source image.  A
full degree-12 ideal functional must therefore annihilate it.  This replay
keeps all y10/y11/y12 terms and exhibits the cancellation explicitly.  The
cancellation is also the guard: it does not imply invariance after projecting
the source image to the y10 C10 layer.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_PATH = HERE / "audit_degree12_full_dual.py"
FULL_RESULT = HERE / "results_degree12_full_dual_fixed_c10.json"
EXPORT_PATH = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
    / "export_full_direct_residual_through10.py"
)
WITNESS = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
    / "results_c10_constant_provider_kernel.json"
)
RESULTS = HERE / "results_lower_kernel_dual_invariance.json"
EXPECTED_FULL_LOGICAL = (
    "cde136aef242841bc78bc9b7da8e56323ab0b273bb637a30253902e9b2729aed"
)
EXPECTED_WITNESS_LOGICAL = (
    "edc37a9c5c1785db383cc518fa151912ad1589e70d929b9e71915153fb3db80e"
)
EXPECTED_WITNESS_SHA256 = (
    "cb1a569493022716d118e8796f8441f902ba693ed7699ccea7a3e51ca6ceb6f0"
)
EXPECTED_LOGICAL_SHA256 = (
    "87e2d04986ec22147d39b5d5783c82d53a3eedcb627ef92d7a13d553e21037dc"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


FULL = load(FULL_PATH, "n8_degree12_lower_kernel_referee")
EXPORT = load(EXPORT_PATH, "n8_degree12_direct_fh_referee")


def add(polynomial, row, coefficient):
    value = polynomial[row] + coefficient
    if value:
        polynomial[row] = value
    else:
        del polynomial[row]


def main():
    full_result = json.loads(FULL_RESULT.read_text())
    witness_result = json.loads(WITNESS.read_text())
    require(full_result["logical_sha256"] == EXPECTED_FULL_LOGICAL,
            "full degree-12 functional authority changed")
    require(witness_result["logical_sha256"] == EXPECTED_WITNESS_LOGICAL,
            "lower-kernel witness logical authority changed")
    require(sha256(WITNESS.read_bytes()).hexdigest() == EXPECTED_WITNESS_SHA256,
            "lower-kernel witness file changed")

    functional = {
        bytes.fromhex(row): Fraction(numerator, denominator)
        for row, numerator, denominator in full_result["functional_rows"]
    }
    require(len(functional) == 20
            and Counter(map(len, functional)) == {10: 1, 11: 3, 12: 16},
            "full functional support profile changed")

    helpers = FULL.D12.D11_HELPERS.D10_HELPERS
    base = helpers.load(helpers.D8_BASE_PATH, "n8_lower_kernel_referee_base")
    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    target = base.TARGET
    witness = witness_result["lex_smallest_minimal_column_witness"]
    columns = witness["source_columns"]
    require(len(columns) == witness["source_column_count"] == 90,
            "90-column witness census changed")

    image = Counter()
    column_pairings = []
    for record in columns:
        code = int(record["code"])
        multiplier = bytes.fromhex(record["multiplier_y"])
        multiplier_t = int(record["multiplier_t_exponent"])
        scalar = int(record["coefficient"])
        require(code in originals and len(multiplier) + multiplier_t == 8,
                "a witness column left homogeneous total degree 12")
        pairing = Fraction(0)
        for term, coefficient in originals[code].items():
            row = bytes(sorted(term + multiplier))
            emitted = scalar * coefficient
            add(image, row, emitted)
            pairing += functional.get(row, 0) * emitted
        column_pairings.append(pairing)

    lower = {row: coefficient for row, coefficient in image.items()
             if len(row) <= 9}
    degree10 = Counter({row: coefficient for row, coefficient in image.items()
                        if len(row) == 10})
    degree10_sha = sha256(b"".join(
        row + str(coefficient).encode("ascii") + b"\n"
        for row, coefficient in sorted(degree10.items())
    )).hexdigest()
    require(not lower, "the witness acquired a nonzero output below y10")
    require(len(degree10) == witness["literal_y10_support"] == 714
            and degree10_sha == witness["literal_y10_sha256"],
            "full replay disagrees with the frozen y10 witness")
    require(degree10[target] == 1,
            "the lower-kernel witness lost its lex coefficient +1")

    pairing_by_y_degree = defaultdict(Fraction)
    support_by_y_degree = Counter()
    for row, coefficient in image.items():
        support_by_y_degree[len(row)] += 1
        pairing_by_y_degree[len(row)] += functional.get(row, 0) * coefficient
    total_pairing = sum(pairing_by_y_degree.values(), Fraction(0))
    require(total_pairing == sum(column_pairings, Fraction(0)),
            "collected-image and source-column pairings disagree")
    require(all(value == 0 for value in column_pairings),
            "one literal degree-12 source column escapes the full ideal dual")
    require(pairing_by_y_degree[10] == 1 and total_pairing == 0,
            "higher filtration failed to cancel the changed lex coefficient")

    # Independent direct target replay.  This constructs the three normalized
    # pure generators and their full homogeneous product rather than using the
    # factored C10 transfer circuit.
    normalized_cache = {}
    def normalized_generator(code):
        if code not in normalized_cache:
            normalized_cache[code] = EXPORT.normalized_generator(code)
        return normalized_cache[code]
    pure_generators = [
        normalized_generator(EXPORT.D5.word_code((colour,) * 8))
        for colour in range(3)
    ]
    direct_fh = EXPORT.truncated_product(pure_generators, 12)
    direct_fh_hits = {
        row: direct_fh[row] for row in functional if direct_fh.get(row)
    }
    direct_fh_pairing = sum((
        functional[row] * coefficient
        for row, coefficient in direct_fh_hits.items()
    ), Fraction(0))
    require(len(direct_fh) == 1_157_625
            and not direct_fh_hits and direct_fh_pairing == 0,
            "direct normalized Fh pairing changed")
    fixed_c10_pairing = Fraction(
        full_result["fixed_c10_evaluation"]["pairing"]
    )
    require(fixed_c10_pairing == -4,
            "fixed deterministic C10 pairing changed")
    omitted_tail_pairing = direct_fh_pairing - fixed_c10_pairing
    require(omitted_tail_pairing == 4,
            "omitted residual tail no longer cancels fixed C10")

    payload = {
        "format": "n8-degree12-lower-kernel-dual-invariance-v1",
        "status": "EXACT_FULL_IMAGE_CANCELLATION_NO_TRUNCATED_INVARIANCE",
        "theorem": (
            "For the frozen normalized chart, lambda annihilates the complete "
            "homogeneous degree-12 source image. The 90-column witness confirms "
            "this exactly: its y10 pairing +1 is canceled by y11 pairing -1. "
            "However C10 retains only the y10 transfer layer, so changing the "
            "lower right inverse changes C10 by pi10(M12(k)), not by the full "
            "source image M12(k). Lambda need not annihilate that projection."
        ),
        "implication": (
            "lambda(M12(k))=0, but lambda(pi10(M12(k))) can be nonzero; the "
            "displayed witness gives 1. Therefore the fixed-C10 nonmembership "
            "certificate does not descend to a lower-right-inverse-invariant "
            "C10 class or to the full F^h class."
        ),
        "full_functional_logical_sha256": full_result["logical_sha256"],
        "lower_kernel_witness_logical_sha256": witness_result["logical_sha256"],
        "lower_kernel_witness_file_sha256": EXPECTED_WITNESS_SHA256,
        "witness_source_columns": len(columns),
        "witness_nonzero_output_support_by_y_degree": {
            str(degree): support_by_y_degree[degree]
            for degree in sorted(support_by_y_degree)
        },
        "witness_lambda_pairing_by_y_degree": {
            str(degree): [value.numerator, value.denominator]
            for degree, value in sorted(pairing_by_y_degree.items())
            if value
        },
        "witness_target_y10_coefficient": degree10[target],
        "witness_full_lambda_pairing": [
            total_pairing.numerator, total_pairing.denominator
        ],
        "witness_individual_source_columns_nonzero_pairings": sum(
            value != 0 for value in column_pairings
        ),
        "fixed_c10_lambda_pairing": int(fixed_c10_pairing),
        "direct_normalized_fh": {
            "terms": len(direct_fh),
            "functional_support_hits": len(direct_fh_hits),
            "lambda_pairing": [
                direct_fh_pairing.numerator, direct_fh_pairing.denominator
            ],
            "omitted_y11_y12_residual_tail_pairing": [
                omitted_tail_pairing.numerator, omitted_tail_pairing.denominator
            ],
            "conclusion": (
                "fixed C10 is not congruent to full F^h under this transfer; "
                "the omitted higher residual tail cancels its pairing"
            ),
        },
        "direct_fh_exporter_sha256": sha256(EXPORT_PATH.read_bytes()).hexdigest(),
        "scope": (
            "exact full-image annihilation and a decisive truncation guard in "
            "the frozen normalized localized chart; fixed deterministic C10 "
            "nonmembership remains, but no right-inverse, F^h, t-saturation, "
            "degree-13, or global unlocalized source inference"
        ),
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "lower-kernel invariance ledger changed")
    RESULTS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("degree-12 lower-kernel/Fh scope referee: PASS")
    print("pairing by y degree:", {
        degree: str(value) for degree, value in sorted(pairing_by_y_degree.items())
        if value
    })
    print("full pairing:", total_pairing)
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
