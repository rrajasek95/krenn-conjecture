# A single live nonuniform cross does not rescue the one-column boundary

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Consider the rank-\(55\), kernel-equals-gauges \(3I+1R+2Z\) branch with
\(P_t=0,\ Q_t\ne0\). Suppose exactly one \(t\)-to-zero block
\(B=M_{tz}\) is nonzero, the other zero \(w\) is endpoint-inactive with
\(M_{tw}=0\), and \(z\) has active P/V data

\[
 U_z^s=0,\qquad V_z^s=f_sv_z,\qquad
 M_{iz}=m_iP_iv_z^{\mathsf T}\quad(i\in I).          \tag{1}
\]

The three nonzero multiples \(m_i\) are assumed not all equal. This note
closes that subcase without terminal complementary-purity or R2
hypotheses. It also closes the opposite active Q/U type at the same
\(P_t=0\) boundary. The symmetric statements with \(Q_t=0\) follow after
interchanging the selected families.

## Mixed localization separates the two exceptional tangents

L1 alignment on \(I\sqcup\{t\}\) gives

\[
 U_i^s=a_sP_i,\quad V_i^s=b_sQ_i,\qquad
 U_t^s=0,\quad V_t^s=d_sQ_t.
\]

Let \(S_t\) have blocks \(P_iQ_t^{\mathsf T}\) on the three \(it\)
edges, let \(S_z\) have blocks \(P_iv_z^{\mathsf T}\) on the three \(iz\)
edges, and let \(T\) be supported only at \(tz\), with \(T_{tz}=B\).
Since \(B\) is the only live \(tZ\) block,

\[
                    S_t=2\tau G(e_t)-2\tau T.       \tag{2}
\]

After removing the aligned core gauge and (2), the \((s,u)\) endpoint
packet is, modulo generalized gauges,

\[
              a_s\bigl(f_uS_z-c_uT\bigr),\qquad
              c_u=2\tau(d_u-b_u).                   \tag{3}
\]

No nonzero combination \(qS_z+rT\) is a generalized gauge. Indeed, the
invertible \(I\)-triangle and the nonzero \(I\)-to-\(t\) blocks first kill
the gauge weights at \(I\sqcup\{t\}\). The three \(I\)-to-\(z\) blocks
then give

\[
                         q=\lambda_zm_i\quad(i\in I).             \tag{4}
\]

For two indices \(i,j\), the exact localized identity

\[
 m_j(\lambda_zm_i-q)-m_i(\lambda_zm_j-q)
                         =q(m_i-m_j)                              \tag{5}
\]

forces \(q=\lambda_z=0\) because the multiples are nonzero and
nonuniform. The live \(tz\) block then forces \(r=0\).

The two mixed target-zero slices therefore impose

\[
 a_0f_1=a_0c_1=a_1f_0=a_1c_0=0.                  \tag{6}
\]

Nongauge pure corrections can occur in at most one colour \(k\). If no
pure correction remains, both pure targets are collinear with
\(H=\Psi(M)\), which is impossible. Otherwise, for \(s=1-k\), the
correction-free pure slice gives

\[
                         H=h\,e_s^{\otimes6},\qquad h\ne0.        \tag{7}
\]

## The pair-shore equations leave one exact cofactor pattern

Put

\[
 X=B,\qquad Y=Q_t\otimes v_z.
\]

Across the physical shore \(\{t,z\}\mid(I\sqcup\{w\})\), the matching
and derivative tensors have the exact forms

\[
 H=X\otimes C+Y\otimes K,\qquad
 d\Psi_M(T)=X\otimes C,\qquad
 d\Psi_M(S_z)=Y\otimes L.                           \tag{8}
\]

There are three matchings in the first class, six in the second, and six
dead matchings using \(tw\) or \(zw=M_{45}\); the selected zero-zero
equation forces \(M_{45}=0\). For \(d\Psi(S_z)\), six of the nine
tangent-cofactor terms survive and all share \(Y\); the other three use
\(tw\).

If \(X,Y\) are dependent, (7), (8), and the other pure equation have one
common left-shore factor, so they cannot produce the complementary pure
pair words \(e_s^{\otimes2}\) and \(e_k^{\otimes2}\). Suppose they are
independent. Here \(C\ne0\): otherwise (7) makes \(Y\) the
\(e_s^{\otimes2}\) factor, and every term in the other pure equation again
has that same left factor. Rank one in (7) now forces \(C,K\) to be
dependent. The other pure equation then puts \(e_k^{\otimes2}\) in

\[
              \operatorname{span}\{e_s^{\otimes2},Y\}.
\]

The only decomposable tensors in the diagonal pair plane
\(\operatorname{span}\{e_0^{\otimes2},e_1^{\otimes2}\}\) are its two
generators. Independence excludes \(Y\parallel e_s^{\otimes2}\), hence

\[
 Q_t\parallel e_k,\qquad v_z\parallel e_k,\qquad
 C=\gamma e_s^{\otimes4}.                            \tag{9}
\]

Comparing the two left-shore coefficients in the remaining pure equation
also shows that the \(S_z\) coefficient is nonzero and

\[
 L=\alpha e_k^{\otimes4}+\beta e_s^{\otimes4},
                         \qquad\alpha\ne0.           \tag{10}
\]

This retains the possible \(e_s^{\otimes4}\) contamination in \(L\); no
unsupported claim that \(L\) itself is pure is used.

## Selected-basis support contradicts the cofactor pattern

Use the selected bases \((P_i,Q_i)\) at \(i\in I\), writing
\(P_i=e_0,Q_i=e_1\) only in these local coordinates. This does not
identify them with the physical GHZ axes. Let \(W_i=M_{iw}\), and
suppress common nonzero scalars. The two four-site cofactors in (8) are

\[
\begin{aligned}
 C&=\sum_{\{i,j,\ell\}=I}J_{ij}\otimes W_\ell,\\
 L&=2\sum_{\{i,j,\ell\}=I}
             (e_0)_i(e_0)_j\otimes W_\ell,
 \qquad J=e_0e_1^{\mathsf T}+e_1e_0^{\mathsf T}.    \tag{11}
\end{aligned}
\]

Choose a covector at \(w\) that kills physical \(e_s\) but not physical
\(e_k\). By (10), the projected \(L\) is a nonzero product of the three
local-coordinate vectors \(x_i\) representing physical \(e_k\). But the
second line of (11) has no word containing two or more selected
\(Q\)-coordinates. Hence at most one \(x_i\) has a nonzero \(Q_i\)
coordinate.

If none does, physical \(e_k\parallel P_i\) at all three inner sites, so
the opposite physical vectors representing \(e_s\) all have nonzero
\(Q_i\) coordinates. The first line of (11) has zero all-\(Q\)
coefficient, contradicting \(C=\gamma e_s^{\otimes4}\).

Otherwise let \(\ell\) be the unique exceptional site and \(i,j\) the
other two. The all-\(Q\) coefficient of \(C\) forces the \(Q_\ell\)
coordinate of physical \(e_s\) to vanish. From the projected \(L\)
coefficients at words having one \(Q\),

\[
 \phi(W_i(Q_i))=\phi(W_j(Q_j))=0,
 \qquad\phi(W_\ell(Q_\ell))\ne0.                    \tag{12}
\]

At the word \(P_iQ_jQ_\ell\), (11) gives

\[
 \phi\bigl(C_{P_iQ_jQ_\ell}\bigr)
 =\phi(W_\ell(Q_\ell))+\phi(W_j(Q_j))\ne0.          \tag{13}
\]

Yet its pure value from (9) is zero because the \(Q_\ell\) coordinate of
physical \(e_s\) vanishes. This contradiction closes the nonuniform P/V
chart.

## Opposite active type

Still assume \(P_t=0,\ Q_t\ne0\), but put active Q/U data at \(z\):

\[
 V_z^s=0,\quad U_z^s=f_su_z,\quad
 M_{iz}=m_iQ_iu_z^{\mathsf T}.
\]

For any colour with \(f_s\ne0\), the \(tz\) L1 equation says that the
nonzero matrix \(Q_tu_z^{\mathsf T}\) is proportional to the live block
\(B\). Thus every nonzero matching term shares the physical pair factor
\(Q_t\otimes u_z\): a term either uses \(tz\), or pairs \(t,z\) to two
inner sites. The exceptional \(t\)-star and the Q/U zero-star derivatives
share it as well. Consequently the right side of each pure L0 equation
has that same pair factor. The two nonzero targets have pair factors
\(e_0^{\otimes2}\) and \(e_1^{\otimes2}\), an immediate contradiction.
This argument does not require the Q/U spoke multiples to be nonuniform.

The standard-library checker
[verify_level_two_three_invertible_one_column_single_live_nonuniform_cross_closure.py](../computations/verify_level_two_three_invertible_one_column_single_live_nonuniform_cross_closure.py)
audits the exceptional radial identity, exact mixed localization,
zero-pattern census, complete matching and derivative decompositions,
pair-shore reduction, every selected-basis cofactor support identity, and
the opposite-type shared-shore obstruction.
