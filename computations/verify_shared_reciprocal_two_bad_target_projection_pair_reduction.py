#!/usr/bin/env python3
"""Exact target-projection pair reduction for the mixed two-bad gate.

The pinned Rees unit excludes every target projection with three nonzero
coordinates.  Over C, a linear subspace all of whose vectors have support
at most two is contained in one fixed coordinate pair.

For K=ker(Phi), N=ker(pi_t|K), and the bilinear kernel-product map T, the
canonical residual

    R_nt = image(A1 tensor (N*K)) in coker(Phi)

absorbs every product containing a target-free kernel factor.  Modulo this
residual, T factors through Sym^2(pi_t K), hence through one fixed pair.
The committed rational common-power packet is rebuilt to show that R_nt is
not generally zero modulo im(Phi), although in that guard it does not hit
the missing pure target class.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import verify_shared_reciprocal_two_bad_quotient as quotient


PINNED_REES_SHA256 = (
    "1f6e581fec653332e366add3bc36b8edf0861c0a76f1ee8373a69ab2605ccb4a"
)
PINNED_QUOTIENT_SHA256 = (
    "7ada76d6a0ff2fb8a7413c15d8a5e8e741a90383437658ea18209b57bb0a6285"
)
EXPECTED_LEDGER_SHA256 = "ac60460e15ee82ff95d0abba8ff1cd9f0efe114aa30e40a6e4a582edc929625e"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    pins = {
        "computations/verify_shared_reciprocal_two_bad_mixed_two_hole_rees_unit.py":
            PINNED_REES_SHA256,
        "computations/verify_shared_reciprocal_two_bad_quotient.py":
            PINNED_QUOTIENT_SHA256,
    }
    for relative, expected in pins.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"dependency changed: {relative}: {actual}")


def audit_coordinate_pair_lemma():
    # If W is not contained in one coordinate pair, the union of the
    # supports of its vectors contains at least three coordinates.  For
    # each such coordinate i, the restriction ell_i of the i-th coordinate
    # functional to W is nonzero.  The product of these nonzero linear
    # forms is nonzero in Sym(W*), so over the infinite field C it has a
    # point outside its zero set.  That point has all union coordinates
    # nonzero, contradicting the support-at-most-two hypothesis.
    sites = tuple(range(5))
    pair_masks = tuple(
        frozenset(subset)
        for size in range(3)
        for subset in itertools.combinations(sites, size)
    )
    require(len(pair_masks) == 16,
            "the five-coordinate support-pair census changed")
    require(all(len(mask) <= 2 for mask in pair_masks),
            "an allowed projection mask exceeded a pair")

    # Record the exact finite-field guard: infinitude is load-bearing.
    # Over F2 the span of 110 and 101 is {000,110,101,011}; every vector
    # has support <=2, but the subspace is not contained in one pair.
    f2_span = {
        tuple((a * x + b * y) % 2 for x, y in zip((1, 1, 0), (1, 0, 1)))
        for a, b in itertools.product(range(2), repeat=2)
    }
    require(f2_span == {(0, 0, 0), (1, 1, 0),
                        (1, 0, 1), (0, 1, 1)},
            "the finite-field mutation guard changed")
    require(max(sum(value != 0 for value in vector)
                for vector in f2_span) == 2,
            "the F2 guard acquired a three-support vector")
    require({index for vector in f2_span for index, value
             in enumerate(vector) if value} == {0, 1, 2},
            "the F2 guard fell into one coordinate pair")

    return {
        "ambient_coordinates": 5,
        "allowed_coordinate_subspaces": len(pair_masks),
        "proof": (
            "the product of the nonzero restricted coordinate forms is "
            "a nonzero polynomial; over C it has a nonvanishing point"
        ),
        "conclusion": "pi_t(ker Phi) is contained in C^S for one |S|<=2",
        "dimension_bound": 2,
        "finite_field_guard": "span_F2{110,101} has union 3 but max support 2",
    }


def add_vectors(left, right):
    out = defaultdict(Fraction)
    for key, value in left.items():
        out[key] += value
    for key, value in right.items():
        out[key] += value
    return {key: value for key, value in out.items() if value}


def scale_vector(vector, scalar):
    return {key: scalar * value for key, value in vector.items()
            if scalar * value}


def symmetric_product(left, right):
    out = defaultdict(Fraction)
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            key = tuple(sorted((left_key, right_key)))
            out[key] += left_value * right_value
    return {key: value for key, value in out.items() if value}


def modulo_target_free_residual(vector):
    return {
        key: value for key, value in vector.items()
        if all(not factor.startswith("n") for factor in key)
    }


def audit_canonical_quotient_factorization():
    # K=N+H with N=<n0,n1> and H a chosen lift of W=<h0,h1>.
    # Change the section H -> H+N arbitrarily.  Every difference of
    # symmetric products contains an N factor and therefore dies modulo
    # N*K.  This is the universal section-independence calculation.
    old = {
        "h0": {"h0": Fraction(1)},
        "h1": {"h1": Fraction(1)},
    }
    new = {
        "h0": {"h0": Fraction(1), "n0": Fraction(2),
                "n1": Fraction(-3)},
        "h1": {"h1": Fraction(1), "n0": Fraction(5),
                "n1": Fraction(7)},
    }
    checked = []
    for left_index, left in enumerate(("h0", "h1")):
        for right in ("h0", "h1")[left_index:]:
            old_product = symmetric_product(old[left], old[right])
            new_product = symmetric_product(new[left], new[right])
            difference = add_vectors(
                new_product, scale_vector(old_product, Fraction(-1))
            )
            require(modulo_target_free_residual(difference) == {},
                    "a section change survived modulo N*K")
            require(modulo_target_free_residual(new_product)
                    == modulo_target_free_residual(old_product),
                    "the induced Sym^2(W) product depends on the section")
            checked.append(f"{left}{right}")
    require(checked == ["h0h0", "h0h1", "h1h1"],
            "the fixed-pair symmetric-square basis changed")
    return {
        "kernel_exact_sequence": "0 -> N -> ker(Phi) -> W -> 0",
        "N": "ker(pi_t|ker(Phi))",
        "residual": "R_nt=image(A1 tensor (N*ker(Phi))) in coker(Phi)",
        "factored_domain": "A1 tensor Sym^2(W)",
        "maximum_symmetric_square_dimension": 3,
        "section_change_checks": checked,
    }


def build_counterguard_packet():
    c = sp.Rational(3, 5)
    s = sp.Rational(4, 5)
    sites = (1, 2, 3, 4, 5)
    target = 2
    cells = {}
    for left, right, colour, value in (
        (2, 3, 0, c), (1, 3, 0, s), (4, 5, 0, 1),
        (1, 2, 1, 1), (3, 4, 1, 1),
    ):
        quotient.put(cells, left, right, colour, colour, value)

    basis = tuple(itertools.product(range(3), repeat=5))
    labels = []
    columns = []
    for hole in sites:
        cofactor_sites = tuple(site for site in sites if site != hole)
        cofactor = quotient.matching_tensor(cofactor_sites, cells)
        for colour in range(3):
            labels.append((hole, colour))
            tensor = quotient.insert_missing(
                cofactor, cofactor_sites, hole, {colour: 1}
            )
            columns.append(sp.Matrix([
                tensor.get(word, 0) for word in basis
            ]))
    phi = sp.Matrix.hstack(*columns)
    kernel_basis = phi.nullspace()
    kernel_matrix = sp.Matrix.hstack(*kernel_basis)
    projection = sp.zeros(len(sites), len(labels))
    for index, site in enumerate(sites):
        projection[index, labels.index((site, target))] = 1
    projected = projection * kernel_matrix
    target_free_coefficients = projected.nullspace()
    target_free = [kernel_matrix * vector
                   for vector in target_free_coefficients]

    require(phi.rank() == 11 and len(kernel_basis) == 4,
            "the rational counterguard cofactor ranks changed")
    require(projected.rank() == 1 and len(target_free) == 3,
            "the rational counterguard target projection changed")

    def vector_as_rows(vector):
        rows = {}
        for index, value in enumerate(vector):
            if value:
                site, colour = labels[index]
                rows.setdefault(site, {})[colour] = value
        return rows

    def product_column(p_vector, u_vector, v_vector):
        answer = defaultdict(lambda: sp.S.Zero)
        for x, p_row in vector_as_rows(p_vector).items():
            for y, u_row in vector_as_rows(u_vector).items():
                for z, v_row in vector_as_rows(v_vector).items():
                    if len({x, y, z}) < 3:
                        continue
                    edge = tuple(sorted(set(sites) - {x, y, z}))
                    for (candidate, left, right), edge_value in cells.items():
                        if candidate != edge:
                            continue
                        for p_colour, p_value in p_row.items():
                            for u_colour, u_value in u_row.items():
                                for v_colour, v_value in v_row.items():
                                    colouring = {
                                        x: p_colour, y: u_colour,
                                        z: v_colour, edge[0]: left,
                                        edge[1]: right,
                                    }
                                    word = tuple(colouring[site]
                                                 for site in sites)
                                    answer[word] += (
                                        p_value * u_value * v_value
                                        * edge_value
                                    )
        return sp.Matrix([sp.simplify(answer[word]) for word in basis])

    p_basis = []
    for index in range(len(labels)):
        vector = sp.zeros(len(labels), 1)
        vector[index] = 1
        p_basis.append(vector)
    residual_columns = [
        product_column(p_vector, n_vector, k_vector)
        for p_vector in p_basis
        for n_vector in target_free
        for k_vector in kernel_basis
    ]
    residual_matrix = sp.Matrix.hstack(*residual_columns)
    augmented = phi.row_join(residual_matrix)
    pure = [
        sp.Matrix([int(word == (colour,) * 5) for word in basis])
        for colour in range(3)
    ]
    pure_matrix = sp.Matrix.hstack(*pure)
    pure_intersection = (
        augmented.rank() + 3 - augmented.row_join(pure_matrix).rank()
    )
    require(residual_matrix[basis.index((target,) * 5), :] ==
            sp.zeros(1, residual_matrix.cols),
            "a target-free residual product acquired a raw X_t coefficient")
    require(residual_matrix.rank() == 6 and augmented.rank() == 16,
            "the target-free residual quotient rank changed")
    require(augmented.rank() > phi.rank(),
            "the target-free residual became absorbable into im(Phi)")
    require(pure_intersection == 2,
            "the counterguard residual acquired a third pure class")
    require(augmented.row_join(pure[target]).rank() == augmented.rank() + 1,
            "X_t entered the counterguard target-free residual")

    # Recheck the pinned full guard as a source-provenance mutation test.
    summary = quotient.audit_binary_common_power_packet()
    require(summary[0] == 11 and summary[1] == 4
            and summary[3] == 16 and summary[4] == 2,
            "the pinned full common-power guard changed")

    return {
        "phi_rank": phi.rank(),
        "kernel_dimension": len(kernel_basis),
        "target_projection_dimension": projected.rank(),
        "target_free_kernel_dimension": len(target_free),
        "target_free_product_rank": residual_matrix.rank(),
        "image_plus_residual_rank": augmented.rank(),
        "residual_cokernel_dimension": augmented.rank() - phi.rank(),
        "pure_intersection_dimension": pure_intersection,
        "Xt_in_image_plus_residual": False,
        "guard_verdict": (
            "R_nt is nonzero modulo im(Phi), so it cannot be discarded; "
            "this packet nevertheless keeps X_t outside"
        ),
    }


def main():
    pin_dependencies()
    pair = audit_coordinate_pair_lemma()
    factorization = audit_canonical_quotient_factorization()
    counterguard = build_counterguard_packet()
    ledger = {
        "pinned_rees_sha256": PINNED_REES_SHA256,
        "pinned_quotient_sha256": PINNED_QUOTIENT_SHA256,
        "coordinate_pair_lemma": pair,
        "canonical_residual_factorization": factorization,
        "rational_target_free_counterguard": counterguard,
        "verdict": (
            "the target projection of ker(Phi) lies in one fixed pair; "
            "modulo the canonical target-free residual the kernel-product "
            "map factors through a three-dimensional Sym^2 pair, while "
            "the residual is load-bearing and remains a separate branch"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the target-projection pair ledger changed: {digest}")

    print("shared reciprocal target-projection pair reduction: PASS")
    print("pi_t(ker Phi): one fixed coordinate pair, dimension <=2")
    print("quotient product domain: A1 tensor Sym^2(W), dimension <=3 per P")
    print("target-free residual guard: nonzero in coker, X_t still outside")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
