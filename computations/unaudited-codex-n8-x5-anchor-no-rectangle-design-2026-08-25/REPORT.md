# Four anchor/no-rectangle X5 records

Status: **PASS exact reconstruction and rank design; one reduced polynomial
representative; no solver run; no complete record closed.**

## Exact census and symmetry

The four parent records are:

- record 12: orbit 6, `A12` present, added
  `{06,07,13,14,17,25,26}`;
- record 13: orbit 6, `A12` present, its mirror
  `{06,07,15,17,23,24,26}`;
- records 14 and 15: the corresponding orbit-7 supports with `A12` absent.

Every record has the same eight supported perfect matchings up to the unique
site involution `(1 2)(6 7)`.  Exhausting all `8!` site permutations gives
two literal source-support classes, `{12,13}` and `{14,15}`, with trivial site
stabilizer and one map between the two members.  All six simultaneous colour
permutations preserve the source-labelled full-X5 word map.  No literal source
map crosses the `A12` boundary.

Nevertheless, `A12` occurs in none of the eight supported perfect matchings
and in none of the selected carriers.  Removing that inactive block gives a
single reduced polynomial class: use record 12 as representative, then lift
with `A12=I3` or `A12=0`.  The exact replay checked 157,464 transported
word-generators.

There are no nonstructural cap-67 guard equations.  For each record all 560
triangle and 168 star candidates were reconstructed with literal response
formulas.  The `A12`-present ledgers have 24 two-sandwich carriers, 12 on an
identity cap; the absent ledgers have 40, 16 on an identity cap.  The complete
2,912-carrier source-labelled ledger is retained rather than inferred from
counts.

## Full-X5 representative

Writing the word as `(a,b,c,d,e,f,g,h)`, the canonical amplitude factors as

```text
(delta_ad delta_ef + A04[a,e] A35[d,f])
(delta_bg delta_ch + A17[b,h] A26[c,g])
+
(A13[b,d] delta_ef + A14[b,e] A35[d,f])
(A06[a,g] delta_ch + A07[a,h] A26[c,g]).
```

Expansion was checked against all eight supported matchings on every one of
the `3^8` words.  This produces an exact rational, solve-free input with nine
matrix blocks, 81 variables, and 6,561 full-X5 equations.  It is strictly
smaller than separately retaining the amplitude-inactive `A12` block.

## Exact carrier/rank split

For records 12/14, cap 27 and star center 1 have precisely

```text
R05 = A07 K^T A25,   R06 = A07 K^T A26,
L(K) = [A25^T | A26^T] K A07^T.
```

Thus the response row space is `P tensor Q`, where
`P=ColSpan(A25,A26)` and `Q=Row(A07)`.  The identity-cap pairing lies in this
space exactly when both `P` and `Q` are three-dimensional; a diagonal
functional `K_ii` lies in it exactly when `e_i` belongs to `P intersection Q`.
The mirror carrier for records 13/15 is cap 16/star center 2, with common
factor `A06` and partners `A15,A17`.

This gives the following fail-closed stratification:

- rank zero of the common factor is closed: `L=0`, so trace and all three
  diagonal functionals are live on the full kernel;
- rank one/two reduce to 27 exact minor/diagonal charts each, five simultaneous
  colour orbits, with inactivity equations `V z=e_i` and
  `A25 u+A26 w=e_i`; the listed ideals have respectively 85/89 variables and
  6,568 generators, but have not been solved;
- rank three is the 81-variable full ideal plus one determinant saturation,
  hence 82 variables/6,562 generators.  The selected carrier still needs a
  proper partner span avoiding every standard basis vector; otherwise another
  carrier or a full-X5 identity is required.

The complete identity-cap carrier portfolio also exposes analogous splits
through common factors `A17`, `A04`, and `A14` (and their mirrors).  This
package does not assert that one of those factors must be singular or that one
carrier must be active.

Scope is intentionally narrow: this is an exact source/ideal reduction and a
finite rank design.  Rank one, rank two, rank three, all four full records, and
the conjecture remain open here.
