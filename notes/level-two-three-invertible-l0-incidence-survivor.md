# A three-invertible packet survives the linear L0 incidence screen

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

The displayed \(3I+1R+2Z\) R2 guard has an exact one-scalar
specialization on its zero-multiplier cut for which

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mixed}=53,
\]

and both pure targets \(e_{0^6},e_{1^6}\) lie in
\(\operatorname{im}D\). Consequently, the necessary linear L0
tangent-incidence condition does not exclude this three-invertible normal
form. This is not a factored L0 completion, and L1 or overlapping
level-two equations are not asserted.

Keep every block of
[the three-invertible R2 guard](level-two-three-invertible-r2-guard.md)
except

\[
 M_{34}=\begin{pmatrix}12&0\\2&0\end{pmatrix}.
\]

Replace it by

\[
 M_{34}=\begin{pmatrix}12&0\\0&0\end{pmatrix}.                 \tag{1}
\]

Thus only \(M_{34}(1,0)\) changes, from \(2\) to \(0\). The edge \(34\)
lies in the zero-multiplier cut: \(\rho_3+\rho_4=0\), while \(X_4=0\).
Hence (1) preserves all 60 scalar generic-kernel identities and, by the
same exact Euler calculation, all 64 selected level-two rows. Its nonzero
entry \(M_{34}(0,0)=12\) still gives the planned pure-zero R2 exit at root
\(3\); every other literal R2 witness is unchanged.

The exact rank certificate is

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

The standard-library checker
[verify_level_two_three_invertible_l0_incidence_survivor.py](../computations/verify_level_two_three_invertible_l0_incidence_survivor.py)
audits the one-cell scope, the zero multiplier, the generic-kernel and
selected-L2 equations, exact differential rank and five-dimensional gauge
kernel, all six literal R2 witness tables, Euler's identity, the universal
256 formal L0 slices, and the five incidence ranks above. It passes normal,
optimized, and isolated Python.
