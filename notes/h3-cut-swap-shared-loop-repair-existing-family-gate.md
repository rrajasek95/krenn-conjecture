# Shared-loop C4 repairs and the existing-family gate

## Outcome

The forced loop (02\mapsto44) is not the end of the combinatorial search.
There are exactly four equivariant ways, at the target-orbit level, to
replace the three shared matchings by single-(C_4) exchanges before the
site collapse.  They reduce to:

```text
rho-paired shared orbit: target pure orbit {0,5} or {2,3};
rho-fixed shared orbit:  target pure column 1 or 4.
```

But none of these occurrence choices is supplied by the committed physical
families.  The literal (M_v) aggregates, clean collision edges, and the
projected reduced-Eq family all lie in the augmentation-zero hyperplane of
the six pure-column module.  A shared occurrence has augmentation one.  A
pure (r_0) column supplies that unit but also has

\[
            (\operatorname{target},\operatorname{ainc})=(1,-1),
\]

and all three named repair families have both protected rows zero.  Thus the
exact remaining datum is still two protected-zero, augmentation-one
relative images: one for the fixed orbit and one for the paired orbit.

## The three shared labels

Their matching indices and matchings are

```text
3: 02 13 45
4: 02 14 35
5: 02 15 34
```

All have repeated direction (02).  The involution acts by

```text
3 <-> 5,   4 fixed.
```

Every successful twelve-label support collapse identifies source sites 0
and 2 at target site 4.  Direct collapse of these three labels therefore
creates the coefficient loop (44).

## Exhaustive single-C4 bypass

Fix any of the four equivariant one-double-fibre collapses from the support
theorem.  For each shared matching, enumerate all perfect matchings with
exactly one common edge.  Such a pair differs by one alternating (C_4).
Retain only replacements whose three edges collapse to one of the six
physical pure multiplier graphs.

Exactly four replacements survive for each shared label and each collapse.
Equivariance compresses them as follows.

For the paired orbit, choosing a replacement for matching 3 forces the
replacement for matching 5.  Four literal choices remain, but their target
images form only two possibilities:

\[
                         \{0,5\},\qquad\{2,3\}.
\]

For the fixed matching 4, the literal rho-fixed replacements are matching 7
or 14, both landing on (B_4).  The other two replacements, matchings 1 and
9, are exchanged by rho and their rational average lands on (B_1).  Thus
the fixed target choice is

\[
                            B_1\quad\text{or}\quad B_4.
\]

This gives four target-orbit assignments in total.

Every selected pair is a same-word single-(C_4) with a common matching
edge, so it has the occurrence typing isolated by the frame-circuit theorem.
That theorem deliberately does not assert that the two occurrences form a
binomial source boundary.  Here the missing object would be precisely such
a collision/relative (C_4) cell, including the change of repeated-edge
direction.

## Why the known families do not realize it

Let (E=\mathbf Q^6) be the coefficient module on the six pure full-nine
columns.  The fifteen literal (M_v) choices have coefficient vectors
obtained by inserting

\[
                        (-1,1,1,-1)

\]

in four of the six positions.  Their span has rank five and is exactly

\[
                    E^0=\{x:\sum_i x_i=0\}.
\]

Clean collision boundaries are differences (e_i-e_j), hence also lie in
(E^0).  The projected reduced-Eq face has no literal pure-column
coefficient and contributes zero to (E).  Consequently the combined
known span still has rank five and is killed by the primitive augmentation
covector

\[
                           (1,1,1,1,1,1).
\]

Each candidate shared repair needs a unit (e_i), detected with value one
by this covector.  It is outside the combined span.

Adding the old pure column (r_{0,i}) would restore the unit occurrence,
but its coarse protected signature is

```text
(occurrence, target, ainc) = (1,1,-1).
```

Every exact (M_v), clean collision, or zero-anchor reduced-Eq correction
has protected `(target,ainc)=(0,0)`.  Therefore no linear combination of
those families cancels the two unwanted protected entries.

## Frontier

The support part of Gate I is already constructed and remains unaffected,
because the three shared labels have coefficient zero in the signed lower
packet.  Extending the comparison to the full physical (U_{15}) module
requires two new source images:

1. a protected-zero, occurrence-augmentation-one image for matching 4;
2. a protected-zero, occurrence-augmentation-one image for matching 3,
   with the image of matching 5 forced by rho.

Equivalently, choose one of the four target-orbit assignments above and
construct its shifted repeated-edge (C_4) relative boundary.  Existing
reduced-Eq/collision/(M_v) cells do not do this; an arbitrary higher
relative collision cell is not excluded.

## Verification

Run:

```text
python3 computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py
python3 -O computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py
python3 -I -S computations/verify_h3_cut_swap_shared_loop_repair_existing_family_gate.py
```

Frozen ledger digest:

```text
f6cc210b684071e9ad55416865fde99902b2709e742c6a12aee3437ac54151b1
```
