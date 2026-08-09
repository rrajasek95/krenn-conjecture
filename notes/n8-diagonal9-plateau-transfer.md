# Exact N=8 diagonal-9 plateau transfer

After the diagonal-10 contraction there are 133 critical source classes.
Exactly 91 have a nonzero diagonal-9 leading part, of rank 81 and supported
on 1,230 state orbits.  Closing those states under every maximal
even-complement fibre gives the exact plateau

```text
target states:  1,629
source columns: 1,055
rank:             880
source kernel:    175
target cokernel:  749
```

All 133 incoming classes—including all seven distinguished descendants of
the root-plateau kernel—have zero projection to the 749-dimensional target
cokernel.  Exact rational correction uses 1,996 plateau-column terms across
the 91 active inputs.  Consequently the new critical dimensions are

```text
source: 175 + 133 = 308
target:             749.
```

This again preserves, rather than kills, every previously retained target
cokernel: seven at diagonal 12 and 159 at diagonal 10.  It transports all
133 source classes one level lower and adds 175 intrinsic diagonal-9
plateau-kernel classes.

The 308 corrected source tails contain 310,440 terms.  Their leading levels
are

```text
diagonal 8: 274 classes; raw level rank 260
diagonal 7:  34 classes.
```

The seven distinguished root descendants all now lead at diagonal 8, with
exact tail term counts `338, 1460, 275, 908, 1485, 719, 1323`.  Their separate
digest is frozen so later contractions can retain that readout even while
the full 308-class source space is processed.

The next exact object is the closed diagonal-8 maximal plateau seeded by all
274 leading classes, not only by the seven distinguished ones.  The
310,440-term input marks a material expansion frontier, but the diagonal-9
closure itself remains finite and exactly certified.

The checker is `computations/analyze_n8_diagonal9_plateau_transfer.py`.  Its
frozen ledger SHA-256 is
`599746a90b1eb36da7946f8669573b44cb3a4f6762ee2388905a51bde8b2bf0f`.
