# Seven-block response minors reduce to thirteen two-sandwich stars

Status: **all 64 unresolved coefficient strata from the seven-block support
boundary admit a star whose entire forbidden-response map consists of two
supported products sharing one source block.**  There are only thirteen
labeled factorization patterns.

For a common left block the map has the form

```text
K -> U K B1, U K B2,
```

and its row space is `P tensor Q`, with `P=Row(U)` and
`Q=ColSpan(B1,B2)`.  The common-right case is the transpose analogue,
`P=RowSpan(U1,U2)` and `Q=Col(B)`.  Thus a diagonal activity `K_ii` is
identically zero on the clean kernel exactly when `e_i` belongs to both `P`
and `Q`.  The cap-pairing activity fails exactly when its coefficient matrix
lies in `P tensor Q` (column space in `P`, row space in `Q`).  If none of the
four activity functionals fails, finite-hyperplane avoidance over `Q` gives a
single clean active covector.

The exact pattern census is:

```text
 1  cap01 center3 common04       1  cap02 center3 common04
 3  cap03 center1 common04      19  cap03 center1 common35
16  cap03 center2 common35       8  cap03 center4 common06
 8  cap03 center4 common07       2  cap04 center1 common03
 2  cap04 center1 common45       1  cap15 center3 common45
 1  cap16 center0 common26       1  cap25 center3 common45
 1  cap26 center0 common16
```

This is a strict reduction, not a seven-block closure theorem.  The remaining
finite obligation is to show, for these thirteen incidence patterns, that the
formal guard and full-X5 equations exclude any failed activity incidence, or
route it to another active carrier.  No counterexample claim is made.

Parent seven-block manifest:
`13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85`.
