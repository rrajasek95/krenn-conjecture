# Exact closure of five-cross pair blocks 15 through 21

## Outcome

The source-faithful fixed-old N=10 audit closes the next seven complete
two-centre blocks.  These are survivor-pair indices 14 through 20 in the
lexicographic order fixed by the affine-signature checker, or blocks 15
through 21 in one-based language.

The calculation covers

\[
                         7\binom{72}{3}=417,480
\]

new grade-3-to-6 supports.  Exact affine reduction leaves 1,845 candidates,
rank-one torus saturation leaves 779, and literal evaluated-column minors
exclude all 779.  There is no literal cut-2 source in these blocks.

The cumulative exact closure is now 1,250,088 of the 11,614,176 supports in
the five-cross pair frontier.  The remaining unaudited frontier has
10,364,088 supports and begins at pair index 21.

This is a bounded fixed-old, fixed-cut N=10 theorem.  It is not a Krenn
counterexample and it does not establish an all-order contraction.

## 1. Complete block census

The seven pairs, their exact affine palettes, and their literal frontiers
are:

| pair index | second centre after \((0,8;1,2)\) | affine signatures | affine candidates | torus candidates | generic divisor supports |
|---:|---|---:|---:|---:|---:|
| 14 | \((1,8;1,0)\) | 647 | 207 | 78 | 35 |
| 15 | \((2,8;0,0)\) | 298 | 0 | 0 | 0 |
| 16 | \((2,8;1,0)\) | 349 | 207 | 58 | 0 |
| 17 | \((2,8;2,0)\) | 295 | 0 | 0 | 0 |
| 18 | \((3,8;1,0)\) | 523 | 612 | 287 | 8 |
| 19 | \((4,8;1,0)\) | 541 | 207 | 78 | 78 |
| 20 | \((5,8;1,0)\) | 719 | 612 | 278 | 5 |

Among the 779 torus candidates, 653 have a square pivot and an augmented
residual minor that are both nonzero torus monomials.  The remaining 126
supports are covered by exact divisor charts.

Blocks 14, 18, and 20 use 53 one-layer charts from the established palette.
Their rank divisors are drawn from

\[
 bc+1,\ bd+1,\ be+1,\ c\mathbin{\pm}d,\
 c\mathbin{\pm}e,\ d\mathbin{\pm}e.
\]

For each chart the checker recomputes a global square and augmented minor at
an exact nonzero point of the divisor, then proves its nonvanishing on the
whole torus divisor by a Groebner-basis unit-ideal calculation.

## 2. The three-component divisor in block 19

Block 19 has 77 supports closed by 80 direct charts: 15 have divisor
\(bd+1\), three have the disjoint pair \((bd+1)(bd-1)\), and 59 have
divisor \(bc+1\).  The remaining support is

\[
\begin{aligned}
 &(0,8;1,2),\ (4,8;1,0),\\
 &(1,9;1,0),\ (3,9;1,2),\ (4,9;0,2).
\end{aligned}                                                   \tag{1}
\]

Its five permanent grades are \((318,338,344,750,1571)\), its permanent
map is

\[
                         (ac,ad,ae,bc,bd),                       \tag{2}
\]

and the complete affine system reduces to \(bc=1\).  At generic evaluated
rank 20, the chosen square pivot and first augmented residual minor both
factor as

\[
 a^4b^5d^2(e-d)(bc+1)^3(d+e)^6.                                \tag{3}
\]

Thus the generic chart leaves three rank-divisor components.  A first-layer
chart on \(e-d=0\) has residual factor \((bc+1)(d+e)\); one on
\(e+d=0\) has residual factor \((bc+1)(e-d)\); and one on \(bc+1=0\)
has residual factor \((e-d)(e+d)\).  The two components \(e-d=0\) and
\(e+d=0\) cannot meet in the coefficient torus.  The only remaining loci
are therefore

\[
 \{bc+1=e-d=0\},\qquad \{bc+1=e+d=0\}.                         \tag{4}
\]

At the exact points \((a,b,c,d,e)=(2,1,-1,1,1)\) and
\((2,1,-1,1,-1)\), the checker selects two more global pivots.  On the
first locus their square and augmented determinants reduce to a nonzero
torus monomial times \(d+e\); on the second they reduce to a nonzero torus
monomial times \(e-d\).  Exact localized unit-ideal checks certify both as
nonvanishing on (4).  Hence (1) is closed by two codimension-two charts; it
is not a literal survivor.

This is the first depth-two chart in the five-cross pair campaign.  It is
still an exact divisor cover, not a coefficient grid.

## 3. Scope and continuation

The next pair is

\[
                 \{(0,8;1,2),(6,8;0,0)\}.                     \tag{5}
\]

No transfer to (5) is claimed: the anchored old source has trivial discrete
stabilizer and all 196 labelled leaf maps remain distinct.  Future bounded
work may reuse the finite monomial/divisor palette only after auditing the
exact leaf map for each pair.  A support that survives all such minors would
still require the full fixed-cut source equations before it could be called
a counterexample.

Run

```text
python3 computations/verify_n10_five_cross_pair_blocks_15_21.py
python3 -O computations/verify_n10_five_cross_pair_blocks_15_21.py
```

The checker uses exact rational arithmetic and Singular determinant,
saturation, and localized unit-ideal calculations.
