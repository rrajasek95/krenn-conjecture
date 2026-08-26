#!/usr/bin/env python3
"""Independent finite-set audit of the scoped residual hitting theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def minimal_sets(values):
    ordered = sorted(set(map(frozenset, values)), key=lambda item: (len(item), tuple(sorted(item))))
    result = []
    for item in ordered:
        if not any(prior <= item for prior in result):
            result.append(item)
    return result


def hits(support, families):
    return all(any(activation <= support for activation in family) for family in families)


def main():
    ledger = json.loads((HERE / "hitting_support_ledger.json").read_text())
    assert ledger["status"] == "PASS_DESIGN_ONLY_NO_Q_IDEALS_RUN"
    assert ledger["violated_equation_count"] == 13
    assert ledger["zero_coordinate_count"] == 70
    assert ledger["normalized_group_count"] == 0
    assert ledger["launch_gate"]["no_q_ideals_run"] is True
    assert ledger["logical_scope"]["not_a_global_quadruple_filter"] is True
    zero = sorted({
        coordinate
        for equation in ledger["equations"]
        for activation in equation["minimal_activation_sets"]
        for coordinate in activation
    } | (set(ledger["base_point"]) ^ set(ledger["base_point"])))
    # The activation union need not use every zero coordinate; recover the
    # exact universe from the pinned generator's 87-17 count via the recorded
    # supports plus exhaustive combination result.  For the size<=4 census,
    # coordinates absent from every activation can never improve a hit.
    active_universe = zero
    families = [
        [frozenset(item) for item in equation["minimal_activation_sets"]]
        for equation in ledger["equations"]
    ]
    for equation, family in zip(ledger["equations"], families):
        expanded = equation["expanded_polynomial"]
        constant = [item for item in expanded if not item["monomial"]]
        assert len(constant) == 1 and constant[0]["coefficient"] == equation["constant_residual"]
        candidates = [frozenset(item["monomial"]) for item in expanded if item["monomial"]]
        assert minimal_sets(candidates) == family
        assert all(item for item in family)

    # Any unused coordinate cannot help, so enumerate the active universe and
    # separately observe that padding with unused coordinates cannot create a
    # hit of size<=4 when no active subset of that size hits.
    independent_counts = {}
    for size in range(5):
        independent_counts[str(size)] = sum(
            hits(frozenset(candidate), families)
            for candidate in itertools.combinations(active_universe, size)
        )
    assert independent_counts == ledger["hitting_support_counts"] == {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 0,
    }

    closure = [frozenset()]
    closure_counts = []
    for family in families:
        closure = minimal_sets(left | right for left in closure for right in family)
        closure_counts.append(len(closure))
    assert closure_counts == ledger["hitting_closure_counts_by_equation"]
    assert len(closure) == ledger["inclusion_minimal_hitting_support_count"] == 259
    minimum = min(map(len, closure))
    minimum_supports = sorted(
        [sorted(item) for item in closure if len(item) == minimum]
    )
    assert minimum == ledger["minimum_fixed_base_hitting_size"] == 7
    assert minimum_supports == sorted(ledger["minimum_fixed_base_hitting_supports"])
    assert len(minimum_supports) == ledger["minimum_fixed_base_hitting_support_count"] == 6
    # Hostile deletion: every coordinate of every minimum support is needed.
    deletion_failures = 0
    for support in map(frozenset, minimum_supports):
        assert hits(support, families)
        for coordinate in support:
            assert not hits(support - {coordinate}, families)
            deletion_failures += 1
    assert deletion_failures == 42

    result = {
        "schema": "KRENN_X5_REP2_FIXED_BASE_HITTING_AUDIT_V1",
        "status": "PASS_SCOPED_FIXED_BASE_MINIMUM_SEVEN_NO_SIZE4_SUPPORT",
        "ledger_sha256": sha256(HERE / "hitting_support_ledger.json"),
        "residual_equations": 13,
        "size0_to4_counts": independent_counts,
        "inclusion_minimal_supports": len(closure),
        "minimum_size": minimum,
        "minimum_support_count": len(minimum_supports),
        "minimum_coordinate_deletion_hostiles": deletion_failures,
        "scope": ledger["logical_scope"],
        "warning": "unused zero coordinates cannot activate any residual monomial; arbitrary movable-base charts remain outside theorem",
    }
    output = HERE / "results_hitting_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
