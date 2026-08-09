# Exact closure of five-cross pair blocks 8 through 14

## Outcome

The source-faithful five-cross palette closes the next seven complete
two-centre blocks.  These are survivor-pair indices 7 through 13 in the
lexicographic order fixed by the earlier checker, or blocks 8 through 14 in
one-based language.

The calculation covers another

\[
                         7\binom{72}{3}=417,480
\]

grade-3-to-6 supports.  Exact affine reduction leaves 1,026 candidates,
rank-one torus saturation leaves 312, and literal evaluated-column minors
exclude all 312.  There is no cut-2 source in these blocks.

Together with the preceding seven-block theorem, the cumulative exact
closure is 832,608 genuinely new five-cell supports.  An exact prefix of
1,712 more supports in the next block is also closed, leaving 10,779,856
unaudited grade-3-to-6 supports.

This is a bounded fixed-old N=10 theorem, not a Krenn counterexample or an
all-order argument.

## 1. Complete block census

The seven two-centre pairs all begin with \((0,8;1,0)\).  Their second
centres and exact affine palettes are:

| block index | second centre | affine signatures | affine candidates | torus candidates | generic divisor cases |
|---:|---|---:|---:|---:|---:|
| 7 | \((5,8;1,2)\) | 719 | 612 | 278 | 5 |
| 8 | \((6,8;0,2)\) | 265 | 0 | 0 | 0 |
| 9 | \((6,8;1,2)\) | 400 | 207 | 28 | 0 |
| 10 | \((6,8;2,2)\) | 294 | 0 | 0 | 0 |
| 11 | \((7,8;0,2)\) | 148 | 0 | 0 | 0 |
| 12 | \((7,8;1,2)\) | 215 | 207 | 6 | 0 |
| 13 | \((7,8;2,2)\) | 204 | 0 | 0 | 0 |

The four affine-empty blocks fail before any weight parametrization.  In
the other three blocks, the checker substitutes every literal permanent
product or endpoint-swap sum and saturates by \(abcde\).  Of the 312 torus
candidates, 307 have a square pivot and augmented residual minor which are
both nonzero torus monomials.

## 2. The five generic exceptions

All five non-monomial generic pivots occur in block 7.  Their rank-drop
factors are drawn from

\[
                   d-e,\ d+e,\ c-e,\ c+e,\ c-d,\ c+d.
\]

For each factor \(f\), a pivot selected at an exact point of \(f=0\)
produces a global square determinant equal to its augmented residual
determinant.  The checker then verifies exactly

\[
             \langle f,\det M_f,\ tabcde-1\rangle=(1).
\]

There are nine divisor charts across the five supports.  Hence the special
pivot is nonzero everywhere on its divisor inside the coefficient torus,
while the generic pivot covers the complement.  All five supports are
excluded for arbitrary nonzero complex weights.

## 3. Frozen boundary in the next block

The next pair is

\[
        \{(0,8;1,2),(1,8;1,0)\}.                       \tag{1}
\]

In exact opposite-triple order, the first 1,711 new supports fail the
affine equations or torus saturation.  The first torus-affine candidate is

\[
\begin{aligned}
 &(0,8;1,2),\ (1,8;1,0),\\
 &(0,9;0,0),\ (3,9;1,2),\ (4,9;1,0).
\end{aligned}                                          \tag{2}
\]

With weights \(a,b,c,d,e\), its permanent map in exact grade order is

\[
                       (ad,ae,bc,bd,be),                \tag{3}
\]

and its enlarged affine system is the single equation

\[
                              be=1.                     \tag{4}
\]

At literal evaluated-column rank 20, a square pivot and an augmented
residual minor are both

\[
                          -a^9b^3d^{12}.                \tag{5}
\]

This is nonzero on the coefficient torus, including (4), so the candidate
is not a literal source.  Equations (1)--(5) freeze the exact continuation
point after 1,712 closed supports in block 14.

## Scope and reproduction

The exact remaining frontier contains 10,779,856 grade-3-to-6 supports.
Ambient old-site/colour shape remains insufficient for transferring block
certificates because the anchored leaf maps differ.  The present palette is
source-faithful and uses no coefficient grid.

Run

```text
python3 computations/verify_n10_five_cross_pair_blocks_8_14.py
python3 -O computations/verify_n10_five_cross_pair_blocks_8_14.py
python3 -I computations/verify_n10_five_cross_pair_blocks_8_14.py
python3 -S computations/verify_n10_five_cross_pair_blocks_8_14.py
```

All affine arithmetic is exact over \(\mathbb Q\); Singular performs the
torus saturation and determinant/divisor certification.
