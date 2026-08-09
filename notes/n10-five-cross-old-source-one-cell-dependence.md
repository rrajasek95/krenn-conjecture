# Old-source dependence of the positive-degree quotient obstruction

## Outcome

The constant-row quotient obstruction survives the complete anchored
one-cell old-source exactness locus.  The earlier arbitrary-weight one-cell
theorem leaves exactly fourteen absent-coordinate families

\[
                         A(t)=A+tE_x
\]

which preserve the three complete old cuts 2, 3, and 4 for nonzero $t$.
On every one of these fourteen charts, all 62 positive-degree quotient
witnesses retain a structural base-rank defect and an augmented full-rank
minor.

The dependence is sharper than coprimality: for each witness and chart, the
selected augmented minor has degree zero in $t$.  Hence its dependence
ideal in \(\mathbb Q[t,t^{-1}]\) is already the unit ideal.  No combination
of witnesses or exceptional parameter chart is needed.  The mechanism is an
exact unipotent column shear, described below.

This advances the fixed-old obstruction toward a structural identity, but
does not prove an arbitrary-old-source theorem.  The computation covers
one-cell deformations of the anchored source and evaluates the cross weights
at one exact nonzero torus point.

## Exactness charts

The sixteen anchored cells and three pure-target characters have rank 15.
Of the 236 absent old coordinates, 230 are torus-normalizable and six have
dependent characters.  The previous exact one-cell theorem proves that the
six dependent families destroy a fixed complete cut for every nonzero
parameter.  Among the 230 normalizable families, exactly fourteen retain all
three complete cuts at the unit representative, hence for every nonzero
parameter:

```text
(2,3;01) (2,3;02) (2,3;10) (2,3;11) (2,3;12) (2,3;20) (2,3;22)
(6,7;01) (6,7;02) (6,7;10) (6,7;11) (6,7;20) (6,7;21) (6,7;22)
```

These are the localized one-variable components of the old-source
three-cylinder exactness locus used by the checker.

## Dependence-ideal certificate

For every one of the 62 quotient jumps, retain the fixed rows selected after
deleting all cross-weight-degree-zero rows.  Write $B_x(t)$ for its base
matrix and $A_x(t)$ for its augmented matrix on one of the fourteen old
charts.

Each matrix entry is affine in $t$, because a perfect matching uses the
added old cell at most once.  The checker performs two independent exact
calculations.

1. It forms the union support of the constant and linear coefficient
   matrices.  Bipartite matching gives

   \[
          \operatorname{rank} B_x(t)<r
          \quad\hbox{identically in }t
   \]

   for all 62 witnesses on all fourteen charts.

2. It selects an $r$-column augmented minor which is nonzero at $t=0$,
   evaluates its determinant at (0,1,\ldots,r), and interpolates the exact
   polynomial in \(\mathbb Q[t]\).  Every one of the 868 polynomials is a
   nonzero constant.

Write the selected square as

\[
                    M(t)=M_0(I+tK),
       \qquad K=M_0^{-1}(M(1)-M_0).
\]

Ten of the fourteen directions have $K=0$ on all 62 witnesses.  Four
directions change selected entries, but every nonzero action has rank one
and satisfies $K^2=0$:

| old direction | witnesses with nonzero $K$ | changed selected entries |
|---|---:|---:|
| $23;11$ | 2 | 2 |
| $67;01$ | 4 | 8 |
| $67;11$ | 24 | 35 |
| $67;21$ | 6 | 10 |

Thus \(I+tK\) is an elementary unipotent column operation and has determinant
one for every $t$.  This directly explains the constant minors; it is not
an inference from interpolation alone.  The interpolation remains as an
independent exact audit of the determinant identity.

Thus

\[
   \bigl(\det A_{x,w}(t):w\in W\bigr)=(1)
       \quad\text{in }\mathbb Q[t,t^{-1}]
\]

for each admissible direction $x$; in fact each displayed generator is a
unit by itself.  This is a genuine cofactor invariance on these exactness
charts, not a finite parameter sample.

## Structural interpretation and remaining gap

Every admissible direction lies on edge 23 or 67.  Relative to cut
2, those are boundary-touching directions.  Most selected positive-degree
matching cofactors do not see their weights; the four visible directions act
only by the square-zero column shears above.  This suggests the next
source-independent lemma:

> after the constant layer is removed, boundary-supported exact deformations
> act on the selected Fitting frame through a nilpotent incidence algebra,
> and therefore preserve its maximal augmented cofactor.

The checker proves that statement on all one-cell generators visible at the
anchored point.  It does not yet prove it for simultaneous two-cell
deformations, occupied-support moduli, or an arbitrary old source.  It also
does not retain the full five-variable cross-weight polynomial: the selected
minor is reconstructed at the exact nonzero point $(1,2,3,5,7)$.  Those are
the two sharp upgrades required for a uniform theorem.

## Reproduction

```text
python3 computations/verify_n10_five_cross_old_source_one_cell_dependence.py
python3 -O computations/verify_n10_five_cross_old_source_one_cell_dependence.py
```

All ranks, determinant values, interpolation coefficients, and polynomial
gcds are exact over \(\mathbb Q\).
