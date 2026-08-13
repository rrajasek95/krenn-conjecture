# Affine normalization retires the centered conormal, not the pointed occurrence

## Corrected centered identity

The earlier projective conormal calculation used coordinates
`(dz_f,dZ,du)` and found

\[
 \gamma=90P_f-B+89\,du,\qquad
 P_f=dz_f-du,\qquad B=dZ-du.                          \tag{1}
\]

On the physical affine chart the target scalar is normalized to `u=1`.
Hence relative tangents satisfy `du=0`, and (1) becomes

\[
                         \boxed{\gamma=90P_f-B}.      \tag{2}
\]

The old scale tangent `(1,1,1)` is not an affine tangent: it evaluates to
one on `du`.  In relative coordinates `(dz_f,dZ)`, `P_f,B` already have rank
two and adjoining `gamma` leaves rank two.

Thus, once a **physical pointed comparison** `P_f` and the complete graph
normal `B` exist, centeredness adds no new relative cotangent class.  This
corrects the frontier of `1816162`.

There is one scope distinction.  Before differentiation,
`90(z_f-u)-(Z-u)` differs from `90z_f-Z` by the fixed constant `-89u`.
Equation (2) is a conormal/principal-parts statement.  It does not create a
selected degree-zero occurrence or make `P_f` physical.

Checker:

```text
computations/verify_h3_affine_pointed_pf_coloop_pivot_gate.py
```

Frozen ledger SHA-256:

```text
14240acd4a635abaddfb19b2b2d8b7067faf444a67fdf29d25637dd792e0e8f6
```

## Why the coloop pivot does not select `P_f`

For a pure-colour fan coloop, the complete rows give

\[
 dC+U=u,\qquad \alpha C+V=0,qquad \alpha C_c=u,       \tag{3}
\]

and hence

\[
                         \alpha U-dV=\alpha u.         \tag{4}
\]

After `u=1`, (4) forces at least one aggregate `U` or `V` to be nonzero and
types all of its literal terms.  It does not distinguish one term.

The smallest obstruction has only two occurrences.  If `U=f+g`, take

```text
alpha=1, d=0, C=0, Cc=1, U=1, V=0, f=g=1/2, u=1.
```

All equations (3) hold.  The tangent

```text
df=1, dg=-1; every other differential, including du, is zero
```

annihilates their differentials and the decomposition `U-f-g=0`, but

\[
                         P_f=df-du=1.                  \tag{5}
\]

Therefore `P_f` is not in their conormal row span.  The `V`-bright branch
has the identical sharp guard:

```text
alpha=1, d=1, C=1, Cc=1, U=0, V=-1, f=g=-1/2, u=1,
V=f+g.
```

Again `df=-dg` is invisible to every pivot row and visible to `P_f`.
Adding the eliminated equation (4) changes nothing because it is already a
linear combination of the complete rows.

## Sharpened surviving theorem

Affine normalization therefore moves the frontier down exactly one layer:

```text
separate centered conormal                 RETIRED
selected pointed occurrence P_f            OPEN
selected db01 and cross-word cap/Eq faces  LATER
```

The next theorem is not another centered projector.  It is pointed
occurrence isolation in the trapped coloop packet:

> Either the pivot aggregate has one effective literal occurrence, an
> internal redistribution gives an anchor-safe complete-column dependence,
> or the selected coordinate covector `e_f^*` lies in the row span of the
> complete physical endpoint-plus-simultaneous-`q` map.  If it does not, the
> resulting dual must extend through every augmented source column before it
> is called a terminal.

This is consistent with the actual endpoint-map audit: a marked coordinate
selector may lie only in the bordered protection row span, not in the
physical response row span.  The coloop pivot supplies the aggregate and its
common-`q` typing; it cannot resolve this protection-only distinction.

## Scope

The positive correction is exact on the canonical `h=3` affine chart.  The
two guards prove nonimplication from the complete two-row coloop pivot plus
affine normalization.  They do not prove that `P_f` is absent from the full
physical endpoint-plus-`q` source complex.
