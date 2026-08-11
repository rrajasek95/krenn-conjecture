# The combined crossed-chart two-escape critical face is unit

Date: 2026-08-11

Checker:
`computations/verify_h3_one_bad_crossed_combined_escape_unit.py`

## Result

Adjoin both minimal departures from `e97a968` simultaneously and no others:

```text
x03_11 += z43,
x06_11 += z44, while x06_22 is unchanged.
```

The resulting 45-variable coefficient packet is empty over `Q`.  The checker
reconstructs all `3^8=6561` literal full-output rows; 292 generators remain
nonzero and have 8,713 collected terms.  Exact Singular standard-basis
computations in both `dp` and `Dp` orders return the one-element basis `[1]`.
Thus the combined critical face is not coefficient-feasible.

This is a genuine critical-pair calculation.  The two-row identity that kills
the isolated `x03_11` extension acquires a nonzero `z44` tail, while the
four-row identity that kills the isolated transverse split acquires a nonzero
`z43` tail.  Neither short identity survives verbatim; their interaction and
the remaining literal source rows restore the unit ideal.

## Reselection audit

The combined chart has 12 persistent literal coordinate-unit blocks and 24
shared distinct-outer-line candidates.  Exact polynomial minors, cofactor
coefficients, and transition minors show that all 24 are generically
four-good, active, and curved.  As in the one-escape faces, rank/activity/
curvature is not the obstruction.  Coefficient exactness kills the packet.

## Certificate boundary

The result is an exact characteristic-zero standard-basis theorem, not a
floating-point or modular solver report.  The checker independently obtains
`[1]` under two monomial orders from a frozen source input digest.

An ordinary multiplier lift through all 292 source rows was also attempted
and capped after 120 seconds.  No compact source-row Nullstellensatz identity
is therefore claimed in this note.  This distinction is deliberate: the
ideal-theoretic emptiness is decided, but a short human certificate remains an
optional compression task rather than a proof gap in the bounded packet.

## Scope

Only the simultaneous `x03_11` insertion and `x06_11-x06_22` split are
allowed.  No third support cell, transverse direction, or higher-order jet is
included.  The theorem closes exactly the final two-escape critical face
requested after `e97a968`; it makes no statement about larger departures.
