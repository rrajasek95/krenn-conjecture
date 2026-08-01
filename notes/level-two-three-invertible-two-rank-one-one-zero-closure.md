# Closure of the three-invertible, two-rank-one, one-zero stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

Let a binary six-site packet satisfy

\[
 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.             \tag{1}
\]

Suppose exactly three endpoint matrices \(X_i\), \(i\in I\), are
invertible, two matrices \(X_r,X_s\) are nonzero of rank one, and
\(X_z=0\).

> **Theorem.**
> \[
>                         \operatorname{rank}d\Psi_M\le54.          \tag{2}
> \]

Thus this entire generic-kernel rank pattern is incompatible with residual
differential rank 55. No R2 assumption is needed. The adjacent pattern with
one nonzero rank-one matrix and two zero matrices is not covered.

Write

\[
 X_r=a_rb_r^{\mathsf T},\qquad X_s=a_sb_s^{\mathsf T},
\]

and make local output changes of basis sending \(a_r,a_s\) to \(e_0\).
Every \(I\)-\(\{r,s\}\) block is then supported only at colour zero at its
rank-one endpoint.

## 2. The aligned rank-one edge

First suppose \(\nu_r+\nu_s\ne0\). Equation (1) makes
\(M_{rs}\) a scalar multiple of \(e_0e_0^{\mathsf T}\). Enlarge the packet
class by allowing all five blocks incident with \(z\) to be arbitrary.

Split output words into the two colours at \(r,s\), the colour at \(z\),
and the three colours on \(I\). Classifying a perfect matching by the
partner of \(z\) gives

\[
 \Psi(M)=e_{00}\otimes F
 +(M_{rz}\otimes e_0)\otimes h_s
 +(e_0\otimes M_{sz})\otimes h_r,                    \tag{3}
\]

where \(F\in\mathbb C^{16}\) and \(h_r,h_s\in\mathbb C^8\).

The enlarged support-preserving space has dimension

\[
 12\ (I\text{-}I)+12\ (I\text{-}\{r,s\})
 +1\ (rs)+20\ (z\text{-star})=45.                    \tag{4}
\]

The first term of (3) contributes at most 16 tangent dimensions. Each
remaining Segre tangent has dimension at most \(4+8-1=11\). When its
eight-vector is nonzero, it meets
\(e_{00}\otimes\mathbb C^{16}\) in at least the two-dimensional space
obtained by fixing its rank-one endpoint to colour zero. When that vector
vanishes, the Segre tangent itself has dimension at most eight. It therefore
adds at most nine dimensions in every case. The restricted tangent rank is
at most
\(16+9+9=34\). The other \(60-45=15\) cell directions give

\[
                         \operatorname{rank}d\Psi_M\le34+15=49.    \tag{5}
\]

This support bound is sharp.

## 3. The exceptional rank-one edge

Now suppose \(\nu_r+\nu_s=0\). Equation (1) forces
\(b_r^{\mathsf T}Jb_s=0\), so \(b_r,b_s\) are proportional, while
\(M_{rs}\) is arbitrary.

Put

\[
 F_z=\{v\ne z:\nu_v+\nu_z=0\}.                        \tag{6}
\]

Every edge from \(z\) outside \(F_z\) is zero; edges from \(z\) into
\(F_z\) are free. Crucially,

\[
                         F_z\subseteq I
 \quad\hbox{or}\quad F_z\subseteq\{r,s\}.              \tag{7}
\]

Indeed, if \(i\in I\) and \(r\in F_z\), then
\(\nu_i=\nu_r=-\nu_z\). Since \(\nu_s=-\nu_r=\nu_z\), one gets
\(\nu_i+\nu_s=0\), contradicting the nonzero numerator
\(X_iJX_s^{\mathsf T}\).

If \(F_z\subseteq I\), enlarge the class by allowing all three
\(I\)-\(z\) blocks to be arbitrary. Matching expansion gives

\[
                         \Psi(M)=M_{rs}\otimes F+e_{00}\otimes G,  \tag{8}
\]

with \(F,G\in\mathbb C^{16}\). The support-preserving parameter space has
dimension \(12+12+4+12=40\). The Segre tangent in (8) has dimension at most
\(4+16-1=19\). When \(F\ne0\), it meets
\(e_{00}\otimes\mathbb C^{16}\) in \(e_{00}\otimes F\); when \(F=0\),
the Segre tangent has dimension at most 16. Hence the restricted rank is
at most 34 in either case. Adding the twenty transverse directions proves

\[
                         \operatorname{rank}d\Psi_M\le54.          \tag{9}
\]

If \(F_z\subseteq\{r,s\}\), enlarge by allowing both \(rz,sz\) blocks.
The matching tensor is just the sum of the last two Segre terms in (3).
Their tangent rank is at most \(11+11=22\). The enlarged support has
dimension \(12+12+4+8=36\), leaving 24 transverse directions, so

\[
                         \operatorname{rank}d\Psi_M\le22+24=46.    \tag{10}
\]

Bounds (5), (9), and (10) prove the theorem.

## 4. Exact audit

[verify_level_two_three_invertible_two_rank_one_one_zero_closure.py](../computations/verify_level_two_three_invertible_two_rank_one_one_zero_closure.py)
checks all three matching decompositions as formal polynomial identities,
audits the exceptional multiplier separation (7), and verifies exact
calibration ranks \(49,50,46\) modulo two primes for the aligned,
\(F_z\subseteq I\), and \(F_z\subseteq\{r,s\}\) support classes. It passes
normal, optimized, and isolated Python.
