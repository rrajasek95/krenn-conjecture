# Invertible zero alignment descends to planes, but survives seven rows

## 1. Outcome

Work at the first \(8\to6\) boundary with a literal full-nine chart

\[
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2,                                  \tag{1}
\]

and put, at a residual site \(x\),

\[
 P_x\xi=\sum_i\xi_i(p_i)_x,
 \qquad S_x\eta=\sum_j\eta_j(s_j)_x,
 \qquad N_{x,e}=P_x^{\mathsf T}J_eS_x.                   \tag{2}
\]

When \(d\) is invertible, total failure of the full-selector dark-cut
descent gives

\[
 T_e=\{x:N_{x,e}=0\},\qquad |T_e|\geq3
 \quad(e=0,1,2).                                        \tag{3}
\]

There are two exact consequences.

First, the nine incidences in (3) cannot remain an unstructured list.
Let

\[
 a_x=|\{e:x\in T_e\}|,
\]

let \(L\) count sites with \(a_x\geq2\) and
\(\operatorname {rank}P_x+\operatorname {rank}S_x\leq3\), and let \(C\)
count sites at which the two images are the same literal coordinate plane.
Then

\[
                         \boxed{2L+C\geq3.}              \tag{4}
\]

Every site counted by \(C\) is aligned at exactly the two coordinate axes
in that plane.  In particular, if there is no local rank-defect site, at
least three residual sites carry common endpoint-star images equal to
literal coordinate planes.  If there is no coordinate-plane site, at
least two sites have one endpoint map of rank at most one.  This is the
case-free rank/plane descent of the invertible alignment survivor.

Second, all nine source rows impose a pure-slice constraint which is not
visible in (3).  For a physical colour \(c\), scalarize the internal
quadratic and endpoint stars at the constant word \(c^6\).  If \(F_c\) is
the scalar hafnian and \(H_c\) its cohafnian matrix, then

\[
                P_c^{\mathsf T}H_cS_c=E_{cc}-F_cd.       \tag{5}
\]

Consequently, for invertible \(d\),

\[
\begin{array}{c|c}
F_c\ne0&\operatorname {rank}P_c,
         \operatorname {rank}S_c\geq2,\\
F_c=0&P_c^{\mathsf T}H_cS_c=E_{cc},
       \quad P_c,S_c\ne0.
\end{array}                                               \tag{6}
\]

Thus a local rank defect in (4) cannot be promoted to a globally missing
physical channel.  The fixed-label diagonal anchors force every physical
colour to occur on both endpoint stars, with rank at least two whenever
the corresponding pure internal hafnian is nonzero.

These facts do **not** yet close the invertible branch.  There is a sharp
literal two-chart guard with

* both direct blocks equal to \(\operatorname {diag}(6,1,1)\);
* four injective endpoint-star triples;
* nonzero physical curvature \(AU-BF=-72\);
* \(T_e\) of size five for every target in both charts;
* the unary diagonal row and all six off-diagonal rows in both charts; and
* exactly the other two diagonal target rows missing.

The guard proves that invertibility, the rank/plane descent, a second
literal chart, and curvature do not replace the two unused target tensors.
The remaining positive statement must mix one of those anchors with an
off-diagonal row before the common power is lost.  This note does not claim
that the complete nine-row system has such a guard.

## 2. The rank/plane incidence lemma

For a fixed target \(e\), the form

\[
 \omega_e(\bar u,\bar v)=\det(u,v,e_e)
\]

is symplectic on \(V/\mathbb Ce_e\).  Hence

\[
 P^{\mathsf T}J_eS=0
 \quad\Longleftrightarrow\quad
 \overline{\operatorname {im}P}_e
 \perp_{\omega_e}
 \overline{\operatorname {im}S}_e.                       \tag{7}
\]

The two quotient dimensions sum to at most two, and each original image
can gain at most the target line.  Therefore

\[
                    \operatorname {rank}P+
                    \operatorname {rank}S\leq4.          \tag{8}
\]

Suppose the same site is aligned at two distinct targets \(e,f\).  For
every \(u\in\operatorname {im}P\) and \(v\in\operatorname {im}S\), the
cross product \(u\times v\) is perpendicular to both \(e_e\) and \(e_f\).
If the rank sum is four, neither image can have dimension three: a
three-dimensional image would force the other image into both target
lines and hence to zero.  Both images are therefore two-planes.  A nonzero
cross product has the unique direction perpendicular to
\(E_{ef}=\operatorname {span}(e_e,e_f)\), forcing

\[
               \operatorname {im}P=
               \operatorname {im}S=E_{ef}.              \tag{9}
\]

Conversely, two surjections onto \(E_{ef}\) are aligned at \(e,f\), but
not at the complementary target.  Thus a site with \(a_x\geq2\) either is
counted by \(L\), or is counted by \(C\) and has \(a_x=2\).

Now

\[
 \sum_xa_x=\sum_e|T_e|\geq9.
\]

At most six sites have \(a_x>0\), so

\[
 \sum_x(a_x-1)_+
   =\sum_xa_x-|\{x:a_x>0\}|\geq3.                       \tag{10}
\]

A site counted by \(L\) contributes at most two to (10), while a site
counted by \(C\) contributes one.  Equation (4) follows.  Notice that this
uses no enumeration of target-set patterns.

There is also a useful fixed-channel rendering of one alignment.  If

\[
 u_{x,c}=P_x^{\mathsf T}e_c^*,\qquad
 v_{x,c}=S_x^{\mathsf T}e_c^*,
\]

and \(\{e,f,g\}=\{0,1,2\}\), then

\[
 N_{x,e}=0
 \quad\Longleftrightarrow\quad
 u_{x,f}v_{x,g}^{\mathsf T}
       =u_{x,g}v_{x,f}^{\mathsf T}.                     \tag{11}
\]

When both sides are nonzero, the \(f,g\) channel rows on the two endpoint
stars have the same proportionality scalar.  If, for example,
\(u_{x,f}=0\), equation (11) forces either \(u_{x,g}=0\) or
\(v_{x,f}=0\); the other three one-factor cases are symmetric.
This is the local mechanism behind the low-rank/coordinate-plane split.

## 3. The complete diagonal anchors give (5)

Let \(Q_c\) be the scalar six-site edge matrix obtained by taking the
\((c,c)\) entry of every internal block of \(q\), and put

\[
 F_c=\operatorname {haf}(Q_c).
\]

Let \(P_c,S_c\in\operatorname {Mat}_{6\times3}\) record the coefficients
of the three endpoint rows at physical colour \(c\).  Taking the constant
word \(c^6\) in every one of the nine equations (1) gives exactly

\[
 P_c^{\mathsf T}H(Q_c)S_c=E_{cc}-F_cd,                  \tag{12}
\]

which is (5).  Endpoint order is retained by the two rectangular factors;
there is no symmetric-edge assumption.

If \(F_c\ne0\), then \(F_cd\) has rank three and \(E_{cc}\) has rank one,
so

\[
 \operatorname {rank}(E_{cc}-F_cd)\geq2.                \tag{13}
\]

The rank of the sandwich in (12) is bounded by the rank of either endpoint
factor, proving the first line of (6).  If \(F_c=0\), equation (12) is the
literal rank-one target anchor \(E_{cc}\), proving the second line.  This
argument is cancellation-safe and uses the physical target labels.

## 4. An invisible direct-block padding lemma

The guard uses one small observation which is useful beyond the example.
Consider overlapping \(pq\)- and \(pr\)-charts.  Suppose

\[
 (q^{pq})^{[3]}=(q^{pr})^{[3]}=0,                       \tag{14}
\]

every monomial of \((q^{pq})^{[2]}\) occupies the cross site \(r\), and
every monomial of \((q^{pr})^{[2]}\) occupies the cross site \(q\).
Then arbitrary changes to the physical block \(A_{pr}\) do not change any
row of the \(pq\)-system: they change only the \(p\)-star at site \(r\),
where every new response term collides with \((q^{pq})^{[2]}\).  In the
\(pr\)-system the same changes multiply \((q^{pr})^{[3]}=0\).  The
transposed assertion holds for arbitrary changes to \(A_{pq}\).

Thus both direct blocks may be padded independently without changing
either nine-row ledger.  Invertibility of the direct block alone carries
no information on this nilpotent boundary.

## 5. The exact two-chart guard

Use the eight sites

\[
                       \{p,q,r,a,b,c,d,s\}              \tag{15}
\]

and only equal-colour aggregate cells.  The nonzero cells are

\[
\begin{array}{c|l}
0&pq:6,\ pr:6,\ pa:1,\ pb:1,\ pc:1,\ qr:1,\ qd:1,
   \ qs:6,\ rd:-1,\ rs:-6,\ ab:-1/12,\\
1&pq:1,\ pr:1,\ pa:1,\ qr:1,\\
2&pq:1,\ pr:1,\ pb:1,\ qr:1.
\end{array}                                               \tag{16}
\]

All unlisted cells vanish.  On both charts the direct block is

\[
                         d=d'=\operatorname {diag}(6,1,1). \tag{17}
\]

### 5.1 The \(pq\)-chart

On \(W_{pq}=\{r,a,b,c,d,s\}\),

\[
 q=-\frac1{12}(ab)_0-(rd)_0-6(rs)_0,                    \tag{18}
\]

and

\[
 q^{[2]}=\frac1{12}(ab)_0(rd)_0
             +\frac12(ab)_0(rs)_0\ne0,
 \qquad q^{[3]}=0.                                      \tag{19}
\]

The endpoint rows are

\[
\begin{aligned}
(P_0,P_1,P_2)&=(a_0+b_0+c_0+6r_0,\ a_1+r_1,\ b_2+r_2),\\
(S_0,S_1,S_2)&=(r_0+d_0+6s_0,\ r_1,\ r_2).
\end{aligned}                                            \tag{20}
\]

Both triples are independent.  Every monomial in (19) contains \(r\), so
the new \(r_1,r_2\) terms are collision-invisible.  Direct multiplication
gives

\[
 P_0S_0q^{[2]}=X_0,
 \qquad P_iS_jq^{[2]}=0\quad(i\ne j),                   \tag{21}
\]

while

\[
 P_1S_1q^{[2]}=P_2S_2q^{[2]}=0.                         \tag{22}
\]

Since \(q^{[3]}=0\), (21) is the unary row and all six off-diagonal rows,
whereas (22) fails exactly the \(X_1,X_2\) anchors.

At \(a,b,c\), the second local endpoint map is zero.  At \(d,s\), the
first local endpoint map is zero.  Therefore

\[
 T_0=T_1=T_2=\{a,b,c,d,s\}.                              \tag{23}
\]

At the remaining site \(r\), \(P_r=d'\) and \(S_r=I\), so
\(P_r^{\mathsf T}J_eS_r\ne0\) for every \(e\).  Thus (23) is exact, not
merely a lower bound.

### 5.2 The \(pr\)-chart and curvature

Deleting \(p,r\) instead gives

\[
 q'=-\frac1{12}(ab)_0+(qd)_0+6(qs)_0,                   \tag{24}
\]

and every monomial of \((q')^{[2]}\) contains \(q\).  The endpoint rows
are

\[
\begin{aligned}
(P'_0,P'_1,P'_2)&=(a_0+b_0+c_0+6q_0,\ a_1+q_1,\ b_2+q_2),\\
(R_0,R_1,R_2)&=(q_0-d_0-6s_0,\ q_1,\ q_2).
\end{aligned}                                            \tag{25}
\]

The same collision calculation proves (21)--(23), with \(q\) replacing
\(r\) as the unique nonaligned residual site.  Both endpoint triples are
again independent.

At the all-zero four-cut \(p,q,r,s\),

\[
 (A,B,F,U)=(6,6,6,-6),
 \qquad AU-BF=-72\ne0.                                  \tag{26}
\]

Because (16) is one literal aggregate packet, all power-free overlap and
Bianchi identities between the two charts hold automatically.  The guard
therefore retains the actual physical curvature, not an abstract scalar
substitute.

For colours \(1,2\), the internal pure matrices in both charts vanish.
Thus \(F_c=H_c=0\), and the left side of (5) is zero.  The failed rows are
precisely the two equations which would replace that zero by \(E_{11}\)
and \(E_{22}\).  This identifies the missing source input without a
genericity argument.

## 6. Exact scope and next lemma

The positive content is the normal form (4) together with the complete-row
rank constraint (6).  The negative content is sharper than a one-chart
seven-row guard: even two literal charts, two invertible direct blocks,
five zero-alignment sites per target, four good endpoint stars, a nonzero
common power \(q^{[2]}\), and nonzero physical curvature survive until the
two complementary diagonal anchors are imposed.

Accordingly the remaining invertible-branch statement can be phrased
without reopening selector cases:

> **Anchored zero-alignment exclusion.**  In a literal two-chart packet
> with the complete nine rows, use a first site coefficient of one of
> \(P_c^{\mathsf T}H_cS_c=E_{cc}-F_cd\), \(c=1,2\), together with an
> off-diagonal common-power row to show that the configuration (4) either
> has a selector with at most two genuinely blocked sites or descends to a
> source-valid filtered overlap class.

The guard proves that deleting either the physical tensor \(E_{11}\) or
\(E_{22}\) from that argument is not a harmless scalar relaxation.  It
does not prove the anchored exclusion and does not close the conjecture.

The lightweight checker
[`verify_invertible_zero_alignment_two_chart_anchor_guard.py`](../computations/verify_invertible_zero_alignment_two_chart_anchor_guard.py)
audits both nine-cell ledgers, the two direct determinants, all four star
ranks, the exact alignment sets, the collision hypotheses of the padding
lemma, the two missing target rows, curvature, and the incidence count in
(4).
