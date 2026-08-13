# Matching--Bianchi does not translate the `tau_plus` pure column

## Outcome

The six-coordinate identity

\[
 B_0+\frac{(B_1-B_0)+(B_4-B_0)}2
   =\frac{B_1+B_4}2                                      \tag{1}
\]

is correct only after forgetting the physical chain row.  It does not
construct the missing `tau_plus` image.

The omitted `tau_plus` collision labels must map into the **pure full-nine
row/multiplier-column module**.  A canonical `B_i` in that module is a
three-edge `P3+K2` multiplier attached to a complete pure row; its literal
differential has 90 distinct seven-edge matching features.  The local
relative-`C4` bypasses under discussion would land on the pure columns `B0`
and `B5`.

By contrast, an endpoint matching--Bianchi difference has output in the
separate **`Q_tail` coefficient row**.  It subtracts two endpoint bars on
one deleted face, so their `Omega` and ordinary-residue entries cancel and
the surviving coefficient is a difference of three-edge tail monomials.
The ridge/Eq/tail composition theorem keeps this `Q_tail` row separate
precisely because such a difference is not a pure full-nine column or a
reduced-companion attachment.

Thus the proposed corrections

\[
 H_0=\frac{(B_1-B_0)+(B_4-B_0)}2,
 \qquad
 H_5=\frac{(B_1-B_5)+(B_4-B_5)}2                       \tag{2}
\]

exist as coefficient/tail arithmetic, but they do not alter the pure-column
component of a `B0` or `B5` bypass.

## Exact typed dual

Work in the direct sum

\[
 E_{\rm pure}\oplus E_Q,
 \qquad E_{\rm pure}\cong E_Q\cong\mathbf Q^6.          \tag{3}
\]

The two local bypasses are `(e0,0)` and `(e5,0)`, while (2) has the form
`(0,H0)` or `(0,H5)`.  The desired image is

\[
             \left(\frac{e_1+e_4}{2},0\right).          \tag{4}
\]

The primitive covector

\[
 \lambda=(0,1,0,0,1,0;\ 0,0,0,0,0,0)                  \tag{5}
\]

kills both local bypasses and every endpoint `Q_tail` correction, but reads
one on (4).  This is the smallest physically typed obstruction.  Equation
(1) is obtained only by identifying the two summands in (3), an
identification no committed source theorem makes.

## Source covariance is an additional issue

The physical target involution sends `B0` to `B5` and fixes `B1,B4`, so it
does produce the vector `H5` from `H0` in the six-dimensional target
quotient.  On the source, however, the site action `(2 5)` sends deleted
face 5 to face 2 and moves the selected normalized `C5` to a different
cycle chart.  A transformed source-chart theorem is therefore required to
promote the target involution to the proposed physical `H5`.  Granting that
covariance still leaves the direct-sum obstruction (5).

The actual decorated multiplier/fine degrees can likewise be granted: the
canonical endpoint routes meet the target in packets

```text
face 3: B0, B4, B5,
face 5: B0, B1, B2.
```

The failure is not lack of a matching graph.  It is the output-row and
chain-degree mismatch between a three-edge `Q_tail` coefficient and a pure
column with its complete 90-term boundary.

## Effect on the proof frontier

After granting a source-valid local relative-`C4` bypass to `B0/B5`, the
generic-even route still needs one of:

1. a protected same-word/fine/repeated-grade homotopy whose **pure-column**
   image is `(B1+B4)/2-B0` and its rho mate;
2. a local relative cell landing directly on `(B1+B4)/2`; or
3. the conditional denominator-Tor plus labelled-residue/anchor-cone route
   already isolated in the even repair audit.

So the untyped Bianchi equality does not retire `delta_plus` or weighted
denominator membership.  If a direct pure-column repair is later
constructed, the denominator route becomes unnecessary on that branch, but
that conclusion would come from the new pure-column cell, not from (2).

The protected two-root comparison does not fill this gap either.  The exact
committed independence guard keeps `Phi`, `J`, and the literal `q=M-a` rows
fixed while changing the labelled-residue map from rank six to rank one.
All protected `q` comparisons remain exact, but the fixed and paired repair
directions disappear.  A uniform theorem must separately transport the
pure-column/labelled-residue square in the exact word and grade.

This is a sharp scope obstruction, not nonexistence in a larger relative
source resolution.

## Verification

Run:

```text
python3 computations/verify_h3_tau_plus_bianchi_tail_chain_typing_guard.py
python3 -O computations/verify_h3_tau_plus_bianchi_tail_chain_typing_guard.py
python3 -I -S computations/verify_h3_tau_plus_bianchi_tail_chain_typing_guard.py
```

Frozen ledger SHA-256:

```text
ab24571975754e9d9e1f45ff0a137d0d78990d4d104916ff1568a88055424f1d
```
