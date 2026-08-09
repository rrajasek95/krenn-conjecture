# N=8 D1: the invertible-star K4 obstruction

The maximal residue support has a short structural obstruction after its
rank-two reduction.  The underlying lemma is independent of support and of
the base field.

Let `U1,...,U4` be two-dimensional vector spaces, let `Aij` be a bilinear
form on every edge of `K4`, and suppose the three forms incident to vertex
`1` are invertible.  Then

```text
A12*A34 + A13*A24 + A14*A23
```

cannot be a nonzero pure four-tensor.

## Normalizing the star

Independent changes of basis at the four vertices normalize
`A12=A13=A14=I`.  Write the alleged pure tensor as `x*y*z*w`.  Contract at
the first vertex by a nonzero covector annihilating `x`, identify the other
three spaces through the normalized identities, and call the resulting
common vector `e0`.  The contraction is zero, so the three opposite forms
have the exact normal form

```text
F = [[ f,  q], [ p, 0]],
E = [[ g, -q], [ r, 0]],
D = [[-f-g,-p], [-r, 0]].                         (1)
```

No division, determinant, or characteristic assumption is used in (1).

## The complementary contraction

Contract instead by a covector taking value one on `x`.  The result `S` is
a nonzero pure `2*2*2` tensor.  Formula (1) gives

```text
S000 = S111 = 0,
S100 + S010 + S001 = 0,
S110 + S101 + S011 = 0.                           (2)
```

But a nonzero pure three-cube with both opposite corners zero is supported
on one cube edge: one factor must lose its zero-coordinate and a different
factor must lose its one-coordinate.  Such an edge contains exactly one
weight-one and one weight-two vertex.  Equations (2) therefore kill both
possible entries, contradicting that `S` is nonzero.

This proves the lemma over every field.

## Role in the D1 proof

On the full residue support, every non-pure slice writes an edge matrix as a
sum of two rank-one matrices, so all six residue edge matrices have rank at
most two.  Whenever the rank-two slice relations give a common two-plane at
each vertex, the restricted edge forms are invertible and the lemma above
closes that component immediately.  The remaining work is now sharply
localized: prove the common-plane reduction and dispose of the rank-one
edge strata.  No further support-cardinality census is needed for the
maximal-support component.

The exact checker
[`verify_n8_d1_k4_invertible_star_pure_obstruction.py`](../computations/verify_n8_d1_k4_invertible_star_pure_obstruction.py)
reconstructs both contractions symbolically and exhausts the six possible
pure-cube support edges.  Its frozen ledger is
`2ecf1b09b853c5d109ffe243f9195e95be24a32e906cde29e0bdd1e938472c6e`.
