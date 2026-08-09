# N=8 P5 third-normal coordinate-component pure coefficients

## Result

The P5 pure membership calculation advances one order on both coordinate
components:

- H1 degree nine vanishes identically on $z_{16}=0$ and $z_{41}=0$;
- H0 degree ten vanishes identically on $z_{16}=0$ and $z_{41}=0$.

No new pure survivor occurs on either coordinate component.  The generic
$L=0$ reduction and the next mixed strict compatibility are separate next
steps, so this is a finite-order coordinate-component checkpoint only.

The exact checker is
`computations/verify_n8_p5_third_order_next_pure.py`.  Its frozen ledger has
SHA-256
`320eabea4a02e275a732589c07eb2091008d97716e95474b5e75060699a8f400`.

## Third ambient-normal graph

The checker constructs the fourth coefficient of the ambient normal graph.
For every one of the 196 Jacobian pivots it forms

$$
Q^{(4)}-D_wQ^{(3)}+D_{n_2}Q^{(2)}
+\frac12D_w^2Q^{(2)}+D_{n_3}Q^{(1)}.
$$

There are 108 active pivot inputs, 376 incoming terms, 112 ambient
coordinates in $n_3$, and 389 direction terms.  Every displayed residual
cancels exactly.

The strict composition must retain the full tangent-polynomial directions.
Composing a direction after its P5 restriction is incorrect because it loses
the variation in the P5-normal tangent coordinates.  The checker therefore
builds full $w$ and $n_2$ directions first, forms all normal/strict bidegrees
of total order at most three, and only then restricts to the P5 strict arc.
Identity-safe caches retain strong references to every source polynomial.

## Regressions and new forms

Before accepting the new coefficients, the checker compares every residual
degree through nine against the frozen second-order strict jets.  It then
recovers exactly:

- the four-term H1 degree-eight form;
- the 424-term H0 degree-nine form.

The new forms are:

- H1 degree nine: 34 terms, SHA-256
  `0a0b52df2ecc4306ce7a974021a219f039d9c8e838dbdb1d7983076231e2778c`;
- H0 degree ten: 1,628 terms, SHA-256
  `a68531bc6106f6de82e28d21c38037fb8fec78aea6c31320c66c059c43d842c9`.

Both forms have the coordinate factors required to vanish on
$z_{16}=0$ and $z_{41}=0$.  Neither is a bare multiple of
$L=z_9z_{25}-z_{11}z_{46}$, so no generic-$L$ conclusion is made here.

## Frontier

The next exact tasks are to reduce these new forms on the symbolic two-bend
$L$ graph and to build the degree-nine mixed tail needed for strict order
seven.  Those computations determine whether the generic $L$ branch has a
pure survivor and whether all three components lift one mixed order further.
