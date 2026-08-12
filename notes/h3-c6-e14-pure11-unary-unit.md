# Complete unary rows close the E14 pure-11 frontier

## Result

Every one of the 36 pure-`11` first extensions left by the response-only
audit has an ordinary two-row unit in the genuine unary equation

```text
q^[3] = X0.
```

Consequently all 1,020 possible first extra internal cells after the minimal
E14 enlargement are ordinary source units.  The 18 Hall reselections and six
fixed-hole diagonal-`C4` switches recorded in `b62a039` are valid
response-only landings, but they are superseded before reselection or rank
landing once the complete unary rows are imposed.

Checker: `computations/verify_h3_c6_e14_pure11_unary_unit.py`.

## Common unary identity

Write `U_w` for the complete coefficient of word `w` in `q^[3]`.  The pure
target and mixed source generators are

```text
F_000000 = U_000000 - 1,
F_w      = U_w                       (w mixed).
```

For each of the 36 affected pure-`11` records the checker finds a literal
mixed word satisfying one of the coefficientwise identities

```text
U_w =  U_000000,   hence  F_w-F_000000=1;
U_w = -U_000000,   hence -F_w-F_000000=1.
```

The normalized rational unary fibre has `U_000000=1`.  Equality is checked
as a polynomial in every formal E14 coefficient and in the new pure-`11`
coefficient; it is not a support-only or selected-monomial statement.

The canonical lexicographic witnesses have the exact census

```text
020002  12
221100   6
022011   6
221010   3
000101   3   (negative sign)
220110   3
022110   3.
```

There are 33 positive and three negative canonical witnesses.  Several
records have additional valid unary witness words; the full lists are
retained in the frozen record ledger.

## Closure of the whole one-cell layer

The complete 1,020-record count is now

```text
969  original target/zero response unit unchanged
 15  mixed-10 companion response unit
 36  pure-11 unary unit
----
1020  ordinary source units.
```

Thus there is no first-extra-cell source-connectivity or active-rank packet.
In particular, the six fixed-hole records requested after `b62a039` are
already killed by the unary rows, uniformly in all three selected X2 tails.

## Exact next boundary

This theorem closes exactly one new internal cell added to the canonical
minimal E14 family.  A survivor in the same local chart must do at least one
of the following:

1. add two or more new internal cells simultaneously, so cross-terms
   contaminate both sides of every displayed response and unary collision;
2. use an endpoint component outside the four core ports; or
3. leave the canonical E14/fixed-fibre normalization through an unrelated
   global source component.

The first item is the next local coefficient problem.  It should be attacked
as a simultaneous-contamination/source-exhaustivity lemma, not inferred by
iterating the one-cell theorem.  Outside endpoint components and the global
multisite/active-rank termination theorem remain separate established
routing interfaces; they are not closed here.

## Verification

```text
python3 computations/verify_h3_c6_e14_pure11_unary_unit.py
python3 -O computations/verify_h3_c6_e14_pure11_unary_unit.py
python3 -I -S computations/verify_h3_c6_e14_pure11_unary_unit.py
```

Frozen ledger SHA-256:

```text
99245d528fcadcc9a182a1615b7b68088f2537d782630488b49a6b841384d22e
```
