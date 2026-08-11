# Both minimal crossed-chart escapes have ordinary source units

Date: 2026-08-11

Checker:
`computations/verify_h3_one_bad_crossed_minimal_escape_units.py`

## Outcome

Neither minimal escape named by `5ab40da` is a new coefficient packet.
Adjoining only `x03_11` leaves a two-row source unit.  Separating only
`x06_11` from `x06_22` produces a four-row source unit.  Both statements are
ordinary polynomial identities over `Q`; no localization, division, clean-cap
construction, OO transport, Gröbner basis, or higher-order deformation is
used.

The checker reconstructs every one of the `3^8=6561` literal full-output
rows in each 44-parameter extension.  The `x03_11` extension has 292 nonzero
rows with 8,313 collected terms.  The transverse `x06_11` extension has 256
nonzero rows with 7,910 collected terms.

## A. The new support cell `x03_11`

The mixed word `12222212` and the pure target word `22222222` both retain the
sole physical matching

```text
06 | 15 | 23 | 47.
```

Their physical tails are identical.  Since only the pure row carries target
augmentation, the source generators satisfy

```text
G_12222212 - G_22222222 = 1.
```

This identity is independent of the new parameter on `x03_11`; that cell does
not occur in the displayed matching.  Thus the candidate support escape is
empty before its new coefficient can matter.

The literal reselection census grows from 11 to 12 persistent coordinate-unit
blocks and from 20 to 24 shared distinct-outer-line candidates.  Exact minors,
cofactor rows, and transition minors show that all 24 are generically
four-good, active, and curved.  Those OO data are not needed because the
two-row unit is stronger and immediate.

## B. The transverse split `x06_11-x06_22`

Let `z43` be added to `x06_11` only, and define

```text
M = (z36-z37)(1+z39)(z38-z39-z40+z42),
L = z36+z37+z38+z40-z42-1.
```

Four literal full-output rows obey the exact identity

```text
(M L) G_11111111
  +     G_21012122
  - M(L-z43) G_21111121
  -     G_22222222
  = 1.
```

The two nonconstant multipliers have respectively 50 and 66 collected
monomials after expansion.  The checker expands the four products and obtains
the scalar polynomial `1` exactly.  This is a source-labelled Nullstellensatz
certificate, not a solver verdict.

The split changes no persistent literal coordinate-unit block.  All 20
shared-arm candidates from `5ab40da` remain generically four-good, active, and
curved.  Again, the direct source unit closes the extension before the OO
route is needed.

## Consequence and scope

The crossed one-bad affine lane is closed under each minimal one-parameter
departure separately:

- one new support cell `x03_11`; or
- one support-preserving transverse split of `x06_11` from `x06_22`.

No genuinely new finite packet survives.  A continuation would have to alter
at least two independent directions simultaneously or leave this physical
normal form in some different named way.  That larger modification is outside
the present theorem and should not be inferred from these units.
