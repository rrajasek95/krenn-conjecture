# Fixing the target removes the extra `89 du` obstruction

## Corrected verdict

The normalization loophole in `1816162` is real.  The physical Krenn source
equations are affine:

\[
                G_{\rm pure}=H_{\rm pure}-1=0.        \tag{1}
\]

The symbol `u` in the homogeneous EqSystem row `H0-u` is an auxiliary
homogenizer.  The physical chart is explicitly obtained by dehomogenizing
`u=1`.  Therefore the physical relative cotangent has

\[
                              du=0.                   \tag{2}
\]

Let `z_f` be the marked occurrence graph coordinate and `Z=sum_M z_M`.  Put

\[
 B=dZ-du,\qquad P_f=d(z_f-u),\qquad
 \gamma_c=90dz_f-dZ.                                 \tag{3}
\]

In the absolute homogenized cone one indeed has

\[
                  \gamma_c=90P_f-B+89du.             \tag{4}
\]

That is the rank-three calculation of `1816162`.  But after restricting to
the actual fixed-target fibre, (2) gives

\[
                  \boxed{\gamma_c=90P_f-B}.           \tag{5}
\]

Hence the centered face is not independent after a physical `P_f` is
granted.  The earlier `89du` detector is the radial target-scale tangent of
the absolute cone, not a physical affine obstruction.

Checker:
[verify_h3_centered_pointed_face_fixed_target_correction.py](../computations/verify_h3_centered_pointed_face_fixed_target_correction.py).

## Exact rank correction

In absolute coordinates `(dz_f,dZ,du)`,

```text
B         = (0, 1,-1),
P_f       = (1, 0,-1),
gamma_c   = (90,-1,0).
```

The first two rows have rank two and `gamma_c` raises the rank to three.
The common-scale tangent `(1,1,1)` kills `B,P_f` and reads `89` on
`gamma_c`.

In the fixed-target relative cotangent `(dz_f,dZ)`,

```text
B         = (0,1),
P_f       = (1,0),
gamma_c   = (90,-1)=90P_f-B.
```

The rank remains two.  This is also the convention used in the exact
private-site identities, where the target constant is the literal `1`, and
in the degree-four EqSystem audit, which explicitly dehomogenizes `u=1`.

## What remains open

This correction does **not** prove that `P_f` is physical.  The safe monic
occurrence graph gives

\[
                [P_f]=-[dG]
\]

for the private mate aggregate `G`; it transfers the pointed obstruction to
one slack direction.  Adjoining `P_f` itself still removes an actual old
tangent and changes the original source fibre.  Thus the corrected shortest
entry theorem is:

> Construct one physically typed pointed occurrence conormal `P_f` in the
> complete response word/fine/q/anchor comparison.  Then the complete
> response normal `B` and (5) automatically construct the centered Maschke
> face and its factor-90 anchor law.

The cap graph remains downstream and differently graded.  No conclusion
about its `01211222 / t*q_(v,N) / P3+K2` placement, physical `q`, shifted
ridge, or eta/sigma follows from (5).

This note supersedes only the fixed-target use of the `89du` obstruction in
`1816162`; its absolute homogenized-cone calculation remains correct.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
