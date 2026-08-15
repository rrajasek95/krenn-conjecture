# Divided roots construct the marked-derived P2 word/fine faces

## Result

The ordinary six-root map on perfect matchings does not literally extend to
collision branches.  A branch has one missing site and one doubled site.  A
fixed order-one root at every changed site therefore either differentiates a
missing variable or recolours only one of two occurrences.  Among the 540
marked branches, the fixed order-one product is correct on only 27, is zero
on 378, and is nonzero but wrong on 135.

The source-valid replacement is canonical: at each changed site use divided
root order equal to that site's occurrence multiplicity.  Thus the order is
zero at a missing site, one at an ordinary site, and two at a doubled site.
The divided-power normalization makes the coefficient on the fully
recoloured monomial exactly one.

The checker verifies this operator on:

- all 540 parent-to-collision trigger squares;
- all 8,640 retained subfaces in the 540 Boolean deletion cubes;
- all 17,280 edge-deletion squares; and
- all 17,280 first-principal-parts terms.

Every square commutes literally, with all missing-site, parent, matching,
fine, and repeated-site marks retained.  This is stronger than an equality
after forgetting to the common 90-parent module.

## The two selected lower faces

For

```text
parent  M = 01|23|45|67,
branch  K = 07|23|45|67,
```

site 1 is missing and site 7 is doubled.  The changed-site divided-root
orders are therefore

```text
site 0:1, site 2:1, site 4:1, site 5:1, site 6:1, site 7:2.
```

Deleting `23` gives the literal map

```text
07:10 45:00 67:00  ->  07:02 45:12 67:22,
```

the marked-derived `0112/q23:21` face.  Deleting `45` gives

```text
07:10 23:11 67:00  ->  07:02 23:21 67:22,
```

the marked-derived `0121/q45:12` face.  These lie in independent
word/fine/repeated summands, so the previously zero decorated word image now
has rank two.  The strict marked Beck--Chevalley theorem applies: the
cofactor together with the original missing-site mark uniquely recovers the
deleted edge and its collision parent.

Because the same operator acts on the distinguished differential factor,
it commutes with the universal first-principal-parts differential.  Hence it
also transports the `q/dq` face.  On the selected centered preimage the
existing occurrence detector reads `35/72`, while its aggregate ordinary
residue is zero.

## Exact scope

This is a positive theorem for the marked-derived cap totalization.  It
constructs the decorated P2 word/fine/repeated faces; it does not by itself
construct the separate physical augmentation

```text
0112/q23:21 -> B1,
0121/q45:12 -> B4.
```

That occurrence-to-label map is an additional augmented readout.  The first
remaining protected discrepancy is still

```text
marked totalization: (delta_plus, delta_plus),
physical output:      (delta_plus, 0),
```

detected by the integral `B-Eq` covector with value 3.  Equivalently, the
missing proper faces are `lower/private=-E` and labelled
`word-ores=+E`.  The theorem also does not identify the derived totalization
with underived `r0` or promote the reduced-Eq detector to an intrinsic
Fredholm class.

The constructive frontier is therefore narrower than before: the
coefficient, word, fine, repeated, restriction, and first-PP maps now exist;
the remaining local construction is the physical `B1/B4`, `B/Eq`, and
labelled-residue augmentation of this same divided-root orbit.

## Verification

Run

```text
python3 computations/verify_h3_divided_root_marked_deletion_p2_naturality.py
python3 -O computations/verify_h3_divided_root_marked_deletion_p2_naturality.py
python3 -I -S computations/verify_h3_divided_root_marked_deletion_p2_naturality.py
```

Frozen ledger SHA-256:

```text
6c61945946ddf7e8935c4ee62cd90a32c212adcc4835e203b2a62a301b66d559
```
