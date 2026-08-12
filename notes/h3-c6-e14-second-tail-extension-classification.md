# First second-tail extensions reduce to seven anchor-contained `10` guards

## Exact classification

Start from the complete minimal `E14` enlargement excluded by `8fe3f8b`.
For each of its nine bright charts, adjoin one previously absent internal
decorated `q` cell with formal coefficient `x`.  There are exactly `1,020`
such chart/cell records.  Expand the same complete `G11` target/zero pair
used by the two-row unit.

The exact split is

```text
unit unchanged:                              969
effective alternate pure-X1 matching:        36
nonanchor offdiagonal free-carrier route:      8
anchor-contained mixed-10 guard:               7
                                              ----
                                              1020.    (1)
```

Checker:
`computations/verify_h3_c6_e14_second_tail_extension_classification.py`.

## The two source-defect types

Before the new cell, the source identity is

```text
F_zero-F_target=1.
```

After adjoining `x`, it becomes

\[
                  F_{zero}-F_{target}=1+xD.           \tag{2}
\]

For `969` records `D=0`, so the ordinary unit survives.  Every nonzero
`D` has exactly two terms: the two orientations of one complete unordered
endpoint hole, with one common literal `q` tail.  There are only two
normalized source signatures:

```text
36:  C*(p1_u:1*s1_v:1 + p1_v:1*s1_u:1),
15:  C*(p1_u:1*s1_v:0 + p1_v:0*s1_u:1).              (3)
```

At a source zero, (2) gives `xD=-1`; in particular, the complete bracket
in (3) is nonzero.  The first line is therefore an effective alternate
pure-`X1` matching, not just another occupied diagonal cell.  The second
line is a typed mixed-`10` response attachment.

This is the honest useful quotient.  The exact rational `q00` coefficients
have trivial physical stabilizer—the checker audits all `6!` site
permutations—so there is no nontrivial coefficient-preserving site symmetry
by which the literal records can be silently identified.

## Free and trapped mixed attachments

Eight mixed cells lie outside the selected pure-anchor union.  They are
exactly the applicable inputs to the pinned nonanchor-offdiagonal theorem,
which supplies the free active-carrier route.  The seven remaining records
are:

| `X1` tail | `X2` tail | new cell | endpoint hole | common tail |
|---:|---:|---|---|---|
| 1 | 2 | `q15:10` | `04` | `q23:11` |
| 1 | 3 | `q05:10` | `14` | `q23:11` |
| 2 | 1 | `q25:10` | `03` | `q14:11` |
| 2 | 2 | `q15:10` | `03` | `q24:11` |
| 2 | 2 | `q25:10` | `03` | `q14:11` |
| 2 | 3 | `q05:10` | `13` | `q24:11` |
| 2 | 3 | `q25:10` | `03` | `q14:11` |

Thus the genuine first two-tail guard has one universal mixed-hole form.
Four records use a selected pure-`11` common tail, and three use the
original response-silent `q14:11` spoke.  Every new physical edge already
belongs to the selected anchor union, so the nonanchor theorem cannot be
invoked.  They enter the decorated-anchor/Hall source interface, but this
checker does not claim that interface is closed.

## Consequence and scope

The first second-tail layer is now finite and coefficient-complete:

1. proportional or irrelevant additions preserve the two-row unit;
2. pure-`11` additions force an effective alternative bright matching;
3. nonanchor `10` additions are free active carriers; and
4. only the seven displayed anchor-contained `10` attachments remain.

This is a source-attachment theorem, not a rank theorem.  In particular,
an effective diagonal matching or an anchor-contained mixed bracket is not
automatically a four-good/clean landing.  The next proof step should apply
complete decorated-anchor exchange to the seven-row table, retaining the
common-tail coefficient and target normalization; no larger one-cell census
is needed.

## Verification

```text
python3 computations/verify_h3_c6_e14_second_tail_extension_classification.py
python3 -O computations/verify_h3_c6_e14_second_tail_extension_classification.py
python3 -I -S computations/verify_h3_c6_e14_second_tail_extension_classification.py
```

Frozen ledger SHA-256:

```text
9d2224d743873367284bc527a6bbbcd8fb9cd09425082f54c39a60a57e736932
```
