# Arbitrary \(M_{05},M_{14}\) changes do not escape the repaired coupled obstruction

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let \(M(A,B)\) agree with the repaired rank-\(55\) packet \(M^\dagger\)
away from two edges and put

\[
                         M_{05}=A,\qquad M_{14}=B,
 \qquad A,B\in\operatorname{Mat}_{2\times2}.
                                                               \tag{1}
\]

The entries of \(A\) and \(B\) are allowed to vary independently. For
every specialization of this eight-dimensional affine family which has
differential rank \(55\) and the required residual R2 conditions, the
actual vertex-sum-coupled shared-factor system is inconsistent. Thus no
rank-\(55\)/R2 point in the entire two-block family evades the repaired
shared-factor obstruction. In fact, after rank \(55\) is imposed, the
algebraic obstruction does not need the R2 hypothesis; R2 only identifies
the intended residual stratum.

This is an exact characteristic-zero statement, not a finite-grid
extrapolation. The eight block entries are adjoined as polynomial
variables, and the resulting universal ideal is the unit ideal over
\(\mathbb Q\). An independently reversed computation is also the unit
ideal over \(\mathbb F_{32003}\).

## Why the vertex sums are necessary

On the full \(K_4=\{0,1,4,5\}\), the four fixed blocks are

\[
\begin{aligned}
M_{01}&=\begin{pmatrix}2&3\\4&6\end{pmatrix},&
M_{04}&=\begin{pmatrix}0&0\\1&0\end{pmatrix},\\
M_{15}&=\begin{pmatrix}0&0\\1&0\end{pmatrix},&
M_{45}&=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
\end{aligned}                                                   \tag{2}
\]

The five universal gauge tangents are independent throughout (1), not
merely at a sampled point. In the basis
\(\mu_i=e_i-e_5\), \(0\leq i<5\), the five fixed tangent cells

\[
 01(0,0),\quad02(1,1),\quad03(0,0),\quad04(1,0),\quad12(0,0)
\]

give the parameter-free minor

\[
\begin{pmatrix}
2&1&1&1&0\\
2&0&0&0&-2\\
0&1&0&0&-2\\
0&0&1&0&0\\
0&0&0&1&0
\end{pmatrix},
\qquad\det=8.                                                   \tag{3}
\]

Consequently, whenever \(\operatorname{rank}d\Psi_{M(A,B)}=55\), its
kernel is exactly the five-dimensional gauge kernel.

For endpoint slice \(st\), write \(N^{st}\) for the shared-star tangent,
\(R^{st}\) for the desired localized residual tangent, and \(w_{st}\) for
the direct endpoint coefficient. Euler's cubic identity

\[
                         d\Psi_M(M)=3\Psi(M)                   \tag{4}
\]

turns

\[
 w_{st}\Psi(M)+d\Psi_M(N^{st})=d\Psi_M(R^{st})                 \tag{5}
\]

into

\[
 N_{ru}^{st}=R_{ru}^{st}
       +(\alpha_r^{st}+\alpha_u^{st})M_{ru}.                   \tag{6}
\]

Here the direct coefficient has been absorbed by
\(\alpha_r^{st}=\mu_r^{st}-w_{st}/6\). Equation (6) is therefore a
necessary condition for a shared completion at every rank-\(55\) member
of (1). Independent edge scalars would be a relaxation and are not used
in this computation.

## The universal full-\(K_4\) ideal

For \(r,u\in\{0,1,4,5\}\), \(s,t,a,b\in\{0,1\}\), impose on all six edges

\[
 U_r^s(a)V_u^t(b)+V_r^t(a)U_u^s(b)
 =R_{ru}^{st}(a,b)
  +(\alpha_r^{st}+\alpha_u^{st})M_{ru}(a,b).                  \tag{7}
\]

The source \(R^{00}\) is supported at \(01(0,0)\), \(R^{11}\) is
supported at \(45(1,1)\), and \(R^{01}=R^{10}=0\). There are

\[
 32\text{ star variables}+16\text{ vertex variables}
 +8\text{ block parameters}=56\text{ variables}
\]

and \(4\cdot6\cdot4=96\) quadrics. If \(I_{\mathrm{univ}}\) is the ideal
of these quadrics, exact degree-reverse-lexicographic Gröbner computation
gives

\[
 \operatorname{slimgb}(I_{\mathrm{univ}})=(1)
 \quad\text{over }\mathbb Q,
 \qquad
 \operatorname{slimgb}(I_{\mathrm{univ}}^{\mathrm{rev}})=(1)
 \quad\text{over }\mathbb F_{32003}.                          \tag{8}
\]

Because the eight entries in (1) are variables in the same polynomial
ring, (8) rules out every joint specialization; it does not merely show
that the generic fiber is empty.

The canonical equation-ledger SHA-256 is

    982ac7f8c1cc1363ae3e41a4a288612d7c21a6d40f970077c1abf963cb4e07db

The exact program hashes are

    Q                 8c5e226c2e56409cbf1d8243730b84b830c1ed44032b9f38d84bd6dfa58cb888
    F32003 reversed   ba8d5450440cca5c28ea6c40e0fe355a3c0f341d50c0bc683ad0d05208fbcfc6

## Nonvacuity and scope

The original repaired point

\[
 A=\begin{pmatrix}6&7\\13&9\end{pmatrix},\qquad
 B=\begin{pmatrix}6&8\\12&11\end{pmatrix}                    \tag{9}
\]

lies in (1). It has exact differential ranks \(55/53\), both separate
factored pure faces, and complete residual R2 witness pairs at all six
roots. Thus the rank-\(55\)/R2 locus being obstructed is nonempty.

The checker
[verify_level_two_repaired_arbitrary_pair_coupled_obstruction.py](../computations/verify_level_two_repaired_arbitrary_pair_coupled_obstruction.py)
regenerates the 56 variables, 96 quadrics, fixed gauge minor, base-point
rank/pure/R2 audit, both exact unit bases, and all ledgers. Python uses only
the standard library; Singular is the sole external executable.

The conclusion closes the full affine \((M_{05},M_{14})\) family with all
other residual blocks fixed at \(M^\dagger\). It does not close arbitrary
deformations of the other thirteen residual blocks or the full \(6R\)
stratum.
