#!/usr/bin/env python3
"""Reduce the balanced chart-square obstruction to private minus Eq.

In the four physical corners let ``B`` denote the private/lower boundary
and ``Eq`` the reduced-Eq boundary.  The committed cap columns tie them
diagonally, while the four signless K2,2 companion columns live only in B.
Their B/Eq projection has rank seven in eight coordinates.  Its primitive
left-kernel is

    Psi = delta . (B-Eq),       delta=(1,1,-1,-1).

Thus the balanced B-face is the unique projected cokernel class.  Cartan
placement, target/W/residue repair, the full-q/anchor family, and ridge
rows cannot affect this statement because they either live outside B/Eq or
tie B to Eq.  A future physical filler must have nonzero delta-weighted
private/Eq mismatch; if the exhaustive map has no such column, Psi is the
canonical terminal detector.

This checker proves the projection theorem.  It does not assert that an
arbitrary column with the right projection has all of its other augmented
faces repaired.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py":
        "10c2ca7ca9168d41f25f428b628710c0eaf8bc2aa910e23100da161869fdc72e",
    "notes/h3-balanced-square-pointed-full-q-cone-gate.md":
        "a81873b5e6f9b5c7c2e220b39dabd4fc74a7e1914690516b7727b578b04b9248",
    "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py":
        "3397fc0b7d773d97fb26e737eb490136c3062549951b07eca701ee46739ff2bb",
    "notes/h3-reduced-eq-cartan-cap-augmentation-dressing.md":
        "2fc3435835d72ed91608cc35245adeb2d65be605151247f991c8768972b6c255",
    "computations/verify_uniform_balanced_chart_square_master_obstruction.py":
        "306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
    "notes/uniform-balanced-chart-square-master-obstruction.md":
        "c758fb43f88d9c02f5200921c6c50637bfe04402536edc3e947f74d108fbd93b",
    "computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py":
        "cd445864a1440b89b213229c6795b409a9c49b84bf388dc4a476ed2030077e91",
    "notes/h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md":
        "fdb07cd655a0bd4dfa519c8c7faed8cafac105345737f44902b8127324f24a2a",
}
EXPECTED_LEDGER_SHA256 = "6949f42c3e22c9116cde405f1e57a1dc77b6473c7523176c20ba2aa4da0a7b76"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(rows: list[tuple[Q, ...]] | tuple[tuple[Q, ...], ...]) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(pivot_row, len(work))
                      if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for i in range(len(work)):
            if i == pivot_row or not work[i][column]:
                continue
            value = work[i][column]
            work[i] = [left - value * right for left, right in
                       zip(work[i], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def vec(*, B: tuple[int, int, int, int] = (0, 0, 0, 0),
        Eq: tuple[int, int, int, int] = (0, 0, 0, 0),
        target: tuple[int, int, int, int] = (0, 0, 0, 0),
        W: tuple[int, int, int, int] = (0, 0, 0, 0),
        ores: tuple[int, int, int, int] = (0, 0, 0, 0),
        M: int = 0, ainc: int = 0, q: int = 0, Pf: int = 0,
        ridge: int = 0, eta: int = 0, sigma: int = 0) -> tuple[Q, ...]:
    return tuple(map(Q, (*B, *Eq, *target, *W, *ores,
                         M, ainc, q, Pf, ridge, eta, sigma)))


def projection_audit() -> dict[str, object]:
    delta = (Q(1), Q(1), Q(-1), Q(-1))
    psi8 = delta + tuple(-x for x in delta)

    # Four cap/private-Eq diagonal columns.
    diagonal = []
    for j in range(4):
        e = tuple(1 if i == j else 0 for i in range(4))
        diagonal.append(tuple(map(Q, e + e)))

    # The four signless K2,2 mate columns: one vertex on each shore.
    # Vertex order is A0,A1,B0,B1, with delta positive on the A shore.
    companions = []
    for a in (0, 1):
        for b in (2, 3):
            B = tuple(1 if i in (a, b) else 0 for i in range(4))
            companions.append(tuple(map(Q, B + (0, 0, 0, 0))))

    old = tuple(diagonal + companions)
    balanced = tuple(map(Q, delta + (0, 0, 0, 0)))
    require(rank(old) == 7, "the projected old span stopped having rank 7")
    require(all(dot(psi8, column) == 0 for column in old),
            "private-minus-Eq stopped killing an old projected column")
    require(dot(psi8, balanced) == 4,
            "the balanced face changed primitive value")
    require(rank(old + (balanced,)) == 8,
            "the balanced face stopped generating the unique cokernel")

    # Exact positive and negative mutation controls.
    eq_only_delta = tuple(map(Q, (0, 0, 0, 0) + delta))
    tied_delta = tuple(map(Q, delta + delta))
    centered_edge = companions[0]
    require(dot(psi8, eq_only_delta) == -4
            and rank(old + (eq_only_delta,)) == 8,
            "the reduced-Eq-only positive control stopped filling projection")
    require(dot(psi8, tied_delta) == 0
            and rank(old + (tied_delta,)) == 7,
            "a tied private/Eq column incorrectly filled the projection")
    require(dot(psi8, centered_edge) == 0,
            "a signless shore-crossing edge stopped being centered")

    return {
        "row_order": ["B0", "B1", "B2", "B3",
                      "Eq0", "Eq1", "Eq2", "Eq3"],
        "delta": [1, 1, -1, -1],
        "primitive_left_kernel": [1, 1, -1, -1, -1, -1, 1, 1],
        "old_projection_rank": 7,
        "rank_with_balanced_B_face": 8,
        "value_on_balanced_B_face": 4,
        "Eq_only_delta_value": -4,
        "tied_B_Eq_delta_value": 0,
        "criterion": "delta dot (B-Eq) is nonzero",
    }


def augmented_named_family_audit() -> dict[str, object]:
    delta = (1, 1, -1, -1)
    zero = (0, 0, 0, 0)
    psi = vec(B=delta, Eq=tuple(-x for x in delta))

    columns: dict[str, tuple[Q, ...]] = {}
    for j in range(4):
        e = tuple(1 if i == j else 0 for i in range(4))
        columns[f"r0_{j}"] = vec(B=e, Eq=e, target=e,
                                  M=-1, ainc=-1, Pf=1)
        columns[f"T_{j}"] = vec(target=e,
                                 W=tuple(-x for x in e))
        columns[f"rho_{j}"] = vec(W=e, ores=e)

    alpha = (-1, 1, 1, -1)
    columns["Cartan"] = vec(ores=alpha, ridge=1, eta=1, sigma=-1)

    # Four K2,2 companion columns have a B shore-crossing edge and no Eq.
    for a in (0, 1):
        for b in (2, 3):
            edge = tuple(1 if i in (a, b) else 0 for i in range(4))
            columns[f"companion_{a}_{b}"] = vec(B=edge)

    # Strong pure-normalization columns and representative rows from the
    # full-q/anchor and ridge families.  Psi is zero on all their blocks.
    columns["pure_target_2"] = vec(target=(0, 0, 1, 0))
    columns["pure_target_3"] = vec(target=(0, 0, 0, 1))
    columns["literal_q_identity"] = vec(M=1, ainc=-1, q=-1)
    columns["pointed_anchor"] = vec(Pf=1)
    columns["ridge_only"] = vec(ridge=1)
    columns["eta_only"] = vec(eta=1)
    columns["sigma_only"] = vec(sigma=1)

    # The physical M_v and any relabelled Cartan/cap placement are allowed
    # to carry arbitrary other rows, but their B and Eq packets are tied.
    columns["M_v"] = vec(B=alpha, Eq=alpha, ores=alpha,
                          ridge=1, eta=1, sigma=-1)

    require(all(dot(psi, column) == 0 for column in columns.values()),
            [(name, dot(psi, column)) for name, column in columns.items()
             if dot(psi, column)])

    balanced = vec(B=delta)
    require(dot(psi, balanced) == 4,
            "the augmented detector lost the balanced face")

    # Placement invariance is symbolic: rows outside B/Eq are invisible,
    # and every tied B=Eq packet is killed for arbitrary coefficients.
    for test in ((2, -3, 5, 7), (-11, 4, 0, 6), delta):
        require(dot(psi, vec(B=test, Eq=test,
                             target=(3, 1, 4, 1),
                             W=(5, 9, 2, 6), ores=(5, 3, 5, 8),
                             M=9, ainc=-2, q=6, Pf=5,
                             ridge=3, eta=5, sigma=8)) == 0,
                ("tied-placement mutation failed", test))

    return {
        "named_columns_checked": sorted(columns),
        "named_column_count": len(columns),
        "canonical_augmented_dual": {
            "B": list(delta),
            "Eq": [-x for x in delta],
            "all_other_rows": 0,
        },
        "value_on_balanced_face": 4,
        "placement_invariance": (
            "arbitrary target/W/ores/q/anchor/ridge/eta/sigma data are "
            "invisible; arbitrary B=Eq packets are killed"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 balanced square private-minus-Eq projection gate",
        "pins": PINS,
        "projection": projection_audit(),
        "augmented_named_family": augmented_named_family_audit(),
        "verdict": (
            "The B/Eq projection of the committed cap diagonals and four "
            "K2,2 companions has rank seven in dimension eight.  Its unique "
            "primitive cokernel detector is delta.(B-Eq), delta=(1,1,-1,-1). "
            "It annihilates every named cap/Cartan/pure-target/full-q/anchor/"
            "ridge family and detects the balanced B face by four.  Hence a "
            "physical filler must break the delta-weighted B=Eq law.  If an "
            "exhaustive same-grade map preserves that law, this two-block "
            "functional is the canonical augmented terminal candidate."
        ),
        "scope": (
            "Exact h3 B/Eq projection and named-family dual extension.  A "
            "nonzero projection is necessary and projection-wise sufficient, "
            "but this checker does not repair arbitrary additional augmented "
            "faces of a proposed physical column and does not prove the full "
            "same-grade map exhaustive."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("balanced private/Eq ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h3 balanced square private-minus-Eq projection: PASS")
    print("old B/Eq rank: 7 -> 8 with balanced face")
    print("canonical detector: delta.(B-Eq)")
    print("filler projection criterion: delta.(B-Eq) != 0")
    print("ledger sha256:", digest)
    print(json.dumps(ledger, sort_keys=True))


if __name__ == "__main__":
    main()
