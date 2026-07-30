# Audit record: SUPERSESSION-2026-07-30-06

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `8d7b561fffc4c9b2725a45996c84ff613460cb86`.

Independent auditor: `/root/sol_ultra_audit_diagonal_rees`.

Outcome: **PATCHED, then PASS.**

The audit independently verified and corrected the following points.

1. The matrices `K0,K1,K2`, their direct scalars, and the identities
   `J1=K1`, `J2=-beta K0+(h-1)K2` have the displayed normalizations.
   Their cap residues are the two generic jets, and all their diagonal
   coefficients are nonzero when `beta!=0`.
2. The scalar-zero cap relation is a lower-symbol relation, not a map from
   the radial generator.  The `tau=0` and localized `tau!=0` distinctions
   agree with the off-diagonal audit.
3. The Taylor--Rees lemma is an exact coefficient proof.  Its saturation
   equality is relative to the specified filtered family; no false global
   equality is asserted when `ker(epsilon)` is larger than the literal
   boundary submodule.
4. A companion with target `-h T(Jr)` has unnormalized ordinary residue
   `-h Zr`, not `-Zr`; after the common legal normalization by `h` it
   cancels the normalized cap residue exactly.  The first draft omitted
   this factor and was patched.
5. At collision the complementary target begins in transverse order
   `h-1`, the selected-colour target begins in order `h`, and the two
   ordinary jet rows collapse and miss the selected colour.
6. The first draft called `qtilde^[h]=X_b+X_c` a binary source without
   excluding colour-`a` cells.  The patch applies the functorial projection
   to the `b,c` local axes first.  The resulting aggregate has palette
   exactly `{b,c}` and proves only that complementary-class vanishing gives
   an allowed binary source, not a ternary minimality contradiction.
7. The result is a source-representative theorem and a necessary-and-
   sufficient lifting criterion.  It does not establish the actual
   principal-part memberships or the target-cancelled chain comparison.

The checker passed normally, under `python3 -O`, and under compilation; all
seven adversarial mutations were rejected.

SHA-256 at the replacement commit:

```text
d070508992e34bacf1dc38c3ac12d4c16f0fc9c85c6d726b3ae15449b948eefb  notes/diagonal-rees-saturation-cap-jet-bockstein.md
12c4cc4a947d99eee22cbd87e900ac6c7a56df2c533c4c44c52f0ab0fcedee2a  computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py
```
