#!/usr/bin/env python3
"""Exact audits for ``notes/two-deletion-quotient-level-algebra.md``.

The cap quotient is a two-step graded algebra.  This script checks two
finite abstract models of all identities which survive in that quotient.

* The 8-dimensional colour-symmetric model has Hilbert function (1,3,4),
  nonzero Q independent of the three target lifts, and P_c=S_c.  It is the
  smallest generic-Q model and has no nontrivial idempotents.
* The 11-dimensional universal model realizes an arbitrary asymmetric
  direct-pair matrix a_cd.  Endpoint reversal carries the model for a to
  the model for a^T exactly.

Both models are commutative and associative; all products of three
positive-degree elements vanish.  Thus the checks concern the quotient
algebra inference, not realization by a physical site quadratic q.
"""

from __future__ import annotations

import itertools

import sympy as sp


KAPPA = sp.Rational(3)  # the n=8 normalization m-1


class FiniteAlgebra:
    def __init__(self, basis, degrees, products):
        self.basis = tuple(basis)
        self.index = {name: i for i, name in enumerate(self.basis)}
        self.degrees = tuple(degrees)
        self.dimension = len(self.basis)
        self.products = products

    def unit(self, name):
        vector = sp.zeros(self.dimension, 1)
        vector[self.index[name]] = 1
        return vector

    def multiply(self, left, right):
        answer = sp.zeros(self.dimension, 1)
        for i in range(self.dimension):
            if left[i] == 0:
                continue
            for j in range(self.dimension):
                if right[j] == 0:
                    continue
                key = tuple(sorted((i, j)))
                answer += left[i] * right[j] * self.products.get(
                    key, sp.zeros(self.dimension, 1)
                )
        return sp.simplify(answer)


def add_product(products, algebra_basis, left, right, terms):
    index = {name: i for i, name in enumerate(algebra_basis)}
    vector = sp.zeros(len(algebra_basis), 1)
    for name, coefficient in terms.items():
        vector[index[name]] += coefficient
    products[tuple(sorted((index[left], index[right])))] = vector


def audit_algebra_axioms(algebra):
    units = [algebra.unit(name) for name in algebra.basis]
    one = units[0]
    for vector in units:
        assert algebra.multiply(one, vector) == vector
        assert algebra.multiply(vector, one) == vector
    for left, right in itertools.product(units, repeat=2):
        assert algebra.multiply(left, right) == algebra.multiply(right, left)
    for left, middle, right in itertools.product(units, repeat=3):
        assert algebra.multiply(algebra.multiply(left, middle), right) == (
            algebra.multiply(left, algebra.multiply(middle, right))
        )

    positive = [
        vector for vector, degree in zip(units, algebra.degrees) if degree > 0
    ]
    for left, middle, right in itertools.product(positive, repeat=3):
        assert algebra.multiply(algebra.multiply(left, middle), right) == sp.zeros(
            algebra.dimension, 1
        )


def symmetric_minimal_model():
    basis = ("1", "e0", "e1", "e2", "y0", "y1", "y2", "Q")
    degrees = (0, 1, 1, 1, 2, 2, 2, 2)
    products = {}
    for name in basis:
        add_product(products, basis, "1", name, {name: 1})
    for colour in range(3):
        add_product(
            products,
            basis,
            f"e{colour}",
            f"e{colour}",
            {f"y{colour}": 1 / KAPPA},
        )
    return FiniteAlgebra(basis, degrees, products)


def audit_symmetric_model():
    algebra = symmetric_minimal_model()
    audit_algebra_axioms(algebra)

    # P_c=S_c=e_c, a_cd=0, and H(y_c)=X_c.  The cap table is exact and Q
    # is independent of all three target lifts.
    for c, d in itertools.product(range(3), repeat=2):
        cap_class = KAPPA * algebra.multiply(
            algebra.unit(f"e{c}"), algebra.unit(f"e{d}")
        )
        expected = algebra.unit(f"y{c}") if c == d else sp.zeros(8, 1)
        assert cap_class == expected
    target_lifts = sp.Matrix.hstack(
        *(algebra.unit(f"y{colour}") for colour in range(3))
    )
    with_q = sp.Matrix.hstack(target_lifts, algebra.unit("Q"))
    assert target_lifts.rank() == 3
    assert with_q.rank() == 4

    # Every colour permutation is an algebra automorphism fixing Q.
    for permutation in itertools.permutations(range(3)):
        images = {"1": "1", "Q": "Q"}
        for colour in range(3):
            images[f"e{colour}"] = f"e{permutation[colour]}"
            images[f"y{colour}"] = f"y{permutation[colour]}"
        matrix = sp.zeros(8, 8)
        for source, target in images.items():
            matrix[algebra.index[target], algebra.index[source]] = 1
        for left, right in itertools.product(
            (algebra.unit(name) for name in algebra.basis), repeat=2
        ):
            assert matrix * algebra.multiply(left, right) == algebra.multiply(
                matrix * left, matrix * right
            )

    # Direct coefficient audit of idempotents.  For x=alpha*1+n, the scalar
    # equation gives alpha in {0,1}; in either branch the degree-one part
    # forces u_i=0 and then the degree-two part forces every remaining
    # coefficient to vanish.
    alpha = sp.symbols("alpha")
    u = sp.symbols("u0:3")
    v = sp.symbols("v0:3")
    w = sp.symbols("w")
    element = alpha * algebra.unit("1") + w * algebra.unit("Q")
    for colour in range(3):
        element += u[colour] * algebra.unit(f"e{colour}")
        element += v[colour] * algebra.unit(f"y{colour}")
    residual = algebra.multiply(element, element) - element
    for scalar_value in (0, 1):
        specialized = [sp.expand(entry.subs(alpha, scalar_value)) for entry in residual]
        groebner = sp.groebner(specialized, *u, *v, w, order="lex")
        assert groebner.is_zero_dimensional
        # The reduced basis is exactly all seven radical coordinates.
        assert {sp.expand(poly.as_expr()) for poly in groebner.polys} == set(
            (*u, *v, w)
        )


def universal_asymmetric_model(direct_matrix):
    basis = (
        "1",
        "p0",
        "p1",
        "p2",
        "s0",
        "s1",
        "s2",
        "y0",
        "y1",
        "y2",
        "Q",
    )
    degrees = (0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2)
    products = {}
    for name in basis:
        add_product(products, basis, "1", name, {name: 1})
    for c, d in itertools.product(range(3), repeat=2):
        terms = {"Q": -sp.Rational(direct_matrix[c][d]) / KAPPA}
        if c == d:
            terms[f"y{c}"] = 1 / KAPPA
        add_product(products, basis, f"p{c}", f"s{d}", terms)
    return FiniteAlgebra(basis, degrees, products)


def audit_universal_asymmetric_model():
    direct = (
        (sp.Rational(1), sp.Rational(2), sp.Rational(-3)),
        (sp.Rational(5), sp.Rational(7), sp.Rational(11)),
        (sp.Rational(-13), sp.Rational(17), sp.Rational(19)),
    )
    algebra = universal_asymmetric_model(direct)
    reverse = universal_asymmetric_model(tuple(zip(*direct)))
    audit_algebra_axioms(algebra)
    audit_algebra_axioms(reverse)

    for c, d in itertools.product(range(3), repeat=2):
        cap_class = direct[c][d] * algebra.unit("Q") + KAPPA * algebra.multiply(
            algebra.unit(f"p{c}"), algebra.unit(f"s{d}")
        )
        expected = algebra.unit(f"y{c}") if c == d else sp.zeros(11, 1)
        assert cap_class == expected

    # Endpoint reversal is covariance a -> a^T and p <-> s.
    swap = sp.zeros(11, 11)
    for name in ("1", "Q", "y0", "y1", "y2"):
        swap[reverse.index[name], algebra.index[name]] = 1
    for colour in range(3):
        swap[reverse.index[f"s{colour}"], algebra.index[f"p{colour}"]] = 1
        swap[reverse.index[f"p{colour}"], algebra.index[f"s{colour}"]] = 1

    source_units = [algebra.unit(name) for name in algebra.basis]
    for left, right in itertools.product(source_units, repeat=2):
        assert swap * algebra.multiply(left, right) == reverse.multiply(
            swap * left, swap * right
        )

    # The positive-degree socle is precisely A_2 in this dense example.
    degree_one = [algebra.unit(name) for name in algebra.basis[1:7]]
    multiplication_blocks = []
    for multiplier in degree_one:
        columns = [
            algebra.multiply(algebra.unit(name), multiplier)
            for name in algebra.basis[1:]
        ]
        multiplication_blocks.append(sp.Matrix.hstack(*columns))
    stacked = sp.Matrix.vstack(*multiplication_blocks)
    kernel = stacked.nullspace()
    assert len(kernel) == 4
    assert all(vector[:6, :] == sp.zeros(6, 1) for vector in kernel)


def main():
    audit_symmetric_model()
    audit_universal_asymmetric_model()
    print("verified minimal (1,3,4) colour-symmetric cap quotient algebra")
    print("verified arbitrary-asymmetric cap table and endpoint reversal")
    print("verified associativity, radical cube zero, and trivial idempotents")


if __name__ == "__main__":
    main()
