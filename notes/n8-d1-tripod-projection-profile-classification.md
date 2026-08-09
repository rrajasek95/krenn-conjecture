# N=8 D1: classification of tripod projection profiles

Let `K` be a two-dimensional subspace of the kernel of

```text
Phi(a,b,c)=a tensor F + E tensor b + D tensor c
```

for nonzero opposite matrices `D,E,F`.  Sort the ranks of the three
projections of `K`.  All ten possible profiles are now classified over every
field.

## A zero projection is impossible

Suppose `pr_X K=0`.  If `pr_Y K` has rank below two, a nonzero kernel vector
`(0,0,z)` forces `D=0`; similarly rank below two for `pr_Z K` forces `E=0`.
If both ranks are two, normalize a basis to

```text
(0,e0,e0), (0,e1,e1).
```

The two relations on the `18` entries of `(E,D)` have rank `18` over `Z`, so
again `E=D=0`.  Thus profiles

```text
000,001,002,011,012,022
```

are impossible whenever all three opposite matrices are nonzero.

## Profile 122

Choose kernel generators `(0,y0,z0)` and `(u,y1,z1)`, with both displayed
pairs independent.  The relations force, up to nonzero scalar gauges,

```text
E=u tensor z0,
D=-u tensor y0,
F=y0 tensor z1-y1 tensor z0.
```

The last matrix has rank two in every characteristic.  Modulo the line `u`,
a companion tensor is `[a] tensor F`.  A nonzero pure target outside `u`
would make this rank-two matrix decomposable.  Hence a pure companion exists
only if the target `X` line equals `u`.

## Profile 112

If the two rank-one projection kernels coincide, a relation with two zero
components forces an opposite matrix to vanish.  Otherwise normalize the
two relations to `(0,y,z0)` and `(x,0,z1)`, with `z0,z1` independent.  Then

```text
E=x tensor z0,   D=-x tensor y,   F=y tensor z1,
```

and every companion is

```text
a tensor y tensor z1 + x tensor b tensor z0
  - x tensor y tensor c.
```

A pure target can occur only in the union of three alignment flags:

```text
(targetY=y, targetZ=z1),
(targetX=x, targetZ=z0),
(targetX=x, targetY=y).
```

## Profile 111

Coincident kernel lines again force an opposite matrix to vanish.  If the
three kernel lines are distinct, their three linear forms on `K` satisfy
`gamma=p*alpha+q*beta` with `p,q` nonzero.  Resolving the two coefficients
forces all three opposite matrices onto the corresponding lines.  After
gauges,

```text
E=-x tensor z,   D=x tensor y,   F=-y tensor z.
```

Every companion lies in

```text
a tensor y tensor z + x tensor b tensor z + x tensor y tensor c.
```

Quotient by each pair of lines.  The three resulting conditions are
`X or Y`, `X or Z`, and `Y or Z`; therefore a pure target must share at least
two of the lines `x,y,z`.  This is the elementary `2x2`-minor proof of the
Segre-tangent intersection, with no geometric or characteristic assumption.

Finally, profile `222` is already impossible by the exact injective-tripod
theorem `aa85cd4`.  Consequently the residue problem no longer has an
unclassified continuous projection-rank stratum: it has only the finite
target-alignment flags above.  Those flags are the inputs for support clauses
and external pure-lift factors on the six maximal residue orbits.

The exact checker
[`verify_n8_d1_tripod_projection_profile_classification.py`](../computations/verify_n8_d1_tripod_projection_profile_classification.py)
verifies every displayed kernel relation and companion normal form, checks
the zero-profile linear map has rank `18`, checks the rank-two wedge, and
freezes the alignment truth tables.
