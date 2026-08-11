# Pure unary attachment obstructs the three-column diagonal transfer

## Result

The `c536b88` common-`q` transfer cannot be completed to a unary source by
adding an arbitrary pure-zero coordinate slice.  The obstruction is an
ordinary integral source identity, not a support census or a formal
cofactor packet.

Keep the seven coordinate-`11` cells of the transfer guard fixed, and put an
independent coefficient `z_uv` on the `00` cell of **every** physical edge
of the eight-site core.  No value of `z04` or `z34` is fixed.  Impose the
literal physical equations

\[
 q^{[4]}=X_0,
 \qquad
 (e_1^{(0)}+e_1^{(1)}+e_1^{(2)})e_1^{(7)}q^{[3]}=X_1.  \tag{1}
\]

Their coefficient ideal is the unit ideal over `Z`.  An exact certificate
uses 22 original source rows and expands directly to `1`.  Therefore an
arbitrary pure-`00` unary attachment cannot preserve even the aggregate
diagonal response, a weaker requirement than preserving the three columns
of `c536b88` separately.

Checker:
`computations/verify_uniform_axis_circuit_k3_pure_unary_attachment_unit.py`.

## Exact source system

The fixed `11` slice is

```text
12:11 =  1       02:11 = -1       56:11 = 1
25:11 =  1       36:11 =  1       13:11 = -1
14:11 =  1.
```

All 28 cells `uv:00` are variables.  Complete perfect-matching expansion of
(1) yields

```text
24 nonzero unary coefficient rows,
23 nonzero aggregate-response coefficient rows.
```

The response is the actual contraction by the three-site star sum.  The
checker never declares the individual columns `C0,C1,C2` as separate source
equations.  This is the source-valid strengthening missing from a
columnwise attachment test.

## The ordinary 22-row lift

Let `g_top(w)` and `g_resp(w)` denote the literal coefficient generators in
(1).  The checker freezes the 22 nonzero multipliers returned by exact
`QQ` `liftstd`, but verifies their identity independently in `Z[z_uv]`:

\[
 \sum_w A_w(z)g_{\rm top}(w)
 +\sum_w B_w(z)g_{\rm resp}(w)=1.                       \tag{2}
\]

The first term is `-g_top(00000000)`; the remaining 21 rows reconstruct its
pure hafnian tail.  Multiplier support is

```text
1 term:   9 multipliers
2 terms:  1 multiplier
3 terms:  4 multipliers
5 terms:  3 multipliers
7 terms:  1 multiplier
10 terms: 2 multipliers
13 terms: 2 multipliers
```

No inverse, saturation variable, nonvanishing assumption, or coefficient
normalization occurs.  In particular (2) does not use `z34-1` or `z04-t`.
The identity is valid over every commutative ring.

## Structural consequence

This closes the first genuine unary attachment to the diagonal transfer
family, including arbitrary cancellation among all pure-zero perfect
matchings.  It also contains the special `t=0` two-column fibre: one cannot
first contract to `k=2` and then attach a pure unary matching.

Combine the result with the nonanchor off-diagonal theorem `336492c`:

* a pure-zero coordinate attachment is impossible by (2);
* an off-diagonal cell on a physical edge outside the union of the three
  selected pure target matchings reselects to a rank-`(3,3)` good pair and
  an active determinant/cofactor product.

Thus an unresolved source-valid unary attachment must leave the pure slice
through one of two sharply named gates:

1. an off-diagonal decoration on an already selected anchor edge; or
2. a simultaneous deformation of the `11/22` coordinate slices.

Only after such an attachment exists is it meaningful to impose the second
diagonal response and the two crossed-zero rows.  This note does not create
a full one-bad source, and it does not claim that a good active pair is
already a clean or curved landing.

## Verification

Run

```text
python3 computations/verify_uniform_axis_circuit_k3_pure_unary_attachment_unit.py
python3 -O computations/verify_uniform_axis_circuit_k3_pure_unary_attachment_unit.py
python3 -I -S computations/verify_uniform_axis_circuit_k3_pure_unary_attachment_unit.py
```

The checker pins the genuine `k=3` common-`q` transfer and the nonanchor
off-diagonal reselection theorem, reconstructs all 47 source rows from
physical matchings, and expands (2) monomial by monomial.

Frozen ledger SHA-256:

```text
f37fc9f482f0876ef60701a3b6ef9438244f23f999fd7d360b0f59899a3e529e
```
