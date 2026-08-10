#!/usr/bin/env python3
r"""Exact mixed normalized-bar / physical-curvature bicomplex at h=3.

The horizontal interval has dE=L-D.  The vertical selected normal row has
boundary kappa*z, where the complete physical identity is

    U f + t H - F g - y N - D_c v = kappa z.

This checker builds the tensor square, expands every normalized-bar
Leibniz commutator, and verifies the Massey lift

    M = D(n) + H_bar(kappa*z),       dM = L(kappa*z).

Thus the D endpoint cancels algebraically.  The complete seven-site word
change also has zero target.  Under the committed old-cap landing, however,
the L endpoint has q-augmentation and ordinary residue both kappa, while
every bar edge has augmentation zero.  The residue face therefore survives.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "notes/h3-local-gl3-normalized-bar-word-change-obstruction.md":
        "a12f8685ecd98a1ad71a2e7829acbe00ba2db597559ad8e726d42105aed60d20",
    "computations/verify_h3_physical_curvature_qzero_attaching_lower_face_obstruction.py":
        "050bfaa16cedb07248f01f58f8cc59927307861e55da45b759219ccde3d24ee1",
    "notes/h3-physical-curvature-qzero-attaching-lower-face-obstruction.md":
        "ec74fe80e80eb62e7f9ba3a0db7c59ddfff1a2f7d40829cd1f2905f9d869ddfa",
}
EXPECTED_LEDGER_SHA256 = "63f0ed1a39231f581a498b8fb4d1fda41ef5eec791f1b0fb4e3bb46138def6f2"

Polynomial = dict[tuple[str, ...], Q]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def constant(value=ONE) -> Polynomial:
    value = Q(value)
    return {(): value} if value else {}


def variable(name: str) -> Polynomial:
    return {(name,): ONE}


def add(*polynomials: Polynomial) -> Polynomial:
    result = defaultdict(Q)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def scale(value, polynomial: Polynomial) -> Polynomial:
    value = Q(value)
    return {monomial: value * coefficient
            for monomial, coefficient in polynomial.items()
            if value * coefficient}


def multiply(*polynomials: Polynomial) -> Polynomial:
    result = constant()
    for polynomial in polynomials:
        output = defaultdict(Q)
        for left, left_coefficient in result.items():
            for right, right_coefficient in polynomial.items():
                output[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        result = {monomial: coefficient
                  for monomial, coefficient in output.items() if coefficient}
    return result


def endpoint(polynomial: Polynomial, prefix: str) -> Polynomial:
    require(prefix in ("D", "L"), "unknown bar endpoint")
    return {
        tuple(sorted(f"{prefix}:{item}" for item in monomial)): coefficient
        for monomial, coefficient in polynomial.items()
    }


def bar_homotopy(polynomial: Polynomial) -> Polynomial:
    """Ordered normalized multiplicative homotopy from D to L.

    On x_1...x_n it is
      sum_i D(x_1)...D(x_{i-1}) E(x_i) L(x_{i+1})...L(x_n).
    This includes every Leibniz commutator and has dH=L-D.
    """
    output = defaultdict(Q)
    for monomial, coefficient in polynomial.items():
        for index, item in enumerate(monomial):
            factors = (
                tuple(f"D:{left}" for left in monomial[:index])
                + (f"E:{item}",)
                + tuple(f"L:{right}" for right in monomial[index + 1:])
            )
            output[tuple(sorted(factors))] += coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def bar_differential(polynomial: Polynomial) -> Polynomial:
    """Differential of a polynomial with at most one degree-one E label."""
    output = defaultdict(Q)
    for monomial, coefficient in polynomial.items():
        edge_positions = [
            index for index, item in enumerate(monomial)
            if item.startswith("E:")
        ]
        require(len(edge_positions) <= 1, "higher bar degree not expected")
        if not edge_positions:
            continue
        position = edge_positions[0]
        base = monomial[position][2:]
        for prefix, sign in (("L", ONE), ("D", -ONE)):
            replaced = list(monomial)
            replaced[position] = f"{prefix}:{base}"
            output[tuple(sorted(replaced))] += sign * coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def evaluate_augmentation(polynomial: Polynomial, values: dict[str, Q]) -> Q:
    result = ZERO
    for monomial, coefficient in polynomial.items():
        term = coefficient
        for item in monomial:
            prefix, base = item.split(":", 1)
            if prefix == "E":
                term = ZERO
                break
            require(prefix in ("D", "L"), f"unknown bar label {prefix}")
            term *= values[base]
        result += term
    return result


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def physical_normal_packet():
    A, B, Fc, U = (variable(name) for name in ("A", "B", "F", "U"))
    z, x, y, t, v, Ecoef = (
        variable(name) for name in ("z", "x", "y", "t", "v", "Ecoef")
    )
    f = add(multiply(A, z), multiply(x, y))
    g = add(multiply(B, z), multiply(x, t))
    Hnormal = add(multiply(A, v), multiply(Ecoef, y), multiply(Fc, x))
    Nnormal = add(multiply(B, v), multiply(Ecoef, t), multiply(U, x))
    Dconnection = add(multiply(A, t), scale(-ONE, multiply(B, y)))
    kappa = add(multiply(A, U), scale(-ONE, multiply(B, Fc)))
    correction_terms = {
        "U*f": multiply(U, f),
        "t*H": multiply(t, Hnormal),
        "-F*g": scale(-ONE, multiply(Fc, g)),
        "-y*N": scale(-ONE, multiply(y, Nnormal)),
        "-D_c*v": scale(-ONE, multiply(Dconnection, v)),
    }
    normal_boundary = add(*correction_terms.values())
    curvature = multiply(kappa, z)
    require(normal_boundary == curvature,
            "the complete physical normal identity changed")
    return correction_terms, normal_boundary, kappa, z


def audit_bicomplex(values: dict[str, Q]):
    correction_terms, normal_boundary, kappa, z = physical_normal_packet()
    curvature = multiply(kappa, z)

    # Every individual product obeys the normalized multiplicative homotopy
    # formula. This explicitly retains the five physical correction terms.
    term_records = {}
    for label, term in correction_terms.items():
        homotopy = bar_homotopy(term)
        require(
            bar_differential(homotopy)
            == add(endpoint(term, "L"), scale(-ONE, endpoint(term, "D"))),
            f"bar Leibniz commutator failed on {label}",
        )
        term_records[label] = len(homotopy)

    h_normal = bar_homotopy(normal_boundary)
    h_curvature = bar_homotopy(curvature)
    require(h_normal == h_curvature,
            "bar homotopy did not preserve the normal identity")
    require(
        bar_differential(h_curvature)
        == add(endpoint(curvature, "L"),
               scale(-ONE, endpoint(curvature, "D"))),
        "curvature bar boundary is not L(kappa z)-D(kappa z)",
    )

    # Full Leibniz expansion:
    # H(kappa*z)=H(kappa)L(z)+D(kappa)H(z), and
    # H(kappa)=H(A)L(U)+D(A)H(U)-H(B)L(F)-D(B)H(F).
    h_kappa = bar_homotopy(kappa)
    expected_h_kappa = add(
        multiply(bar_homotopy(variable("A")), endpoint(variable("U"), "L")),
        multiply(endpoint(variable("A"), "D"), bar_homotopy(variable("U"))),
        scale(-ONE, multiply(
            bar_homotopy(variable("B")), endpoint(variable("F"), "L")
        )),
        scale(-ONE, multiply(
            endpoint(variable("B"), "D"), bar_homotopy(variable("F"))
        )),
    )
    require(h_kappa == expected_h_kappa,
            "the determinant Leibniz commutators changed")
    expected_h_curvature = add(
        multiply(h_kappa, endpoint(z, "L")),
        multiply(endpoint(kappa, "D"), bar_homotopy(z)),
    )
    require(h_curvature == expected_h_curvature,
            "the outer curvature Leibniz commutator changed")

    # Tensor-square boundary. Let n be the physical normal-row chain with
    # dn=kappa*z. The degree-two product E(n) has boundary
    #   L(n)-D(n)-H(kappa*z).
    # Its boundary squares to zero by the preceding identity.
    square_boundary_squared = add(
        endpoint(curvature, "L"),
        scale(-ONE, endpoint(curvature, "D")),
        scale(-ONE, bar_differential(h_curvature)),
    )
    require(not square_boundary_squared, "mixed bicomplex does not square")

    # The associated Massey chain is M=D(n)+H(kappa*z). Its boundary is the
    # single desired L endpoint.
    massey_boundary = add(
        endpoint(curvature, "D"),
        bar_differential(h_curvature),
    )
    require(massey_boundary == endpoint(curvature, "L"),
            "D endpoint did not cancel in the Massey boundary")

    # Normalized augmentation sends D,L to the same physical coefficient
    # and every E edge to zero. The bar correction therefore cannot alter
    # the old-cap equality qaug=ordinary residue.
    augmented_l = evaluate_augmentation(endpoint(curvature, "L"), values)
    augmented_d = evaluate_augmentation(endpoint(curvature, "D"), values)
    augmented_edge = evaluate_augmentation(h_curvature, values)
    kappa_value = values["A"] * values["U"] - values["B"] * values["F"]
    expected = kappa_value * values["z"]
    require(augmented_l == augmented_d == expected,
            "the two normalized endpoint augmentations diverged")
    require(augmented_edge == 0, "a normalized bar edge acquired residue")
    require(expected != 0, "the active curvature probe vanished")
    old_readout = (augmented_l, augmented_l)
    desired_invisible = (augmented_l, ZERO)
    readout_determinant = (
        old_readout[0] * desired_invisible[1]
        - old_readout[1] * desired_invisible[0]
    )
    require(readout_determinant == -(expected ** 2) and readout_determinant,
            "the invisible endpoint entered the old augmented span")

    return {
        "values": {name: str(value) for name, value in sorted(values.items())},
        "kappa": str(kappa_value),
        "normal_correction_homotopy_terms": term_records,
        "H_kappa_terms": len(h_kappa),
        "H_kappa_z_terms": len(h_curvature),
        "mixed_square_d2": 0,
        "massey_boundary": "L(kappa*z)",
        "D_endpoint_cancelled": True,
        "bar_edge_augmentation": str(augmented_edge),
        "L_q_augmentation": str(augmented_l),
        "L_old_ordinary_residue": str(augmented_l),
        "old_readout_rank": 1,
        "rank_with_invisible_endpoint": 2,
        "target_complete_seven_site_word": 0,
        "invisible_endpoint_obtained": False,
    }


def main() -> None:
    pin_dependencies()
    # The complete seven-site word 1211222 contains both input colours, so
    # the all-L endpoint kills the ternary GHZ target. The endpoint-only
    # triples (m_v,2,2) remain nonzero on exactly the two m_v=2 faces.
    odd_word = (1, 2, 1, 1, 2)
    endpoint_target_survivors = sum(
        len({middle, 2}) == 1 for middle in odd_word
    )
    require(endpoint_target_survivors == 2,
            "endpoint-only target survivor count changed")
    full_word = (1, 2, 1, 1, 2, 2, 2)
    require(set(full_word) == {1, 2},
            "complete word change stopped being target-zero")

    samples = (
        {"A": Q(2), "B": Q(3), "F": Q(5), "U": Q(11), "z": Q(1),
         "x": Q(7), "y": Q(-2), "t": Q(4), "v": Q(3),
         "Ecoef": Q(5, 2)},
        {"A": Q(3), "B": Q(0), "F": Q(2), "U": Q(5), "z": Q(1),
         "x": Q(-1), "y": Q(6), "t": Q(2), "v": Q(-4),
         "Ecoef": Q(7)},
        {"A": Q(-2), "B": Q(7), "F": Q(3), "U": Q(-5), "z": Q(2),
         "x": Q(4), "y": Q(1), "t": Q(-3), "v": Q(5),
         "Ecoef": Q(-1, 3)},
    )
    records = [audit_bicomplex(sample) for sample in samples]
    ledger = {
        "pins": PINS,
        "bar_interval": "dE=L-D; epsilon(D)=epsilon(L)=1, epsilon(E)=0",
        "physical_normal_boundary": (
            "U*f+t*H-F*g-y*N-D_c*v=kappa*z, kappa=A*U-B*F"
        ),
        "mixed_product_boundary": (
            "d E(n)=L(n)-D(n)-H_bar(kappa*z)"
        ),
        "massey_chain": "M=D(n)+H_bar(kappa*z)",
        "massey_boundary": "dM=L(kappa*z)",
        "endpoint_only_target_survivors": endpoint_target_survivors,
        "complete_word_target": 0,
        "records": records,
        "verdict": (
            "the mixed bicomplex cancels D and target and leaves the desired "
            "L polynomial endpoint, but its committed ordinary residue is "
            "kappa rather than zero; no invisible attaching chain results"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"mixed bar-curvature ledger changed: {digest}")

    print("h=3 mixed bar-curvature bicomplex: PASS")
    print("all normal-row and determinant Leibniz commutators: exact")
    print("Massey boundary: D cancels and L(kappa*z) survives")
    print("complete word-change target: zero")
    print("committed ordinary residue: kappa (nonzero)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
