# Doubly-good curved OO overlap survives one diagonal anchor

## 1. Outcome

The normalized `22/21` OO atom from
[`oo-one-anchor-permanent-null-frontier.md`](oo-one-anchor-permanent-null-frontier.md)
does **not** imply a curvature-weighted coefficient transport identity.
There is a ten-cell integral eight-site packet with all of the following:

* rank-one direct arms with distinct outgoing head axes `0,1`;
* both arms doubly good, with all four deleted-star ranks equal to three;
* a literal curvature minor `kappa=-1`;
* right-ruling target-`2` alignment at every residual site of both charts;
* the complete `22` target row in both charts; and
* every off-diagonal row equal to zero, in particular the `pq` row `21`
  and its `pr` counterpart `20`.

In fact its complete matching tensor is exactly the single pure tensor
`X_2`.  It fails only the two missing diagonal targets `X_0,X_1`, so it is
not a ternary source.  Thus neither one diagonal anchor plus one
off-diagonal coefficient, nor even one diagonal anchor plus **all six**
off-diagonal rows in both charts, closes the doubly-good curved OO overlap.
At least one differently labelled diagonal anchor is indispensable.

This also disproves the proposed ratio

\[
 [21]_{\omega}=\kappa[22]_{2^6}                              \tag{1}
\]

modulo the doubly-good and target-`2` RR alignment conditions: the two
sides are `0` and `-1` in the packet.

## 2. The ten cells

Use sites

\[
                       p,q,r,a,b,c,d,s.                       \tag{2}
\]

Every displayed cell has coefficient one.  The two direct arms are

\[
                         A_{pq}=E_{00},\qquad
                         A_{pr}=E_{01}.                       \tag{3}
\]

The other incident cells at `p,q` are

\[
\begin{array}{c|l}
p&(pd)_{0,0},\ (pc)_{1,1},\ (pa)_{2,2},\\
q&(qr)_{0,0},\ (qc)_{0,0},\ (qr)_{1,1},\ (qb)_{2,2},
\end{array}                                                  \tag{4}
\]

and the remaining two cells are

\[
                         (rc)_{2,2},\qquad(ds)_{2,2}.          \tag{5}
\]

Here two different endpoint-colour cells on `qr` are retained in the same
aggregate physical block.  Endpoint order in (3)--(5) is literal.

Sites `a,b,s` have only one incident physical block.  Every perfect
matching must therefore use

\[
                         pa\mid qb\mid rc\mid ds,              \tag{6}
\]

and all four selected cells have colour `2`.  Consequently

\[
                              H_8(A)=X_2.                      \tag{7}
\]

Equation (7) proves at once that every off-diagonal pair row vanishes and
the `22` pair row is `X_2` in every chart.

## 3. Goodness, curvature, and alignment

In the `pq` chart the endpoint rows are

\[
\begin{aligned}
 P_0&=e_1^{(r)}+e_0^{(d)},&
 P_1&=e_1^{(c)},&P_2&=e_2^{(a)},\\
 S_0&=e_0^{(r)}+e_0^{(c)},&
 S_1&=e_1^{(r)},&S_2&=e_2^{(b)},
\end{aligned}                                               \tag{8}
\]

which are injective.  In the `pr` chart, deleting `r` leaves the three
independent `p` rows supported respectively at `q/d`, `c`, and `a`.
At `r`, after deleting `p`, rows `0,1` occur at `q` and row `2` at `c`.
Thus all four deleted-star ranks are

\[
                              (3,3,3,3).                       \tag{9}
\]

At the fourth site `c`, with shared `p`-row zero and output colour zero,

\[
 \kappa=A_{pq}(0,0)A_{rc}(1,0)
       -A_{pr}(0,1)A_{qc}(0,0)=0-1=-1.                      \tag{10}
\]

For target `2`, the local matrices

\[
                    N^{q}_{x,2}=P_x^{\mathsf T}J_2S_x
\]

have only column `0`, the head of `A_pq`; their only nonzero sites are
`r,c`.  In the `pr` chart the analogous matrices have only column `1`, the
head of `A_pr`; their only nonzero site is `q`.  Zero matrices count as
aligned, so both right-ruling alignment ledgers contain all six residual
sites, much more than the required three.

## 4. Consequence for the OO full-nine attack

The finite saturation proposed in the previous note is nonempty.  The
packet gives a rational point on the locus with four good-star minors,
nonzero curvature, both target-`2` RR ledgers, the `22` anchor, and the
crossed off-diagonal rows.  Hence no polynomial reduction of the form (1)
can follow from that ideal.

The smallest plausible OO input at this stage was the threshold identified
by the independent one-anchor selector guard:

\[
 \boxed{\text{two differently labelled diagonal target rows, a crossed
 off-diagonal row, and faithful two-chart transport.}}        \tag{11}
\]

The present packet dies as soon as either `X_0` or `X_1` is imposed.
However, the subsequent
[`two-anchor OO counterguard`](oo-doubly-good-two-anchor-counterguard.md)
shows that one additional anchor still does not suffice: an alternating
cycle realizes `X_0+X_2` with the same doubly-good curved OO structure and
all off-diagonal rows.  The remaining threshold is the complete
three-diagonal/full-nine system.

## 5. Reproduction

```sh
python3 computations/verify_oo_doubly_good_one_anchor_counterguard.py
python3 -O computations/verify_oo_doubly_good_one_anchor_counterguard.py
```

The checker enumerates the full endpoint-coloured matching tensor, audits
all four exact star ranks, the curvature minor, both sitewise RR alignment
ledgers, the two pair-chart target/off-diagonal slices, and the numerical
failure of (1).
