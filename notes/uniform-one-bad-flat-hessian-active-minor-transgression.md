# Unary target provenance routes the flat Hessian circuit to an active minor

## Outcome

The `k=2` flat circuit from `5a9d9a7` has an exact source-level dichotomy.
Write its occupied diagonal star as

\[
                 Q_c=Q_0e_c^{(0)}+Q_1e_c^{(1)},
                 \qquad S=Q_0Q_1.                       \tag{1}
\]

The two physical matchings in the mixed debt coefficient share the unit
`D=q34:00` and give

\[
                 g_Y=D(Q_0C+Q_1E)=0,                    \tag{2}
\]

where

```text
C = q12:10,       E = q02:10.
```

The unary pure-`0` target and its word differing only at site `1` give the
target-augmented private-site identity for the off-diagonal cell `C`:

\[
                    \sum_s\Delta_{2s}K_s=-C.             \tag{3}
\]

Combining (1)--(3) yields the ordinary source identity

\[
 \boxed{
 D E S =D Q_0^2\sum_s\Delta_{2s}K_s
 }
 \quad\pmod{g_Y,\ S-Q_0Q_1,\text{ unary pure/mixed rows}}. \tag{4}

After localizing the flat normal-form units `D,E,Q0`, (4) proves:

> either the diagonal-star self-square `S` vanishes, or some literal
> determinant/cofactor product `Delta_2s K_s` is nonzero.

This is the requested new source input.  It uses the constant `-1` in the
genuine unary target equation; it is not another contraction of the
symmetric Hessian recurrence.  The independent colour-2 diagonal target
and both crossed-zero rows can be imposed without changing the conclusion.
They are needed to realize the full eight-site companion row, but the
flat-to-active implication already holds in the weaker packet.

Checker:
`computations/verify_uniform_one_bad_flat_hessian_active_minor_transgression.py`.

## 1. Exact algebra

Multiplying (2) by `Q0` and using (1) gives

\[
 Q_0g_Y=D(E S+Q_0^2C).                                  \tag{5}
\]

For the unary target, put

```text
p_s=A_1s[0,0],       q_s=A_1s[1,0],
Delta_2s=p_2 q_s-q_2 p_s,       q_2=C,
```

and let `K_s` be the pure-`0` cofactor after deleting sites `1,s`.
The literal pure and mixed source rows are

\[
 G_{\rm pure}=\sum_sp_sK_s-1=0,
 \qquad G_{\rm mixed}=\sum_sq_sK_s=0.
\]

Their exact combination is

\[
 p_2G_{\rm mixed}-C G_{\rm pure}
      =C+\sum_s\Delta_{2s}K_s.                          \tag{6}

Substituting (3) into (5) gives (4), including its sign.  The checker
expands both polynomial identities over `Z`; no division is used before the
explicit localization in the nonvanishing conclusion.

This also explains the sharp scope of `5a9d9a7`.  Genuine Hessian
provenance supplied the two carriers in (2), but only the unary target
constant in (6) turns their quotient circuit into an active source minor.

## 2. The first full mixed companion row

In the eight-site common-`q` packet, the first physical companion word is

```text
21000121.
```

Its flat pivot is

```text
06:22 | 12:10 | 34:00 | 57:11.
```

The `06:22` factor is supplied by the independent colour-2 target, the
`57:11` and `34:00` factors are the other diagonal/unary anchors, and
`12:10=C` is tied to the flat self-square by (5).  Hence the pivot is
nonzero whenever `S` is nonzero.

There are 105 perfect matchings of eight sites.  Exactly six keep both
outer arms axis-purified.  Besides the pivot they are

```text
06|13|24|57     with 13:10,
06|14|23|57     with 14:10,
06|17|23|45     with 45:01,
06|17|24|35     with 35:01,
06|17|25|34     with 25:01.
```

Each contains exactly one displayed internal off-diagonal cell.  Every one
of the other 99 matchings has an off-diagonal cell incident with outer site
`6` or `7`.  Therefore the exact mixed zero row has the source-valid
alternative:

* the pivot vanishes, hence the flat self-square vanishes; or
* a nonzero cancellation mate exposes an off-diagonal physical cell.

The complete 105-matching statement is a matching partition of one fixed
source row, not a support-cardinality enumeration.  Arbitrary additional
support only adds terms already covered by one of the two classes.

## 3. What is and is not closed

Equations (4) and (6) close the Hessian-only gap for the `k=2` flat normal
form: a nonzero self-square cannot remain cofactor-invisible.  It enters the
active determinant/cofactor branch of the uniform private-site theorem.

This does **not** yet assert that the active product supplies four rank-three
deleted stars or nonflat overlap.  The crossed quadratic audit shows that
active/nonflat data can still have ranks `(2,2,3,3)`.  Upgrading the active
minor to a certified clean cap or curved doubly-good OO pair is the exact
remaining downstream gate.  The result here neither enumerates larger
supports nor claims arbitrary-`k` concentration.

## Verification

Run

```text
python3 computations/verify_uniform_one_bad_flat_hessian_active_minor_transgression.py
python3 -O computations/verify_uniform_one_bad_flat_hessian_active_minor_transgression.py
python3 -I -S computations/verify_uniform_one_bad_flat_hessian_active_minor_transgression.py
```

The frozen ledger digest is

```text
55dd1c7376c370c347353c58b66775f6f9f315b456a9c805b64ef28d4cf2c1ba
```
