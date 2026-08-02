# The six-zero endpoint chart reaches separate factored pure L0 slices

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

The zero-potential endpoint-rank pattern

\[
                         X_0=\cdots=X_5=0                       \tag{1}
\]

contains an exact residual packet \(M\) with

\[
 \operatorname{rank}d\Psi_M=55,\qquad
 \operatorname{rank}(d\Psi_M)_{\rm mixed}=53,                 \tag{2}
\]

all generic-kernel and selected level-two rows, and residual R2 at all six
roots. The same packet has two separate literal endpoint-star assignments:

\[
 (T_{00},T_{01},T_{10},T_{11})=(e_{0^6},0,0,0),               \tag{3}
\]

and

\[
 (T_{00},T_{01},T_{10},T_{11})=(0,0,0,e_{1^6}).               \tag{4}
\]

Thus the all-zero endpoint chart is not closed by differential rank,
linear incidence, residual R2, or either factored pure slice separately.
The assignments in (3) and (4) are different. This is not a simultaneous
four-slice completion, and Krenn's conjecture is not resolved.

## Exact rebinding

Retain the integral SHARP_M packet and binary endpoint stars from the
[\(1I+5Z\) factored-pure boundary](level-two-one-invertible-five-zero-factored-pure-slice-boundary.md),
but replace its selected data by

\[
                         X_r=0,\qquad \nu_r=0
                         \quad(0\le r<6).                       \tag{5}
\]

Every generic-kernel scalar is \(0=0\). The selected tangent and direct
value also vanish, so all 64 selected rows are zero. The residual packet is
unchanged, hence so are the exact rational and three-prime incidence ranks

\[
\begin{array}{c|c}
\text{matrix}&\text{rank over all four fields}\\ \hline
D&55\\
D_{\rm mixed}&53\\
[D\mid e_{0^6}]&55\\
[D\mid e_{1^6}]&55\\
[D\mid e_{0^6}\mid e_{1^6}]&55.
\end{array}                                                     \tag{6}
\]

The two factored constructions use only binary endpoint rows:
\(U_0^0=V_1^0=e_0\) for (3), and
\(U_4^1=V_5^1=e_1\) for (4). They therefore survive the selected rebinding
unchanged. A direct sum over all 105 eight-site matchings verifies all 256
binary slices for each assignment. The selected rare/rare slice is zero
because every rare endpoint column in (5) vanishes.

At every residual root, all incident selected rare columns vanish.
Consequently each root satisfies the R2 preservation alternative; no
physical pure-column claim is transported through a basis change.

## Remaining obstruction

The committed
[sharp-factor obstruction](level-two-l0-sharp-factor-obstruction.md)
is a theorem about this same residual \(M\) and its binary endpoint-star
equations. Its unit-ideal certificate excludes a single shared assignment
realizing both pure targets and both mixed zeros. Hence the exact packet
reaches the two individual factored faces (3)--(4), but not their
intersection.

This packet-specific failure does not close the full six-zero endpoint
stratum. It identifies simultaneous four-slice compatibility as the next
necessary condition even at endpoint rank zero.

## Exact audit

The standard-library checker
[verify_level_two_zero_invertible_six_zero_factored_pure_slice_boundary.py](../computations/verify_level_two_zero_invertible_six_zero_factored_pure_slice_boundary.py)

- imports the sharp residual packet, its rank-\(55/53\) incidence and
  five-dimensional gauge kernel;
- verifies endpoint ranks \((0,0,0,0,0,0)\), all 60 generic-kernel
  scalars, and all 64 selected rows;
- reruns both literal 256-slice factored endpoint-star audits after the
  all-zero selected rebinding;
- checks R2 preservation at all six residual roots; and
- pins the four residual blocks used by the simultaneous unit-ideal
  obstruction.

It passes normal, optimized, and isolated Python.
