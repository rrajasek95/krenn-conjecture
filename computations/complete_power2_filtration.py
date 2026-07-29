#!/usr/bin/env python3
"""Try to prove P^2 is in the full n=6,q=3 mixed ideal by filtration.

The off-diagonal degree-zero block is the 874-row diagonal computation.  At
each higher degree this script tracks a coefficient-independent support bound
for the remainder, quotients one-term 2+2+2 pivots, closes only the components
meeting that support, and seeks a unitriangular singleton-column peeling.

If every nonempty layer peels and no support remains after degree 18, the
recorded blocks give an exact characteristic-zero existence proof: only the
initial diagonal block uses a modular full-rank minor; every subsequent block
has an explicit triangular integer minor.
"""

from __future__ import annotations

import sys
import pickle
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

import lift_power2_offdiag2 as L


def full_outputs(col):
    c, off, gs = col
    out = []
    for pm in L.PM:
        term = L.term_variables(c, pm)
        row = L.canonical_row(*L.add_term(off, gs, term))
        degree = len(off) + sum(a != b for _, _, a, b in term)
        out.append((degree, row))
    return tuple(out)


def structural_diagonal_columns(d, pivot_indices):
    return {
        L.canonical_column(c, (), gs)
        for j in pivot_indices
        for c, gs in (d["column_reps"][j],)
    }


def add_higher_support(columns, current_degree, supports):
    counts = defaultdict(set)
    for col in columns:
        for degree, row in full_outputs(col):
            if degree > current_degree:
                supports[degree].add(row)
                counts[degree].add(row)
    return {k: len(v) for k, v in sorted(counts.items())}


def solve_support_layer(starts, degree):
    killed_starts = {r for r in starts if L.monomial_killed(r)}
    survivors = set(starts) - killed_starts
    print(
        f"layer {degree}: starts={len(starts)}, monomial={len(killed_starts)}, "
        f"survivor starts={len(survivors)}",
        flush=True,
    )

    rows, cols = L.quotient_component_closure(survivors)
    pivots, remaining = L.peel_component(rows, cols)
    if remaining:
        raise RuntimeError(
            f"layer {degree} did not peel: {len(remaining)} rows remain"
        )
    # The triangular minor proves surjectivity on the whole component, but a
    # remainder supported on `survivors` needs only the reverse dependency
    # closure of those rows.  This support bound is coefficient-independent:
    # solving the triangular system from last pivot to first can introduce
    # only earlier rows occurring in the selected pivot column.
    needed = set(survivors)
    selected_pivots = []
    for row, col, coeff in reversed(pivots):
        if row not in needed:
            continue
        selected_pivots.append((row, col, coeff))
        for rr in L.leading_outputs(col):
            if rr in rows and rr != row:
                needed.add(rr)
    correction = {col for _, col, _ in selected_pivots}

    # Pivot columns can also hit rows discarded by the monomial quotient.
    killed_needed = set(killed_starts)
    for col in correction:
        killed_needed.update(r for r in L.leading_outputs(col) if L.monomial_killed(r))
    for row in killed_needed:
        mono = L.monomial_column(row)
        assert mono is not None
        correction.add(mono)

    print(
        f"layer {degree}: quotient rows={len(rows)}, triangular pivots={len(pivots)}, "
        f"needed pivots={len(selected_pivots)}, "
        f"one-term corrections={len(killed_needed)}, correction columns={len(correction)}",
        flush=True,
    )
    return correction


def main():
    resume_path = Path("/tmp/krenn_p2_filter_after3.pkl")
    if resume_path.exists():
        with resume_path.open("rb") as fh:
            saved = pickle.load(fh)
        supports = defaultdict(set, saved["supports"])
        certificates = list(saved["certificates"])
        first_degree = 4
        print(
            f"resumed after layer 3: { {k: len(v) for k, v in supports.items()} }",
            flush=True,
        )
    else:
        # The actual modular solution is computed only as an audit; structural
        # propagation starts from all 874 columns of a rationally invertible
        # diagonal minor, so it is independent of coefficient coincidences mod p.
        _, _, d, pivot_indices = L.diagonal_remainder()
        assert len(pivot_indices) == d["shape"][0] == 874
        diagonal_columns = structural_diagonal_columns(d, pivot_indices)
        assert len(diagonal_columns) == 874

        supports = defaultdict(set)
        created = add_higher_support(diagonal_columns, 0, supports)
        print(f"structural diagonal remainder supports={created}", flush=True)
        certificates = []
        first_degree = 1

    for degree in range(first_degree, 19):
        starts = supports.pop(degree, set())
        if not starts:
            print(f"layer {degree}: empty", flush=True)
            continue
        correction = solve_support_layer(starts, degree)
        created = add_higher_support(correction, degree, supports)
        certificates.append((degree, len(starts), len(correction)))
        print(f"layer {degree}: propagated supports={created}", flush=True)

        if degree == 3:
            with resume_path.open("wb") as fh:
                pickle.dump(
                    {"supports": dict(supports), "certificates": certificates},
                    fh,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
            print(f"saved checkpoint {resume_path}", flush=True)

        # Layer-local incidence caches can dominate memory and are not needed
        # after its correction columns have been propagated.
        L.incident_leading_columns.cache_clear()
        L.leading_outputs.cache_clear()
        L.monomial_killed.cache_clear()
        L.monomial_column.cache_clear()

    tail = {k: len(v) for k, v in supports.items() if v}
    print(f"certificate blocks={certificates}", flush=True)
    print(f"support beyond degree 18={tail}", flush=True)
    if tail:
        raise RuntimeError("unexpected support beyond the maximum degree")


if __name__ == "__main__":
    main()
