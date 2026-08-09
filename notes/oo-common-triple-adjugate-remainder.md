# The minimal multiplication-safe OO remainder is a 12-term K6 potential row

## Outcome

The nonlower source remainder forced by the curved two-chart lead can be
identified exactly in the literal common-triple coefficient module.  The
105 fixed-`s` second coefficients split into seven independent blocks,
according to the unique edge through `s`.  Each block is the incidence
matrix between the 15 edges and the 15 perfect matchings of a complementary
`K6`; it has rank 10 and kernel dimension 5.  Its entire kernel is

\[
 \alpha_{uv}=\beta_u+\beta_v,\qquad \sum_{u\in K_6}\beta_u=0. \tag{1}
\]

The two curvature halves lie in different blocks.  A normalized nonzero
coefficient in either block requires at least six columns, and this bound
is sharp.  Consequently the smallest multiplication-safe source identity
with lead

\[
                 L=M_{pq\mid rs}-M_{pr\mid qs}                \tag{2}
\]

has 12 columns: the two displayed lead columns and a ten-column remainder
`R`.  All ten remainder columns are in the two-star sector in both charts.
The identity is

\[
                              L+R=0,                            \tag{3}
\]

term by term in literal matching monomials.  Thus this is a genuine
multiplication-safe source row, not a formal degree-two multiple.

However, it does **not** yet kill the missing anchor.  The old integral
covector has

\[
                         \Lambda(L)=1,\qquad \Lambda(R)=-1.     \tag{4}
\]

Adjoining `R` raises the fixed-`s` lower-module rank from 10 to 11 and the
all-edge lower-module rank from 24 to 25.  The 12-term identity therefore
rewrites the curvature-anchor equation through an explicit common-two-star
remainder, but does not put that remainder in the one-edge/diagonal image.
It identifies the smallest new row needed by an adjugate lift and gives a
small exact counterguard against claiming that the adjugate formula alone
closes the overlap gate.

The literal all-nine provenance audit sharpens this further.  At the fixed
fine word, all 18 labelled rows are retained before cutting, but exactly
one mixed row per chart and the two labelled `22` anchors are compatible.
The ten-column remainder is not one physical coefficient row.  It is
exactly the normal side of the single cross-chart direct-double Bianchi
packet (3).  After the full OO rank-one normalization the packet is scaled
by the curvature unit `kappa`; the same integral witness reads
`Lambda(kappa R)=-kappa`, so it remains nonzero on the curvature-open
locus.  The missing object is therefore specifically a
connection-to-diagonal null-homotopy, not another Bianchi relation or a
higher coefficient operation.

## The complete K6 kernel

Fix an edge `sv`.  The other six vertices form a set `U`.  A column is

\[
            M_{sv\mid uv}=sv\,uv\,\partial_{sv}\partial_{uv}H_w,
            \qquad \{u,v\}\subset U.                          \tag{5}
\]

Every matching containing `sv` is `sv` together with a perfect matching
`{e1,e2,e3}` of `U`.  Therefore the coefficient of that matching in the
linear combination defined by (1) is

\[
 \alpha_{e_1}+\alpha_{e_2}+\alpha_{e_3}
       =\sum_{u\in U}\beta_u=0.                               \tag{6}
\]

This proves that the five-dimensional zero-sum potential space lies in the
kernel.  Exact elimination gives rank 10 for the 15 columns, so (1)
exhausts the kernel.  The seven choices of `sv` have disjoint matching
supports, hence the full fixed-`s` kernel is their direct sum and has
dimension 35.

For a normalized edge coefficient `alpha_uv=1`, at least six of the 15
edge coefficients are nonzero.  The checker proves the lower bound by
exhausting every putative support of size at most five over the rationals.
Sharpness is witnessed by the `3+3` potential

\[
 (\beta_1,\ldots,\beta_6)
       =(1/2,1/2,1/2,-1/2,-1/2,-1/2),                        \tag{7}
\]

whose six nonzero edge coefficients are integral: `+1` on the three edges
inside the first triple and `-1` on the three edges inside the second.

## The explicit minimal full coefficient

Write `D={d0,d1,d2,d3}`.  In the `rs` block use the positive triple
`{p,q,d0}` and negative triple `{d1,d2,d3}`.  This gives

\[
\begin{aligned}
0={}&M_{pq\mid rs}+M_{pd_0\mid rs}+M_{qd_0\mid rs}\\
   &-M_{d_1d_2\mid rs}-M_{d_1d_3\mid rs}-M_{d_2d_3\mid rs}.
                                                               \tag{8}
\end{aligned}
\]

In the `qs` block reverse the signs on the triples
`{p,r,d0}` and `{d1,d2,d3}`:

\[
\begin{aligned}
0={}&-M_{pr\mid qs}-M_{pd_0\mid qs}-M_{rd_0\mid qs}\\
   &+M_{d_1d_2\mid qs}+M_{d_1d_3\mid qs}+M_{d_2d_3\mid qs}.
                                                               \tag{9}
\end{aligned}
\]

Adding (8) and (9) gives (3).  The two lead columns are respectively
direct in the `pq` chart and direct in the `pr` chart.  Every other column
in (8)--(9) contains neither deleted pair `pq` nor `pr`, so all ten terms
of `R` have literal common-two-star provenance.

After expanding the second coefficients, both `L` and `R` have six source
matching terms and `R=-L`.  The ten-column presentation is nevertheless
the relevant information: it is the full multiplication-safe coefficient
row whose two-column associated lead is (2).

## Relation to the adjugate proposal

For a normalized rank-two direct block,

\[
 B=uv^{\mathsf T}+qxy^{\mathsf T},\qquad
 \operatorname{adj}(B)=q(v\times y)(u\times x)^{\mathsf T},
 \qquad B\operatorname{adj}(B)=0.                            \tag{10}
\]

Any fixed-`s` common-triple coefficient extracted from (10) is a literal
source relation among the columns (5).  Hence the kernel classification
above forces it to be a sum of the potential rows (1).  If its curvature
lead is normalized to (2), it must use the `rs` and `qs` blocks and has at
least 12-column support.  Equations (8)--(9) give a support-minimal full
coefficient with that lead.  Other adjugate extractions can differ by
additional potential rows, but their source remainder is still `-L` and
still has pairing `-1`.

The same 12-column row is the literal matching expansion of the standard
cross-chart direct-double Bianchi identity: the two direct columns form
`L`, while the ten common-two-star columns form its normal packet `R`.
It is not a single physical full-nine coefficient; it is one labelled
connection relation between the two compatible full-nine presentations.

This is the exact conclusion available from the common-triple module.  A
source-labelled derivation identifying one particular matrix entry of
(10) with the chosen `3+3` representative has not been supplied and is not
needed for the no-go: the kernel classification covers every possible
representative with lead (2).

## Why the new row does not yet close the target

The four-column anchor identity from the preceding calculation is

\[
              L-D^{pq}_{pq\mid rs}+D^{pr}_{pr\mid qs}
                    =\kappa X_2^D.                            \tag{11}
\]

Using (3) rewrites it as

\[
             -R-D^{pq}_{pq\mid rs}+D^{pr}_{pr\mid qs}
                    =\kappa X_2^D.                            \tag{12}
\]

The integral covector from the lower-filtration obstruction kills every
one-edge row and every labelled diagonal row.  It takes value `-1` on `R`,
so `R` is not an existing lower correction.  Exact ranks give

\[
\begin{array}{c|cc}
\text{known lower image}&\operatorname{rank}&
 \operatorname{rank}\text{ after adjoining }R\\ \hline
\text{fixed-}s\text{ one-edge + diagonal}&10&11\\
\text{all one-edge + diagonal}&24&25.
\end{array}                                                   \tag{13}
\]

The all-nine filter is also exact here.  Before taking the coefficient,
there are nine labelled physical rows in each chart.  The fine word
selects precisely the `pq:(a,0)` and `pr:(a,1)` mixed rows, while the
missing-anchor cut selects the two labelled `22` rows.  No other row has
the required multidegree.  Thus the rank calculation already includes
every physical full-nine row that can enter this coefficient packet; it
does not replace the full-nine system by anonymous generators.

These statements are universal in the normalized word
`(a,0,1,ell,2,2,2,2)` and use no division by a source edge.  The curved
rank-one direct-arm normalization supplies the unit curvature lead.  It
scales the normal packet by `kappa`, and (4) becomes
`Lambda(kappa R)=-kappa`, nonzero on the prescribed curvature open set.
So the OO substitutions do not turn (12) into zero.  Since `R` is already
the existing Bianchi normal packet, another Bianchi row or another
principal-parts order would only re-present the same class.  A proof needs
an additional **connection-to-diagonal null-homotopy** whose boundary sends
this normal packet into the labelled anchor difference in (12).

## Reproduction

Run

```text
python3 computations/verify_oo_common_triple_adjugate_remainder.py
python3 -O computations/verify_oo_common_triple_adjugate_remainder.py
```

The checker verifies the seven-block decomposition, exact ranks and kernel
classification, the rational support lower bound, the 12-term integral
identity for all nine normalized colour types, the common-two-star
provenance of all ten remainder columns, the pairings `1/-1`, and both
augmented-rank counterguards.  The frozen ledger digest is

```text
87d3f988aa90c6bb4823062a165348cd42510f55fcfeb034a462d5e67ca15ddd
```
