# One derived filler is the common candidate for the first rootless and face-open inactive cells

## Theorem interface

Fix one deleted face `v`.  Let

```text
d b_v = k_v
```

be the canonical free-resolution cell on the primitive two-chart syzygy.
The shifted Hasse/Koszul construction of `91041f7` supplies a chain `n_v`
with

```text
(d,tgt,ores)(n_v) = (h_v Yw,0,0)
```

and the required chart-terminal correction `-1`.  These data have two
different, but compatible, candidate uses.

1. **Rootless use.**  The pair `(b_v,-n_v)` extends the marked-face map over
   the chart syzygy.  It becomes the primitive relative anchor correction
   required by the pentagon generator-or-annihilator alternative only if
   the physical comparison identifies its `-S_v` terminal correction with
   the pentagon anchor incidence.
2. **Inactive use on `D(h_v)`.**  After localizing `h_v`, the same chain

   ```text
   (kappa/h_v) n_v
   ```

   has *derived* augmented boundary `(kappa Yw,0,0)`, the correct candidate
   for the first missing invisible cap lift in Component IV.  It becomes
   the physical cap column only if the comparison identifies this derived
   `Yw` with the physical `W` coordinate.

Thus the first hard cells in Components III and IV have a common candidate
on the face-open locus.  They would reduce to one datum:

> a derived-to-physical augmented comparison preserving source boundary,
> target, ordinary residue, chart grade, and terminal readout, which also
> proves `-S_v` maps to primitive pentagon anchor incidence and derived
> `Yw` maps to the physical cap coordinate `W`.

The naive diagonal projection to the underived polynomial source is one
sufficient comparison, but it is not necessary.  Its monic commutator from
`ecb299c` excludes that projection and corrections by the old Koszul cell;
it does not invalidate the canonical free-resolution extension.

## Why a physical comparison is still necessary

Adjoining `b_v` formally is legitimate because `k_v` is a genuine
presentation syzygy.  It does not by itself define the physical polar map
`P`, however.  Different derived fillers differ by target correction
homology, and the marked terminal value must be invariant under that
indeterminacy.  Equivalently, the comparison must carry the derived chain
to the physical augmented quotient and make the terminal readout a cocycle.

This is also visible in the Component-IV physical module.  Its primitive
separator

```text
lambda(E,W,T,O) = E+W+T-O
```

kills every old physical lower-face column but reads `1` on the desired cap
direction `(0,1,0,0)`.  Hence no base change among the old columns can
replace the comparison; the latter must really supply the new physical
direction.

## What remains separate

The consolidation is conditional and local.  In particular, the algebraic
scaling above does **not** itself construct either physical generator.

- It does not prove that a physical rootless source lies in some `D(h_v)`.
  The simultaneous face-zero locus `V(h_1,...,h_5)` remains a separate
  cyclotomic/word-changing branch.
- It constructs the first `kappa Yw` boundary only after the comparison.
  The later common horizontal rootless/inactive landing and its final cap
  interpretation remain to be identified.
- It does not claim the conjecture, a physical comparison, or a chart cover.

Checker:
`computations/verify_h3_augmented_derived_comparison_shared_rootless_inactive_interface.py`.

## Verification

```text
python3 computations/verify_h3_augmented_derived_comparison_shared_rootless_inactive_interface.py
python3 -O computations/verify_h3_augmented_derived_comparison_shared_rootless_inactive_interface.py
python3 -I -S computations/verify_h3_augmented_derived_comparison_shared_rootless_inactive_interface.py
```

The checker pins the exact first comparison, shifted filler, rootless
pentagon, and Component-IV physical separator.  It verifies the two scaled
uses and the primitive physical rank obstruction.  This is a theorem
interface, not an existence result.

Frozen ledger SHA-256:

```text
9b768fe6858072b95a7710d8e8feeb82411500801cfeb7245ae92b570359d98e
```
