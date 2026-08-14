# The balanced square is exactly the private-minus-Eq cokernel

## Result

In the four balanced chart corners, retain only the private/lower block
`B` and the reduced-Eq block `Eq`.  Put

```text
delta = (1,1,-1,-1).
```

The four physical cap columns have projection `(e_j,e_j)`.  The four
signless `K2,2` companion columns have one `B` vertex on each shore and no
`Eq` component.  These eight columns have rank seven in the eight-dimensional
`B + Eq` space.  Their unique primitive left-kernel is

```text
Psi = delta dot (B-Eq).
```

The balanced face has projection `(delta,0)`, so `Psi` reads it as `4` and
adjoining it raises the projected rank from seven to eight.  Therefore the
first augmented filling condition is not an ordinary-residue or ridge
condition.  It is exactly

```text
delta dot (B-Eq) != 0.
```

Exact checker:
[`verify_h3_balanced_square_private_eq_projection_gate.py`](../computations/verify_h3_balanced_square_private_eq_projection_gate.py).

## Why the named augmented rows cannot change it

The detector has zero coefficients on target, `W`, ordinary residue,
`M`, anchor incidence, physical `q`, pointed anchor, ridge, eta and sigma.
Consequently it annihilates:

- every `T`, `rho`, pure-target and ridge/terminal column;
- the literal `q=M-ainc` and full scalar-source/pointed-anchor families;
- every Cartan placement, since placement changes ordinary residue and
  terminal rows but not `B-Eq`;
- every physical `M_v` or cap lift whose private and reduced-Eq packets are
  tied; and
- every signless shore-crossing `K2,2` companion, because its `delta`
  augmentation is zero.

This is stronger and cleaner than extending the older local `B` detector
with target, `W`, residue and ridge corrections: after the reduced-Eq block
is included, all those corrections can be eliminated and the surviving
functional is supported on two blocks only.

## Exact positive and negative controls

An Eq-only `delta` packet has detector value `-4` and fills the unique
projected quotient.  A tied packet `(B,Eq)=(delta,delta)` has value zero and
does not change rank.  Thus merely decorating the old cap row more fully is
not enough: the new physical column must make the balanced private and Eq
readouts genuinely unequal.

The criterion is projection-wise exact.  It is not a claim that any column
with a nonzero projection is already a valid physical filler: its target,
word, fine/repeated, `q`, anchor, residue and ridge faces must still be
repaired in the same source-labelled cell.

## Consequence for the remaining proof

The balanced chart-square theorem now has a particularly short local fork.

```text
some exhaustive same-grade column has
    delta dot (B-Eq) != 0
        -> unique balanced projection is filled;
           repair that column's remaining augmented faces

every exhaustive same-grade column has
    delta dot (B-Eq) = 0
        -> Psi/4 is the normalized terminal candidate.
```

This focuses the positive attack on the mixed reduced-Eq incidence of the
same `DQ <-> PS` restriction/insertion cell.  It also focuses the negative
attack: terminal promotion no longer requires solving for arbitrary
target/residue/ridge coefficients, only proving that the full literal map
preserves the balanced `B=Eq` law.

The open inputs are unchanged in substance.  One still needs the exhaustive
same-word/fine/repeated physical map and either its unbalanced reduced-Eq
column or a proof that no such column exists.  This note identifies the
single scalar test that decides between them.

## Scope

This is exact for canonical `h=3` and characteristic zero.  It proves the
eight-coordinate projection theorem and checks every currently named
augmented family.  It does not assert that those families exhaust the full
source, construct the missing cross-grade cell, or by itself promote the
dual to an accepted terminal.

Run normally, optimized, and isolated/no-site.  The checker prints a frozen
ledger digest.
