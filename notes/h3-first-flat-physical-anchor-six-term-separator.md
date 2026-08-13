# The six-term class has a physical anchor interpretation

## Exact substitution

The canonical first-flat calculation produced the integral relation

\[
 Q+\sum_{i=1}^{6}m_i=0,                              \tag{1}
\]

where the `m_i` are six literal private matching coordinates in the
faces-`(3,5)` repeated grade and `Q` records the coefficient sum on pure
repeated rows.

This marker is not an extra physical hypothesis.  On every repeated pure
full-nine column,

\[
                     Q=-\operatorname{ainc}.          \tag{2}
\]

Both sides vanish on nonpure repeated columns.  On the complete order-six
operator block, the exact dependency gives `sum m_i=0`, while the
endpoint-odd Cartan theorem gives `ainc=0`.  Substituting (2) into (1)
therefore produces the fully physical covector

\[
 \boxed{\Lambda=\sum_{i=1}^{6}m_i-operatorname{ainc}.} \tag{3}
\]

No chart, formal Hasse, or coarse face marker remains in (3).

## What it kills

The checker proves that `Lambda` vanishes on:

1. all 288 complete repeated columns in the canonical component;
2. all 8580 columns of the exact first-flat order-six/Spencer block;
3. every absolute higher source/bar landing, by the injectivity theorem;
4. the doubled-chart and natural Tate kernels;
5. every listed eta, left non-Euler, and extra diagonal target stabilizer;
   and
6. the presently specified endpoint-odd relative `alpha=(-1,1,1,-1)` cell,
   because its four pure-column coefficients sum to zero.

On the desired physical relative anchor,

```text
literal matching boundary = 0,
ainc = -1,
W = target = ores = 0,
```

equation (3) reads exactly `1`.

## Consequence

The canonical bounded comparison now has a physically typed alternative.
If a new protected-zero relative generator has nonzero `Lambda` value, it
normalizes to the required relative anchor.  If every admitted relative
generator has `Lambda=0`, then `Lambda` descends as the physical separator.

Thus the remaining comparison task is no longer to interpret the pure
aggregate.  It is only to audit the genuinely relative generator family and
propagate the construction or separator cyclically.  The absolute source
resolution and physical anchor typing are finished in this face.

## Scope

This theorem is exact in the canonical faces-`(3,5)` first-flat block and
for every already constructed absolute or relative family listed above.  It
does not assert that an arbitrary future relative generator is killed, nor
does it prove cyclic propagation or transverse rank landing.  A nonzero
pairing on such a future protected-zero generator would be the positive
generator branch, not a failure of the alternative.

Verification:

```text
python3 computations/verify_h3_first_flat_physical_anchor_six_term_separator.py
python3 -O computations/verify_h3_first_flat_physical_anchor_six_term_separator.py
python3 -I -S computations/verify_h3_first_flat_physical_anchor_six_term_separator.py
```

Frozen ledger SHA-256:

```text
bd41b41fdef28c5a2cfcf2d1c187e7145eb5c1c54a3015be7cbd0d61b3760bbd
```
