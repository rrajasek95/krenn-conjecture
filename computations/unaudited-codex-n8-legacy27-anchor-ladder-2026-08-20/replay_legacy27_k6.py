#!/usr/bin/env python3
"""Independent three-mode replay of the frozen legacy27 K^6 certificate."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_probe_replay", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
RESULT = HERE / "results_k6_exact.json"
EXPECTED_RESULT_SHA256 = (
    "1dc739a4ef4ef5c2e0e6d89d3621d15e0c547a0eaf4802bcc1f87b800e6a3097"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def expand(certificate, normalized=True):
    answer = Counter()
    denominator = len(PROBE.STABILIZER) if normalized else 1
    for coefficient, column in certificate:
        for action in range(len(PROBE.STABILIZER)):
            transformed = PROBE.transform_column(column, action)
            for row in BASE.column_rows(transformed):
                if BASE.row_degree(row, PROBE.ANCHORS) < 6:
                    answer[row] += coefficient / denominator
    return Counter({row: value for row, value in answer.items() if value})


def main():
    payload = json.loads(RESULT.read_text())
    stored = payload.pop("result_sha256")
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    require(stored == EXPECTED_RESULT_SHA256,
            "stored K6 result digest changed")
    require(sha256(encoded.encode("ascii")).hexdigest() == stored,
            "K6 result content no longer matches its digest")
    require(payload["zero_based_chart"] == 30
            and payload["legacy_one_based_chart"] == 27,
            "chart numbering changed")
    require(payload["certificate"]["total_orbit_average_terms"] == 4293,
            "K6 certificate term count changed")
    name_to_id = {
        BASE.cell_name(cell): index for index, cell in enumerate(BASE.CELLS)
    }
    certificate = []
    for item in payload["certificate"]["terms"]:
        column = (
            tuple(map(int, item["word"])),
            bytes(sorted(name_to_id[name] for name in item["multiplier"])),
        )
        require(PROBE.canonical_column(column) == column,
                "certificate column is not its canonical orbit representative")
        require(len(PROBE.column_orbit(column)) == item["column_orbit_size"],
                "column orbit-size ledger changed")
        require(PROBE.column_minimum_degree(column)
                == item["minimum_K_degree"],
                "column K-degree ledger changed")
        certificate.append((
            Fraction(item["coefficient_on_six_transform_average"]), column
        ))
    certificate = tuple(certificate)
    actual = expand(certificate)
    expected = Counter({row: Fraction(value) for row, value in
                        BASE.filtered_target(PROBE.MATCHINGS, 6).items()})
    require(actual == expected, "independent labelled K6 replay failed")
    require(expand(certificate, normalized=False) != expected,
            "orbit normalization must-fire control did not fire")
    require(expand(certificate[1:]) != expected,
            "term-deletion must-fire control did not fire")
    core = {
        "chart": 30,
        "legacy": 27,
        "stabilizer": len(PROBE.STABILIZER),
        "terms": len(certificate),
        "labelled_rows": len(expected),
        "exact_replay": True,
        "multiplicity_control": True,
        "deletion_control": True,
        "source_result_sha256": stored,
    }
    digest = sha256(json.dumps(
        core, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    print(json.dumps({**core, "replay_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
