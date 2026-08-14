#!/usr/bin/env python3
"""Audit the chart-odd operation-tag obstruction to E2/E3 descent.

The model deliberately grants the strongest matching-direction input:
after pure-target normalization, the all-matching Koszul complex is
contractible, and common matching cores are treated as saturated.  The
physical undivided E2/E3 cells nevertheless lift diagonally to the two
chart presentations.  Their image cannot reach the chart-sign carrier.

This is an exact logical/source-typing guard.  It is not a full decorated
source computation.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PINNED = {
    "notes/uniform-bianchi-all-word-signed-kernel-gate.md":
        "13f0d45e91774dcc528b009aedc3d37779120bdefb6caa7d5b010b53cfd222a3",
    "computations/verify_uniform_bianchi_all_word_signed_kernel_gate.py":
        "5bcff5015ce56e9d7ba8ba9b57007080968540dac81429a6a695421ed2bd5338",
    "notes/uniform-strict-four-cut-homotopy-moment-collapse.md":
        "61e0b2267bb5b71253e9bcc4d94173b925851034754cf4f38842575f3bec56de",
    "computations/verify_uniform_strict_four_cut_homotopy_moment_collapse.py":
        "8910f6ce438257d310fce12b8f76c4639d2c42033950ab6ea7072bcca702bf1c",
    "notes/local-c4-coherence-curvature-relative-square.md":
        "5ed2232758948b993826d69158f6cdb57a06c077ad3a37af7db3a5005d9b9b43",
    "computations/verify_local_c4_relative_coherence_curvature_square.py":
        "9753c669db38b29e55706d4d8865c3beb46dcb0835298a90061babcda6483744",
    "computations/verify_n8_chart26_c4_exchange_3cell.py":
        "4398d15df3a5f0b34c2745fdb7087a289452ed03983d22431c4f20d116f019c6",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
    "notes/h3-direct-free-literal-four-face-full-nine-no-go.md":
        "5afe86e3785d8b467ccd0a2e0e26ad91a64a8e3855bb3ea18b054720c6f32606",
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def check_pins() -> None:
    for relative, expected in PINNED.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"source drift: {relative}: {actual}")


Vector = dict[tuple[int, ...], Fraction]


def add_term(vector: Vector, basis: tuple[int, ...], value: Fraction) -> None:
    new_value = vector.get(basis, Fraction(0)) + value
    if new_value:
        vector[basis] = new_value
    else:
        vector.pop(basis, None)


def koszul_d(vector: Vector, weights: list[Fraction]) -> Vector:
    answer: Vector = {}
    for basis, coefficient in vector.items():
        for position, index in enumerate(basis):
            reduced = basis[:position] + basis[position + 1:]
            add_term(answer, reduced,
                     coefficient * ((-1) ** position) * weights[index])
    return answer


def wedge_with_ones(vector: Vector, width: int) -> Vector:
    """Left wedge by u=e_0+...+e_(width-1)."""
    answer: Vector = {}
    for basis, coefficient in vector.items():
        present = set(basis)
        for index in range(width):
            if index in present:
                continue
            # e_index is placed at the left and then sorted.  It crosses
            # exactly the existing indices smaller than it.
            sign = (-1) ** sum(old < index for old in basis)
            enlarged = tuple(sorted((index,) + basis))
            add_term(answer, enlarged, coefficient * sign)
    return answer


def vector_add(first: Vector, second: Vector) -> Vector:
    answer = dict(first)
    for basis, value in second.items():
        add_term(answer, basis, value)
    return answer


def pure_matching_koszul_contraction(width: int) -> dict[str, int]:
    # Nonuniform exact weights make sum a_M=1, the pure hafnian
    # normalization.  The identity d h+h d=id is algebraic and therefore
    # audits the strongest possible all-matching saturation.
    denominator = width * (width + 1) // 2
    weights = [Fraction(index + 1, denominator) for index in range(width)]
    require(sum(weights) == 1, "pure matching weights do not sum to one")

    checked = 0
    for degree in range(width + 1):
        for basis in combinations(range(width), degree):
            vector = {basis: Fraction(1)}
            dh = koszul_d(wedge_with_ones(vector, width), weights)
            hd = wedge_with_ones(koszul_d(vector, weights), width)
            require(vector_add(dh, hd) == vector,
                    f"Koszul contraction failed at width={width}, basis={basis}")
            checked += 1
    return {"matching_width": width, "basis_cells_checked": checked}


def chart_operation_tag_audit() -> dict[str, object]:
    # Once the matching complex is contracted, a global physical cell has
    # diagonal chart boundary (1,1).  beta/t is the sign vector (1,-1).
    diagonal = (Fraction(1), Fraction(1))
    beta = (Fraction(1), Fraction(-1))
    sign_readout = (Fraction(1), Fraction(-1))

    require(diagonal[0] * beta[1] - diagonal[1] * beta[0] != 0,
            "beta accidentally entered the diagonal line")
    require(sum(sign_readout[i] * diagonal[i] for i in range(2)) == 0,
            "sign readout sees a global diagonal exchange cell")
    require(sum(sign_readout[i] * beta[i] for i in range(2)) == 2,
            "sign readout stopped detecting beta")

    # The global diagonal cell has rank one in the two chart coordinates.
    # Adding precisely one chart-odd operation cell makes the boundary rank
    # two and kills beta.
    determinant_with_odd_cell = (
        diagonal[0] * beta[1] - diagonal[1] * beta[0]
    )
    require(determinant_with_odd_cell == -2,
            "chart-odd attachment no longer kills the sign cokernel")
    return {
        "global_exchange_boundary": list(diagonal),
        "operation_tag_class": list(beta),
        "global_boundary_rank": 1,
        "rank_after_chart_odd_attachment": 2,
        "signed_readout_on_beta": 2,
    }


def strict_four_cut_sign_audit() -> dict[str, object]:
    # Coordinates are (q,r,x).  The desired common primitive exists only
    # after the chart-odd gluing class is killed; its boundary sign is then
    # forced by the two oriented factors.
    k_right = (1, 0, -1)
    k_left = (1, -1, 1)
    common_boundary = tuple(-(a + b) for a, b in zip(k_right, k_left))
    require(common_boundary == (-2, 1, 0),
            "strict common four-cut sign changed")
    return {
        "K_right": k_right,
        "K_left": k_left,
        "dGamma": common_boundary,
        "meaning": "r-2q after chart-odd descent",
    }


def mutation_guards() -> None:
    weights = [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)]
    require(sum(weights) == 1, "control pure normalization failed")
    mutated = [Fraction(1, 3), Fraction(1, 3), Fraction(1, 4)]
    require(sum(mutated) != 1,
            "missing pure normalization mutation was not detected")

    diagonal = (1, 1)
    wrongly_tagged = (1, 1)
    require(diagonal[0] * wrongly_tagged[1]
            - diagonal[1] * wrongly_tagged[0] == 0,
            "diagonal-copy mutation unexpectedly killed operation Tor")


def main() -> None:
    check_pins()
    contractions = [pure_matching_koszul_contraction(width)
                    for width in range(2, 8)]
    tag = chart_operation_tag_audit()
    strict = strict_four_cut_sign_audit()
    mutation_guards()
    ledger = (contractions, tag, strict)
    digest = hashlib.sha256(repr(ledger).encode()).hexdigest()
    print("PASS: uniform chart-odd matching-exchange operation-tag Tor gate")
    print("all-matching pure-target Koszul complex: CONTRACTIBLE")
    print("physical E2/E3 lift: CHART-DIAGONAL")
    print("universal beta/t: SURVIVES IN CHART-SIGN COKERNEL")
    print("dGamma=r-2q: REQUIRES ONE CHART-ODD ATTACHMENT")
    print(f"digest: {digest}")


if __name__ == "__main__":
    main()
