# Equal invertible potentials finish the \(2I+1R+3Z\) stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix},                 \tag{1}
\]

and residual R2. Suppose the endpoint ranks are

\[
                              (2,2,1,0,0,0).                     \tag{2}
\]

Call the invertible sites \(0,1\), the nonzero rank-one site \(r=2\),
and the zero sites \(Z=\{3,4,5\}\). If

\[
                              \nu_0=\nu_1\ne\nu_r,              \tag{3}
\]

then

\[
                              \operatorname{rank}d\Psi_M\le48. \tag{4}
\]

This was the sole multiplier boundary left by the
[equal-core-potential closure](level-two-two-invertible-one-rank-one-three-zero-equal-core-potential-closure.md)
and the
[distinct-invertible-potential closure](level-two-two-invertible-one-rank-one-three-zero-distinct-invertible-potential-closure.md).
Consequently the full \(2I+1R+3Z\) generic-kernel/R2 endpoint-rank
stratum misses rank 55.

The proof uses no L0 or L1 equation. It first uses R2 in the physical
coordinates, then makes a local change of basis at the rank-one site solely
for the covariant differential-rank calculation.

## R2 gives one common attachment set

Write

\[
                              \nu_0=\nu_1=\lambda,\qquad
                              \nu_r=\gamma.                      \tag{5}
\]

The three core numerators on \(01,0r,1r\) are nonzero. Hence

\[
                              \lambda\ne0,\qquad
                              \gamma\ne-\lambda.                 \tag{6}
\]

The hypothesis (3) also gives \(\gamma\ne\lambda\). Write

\[
                              X_r=ab^{\mathsf T}.                 \tag{7}
\]

Then \(M_{01}\) is invertible and

\[
                              M_{ir}=c_i a^{\mathsf T}\ne0
                              \qquad(i=0,1).                     \tag{8}
\]

At an invertible root, the edge \(01\) is not a pure-column R2 witness.
If \(a\) is a physical coordinate vector, the edge to \(r\) supplies one
R2 witness colour. If both coordinates of \(a\) are nonzero, it supplies
none. Both invertible roots have the same zero-attachment set

\[
                              A=\{z\in Z:\nu_z=-\lambda\}.       \tag{9}
\]

Only vertices in \(A\) can carry nonzero invertible-to-zero blocks.
Therefore R2 forces

\[
 \begin{cases}
 |A|\ge1,&a\text{ is a coordinate vector},\\
 |A|\ge2,&a\text{ is noncoordinate}.
 \end{cases}                                                     \tag{10}
\]

In particular \(A\ne\varnothing\) in both branches. After extracting this
physical R2 consequence, use a local basis change at \(r\) to send
\(a\) to \(e_0\). Differential rank is unchanged, and both blocks in (8)
are now supported in shore column zero.

## The thirteen support envelopes

Every edge touching a zero endpoint has zero numerator in (1). Its entire
binary block is therefore arbitrary exactly at zero multiplier sum and
otherwise vanishes. Besides \(A\), three special zero-site potential types
control the support:

\[
 \begin{array}{c|c|c}
 \text{type}&\text{potential}&\text{live incidence}\\ \hline
 P&\lambda&\text{joins every vertex of }A,\\
 R&-\gamma&\text{attaches to the rank-one site},\\
 Q&\gamma&\text{has zero-sum edges to type }R.
 \end{array}                                                     \tag{11}
\]

The inequalities \(\gamma\ne\pm\lambda\) make \(P,R,Q,A\) distinct,
except that \(R=Q\) when \(\gamma=0\).

If \(|A|=3\), there is one envelope. If \(|A|=2\), the leftover zero is
of type \(P\), type \(R\), or neither, giving three envelopes. These types
cannot coincide because \(\lambda+\gamma\ne0\).

Now let \(|A|=1\). Up to swapping the two leftover zero sites, the six
possibilities without a mutual zero-sum edge are

\[
                              PP,\ PO,\ PR,\ OO,\ RO,\ RR,       \tag{12}
\]

where \(O\) denotes an otherwise unattached potential. There are three
additional opposite-pair envelopes:

* an opposite \(O,-O\) pair;
* an \(R,Q\) pair;
* two \(R\) vertices with their mutual edge when \(\gamma=0\).

A type-\(P\) vertex cannot belong to an opposite leftover pair, because its
opposite potential \(-\lambda\) would put the other vertex in \(A\).
This proves the exact census

\[
                              1+3+(6+3)=13.                       \tag{13}
\]

The noncoordinate R2 branch simply omits the nine \(|A|=1\) envelopes;
all its members are already contained in the \(|A|=2,3\) support closures.

## Exact cofactor bounds

A cell column of \(d\Psi_M\) obtained by varying edge \(e\) is zero unless
the support on the four complementary vertices admits a perfect matching
with the required local colours. Enumerating all edge choices and binary
words gives

\[
\begin{array}{c|c|c}
|A|&\text{complement pattern}&\text{potentially active cell columns}\\ \hline
3&-&24\\
2&P&44\\
2&R&32\\
2&O&12\\ \hline
1&PP&28\\
1&PO&16\\
1&PR&32\\
1&OO&4\\
1&RQ\text{ edge}&36\\
1&OO\text{ opposite edge}&24\\
1&RO&16\\
1&RR&28\\
1&RR\text{ with }\gamma=0&48.
\end{array}                                                       \tag{14}
\]

The count is cell-specific: the two invertible-to-rank-one blocks use one
shore column, while every zero-multiplier block is arbitrary. Every
unlisted differential column is identically zero, so (14) directly implies

\[
                              \operatorname{rank}d\Psi_M\le48,  \tag{15}
\]

proving (4). Degenerate packets lie in the same support closures.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_one_rank_one_three_zero_equal_invertible_potential_closure.py](../computations/verify_level_two_two_invertible_one_rank_one_three_zero_equal_invertible_potential_closure.py)
verifies the physical R2 thresholds, all thirteen potential representatives,
the \(1+3+9\) support classification, inequivalence of the support graphs,
and every local-colour complementary cofactor. It records the exact active
counts in (14) and modular calibration ranks

\[
                              24,34,27,12,23,14,27,4,29,17,16,27,40
\]

over two prime fields. It passes normal, optimized, and isolated Python.
