# The one-column rank-one-site boundary reduces to two pure cofactor charts

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Retain the rank-55, kernel-equals-gauges, cross-invertible hypotheses of
[the L1/L0 cut normal form](level-two-three-invertible-l1-l0-cut-normal-form.md),
but suppose exactly one selected column at the rank-one site \(t=3\)
vanishes. The boundary is closed unless a residual \(t\)-to-\(Z\) block is
live and the endpoint scalars lie in one of two labelled one-zero charts.
On either surviving chart, the residual matching tensor and an explicit
five-site star cofactor must be complementary pure coordinate tensors.

This is a rigorous reduction. The two exceptional charts are subsequently
excluded by the
[pure-tensor shore obstruction](level-two-three-invertible-one-column-pure-tensor-obstruction.md).
The case with no invertible \(I\)-spoke at a zero site and the rank-below-55
boundary remain outside its hypotheses.

## Exceptional star after L1 alignment

It is enough to treat

\[
                         P_t=0,\qquad Q_t\ne0.
\]

The invertible triangle and zero-site spoke arguments still give

\[
\begin{aligned}
 U_i^s&=a_sP_i,&V_i^s&=b_sQ_i &&(i\in I),\\
 U_z^s&=V_z^s=0 &&&&(z\in Z),
\end{aligned}
\]

but the rank-one-site comparison now leaves

\[
                    U_t^s=0,\qquad V_t^s=d_sQ_t.     \tag{1}
\]

Define the nonzero \(t\)-star packet

\[
 (S_t)_{it}=P_iQ_t^{\mathsf T}\quad(i\in I),\qquad
 (S_t)_{ru}=0\quad\text{otherwise}.                  \tag{2}
\]

Since \(P_iQ_t^{\mathsf T}=2\tau M_{it}\), every endpoint slice is

\[
 N^{su}=a_sb_uG(\nu)+a_s(d_u-b_u)S_t.                \tag{3}
\]

If \(M_{t4}=M_{t5}=0\), then (2) is exactly
\(2\tau\) times the radial vertex gauge at \(t\). Thus every slice in (3)
is a generalized gauge, and the two pure L0 targets contradict
collinearity with \(H=\Psi(M)\). Hence any survivor must have

\[
                         (M_{t4},M_{t5})\ne(0,0).     \tag{4}
\]

## Mixed slices force the cross-products to vanish

If \(D(qS_t)\) is a scalar multiple of \(H\), Euler and
\(\ker D=\) trace-zero gauges imply that \(qS_t\) is a generalized gauge
\(G(\lambda)\). Its support makes this impossible for \(q\ne0\):

* the invertible \(I\)-triangle forces \(\lambda_i=0\) for \(i\in I\);
* one invertible \(I\)-spoke to each zero forces
  \(\lambda_4=\lambda_5=0\);
* the nonzero \(I\)-to-\(t\) blocks give \(\lambda_t=2\tau q\); and
* the live \(t\)-to-\(Z\) block in (4) forces \(\lambda_t=0\).

Applying this to the two target-zero mixed slices of (3) yields

\[
             a_0(d_1-b_1)=0,\qquad a_1(d_0-b_0)=0.  \tag{5}
\]

Put \(\delta_s=d_s-b_s\). If both \(a_s\) are nonzero, (5) gives
\(\delta_0=\delta_1=0\), returning to the closed fully aligned interior.
If both vanish, both pure slices are scalar multiples of \(H\), again
impossible. The only remaining zero patterns are

\[
\begin{array}{c|cccc}
&a_0&a_1&\delta_0&\delta_1\\ \hline
\mathcal E_0&0&\ne0&0&\ne0\\
\mathcal E_1&\ne0&0&\ne0&0.
\end{array}                                           \tag{6}
\]

## Pure slices isolate complementary coordinate tensors

Let \(s\) be the colour with \(a_s=0\), and put \(r=1-s\). The \(ss\)
slice of (3) vanishes, so its pure L0 equation forces

\[
                         H=h\,e_s^{\otimes6},\qquad h\ne0.     \tag{7}
\]

The derivative of (2) factors across \(t\):

\[
                         D(S_t)=Q_t\otimes C_t,        \tag{8}
\]

where the five-site tensor on \(I\sqcup Z\) is

\[
 C_t(x)=\sum_{i\in I}P_i(x_i)\,
   \operatorname{haf}\!\left(M_{R\setminus\{i,t\}};x\right). \tag{9}
\]

The other pure equation has the form

\[
 e_r^{\otimes6}=\kappa_rH+
      a_r\delta_r\,Q_t\otimes C_t.                   \tag{10}
\]

Across the cut \(t\mid(R\setminus\{t\})\), the right side after moving
\(\kappa_rH\) has rank two if \(\kappa_r\ne0\), while the correction in
(8) has rank at most one. Since \(h\ne0\), the pure \(2\times2\) minor
forces \(\kappa_r=0\). Equation (10) then forces

\[
 Q_t=q\,e_r,\qquad C_t=\gamma\,e_r^{\otimes5},\qquad
 a_r\delta_rq\gamma=1.                               \tag{11}
\]

Thus the only \(P_t=0\) survivors are the two charts (6), subject to the
live-star condition (4) and the exact pure tensors (7), (11).

For \(Q_t=0,\ P_t\ne0\), interchange

\[
 (P,U,a)\longleftrightarrow(Q,V,b).
\]

The same theorem holds with \(b_s\), deviations \(d_s-a_s\), selected
vector \(P_t\), and the five-site cofactor built from the \(Q_i\).

The standard-library checker
[verify_level_two_three_invertible_one_column_t_boundary.py](../computations/verify_level_two_three_invertible_one_column_t_boundary.py)
audits the formal exceptional-star identity, the full-rank live-star
support system, the zero-star radial gauge, all scalar zero patterns, the
two pure flattening minors, the five-site cofactor factorization, and the
symmetric \(P_t/Q_t\) dictionary.

The companion
[pure-tensor shore obstruction](level-two-three-invertible-one-column-pure-tensor-obstruction.md)
uses the invertible spoke at each zero site to show that (7) alone is already
impossible. Thus neither terminal chart survives; condition (11) is not
needed for the final contradiction.
