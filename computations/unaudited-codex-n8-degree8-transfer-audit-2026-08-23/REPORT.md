# The exact lambda7-to-lambda8 lift has no natural finite recurrence

Status: **UNAUDITED exact transfer obstruction**.

## Exact positive statement

Let

\[
D_N=(S_N/I^h_N)^*,\qquad
\rho_t:D_{N+1}\longrightarrow D_N,quad
(\rho_t\Lambda)(f)=\Lambda(tf).
\]

The terminal exact files give a genuine compatible pair

\[
\lambda_7\in D_7,\qquad \lambda_8\in D_8,\qquad
\rho_t(\lambda_8)=\lambda_7,qquad
\lambda_N(t^N)=1.
\]

This equality is literal: all 49 invariant lower weights of `lambda8` equal
the frozen `lambda7` weights.  The degree-eight functional adds 512 top row
orbits.  In full monomial space the supports have sizes 191 and 2,229,
respectively, with 2,038 new top rows.

## Top-orbit and profile census

Of the 512 new invariant rows, 507 have stabilizer orbit size four and five
have orbit size two.  Their variable-multiplicity profiles are

```text
1+1+1+1+1+1+1+1       464
2+1+1+1+1+1+1          45
2+2+1+1+1+1              2
2+2+2+2                  1
```

There are six edge-multiplicity profiles, nine site-degree profiles, nine
colour-endpoint profiles, and 94 combined natural profiles.  Coefficients are
not functions of those data: 53 profiles, containing 462 rows, carry more
than one coefficient.  The smallest frozen collision has identical orbit,
variable, edge, site-degree, and colour profiles but weights `1` and `-3/4`:

```text
0408757eaeccf5f6     1
0507757eaeccf5f6    -3/4
```

Thus even the combined natural profile does not define a transfer rule.

## Exact parent and Hankel obstruction

Expand the invariant functional by dividing each weight by its row-orbit
size.  The 2,038 actual top monomials have 16,092 one-coordinate deletions.
All 16,092 are globally distinct, and none belongs to the support of
`lambda7`.  Therefore no rowwise rule of the form “multiply an old support
row by one coordinate” produces any displayed top weight.

The exact first homogeneous catalecticants give a sharper obstruction.  Rows
are contraction by `t` and by each of the 240 normalized source coordinates:

| level | nonzero coordinate channels | plus `t` | exact rank | frozen minor |
|---:|---:|---:|---:|---:|
| 7 | 140 | 1 | 141 | `-2^-152` |
| 8 | 220 | 1 | 221 | `-2^-236` |

At level eight the 220 coordinate contractions of the new top layer are
already mutually independent; contraction by `t` is `lambda7` and adds the
221st direction.  The 220 active coordinate labels form 61 orbits under the
order-four chart stabilizer: 49 of size four and 12 of size two.  The 20 zero
labels form five size-four orbits.

Consequently the pair has no scalar recurrence and no rank-stable first
Hankel recurrence.  Any finite source-labelled state module containing this
particular lift must admit at least 220 new coordinate directions at the
second level.

## Nonuniqueness counterguard

The canonical top row

```text
1313131313131313
```

is the eighth power of raw coordinate 19.  Its four-row stabilizer orbit has
no incident mixed-generator column, and it lies in `ker(rho_t)`.  Hence, for
every `c in Q`,

\[
\lambda_8+c\,\delta_{19^8}
\]

is another compatible exact separator.  With `c=1`, the first catalecticant
rank rises from 221 to 225, with minor `-2^-244`.  Thus neither the displayed
top support nor its Hankel rank is intrinsic to the source class.  A
deterministic sparse extension is not by itself a canonical transfer law.

## Finite transfer criterion and remaining statement

A rigorous all-degree conclusion would follow from a finite-dimensional,
source-labelled inverse-system module stable under every coordinate
contraction, together with a degree-raising map `U` satisfying

\[
\rho_t U=1,
\]

preserving all mixed-generator annihilation relations and the target pairing.
Then iterating `U` would produce compatible `lambda_N` for all `N`.

The exact pair supplies only the first lift.  The rank jump, disjoint parent
support, profile collision, and invisible kernel direction show that none of
the natural scalar, profile-only, row-induced, or flat-Hankel candidates gives
such a `U`.  The smallest missing statement is therefore an exact lift of
`lambda8` to `D9`, or an explicitly enlarged finite contraction module with
a proved right inverse.  No degree-nine incidence or solve was run, and this
audit does not rule out a larger module with new states.

## Replay

```sh
python3 computations/unaudited-codex-n8-degree8-transfer-audit-2026-08-23/audit_lambda7_lambda8_transfer.py --check-results
python3 -O computations/unaudited-codex-n8-degree8-transfer-audit-2026-08-23/audit_lambda7_lambda8_transfer.py --check-results
python3 -I -S computations/unaudited-codex-n8-degree8-transfer-audit-2026-08-23/audit_lambda7_lambda8_transfer.py --check-results
```

The hostile mutation `--mutate-lambda8` changes the first frozen profile
weight and is rejected.  Frozen logical digest:

```text
b0effbc8122fec38eb827ca39b9cf1a921c4dff2ddadeddca454a47bfc011195
```
