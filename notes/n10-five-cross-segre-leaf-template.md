# A source-faithful Segre leaf template for all 196 pair blocks

## Outcome

All 196 surviving two-centre blocks share one exact rank-one weight template.
If the two centre weights are \(a,b\) and the three chosen opposite weights
are \(c,d,e\), every five-cell permanent is one of

\[
                         ac,ad,ae,bc,bd,be.             \tag{1}
\]

These are the entries of a rank-one \(2\times3\) matrix and satisfy

\[
 ac\,bd=ad\,bc,\qquad ac\,be=ae\,bc,\qquad
 ad\,be=ae\,bd.                                        \tag{2}
\]

The checker proves at leaf level, without enumerating opposite triples,
that every survivor pair has exactly 126 valid crossing grades and no grade
collision.  Each of its 72 opposite leaves contributes zero, one, or two
distinct entries of (1).  Consequently every one of the 11,614,176 support
systems is a coordinate restriction of the same Segre template, composed
with its exact source-grade cylinder map.  This gives a uniform description
of the affine and torus stages and explains why coefficient grids are
unnecessary.

It does not yet give a uniform literal-rank theorem.  The source-grade leaf
maps remain pair-specific, and there is an exact obstruction to replacing
them by a fixed row functional.

## Source-faithful data and the stopping point

There are 14,112 pair/leaf records and 24,696 valid grade edges.  Normalizing
each grade by its exact quadratic basis, residual table, and pure-anchor
data gives 1,805 individual grade signatures.  The 196 pair spans collapse
to 66 exact universal-span signatures, but even after forgetting the labels
of the 72 opposite coordinates the full leaf multisets remain all distinct:

\[
            196\text{ pairs}\longrightarrow196
            \text{ source-faithful leaf fingerprints}.          \tag{3}
\]

The anchored old source has trivial old-site/colour stabilizer, so (3)
cannot be quotiented by an actual target-preserving permutation.

There is also no weight-independent row separator for any of the 196 pairs.
For each pair \(P\), let \(W(P)\) be the span of the quadratic and residual
cylinder data from all 126 grades incident to \(P\).  The exact pair sieve
verifies

\[
                         R_{\rm old}\subseteq W(P)       \tag{4}
\]

for every survivor.  Hence any linear functional annihilating all possible
leaf cylinders also annihilates the old residual.  A structural closure must
use the rank-one coupling (2) together with literal evaluated-column/Fitting
data; enlarging the universal linear span cannot work.

The resulting division of labour is sharp:

1. equations (1)--(2) are a single all-pair template for affine/torus
   intersection;
2. the labelled source-grade map supplies the exact affine section for each
   support; and
3. literal Fitting minors currently retain leaf provenance and are the
   remaining obstacle to an all-pair determinant identity.

Thus this template is a real structural compression, but not a claimed
transfer theorem for the already audited minors.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_segre_leaf_template.py
python3 -O computations/verify_n10_five_cross_segre_leaf_template.py
```

The checker reconstructs all leaf incidences and exact source signatures,
verifies the three Segre monomial identities, rechecks (4) over
\(\mathbb Q\), and audits the trivial anchored stabilizer.
