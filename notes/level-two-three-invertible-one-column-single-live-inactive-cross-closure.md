# A single live inactive zero cross does not rescue the one-column boundary

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Work in the rank-\(55\), kernel-equals-gauges \(3I+1R+2Z\) branch with
\(P_t=0,\ Q_t\ne0\). Suppose both zero sites are endpoint-inactive,
exactly one block

\[
                         B=M_{tz}\ne0
\]

is live on the \(t\)-to-\(Z\) star, and \(M_{tw}=0\) at the other zero.
Then no L1/L0 completion exists, for arbitrary \(I\)-to-\(z\) spokes. In
particular, those spokes may be unrelated singular blocks; no common-factor
normal form is required.

This is a pre-terminal physical-flattening closure. It uses neither the
terminal complementary-purity conditions nor a normalized R2 coordinate
claim. The symmetric \(Q_t=0,\ P_t\ne0\) case follows by interchanging the
selected families. Active zero endpoints and two live \(tZ\) blocks remain
outside this note.

## Reduction to the literal live edge

L1 alignment on the invertible triangle gives

\[
 U_i^s=a_sP_i,\quad V_i^s=b_sQ_i,\qquad
 U_t^s=0,\quad V_t^s=d_sQ_t.
\]

Let \((S_t)_{it}=P_iQ_t^{\mathsf T}=2\tau M_{it}\), and let \(T\) be the
tangent supported only on \(tz\), with \(T_{tz}=B\). Since \(M_{tw}=0\),

\[
                         S_t=2\tau G(e_t)-2\tau T.    \tag{1}
\]

Thus, modulo generalized gauges, every endpoint slice has only the
correction

\[
                         -2\tau a_s(d_u-b_u)T.        \tag{2}
\]

There are two spoke cases at \(z\).

* If every \(M_{iz}\) vanishes, \(T=G(e_z)\) because \(tz\) is the only
  live edge incident with \(z\). Every endpoint slice is then a generalized
  gauge, and the two pure targets contradict collinearity with
  \(H=\Psi(M)\).
* If at least one \(M_{iz}\) is nonzero, no nonzero multiple of \(T\) is a
  generalized gauge. The invertible \(I\)-triangle and nonzero \(I\)-to-\(t\)
  blocks kill the weights at \(I,t\); the nonzero \(I\)-to-\(z\) block
  kills the weight at \(z\); and the live \(tz\) block kills the tangent
  coefficient.

In the second case, the mixed target-zero slices force

\[
                 a_0(d_1-b_1)=a_1(d_0-b_0)=0.        \tag{3}
\]

If both pure correction coefficients vanish, pure collinearity again
closes the branch. The only remaining scalar charts have a colour \(s\)
with

\[
 a_s=0,\quad d_s=b_s,\qquad
 a_k\ne0,\quad d_k\ne b_k,\qquad k=1-s.              \tag{4}
\]

The \(ss\) equation then forces

\[
                         H=h\,e_s^{\otimes6},\qquad h\ne0.       \tag{5}
\]

## Two physical flattenings are incompatible

The differential of the live-edge tangent is

\[
                         d\Psi_M(T)=B\otimes C,        \tag{6}
\]

where \(C\) is the four-site matching tensor on \(I\sqcup\{w\}\). The
pure-\(k\) equation has the form

\[
                 e_k^{\otimes6}=\kappa H+q\,B\otimes C,
                 \qquad q\ne0.                       \tag{7}
\]

Across \(\{t,z\}\mid(I\sqcup\{w\})\), the correction has rank one. Its
physical pure \(2\times2\) minor forces \(\kappa=0\), and singleton support
then gives

\[
                         B=\beta E_{kk},\qquad
                         C=\gamma e_k^{\otimes4},\qquad
                         q\beta\gamma=1.              \tag{8}
\]

Now expand the full residual matching tensor. Three matchings use \(tz\)
and sum to \(B\otimes C\). Six matchings pair \(t,z,w\) to the three
vertices of \(I\). Every one contains an \(I\)-to-\(t\) block and therefore
shares the physical \(Q_t\) factor at \(t\); the arbitrary \(I\)-to-\(z\)
blocks impose no factor condition. The remaining six matchings contain
the dead edge \(tw\) or \(zw=M_{45}\). Hence, for a five-site tensor \(K\),

\[
                         H=B\otimes C+Q_t\otimes K.   \tag{9}
\]

Combining (5), (8), and (9) gives

\[
 Q_t\otimes K=h\,e_s^{\otimes6}
                   -\beta\gamma e_k^{\otimes6}.      \tag{10}
\]

The left side has rank at most one across
\(t\mid(R\setminus\{t\})\). The right side has rank two: its physical pure
\(2\times2\) minor is, up to sign, \(h\beta\gamma\ne0\). This contradiction
closes the chart without any condition on the singular \(I\)-to-\(z\)
spokes beyond the zero/nonzero split above.

The standard-library checker
[verify_level_two_three_invertible_one_column_single_live_inactive_cross_closure.py](../computations/verify_level_two_three_invertible_one_column_single_live_inactive_cross_closure.py)
audits the exceptional-star reduction on all fifteen edges, the radial and
nonradial spoke cases, all scalar zero patterns, both exact physical
flattening minors, and the complete \(3+6+6\) matching decomposition.
