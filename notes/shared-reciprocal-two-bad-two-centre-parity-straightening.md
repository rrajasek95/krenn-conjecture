# Colour parity straightens every two-centre kernel bridge

## 1. Result

Continue in the five-site cofactor quotient of
[`shared-reciprocal-two-bad-cofactor-quotient.md`](shared-reciprocal-two-bad-cofactor-quotient.md).
The target-line bridge excluded in
[`shared-reciprocal-two-bad-atomic-kernel-exclusion.md`](shared-reciprocal-two-bad-atomic-kernel-exclusion.md)
is not merely a special alignment when the internal quadratic is
colour-diagonal.

> **Two-centre parity-straightening lemma.**  Let `q` have only
> same-colour endpoint cells, and let a minimal nonzero two-centre kernel
> relation use sites `0,1`.  Its Koszul factorization is
>
> ```text
> K_0 = u_1 tensor Z,       K_1 = u_0 tensor Z.
> ```
>
> Then `u_0,u_1` lie on the same target coordinate line.  If this kernel
> row supplies a nonzero entry to an all-`t` kernel-product monomial, the
> common line is `C e_t`.

Consequently the committed target-line bridge theorem exhausts every
minimal two-centre bridge in the colour-diagonal, one-centre-bright-lift
chart.  A survivor cannot evade it by tilting a two-centre factor line;
it must instead use a mixed-colour internal cell, at least three kernel
centres, or a multi-centre bright lift.

## 2. Factorization

Write the zero relation, after inserting the missing sites, as

```text
u_0^(0) K_0 + u_1^(1) K_1 = 0.                         (1)
```

Minimality says both summands are nonzero.  Contracting (1) at site `0`
by a functional nonzero on `u_0` shows that `K_0` factors by `u_1` at
site `1`; substituting back and cancelling the nonzero factor gives the
same common three-site tensor `Z` in `K_1`.  Up to a nonzero scalar and
sign this is

```text
K_0 = u_1 tensor Z,       K_1 = u_0 tensor Z.           (2)
```

This is the standard two-site Koszul factorization and uses no matching
approximation.

## 3. Even-parity support

Every monomial in a four-site matching of a colour-diagonal quadratic has
an even number of endpoints of each colour.  Choose any nonzero word `z`
of `Z`.  For every colour `d` in the support of `u_1`, equation (2) gives
a nonzero word `(d,z)` of `K_0`, so

```text
parity(z) + e_d = 0 in (Z/2)^3.                         (3)
```

Two different colours in `supp(u_1)` would give two different values for
`parity(z)`, impossible.  Thus `u_1` is a coordinate vector.  Applying the
same argument to `K_1` makes `u_0` a coordinate vector, and the common
word `z` in (3) forces their axes to agree.

There is no coefficient-cancellation caveat: each coefficient in (2) is
the product of two nonzero coefficients in an integral domain, while a
word of odd colour parity is structurally absent from every diagonal
matching.

Finally, an all-`t` term of `P U V q` can select a local entry of this
kernel row only if that entry has colour `t`.  Since the row has one
coordinate axis, the common axis is `t`, exactly the already-excluded
target-line bridge.

## 4. Exact census and scope

The checker enumerates all `7 x 7` nonempty endpoint supports and all 27
three-site words.  Imposing the parity of only `K_0` leaves 147 strata,
including 126 tilted choices on the unconstrained endpoint.  Imposing both
cofactor parities leaves exactly 21:

```text
7 common words on axis 0
7 common words on axis 1
7 common words on axis 2.
```

All 21 have singleton equal endpoint supports.  The one-sided mutation
shows why the common provenance of both cofactors is essential.

This lemma does not straighten a three-or-more-centre Koszul circuit and
does not apply once `q` has mixed-colour endpoint cells.  Those, together
with multi-centre preimages of the two bright pure tensors, are the exact
remaining diagonal-chart boundary.

## 5. Reproduction

```sh
python3 computations/verify_shared_reciprocal_two_bad_two_centre_parity_straightening.py
python3 -O computations/verify_shared_reciprocal_two_bad_two_centre_parity_straightening.py
```

The checker uses only the Python standard library and is independent of
coefficient normalization.
