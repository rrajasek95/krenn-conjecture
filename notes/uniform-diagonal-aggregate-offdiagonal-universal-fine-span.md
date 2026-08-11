# One integral identity closes arbitrary simultaneous ordered 01/10 support

## Result

The concentrated one-bad aggregate chart is empty with arbitrary
simultaneous internal support in

\[
 q_{uv}^{00},q_{uv}^{11},q_{uv}^{22},q_{uv}^{01},q_{uv}^{10} \qquad(u<v).
                                                               \tag{1}
\]

This globalizes the one-, two-, and three-cell results `b1cab97`, `950c353`,
and `2cbdffb`.  It is not a support cover: there is one integral
source-labelled identity valid on the whole 75-coordinate sector.

The identity has 165 nonzero source columns and coefficients only

```text
  1 : 121       -1 : 38        2 : 4        -2 : 2.
```

Its exact lift digest is

```text
7b6f63a4632d93247b4b929c495a694b8968be32a10a4ca1a6481bac0e6a4fea
```

Checker:
[`verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span.py`](../computations/verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span.py).

## Complete source inventory

The pure coefficient product

\[
 T=F_{01}(1111)F_{23}(2222)H(000000)                 \tag{2}
\]

has the fine token sets

```text
site 0: {0,2}       site 1: {0,2}
site 2: {0,1}       site 3: {0,1}
site 4: {0,1,2}     site 5: {0,1,2}.
```

The earlier diagonal identity used the 71 compatible rows having a
nonzero diagonal restriction.  That is not a complete inventory after
decorating the internal quadratic: a word coefficient which is zero on the
diagonal face can acquire `01/10` matching terms.

The checker therefore reconstructs every fine-token-compatible zero-target
row of

```text
top H                 71
cofactor F01          19
cofactor F23          17
cross cofactor F03    18
cross cofactor F12    18
total                143.
```

Exactly 72 of these rows are decorated-only.  Omitting them leaves an
eight-component quadratic separator and does **not** prove the theorem.
Thirty columns in the final identity come from decorated-only rows, so this
correction is load-bearing.

## Finite fine-degree source module

For each labelled row `g_r`, a polynomial multiplier contributing to (2)
must consume exactly the complementary site-colour tokens.  In sector (1),
such a multiplier is precisely a perfect matching of the complementary
tokens using a diagonal or ordered `01/10` cell.  Enumerating these is
finite and complete; it gives

```text
multiplier 01/10 degree 0 :  501 columns
multiplier 01/10 degree 1 : 1634 columns
multiplier 01/10 degree 2 : 1944 columns
multiplier 01/10 degree 3 :  978 columns
multiplier 01/10 degree 4 :  173 columns
total source columns       : 5230.
```

Expanding the columns gives 1,812 distinct monomials in the target fine
degree:

```text
off-diagonal degree 0 :  135
off-diagonal degree 2 : 1134
off-diagonal degree 4 :  543.
```

The odd degrees occur in multipliers of decorated-only rows; the resulting
complete column still has even endpoint-transition parity.  This is why a
degree-by-degree audit of only the old 71 rows cannot globalize the local
units.

## Exact membership and replay

The resulting integer source matrix has shape `1812 x 5230`.  A sparse
audit modulo `1,000,003` gives rank 1,807, cokernel dimension five, and zero
target remainder.  This modular result is diagnostic only.

For the proof, the checker sends the same constant matrix to Singular over
`QQ`, asks for a lift of the 135-term target vector, and verifies

\[
                         T=\sum_{j=1}^{165}c_jm_jg_{r_j} \tag{3}
\]

inside Singular.  It then parses the rational coefficients and independently
replays all 1,812 monomial coordinates in Python.  Every `c_j` is the integer
`+/-1` or `+/-2`, so (3) is in fact an identity over `ZZ`.

The selected columns have multiplier off-diagonal degrees

```text
degree 0 : 109       degree 1 : 24
degree 2 :  26       degree 3 :  6,
```

and use 19 top columns and 146 cofactor columns.  No division, localization,
support choice, or coefficient nonvanishing assumption appears.

Under the normalized source equations every `g_r` in (3) is zero, while
each factor in (2) equals one.  Hence (3) is the ordinary unit `1=0` and the
whole simultaneous-support sector (1) is empty.

## Scope and next interface

This theorem assumes the concentrated ordered response spokes
`(p1,s1)=(0,1)` and `(p2,s2)=(2,3)`.  It closes arbitrary diagonal plus
ordered `01/10` internal support in that chart, including any number of
overlapping decorated perfect matchings and every cancellation stratum.

It does not include ordered `02/20` or `12/21` internal cells, nor multisite
endpoint stars.  The remaining normalization question is whether axis
purification excludes those colour sectors in the projection-degenerate
one-bad landing; otherwise the same complete fine-degree construction must
be repeated with the additional allowed colour transitions.

Run

```sh
python3 computations/verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span.py
python3 -O computations/verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span.py
python3 -I -S computations/verify_uniform_diagonal_aggregate_offdiagonal_universal_fine_span.py
```

Frozen ledger digest:
`283e21edf14b5e7a3c0ce42a70621f2cd28f92a310e4fa770cfa5dab051bf7bd`.
