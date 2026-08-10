# The projection-degenerate two-bad branch retracts to the one-bad packet

## Verdict

The projection-degenerate branch of the fixed-pair quotient does not need a
new support chart.  There is an exact two-parameter ordinary-source
specialization which is stronger than that branch:

> **Zero-row affine retraction.**  In the shared-endpoint two-bad normal
> form, every exact source specializes at the same order to an exact source
> in which both bad arms are essential at their outer endpoints.  The two
> diagonal direct arms, their pure deleted tensors, and hence their activity
> are unchanged.

Thus branch (ii),

\[
       \pi_t(Q_a)=0\quad\hbox{or}\quad\pi_t(R_c)=0,
\]

has an ordinary-source reduction to the already registered scalar-unit
one-bad binary-response packet.  The retraction does **not** prove that the
one-bad packet is empty.  It also need not preserve the maximum-anchor
stratum, so it does not automatically replace the synchronized main-line
representative by its limit.

The exact checker is
`computations/verify_shared_reciprocal_two_bad_zero_row_affine_retraction.py`.

## Literal two-parameter action

Use the common-hafnian notation with colours `(a,c,t)=(0,1,2)`:

\[
 Q_jK=\delta_{jc}X_c,\qquad
 R_kK=\delta_{ka}X_a,
\]

and

\[
 P_t(D_{jk}K+Q_jR_kJ)
       =\delta_{jt}\delta_{kt}X_t.                    \tag{1}
\]

For parameters `(s,u)` make the substitutions

\[
\begin{aligned}
 Q_a&\longmapsto sQ_a,&D_{ak}&\longmapsto sD_{ak}quad(k\ne c),\\
 R_c&\longmapsto uR_c,&D_{jc}&\longmapsto uD_{jc}quad(j\ne a),\\
 &&D_{ac}&\longmapsto suD_{ac}.                       \tag{2}
\end{aligned}
\]

Every odd row remains exact: `Q_aK=0` and `R_cK=0` are homogeneous zero
rows, while the two nonzero bright rows `Q_cK=X_c` and `R_aK=X_a` are
unscaled.  Every full row in (1) is bihomogeneous of degree

\[
                 (\mathbf1_{j=a},\mathbf1_{k=c}).       \tag{3}
\]

Indeed its chord term and two-star term have the same bidegree.  The only
nonzero right side is `(j,k)=(t,t)`, of degree `(0,0)`.  Therefore (2)
preserves all `1,458` literal odd rows and all `2,187` full rows, with all
endpoint order and common matching provenance retained.

This can also be read directly in the full matching expansion.  A matching
with output colour `a` at `q` either uses `pq`, whose complete contribution
is already `X_a`, or uses exactly one of the entries scaled by `s`; the
sum of all terms in the latter class is zero.  The same statement holds at
`r` in colour `c`.  The common cell `A_qr(a,c)` receives the product `su`,
so the two operations commute.

## The zero limit

At `(s,u)=(0,0)` the entire mode-`q` row `a` vanishes away from `pq`:

\[
        Q_a=0,\qquad D_{a0}=D_{a1}=D_{a2}=0.            \tag{4}
\]

Likewise the entire mode-`r` row `c` vanishes away from `pr`:

\[
        R_c=0,\qquad D_{0c}=D_{1c}=D_{2c}=0.            \tag{5}
\]

Equations (4)--(5) are precisely the outer essential flags

\[
                    p\text{ essential at }q,
             \qquad p\text{ essential at }r.           \tag{6}
\]

The direct data

\[
 A_{pq}=\lambda E_{aa},\quad H_{B\setminus\{p,q\}}
      =\lambda^{-1}X_a,
 \qquad
 A_{pr}=\mu E_{cc},\quad H_{B\setminus\{p,r\}}
      =\mu^{-1}X_c                                    \tag{7}
\]

are not changed.  Hence both arms remain active.  In the shared-endpoint
normal form the original flags are at `p`; the limit therefore lies in the
four-flag two-bad packet.  Around either preserved diagonal arm, (7) peels
one pure target and the remaining matchings give the complementary binary
target.  This is exactly the known one-bad scalar-unit packet.

## Minimality and proof-level consequence

The retraction acts on 35 aggregate scalar slots: 18 in the `q` outer row,
18 in the `r` outer row, with `D_ac` shared.  It never creates a nonzero
entry.  Consequently a globally minimum scalar-entry-support exact source
already satisfies (4)--(5); otherwise the zero limit would have smaller
support.

The current uniform spine chooses maximum anchors first and minimizes
support only within that stratum.  Some removed diagonal cells may
themselves be mutual anchors, so no anchor-preservation claim is made.
The exact conclusion is therefore:

1. branch (ii) is not an additional ordinary-existence obstruction;
2. every ordinary two-bad source has a same-order specialization to the
   known one-bad packet;
3. if one insists on retaining the synchronized maximum-anchor source, an
   additional anchor-preservation or re-synchronization lemma is required.

This is a reduction, not a Krenn contradiction and not a rational source
guard.

## Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_zero_row_affine_retraction.py
PYTHONOPTIMIZE=1 uv run python computations/verify_shared_reciprocal_two_bad_zero_row_affine_retraction.py
```

Both modes freeze the same source-row digest and ledger hash printed by the
checker.
