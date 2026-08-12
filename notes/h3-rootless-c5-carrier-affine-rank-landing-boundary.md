# The normalized C5 carrier reaches one sharp rank-landing boundary

## Exact composition

At a synchronized minimum-support representative, every nonzero normalized
`C5` residual tail has an off-cycle cell `e` with complete physical column

\[
 C_e=(D_eq^{[3]},D_e(p_i s_jq^{[2]})_{i,j=1,2}).
\]

If `C_e=0`, deleting `e` is exact and mutual-anchor safe.  Otherwise one of
its unary or response components is nonzero.  Composing the committed
source theorems gives the following exact routes.

* A nonzero response component at the original complement has the forced
  hole `(x,v)`.  Its complete six-term coefficient has one same-tail
  opposite orientation and four different-tail `C4` terms.
* Proportional **complete** same-star columns give an exact one-sided
  joint-kernel update.  Since two distinct components of one star row share
  a coordinate endpoint, neither is a mutual anchor; the update is
  unconditionally `nu`-safe and strictly lowers support.
* Nonproportional endpoint pairs define nonzero determinant functionals on
  the common output dual.  One integral combination of separate witnesses
  avoids both kernels, so the common-covector Fitting carrier is
  source-valid even when no literal fine word witnesses both minors.
* A different-tail `C4` either exposes an off-anchor typed cell or enters
  the finite cross-intersecting Hall normal form: star, triangle, or
  `K_{2,2}`.

Once the carrier is effective and the relevant endpoint envelope is strict,
the certified co-located-star and opposite-shore parts are no longer open.
The co-located Hall star is repaired by its unary centre companion, and the
endpoint-support-complete opposite-shore `K_{2,2}` has the outside-column
deletion/wedge theorem plus the two terminal bistar source units.  Those
results do not create the earlier affine coordinate-line point, and they do
not silently close an arbitrary non-strict triangle/decorated-anchor web.

The checker is
`computations/verify_h3_rootless_c5_carrier_affine_rank_landing_boundary.py`.

## Why the Fitting carrier is not yet four-good

The common output covector solves coefficient synchronization, but it does
not couple independence of the complete response tails to local port
geometry.  The sharp `k=3` rank guard has

```text
complete response-column rank       3
outer-head span                      1
active deleted-star profile          (2,2,3,3).
```

All complete columns may have independent cofactor-tail vectors while
their local outer factors remain the same line.  Adding a third independent
tail therefore does not repair either deficient star.  This disproves the
pure linear-algebra implication

```text
common Fitting carrier + minimum complete-column circuit
    => transverse rank-(3,3,3,3) active pair.
```

The guard is not a full one-bad source.  It shows exactly which additional
source incidence is required; it does not refute a theorem using the unary
top, second diagonal target, and both crossed companions.

## Honest residuals

The composition leaves two pre-landing rank classes, plus the explicitly
finite Hall scope guard.

1. **Unary-only carrier.**  A nonzero top component contains an external
   `x`-spoke, but no committed theorem pairs that spoke with a coloured
   endpoint product on an affine response hole.  This is still
   spoke-to-hole synchronization, not Hall rank.
2. **Same-head Fitting carrier.**  A response component exists and the
   proportional branch is gone, but every active product is trapped in the
   selected anchor web.  The common Fitting carrier has no source-labelled
   transverse outer head, so its natural profile can remain `(2,2,3,3)`.
3. **Non-strict Hall lock.**  A different-tail `C4` can be trapped in a
   triangle or larger decorated-anchor web without yet satisfying the
   effectiveness and endpoint-support-completeness hypotheses of the pinned
   strict units.  This is a finite Hall normal form, not a new affine fibre.

Thus the smallest missing full-source statement is:

> Unary top plus the other diagonal and both crossed companion rows turn a
> unary-only spoke or same-head Fitting carrier into an exact joint-kernel /
> coordinate-line move, a transverse active endpoint arm carrying the two
> missing rank-three minors, or an effective strict Hall lock.

This is narrower than arbitrary Hall closure.  The certified strict Hall
subcharts are downstream and closed; a non-strict triangle/anchor web stays
as a named finite lock.  The missing rank datum is source-labelled local
rank restoration.

## Exact audit and scope

The normalized `C5` inventory has ten tails and fifteen chord occurrences,
split into nine diagonal and six off-diagonal chord occurrences.  Their
complete derivatives have forty-five unary completions and ninety response
q-edge completions.  The forced-hole response rows contribute ten
same-tail opposite terms and forty different-tail `C4` terms.

This is an exact h=3 dependency composition and a sharp tensor-rank
boundary.  It constructs no Krenn counterexample and does not assert the
remaining full-source rank restoration.

Run:

```text
python3 computations/verify_h3_rootless_c5_carrier_affine_rank_landing_boundary.py
python3 -O computations/verify_h3_rootless_c5_carrier_affine_rank_landing_boundary.py
python3 -I -S computations/verify_h3_rootless_c5_carrier_affine_rank_landing_boundary.py
```

Frozen ledger SHA-256:

```text
5ddbd0e3d9fcddcc221e585f76cad96ab60a49d0d366db61a664c34bb13b827b
```
