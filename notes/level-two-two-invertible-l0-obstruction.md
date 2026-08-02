# L0 tangent incidence excludes the displayed two-invertible guard

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

The exact \(2I+2R+2Z\) packet from
[the two-invertible R2 guard](level-two-two-invertible-r2-guard.md) has no
completion to the full eight-site equations. Its six-site differential
\(D=d\Psi_M\) satisfies

\[
\begin{array}{c|c}
\text{matrix}&\text{rank over }\mathbb Q,\mathbb F_{101},
                         \mathbb F_{1000003}\\ \hline
D&(55,55,55)\\
D_{\rm mixed}&(55,55,55)\\
[D\mid e_{0^6}]&(56,56,56)\\
[D\mid e_{1^6}]&(56,56,56)\\
[D\mid e_{0^6}\mid e_{1^6}]&(57,57,57).
\end{array}
\]

For every binary endpoint completion, the \(15+90\) matching partition and
Euler's identity give

\[
 T_{st}=W_{st}\Psi(M)+D(N^{st})\in\operatorname{im}D.
\]

The two pure L0 target slices are \(e_{0^6}\) and \(e_{1^6}\), so both must
belong to \(\operatorname{im}D\). The displayed ranks show that neither
does, and their cokernel classes are independent. Equivalently, a rank-55
packet in a full solution must have mixed-row rank 53, not 55.

This obstruction depends only on the 60 residual binary cells. No choice of
the other 192 ternary edge cells can repair the displayed packet.

The generic-kernel parameters of the guard are

\[
 2\nu=(1,1,1,1,-1,-1).
\]

Once \(X\) and these multipliers are fixed, six positive-multiplier blocks

\[
 01,\ 02,\ 03,\ 12,\ 13,\ 23
\]

are determined by \(X_uJX_v^{\mathsf T}\), and \(45\) is forced to zero.
The only residual freedom lies in the eight zero-multiplier blocks

\[
 \boxed{04,\ 05,\ 14,\ 15,\ 24,\ 25,\ 34,\ 35.}
\]

Therefore any replacement in the same endpoint-matrix/multiplier normal
form must alter at least one of these 32 scalar cells and land on the exact
incidence locus

\[
 \operatorname{rank}[D\mid e_{0^6}\mid e_{1^6}]
 =\operatorname{rank}D,
\qquad
 \operatorname{rank}D_{\rm mixed}=\operatorname{rank}D-2.
\]

This does not exclude the full two-invertible stratum: different choices of
the eight free blocks may change the tangent image. Factored L0 tests are
unnecessary for this exact guard because it already fails the linear screen.

The standard-library checker
[verify_level_two_two_invertible_l0_obstruction.py](../computations/verify_level_two_two_invertible_l0_obstruction.py)
composes the universal formal 256-slice matching identity, verifies Euler,
all five rank triples, and the exact eight-block freedom. It passes normal,
optimized, and isolated Python.

