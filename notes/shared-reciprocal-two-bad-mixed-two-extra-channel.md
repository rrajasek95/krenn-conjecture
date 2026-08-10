# Shared-reciprocal two-bad packet: two-extra channel theorem

## Verdict

The first non-minimal coupled-repair boundary is empty.  Starting from any
of the four minimal simultaneous private-row mate charts, adjoining any two
further nonzero endpoint-colour coordinates leaves

\[
  \operatorname{rank}\Phi\geq 14,
  \qquad \dim\ker\Phi\leq 1.
\]

Thus two further coordinates cannot restore the two independent kernel
directions required by the two-bad pure-kernel-product packet.  No rational
or algebraic \(X_t\) seed reaches the subsequent kernel-product test.

The exact replay is
`computations/verify_shared_reciprocal_two_bad_mixed_two_extra_channel.py`.

## Chart and variables

The four base charts are the products of the two alternate routes for each
private word,

\[
  (03/14,03/14),\ (03/14,04/13),\
  (04/13,03/14),\ (04/13,04/13),
\]

with localized mate parameters \(x,p\ne0\).  Each chart has 16 occupied
coordinates and 74 unused coordinates.  A two-extra chart chooses an
unordered pair and assigns it nonzero weights \(h,k\).  Hence there are

\[
  4\binom{74}{2}=10{,}804
\]

literal charts.

The exact \(S_5\times S_3\) support stabilizer of the four-chart family is
the identity.  Consequently none of these literal pairs can be silently
identified by a vertex/colour symmetry.  This is important: the tempting
rule “each coordinate was harmless separately, so the pair is harmless” is
false because the two new cells can occur together in a cofactor matching.

## Source-faithful pruning

The cofactor map \(\Phi\) is quadratic in source cells.  For every one-extra
coordinate, retain all row sets of the pinned one-extra maximal-minor
certificate.  For a pair \(a,b\), the second cell \(b\) can alter that
certificate only through products of \(b\) with a base cell or with \(a\)
on disjoint physical edges.  Checking those literal matrix positions proves
that 7,376 pair charts inherit an unchanged one-extra Laurent certificate.

This is stricter than output/support pruning and retains the \(hk\) cross
term.  The typewise counts are

| mate type | all pairs | unchanged certificate | new charts |
|---|---:|---:|---:|
| 03/14, 03/14 | 2,701 | 1,847 | 854 |
| 03/14, 04/13 | 2,701 | 1,841 | 860 |
| 04/13, 03/14 | 2,701 | 1,848 | 853 |
| 04/13, 04/13 | 2,701 | 1,840 | 861 |

## Exact Fitting calculation

For each of the remaining 3,428 charts, delete the old duplicate column and
replay the two one-extra row-basis families on the resulting
\(243\times14\) matrix.  In 2,969 charts one of these determinants is a
Laurent monomial, so it is nonzero throughout the torus.

The remaining 459 charts require complementary maximal minors.  Deterministic
rational pivot charts and deterministic row permutations give a finite
minor family \(f_1,\ldots,f_s\).  The checker verifies over \(\mathbb Q\)

\[
 \left\langle f_1,\ldots,f_s,
 uxhpk-1\right\rangle=(1).
\]

The typewise exceptional counts are respectively

\[
  123,\quad120,\quad95,\quad121.
\]

This saturation is the precise nonzero-weight statement: there is no common
torus point at which all recorded rank-14 minors vanish.  Some fixed-column
minor families do have algebraic zero loci, but alternate row/column bases
retain rank 14 there; those loci are chart artifacts, not kernel seeds.

## Scope

This is a complete theorem for exactly two additional coordinates beyond
the four canonical minimal mate charts, with arbitrary nonzero complex
weights.  It is not an unrestricted mixed-colour theorem and does not by
itself classify repairs using three or more new coordinates.  It does,
however, move the exact obstruction frontier two full coupled coordinates
beyond the minimal private-row repair and rules out every seed in that
layer before any output-only invariant is used.
