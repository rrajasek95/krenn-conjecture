#!/usr/bin/env python3
"""Close every first mixed-10 E14 tail by one of two two-row units.

The preceding second-tail census left seven anchor-contained mixed-10
records after looking only at the frozen target/zero pair.  This checker
uses the complete G11 output, not a support or rank argument.  In every
one-cell mixed-10 extension either the original zero row still has the
target tail, or a second literal zero row has its negative.

Writing T for the complete coefficient of G11[111111], the identities are

    G11[zero_i] = T,                                      (120 records)
    G11[110011] = -T,  i=1,                              (6 records)
    G11[110101] = -T,  i=2.                              (9 records)

Consequently the ordinary source generators give respectively
F_zero-F_target=1 or -F_companion-F_target=1.  No localization, rank
landing, or choice of endpoint coefficients is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
E14_PATH = "computations/verify_h3_c6_e14_minimal_enlargement_unit.py"
CLASSIFIER_PATH = (
    "computations/verify_h3_c6_e14_second_tail_extension_classification.py"
)
PINS = {
    E14_PATH:
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "notes/h3-c6-e14-minimal-enlargement-unit.md":
        "552adf8a24410d4b8a09e61809c9a40c40274ad9c49a7ffe01b7ceb0d5ea22a7",
    CLASSIFIER_PATH:
        "68dfff0e3dd85ce8e705b15bbfd7fdf91a9a052e21fe1f88bdd21cc002443656",
    "notes/h3-c6-e14-second-tail-extension-classification.md":
        "790accdf1b1c3441a8038cc5c90fb073295bc68c79e52547cbabb6ee7a99755b",
}
EXPECTED_LEDGER_SHA256 = (
    "bca83e2c4ae4acc529a0a8d18e989576ea31b56cf066c36e8a2efc5a8aa23476"
)
X = "mixed10_companion_x"
TARGET_WORD = (1, 1, 1, 1, 1, 1)
COMPANION_WORD = {
    1: (1, 1, 0, 0, 1, 1),
    2: (1, 1, 0, 1, 0, 1),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def negate(row):
    return {
        endpoint: {
            monomial: -coefficient
            for monomial, coefficient in polynomial.items()
        }
        for endpoint, polynomial in row.items()
    }


def audit():
    pin_dependencies()
    e14 = load(E14_PATH, "c6_e14_mixed10_companion")
    b4 = e14.load(e14.B4_PATH, "c6_e14_mixed10_companion_b4")
    classifier = load(CLASSIFIER_PATH, "c6_e14_second_tail_classifier")
    classification, classification_digest = classifier.audit()
    require(classification_digest == classifier.EXPECTED_LEDGER_SHA256,
            "the pinned second-tail classification did not replay")

    records = []
    route_counts = Counter()
    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            q_cells, _added, _selected = e14.q_inventory(
                b4, first_index, second_index
            )
            for left in range(6):
                for right in range(left + 1, 6):
                    physical = (left, right)
                    require((1, 0) not in q_cells.get(physical, {}),
                            "the first mixed-10 universe acquired a base cell")
                    enlarged = {edge: dict(cells)
                                for edge, cells in q_cells.items()}
                    enlarged.setdefault(physical, {})[(1, 0)] = {
                        (X,): Q(1)
                    }
                    rows = e14.response_11(b4, enlarged)
                    target = rows[TARGET_WORD]
                    zero = rows[e14.ZERO_WORD[first_index]]
                    if zero == target:
                        route = "original_parallel_unit"
                        unit_identity = "F_zero-F_target=1"
                        witness_word = e14.ZERO_WORD[first_index]
                    else:
                        require(first_index in COMPANION_WORD,
                                "a third-tail mixed-10 extension lost the unit")
                        witness_word = COMPANION_WORD[first_index]
                        require(rows[witness_word] == negate(target),
                                "the alternate complete row lost its negative tail")
                        route = "companion_antiparallel_unit"
                        unit_identity = "-F_companion-F_target=1"
                    route_counts[route] += 1
                    records.append({
                        "X1_tail_index": first_index,
                        "X2_tail_index": second_index,
                        "physical_edge": list(physical),
                        "route": route,
                        "witness_word": list(witness_word),
                        "ordinary_source_identity": unit_identity,
                    })

    require(len(records) == 135,
            f"the first mixed-10 universe changed: {len(records)}")
    require(route_counts == Counter({
        "original_parallel_unit": 120,
        "companion_antiparallel_unit": 15,
    }), f"the mixed-10 unit split changed: {route_counts}")

    companion_records = [record for record in records
                         if record["route"] ==
                         "companion_antiparallel_unit"]
    companion_words = Counter(tuple(record["witness_word"])
                              for record in companion_records)
    require(companion_words == Counter({
        COMPANION_WORD[1]: 6,
        COMPANION_WORD[2]: 9,
    }), f"the companion-word split changed: {companion_words}")

    # The seven records previously left as anchor-contained guards are a
    # literal subset of the fifteen companion-row units.
    record_keys = {
        (record["X1_tail_index"], record["X2_tail_index"],
         tuple(record["physical_edge"]))
        for record in companion_records
    }
    guard_records = classification["anchor_contained_guard_records"]
    guard_keys = {
        (record["X1_tail_index"], record["X2_tail_index"],
         tuple(record["physical_edge"]))
        for record in guard_records
    }
    require(len(guard_keys) == 7 and guard_keys <= record_keys,
            "a pinned anchor-contained guard escaped the companion unit")

    record_stream = json.dumps(records, sort_keys=True, separators=(",", ":"))
    ledger = {
        "pins": PINS,
        "mixed10_extension_count": len(records),
        "route_counts": dict(sorted(route_counts.items())),
        "record_stream_sha256": sha256(record_stream.encode()).hexdigest(),
        "companion_word_counts": {
            "110011": companion_words[COMPANION_WORD[1]],
            "110101": companion_words[COMPANION_WORD[2]],
        },
        "previous_anchor_guard_count": len(guard_keys),
        "previous_anchor_guard_keys": [
            [first, second, list(physical)]
            for first, second, physical in sorted(guard_keys)
        ],
        "theorem": (
            "every first mixed-10 internal extension of every minimal E14 "
            "bright chart has an ordinary two-row source unit.  In 120 "
            "records the original zero row equals the target tail.  In "
            "the remaining 15, including all seven former anchor-contained "
            "guards, a literal companion zero row is the negative target tail"
        ),
        "source_identity": (
            "write F_target=T-1.  If F_zero=T, then "
            "F_zero-F_target=1.  If F_companion=-T, then "
            "-F_companion-F_target=1"
        ),
        "scope": (
            "the identities are coefficientwise in the entire E14 formal "
            "parameter family, the new mixed-10 coefficient, and arbitrary "
            "core p1/s1 entries.  They use neither localization nor a rank "
            "landing.  Extensions by two simultaneous new cells are not "
            "asserted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"mixed-10 companion ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 mixed-10 companion-row unit: PASS (exact)")
    print(f"extensions={ledger['mixed10_extension_count']}")
    print(f"routes={ledger['route_counts']}")
    print(f"companion_words={ledger['companion_word_counts']}")
    print(f"closed_previous_anchor_guards={ledger['previous_anchor_guard_count']}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
