# Permanent-zero cross blocks cannot rescue any anchored N=10 cut

## Outcome

Every permanent-zero cross addition to the anchored N=10 forced-pair lift is
excluded at the source level.  Even after enlarging each cut cylinder by all
linear cofactor directions from all 144 cross coordinates independently,
the unchanged forced-lift residual has a nonzero exact quotient row on every
cut.

Consequently, no cross source with zero symmetrized quadratic permanent data
can have even one complete high-sector cylinder.  In particular it cannot
preserve the inherited cuts \(2,3,4\) and cannot create a candidate fourth
cut \(0,1,5\).  This holds for arbitrary complex cross weights and arbitrary
support, provided the old anchored N=8 source and the isolated diagonal pair
are kept fixed.

The smallest nontrivial permanent-zero four-cell block remains a useful
realizable survivor: it has nonzero cross weights, preserves all three pure
anchors, and leaves the full tensor unchanged.  But its linear cofactor
directions are far too small to complete a cut.  It is not a Krenn
counterexample.

## 1. Exact degree decomposition

Let \(A_{10}=A_8\otimes g_{89}+X+Y\), where \(X\) contains the cross cells
incident to new vertex 8 and \(Y\) those incident to new vertex 9.  A full
matching can use neither one cross edge alone nor more than two cross edges.
Therefore

\[
 H_{10}(A_{10})=H_8\otimes g_{89}
       +\sum_p\pi_p(X,Y)D_p,                            \tag{1}
\]

where \(p\) runs over swap-symmetrized permanent grades and \(D_p\) is the
corresponding old \((N-2)\)-site cofactor inserted at its two endpoints.

Likewise, every labelled cofactor column on a cut has the exact form

\[
 c_{h,i}(X,Y)=c^{(0)}_{h,i}
       +\sum_e x_e L^{(e)}_{h,i}
       +\sum_p\pi_p(X,Y)Q^{(p)}_{h,i}.                  \tag{2}
\]

There are no higher terms.  The linear directions occur in new-hole
columns; the quadratic directions occur when both new vertices match
outward in an old-hole column.

If the permanent vector vanishes,

\[
                         \pi(X,Y)=0,                    \tag{3}
\]

then (1)--(2) reduce to

\[
 H_{10}=H_8\otimes g_{89},
 \qquad
 c_{h,i}=c^{(0)}_{h,i}+\sum_ex_eL^{(e)}_{h,i}.           \tag{4}
\]

Thus the full residual and all three pure anchors are exactly those of the
forced lift.  Only lower-degree one-cross cofactor directions remain.

## 2. Universal linear cylinder

For each cut \(z\), define

\[
 {\cal U}^{\rm lin}_z=
 \operatorname{span}_{\mathbb Q}
 \left(
   \{c^{(0)}_{h,i}\}_{h,i}
   \cup
   \{L^{(e)}_{h,i}:e\text{ any of 144 cross coordinates},h,i\}
 \right).                                               \tag{5}
\]

This is a strict superspace of every actual permanent-zero cofactor span:
it allows each base column and every derivative direction to be chosen
independently, whereas an actual source has only 21 labelled columns with
fixed linear combinations.  Hence

\[
 \operatorname{span}\{c_{h,i}(X,Y)\}_{h,i}
                         \subseteq {\cal U}^{\rm lin}_z. \tag{6}

Failure modulo (5) is therefore a uniform source-level exclusion, not a
sample of cross coefficients.

The checker constructs every derivative at weights 1 and 2, verifies its
exact affine dependence, and takes the rational span.  The universal ranks
are

| cut | \(\dim {\cal U}^{\rm lin}_z\) |
|---:|---:|
| 0 | 126 |
| 1 | 126 |
| 2 | 126 |
| 3 | 126 |
| 4 | 126 |
| 5 | 135 |

The ambient row dimension is \(3^7=2187\).  The rank increase over an actual
21-column cylinder is intentionally generous.

## 3. Exact residual witnesses

Let \(R_z\) be the boundary-row table of

\[
                  H_8\otimes g_{89}-\Delta_{10,3}.      \tag{7}
\]

Exact quotient reduction modulo (5) gives:

| cut | boundary words outside \({\cal U}^{\rm lin}_z\) |
|---:|---|
| 0 | 111, 222, 000, 012 |
| 1 | 111, 222, 000, 012 |
| 2 | 111 |
| 3 | 222 |
| 4 | 111, 222 |
| 5 | 000, 012 |

For example, the fixed cut 2 retains the nonzero normal form

\[
                         e_{1089}+e_{1097},              \tag{8}
\]

and fixed cut 3 retains

\[
                         e_{2178}+e_{2182}.              \tag{9}
\]

Every cut has at least one such witness.  By (6), no actual permanent-zero
cylinder can contain all rows of (7).  High-sector completeness already
fails, so no lower-sector audit is needed for the exclusion.

## 4. The smallest realizable survivor

The four-cell block

\[
 Z=E_{08;00}+E_{19;00}+E_{18;00}-E_{09;00}              \tag{10}
\]

has visible permanent \(1-1=0\).  It is the smallest nontrivial cancellation
which uses both new vertices and two distinct old endpoints: the two
endpoint-swapped monomials use four disjoint coordinates, so three cells
cannot cancel them.

The checker reconstructs (10) literally and verifies

\[
                 H_{10}(A_8\otimes g+Z)=H_8\otimes g.   \tag{11}
\]

The three pure coefficients remain \((1,1,1)\).  Its actual cut census is

| cut | actual cofactor rank | full residual membership |
|---:|---:|---|
| 0 | 19 | false |
| 1 | 19 | false |
| 2 | 20 | false |
| 3 | 20 | false |
| 4 | 20 | false |
| 5 | 21 | false |

This source is a nonzero preimage of the zero permanent grade, but it does
not preserve a single complete cut at N=10.

One cross edge is an even smaller trivial permanent-zero source, and pairs
which share a new or old endpoint also have no quadratic full term.  The
universal exclusion covers all of them as well as arbitrary sums and larger
permanent-zero blocks.

## 5. Consequence for the contraction route

The previous note proved that a nonzero permanent vector cannot hide in the
nine-dimensional exact all-cut kernel.  The present note handles the only
remaining exact-invisibility case, \(\pi=0\): its lower-degree linear columns
cannot complete any anchored cut.  Together, the two results eliminate

1. nonzero permanent grades whose full and quadratic cofactor data cancel
   exactly, and
2. zero permanent grades attempting to rescue the cylinders using only
   one-cross linear directions.

What remains outside this conclusion is a more general evaluated cylinder
cancellation in which a **nonzero** permanent grade does not vanish in the
raw labelled data but is absorbed into a parameter-dependent span involving
constant, linear, and quadratic columns.  That is a determinantal
span-membership problem, not an invisible-data kernel problem.

## 6. Scope and stability

The old N=8 source is fixed to the certified anchored family, and vertices
8,9 begin as its isolated diagonal lift.  The universal space (5) includes
all cross additions from old vertices 0 through 7, in all endpoint colours,
but it does not include arbitrary simultaneous changes of old source cells.

On an inherited forced-pair tower, the quotient witnesses contract back to
the displayed N=10/N=8 witnesses as long as new cross edges avoid the
intervening isolated old pair.  A full arbitrary-N stability theorem would
need to include linear directions incident to all intervening vertices and
is not claimed here.

The result is a source-level N=10 exclusion, not a proof of Krenn's
conjecture.  It is nevertheless stronger than a finite search over supports
or weights: all 144 cross directions are included independently in the
universal superspace.

## Reproduction

    python3 computations/verify_n10_permanent_zero_cross_linear_superspace_exclusion.py
    python3 -O computations/verify_n10_permanent_zero_cross_linear_superspace_exclusion.py
    python3 -I computations/verify_n10_permanent_zero_cross_linear_superspace_exclusion.py
    python3 -S computations/verify_n10_permanent_zero_cross_linear_superspace_exclusion.py

All matching expansions, affine derivative identities, span ranks, and
quotient normal forms are exact over the rationals.
