# Equal invertible potentials close the remaining \(2I+4Z\) stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site packet satisfy

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix},       \tag{1}
\]

residual R2, and endpoint ranks

\[
                              (2,2,0,0,0,0).           \tag{2}
\]

If the two invertible sites have equal potentials, then

\[
                         \operatorname{rank}d\Psi_M\le48.         \tag{3}
\]

Together with the
[separated-potential bound](level-two-two-invertible-four-zero-potential-separation.md),
which gives rank at most 28, this closes the full \(2I+4Z\)
generic-kernel/R2 endpoint-rank stratum. No L0 or L1 equation is needed.

## The common witness set

Call the invertible sites \(0,1\) and write

\[
                              \nu_0=\nu_1=\alpha.
\]

The numerator \(X_0JX_1^{\mathsf T}\) is invertible, so
\(2\alpha\ne0\) and \(M_{01}\) is invertible. At either invertible root,
R2 requires two distinct internal pure-column witnesses. They must lie
among the four zero endpoint sites. As in the separated-potential theorem,
a nonzero block from an invertible site to a zero endpoint requires the
zero potential to be \(-\alpha\). Hence the common set

\[
                         A=\{z:\nu_z=-\alpha\}          \tag{4}
\]

has size at least two. Put \(C=Z\setminus A\).

The generic-kernel equation gives the following support envelope:

* \(M_{01}\) and every block from \(\{0,1\}\) to \(A\) may be nonzero;
* every block internal to \(A\), and every block from \(\{0,1\}\) to
  \(C\), vanishes;
* a vertex \(c\in C\) can meet all of \(A\) only when \(\nu_c=\alpha\);
* an edge \(cd\subset C\) can be nonzero only when
  \(\nu_c+\nu_d=0\).

The last two exceptions cannot meet at one vertex: if
\(\nu_c=\alpha\) and \(\nu_c+\nu_d=0\), then
\(\nu_d=-\alpha\), contrary to \(d\in C\).

## Exact support census

Only the size of \(A\) and the two exceptions above matter.

If \(|A|=4\), there is one envelope. Exactly the six edges internal to
\(A\) have potentially nonzero complementary cofactors, so

\[
                         \operatorname{rank}d\Psi_M\le24.         \tag{5}
\]

If \(|A|=3\), the sole vertex in \(C\) either has no live base edge or is
joined to all three vertices of \(A\). The corresponding cofactor-edge
counts are 3 and 12, giving bounds 12 and 48.

If \(|A|=2\), the two vertices in \(C\) have four possible envelopes:
neither is joined to \(A\), exactly one is joined, both are joined, or
their mutual edge is live. The mutual-edge case cannot coexist with an
\(A\)-join. The cofactor-edge counts are respectively

\[
                              1,\quad5,\quad10,\quad6,             \tag{6}
\]

and the resulting rank bounds are \(4,20,40,24\).

In every case the count is exact at the support level: a differential cell
column on a varied edge is zero unless the four complementary vertices
have a perfect matching in the base support envelope. Four cells per
active edge give the displayed bounds. Their maximum is 48, proving (3).

The standard-library checker
[verify_level_two_two_invertible_four_zero_equal_potential_closure.py](../computations/verify_level_two_two_invertible_four_zero_equal_potential_closure.py)
enumerates all seven support envelopes, all complementary perfect
matchings, and the cofactor-edge counts \(6;3,12;1,5,10,6\). It passes
normal, optimized, and isolated Python.
