# Post-KS same-head carriers split into a kernel test and a rank-quotient test

## Outcome

Assume the exact residual-q KS lift used in `2593831`.  It closes the
unequal-tail endpoint holonomy and resolves the E14 endpoint orientation,
but the first transverse-rank gate does not collapse.  The exact
classification has two independent linear tests:

1. a complete-column dependence among occupied cells in one endpoint row
   gives an anchor-safe physical support descent;
2. after those columns are independent, restoring a deleted-star profile
   `(2,2,3,3)` is equivalent to visibility in both one-dimensional deficient
   star quotients.

The pinned same-head/target-coloop modules realize the branch where neither
test fires.  Adjoining the KS endpoint determinant raises endpoint
orientation rank from one to two, but leaves the physical complete-column
kernel zero, the pure target on its original coloop port, the outer-head
span one, and the deleted-star profile `(2,2,3,3)`.

Checker:
`computations/verify_h3_post_ks_same_head_rank_support_counterguard.py`.

This is a structural counterguard, not a physical GHZ source.  Its positive
same-row support theorem is source-valid and applies to a synchronized
physical source.

## Complete same-row dependence always descends support

Fix one literal endpoint row, say `p_i`, and let

\[
 z_1,\ldots,z_m
\]

be its occupied scalar cells.  With `s`, `q`, and every other endpoint row
fixed, write the complete labelled response column

\[
 \mathcal L(z_a)=
 \bigl(z_as_1q^{[2]},z_as_2q^{[2]}\bigr),             \tag{1}
\]

retaining every fine output coefficient.  The identical argument applies
to a fixed `s_j` row.

Suppose there is a relation

\[
             \sum_a k_a\mathcal L(z_a)=0,
             \qquad k_e\ne0.                          \tag{2}
\]

If the current scalar coefficients are `x_a`, make the finite update

\[
                   x'_a=x_a-\frac{x_e}{k_e}k_a.       \tag{3}
\]

Then `x'_e=0`, and (2) says that both complete response tensors involving
the fixed endpoint row are unchanged.  The other two response tensors and
the unary top do not involve that row and are unchanged as well.  Every
coefficient modified in (3) was already occupied, so no scalar support cell
is introduced; at least `z_e` is deleted.

The update is safe for the lexicographic anchor invariant.  All the `z_a`
share the coordinate endpoint `(P,i)` (or `(S,j)`).  Hence none is a mutual
coordinate anchor.  Any old mutual anchor is disjoint from every changed
cell, and deleting any subset of those cells preserves it.  The checker
exhausts arbitrary ambient support graphs around three same-row cells and
all seven nonempty cancellation subsets.

Thus:

> At a maximum-mutual-anchor, then minimum-support representative, the
> complete response columns of the occupied cells in each fixed `p_i` or
> `s_j` row are linearly independent.

This strictly extends the earlier two-column proportional reduction.  It
also gives the exact support criterion for a carrier `e`:

\[
 e\text{ is deletable within its occupied row}
 \quad\Longleftrightarrow\quad
 \mathcal L(e)\in
 \operatorname{span}\{\mathcal L(z):z\ne e\}.         \tag{4}
\]

No Hall statement is used in (1)--(4).

## The remaining rank test is a two-quotient visibility test

After the support branch is excluded, let the two deficient deleted-star
maps have images `U` and `V`, each of rank two in a three-dimensional target.
Their quotient lines are

\[
 Q_u=k^3/U,
 \qquad Q_v=k^3/V.                                    \tag{5}
\]

Equivalently choose nonzero cokernel covectors `lambda_u,lambda_v`.  For a
new physical arm `z`, with endpoint-star projections `z_u,z_v`, the single
arm restores both ranks precisely when

\[
                 \lambda_u(z_u)\lambda_v(z_v)\ne0.    \tag{6}
\]

More generally a set of source columns restores `(3,3,3,3)` exactly when
its image is nonzero in each quotient in (5).  Separate columns may repair
the two sides.  A same-head column is killed by both quotient covectors and
leaves `(2,2,3,3)`.  A one-sided column gives `(3,2,3,3)` or `(2,3,3,3)`;
a double-transverse column, or two split transverse columns, gives
`(3,3,3,3)`.

This is the sharp distinction that selected `2x2` response minors do not
capture.  Those minors can be nonzero while both missing deleted-star rows
remain absent.

## The exact post-KS counterguard

Take the second three-column circuit from the full-five target-coloop
boundary.  Its complete columns have rank three and joint kernel zero.  Its
pure target `X2` is supported only on port zero.  Give the occupied tails the
same local outer head from the minimum axis-circuit guard.  Their complete
tail independence is compatible with outer-head span one and profile

```text
(2,2,3,3).
```

Now adjoin the old signless endpoint row and the KS endpoint determinant,

\[
                          S=(1,1),\qquad D=(1,-1).     \tag{7}
\]

in the endpoint boundary block.  The combined five columns have rank five:
the three physical response columns remain injective, while `(S,D)` has
rank two.  The KS boundary hypothesis has zero target and anchor and does
not assert any new physical deleted-star column.  The smallest compatible
product module therefore gives `(S,D)` zero projection to the two physical
star quotients.  With that compatible choice, (7) does not change the target
support or either quotient in (5).  The resulting ledger is

```text
endpoint orientation rank       1 -> 2
physical column kernel              0
pure target support                 {port 0}
outer-head span                     1
deleted-star profile                (2,2,3,3)
deficient quotient visibility       0 / 0.
```

This proves the logical boundary: the displayed KS boundary hypothesis plus
the five aggregate rows does not imply either physical support descent or
transverse rank.  A construction of the unknown physical lift may carry
additional star data, but that is a new hypothesis to prove.  The example is
a product of exact structural modules, not asserted to satisfy the full
common-`q` source equations.

## First missing theorem

The downstream source theorem can now be stated without mixing in Hall or
termination:

> In the independent target-coloop branch, a literal common-`q` four-hole
> exchange either creates a complete same-row dependence touching the
> carrier, or produces occupied physical columns whose projections are
> nonzero in both deficient deleted-star quotient lines.

The first conclusion invokes (3) and strictly lowers physical support.  The
second restores all four deleted-star ranks and only then permits a curved
four-good or subsequent Hall landing.  If the exchange instead exposes an
off-anchor carrier, that is a separate already routed physical alternative.

The KS typed-component change

\[
                          (s,c)\mapsto(s,c-1)
\]

is also separate: it proves termination of the endpoint/tail provenance
reduction, not a decrease of physical scalar support.  The counterguard
therefore does not reopen the holonomy branch, and no Hall lock is used to
hide the rank defect.

## Verification

Run:

```text
python3 computations/verify_h3_post_ks_same_head_rank_support_counterguard.py
python3 -O computations/verify_h3_post_ks_same_head_rank_support_counterguard.py
python3 -I -S computations/verify_h3_post_ks_same_head_rank_support_counterguard.py
```

The checker pins the conditional KS landing, same-head `(2,2,3,3)` guard,
full-five target-coloop module, and the earlier proportional anchor-safe
support move.

Frozen ledger SHA-256:

```text
6fec2ed27b57816687e7084ef6fa01c042bfc8dbef9c1d50ecdbf7438b09b154
```
