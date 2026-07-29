#!/usr/bin/env python3
"""Coefficient-aware modular continuation of the n=6 P^2 filtration.

Unlike ``dfs_power2_filtration.py``, this script propagates the actual
GF(1009) coefficients of one diagonal solution.  At each positive
off-diagonal degree it constructs a goal-directed triangular right inverse
only for rows whose coefficient is nonzero.  This is exploratory: success
modulo one prime is not a characteristic-zero certificate, but a surviving
dead row pinpoints a genuine terminal constraint and a very small exact
subproblem.
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict

sys.setrecursionlimit(200_000)

import complete_power2_filtration as C
import lift_power2_offdiag2 as L
from verify_reachable_k9_obstruction import BAD_ROW, CONE_COLUMN, CONE_ROW


PRIME = L.PRIME


def normalize(counter):
    return Counter({row: value % PRIME for row, value in counter.items() if value % PRIME})


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
            deps = {
                rr
                for rr in L.leading_outputs(col)
                if rr != row and not L.monomial_killed(rr)
            }
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
    for k, row in enumerate(survivors, 1):
        if not prove(row):
            print(
                f"degree {degree}: triangular failure at {k}/{len(survivors)}, "
                f"row={row}, assigned={len(assigned)}, calls={calls}",
                flush=True,
            )
            return None
        if k % 1000 == 0:
            print(
                f"degree {degree}: assigned starts={k}/{len(survivors)}, "
                f"closure={len(assigned)}, calls={calls}",
                flush=True,
            )
    print(
        f"degree {degree}: triangular closure={len(assigned)}, calls={calls}",
        flush=True,
    )
    return assigned


def solve_triangular(residual, assigned, degree):
    work = Counter({row: (-value) % PRIME for row, value in residual.items()})
    correction = Counter()

    for row, col in reversed(tuple(assigned.items())):
        value = work.get(row, 0) % PRIME
        if not value:
            continue
        outputs = Counter(L.leading_outputs(col))
        diagonal = outputs[row] % PRIME
        assert diagonal
        coefficient = value * pow(diagonal, PRIME - 2, PRIME) % PRIME
        correction[col] = (correction[col] + coefficient) % PRIME
        for other, multiplicity in outputs.items():
            work[other] = (work.get(other, 0) - coefficient * multiplicity) % PRIME

    work = normalize(work)
    while work:
        row, value = next(iter(work.items()))
        if not L.monomial_killed(row):
            print(
                f"degree {degree}: unsolved noncone coefficient {value} at {row}",
                flush=True,
            )
            return None
        col = L.monomial_column(row)
        outputs = Counter(L.leading_outputs(col))
        assert set(outputs) == {row}
        coefficient = value * pow(outputs[row], PRIME - 2, PRIME) % PRIME
        correction[col] = (correction[col] + coefficient) % PRIME
        work[row] = (work[row] - coefficient * outputs[row]) % PRIME
        if not work[row]:
            del work[row]

    correction = normalize(correction)
    # Audit the current associated-graded equation.
    audit = Counter(residual)
    for col, coefficient in correction.items():
        for row in L.leading_outputs(col):
            audit[row] = (audit[row] + coefficient) % PRIME
    assert not normalize(audit)
    print(
        f"degree {degree}: residual support={len(residual)}, "
        f"nonzero corrections={len(correction)}",
        flush=True,
    )
    return correction


def add_future(residuals, correction, degree, maximum_degree=18):
    created = Counter()
    for col, coefficient in correction.items():
        for output_degree, row in C.full_outputs(col):
            if output_degree <= degree or output_degree > maximum_degree:
                continue
            residuals[output_degree][row] = (
                residuals[output_degree].get(row, 0) + coefficient
            ) % PRIME
            created[output_degree] += 1
    for output_degree in tuple(residuals):
        residuals[output_degree] = normalize(residuals[output_degree])
    return {
        output_degree: (created[output_degree], len(residuals[output_degree]))
        for output_degree in sorted(created)
    }


def main():
    rhs2, rhs3, _, _ = L.diagonal_remainder()
    residuals = defaultdict(Counter)
    residuals[2] = normalize(rhs2)
    residuals[3] = normalize(rhs3)

    # Only propagate through degree six.  This decides whether the concrete
    # coefficient-aware lift reaches the known cone-to-dead-row obstruction
    # without constructing the irrelevant degree-seven/eight tails.
    for degree in range(2, 6):
        residual = normalize(residuals.pop(degree, Counter()))
        if not residual:
            print(f"degree {degree}: empty", flush=True)
            continue
        cones = sum(L.monomial_killed(row) for row in residual)
        print(
            f"degree {degree}: actual support={len(residual)}, cones={cones}",
            flush=True,
        )
        assigned = triangular_assignment(tuple(residual), degree)
        if assigned is None:
            raise SystemExit(2)
        correction = solve_triangular(residual, assigned, degree)
        if correction is None:
            raise SystemExit(3)
        created = add_future(residuals, correction, degree, maximum_degree=6)
        print(f"degree {degree}: future (raw,nonzero)={created}", flush=True)

        L.incident_leading_columns.cache_clear()
        L.leading_outputs.cache_clear()
        L.monomial_killed.cache_clear()
        L.monomial_column.cache_clear()

    degree_six = normalize(residuals[6])
    value = degree_six.get(CONE_ROW, 0)
    print(
        f"degree 6 probe: support={len(degree_six)}, "
        f"known cone coefficient={value} mod {PRIME}"
    )
    if value:
        bad_multiplicity = sum(
            output_degree == 9 and row == BAD_ROW
            for output_degree, row in C.full_outputs(CONE_COLUMN)
        )
        assert bad_multiplicity == 1
        print(
            f"using the unique one-term cone correction forces BAD_ROW "
            f"with nonzero coefficient {-value % PRIME} mod {PRIME}"
        )


if __name__ == "__main__":
    main()
