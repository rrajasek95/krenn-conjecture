#!/usr/bin/env python3
"""Close all 36 pure-11 E14 defects by complete unary two-row units.

The response-only frontier b62a039 retained 24 effective X1 reselections.
In the genuine common-q source these do not survive: for every one of the
36 affected pure-11 records, a literal mixed coefficient of q^[3] is equal
to plus or minus the complete pure-zero coefficient.  Since q^[3]=X0, the
two unary generators already contain 1.

Together with the pinned mixed-10 theorem, this makes all 1,020 first extra
internal-cell records after the minimal E14 enlargement ordinary units.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLASSIFIER_PATH = (
    "computations/verify_h3_c6_e14_second_tail_extension_classification.py"
)
MIXED_PATH = "computations/verify_h3_c6_e14_mixed10_companion_row_unit.py"
RESELECTION_PATH = (
    "computations/verify_h3_c6_e14_pure11_reselection_frontier.py"
)
PINS = {
    CLASSIFIER_PATH:
        "68dfff0e3dd85ce8e705b15bbfd7fdf91a9a052e21fe1f88bdd21cc002443656",
    "notes/h3-c6-e14-second-tail-extension-classification.md":
        "790accdf1b1c3441a8038cc5c90fb073295bc68c79e52547cbabb6ee7a99755b",
    MIXED_PATH:
        "4bdc70c34be6cd96c2521c97a3302acea6dd7db0e11bd6a7d5b6d74fbbcb2ba4",
    "notes/h3-c6-e14-mixed10-companion-row-unit.md":
        "842660467a4a39cf4d2002a1f3adf0e1591fc4031b7101b0f8a2d403062bf9ee",
    RESELECTION_PATH:
        "85aa5f3ae06a645f672df043eb4de2f656e130ef07f87266d0808ff52e710321",
    "notes/h3-c6-e14-pure11-reselection-frontier.md":
        "13a9eedf2265adb52a031110c1fbb911f2ab2ca6551fbe58f39aa8044cbb3328",
}
EXPECTED_LEDGER_SHA256 = (
    "99245d528fcadcc9a182a1615b7b68088f2537d782630488b49a6b841384d22e"
)
PURE_ZERO = (0, 0, 0, 0, 0, 0)


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


def unary_rows(e14, b4, q_cells):
    """Every literal word coefficient of the six-site q hafnian."""
    rows = {}
    for tail in b4.perfect_matchings(range(6)):
        choices = [q_cells.get(physical, {}) for physical in tail]
        if any(not options for options in choices):
            continue
        for decorations in product(*[tuple(options) for options in choices]):
            word = [None] * 6
            coefficient = {(): Q(1)}
            for physical, decoration in zip(
                    tail, decorations, strict=True):
                word[physical[0]], word[physical[1]] = decoration
                coefficient = e14.multiply(
                    coefficient, q_cells[physical][decoration]
                )
            word = tuple(word)
            rows[word] = e14.add(rows.get(word, {}), coefficient)
    return rows


def negate(polynomial):
    return {monomial: -coefficient
            for monomial, coefficient in polynomial.items()}


def audit():
    pin_dependencies()
    classifier = load(CLASSIFIER_PATH, "c6_e14_unary_classifier")
    e14 = load(classifier.E14_PATH, "c6_e14_unary_e14")
    b4 = e14.load(e14.B4_PATH, "c6_e14_unary_b4")
    mixed = load(MIXED_PATH, "c6_e14_unary_mixed")
    reselection = load(RESELECTION_PATH, "c6_e14_unary_reselection")
    classification, classification_digest = classifier.audit()
    mixed_ledger, mixed_digest = mixed.audit()
    reselection_ledger, reselection_digest = reselection.audit()
    require(classification_digest == classifier.EXPECTED_LEDGER_SHA256,
            "the pinned second-tail classification did not replay")
    require(mixed_digest == mixed.EXPECTED_LEDGER_SHA256,
            "the pinned mixed-10 theorem did not replay")
    require(reselection_digest == reselection.EXPECTED_LEDGER_SHA256,
            "the pinned response-only reselection frontier did not replay")

    records = []
    sign_counts = Counter()
    witness_counts = Counter()
    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            q_cells, _added, _selected = e14.q_inventory(
                b4, first_index, second_index
            )
            for physical in combinations(range(6), 2):
                if (1, 1) in q_cells.get(physical, {}):
                    continue
                enlarged = {edge: dict(cells)
                            for edge, cells in q_cells.items()}
                enlarged.setdefault(physical, {})[(1, 1)] = {
                    (classifier.X,): Q(1)
                }
                old_zero = classifier.response_row(
                    e14, b4, enlarged, e14.ZERO_WORD[first_index]
                )
                response_target = classifier.response_row(
                    e14, b4, enlarged, (1,) * 6
                )
                defect = classifier.x_coefficient(
                    classifier.subtract(e14, old_zero, response_target)
                )
                if not defect:
                    continue

                rows = unary_rows(e14, b4, enlarged)
                target = rows[PURE_ZERO]
                require(target == {(): Q(1)},
                        "the normalized pure-zero unary target changed")
                positive = sorted(
                    word for word, polynomial in rows.items()
                    if word != PURE_ZERO and polynomial == target
                )
                negative = sorted(
                    word for word, polynomial in rows.items()
                    if polynomial == negate(target)
                )
                require(positive or negative,
                        "an affected pure-11 record lost every unary unit")
                if positive:
                    witness = positive[0]
                    sign = 1
                    source_identity = "F_w-F_000000=1"
                else:
                    witness = negative[0]
                    sign = -1
                    source_identity = "-F_w-F_000000=1"
                require(witness != PURE_ZERO and any(witness),
                        "the unary witness stopped being a mixed zero word")
                sign_counts[sign] += 1
                witness_string = "".join(map(str, witness))
                witness_counts[witness_string] += 1
                records.append({
                    "X1_tail_index": first_index,
                    "X2_tail_index": second_index,
                    "new_cell": [*physical, 1, 1],
                    "unary_witness_word": witness_string,
                    "witness_sign_relative_to_U000000": sign,
                    "ordinary_source_identity": source_identity,
                    "all_positive_witness_words": [
                        "".join(map(str, word)) for word in positive
                    ],
                    "all_negative_witness_words": [
                        "".join(map(str, word)) for word in negative
                    ],
                })

    require(len(records) == 36,
            f"the pure-11 unary-unit count changed: {len(records)}")
    require(sign_counts == Counter({1: 33, -1: 3}),
            f"the canonical unary sign split changed: {sign_counts}")
    require(witness_counts == Counter({
        "020002": 12,
        "221100": 6,
        "022011": 6,
        "221010": 3,
        "000101": 3,
        "220110": 3,
        "022110": 3,
    }), f"the canonical unary witness orbit split changed: {witness_counts}")

    require(reselection_ledger["complete_one_extra_cell_frontier"] == {
        "Hall_intersecting_X1_reselection": 18,
        "fixed_hole_diagonal_C4_connectivity": 6,
        "ordinary_source_unit": 996,
    }, "the response-only frontier changed before unary promotion")
    total_layer = (
        classification["classification_record_count"]
    )
    require(total_layer == 1020,
            "the complete first-extension layer changed size")
    require(mixed_ledger["mixed10_extension_count"] == 135,
            "the pinned mixed-10 layer changed size")

    record_stream = json.dumps(records, sort_keys=True, separators=(",", ":"))
    ledger = {
        "pins": PINS,
        "affected_pure11_count": len(records),
        "canonical_witness_sign_counts": {
            str(sign): count for sign, count in sorted(sign_counts.items())
        },
        "canonical_witness_word_counts": dict(sorted(witness_counts.items())),
        "record_stream_sha256": sha256(record_stream.encode()).hexdigest(),
        "complete_first_extra_internal_cell_count": total_layer,
        "complete_first_extra_internal_cell_units": total_layer,
        "remaining_first_layer_records": 0,
        "theorem": (
            "every affected pure-11 first extension has a complete mixed "
            "unary row equal to plus or minus the pure-zero unary target.  "
            "Together with the response units, every one of the 1,020 first "
            "extra internal-cell records is an ordinary source unit"
        ),
        "source_identity": (
            "q^[3]=X0 gives F_000000=U_000000-1 and F_w=U_w "
            "for mixed w.  U_w=U_000000 yields F_w-F_000000=1; "
            "U_w=-U_000000 yields -F_w-F_000000=1"
        ),
        "supersession": (
            "the 18 Hall and six fixed-hole response-only reselections of "
            "b62a039 are killed before any reselection or rank landing"
        ),
        "next_local_survivor": (
            "a survivor in the same canonical E14 chart must add at least "
            "two new internal cells simultaneously, so cross-contamination "
            "changes both members of every displayed response/unary unit, "
            "or use an outside endpoint component.  This theorem does not "
            "close arbitrary multisite/global source components"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"pure-11 unary-unit ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 pure-11 unary unit: PASS (exact)")
    print(f"pure11_units={ledger['affected_pure11_count']}")
    print(f"witness_signs={ledger['canonical_witness_sign_counts']}")
    print(f"witness_words={ledger['canonical_witness_word_counts']}")
    print("first_extra_internal_cell_layer=1020/1020 ordinary units")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
