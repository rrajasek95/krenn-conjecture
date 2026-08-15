# The fine-marked collision square is Cartesian, but the derived cap does not yet descend to physical `r0`

The finite `h=3` collision groupoid supplies a genuine positive statement.
After retaining the original missing-site mark—the same fine/reinsertion datum
carried by the selected `t*q_(v,N)` cell—the `DQ` replacement flags and the
`P3+K2` cap flags are in literal bijection.  Linearizing the full marked
correspondence gives a derived cap totalization `N` which is a free resolution
of the same 90-parent module as the trigger response resolution.

This proves the derived comparison, not its underived physical descent.  The
comparison is presently unaugmented with respect to the operation, `q`,
anchor, target, residue, `W`, ridge, `eta`, `sigma`, and protected `B/Eq`
readouts.  In particular, replacing physical `r0` by `N` in PAComp still
requires either an absolute decorated `Eq` contraction or an equivalent
theorem on the actual solution locus.  Normalizing `H0-u=0` and using only the
known relative `dK=(H0-u)E` does not suffice.

The executable certificate is
[`verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py`](../computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py).

## 1. The finite marked square

Let `M` be one of the 90 perfect matchings of `K8` avoiding the direct edge
`36`.  Write `0i` for its site-0 edge.  For each `j != i`, form the collision
branch

```text
(M - {0i}) union {0j}.
```

There are six branches per parent and 540 in total.  Every branch remembers
its parent, missing site `i`, and doubled site `j`; no two branch monomials
coincide.  Deleting one edge from every branch gives

```text
3K2 flags      1080
P3+K2 flags    1080.
```

If one forgets the missing-site mark, the 1080 `P3+K2` flags collapse to 380
cofactors.  Sixty cofactors have two lifts and 320 have three lifts.  Thus the
unmarked square is not Cartesian.

If a cap cofactor retains the original missing site `i`, there are exactly
1080 marked cap objects and the map from branch/deletion flags is bijective.
Indeed the three absent sites consist of `i` and the two endpoints of the
removed remote edge.  The mark recovers that remote edge, then the collision
branch, and finally the unique parent `M`.  Consequently the fine-marked
`DQ -> PS` square is strictly Cartesian as a finite species correspondence.

This is the precise positive Beck--Chevalley datum.  It is not available after
the fine/reinsertion label has been forgotten.

## 2. The two resolutions of the 90-parent module

Over one parent the response trigger fibre is the augmented simplex
`Delta^5`.  Its chain dimensions and boundary ranks are

```text
dimensions     6  15  20  15  6  1
ranks             5  10  10   5  1.
```

The full marked derived cap fibre is `Delta^5 x Delta^1`.  Its dimensions and
ranks are

```text
dimensions    12  36  55  50  27  8  1
ranks             11  25  30  20   7  1.
```

Both augmented complexes are exact and free over
`V_parent = Q{90 direct-free matchings}`.  The cap complex retracts onto the
response complex by

```text
projection   id_Delta5 tensor epsilon_Delta1,
section      id_Delta5 tensor (u+v)/2,
h(u) = -e/2,   h(v) = e/2.
```

The checker verifies the chain ranks, `d^2=0`, and this contraction exactly.
For one root, the augmentation-followed-by-boundary ranks are

```text
response    90, 450, 900, 900, 450, 90
cap N       90, 990, 2250, 2700, 1800, 630, 90.
```

Hence claim (i) is proved for the defined fine-marked derived totalization:
the response and `N` are projective resolutions of the same 90-parent module,
and their algebraic comparison cone is acyclic.

## 3. Why this is not yet a physical `Phi`

The first protected underived descent has independent response and `Eq` rows:

```text
dN    = (1,0),
dr0   = (0,1),
omega_Eq = (1,-1).
```

The two columns have rank two, so the derived SDR does not identify them in
the augmented physical category.  If an absolute decorated `Eq` cell `theta`
were present, then

```text
d theta = dr0-dN = (-1,1),
d k     = r0-N-theta
```

would have square zero.  This is the exact global cancellation formula, but
neither the operation-changing `k` nor the required absolute `theta` has been
constructed by the species bijection.

The normalized base-change calculation is the sharp counterexample to every
weaker claim.  Setting `t=H0-u=0` makes the evident top map a chain map, but
its cone retains

```text
H0 = Q{e_Eq}.
```

The relative cell `dK=tE` becomes a new `H1=Q{K}` after the base change.  Only
an absolute `dK=E` makes both `H0` and `H1` vanish.  Thus common-parent
projectivity, an unaugmented quasi-isomorphism, endpoint-even averaging,
normalization, or the relative `K_Eq` relation alone cannot replace `Phi`.

## 4. Weakest sufficient replacement for an underived cell

A literal underived `Phi` cell is not logically indispensable.  The weakest
derived substitute presently visible is the conjunction of:

1. a pointed augmented linearization of the marked collision correspondence,
   preserving the operation, word/fine/repeated/window, `q`, anchor, target,
   residue, `W`, ridge, `eta`, `sigma`, and `B/Eq` readouts;
2. a theorem that every PAComp/descent map factors through the resulting
   marked derived totalization `N`, so the conclusion does not require a
   chosen underived representative `r0`; and
3. an absolute decorated contraction `dK=E` of the surviving `Eq` class, or a
   conservative theorem on actual solutions which proves exactly that class
   vanishes and is compatible with all the same readouts.

Under these hypotheses the acyclic species comparison cone can replace the
underived physical comparison.  Without item 3, the explicit normalized cone
above is a counterexample.  Without items 1--2, the SDR lives only in the
coefficient/common-parent category and is not a morphism in the category in
which PAComp is stated.

## 5. Scope

The certificate proves a finite set/species bijection and its rational chain
linearization.  It does **not** assert that the present physical `AugP2/r0`
packet is the derived totalization `N`, nor that the source DGA already
contains the pointed augmented comparison.  The earliest missing datum is
exactly a physical linearization of the fine-marked correspondence carrying
the protected readouts.  If such a linearization is supplied, the only
remaining descent obstruction in this local calculation is the absolute
decorated `Eq` class just displayed.

All three checker modes have the frozen ledger digest
`519a980ee5f935db8d924324a9321b42848a83ffc0aa00eb1e3da476e345e1ee`.
