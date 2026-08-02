# A two-invertible packet survives the linear L0 incidence screen

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

There is an exact replacement of the 32 scalar entries on the eight
zero-multiplier blocks of the displayed \(2I+2R+2Z\) guard such that

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mixed}=53,
\]

and both pure targets \(e_{0^6},e_{1^6}\) lie in
\(\operatorname{im}D\).  In exact ranks,

\[
\begin{array}{c|c}
\text{matrix}&\operatorname{rank}
   \text{ over }\mathbb Q,\mathbb F_{101},
   \mathbb F_{32003},\mathbb F_{1000003}\\ \hline
D&(55,55,55,55)\\
D_{\rm mixed}&(53,53,53,53)\\
[D\mid e_{0^6}]&(55,55,55,55)\\
[D\mid e_{1^6}]&(55,55,55,55)\\
[D\mid e_{0^6}\mid e_{1^6}]&(55,55,55,55).
\end{array}
\]

Thus the necessary linear L0 tangent-incidence condition does not exclude
the two-invertible normal form.  This is not yet a factored L0 completion,
and L1 or overlapping level-two equations are not asserted.

Keep the endpoint matrices, multipliers, and seven determined blocks from
[the two-invertible R2 guard](level-two-two-invertible-r2-guard.md).  On the
eight zero-multiplier blocks use

\[
\begin{array}{c|c@{\qquad}c|c}
04&\begin{pmatrix}0&85\\0&87\end{pmatrix}&
05&\begin{pmatrix}84&87\\0&28\end{pmatrix}\\[6pt]
14&\begin{pmatrix}0&74\\0&66\end{pmatrix}&
15&\begin{pmatrix}0&76\\37&0\end{pmatrix}\\[6pt]
24&\begin{pmatrix}0&46\\0&23\end{pmatrix}&
25&\begin{pmatrix}56&0\\0&0\end{pmatrix}\\[6pt]
34&\begin{pmatrix}0&3\\29&0\end{pmatrix}&
35&\begin{pmatrix}0&51\\0&96\end{pmatrix}.
\end{array}
\]

Changing only zero-multiplier blocks preserves all 60 scalar
generic-kernel identities and all 64 selected level-two rows.  The exact
differential rank remains 55; its nullity is five and the five independent
vertex gauges span the kernel.  The pure-column-one blocks
\(04,14,24,35\), together with the original pure-column-zero witnesses,
also retain literal R2 exits at all six residual roots.

The candidate was located by finite-field search over the 32 free scalar
entries and then audited independently over the rationals and three finite
fields.  The standard-library checker
[verify_level_two_two_invertible_l0_incidence_survivor.py](../computations/verify_level_two_two_invertible_l0_incidence_survivor.py)
also verifies the universal 256 formal L0 slices, Euler's identity, the
unchanged-block scope, selected L2, the exact gauge kernel, and all R2
witness tables.
