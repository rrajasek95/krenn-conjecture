# Exact affine signatures and a five-cross torus-minor palette

## Outcome

The remaining fixed-old five-cross problem does admit a finite exact
palette reduction, but the anchored old source prevents that palette from
being transferred wholesale between all two-centre supports.

Among the 196 two-centre pairs left by the earlier universal quotient:

1. the ambient old-site/colour classification has 12 shapes;
2. their exact universal \((Q,D)\)-spans have 66 signatures;
3. the signature multiplicities are
   \(1^{26},2^1,3^{30},6^1,9^8\); but
4. retaining the exact map from all 72 opposite coordinates to their
   source-derived grade data gives 196 distinct signatures.

Thus the 66-span quotient is a useful coarse sieve, not a symmetry theorem.
The fixed old source has trivial discrete stabilizer, and no two of the 196
pairs have the same full exact leaf map.  A determinant proved for one pair
cannot be transferred to another merely because their ambient shapes or
universal spans agree.

Nevertheless, exact affine grouping and a small torus-minor palette close
the first seven complete pair blocks: 417,480 five-cell supports, including
415,128 genuinely new grade-3-to-6 supports.  No literal cut-2 source
survives.  The exact unaudited frontier is reduced from 11,614,176 to
11,198,758 grade-3-to-6 supports.

This remains a fixed-old, fixed-cut N=10 statement.  It is not a Krenn
counterexample or an all-order induction theorem.

## 1. Source-faithful signature quotient

For a surviving two-centre pair \(P=\{x_1,x_2\}\), let \(G(P)\) be all
permanent grades obtained by pairing either centre with any of the 72
opposite coordinates.  In the universal constant-plus-linear quotient,
define

\[
 {cal W}(P)=\operatorname{span}
 \{Q_{2,p;h,i},D_{2,p}:p\in G(P)\}.                  \tag{1}
\]

All 196 spaces contain the old residual by construction.  Equality of
their exact rational row-echelon bases produces 66 signatures, with
multiplicity census

| multiplicity | signatures | pairs |
|---:|---:|---:|
| 1 | 26 | 26 |
| 2 | 1 | 2 |
| 3 | 30 | 90 |
| 6 | 1 | 6 |
| 9 | 8 | 72 |

This is the requested exact two-centre affine quotient.

For transfer of a five-cell calculation one needs more than (1).  For each
opposite coordinate \(y\), the checker records the exact individual grade
signatures of the zero, one, or two grades in
\(\{(x_1,y),(x_2,y)\}\).  An individual signature retains its rational
quadratic basis, its full residual table, and all three pure anchors.  The
multiset of these 72 leaf records distinguishes all 196 pairs.

The earlier 12 old-site/colour shapes therefore do not act as symmetries of
the anchored coefficient cylinders.  This is a certified stopping decision
against multiplying one orbit representative by an ambient symmetry count.

## 2. Exact affine palettes on seven complete blocks

Order the 196 pair survivors lexicographically and, for each pair, enumerate
all \(\binom{72}{3}=59,640\) opposite triples.  This is support enumeration,
not a coefficient grid.  Supports with zero grade or a sharing two-grade
image use the earlier theorems.  For each grade-3-to-6 support, reduce the
enlarged cylinder-plus-anchor equations exactly over \(\mathbb Q\) and group
identical reduced systems.

The first seven pairs and their exact palettes are:

| block | second centre after \((0,8;1,0)\) | affine signatures | affine supports | torus supports | non-monomial generic pivots |
|---:|---|---:|---:|---:|---:|
| 0 | \((0,8;1,2)\) | 182 | 612 | 204 | 4 |
| 1 | \((1,8;1,2)\) | 636 | 207 | 78 | 0 |
| 2 | \((2,8;0,2)\) | 295 | 0 | 0 | 0 |
| 3 | \((2,8;1,2)\) | 349 | 207 | 58 | 0 |
| 4 | \((2,8;2,2)\) | 350 | 0 | 0 | 0 |
| 5 | \((3,8;1,2)\) | 523 | 612 | 287 | 2 |
| 6 | \((4,8;1,2)\) | 551 | 207 | 78 | 1 |

For every affine support the checker substitutes its literal permanent
products or endpoint-swap sums and saturates by \(abcde\).  This leaves 705
torus candidates.  Literal evaluated-column determinants exclude 698 by a
square minor and an augmented residual minor which are both nonzero torus
monomials.

## 3. The seven exceptional generic pivots

Seven supports initially have square and augmented minors containing
simple rank-drop factors.  Across the three affected blocks these factors
are drawn from

\[
 e-c,\ e+c,\ d+e,\ d-c,\ d+c.                        \tag{2}
\]

Away from their zero divisors, the generic minors already exclude cylinder
membership.  On every divisor in (2), the checker selects a pivot at an
exact nonzero rational point and constructs its *global* determinant
polynomial.  It then verifies with a Groebner basis that

\[
 \langle f,\det M_f,\ tabcde-1\rangle=(1)             \tag{3}
\]

for the corresponding divisor \(f\).  Equation (3) says the special pivot
never vanishes on that divisor inside the coefficient torus.  The same
factorization occurs for a square minor and an augmented residual minor.

There are 12 divisor charts in total: seven for block 0, three for block 5,
and two for block 6.  One block-5 chart produces the factor
\(bc+ad+ae\); on \(d+e=0\) it becomes \(bc\), and the exact saturation (3)
certifies its nonvanishing.  All seven exceptional supports are therefore
closed, not frozen survivors.

## 4. Smallest candidate in the next block

The next unaudited pair is

\[
 P_7=\{(0,8;1,0),(5,8;1,2)\}.                         \tag{4}
\]

Scanning its opposite triples in exact coordinate order, the first 289
new supports fail either the affine equations or torus saturation.  The
first torus-affine candidate is

\[
\begin{aligned}
 &(0,8;1,0),\ (5,8;1,2),\\
 &(0,9;0,0),\ (0,9;1,2),\ (2,9;1,0).
\end{aligned}                                         \tag{5}
\]

For weights \(a,b,c,d,e\), its permanent map in exact grade order is

\[
                    (ae,bc,bd,be),                    \tag{6}
\]

and its complete enlarged affine system is the single equation

\[
                              ae=1.                    \tag{7}
\]

This is a genuine point of the affine torus relaxation.  It is not a
literal source: at evaluated column rank 21, a square pivot and an
augmented residual minor are both

\[
                              a^3bc^4.                 \tag{8}
\]

Equation (8) is nonzero on the torus, including the subvariety (7).  Thus
the first 290 new supports of block 7 are also closed.  Equations (4)--(8)
freeze the exact boundary from which a continuation can resume.

## 5. What remains and the stopping rule

The remaining 11,198,758 supports start immediately after (5) in block 7
and continue through the other 188 pair blocks.  Their exact condition is
still

\[
 \operatorname{rank}[C_2(S,w)\mid R_2(S,w)]
 =\operatorname{rank}C_2(S,w),\qquad \prod w_e\ne0,   \tag{9}
\]

with the three pure-anchor equations and literal source provenance.

The finite palette works well within a fixed exact leaf map: 59,640
supports reduce to a few hundred affine signatures and at most 287 torus
candidates in the audited blocks.  But the 196 leaf maps are distinct.
Continuing block-by-block is exact and reproducible, yet it is now a finite
enumeration campaign rather than a structural all-order argument.

The stopping rule is therefore sharp: transfer a palette only after proving
equality or an explicit conjugacy of the full labelled leaf maps.  Equality
of ambient shape or of the coarser 66 universal spans is insufficient.  If
no such conjugacy is found, this lane should be treated as a bounded N=10
falsification audit while the uniform proof effort seeks a structural
coefficient-cylinder identity.

## Reproduction

Run

```text
python3 computations/verify_n10_five_cross_affine_signature_palette.py
python3 -O computations/verify_n10_five_cross_affine_signature_palette.py
python3 -I computations/verify_n10_five_cross_affine_signature_palette.py
python3 -S computations/verify_n10_five_cross_affine_signature_palette.py
```

The checker uses exact rational arithmetic and Singular Groebner bases and
determinant factorizations.  It does not sample a coefficient grid.
