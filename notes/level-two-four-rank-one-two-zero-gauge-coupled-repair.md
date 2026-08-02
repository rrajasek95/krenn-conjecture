# The shared gauge-coupled family reaches \(4R+2Z\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Start from the integrated shared four-slice gauge-coupled packet and write
\(p=M_{23}(00)=2\).  Add three pure-zero cells

\[
 M_{03}(00)=a=2,\qquad M_{12}(00)=b=1,\qquad
 M_{01}(00)=c=-1.                                      \tag{1}
\]

Their only new contribution to the complementary \(0123\) matching is

\[
                 cp+ab=0.                              \tag{2}
\]

Consequently the same endpoint stars still realize the exact four slices

\[
       (T_{00},T_{01},T_{10},T_{11})
                  =(e_{0^6},0,0,e_{1^6}).               \tag{3}
\]

The repair raises the residual differential ranks from \(38/36\) to

\[
                 \operatorname{rank}D=42,\qquad
                 \operatorname{rank}D_{\rm mixed}=40.   \tag{4}
\]

More importantly, roots \(0,1,2,3\) now all have complete internal R2
witness pairs with nonzero complementary cofactors.  Thus any subset
\(A\subseteq\{0,1,2,3\}\) can be activated by

\[
 X_i=h_i e_0^{\mathsf T}\quad(i\in A),\qquad
 X_i=0\quad(i\notin A).                                 \tag{5}
\]

The common input line is isotropic, so every pair numerator is zero with
all potentials zero.  The sixteen subsets satisfy the generic-kernel
equations, the selected level-two row, literal rare/rare vanishing, and
R2 at every active root.  In particular the shared construction reaches
\(4R+2Z\) at rank \(42\).

This is still a low-rank boundary family.  It neither reaches the
rank-\(55\) target nor closes the full \(4R+2Z\) stratum.

## Exact witnesses

The checker uses

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31.
\end{array}                                               \tag{6}
\]

The complementary four-site cofactors have respectively
\(4,4,4,4,8,4,8,4\) nonzero binary entries in row order.

The standard-library checker
[verify_level_two_four_rank_one_two_zero_gauge_coupled_repair.py](../computations/verify_level_two_four_rank_one_two_zero_gauge_coupled_repair.py)
verifies the cancellation (2), the exact four differential slices, ranks
over \(\mathbb Q\) and three finite fields, all witness cofactors, and all
sixteen literal eight-site subset cases.  It is intended to run normally,
with -O, and with -I -S.
