#!/usr/bin/env python3
"""Exact h=3,4 augmented membership gate for the Hasse/moment route.

The complete principal-parts Hasse tower contains the formal response
orders B_2,...,B_h.  The Hilbert--Cauchy calculation gives coefficient
relations after forgetting physical augmented rows.  This checker computes
the exact h=3,4 coefficient matrices and lifts the question to a finite
rank criterion with arbitrary protected/terminal/q rows.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/uniform-diagonal-second-polar-fitting-gap.md":
        "abd35f7f9e2788bf194f95a76b3b4a7d2c6fbf574572e58c201046dbd9e1d7b3",
    "computations/verify_uniform_diagonal_second_polar_fitting_gap.py":
        "1a45ad1a913d8e43767596b191dc011457b24bbf908ad1b097911f692cf9487c",
    "notes/scalar-unit-carrier-moment-tower-hilbert-cauchy.md":
        "c9a58db12d8959a3b498c3e6b0ae54aeb49224476fb02d264d21d77d8a230855",
    "computations/verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py":
        "b1674da530c0af1790780bb19fadc7622117b373ece3e9a0845cbb532870e3f3",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
}
EXPECTED_LEDGER_SHA256 = (
    "97adf8a4adbafd8ce555388f671fa6831e986889f6703a809744ea82fb8d34c0"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: list[Fraction]) -> list[Fraction]:
    require(vectors, "empty vector sum")
    require(len({len(vector) for vector in vectors}) == 1,
            "vector width mismatch")
    return [sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True)]


def scale(value: Fraction, vector: list[Fraction]) -> list[Fraction]:
    return [value * entry for entry in vector]


def multiply_q(vector: list[Fraction], degree: int) -> list[Fraction]:
    """Ordinary q multiplication in divided-power r-degree order."""
    require(len(vector) == degree + 1, "q multiplication width")
    answer = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, entry in enumerate(vector):
        answer[r_degree] += Fraction(degree - r_degree + 1) * entry
    return answer


def multiply_r(vector: list[Fraction], degree: int) -> list[Fraction]:
    """Ordinary r multiplication in divided-power r-degree order."""
    require(len(vector) == degree + 1, "r multiplication width")
    answer = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, entry in enumerate(vector):
        answer[r_degree + 1] += Fraction(r_degree + 1) * entry
    return answer


def moment(h: int, s: int) -> list[Fraction]:
    return [Fraction(1, s + ell + 1) for ell in range(h - 1)]


def carrier(h: int, s: int) -> list[Fraction]:
    h_s = moment(h, s)
    return add(multiply_r(h_s, h - 2), scale(-2, multiply_q(h_s, h - 2)))


def relation_columns(h: int) -> list[list[Fraction]]:
    indices = [0, 1] if h == 3 else list(range(h - 2))
    columns = []
    for s in indices:
        c_s = carrier(h, s)
        columns.extend((multiply_q(c_s, h - 1), multiply_r(c_s, h - 1)))
    return columns


def clean(h: int) -> list[Fraction]:
    return [Fraction(int(j >= 2)) for j in range(h + 1)]


def target(h: int) -> list[Fraction]:
    return [Fraction(int(j <= 1)) for j in range(h + 1)]


def rows_from_columns(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    require(columns, "empty column matrix")
    require(len({len(column) for column in columns}) == 1,
            "column height mismatch")
    return [list(entries) for entries in zip(*columns, strict=True)]


def affine_solve(
    columns: list[list[Fraction]], target_vector: list[Fraction]
) -> tuple[list[Fraction] | None, list[list[Fraction]]]:
    """Return one solution and a basis of the homogeneous kernel."""
    rows = rows_from_columns(columns)
    require(len(rows) == len(target_vector), "solve height mismatch")
    work = [row + [rhs] for row, rhs in zip(rows, target_vector, strict=True)]
    row_count = len(work)
    variable_count = len(columns)
    pivot_columns = []
    pivot_row = 0
    for column in range(variable_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    if any(
        all(not work[row][column] for column in range(variable_count))
        and work[row][-1]
        for row in range(row_count)
    ):
        return None, []
    particular = [Fraction(0) for _ in range(variable_count)]
    for row, column in enumerate(pivot_columns):
        particular[column] = work[row][-1]
    free_columns = [
        column for column in range(variable_count)
        if column not in pivot_columns
    ]
    kernel = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(variable_count)]
        vector[free] = Fraction(1)
        for row, column in enumerate(pivot_columns):
            vector[column] = -work[row][free]
        kernel.append(vector)
    return particular, kernel


def linear_combination(
    coefficients: list[Fraction], columns: list[list[Fraction]]
) -> list[Fraction]:
    require(len(coefficients) == len(columns), "combination width mismatch")
    return add(*(
        scale(coefficient, column)
        for coefficient, column in zip(coefficients, columns, strict=True)
    ))


def matrix_rank(columns: list[list[Fraction]]) -> int:
    zero = [Fraction(0) for _ in range(len(columns[0]))]
    _particular, kernel = affine_solve(columns, zero)
    return len(columns) - len(kernel)


def h34_algebraic_audit() -> dict[str, object]:
    records = {}
    for h in (3, 4):
        columns = [clean(h)] + relation_columns(h)
        particular, kernel = affine_solve(columns, target(h))
        require(particular is not None, ("moment target not spanned", h))
        require(linear_combination(particular, columns) == target(h),
                ("particular solution failed", h))
        for relation in kernel:
            require(linear_combination(relation, columns)
                    == [Fraction(0) for _ in range(h + 1)],
                    ("kernel relation failed", h))
        require(matrix_rank(columns) == h + 1,
                ("full algebraic rank changed", h))
        require(len(kernel) == (1 if h == 3 else 0),
                ("affine freedom changed", h))
        records[h] = {
            "column_order": [
                "u"
            ] + [
                f"{multiplier}c_{s}"
                for s in ([0, 1] if h == 3 else list(range(h - 2)))
                for multiplier in ("q", "r")
            ],
            "columns": [[str(entry) for entry in column] for column in columns],
            "target": [str(entry) for entry in target(h)],
            "particular": [str(entry) for entry in particular],
            "kernel": [
                [str(entry) for entry in relation] for relation in kernel
            ],
        }
    return records


def augmented_membership_audit() -> dict[str, object]:
    """Verify the exact rank test after arbitrary additional readout rows."""
    records = {}
    for h in (3, 4):
        algebraic_columns = [clean(h)] + relation_columns(h)
        # Give every moment consequence its own unresolved physical row.
        extra_count = len(algebraic_columns) - 1
        augmented_columns = []
        for column_index, column in enumerate(algebraic_columns):
            extra = [Fraction(0) for _ in range(extra_count)]
            if column_index:
                extra[column_index - 1] = Fraction(1)
            augmented_columns.append(column + extra)
        augmented_target = target(h) + [Fraction(0) for _ in range(extra_count)]
        solution, _kernel = affine_solve(augmented_columns, augmented_target)
        require(solution is None,
                ("formal physical defects vanished without relations", h))

        # Add correction columns which kill those unresolved rows but have
        # zero algebraic shadow.  The membership test must then pass.
        corrections = []
        for row in range(extra_count):
            correction = [Fraction(0) for _ in range(h + 1 + extra_count)]
            correction[h + 1 + row] = Fraction(1)
            corrections.append(correction)
        repaired_solution, _ = affine_solve(
            augmented_columns + corrections, augmented_target
        )
        require(repaired_solution is not None,
                ("augmented correction criterion failed", h))
        require(
            matrix_rank(augmented_columns + corrections)
            == matrix_rank(augmented_columns + corrections + [augmented_target]),
            ("rank membership criterion failed", h),
        )
        records[h] = {
            "algebraic_rows": h + 1,
            "moment_consequence_columns": extra_count,
            "unresolved_augmented_rows_in_universal_guard": extra_count,
            "without_physical_relations": "target not in image",
            "with_zero-shadow_corrections": "target in image",
            "finite_test": "rank([A_aug C])=rank([A_aug C | x_aug])",
        }
    return records


def source_scope_audit() -> dict[str, object]:
    hasse = (ROOT / "notes/h3-hasse-coproduct-cosimplicial-totalization.md").read_text()
    moments = (ROOT / "notes/scalar-unit-carrier-moment-tower-hilbert-cauchy.md").read_text()
    second = (ROOT / "notes/uniform-diagonal-second-polar-fitting-gap.md").read_text()
    require("complete principal-parts source resolution" in hasse
            and "physical augmented correction complex" in hasse,
            "principal-parts/physical comparison frontier changed")
    require("is the only member of the moment family" in moments
            and r"prove \(c_0=0\)" in moments
            and r"Even \(c_0=0\) follows only" in moments,
            "first moment source frontier changed")
    require(r"orders \(2,\ldots,h\)" in second,
            "higher response-order target changed")
    return {
        "formal_Hasse_orders_2_through_h": (
            "source-valid in the complete principal-parts totalization"
        ),
        "physical_moment_relations": "not constructed",
        "first_missing_relation": (
            "c_0=(r-2q)H_0=0 in one physical degree-(h-1) module"
        ),
        "next_missing_moment_at_h3_h4": (
            "H_1 with the same affine density, endpoint ordering, and carrier"
        ),
        "multiplication_guard": (
            "q*c_s and r*c_s must be legal chain maps with zero protected, "
            "anchor, terminal, and q-cocycle indeterminacy"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3/h4 Hasse-moment augmented membership gate",
        "pins": PINS,
        "scope": source_scope_audit(),
        "algebraic_h3_h4": h34_algebraic_audit(),
        "augmented_membership": augmented_membership_audit(),
        "verdict": (
            "The complete principal-parts Hasse tower supplies formal orders "
            "2 through h, and the Hilbert-Cauchy matrix closes the scalar "
            "degree-h quotient at h=3,4. It does not construct the physical "
            "carrier relations. The first missing relation is already c_0=0; "
            "H_1 is then the next missing moment at both h=3 and h=4. After "
            "adjoining all protected/terminal/q rows, closure is exactly one "
            "finite column-membership rank test."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Hasse/moment augmented ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    for h in (3, 4):
        record = ledger["algebraic_h3_h4"][h]
        print(f"h={h} particular={record['particular']}")
        print(f"h={h} kernel={record['kernel']}")
    print("first physical missing relation: c_0=0")
    print("next missing moment at h=3,4: H_1")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
