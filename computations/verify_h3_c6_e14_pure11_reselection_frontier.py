#!/usr/bin/env python3
"""Locate the exact frontier after every first E14 internal extension.

The first second-tail census found 36 pure-11 extensions whose old
target/zero collision was broken by an effective alternate X1 matching.
Expanding every complete G11 word sharpens these records:

* 12 already have a literal antiparallel companion row and are units;
* 18 reselect X1 through a hole meeting the selected X2 hole 34, hence
  enter the Hall/active-rank interface; and
* 6 retain hole 01 and switch X1 tail 1 or 3 to tail 2.  These are the
  first fixed-port diagonal-C4 source-exhaustivity packets.

Together with the pinned mixed-10 theorem, the complete 1,020-record
one-extra-internal-cell layer is therefore 996 ordinary units and 24
effective target reselections.  This checker does not claim rank landing.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLASSIFIER_PATH = (
    "computations/verify_h3_c6_e14_second_tail_extension_classification.py"
)
MIXED_PATH = "computations/verify_h3_c6_e14_mixed10_companion_row_unit.py"
PINS = {
    CLASSIFIER_PATH:
        "68dfff0e3dd85ce8e705b15bbfd7fdf91a9a052e21fe1f88bdd21cc002443656",
    "notes/h3-c6-e14-second-tail-extension-classification.md":
        "790accdf1b1c3441a8038cc5c90fb073295bc68c79e52547cbabb6ee7a99755b",
    MIXED_PATH:
        "4bdc70c34be6cd96c2521c97a3302acea6dd7db0e11bd6a7d5b6d74fbbcb2ba4",
    "notes/h3-c6-e14-mixed10-companion-row-unit.md":
        "842660467a4a39cf4d2002a1f3adf0e1591fc4031b7101b0f8a2d403062bf9ee",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
}
EXPECTED_LEDGER_SHA256 = (
    "1e53202218683be805c5069846190068a5d9adb0d166aaf14d703e6fbc55c343"
)
TARGET_WORD = (1, 1, 1, 1, 1, 1)
COMPANION_WORD = {
    1: (1, 1, 0, 0, 1, 1),
    2: (1, 1, 0, 1, 0, 1),
}
X2_HOLE = frozenset((3, 4))


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


def matching_json(matching):
    return [list(edge) for edge in sorted(matching)]


def audit():
    pin_dependencies()
    classifier = load(CLASSIFIER_PATH, "c6_e14_pure11_classifier")
    e14 = load(classifier.E14_PATH, "c6_e14_pure11_e14")
    b4 = e14.load(e14.B4_PATH, "c6_e14_pure11_b4")
    mixed = load(MIXED_PATH, "c6_e14_mixed10_unit")
    classification, classification_digest = classifier.audit()
    mixed_ledger, mixed_digest = mixed.audit()
    require(classification_digest == classifier.EXPECTED_LEDGER_SHA256,
            "the pinned second-tail classification did not replay")
    require(mixed_digest == mixed.EXPECTED_LEDGER_SHA256,
            "the pinned mixed-10 unit theorem did not replay")

    records = []
    route_counts = Counter()
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
                target_sparse = classifier.response_row(
                    e14, b4, enlarged, TARGET_WORD
                )
                defect = classifier.x_coefficient(
                    classifier.subtract(e14, old_zero, target_sparse)
                )
                if not defect:
                    continue

                rows = e14.response_11(b4, enlarged)
                target = rows[TARGET_WORD]
                companion_words = [
                    word for word in COMPANION_WORD.values()
                    if rows.get(word) == negate(target)
                ]
                endpoints = tuple(defect)
                require(len(endpoints) == 2,
                        "a pure-11 defect lost its unordered endpoint hole")
                hole = frozenset(endpoints[0][:2])
                require(hole == frozenset(endpoints[1][:2]),
                        "the two pure-11 defect orientations use different holes")
                require(not (hole & set(physical)),
                        "the new pure-11 edge met its endpoint hole")
                tail_vertices = set(range(6)) - set(hole) - set(physical)
                require(len(tail_vertices) == 2,
                        "the common q tail stopped being determined")
                common_tail = tuple(sorted(tail_vertices))
                alternate_matching = frozenset((
                    tuple(sorted(hole)), tuple(physical), common_tail
                ))
                require(len({site for edge in alternate_matching for site in edge})
                        == 6,
                        "the alternate pure-X1 response stopped being a matching")

                if companion_words:
                    require(len(companion_words) == 1,
                            "a pure-11 record acquired multiple companion rows")
                    route = "ordinary_companion_unit"
                    detail = {
                        "companion_word": list(companion_words[0]),
                        "ordinary_source_identity":
                            "-F_companion-F_target=1",
                    }
                elif hole & X2_HOLE:
                    route = "Hall_intersecting_X1_reselection"
                    detail = {
                        "X1_endpoint_hole": sorted(hole),
                        "selected_X2_endpoint_hole": sorted(X2_HOLE),
                        "rank_scope": (
                            "Hall incidence only; four-good/clean rank landing "
                            "is not asserted"
                        ),
                    }
                else:
                    route = "fixed_hole_diagonal_C4_connectivity"
                    require(hole == frozenset((0, 1)),
                            "a non-Hall pure-11 reselection left the fixed hole")
                    require(first_index in (1, 3),
                            "the fixed-hole survivor changed its old X1 tail")
                    require(frozenset((physical, common_tail))
                            == frozenset(b4.BRIGHT_TAILS[1][1]),
                            "the fixed-hole survivor stopped selecting X1 tail 2")
                    selected_tail = frozenset(
                        b4.BRIGHT_TAILS[1][first_index - 1]
                    )
                    alternate_tail = frozenset((physical, common_tail))
                    cycle = selected_tail ^ alternate_tail
                    require(len(cycle) == 4
                            and len({site for edge in cycle for site in edge}) == 4,
                            "the fixed-hole source frontier stopped being one C4")
                    route = "fixed_hole_diagonal_C4_connectivity"
                    detail = {
                        "X1_endpoint_hole": [0, 1],
                        "old_X1_tail_index": first_index,
                        "alternate_X1_tail_index": 2,
                        "diagonal_C4_edges": matching_json(cycle),
                        "missing_input": (
                            "a complete-row typed attachment/flat-column "
                            "dependence for this affine pure-target C4"
                        ),
                    }

                route_counts[route] += 1
                records.append({
                    "X1_tail_index": first_index,
                    "X2_tail_index": second_index,
                    "new_cell": [*physical, 1, 1],
                    "alternate_X1_matching": matching_json(alternate_matching),
                    "route": route,
                    "detail": detail,
                })

    require(len(records) == 36,
            f"the affected pure-11 record count changed: {len(records)}")
    require(route_counts == Counter({
        "ordinary_companion_unit": 12,
        "Hall_intersecting_X1_reselection": 18,
        "fixed_hole_diagonal_C4_connectivity": 6,
    }), f"the pure-11 frontier split changed: {route_counts}")

    fixed_records = [record for record in records
                     if record["route"] ==
                     "fixed_hole_diagonal_C4_connectivity"]
    require({record["X1_tail_index"] for record in fixed_records} == {1, 3},
            "the fixed-hole frontier lost one old X1 tail")
    require({record["X2_tail_index"] for record in fixed_records} == {1, 2, 3},
            "the fixed-hole frontier lost one X2 chart")
    require({tuple(record["new_cell"]) for record in fixed_records}
            == {(2, 4, 1, 1)},
            "the fixed-hole frontier stopped being the q24:11 completion")

    original_totals = Counter(classification["total_routes"])
    require(original_totals == Counter({
        "unit_persists": 969,
        "effective_alternate_X1_matching": 36,
        "nonanchor_offdiagonal_free_carrier": 8,
        "anchor_contained_two_tail_guard": 7,
    }), "the pinned 1,020-record split changed")
    layer_totals = Counter({
        "ordinary_source_unit": (
            original_totals["unit_persists"]
            + mixed_ledger["route_counts"]["companion_antiparallel_unit"]
            + route_counts["ordinary_companion_unit"]
        ),
        "Hall_intersecting_X1_reselection":
            route_counts["Hall_intersecting_X1_reselection"],
        "fixed_hole_diagonal_C4_connectivity":
            route_counts["fixed_hole_diagonal_C4_connectivity"],
    })
    require(layer_totals == Counter({
        "ordinary_source_unit": 996,
        "Hall_intersecting_X1_reselection": 18,
        "fixed_hole_diagonal_C4_connectivity": 6,
    }), f"the complete first-extension frontier changed: {layer_totals}")

    record_stream = json.dumps(records, sort_keys=True, separators=(",", ":"))
    ledger = {
        "pins": PINS,
        "affected_pure11_record_count": len(records),
        "pure11_route_counts": dict(sorted(route_counts.items())),
        "pure11_record_stream_sha256": sha256(
            record_stream.encode()
        ).hexdigest(),
        "complete_one_extra_cell_frontier": dict(sorted(layer_totals.items())),
        "fixed_hole_frontier_records": fixed_records,
        "theorem": (
            "the entire first extra internal-cell layer after minimal E14 "
            "is reduced exactly to 996 ordinary units, 18 effective X1 "
            "reselections whose endpoint hole meets the selected X2 hole, "
            "and six fixed-hole pure-target diagonal-C4 switches"
        ),
        "earliest_survivor": (
            "the six fixed-hole records have old X1 tail 1 or 3, new "
            "q24:11 completing tail 2 with q35:11, fixed endpoint hole 01, "
            "and arbitrary selected X2 tail 1/2/3.  They require the "
            "source connectivity/exhaustivity attachment for an affine "
            "pure-target C4"
        ),
        "scope": (
            "the 18 Hall records are only routed to the existing Hall/active-"
            "rank interface.  This checker proves neither four-good rank "
            "landing nor termination, and does not enumerate two-cell "
            "extensions beyond the forced reselection support"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"pure-11 reselection frontier changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 pure-11 reselection frontier: PASS (exact)")
    print(f"pure11_routes={ledger['pure11_route_counts']}")
    print(f"full_layer={ledger['complete_one_extra_cell_frontier']}")
    print(f"fixed_hole_survivors={len(ledger['fixed_hole_frontier_records'])}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
