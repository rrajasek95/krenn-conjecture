# A tilted second chart is active unless its whole direct block vanishes

## 1. Outcome

The automatic two-chart packet left generic activity of the second canonical
line as an extraction gate.  The scalar activity obstruction can be removed
after allowing an explicit physical tilt, except when the whole direct block
vanishes.  The price is a new, explicit theorem-design obligation: the
canonical overlap and inactive-root arguments must be extended to the tilted
matrix direction.

Use the all-label notation

\[
\begin{aligned}
 P_{ij}&=A_{pq}(i,j),& R_{ik}&=A_{pr}(i,k),\\
 Q_{jl}&=A_{qs}(j,l),& S_{kl}&=A_{rs}(k,l),
\end{aligned}
\]

and fix the selected entries

\[
 A=P_{ab}\ne0,\quad B=R_{ac},\quad F=Q_{bd},\quad U=S_{cd},
 \qquad \kappa=AU-BF\ne0.                                  \tag{1}
\]

**Theorem 1.1 (tilted second-chart activity).**

1. If \(R=A_{pr}\ne0\), then either the canonical line
   \(uE_{ac}+vI\) is already active or an explicit line

   \[
                         K(u,v)=uE_{ac}+v(I+E_{ij})            \tag{2}
   \]

   through the same selected cap is generically active.  Here \(R_{ij}\)
   is any nonzero entry chosen only in the residual case
   \(B=\operatorname{tr}R=0\).  The tilt retains all nine physical-label
   rows and preserves \(\kappa\) as the \(u\)-coefficient of the literal
   four-cut curvature.
2. The intrinsic same-pair obstruction is exactly \(R=0\), not merely
   \(B=\operatorname{tr}R=0\).  In this case no line of cap matrices on
   \(pr\) can be active.  Nevertheless the chart remains a split,
   power-free auxiliary:

   \[
       p_it_kq^{[h-1]}=\delta_{ik}X_i,\qquad
       D=At,\qquad
       C_4=Atv+AUz.                                           \tag{3}
   \]

   Since \(A,U\ne0\), this auxiliary is triangular and nonflat.

Thus a suitably generalized two-chart saturation theorem need localize only
the first, already active \(pq\)-chart.  The \(pr\)-chart may enter through
its power-free overlap even on the intrinsic zero-block boundary.  What
remains open is the one-sided overlap rank defect: one literal diagonal
target row must still be passed through the split.  The tilt changes the
distinguished matrix direction from \(I\) to \(I+E_{ij}\), mixes the common
\(p\)-label in its \(J\)-term, and does not automatically preserve the
canonical common-\((L,M)\) packet.  Branch-specific overlap and inactive
routing must therefore be proved for that general direction.

## 2. Full-nine contraction along an arbitrary cap matrix

Let \(q\) be the \(pr\)-internal quadratic and \(p_i,t_k\) its two endpoint
stars.  The complete pair rows are

\[
             R_{ik}q^{[h]}+p_it_kq^{[h-1]}=\delta_{ik}X_i.
                                                                    \tag{4}
\]

For any \(3\times3\) matrix \(K\), put

\[
\begin{aligned}
 s(K)&=\sum_{i,k}K_{ik}R_{ik},\\
 r(K)&=\sum_{i,k}K_{ik}p_it_k,\\
 T(K)&=\sum_iK_{ii}X_i.
\end{aligned}                                                \tag{5}
\]

Multiplying (4) by \(K_{ik}\) and summing gives the exact fixed-label
identity

\[
                         s(K)q^{[h]}+r(K)q^{[h-1]}=T(K).       \tag{6}
\]

No endpoint basis change or target relabelling is involved.

## 3. Explicit tilt when the canonical scalar vanishes

The canonical line is already generically active when
\((B,\operatorname{tr}R)\ne(0,0)\).  It remains to assume

\[
                         B=0,\qquad\operatorname{tr}R=0,
 \qquad R\ne0.                                               \tag{7}
\]

Choose a nonzero entry \(R_{ij}\) and set

\[
                         J=I+E_{ij},\qquad
                         \beta=\sum_{r,s}J_{rs}R_{rs}.
\]

Equation (7) gives

\[
                         \beta=R_{ij}\ne0.                    \tag{8}
\]

This remains true when \(i=j\): the corresponding diagonal entry of \(J\)
is two and the trace contribution is zero.  Every diagonal entry
\(j_l=J_{ll}\) is nonzero.

On the line (2), equations (5) give

\[
\begin{aligned}
 s(u,v)&=\beta v,\\
 \kappa_l(u,v)&=K_{ll}(u,v)
      =u\,{\bf1}_{a=c=l}+vj_l.
\end{aligned}                                                \tag{9}
\]

Therefore its activity polynomial is

\[
 s\prod_l\kappa_l=
 \begin{cases}
 \beta j_0j_1j_2v^4,&a\ne c,\\
 \beta\left(\prod_{l\ne a}j_l\right)v^3(u+j_av),&a=c.
 \end{cases}                                                 \tag{10}
\]

Both expressions are nonzero.  Substitution in (6) records the exact
tilted line:

\[
\begin{aligned}
 \beta vq^{[h]}
 +\left(up_at_c+v\sum_{i,k}J_{ik}p_it_k\right)q^{[h-1]}
 =u\delta_{ac}X_a+v\sum_i j_iX_i.                            \tag{11}
\end{aligned}
\]

Thus the same good physical pair is active without choosing a new minor or
changing a fixed label.

## 4. The original curvature is retained

On the common complement of \(p,q,r,s\), let \(z\) be the internal
quadratic, \(x_i,y_b,t_k,v_d\) the four star rows, and put
\(E_{id}=A_{ps}(i,d)\).  Use the raw effective forms

\[
\begin{aligned}
 f_{ib}&=P_{ib}z+x_iy_b,\\
 g_{ik}&=R_{ik}z+x_it_k,\\
 H_{ib;d}&=P_{ib}v_d+E_{id}y_b+Q_{bd}x_i,\\
 N_{ik;d}&=R_{ik}v_d+E_{id}t_k+S_{kd}x_i.
\end{aligned}                                                \tag{12}
\]

These are the raw normalization \(sq+r\), not the canonical
\(h\,r+sq\) normalization; no factor of \(h\) belongs in the following
power-free identity.

For the fixed outer labels \(b,d\), define

\[
 \Gamma_{bd}(K)
   =\sum_{i,k}K_{ik}
      \left(P_{ib}S_{kd}-R_{ik}Q_{bd}\right).                 \tag{13}
\]

The all-label four-cut identity, multiplied by \(K_{ik}\) and summed, is

\[
\begin{aligned}
 \sum_{i,k}K_{ik}\bigl(
   S_{kd}f_{ib}+t_kH_{ib;d}
   -Q_{bd}g_{ik}-y_bN_{ik;d}\bigr)
 ={}&\sum_{i,k}K_{ik}(P_{ib}t_k-R_{ik}y_b)v_d\\
    &+\Gamma_{bd}(K)z.                                      \tag{14}
\end{aligned}
\]

At the selected matrix unit,

\[
                         \Gamma_{bd}(E_{ac})
                           =P_{ab}S_{cd}-R_{ac}Q_{bd}
                           =\kappa.                           \tag{15}
\]

Hence the tilted line has

\[
                         \Gamma_{bd}(K(u,v))
                           =u\kappa+v\Gamma_{bd}(J),           \tag{16}
\]

a nonzero polynomial.  The tilt preserves the original source curvature as
its \(u\)-coefficient; it does not replace it by a generic reselection.
This says that the tilted line is not identically curvature-flat.  It does
not say that \(\Gamma_{bd}(K)\) is nonzero at a clean root, nor that the
tilted \(J\)-term remains in the fixed common-\((L,M)\) chart used by the
canonical two-chart lemma.

## 5. Trace-only activity and its two boundary orientations

If \(B=0\) but \(\tau=\operatorname{tr}R\ne0\), no tilt is needed.  With
\(J=I\), the canonical activity polynomial is

\[
 \begin{cases}
 \tau v^4,&a\ne c,\\
 \tau v^3(u+v),&a=c.
 \end{cases}                                                 \tag{17}
\]

In the off-diagonal case \(v=0\) is the sole inactive point; both the scalar
and all diagonal target coordinates vanish there.  In the diagonal case,
\(v=0\) is scalar-zero and unary, while \(u+v=0\) has nonzero scalar and a
weighted-binary target.  These points are not by themselves the desired
\(\Omega\)-routing; they record the trace-only orientation which a general
inactive-boundary theorem must handle.

## 6. The intrinsic zero-block boundary

Assume now

\[
                              R=A_{pr}=0.                     \tag{18}
\]

Then \(s(K)=0\) for every matrix \(K\), so no cap line on this same pair can
be active.  The nine rows (4) are direct-free:

\[
                         p_it_kq^{[h-1]}=\delta_{ik}X_i.       \tag{19}
\]

Put

\[
                         R_0=p_at_c,\qquad
                         R_I=\sum_i p_it_i.
\]

Equation (19) gives the exact polarized bridge

\[
\begin{aligned}
 R_0q^{[h-1]}&=\delta_{ac}X_a,\\
 R_Iq^{[h-1]}&=\Delta,\\
 {\cal E}_{pr}(u,v)&=(uR_0+vR_I)^{[h]}.
\end{aligned}                                                \tag{20}
\]

If \(a\ne c\), \(R_0\in\operatorname{Ann}(q^{[h-1]})\).  If \(a=c\),
\(R_0\) is a unary lift and \(R_I-R_0\) is its complementary binary lift.
This is the honest full-nine boundary in place of second-chart activity.

The selected curvature simplifies but does not disappear.  Equation (1)
forces

\[
                         \kappa=AU,\qquad A,U\ne0.             \tag{21}
\]

In the power-free overlap notation, use the selected shorthand

\[
 f=f_{ab},\quad g=g_{ac},\quad H=H_{ab;d},\quad
 N=N_{ac;d},\quad t=t_c,\quad y=y_b,\quad v=v_d,
\]

and let

\[
                         D=At,\qquad
                         C_4=Uf+tH-Fg-yN.
\]

The two overlap equations are

\[
                         ft-gy=Atz,\qquad
                         C_4=Atv+AUz.                         \tag{22}
\]

Because \(A,U\ne0\), they split triangularly:

\[
                         t=A^{-1}D,\qquad
                         z=(C_4-Dv)/(AU).                     \tag{23}
\]

This is a formal invertible triangular change in the pair \((t,z)\), not a
rank, nonvanishing, or clean-root conclusion.  It shows only that the
inactive chart retains the transition row and the common quadratic without
localization at a second activity divisor.  The pair \(rs\) also has the
nonzero direct entry \(U\), although goodness of \(rs\) is not an automatic
output.

## 7. One-sided saturation consequence and limitation

Let \(S=\mathbb C[u,v]\), let \(I_{pr}\subset S\) be the ideal generated
by the scalar coordinates of the second-chart clean error on the chosen
line, and let \(a_{pr}\) be its activity polynomial.  On the intrinsic
boundary (18), \(a_{pr}=0\).  Algebraically,

\[
                         (I_{pr}:a_{pr}^{\infty})=S,           \tag{24}
\]

because \(I_{pr}:0=S\).  A proposed conclusion

\[
 (I_{pq}:a_{pq}^{\infty})\ne S
 \quad\text{or}\quad
 (I_{pr}:a_{pr}^{\infty})\ne S
\]

therefore reduces formally to the desired one-sided \(pq\)-conclusion.
This is a fiberwise saturation tautology and gives no rank defect or
nontrivial information about the \(pq\)-ideal.  Its value is only that the
second chart need not be localized to be used as an auxiliary; equations
(14) and (19)--(23) retain its source-relative data.

This does not prove that first conclusion.  After multiplication by the
matching powers, the triangular packet undergoes the already known
cancellation.  A literal diagonal row from (19)--(20) must still survive in
the residual Macaulay quotient or the inactive-root boundary.  The theorem
removes second-chart activity from extraction; it does not supply the
missing one-sided overlap exactness.
