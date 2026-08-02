# Separated invertible potentials close a \(2I+4Z\) stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.       \tag{1}
\]

Suppose the endpoint ranks are

\[
                              (2,2,0,0,0,0),           \tag{2}
\]

and impose residual R2 at the two invertible endpoint sites. If their
potentials are distinct, then

\[
                         \operatorname{rank}d\Psi_M\le28.         \tag{3}
\]

Thus this whole subcase misses differential rank 55. The result uses no L0
or L1 equation. Its only unresolved multiplier boundary is equality of the
two invertible-site potentials.

## R2 partitions the four zero sites

Call the invertible sites \(0,1\) and the zero endpoint sites \(Z\). The
numerator on edge \(01\) is invertible. Hence

\[
                         \nu_0+\nu_1\ne0,\qquad M_{01}\text{ invertible}.
                                                               \tag{4}
\]

At an invertible endpoint site both selected endpoint stars are nonzero.
R2 therefore requires two distinct internal pure-column witnesses. The
edge \(01\) cannot be one because it is invertible, so both witnesses lie
in \(Z\). A nonzero block \(M_{iz}\), with \(X_z=0\), can satisfy (1) only
when

\[
                              \nu_z=-\nu_i.             \tag{5}
\]

Consequently each of the sets

\[
 A=\{z\in Z:\nu_z=-\nu_0\},\qquad
 B=\{z\in Z:\nu_z=-\nu_1\}                              \tag{6}
\]

has at least two elements. If \(\nu_0\ne\nu_1\), the sets are disjoint.
Since \(|Z|=4\), they partition \(Z\) into two pairs.

## Three support envelopes

Equation (1) now forces every block outside the following envelope to
vanish:

* \(M_{01}\), the two blocks from \(0\) to \(A\), and the two blocks
  from \(1\) to \(B\) may be nonzero;
* every \(A\)-to-\(B\), \(0\)-to-\(B\), and \(1\)-to-\(A\) block is zero;
* the single \(A\)-internal block may be nonzero only if \(\nu_0=0\);
* the single \(B\)-internal block may be nonzero only if \(\nu_1=0\).

The first cross-shore assertion uses

\[
 \nu_a+\nu_b=-(\nu_0+\nu_1)\ne0
 \qquad(a\in A,b\in B),                                \tag{7}
\]

and the two wrong-core assertions use \(\nu_0-\nu_1\ne0\). By (4), at
most one of \(\nu_0,\nu_1\) vanishes. There are therefore only three
support envelopes: neither pair-internal edge, the \(A\)-edge, or the
\(B\)-edge.

## Cofactor support bounds the differential

A cell column of \(d\Psi_M\) obtained by varying edge \(e\) is zero unless
the support envelope on the four complementary vertices has a perfect
matching. This gives an exact, basis-free count.

If both invertible potentials are nonzero, only the four \(A\)-to-\(B\)
variation edges have a potentially nonzero cofactor. Their four cells give

\[
                         \operatorname{rank}d\Psi_M\le4\cdot4=16. \tag{8}
\]

If \(\nu_0=0\), the potentially nonzero cofactor edges are the four
\(A\)-to-\(B\) edges, the two \(0\)-to-\(B\) edges, and the \(B\)-internal
edge. There are seven edges and hence at most 28 cell columns. If
\(\nu_1=0\), interchange \(A,B\) and \(0,1\). This proves (3).

The equal-potential boundary \(\nu_0=\nu_1\ne0\) is genuinely absent from
the partition argument: the two R2 witness sets in (6) may overlap, and
the other zero sites can carry additional opposite-potential incidences.
No claim about that boundary is made here.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_four_zero_potential_separation.py](../computations/verify_level_two_two_invertible_four_zero_potential_separation.py)
enumerates every R2 witness-set partition, verifies the three exact
zero-multiplier support envelopes, exhausts all complementary perfect
matchings, and obtains the cofactor-edge counts \(4,7,7\). It passes
normal, optimized, and isolated Python.
