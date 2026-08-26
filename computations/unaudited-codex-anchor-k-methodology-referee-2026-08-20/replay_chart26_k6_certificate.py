#!/usr/bin/env python3
"""Independent actual-row replay of the producer zero26 K^6 certificate."""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCER = (
    HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
    / "results_degree5_chart26.json"
)
REFEREE_PATH = HERE / "verify_anchor_k_methodology.py"
EXPECTED_FILE_SHA256 = (
    "9b866673d56f32cd2ed3f916d4f4e4d3a3707c1e74f6061865d3810d88f5adfe"
)
EXPECTED_RESULT_SHA256 = (
    "2c7e35f08ed2932cd99e4df4deb603625f55439281a69ac15759f7ad9b412f5c"
)
EXPECTED_TERMS_SHA256 = (
    "5dd85fba887d51ed2dd2bb07d026bcc9f3d4b8321b7c424595b1bf40d7661cf8"
)
EXPECTED_LEDGER_SHA256 = (
    "a5f84c0965cdbe026eae3ccf3a9dd4e845e90ccbe42f69375172303115c983a0"
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REF = load("anchor_k_referee_base", REFEREE_PATH)
NAME_ID = {
    f"x{u}{v}_{a}{b}": index
    for index, (u, v, a, b) in enumerate(REF.CELLS)
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def exact_counter(counter):
    return Counter({key: value for key, value in counter.items() if value})


def load_artifact():
    raw = PRODUCER.read_bytes()
    require(sha256(raw).hexdigest() == EXPECTED_FILE_SHA256,
            "producer chart26 K6 artifact changed")
    payload = json.loads(raw)
    stored_digest = payload.pop("result_sha256")
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    require(sha256(encoded.encode("ascii")).hexdigest()
            == stored_digest == EXPECTED_RESULT_SHA256,
            "producer internal result digest changed")
    payload["result_sha256"] = stored_digest
    terms = payload["certificate"]["terms"]
    terms_encoded = json.dumps(terms, sort_keys=True, separators=(",", ":"))
    require(sha256(terms_encoded.encode("ascii")).hexdigest()
            == EXPECTED_TERMS_SHA256, "producer certificate payload changed")
    return payload


def decode_certificate(payload):
    answer = []
    for item in payload["certificate"]["terms"]:
        column = (
            tuple(map(int, item["word"])),
            bytes(sorted(NAME_ID[name] for name in item["multiplier"])),
        )
        coefficient = Fraction(item["coefficient_on_orbit_average"])
        transforms = {
            REF.transform_column(column, action)
            for action in range(len(REF.STABILIZER))
        }
        require(len(transforms) == item["column_orbit_size"],
                "stored column orbit size changed")
        require(REF.column_minimum_degree(column)
                == item["minimum_K_degree"],
                "stored column minimum K degree changed")
        answer.append((coefficient, column))
    return tuple(answer)


def filtered_target(cutoff=6):
    groups = []
    for colour in REF.COLORS:
        by_degree = defaultdict(list)
        for row in REF.word_terms((colour,) * REF.N):
            degree = REF.row_degree(row)
            if degree < cutoff:
                by_degree[degree].append(row)
        groups.append(by_degree)
    answer = Counter()
    for degrees in product(range(cutoff), repeat=3):
        if sum(degrees) >= cutoff:
            continue
        for terms in product(*(groups[colour].get(degrees[colour], ())
                               for colour in REF.COLORS)):
            answer[bytes(sorted(b"".join(terms)))] += 1
    return answer


def expand_average(certificate, cutoff=6):
    answer = Counter()
    order = len(REF.STABILIZER)
    for position, (coefficient, column) in enumerate(certificate, 1):
        scalar = coefficient / order
        # Sum over all group elements, including repetitions from a column
        # stabilizer.  Deduplicating transforms while retaining /16 is invalid.
        for action in range(order):
            transformed = REF.transform_column(column, action)
            for row in REF.column_rows(transformed):
                if REF.row_degree(row) < cutoff:
                    answer[row] += scalar
        if position % 500 == 0:
            answer = exact_counter(answer)
            print("actual-row replay", position, "/", len(certificate),
                  "support", len(answer), flush=True)
    return exact_counter(answer)


def audit():
    payload = load_artifact()
    require(payload["chart"] == 26 and payload["legacy_one_based_chart"] == 29,
            "producer artifact is not zero26/legacy29")
    require(payload["stabilizer_order"] == len(REF.STABILIZER) == 16,
            "chart26 stabilizer mismatch")
    require(payload["augmented_lower_system"] == {
        "lower_column_orbits": 4513,
        "lower_row_orbits": 1201,
        "rank_mod_1009": 1239,
        "rows_with_degree5_quotient": 1243,
    }, "producer Schur ledger changed")
    certificate = decode_certificate(payload)
    require(len(certificate) == 2041,
            "chart26 K6 certificate size changed")
    coefficient_histogram = Counter(str(value) for value, _column in certificate)
    require(dict(sorted(coefficient_histogram.items()))
            == payload["certificate"]["coefficient_histogram"],
            "certificate coefficient histogram changed")

    replay = expand_average(certificate)
    target = filtered_target()
    require(replay == target,
            "producer chart26 K6 certificate failed independent actual-row replay")
    degree_histogram = Counter(REF.row_degree(row) for row in target)
    require(degree_histogram == Counter({
        0: 1, 2: 36, 3: 96, 4: 612, 5: 2304,
    }), "chart26 K6 target degree census changed")
    require(set(target.values()) == {1},
            "pure target acquired repeated monomial coefficients")

    negative = next((item for item in certificate if item[0] < 0), None)
    require(negative is not None, "certificate lost its negative term")
    mutated = Counter(replay)
    coefficient, column = negative
    for action in range(len(REF.STABILIZER)):
        transformed = REF.transform_column(column, action)
        for row in REF.column_rows(transformed):
            if REF.row_degree(row) < 6:
                mutated[row] -= Fraction(2 * coefficient,
                                         len(REF.STABILIZER))
    require(exact_counter(mutated) != target,
            "K6 certificate sign mutation did not fire")

    # Orbit-average hostile regression: at least one certificate term has a
    # nontrivial stabilizer.  Summing distinct transforms with coefficient/16
    # underweights it; group averaging and distinct-orbit averaging agree only
    # after using /orbit_size in the latter.
    orbit_histogram = Counter()
    nontrivial = None
    for coefficient, column in certificate:
        orbit_size = len({REF.transform_column(column, action)
                          for action in range(len(REF.STABILIZER))})
        orbit_histogram[orbit_size] += 1
        if orbit_size < len(REF.STABILIZER) and nontrivial is None:
            nontrivial = coefficient, column, orbit_size
    require(nontrivial is not None,
            "certificate has no nontrivially stabilized column regression")
    coefficient, column, orbit_size = nontrivial
    group_average = Counter()
    wrong_deduplicated = Counter()
    distinct = {REF.transform_column(column, action)
                for action in range(len(REF.STABILIZER))}
    for action in range(len(REF.STABILIZER)):
        for row in REF.column_rows(REF.transform_column(column, action)):
            if REF.row_degree(row) < 6:
                group_average[row] += coefficient / len(REF.STABILIZER)
    for transformed in distinct:
        for row in REF.column_rows(transformed):
            if REF.row_degree(row) < 6:
                wrong_deduplicated[row] += coefficient / len(REF.STABILIZER)
    require(exact_counter(group_average) != exact_counter(wrong_deduplicated),
            "deduplicated-/16 orbit-average mutation did not fire")

    # Both fixed methodology regressions are rerun in this certificate audit.
    hostile_mass = REF.quotient_mass_vector(REF.HOSTILE_LOWER_COLUMN, 5)
    require(Counter(hostile_mass.values()) == Counter({2: 28, 1: 12}),
            "set-vs-multiplicity regression changed")
    early_stop = REF.early_stop_regression()

    ledger = {
        "producer_result_sha256": EXPECTED_RESULT_SHA256,
        "producer_file_sha256": EXPECTED_FILE_SHA256,
        "producer_terms_sha256": EXPECTED_TERMS_SHA256,
        "certificate_terms": len(certificate),
        "column_orbit_size_histogram": dict(sorted(orbit_histogram.items())),
        "actual_target_rows": len(target),
        "actual_target_degree_histogram": dict(sorted(degree_histogram.items())),
        "actual_row_exact_replay": True,
        "negative_sign_mutation_fired": True,
        "deduplicated_divide16_mutation_fired": True,
        "set_vs_multiplicity_regression": {"1": 12, "2": 28},
        "early_stop_regression": early_stop,
        "schur_rank_ledger": [1239, 1243],
        "schur_rank_scope": (
            "not independently recomputed; exact actual-row certificate replay "
            "proves membership independently of modular discovery/rank"
        ),
        "conclusion": "zero26 H0*H1*H2 belongs to I_mix + K_anchor^6 over Q",
        "full_membership_claimed": False,
        "remaining_anchor_K_degrees": list(range(6, 13)),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart26 K6 independent replay ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    (HERE / "chart26_k6_replay.json").write_text(json.dumps(
        {"ledger": ledger, "sha256": digest}, indent=2, sort_keys=True
    ) + "\n")
    print("chart26 K6 independent actual-row replay: PASS")
    print("certificate/target:", ledger["certificate_terms"],
          ledger["actual_target_rows"])
    print("orbit sizes:", ledger["column_orbit_size_histogram"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
