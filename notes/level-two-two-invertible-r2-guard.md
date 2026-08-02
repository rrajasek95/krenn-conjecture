# A rank-55 two-invertible guard survives the generic kernel and R2

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

There is an exact binary residual packet with endpoint-matrix ranks

\[
                              (2,2,1,1,0,0)
\]

which simultaneously satisfies:

* the generic-kernel equations
  \[
  X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv};
  \]
* all 64 selected level-two equations;
* \(\operatorname{rank}d\Psi_M=55\), with kernel exactly the five vertex
  gauges; and
* literal R2 exits at all six residual roots.

Thus no unconditional differential-rank drop is possible for the stratum
with exactly two invertible endpoint matrices. This is a selected-block/R2
guard, not a full eight-site solution; L0/L1 and overlapping level-two
equations are not asserted.

Take \(J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\),
\(\rho=2\nu=(1,1,1,1,-1,-1)\), and

\[
 X_0=X_1=I,\quad
 X_2=\begin{pmatrix}1&2\\0&0\end{pmatrix},\quad
 X_3=\begin{pmatrix}2&5\\0&0\end{pmatrix},\quad
 X_4=X_5=0.
\]

On the positive-multiplier edges put
\(M_{uv}=X_uJX_v^{\mathsf T}\). The eight edges from
\(\{0,1,2,3\}\) to \(\{4,5\}\) have zero multiplier and are free; the
checker records a small integral choice. Four of them are pure in output
column one:

\[
                         04,\quad14,\quad24,\quad35.
\]

Together with the pure-column-zero blocks \(02,12,23,32\), respectively,
these give two distinct internal R2 witnesses at roots \(0,1,2,3\).
At roots \(4,5\), the selected endpoint stars vanish, and binary endpoint
blocks with zero outside column provide the standard pure-zero/pure-one
completion.

The exact audit is
[verify_level_two_two_invertible_r2_guard.py](../computations/verify_level_two_two_invertible_r2_guard.py).
It verifies all 60 scalar generic-kernel identities, all 64 selected rows,
the rational and two modular differential ranks, the five-dimensional
gauge kernel, and the six R2 witness tables. It passes normal, optimized,
and isolated Python.
