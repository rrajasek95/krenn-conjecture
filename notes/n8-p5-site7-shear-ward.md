# P5 site-7 shear and exact Ward transgression

The P5 Rees chart carries an exact square-zero site-7 action, but with an
important distinction.  The four-cell direction `z46` is **not** the orbit
tangent at the translated centre: its edge blocks 27 and 37 vanish there.
Instead, the nilpotent shear

```text
N = E20+E21 at site 7
```

fixes the centre because the nonzero site-7 columns 0 and 1 cancel rowwise,
and acts on the mixed tangent space by

```text
N(z44)=z46,  N(z45)=z46,
N(z52)=z54,  N(z53)=z54,
```

with every other tangent parameter killed.  Thus `N^2=0`, P5 is invariant,
and on the `b=z44+z45 != 0` chart the finite action is

```text
z46 -> z46 + rho*b,
z54 -> z54 + rho*(z52+z53).
```

So `z46/b` really is a unipotent orbit coordinate on the P5 tangent chart,
even though `z46` is not the orbit tangent of the centre itself.

## The 196 normal coordinates

On the ambient-normal quotient dual to the 196 mixed Jacobian rows, the same
shear is a sparse square-zero map with exactly 31 arrows, all with coefficient
one.  They are the literal site-7 column maps

```text
y_(u7,a,0), y_(u7,a,1) -> y_(u7,a,2)
```

whenever both cells are normal pivots.  There are only two tangent correction
terms: the normal cells `(0,7,2,0)` and `(0,7,2,1)` both map to the tangent
cell `(0,7,2,2)=z24`.  These are the only Koszul corrections needed to make
the normal-coordinate change equivariant.  The checker exports all 31 arrows
with literal ambient-cell provenance.

## Exact output Ward identity

Matching covariance gives the source identity

```text
delta H_(w,2) = H_(w,0) + H_(w,1),
delta H_(w,0) = delta H_(w,1) = 0.
```

The checker verifies this directly on all `3^8=6561` words and their 105
matching monomials.  Modulo the mixed output ideal, the two exceptional
two-step modules are

```text
delta H_00000002 = H_00000000,
delta H_11111112 = H_11111111.
```

This is the exact all-degree Ward source behind the repeated pure/mixed
transgression in the P5 calculations.

## What it does not yet prove

The constant shear is transverse to the recovered generic-L centre:

```text
delta(z9*z25-z11*z46) = -z11*(z44+z45),
```

a unit multiple on the dense chart.  Moreover the raw source functionals for
rows M30 and M33 have no pure Ward term.  Their observed H/G relation is
therefore produced only after normal/transverse Schur elimination and bend
corrections; it is not a bare output-coordinate identity.

Consequently the shear does not by itself prove full-germ membership or the
all-order Nakayama recurrence.  The precise remaining promotion is filtered:
lift this square-zero action through the 207-row Schur graph, include the two
`z24` Koszul corrections, and correct it by the monic newest-bend equation
`G`.  Then test whether the corrected derivation preserves all 28 mixed germs
and sends the two near-pure mixed rows to H0/H1 modulo that ideal.

The exact checker is
`computations/verify_n8_p5_site7_shear_ward.py`.
Its frozen ledger has SHA-256
`957abd7f8456dda477050cd438f15d442a0a3614fb5b98dca126b0e098cb810a`.
