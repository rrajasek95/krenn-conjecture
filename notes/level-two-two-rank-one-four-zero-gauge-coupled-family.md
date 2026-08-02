# The shared gauge-coupled family reaches \(2R+4Z\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The shared four-slice gauge-coupled packet has two residual roots, \(2\)
and \(3\), with complete internal R2 witness pairs.  Activate either or both
selected matrices on one common isotropic input line:

\[
 X_i=h_i e_0^{\mathsf T}\quad(i\in A),\qquad
 X_i=0\quad(i\notin A),\qquad A\subseteq\{2,3\}.               \tag{1}
\]

With all potentials zero, each of the four active subsets satisfies every
generic-kernel and selected row, residual R2 at all six roots, and one
shared endpoint-star assignment realizing

\[
                 (T_{00},T_{01},T_{10},T_{11})
                           =(e_{0^6},0,0,e_{1^6}).              \tag{2}
\]

The residual differential ranks are

\[
                         \operatorname{rank}D=38,\qquad
                         \operatorname{rank}D_{\rm mixed}=36.  \tag{3}
\]

Thus simultaneous four-slice compatibility extends through \(2R+4Z\),
not merely the \(6Z\), \(1R+5Z\), and \(1I+5Z\) patterns previously
recorded.  This remains a low-rank boundary family, not a rank-\(55\)
survivor or a closure of the \(2R+4Z\) stratum.

## Selected and R2 checks

The common input line is isotropic:

\[
                         e_0^{\mathsf T}Je_0=0.
\]

Hence the only potentially nonzero pair numerator, between sites \(2\) and
\(3\), also vanishes.  The rare/rare endpoint slice is the corresponding
zero differential tangent; the checker additionally evaluates it literally
for all four subsets.

The physical internal witnesses are

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
2&23&20\\
3&32&31.
\end{array}                                                     \tag{4}
\]

Each complementary four-site cofactor has four nonzero binary entries.
An active root uses these two witnesses; every inactive root preserves.

The standard-library checker
[verify_level_two_two_rank_one_four_zero_gauge_coupled_family.py](../computations/verify_level_two_two_rank_one_four_zero_gauge_coupled_family.py)
reruns the exact \(40\)-by-\(34\) rigidity Jacobian, all rational and
three-prime differential ranks, the four full endpoint-slice audits, and
the selected/R2 equations.  It passes normal, optimized, and isolated
Python.  The enlarged sparse deformation chart remains the same rigid
rank-\(38/36\) diagonal orbit.
