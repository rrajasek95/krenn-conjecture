#!/usr/bin/env python3
"""Promote one-sided proportionality to a nu-safe support reduction.

The synchronized representative maximizes the number nu of mutual scalar
anchors, then minimizes scalar support.  The outside and companion cells in
the one-sided coloop reduction are distinct nonzero components of one p_i or
s_j row, hence share one coordinate endpoint.  Neither is a mutual anchor.
The exact proportional-column modification introduces no cell and deletes
the outside cell (and possibly the companion).  It therefore preserves every
old mutual anchor and strictly reduces support, contradicting the
lexicographic choice.  The former protected-decoration caveat does not apply
to nu.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
    "computations/verify_anchor_lexicographic_curvature_synchronization.py":
        "def1cfcc191d7755e619100197704b952a2e897ac735ecde5fec5fbbff59f4a9",
    "notes/anchor-lexicographic-curvature-synchronization.md":
        "1f4a3eb5679409a640bc1596fd6dce4b01fbf7296cd02f8d0b342c8e08f85e8a",
}
EXPECTED_LEDGER_SHA256 = (
    "151e0588d4047c09da0e385c3c8eae2a577ffc106d0cb8415a577670989e774d"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def mutual_anchors(edges):
    degrees = {}
    for left, right in edges:
        degrees[left] = degrees.get(left, 0) + 1
        degrees[right] = degrees.get(right, 0) + 1
    return frozenset(pair for pair in edges
                     if degrees[pair[0]] == degrees[pair[1]] == 1)


def audit_graph_monotonicity():
    # H=(P,i) is the common coordinate endpoint.  O,C are the outside and
    # companion tail-coordinate endpoints.  The remaining vertices and
    # optional edges model an arbitrary ambient scalar support graph.
    head, outside_tail, companion_tail = "H", "O", "C"
    outside = tuple(sorted((head, outside_tail)))
    companion = tuple(sorted((head, companion_tail)))
    vertices = (head, outside_tail, companion_tail, "A", "B", "D")
    candidates = tuple(
        tuple(sorted(pair)) for pair in combinations(vertices, 2)
        if tuple(sorted(pair)) not in (outside, companion)
    )
    audited = 0
    created_histogram = {}
    for mask in range(1 << len(candidates)):
        old = {outside, companion}
        old.update(candidates[index] for index in range(len(candidates))
                   if mask & (1 << index))
        old_anchors = mutual_anchors(old)
        require(outside not in old_anchors and companion not in old_anchors,
                "a same-row cell became a mutual anchor")
        for cancel_companion in (False, True):
            new = set(old)
            new.remove(outside)
            if cancel_companion:
                new.remove(companion)
            new_anchors = mutual_anchors(new)
            require(old_anchors <= new_anchors,
                    "deleting same-row cells destroyed an old mutual anchor")
            require(len(new) < len(old),
                    "the proportional move stopped reducing support")
            increase = len(new_anchors) - len(old_anchors)
            created_histogram[increase] = created_histogram.get(increase, 0) + 1
            audited += 1
    require(audited == 2 * (1 << len(candidates)),
            "the ambient support-graph audit count changed")
    return {
        "coordinate_vertices": list(vertices),
        "ambient_optional_edges": len(candidates),
        "support_graphs_times_two_update_strata": audited,
        "anchor_increase_histogram": created_histogram,
        "universal_relation": (
            "old mutual anchors are a subset of new mutual anchors after "
            "deleting the outside cell, with or without cancelling the "
            "same-row companion"
        ),
    }


def audit_exact_proportional_move():
    companion_column = (Q(2), Q(-1), Q(3), Q(4))
    scale = Q(-3, 2)
    outside_column = tuple(scale * value for value in companion_column)
    samples = []
    for outside_coefficient, companion_coefficient in (
            (Q(4), Q(5)), (Q(4), Q(6)), (Q(-2), Q(-3))):
        updated = companion_coefficient + scale * outside_coefficient
        old = tuple(outside_coefficient * outside_column[index]
                    + companion_coefficient * companion_column[index]
                    for index in range(len(companion_column)))
        new = tuple(updated * value for value in companion_column)
        require(old == new,
                "the exact proportional response identity changed")
        samples.append({
            "outside_coefficient": str(outside_coefficient),
            "companion_coefficient": str(companion_coefficient),
            "updated_companion": str(updated),
            "companion_cancelled": updated == 0,
            "response": [str(value) for value in old],
        })
    require(any(sample["companion_cancelled"] for sample in samples)
            and any(not sample["companion_cancelled"] for sample in samples),
            "the two proportional update strata were not both audited")
    return {
        "column_relation": "L(out)=lambda*L(companion)",
        "finite_update": "x_out'=0, x_comp'=x_comp+lambda*x_out",
        "samples": samples,
        "source_rows_preserved": (
            "all four responses exactly; unary and other endpoint rows "
            "are unchanged"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "exact_source_update": audit_exact_proportional_move(),
        "mutual_anchor_monotonicity": audit_graph_monotonicity(),
        "theorem": (
            "at a maximum-mutual-anchor then minimum-support source, two "
            "distinct occupied components in one p_i or s_j row cannot "
            "have proportional complete response columns.  The exact "
            "one-sided update removes the outside component and possibly "
            "its companion; because both shared the same coordinate head, "
            "neither was a mutual anchor, every old mutual anchor persists, "
            "and support strictly decreases"
        ),
        "scope_correction": (
            "a companion may be protected as a chosen matching decoration, "
            "but it is not protected by the lexicographic invariant nu.  "
            "The earlier conservative Hall/lock stratum is therefore empty "
            "at the synchronized representative.  This uses full tensor-"
            "column proportionality, never a single coefficient"
        ),
        "remaining_branch": (
            "both one-sided complete-column pairs are nonproportional; the "
            "selected-word corner then gives an external q mate or the "
            "bistar/Fitting carrier from the pinned companion boundary"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"proportional nu-safe ledger changed: {digest}")
    print("h3 target-coloop proportional nu-safe reduction: PASS")
    print("same-row occupied cells are never mutual coordinate anchors")
    print("proportional full columns -> exact nu-safe support reduction")
    print("remaining branch: nonproportional bistar/minor only")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
