# Degree-12 scope referee and degree-13 initial boundary

## Degree-12 verdict

The 20-row functional is a valid exact dual of the complete homogeneous
degree-12 normalized mixed source image.  Independent replay finds 22
incident columns and zero nonzero pairings.  It also annihilates the explicit
90-column lower-kernel witness:

```text
y10 pairing  +1
y11 pairing  -1
total         0
```

Every one of the 90 literal source columns pairs zero individually.  Hence
the functional is invariant under **every** homogeneous degree-12
source-image/right-inverse change, not merely the displayed witness.

However, the claimed upgrade from fixed `C10` to the original target is
false.  Direct source-faithful expansion gives

```text
normalized Fh terms                         1,157,625
functional support rows occurring in Fh             0
lambda(Fh)                                           0
lambda(C10)                                         -4
```

Because the functional annihilates the ideal, these unequal pairings prove
that `C10` alone is **not congruent** to `Fh` modulo the normalized ideal.
The omitted y11/y12 part of the actual post-correction residual necessarily
pairs by `+4`.  The fixed-C10 and monomial dual statements remain valid; the
`Fh`-class/nonmembership wording must be retracted.

## Degree-13 initial boundary

Treat the degree-12 functional as `t*lambda12`.  All positive-`t` columns are
inherited and still pair zero.  The new primitive nonic-multiplier boundary is:

| item | count |
|---|---:|
| all incident columns | 144 |
| primitive incident columns | 122 |
| crossing primitive columns | 112 |
| top owner rows | 7,894 |
| owner columns | 7,309 |
| singleton/private pivots | 1,833 |
| crossings removed privately | 85 |
| residual columns | 5,476 |
| residual crossing columns | 27 |

Thus private top-row repair does not extend the dual to degree 13.  The
lex-first surviving crossing lies in a component of 1,567 columns, 942 rows,
and 15 crossing columns.  This is only a first coupled core: it does not prove
that a non-private linear correction is impossible.

## Replay

```bash
python3 audit_degree13_full_dual_referee.py
python3 -O audit_degree13_full_dual_referee.py
python3 -I -S audit_degree13_full_dual_referee.py
```

All modes give logical digest
`0942f658d68bf670f17af93e6201414a55d25611c84a88a623021f411be2eee8`.
Checker SHA-256 is
`363a87aa490e36aae7e8412c297d747778274ea5ee0f6ce252014f22504ea5b5`;
result SHA-256 is
`3160c65f21b2cc5d2ec4b4197706ddcb1be7c0f9152c9fdf8312d79054be6b25`.

Scope is the normalized orbit26 chart only.  No degree-13 theorem,
`t`-saturation, degree 14, or global inference is made.
