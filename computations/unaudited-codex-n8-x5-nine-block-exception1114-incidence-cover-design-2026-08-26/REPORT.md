# Representative 1114 exact incidence/rank design

This design reduces records `1114,1978,2014,2036` to the one exact
source-site transport orbit already replayed by the parent seal.  Site
relabeling transports each record's source-labelled carrier and guard; it is
not used to identify distinct incidence profiles within record 1114.

The representative has 12 arbitrary source matrices, four fixed identity
edges, 15 supported perfect matchings, and the literal 6,561 GHZ amplitude
equations.  The cap67/triangle012 guard contributes 45 scalar equations.
Solving its first two matrix equations gives

```text
A37=-A36*A17^T,  A47=-A46*A17^T,
(I-A26*A17)*A36^T=0,
(I-A26*A17)*A46^T=0,
A36*(A17+A17^T)*A46^T=0.
```

All 416 triangle/star carriers are listed literally.  Exactly 16 have load
two.  Four useful orientations have annihilators
`Col(F) tensor Q^3`, with `(F,C)` equal to
`(A04,A01)`, `(A17,A01^T)`, `(A26,A25)`, and
`(A35^T,A25^T)`.  Such a carrier is active exactly when `F` is singular,
no coordinate axis belongs to `Col(F)`, and `Col(C)` is not contained in
`Col(F)`.  Hence failure is the exact union of `det(F)!=0`, one of the three
incidences `F*x=e_i`, or the containment `F*Y=C`.

The four-factor product gives 625 raw incidence profiles and 150 exact
simultaneous-colour S3 orbits.  Cramer pivoting is reversible but expands
this to 14,641 raw / 2,486 orbit charts, so the 150-orbit cover is the
smallest finite cover found.  Substituting the two linear guards leaves
90 variables and 6,588 base generators; the cover ranges from 91/6,589 to
126/6,624.

On the all-invertible profile put `H=[A36^T|A46^T]`.  Rank three forces
`A26*A17=I` and gives 20 minor charts / six colour orbits at 83/6,572.
Rank two has an exact `H=UV` gauge reduction.  Rank one has
`H=u(v36^T|v46^T)`; exact support excludes rank zero.  The canonical
rank-one chart `v36_0=1`, `u0*v46_0!=0` is the smallest retained input at
81 variables / 6,566 generators.  Its Q source is frozen but has no solver
epilogue or launch clearance.

The complete entry grading has exact rank 98 and nullity 10: 98 constraints
are independent modulo 1,000,003, while ten primitive integer null vectors
replay every constraint.  Torus normalization needs a large nonzero-entry
subcover and therefore does not improve the finite-cover objective.

No ideal, Singular, SAT, DRAT, or large-CNF computation ran.  This is a
design and held-chart result only; none of the four records is closed.
