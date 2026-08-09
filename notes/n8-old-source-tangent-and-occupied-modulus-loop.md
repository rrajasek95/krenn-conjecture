# Exact old-source tangent and the first occupied-modulus loop

## Outcome

At the anchored (N=8) three-cut source, the full old-source exactness
tangent has dimension 27.  Target-stabilizing local-colour gauge together
with the fourteen previously certified absent boundary cells has rank 26.
The unique remaining tangent class is the already occupied cell

```text
23;21.
```

This class is not merely infinitesimal.  Changing its coefficient by an
arbitrary parameter preserves the pure anchors, the one-cross cylinder, the
combined residual cylinder, the rank-14 cofactor frames, and a nonzero target
defect on all three cuts 2, 3, and 4.  It is therefore an exact one-parameter
old-source modulus.

On the 62 positive-cross-degree (N=10) Fitting witnesses, however, this
modulus is not square-zero.  It acts trivially on 50 witnesses and by a
rank-one idempotent on 12.  Those 12 actions are literal diagonal loops.
Thus the proposed statement that every exact old-source deformation acts
through a square-zero incidence algebra is false, already for one exact
occupied-coordinate deformation.

The correct algebra on this anchored two-edge chart is slightly larger:

\[
                 \mathbb Q I+\mathbb Q P+R,
       \qquad P^2=P,\quad R^2=0,\quad PR=0,\quad RP=R
\]

on each of the 12 nontrivial witnesses (with (R=0) allowed on the other
50).  Hence the radical is still square-zero, but the associated semisimple
piece contains the occupied-weight idempotent.  Equivalently, the first
commutator is ([P,R]=-R); the quiver has one arrow into the idempotent vertex
and no length-two radical path.  This is the minimal exact cyclic action: a
single diagonal loop, not a directed cycle through two distinct vertices.

## Full exactness tangent

All 252 decorated old-edge coordinate derivatives are imposed
simultaneously.  For each cut, the checker linearizes both

1. the one-cross tensor in the cofactor-insertion cylinder; and
2. the full matching residual minus the GHZ target in that cylinder,

together with the three pure anchors.  The exact rational constraint matrix
has rank 225, so its kernel has dimension 27.

The 21 displayed target-stabilizing local-colour gauge generators have rank
12.  Adding the fourteen absent-cell boundary directions raises the rank to
26, and all 26 lie in the exactness tangent.  Modulo this span, the tangent
quotient is one-dimensional, represented by the unit variation of the
occupied source (23;21).

This is a classification of the Zariski tangent at the anchored source.  It
does not rule out remote or nonlinear components of the arbitrary-source
exactness variety.

## Exact integration of the extra tangent class

Write the cofactor frame and either cylinder row as

\[
 C(t)=C_0+tC_1,\qquad r(t)=r_0+tr_1.
\]

All entries are affine because a matching uses the physical edge 23 at most
once.  The checker solves the coefficient recurrence

\[
 C_0\lambda_0=r_0,
 \quad C_0\lambda_1=r_1-C_1\lambda_0,
 \quad C_0\lambda_{j+1}=-C_1\lambda_j.
\]

For each of the (3\cdot27=81) boundary rows in each cylinder family, the
recurrence terminates after degree at most one: 77 rows need no moving
coefficient and four need a degree-one coefficient.  No higher obstruction
occurs.

Independently, fixed cofactor-frame minors on cuts 2, 3, and 4 are the
constant polynomials (-1,1,-1).  Fixed target-defect minors are (1,1,-1).
The pure-word derivatives vanish.  These polynomial identities prove that
the complete three-cut conditions remain active for every complex value of
the occupied-cell parameter, including the value (-1) that deletes the
cell from the anchored source.

The full matching tensor is **not** constant on this line.  Its exact
derivative has the two mixed entries

    00210000 :  1
    00210012 : -1

This distinction is essential.  The line is an exact deformation of the
three-cylinder relaxation, not a deformation inside the full GHZ fibre.
Consequently global minimum-support for a hypothetical realization cannot
be invoked to set this occupied weight to zero.  Such a reduction would
first require a new source-provenance implication showing that the mixed
derivative vanishes (or is cancelled) on the full matching fibre.

## The diagonal-plus-radical incidence algebra

Adjoin the occupied modulus to the fourteen boundary directions.  There are
now eight directions on physical edge 23 and seven on physical edge 67.
Every lifted (N=10) coefficient matrix has exact bidegree at most ((1,1)),
so its entire parameter dependence is recovered from the 15 linear and 56
cross-edge bilinear coefficient matrices.  No coefficient grid or untested
higher interaction is present.

After normalization by each anchored augmented square, the 62 incidence
graphs are:

| arrows | loops | longest non-loop path | witnesses |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 7 |
| 1 | 0 | 1 | 36 |
| 2 | 0 | 1 | 7 |
| 1 plus the loop | 1 | 1 | 12 |

All non-loop arrows remain noncomposable, so they span a square-zero radical
(R).  On each of the 12 exceptional witnesses, the occupied modulus is a
rank-one idempotent (P), and the unique radical arrow points into its loop
vertex.  This gives (PR=0), (RP=R), and ([P,R]=-R).  No 
radical (\operatorname{Ext}^2) path appears.

If (t) denotes the added coefficient, the selected augmented determinant
is unchanged on 50 witnesses and is multiplied by (1+t) on 12.  Thus it is
nonzero after localizing the physical occupied weight (w=1+t), but it
vanishes when the occupied cell is deleted.  Direct exact ranks at (w=0)
give:

```text
50 witnesses: base defect 1, quotient jump 1
12 witnesses: base defect 1, quotient jump 0
```

Those twelve failures occur on twelve of the 52 cross supports; only 40 of
52 supports retain one of the audited positive-degree jumps after deletion.
The first literal failure is the `aug3` witness on

```text
((0,8,1,0), (0,8,1,2), (5,9,1,0), (5,9,1,2), (6,9,0,0)).
```

This is a countermodel to extending the present positive-degree Fitting
certificate unchanged to arbitrary exact old sources.  It is not a Krenn
counterexample: disappearance of this particular quotient jump neither
proves a fourth cut nor verifies the full target tensor.

## Strategic consequence

The strongest viable structural replacement is not a pure square-zero
theorem.  It is a stratified statement:

> after localizing the occupied source weights, exact boundary deformations
> act through a triangular algebra whose radical is square-zero, while
> occupied-support moduli act through diagonal idempotents.

Such a theorem can preserve the obstruction on the support torus.  A truly
arbitrary-source theorem must additionally cross the coordinate boundary
(w=0), where the present witness really dies, by supplying another Fitting
grade or a specialization/induction argument.  Further fixed-old five-cross
batching cannot repair this gap by itself.

Nor does maximum-anchor/minimum-support selection currently force this
boundary: although the pure anchors and all three relaxed cuts survive at
`w=0`, the two-entry mixed full-tensor derivative above means the GHZ
equation is not preserved along the degeneration.

## Reproduction

```text
python3 computations/verify_n8_three_cut_exactness_tangent.py
python3 -O computations/verify_n8_three_cut_exactness_tangent.py
python3 computations/verify_n10_five_cross_occupied_modulus_incidence.py
python3 -O computations/verify_n10_five_cross_occupied_modulus_incidence.py
```

All tangent kernels, coefficient recurrences, minors, ranks, matrix inverses,
and incidence products are computed exactly over (mathbb Q).
