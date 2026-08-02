# A determined zero shore closes a \(2I+3R+1Z\) stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.         \tag{1}
\]

Suppose the endpoint-matrix ranks are

\[
                              (2,2,1,1,1,0).                       \tag{2}
\]

Write \(I\) for the two invertible sites, \(T\) for the three nonzero
rank-one sites, and \(z\) for the zero site. Assume

\[
                              \nu_z+\nu_t\ne0\qquad(t\in T).      \tag{3}
\]

Then

\[
                              \operatorname{rank}d\Psi_M\le51.   \tag{4}
\]

In particular this entire subcase misses differential rank 55. This is a
support-defined stratum theorem, not an obstruction to an exact packet. It
does not use L0, L1, R2, or a physical target coordinate.

The fewer-invertible frontier includes the endpoint-rank patterns
\(2I+kR+(4-k)Z\) for \(0\le k\le4\), followed by the one- and
zero-invertible strata. Existing exact guards show that the
\(2I+2R+2Z\) pattern can attain rank 55 before overlapping equations are
imposed. The theorem here treats a different adjacent pattern and isolates
its remaining boundary exactly: at least one free zero-multiplier
\(z\)-to-\(T\) block.

## Fixed factors on the rank-one shore

Write a rank-one endpoint matrix as

\[
                              X_t=a_tb_t^{\mathsf T}.              \tag{5}
\]

For \(i\in I\), the numerator in (1) is

\[
 X_iJX_t^{\mathsf T}=(X_iJb_t)a_t^{\mathsf T}.                    \tag{6}
\]

It is nonzero because \(X_i\) is invertible and \(b_t\ne0\). Hence
\(\nu_i+\nu_t\ne0\), and \(M_{it}\) has the fixed right factor
\(a_t^{\mathsf T}\) at its \(T\)-endpoint.

The zero endpoint has zero numerator on every incident edge. Assumption
(3) therefore gives

\[
                              M_{zt}=0\qquad(t\in T).              \tag{7}
\]

Finally, on an edge \(tu\subset T\),

\[
 X_tJX_u^{\mathsf T}
       =(b_t^{\mathsf T}Jb_u)a_ta_u^{\mathsf T}.                  \tag{8}
\]

If \(\nu_t+\nu_u\ne0\), equation (1) makes \(M_{tu}\) a scalar multiple
of \(a_ta_u^{\mathsf T}\). If the multiplier sum vanishes, the block is
unconstrained and is an exceptional shore edge.

Independent local changes of basis at the three sites of \(T\) send the
three nonzero vectors \(a_t\) to \(e_0\). These changes preserve
differential rank. Equations (6)--(8) now place \(M\) exactly in the
coordinate-shore support class; the blocks internal to \(I\sqcup\{z\}\)
remain arbitrary, as allowed by that theorem.

## The zero-sum graph gives four exact bounds

Let

\[
 E=\{tu\in\tbinom T2:\nu_t+\nu_u=0\}.                            \tag{9}
\]

On three vertices, \(E\) is empty, one edge, a two-edge path, or the full
triangle. The first three cases are exactly the coordinate-shore bounds

\[
\begin{array}{c|ccc}
E&\varnothing&\text{one edge}&\text{two-edge path}\\ \hline
\operatorname{rank}d\Psi_M&\le35&\le42&\le49.
\end{array}                                                       \tag{10}
\]

It remains to treat the triangle. The three equations
\(\nu_t+\nu_u=0\) have full rank, so

\[
                              \nu_t=0\qquad(t\in T).              \tag{11}
\]

They also force

\[
                              b_t^{\mathsf T}Jb_u=0
                              \qquad(t\ne u).                     \tag{12}
\]

For the symmetric binary matrix
\(J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\),
three nonzero pairwise-orthogonal vectors lie on one isotropic line. To see
this, write \(b_0=(x,y)\). Its orthogonal line is spanned by
\(k=(x,-y)\), so \(b_1=c_1k,b_2=c_2k\). The remaining pairing is

\[
                              b_1^{\mathsf T}Jb_2
                              =-2c_1c_2xy.                         \tag{13}
\]

Since \(b_1,b_2\ne0\), equation (12) gives \(xy=0\). Then \(k\) is
proportional to \(b_0\), proving that all three \(b_t\) share a line. Use
the scale freedom in (5) to absorb their proportionality constants into the
corresponding \(a_t\). The factors \(b_t\) may then be taken equal.

For fixed \(i\in I\), formula (6) is consequently independent of
\(t\in T\) after the local normalizations \(a_t=e_0\); for \(i=z\) it is
identically zero by (7). Thus the cross spokes genuinely have the constant
form

\[
                              M_{it}=u_i e_0^{\mathsf T}
                              \qquad(i\in I\sqcup\{z\},\ t\in T). \tag{14}
\]

All three shore edges may be arbitrary. The constant-cross coordinate-shore
theorem gives

\[
                              \operatorname{rank}d\Psi_M\le51,   \tag{15}
\]

which proves (4).

## Remaining boundary

The sole omitted multiplier condition is

\[
                              \nu_z+\nu_t=0
                              \quad\text{for some }t\in T.        \tag{16}
\]

Because \(X_z=0\), equation (1) is then \(0=0\cdot M_{zt}\) and leaves the
entire `2 x 2` block \(M_{zt}\) free. Such a block need not carry the fixed
factor at \(t\), so the coordinate-shore bounds do not apply. This free-edge
boundary, rather than the determined-zero-shore subcase, is the sharply
bounded unresolved target in the \(2I+3R+1Z\) pattern.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_three_rank_one_one_zero_closure.py](../computations/verify_level_two_two_invertible_three_rank_one_one_zero_closure.py)
verifies the formal rank-one numerator factorizations, the four zero-sum
graph types, the common isotropic line in the triangle case, and imports the
exact 35/42/49/51 coordinate-shore matching identities and dimension counts.
It passes normal, optimized, and isolated Python.
