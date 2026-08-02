# Linear L0 excludes the exact \(1I+5Z\) rank-\(55\) guard

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

The exact residual packet from the
[\(1I+5Z\) generic-kernel/R2 guard](level-two-one-invertible-five-zero-r2-guard.md)
has no completion to the full eight-site equations. Its binary matching
differential \(D=d\Psi_M\) has the exact ranks

\[
\begin{array}{c|c}
\text{matrix}&\operatorname{rank}
  \text{ over }\mathbb Q,\mathbb F_{101},\mathbb F_{1000003}\\ \hline
D&(55,55,55)\\
D_{\rm mixed}&(55,55,55)\\
[D\mid e_{0^6}]&(56,56,56)\\
[D\mid e_{1^6}]&(56,56,56)\\
[D\mid e_{0^6}\mid e_{1^6}]&(57,57,57).
\end{array}                                                     \tag{1}
\]

Thus neither pure binary target \(e_{0^6}\) nor \(e_{1^6}\) lies in
\(\operatorname{im}D\), and their two cokernel classes are independent.
Linear L0 pure-target incidence already contradicts any full completion,
so no factored-L0 or overlapping-L1 calculation is needed for this fixed
packet.

This is packet-specific. It does not close the full \(1I+5Z\) endpoint
stratum, the all-zero-potential component, or any other residual \(M\).
It does not retract the earlier selected-block guard: that packet still
satisfies the generic-kernel identities, the selected level-two equations,
and the six selected residual R2 alternatives exactly. The new result says
only that it cannot satisfy the additional L0 rows of a full source.

## Universal binary endpoint-slice identity

Let \(p,q\) be the two endpoint sites and retain the fixed six-site binary
packet \(M\). For endpoint colours \(s,t\), write \(W_{st}\) for the direct
endpoint cell and let \(U_r^s,V_r^t\) denote the two endpoint-star rows.
Partitioning the \(105\) perfect matchings of eight sites according to
whether they contain \(pq\) gives \(15+90\) terms and the exact identity

\[
 T_{st}
   =W_{st}\Psi(M)+d\Psi_M(N^{st}),                              \tag{2}
\]

where

\[
 N^{st}_{ru}
   =U_r^s(V_u^t)^{\mathsf T}
      +V_r^t(U_u^s)^{\mathsf T}.                               \tag{3}
\]

Euler's identity for the degree-three residual matching tensor is

\[
                              d\Psi_M(M)=3\Psi(M).              \tag{4}
\]

Over characteristic zero, (2)--(4) imply

\[
                              T_{st}\in\operatorname{im}D       \tag{5}
\]

for every endpoint completion and every binary endpoint slice. This
conclusion allows arbitrary endpoint stars and a direct endpoint cell; it
does not set any unlisted ternary cell to zero.

For the GHZ target, the two pure L0 slices are precisely
\(e_{0^6}\) and \(e_{1^6}\). Therefore their membership in
\(\operatorname{im}D\) is a necessary condition for a full source. The
last three rows of (1) show that the exact guard violates both necessary
memberships independently.

## Why outside cells cannot repair the packet

The differential image in (5) depends only on the \(60\) scalar cells of
the fixed residual binary packet \(M\). An arbitrary ternary eight-site
edge system has

\[
                  \binom82\cdot3^2=252
\]

scalar cells, leaving \(252-60=192\) cells outside \(M\). These cells may
change \(W_{st}\) and the factored tangent \(N^{st}\), but (2) still places
their entire contribution inside the same image \(\operatorname{im}D\).
They cannot change either augmented rank in (1).

The mixed-row rank in (1) supplies an equivalent diagnostic. Removing the
two pure output rows leaves the full rank \(55\), whereas admitting the two
independent pure targets would require those two cokernel directions to
vanish. The direct augmented-rank test is already conclusive.

## Relation to the endpoint-rank frontier

The earlier guard isolated the reason generic-kernel plus selected R2 is
too weak on the all-zero-potential \(1I+5Z\) component: with only one
nonzero endpoint matrix, the generic-kernel equation is \(0=0\) on every
residual edge and permits an arbitrary \(M\). The present calculation shows
that the first explicit rank-\(55\) choice of \(M\) does not survive L0.

This does not imply that every rank-\(55\) residual packet on that component
fails the same incidence test. A stratum-wide continuation must either
prove that no generic-kernel-compatible \(M\) can contain both pure targets
in its tangent image, or classify the incidence survivors and then impose
their factored endpoint-star or overlap equations.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_five_zero_l0_obstruction.py](../computations/verify_level_two_one_invertible_five_zero_l0_obstruction.py)

* reconstructs and reaudits the exact endpoint ranks
  \((2,0,0,0,0,0)\), all \(60\) generic-kernel identities, all \(64\)
  selected rows, differential rank \(55\), and the six selected residual
  R2 alternatives;
* rebinds the \(15+90\) formal matching-partition identity to this packet
  and checks all \(4\cdot64=256\) endpoint slices;
* verifies Euler's identity and every rank in (1) over the rationals and
  two prime fields; and
* audits the \(60/192\) residual/outside cell scope.

It passes normal, optimized, and isolated Python.
