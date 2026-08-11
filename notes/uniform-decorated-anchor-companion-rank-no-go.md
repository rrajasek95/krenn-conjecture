# Same-cell companion rows cannot finish the decorated-anchor repair

## Result

The exact exchange theorem `8ef0754` leaves one rank question: can the
other full-output rows containing the same decorated anchor cell provide
the missing endpoint repair?

They cannot.  Let

\[
                       q_{uv}^{ij}\ne0,qquad i\ne j.  \tag{1}
\]

For every choice of common colour `k` on the remaining sites, every
matching in that complete companion row still has endpoint colours `i` at
`u` and `j` at `v`.  Avoiding `uv` changes the physical partners, but not
the endpoint rows.  Therefore:

* if `uv` is a selected pure-`i` anchor, same-cell companions may repair
  the `i` column at `u`, but never at `v`;
* if it is a selected pure-`j` anchor, the dual statement holds; and
* if it is a selected anchor in the third colour, none of the companions
  repairs that pure row at either endpoint.

This is an all-order label obstruction, independent of coefficients and
the number of companion rows.  The next source input must be a pure-anchor
reselection, an off-anchor escape, or a genuinely new direct cell with the
missing target label at the deficient endpoint.

Checker:
`computations/verify_uniform_decorated_anchor_companion_rank_no_go.py`.

## A six-site complete-row guard

The obstruction is sharp already on six sites.  Choose

```text
Q0 = 01 | 23 | 45,
Q1 = 02 | 13 | 45,
Q2 = 03 | 12 | 45,
```

and decorate the `Q0` edge `01` by `q01_10=1`.  For each rest colour
`k=0,1,2`, retain one avoiding matching with coefficient `-1` against the
through-`01` term.  Literal matching expansion gives the three complete
rows

```text
word 100000:  +1 -1 = 0,
word 101111:  +1 -1 = 0,
word 102222:  +1 -1 = 0.
```

All cells in the through terms and avoiding mates lie on the physical
anchor union

```text
{01,23,45,02,13,03,12}.
```

The three pure target coefficients remain one.  Nevertheless, after
deleting `01`, the literal endpoint rows are

```text
endpoint 0: {1,2},
endpoint 1: {0,1,2},
```

so the deleted-star ranks are exactly `(2,3)`.  All three same-cell
companion rows have repaired only the endpoint whose fixed decoration
label agrees with their available row.  Adding still more tails to these
same words cannot create row zero at endpoint `0`.

The checker enumerates all `216` choices of off-diagonal endpoint labels,
rest colour, and avoiding six-site matching and verifies the endpoint-label
invariant directly.

## Interface with the triangle residual

For the Hall-triangle `10/20` correction forced by the three-term lock,
`8ef0754` remains decisive:

```text
dark pure cofactor  -> pure selected-anchor matching avoids the edge;
non-dark cofactor   -> a complete mixed row forces an avoiding matching;
off-anchor escape   -> rank-three active route.
```

The present theorem identifies the exact boundary when every avoiding
matching remains in the anchor union.  Reusing the same decorated cell in
the remaining colour grades cannot by itself upgrade a one-sided or
third-colour repair.  A proof must show that one of those grades forces a
**different endpoint label**, or else produce a pure-anchor switch/source
unit.  This removes an unproductive infinite companion-tail iteration.

## Scope

The displayed packet contains the complete matching expansion of the
three companion rows and the three pure target coefficients.  It is not a
full GHZ source: other mixed output rows are not required to vanish.  Thus
it is a sharp source-row guard, not a Krenn counterexample.

Run

```text
python3 computations/verify_uniform_decorated_anchor_companion_rank_no_go.py
python3 -O computations/verify_uniform_decorated_anchor_companion_rank_no_go.py
python3 -I -S computations/verify_uniform_decorated_anchor_companion_rank_no_go.py
```

Frozen ledger SHA-256:

```text
ae38d44b325daa78b1aedb3774c7ace31392c20fb6461d2f4c4a305b7f3af685
```
