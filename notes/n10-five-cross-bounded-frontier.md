# The bounded fixed-old five-cross frontier

## Outcome

The support-size-five audit cleanly separates one closed topology from one
large genuinely new topology on the anchored N=10 forced-pair lift.

Modulo the exact swap of new vertices 8 and 9, all 240,504,264 five-cell
supports split as follows:

| split across 8 and 9 | support orbits | status on fixed cut 2 |
|---|---:|---|
| \(5+0\) | 13,991,544 | permanent zero; earlier theorem |
| \(1+4\) | 74,072,880 | excluded uniformly here |
| \(2+3\) | 152,439,840 | reduced to 11,689,440; general case open |

The old-source/cut-2 discrete stabilizer remains the identity.  Thus these
are actual anchored-source orbit counts; no hidden old-vertex or global
colour symmetry reduces them further.  This calculation finds no N=10
source and is not a Krenn counterexample.

## 1. Exact permanent-grade census

A cross coordinate has an old endpoint-colour node and a colour at its new
endpoint.  A valid \(X\)-\(Y\) pair uses distinct old vertices.  Its
swap-symmetrized permanent grade is determined by the unordered pair of
old endpoint-colour nodes and the ordered new colours.  The checker verifies
that this combinatorial key agrees exactly with all 2,268 source-derived
grade classes.

For a \(1+4\) star, the singleton has 63 valid and nine invalid opposite
coordinates.  Therefore the number with \(k\) grades is

\[
             72\binom{63}{k}\binom9{4-k}.
\]

The census is

| grades | star orbits |
|---:|---:|
| 0 | 9,072 |
| 1 | 381,024 |
| 2 | 5,062,176 |
| 3 | 25,732,728 |
| 4 | 42,887,880 |

For the \(2+3\) split, a two-coordinate side has only five ambient equality
types: three same-old-vertex types, and different-old-vertex types with
equal or unequal new colours.  Their multiplicities are

\[
                        72, 72, 144, 756, 1512.
\]

Enumerating the 72 choose 3 opposite triples once for each type gives the
full exact census:

| grades | \(2+3\) support orbits |
|---:|---:|
| 0 | 24,192 |
| 2 | 689,472 |
| 3 | 1,936,872 |
| 4 | 23,677,920 |
| 5 | 58,419,144 |
| 6 | 67,692,240 |

There are no one-grade supports in this topology.

## 2. What scales from four cells

### Centre-universal stars

For each singleton centre \(x\), grant independently every quadratic
cofactor and residual direction from all 63 grades incident to \(x\), in
the quotient by the universal constant-plus-linear column space.  The old
cut-2 residual remains outside this larger space at all 72 centres, exactly
as in the four-cell calculation.

Every four-leaf star uses a subspace of this centre-universal space.
Consequently all 74,072,880 \(1+4\) supports fail cut 2 for arbitrary
nonzero weights.  The argument is independent of the number and choice of
leaves, so this part of the template scales without new enumeration.

### Two-centre reduction

On the two-coordinate side of a \(2+3\) support, the two-centre universal
test leaves only 196 of the 2,556 pairs.  Thus the literal frontier drops
from 152,439,840 to

\[
                       196\binom{72}{3}=11,689,440.
\]

Its grade census is

| grades | pair-reduced supports |
|---:|---:|
| 0 | 2,688 |
| 2 | 72,576 |
| 3 | 133,824 |
| 4 | 1,917,432 |
| 5 | 4,224,312 |
| 6 | 5,338,608 |

Every two-grade pair in this reduced census is one of the 231,336 sharing
class pairs excluded by the earlier source-independent theorem.  The
zero-grade cases are covered by permanent-zero exclusion.  The exact new
frontier is therefore the 11,614,176 supports with three through six
grades.

The two-centre template stops here: for each of the 196 pairs its universal
space already absorbs the old residual, so further enlarging that space
cannot recover an obstruction.  Actual evaluated-column coupling is now
essential.

## 3. A closed five-variable biclique family

The smallest natural full-grade family fixes one old endpoint-colour node
on each side, takes two new colours on the first side, and all three new
colours on the second.  There are 1,512 such \(2\times3\) old-node
bicliques before the source-dependent pair test.  Exactly 294 use one of
the 196 surviving pairs.

All 294 have six independent permanent grades.  The enlarged affine
cylinder and pure-anchor equations leave 14.  Substituting the literal
rank-one products

\[
             ac,\ ad,\ ae,\ bc,\ bd,\ be
\]

and saturating by \(abcde\) leaves six.  The checker constructs the literal
21 evaluated cofactor columns for those six.  In every case a square minor
and an augmented residual minor are the same nonzero torus monomial, up to
sign.  The certificate census is

| column rank | monomial | cases |
|---:|---|---:|
| 20 | \(\pm a^9c^8d\) | 2 |
| 21 | \(\pm a^4c^3d\) | 4 |

Hence all six fail for arbitrary nonzero \(a,b,c,d,e\), and the entire
old-node biclique family is closed.

## 4. The lexicographically first torus-affine candidate

As a guard against mistaking the enlarged affine relaxation for an actual
source, the checker scans the first pair-surviving support block in exact
coordinate order.  The first support with three or more grades whose
affine equations meet the coefficient torus is

\[
\begin{aligned}
 &(0,8;1,0),\ (0,8;1,2),\ (0,9;0,0),\\
 &(3,9;1,0),\ (3,9;1,2).
\end{aligned}
\]

The third cell is permanent-inert because it repeats old vertex 0.  With
weights \(a,b,c,d,e\), the four visible permanent scalars are

\[
                         ad,\ ae,\ bd,\ be.
\]

The enlarged affine system places no conditions on them, but the literal
evaluated matrix does: at generic rank 20 the square pivot and one
augmented residual minor are both

\[
                            -a^9d^8e.
\]

This is nonzero on the coefficient torus.  Thus even the earliest apparent
five-cell repair is exactly excluded; it is not a survivor of the literal
cylinder equations.

## 5. Frozen remaining system and stopping rule

For each of the remaining grade-3-to-6 supports \(S\), with its five
nonzero weights \(w\), the unresolved fixed-cut condition is

\[
 \operatorname{rank}[C_2(S,w)\mid R_2(S,w)]
   =\operatorname{rank}C_2(S,w),\qquad \prod_{e\in S}w_e\ne0,
\]

together with the three pure-anchor equations.  Both matrices are literal
degree-at-most-two matching polynomials, and every permanent scalar retains
its source product or endpoint-swap sum.

Raw exact saturation of 11.6 million systems is not a useful next step.
The bounded evidence says the determinant template scales once supports
have been reduced, but a further source-faithful signature or structural
identity is needed before applying it globally.  A sensible stopping rule
is: first quotient the 196 surviving pairs by equality of their full
labelled \((Q,D,L)\) data against right triples; continue only if that gives
a small exact signature set.  Otherwise this lane should yield to a
structural coefficient-cylinder identity rather than a coefficient grid.

## Scope and reproduction

The old N=8 source, the isolated diagonal pair, and cut 2 are fixed.  The
result closes all five-cell stars and the stated old-node bicliques, not all
five-cell additions, arbitrary old-source deformations, or an N-to-N+2
induction step.

Run

```text
python3 computations/verify_n10_five_cross_bounded_frontier.py
python3 -O computations/verify_n10_five_cross_bounded_frontier.py
python3 -I computations/verify_n10_five_cross_bounded_frontier.py
python3 -S computations/verify_n10_five_cross_bounded_frontier.py
```

The checker uses exact rational arithmetic and invokes Singular for torus
saturation and determinant factorization.
