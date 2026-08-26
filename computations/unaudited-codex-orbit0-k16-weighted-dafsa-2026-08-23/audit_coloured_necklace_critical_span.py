#!/usr/bin/env python3
"""Bounded critical-pair span on the corrected coloured-necklace closure.

Every alternative four-cut relation is reduced by the deterministic signed
normal-form map, and its difference from the chosen relation is inserted into
a sparse modular row basis.  The run is target-rooted and therefore a nonzero
remainder is only bounded evidence.  Modular zero is explicitly not promoted
to characteristic-zero membership without an exact replay.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import time


HERE = Path(__file__).resolve().parent
PROVIDER = HERE / "audit_coloured_necklace_target_reduction.py"
OUT = HERE / "results_coloured_necklace_critical_span.json"
SELECTED = HERE / "coloured_necklace_critical_span_selected.tsv"
PRIME = 32003
TIME_CAP = 235.0
STATE_CAP = 250_000
RELATION_CAP = 500_000
BASIS_NNZ_CAP = 30_000_000


def load_provider():
    spec = importlib.util.spec_from_file_location("coloured_necklace_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load_provider()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def modular(counter):
    return {coordinate: value % PRIME for coordinate, value in counter.items()
            if value % PRIME}


def subtract(left, scale, right):
    for coordinate, value in right.items():
        updated = (left.get(coordinate, 0) - scale * value) % PRIME
        if updated:
            left[coordinate] = updated
        else:
            left.pop(coordinate, None)


class SparseBasis:
    def __init__(self):
        self.rows = {}
        self.nnz = 0

    def reduce(self, row):
        row = dict(row)
        while row:
            pivot = min(row)
            basis = self.rows.get(pivot)
            if basis is None:
                return row
            subtract(row, row[pivot], basis)
        return row

    def insert(self, row):
        row = self.reduce(row)
        if not row:
            return False, None
        pivot = min(row)
        inverse = pow(row[pivot], PRIME - 2, PRIME)
        row = {coordinate: value * inverse % PRIME
               for coordinate, value in row.items()}
        self.rows[pivot] = row
        self.nnz += len(row)
        return True, pivot


def exact_difference(reducer, state, indices, cuts):
    expected = reducer.normal(state)
    right = Counter()
    for child, count in C.relation_children(state, indices, cuts):
        for terminal, coefficient in reducer.normal(child).items():
            right[terminal] -= count * coefficient
    right = C.retain_nonzero(right)
    difference = Counter(right)
    for terminal, coefficient in expected.items():
        difference[terminal] -= coefficient
    return C.retain_nonzero(difference)


def relation_key(difference):
    # Exact signed vector key; Python tuples avoid a digest-collision argument.
    return tuple(sorted(difference.items()))


def build():
    start = time.monotonic()
    reducer = C.Reducer()
    target = Counter()
    for state, multiplicity in sorted(C.initial_target().items(),
                                      key=lambda item: C.state_text(item[0])):
        for terminal, coefficient in reducer.normal(state).items():
            target[terminal] += multiplicity * coefficient
    target = C.retain_nonzero(target)
    require(len(target) == 10_354, len(target))

    basis = SparseBasis()
    seen = set()
    selected = []
    choices = 0
    zero_differences = 0
    duplicate_differences = 0
    states_checked = 0
    cursor = 0
    target_remainder = basis.reduce(modular(target))
    status = "UNRESOLVED_CAP"
    cap_reason = None

    while cursor < len(reducer.order):
        elapsed = time.monotonic() - start
        if elapsed > TIME_CAP:
            cap_reason = "time"
            break
        if len(reducer.memo) > STATE_CAP:
            cap_reason = "states"
            break
        if len(seen) >= RELATION_CAP:
            cap_reason = "relations"
            break
        if basis.nnz > BASIS_NNZ_CAP:
            cap_reason = "basis_nnz"
            break
        state = reducer.order[cursor]
        cursor += 1
        if len(state) <= 3:
            states_checked += 1
            continue
        chosen = reducer.choices[state]
        local_seen = set()
        for indices, cuts, _ in C.all_valid_choices(state):
            if time.monotonic() - start > TIME_CAP:
                cap_reason = "time"
                break
            choices += 1
            children = C.relation_children(state, indices, cuts)
            if children in local_seen:
                continue
            local_seen.add(children)
            difference = exact_difference(reducer, state, indices, cuts)
            if not difference:
                zero_differences += 1
                continue
            key = relation_key(difference)
            if key in seen:
                duplicate_differences += 1
                continue
            seen.add(key)
            independent, pivot = basis.insert(modular(difference))
            if independent:
                selected.append((state, indices, cuts, len(difference), pivot))
                # A fresh pivot is the only event that can change membership.
                target_remainder = basis.reduce(modular(target))
                if not target_remainder:
                    status = "MODULAR_TARGET_ZERO_EXACT_REPLAY_REQUIRED"
                    cap_reason = None
                    break
            if len(seen) >= RELATION_CAP or basis.nnz > BASIS_NNZ_CAP:
                cap_reason = "relations" if len(seen) >= RELATION_CAP else "basis_nnz"
                break
        states_checked += 1
        if status != "UNRESOLVED_CAP" or cap_reason is not None:
            break
        if states_checked % 100 == 0:
            print(f"CHECKPOINT states={states_checked} memo={len(reducer.memo)} "
                  f"relations={len(seen)} rank={len(basis.rows)} nnz={basis.nnz} "
                  f"target_rem={len(target_remainder)} elapsed={time.monotonic()-start:.1f}",
                  file=sys.stderr, flush=True)

    if cursor >= len(reducer.order) and status == "UNRESOLVED_CAP" and cap_reason is None:
        status = "TARGET_ROOTED_CLOSURE_COMPLETE_MODULAR_NONZERO"

    selected_lines = ["ordinal\tstate\tindices\tcuts\tdifference_support\tpivot"]
    for ordinal, (state, indices, cuts, support, pivot) in enumerate(selected, 1):
        selected_lines.append(
            f"{ordinal}\t{C.state_text(state)}\t{','.join(map(str, indices))}\t"
            f"{','.join(map(str, cuts))}\t{support}\t{C.state_text(pivot)}")
    selected_payload = "\n".join(selected_lines) + "\n"

    relation_digest = sha256()
    for key in sorted(seen):
        relation_digest.update(repr(key).encode())
        relation_digest.update(b"\n")
    remainder_digest = sha256()
    for coordinate, coefficient in sorted(target_remainder.items()):
        remainder_digest.update(repr((coordinate, coefficient)).encode())
        remainder_digest.update(b"\n")

    result = {
        "schema": "orbit0-coloured-necklace-critical-span-v1",
        "status": status,
        "cap_reason": cap_reason,
        "prime": PRIME,
        "time_cap_seconds": TIME_CAP,
        "state_cap": STATE_CAP,
        "relation_cap": RELATION_CAP,
        "basis_nnz_cap": BASIS_NNZ_CAP,
        "corrected_target_normal_support": len(target),
        "states_checked": states_checked,
        "memoized_states": len(reducer.memo),
        "cut_choices_checked": choices,
        "distinct_nonzero_critical_relations": len(seen),
        "zero_differences": zero_differences,
        "duplicate_differences": duplicate_differences,
        "modular_critical_rank": len(basis.rows),
        "modular_basis_nnz": basis.nnz,
        "selected_relation_rows": len(selected),
        "modular_target_remainder_support": len(target_remainder),
        "modular_target_zero": not target_remainder,
        "critical_relation_digest": relation_digest.hexdigest(),
        "target_remainder_digest": remainder_digest.hexdigest(),
        "selected_tsv_sha256": sha256(selected_payload.encode()).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "scope_guard": (
            "A nonzero remainder is only evidence in the reached downward closure. A modular "
            "zero is not characteristic-zero membership until an exact selected-row replay lands."
        ),
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return result, selected_payload


def main():
    result, selected_payload = build()
    result_payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--verify" in sys.argv:
        require(SELECTED.read_text() == selected_payload, "selected ledger differs")
        stored = json.loads(OUT.read_text())
        for key, value in result.items():
            if key != "elapsed_seconds":
                require(stored[key] == value, (key, stored[key], value))
    else:
        SELECTED.write_text(selected_payload)
        OUT.write_text(result_payload)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
