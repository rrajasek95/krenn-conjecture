#!/usr/bin/env python3
"""Restartable coefficient-aware preparation/solve of the n=6 P^2 K6 block.

This preserves the exact orbit conventions of coefficient_power2_filtration.py
but checkpoints before and after every expensive tail-propagation step.  It is
intended as the reference implementation for a faster Rust port.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import pickle
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.setrecursionlimit(500_000)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import complete_power2_filtration as C
import lift_power2_offdiag2 as L


def normalize(counter, prime):
    return Counter({row: value % prime for row, value in counter.items()
                    if value % prime})


def save(path, state):
    payload = pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with gzip.open(temporary, "wb", compresslevel=3) as handle:
        handle.write(payload)
    temporary.replace(path)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"checkpoint={path} decoded_sha256={digest} bytes={path.stat().st_size}",
          flush=True)


def load(path):
    with gzip.open(path, "rb") as handle:
        return pickle.load(handle)


def triangular_assignment(starts, degree):
    assigned = {}
    used_columns = set()
    visiting = set()
    calls = 0

    def prove(row):
        nonlocal calls
        calls += 1
        if L.monomial_killed(row) or row in assigned:
            return True
        if row in visiting:
            return False
        visiting.add(row)
        options = []
        for col in L.incident_leading_columns(row):
            if col in used_columns:
                continue
            deps = {rr for rr in L.leading_outputs(col)
                    if rr != row and not L.monomial_killed(rr)}
            options.append((len(deps), col, tuple(sorted(deps))))
        options.sort(key=lambda item: (item[0], item[1]))
        for _, col, deps in options:
            if col in used_columns:
                continue
            if all(prove(dep) for dep in deps):
                if col in used_columns:
                    continue
                assigned[row] = col
                used_columns.add(col)
                visiting.remove(row)
                return True
        visiting.remove(row)
        return False

    survivors = [row for row in starts if not L.monomial_killed(row)]
    for index, row in enumerate(survivors, 1):
        if not prove(row):
            print(f"degree {degree}: DEAD_OR_CYCLIC row={row} "
                  f"at={index}/{len(survivors)} assigned={len(assigned)} calls={calls}",
                  flush=True)
            return None, row
        if index % 5000 == 0:
            print(f"degree {degree}: starts={index}/{len(survivors)} "
                  f"closure={len(assigned)} calls={calls}", flush=True)
    print(f"degree {degree}: triangular closure={len(assigned)} calls={calls}",
          flush=True)
    return assigned, None


def solve_triangular(residual, assigned, degree, prime):
    work = Counter({row: (-value) % prime for row, value in residual.items()})
    correction = Counter()
    for row, col in reversed(tuple(assigned.items())):
        value = work.get(row, 0) % prime
        if not value:
            continue
        outputs = Counter(L.leading_outputs(col))
        diagonal = outputs[row] % prime
        if not diagonal:
            return None, ("zero_diagonal", row, col)
        coefficient = value * pow(diagonal, prime - 2, prime) % prime
        correction[col] = (correction[col] + coefficient) % prime
        for other, multiplicity in outputs.items():
            work[other] = (work.get(other, 0) - coefficient * multiplicity) % prime
    work = normalize(work, prime)
    while work:
        row, value = next(iter(work.items()))
        if not L.monomial_killed(row):
            return None, ("unsolved_noncone", row, value)
        col = L.monomial_column(row)
        outputs = Counter(L.leading_outputs(col))
        if set(outputs) != {row}:
            return None, ("bad_cone", row, col)
        coefficient = value * pow(outputs[row] % prime, prime - 2, prime) % prime
        correction[col] = (correction[col] + coefficient) % prime
        work[row] = (work[row] - coefficient * outputs[row]) % prime
        if not work[row]:
            del work[row]
    correction = normalize(correction, prime)
    audit = Counter(residual)
    for col, coefficient in correction.items():
        for row in L.leading_outputs(col):
            audit[row] = (audit[row] + coefficient) % prime
    if normalize(audit, prime):
        return None, ("audit_nonzero", len(normalize(audit, prime)))
    print(f"degree {degree}: residual={len(residual)} corrections={len(correction)}",
          flush=True)
    return correction, None


def propagate(residuals, correction, degree, prime, maximum_degree=6):
    created = Counter()
    for index, (col, coefficient) in enumerate(correction.items(), 1):
        for output_degree, row in C.full_outputs(col):
            if degree < output_degree <= maximum_degree:
                residuals[output_degree][row] = (
                    residuals[output_degree].get(row, 0) + coefficient) % prime
                created[output_degree] += 1
        if index % 20000 == 0:
            print(f"degree {degree}: propagated columns={index}/{len(correction)}",
                  flush=True)
    for output_degree in tuple(residuals):
        residuals[output_degree] = normalize(residuals[output_degree], prime)
    return {key: (created[key], len(residuals[key])) for key in sorted(created)}


def prepare_degree6(prime, checkpoint):
    L.PRIME = prime
    if checkpoint.exists():
        state = load(checkpoint)
        if state["prime"] != prime:
            raise RuntimeError("checkpoint prime mismatch")
        residuals = defaultdict(Counter, state["residuals"])
        next_degree = state["next_degree"]
        pending = state.get("pending")
        print(f"resume={checkpoint} next_degree={next_degree} "
              f"supports={ {k:len(v) for k,v in residuals.items()} }", flush=True)
    else:
        rhs2, rhs3, _, _ = L.diagonal_remainder()
        residuals = defaultdict(Counter)
        residuals[2] = normalize(rhs2, prime)
        residuals[3] = normalize(rhs3, prime)
        next_degree = 2
        pending = None
        save(checkpoint, {"prime": prime, "next_degree": next_degree,
                          "residuals": dict(residuals), "pending": None})

    if pending is not None:
        degree, correction = pending
        print(f"resume pending propagation degree={degree} cols={len(correction)}",
              flush=True)
        created = propagate(residuals, correction, degree, prime)
        print(f"degree {degree}: future={created}", flush=True)
        next_degree = degree + 1
        pending = None
        save(checkpoint, {"prime": prime, "next_degree": next_degree,
                          "residuals": dict(residuals), "pending": None})
        L.incident_leading_columns.cache_clear()
        L.leading_outputs.cache_clear()
        L.monomial_killed.cache_clear()
        L.monomial_column.cache_clear()

    for degree in range(next_degree, 6):
        residual = normalize(residuals.pop(degree, Counter()), prime)
        if not residual:
            continue
        cones = sum(L.monomial_killed(row) for row in residual)
        print(f"degree {degree}: residual={len(residual)} cones={cones}", flush=True)
        assigned, dead = triangular_assignment(tuple(residual), degree)
        if dead is not None:
            raise RuntimeError(f"unexpected lower-degree failure {dead}")
        correction, failure = solve_triangular(residual, assigned, degree, prime)
        if failure is not None:
            raise RuntimeError(f"unexpected lower-degree solve failure {failure}")
        save(checkpoint, {"prime": prime, "next_degree": degree,
                          "residuals": dict(residuals),
                          "pending": (degree, correction)})
        created = propagate(residuals, correction, degree, prime)
        print(f"degree {degree}: future={created}", flush=True)
        save(checkpoint, {"prime": prime, "next_degree": degree + 1,
                          "residuals": dict(residuals), "pending": None})
        L.incident_leading_columns.cache_clear()
        L.leading_outputs.cache_clear()
        L.monomial_killed.cache_clear()
        L.monomial_column.cache_clear()

    degree6 = normalize(residuals[6], prime)
    print(f"degree 6 prepared: support={len(degree6)}", flush=True)
    return degree6


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--solve-degree6", action="store_true")
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    checkpoint = args.checkpoint or Path(
        f"/tmp/krenn_p2_coeff_p{args.prime}_through5.pkl.gz")
    degree6 = prepare_degree6(args.prime, checkpoint)
    if not args.solve_degree6:
        return
    assigned, dead = triangular_assignment(tuple(degree6), 6)
    if dead is not None:
        print(f"degree 6 verdict: triangular failure row={dead}", flush=True)
        raise SystemExit(2)
    correction, failure = solve_triangular(
        degree6, assigned, 6, args.prime)
    if failure is not None:
        print(f"degree 6 verdict: solve failure={failure}", flush=True)
        raise SystemExit(3)
    save(Path(f"/tmp/krenn_p2_coeff_p{args.prime}_degree6_solution.pkl.gz"), {
        "prime": args.prime,
        "residual": degree6,
        "assigned": assigned,
        "correction": correction,
    })
    print("degree 6 verdict: CORRECTED_MOD_PRIME", flush=True)


if __name__ == "__main__":
    main()
