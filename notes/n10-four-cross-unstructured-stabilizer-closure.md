# Exact closure of the fixed-old four-cross frontier

## Outcome

The previously open unstructured four-cell frontier on the anchored
forced-pair N=10 lift is empty.  On fixed cut 2:

1. a centre-universal quotient excludes all 2,859,192 genuinely new
   three-grade stars;
2. a two-centre quotient reduces all rectangles to 19,306 exact
   forced-pair-swap orbit representatives;
3. the enlarged affine equations exclude 16,305 of the new three- and
   four-grade representatives and leave 91;
4. saturation by the four nonzero weights leaves 45; and
5. literal evaluated-column minors exclude all 45 over the coefficient
   torus.

Together with the earlier permanent-zero and at-most-three-cell theorems,
this proves

\[
 \boxed{\text{No fixed-old cross addition supported on at most four
 cells preserves cut 2.}}
\]

This is a source-level exclusion for the fixed anchored old source.  It is
not a Krenn counterexample and it does not address additions with five or
more cross cells, old-source deformations, or arbitrary even order.

## 1. The actual discrete stabilizer

The checker tests every old-vertex permutation preserving the cut boundary
\(\{2,6,7\}\), together with every global colour permutation.  Requiring
the anchored N=8 source to be fixed leaves only

\[
 (\mathrm{id}_{\{0,\ldots,7\}},\mathrm{id}_{\{0,1,2\}}).
\]

Thus the old source supplies no unrecorded discrete orbit reduction.  The
remaining exact support symmetry is the forced-pair swap \(8\leftrightarrow
9\).  Diagonal coefficient-torus actions normalize weights but do not
identify distinct support sets.

## 2. Uniform exclusion of every three-grade star

Fix one of the 72 cross coordinates \(x\) incident to vertex 8.  It has 63
valid opposite coordinates and hence 63 possible permanent grades.  In the
cut-2 quotient by the 126-dimensional universal constant-plus-linear
column space, form the deliberately enlarged space

\[
 {cal W}_x=\operatorname{span}\{Q_{2,p;h,i},D_{2,p}:p\text{ incident to }x\}.
\]

This grants every quadratic column direction and every residual direction
from all 63 grades independently.  Nevertheless the old residual is not
in \({\cal W}_x\) for any of the 72 centres.  Its remaining word-111
normal form is

\[
 e_{1089}+e_{1097}\quad(44\text{ centres}),\qquad
 e_{1097}\quad(14),\qquad e_{1089}\quad(14).
\]

Every actual three-leaf star uses a subspace of \({\cal W}_x\), so this one
calculation excludes every choice of leaves and every choice of weights.
It closes

\[
              72\binom{63}{3}=2,859,192
\]

three-grade star orbits; the forced-pair swap covers the opposite
orientation.  No coefficient grid is used.

## 3. Two-centre reduction of the rectangle family

There are \(\binom{72}{2}=2,556\) unordered pairs on one new-vertex side.
For each pair \(\{x_1,x_2\}\), grant all quadratic and residual grade
directions incident to either centre.  If the old residual remains outside
this larger space, no rectangle using that pair can work, regardless of
the opposite pair.

Exactly 196 pairs survive this necessary test; all use new-end colours
\(\{0,2\}\).  Applying the same test after the forced-pair swap means that
both sides of a surviving rectangle must be chosen from these 196 pairs.
Modulo the swap there are therefore only

\[
                     \binom{196+1}{2}=19,306
\]

representatives.  The exact permanent-class/affine census is

| permanent classes | affine result | representatives |
|---:|---|---:|
| 0 | earlier theorem | 140 |
| 2 | earlier theorem | 2,770 |
| 3 | inconsistent | 6,654 |
| 4 | inconsistent | 9,651 |
| 3 | affine survivor | 18 |
| 4 | affine survivor | 73 |

The affine system is the necessary enlarged-cylinder system from the
bounded-frontier note: each labelled quadratic cofactor is allowed to vary
independently, while the residual grade coefficients and all three pure
anchors retain their common permanent scalars.

## 4. Exact nonzero-weight saturation

Put weights \(a,b,c,d\) on a rectangle.  The checker reconstructs every
permanent scalar as its literal polynomial in these weights, including
endpoint-swap recombination.  If the reduced affine equations are
\(A\pi=b_0\), it computes over \(\mathbb Q\)

\[
 \left\langle A\pi(a,b,c,d)-b_0,\;tabcd-1\right\rangle
 \subset\mathbb Q[a,b,c,d,t].
\]

A unit Groebner basis excludes the support on the coefficient torus.  Of
the 91 affine survivors, 46 saturate to the unit ideal and 45 remain as
necessary enlarged-space candidates.

For each of those 45, the checker then constructs the literal 21 evaluated
cofactor columns and the literal forced residual.  A square column minor
and an augmented residual minor exclude 41 immediately: both are nonzero
torus monomials.  Four initial pivots instead contain the rank-drop factors
\((bc+1)^3\) (three cases) or \((ac+1)^3\) (one case).  Selecting a pivot
at the corresponding divisor gives a different *global* polynomial minor.
The square and augmented minors are, up to sign,

\[
 a^{10}c^9d,\qquad a^4b^5d^9,\qquad b^4c^3d,
 \qquad b^6c^5d.
\]

Each is nonzero whenever \(abcd\ne0\).  Hence the apparent rank-drop
components contain no literal cylinder source, and all 45 candidates are
excluded.

## 5. Scope and next stopping rule

The result closes the entire support-size-four problem for the fixed old
source, not merely the old-node structured subfamilies.  It combines with
the earlier theorem for support at most three and with arbitrary-support
permanent-zero exclusion.

Enumeration should stop here for this support size.  A five-cell attack
must begin with an analogous centre/pair universal reduction; if that does
not collapse the support census sharply, the useful next target is a
structural coefficient-cylinder identity rather than a raw coefficient
grid.  Nothing here proves an N-to-N+2 contraction for arbitrary cross
support.

## Reproduction

Run

```text
python3 computations/verify_n10_four_cross_unstructured_stabilizer_frontier.py
python3 -O computations/verify_n10_four_cross_unstructured_stabilizer_frontier.py
python3 -I computations/verify_n10_four_cross_unstructured_stabilizer_frontier.py
python3 -S computations/verify_n10_four_cross_unstructured_stabilizer_frontier.py
```

The checker uses exact rational arithmetic and invokes Singular for the
Groebner bases and determinant factorizations.
